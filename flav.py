# ---------------------------------------------------------
# Core dashboard renderer for the flav-data Streamlit app.
#
# ``main.py`` dispatches every navigable page to one of the
# renderers below; there are no per-group page modules.
# ---------------------------------------------------------

# ---------------------------------------------------------
# Load packages and definitions
# ---------------------------------------------------------
import json
import os

import streamlit as st

try:
    _HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _HERE = os.path.dirname(os.path.abspath('flav.py'))

with open(os.path.join(_HERE, 'defs.py'), 'r', encoding='utf-8') as f:
    exec(f.read())


# ---------------------------------------------------------
# Data loading
# ---------------------------------------------------------
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
    folder = resolve_folder(lab, group, folder_override)

    for year in years:
        index_path = fr'{base_path}/{folder}/{year}/{group}@{year}.json'
        try:
            json_index = _get_json_func(index_path)
        except (FileNotFoundError, json.JSONDecodeError):
            continue
        if not isinstance(json_index, dict):
            continue

        for m_key, item_ids in json_index.items():
            try:
                month = int(m_key)
            except (TypeError, ValueError):
                continue
            if month not in months or not 1 <= month <= 12:
                continue
            if not isinstance(item_ids, list):
                continue
            for fid in item_ids:
                detail = None
                for detail_path in (
                    fr'{base_path}/{folder}/{year}/{m_key}/{fid}.json',
                    fr'{base_path}/{folder}/{year}/{fid}.json',
                ):
                    try:
                        detail = _get_json_func(detail_path)
                        break
                    except (FileNotFoundError, json.JSONDecodeError):
                        continue
                if not detail:
                    continue
                # Inject metadata for downstream sorting/display
                detail['_year'] = year
                detail['_month'] = m_key
                data_pool.append(detail)

    return data_pool


@st.cache_data(ttl=300)
def detect_years(lab, group, year_min, year_max, _get_json_func, base_path, folder_override=None):
    """Return the list of years that have an annual index file for ``group``.

    ``_get_json_func`` is unhashable to Streamlit (function object);
    the leading underscore disables hashing for this parameter.
    """
    folder = resolve_folder(lab, group, folder_override)
    years = []
    for year in range(year_min, year_max + 1):
        idx = os.path.join(base_path, folder, str(year), f'{group}@{year}.json')
        if os.path.isfile(idx):
            years.append(year)
    return years


# ---------------------------------------------------------
# Dashboard UI
# ---------------------------------------------------------
def iter_data_groups(data):
    """Yield the data groups of a paper.

    ``data`` is an array of groups; each group maps one or more
    transition channels to ``obs@N`` objects and may carry a group-level
    correlation/covariance matrix.
    """
    if not isinstance(data, list):
        return
    for group in data:
        if isinstance(group, dict):
            yield group


def is_matrix_key(key):
    return key.endswith(('correlation', 'covariance'))


def matrix_label(key, group):
    """Return a display label for a group-level matrix key."""
    kind = 'COVARIANCE' if key.endswith('covariance') else 'CORRELATION'
    if not key.startswith('type@'):
        return f'TOTAL-{kind}'
    prefix = key.split('_', 1)[0]
    for channel in group.values():
        if not isinstance(channel, dict):
            continue
        for obs in channel.values():
            if isinstance(obs, dict) and f'{prefix}_error' in obs:
                return f'{str(obs[f"{prefix}_error"]).upper()}-{kind}'
    return key


