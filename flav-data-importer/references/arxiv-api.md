# arXiv API Reference

Extract paper metadata from the arXiv API for flav-data JSON files.

**Endpoint**: `https://export.arxiv.org/api/query` — returns Atom XML.
Rate-limited (~1 req/3s); avoid rapid successive requests.

## Query Methods

```bash
# By arXiv ID (most common)
curl -sL "https://export.arxiv.org/api/query?id_list=1512.04442"

# By title
curl -sL "https://export.arxiv.org/api/query?search_query=ti:angular+analysis+cat:hep-ex&max_results=10"

# By author
curl -sL "https://export.arxiv.org/api/query?search_query=au:Roel_Aaij&max_results=20"
```

## Key Response Fields (`<entry>` element)

| XML Path | Use in flav-data |
|----------|-----------------|
| `<atom:published>` | `time` → `2015.12.14` (v1 date) |
| `<atom:title>` | `title` (LaTeX preserved) |
| `<atom:summary>` | `abstract` (LaTeX preserved) |
| `<atom:author>` → `<atom:name>` | First author for `author` field |
| `<atom:link title="pdf">` → `href` | `pdf` URL |
| `<atom:id>` | Version number (e.g. `.../abs/1512.04442v1`) |
| `<arxiv:primary_category term="...">` | `arxiv` field prefix |

## Constructing the `arxiv` Field

Format: `[primary_category/arxiv_idvN](https://arxiv.org/pdf/{id})`
Example: `[hep-ex/1512.04442v1](https://arxiv.org/pdf/1512.04442)`

Extract the versioned ID from `<atom:id>` using regex `abs/(\d+\.\d+)(v\d+)?`.
If no arXiv page exists (journal-only paper), set `arxiv` to `null`.

**Version note**: `<atom:id>` contains the **latest** version (e.g. `v2`).
The `vN` in the JSON should match the version data was cited from. The `time`
field always uses v1 submission date. HEPData values take priority over PDF
values when both are available.

## Python API (`scripts/arxiv-ext.py`)

| Function | Purpose |
|---|---|
| `get_arxiv_info(arxiv_id)` → `dict` | Query arXiv API, return 18-field metadata dict |
| `download_pdf(arxiv_id, output_dir)` → `str` | Download PDF to `<output_dir>/<arxiv_id>.pdf` |

Output keys of `get_arxiv_info`: `arxiv_id`, `arxiv_id_with_version`,
`primary_category`, `id_url`, `published`, `updated`, `title`, `abstract`,
`authors`, `author_str`, `pdf_url`, `abs_url`, `arxiv_link`, `categories`,
`comment`, `journal_ref`, `doi`, `time`.

CLI usage:
```bash
python3 scripts/arxiv-ext.py 1512.04442
python3 scripts/arxiv-ext.py 1512.04442 --output_dir /tmp/dl
python3 scripts/arxiv-ext.py 1512.04442 --no-pdf   # metadata only
```

## Notes

1. **`published` is v1 time**, `updated` is the latest version — always use `published`.
2. **Author truncation**: Use "FirstAuthor and others" with InspireHEP BibTeX initials (see SKILL.md rule 3).
3. **Unicode escaping**: Replace all Unicode with LaTeX equivalents (see SKILL.md rule 4).
4. **Network access**: arXiv API may be unreachable from restricted environments — use the local terminal.
5. **Error handling**: HTTP 200 even for missing IDs, but `<total>0</total>`. Check for `<atom:entry>`.
