# Workflow Example: Importing LHCb:2015svh

This document walks through the complete process of importing data from a real paper into the flav-data database.

**Paper**: Angular analysis of the B⁰→K*⁰μ⁺μ⁻ decay
**arXiv**: 1512.04442 | **Inspire recid**: 1409497 | **HEPData**: 83 tables | **Published**: JHEP 02 (2016) 104

## Step 1: Search for Existing Entry

Check whether this paper's data is already in the database:

```python
import json, os

base = 'Experimental/CERN-LHCb'
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
- `TexKey`: `"LHCb:2015svh"`
- `recid`: `1409497`
- `preprint_date`: `"2015-12-14"` → `time: "2015.12.14"`
- `collaborations`: `[{"value": "LHCb"}]`
- `titles` (arXiv source): `"Angular analysis of the $B^{0}\\to K^{*0}\\mu^{+}\\mu^{-}$ decay"`
- `abstracts` (arXiv source): `"An angular analysis of the..."`
- `authors`: 500+ → `author: "Aaij, R. and others"` (InspireHEP BibTeX form; convert from `"Aaij, Roel and others"`)

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

**Table classification** (83 tables = 8 observable tables + 75 matrix tables):
- **Tables 1–8: observables.** Table 1 has 22 observables at 2 q² bins; Table 2 has 8 CP-averaged observables (FL, S3–S9) at 8 bins; Tables 3–4 are the CP-asymmetric (A3–A9) and optimised (P1–P3, P'4/5/8) sets at 8 bins; Tables 5–7 repeat those sets with the method of moments at 15 bins; Table 8 holds zero-crossing points.
- **Tables 9–38: likelihood correlation matrices**, three 10-table sets with the same q² binning — 8 individual bins plus the merged ranges 1.1–6.0 and 15.0–19.0. Each matrix is 8×8 and belongs to one observable set; pick the set that matches the observables you imported.
- **Tables 39–53, 54–68, 69–83: bootstrap correlation matrices**, three 15-table sets using the finer q² binning (0.1–8, 11–12.5, 15–19). The 39–53 and 69–83 sets are 8×8; 54–68 is 7×7.

Do not classify by table description alone — `hepdata-ext.detect_table_type()`
inspects the YAML (a single dependent variable over 64/49 cells is a matrix;
repeated `CORR`-style independent variables confirm it).

**Download individual tables** (the CLI handles quoting; no URL-encoding needed):

```bash
python3 flav-data-importer/scripts/hepdata-ext.py 1409497 \
  --output_dir <output_dir> --table "Table 1"

python3 flav-data-importer/scripts/hepdata-ext.py 1409497 \
  --output_dir <output_dir> --table "Table 9"
```

## Step 4: Build JSON

Parse the YAML tables and construct the JSON entry:

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
    "transition-mode": "semileptonic-decay",
    "data": {
        "B0.2.Kst0.mu+.mu-": [
            {
                "obs@1": {
                    "name": "FL",
                    "latex": "$F_L(B^{0}\\to K^{*0}\\mu^{+}\\mu^{-})$",
                    "value": "0.69",
                    "type@1_error": "stat",
                    "type@1_upper": "0.035",
                    "type@1_lower": "0.036",
                    "type@2_error": "syst",
                    "type@2_upper": "0.017",
                    "type@2_lower": "0.017",
                    "q2min": "0.1",
                    "q2max": "1.1"
                },
                "obs@2": {
                    "name": "S3",
                    "latex": "$S_3(B^{0}\\to K^{*0}\\mu^{+}\\mu^{-})$",
                    "value": "0.012",
                    "type@1_error": "stat",
                    "type@1_upper": "0.038",
                    "type@1_lower": "0.038",
                    "type@2_error": "syst",
                    "type@2_upper": "0.004",
                    "type@2_lower": "0.004",
                    "q2min": "0.1",
                    "q2max": "1.1"
                },
                "...": "...",
                "type@1_correlation": [[1.0, 0.06, ...], [0.06, 1.0, ...], ...]
            }
        ]
    }
}
```

Each q² bin from the paper becomes a separate element in that channel's
`data` group array — its own group. The correlation matrix from
Table 9 goes into the first group (low q² bin), Table 10 into the
second, and so on. Observables coupled by one source matrix (including
angular and differential ones) stay together in that group
(SKILL.md rule 6).

## Step 5: Write File and Update Index

```bash
# Create directory structure
mkdir -p Experimental/CERN-LHCb/2015/12

# Write JSON file
# → Experimental/CERN-LHCb/2015/12/LHCb:2015svh.json
```

**Update the annual index** at `Experimental/CERN-LHCb/2015/LHCb@2015.json`:

```json
{
    "12": ["LHCb:2015svh"]
}
```

If the index already had entries for other months, preserve them and add month "12".

## Step 6: Validate

```bash
python3 flav-data-importer/scripts/json-valid.py \
  Experimental/CERN-LHCb/2015/12/LHCb:2015svh.json
```

Expected output:
```console
Validating: Experimental/CERN-LHCb/2015/12/LHCb:2015svh.json
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

1. **HEPData has 83 tables** — use `detect_table_type()` (structure-based), not the description text, to separate observables from matrices.
2. **Multiple correlation matrix sets** — Appendices C–H provide likelihood and bootstrap matrices for the same q² bins; choose one set (likelihood is the paper's nominal result) and keep its binning consistent with the observable table you imported.
3. **One group per q² bin** — each bin requires its own element in that channel's `data` group array.
4. **Observable naming** — use `FL(B0.2.Kst0.mu+.mu-)`: abbreviation + (transition). The transition follows canonical order (`obs-abbr.md` §1): `.2.` separates initial/final states, particles ordered baryon -> meson -> charged lepton -> neutral lepton, then heaviest -> lightest within a type, then `+` -> `-` -> `0` for equal masses; hadrons capitalized, leptons lowercase.
5. **LaTeX escaping** — `\\to` in JSON becomes `\to` after parsing.
6. **arxiv field** — must include primary category and version: `[hep-ex/1512.04442v1](...)`.
7. **transition-mode** — use the hyphenated property names (e.g. `"semileptonic-decay"`), never "rare decay".
8. **Folder naming** — `Experimental/CERN-LHCb/` (Lab-Collaboration), data file uses collaboration name only.
