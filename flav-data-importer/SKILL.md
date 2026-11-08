---
name: flav-data-importer
description: Import flavor-physics measurement data from arXiv, InspireHEP, and HEPData into the flav-data JSON format. Use for the full lifecycle, i.e., metadata lookup, HEPData extraction, transition-symbol and observable-name construction, JSON schema validation, and paper-index maintenance.
license: MIT
category: data-science
tags: [flavor-physics, data-collecting, json-importer]
---

# flav-data Importer

Extract structured flavor-physics data from arXiv, InspireHEP, and HEPData into the `flav-data` standard JSON format. One JSON file per paper with single or multiple collaborations under `expe-data/<Lab>-<Collaboration>/<year>/<month>/<Collaboration>:<TexKey>.json`, with annual index files alongside. Covers the full lifecycle: discovery → extraction → validation → index maintenance.

This is **not** a fit tool. It produces JSON inputs consumed by downstream fitting tools.

## Directory

```text
flav-data-importer/
├── SKILL.md                    # Workflow, conventions, pitfalls (this file)
├── references/                 # Authority documents
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

## Requirements

- Python 3.10+
- `hepdata-cli`: `pip install hepdata-cli` (HEPData access)
- `pymupdf`: `pip install pymupdf` (PDF fallback extraction)
- `pyyaml`: `pip install pyyaml` (HEPData YAML parsers)

arXiv and InspireHEP APIs are unauthenticated and rate-limited
(~1 req/3s and ~2 req/s respectively).

## Python Helpers

Run from the project root; helper modules are loaded from `flav-data-importer/scripts/`:

```python
import importlib.util
from pathlib import Path

scripts = Path("flav-data-importer/scripts")

