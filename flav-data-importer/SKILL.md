---
name: flav-data-importer
description: >-
  Extract structured flavor physics data from arXiv / InspireHEP / HEPData
  papers and save as flav-data standard JSON. Covers the full lifecycle:
  metadata lookup, YAML parsing, transition-symbol + observable-name
  construction, JSON schema validation, and index updates.
  Works with LHCb / ATLAS / CMS / Belle / BaBar / BESIII / PDG
  / HFLAV / theory groups.
when_to_use: |
  Use this skill to:
  - Import, add, or update a flavor-physics paper
  - Delete or remove a paper from the database
  - Verify or validate an existing JSON file
  - Maintain the paper index (add, check, rebuild)
  - Build a JSON file from scratch following the flav-data schema
  - Diagnose validation errors in a JSON file
  Do NOT use for: general arXiv/InspireHEP browsing unrelated to
  data extraction, fitting the imported data, or rendering the dashboard.
category: data-science
tags: [flavor-physics, data-collecting, json-importer, hepdata, lhcb, b-decays, bsm]
version: 1.0.0
---

# flav-data Importer

Extract structured flavor-physics data from papers into standard JSON.
Covers the full lifecycle: discovery → extraction → validation → index maintenance.

## Directory

```text
flav-data-importer/
├── SKILL.md                    # Workflow, conventions, pitfalls (this file)
├── references/
│   ├── json-meta.md            # JSON field spec (authority)
│   ├── obs-abbr.md             # Transition symbols, observable naming, LaTeX
│   ├── file-index.md           # Directory layout, indexing
│   ├── data-source.md          # Source priority, scope
│   ├── arxiv-api.md            # arXiv API usage
│   ├── inspirehep-api.md       # InspireHEP API usage
│   └── hepdata-cli.md          # HEPData CLI usage
├── assets/
│   └── workflow-lhcb-2015svh.md # Full import example
└── scripts/
    ├── common.py               # Shared: Unicode→LaTeX + BibTeX helpers
    ├── arxiv-ext.py            # arXiv metadata + PDF download
    ├── inspirehep-ext.py       # InspireHEP metadata
    ├── hepdata-ext.py          # HEPData table extraction
    └── json-valid.py           # JSON validation
```

## Tool Inventory

| Tool | Use |
|------|-----|
| **arXiv API** | v1 date, title, abstract, primary category, PDF URL → `references/arxiv-api.md` |
| **InspireHEP API** | TexKey, recid, collaboration, DOI, authors → `references/inspirehep-api.md` |
| **hepdata-cli** | Machine-readable HEPData. Install: `pip install hepdata-cli` → `references/hepdata-cli.md` |
| **pymupdf** | PDF text extraction (fallback data source) |
| **vision_analyze** | Table screenshot extraction |

## Scope

| Supported | Not Supported |
|-----------|--------------|
| Experimental measurements (LHCb, CMS, ATLAS, Belle, BaBar, BESIII, etc.) | Conference/report papers (no formal preprint) |
| Theoretical calculations (HPQCD, RBC/UKQCD, FNAL/MILC, etc.) | Informal non-peer-reviewed results |
| arXiv preprints and journal papers | Phenomenological fits to experimental data |

**Rules:**
- Unsupported data: reply "Not supported" or find the formal paper on arXiv/InspireHEP.
- Multiple arXiv papers for one measurement → single JSON, retain all IDs and DOIs.
- Multi-collaboration → fill data for all involved groups under their directories.

## Workflow

### Step 1: File Search

1. Query InspireHEP API for TexKey and recid → `references/inspirehep-api.md`
2. Search database index by TexKey → `references/file-index.md`
3. **Decision**:
   - **Found in index, file on disk** → compare versions (update if newer)
   - **Found in index, file missing** → verify index integrity; rebuild file or remove stale index entry
   - **Not found** → proceed to Step 2

**Tip**: always use the collaboration-level TexKey (`LHCb:2015svh`), not author-level (`Aaij:2015oid`).

### Step 2: Data Operations

**Data source priority** (see `references/data-source.md`):
1. HEPData → `scripts/hepdata-ext.py` or `hepdata-cli`
2. CDS → curl search
3. LHCb Public Pages
4. arXiv PDF → pymupdf (fallback)
5. ar5iv HTML
6. vision_analyze (user-provided screenshots)

