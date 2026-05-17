# Workflow Example: Importing LHCb:2015svh

This document walks through the complete process of importing data from a real paper into the flav-data database.

**Paper**: Angular analysis of the B⁰→K*⁰μ⁺μ⁻ decay
**arXiv**: 1512.04442 | **Inspire recid**: 1409497 | **HEPData**: 83 tables | **Published**: JHEP 02 (2016) 104

## Step 1: Search for Existing Entry

Check whether this paper's data is already in the database:

```python
import json, os

base = 'Experimental/LHCb'
target = 'LHCb:2015svh'

for year in sorted(os.listdir(base)):
    if year.isdigit():
        idx_path = os.path.join(base, year, f'LHCb@{year}.json')
        if os.path.exists(idx_path):
            index = json.load(open(idx_path))
            for month, files in index.items():
                if target in files:
                    print(f"Already exists: {year}/{month}/{target}.json")
                    break
```

**Result**: Not found → proceed with import.

## Step 2: Retrieve Metadata

### From InspireHEP

```bash
curl -s -H 'Accept: application/json' \
  'https://inspirehep.net/api/literature?q=eprint:1512.04442'
```

Extract:
- `texkey`: `"LHCb:2015svh"`
- `recid`: `1409497`
- `preprint_date`: `"2015-12-14"` → `time: "2015.12.14"`
- `collaborations`: `[{"value": "LHCb"}]`
- `titles` (arXiv source): `"Angular analysis of the $B^{0}\\to K^{*0}\\mu^{+}\\mu^{-}$ decay"`
- `abstracts` (arXiv source): `"An angular analysis of the..."`
- `authors`: 500+ → `author: "Aaij, Roel and others"`

### From arXiv

```bash
curl -sL "https://export.arxiv.org/api/query?id_list=1512.04442"
```

Extract:
- `published`: `"2015-12-14T16:00:00Z"` → confirms `time: "2015.12.14"`
- `primary_category`: `"hep-ex"`
- `<atom:id>`: `"http://arxiv.org/abs/1512.04442v1"` → version `v1`

Construct the `arxiv` field: `[hep-ex/1512.04442v1](https://arxiv.org/pdf/1512.04442)`

## Step 3: Retrieve Data from HEPData

```bash
HEPDATA_CLI="hepdata-cli"

# List tables
$HEPDATA_CLI fetch-names -i inspire 1409497
# Returns: ["Table 1", "Table 2", ..., "Table 83"]

# Download metadata
$HEPDATA_CLI download -f json -i inspire 1409497 -d <output_dir>
```

**Table classification**:
- Tables 1–8: Angular observables per q² bin (FL, S3–S9, A3–A9, P1–P3, P'₄, P'₅, P'₈)
- Tables 9–18: Likelihood correlation matrices (Appendix C) — 8 bins × 1 matrix each
- Tables 19–28: Likelihood correlation matrices (Appendix D)
- Tables 29–38: Likelihood correlation matrices (Appendix E)
- Tables 39–53: Bootstrap correlation matrices (Appendix F)
- Tables 54–68: Bootstrap correlation matrices (Appendix G)
- Tables 69–83: Bootstrap correlation matrices (Appendix H)

**Download individual tables** (URL-encode spaces):

```bash
curl -sL -A "Mozilla/5.0" \
  "https://www.hepdata.net/download/table/ins1409497/Table%201/yaml" \
  > <output_dir>/table1.yaml

curl -sL -A "Mozilla/5.0" \
  "https://www.hepdata.net/download/table/ins1409497/Table%209/yaml" \
  > <output_dir>/table9.yaml
```

## Step 4: Build JSON

Parse the YAML tables and construct the JSON entry:

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
            },
            "obs@2": {
                "name": "S3(B0.2.Kst0.mu+.mu-)",
                "latex": "$S_3(B^{0}\\to K^{*0}\\mu^{+}\\mu^{-})$",
                "value": "0.012",
                "type@1_err": "stat",
                "type@1_err_up": "0.038",
                "type@1_err_down": "0.038",
                "type@2_err": "syst",
                "type@2_err_up": "0.004",
                "type@2_err_down": "0.004",
                "q2min": "0.1",
                "q2max": "1.1"
            },
            "...": "...",
            "type@1_correlation": [[1.0, 0.06, ...], [0.06, 1.0, ...], ...]
        }
    ],
    "transition-mode": "semileptonic decay"
}
```

Each q² bin from the paper becomes a separate `data[]` entry. The correlation matrix from Table 9 goes into the first entry (low q² bin), Table 10 into the second, and so on.

## Step 5: Write File and Update Index

```bash
# Create directory structure
mkdir -p Experimental/LHCb/2015/12

# Write JSON file
# → Experimental/LHCb/2015/12/LHCb:2015svh.json
```

**Update the annual index** at `Experimental/LHCb/2015/LHCb@2015.json`:

```json
{
    "12": ["LHCb:2015svh"]
}
```

If the index already had entries for other months, preserve them and add month "12".

## Step 6: Validate

```bash
python3 scripts/json-valid.py \
  Experimental/LHCb/2015/12/LHCb:2015svh.json
```

Expected output:
```
Validating: Experimental/LHCb/2015/12/LHCb:2015svh.json
  [OK] JSON format correct
  [OK] Top-level fields complete
  [OK] All checks passed
All files validated successfully.
```

## Step 7: Cleanup

```bash
rm -rf <output_dir>
```

Remove all temporary PDFs, YAML files, and intermediate JSONs.

## Key Lessons

1. **HEPData has 83 tables** — distinguish observable tables from correlation matrices by description.
2. **Multiple correlation matrix sets** — Appendices C–H each provide matrices for all q² bins using different statistical methods (likelihood vs bootstrap).
3. **Many q² bins** — each bin requires its own `data[]` entry.
4. **Observable naming** — use `FL(B0.2.Kst0.mu+.mu-)`: abbreviation + (transition).
5. **LaTeX escaping** — `\\to` in JSON (double backslash), becomes `\to` after parsing.
6. **arxiv field** — must include primary category and version: `[hep-ex/1512.04442v1](...)`.
7. **transition-mode** — use property-based names like "semileptonic decay", never "rare decay".
8. **Folder naming** — `Experimental/LHCb/` (collaboration name only).
