# ---------------------------------------------------------
# Core dashboard renderer for the flav-data Streamlit app.
#
# Each Experimental/<Lab>-<Collaboration>/<Collaboration>.py
# and Theoretical/<group>/<group>.py file is a thin wrapper that
# loads defs.py (via exec) and then calls run_dashboard(...) with
# the appropriate lab/group/base_path combination.
# ---------------------------------------------------------

# ---------------------------------------------------------
# Load packages and definitions
# ---------------------------------------------------------
with open('defs.py', 'r', encoding='utf-8') as f:
    exec(f.read())


# ---------------------------------------------------------
# Data loading
# ---------------------------------------------------------
def _resolve_folder(lab, group, folder_override=None):
    """Build the on-disk folder name for a group.

    For experimental groups the convention is ``<Lab>-<Collaboration>``
    (e.g. ``CERN-LHCb``). For theoretical groups ``lab`` is empty
    and the bare group name is used (e.g. ``HPQCD``). The optional
    ``folder_override`` lets a group live under a non-standard
    parent directory (currently unused by any registered group).
    """
    if folder_override:
        return folder_override
    return f"{lab}-{group}" if lab else group


@st.cache_data(ttl=3600)
def get_cached_data(lab, group, years, months, _get_json_func, base_path, folder_override=None):
    """Walk the selected years/months and load every JSON entry into memory.

    The leading underscore on ``_get_json_func`` tells Streamlit not
    to try to hash the function object (which it can't pickle). The
    other arguments are immutable values that *can* be hashed, so the
    cache still works correctly.

    Returns
    -------
    list[dict]
        Each entry is the parsed JSON of one paper, with the helper
        keys ``_year`` and ``_month`` injected for downstream sorting.
    """
    data_pool = []
    folder = _resolve_folder(lab, group, folder_override)

    for year in years:
        index_path = fr'{base_path}/{folder}/{year}/{group}@{year}.json'
        try:
            json_index = _get_json_func(index_path)
        except FileNotFoundError:
            continue

        for m_key, item_ids in json_index.items():
            if int(m_key) not in months:
                continue
            for fid in item_ids:
                detail_path = fr'{base_path}/{folder}/{year}/{m_key}/{fid}.json'
                try:
                    detail = _get_json_func(detail_path)
                except FileNotFoundError:
                    continue
                if detail:
                    # Inject metadata for downstream sorting/display
                    detail['_year'] = year
                    detail['_month'] = m_key
                    data_pool.append(detail)

    return data_pool


def detect_years(lab, group, year_min, year_max, _get_json_func, base_path, folder_override=None):
    """Return the list of years that have an annual index file for ``group``.

    ``_get_json_func`` is unhashable to Streamlit (function object);
    the leading underscore disables hashing for this parameter.
    """
    folder = _resolve_folder(lab, group, folder_override)
    years = []
    for year in range(year_min, year_max + 1):
        idx = fr'{base_path}/{folder}/{year}/{group}@{year}.json'
        try:
            _get_json_func(idx)
            years.append(year)
        except FileNotFoundError:
            continue
    return years


