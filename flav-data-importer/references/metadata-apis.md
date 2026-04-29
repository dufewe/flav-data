# Metadata Extraction APIs

## InspireHEP API

### Search by arXiv ID
```bash
curl -s -H 'Accept: application/json' \
  'https://inspirehep.net/api/literature?q=eprint:2504.06346'
```

### Key fields in response
```python
metadata = response['hits']['hits'][0]['metadata']

# Inspire ID (e.g., "LHCb:2025rfy")
texkey = metadata.get('texkeys', [''])[0]

# Collaboration
collaboration = metadata.get('collaborations', [{}])[0].get('value', '')

# Title
title = metadata.get('titles', [{}])[0].get('title', '')

# Abstract
abstract = metadata.get('abstracts', [{}])[0].get('value', '')

# Authors (first author + "and others")
authors = metadata.get('authors', [])
if len(authors) > 1:
    author_str = f"{authors[0].get('full_name', '')} and others"
else:
    author_str = authors[0].get('full_name', '') if authors else ''

# Publication date (for time field)
# Use preprint_date if available
preprint_date = metadata.get('preprint_date', '')
# Format: "2025-04-08" -> "2025.04.08"

# arXiv eprint
eprints = metadata.get('arxiv_eprints', [{}])
arxiv_id = eprints[0].get('id', '') if eprints else ''

# InspireHEP literature ID
recid = metadata.get('control_number', '')
inspire_url = f"https://inspirehep.net/literature/{recid}"
```

### Search by collaboration and year
```bash
curl -s -H 'Accept: application/json' \
  'https://inspirehep.net/api/literature?q=collaboration:LHCb%20and%20earliest_date:2025'
```

## arXiv API (for v1 submission date)

### Query by arXiv ID
```bash
curl -sL "http://export.arxiv.org/api/query?id_list=2504.06346"
```

### Parse response
```python
import xml.etree.ElementTree as ET

root = ET.fromstring(xml_data)
ns = {'atom': 'http://www.w3.org/2005/Atom'}

# v1 submission date
published = root.find('atom:entry/atom:published', ns).text
# Example: "2025-04-08T18:29:53Z" -> "2025.04.08"

# Title
title_elem = root.find('atom:entry/atom:title', ns).text

# Authors
author_elems = root.findall('atom:entry/atom:author', ns)
authors = [a.find('atom:name', ns).text for a in author_elems]

# Abstract
summary = root.find('atom:entry/atom:summary', ns).text
```

## HEPData

### Using hepdata-cli (recommended)
```bash
HEPDATA_CLI="/Users/dufewe/.hermes/hermes-agent/venv/bin/hepdata-cli"

# List tables
$HEPDATA_CLI fetch-names -i inspire <inspire_id>

# Download metadata
$HEPDATA_CLI download -f json -i inspire <inspire_id> -d /tmp/out
```

### HEPData Record IDs for Common LHCb Papers
| arXiv | Inspire ID | HEPData Record | Notes |
|-------|-----------|----------------|-------|
| 1512.04442 | 1409497 | ins1409497 | B0->K*mumu angular (Tables 40-83) |
| 1506.08777 | 1384005 | ins1384005 | Bs0->phimumu branching |
| 1509.00414 | 1391325 | ins1391325 | B+->pi+mumu |
| 1403.8044 | 1284619 | ins1284619 | B+->K(*)+mumu branching |
| 1409.6733 | 1317676 | ins1317676 | B->Kmumu AFB/FH |
| 2105.14007 | 1862843 | ins1862843 | Bs0->phimumu angular |
| 1512.00441 | 1408772 | ins1408772 | B0->K*ee low q2 |
| 1808.00264 | 1692209 | ins1692209 | Lb0->Lmumu angular moments |
| 2012.07236 | 1843346 | ins1843346 | B0->K*ee angular |

## CDS

### Search by arXiv ID
```bash
curl -s "https://cds.cern.ch/search?f1=reportnumber&p1=2504.06346&action_search=Search&c=LHCb&sc=1&sf=reportnumber&so=a&rg=10&of=hb"
```

### Direct record access
```bash
curl -s "https://cds.cern.ch/api/record/<RECORD_ID>"
```

## Building the inspire-hep Markdown Link

```python
# Format: [InspireID](https://inspirehep.net/literature/<recid>)
inspire_hep_link = f"[{texkey}](https://inspirehep.net/literature/{recid})"
# Example: "[LHCb:2025rfy](https://inspirehep.net/literature/2909896)"

# arXiv link
arxiv_link = f"[{arxiv_id}](https://arxiv.org/pdf/{arxiv_id})"
# Example: "[hep-ex/2504.06346v2](https://arxiv.org/pdf/2504.06346)"

# PDF link
pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
```