**Metadata sources:**
| Field | Source |
|-------|--------|
| `inspire-hep`, `author`, `collaboration`, `title`, `abstract` | InspireHEP (arXiv-sourced preferred for title/abstract) |
| `arxiv`, `time`, `pdf` | arXiv API |
| `transition-mode` | Paper content |

#### Add
1. **Determine the target folder** by looking up the group in the
   `Lab-Collaboration` table in `references/file-index.md` §1. If the
   group is not listed yet, add a new entry to that table **first**
   (commit it separately) and then proceed.
2. Build path per `references/file-index.md` — `<Lab>-<Collaboration>`
   folder, collaboration-only filename
3. `mkdir -p Experimental/<Lab>-<Collaboration>/<year>/<month>`
4. Determine transition symbol + observable naming → `references/obs-abbr.md`
5. Build JSON metadata → `references/json-meta.md`
6. Extract values and populate JSON
7. Write JSON to month subdirectory
8. Update annual index at `Experimental/<Lab>-<Collaboration>/<year>/<Collaboration>@<year>.json`

**Special cases**:
- **HFLAV / PDG** use a non-standard schema (one snapshot per year).
  Do **not** create per-paper JSONs — write a single year-level file
  matching the existing schema (see `references/json-meta.md` for
  the subgroup structure). **These files skip `json-valid.py`**
  — validate them manually against the HFLAV/PDG schema in json-meta.md.

#### Update
1. Locate existing file via index
2. Compare; update changed fields

#### Delete
1. Locate file via index
2. Delete file; remove from annual index

#### Verify (read-only)
1. Locate file via index
2. `python3 scripts/json-valid.py <file>`
3. Cross-check against source paper — **do not modify**

### Step 3: Cleanup

Remove all temporary files (PDFs, YAML, intermediate JSONs).

## Core Conventions

### Transition Symbol: `A.B.2.C.D`

Full spec → `references/obs-abbr.md` §1. Key rules:
- Charge order: `+`, `-`, `0`
- Antiparticles: neutral mesons → `B0Bar`; baryons → `Lambdac+Bar` (Bar at **end**); charged particles use charge alone (`B+`/`B-`)
- Neutrinos: no flavor → `nu`/`nuBar`

### Observable Naming: `OBS(transition)[condition]`

Full spec → `references/obs-abbr.md` §2. Key rules:
- **Basic** (intrinsic properties): `OBS(particle)` — `Mass(t)`, `Tau(e-)`
- **Composite** (decay/scattering): `OBS(transition)[condition]` — `Br(B0.2.e+.e-)`
- `[condition]` only for multi-transition: `/` = ratio, `-` = difference. NOT for q² bins.
- `DeltaOBS` / `ROBS`: `DeltaOBS(transition)[condition]`, `ROBS(transition)[condition]`

### Numeric Format

Full spec → `references/json-meta.md`. Key rules:
- **All values are strings** (`"0.69"`). Exception: matrix elements are floats.
- **Component errors preferred**: `type@N_err_up`/`_down` + `type@N_err` label.
- **Total error** (no stat/syst breakdown): `tot_err_up`/`tot_err_down`
- **Upper limits**: `type@N_upper_limit` = value, `type@N_level` = `"90%@CLs"`
- **LaTeX in JSON**: double backslash (`\\to`) in JSON file text
- **Indentation**: 4 spaces

> **Tip**: Do NOT use `[condition]` for q² bins — use `q2min`/`q2max` per obs.
> Do NOT use property `"rare decay"` — use `"semileptonic decay"` etc.
> When a paper reports fit results (value + errors) AND CLs upper limits, **import both**. They come from different statistical procedures and both belong in the JSON. See `references/json-meta.md` "Combined Fit + Upper Limit Format".

Four formatting rules for imported data:

1. **Matrix format (row-per-line)** — each matrix row on one line:
   ```json
   "tot_correlation": [
       [1.0, 0.5, 0.3],
       [0.5, 1.0, 0.2],
       [0.3, 0.2, 1.0]
   ]
```text
   Applies to all `*_correlation` / `*_covariance` fields.

2. **Abstract = single line** — collapse multi-line LaTeX blocks:
   → `\\begin{align*}...\\end{align*}` becomes comma-separated inline LaTeX.

