#!/usr/bin/env python3
"""
Extract paper information from the arXiv API and download PDF files.

Usage:
    python3 arxiv-ext.py <arxiv_id> [--output_dir /path/to/dir]

Example:
    python3 arxiv-ext.py 1512.04442
    python3 arxiv-ext.py 1512.04442 --output_dir <output_dir>
"""

import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
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
    (e.g. ``"A.M."``, ``"R."``) — each whitespace-separated part is
    1-2 chars followed by a period — return the input unchanged.
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


def get_arxiv_info(arxiv_id):
    """Fetch paper information from the arXiv API."""
    url = f'https://export.arxiv.org/api/query?id_list={arxiv_id}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req, timeout=15)
    except urllib.error.HTTPError as e:
        raise ValueError(f"arXiv API request failed (HTTP {e.code}): {e.reason}")
    except urllib.error.URLError as e:
        raise ValueError(f"arXiv API connection failed: {e.reason}")
    xml_data = response.read().decode('utf-8')

    root = ET.fromstring(xml_data)
    ns = {'atom': 'http://www.w3.org/2005/Atom',
          'arxiv': 'http://arxiv.org/schemas/atom'}

    entry = root.find('atom:entry', ns)
    if entry is None:
        # arXiv returns HTTP 200 even for non-existent IDs; check <total>
        total_elem = root.find('atom:total', ns)
        total = total_elem.text if total_elem is not None else 'unknown'
        raise ValueError(
            f"No entry found for arXiv ID: {arxiv_id} "
            f"(API returned total={total})"
        )

    # Basic info (safe checks: elements may be missing)
    # Apply Unicode -> LaTeX to title/abstract (Test/improve.md rule 4)
    published_elem = entry.find('atom:published', ns)
    published = published_elem.text if published_elem is not None else ''
    updated_elem = entry.find('atom:updated', ns)
    updated = updated_elem.text if updated_elem is not None else ''
    title_elem = entry.find('atom:title', ns)
    title = _unicode_to_latex(title_elem.text.strip()) if title_elem is not None else ''
    summary_elem = entry.find('atom:summary', ns)
    summary = _unicode_to_latex(summary_elem.text.strip()) if summary_elem is not None else ''

    # Authors (full names; convert first to BibTeX form for `author_str`)
    authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]

    # PDF link and ID URL
    pdf_link = None
    id_url = entry.find('atom:id', ns).text  # e.g., "http://arxiv.org/abs/1512.04442v1"

    for link in entry.findall('atom:link', ns):
        if link.get('title') == 'pdf':
            pdf_link = link.get('href')
            break

    # Extract versioned arxiv_id from id_url
    # id_url format: "http://arxiv.org/abs/1512.04442v1"
    version_match = re.search(r'abs/(\d+\.\d+)(v\d+)?', id_url)
    if version_match:
        base_id = version_match.group(1)
        version = version_match.group(2) or ''
        arxiv_id_with_version = f"{base_id}{version}"
    else:
        arxiv_id_with_version = arxiv_id

    # Primary category
    primary_category_elem = entry.find('arxiv:primary_category', ns)
    primary_category = (
        primary_category_elem.get('term', '')
        if primary_category_elem is not None else ''
    )
    if not primary_category:
        categories = [c.get('term') for c in entry.findall('atom:category', ns)]
        primary_category = categories[0] if categories else ''

    # Categories
    categories = [c.get('term') for c in entry.findall('atom:category', ns)]

    # Comments
    comment_elem = entry.find('arxiv:comment', ns)
    comment = comment_elem.text if comment_elem is not None else ''

    # Journal reference
    journal_ref_elem = entry.find('arxiv:journal_ref', ns)
    journal_ref = journal_ref_elem.text if journal_ref_elem is not None else ''

    # DOI
    doi_elem = entry.find('arxiv:doi', ns)
    doi = doi_elem.text if doi_elem is not None else ''

    return {
        'arxiv_id': arxiv_id,
        'arxiv_id_with_version': arxiv_id_with_version,
        'primary_category': primary_category,
        'id_url': id_url,
        'published': published,
        'updated': updated,
        'title': title,
        'abstract': summary,
        'authors': authors,
        # Test/improve.md rule 3: convert full first name to BibTeX initials form
        'author_str': (
            f"{_to_bibtex(authors[0])} and others"
            if len(authors) > 1
            else (_to_bibtex(authors[0]) if authors else '')
        ),
        'pdf_url': pdf_link,
        'abs_url': f'https://arxiv.org/abs/{arxiv_id}',
        # Markdown link for JSON arxiv field
        'arxiv_link': (
            f'[{primary_category}/{arxiv_id_with_version}]'
            f'(https://arxiv.org/pdf/{arxiv_id})'
        ),
        'categories': categories,
        'comment': comment,
        'journal_ref': journal_ref,
        'doi': doi,
        'time': published[:10].replace('-', '.'),  # YYYY.MM.DD
    }


def download_pdf(arxiv_id, output_dir):
    """Download the PDF file to the specified directory."""
    os.makedirs(output_dir, exist_ok=True)
    pdf_url = f'https://arxiv.org/pdf/{arxiv_id}'
    pdf_path = os.path.join(output_dir, f'{arxiv_id}.pdf')

    req = urllib.request.Request(pdf_url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req, timeout=30)
    with open(pdf_path, 'wb') as f:
        f.write(response.read())

    return pdf_path


def main():
    parser = argparse.ArgumentParser(
        description='Extract arXiv paper information and download PDF'
    )
    parser.add_argument('arxiv_id', help='arXiv ID (e.g., 1512.04442)')
    parser.add_argument('--output_dir', '-o', default='.', help='Output directory')
    parser.add_argument('--no-pdf', action='store_true', help='Skip PDF download')
    args = parser.parse_args()

    print(f"Fetching arXiv info for: {args.arxiv_id}")
    info = get_arxiv_info(args.arxiv_id)

    # Print results
    print(f"\nTitle: {info['title']}")
    print(f"Authors: {info['author_str']}")
    print(f"Published: {info['published']}")
    print(f"Time (v1): {info['time']}")
    print(f"Primary category: {info['primary_category']}")
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

    # Save JSON output
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, f'{args.arxiv_id}_arxiv.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=4, ensure_ascii=False)
    print(f"\nJSON saved to: {json_path}")

    # Download PDF
    if not args.no_pdf:
        print(f"\nDownloading PDF...")
        pdf_path = download_pdf(args.arxiv_id, output_dir)
        print(f"PDF saved to: {pdf_path}")


if __name__ == '__main__':
    main()
