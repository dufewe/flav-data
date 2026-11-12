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
    "transition-mode": "semileptonic-decay",
    "data": [
        {
            "B0.2.K*0.mu+.mu-": {
                "obs@1": { ... },
                "obs@2": { ... }
            },
            "correlation": [
                [1.0, 0.5],
                [0.5, 1.0]
            ]
        }
    ]
}
```

## Top-Level Metadata Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `inspire-hep` | string | Yes | Markdown link: `[TexKey](https://inspirehep.net/literature/{recid})`. TexKey is the InspireHEP BibTeX citation key; recid is the control number. Always verify via InspireHEP API. | `[LHCb:2015svh](https://inspirehep.net/literature/1409497)` |
| `author` | string | Yes | InspireHEP BibTeX format with initials only: 1 author → `"Surname, I."`; 2 → `"A and B"`; 3 → `"A, B, and C"`; 4+ → `"Surname, I. and others"`. If no person names are found, fall back to `"{group} collaboration"`. | `Aaij, R. and others` |
| `collaboration` | string | Conditional | Required for named collaborations: experimental collaborations, HFLAV/PDG, and large theory collaborations (HPQCD, JLQCD, RBC/UKQCD, ...). For multi-collaboration papers, use comma-separated names (e.g., `"ATLAS, CMS"`). **Omit the key entirely** for papers by individual authors or small theory groups. | `LHCb` |
| `title` | string | Yes | The paper title from the latest InspireHEP or arXiv version. Must preserve LaTeX for any formulas. Double-backslash escaped in JSON. Prefer arXiv-sourced titles. All Unicode characters in the original title (Greek letters, math symbols, etc.) must be converted to LaTeX. | `Angular analysis of the $B^{0}\\to K^{*0}\\mu^{+}\\mu^{-}$ decay` |
| `arxiv` | string/null | Yes | Markdown link: `[primary_category/arxiv_idvN](https://arxiv.org/pdf/{id})`. The version number (vN) must match the article version from which data was cited. If no arXiv ID exists (e.g., some older journal-only papers), set to `null`. A malformed link or the string `"null"` fails validation; a legacy bare string passes and a missing `vN` only warns — new imports always use the full form. | `[hep-ex/1512.04442v1](https://arxiv.org/pdf/1512.04442)` |
| `time` | string | Yes | arXiv v1 first submission date in `YYYY.MM.DD` format (dot-separated). If no arXiv v1 date exists, use the journal acceptance date instead. Database file indexing is based on this date. The validator checks presence only, not the format. | `2015.12.14` |
| `abstract` | string | Yes | The complete abstract from the latest InspireHEP or arXiv version, with LaTeX preserved. **Multi-line LaTeX blocks** (`\begin{align*} ... \end{align*}`) **must be converted to single-line LaTeX** so the abstract is a single line. Use arXiv-sourced abstracts from InspireHEP when available; fall back to journal abstracts. All Unicode must be LaTeX-escaped. | `An angular analysis of the...` |
| `transition-mode` | string | Yes | Must immediately precede `data`; `data` is the final top-level key. Describes the physical process type using a property-based category. Do NOT use non-property descriptors like "rare decay". | `semileptonic-decay` |
| `data` | array | Yes | **Non-empty array of data groups**. Each group is an object mapping one or more canonical transition channels (`A.B.2.C.D`, or `"no-transition"`) to an `obs@N` object, plus optional group-level `dataset`/`scheme` strings and `correlation`/`covariance` matrices. Grouping channels together lets one matrix correlate observables across channels. | See Data Entries section |

## Metadata Field Sources

| Field | Source | Notes |
|-------|--------|-------|
| `inspire-hep` | InspireHEP BibTeX info | `[TexKey](https://inspirehep.net/literature/{recid})` |
| `author` | InspireHEP BibTeX info | 1 / 2 / 3 / 4+ tiers; initials only (see `format_authors()` in `scripts/common.py`) |
| `collaboration` | InspireHEP BibTeX info | Only for named collaborations; omit for individual/small-group papers |
| `title` | InspireHEP (arXiv-sourced preferred) | Preserves LaTeX |
| `abstract` | InspireHEP (arXiv-sourced preferred) | Preserves LaTeX |
| `arxiv` | arXiv webpage | `[primary_category/arxiv_idvN](https://arxiv.org/pdf/<id>)` |
| `time` | arXiv webpage | v1 submission date, `YYYY.MM.DD` |
| `transition-mode` | Paper information | Property-based decay/scattering name |
| `data` | Extracted from data source | HEPData, CDS, arXiv ancillary files, LaTeX source, PDF (see `data-source.md`) |

## Data Eligibility

Only two kinds of input belong in the database:

- **Experimental measurements** — including published experimental
  combinations and the HFLAV/PDG snapshots.
- **Theoretical calculations** — lattice QCD, perturbative QCD, and other
  first-principles or fixed-order calculations, including form-factor
  parametrization fits (`aN_FF` coefficients with a group-level `scheme`).
  Those fits are primary theory data even when they combine lattice, LCSR,
  and experimental input (`dataset: "LQCD+LCSR+EXPE"`).

Do **not** import **global analyses**: Wilson-coefficient fits,
CKM/parameter determinations, mass or coupling bounds, and world averages
that reinterpret existing measurements. Those are analysis outputs, not
primary data.

## Data Entries (`data[]`)

`data` is a **non-empty array of data groups**. A group is an object whose
keys are transition channels (each mapping to an `obs@N` object) plus
optional group-level metadata (`dataset`, `scheme`) and matrices:

```json
"data": [
    {
        "B0.2.K*0.mu+.mu-": {
            "obs@1": { ... },
            "obs@2": { ... }
        },
        "correlation": [
            [1.0, 0.4],
            [0.4, 1.0]
        ]
    },
    {
        "B+.2.K+.mu+.mu-": {
            "obs@1": { ... }
        },
        "B+.2.K*+.mu+.mu-": {
            "obs@1": { ... },
            "obs@2": { ... }
        },
        "correlation": [ ... ]
    },
    {
        "no-transition": {
            "obs@1": { ... }
        }
    }
]
```

1. **Transition channel** — a canonical transition (`A.B.2.C.D`, per
   `obs-abbr.md` §1) or `"no-transition"` for basic observables (`MZ`,
   `Tau(B0)`, CKM elements, ...). The channel key alone carries the
   transition: observable `name` values must not repeat it. The validator
   rejects a transition embedded in `name` (e.g.
   `FL(B0.2.K*0.mu+.mu-)`); write `FL` instead. Each channel maps to an
   object of `obs@N` entries; no LaTeX is stored in `data`. Every particle
   token follows `<name>[*]<charge>[Bar]` and must carry an explicit
   charge: neutral states get `0` (`phi0`, `J/psi0`, `n0`, `Lambda0`),
   charged states get `+`/`-` (`p+`, `B-`, `l+`). The only charge-less
   exceptions are neutrinos (`v`/`vBar`, `ve`, `vmu`, `vtau`) and the
   neutral gauge bosons `Z`, `gamma`, `g`. Placeholders, partons,
   inclusive systems, nuclei, and pseudo-labels (`l`, `q`, `Xs`, `Au`,
   `all`, `had`, ...) have no charge slot. Charge-averaged measurements
   use one concrete charge-conjugate representative.
2. **Data group** — one element of the array: a measurement context whose
   observables share one correlation/covariance matrix. A group may hold
   **several channels** when the source matrix correlates observables
   across them; channels placed in different groups are uncorrelated.
3. **Group-level `dataset`** — an optional string naming the data sources
   behind the group, never the analysis technique or fit choice. Use the
   canonical tokens `LQCD`, `LCSR`, and `EXPE`, joined with `+` in
   that order: `"LQCD"`, `"LCSR"`, `"LQCD+LCSR"`,
   `"LQCD+LCSR+EXPE"`. The validator rejects other tokens, spaces,
   duplicates, and wrong order. Experimental groups normally omit the
   key because their source is the paper itself. It sits beside the
   channel keys, never inside `obs@N`.
4. **Group-level `scheme`** — required for any group holding form-factor
   expansion coefficients (`aN_FF`): one of `BK`, `BGL`, `BCL`, `BSZ`, `DLM`
   (mapping to full names and arXiv IDs in `obs-abbr.md` §2.4). Optional
   for other groups. It follows `dataset` and precedes any matrix.
5. **Group-level `note`** — optional non-empty string placed after
   `scheme` and immediately before the matrix. It documents the
   accompanying matrix, for example a coefficient that the source prints
   outside `[-1, 1]`; such an element is then reported as a warning
   instead of an error.
6. **Matrix alignment** — an N×N group matrix covers N observables in
   total across the group's channels: rows follow the channel keys in
   written order, then each channel's `obs@1 … obs@N` order. Keep all
   channel keys before `dataset`, `dataset` before `scheme`, `scheme`
   before `note`, and all of them before the matrix key; the validator
   rejects a channel after any metadata key or any key after a matrix.
7. **Per-channel numbering** — each channel restarts at `obs@1` and runs
   contiguously (1..N) within that channel.
8. **Separate contexts** — different datasets, schemes, or fit choices
   always go into separate groups, even for the same channel. Different
   kinematic bins go into separate groups unless one source matrix
   couples their observables (§Data Grouping). Kinematic boundaries
   (`q2min`/`q2max`, ...) live inside each `obs@N`, never at group or
   channel level.
9. **No category layer** — observables are distinguished solely by
   `name`.

### Form-Factor Expansion Coefficients

Coefficients of a form-factor expansion are named `aN_FF`, where `N` is
the expansion order (0, 1, 2, ...) and `FF` is the form-factor symbol
(`obs-abbr.md` §2.4). Examples: `a0_F+`, `a1_F0`, `a2_Fv`, `a0_Gv`.

When the source reports one number that applies to several form factors
(e.g. both `a0_Gv` and `a0_G+`), write **one observable per form factor**
and repeat the value/errors. Do not join symbols into `a0_Gv_G+`: each
named coefficient is its own observable.

Fit choices (nominal, higher-order, ...) are **not** part of the name and
are not stored in the group metadata; keep such variants as separate
groups. Every coefficient group also needs the group-level `scheme`
value from `obs-abbr.md` §2.4 (`BK`, `BGL`, `BCL`, `BSZ`, or `DLM`), because
the same coefficients are meaningless without the expansion form that
defines them.

### Standard Measurement Format

Use this format when the paper reports a central value with two or more component errors (statistical, systematic, etc.). A single error uses §Total Error Format instead:

```json
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
}
```

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Observable symbol, optionally followed by a `[condition]` or a parameter tag: `OBS`, `OBS[condition]`, `OBS(parameter)`. Do **not** embed the transition channel — the `data` key already carries it. Symbolic notation only — no full expression definitions. |
| `value` | Yes | string | Central value. Must be a string, even for integers. |
| `total_upper` | Conditional | string | Total upper error. Required whenever the measurement has exactly one error; pair with `total_lower`. For symmetric errors the two are equal. |
| `total_lower` | Conditional | string | Total lower error. Required whenever the measurement has exactly one error. |
| `type@N_error` | Conditional | string | Error type label for component N (e.g., `"stat"`, `"syst"`, `"lumi"`, `"norm"`, `"theo"`, `"expe"`; a `theo` component may name its input as `"theo:<source>"`). Only allowed when the measurement has **two or more** errors; each component requires its own `_error`, `_upper`, and `_lower` triplet. |
| `type@N_upper` | Conditional | string | With `type@N_error`: upper error bound for component N. With `type@N_level` and no `type@N_error`: numeric upper bound (upper limit) at that confidence level. |
| `type@N_lower` | Conditional | string | With `type@N_error`: lower error bound for component N. With `type@N_level` and no `type@N_error`: numeric lower bound (lower limit) at that confidence level. |
| `type@N_level` | Conditional | string | Confidence level of a bound, e.g. `"90%@CLs"`, `"95%@CLs"`. Never mixed with `type@N_error`. |
| `q2min` | Conditional | string | Lower kinematic boundary (usually q² in GeV²). String-formatted float, e.g. `"0.1"`. If the lower bound is unbounded, **omit the field** or use `"+inf"` (see §Combined Kinematic Bins). |
| `q2max` | Conditional | string | Upper kinematic boundary. String-formatted float, e.g. `"1.1"`. If the upper bound is unbounded, **omit the field** or use `"+inf"` (see §Combined Kinematic Bins). |
| `pTmin`/`pTmax` | Conditional | string | Transverse momentum boundaries. Use instead of q² for non-decay processes. |
| `etamin`/`etamax` | Conditional | string | Pseudorapidity boundaries. |
| `w_min`/`w_max` | Conditional | string | Hadronic invariant-mass boundaries (semi-inclusive processes). |
| `cos_min`/`cos_max` | Conditional | string | Angular boundaries for a measured decay angle. |
| `chi_min`/`chi_max` | Conditional | string | Binned boundaries for the χ angular variable. |
| `mxs_min`/`mxs_max` | Conditional | string | Missing-mass boundaries. |
| `unit` | Conditional | string | Physical unit only (e.g., `"GeV"`, `"ps"`, `"fb"`). A scientific-notation scale factor (`"1e-6"`, `"10^{-4}"`) is **not** a unit: multiply `value`, `total_upper`/`total_lower`, and any bounds by it, then omit `unit`. Omit for dimensionless observables. |
| `ref` | Conditional | string | External reference as Markdown link for cited values. Look up the arXiv ID in the paper's references, then search InspireHEP for the correct TexKey. Never guess. |
| `dataset` | No | string | Prose description of the data sample or dataset selection. |
| `note` | No | string | Free-form provenance note carried over from the source. |

Data sources and expansion scheme are **group-level**, not
per-observable: see the `dataset` and `scheme` bullets in §"Data Entries"
above. The per-observable `dataset` field above is a free-form sample
description inside one `obs@N`; it is unrelated to the group-level
source list.

**Standard error type labels** (`type@N_error`):
| Label | Meaning |
|-------|---------|
| `stat` | Statistical uncertainty |
| `syst` | Systematic uncertainty |
| `lumi` | Luminosity uncertainty |
| `norm` | Normalisation uncertainty |
| `theo` | Theoretical uncertainty |
| `expe` | Experimental uncertainty (combined stat+syst when not split) |
| `theo:<source>` | Theoretical uncertainty from one named input |

Any other label is rejected. Keep the bare `theo` label for a theory error
that is not attributed to a specific input; when the source splits its
theory error by input parameter, name each input after the colon, e.g.
`theo:mu_pi`, `theo:m2_s0`. `<source>` is lowercase ASCII letters, digits
and underscores only (no spaces, LaTeX, or uppercase). A `type@N_error`
triplet is only allowed when the measurement has **two or more** errors;
every component requires the full `type@N_upper` + `type@N_lower` pair.

**Single vs multiple errors.** If the paper reports exactly one error, record
it as the total error (`total_upper`/`total_lower`), regardless of whether the
source labels it stat/syst/theo. Split errors into `type@N_error` triplets
only when there are two or more components.

### Exactly One Measurement Format

Each `obs@N` uses exactly one error scheme: total error (`value` +
`total_upper`/`total_lower`) for a single error, or component errors (`value`
+ two or more `type@N_error` triplets). In addition it may carry `ref` (an
external reference) and/or confidence-level bounds (`type@N_upper` /
`type@N_lower` + `type@N_level`). A bound-only entry has no `value` and no
errors. A combined fit + bound entry has `value` plus **either** component
errors or total errors, together with the bound slots. Do not mix component
errors with total errors, and do not add `value` to a bound-only entry. All
numeric fields are float-as-strings (`"0.69"`, `"5.9e-6"`).

Unknown keys inside `obs@N` are rejected by the validator. The only
allowed keys are `name`, `value`, `unit`, `ref`,
`dataset`, `note`, the kinematic boundaries, `total_upper`/`total_lower`,
and the `type@N_*` patterns documented here.

### Bound (Limit) Format

Use this format when the paper reports a confidence-level upper or lower
limit rather than a measured central value. A bound occupies its own
`type@N` slot and carries a level but no `type@N_error`:

```json
"obs@1": {
    "name": "Br",
    "type@1_upper": "5.9e-6",
    "type@1_level": "90%@CLs"
}
```

A lower limit uses `type@N_lower`; a two-sided interval may carry both
`type@N_upper` and `type@N_lower` at the same level.

| Field | Description |
|-------|-------------|
| `type@N_upper` | Numeric upper bound at the given confidence level. |
| `type@N_lower` | Numeric lower bound at the given confidence level. |
| `type@N_level` | The confidence level as a string, e.g., `"90%@CLs"`, `"95%@CLs"`. |

**Multiple confidence levels**: use distinct N slots (e.g. `type@1` for the
primary 90% CL and `type@2` for 95%). **Critical:** the bound value and the
level must not be swapped.

### Total Error Format

Use this format whenever the paper reports a single error (combined or not)
and the data comes from the current paper itself (not an external reference):

```json
{
    "name": "FL",
    "value": "0.69",
    "total_upper": "0.039",
    "total_lower": "0.039",
    "q2min": "0.1",
    "q2max": "1.1"
}
```

### Combined Fit + Bound Format

Use this format when the paper reports both a fit result (central value + total
uncertainty) and CLs bounds. Common in BSM searches where the fit can return
a central value near zero (or negative) while the CLs method sets a physical
bound. Both sets of fields are required: `value` +
`total_upper`/`total_lower` (or two or more component triplets) for the fit
result, and `type@N_upper`/`type@N_lower` + `type@N_level` for each confidence
level. Bound slots must use N values distinct from any component errors, e.g.
`type@1_error` + `type@2_error` + `type@3_upper` + `type@3_level`. They come
from different statistical procedures and coexist in the same `obs@N` entry.

### External Reference Format

Use this format for values taken from external sources (PDG world averages, HFLAV combinations, earlier papers). Per `obs-abbr.md` §2.2.2, **ratio observable names use the `R<OBS>[cond]` form** (e.g. `RBr`, `RFL`, `RDeltaGamma`); the transition is carried by the data key. When the ratio is the canonical LFU ratio whose final state is already fixed by the channel key (e.g. \(R(D)\), \(R(D^*)\)), write the bare symbol `R`:

```json
{
    "name": "RBr[mu/e]",
    "value": "0.175",
    "total_upper": "0.012",
    "total_lower": "0.012",
    "ref": "[LHCb:2015svh](https://inspirehep.net/literature/1409497)"
}
```

The `ref` field must be a Markdown link with a verified InspireHEP TexKey. Look up the source paper's arXiv ID from the reference list, then search InspireHEP.

## Correlation and Covariance Matrices

Matrices are **group-level keys** placed alongside the channel keys, never
inside an `obs@N` object:

```json
{
    "B0.2.K*0.mu+.mu-": { "obs@1": { ... }, "obs@2": { ... } },
    "B+.2.K+.mu+.mu-": { "obs@1": { ... } },
    "correlation": [
        [1.0, 0.5, 0.1],
        [0.5, 1.0, 0.2],
        [0.1, 0.2, 1.0]
    ]
}
```

**Rules:**
- **Key** — `correlation` (unit diagonal) or `covariance` (diagonal holds
  the variance). A `type@N_` prefix (`type@1_correlation`) labels a matrix
  describing only that component error and matches `type@N_error`; the
  unprefixed key describes the total uncertainty. A group carries at most
  one unprefixed matrix and one matrix per component prefix; all share the
  same dimension and ordering.
- **Diagonal** — correlation matrices must have 1.0 on the diagonal and
  off-diagonal elements within `[-1, 1]`; covariance diagonals are the
  squared errors and are checked against the reported total uncertainties
  (5% relative tolerance to absorb rounding of the reported errors). Both
  must be symmetric (`M[i][j] == M[j][i]`) with finite numeric elements
  (no `null`, `NaN`, `Infinity`, or booleans).
- **Out-of-range elements** — off-diagonal correlation elements must lie in
  `[-1, 1]`. An element outside that range is an error unless the same
  group carries a group-level `note`, in which case it is reported as a
  warning and the value is imported exactly as published. Do not round the
  value or relax the global `[-1, 1]` rule.
- **Note** — optional group-level `note` (non-empty string) placed after
  `scheme` and before the matrix; it documents the accompanying matrix.
  Keep the explanation factual (what the source prints) and do not use it
  to acknowledge unrelated cells.
- **Dimension** — N×N must equal the total number of observables in all
  channels of the group.
- **Order** — channel keys in written order, then `obs@N` order within each
  channel.
- **Format** — matrix elements are floats (not strings), one row per line.
  Do not put each element on its own line (SKILL.md rule 1).
- If no matrix is available, **omit the key entirely** (do not set `null`).

### Data Grouping

Each element of the `data` array is a **data group** — one measurement
context:

- **Group boundary**: defined by a correlation or covariance matrix. All
  observables linked by the same matrix belong to one group, whether they
  sit in one channel or several.
- **Matrix dimension**: the N×N matrix covers exactly N observables across
  the group's channels.
- **No matrix**: observables without a matrix can share a group or be split
  across groups as appropriate.
- **Several groups**: add another element to the `data` array. Do not merge
  groups whose properties differ (dataset, scheme, fit choice, kinematic
  region).

### Combined Kinematic Bins

When measurements are performed across non-contiguous regions and combined into a single result:

- `q2min` and `q2max` (and similarly `pTmin`/`pTmax`, `etamin`/`etamax`) accept **comma-separated multi-interval** strings.
- Ranges must be paired one-to-one: `"q2min": "11.0,17.5"` with `"q2max": "15.0,+inf"`.
- `"+inf"` denotes an unbounded upper limit. Example: two non-contiguous bins covering [11.0, 15.0] ∪ [17.5, +∞).
- Symbolic endpoints such as `E_max` are invalid; use `"+inf"` when the bound is the kinematic endpoint.

## transition-mode Values

The `transition-mode` field classifies the physical process. All values are
hyphenated property names: decay modes are named by their lepton content,
while scattering/production and precision categories describe the
measurement process.

| Value | Use For | Examples |
|-------|---------|----------|
| `leptonic-decay` | Pure leptonic decays | $B \to \ell\ell$, $\tau \to \mu\mu\mu$ |
| `semileptonic-decay` | Semileptonic decays | $B \to K^{(*)}\ell\ell$, $\Lambda \to p\ell\nu$ |
| `non-leptonic-decay` | Hadronic (non-leptonic) decays | $B \to J/\psi\, p\,\pi$, $B \to D\pi$ |
| `radiative-decay` | Radiative decays | $B \to K^*\gamma$, $B \to X_s\gamma$ |
| `neutron-beta-decay` | Neutron decay observables | $n \to p\,e^-\,\bar{\nu}_e$ correlations |
| `higgs-decay` | Higgs boson decays | $H \to \gamma\gamma$, $H \to ZZ^*$ |
| `mixing` | Mixing, oscillation, and lifetime measurements | $\Delta m_s$, $\Delta\Gamma_s$, $\tau(B_s^0)$ |
| `scattering` | Scattering and production processes | $pp \to W$, $pp \to t\bar{t}$, $e^+e^- \to \mu^+\mu^-$ |
| `electroweak-precision` | Z-pole, W mass, weak mixing angle | LEP/SLC Z-pole |
| `w-production` | W production and decay | Tevatron/LHC W cross sections |
| `higgs-production` | Higgs boson production | $pp \to H$, VBF, $t\bar{t}H$ |
| `low-energy` | Low-energy precision measurements | $g-2$, atomic parity violation |
| `oblique-corrections` | S, T, U parameter fits | New physics constraints |

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
            "obs@1": {
                "name": "MW", "value": 80.3692,
                "total_upper": 0.0133, "total_lower": 0.0133, "unit": "GeV"
            },
            "obs@27": {
                "name": "Br(W2lnu)", "value": 0.1086,
                "total_upper": 0.0009, "total_lower": 0.0009
            },
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
            {
                "name": "Tau(B0)", "value": 1.517,
                "total_upper": 0.004, "total_lower": 0.004, "unit": "ps"
            }
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
- Each observable needs `name`, `value`, and the numeric total error pair
  `total_upper`/`total_lower`. Snapshots never split errors into
  components: write a symmetric source error as an equal pair, and an
  asymmetric interval directly into the two fields. Do not use
  `type@N_*` fields.
- Unknown observable keys are rejected: the only allowed fields are
  `name`, `value`, `total_upper`, `total_lower`, `unit`, `limit`.
- `unit` is a free-form string (`"GeV"`, `"ps"`, `"fb"`).
- Optional subgroup `correlation` is a square N×N matrix whose
  dimension must equal the observable count; `null` is allowed.
- HFLAV observables may carry a free-form `limit` string annotating
  the phase-space or charge combination.

## Key Constraints

1. **All numeric values are strings** (`"0.25"`) except matrix elements (floats). Applies to `value`, the kinematic boundaries (`q2min`/`q2max`, `pTmin`/`pTmax`, ...), and every error/bound field. `unit` is a unit string, not a number.
2. **LaTeX uses double backslash** — in `title`/`abstract`, `\\to` in the JSON file becomes `\to` after `json.load()`.
3. **4-space indentation** — JSON files use exactly 4 spaces per indent level.
4. **Field order** — Top-level fields follow the Top-Level Fields table order; group keys are ordered channels → `dataset` → `scheme` → matrices; each channel value is an `obs@N` object; within `obs@N`, follow the Standard Measurement table.
5. **arxiv format** — `[hep-ex/1512.04442v1](https://arxiv.org/pdf/1512.04442)`; no arXiv ID → `null`. Malformed links and the string `"null"` fail; legacy bare strings pass and a missing `vN` warns.
6. **No `year`/`pdf` fields** — The standard schema has neither a top-level `year` nor `pdf` field (HFLAV/PDG snapshots use `year`; see §Non-Standard Schemas). Citations come from the `arxiv` and `inspire-hep` fields.
7. **Omit empty fields** — Do not include keys with empty string or `null` values (except `arxiv`, which uses `null` when absent).
8. **Top-level key order** — `transition-mode` must immediately precede `data`, and `data` must be the final key in the JSON object.
9. **Matrix layout: row-per-line** — Each `*_correlation`/`*_covariance` row is on a single line. (SKILL.md rule 1.)
10. **Author format** — initials only, 1 / 2 / 3 / 4+ tiers as in the `author` row above (`format_authors()` in `scripts/common.py`; SKILL.md rule 3).
11. **Abstract = single line** — Collapse multi-line `align*`/`gather*`/etc. blocks to single-line LaTeX. Line breaks (`\\`) become `, ` separators, with `and` before the last. (SKILL.md rule 2.)
12. **No Unicode** — Replace all Unicode chars (`μ`, `Δ`, `±`, `×`, `→`, `°`, smart quotes, dashes) with LaTeX equivalents (`\mu`, `\Delta`, `\pm`, `\times`, `\to`, `^{\circ}`, `` ` ``/`'`/`` `` ``/`''`). Latin ligatures from PDF text extraction (`ﬀ`, `ﬁ`, `ﬂ`, `ﬃ`, `ﬄ`) are replaced by their plain letter sequences. Accented Latin letters in author names (`ć`, `č`, `ç`, `ü`, `ø`, `ß`) become LaTeX accents (`\'{c}`, `\v{c}`, `\c{c}`, `\"{u}`, `\o`, `\ss`). The `author`, `title` and `abstract` fields are validated Unicode-free. (SKILL.md rule 4.)
13. **Transition order** — a channel key is `A.B.2.C.D` (`no-transition` is the only exception; ratios join two full keys with `/`) and follows the canonical order (SKILL.md rule 5): baryon → meson → charged lepton → neutral lepton, then heaviest → lightest within each type, then `+` → `-` → `0` for equal masses. Every particle state is `<name>[*]<charge>[Bar]`: charge is mandatory and written `+`/`-`/`0` only (`p`/`m` suffixes and charge-less names are rejected); `*` sits between the name and the charge; neutral antiparticles append capital `Bar` after the charge (lowercase `bar` is rejected). Only neutrinos (`v`/`vBar`, `ve`, `vmu`, `vtau`) and the neutral gauge bosons `Z`, `gamma`, `g` may omit the charge. The validator fails non-canonical order. Particle tokens use the handwritten case (`pi0`, `Lambdab0`, `KS0`, `KL0`); see obs-abbr.md §1.
14. **`data` is an array of groups** — each group maps one or more transition keys (`A.B.2.C.D` or `no-transition`) to an `obs@N` object, optionally carries group-level `dataset`/`scheme` strings, and optionally a group-level matrix; channels that share a matrix belong to the same group (SKILL.md rule 7). JSON data stores no LaTeX for channels or observables.
15. **One group per property set** — observables whose dataset, scheme, fit choice, or kinematic region differ belong to separate groups, even when they share a transition channel (SKILL.md rule 6).
16. **Exactly one error scheme** — a single error is the total error (`total_upper`/`total_lower`); two or more errors are separate component triplets (`type@N_error`/`_upper`/`_lower`). Confidence-level bounds use `type@N_upper`/`type@N_lower` + `type@N_level` with no `type@N_error`; a combined fit + bound uses distinct N slots. Error labels are limited to `stat`, `syst`, `lumi`, `norm`, `theo`, `expe`, plus `theo:<source>` when a theory component comes from a named input. Unknown observable fields are rejected.
17. **`collaboration` is conditional** — required for named collaborations (experiments, HFLAV/PDG, large theory groups such as HPQCD); omit the key for individual-author and small-group papers (SKILL.md rule 8).
18. **Form-factor coefficients use `aN_FF`** — expansion order first, form-factor symbol second (`a0_F+`, `a2_Gv`). When several form factors take the same number, repeat the observable once per symbol (`a0_Gv`, `a0_G+`); never join symbols. The group must declare `scheme`; fit choices are not stored in the name or metadata (SKILL.md rule 9).
19. **`unit` is a physical unit** — never store a scientific-notation scale factor (`1e-6`, `10^{-4}`) in `unit`; multiply it into `value`, `total_upper`/`total_lower`, and any bounds, then omit the field. The validator rejects scale-factor units.
20. **`dataset` lists data sources only** — canonical tokens `LQCD`, `LCSR`, `EXPE` joined by `+` in that order (`LQCD`, `LQCD+LCSR`, `LQCD+LCSR+EXPE`). Analysis techniques, fit choices, and the expansion scheme never go there; experimental groups normally omit the key.
21. **`scheme` is the expansion short code** — form-factor coefficient groups carry exactly `BK`, `BGL`, `BCL`, `BSZ`, or `DLM`; the full names and arXiv IDs are in `obs-abbr.md` §2.4 and are never written into the JSON. The validator rejects any other value.

## Extending This Specification

When a paper introduces metadata or data structures not covered by this document:

1. **Identify the new pattern** — is it a new field, a new error type, a new kinematic variable, or a new data format?
2. **Check existing conventions** — review this document and `obs-abbr.md` for naming patterns that can be extended.
3. **Add the new pattern** to the relevant section of this document.
4. **Update the validator** (`scripts/json-valid.py`) if the new pattern requires structural checks.
5. **Keep it consistent** — use the same naming conventions, string types, and ordering rules as existing fields.

Examples of extensions:
- New kinematic boundary: add `{var}min`/`{var}max` to `DATA_ENTRY_KINEMATIC_FIELDS` and `is_observable_field` in `json-valid.py`
- New error label: add it to `STANDARD_ERROR_LABELS` in `json-valid.py` **and** to the label table above
- New data format (e.g., asymmetric confidence intervals): document as a new subsection under Data Entries and extend `_validate_measurement_scheme` in `json-valid.py`
