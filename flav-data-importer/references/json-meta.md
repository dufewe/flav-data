# JSON Metadata Structure

This document is the authoritative specification for the flav-data JSON format. Every JSON file in the database must conform to this structure.

## Top-Level Structure

Each paper (experimental or theoretical) corresponds to exactly one JSON file:

```json
{
    "inspire-hep": "[LHCb:2015svh](https://inspirehep.net/literature/1409497)",
    "author": "Aaij, R. and others",
    "collaboration": "LHCb",
    "title": "Angular analysis of the $B^{0}\\to K^{*0}\\mu^{+}\\mu^{-}$ decay",
    "arxiv": "[hep-ex/1512.04442v1](https://arxiv.org/pdf/1512.04442)",
    "time": "2015.12.14",
    "abstract": "An angular analysis of the $B^{0}\\to K^{*0}(\\to K^{+}\\pi^{-})\\mu^{+}\\mu^{-}$ decay...",
    "pdf": "https://arxiv.org/pdf/1512.04442",
    "transition-mode": "semileptonic decay",
    "data": {
        "B0.2.Kst0.mu+.mu-": {
            "angular": [
                {
                    "obs@1": { ... },
                    "obs@2": { ... },
                    "type@1_correlation": [
                        [1.0, 0.5, 0.1],
                        [0.5, 1.0, 0.2],
                        [0.1, 0.2, 1.0]
                    ]
                }
            ]
        }
    }
}
```

## Top-Level Metadata Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `inspire-hep` | string | Yes | Markdown link: `[TexKey](https://inspirehep.net/literature/{recid})`. TexKey is the InspireHEP BibTeX citation key; recid is the control number. Always verify via InspireHEP API. | `[LHCb:2015svh](https://inspirehep.net/literature/1409497)` |
| `author` | string | Yes | InspireHEP BibTeX format with initials only: 1 author → `"Surname, I."`; 2–3 → all names, comma-separated with `and`; 4+ → `"Surname, I. and others"`. If no person names are found, fall back to `"{group} collaboration"`. | `Aaij, R. and others` |
| `collaboration` | string | Yes | The experimental collaboration or theory group name. For multi-collaboration papers, use comma-separated names (e.g., `"ATLAS, CMS"`). | `LHCb` |
| `title` | string | Yes | The paper title from the latest InspireHEP or arXiv version. Must preserve LaTeX for any formulas. Double-backslash escaped in JSON. Prefer arXiv-sourced titles. All Unicode characters in the original title (Greek letters, math symbols, etc.) must be converted to LaTeX. | `Angular analysis of the $B^{0}\\to K^{*0}\\mu^{+}\\mu^{-}$ decay` |
| `arxiv` | string/null | Yes | Markdown link: `[primary_category/arxiv_idvN](https://arxiv.org/pdf/{id})`. The version number (vN) must match the article version from which data was cited. If no arXiv ID exists (e.g., some older journal-only papers), set to `null`. | `[hep-ex/1512.04442v1](https://arxiv.org/pdf/1512.04442)` |
| `time` | string | Yes | arXiv v1 first submission date in `YYYY.MM.DD` format (dot-separated). If no arXiv v1 date exists, use the journal acceptance date instead. Database file indexing is based on this date. | `2015.12.14` |
| `abstract` | string | Yes | The complete abstract from the latest InspireHEP or arXiv version, with LaTeX preserved. **Multi-line LaTeX blocks** (`\begin{align*} ... \end{align*}`) **must be converted to single-line LaTeX** so the abstract is a single line. Use arXiv-sourced abstracts from InspireHEP when available; fall back to journal abstracts. All Unicode must be LaTeX-escaped. | `An angular analysis of the...` |
| `pdf` | string | Yes | URL to the paper PDF. Prefer the arXiv PDF URL. If no arXiv page exists, fall back to the InspireHEP file URL or the journal article homepage. | `https://arxiv.org/pdf/1512.04442` |
| `transition-mode` | string | Yes | Must immediately precede `data`; `data` is the final top-level key. Describes the physical process type using a property-based category. Do NOT use non-property descriptors like "rare decay". | `semileptonic decay` |
| `data` | object | Yes | Dictionary keyed by transition channel: `data["A.B.2.C.D"] = {category: [group, ...]}`; use `"no-transition"` for basic observables. Each category holds a non-empty list of data groups, and each group is bounded by its own correlation/covariance matrix. Allowed field names within a group are exact: `obs@N`, `type@N_correlation`, `type@N_covariance`, `tot_correlation`, `tot_covariance`, `q2min`/`q2max`/`pTmin`/`pTmax`/`etamin`/`etamax`. The legacy flat-list form is accepted only for unmigrated files. | See Data Entries section |

