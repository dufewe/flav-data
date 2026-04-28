# Load packages and definitions
with open('defs.py', 'r', encoding='utf-8') as f:
    exec(f.read())

# Specify experimental collaboration
exp_group = "LHCb"

# Find exp data year
exp_year_list = []
for year in range(year_min,year_max+1):
    try:
        get_json(f'Experimental/{exp_group}/{year}/{exp_group}@{year}.json')
        exp_year_list.append(year)
    except FileNotFoundError:
        continue

# Sidebar settings
with st.sidebar:
    ## Filters
    st.markdown("# Filters")

    ### Year filter
    st.markdown("##### Select Year Range")
    year_range = st.slider(
        "Select Year Range",
        min_value = min(exp_year_list),
        max_value = max(exp_year_list),
        value = (min(exp_year_list), max(exp_year_list)),
        step=1,
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
        step=1,
        label_visibility = "collapsed"
    )
    selected_months = list(range(month_range[0], month_range[1] + 1))
    
    ### Transition filter
    transition_list = []
    for year in selected_years:
        try:
            json_index = get_json(f'Experimental/{exp_group}/{year}/{exp_group}@{year}.json')
        except FileNotFoundError:
            continue
        for index_key, index_value in json_index.items():
            if int(index_key) in selected_months:
                for item_index in index_value:
                    json_detail = get_json(f'Experimental/{exp_group}/{year}/{index_key}/{item_index}.json')
                    if json_detail["transition-mode"] not in transition_list:
                        transition_list.append(json_detail["transition-mode"])
    transition_list.sort()
    st.markdown("##### Select Transition Mode")
    selected_transitions = []
    for trans in transition_list:
        if st.checkbox(trans):
            selected_transitions.append(trans)
        
    ## Statistics
    st.markdown("# Statistics")

    tot_exp, tot_obs = 0, 0
    for year in selected_years:
        try:
            json_index = get_json(f'Experimental/{exp_group}/{year}/{exp_group}@{year}.json')
        except FileNotFoundError:
            continue
        for index_key, index_value in json_index.items():
            if int(index_key) in selected_months:
                for item_index in index_value:
                    json_detail = get_json(f'Experimental/{exp_group}/{year}/{index_key}/{item_index}.json')
                    data = json_detail['data']
                    if json_detail['transition-mode'] in selected_transitions:
                        tot_exp += 1
                        for data_index, data_value in enumerate(data):
                            data_obs = []
                            for i in range(1,len(data_value)+1):
                                try:
                                    data_obs.append(data_value[f"obs@{i}"])
                                except KeyError:
                                    continue
                            tot_obs += len(data_obs)
    st.markdown("##### Total Experiments")
    st.metric("Total Experiments", tot_exp, label_visibility = "collapsed")
    st.markdown("##### Total Observables")
    st.metric("Total Observables", tot_obs, label_visibility = "collapsed")
        
# Display exp data through year
for year in selected_years:
    ## get json-index file at {year}
    try:
        json_index = get_json(f'Experimental/{exp_group}/{year}/{exp_group}@{year}.json')
    except FileNotFoundError:
        continue

    ## specify data with selected properties
    for index_key, index_value in json_index.items():
        if int(index_key) in selected_months:
            st.markdown(f'# {exp_group} data from {month_label[index_key]} {year}')
            for item_index in index_value:  
                json_detail = get_json(f'Experimental/{exp_group}/{year}/{index_key}/{item_index}.json')
                data = json_detail['data']
                if json_detail['transition-mode'] in selected_transitions:

                    ## display data with {key: value}
                    with st.container(border=True):
                        st.markdown(f"### {json_detail['title']}")
                        col1, col2 = st.columns(2)
                        with col1:
                            for items in ['author','inspire-hep','arxiv','collaboration','time','abstract']:
                                st.markdown(f'- {items.upper()}: {json_detail[items]}')
                        with col2:
                            st.pdf(f"{json_detail['pdf']}",height=300)

                        ## show details
                        with st.expander('see data'):
                            for data_index, data_value in enumerate(data):
                                with st.container(border=True):

                                    ## show observables
                                    data_obs = []
                                    data_cor = []
                                    for key, value in data_value.items():
                                        try:
                                            if int(key.replace("obs@","")) % 1 == 0:
                                                data_obs.append(value)
                                        except ValueError:
                                            data_cor.append(key)
                                    st.markdown('- OBSERVABLE:')
                                    st.table(data_obs)

                                    ## show correlations
                                    for key in data_cor:
                                        err_name = data_value["obs@1"][key.replace("correlation","err")]
                                        st.markdown(f'- {err_name.upper()}-CORRELATION:')
                                        st.table(data_value[key])
