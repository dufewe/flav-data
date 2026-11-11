#!/usr/bin/env python3
"""
Extract paper information from the arXiv API and download PDF files.

Usage:
    python3 arxiv-ext.py <arxiv_id> [--output_dir /path/to/dir] [--no-pdf] [--source]

Example:
    python3 arxiv-ext.py 1512.04442
    python3 arxiv-ext.py 1512.04442 --output_dir /tmp/dl --no-pdf
    python3 arxiv-ext.py 1512.04442 --source -o /tmp/dl
"""

import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import gzip
import json
import os
import shutil
import sys
import tarfile
import argparse
import re
from pathlib import Path

# Shared helpers (Unicode -> LaTeX mapping, BibTeX name conversion).
# See common.py for the canonical implementations and SKILL.md
# "Core Conventions" rules 3 + 4 for the policies.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (
    unicode_to_latex, unicode_to_latex as _unicode_to_latex,
    to_bibtex, to_bibtex as _to_bibtex,
    format_authors, arxiv_name_to_bibtex,
)  # noqa: E402,F401

# Candidate machine-readable data files in an arXiv e-print package.
_DATA_SUFFIXES = ('.dat', '.txt', '.csv', '.tsv', '.json', '.yaml', '.yml')


def get_arxiv_info(arxiv_id: str) -> dict:
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
    # Apply Unicode -> LaTeX to title/abstract (rule 4 of SKILL.md "Core Conventions")
    published_elem = entry.find('atom:published', ns)
    published = published_elem.text if published_elem is not None else ''
    updated_elem = entry.find('atom:updated', ns)
    updated = updated_elem.text if updated_elem is not None else ''
    title_elem = entry.find('atom:title', ns)
    title = _unicode_to_latex(title_elem.text.strip()) if title_elem is not None else ''
    summary_elem = entry.find('atom:summary', ns)
    summary = _unicode_to_latex(summary_elem.text.strip()) if summary_elem is not None else ''

    # Authors (full names; convert first to BibTeX form for `author_str`).
    # Strip XML whitespace: arXiv payloads for collaboration papers wrap
    # the author text in whitespace, which leaks into the final author_str
    # and breaks the "Surname and others" rendering.
    authors: list[str] = []
    for a in entry.findall('atom:author', ns):
        name_elem = a.find('atom:name', ns)
        if name_elem is None or name_elem.text is None:
            continue
        name = name_elem.text.strip()
        if name:
            authors.append(name)

    # PDF + versioned ID from <atom:id> (e.g. ".../abs/1512.04442v1")
    pdf_link = None
    id_elem = entry.find('atom:id', ns)
    if id_elem is None or not id_elem.text:
        raise ValueError(f"arXiv API entry for {arxiv_id} is missing atom:id")
    id_url = id_elem.text.strip()

    for link in entry.findall('atom:link', ns):
        if link.get('title') == 'pdf':
            pdf_link = link.get('href')
            break

    # Extract versioned arxiv_id from id_url. Handles new-style
    # ("1512.04442v1") and old-style ("hep-ex/9901001v1") identifiers.
    # id_url format: "http://arxiv.org/abs/<id>[vN]"
    tail_match = re.search(r'/abs/(.+)$', id_url)
    arxiv_id_with_version = tail_match.group(1) if tail_match else arxiv_id

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
        # Rule 3 author tiers (1 / 2 / 3 / 4+), BibTeX initials only.
        # arXiv gives "First Last"; normalise to "Last, First" first.
        'author_str': format_authors([arxiv_name_to_bibtex(a) for a in authors]),
        'pdf_url': pdf_link,
        'abs_url': f'https://arxiv.org/abs/{arxiv_id}',
        # Markdown link for JSON arxiv field. Old-style IDs already
        # contain their category prefix, so do not prepend it twice.
        'arxiv_link': (
            f'[{arxiv_id_with_version}]'
            f'(https://arxiv.org/pdf/{arxiv_id})'
            if '/' in arxiv_id_with_version
            else (
                f'[{primary_category}/{arxiv_id_with_version}]'
                f'(https://arxiv.org/pdf/{arxiv_id})'
                if primary_category
                else f'[{arxiv_id_with_version}]'
                     f'(https://arxiv.org/pdf/{arxiv_id})'
            )
        ),
        'categories': categories,
        'comment': comment,
        'journal_ref': journal_ref,
        'doi': doi,
        'time': published[:10].replace('-', '.'),  # YYYY.MM.DD
    }


