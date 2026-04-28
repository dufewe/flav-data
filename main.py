# Streamlit page of data presentation

# Load packages and definitions
with open('defs.py', 'r', encoding='utf-8') as f:
    exec(f.read())

# Load streamlit Pages
st.set_page_config(
    layout="wide"
)

main_pages = {
    "Home": [
        st.Page("home.py", title="Home")
    ],
    "Observable": [
        st.Page(f"Observable/{obs}.py", title=f"{obs}") for obs in ["Flavor","EWPO"]
    ],
    "Experimental": [
        st.Page(f"Experimental/{exp}/{exp}.py", title=f"{exp}") for exp in ["ATLAS","CMS","LHCb"]
    ],
    "Theoretical": [
        st.Page(f"Theoretical/{theo}/{theo}.py", title=f"{theo}") for theo in ["HPQCD"]
    ]
}

main_navi = st.navigation(main_pages, position="top")
main_navi.run()