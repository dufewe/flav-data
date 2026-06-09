# Data Source Priority and Scope

This document defines which data sources to use, in what order, and what data is eligible for import into the flav-data database.

## Scope

### Supported for Import
- **Experimental measurements** from recognized collaborations: LHCb, CMS, ATLAS, Belle, BaBar, BESIII, CDF, D0, HFLAV, LEP, NA62, KOTO, etc.
- **Theoretical calculations** from established groups: HPQCD, RBC/UKQCD, FNAL/MILC, JLQCD, etc.
- **arXiv preprints** and **peer-reviewed journal papers**

### Not Supported for Import
- **Phenomenological fits** — results from fitting theoretical parameters (Wilson coefficients, form factors, etc.) to experimental data. These are interpretations, not primary measurements.
- **Conference papers** — results presented only at conferences without a formal arXiv preprint or journal publication.
- **Report papers** — preliminary notes, conference contributions, or internal reports without peer review.
- **Informal non-peer-reviewed results** — blog posts, personal web pages, unpublished notes.

**Handling unsupported requests**: If a user asks to import unsupported data, respond with "This data is not supported for import." Then, if applicable, search arXiv and InspireHEP for the corresponding formal paper and offer to import from that instead.

**Multi-paper merging**: When multiple arXiv papers describe the same measurement (e.g., a conference note superseded by a full paper, or a short letter followed by a detailed analysis), merge all data into a single JSON file. Retain metadata (Inspire IDs, arXiv IDs, DOIs) from all contributing papers.

## Data Source Priority

Try sources in the following order. Move to the next source only if the current one does not yield usable data.

### 1. HEPData (Preferred)

**Why**: Machine-readable, structured data with proper error breakdowns and correlation matrices.

**When to use**: Experimental papers that have uploaded their data to HEPData. Most LHC and many Belle/BaBar papers have HEPData entries.

**How to access**:
```bash
# hepdata-cli is installed in the Hermes venv:
#   ~/.hermes/hermes-agent/venv/bin/hepdata-cli
HEPDATA_CLI="hepdata-cli"

# List available tables for a paper
$HEPDATA_CLI fetch-names -i inspire <inspire_recid>

# Download metadata (contains table URLs and paper info)
$HEPDATA_CLI download -f json -i inspire <inspire_recid> -d <output_dir>
```

**Downloading specific tables**:
```bash
# URL-encode the table name (spaces → %20)
curl -sL -A "Mozilla/5.0" \
  "https://www.hepdata.net/download/table/ins<recid>/Table%201/yaml"
```

**Limitations**:
- Theory papers almost never have HEPData entries.
- Many BSM search papers (mass limits, exclusion contours) do not upload tabulated data.
- Fall through to PDF extraction quickly for these cases.

See `references/hepdata-cli.md` for detailed YAML parsing guidance.

### 2. CDS (CERN Document Server)

**Why**: Contains supplementary materials, additional data tables, and CMS Physics Analysis Summaries (PAS).

**When to use**: CERN-based experiments (ATLAS, CMS, LHCb) that have supplementary materials on CDS but no HEPData entry.

**How to search**:
```bash
# Search by arXiv ID
curl -sL "https://cds.cern.ch/search?f=reportnumber&p1=<arxiv_id>"

# Search by paper title
curl -sL "https://cds.cern.ch/search?f=title&p1=<paper_title>"
```

**Note**: Some CDS URLs may redirect to authentication pages. Check the downloaded file size — a real PDF will be >100KB; an HTML login page will be <20KB.

### 3. LHCb Public Pages

**Why**: LHCb publishes official analysis result pages with structured data including correlation matrices.

**When to use**: LHCb analyses that have public pages but no HEPData entry.

**URL pattern**: `https://lbfence.cern.ch/alcm/public/analysis/full-details/<ANALYSIS_ID>/`

### 4. arXiv PDF (Last Resort)

**Why**: Every paper has an arXiv PDF. This is the fallback when no structured data source is available.

**When to use**: All other sources have been exhausted.

