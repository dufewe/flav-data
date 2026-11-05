# ---------------------------------------------------------
# Streamlit page for the LNF Frascati DAΦNE KLOE-2.
#
# Lab-Collaboration folder: ``Experimental/INFN-KLOE-2/``.
# ---------------------------------------------------------

# ---------------------------------------------------------
# Load packages and definitions
# ---------------------------------------------------------
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, PROJECT_ROOT)

with open(os.path.join(PROJECT_ROOT, 'defs.py'), 'r', encoding='utf-8') as f:
    exec(f.read())

from flav_dashboard import run_dashboard

# ---------------------------------------------------------
# Run dashboard UI for the (INFN, KLOE-2) collaboration
# ---------------------------------------------------------
run_dashboard(
    lab="INFN",
    group="KLOE-2",
    year_min=year_min,
    year_max=year_max,
    get_json_func=get_json,
    month_label=month_label,
    base_path=EXPERIMENTAL_BASE
)
