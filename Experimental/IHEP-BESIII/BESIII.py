# ---------------------------------------------------------
# Streamlit page for the IHEP BEPCII BESIII.
#
# Lab-Collaboration folder: ``Experimental/IHEP-BESIII/``.
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
# Run dashboard UI for the (IHEP, BESIII) collaboration
# ---------------------------------------------------------
run_dashboard(
    lab="IHEP",
    group="BESIII",
    year_min=year_min,
    year_max=year_max,
    get_json_func=get_json,
    month_label=month_label,
    base_path=EXPERIMENTAL_BASE
)
