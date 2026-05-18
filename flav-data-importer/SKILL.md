---
name: flav-data-importer
description: Extract structured flavor physics data from papers and save as flav-data standard JSON. Use this skill when importing, updating, deleting, or verifying data from a paper or website.
category: data-science
tags: [flavor-physics, data-collecting, json-importer, hepdata]
---

# flav-data Importer

Extract structured data from flavor physics papers into the flav-data standard JSON format. Covers the complete lifecycle: discovery → extraction → validated JSON → index maintenance.

## Directory

```
flav-data-importer/
├── SKILL.md                    # Workflow, conventions, pitfalls
├── references/
│   ├── json-meta.md            # JSON field spec (authority)
│   ├── obs-abbr.md             # Transition symbols, observable naming, LaTeX
│   ├── file-index.md           # Directory layout, indexing
│   ├── data-source.md          # Source priority, scope
│   ├── arxiv-api.md            # arXiv API usage
│   ├── inspirehep-api.md       # InspireHEP API usage
│   └── hepdata-cli.md          # HEPData CLI usage
├── scripts/
│   ├── arxiv-ext.py            # arXiv metadata + PDF download
│   ├── inspirehep-ext.py       # InspireHEP metadata
│   ├── hepdata-ext.py          # HEPData table extraction
│   └── json-valid.py           # JSON validation (12 checks)
└── assets/
    └── workflow-lhcb-2015svh.md # Full import example
```

## Tool Inventory

| Tool | Use |
|------|-----|
| **arXiv API** | v1 date, title, abstract, primary category, PDF URL → `scripts/arxiv-ext.py` |
| **InspireHEP API** | TexKey, recid, collaboration, DOI, authors → `scripts/inspirehep-ext.py` |
| **hepdata-cli** | Machine-readable HEPData (bypasses Cloudflare). Installed in Hermes venv. → `scripts/hepdata-ext.py` |
| **pymupdf** | PDF text extraction (fallback data source) |
| **vision_analyze** | Table screenshot extraction |

## Scope

| Supported | Not Supported |
|-----------|--------------|
| Experimental measurements (LHCb, CMS, ATLAS, Belle, BaBar, BESIII, etc.) | Phenomenological fits to experimental data |
| Theoretical calculations (HPQCD, RBC/UKQCD, FNAL/MILC, etc.) | Conference/report papers |
| arXiv preprints and journal papers | Informal non-peer-reviewed results |

**Rules:**
- For unsupported data: reply "This data is not supported for import" or find the formal paper on arXiv/InspireHEP.
- Multiple arXiv papers for one measurement → single JSON, retain all Inspire/arXiv IDs and DOIs.
- Multi-collaboration measurements → fill data for all involved groups under their respective directories.

## Workflow

### Step 1: File Search

1. Query InspireHEP API for TexKey and recid → `references/inspirehep-api.md`
2. Search database index by TexKey → `references/file-index.md`
3. **Decision**: exists → compare versions; not found → Step 2

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
1. Build path per `references/file-index.md` — `Lab-Collaboration` folders, collaboration-only filenames
2. `mkdir -p Experimental/CERN-LHCb/2015/12`
3. Determine transition symbol + observable naming → `references/obs-abbr.md`
4. Build JSON metadata → `references/json-meta.md`
5. Extract values and populate JSON
6. Write JSON to month subdirectory
7. Update annual index at `Experimental/CERN-LHCb/2015/LHCb@2015.json`

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
- Antiparticles: neutral mesons = `B0Bar`; baryons = `Lambdac+Bar` (Bar at **end** after charge); charged mesons/leptons use charge only (`B+`/`B-`)
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
- **Component errors preferred**: `type@N_err_up`/`_down` + `type@N_err` label. Never pre-combine.
- **Total error** (no stat/syst breakdown): `tot_err_up`/`tot_err_down`
- **Symmetric errors**: `err_up` = `err_down` (both required)
- **Upper limits**: `type@N_upper_limit` = value, `type@N_level` = `"90%@CLs"`. Do NOT swap.
- **Single boundary**: literal `"q2min"` or `"q2max"`
- **unit**: only dimensional observables; omit for dimensionless
- **LaTeX in JSON**: double backslash (two backslash characters) in JSON file text; Python reads single backslash after json.load()
- **Indentation**: 4 spaces

