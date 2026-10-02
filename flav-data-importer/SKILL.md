---
name: flav-data-importer
description: Import flavor-physics measurement data from arXiv, InspireHEP, and HEPData into the flav-data JSON format. Use for the full lifecycle, i.e., metadata lookup, HEPData extraction, transition-symbol and observable-name construction, JSON schema validation, and paper-index maintenance.
license: MIT
category: data-science
tags: [flavor-physics, data-collecting, json-importer]
---

# flav-data Importer

Extract structured flavor-physics data from arXiv, InspireHEP, and HEPData into the `flav-data` standard JSON format. One JSON file per paper with single or multiple collaborations under `Experimental/<Lab>-<Collaboration>/<year>/<month>/<Collaboration>:<TexKey>.json`, with annual index files alongside. Covers the full lifecycle: discovery → extraction → validation → index maintenance.

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
latex_for_obs = common.latex_for_obs

# Unicode → LaTeX (86 single chars + 8 multi-char sequences)
unicode_to_latex("B⁰ → K*⁰ μ⁺μ⁻")   # → "B^0 \\to K^{*0} \\mu^+\\mu^-"

# Author name → BibTeX initials
to_bibtex("Aaij, Roel")               # → "Aaij, R."

# Observable name → LaTeX field for obs@N.latex
# (expands the OBSERVABLE abbreviation; leaves compact transition form intact)
latex_for_obs("FL(B0.2.Kst0.mu+.mu-)")  # → "$F_L(B0.2.Kst0.mu+.mu-)$"
latex_for_obs("gammaCKM")               # → "$\\gamma$"
latex_for_obs("Mass(B0)")               # → "$M_{B0}$"
```

Note: `latex_for_obs` does **not** expand compact transition notation
(`B0.2.Kst0.mu+.mu-` is left as-is). For the fully-expanded form (e.g.
`$F_L(B^{0} \\to K^{*0} \\mu^{+}\\mu^{-})$`), see `references/obs-abbr.md`
§1.2 and write the `latex` field by hand.

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
| `scripts/common.py` | Unicode → LaTeX mapping (86 single + 8 multi-char) + BibTeX author-name conversion. Imported by every other script. |
| `scripts/arxiv-ext.py` | arXiv API metadata + PDF download. `python3 scripts/arxiv-ext.py 1512.04442`. |
| `scripts/inspirehep-ext.py` | InspireHEP API metadata. `python3 scripts/inspirehep-ext.py --arxiv-id 1512.04442`. |
| `scripts/hepdata-ext.py` | HEPData table extraction (YAML parsing, matrix support). `python3 scripts/hepdata-ext.py <inspire_id>`. |
| `scripts/json-valid.py` | JSON schema validator (standard + HFLAV/PDG snapshot modes). `python3 scripts/json-valid.py <file>`. |

## Scope

| Supported | Not Supported |
|-----------|--------------|
| Experimental measurements (LHCb, CMS, ATLAS, Belle, BaBar, BESIII, etc.) | Conference/report papers (no formal preprint) |
| HFLAV/PDG snapshots (special schema) | Fits and global averages derived downstream |
| Theoretical groups (HPQQCD, RBC/UKQCD, etc.) | Unpublished results, theses |
| Multi-collaboration papers | Internal notes (CDS restricted) |

## Workflow

### Step 1: Discovery

**Always start by searching for an existing entry** in the paper index.
This prevents duplicates and tracks the version history of each measurement.

1. Check if the file already exists:
   ```bash
   ls "Experimental/CERN-LHCb/2015/12/LHCb:2015svh.json"
   ```
2. If found, **compare versions**:
   - `arxiv` field has same arXiv ID → no action
   - `arxiv` field has new version → update metadata + data, bump index
   - `arxiv` field has different ID → different paper, create new entry
3. If not found, proceed to Step 2.

**Index files** (`Experimental/<Lab>-<Collaboration>/<year>/<Collaboration>@<year>.json`)
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
       observables, qualifiers = hepdata_ext.parse_yaml_observables(yaml_text)
       matrix_type, matrix, qualifiers = hepdata_ext.parse_yaml_correlation(yaml_text)
   ```
   If HEPData is unavailable or incomplete, fall back to the PDF + pymupdf.
   See `references/hepdata-cli.md` and `references/data-source.md`.