## Metadata Field Sources

| Field | Source | Notes |
|-------|--------|-------|
| `inspire-hep` | InspireHEP BibTeX info | `[TexKey](https://inspirehep.net/literature/{recid})` |
| `author` | InspireHEP BibTeX info | 1 / 2–3 / 4+ tiers; initials only (see `format_authors()` in `scripts/common.py`) |
| `collaboration` | InspireHEP BibTeX info | Collaboration name |
| `title` | InspireHEP (arXiv-sourced preferred) | Preserves LaTeX |
| `abstract` | InspireHEP (arXiv-sourced preferred) | Preserves LaTeX |
| `arxiv` | arXiv webpage | `[primary_category/arxiv_idvN](https://arxiv.org/pdf/<id>)` |
| `time` | arXiv webpage | v1 submission date, `YYYY.MM.DD` |
| `pdf` | arXiv webpage (preferred) | Fallback to InspireHEP or journal link |
| `transition-mode` | Paper information | Property-based decay/scattering name |
| `data` | Extracted from data source | HEPData, CDS, PDF, etc. |

## Data Entries (`data{transition}{category}[]`)

`data` is a dictionary with three levels:

1. **Transition channel** — a canonical transition (`A.B.2.C.D`, per
   `obs-abbr.md` §1) or `"no-transition"` for basic observables (`MZ`,
   `Tau(B0)`, CKM elements, ...).
2. **Observable category** — unlike measurements must not share a
   dictionary (SKILL.md rule 6).
3. **Data groups** — a non-empty **list** of groups. Each group is a set
   of observables linked by a common correlation/covariance matrix (see
   Data Grouping below). Different q² bins of the same observable go
   into separate groups with identical `name` but different
   `q2min`/`q2max` values.

The validator checks that every observable's transition in `name`
matches the enclosing transition key, and that its abbreviation belongs
to the enclosing category (unless the observable maps to `other`).

### Observable Categories

| Category | Use For | Examples |
|----------|---------|----------|
| `angular` | Angular coefficients, polarization fractions, optimized observables | `FL`, `S1c`–`S9`, `P1`–`P8p`, `A3`–`A9`, `SS1re`, `DeltaFL` |
| `differential` | Differential decay rates / cross sections | `dBr/dq2`, `dGdw`, `dSigma/dpT` |
| `branching` | Branching fractions | `Br`, `BrW2had` |
| `asymmetry` | CP, forward-backward, and charge asymmetries | `ACP`, `AFB_CP`, `AC`, `S_phigamma` |
| `ratio` | Ratios of observables or decay channels | `RBr`, `RFL`, `r`, `fs/fd`, `ge/gmu` |
| `lifetime` | Lifetimes | `Tau(B0)`, `Tau(e-)` |
| `mass-mixing` | Masses, widths, and neutral-meson mixing parameters | `MZ`, `Mass(B0)`, `Gamma`, `DeltaMs`, `DeltaGamma` |
| `cross-section` | Total/fiducial cross sections and production rates | `Sigma`, `sigmaWtaunu` |
| `other` | Anything not classified above | `S1`, `f`, `R_b` |

Angular coefficients and differential widths **must** be in separate
category dictionaries, even when they share the same correlation matrix.
Split the matrix into one group per category if necessary.

### Standard Measurement Format

Use this format when the paper reports a central value with component errors (statistical, systematic, etc.):

