---
name: flav-data-importer
description: Extract structured flavor physics data from papers and save as flav-data standard JSON. Use this skill when the user wants to import, update, delete, or verify data from a paper or website.
category: data-science
tags: [flavor-physics, data-collecting, json-importer, hepdata]
---

# flav-data Importer

Extract structured data from flavor physics experiment/theory papers and import into the flav-data standard JSON format. This skill governs the complete lifecycle of data management — from discovering papers to building validated JSON entries and maintaining the database index.

## Quick Reference

### Directory Overview

```
flav-data-importer/
├── SKILL.md                          # This file — workflow, conventions, pitfalls, tool reference
├── references/                       # Reference materials
│   ├── json-meta.md                  # JSON field specification (the authority on structure)
│   ├── obs-abbr.md                   # Transition symbols, observable naming, LaTeX mappings
│   ├── file-index.md                 # Directory layout, indexing rules, query patterns
│   ├── data-source.md                # Data source priority, scope limitations, extraction guides
│   ├── arxiv-api.md                  # arXiv API extraction — fields, parsing, examples
│   ├── inspirehep-api.md             # InspireHEP API extraction — fields, queries, examples
│   └── hepdata-cli.md                # HEPData CLI usage — commands, YAML structure, parsing
├── scripts/                          # Python scripts
│   ├── arxiv-ext.py                  # Extract arXiv metadata and download PDF
│   ├── inspirehep-ext.py             # Extract InspireHEP metadata
│   ├── hepdata-ext.py                # Extract and parse HEPData tables
│   └── json-valid.py                 # Validate JSON format compliance
└── assets/                           # Workflow examples
    └── workflow-lhcb-2015svh.md      # End-to-end import example (B0→K*μμ)
```

### Reference Guide

| File | Purpose | Relevance |
|------|---------|-----------|
| `file-index.md` | Directory structure and file indexing | Information search |
| `obs-abbr.md` | Transition symbols and observable naming | JSON format |
| `json-meta.md` | JSON metadata structure | JSON format |
| `data-source.md` | Data source priority and scope | Data retrieval |
| `arxiv-api.md` | arXiv API usage | Tool usage |
| `inspirehep-api.md` | InspireHEP API usage | Tool usage |
| `hepdata-cli.md` | HEPData CLI usage | Tool usage |
| `workflow-lhcb-2015svh.md` | Complete import workflow example | Workflow reference |

### Scripts Guide

| Script | Purpose | Relevance |
|--------|---------|-----------|
| `arxiv-ext.py` | Extract arXiv paper metadata and download PDF | Information extraction |
| `inspirehep-ext.py` | Extract InspireHEP paper metadata | Information extraction |
| `hepdata-ext.py` | Extract HEPData tables and metadata | Information extraction |
| `json-valid.py` | Validate JSON file format and data completeness | JSON validation |

## Required Tools

| Category | Tool | Purpose |
|----------|------|---------|
| Network | arXiv API | Get v1 submission date, title, abstract, primary category |
| Network | InspireHEP API | Get texkey, recid, collaboration, DOI, authors |
| Network | hepdata-cli | Get machine-readable HEPData (bypasses Cloudflare). Installed in Hermes venv. |
| Network | web-search / web-extract | Search and extract supplementary web content |
| File reading | pymupdf | PDF text extraction (run via terminal) |
| File reading | vision_analyze | Table image data extraction |
| File processing | read_file / write_file / patch | Read and modify JSON files |
| File processing | terminal | Run Python scripts, validate JSON files |

## Scope

| Supported | Not Supported |
|-----------|--------------|
| Pure experimental measurements (LHCb, CMS, ATLAS, Belle, BaBar, BESIII, etc.) | Phenomenological fits of theoretical parameters using experimental data |
| Theoretical calculations (HPQCD, RBC/UKQCD, FNAL/MILC, etc.) | Conference papers and report papers |
| arXiv preprints and peer-reviewed journal papers | Informal non-peer-reviewed results |

