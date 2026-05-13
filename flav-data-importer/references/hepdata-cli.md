# hepdata-cli Reference

This document describes how to use the `hepdata-cli` binary to access HEPData structured data.

## Overview

- **Path**: `/hepdata-cli`
- **Purpose**: Fetch high-energy physics experimental data from HEPData, bypassing Cloudflare protection.
- **Input**: InspireHEP control number (recid) or HEPData record ID.
- **Output**: JSON metadata and YAML table data.

## Commands

```bash
hepdata-cli --help

Commands:
  download     Download HEPData record data (metadata + table URLs)
  fetch-names  List available table names for a record
  find         Search HEPData records by keyword or ID
  upload       Upload data to HEPData (not used in this workflow)
```

## Workflow

### Step 1: List Available Tables

```bash
hepdata-cli fetch-names -i inspire 1409497
```

Returns a JSON array of table names:
```json
["Table 1", "Table 2", "Table 3", ..., "Table 83"]
```

### Step 2: Download Metadata

```bash
hepdata-cli download -f json -i inspire 1409497 -d /tmp/hepdata_out
```

Downloads a JSON file containing:

| Field | Description |
|-------|-------------|
| `recid` | HEPData record ID |
| `inspire_id` | Corresponding InspireHEP control number |
| `hepdata_doi` | HEPData DOI for the record |
| `record` | Paper metadata (title, arXiv ID, DOI, collaborations, year, abstract) |
| `data_tables` | Array of table objects with names, descriptions, and download URLs |

Each table in `data_tables`:
```json
{
  "name": "Table 1",
  "description": "CP-averaged angular observables in the low q² bin",
  "location": "Data from Appendix A, Table 3",
  "doi": "10.17182/hepdata.74247.v1/t1",
  "data": {
    "csv": "https://www.hepdata.net/download/table/ins1409497/Table 1/csv",
    "json": "https://www.hepdata.net/download/table/ins1409497/Table 1/json",
    "yaml": "https://www.hepdata.net/download/table/ins1409497/Table 1/yaml"
  }
}
```

### Step 3: Download Individual Tables

The metadata JSON contains URLs but not the actual data. Download tables via curl:

```bash
# URL-encode table names (spaces → %20, + → %2B, # → %23)
curl -sL -A "Mozilla/5.0" \
  "https://www.hepdata.net/download/table/ins1409497/Table%201/yaml"
```

**Why YAML**: YAML preserves the structured hierarchy of observables, qualifiers, and errors better than CSV or JSON for HEPData's nested format.

## YAML Data Structure

### Observable Tables

```yaml
dependent_variables:
- header: {name: '$F_L$'}              # Observable name (LaTeX)
  qualifiers:
  - {name: RE, value: 'P P --> B0 < K*0 ...'}   # Reaction
  - {name: SQRT(S), units: GeV, value: '7000.0'} # Center-of-mass energy
  values:
  - errors:
    - asymerror: {minus: -0.036, plus: 0.035}
      label: stat
    - {label: sys, symerror: 0.017}
    value: 0.69                          # Central value
```

**Key fields:**
- `dependent_variables[].header.name` — Observable name in LaTeX
- `dependent_variables[].values[].value` — Central value
- `dependent_variables[].values[].errors[].label` — Error type (`stat`, `sys`, etc.)
- `dependent_variables[].values[].errors[].symerror` — Symmetric error value
- `dependent_variables[].values[].errors[].asymerror` — Asymmetric error with `plus` and `minus`
- `qualifiers[].name` — Kinematic variable name (e.g., $q^2$, RE, SQRT(S))
- `qualifiers[].value` — Kinematic variable value or range (e.g., `0.1-0.98`)

### Correlation/Covariance Matrices

```yaml
dependent_variables:
- header: {name: ''}
  qualifiers:
  - {name: '$q^2$', units: GeV^2, value: 0.1-0.98}
  values:
  - {value: 1.0}    # [0,0]
  - {value: 0.06}   # [0,1]
  - {value: 0.0}    # [0,2]
  ...
```

Values are listed in row-major order. To reconstruct the N×N matrix:
```python
n = int(len(values) ** 0.5)
matrix = [values[i*n:(i+1)*n] for i in range(n)]
```

## Notes

1. **Must use hepdata-cli** — Direct curl to hepdata.net will be blocked by Cloudflare.
2. **Theory papers** typically lack HEPData entries — fall through to PDF extraction.
3. **URL-encode table names** — "Table 1" → "Table%201", "Table 3 (low)" → "Table%203%20(low)".
4. **Invalid values** — Some bins may have `value: "-"` (meaning no measurement). Skip these.
5. **Units** — The `units` field may contain strings like `"10^-8"` that need conversion.
6. **User-Agent** — Always set a User-Agent header in curl requests to hepdata.net.
