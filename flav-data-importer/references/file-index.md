# File Indexing and Directory Structure

This document specifies the directory layout, file naming conventions, and annual index management for the flav-data database.

## Directory Layout

Experimental folders use the `Lab-Collaboration` format (实验室-实验组). Data file and index filenames inside keep only the collaboration name.

```text
flav-data/
├── Experimental/                          # Experimental measurement data
│   ├── CERN-LHCb/                         # Lab-Collaboration folder
│   │   ├── LHCb.py                        # Streamlit dashboard page
│   │   ├── 2015/
│   │   │   ├── LHCb@2015.json             # Annual index
│   │   │   └── 12/
│   │   │       └── LHCb:2015svh.json     # Data file (Collaboration:TexKey)
│   ├── CERN-ATLAS/, CERN-CMS/, CERN-DELPHI/, CERN-OPAL/,
│   ├── CERN-LEP/                          # Combined LEP (ALEPH+DELPHI+L3+OPAL)
│   ├── CERN-NA62/, CERN-CHARM-II/
│   ├── KEK-Belle/, KEK-KOTO/
│   ├── SLAC-BaBar/, SLAC-SLD/
│   ├── Fermilab-CDF/, Fermilab-D0/, Fermilab-Tevatron/, Fermilab-Muong-2/
│   ├── IHEP-BESIII/, IHEP-ISTRA+/
│   ├── INFN-KLOE-2/
│   ├── BNL-E949/, Cornell-CLEO/, TRIUMF-PiENu/
│   ├── PSI-SINDRUM-II/, PSI-nTRV/
│   ├── LANL-UCNA/, NIST-aCORN/
│   └── HFLAV/, PDG/                                # No-lab aggregation
└── Theoretical/
    └── ...                                          # Theory group folders (HPQCD, UKQCD, etc.)
```text

## Naming Rules

### Folder Names

Experimental directories use the `Lab-Collaboration` format (实验室-实验组).
When there is no parent lab (aggregation groups like HFLAV/PDG, or
standalone individual measurements), the collaboration/group name is
used directly as the folder. Data files and annual index files inside
the folder retain only the collaboration name (not the lab prefix).

| Folder | Lab | Collaboration | Notes |
|--------|-----|--------------|-------|
| `CERN-LHCb` | CERN | LHCb | |
| `CERN-ATLAS` | CERN | ATLAS | |
| `CERN-CMS` | CERN | CMS | |
| `CERN-DELPHI` | CERN | DELPHI | LEP |
| `CERN-OPAL` | CERN | OPAL | LEP |
| `CERN-LEP` | CERN | LEP | Combined LEP experiments (ALEPH+DELPHI+L3+OPAL) |
| `CERN-NA62` | CERN | NA62 | Kaon rare decays |
| `CERN-CHARM-II` | CERN | CHARM-II | Neutrino experiment |
| `KEK-Belle` | KEK | Belle | |
| `KEK-KOTO` | KEK | KOTO | J-PARC |
| `SLAC-BaBar` | SLAC | BaBar | |
| `SLAC-SLD` | SLAC | SLD | |
| `Fermilab-CDF` | Fermilab | CDF | Tevatron |
| `Fermilab-D0` | Fermilab | D0 | Tevatron |
| `Fermilab-Tevatron` | Fermilab | Tevatron | Combined CDF+D0 |
| `Fermilab-Muong-2` | Fermilab | Muong-2 | |
| `IHEP-BESIII` | IHEP | BESIII | Beijing Spectrometer |
| `IHEP-ISTRA+` | IHEP | ISTRA+ | |
| `INFN-KLOE-2` | INFN | KLOE-2 | LNF Frascati DAΦNE |
| `BNL-E949` | BNL | E949 | K+ rare decays |
| `Cornell-CLEO` | Cornell | CLEO | CESR |
| `TRIUMF-PiENu` | TRIUMF | PiENu | |
| `PSI-SINDRUM-II` | PSI | SINDRUM-II | Mu-e conversion |
| `PSI-nTRV` | PSI | nTRV | Neutron trimer |
| `LANL-UCNA` | LANL | UCNA | |
| `NIST-aCORN` | NIST | aCORN | |
| `HFLAV` | — | HFLAV | No parent lab; non-standard schema |
| `PDG` | — | PDG | No parent lab; non-standard schema |