**Rules:**
- If the user requests importing unsupported data, respond with "This data is not supported for import," or find the corresponding formal paper on arXiv/InspireHEP and import from that instead.
- When multiple arXiv papers describe the same measurement (e.g., a conference note + full paper), merge all data into a single JSON file. Retain all papers' Inspire IDs, arXiv IDs, and DOIs.
- When a measurement involves multiple collaborations (e.g., ATLAS+CMS combination), fill the corresponding data for all involved groups in the database under their respective directories.

## Workflow

Given a paper's arXiv ID, InspireHEP ID, or title, follow these steps:

### Step 1: File Search

Search the database for an existing entry using the paper's identifiers.
- Query the InspireHEP API to obtain the TexKey and control number. See `references/inspirehep-api.md`.
- Search the database index using the TexKey. See `references/file-index.md` for query patterns.
- **Decision**: File exists → compare versions. Update if requested, skip otherwise. File not found → proceed to Step 2.

**Tip**: Always use the collaboration-level TexKey (e.g., `LHCb:2015svh`) not the author-level one (e.g., `Aaij:2015oid`).

### Step 2: Data Operations

Retrieve data following the priority in `references/data-source.md`:
1. **HEPData** (preferred) → Use `scripts/hepdata-ext.py` or `hepdata-cli`
2. **CDS** → curl search CERN Document Server
3. **LHCb Public Pages** → Analysis result pages
4. **arXiv PDF** → Use pymupdf (fallback)
5. **ar5iv HTML** → Table parsing from HTML
6. **vision_analyze** → When user provides table screenshots

Retrieve metadata from two sources:
- **arXiv API** → v1 date, title, abstract, primary category, PDF URL (`scripts/arxiv-ext.py`)
- **InspireHEP API** → TexKey, recid, collaboration, DOI, authors (`scripts/inspirehep-ext.py`)

**Metadata field sources:**
| Field | Source |
|-------|--------|
| `inspire-hep`, `author`, `collaboration`, `title`, `abstract` | InspireHEP BibTeX info |
| `arxiv`, `time`, `pdf` | arXiv webpage |
| `transition-mode` | Paper information |

#### Data Add
1. Build file path per `references/file-index.md` — note the **Lab-Collaboration** folder structure: `Experimental/LHC-LHCb/2015/12/LHCb:2015svh.json` (folder uses `Lab-Collaboration`, data file uses collaboration-only name)
2. Create year and month directories if they don't exist (`mkdir -p Experimental/LHC-LHCb/2015/12`)
3. Determine transition symbol and observable naming per `references/obs-abbr.md`
4. Build JSON metadata per `references/json-meta.md`
5. Extract numerical values and populate the JSON
6. Write the JSON file to the month subdirectory
7. Update the annual index at `Experimental/LHC-LHCb/2015/LHCb@2015.json`

#### Data Update
1. Locate the existing `xxxx.json` file via the index
2. Compare existing data with new data
3. Update changed fields

#### Data Delete
1. Locate the `xxxx.json` file via the index
2. Delete the file and remove it from the annual index

#### Data Verify
1. Locate the `xxxx.json` file via the index
2. Validate using `scripts/json-valid.py`
3. Cross-check against the source paper data — **do not modify any JSON file**

### Step 3: Cleanup

Remove all temporary files (PDFs, YAML downloads, intermediate JSONs) from your output directory. Keep the database tidy.

## Core Conventions

### Transition Symbol: `A.B.2.C.D`

$A + B \to C + D$ → `A.B.2.C.D`. Core rules (full spec in `references/obs-abbr.md` §1):
- Particles ordered by charge: `+`, `-`, `0`
- Antiparticles: `Bar` suffix (except charged: `W-` not `WBar`)
- Neutrinos: no flavor — `nu` / `nuBar`
- Cascade: `p.p.2.W+.2.mu+.nu`; dilepton resonance: `J/psi(2.l+.l-)`

Quick reference:
| Process | Symbol |
|---------|--------|
| $B^0 \to e^+ e^-$ | `B0.2.e+.e-` |
| $\bar{B}^0 \to e^+ e^-$ | `B0Bar.2.e+.e-` |
| $W^- \to \mu^- \bar{\nu}_\mu$ | `W-.2.mu-.nuBar` |
| $pp \to Z \to \mu^+ \mu^-$ | `p.p.2.Z.2.mu+.mu-` |

