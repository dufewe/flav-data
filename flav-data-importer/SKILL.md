---
name: flav-data-importer
description: Extract structured flavor physics data from papers and save as flav-data standard JSON. Use this skill when the user wants to import, update, delete, or verify data from a paper or website.
category: data-science
tags: [flavor-physics, data-collecting, json-importer, hepdata]
---

# flav-data Importer

Extract structured data from flavor physics papers into the flav-data standard JSON format. This skill governs the complete lifecycle of data management — from discovering papers to building validated JSON entries and maintaining the database index.

## Directory Overview

```
flav-data-importer/
├── SKILL.md                          # This file — workflow, conventions, pitfalls, tool reference
├── references/
│   ├── json-meta.md                  # JSON field specification (the authority on structure)
│   ├── obs-abbr.md                   # Transition symbols, observable naming, LaTeX mappings
│   ├── file-index.md                 # Directory layout, indexing rules, query patterns
│   ├── data-source.md                # Data source priority, scope limitations, extraction guides
│   ├── arxiv-api.md                  # arXiv API extraction — fields, parsing, examples
│   ├── inspirehep-api.md             # InspireHEP API extraction — fields, queries, examples
│   └── hepdata-cli.md                # HEPData CLI usage — commands, YAML structure, parsing
├── scripts/
│   ├── arxiv-ext.py                  # Extract arXiv metadata and download PDF
│   ├── inspirehep-ext.py             # Extract InspireHEP metadata
│   ├── hepdata-ext.py                # Extract and parse HEPData tables
│   └── json-valid.py                 # Validate JSON format compliance
└── assets/
    └── workflow-lhcb-2015svh.md      # End-to-end import example (B0→K*μμ)
```

Database root: `flav-data/`
- Experimental: `flav-data/Experimental/{group}/{year}/{month}/{file_id}.json`
- Theoretical: `flav-data/Theoretical/{group}/{year}/{month}/{file_id}.json`

## Scope

| Supported | Not Supported |
|-----------|--------------|
| Pure experimental measurements (LHCb, CMS, ATLAS, Belle, BaBar, BESIII, etc.) | Phenomenological fits of theoretical parameters using experimental data |
| Theoretical calculations (HPQCD, RBC/UKQCD, FNAL/MILC, etc.) | Conference papers and report papers |
| arXiv preprints and peer-reviewed journal papers | Informal non-peer-reviewed results |

**Rules:**
- If the user requests importing unsupported data, respond with "This data is not supported for import," or find the corresponding formal paper on arXiv/InspireHEP and import from that instead.
- When multiple arXiv papers describe the same measurement (e.g., a conference note + full paper, or a short letter + detailed analysis), merge all data into a single JSON file. Retain all papers' Inspire IDs, arXiv IDs, and DOIs in the metadata fields.
- When a measurement involves multiple experimental collaborations (e.g., ATLAS+CMS combination), fill the corresponding data for all involved groups in the database under their respective directories.

## Workflow

### Step 1: Search and Confirm

Before creating any file, check whether the data already exists in the database:

1. **Identify the paper** — get the arXiv ID, Inspire ID, or full title from the user.
2. **Query the InspireHEP API** to obtain the TexKey and control number. See `references/inspirehep-api.md`.
3. **Search the database index** using the TexKey. See `references/file-index.md` for query patterns.
4. **Decision**:
   - File exists → compare versions. If the user wants an update, proceed to Step 2 with the new data. If not, skip.
   - File not found → proceed to Step 2.

**Tip**: Always use the collaboration-level TexKey (e.g., `LHCb:2015svh`) not the author-level one (e.g., `Aaij:2015oid`) for filenames and indices. If both exist, pick the collaboration-level one.

### Step 2: Retrieve Metadata

You need metadata from two sources:

| Source | Fields Retrieved | Tool | Reference |
|--------|-----------------|------|-----------|
| arXiv API | v1 submission date, title, abstract, first author, primary category, PDF URL | `scripts/arxiv-ext.py` | `references/arxiv-api.md` |
| InspireHEP API | TexKey, control number (recid), collaboration, DOI, journal info, full author list | `scripts/inspirehep-ext.py` | `references/inspirehep-api.md` |

**Important field mappings:**
- `time` ← arXiv `<published>` date as `YYYY.MM.DD`. If no arXiv v1 date, use the journal acceptance date.
- `title` ← InspireHEP `titles[]` with `source: "arXiv"` (preserves LaTeX). Fallback to any available title.
- `abstract` ← InspireHEP `abstracts[]` with `source: "arXiv"`. Fallback to any available abstract.
- `author` ← First author + `" and others"`. If no person names found, use `"{collaboration} collaboration"`.
- `inspire-hep` ← `[{texkey}](https://inspirehep.net/literature/{recid})`
- `arxiv` ← `[{primary_category}/{arxiv_id}v{N}](https://arxiv.org/pdf/{id})`. Use `null` if no arXiv ID.

