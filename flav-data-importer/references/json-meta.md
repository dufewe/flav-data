# JSON Metadata Structure

This document is the authoritative specification for the flav-data JSON format. Every JSON file in the database must conform to this structure.

## Top-Level Structure

Each paper (experimental or theoretical) corresponds to exactly one JSON file:

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
            "obs@1": { ... },
            "obs@2": { ... },
            "type@1_correlation": [[1.0, 0.5, 0.1], [0.5, 1.0, 0.2], [0.1, 0.2, 1.0]]
        }
    ],
    "transition-mode": "semileptonic decay"
}
```

## Top-Level Metadata Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `inspire-hep` | string | Yes | Markdown link: `[TexKey](https://inspirehep.net/literature/{recid})`. TexKey is the InspireHEP BibTeX citation key; recid is the control number. Always verify via InspireHEP API. | `[LHCb:2015svh](https://inspirehep.net/literature/1409497)` |
| `author` | string | Yes | Format: `"name1 and others"` where name1 is the first author's full name from InspireHEP. If no person names are found (e.g., some older records), fall back to `"{group} collaboration"`. | `Aaij, Roel and others` |
| `collaboration` | string | Yes | The experimental collaboration or theory group name. For multi-collaboration papers, use comma-separated names (e.g., `"ATLAS, CMS"`). | `LHCb` |
| `title` | string | Yes | The paper title from the latest InspireHEP or arXiv version. Must preserve LaTeX for any formulas. Double-backslash escaped in JSON. Prefer arXiv-sourced titles. | `Angular analysis of the $B^{0}\\to K^{*0}\\mu^{+}\\mu^{-}$ decay` |
| `arxiv` | string/null | Yes | Markdown link: `[primary_category/arxiv_idvN](https://arxiv.org/pdf/{id})`. The version number (vN) must match the article version from which data was cited. If no arXiv ID exists (e.g., some older journal-only papers), set to `null`. | `[hep-ex/1512.04442v1](https://arxiv.org/pdf/1512.04442)` |
| `time` | string | Yes | arXiv v1 first submission date in `YYYY.MM.DD` format (dot-separated). If no arXiv v1 date exists, use the journal acceptance date instead. Database file indexing is based on this date. | `2015.12.14` |
| `abstract` | string | Yes | The complete abstract from the latest arXiv version. Must preserve LaTeX for any formulas. If no arXiv abstract is available, use the journal abstract. | `An angular analysis of the...` |
| `pdf` | string | Yes | URL to the paper PDF. Prefer the arXiv PDF URL. If no arXiv page exists, fall back to the InspireHEP file URL or the journal article homepage. | `https://arxiv.org/pdf/1512.04442` |
| `data` | array | Yes | Array of data entries, one per q² bin, dataset, or measurement group. Each entry contains `obs@N` observables and optionally correlation/covariance matrices. **Allowed fields: `obs@N`, `type@N_correlation`, `type@N_covariance`, `tot_correlation`, `tot_covariance`.** | See Data Entries section |
| `transition-mode` | string | Yes | **Must be the last field in the JSON file.** Describes the physical process type. Only "scattering" and "decay" are valid top-level categories, subdivided by specific property. Do NOT use non-property descriptors like "rare decay". | `semileptonic decay` |

## Metadata Field Sources

| Field | Source | Notes |
|-------|--------|-------|
| `inspire-hep` | InspireHEP BibTeX info | `[TexKey](https://inspirehep.net/literature/{recid})` |
| `author` | InspireHEP BibTeX info | `"name1 and others"` format |
| `collaboration` | InspireHEP BibTeX info | Collaboration name |
| `title` | InspireHEP (arXiv-sourced preferred) | Preserves LaTeX |
| `abstract` | InspireHEP (arXiv-sourced preferred) | Preserves LaTeX |
| `arxiv` | arXiv webpage | `[primary_category/arxiv_idvN](url)` |
| `time` | arXiv webpage | v1 submission date, `YYYY.MM.DD` |
| `pdf` | arXiv webpage (preferred) | Fallback to InspireHEP or journal link |
| `transition-mode` | Paper information | Property-based decay/scattering name |
| `data` | Extracted from data source | HEPData, CDS, PDF, etc. |

## Data Entries (data[])

Each element in the `data` array represents one measurement context — typically one q² bin, one dataset, or one fit scenario. Different q² bins of the same observable go into separate `data[]` entries with identical `name` fields but different `q2min`/`q2max` values.

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
| `name` | Yes | string | Observable identifier in `OBS(transition)[condition]` format. Symbolic notation only — no full expression definitions. |
| `latex` | Yes | string | LaTeX representation of the observable name. Use `\\` for backslashes in JSON (becomes single `\` after parsing). |
| `value` | Yes | string | Central value. Must be a string, even for integers. |
| `type@1_err` | Yes | string | Error type label for the first error component (usually `"stat"`). |
| `type@1_err_up` | Yes | string | Upper error bound for type 1. For symmetric errors, equals `type@1_err_down`. |
| `type@1_err_down` | Yes | string | Lower error bound for type 1. |
| `type@N_err` | No | string | Additional error type labels (e.g., `"syst"`, `"lumi"`, `"norm"`, `"theo"`). Each additional error type requires its own `_err`, `_err_up`, and `_err_down` triplet. |
| `type@N_err_up` | No | string | Upper error for type N. |
| `type@N_err_down` | No | string | Lower error for type N. |
| `q2min` | Conditional | string | Lower kinematic boundary (usually q² in GeV²). If only an upper bound exists, use the literal string `"q2min"`. |
| `q2max` | Conditional | string | Upper kinematic boundary. If only a lower bound exists, use the literal string `"q2max"`. |
| `pTmin`/`pTmax` | Conditional | string | Transverse momentum boundaries. Use instead of q² for non-decay processes. |
| `etamin`/`etamax` | Conditional | string | Pseudorapidity boundaries. |
| `unit` | Conditional | string | Physical unit (e.g., `"GeV"`, `"ps"`, `"fb"`). Omit for dimensionless observables. |
| `ref` | Conditional | string | External reference as Markdown link for cited values. Look up the arXiv ID in the paper's references, then search InspireHEP for the correct TexKey. Never guess. |

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
| `type@N_level` | The confidence level as a string, e.g., `"90%@CLs"`, `"95%@CL"`, `"90%@CL"`. |

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

### External Reference Format

Use this format for values taken from external sources (PDG world averages, HFLAV combinations, earlier papers):

```json
{
    "name": "R(Lambda.2.p)[mu/e]",
    "latex": "$\\mathcal{R}_{\\Lambda \\to p}^{\\mu/e}$",
    "value": "0.175",
    "tot_err_up": "0.012",
    "tot_err_down": "0.012",
    "ref": "[ParticleDataGroup:2024cfk](https://inspirehep.net/literature/2817040)"
}
```

The `ref` field must be a Markdown link with a verified InspireHEP TexKey. Look up the source paper's arXiv ID from the reference list, then search InspireHEP.

### Correlation and Covariance Matrices

### Correlation Matrix (`type@N_correlation`)

Placed at the data entry level (alongside `obs@N` keys, not inside any obs):

```json
"type@1_correlation": [[1.0, 0.5, 0.1], [0.5, 1.0, 0.2], [0.1, 0.2, 1.0]]
```

**Rules:**
- **Diagonal elements must be 1.0** (correlation of an observable with itself).
- **Matrix must be symmetric**: `M[i][j] == M[j][i]`.
- **Dimension**: matrix size (N×N) must equal the number of `obs@N` entries in the same data entry.
- **Order**: matrix indices correspond to obs@N numbering order (obs@1 → index 0, obs@2 → index 1, etc.).
- **Naming**: use `type@1_correlation` to match `type@1_err` (stat), `type@2_correlation` to match `type@2_err` (syst), etc.
- **Format**: matrix elements are floats (not strings).
- If no correlation matrix is available, **omit the field entirely** (do not set to `null`).

### Total Error Correlation/Covariance (`tot_correlation`, `tot_covariance`)

When using the total error format (`tot_err_up`/`tot_err_down` without separate `type@N_err` components), the matrix fields use the `tot_` prefix:

```json
"tot_correlation": [[1.0, 0.5], [0.5, 1.0]]
```

**Rules:** Same as `type@N_correlation`/`type@N_covariance` above. The `tot_` prefix corresponds to the `tot_err` naming. Do NOT use `tot_correlation` when component errors (`type@N_err`) are present — use `type@N_correlation` matching the specific error type instead.

### Covariance Matrix (`type@N_covariance`)

```json
"type@1_covariance": [[0.01, 0.005], [0.005, 0.01]]
```

**Rules:**
- **Matrix must be symmetric**.
- **Diagonal elements** are the variances (error squared) for each observable. These must be manually verified against the reported errors.
- **Dimension and order** follow the same rules as correlation matrices.
- Matrix elements are floats.
- Omit the field if not available.

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

## Key Constraints

1. **All numeric values are strings** — `"0.25"` not `0.25`. Applies to `value`, `q2min`, `q2max`, `pTmin`, `pTmax`, all error fields, and `unit`. Exception: correlation/covariance matrix elements are floats.
2. **LaTeX uses double backslash** — `\\to` in the JSON file. After `json.load()`, this becomes `\to` in Python.
3. **4-space indentation** — JSON files use exactly 4 spaces per indent level.
4. **Field order** — Top-level fields follow the order documented in the Top-Level Fields table. Within obs@N, follow the field order shown in the Standard Measurement table.
5. **arxiv format** — Must include primary category and version: `[hep-ex/1512.04442v1](https://arxiv.org/pdf/1512.04442)`. If no arXiv ID, use `null`.
6. **No `year` field** — The database does not support a top-level `year` field.
7. **Omit empty fields** — Do not include keys with empty string or `null` values (except `arxiv` which uses `null` when absent).
8. **transition-mode last** — This field must always be the final key in the JSON object.

## Extending This Specification

When a paper introduces metadata or data structures not covered by this document:

1. **Identify the new pattern** — is it a new field, a new error type, a new kinematic variable, or a new data format?
2. **Check existing conventions** — review this document and `references/obs-abbr.md` for naming patterns that can be extended.
3. **Add the new pattern** to the relevant section of this document.
4. **Update the validator** (`scripts/json-valid.py`) if the new pattern requires structural checks.
5. **Keep it consistent** — use the same naming conventions, string types, and ordering rules as existing fields.

Examples of extensions:
- New kinematic boundary: add `{var}min`/`{var}max` to the Numeric Field Patterns list
- New error type: add `type@N_err` triplet with a descriptive label
- New data format (e.g., asymmetric confidence intervals): document as a new subsection under Data Entries