def download_pdf(arxiv_id: str, output_dir: str) -> str:
    """Download the arXiv PDF to ``<output_dir>/<arxiv_id>.pdf``.

    Parameters
    ----------
    arxiv_id : str
        arXiv identifier. May be bare (``"1512.04442"``) or
        versioned (``"1512.04442v1"``). The downloaded file is named
        after the full string passed in, including the version
        suffix, so subsequent calls with a different version won't
        collide.
    output_dir : str
        Directory to write the PDF to. Created if it does not exist.

    Returns
    -------
    str
        Absolute path to the saved PDF, e.g.
        ``"/tmp/dl/1512.04442v1.pdf"``.

    Raises
    ------
    urllib.error.URLError
        If the network request fails.
    ValueError
        If the arXiv server returns an HTTP error (via urllib).
    OSError
        If the PDF cannot be written to disk.
    """
    os.makedirs(output_dir, exist_ok=True)
    pdf_url = f'https://arxiv.org/pdf/{arxiv_id}'
    safe_id = arxiv_id.replace('/', '_')
    pdf_path = os.path.join(output_dir, f'{safe_id}.pdf')

    req = urllib.request.Request(pdf_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req, timeout=30)
    except urllib.error.HTTPError as e:
        raise ValueError(
            f"arXiv PDF download failed (HTTP {e.code}): {e.reason}"
        ) from e
    except urllib.error.URLError as e:
        raise ValueError(
            f"arXiv PDF download connection failed: {e.reason}"
        ) from e
    with open(pdf_path, 'wb') as f:
        f.write(response.read())

    return pdf_path


def _safe_extract_tar(archive_path: str, target_dir: str) -> None:
    """Extract a tar archive, rejecting members that escape ``target_dir``."""
    target = os.path.realpath(target_dir)
    with tarfile.open(archive_path) as tar:
        for member in tar.getmembers():
            dest = os.path.realpath(os.path.join(target, member.name))
            if dest != target and not dest.startswith(target + os.sep):
                raise ValueError(
                    f"unsafe path in arXiv source archive: {member.name}"
                )
            if not (member.isfile() or member.isdir()):
                raise ValueError(
                    f"unsupported member in arXiv source archive: {member.name}"
                )
        tar.extractall(target_dir)


def unpack_source(archive_path: str, source_dir: str) -> list[str]:
    """Unpack an arXiv e-print package (tar archive or gzipped single file).

    Returns the extracted files as POSIX paths relative to ``source_dir``.
    """
    os.makedirs(source_dir, exist_ok=True)
    if tarfile.is_tarfile(archive_path):
        _safe_extract_tar(archive_path, source_dir)
    else:
        base = os.path.basename(archive_path)
        if base.endswith('.gz'):
            base = base[:-3]
        if base.endswith('_src'):
            base = base[:-4]
        tex_path = os.path.join(source_dir, f'{base}.tex')
        try:
            with gzip.open(archive_path, 'rb') as src, \
                    open(tex_path, 'wb') as out:
                shutil.copyfileobj(src, out)
        except OSError as e:
            raise ValueError(
                f"unsupported arXiv source package: {archive_path} ({e})"
            ) from e

    root = Path(source_dir)
    return sorted(
        p.relative_to(root).as_posix()
        for p in root.rglob('*') if p.is_file()
    )