def load_script(name):
    spec = importlib.util.spec_from_file_location(name, scripts / f"{name.replace('_', '-')}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

common = load_script("common")
unicode_to_latex = common.unicode_to_latex
to_bibtex = common.to_bibtex

# Unicode → LaTeX (Greek/math + typographic replacements)
unicode_to_latex("B⁰ → K*⁰ μ⁺μ⁻")   # → "B^{0} \\to K*^{0} \\mu^{+}\\mu^{-}"

# Author name → BibTeX initials
to_bibtex("Aaij, Roel")               # → "Aaij, R."
```

## Tool Inventory

### External APIs / CLIs

| Tool | Use |
|------|-----|
| **arXiv API** | v1 date, title, abstract, primary category, PDF URL, ancillary/source files → `references/arxiv-api.md` |
| **InspireHEP API** | TexKey, recid, collaboration, DOI, authors → `references/inspirehep-api.md` |
| **hepdata-cli** | Machine-readable HEPData. Install: `pip install hepdata-cli` → `references/hepdata-cli.md` |
| **pymupdf** | PDF text extraction (fallback data source) |
| **Image reading** | Table screenshots and PDF page images, read with the agent's image tool |

### Local scripts

| Script | Use |
|--------|-----|
| `scripts/common.py` | Unicode → LaTeX mapping + BibTeX author-name conversion (`to_bibtex`, `format_authors`). Imported by every other script. |
| `scripts/arxiv-ext.py` | arXiv API metadata + PDF and e-print source download (`--source` lists ancillary data files). `python3 flav-data-importer/scripts/arxiv-ext.py 1512.04442`. |
| `scripts/inspirehep-ext.py` | InspireHEP API metadata. `python3 flav-data-importer/scripts/inspirehep-ext.py --arxiv-id 1512.04442`. |
| `scripts/hepdata-ext.py` | HEPData table extraction (YAML parsing, q² pairing, matrix detection). `python3 flav-data-importer/scripts/hepdata-ext.py <inspire_id>`. |
| `scripts/json-valid.py` | JSON schema validator (standard + auto-detected HFLAV/PDG snapshots). `python3 flav-data-importer/scripts/json-valid.py <file>`. |

## Scope

| Supported | Not Supported |
|-----------|--------------|
| Experimental measurements (LHCb, CMS, ATLAS, Belle, BaBar, BESIII, etc.) | Conference/report papers (no formal preprint) |
| Published experimental combinations and HFLAV/PDG snapshots | Global analyses: Wilson-coefficient fits, CKM/parameter determinations, mass or coupling bounds, world averages |
| Theoretical calculations (HPQCD, lattice QCD, perturbative QCD, etc.) | Unpublished results, theses |
| Multi-collaboration papers | Internal notes (CDS restricted) |

Form-factor parametrization fits (`aN_FF` coefficients plus a group-level
`scheme`) are primary theory data and **are** imported, even when they
combine lattice, LCSR, and experimental input. The exclusion above covers
global analyses that reinterpret existing measurements, not the
parametrization of a form factor. See `references/data-source.md` §Scope.

## Workflow

### Step 1: Discovery

**Always start by searching for an existing entry** in the paper index.
This prevents duplicates and tracks the version history of each measurement.

1. Check if the file already exists. New imports go to `<year>/<month>/`,
   but legacy files may sit directly under `<year>/`, so search both depths:
   ```bash
   find expe-data/CERN-LHCb -mindepth 2 -maxdepth 3 -name 'LHCb:2015svh.json'
   ```
2. If found, **compare versions**:
   - `arxiv` field has same arXiv ID → no action
   - `arxiv` field has new version → update metadata + data, bump index
   - `arxiv` field has different ID → different paper, create new entry
3. If not found, proceed to Step 2.

**Index files** (`expe-data/<Lab>-<Collaboration>/<year>/<Collaboration>@<year>.json`)
list every paper in that directory. Rebuild the index after any add/remove.
See `references/file-index.md`.

### Step 2: Data Operations

Choose one based on user intent:

#### 2.1 Add a new paper

Run the following Python from the project root. The scripts use hyphenated filenames, so load them by path:

```python
import importlib.util
from pathlib import Path

scripts = Path("flav-data-importer/scripts")

def load_script(name):
    spec = importlib.util.spec_from_file_location(name, scripts / f"{name.replace('_', '-')}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

inspirehep_ext = load_script("inspirehep_ext")
arxiv_ext = load_script("arxiv_ext")
hepdata_ext = load_script("hepdata_ext")
common = load_script("common")
```

1. **Look up InspireHEP** by arXiv ID, TexKey, or recid:
   ```python
   hit = inspirehep_ext.get_inspire_by_arxiv('1512.04442')
   meta = inspirehep_ext.extract_metadata(hit)
   ```
   The metadata dict uses `recid` for the record ID and contains the TexKey,
   title, authors, collaboration, DOI, journal reference, and related fields.

2. **Look up arXiv** for versioned PDF URL + primary category:
   ```python
   arxiv = arxiv_ext.get_arxiv_info('1512.04442')
   ```
   This gives `primary_category` (e.g. `hep-ex`) + `arxiv_id_with_version`
   (e.g. `1512.04442v1`) needed for the canonical arXiv Markdown link.

3. **Extract data from HEPData** (machine-readable):
   ```python
   tables = hepdata_ext.fetch_table_names(meta['recid'])
   for table in tables:
       yaml_text = hepdata_ext.download_table_yaml(meta['recid'], table)
       table_type = hepdata_ext.detect_table_type(yaml_text)
       if table_type in ('correlation', 'covariance'):
           matrix_type, matrix, qualifiers = hepdata_ext.parse_yaml_correlation(yaml_text)
       else:
           observables, qualifiers = hepdata_ext.parse_yaml_observables(yaml_text)
   ```
   Table names (`"Table 9"`) carry no type information — always use
   `detect_table_type()` rather than the name. Each observable data point
   carries its own `q2min`/`q2max` (pairing is positional with
   `independent_variables`), so one q² bin becomes one group in the
   `data` array, holding that channel's observables.
   If HEPData is unavailable or incomplete, check the arXiv ancillary files
   before falling back to the PDF: download the e-print package with
   `arxiv_ext.download_source(arxiv_id, output_dir)`, use any machine-readable
   data file (`.dat`/`.txt`/`.csv`/`.json`/`.yaml`) as the primary source, and
   validate its numbers against the paper's own tables. Only when no ancillary
   data exists, extract from the e-print LaTeX source (preferred over the PDF)
   and cross-check each table. See `references/data-source.md` §4 and
   `references/arxiv-api.md` "Ancillary Files".

4. **Write the JSON file** at the canonical path. The full assembly:

   ```python
   unicode_to_latex = common.unicode_to_latex

   meta = inspirehep_ext.extract_metadata(hit)
   json_doc = {
       # ----- from inspirehep-ext (extract_metadata) -----
       "inspire-hep":     meta["inspire_hep_link"],     # Markdown link "[TexKey](url)"
       "author":          meta["author_str"],            # BibTeX form, see SKILL.md rule 3
       # Named collaborations only; omit this key entirely for
       # individual/small-group papers (SKILL.md rule 8).
       "collaboration":   meta["collaboration"],
       "title":           meta["title"],                 # already Unicode→LaTeX
       "abstract":        meta["abstract"],             # already Unicode→LaTeX
       # ----- from arxiv-ext (get_arxiv_info) -----
       "arxiv":           arxiv["arxiv_link"],          # Markdown link [primary_category/arxiv_idvN](url)
       "time":            arxiv["time"],                 # "YYYY.MM.DD" (v1 submission date)
       # ----- human-picked (per references/json-meta.md §"transition-mode Values") -----
       "transition-mode": "semileptonic-decay",          # hyphenated whitelist
       "data": [
           {
               # each group maps one or more transition channels to an
               # obs@N object, then optionally one group-level matrix
               "B0.2.K*0.mu+.mu-": {
                   # for each obs@N:
                   #   "name":  "FL"                    # symbol only; channel is the group key
                   #   "value": "0.69"
                   #   "type@1_error": "stat"
                   #   "type@1_upper": "0.035"
                   #   "type@1_lower": "0.036"
                   # optionally: "q2min": "0.1", "q2max": "1.1", etc.
               },
               # optional; rows align with channel order, then obs@N order:
               # "correlation": [[1.0, 0.5], [0.5, 1.0]]
           }
       ],
   }
   ```

   `data` is an array of data groups. Each group keys one or more
   transition channels (`A.B.2.C.D`, or `no-transition` for basic
   observables such as `MZ` or `Tau(B0)`) to their observables, and may
   carry a group-level `correlation`/`covariance` matrix. Channels that
   share a matrix belong to the same group; add another element when the
   dataset, scheme, fit choice, kinematic bin, or matrix differs.
   See rules 6 and 7 below and `references/json-meta.md` §"Data Entries".

   Field-source priorities when there are two candidates:
   - **Title / Abstract**: InspireHEP preferred (LaTeX-preserved);
     fall back to arXiv only if InspireHEP lacks the paper.
   - **Author**: Always from InspireHEP; apply `to_bibtex()` to each
     full name, then arrange by author count per SKILL.md rule 3.

#### 2.2 Update an existing paper

Diff the new metadata against the stored JSON. Update only changed fields.
If a new arXiv version supersedes an old one, bump the `arxiv` field's
version suffix and the annual index entry.

#### 2.3 Delete a paper

Remove the JSON file **and** update the annual index. Don't leave orphan
references in any index file.

#### 2.4 Verify

```bash
python3 flav-data-importer/scripts/json-valid.py <file>
```

Runs the standard schema validator. HFLAV and PDG snapshots are
auto-detected by shape: PDG has a top-level `data` dict of `obs@N`
subgroups; HFLAV has top-level `HFLAV@...` subgroup keys containing an
`observables` list. Snapshots are validated against their own relaxed
schema (see `references/json-meta.md` §"Non-Standard Schemas").

For standard files the `data` array of groups is validated strictly
(unknown observable fields, error triplets/labels, one measurement
format, transition match, and particle masses). Every group maps one or
more transition channels to per-channel `obs@N` objects;
its optional matrix dimension must equal the group's total observable
count.

### Step 3: Cleanup

Run these commands from the project root:

```bash
# 1. Validate every changed file
python3 flav-data-importer/scripts/json-valid.py expe-data/CERN-LHCb/2015/LHCb:2015svh.json

# 2. Rebuild the year index if you added or removed papers
# (manual edit; see flav-data-importer/references/file-index.md)

# 3. Confirm the file location (month subdirectory or flat year level)
find expe-data/CERN-LHCb/2015 -mindepth 1 -maxdepth 2 -name 'LHCb:2015svh.json' -print
```

## Core Conventions

These are the 9 hard rules for writing JSON files in this repo. Each
reference doc points back to these.

1. **Matrix format (row-per-line)** — each matrix row on one line:
   ```json
   "correlation": [
       [1.0, 0.5, 0.3],
       [0.5, 1.0, 0.2],
       [0.3, 0.2, 1.0]
   ]
   ```
   Applies to all group-level `*_correlation` and `*_covariance` keys.
   Do **not** put each element on its own line.

2. **Abstract = single line** — Collapse multi-line `align*` / `gather*` /
   etc. blocks to a single-line LaTeX string. Internal line breaks (`\\`)
   become `, ` separators, with `and` before the last equation.

3. **Author format** — use one of these tiers by author count:

   | Author count | Format | Example |
   |---|---|---|
   | **1** | `"Surname, I."` (no "and others") | `"Polchinski, J."` |
   | **2** | Both names joined by "and" | `"Aaij, R. and Smith, J."` |
   | **3** | All names, commas + "and" | `"Aaij, R., Smith, J., and Oyanguren, A."` |
   | **4+** | `"Surname, I. and others"` | `"Aaij, R. and others"` |
   | **Group-only** (no person names) | `"{Collaboration} collaboration"` | `"HPQCD collaboration"` |

   `to_bibtex()` in `scripts/common.py` converts an InspireHEP full name
   (`"Surname, Full First Name"`) → BibTeX initials (`"Surname, I."`).
   For LHCb papers with the standard `Aaij:NNNNNNN` authorship use the
   4+ tier (`"Aaij, R. and others"`).

4. **No Unicode** — replace with LaTeX equivalents:
   `μ`→`\mu`, `Δ`→`\Delta`, `±`→`\pm`, `→`→`\to`,
   `°`→`^{\circ}`, `¯`→`\bar{}`, smart quotes → `` ` ``/`'`/`` `` ``/`''`.
   The mapping lives in `scripts/common.py`: Greek letters and math
   symbols, plus typographic replacements (dashes, smart quotes, Latin
   ligatures, BOM, zero-width space). Characters outside it pass through
   unchanged — convert those by hand.

5. **Transition symbol order** — inside a `data` transition key, the
   transition follows `obs-abbr.md` §1:
   - `.2.` separates the initial state from the final state (repeat it for
     cascades, e.g. `p.p.2.W+.2.mu+.v`).
   - Within each state, order by particle type:
     **baryon → meson → charged lepton → neutral lepton**.
   - Among particles of the same type, order by mass:
     **heaviest → lightest** (e.g. `Lambdab0.2.p.J/psi.pi-`,
     `B0.2.K*0.tau-.e+`).
   - Equal-mass particles of the same type follow charge order:
     **`+` → `-` → `0`** (e.g. `e+.e-`, `mu+.mu-`).
   - A charge is written `+`, `-`, or `0` (`B+`, `B-`, `D*+`); `p`/`m`
     suffixes (`Bp`, `pip`, `ep`) are rejected.
   - Neutral antiparticles append capital `Bar` (`B0Bar`, `K*0Bar`);
     lowercase `bar` is invalid.
   - Particle-name case follows the handwritten symbol: Latin hadrons and
     capital Greek letters stay capital (`B0`, `Lambdab0`, `Sigma-`),
     lower-case Greek letters stay lower case (`pi0`, `rho+`, `phi`);
     lepton symbols keep their conventional case (`e+`, `mu-`, `tau-`).
     Subscripts precede superscripts ($K_S^0$ → `KS0`, $K_L^0$ → `KL0`)
     and superscripts are appended as digits ($\pi^0$ → `pi0`,
     $\Lambda_b^0$ → `Lambdab0`).
   - Neutrinos are written `v`/`vBar`; flavor-specific signatures append
     the flavor (`ve`, `vmu`, `vtau`, `veBar`, ...). `nu`/`nuBar` and
     lowercase-`bar` forms are rejected.

   `json-valid.py` reports non-canonical order as a failure. Every key is
   `A.B.2.C.D`; `no-transition` is the only exception, and a
   multi-transition ratio joins two full keys with `/`
   (`B0.2.K*0.e+.e-/B0.2.K*0.mu+.mu-`). Generic placeholders (`l+`, `q1`)
   and states containing W/Z/γ particles are not order-checked. Mass
   values come from `references/particle-masses.json` (PDG 2024). A
   particle with no mass there is an error for a transition key; add its
   PDG mass (or list it under `non_orderable` when it cannot be ordered)
   before using the transition.

6. **One group per property set** — a data group is a set of observables
   linked by one correlation/covariance matrix and one measurement
   context. Do not merge into one group measurements whose dataset,
   scheme, fit choice, or kinematic region differ; add another element to
   the `data` array instead. In particular, angular observables (`FL`,
   `S3`, `P5p`, ...) and differential widths (`dBr/dq2`, `dGdw`, ...)
   never share a group unless the source matrix genuinely couples them.

7. **`data` is an array of groups** — each group maps one or more
   transition symbols (`A.B.2.C.D`, or `no-transition` for observables
   without a transition) to an `obs@N` object, then optionally a
   group-level `dataset` string naming the data sources, then a `scheme`
   short code for form-factor coefficient groups, then an optional
   group-level matrix. Group keys are ordered channels → `dataset` →
   `scheme` → matrices. JSON data stores no LaTeX for channels or
   observables. Channels that share a matrix belong to the same group;
   separate measurement contexts are separate array elements. The
   channel key alone carries the transition, so observable `name` values
   must **not** repeat it: `FL`, not `FL(B0.2.K*0.mu+.mu-)`. Conditions
   and parameter tags stay in the name (`Q6[mu-e]`, `Vcb(CLN)`); the
   validator rejects an embedded transition. Matrix rows follow the
   channel keys in written order, then each channel's `obs@N` order.

8. **`collaboration` only for named collaborations** — include the key for
   experimental collaborations, HFLAV/PDG, and large theory collaborations
   (HPQCD, JLQCD, RBC/UKQCD, ...). For papers by individual authors or
   small theory groups, omit the key entirely rather than repeating the
   author's surname there.

9. **Form-factor expansion coefficients use `aN_FF`** — `N` is the
   expansion order (0, 1, 2, ...) and `FF` is the form-factor symbol from
   `references/obs-abbr.md` §2.4 (`Fp`, `F0`, `Fv`, `Gp`, `G0`, `Gv`,
   `hp`, `hv`, `fp`, `f0`, `fT`, `V`, `A0`, `A1`, `A12`, `T1`, `T2`,
   `T23`, ...). Examples: `a0_Fp`, `a1_F0`, `a2_Gv`. When one reported
   number applies to several form factors (e.g. both `a0_Gv` and
   `a0_Gp`), write one observable per form factor and repeat its
   value/errors; never join symbols into a name like `a0_Gv_Gp`. Fit
   choices (nominal, higher-order, ...) are neither part of the name nor
   stored in the group metadata; keep such variants as separate groups.
   Every coefficient group declares its expansion form in the group-level
   `scheme` field as a short code: `BGL`, `BCL`, `BSZ`, or `DLM`. The
   full names and defining papers are in `references/obs-abbr.md` §2.4:

   | Scheme | Parametrization | Source |
   |--------|-----------------|--------|
   | `BGL` | Boyd-Grinstein-Lebed | arXiv:hep-ph/9504235 |
   | `BCL` | Bourrely-Caprini-Lellouch | arXiv:0807.2722 |
   | `BSZ` | Bharucha-Straub-Zwicky | arXiv:1503.05534 |
   | `DLM` | Detmold-Lehner-Meinel | arXiv:1503.01421 |

   The JSON stores only the short code; the validator rejects any other
   spelling and rejects a coefficient group without `scheme`.

## Decision Points

**Q: What if the paper has a CERN note number instead of an arXiv ID?**
A: Set `arxiv` to `null`. Use a Markdown link for `inspire-hep`:
`[LHCb-NOTE-2015-001](https://cds.cern.ch/record/1234567)`. The validator
accepts any non-null Markdown link as the `inspire-hep` value.

**Q: What if there's no HEPData entry for this paper?**
A: First check the arXiv ancillary files (e-print package): a machine-readable
data file is the preferred source, and the paper's tables validate it. If none
exists, extract from the e-print LaTeX source (preferred) or the PDF via
`pymupdf`, or by reading table screenshots. An empty `data: []`
fails validation, so a paper with no extractable data must not be committed
until its data is filled in.

**Q: What if the ancillary file and the paper disagree?**
A: Do not import until the difference is explained — it usually means an older
arXiv version or a different fit scenario. If it cannot be resolved, use the
published paper table for the JSON values and note the conflict in the
paper's `abstract`.

**Q: How to handle mixed q² bins across different obs entries?**
A: Each q² bin is its own element of the paper's `data` array, with
`q2min`/`q2max` inside each `obs@N` (observables sharing one matrix may
carry different bins). The `[condition]` syntax is for multi-channel
ratios only (e.g. `RBr[mu/e]`).

## Troubleshooting

### Error: "JSON format correct" but obs fields missing

Run `python3 flav-data-importer/scripts/json-valid.py <file>` and read all
`[FAIL]` lines above the summary. Common ones:

- `obs@N: missing required field: type@1_error` — add a `type@N_error` field
  with one of `stat`, `syst`, `lumi`, `norm`, `theo`, `expe`.
- `obs@N: missing required field: type@1_upper`/`_lower` — paired
  asymmetric error bars; both required if either present.
- `transition-mode: invalid value` — must be one of:
  `leptonic-decay`, `semileptonic-decay`, `non-leptonic-decay`,
  `radiative-decay`, `neutron-beta-decay`, `higgs-decay`, `mixing`,
  `scattering`, `electroweak-precision`, `w-production`,
  `higgs-production`, `low-energy`, `oblique-corrections`
  (see `references/json-meta.md` §"transition-mode Values").
- `matrix not symmetric [i][j] != [j][i]` — fix the matrix entries.
  Re-check the source PDF table for the correct `ij`/`ji` pair.

### Error: "name must not embed the transition channel"

The channel lives in the `data` key. Keep only the observable symbol in
`name`: `FL`, `Br`, `a0_F0`, `dBr/dq2`. Keep a `[condition]` or a
parameter tag when the source reports one (`Q6[mu-e]`, `Vcb(CLN)`), but
never `FL(B0.2.K*0.mu+.mu-)`. **Basic observables** (particle masses,
lifetimes, CKM parameters, EW parameters) use their documented forms:
`Mass(Z)`, `Tau(e-)`, `gammaCKM`, `MZ` (see `references/obs-abbr.md`
§2.1).

### Error: "data must be an array of data groups"

`data` must be an array of **data group** objects, each mapping one or
more transition channels to an `obs@N` object
(`{"B0.2.K*0.mu+.mu-": {"obs@1": {...}, "obs@2": {...}}, "correlation": [...]}`);
each `obs@N` value must itself be an object. See
`assets/workflow-lhcb-2015svh.md` Step 4 for the canonical shape.

### Error: "unknown observable field" / "unknown error label" / "incomplete error triplet" / "single error must be written as the total error"

Per-paper files accept only the documented `obs@N` fields:
`name`, `value`, `unit`, `ref`, `dataset`, `note`,
the kinematic boundaries, `total_upper`/`total_lower`, and the
`type@N_*` keys. Data sources and the expansion scheme are **group-level**
(`"dataset": "..."`, `"scheme": "..."` beside the channel keys), never
inside `obs@N`; fit choices are not stored in the JSON.

A measurement with **exactly one error** records it as the total error
(`total_upper`/`total_lower`) even when the source labels it stat or theo.
Only **two or more** errors become component triplets (`type@N_error` +
`type@N_upper` + `type@N_lower`), each labelled `stat`, `syst`, `lumi`,
`norm`, `theo`, or `expe`. Never mix component errors with total errors,
and never create a lone `type@N` triplet. Confidence-level bounds use
`type@N_upper`/`type@N_lower` with a required `type@N_level` and no
`type@N_error`; a combined fit + bound keeps the bound on N values
distinct from the error components.

### Error: "HEPData 401 / Cloudflare blocked"

Direct `curl` to hepdata.net is blocked. Install `hepdata-cli`:

```bash
pip install hepdata-cli
```

Then re-run `flav-data-importer/scripts/hepdata-ext.py`. The script resolves the binary from
`$PATH`, the active venv, `~/.local/bin/`, or Homebrew prefixes.

### Error: "I have TexKey from InspireHEP but JSON doesn't show it"

The JSON field is `inspire-hep` (a Markdown link whose display text is the
TexKey and whose target is the InspireHEP record URL), not a bare `texkey`
key. Run `inspirehep-ext.py` to get the correct `inspire-hep` value. The
`texkey` itself is embedded in that link.

## Verification Checklist

Before committing any new or updated JSON file:

- [ ] File parses: `python3 flav-data-importer/scripts/json-valid.py <file>` returns no issues (HFLAV/PDG snapshots are auto-detected)
- [ ] `time` field is v1 arXiv submission date in `YYYY.MM.DD` format
- [ ] `arxiv` field is either `null` or a Markdown link with display text `primary_category/<id>v<N>` and target the arXiv PDF URL
- [ ] `inspire-hep` is `[<TexKey>](https://inspirehep.net/literature/<recid>)` with verified TexKey
- [ ] arXiv ancillary files were checked before the PDF; if data came from them, every value was validated against the paper's table
- [ ] `author` follows the 1 / 2 / 3 / 4+ tier rule (initials only)
- [ ] `transition-mode` is immediately before `data`, and `data` is the final top-level key
- [ ] `data` is a non-empty array of groups; each group maps channel keys to an `obs@N` object, then an optional group-level `dataset` string, then a `scheme` string for coefficient groups, then any group matrices; no observable repeats the channel in its `name`, and any group matrix dimension matches the group's observable count
- [ ] Each `obs@N` has `name`, plus exactly one error scheme
      (`value` + `total_upper`/`total_lower` for a single error, or
      `value` + two or more complete `type@N_error`/`_upper`/`_lower`
      triplets), optionally with `ref` and/or confidence bounds; bound-only
      entries carry `type@N_upper`/`type@N_lower` + `type@N_level` and no
      `value` or errors
- [ ] Error labels are one of `stat`, `syst`, `lumi`, `norm`, `theo`, `expe`; only `dataset`, `note` and documented kinematic fields are allowed alongside them; `dataset` and `scheme` are group-level, not per-observable
- [ ] `unit` holds only a physical unit (`GeV`, `ps`, ...); scientific-notation scale factors (`1e-6`, `10^{-4}`) are multiplied into the numbers and the field omitted; `dataset` uses canonical source names (`LQCD`, `LCSR`, `EXPE`)
- [ ] Groups that differ in dataset, scheme, fit choice, or kinematic region are separate elements of the `data` array, not merged
- [ ] Form-factor expansion coefficients use `aN_FF` (`a0_Fp`, `a2_Gv`); a value quoted for several form factors is repeated as one observable per symbol (`a0_Gv`, `a0_Gp`), never joined; fit choices are separate groups, and the group-level `scheme` is one of `BGL`, `BCL`, `BSZ`, `DLM`
- [ ] Matrix fields use row-per-line layout, symmetric for correlation
- [ ] No non-ASCII characters remain (`μ`, `Δ`, `±`, `→`, ligatures, smart quotes)
- [ ] Annual index file includes the new paper if added (or excludes if deleted)

## Known Limitations

1. **No bulk import**. Each paper is imported individually. There's no
   "import all HEPData for collaboration X in year Y" — the user (or a
   wrapping script) iterates by recid.
2. **No auto-update**. There's no watcher that checks for new arXiv
   versions. Re-run `arxiv-ext.py` periodically and diff.
3. **No PDF table extraction**. For paper-only sources, you extract data
   by reading the e-print LaTeX, the PDF (via `pymupdf`), or screenshots.
   Ancillary files are discovered and unpacked by `arxiv-ext.py --source`,
   but their contents are read manually.
4. **No combination building**. Published HFLAV/PDG snapshots are stored
   as they appear; the importer never computes an average itself.
5. **Atomicity is manual**. If you crash between writing the JSON and
   updating the index, you must re-run Cleanup (Step 3) by hand.

## FAQ

**Q: What is the canonical JSON file path?**
A: `expe-data/<Lab>-<Collaboration>/<year>/<month>/<Collaboration>:<TexKey>.json`
(legacy files may sit directly under `<year>/`). For a multi-collaboration
paper, use the primary collaboration's directory and list all groups in
the `collaboration` field (`"LHCb, CMS"`). If no TexKey exists, use
`<Collaboration>:<recid>` as the filename stem and record it in the annual
index.

**Q: Can I import a paper with no arXiv ID (journal-only)?**
A: Yes. Set `arxiv` to `null`. Look up the paper by DOI or title on
InspireHEP and use the InspireHEP-only metadata path.

**Q: How do I name the observable for a branching ratio?**
A: Use `Br`; the decay channel is the enclosing `data` key. For Lepton
Flavor Universality ratios, use `RBr[mu/e]` (R + observable + condition)
under the same channel key.

**Q: What about a CP asymmetry measurement?**
A: Use `ACP` for time-integrated, or `ACP_bplus` for the B+ specific
case; the channel is the `data` key. See `references/obs-abbr.md` §3.

**Q: Why are there `obs@N` suffixes on field names?**
A: To group the observables that share one correlation/covariance matrix
inside a single data group. Different q² bins are **separate**
groups (each with its own `q2min`/`q2max`), not extra `obs@N`
keys. See `assets/workflow-lhcb-2015svh.md` for a worked example.

## See Also

- `assets/workflow-lhcb-2015svh.md` — worked import example (LHCb
  B⁰ → K*⁰ μ⁺μ⁻ angular analysis, arXiv 1512.04442)
- `references/json-meta.md` — full JSON field specification
- `references/obs-abbr.md` — transition symbols and observable naming
- `references/file-index.md` — directory layout and index format
- `references/data-source.md` — source priority and scope decisions
- `references/arxiv-api.md` — arXiv API usage
- `references/inspirehep-api.md` — InspireHEP API usage
- `references/hepdata-cli.md` — HEPData CLI and YAML parsing