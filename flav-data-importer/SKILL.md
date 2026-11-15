---
name: flav-data-importer
description: Import flavor-physics measurement data from arXiv, InspireHEP, and HEPData into the flav-data JSON format. Use for the full lifecycle, i.e., metadata lookup, HEPData extraction, channel-key and observable-name construction, JSON schema validation, and paper-index maintenance.
license: MIT
category: data-science
tags: [flavor-physics, data-collecting, json-importer]
---

# flav-data Importer

Extract structured flavor-physics data from arXiv, InspireHEP, and HEPData into the `flav-data` standard JSON format. One JSON file per paper with single or multiple collaborations: experimental results under `expe-data/<Lab>-<Collaboration>/<year>/<month>/`, theoretical calculations under `theo-data/` (layout in `references/file-index.md`), with annual index files alongside. Covers the full lifecycle: discovery → extraction → validation → index maintenance.

This is **not** a fit tool. It produces JSON inputs consumed by downstream fitting tools.

## Directory

```text
flav-data-importer/
├── SKILL.md                    # Workflow, conventions, pitfalls (this file)
├── references/                 # Authority documents
│   ├── json-meta.md            # JSON field spec (authority)
│   ├── observable-naming.md    # Channel-key ordering, observable naming, LaTeX
│   ├── particle-naming.md      # Internal pid scheme + particle registry
│   ├── file-index.md           # Directory layout, indexing
│   ├── data-source.md          # Source priority, scope
│   ├── arxiv-api.md            # arXiv API usage
│   ├── inspirehep-api.md       # InspireHEP API usage
│   └── hepdata-cli.md          # HEPData CLI usage
├── assets/
│   └── workflow-lhcb-2015svh.md # Paper-specific import notes
└── scripts/
    ├── common.py               # Shared: Unicode→LaTeX, BibTeX, I/O helpers
    ├── arxiv-ext.py            # arXiv metadata + PDF download
    ├── inspirehep-ext.py       # InspireHEP metadata
    ├── hepdata-ext.py          # HEPData table extraction
    └── json-valid.py           # JSON validation
```

## Requirements

- Python 3.10+
- `hepdata-cli`: `pip install hepdata-cli` (HEPData access)
- `pymupdf`: `pip install pymupdf` (PDF fallback extraction)
- `marker-pdf`: `pip install marker-pdf` (optional, scanned-PDF OCR)
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
| **hepdata-cli** | Machine-readable HEPData → `references/hepdata-cli.md` |
| **pymupdf** | PDF text extraction (fallback data source) |
| **marker-pdf** | Scanned-PDF OCR, replaces pymupdf (optional) → `references/data-source.md` §5 |
| **Image reading** | Table screenshots and PDF page images, read with the agent's image tool |

### Local scripts

| Script | Use |
|--------|-----|
| `scripts/common.py` | Unicode → LaTeX mapping, BibTeX author-name conversion (`to_bibtex`, `format_authors`), and shared I/O (`open_url` normalises HTTP/connection failures to `ValueError`; `write_json` writes 4-space-indented JSON, creating parent dirs). Imported by every other script. |
| `scripts/arxiv-ext.py` | arXiv API metadata + PDF and e-print source download (`--source` lists ancillary data files). `python3 flav-data-importer/scripts/arxiv-ext.py 1512.04442`. |
| `scripts/inspirehep-ext.py` | InspireHEP API metadata. `python3 flav-data-importer/scripts/inspirehep-ext.py --arxiv-id 1512.04442`. |
| `scripts/hepdata-ext.py` | HEPData table extraction (YAML parsing, q² pairing, matrix detection). `python3 flav-data-importer/scripts/hepdata-ext.py <inspire_id>`. |
| `scripts/json-valid.py` | JSON schema validator. `python3 flav-data-importer/scripts/json-valid.py <file> [<file> ...] [--quiet]`. |

## Scope

