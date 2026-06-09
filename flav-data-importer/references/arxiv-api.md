# arXiv API Reference

This document describes how to use the arXiv API to extract paper metadata for flav-data JSON files.

## Endpoint

```
https://export.arxiv.org/api/query
```

Returns Atom XML format. Rate-limited; avoid rapid successive requests.

## Query Methods

### By arXiv ID (Most Common)

```bash
curl -sL "https://export.arxiv.org/api/query?id_list=1512.04442"
```

### By Title

```bash
curl -sL "https://export.arxiv.org/api/query?search_query=ti:angular+analysis+cat:hep-ex&max_results=10"
```

### By Author

```bash
curl -sL "https://export.arxiv.org/api/query?search_query=au:Roel_Aaij&max_results=20"
```

## Response Fields

The API returns an Atom XML `<entry>` element. Key fields:

| XML Path | Content | Use in flav-data |
|----------|---------|-----------------|
| `<atom:published>` | v1 submission timestamp (e.g., `2015-12-14T16:00:00Z`) | `time` → `2015.12.14` |
| `<atom:updated>` | Latest version timestamp | Informational only |
| `<atom:title>` | Paper title with LaTeX (e.g., `$B^{0}\to K^{*0}\mu^{+}\mu^{-}$`) | `title` |
| `<atom:summary>` | Paper abstract with LaTeX | `abstract` |
| `<atom:author>` → `<atom:name>` | First author name | `author` → `"FirstAuthor and others"` |
| `<atom:link title="pdf">` → `href` | Direct PDF download URL | `pdf` |
| `<atom:id>` | Unique identifier with version (e.g., `.../abs/1512.04442v1`) | Extract version number |
| `<arxiv:primary_category term="...">` | Primary arXiv category | `arxiv` field prefix |
| `<atom:category term="...">` | All categories | Classification info |
| `<arxiv:comment>` | Author comments (page count, figures) | Informational |
| `<arxiv:journal_ref>` | Journal reference after publication | Informational |
| `<arxiv:doi>` | DOI after publication | Informational |

## Constructing the arxiv Field

The `arxiv` field in flav-data JSON must follow this exact format:

```
[primary_category/arxiv_idvN](https://arxiv.org/pdf/{id})
```

Example: `[hep-ex/1512.04442v1](https://arxiv.org/pdf/1512.04442)`

**Steps:**
1. Extract the primary category from `<arxiv:primary_category term="hep-ex" />`.
2. Extract the versioned ID from `<atom:id>` (format: `http://arxiv.org/abs/1512.04442v1`). Use regex `abs/(\d+\.\d+)(v\d+)?` to capture `1512.04442` and `v1`.
3. If the paper has no arXiv page (e.g., some older journal-only papers), set `arxiv` to `null`.

**Note on versions**: The arXiv API `<atom:id>` contains the **latest** version number (e.g., `v2`), not `v1`. The `vN` in the `arxiv` field should match the version from which data was cited. For most papers, the latest version is appropriate since it contains corrections. Use `<atom:id>` to extract the version.

**Version priority for data values**: When arXiv has multiple versions (v1, v2, v3...), data values in the JSON should come from the latest submitted version (vN). The `time` field always uses v1 submission date. When HEPData tabulated values differ from the arXiv PDF, HEPData takes priority; if no HEPData entry exists, use the PDF body text.

## Python Extraction

The canonical implementation lives in `scripts/arxiv-ext.py`. It
applies two transforms from `Test/improve.md` rules 3 + 4 before
returning the metadata dict:

- **Rule 3 (BibTeX author)**: `_to_bibtex()` converts `"Aaij, Roel"` →
  `"Aaij, R."` (passes through already-initials form like `"A.M."`).
- **Rule 4 (Unicode → LaTeX)**: `_unicode_to_latex()` rewrites Greek
  letters, math symbols, and typographic punctuation to their LaTeX
  equivalents in the title and abstract.