### Step 3: Retrieve Data

Data sources in priority order. Try each in sequence until usable data is found:

1. **HEPData** (preferred — structured, machine-readable)
   - Use `scripts/hepdata-ext.py` or the `hepdata-cli` binary at `/hepdata-cli`.
   - Run `hepdata-cli fetch-names -i inspire <recid>` to list available tables.
   - Run `hepdata-cli download -f json -i inspire <recid> -d /tmp/out` to download metadata.
   - Download individual tables via curl (URL-encode table names: "Table 1" → "Table%201").
   - See `references/hepdata-cli.md` for YAML parsing details.
   - Note: Theory papers and many BSM search papers do not have HEPData entries. Fall through quickly.

2. **CDS** (CERN Document Server)
   - Search by arXiv ID: `curl -sL "https://cds.cern.ch/search?f=reportnumber&p1=<arxiv_id>"`
   - Useful for CMS PAS records and supplementary materials.

3. **LHCb Public Analysis Pages**
   - URL pattern: `https://lbfence.cern.ch/alcm/public/analysis/full-details/<ANALYSIS_ID>/`
   - Contains YAML/JSON data with correlation matrices.

4. **arXiv PDF** (last resort)
   - Download: `curl -sL -O "https://arxiv.org/pdf/<arxiv_id>.pdf"`
   - Extract with pymupdf: `python3 -c "import pymupdf; doc=pymupdf.open('paper.pdf'); [print(p.get_text()) for p in doc]"`
   - pymupdf is at `/python/site-packages` — run via terminal, not execute_code sandbox.
   - Parsing values from PDF tables is error-prone; cross-check against paper text.

5. **ar5iv HTML** (alternative to PDF)
   - URL: `https://ar5iv.labs.arxiv.org/html/<arxiv_id>`
   - Easier to parse tables from HTML than from PDF text. May not be the latest version.

6. **vision_analyze** (table screenshots)
   - Use when the user provides screenshots of tables from a paper.

### Step 4: Build JSON

Construct the JSON file following these references:
- **File path and index rules** → `references/file-index.md`
- **Transition symbol** → `references/obs-abbr.md` §1
- **Observable naming** → `references/obs-abbr.md` §2
- **JSON structure and field rules** → `references/json-meta.md`

**Key decisions during construction:**
- One `data[]` entry per q² bin / dataset / measurement group.
- Each entry contains `obs@1`, `obs@2`, ... for all observables measured in that bin.
- Use `q2min`/`q2max` for kinematic binning. Do NOT use `[condition]` for different bins.
- Include `type@N_correlation` or `type@N_covariance` at the entry level if available.
- For upper limits, use `type@N_upper_limit` + `type@N_level`. Do NOT use `err_up` for limits.

### Step 5: Validate

```bash
python3 scripts/json-valid.py <path/to/file.json>
```

The validator checks:
- JSON parseability
- All required top-level fields present
- Each obs@N has required fields for its format (standard, upper limit, total error, external ref)
- Numeric fields are strings (except matrix elements)
- Correlation matrices: symmetric, diagonal = 1.0, dimension matches obs count
- Covariance matrices: symmetric
- LaTeX fields non-empty
- Transition symbols conform to `A.B.2.C.D`
- arxiv field format correct (`[category/idvN](url)` or `null`)
- transition-mode contains "decay" or "scattering"

### Step 6: Update Index and Cleanup

1. **Update the annual index** at `{group}/{year}/{group}@{year}.json`:
   - Add the file_id to the appropriate month key (zero-padded: "01"–"12").
   - If the month key doesn't exist, create it.
   - Sort file_ids within each month by arXiv v1 submission date.

2. **Verify index integrity**:
   ```python
   import json, os
   # Compare indexed files vs actual files on disk
   ```
   See `references/file-index.md` for the full script.

3. **Clean up** all temporary files (PDFs, YAML downloads, intermediate JSONs) from `/tmp`.

## Core Conventions

### Transition Symbol: `A.B.2.C.D`

The transition `A + B → C + D` is written as `A.B.2.C.D`:
- `2` replaces the arrow to clearly separate initial and final states.
- Particles within each state are ordered by charge: `+`, `-`, `0`.
- Antiparticles: particle name + `Bar` suffix (e.g., `B0Bar`). Exception: charged particles use their charge directly (`W-` not `WBar`).
- Neutrinos: no flavor indicator — always `nu` or `nuBar`.
- Multi-step processes use multiple `2` separators: `p.p.2.W+.2.mu+.nu`.
- Intermediate resonances decaying to dileptons: `(2.l+.l-)` suffix, e.g., `B0.2.Kst0.J/psi(2.l+.l-)`.

