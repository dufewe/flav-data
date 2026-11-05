# ---------------------------------------------------------
# Streamlit page for the Fermilab Tevatron combined (CDF+D0).
#
# Lab-Collaboration folder: ``Experimental/Fermilab-Tevatron/``.
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
# Run dashboard UI for the (Fermilab, Tevatron) collaboration
# ---------------------------------------------------------
run_dashboard(
    lab="Fermilab",
    group="Tevatron",
    year_min=year_min,
    year_max=year_max,
    get_json_func=get_json,
    month_label=month_label,
    base_path=EXPERIMENTAL_BASE
)
