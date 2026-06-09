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
import re


# Unicode -> LaTeX mapping (see Test/improve.md rule 4). Conservative:
# only the most common HEP / math characters. For exotic chars,
# manual review is required.
_UNICODE_TO_LATEX = {
    # Greek letters (lowercase)
    "\u03b1": r"\alpha", "\u03b2": r"\beta", "\u03b3": r"\gamma",
    "\u03b4": r"\delta", "\u03b5": r"\epsilon", "\u03b6": r"\zeta",
    "\u03b7": r"\eta", "\u03b8": r"\theta", "\u03b9": r"\iota",
    "\u03ba": r"\kappa", "\u03bb": r"\lambda", "\u03bc": r"\mu",
    "\u03bd": r"\nu", "\u03be": r"\xi", "\u03c0": r"\pi",
    "\u03c1": r"\rho", "\u03c3": r"\sigma", "\u03c4": r"\tau",
    "\u03c5": r"\upsilon", "\u03c6": r"\phi", "\u03c7": r"\chi",
    "\u03c8": r"\psi", "\u03c9": r"\omega",
    # Greek letters (uppercase)
    "\u0393": r"\Gamma", "\u0394": r"\Delta", "\u0398": r"\Theta",
    "\u039b": r"\Lambda", "\u039e": r"\Xi", "\u03a0": r"\Pi",
    "\u03a3": r"\Sigma", "\u03a5": r"\Upsilon", "\u03a6": r"\Phi",
    "\u03a8": r"\Psi", "\u03a9": r"\Omega",
    # Common math symbols
    "\u00b1": r"\pm", "\u2213": r"\mp", "\u00d7": r"\times",
    "\u00f7": r"\div", "\u221e": r"\infty", "\u2202": r"\partial",
    "\u2207": r"\nabla", "\u2208": r"\in", "\u2200": r"\forall",
    "\u2203": r"\exists", "\u2229": r"\cap", "\u222a": r"\cup",
    "\u2264": r"\leq", "\u2265": r"\geq", "\u2260": r"\neq",
    "\u2248": r"\approx", "\u2261": r"\equiv", "\u2192": r"\to",
    "\u2190": r"\leftarrow", "\u21d2": r"\Rightarrow", "\u21d0": r"\Leftarrow",
    # Common typographic
    "\u2013": r"--",      # en-dash
    "\u2014": r"---",     # em-dash
    "\u2018": r"`",       # left single quote
    "\u2019": r"'",       # right single quote
    "\u201c": r"``",      # left double quote
    "\u201d": r"''",      # right double quote
    "\u00b0": r"^{\circ}",  # degree
    "\u00a0": r"~",       # non-breaking space
}
_UNICODE_RE = re.compile("|".join(re.escape(k) for k in _UNICODE_TO_LATEX.keys()))


def _unicode_to_latex(text):
    """Replace Unicode chars with LaTeX equivalents (Test/improve.md rule 4)."""
    if not text:
        return text
    return _UNICODE_RE.sub(lambda m: _UNICODE_TO_LATEX[m.group(0)], text)


def _to_bibtex(full_name):
    """Convert 'Surname, Full First Name' -> 'Surname, F.' (InspireHEP BibTeX form).

    Per Test/improve.md rule 3, the ``author`` JSON field uses the
    InspireHEP BibTeX format (initials only), not the full first name
    form returned by the arXiv / InspireHEP API.

    Pass-through case: if the given name is already in initials form
    (e.g. ``"A.M."``, ``"R."``) — return the input unchanged.
    """
    if not full_name or ',' not in full_name:
        return full_name
    surname, given = full_name.rsplit(',', 1)
    surname = surname.strip()
    given = given.strip()
    if not given:
        return surname
    parts = re.split(r'[\s\-]+', given)
    # Pass through if all parts are already initials (one or more
    # capital-letter-then-period, e.g. "R.", "A.M.", "J.R.R.")
    if all(re.fullmatch(r'([A-Z]\.)+', p) for p in parts if p):
        return full_name
    initials = '.'.join(p[0].upper() for p in parts if p) + '.'
    return f"{surname}, {initials}"


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

    # Title (prefer arXiv source, preserves full LaTeX).
    # Apply Unicode -> LaTeX per Test/improve.md rule 4.
    title = ''
    for t in meta.get('titles', []):
        if t.get('source') == 'arXiv':
            title = _unicode_to_latex(t['title'])
            break
    if not title:
        title = _unicode_to_latex(meta.get('titles', [{}])[0].get('title', ''))

    # Abstract (prefer arXiv source, preserves LaTeX format).
    # Apply Unicode -> LaTeX per Test/improve.md rule 4.
    abstract = ''
    for a in meta.get('abstracts', []):
        if a.get('source') == 'arXiv':
            abstract = _unicode_to_latex(a['value'])
            break
    if not abstract:
        abstract = _unicode_to_latex(meta.get('abstracts', [{}])[0].get('value', ''))

    # Author list. Convert first author to InspireHEP BibTeX form
    # (initials only) per Test/improve.md rule 3.
    authors = meta.get('authors', [])
    author_list = [a.get('full_name', '') for a in authors]
    if len(author_list) > 1:
        author_str = f"{_to_bibtex(author_list[0])} and others"
    elif author_list:
        author_str = _to_bibtex(author_list[0])
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