For clarity, the bare extraction flow (no transforms) is shown below:

```python
import urllib.request
import xml.etree.ElementTree as ET
import re

def get_arxiv_info(arxiv_id):
    """Fetch paper metadata from the arXiv API.

    Returns a dict with fields mapped to flav-data JSON requirements.
    """
    url = f'https://export.arxiv.org/api/query?id_list={arxiv_id}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req, timeout=15)
    root = ET.fromstring(response.read().decode('utf-8'))

    ns = {'atom': 'http://www.w3.org/2005/Atom',
          'arxiv': 'http://arxiv.org/schemas/atom'}
    entry = root.find('atom:entry', ns)

    if entry is None:
        raise ValueError(f"No entry found for arXiv ID: {arxiv_id}")

    # v1 submission date → time field
    published = entry.find('atom:published', ns).text   # "2015-12-14T16:00:00Z"
    time_str = published[:10].replace('-', '.')          # "2015.12.14"

    # Title and abstract
    title = entry.find('atom:title', ns).text.strip()
    abstract = entry.find('atom:summary', ns).text.strip()

    # Authors (full names; convert first to BibTeX form for `author_str`)
    authors = [a.find('atom:name', ns).text
               for a in entry.findall('atom:author', ns)]
    author_str = (f"{_to_bibtex(authors[0])} and others"
                  if len(authors) > 1
                  else (_to_bibtex(authors[0]) if authors else ''))

    # PDF link
    pdf_link = None
    for link in entry.findall('atom:link', ns):
        if link.get('title') == 'pdf':
            pdf_link = link.get('href')
            break

    # Versioned arxiv_id from <atom:id>
    id_url = entry.find('atom:id', ns).text
    vm = re.search(r'abs/(\d+\.\d+)(v\d+)?', id_url)
    arxiv_id_v = f"{vm.group(1)}{vm.group(2) or ''}" if vm else arxiv_id
    # Note: <atom:id> contains the latest version (e.g., v2), not v1

    # Primary category
    pc = entry.find('arxiv:primary_category', ns)
    primary = pc.get('term', '') if pc is not None else ''
    if not primary:
        cats = [c.get('term') for c in entry.findall('atom:category', ns)]
        primary = cats[0] if cats else ''

    return {
        'time': time_str,
        'title': title,
        'abstract': abstract,
        'author_str': author_str,
        'pdf_url': pdf_link,
        'arxiv_id_with_version': arxiv_id_v,
        'primary_category': primary,
        'arxiv_link': f'[{primary}/{arxiv_id_v}](https://arxiv.org/pdf/{arxiv_id})',
    }
```

## Notes

1. **`published` is v1 time**, `updated` is the latest version time. Always use `published` for the `time` field.
2. **Author truncation**: Use "FirstAuthor and others" when more than one author exists. **Convert to InspireHEP BibTeX format** (initials only) before storing — see `Test/improve.md` rule 3 and `inspirehep-api.md` for the `_to_bibtex` helper.
3. **Title LaTeX**: The arXiv API returns titles with `$...$` LaTeX delimiters. These may need escaping for JSON (double backslashes). All Unicode characters in the original title must be converted to LaTeX (e.g. `μ` → `\mu`, `Δ` → `\Delta`).
4. **Abstract = single line**: The arXiv API may return abstracts with multi-line `\\begin{align*} ... \\end{align*}` blocks. These must be collapsed to a single line of LaTeX (line breaks become `, `, with `and` before the last entry). See `Test/improve.md` rule 2.
5. **Network access**: The arXiv API may be unreachable from restricted environments. Use the local terminal for requests.
6. **Error handling**: The API returns HTTP 200 even for non-existent IDs, but with `<total>0</total>`. Check for `<atom:entry>` existence.
7. **Unicode escaping**: Strip any remaining Unicode characters from extracted data (title, abstract, author) and replace with LaTeX equivalents. See `Test/improve.md` rule 4.
