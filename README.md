# flav-data

A structured, machine-readable database of flavor physics measurements.

## Overview

**flav-data** curates experimental and theoretical results in flavor physics — branching fractions, angular observables, CP asymmetries, lepton flavor universality ratios, form factors, and more — into standardized JSON entries following a consistent naming convention and format specification.

The database covers measurements from **1990** to the present, organized by collaboration/theory group and indexed by year.

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

Only **HPQCD** is currently registered in `THEOGROUP` and exposed in the
navigation; other theoretical groups' data is not yet wired into the app.
The database stores only experimental measurements and theoretical
calculations — fits, parameter determinations, bounds and theory-group
averages derived from existing data are not ingested. Small calculation
groups are filed under a method folder (`Theoretical/LQCD/`,
`Theoretical/QCD/`) instead of their own group folder.

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
    "transition-mode": "semileptonic-decay",
    "data": [
        {
            "B0.2.Kst0.mu+.mu-": [
                "$B^{0}\\to K^{*0}\\mu^{+}\\mu^{-}$",
                {
                    "obs@1": {
                        "name": "FL",
                        "value": "0.69",
                        "type@1_error": "stat",
                        "type@1_upper": "0.035",
                        "type@1_lower": "0.036",
                        "type@2_error": "syst",
                        "type@2_upper": "0.017",
                        "type@2_lower": "0.017",
                        "q2min": "0.1",
                        "q2max": "1.1"
                    },
                    "obs@2": { ... }
                }
            ],
            "type@1_correlation": [[1.0, 0.06], [0.06, 1.0]]
        }
    ]
}
```

`data` is an array of groups. Each group maps one or more transition
channels to a `[latex, obs@N object]` pair and may carry a group-level
matrix whose rows follow the channel keys, then their `obs@N` order.
The channel LaTeX is written once per channel; observables carry no
`latex`. Add another group for different kinematic bins, fit methods, or
datasets.

### Key Design Principles

| Principle | Rule |
|-----------|------|
| Numeric values | All strings: `"0.69"` not `0.69` |
| Errors | Component-level (`stat`, `syst`) preferred |
| Matrices | Float arrays alongside channel keys in each group, diagonal = 1.0 for correlation |
| LaTeX | One channel-level formula per channel; double-backslash escaping: `\\to` in JSON → `\to` in Python |
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

### Observable Name: `OBS` / `OBS[condition]`

The transition is the `data` key, so `name` carries only the observable
symbol plus optional condition/method tags.

| Component | Description |
|-----------|-------------|
| `OBS` | Symbolic abbreviation (`Br`, `FL`, `ACP`, `R`, ...) |
| `condition` | Optional qualifier for multi-transition observables (`[mu/e]`) |
| `method` | Optional non-transition tag (`Vcb(CLN)`) |

**Special patterns:**
- Differences: `DeltaOBS[condition]` → $\Delta_{OBS}^{condition}$
- Ratios: `ROBS[condition]` → $R_{OBS}^{condition}$
- CKM parameters: `r`, `delta` (under the `B-.2.D0.K-` key)

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
│   ├── CERN-LHCb/
│   │   ├── LHCb.py                 # Streamlit dashboard page
│   │   └── ...                     # Year-indexed data directories
│   ├── HFLAV/
│   │   ├── HFLAV.py               # Snapshot dashboard page
│   │   └── HFLAV@2024.json        # Flat snapshot (year subdirs also supported)
│   ├── PDG/
│   │   ├── PDG.py                 # Snapshot dashboard page
│   │   └── 2024/PDG@2024.json
│   └── ...                         # Other experimental groups
├── Theoretical/
│   ├── HPQCD/                       # Large collaborations: own folder
│   └── LQCD/, QCD/                  # Smaller calculation groups, grouped by method
├── Observable/
│   ├── Flavor.py                    # Observable naming guide
│   └── EWPO.py                      # EWPO naming guide
├── tests/
│   ├── test_importer_regressions.py
│   ├── Experimental/                # Fixture data
│   └── Theoretical/                 # Fixture data
├── main.py                          # Streamlit app entry
├── home.py                          # Homepage
├── flav_dashboard.py                # Dashboard component
└── defs.py                          # Shared definitions
```

The full Lab-Collaboration folder convention is:

| Folder | Lab | Collaboration | Notes |
|--------|-----|---------------|-------|
| `CERN-LHCb` | CERN | LHCb | |
| `CERN-ATLAS` | CERN | ATLAS | |
| `CERN-CMS` | CERN | CMS | |
| `CERN-DELPHI` | CERN | DELPHI | LEP |
| `CERN-OPAL` | CERN | OPAL | LEP |
| `CERN-LEP` | CERN | LEP | Combined LEP (ALEPH+DELPHI+L3+OPAL) |
| `CERN-NA62` | CERN | NA62 | Kaon rare decays |
| `CERN-CHARM-II` | CERN | CHARM-II | Neutrino experiment |
| `KEK-Belle` | KEK | Belle | |
| `KEK-KOTO` | KEK | KOTO | J-PARC |
| `SLAC-BaBar` | SLAC | BaBar | |
| `SLAC-SLD` | SLAC | SLD | |
| `Fermilab-CDF` | Fermilab | CDF | Tevatron |
| `Fermilab-D0` | Fermilab | D0 | Tevatron |
| `Fermilab-Tevatron` | Fermilab | Tevatron | Combined CDF+D0 |
| `Fermilab-Muong-2` | Fermilab | Muong-2 | |
| `IHEP-BESIII` | IHEP | BESIII | Beijing Spectrometer |
| `IHEP-ISTRA+` | IHEP | ISTRA+ | |
| `INFN-KLOE-2` | INFN | KLOE-2 | LNF Frascati DAΦNE |
| `BNL-E949` | BNL | E949 | K+ rare decays |
| `Cornell-CLEO` | Cornell | CLEO | CESR |
| `TRIUMF-PiENu` | TRIUMF | PiENu | |
| `PSI-SINDRUM-II` | PSI | SINDRUM-II | Mu-e conversion |
| `PSI-nTRV` | PSI | nTRV | Neutron trimer |
| `LANL-UCNA` | LANL | UCNA | |
| `NIST-aCORN` | NIST | aCORN | |
| `HFLAV` | — | HFLAV | Aggregation, non-standard schema (uses `run_dashboard`-bypassing custom page) |
| `PDG` | — | PDG | Aggregation, non-standard schema |

### Special cases

- **HFLAV** and **PDG** store data in a non-standard flav-data schema
  (one snapshot JSON per year whose keys are subgroup names containing
  nested observables). They have dedicated Streamlit pages at
  `Experimental/HFLAV/HFLAV.py` and `Experimental/PDG/PDG.py` that bypass
  `run_dashboard`.

The Experimental registry that drives this lives in `defs.py` (`EXPEGROUP`). Each entry is a 2-tuple `(lab, group)` for the default `<Lab>-<Group>` path. A 3-tuple `(lab, group, folder_override)` is supported for groups that need a non-standard parent directory but is currently unused. To add a new group: (1) add the tuple to `EXPEGROUP`, (2) create `Experimental/<folder>/<group>.py` calling `run_dashboard(lab=..., group=...)` (or pass `folder_override=` if needed), (3) drop data into `Experimental/<folder>/<year>/<month>/...` with the standard `<group>@<year>.json` index.

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
| **Experimental** → [Group] | Interactive dashboard with year, month, and transition-mode filters |
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
