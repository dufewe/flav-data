---
name: flav-data-importer
category: data-science
description: Import experimental flavor physics data from arXiv/HEPData/CDS into the flav-data JSON format and directory structure. Supports LHCb, ATLAS, CMS, Belle, BaBar, LEP, PDG, and HFLAV.
tags: [flav-data, lhcb, hepdata, json-import, streamlit]
---

# flav-data Importer

Import experimental flavor physics data into the `flav-data` Streamlit application's JSON format and directory structure.

## When to Use

- Adding new experimental measurements to flav-data (LHCb, ATLAS, CMS, Belle, BaBar, LEP, PDG, HFLAV)
- Updating existing JSON files with new data from papers
- Creating index files (`{group}@{year}.json`) for the Streamlit dashboard
- Extracting observables, correlation matrices, and metadata from HEPData, CDS, or arXiv PDFs

## Directory Structure

```
flav-data/Experimental/{group}/{year}/{month}/{file_id}.json
flav-data/Experimental/{group}/{year}/{group}@{year}.json        <-- index file
```

**Supported groups**: ATLAS, BaBar, Belle, CDF, CMS, HFLAV, LEP, LHCb, PDG

**Example paths**:
```
Experimental/LHCb/2025/04/LHCb:2025rfy.json
Experimental/LHCb/2025/LHCb@2025.json          <-- index
Experimental/CMS/2024/CMS@2024.json            <-- index
```

## Index File Format

Each year has an index file mapping months to file IDs:

```json
{
    "02": ["LHCb:2025bfy", "LHCb:2025pxz"],
    "04": ["LHCb:2025rfy", "LHCb:2025evf"],
    "05": ["LHCb:2025ilq", "LHCb:2025nob"],
    "12": ["LHCb:2025kfp"]
}
```

- Keys are zero-padded month strings ("01" to "12")
- Values are arrays of file IDs (without `.json` extension)
- File IDs typically follow the pattern `{Collaboration}:{YYYY}{inspire_suffix}`

## JSON File Format

Each paper/measurement is a single JSON file with this structure:

```json
{
    "inspire-hep": "[LHCb:2025rfy](https://inspirehep.net/literature/2909896)",
    "author": "Aaij, Roel and others",
    "collaboration": "LHCb",
    "title": "Angular analysis of the decay $B^0_s \\\\to \\\\phi e^+ e^-$",
    "arxiv": "[hep-ex/2504.06346v2](https://arxiv.org/pdf/2504.06346)",
    "time": "2025.04.08",
    "abstract": "an angular analysis of the decay...",
    "pdf": "https://arxiv.org/pdf/2504.06346",
    "data": [
        {
            "obs@1": {
                "name": "FL(Bs0.2.phi.e+.e-)",
                "latex": "$F_L(B^0_s\\\\to \\\\phi e^+e^-)$",
                "value": "0.25",
                "type@1_err": "stat",
                "type@1_err_up": "0.12",
                "type@1_err_down": "0.12",
                "type@2_err": "syst",
                "type@2_err_up": "0.06",
                "type@2_err_down": "0.06",
                "q2min": "0.1",
                "q2max": "1.1"
            },
            "obs@2": { ... },
            "obs@3": { ... },
            "obs@4": { ... }
        },
        {
            "obs@1": { ... },
            "tot_correlation": [[1.0, 0.5, ...], [0.5, 1.0, ...], ...]
        }
    ],
    "transition-mode": "semi-leptonic decay"
}
```

### Field Specifications

**Top-level metadata** (required order):
1. `inspire-hep` - Markdown link: `[InspireID](https://inspirehep.net/literature/{id})`
2. `author` - Author list (e.g., `"Aaij, Roel and others"`)
3. `collaboration` - Experiment name (`"LHCb"`, `"ATLAS"`, etc.)
4. `title` - Paper title (LaTeX format, double-escaped backslashes)
5. `arxiv` - Markdown link: `[arxiv_id](https://arxiv.org/pdf/{id})`
6. `time` - v1 submission date in `YYYY.MM.DD` format
7. `abstract` - Paper abstract (LaTeX format)
8. `pdf` - PDF URL (usually `https://arxiv.org/pdf/{arxiv_id}`)
9. `data` - Array of data entries (one per q2 range / dataset)

**Observation fields** (`obs@N`):
1. `name` - Observable identifier (format: `OBS(decay_mode)`)
2. `latex` - LaTeX representation (double-escaped in JSON)
3. `value` - Central value as **string**
4. `type@1_err` - Error type 1 name (usually `"stat"`)
5. `type@1_err_up` - Upper statistical error as string
6. `type@1_err_down` - Lower statistical error as string
7. `type@2_err` - Error type 2 name (usually `"syst"`)
8. `type@2_err_up` - Upper systematic error as string
9. `type@2_err_down` - Lower systematic error as string
10. `q2min` - q2 minimum as string (or other bin boundary)
11. `q2max` - q2 maximum as string

**Note**: Reference values from external sources (PDG, other papers) may use a different format:
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
Use the `ref` field to cite the external source. Error fields can be `tot_err_up/down` for total uncertainty.