Examples:
| LaTeX | Symbol |
|-------|--------|
| $B^0 \to K^{*0} \mu^+ \mu^-$ | `B0.2.Kst0.mu+.mu-` |
| $B^+ \to K^+ \mu^+ \mu^-$ | `B+.2.K+.mu+.mu-` |
| $\bar{B}^0 \to e^+ e^-$ | `B0Bar.2.e+.e-` |
| $pp \to Z \to \mu^+ \mu^-$ | `p.p.2.Z.2.mu+.mu-` |

Full particle table → `references/obs-abbr.md` §1.

### Observable Naming: `OBS(transition)[condition]`

- **OBS**: symbolic abbreviation only (e.g., `Br`, `FL`, `ACP`). Never write full expression definitions.
- **transition**: the `A.B.2.C.D` symbol from above.
- **condition**: optional qualifier in square brackets, used ONLY for multi-transition ratios (e.g., `[mu/e]` for lepton flavor universality tests). Not used for different q² bins of the same observable.

**Special patterns:**
- Observable differences: `DeltaOBS(transition)[condition]`, LaTeX: `$\Delta_{OBS}^{condition}(transition)$`
- Observable ratios: `ROBS(transition)[condition]`, LaTeX: `$R_{OBS}^{condition}(transition)$`
- CKM parameters $r$ and $\delta$: the B meson and final-state meson carry negative charge in the transition (e.g., `B-.2.D0.K-`).

Full observable table → `references/obs-abbr.md` §2–3.

### Numeric Format

- **All values are strings**: `"0.69"` not `0.69`. This includes `value`, `q2min`, `q2max`, all error fields, and `unit`. Exception: correlation/covariance matrix elements are floats.
- **Component errors preferred**: When a paper reports separate statistical and systematic errors, record each as a separate `type@N_err` group. Do NOT pre-combine them into a total error.
- **Symmetric errors**: `err_up` = `err_down` (both required even when equal).
- **Upper limits**: `type@N_upper_limit` = numeric value (string), `type@N_level` = confidence level (e.g., `"90%@CLs"`). Do not swap these fields. Do NOT use `err_up` for limits.
- **Single boundary**: If only one kinematic boundary exists (e.g., $q^2 > 14.0$ GeV²), fill the other with the literal string: `"q2min": "14.0"`, `"q2max": "q2max"`.
- **unit**: Fill only for dimensional observables (e.g., `"unit": "GeV"`, `"unit": "ps"`). Dimensionless observables omit this field entirely.
- **LaTeX escaping**: Use `\\to` in JSON files (double backslash). After `json.load()`, this becomes `\to` in Python strings — which is correct.
- **Indentation**: 4 spaces.

### Folder Naming

- Experimental folders use the collaboration name: `Experimental/LHCb/`, `Experimental/ATLAS/`, `Experimental/CMS/`, `Experimental/BaBar/`, `Experimental/Belle/`, `Experimental/PDG/`, `Experimental/HFLAV/`, `Experimental/LEP/`.
- Theoretical folders use just the group name: `Theoretical/HPQCD/`, `Theoretical/RBC-UKQCD/`.
- **Data files and index filenames always use only the collaboration name**: `LHCb:2015svh.json`, `LHCb@2015.json`.

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
| `tot_correlation` instead of `type@1_correlation` | Use `type@N_correlation` matching the error type label |
| Matrix dimension mismatch with obs count | Ensure matrix size = number of obs@N in the same entry |
| Using author-level texkey for filenames | Always use the collaboration-level texkey (e.g., `LHCb:2015svh` not `Aaij:2015oid`) |
| Double-escaping LaTeX (`\\\\to` instead of `\\to`) | Use single double-backslash `\\to` in the JSON file text |

## JSON Example

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

## Required Tools

| Tool | Purpose | Path / URL | Notes |
|------|---------|-----------|-------|
| arXiv API | Metadata: v1 date, title, abstract, primary category | `https://export.arxiv.org/api/query` | Atom XML format |
| InspireHEP API | Metadata: texkey, recid, collaboration, DOI | `https://inspirehep.net/api/literature` | JSON format, needs `Accept` header |
| hepdata-cli | Machine-readable HEPData (bypasses Cloudflare) | `/hepdata-cli` | Binary, not a Python package |
| pymupdf | PDF text extraction | `/python/site-packages` | Run via terminal, not execute_code |
| web-search / web-extract | Supplementary web content | — | Built-in tools |
| vision_analyze | Table image extraction | — | Built-in tool |
| terminal | Run Python scripts and shell commands | — | Built-in tool |
