# File Indexing and Directory Structure

This document specifies the directory layout, file naming conventions, and annual index management for the flav-data database.

## Directory Layout

```
flav-data/
├── Experimental/                          # Experimental measurement data
│   ├── LHCb/                              # Collaboration name
│   │   ├── LHCb.py                        # LHCb-specific data loading script
│   │   ├── 2015/
│   │   │   ├── LHCb@2015.json             # Annual index file
│   │   │   ├── 06/                        # Month subdirectory (zero-padded)
│   │   │   │   └── LHCb:2015svh.json     # Data file
│   │   │   └── 12/
│   │   │       └── LHCb:2015abc.json
│   │   └── 2025/
│   │       ├── LHCb@2025.json
│   │       └── 03/
│   │           └── LHCb:2025xyz.json
│   ├── ATLAS/
│   ├── CMS/
│   ├── BaBar/
│   ├── Belle/
│   ├── BESIII/
│   ├── CDF/
│   ├── D0/
│   ├── HFLAV/
│   ├── LEP/
│   └── PDG/
└── Theoretical/                           # Theoretical calculation data
    └── HPQCD/
        └── 2023/
            ├── HPQCD@2023.json
            └── 06/
                └── HPQCD:2023abc.json
```

## Naming Rules

### Folder Names

Experimental directories use the collaboration name directly:

| Folder | Description |
|--------|-------------|
| `LHCb` | LHCb collaboration |
| `ATLAS` | ATLAS collaboration |
| `CMS` | CMS collaboration |
| `BaBar` | BaBar collaboration |
| `Belle` | Belle collaboration |
| `BESIII` | BESIII collaboration |
| `CDF` | CDF collaboration |
| `D0` | D0 collaboration |
| `HFLAV` | Heavy Flavor Averaging Group |
| `PDG` | Particle Data Group |
| `LEP` | LEP experiments combination |

Theoretical folders use the group name: `HPQCD`, `RBC-UKQCD`, `FNAL-MILC`, `JLQCD`, etc.

### Data Files

Format: `{group}:{TexKey}.json`

The filename uses the collaboration name and TexKey from InspireHEP: `{group}:{TexKey}.json`.

| Example | Description |
|---------|-------------|
| `LHCb:2015svh.json` | LHCb paper, texkey LHCb:2015svh |
| `CMS:2023abc.json` | CMS paper, texkey CMS:2023abc |
| `Belle:2019dgy.json` | Belle paper, texkey Belle:2019dgy |

**TexKey selection**: Papers often have multiple texkeys (collaboration-level + author-level). Always use the collaboration-level texkey for the filename. For example, if a paper has texkeys `["LHCb:2015svh", "Aaij:2015oid"]`, use `LHCb:2015svh.json`.

### Annual Index Files

Format: `{group}@{year}.json`

Location: `Experimental/{group}/{year}/` or `Theoretical/{group}/{year}/`

```json
{
    "03": ["LHCb:2025xyz"],
    "06": ["LHCb:2015svh"],
    "12": ["LHCb:2015abc", "LHCb:2015def"]
}
```

- **Keys**: Zero-padded month strings ("01" through "12").
- **Values**: Arrays of file_ids (without the `.json` extension).
- **Month ordering**: Keys in ascending order.
- **File ordering**: Within each month, file_ids sorted by arXiv v1 submission date.
- **Texkey freshness**: Always use the latest TexKey version from InspireHEP when updating indices.

## Index Operations

### Check if a Paper Exists

```python
import json, os

base = 'Experimental/LHCb'
target = 'LHCb:2025xyz'

for year in sorted(os.listdir(base)):
    if year.isdigit():
        idx_path = os.path.join(base, year, f'LHCb@{year}.json')
        if os.path.exists(idx_path):
            index = json.load(open(idx_path))
            for month, files in index.items():
                if target in files:
                    print(f"Found: {year}/{month}/{target}.json")
                    break
```

### Verify Index Integrity

Compare indexed entries against actual files on disk to detect discrepancies:

```python
import json, os

base = 'Experimental/LHCb/2015'
index = json.load(open(f'{base}/LHCb@2015.json'))

# Collect all file_ids from the index
indexed = set()
for month_files in index.values():
    indexed.update(month_files)

# Collect all file_ids from disk
on_disk = set()
for month_dir in sorted(os.listdir(base)):
    if month_dir.isdigit() and len(month_dir) == 2:
        for fname in os.listdir(f'{base}/{month_dir}'):
            if fname.endswith('.json') and '@' not in fname:
                on_disk.add(fname[:-5])  # Remove .json extension

# Report discrepancies
missing_in_index = on_disk - indexed   # Files on disk but not in index
missing_on_disk = indexed - on_disk    # Files in index but not on disk

if missing_in_index:
    print("Files on disk but missing from index:", sorted(missing_in_index))
if missing_on_disk:
    print("Files in index but missing from disk:", sorted(missing_on_disk))
if not missing_in_index and not missing_on_disk:
    print("Index is consistent with disk.")
```

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
- Use the primary collaboration (first in the texkey) for the directory.
- The texkey reflects all collaborations.
- Fill corresponding data entries for all involved groups in their respective database directories.

## Notes

1. **Always update the index** after adding or deleting a JSON file.
2. **Month assignment** is based on the arXiv v1 submission date.
3. **File size limit**: Keep individual JSON files under 10MB. If correlation matrix data is very large, consider splitting into separate entries.
4. **Always validate** with `python3 scripts/json-valid.py` after writing a new file.
5. **Backup before modifying** — especially when updating indices or replacing existing files.
