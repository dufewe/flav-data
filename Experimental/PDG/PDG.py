# ---------------------------------------------------------
# Streamlit page for the Particle Data Group (PDG) review.
#
# PDG data is stored in a non-standard flav-data schema
# (one JSON per year containing every PDG subgroup as a
# flat dict of obs@N entries), so this page renders the
# PDG-specific layout directly instead of calling
# ``run_dashboard``.
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
    page_title="PDG — Particle Data Group",
    page_icon=":atom_symbol:",
    layout="wide"
)

st.title("PDG — Particle Data Group")
st.markdown(
    "**World-average particle properties from the PDG review "
    "(`inspire-hep = ParticleDataGroup:2024cfk`).**"
)

# ---------------------------------------------------------
# Load the most recent PDG snapshot
# ---------------------------------------------------------
base_dir = os.path.join(EXPERIMENTAL_BASE, "PDG")
year_dirs = sorted(
    (d for d in os.listdir(base_dir) if d.isdigit() and len(d) == 4),
    reverse=True,
)

if not year_dirs:
    st.warning(f"No PDG data found in {base_dir}/")
    st.stop()

latest_year = year_dirs[0]
idx_path = os.path.join(base_dir, latest_year, f"PDG@{latest_year}.json")

try:
    pdg = get_json(idx_path)
except (FileNotFoundError, json.JSONDecodeError) as e:
    st.error(f"Failed to load {idx_path}: {e}")
    st.stop()

# Header
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown(f"- **YEAR**: {latest_year}")
    st.markdown(f"- **INPIRE-HEP**: {pdg.get('inspire-hep', 'N/A')}")
    st.markdown(f"- **AUTHOR**: {pdg.get('author', 'N/A')}")
with col2:
    st.markdown(f"- **TITLE**: {pdg.get('title', 'N/A')}")
    abstract = pdg.get('abstract', 'N/A')
    if isinstance(abstract, str) and len(abstract) > 800:
        abstract = abstract[:800] + "..."
    st.markdown(f"- **ABSTRACT**: {abstract}")

st.divider()

# ---------------------------------------------------------
# Subgroup navigation
# ---------------------------------------------------------
data = pdg.get("data", {})
if not data:
    st.warning("No subgroup data found in this PDG snapshot.")
    st.stop()

# Sidebar picker (which subgroup to inspect)
with st.sidebar:
    st.markdown("# Filters")
    st.markdown("##### PDG Subgroup")
    subgroup = st.radio(
        "PDG Subgroup",
        list(data.keys()),
        label_visibility="collapsed",
    )

# Render the chosen subgroup as a table
st.subheader(subgroup)
subgroup_data = data[subgroup]

# Pull out obs@N entries (skip the optional correlation key)
rows = []
for k, v in subgroup_data.items():
    if not k.startswith("obs@"):
        continue
    row = {"key": k, **v}
    rows.append(row)

if not rows:
    st.info("No obs@N entries in this subgroup.")
else:
    st.table(rows)

# Correlation matrix, if present
corr = subgroup_data.get("correlation")
if corr is not None:
    st.markdown("**Correlation matrix**")
    st.table(corr)