4. **Write the JSON file** at the canonical path. The full assembly:

   ```python
   latex_for_obs = common.latex_for_obs
   unicode_to_latex = common.unicode_to_latex

   meta = inspirehep_ext.extract_metadata(hit)
   json_doc = {
       # ----- from inspirehep-ext (extract_metadata) -----
       "inspire-hep":     meta["inspire_hep_link"],     # Markdown link "[TexKey](url)"
       "author":          meta["author_str"],            # BibTeX form, see SKILL.md rule 3
       "collaboration":   meta["collaboration"],
       "title":           meta["title"],                 # already Unicode→LaTeX
       "abstract":        meta["abstract"],             # already Unicode→LaTeX
       # ----- from arxiv-ext (get_arxiv_info) -----
       "arxiv":           arxiv["arxiv_link"],          # Markdown link [primary_category/arxiv_idvN](url)
       "time":            arxiv["time"],                 # "YYYY.MM.DD" (v1 submission date)
       "pdf":             arxiv["pdf_url"],              # prefer arXiv over InspireHEP
       # ----- human-picked (per references/json-meta.md §"transition-mode Values") -----
       "transition-mode": "semileptonic decay",          # 7-value whitelist
       "data": [
           # each entry: {"obs@1": {...}, "obs@2": {...}, ..., "tot_correlation": [...]}
           # for each obs@N:
           #   "name":  "FL(B0.2.Kst0.mu+.mu-)"        # compact form (per obs-abbr.md)
           #   "latex": "$F_L(B^{0} \\to K^{*0} \\mu^{+}\\mu^{-})$"  # fully-expanded LaTeX
           #   "value": "0.69"
           #   "type@1_err":      "stat"
           #   "type@1_err_up":   "0.035"
           #   "type@1_err_down": "0.036"
           # optionally: "q2min": "0.1", "q2max": "1.1", etc.
       ],
   }
   ```

   Field-source priorities when there are two candidates:
   - **Title / Abstract**: InspireHEP preferred (LaTeX-preserved);
     fall back to arXiv only if InspireHEP lacks the paper.
   - **PDF URL**: arXiv preferred (canonical, version-pinned);
     fall back to InspireHEP's `pdf_url` only for journal-only papers
     (`arxiv == null`).
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
python3 scripts/json-valid.py <file>
```

Runs the standard schema validator. For HFLAV/PDG snapshots, the validator
auto-detects the snapshot schema (no `transition-mode` field, `data` is a
dict of subgroups with `error` scalar per entry).

### Step 3: Cleanup

Run these commands from the project root:

```bash
# 1. Validate every changed file
python3 flav-data-importer/scripts/json-valid.py Experimental/CERN-LHCb/2015/12/LHCb:2015svh.json

# 2. Rebuild the year index if you added or removed papers
# (manual edit; see flav-data-importer/references/file-index.md)

