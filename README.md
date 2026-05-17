# flav-data

A structured, machine-readable database of flavor physics measurements.

## Overview

**flav-data** curates experimental and theoretical results in flavor physics — branching fractions, angular observables, CP asymmetries, lepton flavor universality ratios, form factors, and more — into standardized JSON entries following a consistent naming convention and format specification.

The database covers measurements from **1995** to the present, organized by collaboration/theory group and indexed by year.

## Supported Groups

### Experimental

| Collaboration | Scope |
|---------------|-------|
| **LHCb** | B-physics, charm, electroweak at LHC |
| **ATLAS** | Higgs, B-physics, electroweak |
| **CMS** | Higgs, B-physics, electroweak |
| **Belle** | B-physics, τ physics at KEKB |
| **BaBar** | B-physics at PEP-II |
| **BESIII** | Charm, τ physics at BEPCII |
| **CDF** | B-physics at Tevatron |
| **D0** | B-physics at Tevatron |
| **HFLAV** | Heavy Flavor Averaging Group combinations |
| **LEP** | Electroweak precision at LEP |
| **PDG** | Particle Data Group world averages |

### Theoretical

| Group | Scope |
|-------|-------|
| **HPQCD** | Lattice QCD calculations |

## Data Format

Each paper corresponds to one JSON file with the following structure:

```json
{
    "inspire-hep": "[LHCb:2015svh](https://inspirehep.net/literature/1409497)",
    "author": "Aaij, Roel and others",
    "collaboration": "LHCb",
    "title": "Angular analysis of the $B^{0}\\to K^{*0}\\mu^{+}\\mu^{-}$ decay",
    "arxiv": "[hep-ex/1512.04442v1](https://arxiv.org/pdf/1512.04442)",
    "time": "2015.12.14",
    "abstract": "...",
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
            "type@1_correlation": [[1.0, 0.06, ...], ...]
        }
    ],
    "transition-mode": "semileptonic decay"
}
```

### Key Design Principles

| Principle | Rule |
|-----------|------|
| Numeric values | All strings: `"0.69"` not `0.69` |
| Errors | Component-level (`stat`, `syst`) preferred |
| Matrices | Float arrays at data entry level, diagonal = 1.0 for correlation |
| LaTeX | Double-backslash escaping: `\\to` in JSON → `\to` in Python |
| Indentation | 4 spaces |
| Empty fields | Omit key entirely (except `arxiv` which uses `null`) |

## Naming Convention

### Transition Symbol: `A.B.2.C.D`

Represents $A + B \to C + D$ with `2` replacing the arrow.

| Rule | Example |
|------|---------|
| Charge ordering: `+` → `-` → `0` | `B+.2.K+.mu+.mu-` |
| Antiparticles: name + `Bar` | `B0Bar.2.e+.e-` |
| Charged particles: use charge directly | `W-.2.mu-.nuBar` |
| Neutrinos: no flavor tag | `nu`, `nuBar` |
| Multi-step: additional `2` separators | `p.p.2.Z.2.mu+.mu-` |

### Observable Name: `OBS(transition)[condition]`

| Component | Description |
|-----------|-------------|
| `OBS` | Symbolic abbreviation (`Br`, `FL`, `ACP`, `R`, ...) |
| `transition` | The `A.B.2.C.D` transition symbol |
| `condition` | Optional qualifier for multi-transition observables (`[mu/e]`) |

**Special patterns:**
- Differences: `DeltaOBS(transition)[condition]` → $\Delta_{OBS}^{condition}(transition)$
- Ratios: `ROBS(transition)[condition]` → $R_{OBS}^{condition}(transition)$
- CKM parameters: `r(B-.2.D0.K-)`, `delta(B-.2.D0.K-)`

### Observable Categories

| Category | Abbreviations |
|----------|---------------|
| Branching fractions | `Br`, `dBr/dq2`, `Gamma` |
| Lifetimes | `Tau` |
| Masses | `Mass`, `mass`, `DeltaMass` |
| Cross sections | `Sigma`, `dSigma/dpT`, `dSigma/deta` |
| Angular coefficients | `FL`, `S3`–`S9`, `AFB`, `FH` |
| CP asymmetries | `ACP`, `DeltaACP`, `A3`–`A9`, `SigmaAFB`, `DeltaAFB` |
| Optimized (P) | `P1`–`P3`, `P4p`, `P5p`, `P6p`, `P8p` |
| LFU differences (Q) | `QFL`, `Q1`–`Q6`, `Q8` |
| Ratios | `R`, `r` |
| CKM parameters | `gammaCKM`, `r`, `delta` |

## Directory Structure

```
flav-data/
├── Experimental/
│   ├── LHCb/
│   │   ├── LHCb.py                  # Streamlit dashboard
│   │   ├── 2015/
│   │   │   ├── LHCb@2015.json       # Annual index
│   │   │   └── 12/
│   │   │       └── LHCb:2015svh.json  # Data file
│   │   └── 2025/
│   │       └── ...
│   └── ATLAS/, CMS/, Belle/, ...
├── Theoretical/
│   └── HPQCD/
│       └── ...
├── Observable/
│   ├── Flavor.py                    # Observable naming guide
│   └── EWPO.py                      # EWPO naming guide
├── main.py                          # Streamlit app entry
├── home.py                          # Homepage
├── flav_dashboard.py                # Dashboard component
└── defs.py                          # Shared definitions
```

### Index File Format

Annual index files (`LHCb@2025.json`) map months to file IDs:

```json
{
    "03": ["LHCb:2025xyz"],
    "06": ["LHCb:2015svh"],
    "12": ["LHCb:2015abc", "LHCb:2015def"]
}
```

## Streamlit App

Run the interactive database viewer:

```bash
cd flav-data
streamlit run main.py
```

### Pages

| Page | Content |
|------|---------|
| **Home** | Database overview, format specification, statistics |
| **Observable** → Flavor | Transition symbols, particle table, observable abbreviations |
| **Observable** → EWPO | Electroweak precision observable definitions |
| **Experimental** → [Group] | Interactive dashboard with timeline, filters, data export |
| **Theoretical** → [Group] | Theory group results browser |

## Contributing

See [`flav-data-importer/`](flav-data-importer/) for the complete import workflow, format specification, and validation scripts.

### Quick Start for Importing

1. **Search** — Check if the paper already exists in the annual index
2. **Retrieve** — Get metadata from InspireHEP API and arXiv API
3. **Extract** — Get data from HEPData (preferred), CDS, LHCb public pages, or PDF
4. **Build** — Construct JSON following `references/json-meta.md`
5. **Validate** — Run `python3 flav-data-importer/scripts/json-valid.py <file.json>`
6. **Index** — Update the annual index file

### Scope

| Supported | Not Supported |
|-----------|---------------|
| Experimental measurements (LHCb, CMS, ATLAS, Belle, BaBar, BESIII, ...) | Phenomenological fits of theoretical parameters |
| Theoretical calculations (HPQCD, RBC/UKQCD, ...) | Conference papers without arXiv/journal version |
| arXiv preprints and peer-reviewed papers | Informal non-peer-reviewed results |

## License

This database is maintained for research purposes. Please cite the original papers when using data from this repository.