### Observable Naming: `OBS(transition)[condition]`

- **OBS**: abbreviation only (never full expressions). Full table → `references/obs-abbr.md` §2–3.
- **transition**: the `A.B.2.C.D` symbol.
- **`[condition]`**: used ONLY for multi-transition observables; NOT for q² bins (use separate `data[]` entries).
  - `/` → ratio: `R(B0.2.Kst0.l+.l-)[mu/e]`
  - `-` → difference: `DeltaACP(B-.2.l-.nuBar)[mu-e]`

Special patterns (see `references/obs-abbr.md` §2 for full details):
- Differences: `DeltaOBS(transition)[condition]`, LaTeX: $\Delta_{OBS}^{condition}(transition)$
- Ratios: `ROBS(transition)[condition]`, LaTeX: $R_{OBS}^{condition}(transition)$
- CKM $r$/$\delta$: B meson + final-state meson carry **negative** charge (`B-.2.D0.K-`)

### Numeric Format

- **All values are strings**: `"0.69"` not `0.69`. Includes `value`, `q2min`, `q2max`, all error fields, and `unit`. Exception: correlation/covariance matrix elements are floats.
- **Component errors preferred**: Record separate `type@N_err` groups (e.g., `type@1_err: "stat"`, `type@2_err: "syst"`). Do NOT pre-combine into total errors when component errors are available.
- **Total error format**: When the paper reports only a single combined error (no stat/syst breakdown), use `tot_err_up` / `tot_err_down` instead of `type@N_err` fields. If the value is from an external reference, also add a `ref` field (see External Reference Format in `references/json-meta.md`).
- **Symmetric errors**: `err_up` = `err_down` (both required even when equal).
- **Upper limits**: `type@N_upper_limit` = numeric value, `type@N_level` = confidence level (e.g., `"90%@CLs"`). Do NOT swap or use `err_up`.
- **Single boundary**: Fill the missing boundary with the literal string (`"q2min"` or `"q2max"`).
- **unit**: Only for dimensional observables. Omit for dimensionless.
- **LaTeX escaping**: `\\to` in JSON file text. After `json.load()`, this becomes `\to` in Python.
- **Indentation**: 4 spaces.

### Data Entry Field Whitelist

Each element inside the `data[]` array may contain **only** these field patterns:
- `obs@N` — observable entries (where N is a positive integer)
- `type@N_correlation` — correlation matrix matching the error type label (e.g., `type@1_correlation` for `type@1_err`)
- `type@N_covariance` — covariance matrix matching the error type label
- `tot_correlation` — correlation matrix for total error format (`tot_err_up`/`tot_err_down`)
- `tot_covariance` — covariance matrix for total error format

**No other fields are allowed** inside a data entry. Do not add custom metadata keys, comments, or auxiliary fields within `data[]`.

The matrix naming must match the error type: component errors use `type@N_*`, total error uses `tot_*`.

### Folder Naming

- Experimental folders use the `Lab-Collaboration` format (实验室-实验组): `Experimental/LHC-LHCb/`, `Experimental/LHC-ATLAS/`, `Experimental/LHC-CMS/`, `Experimental/PEPII-BaBar/`, `Experimental/KEK-Belle/`, `Experimental/BEPCII-BESIII/`, `Experimental/PDG/`, `Experimental/HFLAV/`, `Experimental/LEP/`.
- When no parent lab exists, use the collaboration/group name directly (e.g., `HFLAV`, `PDG`).
- Theoretical folders use the group name: `Theoretical/HPQCD/`, `Theoretical/RBC-UKQCD/`.
- Data files and index filenames always use only the collaboration name: `LHCb:2015svh.json`, `LHCb@2015.json`.

## Common Pitfalls

