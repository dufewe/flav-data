# ---------------------------------------------------------
# Streamlit app entry point. Builds the top-level navigation
# tree from the EXPEGROUP / THEOGROUP registries in defs.py and
# dispatches every group to the shared dashboard renderers.
# ---------------------------------------------------------

import os
import sys
from functools import partial

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)

with open(os.path.join(HERE, 'defs.py'), 'r', encoding='utf-8') as f:
    exec(f.read())

import streamlit as st

from flav_dashboard import run_dashboard, run_snapshot_dashboard

st.set_page_config(layout="wide")


def _dashboard_page(lab, group, base_path):
    return partial(
        run_dashboard, lab=lab, group=group,
        year_min=year_min, year_max=year_max,
        get_json_func=get_json, month_label=month_label,
        base_path=base_path,
    )


def _snapshot_page(group):
    return partial(
        run_snapshot_dashboard, group=group,
        get_json_func=get_json, base_path=EXPERIMENTAL_BASE,
    )


def _experimental_page(entry):
    lab, group = entry[0], entry[1]
    if group in ('HFLAV', 'PDG'):
        return _snapshot_page(group)
    return _dashboard_page(lab, group, EXPERIMENTAL_BASE)


def _title(entry):
    lab, group = entry[0], entry[1]
    return f"{lab}-{group}" if lab else group


main_pages = {
    "Home": [st.Page("home.py", title="Home")],
    "Observable": [
        st.Page(f"Observable/{obs}.py", title=obs) for obs in OBSGROUP
    ],
    "Experimental": [
        st.Page(_experimental_page(entry), title=_title(entry),
                url_path=_title(entry))
        for entry in EXPEGROUP
    ],
    "Theoretical": [
        st.Page(_dashboard_page("", theo, THEORETICAL_BASE), title=theo,
                url_path=theo)
        for theo in THEOGROUP
    ],
}

st.navigation(main_pages, position="top").run()
