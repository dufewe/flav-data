# InspireHEP API Reference

Authoritative source for TexKeys, collaboration names, and citation information.

**Endpoint**: `https://inspirehep.net/api/literature` — returns JSON.
Rate-limited (~2 req/s). Required header: `Accept: application/json`.

## Query Methods

| Query Type | URL |
|------------|-----|
| By arXiv ID | `https://inspirehep.net/api/literature?q=eprint:{id}` |
| By recid | `https://inspirehep.net/api/literature/{recid}` |
| By TexKey | `https://inspirehep.net/api/literature?q={texkey}` |
| By DOI | `https://inspirehep.net/api/literature?q={doi}` |

## Key Metadata Fields

| Field | Path | Use |
|-------|------|-----|
| `control_number` | `id` (search) / `metadata.control_number` (direct) | recid for InspireHEP URLs |
| `texkeys[]` | `metadata.texkeys[]` | Use first (collaboration-level) for filenames |
| `titles[]` | `metadata.titles[]` | Prefer `source: "arXiv"` (preserves LaTeX) |
| `abstracts[]` | `metadata.abstracts[]` | Prefer `source: "arXiv"` |
| `authors[].full_name` | `metadata.authors[].full_name` | Form: `"Surname, Full First Name"` |
| `collaborations[].value` | `metadata.collaborations[].value` | Collaboration name |
| `preprint_date` | `metadata.preprint_date` | arXiv v1 date (YYYY-MM-DD) → `time` |
| `arxiv_eprints[].value` | `metadata.arxiv_eprints[].value` | arXiv ID (no version number) |
| `dois[].value` | `metadata.dois[].value` | DOI |

## Two ID Types

| Name | Example | Type | Purpose |
|------|---------|------|---------|
| control_number (recid) | `1409497` | Integer | Database primary key for URLs |
| TexKey | `LHCb:2015svh` | String | BibTeX key, used for filenames |

URL uses recid (`https://inspirehep.net/literature/1409497`); display text uses TexKey (`[LHCb:2015svh](https://inspirehep.net/literature/1409497)`).

## Python API (`flav-data-importer/scripts/inspirehep-ext.py`)

| Function | Purpose |
|---|---|
| `get_inspire_by_arxiv(arxiv_id)` → `dict` | Query by arXiv ID, return raw API hit (pass to `extract_metadata()`) |
| `get_inspire_by_recid(recid)` → `dict` | Query by recid directly, return raw record |
| `extract_metadata(meta)` → `dict` | Normalize a raw metadata object into the structured 22-field dict |

`extract_metadata` applies `unicode_to_latex`, `to_bibtex`/`format_authors`, and
returns a dict with these 22 keys:
`texkey`, `recid`, `title`, `abstract`, `authors`, `author_str`, `collaboration`,
`time`, `arxiv_id`, `arxiv_categories`, `journal`, `journal_year`, `journal_volume`,
`journal_issue`, `artid`, `doi`, `keywords`, `citation_count`,
`citation_without_self`, `inspire_hep_link`, `arxiv_link`, `pdf_url`.

CLI usage:
```bash
python3 flav-data-importer/scripts/inspirehep-ext.py 1512.04442
python3 flav-data-importer/scripts/inspirehep-ext.py --arxiv-id 1512.04442   # same as positional
python3 flav-data-importer/scripts/inspirehep-ext.py 1512.04442 --output_dir /tmp/meta
python3 flav-data-importer/scripts/inspirehep-ext.py --recid 1409497
python3 flav-data-importer/scripts/inspirehep-ext.py 1512.04442 --no-write   # stdout only
```

Without `--output_dir` nothing is written; `--no-write` forces stdout-only
even when a directory is given.

## Notes

1. Always prefer arXiv-sourced titles/abstracts — they preserve LaTeX formatting. Journal-sourced versions often strip LaTeX.
2. `author_str` uses the 1 / 2 / 3 / 4+ tiers (SKILL.md rule 3). If no person authors, fall back to `"{group} collaboration"`.
3. Multi-collaboration records are joined with `", "` (e.g. `"ATLAS, CMS"`).
4. Use the collaboration-level TexKey for filenames and indices, not the author-level one.
5. TexKeys can change when papers are updated — always verify before writing indices.
6. `inspire_hep_link`, `arxiv_link`, and `pdf_url` are `None` when the required
   identifiers are absent — never build `[]()` / `(...)` stubs.
7. The script issues a single request with no retry or backoff. On
   timeout/empty response, wait ~2s and rerun it yourself, or fetch the
   bibtex fallback: `https://inspirehep.net/api/literature/{recid}?format=bibtex`.
8. `arxiv_eprints.value` does NOT include version number — use arXiv API for that.