```json
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
}
```

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Observable identifier in `OBS(transition)[condition]` format. Symbolic notation only — no full expression definitions. Transition states follow the canonical order from `obs-abbr.md` §1 (baryon → meson → charged lepton → neutral lepton, then heaviest → lightest, then `+` → `-` → `0` for equal masses); the validator enforces it. |
| `latex` | Yes | string | LaTeX representation of the observable. Double backslash for JSON escaping; after json.load(), Python reads single backslash. |
| `value` | Yes | string | Central value. Must be a string, even for integers. |
| `type@1_err` | Yes | string | Error type label for the first error component (usually `"stat"`). |
| `type@1_err_up` | Yes | string | Upper error bound for type 1. For symmetric errors, equals `type@1_err_down`. |
| `type@1_err_down` | Yes | string | Lower error bound for type 1. |
| `type@N_err` | No | string | Additional error type labels (e.g., `"syst"`, `"lumi"`, `"norm"`, `"theo"`). Each additional error type requires its own `_err`, `_err_up`, and `_err_down` triplet. |
| `type@N_err_up` | No | string | Upper error for type N. |
| `type@N_err_down` | No | string | Lower error for type N. |
| `q2min` | Conditional | string | Lower kinematic boundary (usually q² in GeV²). String-formatted float, e.g. `"0.1"`. If the lower bound is unbounded, **omit the field** or use `"+inf"` (see §Combined Kinematic Bins). |
| `q2max` | Conditional | string | Upper kinematic boundary. String-formatted float, e.g. `"1.1"`. If the upper bound is unbounded, **omit the field** or use `"+inf"` (see §Combined Kinematic Bins). |
| `pTmin`/`pTmax` | Conditional | string | Transverse momentum boundaries. Use instead of q² for non-decay processes. |
| `etamin`/`etamax` | Conditional | string | Pseudorapidity boundaries. |
| `unit` | Conditional | string | Physical unit (e.g., `"GeV"`, `"ps"`, `"fb"`). Omit for dimensionless observables. |
| `ref` | Conditional | string | External reference as Markdown link for cited values. Look up the arXiv ID in the paper's references, then search InspireHEP for the correct TexKey. Never guess. |

**Standard error type labels** (`type@N_err`):
| Label | Meaning |
|-------|---------|
| `stat` | Statistical uncertainty |
| `syst` | Systematic uncertainty |
| `lumi` | Luminosity uncertainty |
| `norm` | Normalisation uncertainty |
| `theo` | Theoretical uncertainty |
| `expe` | Experimental uncertainty (combined stat+syst when not split) |

Any other label is rejected. Every `type@N_err` label requires the full
`type@N_err_up` + `type@N_err_down` pair; a lone `type@N_err` (or a
lone bound) is invalid.

### Exactly One Measurement Format

Each `obs@N` uses exactly one of: standard component errors
(`value` + `type@N_err` triplets), total error (`value` +
`tot_err_up`/`tot_err_down`), external reference (`value` +
`tot_err_up`/`tot_err_down` + `ref`), upper limit only
(`type@N_upper_limit` + `type@N_level`, no `value`), or combined fit +
limit (`value` + total error + upper limit). Do not mix component
errors with total errors, and do not add `value` to an upper-limit-only
entry unless total errors are also present. All numeric fields are
float-as-strings (`"0.69"`, `"5.9e-6"`).

Unknown keys inside `obs@N` are rejected by the validator in the dict
schema. The only allowed keys are `name`, `latex`, `value`, `unit`,
`ref`, the kinematic boundaries, and the `type@N_*` / `tot_err_*`
patterns documented here.

### Upper Limit Format

Use this format when the paper reports a confidence-level upper limit rather than a measured central value:

```json
"obs@1": {
    "name": "Br(B0.2.Kst0.tau-.e+)",
    "latex": "$\\mathcal{B}(B^{0}\\to K^{*0} \\tau^{-} e^{+})$",
    "type@1_upper_limit": "5.9e-6",
    "type@1_level": "90%@CLs"
}
```

| Field | Description |
|-------|-------------|
| `type@N_upper_limit` | The numeric upper limit value (string). This is the observable's maximum allowed value at the given confidence level. |
| `type@N_level` | The confidence level as a string, e.g., `"90%@CLs"`, `"95%@CLs"`. |

**Multiple confidence levels**: When a paper reports upper limits at multiple CLs (e.g., 90% and 95%), use `type@1_*` for the primary (typically lowest) CL and `type@2_*` for the secondary CL. Each requires its own `_upper_limit` + `_level` pair.

**Critical:** `upper_limit` is the numeric value, `level` is the confidence — do not swap these fields. Do NOT use `type@N_err_up` for upper limits.

### Total Error Format

Use this format when the paper reports a single combined (total) error without separate stat/syst breakdown, and the data comes from the current paper itself (not an external reference):

```json
{
    "name": "FL(B0.2.Kst0.mu+.mu-)",
    "latex": "$F_L(B^{0}\\to K^{*0}\\mu^{+}\\mu^{-})$",
    "value": "0.69",
    "tot_err_up": "0.039",
    "tot_err_down": "0.039",
    "q2min": "0.1",
    "q2max": "1.1"
}
```