# ---------------------------------------------------------
# Dashboard UI
# ---------------------------------------------------------
def run_dashboard(lab, group, year_min, year_max, get_json_func,
                  month_label=None, base_path='Experimental',
                  folder_override=None):
    """Render the full experimental/theoretical dashboard for one group.

    Parameters
    ----------
    lab : str
        Parent institution (e.g. ``"CERN"``, ``"KEK"``, ``"SLAC"``) for
        experimental groups — the on-disk folder is then built as
        ``<lab>-<group>`` (e.g. ``CERN-LHCb``). Pass an empty string
        for theoretical groups whose folder uses the bare group name
        (e.g. ``HPQCD``).
    group : str
        Collaboration / theory group name (e.g. ``"LHCb"``, ``"HPQCD"``).
    year_min, year_max : int
        Inclusive range of years to scan for annual index files.
    get_json_func : callable
        Loader used to read JSON files. Usually ``get_json`` from
        ``defs.py``.
    month_label : dict, optional
        Mapping from zero-padded month string to display label. Falls
        back to the raw key if a month isn't in the mapping.
    base_path : str
        Top-level directory containing the group's data, typically
        ``"Experimental"`` or ``"Theoretical"``.
    folder_override : str, optional
        If given, use this exact folder name under ``base_path``
        instead of building ``<lab>-<group>``. Currently unused
        by any registered group; retained as an escape hatch
        for future non-standard parent directories.
    """
    if month_label is None:
        month_label = {}

    # Detect available years
    exp_year_list = detect_years(lab, group, year_min, year_max,
                                 get_json_func, base_path, folder_override)

    if not exp_year_list:
        folder = _resolve_folder(lab, group, folder_override)
        st.warning(fr"No {group} data found in {base_path}/{folder}/")
        return

    # ---------------------------------------------------------
    # Sidebar: filters + statistics
    # ---------------------------------------------------------
    with st.sidebar:
        st.markdown("# Filters")

        # Year range slider. When only one year has data the slider
        # would reject (min == max) inputs, so fall back to a fixed
        # display instead.
        st.markdown("##### Select Year Range")
        if min(exp_year_list) == max(exp_year_list):
            st.caption(
                f"Only one year available: {min(exp_year_list)}"
            )
            year_range = (min(exp_year_list), max(exp_year_list))
        else:
            year_range = st.slider(
                "Select Year Range",
                min_value=min(exp_year_list),
                max_value=max(exp_year_list),
                value=(min(exp_year_list), max(exp_year_list)),
                step=1,
                label_visibility="collapsed"
            )
        selected_years = list(range(year_range[0], year_range[1] + 1))

        # Month range slider
        st.markdown("##### Select Month Range")
        month_range = st.slider(
            "Select Month Range",
            min_value=1,
            max_value=12,
            value=(1, 12),
            step=1,
            label_visibility="collapsed"
        )
        selected_months = list(range(month_range[0], month_range[1] + 1))

        # One-shot I/O for the whole selected window
        raw_data = get_cached_data(lab, group, selected_years,
                                   selected_months, get_json_func, base_path,
                                   folder_override)

        # Transition-mode filter
        transition_set = {mode.get("transition-mode") for mode in raw_data
                          if "transition-mode" in mode}
        transition_list = sorted(transition_set)

        st.markdown("##### Select Transition Mode")
        # Default to all transition modes selected, so the page
        # actually shows data on first load. Users can untick
        # any mode they want to filter out.
        for t in transition_list:
            st.checkbox(t, value=True, key=f"tx_{t}")
        # Pull the current selection back out of session_state
        # (streamlit reruns the whole script on every interaction,
        # so checkbox state lives there between runs).
        selected_transitions = [
            t for t in transition_list
            if st.session_state.get(f"tx_{t}", True)
        ]

        # Apply the transition-mode filter
        filtered_data = [
            mode for mode in raw_data
            if mode.get('transition-mode') in selected_transitions
        ]

        # Statistics (in-memory, no I/O)
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

    # ---------------------------------------------------------
    # Main content
    # ---------------------------------------------------------
    # Sort newest first
    filtered_data.sort(
        key=lambda x: (x.get('_year', 0), x.get('_month', '00')),
        reverse=True
    )

    # Render in groups keyed by (year, month)
    current_header = ""
    for json_detail in filtered_data:
        year = json_detail.get('_year')
        month_key = json_detail.get('_month')
        month_name = month_label.get(str(month_key), month_key)
        header_text = fr'# {group} Data from {month_name} {year}'

        if header_text != current_header:
            st.markdown(header_text)
            current_header = header_text

        with st.container(border=True):
            st.markdown(fr"### {json_detail.get('title', 'Untitled')}")
            col1, col2 = st.columns([1, 3])

            with col1:
                for items in ['author', 'inspire-hep', 'arxiv',
                              'collaboration', 'time']:
                    st.markdown(
                        fr'- **{items.upper()}**: '
                        fr'{json_detail.get(items, "N/A")}'
                    )

            with col2:
                st.markdown(
                    fr'- **{"abstract".upper()}**: '
                    fr'{json_detail.get("abstract", "N/A")}'
                )

            # Expandable data view
            with st.expander('View Data'):
                data = json_detail.get('data', [])
                for data_value in data:
                    with st.container(border=True):
                        # Observable list (rendered as a table)
                        data_obs = [value for key, value in data_value.items()
                                    if key.startswith("obs@")]
                        if data_obs:
                            st.markdown('- **OBSERVABLE**')
                            st.table(data_obs)

                        # Correlation/covariance matrices
                        data_cor = [key for key in data_value
                                    if "correlation" in key.lower()]
                        for key in data_cor:
                            try:
                                obs1 = data_value.get("obs@1", {})
                                err_key = key.replace("correlation", "err")
                                err_name = obs1.get(err_key, "Unknown")
                                st.markdown(
                                    fr'- **{err_name.upper()}-CORRELATION**'
                                )
                                st.table(data_value[key])
                            except Exception:
                                # Defensive: never let a bad matrix block
                                # the rest of the page
                                pass
