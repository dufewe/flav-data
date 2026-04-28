# ---------------------------------------------------------
# Load packages and definitions
# ---------------------------------------------------------
with open('defs.py', 'r', encoding='utf-8') as f:
    exec(f.read())

# ---------------------------------------------------------
# Core Optimization: Pre-loader Function
# Loads all selected JSON files into memory at once to avoid repetitive I/O
# ---------------------------------------------------------
@st.cache_data(ttl = 3600)
def get_cached_data(group, years, months, _get_json_func, base_path = 'Experimental'):
    """
    Traverse all selected years and months, load JSON details into a list.
    Returns a list of dictionaries, each representing one paper/entry.
    """
    data_pool = []
    
    for year in years:
        index_path = f'{base_path}/{group}/{year}/{group}@{year}.json'
        try:
            json_index = _get_json_func(index_path)
            for m_key, item_ids in json_index.items():
                if int(m_key) in months:
                    for fid in item_ids:
                        detail_path = f'{base_path}/{group}/{year}/{m_key}/{fid}.json'
                        detail = _get_json_func(detail_path)
                        if detail:
                            # Inject metadata for subsequent sorting and grouping
                            detail['_year'] = year
                            detail['_month'] = m_key
                            data_pool.append(detail)
        except FileNotFoundError:
            continue
    return data_pool


# ---------------------------------------------------------
# Detect available years (Lightweight detection, does not load content)
# ---------------------------------------------------------
def detect_years(group, year_min, year_max, get_json_func, base_path = 'Experimental'):
    years = []
    for year in range(year_min, year_max + 1):
        try:
            get_json_func(f'{base_path}/{group}/{year}/{group}@{year}.json')
            years.append(year)
        except FileNotFoundError:
            continue
    return years
    

# ---------------------------------------------------------
# Display the full dashboard UI
# ---------------------------------------------------------
def run_dashboard(group, year_min, year_max, get_json_func, month_label = None, base_path = 'Experimental'):
    if month_label is None: month_label = {}
    
    ## Detect available years
    exp_year_list = detect_years(group, year_min, year_max, get_json_func, base_path)
        
    if not exp_year_list:
        st.warning(f"No {group} data found in {base_path}/{group}/")
        return
    
    ## Sidebar Settings & Filtering
    with st.sidebar:
        st.markdown("# Filters")

        ### Year filter
        st.markdown("##### Select Year Range")
        year_range = st.slider(
            "Select Year Range",
            min_value = min(exp_year_list),
            max_value = max(exp_year_list),
            value = (min(exp_year_list), max(exp_year_list)),
            step = 1,
            label_visibility = "collapsed"
        )
        selected_years = list(range(year_range[0], year_range[1] + 1))

        ### Month filter
        st.markdown("##### Select Month Range")
        month_range = st.slider(
            "Select Month Range",
            min_value = 1,
            max_value = 12,
            value = (1, 12),
            step = 1,
            label_visibility = "collapsed"
        )
        selected_months = list(range(month_range[0], month_range[1] + 1))

        ### Pre-load all data (One-time I/O)
        raw_data = get_cached_data(group, selected_years, selected_months, get_json_func, base_path)

        ### Transition filter
        transition_set = set(mode.get("transition-mode") for mode in raw_data if "transition-mode" in mode)
        transition_list = sorted(list(transition_set))

        st.markdown("##### Select Transition Mode")
        selected_transitions = [t for t in transition_list if st.checkbox(t)]
        
        ### Apply filters
        filtered_data = [
            mode for mode in raw_data 
            if mode.get('transition-mode') in selected_transitions
        ]

        ### Statistics (Operate directly on memory objects, zero I/O)
        st.markdown("# Statistics")
        tot_exp = len(filtered_data)

        tot_obs = sum(
            sum(1 for k in entry if k.startswith("obs@"))
            for mode in filtered_data
            for entry in mode.get('data', [])
            if isinstance(entry, dict)
        )
                
        st.markdown("##### Total Experiments")
        st.metric("Total Experiments", tot_exp, label_visibility="collapsed")
        st.markdown("##### Total Observables")
        st.metric("Total Observables", tot_obs, label_visibility="collapsed")

    ## Main Content Display
    ### Sort by year and month for sequential rendering (Descending order)
    filtered_data.sort(key = lambda x: (x.get('_year', 0), x.get('_month', '00')), reverse = True)

    ### Iterate and display in groups
    current_header = ""
    for json_detail in filtered_data:
        year = json_detail.get('_year')
        month_key = json_detail.get('_month')
    
        #### Generate header text, consistent with the original version
        month_name = month_label.get(str(month_key), month_key)
        header_text = f'# {group} Data from {month_name} {year}'
    
        if header_text != current_header:
            st.markdown(header_text)
            current_header = header_text

        #### Display data with {key: value}
        with st.container(border = True):
            st.markdown(f"### {json_detail.get('title', 'Untitled')}")
            col1, col2 = st.columns(2)

            with col1:
                for items in ['author', 'inspire-hep', 'arxiv', 'collaboration', 'time', 'abstract']:
                    st.markdown(f'- **{items.upper()}**: {json_detail.get(items, "N/A")}')
        
            with col2:
                pdf_path = json_detail.get('pdf')
                if pdf_path:
                    # PDF lazy loading optimization: prevents freezing from rendering many PDFs at once
                    # if st.checkbox("Preview PDF", key = f"pdf_{year}_{month_key}_{json_detail.get('title', 'raw')}"):
                        st.pdf(pdf_path, height = 300)
                        
            ##### Show details (Expander)
            with st.expander('View Data'):
                data = json_detail.get('data', [])
                for data_value in data:
                    with st.container(border = True):
                        ###### Show observables
                        data_obs = [value for key, value in data_value.items() if key.startswith("obs@")]
                        data_cor = [key for key in data_value if "correlation" in key.lower()]

                        if data_obs:
                            st.markdown('- **OBSERVABLE**')
                            st.table(data_obs)

                        ###### Show correlations
                        for key in data_cor:
                            try:
                                obs1 = data_value.get("obs@1", {})
                                err_key = key.replace("correlation", "err")
                                err_name = obs1.get(err_key, "Unknown")
                                st.markdown(f'- **{err_name.upper()}-CORRELATION**')
                                st.table(data_value[key])
                            except Exception:
                                pass                            