### Combined Fit + Upper Limit Format

Use this format when the paper reports both a fit result (central value + total
uncertainty) and CLs upper limits. Common in BSM searches where the fit can return
a central value near zero (or negative) while the CLs method sets a physical upper
bound. Both sets of fields are required: `value` + `tot_err_up`/`tot_err_down`
for the fit result, and `type@N_upper_limit` + `type@N_level` for each confidence
level. They come from different statistical procedures and coexist in the same
`obs@N` entry.

### External Reference Format

Use this format for values taken from external sources (PDG world averages, HFLAV combinations, earlier papers). Per `obs-abbr.md` §2.2.2, **ratio observable names must use the `R<OBS>(transition)[cond]` form** (e.g. `RBr`, `RFL`, `RDeltaGamma`); a bare `R(transition)[cond]` is not valid for new imports (the validator still accepts it for legacy files):

```json
{
    "name": "RBr(Lambdac+.2.p.l+.nu)[mu/e]",
    "latex": "$\\mathcal{R}^{\\mu/e}_{\\Lambda_c^+\\to p\\ell\\nu}$",
    "value": "0.175",
    "tot_err_up": "0.012",
    "tot_err_down": "0.012",
    "ref": "[LHCb:2015svh](https://inspirehep.net/literature/1409497)"
}
```

The `ref` field must be a Markdown link with a verified InspireHEP TexKey. Look up the source paper's arXiv ID from the reference list, then search InspireHEP.

## Correlation and Covariance Matrices

### Correlation Matrix (`type@N_correlation`)

Placed at the data entry level (alongside `obs@N` keys, not inside any obs):

```json
"type@1_correlation": [
    [1.0, 0.5, 0.1],
    [0.5, 1.0, 0.2],
    [0.1, 0.2, 1.0]
]
```

**Rules:**
- **Diagonal elements must be 1.0** (correlation of an observable with itself).
- **Matrix must be symmetric**: `M[i][j] == M[j][i]`.
- **Dimension**: matrix size (N×N) must equal the number of `obs@N` entries in the same data entry.
- **Order**: matrix indices correspond to obs@N numbering order (obs@1 → index 0, obs@2 → index 1, etc.).
- **Naming**: use `type@1_correlation` to match `type@1_err` (stat), `type@2_correlation` to match `type@2_err` (syst), etc.
- **Format**: matrix elements are floats (not strings).
- **Layout**: each matrix row is on a single line; do **not** put each element on its own line. This applies to all `*_correlation` and `*_covariance` fields. (See SKILL.md "Core Conventions" rule 1.)
- If no correlation matrix is available, **omit the field entirely** (do not set to `null`).

### Total Error Correlation/Covariance (`tot_correlation`, `tot_covariance`)

When using total error format (`tot_err_up`/`tot_err_down`), use the `tot_` prefix for matrices: `tot_correlation` or `tot_covariance`. Same rules as `type@N_correlation`/`type@N_covariance`. Do NOT mix `tot_correlation` with component errors (`type@N_err`).

### Covariance Matrix (`type@N_covariance`)

```json
"type@1_covariance": [
    [0.01, 0.005],
    [0.005, 0.01]
]
```

**Rules:**
- **Matrix must be symmetric**.
- **Diagonal elements** are the variances (error squared) for each observable. These must be manually verified against the reported errors.
- **Dimension and order** follow the same rules as correlation matrices.
- Matrix elements are floats.
- Omit the field if not available.

### Data Grouping

Each element in a category's list is a **data group** — a set of observables that share a common measurement context:

- **Group boundary**: defined by a correlation or covariance matrix. All observables linked by the same matrix belong to one group.
- **Matrix dimension**: the N×N matrix covers exactly N observables (`obs@1` through `obs@N`).
- **No matrix**: observables without a correlation/covariance matrix can be placed together in the same group, or split across groups as appropriate.
- **One category per list**: a group holds observables of the same category. If a source matrix couples angular and differential observables, split it into separate groups (one per category).

### Combined Kinematic Bins

When measurements are performed across non-contiguous regions and combined into a single result:

- `q2min` and `q2max` (and similarly `pTmin`/`pTmax`, `etamin`/`etamax`) accept **comma-separated multi-interval** strings.
- Ranges must be paired one-to-one: `"q2min": "11.0,17.5"` with `"q2max": "15.0,+inf"`.
- `"+inf"` denotes an unbounded upper limit. Example: two non-contiguous bins covering [11.0, 15.0] ∪ [17.5, +∞).

