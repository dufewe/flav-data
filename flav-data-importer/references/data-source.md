# Data Source Priority and Scope

This document defines which data sources to use, in what order, and what data is eligible for import into the flav-data database.

## Scope

### Supported for Import
- **Experimental measurements** from recognized collaborations: LHCb, CMS, ATLAS, Belle, BaBar, BESIII, CDF, D0, HFLAV, LEP, NA62, KOTO, etc.
- **Theoretical calculations** (lattice QCD, perturbative QCD, first-principles or fixed-order results) from established groups: HPQCD, RBC/UKQCD, FNAL/MILC, JLQCD, etc. Form-factor parametrization fits belong here: they produce the `aN_FF` coefficients plus a group-level `scheme`, and are imported even when the fit combines lattice, LCSR, and experimental input (`dataset: "LQCD+LCSR+EXPE"`).
- **arXiv preprints** and **peer-reviewed journal papers**

### Not Supported for Import
- **Global analyses** — interpretations of existing measurements rather than primary data: Wilson-coefficient fits, CKM/parameter determinations, mass or coupling bounds, and world averages.
- **Conference papers** — results without a formal preprint or publication.
- **Report papers** — conference contributions or internal reports without peer review.
- **Informal non-peer-reviewed results** — blog posts, personal web pages, unpublished notes.

**Handling unsupported requests**: If a user asks to import unsupported data, respond with "This data is not supported for import." Then, if applicable, search arXiv and InspireHEP for the corresponding formal paper and offer to import from that instead.

**Multi-paper merging**: When multiple arXiv papers describe the same measurement (e.g., a conference note superseded by a full paper, or a short letter followed by a detailed analysis), merge all data into a single JSON file. The schema stores a single `inspire-hep`/`arxiv` citation set, so use the **primary** (normally the peer-reviewed) paper for those fields and mention superseded identifiers in the abstract only when that context matters — do not add extra citation fields.

## Data Source Priority

Try sources in the following order. Move to the next source only if the current one does not yield usable data.

### 1. HEPData (Preferred)

**Why**: Machine-readable, structured data with proper error breakdowns and correlation matrices.

**When to use**: Experimental papers that have uploaded their data to HEPData. Most LHC and many Belle/BaBar papers have HEPData entries.

**How to access**:
```bash
# hepdata-cli install + lookup: see ./hepdata-cli.md.
# Briefly: install with `pip install hepdata-cli`; the importer resolves
# the binary at runtime from $PATH / venv bin / ~/.local/bin.
HEPDATA_CLI="hepdata-cli"

# List available tables for a paper
$HEPDATA_CLI fetch-names -i inspire <inspire_recid>

# Download metadata (contains table URLs and paper info)
$HEPDATA_CLI download -f json -i inspire <inspire_recid> -d <output_dir>
```

**Downloading specific tables**:
```bash
# HEPData blocks plain HTTP clients (Cloudflare), so always go through
# hepdata-cli rather than curl/wget.
$HEPDATA_CLI download -f yaml -i inspire <inspire_recid> \
  -t "Table 1" -d <output_dir>
```
`scripts/hepdata-ext.py` wraps this in `download_table_yaml()` and then
parses the YAML with `parse_yaml_observables()` /
`parse_yaml_correlation()`; `detect_table_type()` decides which parser
to use from the table structure.

**Limitations**:
- Theory papers almost never have HEPData entries.
- Many BSM search papers (mass limits, exclusion contours) do not upload tabulated data.
- For these cases move on to the arXiv ancillary files (§4), not straight to the PDF.

See `hepdata-cli.md` for detailed YAML parsing guidance.

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

### 4. arXiv Ancillary Files (Primary inside the arXiv route)

**Why**: Many theory papers (and some experimental ones) ship machine-readable
tables with the arXiv submission — `.dat`, `.txt`, `.csv`, `.json`, `.yaml`
files listed under "Ancillary files" on the abstract page. They contain exactly
the numbers behind the paper's tables and need no OCR.

**When to use**: Before extracting anything from the paper itself. For every
arXiv paper, inspect the abstract page's "Ancillary files" section and the
e-print package, even when HEPData exists (ancillary files may hold tables the
HEPData entry omits).

**Rule** — ancillary data first, paper data as validation:

1. If a usable ancillary file exists, it is the **primary source**. Read the
   numbers from it.
2. Then **validate them against the paper's own tables**: the same quantity
   must appear with the same central value and uncertainty. If they disagree,
   the file may belong to an older version or a different fit scenario — do
   not import until the discrepancy is explained. When it cannot be resolved,
   use the paper's published table for the JSON values and record the conflict.
3. If no machine-readable ancillary file exists, use the e-print LaTeX source
   (better than PDF text) as the data source and still cross-check every value
   against the paper's table.

**How to access**:
```bash
# e-print package: usually a .tar.gz, sometimes a single gzipped file
curl -sL -A 'Mozilla/5.0' -o src.tar.gz "https://arxiv.org/e-print/<arxiv_id>"
tar tzf src.tar.gz

# or via the helper (downloads, unpacks, lists candidate data files)
python3 flav-data-importer/scripts/arxiv-ext.py <arxiv_id> --source -o <output_dir>
```
Ancillary data is usually small text/CSV; the package also carries the LaTeX
source, which preserves table structure that PDF extraction loses.

### 5. arXiv PDF / LaTeX Source (Last Resort)

**Why**: Every paper has an arXiv PDF. This is the fallback when no HEPData
entry and no ancillary data file are available.

**When to use**: All structured sources have been exhausted.

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

Prefer the LaTeX source from the e-print package over the PDF when a table is
needed: `\begin{tabular}` blocks keep row/column alignment that PDF text loses.

**Important**: pymupdf must be installed in the Python environment (`pip install pymupdf`).

**Limitations**:
- Table extraction from PDF text is error-prone. Column alignment may be lost.
- Cross-check extracted values against the paper's text and summary tables.
- For scanned PDFs (rare in HEP), use `marker-pdf` instead of pymupdf.

### 6. ar5iv HTML (Alternative to PDF)

**Why**: HTML format preserves table structure better than PDF text extraction.

**When to use**: When PDF extraction yields garbled or incomplete table data.

**URL**: `https://ar5iv.labs.arxiv.org/html/<arxiv_id>`

**How to extract tables**:
```bash
curl -sL "https://ar5iv.labs.arxiv.org/html/<arxiv_id>" | grep -A 50 "Table"
```

**Limitations**: The HTML version may not be the latest paper version.

### 7. Table Screenshots

**Why**: Values can be read directly from a table image when no
machine-readable or text source survives.

**When to use**: The user provides screenshots of tables from a paper.
Read the image file with the agent's image tool and transcribe the numbers,
then cross-check them against the paper text.

---

### Metadata Source (parallel, not sequential)

**InspireHEP API** provides paper metadata (title, authors, collaboration, TexKey, DOI) but NOT experimental data. Query it in parallel with steps 1–7 for every paper:

- **Why**: metadata (not data values) is always needed.
- **How**: query by arXiv ID, recid, TexKey, or DOI (see `inspirehep-api.md`).

## Scenario Guide

| Scenario | Best Source | Notes |
|----------|------------|-------|
| LHCb angular analysis | HEPData | Usually has full angular observables + correlation matrices |
| LHCb branching fraction | HEPData or CDS | Check both |
| Belle/BaBar data | HEPData or PDF | Many older Belle papers lack HEPData |
| BESIII data | PDF (pymupdf) or HEPData | Some BESIII papers have HEPData; many don't |
| CDF/D0 data | HEPData or PDF | Older Tevatron papers often lack HEPData |
| PDG world averages | PDG website or HEPData | PDG review PDFs at pdg.lbl.gov |
| HFLAV averages | HFLAV website | Dedicated combination results |
| Theory calculations | arXiv ancillary files or LaTeX source | Theory papers rarely have HEPData; check the e-print package first |
| Any arXiv paper before PDF | arXiv ancillary files | Prefer machine-readable files; validate against the paper tables |
| Table screenshots | Image reading | User-provided images |
| CMS PAS | CDS | CMS preliminary analyses on CDS |

## Output Formatting Rules

See SKILL.md "Core Conventions" — the 9 hard rules there (matrix layout,
single-line abstract, InspireHEP author format, LaTeX-only Unicode,
canonical transition order, one group per property set, the `data`
array of channel-keyed groups, conditional
`collaboration`, and `aN_FF` form-factor naming)
apply to all JSON output.