| Supported | Not Supported |
|-----------|--------------|
| Experimental measurements (LHCb, CMS, ATLAS, Belle, BaBar, BESIII, etc.) | Conference/report papers (no formal preprint) |
| Published experimental combinations and HFLAV/PDG world averages | Global analyses: Wilson-coefficient fits, CKM/parameter determinations, mass or coupling bounds |
| Theoretical calculations (HPQCD, lattice QCD, perturbative QCD, etc.) | Unpublished results, theses |
| Multi-collaboration papers | Internal notes (CDS restricted) |

Form-factor parametrization fits (`aN_FF` coefficients plus a group-level
`scheme`) **are** imported, even when they combine lattice, LCSR, and
experimental input; the exclusion above covers global analyses only
(`references/data-source.md` §Scope).

## Workflow

### Step 1: Discovery

**Always start by searching for an existing entry** in the paper index.

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

Run the following Python from the project root, loading the helper
modules as shown in [Python Helpers](#python-helpers):

```python
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
   If HEPData is unavailable or incomplete, unpack the arXiv e-print with
   `arxiv_ext.download_source(arxiv_id, output_dir)`: prefer a
   machine-readable ancillary data file (`.dat`/`.txt`/`.csv`/`.json`/`.yaml`),
   then the LaTeX source, then the PDF, validating every number against the
   paper's own tables (`references/data-source.md` §4,
   `references/arxiv-api.md` §"Ancillary Files and the e-Print Package").

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
               # obs@N object, then optionally the group matrices
               "dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0": {
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
   transition channels (pids joined by `.2.`, or `no-transition` for basic
   observables such as `Mass(Z)` or `Tau(...)`) to their observables, and may
   carry a group-level `correlation`/`covariance` matrix. Channels that
   share a matrix belong to the same group; add another element when the
   dataset, scheme, fit choice, kinematic bin, or matrix differs.
   See rules 6 and 7 below and `references/json-meta.md` §"Data Entries".

   Field-source priorities when there are two candidates:
   - **Title / Abstract**: from InspireHEP, preferring its `source: "arXiv"`
     entry (LaTeX-preserved); fall back to the arXiv API only if InspireHEP
     lacks the paper.
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

Runs the schema validator. The `data` array of groups is validated strictly
(unknown observable fields, error triplets/labels, one measurement
format, and channel-key ordering against the pid registry). Every group
maps one or more transition channels to per-channel `obs@N` objects;
its optional matrix dimension must equal the group's total observable
count.

### Step 3: Cleanup

Run these commands from the project root:

```bash
# 1. Validate every changed file
python3 flav-data-importer/scripts/json-valid.py expe-data/CERN-LHCb/2015/12/LHCb:2015svh.json

# 2. Rebuild the year index if you added or removed papers
# (manual edit; see flav-data-importer/references/file-index.md)

# 3. Confirm the file location (month subdirectory or flat year level)
find expe-data/CERN-LHCb/2015 -mindepth 1 -maxdepth 2 -name 'LHCb:2015svh.json' -print
```

## Core Conventions

These are the 9 hard rules for writing JSON files in this repo.

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

4. **No Unicode** — replace with LaTeX equivalents:
   `μ`→`\mu`, `Δ`→`\Delta`, `±`→`\pm`, `→`→`\to`,
   `°`→`^{\circ}`, `¯`→`\bar{}`, smart quotes → `` ` ``/`'`/`` `` ``/`''`.
   The mapping lives in `scripts/common.py`: Greek letters, math
   symbols, accented Latin letters (author names, e.g. `ć`→`\'{c}`,
   `ç`→`\c{c}`, `ü`→`\"{u}`), plus typographic replacements (dashes,
   smart quotes, Latin ligatures, BOM, zero-width space). `author`,
   `title` and `abstract` are validated Unicode-free. Characters outside
   the mapping pass through unchanged — convert those by hand.

5. **Channel key** — a `data` channel key joins pids with `.` and the
   arrow `.2.` (`no-transition` is the only exception; a ratio joins two
   full keys with `/`). `.2.` separates the initial from the final state
   and repeats for cascades
   (`uud_I1?_1+n_0.uud_I1?_1+n_0.2.WB_I??_1??_0.2.mu_I??_1+n_0.VMU_I??_1+n_0`).
   Within each state, order by
   - particle type: **baryon → meson → charged lepton → neutral lepton**;
   - then mass: **heaviest → lightest**
     (`udb_I0?_1+n_0.2.uud_I1?_1+n_0.cC_I0-_1--_0.Ud_I2-_0-n_0`);
   - then charge for equal masses: **`+` → `-` → `0`**
     (`E_I??_1+n_0.e_I??_1+n_0`).

   The pid grammar (`<core>_<ig>_<jpc>_<serial>`), registry, masses and
   widths are in `references/particle-naming.md`; `json-valid.py` fails an
   unregistered pid or a non-canonical order. Ordering is skipped for the
   placeholders of `particle-naming.md` §2.7 (`l`, `v`, `q`, `Xs`, ...),
   exotics without a registered mass, and nuclei. A mass label, fit
   scenario, or measurement suffix never enters the key — record it in the
   group `note`.

6. **One group per property set** — a data group is a set of observables
   linked by one correlation/covariance matrix and one measurement
   context. Do not merge into one group measurements whose dataset,
   scheme, fit choice, or kinematic region differ; add another element to
   the `data` array instead. In particular, angular observables (`FL`,
   `S3`, `P5p`, ...) and differential widths (`dBr/dq2`, `dGdw`, ...)
   never share a group unless the source matrix genuinely couples them.

7. **`data` is an array of groups** — each group maps one or more
   channel keys (rule 5, or `no-transition` for observables without a
   transition) to an `obs@N` object, then optionally a group-level
   `dataset` string naming the data sources, a `scheme` short code for
   form-factor coefficient groups, a `note`, and the group matrices.
   Group keys are ordered channels → `dataset` → `scheme` → `note` →
   matrices. JSON data stores no LaTeX for channels or observables. The
   channel key alone carries the transition, so observable `name` values
   must **not** repeat it: `FL`, not
   `FL(dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0)`. Conditions
   and parameter tags stay in the name (`DeltaP6p[mu-e]`, `Vcb(CLN)`); the
   validator rejects an embedded transition. Matrix rows follow the
   channel keys in written order, then each channel's `obs@N` order.

8. **`collaboration` only for named collaborations** — include the key for
   experimental collaborations, HFLAV/PDG, and large theory collaborations
   (HPQCD, JLQCD, RBC/UKQCD, ...). For papers by individual authors or
   small theory groups, omit the key entirely rather than repeating the
   author's surname there.

9. **Form-factor expansion coefficients use `aN_FF`** — `N` is the
   expansion order (0, 1, 2, ...) and `FF` is the form-factor symbol from
   `references/observable-naming.md` §2.4 (`F+`, `F0`, `Fv`, `G+`, `G0`, `Gv`,
   `h+`, `hv`, `f+`, `f0`, `fT`, `V`, `A0`, `A1`, `A12`, `T1`, `T2`,
   `T23`, ...). Examples: `a0_F+`, `a1_F0`, `a2_Gv`. When one reported
   number applies to several form factors (e.g. both `a0_Gv` and
   `a0_G+`), write one observable per form factor and repeat its
   value/errors; never join symbols into a name like `a0_Gv_G+`. Fit
   choices (nominal, higher-order, ...) are not part of the name and get
   no dedicated field: keep such variants as separate groups and say
   which is which in the group `note`.
   Every coefficient group declares its expansion form in the group-level
   `scheme` field as a short code: `BK`, `BGL`, `BCL`, `BSZ`, `DLM`, or
   `MR`; the full names and defining papers are in
   `references/observable-naming.md` §2.4. The validator rejects any other
   spelling and rejects a coefficient group without `scheme`.

## Decision Points

**Q: What if the paper has no arXiv ID (CERN note, journal-only)?**
A: Set `arxiv` to `null` and use the InspireHEP-only metadata path — look the
paper up by DOI or title. For a CERN note, `inspire-hep` may link to CDS
instead: `[LHCb-NOTE-2015-001](https://cds.cern.ch/record/1234567)`. The
validator accepts any non-null Markdown link as the `inspire-hep` value.

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
A: `q2min`/`q2max` live inside each `obs@N`. When each bin comes with its
own source matrix (the usual case), each bin is its own element of the
paper's `data` array; observables coupled by one matrix stay in one group
even when their bins differ. A `[condition]` may name the sides of a
comparison or qualify the measurement (`[mu/e]`, `[90%@CL]`, `[13TeV]`), but
never a bin or threshold.

## Troubleshooting

Run `python3 flav-data-importer/scripts/json-valid.py <file>` and read every
`[FAIL]` line above the summary. Each message names the offending key; the
rule it enforces is in `references/json-meta.md` (fields, errors, matrices)
or `references/observable-naming.md` (names and channel keys). Common ones:

- `incomplete error triplet for 'type@1'` — every component error needs
  `type@N_error` + `type@N_upper` + `type@N_lower` together.
- `a single error must be written as the total error` — move the lone
  error to `total_upper`/`total_lower`; `type@N` triplets need two or
  more components.
- `mixes component errors (type@N_error) with total errors` — pick one
  error scheme per observable.
- `transition-mode '...' is not in the allowed list` — pick a hyphenated
  value from `references/json-meta.md` §"transition-mode Values".
- `matrix not symmetric` — re-check the source table for the correct
  `ij`/`ji` pair.
- `is not a registered pid` — register the state in
  `references/particle-naming.md` §3 before using it in a channel key.
- `name must not embed the transition channel` — keep only the symbol
  (`FL`, `Br`, `a0_F0`, `dBr/dq2`), with a `[condition]` or parameter tag
  when the source reports one (`DeltaP6p[mu-e]`, `Vcb(CLN)`). Basic
  observables use their documented forms (`Mass(Z)`, `Tau(...)`,
  `gammaCKM`); see `references/observable-naming.md` §2.1.
- `condition '[...]' is a kinematic bin` — move it to `q2min`/`q2max` or
  `emin`/`emax`, or record the window in the group `note`.
- `ratio symbol '...' embeds the channel` / `a lepton-flavour ratio of
  rates is named 'R'` — write bare `R` and put both full transitions in
  the data key; ratios of other observables keep `ROBS[condition]`
  (`observable-naming.md` §2.2.2, §2.3).
- `empty particle state` — every stage around `.2.` must name at least
  one pid.
- `is not a bare ASCII unit` — no LaTeX, `%` or scale prefix; multiply the
  scale factor into every number (`json-meta.md` §"Standard Measurement
  Format").
- `the inclusive system is '...'` / `must be accompanied by '...'` — the
  final state must follow the parent's $b$ flavour and match the charged
  lepton's charge and flavour (`particle-naming.md` §2.1, §2.7).

**HEPData 401 / Cloudflare blocked** — direct `curl` to hepdata.net is
blocked. `pip install hepdata-cli`, then re-run `hepdata-ext.py`; it
resolves the binary from `$PATH`, the active venv, `~/.local/bin/`, or
Homebrew prefixes.

**TexKey missing from the JSON** — the field is `inspire-hep`, a Markdown
link whose display text is the TexKey and whose target is the InspireHEP
record URL. `inspirehep-ext.py` returns it as `inspire_hep_link`.

## Verification Checklist

`json-valid.py` enforces rules 4-9 and every field and error format in
`json-meta.md`. These are the checks it cannot make:

- [ ] Each matrix row sits on one line, and `abstract` is a single line
      (rules 1-2)
- [ ] `time` is the arXiv v1 submission date, and the `arxiv` link's `vN`
      is the version the data was cited from
- [ ] `inspire-hep` TexKey and recid were verified against InspireHEP
- [ ] arXiv ancillary files were checked before the PDF, and every value
      taken from them was validated against the paper's own table
- [ ] `author` follows the 1 / 2 / 3 / 4+ tier rule (initials only)
- [ ] `transition-mode` describes the actual process, and the group
      `dataset`/`scheme`/`note` match the source
- [ ] The annual index includes the new paper (or excludes the deleted one)

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
4. **No combination building**. Published HFLAV/PDG world averages are
   stored as they appear; the importer never computes an average itself.
5. **Atomicity is manual**. If you crash between writing the JSON and
   updating the index, you must re-run Cleanup (Step 3) by hand.
