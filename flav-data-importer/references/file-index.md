# File Indexing and Directory Structure

This document specifies the directory layout, file naming conventions, and annual index management for the flav-data database.

## Directory Layout

Experimental measurements live in `expe-data/`, theoretical calculations in
`theo-data/`. The tree shows the canonical layout for new imports.

```
flav-data/
├── expe-data/                                     # Experimental measurement data
│   ├── CERN-LHCb/                                 # Lab-Collaboration folder
│   │   ├── 2015/
│   │   │   ├── LHCb@2015.json                     # Annual index
│   │   │   └── 12/
│   │   │       └── LHCb:2015svh.json              # Data file (Collaboration:TexKey)
│   ├── CERN-ATLAS/, CERN-CMS/, CERN-DELPHI/, CERN-OPAL/,
│   ├── CERN-LEP/                                  # Combined LEP (ALEPH+DELPHI+L3+OPAL)
│   ├── CERN-NA62/, CERN-CHARM-II/
│   ├── KEK-Belle/, KEK-KOTO/
│   ├── SLAC-BaBar/, SLAC-SLD/
│   ├── Fermilab-CDF/, Fermilab-D0/, Fermilab-Tevatron/, Fermilab-Muong-2/
│   ├── IHEP-BESIII/, IHEP-ISTRA+/
│   ├── INFN-KLOE-2/
│   ├── BNL-E949/, Cornell-CLEO/, TRIUMF-PiENu/
│   ├── PSI-SINDRUM-II/, PSI-nTRV/
│   ├── LANL-UCNA/, NIST-aCORN/
│   └── HFLAV/, PDG/                               # No-lab aggregation
└── theo-data/
    ├── FNAL-MILC/                                 # Large collaborations keep a group folder
    │   └── <year>/...
    ├── LQCD/                                      # Method folder for smaller groups
    │   └── 2015/
    │       ├── LQCD@2015.json                     # Method-level annual index
    │       └── 03/
    │           └── Detmold:2015aaa.json           # Data file (TexKey)
    └── QCD/                                       # Perturbative QCD calculations
```

**File depth**: new imports go to `<year>/<month>/<file>.json`, but legacy
files may sit directly under `<year>/`. The annual index records the month
either way, so resolve a file by checking both depths before concluding it
is missing (the snippets below do).

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

Theoretical folders depend on the size of the group:

- **Large collaborations** (HPQCD, JLQCD, RBC/UKQCD, FNAL/MILC, ...) keep
  their own top-level folder and follow the normal layout:
  `theo-data/<Group>/<year>/<month>/<TexKey>.json` with the annual index
  `theo-data/<Group>/<year>/<Group>@<year>.json`. A joint collaboration
  whose name contains `/` writes `-` in the folder and registry name
  (`FNAL-MILC`, `RBC-UKQCD`); the JSON `collaboration` field keeps the
  conventional slash spelling (`FNAL/MILC`).
- **Smaller calculation groups** are collected by the method they use:
  `theo-data/<Method>/<year>/<month>/<TexKey>.json`, with a method-level
  annual index `theo-data/<Method>/<year>/<Method>@<year>.json`. The
  method folders are `LQCD` (lattice QCD) and `QCD` (perturbative QCD);
  add a new method folder only for a new calculation method. Papers from
  small groups omit the `collaboration` key (SKILL.md rule 8), and TexKeys
  are unique, so several groups can share one method folder and index.

Only experimental data and theoretical calculations are stored; global
analyses (Wilson-coefficient fits, parameter determinations, bounds, world
averages) are not ingested. Form-factor parametrization fits are primary
theory data and are imported (see SKILL.md §Scope).

The Streamlit navigation links every entry in `defs.THEOGROUP`. The
method folders `LQCD` and `QCD` are registered there, so each gets a
navigation page scanning its year/month tree. A large-collaboration folder
(e.g. `FNAL-MILC`) is added to `THEOGROUP` the same way once it exists on disk.

**Special cases**:

- **HFLAV** and **PDG** use a non-standard flav-data schema (one
  snapshot JSON per year whose keys are subgroup names containing
  nested observables). See `json-meta.md` for details.
  When importing data into these groups, build a single year-level
  snapshot file rather than per-paper JSONs.

### Data Files

Format: `{Collaboration}:{TexKey}.json`

The filename uses only the collaboration name (not the full `Lab-Collaboration` folder name). For example, under `expe-data/CERN-LHCb/`, the data file is `LHCb:2015svh.json`. TexKey comes from InspireHEP.

| Example | Description |
|---------|-------------|
| `LHCb:2015svh.json` | LHCb paper, TexKey LHCb:2015svh |

**TexKey selection**: When a paper has both a collaboration-level and an author-level TexKey, the collaboration-level TexKey is canonical for filenames, paper indexing, and cross-references throughout this database. The author-level key is kept for citation but is not used in paths.

### Annual Index Files

Format: `{Collaboration}@{year}.json` — uses the collaboration name only (e.g., `LHCb@2015.json`).

Location: within the `Lab-Collaboration` folder's year subdirectory (e.g., `expe-data/CERN-LHCb/2015/LHCb@2015.json`).

```json
{
    "12": ["LHCb:2015svh"]
}
```

- **Keys**: Zero-padded month strings ("01" through "12").
- **Values**: Arrays of file_ids (without the `.json` extension).
- **Month ordering**: Keys in ascending order.
- **File ordering**: Within each month, file_ids sorted by arXiv v1 submission date.
- **TexKey freshness**: Always use the latest TexKey version from InspireHEP when updating indices.