Theoretical folders use the group name directly: `HPQCD`, `UKQCD`, `Akeroyd`, `Altmannshofer`, `Greljo`, etc. (only those registered in `defs.THEOGROUP` are linked from the Streamlit sidebar).

**Special cases**:

- **HFLAV** and **PDG** use a non-standard flav-data schema (one
  snapshot JSON per year whose keys are subgroup names containing
  nested observables). See `../references/json-meta.md` for details.
  When importing data into these groups, build a single year-level
  snapshot file rather than per-paper JSONs.

### Data Files

Format: `{Collaboration}:{TexKey}.json`

The filename uses only the collaboration name (not the full `Lab-Collaboration` folder name). For example, under `Experimental/CERN-LHCb/`, the data file is `LHCb:2015svh.json`. TexKey comes from InspireHEP.

| Example | Description |
|---------|-------------|
| `LHCb:2015svh.json` | LHCb paper, TexKey LHCb:2015svh |

**TexKey selection**: Papers often have multiple TexKeys (collaboration-level + author-level). Always use the collaboration-level TexKey for the filename. For example, if a paper has TexKeys `["LHCb:2015svh", "Aaij:2015oid"]`, use `LHCb:2015svh.json`.

### Annual Index Files

Format: `{Collaboration}@{year}.json` — uses the collaboration name only (e.g., `LHCb@2015.json`).

Location: within the `Lab-Collaboration` folder's year subdirectory (e.g., `Experimental/CERN-LHCb/2015/LHCb@2015.json`).

```json
{
    "12": ["LHCb:2015svh"]
}
```text

- **Keys**: Zero-padded month strings ("01" through "12").
- **Values**: Arrays of file_ids (without the `.json` extension).
- **Month ordering**: Keys in ascending order.
- **File ordering**: Within each month, file_ids sorted by arXiv v1 submission date.
- **TexKey freshness**: Always use the latest TexKey version from InspireHEP when updating indices.

## Index Operations

### Check if a Paper Exists

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
                    print(f"Found: {year}/{month}/{target}.json")
                    break
```text

### Verify Index Integrity

Compare indexed entries against actual files on disk to detect discrepancies:

```python
import json, os

base = 'Experimental/CERN-LHCb/2015'
index = json.load(open(f'{base}/LHCb@2015.json'))

# Index file_ids
indexed = set()
for month_files in index.values():
    indexed.update(month_files)

# Disk file_ids
on_disk = set()
for month_dir in sorted(os.listdir(base)):
    if month_dir.isdigit() and len(month_dir) == 2:
        for fname in os.listdir(f'{base}/{month_dir}'):
            if fname.endswith('.json') and '@' not in fname:
                on_disk.add(fname[:-5])  # Strip .json

# Report discrepancies
missing_in_index = on_disk - indexed
missing_on_disk = indexed - on_disk

if missing_in_index:
    print("Files on disk but missing from index:", sorted(missing_in_index))
if missing_on_disk:
    print("Files in index but missing from disk:", sorted(missing_on_disk))
if not missing_in_index and not missing_on_disk:
    print("Index is consistent with disk.")
```text

### Update an Index

When adding a new file:
1. Load the existing index (or create a new one if it doesn't exist).
2. Determine the month from the arXiv v1 submission date (zero-padded).
3. Add the file_id to the appropriate month's array.
4. Sort the array by arXiv v1 date if multiple entries exist.
5. Write the updated index back.

When removing a file:
1. Load the index.
2. Remove the file_id from the appropriate month's array.
3. If the month's array becomes empty, remove the month key.
4. Write the updated index back.

### Multi-Collaboration Papers

When a paper is a joint effort between multiple collaborations (e.g., ATLAS+CMS combination):
- Use the primary collaboration (first in the TexKey) for the directory.
- The TexKey reflects all collaborations.
- Fill corresponding data entries for all involved groups in their respective database directories.

## Notes

1. **Always update the index** after adding or deleting a JSON file.
2. **Month assignment** is based on the arXiv v1 submission date.
3. **File size limit**: Keep JSON files under 10MB; split large correlation matrices.
4. **Validate** with `python3 scripts/json-valid.py` after writing.
5. **Backup before modifying** — especially when updating indices or replacing existing files.
