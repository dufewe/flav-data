# ---------------------------------------------------------
# Homepage of flav-data — Flavor Physics Database
# ---------------------------------------------------------

# ---------------------------------------------------------
# Load packages and definitions
# ---------------------------------------------------------
with open('defs.py', 'r', encoding='utf-8') as f:
    exec(f.read())

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="flav-data — Flavor Physics Database",
    page_icon=":atom_symbol:",
    layout="wide"
)

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.title("flav-data")
st.markdown("**A Structured Flavor Physics Measurement Database**")

st.divider()

# ---------------------------------------------------------
# Overview
# ---------------------------------------------------------
st.header("Overview")

# Collaboration labels for the table summary
expe_labels = [g for _, g, *_ in EXPEGROUP]

st.markdown(f'''
**flav-data** is a curated, machine-readable database of flavor physics measurements
from major experimental collaborations and theory groups. It provides standardized
JSON entries for branching fractions, angular observables, CP asymmetries, lepton
flavor universality ratios, and more — all following a consistent naming convention
and format specification.

The database covers measurements from **{year_min}** to **{year_max}** and supports
the following groups:

| Category | Groups |
|----------|--------|
''')

st.markdown(f"| Experimental | {', '.join(expe_labels)} |")
st.markdown(f"| Theoretical | {', '.join(THEOGROUP)} |")
st.markdown(f"| Observable | {', '.join(OBSGROUP)} |")

st.markdown('''
## Features

- **Standardized JSON format** — every entry follows the same schema with metadata, data arrays, and transition-mode classification
- **Machine-parseable naming** — transition symbols (`A.B.2.C.D`) and observable names (`OBS(transition)[condition]`) enable automated data retrieval
- **Year-indexed organization** — annual index files (`LHCb@2025.json`) for fast lookup
- **Month subdirectories** — files organized by arXiv v1 submission date
- **Complete error breakdown** — component-level (stat/syst) errors with optional correlation matrices
- **Cross-paper merging** — multiple arXiv papers describing the same measurement merged into a single JSON
''')

# ---------------------------------------------------------
# Quick Navigation
# ---------------------------------------------------------
st.header("Quick Navigation")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Observable Guide")
    st.markdown('''
    Browse the naming conventions and observable abbreviations:

    - **Flavor** — Transition symbols, particle abbreviations,
      observable naming rules, angular coefficients, CP asymmetries,
      optimized observables (P), LFU differences (Q), CKM parameters
    - **EWPO** — Electroweak precision observables: Z-pole,
      W boson, weak mixing angle, Higgs, S/T/U parameters
    ''')

with col2:
    st.subheader("Experimental Data")
    st.markdown(f'''
    Browse measurements by collaboration:

    {", ".join(expe_labels)}

    Each collaboration page features an interactive dashboard with
    timeline views, observable filtering, and data export.
    ''')

with col3:
    st.subheader("Theoretical Calculations")
    st.markdown(f'''
    Browse theory group results:

    {", ".join(THEOGROUP)}

    Includes lattice QCD calculations of form factors, decay constants,
    and other non-perturbative parameters.
    ''')

st.divider()

# ---------------------------------------------------------
# JSON Format Example
# ---------------------------------------------------------
st.header("JSON Format Example")

st.markdown('''
Each JSON file corresponds to one experimental or theoretical paper:
''')
st.code('''{
    "inspire-hep": "[LHCb:2015svh](https://inspirehep.net/literature/1409497)",
    "author": "Aaij, Roel and others",
    "collaboration": "LHCb",
    "title": "Angular analysis of the $B^{0}\\\\to K^{*0}\\\\mu^{+}\\\\mu^{-}$ decay",
    "arxiv": "[hep-ex/1512.04442v1](https://arxiv.org/pdf/1512.04442)",
    "time": "2015.12.14",
    "abstract": "An angular analysis of the $B^{0}\\\\to K^{*0}(\\\\to K^{+}\\\\pi^{-})\\\\mu^{+}\\\\mu^{-}$ decay...",
    "pdf": "https://arxiv.org/pdf/1512.04442",
    "data": [
        {
            "obs@1": {
                "name": "FL(B0.2.Kst0.mu+.mu-)",
                "latex": "$F_L(B^{0}\\\\to K^{*0}\\\\mu^{+}\\\\mu^{-})$",
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
            "obs@2": { "...": "..." },
            "type@1_correlation": [[1.0, 0.06], [0.06, 1.0]]
        }
    ],
    "transition-mode": "semileptonic decay"
}''', language="json")

st.markdown('''
**Key design principles:**

| Principle | Implementation |
|-----------|----------------|
| All numeric values are strings | `"0.69"` not `0.69` |
| Component errors preferred | Separate `type@1_err` (stat), `type@2_err` (syst) |
| Correlation matrices at entry level | `type@1_correlation` alongside `obs@N` keys |
| LaTeX escaping | `\\\\to` in JSON → `\\to` after parsing |
| Transition symbol | `A.B.2.C.D` replaces $A + B \\to C + D$ |
| Observable naming | `OBS(transition)[condition]` |
''')

# ---------------------------------------------------------
# Database Statistics
# ---------------------------------------------------------
st.divider()
st.header("Database Statistics")

# Count indexed files dynamically. We walk every Lab-Collaboration
# folder listed in EXPEGROUP plus every THEOGROUP entry.
total_files = 0
file_ids = []

for entry in EXPEGROUP:
    lab, group = entry[0], entry[1]
    # entry may be a 2-tuple (lab, group) or a 3-tuple
    # (lab, group, folder_override). When the folder is overridden
    # use that explicit path; otherwise build ``<lab>-<group>``,
    # or the bare group name when lab is empty (aggregation
    # groups like HFLAV and PDG).
    if len(entry) >= 3 and entry[2]:
        group_dir = os.path.join(EXPERIMENTAL_BASE, entry[2])
    elif lab:
        group_dir = os.path.join(EXPERIMENTAL_BASE, f"{lab}-{group}")
    else:
        group_dir = os.path.join(EXPERIMENTAL_BASE, group)
    if not os.path.isdir(group_dir):
        continue
    for year in sorted(os.listdir(group_dir)):
        if not (year.isdigit() and len(year) == 4):
            continue
        idx_path = os.path.join(group_dir, year, f"{group}@{year}.json")
        if not os.path.exists(idx_path):
            continue
        try:
            index = get_json(idx_path)
        except (FileNotFoundError, json.JSONDecodeError):
            continue
        for _month, ids in index.items():
            for fid in ids:
                total_files += 1
                file_ids.append(f"{group}:{year}")

for group in THEOGROUP:
    group_dir = os.path.join(THEORETICAL_BASE, group)
    if not os.path.isdir(group_dir):
        continue
    for year in sorted(os.listdir(group_dir)):
        if not (year.isdigit() and len(year) == 4):
            continue
        idx_path = os.path.join(group_dir, year, f"{group}@{year}.json")
        if not os.path.exists(idx_path):
            continue
        try:
            index = get_json(idx_path)
        except (FileNotFoundError, json.JSONDecodeError):
            continue
        for _month, ids in index.items():
            for fid in ids:
                total_files += 1
                file_ids.append(f"{group}:{year}")

st.metric("Total JSON Entries", total_files)

# Year list comes from the year field embedded in `group:year` IDs
unique_years = sorted({fid.split(":")[-1] for fid in file_ids if fid.split(":")[-1].isdigit()})
if unique_years:
    st.caption(f"Spanning years: {', '.join(unique_years)}")
