# ---------------------------------------------------------
# Streamlit page for the HPQCD theoretical group.
# Lab-Collaboration folder: ``Theoretical/HPQCD/`` (theoretical
# groups use the bare group name, not ``<Lab>-<Collaboration>``).
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
# Run dashboard UI for the HPQCD theoretical group
# ---------------------------------------------------------
run_dashboard(
    lab="",
    group="HPQCD",
    year_min=year_min,
    year_max=year_max,
    get_json_func=get_json,
    month_label=month_label,
    base_path=THEORETICAL_BASE
)
