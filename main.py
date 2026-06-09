# ---------------------------------------------------------
# Streamlit app entry point. Builds the top-level navigation
# tree from the EXPEGROUP / THEOGROUP registries in defs.py
# and dispatches the active page via st.navigation.
# ---------------------------------------------------------

# ---------------------------------------------------------
# Load packages and definitions
# ---------------------------------------------------------
with open('defs.py', 'r', encoding='utf-8') as f:
    exec(f.read())

# ---------------------------------------------------------
# Configure page layout
# ---------------------------------------------------------
st.set_page_config(
    layout="wide"
)


def _page_path(lab, exp, folder_override=None):
    """Build the relative path of a Streamlit page file.

    Most groups follow the ``<Lab>-<Collaboration>`` folder
    convention (e.g. ``Experimental/CERN-LHCb/LHCb.py``,
    ``Experimental/KEK-Belle/Belle.py``). Groups with no
    parent lab (``HFLAV``, ``PDG``) use
    the bare group name as the folder. ``folder_override``
    is currently unused by any registered group but is
    retained as an escape hatch for future non-standard
    parent directories.
    """
    if folder_override:
        folder = folder_override
    else:
        folder = f"{lab}-{exp}" if lab else exp
    return f"Experimental/{folder}/{exp}.py"


# Build the navigation tree. Each Experimental page lives at
# Experimental/<Lab>-<Collaboration>/<Collaboration>.py and each
# Theoretical page lives at Theoretical/<group>/<group>.py.
#
# We derive the page path directly from the registries in defs.py
# so adding a new group only requires updating defs.py + creating
# the matching .py file (no edits to main.py needed).
main_pages = {
    "Home": [
        st.Page("home.py", title="Home")
    ],
    "Observable": [
        st.Page(f"Observable/{obs}.py", title=obs) for obs in OBSGROUP
    ],
    "Experimental": [
        st.Page(_page_path(*entry),
                title=(
                    f"{entry[0]}-{entry[1]}"
                    if entry[0] else entry[1]
                ))
        for entry in EXPEGROUP
    ],
    "Theoretical": [
        st.Page(f"Theoretical/{theo}/{theo}.py", title=theo)
        for theo in THEOGROUP
    ]
}

main_navi = st.navigation(main_pages, position="top")
main_navi.run()
