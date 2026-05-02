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
import xml.etree.ElementTree as ET
import json
import os
import sys
import argparse
import time


def get_arxiv_info(arxiv_id):
    """从 arXiv API 获取论文信息。"""
    url = f'http://export.arxiv.org/api/query?id_list={arxiv_id}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req, timeout=15)
    xml_data = response.read().decode('utf-8')

    root = ET.fromstring(xml_data)
    ns = {'atom': 'http://www.w3.org/2005/Atom',
          'arxiv': 'http://arxiv.org/schemas/atom'}

    entry = root.find('atom:entry', ns)
    if entry is None:
        raise ValueError(f"No entry found for arXiv ID: {arxiv_id}")

    # 基本信息
    published = entry.find('atom:published', ns).text
    updated = entry.find('atom:updated', ns).text
    title = entry.find('atom:title', ns).text.strip()
    summary = entry.find('atom:summary', ns).text.strip()

    # 作者
    authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]

    # PDF 链接
    pdf_link = None
    for link in entry.findall('atom:link', ns):
        if link.get('title') == 'pdf':
            pdf_link = link.get('href')
            break

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

    # arXiv ID (可能带版本号)
    id_url = entry.find('atom:id', ns).text

    return {
        'arxiv_id': arxiv_id,
        'id_url': id_url,
        'published': published,          # e.g. "2021-11-09T14:42:07Z"
        'updated': updated,
        'title': title,
        'abstract': summary,
        'authors': authors,
        'author_str': f"{authors[0]} and others" if len(authors) > 1 else (authors[0] if authors else ''),
        'pdf_url': pdf_link,
        'abs_url': f'https://arxiv.org/abs/{arxiv_id}',
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