### Data Entry Whitelist

Each `data[]` element may contain ONLY: `obs@N`, `type@N_correlation`, `type@N_covariance`, `tot_correlation`, `tot_covariance`. Matrix naming matches error type: component = `type@N_*`, total = `tot_*`.

### Folder Naming

`Lab-Collaboration` (实验室-实验组, institution-based):
`Experimental/CERN-LHCb/`, `Experimental/CERN-ATLAS/`, `Experimental/SLAC-BaBar/`, `Experimental/KEK-Belle/`, `Experimental/IHEP-BESIII/`, `Experimental/Fermilab-CDF/`, `Experimental/CERN-LEP/`, `Experimental/HFLAV/`, `Experimental/PDG/`.
Theoretical: `Theoretical/HPQCD/`, `Theoretical/RBC-UKQCD/`.
Data files always use collaboration name only: `LHCb:2015svh.json`.

## Common Pitfalls

| Pitfall | Correct |
|---------|---------|
| `[condition]` for q² bins | Separate `data[]` entries with `q2min`/`q2max` |
| Guessing TexKey for `ref` | Search arXiv ID → InspireHEP for verified TexKey |
| `type@1_err` missing when `_up`/`_down` present | Add `type@1_err` label (e.g., `"stat"`) — all three are required |
| `upper_limit` and `level` swapped | `upper_limit` = numeric, `level` = confidence string |
| Non-property transition-mode (`"rare decay"`) | Property-based: `"semileptonic decay"`, `"leptonic decay"`, `"scattering"` |
| Annual index with outdated texkey | Verify latest texkey on InspireHEP before writing index |
| Empty fields as empty strings | Omit key entirely; only `arxiv` uses `null` |
| `year` field present | Not supported — remove |
| `tot_correlation` with component errors | Use `type@N_correlation` matching the error type label |
| Matrix dimension ≠ obs count | Matrix N×N must equal number of obs@N in that entry |
| Author-level texkey for filenames | Collaboration-level only: `LHCb:2015svh` |
| Single backslash in JSON LaTeX | Two backslash characters required in JSON file text |
| Author name with initials | Full first name: `"Aaij, Roel and others"` |
| Abstract starting lowercase | Match arXiv exactly; typically capital |
| Hyphenated transition-mode | No hyphens: `"semileptonic decay"` |
| `unit` field as empty string | Omit for dimensionless observables |
| Custom fields in data entries | Only `obs@N`, `*_correlation`, `*_covariance` allowed |
| `transition-mode` not last | Must be the final key in JSON |
| Observable name includes q² bin | `name` = `OBS(transition)[condition]`; q² bins → `q2min`/`q2max` |
| arXiv link missing version | `[hep-ex/1512.04442v1](https://arxiv.org/pdf/1512.04442)` |
| Correlation diagonal ≠ 1.0 | It's a covariance matrix → `*_covariance` |
| Anti-baryon `Bar` before charge (`LambdacBar-`) | `Bar` at end: `Lambdac+Bar`, `Lambdab0Bar`, `Sigma-Bar` |
| Charge ordering wrong (`tau-.2.mu-.mu+.mu-`) | Final state ordered `+`, `-`, `0`: `tau-.2.mu+.mu-.mu-` (validator does NOT check this) |

### Matrix Format

```json
"type@1_correlation": [
    [1.0, 0.06, 0.02],
    [0.06, 1.0, 0.03],
    [0.02, 0.03, 1.0]
]
```

- `*_correlation`: diagonal = 1.0, off-diagonal ∈ [-1, 1]
- `*_covariance`: diagonal = error², off-diagonal = covariance
- Compact row-per-line; matrix elements are floats

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
            "obs@2": { "...": "..." },
            "type@1_correlation": [[1.0, 0.06], [0.06, 1.0]]
        }
    ],
    "transition-mode": "semileptonic decay"
}
```

Full specification → `references/json-meta.md`