def download_source(arxiv_id: str, output_dir: str) -> dict:
    """Download and unpack the arXiv e-print package.

    Ancillary data files (``.dat``/``.txt``/``.csv``/``.json``/``.yaml``) in
    the package are the preferred data source; the paper tables are then used
    to validate their numbers (see ``references/data-source.md`` §4).

    Returns
    -------
    dict
        ``archive_path``, ``source_dir``, ``files`` (relative paths), and
        ``data_files`` (candidate machine-readable data files).
    """
    os.makedirs(output_dir, exist_ok=True)
    safe_id = arxiv_id.replace('/', '_')
    archive_path = os.path.join(output_dir, f'{safe_id}_src')
    source_dir = os.path.join(output_dir, f'{safe_id}_src_files')
    url = f'https://arxiv.org/e-print/{arxiv_id}'

    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=60) as response, \
                open(archive_path, 'wb') as out:
            shutil.copyfileobj(response, out)
    except urllib.error.HTTPError as e:
        raise ValueError(
            f"arXiv source download failed (HTTP {e.code}): {e.reason}"
        ) from e
    except urllib.error.URLError as e:
        raise ValueError(
            f"arXiv source download connection failed: {e.reason}"
        ) from e

    if os.path.exists(source_dir):
        shutil.rmtree(source_dir)
    files = unpack_source(archive_path, source_dir)
    return {
        'archive_path': archive_path,
        'source_dir': source_dir,
        'files': files,
        'data_files': [
            name for name in files
            if name.lower().endswith(_DATA_SUFFIXES)
        ],
    }


def main() -> None:
    """CLI entry point.

    Examples
    --------
    >>> python3 flav-data-importer/scripts/arxiv-ext.py 1512.04442
    >>> python3 flav-data-importer/scripts/arxiv-ext.py 1512.04442 --output_dir /tmp/dl --no-pdf
    >>> python3 flav-data-importer/scripts/arxiv-ext.py 1512.04442 --source -o /tmp/dl
    """
    parser = argparse.ArgumentParser(
        description='Extract arXiv paper information and download PDF'
    )
    parser.add_argument(
        'arxiv_id', help='arXiv ID (e.g., 1512.04442)'
    )
    parser.add_argument(
        '--output_dir', '-o', default=None,
        help='Output directory for JSON dump and PDF. If omitted, no '
             'files are written (only stdout summary). Specify a path '
             '(e.g. /tmp/dl) to enable file output.'
    )
    parser.add_argument(
        '--no-pdf', action='store_true', help='Skip PDF download'
    )
    parser.add_argument(
        '--source', action='store_true',
        help='Download and unpack the arXiv e-print package and list '
             'candidate ancillary data files (needs --output_dir).'
    )
    parser.add_argument(
        '--no-write', dest='no_write', action='store_true',
        help='Skip writing JSON dump and PDF; print summary only.'
    )
    args = parser.parse_args()

    print(f"Fetching arXiv info for: {args.arxiv_id}")
    info = get_arxiv_info(args.arxiv_id)

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

    # Save JSON + download PDF (only when --output_dir is given and not --no-write)
    output_dir = args.output_dir
    if output_dir and not args.no_write:
        os.makedirs(output_dir, exist_ok=True)
        # Old-style IDs contain '/' (e.g. hep-ph/9504235); keep the file
        # inside output_dir instead of creating a subdirectory.
        safe_id = args.arxiv_id.replace('/', '_')
        json_path = os.path.join(output_dir, f'{safe_id}_arxiv.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=4, ensure_ascii=False)
        print(f"\nJSON saved to: {json_path}")

        if not args.no_pdf:
            print(f"\nDownloading PDF...")
            pdf_path = download_pdf(args.arxiv_id, output_dir)
            print(f"PDF saved to: {pdf_path}")

        if args.source:
            print("\nDownloading e-print package...")
            package = download_source(args.arxiv_id, output_dir)
            print(f"Source unpacked to: {package['source_dir']}")
            print(f"Files: {len(package['files'])}")
            if package['data_files']:
                print("Candidate data files:")
                for name in package['data_files']:
                    print(f"  {name}")
            else:
                print("No machine-readable ancillary data files found; "
                      "use the paper tables as the data source.")
    elif args.source:
        print("\nError: --source needs --output_dir/-o to unpack the package.")
    else:
        print("\nNo file written (use --output_dir /path to save JSON + PDF).")


if __name__ == '__main__':
    main()