## Index Operations

### Check if a Paper Exists

```python
import json, os

base = 'expe-data/CERN-LHCb'
target = 'LHCb:2015svh'

for year in sorted(os.listdir(base)):
    if not year.isdigit():
        continue
    idx_path = os.path.join(base, year, f'LHCb@{year}.json')
    if not os.path.exists(idx_path):
        continue
    for month, files in json.load(open(idx_path)).items():
        if target in files:
            for folder in (os.path.join(base, year, month), os.path.join(base, year)):
                path = os.path.join(folder, f'{target}.json')
                if os.path.exists(path):
                    print(f'Found: {path} (index month {month})')
```

### Verify Index Integrity

Compare indexed entries against actual files on disk to detect discrepancies:

```python
import json, os

base = 'expe-data/CERN-LHCb/2015'
index = json.load(open(f'{base}/LHCb@2015.json'))

# Index file_ids
indexed = {fid for files in index.values() for fid in files}

# Disk file_ids — both month subdirectories (YYYY/MM/) and flat files
# under the year directory (YYYY/). correlation.json is a matrix
# sidecar, not a paper, and is never indexed.
def is_paper(name):
    return name.endswith('.json') and '@' not in name and name != 'correlation.json'

on_disk = set()
for entry in sorted(os.listdir(base)):
    path = f'{base}/{entry}'
    if os.path.isdir(path) and entry.isdigit() and len(entry) == 2:
        on_disk |= {f[:-5] for f in os.listdir(path) if is_paper(f)}
    elif is_paper(entry):
        on_disk.add(entry[:-5])

# Report discrepancies
missing_in_index = on_disk - indexed
missing_on_disk = indexed - on_disk

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

#### Concrete Recipe (add new paper)

The index file (`expe-data/CERN-LHCb/2015/LHCb@2015.json`) does NOT
store submission dates — only file_ids — so re-sorting requires reading
each referenced JSON's `time` field. The most reliable workflow:

```bash
# Variables
TEXKEY="LHCb:2015svh"
COLLAB="LHCb"
YEAR="2015"
MONTH="12"  # zero-padded, from paper's arXiv v1 submission date
FILE_ID="LHCb:2015svh"  # TexKey, equals filename without ".json"
BASE="expe-data/CERN-LHCb/${YEAR}"
INDEX="${BASE}/${COLLAB}@${YEAR}.json"
PAPER="${BASE}/${MONTH}/${FILE_ID}.json"

# 1. Confirm the paper JSON exists and parses
python3 flav-data-importer/scripts/json-valid.py "${PAPER}"

# 2. Create index file (or load existing) and add file_id to month array.
#    Uses a small inline Python snippet — no separate script required.
python3 - <<PYEOF
import json, os
index_path = "${INDEX}"
paper_path = "${PAPER}"
file_id    = "${FILE_ID}"
month      = "${MONTH}"

if os.path.exists(index_path):
    with open(index_path) as f:
        idx = json.load(f)
else:
    idx = {}

# Add the file_id to its month (de-duplicate)
month_list = idx.setdefault(month, [])
if file_id not in month_list:
    month_list.append(file_id)

# Re-sort by arXiv v1 date (read 'time' field from each paper JSON).
# Papers may live in a YYYY/MM/ subdirectory or flat under YYYY/.
month_dir = os.path.dirname(paper_path)

def resolve(fid):
    for candidate in (
        os.path.join(month_dir, fid + '.json'),
        os.path.join(os.path.dirname(month_dir), fid + '.json'),
    ):
        if os.path.exists(candidate):
            return candidate
    raise FileNotFoundError(f'{fid}.json not found under {month_dir} or its parent')

def v1_date(fid):
    with open(resolve(fid)) as f:
        return json.load(f)['time']
idx[month] = sorted(month_list, key=v1_date)

os.makedirs(os.path.dirname(index_path), exist_ok=True)
with open(index_path, 'w') as f:
    json.dump(idx, f, indent=4, sort_keys=True)
    f.write('\n')
print(f'Updated {index_path}: month {month} now has {len(idx[month])} entries')
PYEOF

# 3. Confirm the index matches the files on disk (both depths)
#    → run the "Verify Index Integrity" snippet above
```

### Multi-Collaboration Papers

When a paper is a joint effort between multiple collaborations (e.g., ATLAS+CMS combination):
- Use the primary collaboration (first in the TexKey) for the directory and filename.
- The `collaboration` field in JSON lists all involved groups (e.g. `"ATLAS, CMS"`).
- Store the paper as a single JSON in the primary collaboration's directory. When each group's dataset differs, distinguish them with separate data groups (group-level `dataset`) inside that file — do not duplicate the paper across folders.

## Notes

1. **Always update the index** after adding or deleting a JSON file.
2. **Month assignment** is based on the arXiv v1 submission date.
3. **File size limit**: Keep JSON files under 10MB; split large correlation matrices.
4. **Validate** with `python3 flav-data-importer/scripts/json-valid.py` after writing (it also handles HFLAV/PDG snapshots — see json-meta.md).
5. **Backup before modifying** — especially when updating indices or replacing existing files.
6. **Index file ordering**: Within each month array, file_ids are sorted by arXiv v1 submission date. Since the index file itself doesn't store dates, re-sort whenever adding a new entry — look up each file's `time` field from its JSON content, then sort.