**How to extract**:
```bash
# Download the PDF
curl -sL -O "https://arxiv.org/pdf/<arxiv_id>.pdf"

# Extract text with pymupdf
python3 -c "
import pymupdf
doc = pymupdf.open('paper.pdf')
for page in doc:
    print(page.get_text())
"
```

**Important**: pymupdf must be available in the Python environment. Run via terminal, not the execute_code sandbox.

**Limitations**:
- Table extraction from PDF text is error-prone. Column alignment may be lost.
- Cross-check extracted values against the paper's text and summary tables.
- For scanned PDFs (rare in HEP), use `marker-pdf` instead of pymupdf.

### 5. ar5iv HTML (Alternative to PDF)

**Why**: HTML format preserves table structure better than PDF text extraction.

**When to use**: When PDF extraction yields garbled or incomplete table data.

**URL**: `https://ar5iv.labs.arxiv.org/html/<arxiv_id>`

**How to extract tables**:
```bash
curl -sL "https://ar5iv.labs.arxiv.org/html/<arxiv_id>" | grep -A 50 "Table"
```

**Limitations**: The HTML version may not be the latest paper version.

### 6. InspireHEP API (Metadata Only)

**Why**: Provides paper metadata (title, authors, collaboration, TexKey, DOI) but NOT experimental data values.

**When to use**: Always — for metadata extraction, not for data values. Use this in parallel with Steps 1–5 (which extract data values), not as a sequential fallback.

**How to use**: Query by arXiv ID, recid, TexKey, or DOI. See `references/inspirehep-api.md` for query details and Python extraction code.

**Note**: InspireHEP metadata is retrieved independently of the data source priority chain. You will always need it regardless of which data source (HEPData, CDS, PDF, etc.) provides the actual measurement values.

### 7. vision_analyze (Table Screenshots)

**Why**: Can read values directly from table images.

**When to use**: The user provides screenshots of tables from a paper.

## Scenario Guide

| Scenario | Best Source | Notes |
|----------|------------|-------|
| LHCb angular analysis | HEPData | Usually has full angular observables + correlation matrices |
| LHCb branching fraction | HEPData or CDS | Check both |
| Belle/BaBar data | HEPData or PDF | Many older Belle papers lack HEPData |
| BESIII data | PDF (pymupdf) or HEPData | Some BESIII papers have HEPData; many don't |
| CDF/D0 data | InspireHEP files or PDF | Older Tevatron papers often lack HEPData |
| PDG world averages | PDG website or HEPData | PDG review PDFs at pdg.lbl.gov |
| HFLAV averages | HFLAV website | Dedicated combination results |
| Theory calculations | PDF (pymupdf) | Theory papers rarely have HEPData |
| Table screenshots | vision_analyze | User-provided images |
| CMS PAS | CDS | CMS preliminary analyses on CDS |

## Output Formatting Rules

When writing the extracted data to a JSON file, apply these 4 formatting
rules (canonical reference: `Test/improve.md`):

1. **Matrix layout**: each `*_correlation` / `*_covariance` row is on a
   single line in the JSON file; do NOT put each matrix element on its
   own line.
2. **Abstract = single line**: convert multi-line `\\begin{align*} ...
   \\end{align*}` blocks in abstracts to single-line LaTeX. Line breaks
   become `, ` separators, with `and` before the last entry.
3. **Author format**: use InspireHEP BibTeX format — first author
   `Surname, Initials.` (e.g. `"Aaij, R. and others"`), NOT full first
   name (`"Aaij, Roel"`).
4. **No Unicode**: replace all Unicode chars in extracted data with
   LaTeX equivalents (`μ` → `\mu`, `Δ` → `\Delta`, `±` → `\pm`,
   `→` → `\to`, smart quotes → `` ` ``/`'`/`` `` ``/`''`, etc.).

A reference migration script for these rules is at
`/Users/dufewe/Backup/Selia/projects/2HDM-SMEFT/Fitting/Streamlit/flav-data/.hermes/migrate-rules.py`.
