# ---------------------------------------------------------
# Streamlit page for the Heavy Flavor Averaging Group (HFLAV).
#
# HFLAV data is stored in a non-standard flav-data schema
# (one snapshot JSON whose keys are HFLAV subgroup names
# containing nested observables), so this page renders the
# HFLAV-specific layout directly instead of calling
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
    page_title="HFLAV — Heavy Flavor Averaging Group",
    page_icon=":atom_symbol:",
    layout="wide"
)

st.title("HFLAV — Heavy Flavor Averaging Group")
st.markdown(
    "**World-average heavy-flavor measurements from the HFLAV review "
    "(`inspire-hep = HeavyFlavorAveragingGroupHFLAV:2024ctg`).**"
)

# ---------------------------------------------------------
# Load the most recent HFLAV snapshot
# ---------------------------------------------------------
base_dir = os.path.join(EXPERIMENTAL_BASE, "HFLAV")
candidates = sorted(
    (f for f in os.listdir(base_dir) if f.endswith(".json")),
    reverse=True,
)
if not candidates:
    st.warning(f"No HFLAV data found in {base_dir}/")
    st.stop()

idx_path = os.path.join(base_dir, candidates[0])
try:
    hfla = get_json(idx_path)
except (FileNotFoundError, json.JSONDecodeError) as e:
    st.error(f"Failed to load {idx_path}: {e}")
    st.stop()

# Sidebar: which HFLAV subgroup to view
subgroup_keys = [k for k in hfla.keys() if k.startswith("HFLAV@")]
with st.sidebar:
    st.markdown("# Filters")
    st.markdown("##### HFLAV Subgroup")
    subgroup = st.radio(
        "HFLAV Subgroup",
        subgroup_keys,
        label_visibility="collapsed",
    )

# Render the chosen subgroup
subgroup_data = hfla.get(subgroup, {})
st.subheader(subgroup)

col1, col2 = st.columns([1, 2])
with col1:
    for k, v in subgroup_data.items():
        if k == "observables":
            continue
        st.markdown(f"- **{k.upper()}**: {v}")
with col2:
    observables = subgroup_data.get("observables", [])
    if observables:
        st.markdown(f"**{len(observables)} observables**")
        st.table(observables)
    else:
        st.info("No observables in this subgroup.")
