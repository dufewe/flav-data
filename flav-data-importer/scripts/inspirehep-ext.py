#!/usr/bin/env python3
"""
从 InspireHEP API 提取论文详细信息。

Usage:
    python3 inspirehep-ext.py <arxiv_id> [--output_dir /path/to/dir]
    python3 inspirehep-ext.py --recid <recid>

Example:
    python3 inspirehep-ext.py 1512.04442
    python3 inspirehep-ext.py --recid 1409497
"""

import urllib.request
import json
import os
import sys
import argparse


def get_inspire_by_arxiv(arxiv_id):
    """按 arXiv ID 查询 InspireHEP。"""
    url = f'https://inspirehep.net/api/literature?q=eprint:{arxiv_id}'
    req = urllib.request.Request(url, headers={'Accept': 'application/json'})
    response = urllib.request.urlopen(req, timeout=15)
    data = json.loads(response.read().decode('utf-8'))

    if not data.get('hits', {}).get('hits'):
        raise ValueError(f"No InspireHEP entry found for arXiv: {arxiv_id}")

    return data['hits']['hits'][0]


def get_inspire_by_recid(recid):
    """按 InspireHEP 控制号直接查询。"""
    url = f'https://inspirehep.net/api/literature/{recid}'
    req = urllib.request.Request(url, headers={'Accept': 'application/json'})
    response = urllib.request.urlopen(req, timeout=15)
    data = json.loads(response.read().decode('utf-8'))

    return data


def extract_metadata(hit):
    """从 InspireHEP hit 提取结构化元数据。"""
    # 处理直接查询 (无 hits 包装) 和搜索查询
    if 'metadata' in hit:
        meta = hit['metadata']
        recid = hit.get('id', meta.get('control_number', ''))
    else:
        meta = hit
        recid = meta.get('control_number', '')

    # TexKey
    texkeys = meta.get('texkeys', [''])
    texkey = texkeys[0] if texkeys else ''

    # 标题 (优先 arXiv 来源)
    title = ''
    for t in meta.get('titles', []):
        if t.get('source') == 'arXiv':
            title = t['title']
            break
    if not title:
        title = meta.get('titles', [{}])[0].get('title', '')

    # 摘要 (优先 arXiv 来源)
    abstract = ''
    for a in meta.get('abstracts', []):
        if a.get('source') == 'arXiv':
            abstract = a['value']
            break
    if not abstract:
        abstract = meta.get('abstracts', [{}])[0].get('value', '')

    # 作者
    authors = meta.get('authors', [])
    author_list = [a.get('full_name', '') for a in authors]
    if len(author_list) > 1:
        author_str = f"{author_list[0]} and others"
    elif author_list:
        author_str = author_list[0]
    else:
        author_str = ''

    # 第一作者完整信息
    first_author = meta.get('first_author', {})

    # 合作组
    collaborations = meta.get('collaborations', [])
    collaboration = collaborations[0].get('value', '') if collaborations else ''

    # 日期
    preprint_date = meta.get('preprint_date', '')
    time_str = preprint_date.replace('-', '.') if preprint_date else ''

    # arXiv 信息
    eprints = meta.get('arxiv_eprints', [{}])
    arxiv_id = eprints[0].get('value', '') if eprints else ''
    arxiv_categories = eprints[0].get('categories', []) if eprints else []

    # 发表信息
    pub_info = meta.get('publication_info', [{}])[0] if meta.get('publication_info') else {}
    journal = pub_info.get('journal_title', '')
    journal_year = pub_info.get('year', '')
    journal_volume = pub_info.get('journal_volume', '')
    journal_issue = pub_info.get('journal_issue', '')
    artid = pub_info.get('artid', '')

    # DOI
    dois = meta.get('dois', [])
    doi = dois[0].get('value', '') if dois else ''

    # 关键词
    keywords = [k.get('value', '') for k in meta.get('keywords', [])]

    # 引用统计
    citation_count = meta.get('citation_count', 0)
    citation_without_self = meta.get('citation_count_without_self_citations', 0)

    return {
        'texkey': texkey,
        'recid': str(recid),
        'title': title,
        'abstract': abstract,
        'authors': author_list,
        'author_str': author_str,
        'collaboration': collaboration,
        'time': time_str,
        'arxiv_id': arxiv_id,
        'arxiv_categories': arxiv_categories,
        'journal': journal,
        'journal_year': str(journal_year),
        'journal_volume': str(journal_volume),
        'journal_issue': str(journal_issue),
        'artid': str(artid),
        'doi': doi,
        'keywords': keywords,
        'citation_count': citation_count,
        'citation_without_self': citation_without_self,
        # 构建的 Markdown 链接
        'inspire_hep_link': f'[{texkey}](https://inspirehep.net/literature/{recid})',
        'arxiv_link': f'[{arxiv_id}](https://arxiv.org/pdf/{arxiv_id})',
        'pdf_url': f'https://arxiv.org/pdf/{arxiv_id}',
    }


def main():
    parser = argparse.ArgumentParser(description='提取 InspireHEP 论文信息')
    parser.add_argument('arxiv_id', nargs='?', help='arXiv ID')
    parser.add_argument('--recid', help='InspireHEP control number')
    parser.add_argument('--output_dir', '-o', default='.', help='输出目录')
    args = parser.parse_args()

    if not args.arxiv_id and not args.recid:
        parser.error("Either arxiv_id or --recid is required")

    # 获取数据
    if args.recid:
        print(f"Fetching InspireHEP record: {args.recid}")
        hit = get_inspire_by_recid(args.recid)
    else:
        print(f"Searching InspireHEP for arXiv: {args.arxiv_id}")
        hit = get_inspire_by_arxiv(args.arxiv_id)

    # 提取元数据
    info = extract_metadata(hit)

    # 打印摘要
    print(f"\nTexKey: {info['texkey']}")
    print(f"RecID: {info['recid']}")
    print(f"Title: {info['title']}")
    print(f"Author: {info['author_str']}")
    print(f"Collaboration: {info['collaboration']}")
    print(f"Time: {info['time']}")
    print(f"Journal: {info['journal']} {info['journal_volume']} ({info['journal_year']})")
    if info['doi']:
        print(f"DOI: {info['doi']}")
    print(f"Citations: {info['citation_count']} (w/o self: {info['citation_without_self']})")
    print(f"\nInspire Link: {info['inspire_hep_link']}")
    print(f"ArXiv Link: {info['arxiv_link']}")

    # 保存 JSON
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{info['texkey'] or info['recid']}_inspire.json"
    json_path = os.path.join(output_dir, filename)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=4, ensure_ascii=False)
    print(f"\nJSON saved to: {json_path}")


if __name__ == '__main__':
    main()