## transition-mode Values

The `transition-mode` field classifies the physical process. Only two top-level categories are valid: **decay** and **scattering**. Subdivide by specific property.

| Value | Use For | Examples |
|-------|---------|----------|
| `leptonic decay` | Pure leptonic decays | $B \to \ell\ell$, $\tau \to \mu\mu\mu$ |
| `semileptonic decay` | Semileptonic decays | $B \to K^{(*)}\ell\ell$, $\Lambda \to p\ell\nu$ |
| `non-leptonic decay` | Hadronic (non-leptonic) decays | $B \to J/\psi\, p\,\pi$, $B \to D\pi$ |
| `radiative decay` | Radiative decays | $B \to K^*\gamma$, $B \to X_s\gamma$ |
| `neutron beta decay` | Neutron decay observables | $n \to p\,e^-\,\bar{\nu}_e$ correlations |
| `Higgs decay` | Higgs boson decays | $H \to \gamma\gamma$, $H \to ZZ^*$ |
| `scattering` | Scattering and production processes | $pp \to W$, $pp \to t\bar{t}$, $e^+e^- \to \mu^+\mu^-$ |

**Do NOT use** non-property descriptors such as "rare decay", "flavor-changing", "BSM search", etc.

## Non-Standard Schemas: HFLAV and PDG

The aggregation groups **HFLAV** and **PDG** do not follow the
per-paper schema above. Each ships one snapshot JSON per year.
`scripts/json-valid.py` auto-detects both (a `data` dict whose subgroup
keys are `obs@N`/`correlation` means PDG; top-level values containing an
`observables` list mean HFLAV) and validates them with dedicated rules —
they are no longer checked by hand.

### PDG snapshot

Top level: `inspire-hep`, `author`, `collaboration`, `title`,
`year`, `data`. All six are required, and `year` must be a four-digit
string (e.g. `"2024"`). `data` is an **object keyed by subgroup name**
(e.g. `PDG@W`, `PDG@Z`, `PDG@Higgs`). Each subgroup holds flat
`obs@N` entries plus an optional `correlation` matrix; `obs@N`
numbering may be sparse (only `obs@N` and `correlation` are allowed
as subgroup keys).

```json
{
    "inspire-hep": "[PDG:2024](https://...)",
    "author": "Navas, S. and others",
    "collaboration": "PDG",
    "title": "Review of Particle Physics",
    "year": "2024",
    "data": {
        "PDG@W": {
            "obs@1": { "name": "MW", "latex": "$M_W$", "value": 80.3692, "error": 0.0133, "unit": "GeV" },
            "obs@27": { "name": "Br(W2lnu)", "value": 0.1086, "error": 0.0009 },
            "correlation": null
        },
        "PDG@Z": { "...": "..." }
    }
}
```

### HFLAV snapshot

There is **no top-level `data`**. Each top-level key is a subgroup
name (`HFLAV@overview`, `HFLAV@B02pilnu`, ...) mapping to an object
with `group`, `arxiv`, `inspire-hep`, `description`, an
`observables` **array**, and an optional `correlation` matrix.

```json
{
    "HFLAV@overview": {
        "group": "HFLAV",
        "arxiv": null,
        "inspire-hep": "[HFLAV:2024](https://...)",
        "description": "overview of popular observables",
        "observables": [
            { "name": "Tau(B0)", "value": 1.517, "error": 0.004, "unit": "ps" }
        ],
        "correlation": null
    },
    "HFLAV@B02pilnu": { "...": "..." }
}
```

### Shared rules for both snapshots

- No `transition-mode` field — each subgroup is a different process.
- Snapshot `value`/error fields are **numbers**, not strings (the
  all-strings rule in §Key Constraints applies only to the standard
  per-paper schema).
- Each observable needs `name` and `value`, plus one error form:
  `error` (scalar), `error_up`/`error_down`, or
  `tot_err_up`/`tot_err_down`. Do not use `type@N_err` triplets.
- Unknown observable keys are rejected: the only allowed fields are
  `name`, `latex`, `value`, `error`, `error_up`, `error_down`,
  `tot_err_up`, `tot_err_down`, `unit`, `limit`.
