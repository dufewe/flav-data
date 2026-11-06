# ---------------------------------------------------------
# Homepage of flav-data — Flavor Physics Database
# ---------------------------------------------------------

# ---------------------------------------------------------
# Load packages and definitions
# ---------------------------------------------------------
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(PROJECT_ROOT, 'defs.py'), 'r', encoding='utf-8') as f:
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
| Experimental | {', '.join(expe_labels)} |
| Theoretical | {', '.join(THEOGROUP)} |
| Observable | {', '.join(OBSGROUP)} |
''')

st.markdown('''
## Features

- **Standardized JSON format** — every entry follows the same schema with metadata, data arrays, and transition-mode classification
- **Machine-parseable naming** — `data` keys carry transition symbols (`A.B.2.C.D`) and observable names are bare symbols with optional `[condition]` qualifiers
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
    year, month, and transition-mode filters.
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
    "transition-mode": "semileptonic-decay",
    "data": [
        {
            "B0.2.Kst0.mu+.mu-": {
                "obs@1": {
                    "name": "FL",
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
                "obs@2": { "...": "..." }
            },
            "type@1_correlation": [[1.0, 0.06], [0.06, 1.0]]
        }
    ]
}''', language="json")

st.markdown('''
**Key design principles:**

| Principle | Implementation |
|-----------|----------------|
| All numeric values are strings | `"0.69"` not `0.69` |
| Component errors preferred | Separate `type@1_error` (stat), `type@2_error` (syst) |
| Correlation matrices at group level | `correlation`/`type@1_correlation` alongside channel keys |
| Transition key | group channel key `A.B.2.C.D` replaces $A + B \\to C + D$ |
| No channel LaTeX | transition is encoded by the channel key; `data` stores no LaTeX |
| LaTeX escaping | `\\\\to` in `title`/`abstract` JSON → `\\to` after parsing |
| Observable naming | bare `OBS` symbol; `[condition]` only for multi-transition ratios |
''')

# ---------------------------------------------------------
# Database Statistics
# ---------------------------------------------------------
@st.cache_data(ttl=300)
def get_database_statistics(experimental_groups, theoretical_groups,
                           experimental_base, theoretical_base):
    total_files = 0
    years = set()

    def count_group(group, group_dir):
        nonlocal total_files
        if not os.path.isdir(group_dir):
            return
        for year in os.listdir(group_dir):
            if not (year.isdigit() and len(year) == 4):
                continue
            idx_path = os.path.join(group_dir, year, f"{group}@{year}.json")
            try:
                index = get_json(idx_path)
            except (FileNotFoundError, json.JSONDecodeError):
                continue
            if not isinstance(index, dict):
                continue
            entry_ids = [ids for ids in index.values() if isinstance(ids, list)]
            total_files += sum(len(ids) for ids in entry_ids)
            if any(entry_ids):
                years.add(year)

    for entry in experimental_groups:
        lab, group = entry[0], entry[1]
        override = entry[2] if len(entry) >= 3 else None
        folder = resolve_folder(lab, group, override)
        count_group(group, os.path.join(experimental_base, folder))

    for group in theoretical_groups:
        count_group(group, os.path.join(theoretical_base, group))

    return total_files, sorted(years)


total_files, unique_years = get_database_statistics(
    tuple(tuple(entry) for entry in EXPEGROUP),
    tuple(THEOGROUP),
    EXPERIMENTAL_BASE,
    THEORETICAL_BASE,
)
st.metric("Total Indexed Entries", total_files)
if unique_years:
    st.caption(f"Spanning years: {', '.join(unique_years)}")