### Correlation matrix:
- Use `tot_correlation` at the data entry level (not inside obs@N)
- Compact single-line array format: `[[1.0, 0.5, ...], [0.5, 1.0, ...], ...]`
- Diagonal must be 1.0, matrix must be symmetric
- If no correlation provided: omit the field (don't set to null)

### Common Observable Name Patterns

**Decay mode abbreviations** (used in `name` field):
| Decay | Abbreviation |
|-------|-------------|
| B+ -> K+ mu+ mu- | Bp2Kpmumu |
| B0 -> K*0 mu+ mu- | B02Kstmumu |
| B0_s -> phi mu+ mu- | Bs0.2.phimumumu |
| B0_s -> phi e+ e- | Bs0.2.phi.e+.e- |
| Lambda_b -> Lambda mu+ mu- | Lb2Lmumu |
| B+ -> pi+ mu+ mu- | Bp2pimumu |

**Observable types**:
- `FL`, `S3`-`S9` - CP-averaged angular observables
- `A3`-`A9` - CP-asymmetric observables
- `P1`-`P8'` - Optimised observables
- `AFB_CP` - CP-averaged forward-backward asymmetry
- `A6p` - Reduced forward-backward asymmetry (A6/(1-FL))

### transition-mode Values

Common values used in the Streamlit dashboard filter:
- `"semi-leptonic decay"` - B meson semi-leptonic decays
- `"W boson production"` - W cross-section measurements
- `"top quark production"` - Top quark cross-sections
- `"Higgs boson production"` - Higgs measurements

## Data Sources (Priority Order)

### 1. HEPData (Preferred - Machine-readable)

HEPData is the primary source for LHCb and other experiment data.

**IMPORTANT**: Direct `curl` to HEPData is blocked by Cloudflare. Use `hepdata-cli`:

```bash
HEPDATA_CLI="/Users/dufewe/.hermes/hermes-agent/venv/bin/hepdata-cli"

# Step 1: List available tables
$HEPDATA_CLI fetch-names -i inspire <inspire_id>

# Step 2: Download metadata as JSON (contains resource URLs)
$HEPDATA_CLI download -f json -i inspire <inspire_id> -d /tmp/hepdata_out

# Step 3: Download specific data resources
# The downloaded JSON contains resource URLs like:
# https://www.hepdata.net/record/resource/4171754?view=true
# curl these URLs to get actual numerical data
curl -sL "https://www.hepdata.net/record/resource/4171754?view=true" > /tmp/data.json
```

**HEPData Resource JSON structure**:
```json
{
    "independent_variables": { "values": [[0.1, 1.1], [1.1, 2.0], ...] },
    "dependent_variables": {
        "FL": {
            "units": 1.0,
            "values": [
                { "val": 0.25, "hi_stat_err": 0.12, "lo_stat_err": -0.12,
                  "hi_syst_err": 0.06, "lo_syst_err": -0.06 },
                ...
            ]
        }
    }
}
```

**Parsing correlation JSON** (sparse dictionary format):
```json
{
    "FL_bin0": {
        "FL_bin0": 1.0,
        "S3_bin0": 0.5,
        "A6p_bin0": -0.1
    },
    "S3_bin0": { ... }
}
```

### 2. CDS Repository (CERN Document Server)

URL: `https://cds.cern.ch/record/<RECORD_ID>/`

- Supplementary materials (YAML, JSON, ROOT files)
- Often contains machine-readable data not in PDF
- Search by paper title or arXiv ID

### 3. LHCb Public Analysis Pages

URL: `https://lbfence.cern.ch/alcm/public/analysis/full-details/<ANALYSIS_ID>/`

- Official LHCb analysis results
- YAML/JSON data files, covariance matrices
- Often linked from paper footnotes

### 4. arXiv PDF (Fallback)

When HEPData/CDS don't have the data, extract from PDF:

```bash
python3 << 'EOF'
import pymupdf
doc = pymupdf.open('/path/to/paper.pdf')
for page in doc:
    text = page.get_text()
    # Search for table content
EOF
```

**WARNING**: `pymupdf` is NOT available in `execute_code` sandbox. Use `terminal` with `python3` heredoc.

pymupdf path: `/Users/dufewe/Library/Python/3.9/lib/python/site-packages`

### 5. ar5iv HTML (Alternative)

```bash
curl -sL "https://ar5iv.labs.arxiv.org/html/<arxiv_id>" | grep -A 50 "Table"
```

### 6. InspireHEP API (for metadata)

```bash
curl -s -H 'Accept: application/json' \
  'https://inspirehep.net/api/literature?q=eprint:<arxiv_id>'
```

Extract: `texkeys[0]` (Inspire ID like `LHCb:2025rfy`), `collaborations`, `titles`, `abstracts`, `preprint_date`

## Import Workflow

### Step 1: Identify Paper

Get the arXiv ID or InspireHEP ID of the paper to import.

### Step 2: Gather Metadata

```bash
# Get InspireHEP metadata
curl -s -H 'Accept: application/json' \
  'https://inspirehep.net/api/literature?q=eprint:2504.06346'

# Get arXiv v1 submission date
curl -sL "http://export.arxiv.org/api/query?id_list=2504.06346"
```

### Step 3: Extract Data

Try HEPData first, then CDS/LHCb public pages, then PDF extraction.

### Step 4: Build JSON

Structure the data according to the format specification above. Use 4-space indentation.

### Step 5: Write File

1. Create directory: `Experimental/{group}/{year}/{month}/`
2. Write JSON file: `Experimental/{group}/{year}/{month}/{file_id}.json`
3. Update index: `Experimental/{group}/{year}/{group}@{year}.json`

### Step 6: Update Index File

```python
import json

index_path = f'Experimental/{group}/{year}/{group}@{year}.json'
try:
    with open(index_path, 'r') as f:
        index = json.load(f)
except FileNotFoundError:
    index = {}

month_key = f"{int(month):02d}"
file_id = "LHCb:2025xxx"  # e.g., from InspireHEP texkeys

if month_key not in index:
    index[month_key] = []
if file_id not in index[month_key]:
    index[month_key].append(file_id)

# Sort keys
index = dict(sorted(index.items()))

with open(index_path, 'w') as f:
    json.dump(index, f, indent=4)
```

### Step 7: Verify

```bash
# Validate JSON
python3 -c "import json; json.load(open('path/to/file.json'))"

# Check Streamlit loads it
cd /Users/dufewe/Backup/Selia/projects/2HDM-SMEFT/Fitting/Streamlit/flav-data
python3 -c "
from defs import get_json
data = get_json('Experimental/LHCb/2025/04/LHCb:2025xxx.json')
print('Keys:', list(data.keys()))
print('Data entries:', len(data.get('data', [])))
"
```

## Common Paper Patterns

### Pattern 1: Angular Analysis (B->K*ll, Bs->phill)

- Multiple q2 bins, each with 4-8 observables
- Correlation matrices per q2 bin
- Example: LHCb:2025rfy (Bs->phi ee), LHCb:2015svh (B0->K* mumu)

### Pattern 2: Branching Fractions

- q2 bins with absolute and/or relative dBr/dq2
- Usually no correlation matrix
- Example: LHCb:2021zwz

### Pattern 3: Cross-section Measurements

- pT or eta bins instead of q2
- Multiple error types (stat, syst, lumi)
- Use `pTmin`/`pTmax` or `eta_min`/`eta_max` fields
- Example: LHCb:2025msn (W->munu)

### Pattern 4: Asymmetries

- 1-2 observables per q2 bin (FB, FH, etc.)
- Usually no correlation
- Example: LHCb:2014auh

## Pitfalls

1. **hepdata-cli path**: Always use `/Users/dufewe/.hermes/hermes-agent/venv/bin/hepdata-cli`
2. **Cloudflare**: Direct `curl` to hepdata.net is blocked -- always use hepdata-cli
3. **pymupdf**: Not in execute_code sandbox -- use terminal with python3 heredoc
4. **String values**: All numeric values in JSON must be strings ("0.25" not 0.25)
5. **LaTeX escaping**: Double backslashes in JSON strings (`\\\\to` not `\\to`)
6. **Index sync**: Always update the index file after adding a new JSON file
7. **Month zero-padding**: Index keys must be "01"-"12", not "1"-"12"
8. **Duplicate IDs**: Check if file_id already exists in index before appending
9. **f-string backslashes**: Python f-strings cannot contain backslashes in expressions -- use string concatenation for LaTeX
10. **transition-mode**: Required for Streamlit filtering -- check existing files for common values
11. **time field**: Use v1 submission date, not latest revision date
12. **Correlation symmetry**: If only lower-triangular provided, symmetrize the matrix
13. **HEPData units**: Check the `units` field -- values may need multiplication (e.g., `units: 0.1` means multiply by 0.1)
14. **Missing HEPData values**: Sometimes `val` is `"-"` instead of a number -- check `isinstance(val, (int, float))` before processing

## Validation Checklist

- [ ] JSON file parses without errors
- [ ] All required top-level fields present (inspire-hep, author, collaboration, title, arxiv, time, abstract, pdf, data)
- [ ] All obs@N entries have: name, latex, value, type@1_err, type@1_err_up, type@1_err_down
- [ ] Numeric values stored as strings
- [ ] LaTeX has proper double-escaping
- [ ] Index file updated with new file_id
- [ ] Index file keys are zero-padded months
- [ ] transition-mode field present and matches existing conventions
- [ ] Correlation matrices (if present) are symmetric with diagonal = 1.0
- [ ] File placed in correct `{group}/{year}/{month}/` directory

## Related Skills

- `lhcb-json-data-extraction` - Extract data from arXiv PDFs (detailed PDF parsing)
- `lhcb-json-format-standardization` - Standardize JSON format and field ordering
- `lhcb-correlation-matrix-extraction` - Extract correlation matrices from HEPData
- `lhcb-data-validation` - Validate JSON data against source papers
