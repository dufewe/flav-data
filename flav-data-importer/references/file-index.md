# File Indexing and Directory Structure

This document specifies the directory layout, file naming conventions, and annual index management for the flav-data database.

## Directory Layout

Experimental measurements live in `expe-data/`, theoretical calculations in
`theo-data/`. The tree shows the canonical layout for new imports.

```
flav-data/
├── expe-data/
│   └── <Lab>-<Collaboration>/                 # e.g. CERN-LHCb; HFLAV/ and PDG/ have no lab
│       └── <year>/
│           ├── <Collaboration>@<year>.json    # Annual index
│           └── <month>/
│               └── <Collaboration>:<TexKey>.json
└── theo-data/
    └── <Group-or-Method>/                     # e.g. FNAL-MILC, LQCD, LCSR, QCD
        └── <year>/
            ├── <Group-or-Method>@<year>.json
            └── <month>/
                └── <TexKey>.json
```

The folder table below lists every experimental group currently on disk.

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
| `PSI-nTRV` | PSI | nTRV | Neutron decay electron polarization |
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
  method folders are `LCSR` (light-cone sum rules), `LQCD` (lattice QCD)
  and `QCD` (perturbative QCD);
  add a new method folder only for a new calculation method. Papers from
  small groups omit the `collaboration` key (SKILL.md rule 8), and TexKeys
  are unique, so several groups can share one method folder and index.

Import eligibility (measurements and calculations only, no global analyses)
is defined in `data-source.md` §Scope.

The Streamlit navigation links every entry in `defs.THEOGROUP`. The
method folders `LCSR`, `LQCD` and `QCD` are registered there, so each gets a
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

Search both depths before concluding a paper is missing (SKILL.md Step 1):

```bash
find expe-data/CERN-LHCb -mindepth 2 -maxdepth 3 -name 'LHCb:2015svh.json'
```

To check the index rather than the disk, load each
`<Collaboration>@<year>.json` under the group folder and look for the
file_id in its month arrays.

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

The index stores only file_ids, not submission dates, so re-sorting means
reading each referenced paper's `time` field. Papers may sit in
`<year>/<month>/` or flat under `<year>/`, hence `resolve()` tries both.

```bash
BASE="expe-data/CERN-LHCb/2015"
INDEX="${BASE}/LHCb@2015.json"
MONTH="12"                       # zero-padded, from the arXiv v1 date
FILE_ID="LHCb:2015svh"           # TexKey = filename without ".json"
PAPER="${BASE}/${MONTH}/${FILE_ID}.json"

python3 flav-data-importer/scripts/json-valid.py "${PAPER}"

python3 - <<PYEOF
import json, os
idx = json.load(open("${INDEX}")) if os.path.exists("${INDEX}") else {}
month_list = idx.setdefault("${MONTH}", [])
if "${FILE_ID}" not in month_list:
    month_list.append("${FILE_ID}")

def resolve(fid):
    for folder in ("${BASE}/${MONTH}", "${BASE}"):
        path = os.path.join(folder, fid + '.json')
        if os.path.exists(path):
            return path
    raise FileNotFoundError(fid)

idx["${MONTH}"] = sorted(
    month_list, key=lambda fid: json.load(open(resolve(fid)))['time'])
with open("${INDEX}", 'w') as f:
    json.dump(idx, f, indent=4, sort_keys=True)
    f.write('\n')
PYEOF
```

Then run "Verify Index Integrity" above to confirm the index matches disk.

### Multi-Collaboration Papers

When a paper is a joint effort between multiple collaborations (e.g., ATLAS+CMS combination):
- Use the primary collaboration (first in the TexKey) for the directory and filename.
- The `collaboration` field in JSON lists all involved groups (e.g. `"ATLAS, CMS"`).
- Store the paper as a single JSON in the primary collaboration's directory. When each group's dataset differs, distinguish them with separate data groups (group-level `dataset`) inside that file — do not duplicate the paper across folders.

## Notes

1. **File size limit**: Keep JSON files under 10MB; split large correlation matrices.
2. **Validate** with `python3 flav-data-importer/scripts/json-valid.py <file> [<file> ...] [--quiet]` after writing (it also handles HFLAV/PDG snapshots — see json-meta.md).
3. **Backup before modifying** — especially when updating indices or replacing existing files.