# 3. Find the paper file at its month-directory depth
find Experimental/CERN-LHCb/2015 -mindepth 2 -maxdepth 2 -name 'LHCb:2015svh.json' -print
```

## Core Conventions

These are the 4 hard rules for writing JSON files in this repo. Each
reference doc points back to these.

1. **Matrix format (row-per-line)** — each matrix row on one line:
   ```json
   "tot_correlation": [
       [1.0, 0.5, 0.3],
       [0.5, 1.0, 0.2],
       [0.3, 0.2, 1.0]
   ]
   ```
   Applies to all `*_correlation` and `*_covariance` fields. Do **not**
   put each element on its own line.

2. **Abstract = single line** — Collapse multi-line `align*` / `gather*` /
   etc. blocks to a single-line LaTeX string. Internal line breaks (`\\`)
   become `, ` separators, with `and` before the last equation.

3. **Author format** — use one of these tiers by author count:

   | Author count | Format | Example |
   |---|---|---|
   | **1** | `"Surname, I."` (no "and others") | `"Polchinski, J."` |
   | **2–3** | List all, BibTeX form, separated by commas + "and" | `"Aaij, R., A. Oyanguren, and J. Smith"` |
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

## Decision Points

**Q: What if the paper has a CERN note number instead of an arXiv ID?**
A: Set `arxiv` to `null`. Use a Markdown link for `inspire-hep`:
`[LHCb-NOTE-2015-001](https://cds.cern.ch/record/1234567)`. The validator
accepts any non-null Markdown link as the `inspire-hep` value.

**Q: What if there's no HEPData entry for this paper?**
A: Fall back to extracting from the source PDF via `pymupdf` (preferred)
or table screenshots via `vision_analyze`. Mark `data` as `[]` only as a
last resort — the validator will warn but not fail.

**Q: arXiv vs InspireHEP — which metadata wins?**
A: arXiv provides version number and PDF URL; InspireHEP provides
authoritative author list and DOI. Use InspireHEP for metadata, arXiv
for PDF.

**Q: How to handle mixed q² bins across different obs entries?**
A: Use `q2min`/`q2max` per `obs@N`. The `[condition]` syntax is for
multi-decay-channel ratios only (e.g.
`RBr(B+.2.K+.l+.l-)[mu/e]`).

## Troubleshooting

### Error: "JSON format correct" but obs fields missing

Run `python3 scripts/json-valid.py <file>` and read all `[FAIL]` lines
above the summary. Common ones:

- `obs@N: missing required field: type@1_err` — add a `type@N_err` field
  with one of `stat`, `syst`, `total`, `model`, `ext`.
- `obs@N: missing required field: type@1_err_up`/`_down` — paired
  asymmetric error bars; both required if either present.
- `transition-mode: invalid value` — must be one of:
  `leptonic decay`, `semileptonic decay`, `non-leptonic decay`,
  `radiative decay`, `neutron beta decay`, `Higgs decay`, `scattering`
  (see `references/json-meta.md` §"transition-mode Values").
- `matrix not symmetric [i][j] != [j][i]` — fix the matrix entries.
  Re-check the source PDF table for the correct `ij`/`ji` pair.

### Error: "Validator says transition symbol missing"

The `OBS(transition)` syntax is **only** for observables from a specific
decay channel. **Basic observables** (particle masses, lifetimes, CKM
parameters, EW parameters) do not take a transition — write them as
`Mass(Z)`, `Tau(e-)`, `gammaCKM`, `MZ`, etc. (see `references/obs-abbr.md`
§2.1).

If you see this error for an observable that should NOT have a transition,
rename it to its basic-observable form, not to `OBS(transition)`.

### Error: "ARXIV_FIELDS_MUST_BE_DICT"

Each `data` entry must be a dict (`{"obs@1": {...}, "obs@2": {...}, ...}`),
not a list. See `assets/workflow-lhcb-2015svh.md` Step 3 for the canonical
shape.

### Error: "HEPData 401 / Cloudflare blocked"

Direct `curl` to hepdata.net is blocked. Install `hepdata-cli`:

```bash
pip install hepdata-cli
```

Then re-run `scripts/hepdata-ext.py`. The script resolves the binary from
`$PATH`, the active venv, `~/.local/bin/`, or Homebrew prefixes.

### Error: "I have TexKey from InspireHEP but JSON doesn't show it"

The JSON field is `inspire-hep` (a Markdown link whose display text is the
TexKey and whose target is the InspireHEP record URL), not a bare `texkey`
key. Run `inspirehep-ext.py` to get the correct `inspire-hep` value. The
`texkey` itself is embedded in that link.

## Verification Checklist

Before committing any new or updated JSON file:

- [ ] File parses: `python3 flav-data-importer/scripts/json-valid.py <file>` returns no issues (the validator has a limited HFLAV/PDG snapshot check; review `json-meta.md` §"Non-Standard Schemas" manually as well)
- [ ] `time` field is v1 arXiv submission date in `YYYY.MM.DD` format
- [ ] `arxiv` field is either `null` or a Markdown link with display text `primary_category/<id>v<N>` and target the arXiv PDF URL
- [ ] `inspire-hep` is `[<TexKey>](https://inspirehep.net/literature/<recid>)` with verified TexKey
- [ ] `author` is `Surname, Initials. and others` (initials only)
- [ ] `transition-mode` is immediately before `data`, and `data` is the final top-level key
- [ ] `data` is a list (standard) or dict-of-subgroups (snapshot), each entry is a dict with `obs@N` keys
- [ ] Each `obs@N` has `name`, `latex`, `value`, and a `type@N_err` family
- [ ] Matrix fields use row-per-line layout, symmetric for correlation
- [ ] Unicode is fully escaped (no `μ`, `Δ`, `±`, `→`, smart quotes)
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
A: `Experimental/<Lab>-<Collaboration>/<year>/<month>/<Collaboration>:<TexKey>.json`.
For a multi-collaboration paper, use the primary collaboration's directory
and list all collaborations in the `Collaboration` field
(`"LHCb, CMS"`). For HEPData-only updates, use the recid as the TexKey.

**Q: Can I import a paper with no arXiv ID (journal-only)?**
A: Yes. Set `arxiv` to `null`. Look up the paper by DOI or title on
InspireHEP and use the InspireHEP-only metadata path.

**Q: How do I name the observable for a branching ratio?**
A: `Br(transition)[condition]` if multi-decay, otherwise just
`Br(B+.2.K+.mu+.mu-)` for a single decay. For Lepton Flavor Universality
ratios, use `RBr(B+.2.K+.l+.l-)[mu/e]` (R + obs + transition + condition).

**Q: What about a CP asymmetry measurement?**
A: Use `ACP(transition)` for time-integrated, or `ACP_bplus(transition)`
for the B+ specific case. See `references/obs-abbr.md` §2.3.

**Q: Why are there `obs@N` suffixes on field names?**
A: To support multi-value observables (e.g. `obs@1`, `obs@2`, `obs@3`
for three q² bins). The validator treats `obs@1` and `obs@2` as separate
entries with their own errors. See `assets/workflow-lhcb-2015svh.md`
for a worked example.

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