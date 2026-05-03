#!/usr/bin/env python3
"""
从 arXiv API 提取论文信息并下载 PDF 文件。

Usage:
    python3 arxiv-ext.py <arxiv_id> [--output_dir /path/to/dir]

Example:
    python3 arxiv-ext.py 1512.04442
    python3 arxiv-ext.py 1512.04442 --output_dir /tmp/arxiv_out
"""

import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import json
import os
import sys
import argparse
import re


def get_arxiv_info(arxiv_id):
    """从 arXiv API 获取论文信息。"""
    url = f'https://export.arxiv.org/api/query?id_list={arxiv_id}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req, timeout=15)
    except urllib.error.HTTPError as e:
        raise ValueError(f"arXiv API 请求失败 (HTTP {e.code}): {e.reason}")
    except urllib.error.URLError as e:
        raise ValueError(f"arXiv API 连接失败: {e.reason}")
    xml_data = response.read().decode('utf-8')

    root = ET.fromstring(xml_data)
    ns = {'atom': 'http://www.w3.org/2005/Atom',
          'arxiv': 'http://arxiv.org/schemas/atom'}

    entry = root.find('atom:entry', ns)
    if entry is None:
        raise ValueError(f"No entry found for arXiv ID: {arxiv_id}")

    # 基本信息 (安全检查: 元素可能缺失)
    published_elem = entry.find('atom:published', ns)
    published = published_elem.text if published_elem is not None else ''
    updated_elem = entry.find('atom:updated', ns)
    updated = updated_elem.text if updated_elem is not None else ''
    title_elem = entry.find('atom:title', ns)
    title = title_elem.text.strip() if title_elem is not None else ''
    summary_elem = entry.find('atom:summary', ns)
    summary = summary_elem.text.strip() if summary_elem is not None else ''

    # 作者
    authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]

    # PDF 链接和 ID URL
    pdf_link = None
    id_url = entry.find('atom:id', ns).text  # e.g. "http://arxiv.org/abs/1512.04442v1"
    
    for link in entry.findall('atom:link', ns):
        if link.get('title') == 'pdf':
            pdf_link = link.get('href')
            break

    # 从 id_url 提取带版本号的 arxiv_id
    # id_url 格式: "http://arxiv.org/abs/1512.04442v1"
    version_match = re.search(r'abs/(\d+\.\d+)(v\d+)?', id_url)
    if version_match:
        base_id = version_match.group(1)
        version = version_match.group(2) or ''
        arxiv_id_with_version = f"{base_id}{version}"
    else:
        arxiv_id_with_version = arxiv_id

    # 分类
    categories = [c.get('term') for c in entry.findall('atom:category', ns)]

    # 备注
    comment_elem = entry.find('arxiv:comment', ns)
    comment = comment_elem.text if comment_elem is not None else ''

    # 期刊引用
    journal_ref_elem = entry.find('arxiv:journal_ref', ns)
    journal_ref = journal_ref_elem.text if journal_ref_elem is not None else ''

    # DOI
    doi_elem = entry.find('arxiv:doi', ns)
    doi = doi_elem.text if doi_elem is not None else ''

    return {
        'arxiv_id': arxiv_id,
        'arxiv_id_with_version': arxiv_id_with_version,
        'id_url': id_url,              # arXiv 唯一标识 URL (含版本号)
        'published': published,          # e.g. "2015-12-14T16:00:00Z"
        'updated': updated,
        'title': title,
        'abstract': summary,
        'authors': authors,
        'author_str': f"{authors[0]} and others" if len(authors) > 1 else (authors[0] if authors else ''),
        'pdf_url': pdf_link,
        'abs_url': f'https://arxiv.org/abs/{arxiv_id}',
        # Markdown 链接 (用于 JSON 文件)
        'arxiv_link': f'[{arxiv_id_with_version}](https://arxiv.org/pdf/{arxiv_id})',
        'categories': categories,
        'primary_category': categories[0] if categories else '',
        'comment': comment,
        'journal_ref': journal_ref,
        'doi': doi,
        'time': published[:10].replace('-', '.'),  # YYYY.MM.DD
    }


def download_pdf(arxiv_id, output_dir):
    """下载 PDF 文件到指定目录。"""
    os.makedirs(output_dir, exist_ok=True)
    pdf_url = f'https://arxiv.org/pdf/{arxiv_id}'
    pdf_path = os.path.join(output_dir, f'{arxiv_id}.pdf')

    req = urllib.request.Request(pdf_url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req, timeout=30)
    with open(pdf_path, 'wb') as f:
        f.write(response.read())

    return pdf_path


def main():
    parser = argparse.ArgumentParser(description='提取 arXiv 论文信息并下载 PDF')
    parser.add_argument('arxiv_id', help='arXiv ID (如 1512.04442)')
    parser.add_argument('--output_dir', '-o', default='.', help='输出目录')
    parser.add_argument('--no-pdf', action='store_true', help='不下载 PDF')
    args = parser.parse_args()

    print(f"Fetching arXiv info for: {args.arxiv_id}")
    info = get_arxiv_info(args.arxiv_id)

    # 打印结果
    print(f"\nTitle: {info['title']}")
    print(f"Authors: {info['author_str']}")
    print(f"Published: {info['published']}")
    print(f"Time (v1): {info['time']}")
    print(f"arXiv ID (with version): {info['arxiv_id_with_version']}")
    print(f"Categories: {', '.join(info['categories'])}")
    if info['journal_ref']:
        print(f"Journal: {info['journal_ref']}")
    if info['doi']:
        print(f"DOI: {info['doi']}")
    if info['comment']:
        print(f"Comment: {info['comment']}")
    print(f"\nPDF URL: {info['pdf_url']}")
    print(f"Abstract URL: {info['abs_url']}")

    # 输出 JSON
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, f'{args.arxiv_id}_arxiv.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=4, ensure_ascii=False)
    print(f"\nJSON saved to: {json_path}")

    # 下载 PDF
    if not args.no_pdf:
        print(f"\nDownloading PDF...")
        pdf_path = download_pdf(args.arxiv_id, output_dir)
        print(f"PDF saved to: {pdf_path}")


if __name__ == '__main__':
    main()
