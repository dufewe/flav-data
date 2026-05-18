#!/usr/bin/env python3
"""
Extract detailed paper information from the InspireHEP API.

Usage:
    python3 inspirehep-ext.py <arxiv_id> [--output_dir /path/to/dir]
    python3 inspirehep-ext.py --recid <recid>

Example:
    python3 inspirehep-ext.py 1512.04442
    python3 inspirehep-ext.py --recid 1409497
"""

import urllib.request
import urllib.error
import json
import os
import sys
import argparse


def get_inspire_by_arxiv(arxiv_id):
    """Query InspireHEP by arXiv ID."""
    url = f'https://inspirehep.net/api/literature?q=eprint:{arxiv_id}'
    req = urllib.request.Request(url, headers={'Accept': 'application/json'})
    try:
        response = urllib.request.urlopen(req, timeout=15)
    except urllib.error.HTTPError as e:
        raise ValueError(f"InspireHEP API request failed (HTTP {e.code}): {e.reason}")
    except urllib.error.URLError as e:
        raise ValueError(f"InspireHEP API connection failed: {e.reason}")
    data = json.loads(response.read().decode('utf-8'))

    if not data.get('hits', {}).get('hits'):
        raise ValueError(f"No InspireHEP entry found for arXiv: {arxiv_id}")

    return data['hits']['hits'][0]


def get_inspire_by_recid(recid):
    """Query InspireHEP directly by control number."""
    url = f'https://inspirehep.net/api/literature/{recid}'
    req = urllib.request.Request(url, headers={'Accept': 'application/json'})
    try:
        response = urllib.request.urlopen(req, timeout=15)
    except urllib.error.HTTPError as e:
        raise ValueError(f"InspireHEP API request failed (HTTP {e.code}): {e.reason}")
    except urllib.error.URLError as e:
        raise ValueError(f"InspireHEP API connection failed: {e.reason}")
    data = json.loads(response.read().decode('utf-8'))

    return data


def extract_metadata(hit):
    """Extract structured metadata from an InspireHEP hit."""
    # Handle direct query (no hits wrapper) and search query
    if 'metadata' in hit:
        meta = hit['metadata']
        recid = hit.get('id', meta.get('control_number', ''))
    else:
        meta = hit
        recid = meta.get('control_number', '')

    # TexKey (prefer the first one)
    texkeys = meta.get('texkeys', [''])
    texkey = texkeys[0] if texkeys else ''

    # Title (prefer arXiv source, preserves full LaTeX)
    title = ''
    for t in meta.get('titles', []):
        if t.get('source') == 'arXiv':
            title = t['title']
            break
    if not title:
        title = meta.get('titles', [{}])[0].get('title', '')

    # Abstract (prefer arXiv source, preserves LaTeX format)
    abstract = ''
    for a in meta.get('abstracts', []):
        if a.get('source') == 'arXiv':
            abstract = a['value']
            break
    if not abstract:
        abstract = meta.get('abstracts', [{}])[0].get('value', '')

    # Author list
    authors = meta.get('authors', [])
    author_list = [a.get('full_name', '') for a in authors]
    if len(author_list) > 1:
        author_str = f"{author_list[0]} and others"
    elif author_list:
        author_str = author_list[0]
    else:
        # If no person name found, use collaboration name
        collaborations = meta.get('collaborations', [])
        if collaborations:
            author_str = f"{collaborations[0]['value']} collaboration"
        else:
            author_str = ''

    # First author full info (includes email, etc.)
    first_author = meta.get('first_author', {})

    # Collaboration
    collaborations = meta.get('collaborations', [])
    collaboration = collaborations[0]['value'] if collaborations else ''

    # Date (use preprint_date = arXiv v1 submission date)
    preprint_date = meta.get('preprint_date', '')
    time_str = preprint_date.replace('-', '.') if preprint_date else ''

    # arXiv info
    eprints = meta.get('arxiv_eprints', [{}])
    arxiv_id = eprints[0].get('value', '') if eprints else ''
    arxiv_categories = eprints[0].get('categories', []) if eprints else []

    # Publication info
    pub_info = (
        meta.get('publication_info', [{}])[0]
        if meta.get('publication_info') else {}
    )
    journal = pub_info.get('journal_title', '')
    journal_year = pub_info.get('year', '')
    journal_volume = pub_info.get('journal_volume', '')
    journal_issue = pub_info.get('journal_issue', '')
    artid = pub_info.get('artid', '')

    # DOI
    dois = meta.get('dois', [])
    doi = dois[0]['value'] if dois else ''

    # Keywords
    keywords = [k.get('value', '') for k in meta.get('keywords', [])]

    # Citation stats
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
        'journal_year': str(journal_year) if journal_year is not None else '',
        'journal_volume': str(journal_volume) if journal_volume is not None else '',
        'journal_issue': str(journal_issue) if journal_issue is not None else '',
        'artid': str(artid) if artid is not None else '',
        'doi': doi,
        'keywords': keywords,
        'citation_count': citation_count,
        'citation_without_self': citation_without_self,
        # Markdown links (for JSON files)
        # NOTE: arxiv_link is a simplified link — the full 'arxiv' JSON field
        # requires primary_category and version, obtainable from arxiv-ext.py.
        'inspire_hep_link': f'[{texkey}](https://inspirehep.net/literature/{recid})',
        'arxiv_link': f'[{arxiv_id}](https://arxiv.org/pdf/{arxiv_id})',
        'pdf_url': f'https://arxiv.org/pdf/{arxiv_id}',
    }


def main():
    parser = argparse.ArgumentParser(
        description='Extract InspireHEP paper information'
    )
    parser.add_argument('arxiv_id', nargs='?', help='arXiv ID')
    parser.add_argument('--recid', help='InspireHEP control number')
    parser.add_argument('--output_dir', '-o', default='.', help='Output directory')
    args = parser.parse_args()

    if not args.arxiv_id and not args.recid:
        parser.error("Either arxiv_id or --recid is required")

    # Fetch data
    if args.recid:
        print(f"Fetching InspireHEP record: {args.recid}")
        hit = get_inspire_by_recid(args.recid)
    else:
        print(f"Searching InspireHEP for arXiv: {args.arxiv_id}")
        hit = get_inspire_by_arxiv(args.arxiv_id)

    # Extract metadata
    info = extract_metadata(hit)

    # Print summary
    print(f"\nTexKey: {info['texkey']}")
    print(f"RecID: {info['recid']}")
    print(f"Title: {info['title']}")
    print(f"Author: {info['author_str']}")
    print(f"Collaboration: {info['collaboration']}")
    print(f"Time: {info['time']}")
    print(
        f"Journal: {info['journal']} {info['journal_volume']} "
        f"({info['journal_year']})"
    )
    if info['doi']:
        print(f"DOI: {info['doi']}")
    print(
        f"Citations: {info['citation_count']} "
        f"(w/o self: {info['citation_without_self']})"
    )
    print(f"\nInspire Link: {info['inspire_hep_link']}")
    print(f"ArXiv Link: {info['arxiv_link']}")

    # Save JSON
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{info['texkey'] or info['recid']}_inspire.json"
    json_path = os.path.join(output_dir, filename)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=4, ensure_ascii=False)
    print(f"\nJSON saved to: {json_path}")


if __name__ == '__main__':
    main()
