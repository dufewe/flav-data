# arXiv API Reference

Extract paper metadata from the arXiv API for flav-data JSON files.

**Endpoint**: `https://export.arxiv.org/api/query` — returns Atom XML.
Rate-limited (~1 req/3s). The script issues one request per run with no
pacing or retry, so space successive runs yourself.

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
| `<atom:author>` → `<atom:name>` | `authors` list; `author_str` uses the 1 / 2 / 3 / 4+ tiering |
| `<atom:link title="pdf">` → `href` | PDF link target inside the `arxiv` Markdown link |
| `<atom:id>` | Version number (e.g. `.../abs/1512.04442v1`) |
| `<arxiv:primary_category term="...">` | `arxiv` field prefix |

## Constructing the `arxiv` Field

Format: `[primary_category/arxiv_idvN](https://arxiv.org/pdf/{id})`
Example: `[hep-ex/1512.04442v1](https://arxiv.org/pdf/1512.04442)`

Extract the versioned ID from `<atom:id>` by taking everything after
`/abs/` — this handles both new-style (`1512.04442v1`) and old-style
(`hep-ex/9901001v1`) identifiers. When the ID already contains a `/`
(old style), the `arxiv` link text keeps it as-is instead of adding
the primary category a second time. If no arXiv page exists
(journal-only paper), set `arxiv` to `null`.

**Version note**: `<atom:id>` contains the **latest** version (e.g. `v2`).
The `vN` in the JSON should match the version data was cited from. The `time`
field always uses v1 submission date. HEPData values take priority over PDF
values when both are available.

## Ancillary Files and the e-Print Package

arXiv papers may ship supplementary material ("ancillary files") next to the
PDF. Check them **before** extracting numbers from the paper (see
`data-source.md` §4): machine-readable ancillary data is the primary source,
and the paper's tables are the validation.

1. Inspect `https://arxiv.org/abs/<id>` — the "Ancillary files" section lists
   each file with its own link (`https://arxiv.org/src/<id>/anc/<name>`).
2. Download the whole e-print package: `https://arxiv.org/e-print/<id>`
   (usually a `.tar.gz`, sometimes a single gzipped `.tex`).
3. Unpack and list: `tar tzf src.tar.gz`.

The package always contains the LaTeX source, which preserves table structure
better than PDF text extraction. Candidate data files use `.dat`, `.txt`,
`.csv`, `.tsv`, `.json`, `.yaml`, or `.yml`; `arxiv-ext.download_source()`
returns them under `data_files`.

## Python API (`flav-data-importer/scripts/arxiv-ext.py`)

| Function | Purpose |
|---|---|
| `get_arxiv_info(arxiv_id)` → `dict` | Query arXiv API, return 18-field metadata dict |
| `download_pdf(arxiv_id, output_dir)` → `str` | Download PDF to `<output_dir>/<safe_id>.pdf` (old-style slash → `_`) |
| `download_source(arxiv_id, output_dir)` → `dict` | Download + unpack the e-print package; returns `archive_path`, `source_dir`, `files`, `data_files` |
| `unpack_source(archive_path, source_dir)` → `list[str]` | Unpack an already-downloaded e-print archive and list its files |

Output keys of `get_arxiv_info`: `arxiv_id`, `arxiv_id_with_version`,
`primary_category`, `id_url`, `published`, `updated`, `title`, `abstract`,
`authors`, `author_str`, `pdf_url`, `abs_url`, `arxiv_link`, `categories`,
`comment`, `journal_ref`, `doi`, `time`.

CLI usage:
```bash
python3 flav-data-importer/scripts/arxiv-ext.py 1512.04442
python3 flav-data-importer/scripts/arxiv-ext.py 1512.04442 --output_dir /tmp/dl
python3 flav-data-importer/scripts/arxiv-ext.py 1512.04442 --no-pdf   # metadata only
python3 flav-data-importer/scripts/arxiv-ext.py 1512.04442 --source -o /tmp/dl  # e-print package
python3 flav-data-importer/scripts/arxiv-ext.py 1512.04442 --no-write   # stdout only
```

Without `--output_dir` nothing is written; `--no-write` forces stdout-only
even when a directory is given.

## Notes

1. **`published` is v1 time**, `updated` is the latest version — always use `published`.
2. **Ancillary data first** — if the package ships machine-readable tables, read the values from them and validate against the paper's tables; only fall back to the LaTeX/PDF tables when no ancillary data exists.
3. **Author tiering**: `author_str` follows SKILL.md rule 3 with InspireHEP BibTeX initials — `"Polchinski, J."` for 1, `"Aaij, R. and Smith, J."` for 2, `"Aaij, R., Smith, J., and Oyanguren, A."` for 3, `"Aaij, R. and others"` for 4+.
4. **Unicode escaping**: Replace all Unicode with LaTeX equivalents (see SKILL.md rule 4).
5. **Network access**: arXiv API may be unreachable from restricted environments — use the local terminal.
6. **Error handling**: HTTP 200 even for missing IDs, but `<total>0</total>`. Check for `<atom:entry>`.