| Pitfall | Correct Approach |
|---------|-----------------|
| Using `[condition]` for different q² bins | Use separate `data[]` entries with `q2min`/`q2max` |
| Guessing TexKey for `ref` fields | Look up arXiv ID in the paper's references → search InspireHEP → use the verified TexKey |
| `type@1_err` missing when `_up`/`_down` exist | Add `type@1_err` with the average or symmetric component |
| `upper_limit` and `level` swapped | `upper_limit` = numeric value, `level` = confidence string |
| Non-property transition-mode (e.g., "rare decay") | Use property-based names: "semileptonic decay", "leptonic decay", "scattering" |
| Annual index with outdated texkey | Always verify the latest texkey on InspireHEP before writing the index |
| Empty fields as empty strings | Omit the key entirely; only `arxiv` uses `null` when absent |
| `year` field in JSON | Not supported — omit it |
| Using `tot_correlation` with component errors | Use `type@N_correlation` matching the error type (e.g., `type@1_correlation` for `type@1_err`). `tot_correlation` is only valid with `tot_err_up`/`tot_err_down` format. |
| Matrix dimension mismatch with obs count | Ensure matrix size = number of obs@N in the same entry |
| Using author-level texkey for filenames | Always use the collaboration-level texkey (e.g., `LHCb:2015svh` not `Aaij:2015oid`) |
| Double-escaping LaTeX (`\\to` instead of `\to`) | Use `\\to` in the JSON file text (double backslash) |
| Author name with initials | Use full first name: `"Aaij, Roel and others"`, not `"Aaij, R. and others"` |
| Abstract starting with lowercase | Must match arXiv exactly; typically starts with capital letter (e.g., "A measurement...") |
| Hyphenated transition-mode | No hyphens: use `"semileptonic decay"`, not `"semi-leptonic decay"` |
| `unit` field as empty string | Omit the `unit` key entirely for dimensionless observables |
| Adding `comment` or custom fields in data entries | Not allowed — data entries may only contain `obs@N`, `type@N_correlation`, `type@N_covariance`, `tot_correlation`, or `tot_covariance` |
| `transition-mode` not as last field | Must be the final key in the JSON object |
| Observable name includes q² bin | The `name` field should only contain `OBS(transition)[condition]` — q² bins go in `q2min`/`q2max` fields |
| arXiv link text missing version number | Must include version: `[hep-ex/1512.04442v1](https://arxiv.org/pdf/1512.04442)` |
| Correlation matrix diagonal ≠ 1.0 | If diagonal is not 1.0, it's a covariance matrix — use `*_covariance` instead |

### Matrix Format

Matrices (correlation/covariance) use compact row-per-line format:

```json
"type@1_correlation": [
    [1.0, 0.06, 0.02],
    [0.06, 1.0, 0.03],
    [0.02, 0.03, 1.0]
]
```

**Correlation vs Covariance**: 
- `tot_correlation`: diagonal = 1.0, off-diagonal ∈ [-1, 1]
- `tot_covariance`: diagonal = variance (error²), off-diagonal = covariance
- If diagonal elements are not 1.0, use `*_covariance` naming

## JSON Example

Standard measurement with component errors:

```json
{
    "inspire-hep": "[LHCb:2015svh](https://inspirehep.net/literature/1409497)",
    "author": "Aaij, Roel and others",
    "collaboration": "LHCb",
    "title": "Angular analysis of the $B^{0}\\to K^{*0}\\mu^{+}\\mu^{-}$ decay",
    "arxiv": "[hep-ex/1512.04442v1](https://arxiv.org/pdf/1512.04442)",
    "time": "2015.12.14",
    "abstract": "An angular analysis of the $B^{0}\\to K^{*0}(\\to K^{+}\\pi^{-})\\mu^{+}\\mu^{-}$ decay...",
    "pdf": "https://arxiv.org/pdf/1512.04442",
    "data": [
        {
            "obs@1": {
                "name": "FL(B0.2.Kst0.mu+.mu-)",
                "latex": "$F_L(B^{0}\\to K^{*0}\\mu^{+}\\mu^{-})$",
                "value": "0.69",
                "type@1_err": "stat",
                "type@1_err_up": "0.035",
                "type@1_err_down": "0.036",
                "type@2_err": "syst",
                "type@2_err_up": "0.017",
                "type@2_err_down": "0.017",
                "q2min": "0.1",
                "q2max": "1.1"
            },
            "obs@2": { ... },
            "type@1_correlation": [[1.0, 0.06, ...], [0.06, 1.0, ...], ...]
        }
    ],
    "transition-mode": "semileptonic decay"
}
```

Full specification → `references/json-meta.md`