def run_dashboard(lab, group, year_min, year_max, get_json_func,
                  month_label=None, base_path='expe-data',
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
        ``"expe-data"`` or ``"theo-data"``.
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
        folder = resolve_folder(lab, group, folder_override)
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
        selected_years = [
            year for year in exp_year_list
            if year_range[0] <= year <= year_range[1]
        ]

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

        # Apply the transition-mode filter. Entries without a
        # transition-mode are shown rather than silently dropped.
        filtered_data = [
            mode for mode in raw_data
            if mode.get('transition-mode') in selected_transitions
            or 'transition-mode' not in mode
        ]

        # Statistics (in-memory, no I/O)
        st.markdown("# Statistics")
        tot_exp = len(filtered_data)
        tot_obs = sum(
            sum(1 for k in channel if k.startswith("obs@"))
            for mode in filtered_data
            for group in iter_data_groups(mode.get('data', []))
            for key, channel in group.items()
            if not is_matrix_key(key) and isinstance(channel, dict)
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
    for paper_index, json_detail in enumerate(filtered_data):
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
            expander = st.expander(
                'View Data', on_change='rerun',
                key=(
                    f"view_data_{group}_{paper_index}_"
                    f"{json_detail.get('inspire-hep', json_detail.get('arxiv', json_detail.get('title', 'untitled')))}"
                )
            )
            if expander.open:
                with expander:
                    data = json_detail.get('data', [])
                    for data_group in iter_data_groups(data):
                        with st.container(border=True):
                            for meta_key in ('dataset', 'scheme'):
                                if data_group.get(meta_key):
                                    st.markdown(
                                        '- **{}**: {}'.format(
                                            meta_key.upper(),
                                            data_group[meta_key],
                                        )
                                    )
                            for channel, obs_bundle in data_group.items():
                                if is_matrix_key(channel):
                                    continue
                                if not isinstance(obs_bundle, dict) or not obs_bundle:
                                    continue
                                st.markdown(
                                    '- **{}**'.format(channel.replace('*', r'\*'))
                                )
                                data_obs = [
                                    value for key, value in obs_bundle.items()
                                    if key.startswith("obs@")
                                ]
                                if data_obs:
                                    st.markdown('- **OBSERVABLE**')
                                    st.table(data_obs)

                            for key, matrix in data_group.items():
                                if not is_matrix_key(key) or matrix is None:
                                    continue
                                st.markdown(
                                    fr'- **{matrix_label(key, data_group)}**'
                                )
                                st.table(matrix)


# ---------------------------------------------------------
# Snapshot dashboards (HFLAV / PDG non-standard schemas)
# ---------------------------------------------------------
def _latest_snapshot(base_dir, group):
    """Return ``(year, path)`` for the newest ``group@year.json``."""
    if not os.path.isdir(base_dir):
        return None
    candidates = []
    for entry in os.listdir(base_dir):
        path = os.path.join(base_dir, entry)
        if entry.isdigit() and len(entry) == 4:
            year = entry
            candidate = os.path.join(path, f'{group}@{year}.json')
        elif entry.startswith(f'{group}@') and entry.endswith('.json'):
            year = entry[len(group) + 1:-len('.json')]
            candidate = path
        else:
            continue
        if year.isdigit() and len(year) == 4 and os.path.isfile(candidate):
            candidates.append((year, candidate))
    return max(candidates) if candidates else None


def run_snapshot_dashboard(group, get_json_func, base_path='expe-data'):
    """Render the latest HFLAV or PDG snapshot."""
    base_dir = os.path.join(base_path, group)
    found = _latest_snapshot(base_dir, group)
    if not found:
        st.warning(f"No {group} data found in {base_dir}/")
        return

    year, path = found
    try:
        doc = get_json_func(path)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        st.error(f"Failed to load {path}: {exc}")
        return

    if group == 'HFLAV':
        st.title("HFLAV — Heavy Flavor Averaging Group")
        st.markdown(
            "**World-average heavy-flavor measurements from the HFLAV "
            "review (`inspire-hep = HeavyFlavorAveragingGroupHFLAV:2024ctg`).**"
        )
        st.caption(f"Snapshot year: {year}")
        subgroups = [key for key in doc if key.startswith('HFLAV@')]
        if not subgroups:
            st.warning("No HFLAV subgroups found in this snapshot.")
            return
        with st.sidebar:
            st.markdown("# Filters")
            st.markdown("##### HFLAV Subgroup")
            subgroup = st.selectbox(
                "HFLAV Subgroup", subgroups, label_visibility="collapsed",
            )
        subgroup_data = doc.get(subgroup, {})
        st.subheader(subgroup)
        col1, col2 = st.columns([1, 2])
        with col1:
            for key, value in subgroup_data.items():
                if key != 'observables':
                    st.markdown(f"- **{key.upper()}**: {value}")
        with col2:
            observables = subgroup_data.get('observables', [])
            if observables:
                st.markdown(f"**{len(observables)} observables**")
                st.table(observables)
            else:
                st.info("No observables in this subgroup.")
        correlation = subgroup_data.get('correlation')
        if correlation:
            expander = st.expander(
                "View Correlation", on_change='rerun',
                key=f"hflav_correlation_{subgroup}",
            )
            if expander.open:
                with expander:
                    st.table(correlation)
        return

    st.title("PDG — Particle Data Group")
    st.markdown(
        "**World-average particle properties from the PDG review "
        "(`inspire-hep = ParticleDataGroup:2024cfk`).**"
    )
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"- **YEAR**: {year}")
        st.markdown(f"- **INSPIRE-HEP**: {doc.get('inspire-hep', 'N/A')}")
        st.markdown(f"- **AUTHOR**: {doc.get('author', 'N/A')}")
    with col2:
        st.markdown(f"- **TITLE**: {doc.get('title', 'N/A')}")
        abstract = doc.get('abstract', 'N/A')
        if isinstance(abstract, str) and len(abstract) > 800:
            abstract = abstract[:800] + "..."
        st.markdown(f"- **ABSTRACT**: {abstract}")
    st.divider()

    data = doc.get('data', {})
    if not data:
        st.warning("No subgroup data found in this PDG snapshot.")
        return
    with st.sidebar:
        st.markdown("# Filters")
        st.markdown("##### PDG Subgroup")
        subgroup = st.selectbox(
            "PDG Subgroup", list(data), label_visibility="collapsed",
        )
    st.subheader(subgroup)
    subgroup_data = data[subgroup]
    rows = [
        {"key": key, **value}
        for key, value in subgroup_data.items()
        if key.startswith('obs@')
    ]
    if rows:
        st.table(rows)
    else:
        st.info("No obs@N entries in this subgroup.")

    correlation = subgroup_data.get('correlation')
    if correlation is not None:
        st.markdown("**Correlation matrix**")
        st.table(correlation)
