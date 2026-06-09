# ---------------------------------------------------------
# Streamlit page for the NIST aCORN.
#
# Lab-Collaboration folder: ``Experimental/NIST-aCORN/``.
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
# Run dashboard UI for the (NIST, aCORN) collaboration
# ---------------------------------------------------------
run_dashboard(
    lab="NIST",
    group="aCORN",
    year_min=year_min,
    year_max=year_max,
    get_json_func=get_json,
    month_label=month_label,
    base_path=EXPERIMENTAL_BASE
)