3. **Author = InspireHEP BibTeX** — `"Aaij, R. and others"` (initials only).
   ✗ `"Aaij, Roel and others"` (full name).
   Fallback (no authors): `"{group} collaboration"`.

4. **No Unicode** — replace with LaTeX equivalents:
   `μ`→`\mu`, `Δ`→`\Delta`, `±`→`\pm`, `→`→`\to`,
   `°`→`^{\circ}`, `¯`→`\bar{}`, smart quotes → `` ` ``/`'`/`` `` ``/`''`.
   (The mapping in `common.py` covers Greek letters, math symbols, superscripts,
   and typographic punctuation. Unrecognized characters pass through unchanged —
   review titles/abstracts before commit.)


## Troubleshooting

### `hepdata-cli: command not found`

External package. Install once:
```bash
pip install hepdata-cli
```
Then re-run `scripts/hepdata-ext.py`. The script resolves the binary from:
`$PATH` → venv `bin/` → `~/.local/bin/` → Homebrew prefixes.

### PyYAML not installed (`HAS_YAML = False`)

Optional for CLI wrappers, required for YAML parsers:
```bash
pip install pyyaml
```

### arXiv / InspireHEP API returns errors

Both APIs are unauthenticated and rate-limited:
1. **Verify the ID** (e.g. `1512.04442`, not `hep-ex/1512.04442`).
2. **Wait and retry** — arXiv ~1 req/3s; InspireHEP ~2 req/s.
3. **Fall back** to PDF extraction if the API never returns.

### Validator reports issues

The validator never auto-fixes — it only reports.

| Common Issue | Fix |
|---|---|
| `arxiv field is '"null"'` | Use JSON `null`, not the string `"null"` |
| `obs@N numbering not contiguous` | Renumber after deletion |
| `transition-mode not in allowed list` | Use a valid mode from json-meta.md |
| `*_correlation: matrix not symmetric` | Ensure M[i][j] == M[j][i] |

## Known Limitations

1. **PDF extraction is best-effort.** The scripts focus on structured sources (arXiv, InspireHEP, HEPData). Image-based PDFs need `vision_analyze` + human review.

2. **HEPData requires `hepdata-cli`.** Direct `curl` to hepdata.net is blocked by Cloudflare.

3. **arXiv BibTeX is approximate.** `arxiv-ext.py` produces a best-effort author string. Use `inspirehep-ext.py` for the canonical InspireHEP version.

4. **Unicode→LaTeX mapping is conservative.** Exotic characters (emoji, CJK) pass through unchanged — review titles/abstracts before commit.

5. **No automatic index sync.** If the import crashes between writing the file and updating the index, re-run `Verify` (or check `file-index.md`) to detect the discrepancy.

6. **Not a fit tool.** This skill produces JSON inputs for downstream fitting tools — it does not perform fits.

## FAQ

**Q: Can I import a paper with no arXiv ID (journal-only)?**
A: Yes. Set `arxiv` to `null`.

**Q: What if the paper has a CERN note number instead of an arXiv ID?**
A: Use a Markdown link: `"[LHCb-NOTE-2015-001](https://...)"`. The validator accepts any non-arXiv-ID link.

**Q: How to handle mixed q² bins across different obs entries?**
A: Use `q2min`/`q2max` per `obs@N`. The `[condition]` syntax is for multi-decay-channel ratios only (e.g. `R(D)`).

**Q: Validator complains about missing transition symbol — where to add it?**
A: If the observable is a decay or scattering measurement (e.g. branching fraction), rename to `OBS(transition)[condition]` form. Basic intrinsic properties (mass, lifetime, charge — e.g. `Mass(Z)`, `Tau(e-)`) do not need a transition symbol; the validator accepts them as-is. See `references/obs-abbr.md` for naming rules.

**Q: Can I run both `arxiv-ext.py` and `inspirehep-ext.py` for the same paper?**
A: Yes. arXiv provides version number and PDF URL; InspireHEP provides authoritative author list and DOI. Use InspireHEP for metadata, arXiv for PDF.

**Q: I have `texkey` from InspireHEP but my JSON doesn't show it?**
A: The JSON field is `inspire-hep` (a Markdown link `[TexKey](url)`), not a bare `texkey` key. Run `inspirehep-ext.py` to get the correct `inspire-hep` value. The `texkey` itself is embedded in that link.
