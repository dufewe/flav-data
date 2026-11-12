# ---------------------------------------------------------
# Shared definitions for the flav-data Streamlit app.
# Loaded via `exec` from main.py (and the obs-info pages) so the
# same name bindings (get_json, EXPEGROUP, ...) are available in the
# caller's module scope. As a side effect this also injects
# `streamlit` (as `st`), `json`, and `os` into the caller's globals.
# ---------------------------------------------------------

import streamlit as st
import json
import os
from datetime import datetime

# Project root resolved by walking up from the calling page (or the
# working directory when __file__ is unavailable, e.g. under exec),
# so pages and data paths do not depend on the launch directory.
def _find_project_root():
    try:
        current = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        current = os.getcwd()
    while True:
        if os.path.isfile(os.path.join(current, 'defs.py')):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return os.path.dirname(os.path.abspath('defs.py'))
        current = parent


PROJECT_ROOT = _find_project_root()

# I/O ----------------------------------------------------------------

def get_json(file_path):
    """Load a JSON file from disk and return its parsed contents.

    Raises FileNotFoundError if the path does not exist; callers are
    responsible for handling that case (typically by skipping the
    entry or showing a placeholder).
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Configuration -------------------------------------------------------

# Year range scanned when looking for annual index files. The
# earliest indexed entry is CHARM-II 1990.
year_min, year_max = 1990, datetime.now().year

# Mapping from month-number string (zero-padded, as used in the
# annual index file and the month subdirectory name) to the
# short English label shown in the dashboard headers.
month_label = {
    "01": "Jan.", "02": "Feb.", "03": "Mar.", "04": "Apr.",
    "05": "May.", "06": "Jun.", "07": "Jul.", "08": "Aug.",
    "09": "Sep.", "10": "Oct.", "11": "Nov.", "12": "Dec.",
}

# Collaboration registry ---------------------------------------------
#
# Each entry produces an ``expe-data/<Lab>-<Collaboration>/`` folder
# (or ``expe-data/<Collaboration>/`` when ``lab`` is empty for
# aggregation groups, or ``theo-data/<Collaboration>`` for theoretical
# groups). A 2-tuple ``(lab, collaboration)`` uses that default; a
# 3-tuple with a third ``folder_override`` element lets a group live
# under a non-standard path (currently unused; kept as an escape hatch).
#
# Navigation entries are generated in ``main.py`` from the same
# registries, so adding a group only requires updating this list.
EXPEGROUP = [
    # CERN
    ("CERN", "LHCb"),
    ("CERN", "ATLAS"),
    ("CERN", "CMS"),
    ("CERN", "DELPHI"),
    ("CERN", "OPAL"),
    ("CERN", "LEP"),         # Combined LEP (ALEPH+DELPHI+L3+OPAL)
    ("CERN", "NA62"),
    ("CERN", "CHARM-II"),
    # KEK
    ("KEK",  "Belle"),
    ("KEK",  "KOTO"),
    # SLAC
    ("SLAC", "BaBar"),
    ("SLAC", "SLD"),
    # Fermilab
    ("Fermilab", "CDF"),
    ("Fermilab", "D0"),
    ("Fermilab", "Tevatron"),  # Combined CDF+D0
    ("Fermilab", "Muong-2"),
    # IHEP / Beijing
    ("IHEP", "BESIII"),
    ("IHEP", "ISTRA+"),
    # INFN / Frascati
    ("INFN", "KLOE-2"),
    # Other physics labs
    ("BNL",     "E949"),
    ("Cornell", "CLEO"),
    ("TRIUMF",  "PiENu"),
    ("PSI",     "SINDRUM-II"),
    ("PSI",     "nTRV"),
    ("LANL",    "UCNA"),
    ("NIST",    "aCORN"),
    # Aggregation groups (no parent lab)
    ("", "HFLAV"),
    ("", "PDG"),
]

THEOGROUP = [
    "FNAL-MILC",
    "LQCD",
    "QCD",
    "RBC-UKQCD",
]

OBSGROUP = ["Flavor", "EWPO"]

# Paths ---------------------------------------------------------------
# Absolute so pages work regardless of the launch directory.
EXPERIMENTAL_BASE = os.path.join(PROJECT_ROOT, "expe-data")
THEORETICAL_BASE  = os.path.join(PROJECT_ROOT, "theo-data")


def resolve_folder(lab, group, folder_override=None):
    """Return the on-disk folder name for a group.

    ``<Lab>-<Collaboration>`` for experimental groups, the bare group
    name when ``lab`` is empty, or ``folder_override`` when given.
    """
    if folder_override:
        return folder_override
    return f"{lab}-{group}" if lab else group