- `latex` is optional but, when present, must be Unicode-free.
- `unit` is a free-form string (`"GeV"`, `"ps"`, `"fb"`).
- Optional subgroup `correlation` is a square N×N matrix whose
  dimension must equal the observable count; `null` is allowed.
- HFLAV observables may carry a free-form `limit` string annotating
  the phase-space or charge combination.

## Key Constraints

1. **All numeric values are strings** (`"0.25"`) except matrix elements (floats). Applies to `value`, `q2min`/`q2max`, `pTmin`/`pTmax`, all error fields, and `unit`.
2. **LaTeX uses double backslash** — `\\to` in the JSON file. After `json.load()`, this becomes `\to` in Python.
3. **4-space indentation** — JSON files use exactly 4 spaces per indent level.
4. **Field order** — Top-level fields follow the Top-Level Fields table order; within `obs@N`, follow the Standard Measurement table.
5. **arxiv format** — Must include primary category and version: `[hep-ex/1512.04442v1](https://arxiv.org/pdf/1512.04442)`. If no arXiv ID, use `null`.
6. **No `year` field** — Standard schema does not support a top-level `year` field (HFLAV/PDG non-standard snapshots are the only exception; see §Non-Standard Schemas).
7. **Omit empty fields** — Do not include keys with empty string or `null` values (except `arxiv` which uses `null` when absent).
8. **Top-level key order** — `transition-mode` must immediately precede `data`, and `data` must be the final key in the JSON object.
9. **Matrix layout: row-per-line** — Each `*_correlation`/`*_covariance` row is on a single line. (SKILL.md rule 1.)
10. **Author format** — initials only, with 1 / 2–3 / 4+ tiers: `"Polchinski, J."`, `"Aaij, R., Smith, J., and Oyanguren, A."`, or `"Aaij, R. and others"`. (SKILL.md rule 3.)
11. **Abstract = single line** — Collapse multi-line `align*`/`gather*`/etc. blocks to single-line LaTeX. Line breaks (`\\`) become `, ` separators, with `and` before the last. (SKILL.md rule 2.)
12. **No Unicode** — Replace all Unicode chars (`μ`, `Δ`, `±`, `×`, `→`, `°`, smart quotes) with LaTeX equivalents (`\mu`, `\Delta`, `\pm`, `\times`, `\to`, `^{\circ}`, `` ` ``/`'`/`` `` ``/`''`). (SKILL.md rule 4.)
13. **Transition order** — Dotted `.2.` transitions follow the canonical order (SKILL.md rule 5): baryon → meson → charged lepton → neutral lepton, then heaviest → lightest within each type, then `+` → `-` → `0` for equal masses; neutral antiparticles append `Bar`. The validator fails non-canonical order.
14. **`data` is a dictionary** — keyed by transition channel (`A.B.2.C.D` or `no-transition`), then by observable category, then a list of data groups (SKILL.md rule 7). The legacy list form is accepted only for unmigrated files.
15. **One category per dictionary** — angular, differential, branching, asymmetry, ratio, lifetime, mass-mixing, cross-section, and other measurements must not be mixed (SKILL.md rule 6); angular and differential observables in particular require separate dictionaries.
16. **Exactly one measurement format** — component-error triplets, total error, external reference, upper limit, or combined fit + limit; error labels are limited to `stat`, `syst`, `lumi`, `norm`, `theo`, `expe`. Unknown observable fields are rejected in the dict schema.

## Extending This Specification

When a paper introduces metadata or data structures not covered by this document:

1. **Identify the new pattern** — is it a new field, a new error type, a new kinematic variable, or a new data format?
2. **Check existing conventions** — review this document and `../references/obs-abbr.md` for naming patterns that can be extended.
3. **Add the new pattern** to the relevant section of this document.
4. **Update the validator** (`../scripts/json-valid.py`) if the new pattern requires structural checks.
5. **Keep it consistent** — use the same naming conventions, string types, and ordering rules as existing fields.

Examples of extensions:
- New kinematic boundary: add `{var}min`/`{var}max` to `DATA_ENTRY_KINEMATIC_FIELDS` and `is_observable_field` in `json-valid.py`
- New error label: add it to `STANDARD_ERROR_LABELS` in `json-valid.py` **and** to the label table above
- New data category: add it to `OBSERVABLE_CATEGORIES` and the abbreviation sets in `json-valid.py`, plus the category table above
- New data format (e.g., asymmetric confidence intervals): document as a new subsection under Data Entries and extend `_validate_measurement_scheme` in `json-valid.py`
