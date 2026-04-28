# necessary packages and definitions

import streamlit as st
import json
import numpy as np
import pandas as pd
import sys
import os

def get_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
year_min, year_max = 1995, 2026
month_label = {
    "01": "Jan.",
    "02": "Feb.",
    "03": "Mar.",
    "04": "Apr.",
    "05": "May.",
    "06": "Jun.",
    "07": "Jul.",
    "08": "Aug.",
    "09": "Sep.",
    "10": "Oct.",
    "11": "Nov.",
    "12": "Dec."
}
