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

# Unicode → LaTeX (86 single chars + 8 multi-char sequences)
unicode_to_latex("B⁰ → K*⁰ μ⁺μ⁻")   # → "B^{0} \\to K*^{0} \\mu^{+}\\mu^{-}"

# Author name → BibTeX initials
to_bibtex("Aaij, Roel")               # → "Aaij, R."
```

## Tool Inventory

### External APIs / CLIs

| Tool | Use |
|------|-----|
| **arXiv API** | v1 date, title, abstract, primary category, PDF URL → `references/arxiv-api.md` |
| **InspireHEP API** | TexKey, recid, collaboration, DOI, authors → `references/inspirehep-api.md` |
| **hepdata-cli** | Machine-readable HEPData. Install: `pip install hepdata-cli` → `references/hepdata-cli.md` |
| **pymupdf** | PDF text extraction (fallback data source) |
| **vision_analyze** | Table screenshot and PDF context extractions |

### Local scripts

| Script | Use |
|--------|-----|
| `scripts/common.py` | Unicode → LaTeX mapping (86 single + 8 multi-char) + BibTeX author-name conversion (`to_bibtex`, `format_authors`). Imported by every other script. |
| `scripts/arxiv-ext.py` | arXiv API metadata + PDF download. `python3 flav-data-importer/scripts/arxiv-ext.py 1512.04442`. |
| `scripts/inspirehep-ext.py` | InspireHEP API metadata. `python3 flav-data-importer/scripts/inspirehep-ext.py --arxiv-id 1512.04442`. |
| `scripts/hepdata-ext.py` | HEPData table extraction (YAML parsing, q² pairing, matrix detection). `python3 flav-data-importer/scripts/hepdata-ext.py <inspire_id>`. |
| `scripts/json-valid.py` | JSON schema validator (standard + auto-detected HFLAV/PDG snapshots). `python3 flav-data-importer/scripts/json-valid.py <file>`. |

## Scope

| Supported | Not Supported |
|-----------|--------------|
| Experimental measurements (LHCb, CMS, ATLAS, Belle, BaBar, BESIII, etc.) | Conference/report papers (no formal preprint) |
| Published experimental combinations and HFLAV/PDG snapshots | Fit results, parameter determinations, bounds, and averages produced by theory groups from existing data |
| Theoretical calculations (HPQCD, lattice QCD, perturbative QCD, etc.) | Unpublished results, theses |
| Multi-collaboration papers | Internal notes (CDS restricted) |

## Workflow

### Step 1: Discovery

**Always start by searching for an existing entry** in the paper index.
This prevents duplicates and tracks the version history of each measurement.

1. Check if the file already exists:
   ```bash
   ls "expe-data/CERN-LHCb/2015/12/LHCb:2015svh.json"
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
   If HEPData is unavailable or incomplete, fall back to the PDF + pymupdf.
   See `references/hepdata-cli.md` and `references/data-source.md`.

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
               "B0.2.Kst0.mu+.mu-": {
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
   fit method, kinematic bin, or matrix differs.
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
python3 flav-data-importer/scripts/json-valid.py expe-data/CERN-LHCb/2015/12/LHCb:2015svh.json

# 2. Rebuild the year index if you added or removed papers
# (manual edit; see flav-data-importer/references/file-index.md)

# 3. Find the paper file at its month-directory depth
find expe-data/CERN-LHCb/2015 -mindepth 2 -maxdepth 2 -name 'LHCb:2015svh.json' -print
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
   | **2–3** | List all, BibTeX form, separated by commas + "and" | `"Aaij, R., Smith, J., and Oyanguren, A."` |
   | **4+** | `"Surname, I. and others"` | `"Aaij, R. and others"` |
   | **Group-only** (no person names) | `"{Collaboration} collaboration"` | `"HPQCD collaboration"` |

   `to_bibtex()` in `scripts/common.py` converts an InspireHEP full name
   (`"Surname, Full First Name"`) → BibTeX initials (`"Surname, I."`).
   For LHCb papers with the standard `Aaij:NNNNNNN` authorship use the
   4+ tier (`"Aaij, R. and others"`).

4. **No Unicode** — replace with LaTeX equivalents:
   `μ`→`\mu`, `Δ`→`\Delta`, `±`→`\pm`, `→`→`\to`,
   `°`→`^{\circ}`, `¯`→`\bar{}`, smart quotes → `` ` ``/`'`/`` `` ``/`''`.
   The full mapping in `scripts/common.py` covers 86 single characters
   (Greek/math) plus 8 multi-character sequences (en-dash, em-dash,
   smart quotes, BOM, zero-width space). Characters not in the mapping
   pass through unchanged. The full Unicode→LaTeX mapping is conservative:
   if a character appears in a flav-data JSON that isn't in the mapping,
   convert it by hand.

5. **Transition symbol order** — inside a `data` transition key, the
   transition follows `obs-abbr.md` §1:
   - `.2.` separates the initial state from the final state (repeat it for
     cascades, e.g. `p.p.2.W+.2.mu+.nu`).
   - Within each state, order by particle type:
     **baryon → meson → charged lepton → neutral lepton**.
   - Among particles of the same type, order by mass:
     **heaviest → lightest** (e.g. `Lambdab0.2.p.J/psi.pi-`,
     `B0.2.Kst0.tau-.e+`).
   - Equal-mass particles of the same type follow charge order:
     **`+` → `-` → `0`** (e.g. `e+.e-`, `mu+.mu-`).
   - Neutral antiparticles append `Bar` (`B0Bar`, `Kst0Bar`); hadron
     symbols start uppercase, while leptons and light mesons keep their
     lowercase forms (`e+`, `mu-`, `pi-`, `nu`).

   `json-valid.py` reports non-canonical order as a failure for dotted
   transitions. Generic placeholders (`l+`, `q1`) and states containing
   W/Z/γ particles are not order-checked; compact legacy forms without
   `.2.` remain accepted. Mass values come from
   `references/particle-masses.json` (PDG 2024). A particle with no mass
   there is an error for a transition key; add its PDG mass
   (or list it under `non_orderable` when it cannot be ordered) before
   using the transition.

6. **One group per property set** — a data group is a set of observables
   linked by one correlation/covariance matrix and one measurement
   context. Do not merge into one group measurements whose fit method,
   dataset, or kinematic region differ; add another element to the
   `data` array instead. In particular, angular observables (`FL`, `S3`,
   `P5p`, ...) and differential widths (`dBr/dq2`, `dGdw`, ...) never
   share a group unless the source matrix genuinely couples them.

7. **`data` is an array of groups** — each group maps one or more
   transition symbols (`A.B.2.C.D`, or `no-transition` for observables
   without a transition) to an `obs@N` object, then optionally a
   group-level `method` string shared by every observable in the group,
   then an optional group-level matrix. Group keys are ordered channels
   → `method` → matrices. JSON data stores no LaTeX for channels or
   observables. Channels that share a matrix belong to
   the same group; separate measurement contexts are separate array
   elements. The channel key alone carries the transition, so observable
   `name` values must **not** repeat it: `FL`, not
   `FL(B0.2.Kst0.mu+.mu-)`. Conditions and parameter tags stay in the name
   (`Q6[mu-e]`, `Vcb(CLN)`); the validator rejects an embedded
   transition. Matrix rows follow the channel keys in written order,
   then each channel's `obs@N` order.

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
   choices (nominal, higher-order, ...) belong in the group-level
   `method` field (`"nominal"`, `"higher-order"`), never in the name or
   inside `obs@N`.

## Decision Points

**Q: What if the paper has a CERN note number instead of an arXiv ID?**
A: Set `arxiv` to `null`. Use a Markdown link for `inspire-hep`:
`[LHCb-NOTE-2015-001](https://cds.cern.ch/record/1234567)`. The validator
accepts any non-null Markdown link as the `inspire-hep` value.

**Q: What if there's no HEPData entry for this paper?**
A: Fall back to extracting from the source PDF via `pymupdf` (preferred)
or table screenshots via `vision_analyze`. An empty `data: []` fails
validation, so a paper with no extractable data must not be committed
until its data is filled in.

**Q: arXiv vs InspireHEP — which metadata wins?**
A: arXiv provides version number and PDF URL; InspireHEP provides
authoritative author list and DOI. Use InspireHEP for metadata, arXiv
for PDF.

**Q: How to handle mixed q² bins across different obs entries?**
A: Each q² bin is its own group (an element of that channel's `data`
array) carrying `q2min`/`q2max` (or
per-`obs@N` boundaries when observables within one matrix use different
bins). The `[condition]` syntax is for multi-decay-channel ratios only
(e.g. `RBr[mu/e]` under the channel key).

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
never `FL(B0.2.Kst0.mu+.mu-)`. **Basic observables** (particle masses,
lifetimes, CKM parameters, EW parameters) use their documented forms:
`Mass(Z)`, `Tau(e-)`, `gammaCKM`, `MZ` (see `references/obs-abbr.md`
§2.1).

### Error: "data must be an array of data groups"

`data` must be an array of **data group** objects, each mapping one or
more transition channels to an `obs@N` object
(`{"B0.2.Kst0.mu+.mu-": {"obs@1": {...}, "obs@2": {...}}, "correlation": [...]}`);
each `obs@N` value must itself be an object. See
`assets/workflow-lhcb-2015svh.md` Step 4 for the canonical shape.

### Error: "unknown observable field" / "unknown error label" / "incomplete error triplet"

Per-paper files accept only the documented `obs@N` fields:
`name`, `value`, `unit`, `ref`, `dataset`, `note`,
the kinematic boundaries, `error_upper`/`error_lower`, and the
`type@N_*` keys. Measurement method and fit choice are **group-level**
(`"method": "..."` beside the channel keys), never inside `obs@N`.
Component errors must be a complete `type@N_error`, `type@N_upper`,
`type@N_lower` triplet, and the label must be one of `stat`, `syst`,
`lumi`, `norm`, `theo`, `expe`. Use `error_upper`/`error_lower` for a
single combined error, and never mix component errors with total errors.
`ref` may accompany either scheme, and upper limits may be combined with
a fit result (`value` + errors) or stand alone (limit only).

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
- [ ] `author` follows the 1 / 2–3 / 4+ tier rule (initials only)
- [ ] `transition-mode` is immediately before `data`, and `data` is the final top-level key
- [ ] `data` is a non-empty array of groups; each group maps channel keys to an `obs@N` object, then an optional group-level `method` string, then any group matrices; no observable repeats the channel in its `name`, and any group matrix dimension matches the group's observable count
- [ ] Each `obs@N` has `name`, plus exactly one error scheme
      (`value` + complete `type@N_error`/`_upper`/`_lower` triplets or
      `error_upper`/`error_lower`), optionally with `ref` and/or upper limits;
      upper-limit-only entries carry no `value` or errors
- [ ] Error labels are one of `stat`, `syst`, `lumi`, `norm`, `theo`, `expe`; only `dataset`, `note` and documented kinematic fields are allowed alongside them; `method` is group-level, not per-observable
- [ ] Groups that differ in method, dataset, or kinematic region are separate elements of the `data` array, not merged
- [ ] Form-factor expansion coefficients use `aN_FF` (`a0_Fp`, `a2_Gv`); a value quoted for several form factors is repeated as one observable per symbol (`a0_Gv`, `a0_Gp`), never joined; fit choices are in the group-level `method`
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
   by reading the PDF (or by `pymupdf`/`vision_analyze`). The skill does
   not do automatic table OCR.
4. **No HFLAV combination**. The skill imports raw paper measurements;
   global HFLAV combinations are produced by the downstream fitting tools,
   not by this importer.
5. **Atomicity is manual**. If you crash between writing the JSON and
   updating the index, you must re-run Cleanup (Step 3) by hand.

## FAQ

**Q: What is the canonical JSON file path?**
A: `expe-data/<Lab>-<Collaboration>/<year>/<month>/<Collaboration>:<TexKey>.json`.
For a multi-collaboration paper, use the primary collaboration's directory
and list all collaborations in the `Collaboration` field
(`"LHCb, CMS"`). If HEPData is the only source and no TexKey exists, use
`<Collaboration>:<recid>` as the filename stem and record that in the
annual index.

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

**Q: What if I see `Heisenberg` or other implementation-detail fields?**
A: Those are private to the fitting tools. Don't put them in the flav-data
JSON. The validator will reject unknown top-level fields.

## See Also

- `assets/workflow-lhcb-2015svh.md` — worked import example (LHCb
  B⁰ → K*⁰ μ⁺μ⁻ angular analysis, arXiv 1512.04442)
- `references/json-meta.md` — full JSON field specification
- `references/obs-abbr.md` — transition symbols and observable naming
- `references/file-index.md` — directory layout and index format
- `references/data-source.md` — source priority and scope decisions
- `references/arxiv-api.md` — arXiv API usage
- `references/inspirehep-api.md` — InspireHEP API usage
- `references/hepdata-cli.md` — HEPData CLI usage