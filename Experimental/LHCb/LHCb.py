# ---------------------------------------------------------
# Load packages and definitions
# ---------------------------------------------------------
with open('defs.py', 'r', encoding='utf-8') as f:
    exec(f.read())
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Test.OBS.flav_dashboard import run_dashboard

# ---------------------------------------------------------
# Run dashboard UI by specify experimental collaboration
# ---------------------------------------------------------
run_dashboard(
    group = "LHCb", 
    year_min = year_min, 
    year_max = year_max, 
    get_json_func = get_json, 
    month_label = month_label
)
