# ---------------------------------------------------------
# Streamlit page for the CERN LEP combined (ALEPH+DELPHI+L3+OPAL).
#
# Lab-Collaboration folder: ``Experimental/CERN-LEP/``.
# ---------------------------------------------------------

# ---------------------------------------------------------
# Load packages and definitions
# ---------------------------------------------------------
with open('defs.py', 'r', encoding='utf-8') as f:
    exec(f.read())

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flav_dashboard import run_dashboard

# ---------------------------------------------------------
# Run dashboard UI for the (CERN, LEP) collaboration
# ---------------------------------------------------------
run_dashboard(
    lab="CERN",
    group="LEP",
    year_min=year_min,
    year_max=year_max,
    get_json_func=get_json,
    month_label=month_label,
    base_path=EXPERIMENTAL_BASE
)
