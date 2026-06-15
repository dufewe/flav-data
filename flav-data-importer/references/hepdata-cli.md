# hepdata-cli Reference

Access HEPData structured data via `hepdata-cli`, bypassing Cloudflare.

**Install**: `pip install hepdata-cli`

Binary resolution order: `$PATH` → venv `bin/` → `~/.local/bin/` → Homebrew
prefixes. Raises `RuntimeError` with install instructions if not found.

## CLI Commands

```bash
hepdata-cli --help
  download     Download HEPData record data (metadata + table URLs)
  fetch-names  List available table names for a record
  find         Search HEPData records by keyword or ID
  upload       Upload data to HEPData (not used in this workflow)
```

## Workflow

### Step 1: List Available Tables

```bash
hepdata-cli fetch-names -i inspire 1409497
# → ["Table 1", "Table 2", "Table 3", ..., "Table 83"]
```

### Step 2: Download Metadata

```bash
hepdata-cli download -f json -i inspire 1409497 -d <output_dir>
```

The metadata JSON contains a `data_tables` array; each table has `name`,
`description`, and download URLs (csv/json/yaml).

### Step 3: Download Individual Tables

The metadata JSON contains URLs but not the actual data. Download via curl:

```bash
# URL-encode table names (spaces → %20, + → %2B, # → %23)
curl -sL -A "Mozilla/5.0" \
  "https://www.hepdata.net/download/table/ins1409497/Table%201/yaml"
```

YAML is preferred because it preserves the structured hierarchy of observables,
qualifiers, and errors better than CSV or JSON for HEPData's nested format.

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

## Python API (`scripts/hepdata-ext.py`)

The script wraps the `hepdata-cli` binary and exposes:

| Function | Purpose |
|---|---|
| `fetch_table_names(inspire_id)` → `list[str] \| None` | List table names for a record |
| `download_metadata(inspire_id, output_dir)` → `str \| None` | Download metadata JSON to dir |
| `download_table_yaml(inspire_id, table_name)` → `str` | Direct HTTP download of YAML (may be blocked by Cloudflare) |
| `parse_yaml_observables(yaml_text)` → `(list[dict], dict)` | Parse observable YAML into structured entries |
| `parse_yaml_correlation(yaml_text)` → `(str, list[list[float]], dict)` | Parse correlation/covariance matrix YAML |
| `parse_metadata(metadata_path)` → `dict` | Parse downloaded metadata JSON |

Constants: `HEPDATA_CLI` (absolute path to binary, or `''`) and
`HAS_YAML` (whether PyYAML is available).

**Loading the script** (hyphen in filename prevents direct import):
```python
import importlib.util, os
spec = importlib.util.spec_from_file_location(
    "hepdata_ext", "scripts/hepdata-ext.py",
)
hepdata_ext = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hepdata_ext)

tables = hepdata_ext.fetch_table_names(1409497)
meta = hepdata_ext.parse_metadata(
    hepdata_ext.download_metadata(1409497, "/tmp/hd")
)
```

### CLI entry point

```bash
python3 scripts/hepdata-ext.py 1409497
python3 scripts/hepdata-ext.py 1409497 -o /tmp/hd --table "Table 1"
```

## Notes

1. **Must use hepdata-cli** — direct curl is blocked by Cloudflare.
2. **Theory papers** rarely have HEPData — fall through to PDF extraction.
3. **URL-encode table names**: `"Table 1"` → `"Table%201"`.
4. **Invalid values**: bins with `value: "-"` mean no measurement — skip.
5. **PyYAML** required for YAML parsers (`pip install pyyaml`).
