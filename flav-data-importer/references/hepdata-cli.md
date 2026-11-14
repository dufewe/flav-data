# hepdata-cli Reference

Access HEPData structured data via `hepdata-cli`, bypassing Cloudflare.

**Install**: `pip install hepdata-cli`

Binary resolution order: `$PATH` → venv `bin/` → `~/.local/bin/` → Homebrew
prefixes. Raises `RuntimeError` with install instructions if not found.

## CLI Commands

This workflow uses only `fetch-names` and `download` (invocations below);
`find` and `upload` exist but are unused.

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

The metadata JSON lists table URLs but not the data itself. `download_table_yaml()`
shells out to `hepdata-cli download -f yaml -t <table>`, so Cloudflare never sees a
plain `curl` — do not re-implement it with `urllib`/`requests`.

```python
hepdata_ext = load_script("hepdata_ext")   # SKILL.md §"Python Helpers"

yaml_text = hepdata_ext.download_table_yaml("1409497", "Table 1")
table_type = hepdata_ext.detect_table_type(yaml_text)  # 'observable' | 'correlation' | 'covariance' | 'unknown'
if table_type == 'observable':
    observables, qualifiers = hepdata_ext.parse_yaml_observables(yaml_text)
else:
    matrix_type, matrix, qualifiers = hepdata_ext.parse_yaml_correlation(yaml_text)
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

`detect_table_type` recognises this shape even with an empty header: a
single dependent variable, **no** independent variable, and a perfect-square
number of values (n², n ≥ 2) is classified as a matrix. Observable tables
always carry an independent kinematic axis, so they are not misclassified.
A `correlation`/`covariance` header (or repeated `CORR`/`COV` independent
variables) takes precedence when present.

## Python API (`scripts/hepdata-ext.py`)

The script wraps the `hepdata-cli` binary and exposes:

| Function | Purpose |
|---|---|
| `fetch_table_names(inspire_id)` → `list[str] \| None` | List table names for a record |
| `download_metadata(inspire_id, output_dir)` → `str \| None` | Download (or reuse an existing matching) metadata JSON |
| `download_table_yaml(inspire_id, table_name)` → `str` | Fetch one table's YAML through `hepdata-cli` |
| `detect_table_type(yaml_text)` → `str` | `'observable'`, `'correlation'`, `'covariance'`, or `'unknown'` (PyYAML missing / unparseable YAML) |
| `parse_yaml_observables(yaml_text)` → `(list[dict], dict)` | Parse observable YAML into per-point entries (incl. `q2min`/`q2max`) |
| `parse_yaml_correlation(yaml_text)` → `(matrix_type: str, matrix: list[list[float]], qualifiers: dict)` | Parse correlation/covariance matrix YAML |
| `parse_metadata(metadata_path)` → `dict` | Parse downloaded metadata JSON |

Constants: `HEPDATA_CLI` (absolute path to binary, or `''`) and
`HAS_YAML` (whether PyYAML is available).

**Loading the script**: `load_script("hepdata_ext")` from SKILL.md
§"Python Helpers" — the hyphen in the filename prevents a direct import.

```python
tables = hepdata_ext.fetch_table_names(1409497)
meta = hepdata_ext.parse_metadata(
    hepdata_ext.download_metadata(1409497, "/tmp/hd")
)
```

### CLI entry point

```bash
python3 flav-data-importer/scripts/hepdata-ext.py 1409497
python3 flav-data-importer/scripts/hepdata-ext.py 1409497 -o /tmp/hd --table "Table 1"
python3 flav-data-importer/scripts/hepdata-ext.py 1409497 --no-write   # stdout only
```

Without `--output_dir` nothing is written; `--no-write` forces stdout-only
even when a directory is given.

## Notes

1. **Must use hepdata-cli** — direct `curl`/`urllib` is blocked by Cloudflare.
2. **Theory papers** rarely have HEPData — check the arXiv ancillary files
   and e-print LaTeX source next (`data-source.md` §4), PDF last.
3. **Table names are passed verbatim** — `hepdata-cli` handles quoting/encoding.
4. **Missing matrix entries**: `value: "-"` (or any non-numeric cell) is
   substituted with `0.0` and reported as a warning, keeping the matrix square.
5. **PyYAML** required for YAML parsers (`pip install pyyaml`).
