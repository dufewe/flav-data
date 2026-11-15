#!/usr/bin/env python3
"""Validate flav-data JSON files against the schema in references/json-meta.md.

Usage:
    python3 json-valid.py <path/to/file.json> [path/to/file2.json ...] [--quiet]
"""

import json
import math
import re
import sys
import os
import argparse

REQUIRED_TOP_FIELDS = [
    'inspire-hep', 'author', 'title',
    'arxiv', 'time', 'abstract', 'transition-mode', 'data'
]

# ``collaboration`` is required only for named collaborations (experiments
# and large theory groups). Individual/small-group papers omit it entirely.
CONDITIONAL_TOP_FIELDS = ['collaboration']

# Fields that must NOT appear in a per-paper JSON. The publication year
# is the directory name, not a field.
FORBIDDEN_FIELDS = ['year', 'pdf']

# Standard measurement error labels (json-meta.md §"Standard error type
# labels"). Labels outside this set are rejected; a ``theo`` component may
# append the theoretical input it comes from (``theo:mu_pi``).
STANDARD_ERROR_LABELS = {
    'stat', 'syst', 'lumi', 'norm', 'theo', 'expe',
}
THEO_SOURCE_LABEL_RE = re.compile(r'theo:[a-z0-9_]+')

# Per-paper observable fields. ``type@N_*`` keys are matched by pattern;
# everything else must match exactly.
OBS_EXACT_FIELDS = {
    'name', 'value', 'unit', 'ref',
    'total_upper', 'total_lower',
    # Optional provenance metadata carried over from imported papers.
    'dataset', 'note',
}
_OBS_KEY_RE = re.compile(
    r'type@\d+_(?:error|upper|lower|level)$'
)
_NUMERIC_OBS_KEY_RE = re.compile(
    r'(?:value|type@\d+_(?:upper|lower)|total_upper|total_lower)$'
)
_UNIT_RE = re.compile(r'[A-Za-z]{1,4}(?:-?\d+)?')


def is_observable_field(key: str) -> bool:
    return (
        key in OBS_EXACT_FIELDS
        or key in DATA_ENTRY_KINEMATIC_FIELDS
        or bool(_OBS_KEY_RE.fullmatch(key))
    )

# transition-mode whitelist (json-meta.md §"transition-mode Values" table)
VALID_TRANSITION_MODES = [
    'leptonic-decay',
    'semileptonic-decay',
    'non-leptonic-decay',
    'radiative-decay',
    'neutron-beta-decay',
    'higgs-decay',
    'mixing',
    'scattering',
    'electroweak-precision',
    'w-production',
    'higgs-production',
    'low-energy',
    'oblique-corrections',
    'world-average',
]

# Top-level fields allowed in the schema.
TOP_LEVEL_ALLOWED_FIELDS = set(REQUIRED_TOP_FIELDS) | set(CONDITIONAL_TOP_FIELDS)

# Kinematic boundary fields, valid inside an ``obs@N`` object.
DATA_ENTRY_KINEMATIC_FIELDS = {
    'q2min', 'q2max', 'emin', 'emax', 'pTmin', 'pTmax', 'etamin', 'etamax',
    # Additional kinematic boundaries used by existing measurements.
    'w_min', 'w_max', 'cos_min', 'cos_max',
    'chi_min', 'chi_max', 'mxs_min', 'mxs_max',
}
# Group-level matrices sit alongside the channel keys. ``correlation`` /
# ``covariance`` describe the total uncertainty; the ``type@N_`` prefix
# optionally marks a component-error matrix (e.g. statistical only).
_GROUP_MATRIX_KEY_RE = re.compile(
    r'(?:type@\d+_)?(?:correlation|covariance)$'
)


def is_group_matrix_key(key: str) -> bool:
    return bool(_GROUP_MATRIX_KEY_RE.fullmatch(key))


# Form-factor expansion coefficients (``aN_FF``) come from a fit to a
# named expansion form, recorded once per data group.  The ``+`` in
# symbols such as ``f+``/``F+``/``G+`` is part of the form-factor name.
_FORM_FACTOR_COEFFICIENT_RE = re.compile(r"a\d+_[A-Za-z0-9+']+")
# Obsolete fraction spellings; the plus charge is written explicitly.
_DEPRECATED_FORM_FACTOR_NAMES = {
    'fp': 'f+', 'Fp': 'F+', 'Gp': 'G+', 'hp': 'h+', 'htp': 'ht+',
}
# LFU-difference Q notation (the papers' Q_i / Q_FL) is stored as the
# unified Delta form; see references/observable-naming.md §"LFU Difference
# Observables" for the correspondence.
_DEPRECATED_LFU_Q_NAMES = {
    'Q1': 'DeltaP1', 'Q2': 'DeltaP2', 'Q3': 'DeltaP3',
    'Q4': 'DeltaP4p', 'Q5': 'DeltaP5p', 'Q6': 'DeltaP6p',
    'Q8': 'DeltaP8p', 'QFL': 'DeltaFL',
}
# Single-token mass shortcuts; the argument form takes the PDG particle
# label (references/observable-naming.md §2.1).
_DEPRECATED_MASS_NAMES = {
    'MZ': 'Mass(Z)', 'MW': 'Mass(W)', 'Mtop': 'Mass(t)',
    'MH': 'Mass(H)', 'Mh': 'Mass(H)',
}
FORM_FACTOR_SCHEMES = {'BK', 'BGL', 'BCL', 'BSZ', 'DLM', 'MR'}

# Group-level ``dataset`` names the data sources behind a group, in this
# canonical order, joined with ``+`` (e.g. ``LQCD+LCSR``).
DATASET_SOURCES = ('LQCD', 'LCSR', 'QCDSR', 'EXPE')


def _dataset_issue(value) -> str:
    """Return an error message for an invalid ``dataset`` value."""
    if not isinstance(value, str) or not value.strip():
        return "must be a non-empty string"
    parts = value.split('+')
    if any(part not in DATASET_SOURCES for part in parts):
        return (
            f"unsupported source in {value!r}; use sources from: "
            f"{', '.join(DATASET_SOURCES)}"
        )
    if len(set(parts)) != len(parts):
        return f"duplicate source in {value!r}"
    ranks = [DATASET_SOURCES.index(part) for part in parts]
    if ranks != sorted(ranks):
        return (
            f"sources in {value!r} must follow the order "
            f"{'+'.join(DATASET_SOURCES)}"
        )
    return ""


# --- Particle registry and transition ordering (particle-naming.md) ----------
# The registry tables in references/particle-naming.md are the single
# source of pids, masses and charges. A table with ``pid`` and ``mass``
# columns registers orderable states; a ``pid`` table without ``mass``
# (exotics) or a ``token`` table (placeholders) registers non-orderable
# tokens.
_TYPE_NAMES = {
    1: 'baryon', 2: 'meson', 3: 'charged lepton', 4: 'neutral lepton',
}
_CHARGED_LEPTON_CORES = {'e', 'E', 'mu', 'MU', 'tau', 'TAU'}
_NEUTRAL_LEPTON_CORES = {'ve', 'VE', 'vmu', 'VMU', 'vtau', 'VTAU'}


def _load_registry() -> tuple[
    dict[str, tuple[float, int | None]], set[str], set[str]
]:
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, '..', 'references', 'particle-naming.md')
    with open(os.path.abspath(path), 'r', encoding='utf-8') as handle:
        lines = handle.readlines()

    states: dict[str, tuple[float, int | None]] = {}
    non_orderable: set[str] = set()
    fundamental: set[str] = set()

    def backticked(cell: str) -> list[str]:
        return re.findall(r'`([^`]+)`', cell)

    def cells(row: str) -> list[str]:
        return [part.strip() for part in row.strip().strip('|').split('|')]

    def charge(cell: str) -> int | None:
        try:
            return int(cell.strip().strip('$'))
        except ValueError:
            return None

    index = 0
    while index < len(lines):
        if not lines[index].strip().startswith('|'):
            index += 1
            continue
        block = []
        while index < len(lines) and lines[index].strip().startswith('|'):
            block.append(lines[index].strip())
            index += 1
        if len(block) < 3:
            continue
        header = [cell.lower() for cell in cells(block[0])]
        if 'token' in header:
            column = header.index('token')
            for row in block[2:]:
                non_orderable.update(backticked(cells(row)[column]))
            continue
        if 'pid' not in header:
            continue
        pid_column = header.index('pid')
        anti_column = (
            header.index('antiparticle pid')
            if 'antiparticle pid' in header else None
        )
        mass_column = header.index('mass') if 'mass' in header else None
        charge_column = header.index('q') if 'q' in header else None
        for row in block[2:]:
            row_cells = cells(row)
            pids = backticked(row_cells[pid_column])
            if not pids:
                continue
            if mass_column is None:
                non_orderable.update(pids)
                continue
            try:
                mass = float(row_cells[mass_column])
            except ValueError:
                non_orderable.update(pids)
                continue
            q = (
                charge(row_cells[charge_column])
                if charge_column is not None else None
            )
            for pid in pids:
                states[pid] = (mass, q)
            if anti_column is not None:
                anti_pids = backticked(row_cells[anti_column])
                fundamental.update(pids)
                fundamental.update(anti_pids)
                for anti_pid in anti_pids:
                    states[anti_pid] = (mass, -q if q is not None else None)

    if not states:
        raise RuntimeError(
            f'{path}: no registry tables with pid and mass columns'
        )
    return states, non_orderable, fundamental


_REGISTRY, _NON_ORDERABLE, _FUNDAMENTAL_PIDS = _load_registry()


def _charge_rank(charge_value: int | None) -> int | None:
    """Map a charge to the equal-mass order: + -> 0, - -> 1, 0 -> 2."""
    return {1: 0, -1: 1, 0: 2}.get(charge_value)


def _particle_meta(token: str) -> tuple[int | None, int | None, float | None]:
    """Return ``(type_rank, charge_rank, mass)`` for a registered pid."""
    entry = _REGISTRY.get(token)
    if entry is None:
        return None, None, None
    mass, q = entry
    core = token.split('_', 1)[0]
    if token in _FUNDAMENTAL_PIDS:
        if core in _CHARGED_LEPTON_CORES:
            type_rank = 3
        elif core in _NEUTRAL_LEPTON_CORES:
            type_rank = 4
        else:
            type_rank = None
    elif token.startswith('n~') or core == 'x':
        type_rank = None
    elif len(core) == 2:
        type_rank = 2
    elif len(core) == 3:
        type_rank = 1
    else:
        type_rank = None
    return type_rank, _charge_rank(q), mass


def _parenthetical_blocks(name: str) -> list[tuple[int, int, str]]:
    """Return outer-level ``(...)`` blocks as ``(start, end, body)``.

    Parentheses inside a ``[...]`` condition are ignored, and nested
    parentheses are part of the enclosing block's body.
    """
    blocks = []
    index = 0
    bracket_depth = 0
    while index < len(name):
        char = name[index]
        if char == '[':
            bracket_depth += 1
        elif char == ']':
            bracket_depth = max(0, bracket_depth - 1)
        elif char == '(' and bracket_depth == 0:
            depth = 1
            end = index + 1
            while end < len(name) and depth:
                if name[end] == '(':
                    depth += 1
                elif name[end] == ')':
                    depth -= 1
                end += 1
            if depth == 0:
                blocks.append((index, end, name[index + 1:end - 1]))
                index = end
                continue
        index += 1
    return blocks


def _looks_like_transition(text: str) -> bool:
    """Heuristic: does ``text`` contain a particle transition?"""
    return '.2.' in text


def validate_transition_key(key: str) -> list[str]:
    """Validate a bare transition used as a ``data`` dictionary key."""
    if key == 'no-transition':
        return []
    if '.2.' not in key:
        return [
            f"  data key '{key}' is not a transition channel; expected "
            f"<pid>.<pid>.2.<pid>.<pid> (or 'no-transition' for "
            f"observables without one)"
        ]
    if any(
        not stage.replace('.', '')
        for part in key.split('/')
        for stage in part.split('.2.')
    ):
        return [
            f"  data key '{key}': empty particle state; every stage separated "
            f"by '.2.' must name at least one pid"
        ]
    issues = _order_issues_for_body(key, f"data key '{key}'")
    issues.extend(_flow_issues(key, f"data key '{key}'"))
    return issues


# An anti-b meson decays through anti-b -> anti-c/anti-s, so its inclusive
# system is barred; a b meson decays through b -> c/s and takes the
# unbarred token. The charge-averaged ``B`` and ``Xu`` carry no flavour
# constraint.
_B_QUARK_CONTENT = {
    'uB': 'bar', 'dB': 'bar', 'sB': 'bar', 'cB': 'bar',
    'Ub': 'quark', 'Db': 'quark', 'Sb': 'quark', 'Cb': 'quark',
}
_INCLUSIVE_FLAVOUR = {
    'Xc': 'quark', 'XcBar': 'bar', 'Xs': 'quark', 'XsBar': 'bar',
}
_LEPTON_CHARGE = {
    'e': -1, 'mu': -1, 'tau': -1, 'l-': -1,
    'E': 1, 'MU': 1, 'TAU': 1, 'l+': 1,
}
# Neutrino token -> (charged-lepton flavour, partner lepton charge). A
# neutrino accompanies l+, an antineutrino accompanies l-; ``None`` is the
# flavour-unspecified generic token.
_NEUTRINO_PARTNER = {
    'v': (None, 1), 'vBar': (None, -1),
    've': ('e', 1), 'VE': ('e', -1),
    'vmu': ('mu', 1), 'VMU': ('mu', -1),
    'vtau': ('tau', 1), 'VTAU': ('tau', -1),
}
_NEUTRINO_TOKEN = {
    partner: token for token, partner in _NEUTRINO_PARTNER.items()
}


def _flow_issues(key: str, label: str) -> list[str]:
    """Check quark-flavour flow and lepton/neutrino charge correlation.

    Only the final state of each transition is inspected. Scattering (a
    neutrino already in the initial state), exotic ``x_`` cascades and the
    flavour-ambiguous ``l`` are left alone.
    """
    issues = []
    for part in key.split('/'):
        stages = [
            [token for token in stage.split('.') if token]
            for stage in part.split('.2.')
        ]
        if len(stages) < 2:
            continue
        initial, final = stages[0], stages[-1]
        cores = [token.split('_', 1)[0] for token in final]
        label_part = f"{label} state '{'.'.join(final)}'"

        wanted = _B_QUARK_CONTENT.get(initial[0].split('_', 1)[0])
        if wanted:
            for core in cores:
                if _INCLUSIVE_FLAVOUR.get(core) not in (None, wanted):
                    expected = core[:-3] if wanted == 'quark' else core + 'Bar'
                    quark = 'a b' if wanted == 'quark' else 'an anti-b'
                    issues.append(
                        f"  {label_part}: '{initial[0]}' decays through "
                        f"{quark} quark, so "
                        f"the inclusive system is '{expected}', not '{core}'"
                    )

        if any(token.startswith('x_') for token in part.split('.')):
            continue
        if any(
            token.split('_', 1)[0] in _NEUTRINO_PARTNER
            for stage in stages[:-1] for token in stage
        ):
            continue
        leptons = [core for core in cores if core in _LEPTON_CHARGE]
        neutrinos = [core for core in cores if core in _NEUTRINO_PARTNER]
        if len(leptons) != 1 or len(neutrinos) != 1 or leptons[0] == 'l':
            continue
        lepton, neutrino = leptons[0], neutrinos[0]
        flavour, charge = _NEUTRINO_PARTNER[neutrino]
        if flavour is not None and flavour != lepton.lower():
            issues.append(
                f"  {label_part}: neutrino '{neutrino}' does not match the "
                f"charged lepton '{lepton}'"
            )
        elif charge != _LEPTON_CHARGE[lepton]:
            expected = _NEUTRINO_TOKEN[(flavour, _LEPTON_CHARGE[lepton])]
            issues.append(
                f"  {label_part}: '{lepton}' must be accompanied by "
                f"'{expected}', not '{neutrino}'"
            )
    return issues


def _order_issues_for_body(body: str, label: str) -> list[str]:
    """Check one transition body and return order/registry issues.

    Every particle token must be a pid registered in
    ``references/particle-naming.md`` or a placeholder listed there as
    non-orderable; otherwise the state would silently escape the checks.
    """
    issues = []
    parts = [part for part in body.split('/') if part]
    if len(parts) > 1 and all('.2.' in part for part in parts):
        for part in parts:
            issues.extend(_order_issues_for_body(part, label))
        return issues
    for stage in body.split('.2.'):
        tokens = [token for token in stage.split('.') if token]
        classified = [_particle_meta(token) for token in tokens]
        types = [entry[0] for entry in classified]
        charges = [entry[1] for entry in classified]
        masses = [entry[2] for entry in classified]

        for token in tokens:
            if token in _NON_ORDERABLE or token in _REGISTRY:
                continue
            issues.append(
                f"  {label}: state '{stage}' particle '{token}' is not a "
                f"registered pid; add it to the registry tables of "
                f"references/particle-naming.md (or list it as non-orderable "
                f"if it cannot be ordered)"
            )

        if all(value is not None for value in types):
            for left in range(len(types) - 1):
                if types[left] > types[left + 1]:
                    expected = '.'.join(
                        token for token, _, _, _ in sorted(
                            zip(tokens, types, charges, masses),
                            key=lambda item: (
                                item[1],
                                -item[3] if item[3] is not None else float('inf'),
                                item[2] if item[2] is not None else 2,
                            ),
                        )
                    )
                    issues.append(
                        f"  {label}: state '{stage}' orders "
                        f"{_TYPE_NAMES[types[left]]} before "
                        f"{_TYPE_NAMES[types[left + 1]]}; expected '{expected}' "
                        f"(baryon -> meson -> charged lepton -> neutral lepton)"
                    )
                    break
            else:
                left = None
            if left is not None:
                continue

        index = 0
        while index < len(classified):
            end = index + 1
            while end < len(classified) and classified[end][0] == classified[index][0]:
                end += 1
            group_tokens = tokens[index:end]
            group_charges = charges[index:end]
            group_masses = masses[index:end]

            mass_problem = False
            if all(mass is not None for mass in group_masses):
                for pos in range(len(group_masses) - 1):
                    if group_masses[pos] + 1e-9 < group_masses[pos + 1]:
                        expected = '.'.join(
                            token for _, token, _ in sorted(
                                zip(group_charges, group_tokens, group_masses),
                                key=lambda item: (
                                    -item[2],
                                    item[0] if item[0] is not None else 2,
                                ),
                            )
                        )
                        issues.append(
                            f"  {label}: state '{stage}' orders "
                            f"'{'.'.join(group_tokens)}' light to heavy; "
                            f"expected '{expected}' (heaviest -> lightest "
                            f"within one particle type)"
                        )
                        mass_problem = True
                        break
            if mass_problem:
                index = end
                continue

            if all(charge is not None for charge in group_charges):
                for pos in range(len(group_masses) - 1):
                    if (
                        group_masses[pos] is not None
                        and group_masses[pos + 1] is not None
                        and abs(group_masses[pos] - group_masses[pos + 1]) < 1e-9
                        and group_charges[pos] > group_charges[pos + 1]
                    ):
                        expected = '.'.join(
                            token for _, token in sorted(
                                zip(group_charges, group_tokens),
                                key=lambda item: item[0],
                            )
                        )
                        issues.append(
                            f"  {label}: state '{stage}' breaks "
                            f"charge order in '{'.'.join(group_tokens)}'; "
                            f"expected '{expected}' "
                            f"(equal masses: + -> - -> 0)"
                        )
                        break
            index = end
    return issues


def _observable_symbol(name: str) -> str:
    """Return the bare symbol, dropping a ``[condition]``/``(parameter)`` tag."""
    return re.split(r'[\[(]', name, maxsplit=1)[0]


# A condition may qualify the measurement (confidence level, model, data
# set) but never a kinematic bin: those live in q2min/q2max, emin/emax or
# the group note. ``=`` is deliberately not matched, so parameter tags
# such as ``mH=125GeV`` survive.
_KINEMATIC_CONDITION_RE = re.compile(
    r'[<>]|q2|^\d+(?:\.\d+)?[,-]\d+(?:\.\d+)?$', re.IGNORECASE
)
# Lepton-flavour ratios of rates are named ``R``; the two transitions are
# the key. Ratios of other observables keep ``ROBS[condition]``.
_LEPTON_FLAVOUR_RATIO_RE = re.compile(
    r'^(?:e|mu|tau|l)\s*/\s*(?:e|mu|tau|l)$', re.IGNORECASE
)
_RATE_SYMBOLS = {'Br', 'Gamma', 'dBr/dq2', 'dGamma/dq2'}
_DEPRECATED_RATIO_NAMES = {
    'RK': 'R', 'RK*': 'R', 'RK+': 'R', 'RD': 'R', 'RD*': 'R',
    'Rmue': 'R', 'Rtaumu': 'R', 'Re/mu': 'R', 'RWenu2Wmumu': 'R',
}


def validate_observable_name(name: str) -> list[str]:
    """Check that the observable name does not embed a transition channel.

    The channel is carried by the ``data`` key. Names are the observable
    symbol, optionally followed by a condition or a parameter tag:
    ``OBS``, ``OBS[condition]``, ``OBS(parameter)``, ``f+.Vcs``.
    """
    issues = []
    symbol = _observable_symbol(name)
    match = re.fullmatch(r'a\d+_([A-Za-z0-9]+)', symbol)
    if match and match.group(1) in _DEPRECATED_FORM_FACTOR_NAMES:
        issues.append(
            f"  Observable '{name}': obsolete form-factor symbol "
            f"'{match.group(1)}'; write "
            f"'{_DEPRECATED_FORM_FACTOR_NAMES[match.group(1)]}' instead"
        )
    if symbol in _DEPRECATED_LFU_Q_NAMES:
        issues.append(
            f"  Observable '{name}': obsolete LFU-difference symbol "
            f"'{symbol}'; write '{_DEPRECATED_LFU_Q_NAMES[symbol]}' instead"
        )
    if symbol in _DEPRECATED_MASS_NAMES:
        issues.append(
            f"  Observable '{name}': obsolete mass shortcut '{symbol}'; write "
            f"'{_DEPRECATED_MASS_NAMES[symbol]}' instead"
        )
    if symbol in _DEPRECATED_RATIO_NAMES:
        issues.append(
            f"  Observable '{name}': ratio symbol '{symbol}' embeds the "
            f"channel; write '{_DEPRECATED_RATIO_NAMES[symbol]}' and put both "
            f"transitions in the data key"
        )
    for condition in re.findall(r'\[([^\]]*)\]', name):
        if _KINEMATIC_CONDITION_RE.search(condition):
            issues.append(
                f"  Observable '{name}': condition '[{condition}]' is a "
                f"kinematic bin; use q2min/q2max or emin/emax, or record the "
                f"window in the group note"
            )
        if _LEPTON_FLAVOUR_RATIO_RE.fullmatch(condition.strip()):
            base = symbol[1:] if symbol.startswith('R') else symbol
            if base in _RATE_SYMBOLS or not symbol.startswith(('R', 'Delta')):
                issues.append(
                    f"  Observable '{name}': a lepton-flavour ratio of rates "
                    f"is named 'R' (or 'DeltaOBS' for a difference); the data "
                    f"key carries both transitions"
                )
    for _, _, body in _parenthetical_blocks(name):
        if _looks_like_transition(body):
            issues.append(
                f"  Observable '{name}': name must not embed the transition "
                f"channel ('{body}'); the data key already carries it"
            )
    return issues


def validate_latex(text: str, field_name: str, obs_key: str) -> list[str]:
    """Check that the LaTeX field is non-empty and Unicode-free.

    Per SKILL.md rule 4 and json-meta.md §"Key Constraints",
    every non-ASCII character must be replaced by its LaTeX equivalent
    before writing the JSON. This deliberately flags *all* non-ASCII
    characters rather than a hand-maintained blocklist; scripts/common.py
    holds the canonical Unicode→LaTeX mapping.
    """
    issues = []
    if not text or not text.strip():
        issues.append(f"  {obs_key}.{field_name}: LaTeX field is empty")
        return issues

    found = sorted({c for c in text if ord(c) > 127})
    if found:
        chars = ', '.join(f'{c!r} (U+{ord(c):04X})' for c in found)
        issues.append(
            f"  {obs_key}.{field_name}: non-ASCII chars not converted to LaTeX "
            f"({chars}); see SKILL.md rule 4 (No Unicode) and "
            f"scripts/common.py for the mapping"
        )
    return issues


def _field_number(value):
    """Parse a numeric observable field (number or float-string) to float."""
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value) if math.isfinite(value) else None
    if isinstance(value, str):
        try:
            number = float(value)
        except ValueError:
            return None
        return number if math.isfinite(number) else None
    return None


def _symmetric_sigma(upper, lower):
    """Average asymmetric bounds into one sigma; None when both absent."""
    if upper is None and lower is None:
        return None
    if upper is None:
        return abs(lower)
    if lower is None:
        return abs(upper)
    return (abs(upper) + abs(lower)) / 2


def _observable_sigma(obs, component=None):
    """Total (or single-component) uncertainty of an observable, or None.

    ``component`` (e.g. ``'type@1'``) selects one component error; otherwise
    the total error is used (``total_upper``/``total_lower``, or the
    component errors added in quadrature). ``type@N_error`` holds the label,
    so magnitudes come from ``type@N_upper``/``_lower``.
    """
    if not isinstance(obs, dict):
        return None
    if component is not None:
        return _symmetric_sigma(
            _field_number(obs.get(f'{component}_upper')),
            _field_number(obs.get(f'{component}_lower')),
        )
    total = _symmetric_sigma(
        _field_number(obs.get('total_upper')),
        _field_number(obs.get('total_lower')),
    )
    if total is not None:
        return total
    tags = sorted({
        key.split('_', 1)[0] for key in obs
        if re.fullmatch(r'type@\d+_(?:upper|lower)', key)
    }, key=lambda tag: int(tag.split('@')[1]))
    squares = []
    for tag in tags:
        sigma = _symmetric_sigma(
            _field_number(obs.get(f'{tag}_upper')),
            _field_number(obs.get(f'{tag}_lower')),
        )
        if sigma is not None:
            squares.append(sigma * sigma)
    if not squares:
        return None
    return math.sqrt(sum(squares))


def _ordered_channel_obs(channel):
    """Observable dicts of a channel in obs@N order (matrix flattening)."""
    if not isinstance(channel, dict):
        return []
    keys = [key for key in channel if re.fullmatch(r'obs@\d+', key)]
    keys.sort(key=lambda key: int(key.split('@', 1)[1]))
    return [channel[key] for key in keys]


def validate_correlation(matrix: list, label: str, is_covariance: bool = False,
                         sigmas: list | None = None,
                         acknowledged: bool = False) -> list[str]:
    """Check a correlation/covariance matrix.

    Both: numeric (bool rejected), finite, symmetric. Correlation: diagonal
    = 1.0 and off-diagonal within [-1, 1]. Covariance: diagonal is the
    variance, checked against the per-observable total error (``sigmas``,
    flattened in channel then obs@N order) when available.

    An out-of-range correlation element in a group that carries a
    group-level ``note`` is reported as a warning instead of an error, so
    the published value can be imported as-is and documented beside the
    matrix.
    """
    issues = []
    n = len(matrix)
    for i, row in enumerate(matrix):
        if not isinstance(row, list) or len(row) != n:
            row_len = len(row) if isinstance(row, list) else 'N/A'
            issues.append(
                f"  {label}: matrix row {i} length ({row_len}) "
                f"does not match column count ({n})"
            )
            return issues
    for i in range(n):
        for j in range(n):
            element = matrix[i][j]
            if isinstance(element, bool) or not isinstance(element, (int, float)):
                issues.append(
                    f"  {label}: matrix element [{i}][{j}] "
                    f"is not numeric (type: {type(element).__name__})"
                )
                return issues
            if not math.isfinite(element):
                issues.append(
                    f"  {label}: matrix element [{i}][{j}] "
                    f"is not finite ({element})"
                )
                return issues
    for i in range(n):
        if is_covariance:
            if matrix[i][i] < 0:
                issues.append(
                    f"  {label}: covariance diagonal [{i}][{i}] = "
                    f"{matrix[i][i]} is negative"
                )
            if sigmas is not None and i < len(sigmas) and sigmas[i] is not None:
                expected = sigmas[i] ** 2
                # Reported errors are rounded (often 2 significant figures),
                # so the variance matches only approximately; 5% tolerates
                # rounding while still catching gross mistakes.
                if expected > 0 and abs(matrix[i][i] - expected) > 0.05 * expected:
                    issues.append(
                        f"  {label}: covariance diagonal [{i}][{i}] = "
                        f"{matrix[i][i]} does not match the observable "
                        f"variance {expected:.6g} (error {sigmas[i]:.6g})"
                    )
        elif abs(matrix[i][i] - 1.0) > 0.001:
            issues.append(
                f"  {label}: correlation matrix diagonal "
                f"[{i}][{i}] = {matrix[i][i]}, expected 1.0"
            )
        for j in range(i + 1, n):
            if abs(matrix[i][j] - matrix[j][i]) > 0.001:
                issues.append(
                    f"  {label}: matrix not symmetric "
                    f"[{i}][{j}] = {matrix[i][j]} vs [{j}][{i}] = {matrix[j][i]}"
                )
            if not is_covariance and abs(matrix[i][j]) > 1.001:
                message = (
                    f"  {label}: correlation element [{i}][{j}] = "
                    f"{matrix[i][j]} outside [-1, 1]"
                )
                if acknowledged:
                    print("  [WARN] " + message.strip()
                          + " (documented by the group-level 'note')")
                else:
                    issues.append(message)
    return issues


def validate_arxiv_format(arxiv) -> list[str]:
    """Check the arxiv field: JSON null, a ``[id](url)`` Markdown link, or a
    legacy bare ID string (normalized to Markdown on re-import).

    The link text may be an arXiv ID (with or without ``vN``) or a non-arXiv
    identifier such as ``LHCb-NOTE-2015-001``.
    """
    issues = []
    if arxiv is None:
        return issues
    if not isinstance(arxiv, str):
        issues.append(
            f"  arxiv field must be a string or null, "
            f"got {type(arxiv).__name__}"
        )
        return issues
    # JSON's null is the bare value, not the 4-char literal "null".
    if arxiv == "null":
        issues.append(
            f"  arxiv field is the string '\"null\"'; use JSON null instead"
        )
        return issues
    if not arxiv.strip():
        issues.append("  arxiv field is empty; use JSON null instead")
        return issues
    if not arxiv.startswith("["):
        return issues
    md_match = re.match(r'^\[([^\]]+)\]\(([^)]*)\)$', arxiv)
    if not md_match:
        issues.append(
            f"  arxiv field format error; expected "
            f"[text](url), got: {arxiv}"
        )
        return issues
    link_text = md_match.group(1)
    # A slash means a real arXiv ID; a missing vN is a warning, not a
    # failure, so legacy files stay valid inputs.
    if '/' in link_text and 'v' not in link_text.split('/', 1)[1]:
        print(
            f"  [WARN] arxiv field '{link_text}' is missing version suffix "
            f"(e.g. 'v1', 'v2') — consider adding it"
        )
    return issues


_INSPIRE_LINK_RE = re.compile(
    r'\[([^\]]+)\]\(https://inspirehep\.net/literature/(\d+)\)'
)


def validate_inspire_format(inspire) -> list[str]:
    """Check the inspire-hep field: ``[TexKey](https://inspirehep.net/literature/<recid>)``.

    Unlike ``arxiv``, no legacy bare form is accepted: json-meta.md
    §"Top-Level Metadata Fields" requires the Markdown link.
    """
    if not isinstance(inspire, str):
        return [
            f"  inspire-hep field must be a string, "
            f"got {type(inspire).__name__}"
        ]
    if not _INSPIRE_LINK_RE.fullmatch(inspire.strip()):
        return [
            f"  inspire-hep field must be a Markdown link "
            f"'[TexKey](https://inspirehep.net/literature/<recid>)', "
            f"got: {inspire!r}"
        ]
    return []


def _validate_channel_entry(channel, label: str,
                            allow_empty: bool = False) -> tuple[list[str], int]:
    """Validate one channel entry: an object of ``obs@N`` entries.

    The channel key carries the transition; the value holds only
    ``obs@N`` entries. Kinematic bounds belong inside the observable and
    matrices at the group level. Returns the issues and the observable
    count, which feeds the group matrix dimension check. An empty channel
    is rejected unless ``allow_empty`` is set; only a ``no-transition``
    group whose ``note`` records that the source tabulates no numbers may
    be empty (json-meta.md §"Data Entries").
    """
    issues = []
    if not isinstance(channel, dict):
        return [
            f"  {label}: must be an object of obs@N entries"
        ], 0

    obs_keys = []
    for key in channel:
        if not re.fullmatch(r'obs@\d+', key):
            issues.append(
                f"  {label}: disallowed field '{key}'; a channel value "
                f"holds only obs@N entries — put kinematic bounds inside "
                f"the observable and matrices at the group level"
            )
            continue
        try:
            num = int(key.split('@', 1)[1])
        except (ValueError, IndexError):
            issues.append(
                f"  {label}: invalid obs key '{key}'; "
                f"expected obs@N format (N as integer)"
            )
            continue
        obs_keys.append((num, key))
    obs_keys.sort(key=lambda item: item[0])
    obs_nums = [num for num, _ in obs_keys]
    obs_keys = [key for _, key in obs_keys]

    # Numbering is per channel: start at 1 and run 1..N with no gaps.
    if obs_nums:
        expected = list(range(1, len(obs_nums) + 1))
        if obs_nums != expected:
            missing = [num for num in expected if num not in obs_nums]
            issues.append(
                f"  {label}: obs@N numbering is not contiguous; found "
                f"{obs_nums}, expected 1..{len(obs_nums)}; missing "
                f"obs@{missing}"
            )
    elif not allow_empty:
        issues.append(f"  {label}: no obs@N entries")

    for obs_key in obs_keys:
        issues.extend(_validate_observable(
            channel[obs_key], f"{label}.{obs_key}",
        ))
    return issues, len(obs_keys)


def _is_float_string(text) -> bool:
    if not isinstance(text, str) or not text.strip():
        return False
    try:
        float(text)
    except ValueError:
        return False
    return True


def _unit_issue(unit, label: str) -> list[str]:
    """Units are bare ASCII symbols with an optional integer power.

    Scale factors and percentages belong in the numbers, not in ``unit``
    (json-meta.md §"unit").
    """
    if not isinstance(unit, str):
        return []
    text = unit.strip()
    if _UNIT_RE.fullmatch(text):
        return []
    if '%' in text:
        hint = (
            "divide value/errors/bounds by 100 and omit unit"
        )
    elif re.search(r'\d[eE][+-]?\d|10\^|\d\s+[A-Za-z]', text):
        hint = (
            "multiply the scale factor into value/total_upper/total_lower/"
            "type@N_upper/type@N_lower and keep only the physical unit"
        )
    else:
        hint = (
            "write a bare ASCII unit with an optional integer power "
            "(GeV, GeV-2, GeV2, MeV, ps-1); no LaTeX and no scale prefix"
        )
    return [f"  {label}.unit: {unit!r} is not a bare ASCII unit; {hint}"]


def _kinematic_issues(value, label: str) -> list[str]:
    """Kinematic bounds are float-strings, comma lists, or '+inf'."""
    if not isinstance(value, str):
        return [
            f"  {label}: must be a string (float-as-string, "
            f"comma-separated list, or '+inf'); got {type(value).__name__}"
        ]
    issues = []
    for part in value.split(','):
        part = part.strip()
        if part == '+inf' or _is_float_string(part):
            continue
        issues.append(
            f"  {label}: part {part!r} is not a valid float-as-string and "
            f"not '+inf'; per json-meta.md §Combined Kinematic Bins"
        )
    return issues


def _validate_component_errors_and_bounds(obs: dict, label: str) -> list[str]:
    """Validate typed component errors and bound (limit) slots.

    A ``type@N`` slot is either a component error (``_error`` + ``_upper``
    + ``_lower``, no ``_level``) or a bound (``_upper``/``_lower`` +
    ``_level``, no ``_error``). A lone error is the total error and must use
    ``total_upper``/``total_lower`` instead of a ``type@N`` triplet.
    """
    issues = []
    tags = sorted({
        key.split('_', 1)[0]
        for key in obs
        if re.fullmatch(r'type@\d+_(?:error|upper|lower|level)', key)
    }, key=lambda tag: int(tag.split('@')[1]))
    component_tags = []
    for tag in tags:
        base, up, down, level = (
            f'{tag}_error', f'{tag}_upper', f'{tag}_lower', f'{tag}_level'
        )
        has_error = base in obs
        has_upper = up in obs
        has_lower = down in obs
        has_level = level in obs
        if has_error:
            component_tags.append(tag)
            missing = [key for key in (up, down) if key not in obs]
            if missing:
                issues.append(
                    f"  {label}: incomplete error triplet for '{tag}'; missing "
                    f"{missing}; each component error requires '{base}', "
                    f"'{up}' and '{down}' together"
                )
            if has_level:
                issues.append(
                    f"  {label}: '{tag}' is used both as a component error "
                    f"('{base}') and as a bound ('{level}'); use distinct "
                    f"type@N slots"
                )
            value = obs[base]
            if not isinstance(value, str) or not value.strip():
                issues.append(
                    f"  {label}.{base}: error label must be a non-empty string"
                )
            elif (value.strip() not in STANDARD_ERROR_LABELS
                  and not THEO_SOURCE_LABEL_RE.fullmatch(value.strip())):
                issues.append(
                    f"  {label}.{base}: unknown error label '{value}'; allowed "
                    f"labels are {sorted(STANDARD_ERROR_LABELS)} or "
                    f"'theo:<source>'"
                )
            continue
        if not has_level:
            issues.append(
                f"  {label}: '{up}'/'{down}' present without '{level}'; "
                f"error bounds need a component error, limits need a level"
            )
        if not (has_upper or has_lower):
            issues.append(
                f"  {label}: '{level}' present without a bound; add "
                f"'{tag}_upper' or '{tag}_lower'"
            )
    if len(component_tags) == 1:
        issues.append(
            f"  {label}: a single error must be written as the total error "
            f"('total_upper'/'total_lower'), not as a type@N triplet"
        )
    return issues


def _validate_measurement_scheme(obs: dict, label: str) -> list[str]:
    """Enforce exactly one measurement format (SKILL.md checklist)."""
    issues = []
    has_value = 'value' in obs
    has_component = any(re.fullmatch(r'type@\d+_error', key) for key in obs)
    has_total = 'total_upper' in obs or 'total_lower' in obs
    has_bound = any(re.fullmatch(r'type@\d+_level', key) for key in obs)

    if has_component and has_total:
        issues.append(
            f"  {label}: mixes component errors (type@N_error) with total "
            f"errors (total_upper/total_lower); use exactly one error scheme"
        )
    if has_value and not (has_component or has_total):
        issues.append(
            f"  {label}: measurement has no error; add component errors "
            f"(type@N_error) or total_upper/total_lower"
        )
    if not has_value and not has_bound:
        issues.append(
            f"  {label}: missing 'value' or a bound "
            f"(type@N_upper/type@N_lower + type@N_level)"
        )
    if not has_value and (has_component or has_total):
        issues.append(
            f"  {label}: bound-only entries must not carry value or errors; "
            f"use the combined format (value + errors) when a fit result is "
            f"also reported"
        )
    return issues


_MARKDOWN_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


def _validate_observable(obs, label: str) -> list[str]:
    """Validate one ``obs@N`` object."""
    if not isinstance(obs, dict):
        return [f"  {label}: must be an object"]

    issues = []

    for key, value in obs.items():
        if not is_observable_field(key):
            issues.append(
                f"  {label}: unknown observable field '{key}'; allowed "
                f"fields are {sorted(OBS_EXACT_FIELDS)} plus "
                f"type@N_error/type@N_upper/type@N_lower/type@N_level"
            )
        if key == 'unit':
            if not isinstance(value, str) or not value.strip():
                issues.append(f"  {label}.{key}: must be a non-empty string")
            else:
                issues.extend(_unit_issue(value, label))
        elif key in DATA_ENTRY_KINEMATIC_FIELDS:
            issues.extend(_kinematic_issues(value, f"{label}.{key}"))
        elif key in ('dataset', 'note'):
            if not isinstance(value, str) or not value.strip():
                issues.append(f"  {label}.{key}: must be a non-empty string")
        elif key == 'ref':
            if (not isinstance(value, str)
                    or not _MARKDOWN_LINK_RE.fullmatch(value.strip())):
                issues.append(
                    f"  {label}.{key}: must be a Markdown link "
                    f"'[TexKey](https://inspirehep.net/literature/<recid>)'"
                )
        elif _NUMERIC_OBS_KEY_RE.fullmatch(key):
            if not isinstance(value, str):
                issues.append(
                    f"  {label}.{key}: expected string, "
                    f"got {type(value).__name__}"
                )
            elif not value.strip():
                issues.append(f"  {label}.{key}: must not be empty")
            elif not _is_float_string(value):
                issues.append(
                    f"  {label}.{key}: expected a float-as-string, "
                    f"got {value!r}"
                )

    if 'name' not in obs:
        issues.append(f"  {label}: missing required field: name")
    issues.extend(_validate_component_errors_and_bounds(obs, label))
    has_tot_up = 'total_upper' in obs
    if has_tot_up != ('total_lower' in obs):
        missing = 'total_lower' if has_tot_up else 'total_upper'
        issues.append(
            f"  {label}: total error is one-sided; missing '{missing}'"
        )
    issues.extend(_validate_measurement_scheme(obs, label))

    if 'name' in obs:
        name = obs['name']
        if not isinstance(name, str) or not name.strip():
            issues.append(f"  {label}.name: must be a non-empty string")
        else:
            issues.extend(validate_observable_name(name))

    return issues


def _validate_data_group(group, label: str) -> list[str]:
    """Validate one data group: channel bundles, metadata, matrices.

    A group is an object whose non-matrix, non-metadata keys are
    transition channels (each mapping to an object of ``obs@N`` entries).
    The optional group-level ``dataset`` string names the data sources
    behind the group, followed by an optional ``scheme`` string when the
    group holds form-factor expansion coefficients. An optional
    group-level ``note`` documents the accompanying matrix (e.g. a
    published out-of-range correlation element). These keys must precede
    any matrix key. The optional ``correlation``/``covariance`` matrices
    align with the observables of all channels, flattened in channel
    order then ``obs@N`` order.
    """
    issues = []
    if not isinstance(group, dict):
        return [f"  {label}: must be an object"]

    matrix_keys = []
    channel_count = 0
    obs_total = 0
    ordered_obs = []
    first_metadata = None
    saw_scheme = False
    saw_note = False
    saw_matrix = False
    has_coefficients = False
    for key in group:
        if key in ('dataset', 'scheme', 'note'):
            if first_metadata is None:
                first_metadata = key
            value = group[key]
            if not isinstance(value, str) or not value.strip():
                issues.append(f"  {label}.{key}: must be a non-empty string")
            elif key == 'scheme' and value not in FORM_FACTOR_SCHEMES:
                issues.append(
                    f"  {label}.scheme: unsupported value {value!r}; "
                    f"use one of: {', '.join(sorted(FORM_FACTOR_SCHEMES))}"
                )
            elif key == 'dataset':
                issue = _dataset_issue(value)
                if issue:
                    issues.append(f"  {label}.dataset: {issue}")
            if saw_matrix:
                issues.append(
                    f"  {label}: '{key}' appears after a matrix key; "
                    f"keep it before the matrices"
                )
            if key == 'dataset':
                if saw_scheme:
                    issues.append(
                        f"  {label}: 'dataset' appears after 'scheme'; "
                        f"keep 'dataset' first"
                    )
                elif saw_note:
                    issues.append(
                        f"  {label}: 'dataset' appears after 'note'; "
                        f"keep 'dataset' first"
                    )
            elif key == 'scheme':
                if saw_note:
                    issues.append(
                        f"  {label}: 'scheme' appears after 'note'; "
                        f"keep 'scheme' before 'note'"
                    )
                saw_scheme = True
            else:
                saw_note = True
            continue
        if is_group_matrix_key(key):
            matrix_keys.append(key)
            saw_matrix = True
            continue
        if first_metadata is not None:
            issues.append(
                f"  {label}: channel '{key}' appears after "
                f"'{first_metadata}'; keep all channel keys first"
            )
        if saw_matrix:
            issues.append(
                f"  {label}: channel '{key}' appears after a matrix key; "
                f"keep all channel keys first so the matrix ordering is "
                f"unambiguous"
            )
        channel_count += 1
        issues.extend(validate_transition_key(key))
        allow_empty = (
            key == 'no-transition'
            and isinstance(group.get('note'), str)
            and bool(group['note'].strip())
        )
        channel_issues, obs_count = _validate_channel_entry(
            group[key], f"{label}['{key}']", allow_empty=allow_empty,
        )
        issues.extend(channel_issues)
        obs_total += obs_count
        ordered_obs.extend(_ordered_channel_obs(group[key]))
        if isinstance(group[key], dict):
            has_coefficients = has_coefficients or any(
                isinstance(obs, dict)
                and isinstance(obs.get('name'), str)
                and _FORM_FACTOR_COEFFICIENT_RE.fullmatch(
                    _observable_symbol(obs['name'])
                )
                for obs in group[key].values()
            )

    if not channel_count:
        issues.append(
            f"  {label}: no transition channel; every data group needs at "
            f"least one channel key (or 'no-transition')"
        )

    if has_coefficients and not saw_scheme:
        issues.append(
            f"  {label}: form-factor coefficient data must declare a "
            f"group-level 'scheme'"
        )

    acknowledged = isinstance(group.get('note'), str) and bool(
        group['note'].strip()
    )
    for key in matrix_keys:
        matrix = group[key]
        if matrix is None:
            issues.append(
                f"  {label}['{key}']: omit the key entirely when no matrix "
                f"is available; do not set it to null"
            )
            continue
        if not isinstance(matrix, list):
            issues.append(f"  {label}['{key}']: expected 2D array")
            continue
        is_covariance = 'covariance' in key
        sigmas = None
        if is_covariance:
            prefix = re.match(r'(type@\d+)_', key)
            component = prefix.group(1) if prefix else None
            sigmas = [_observable_sigma(obs, component) for obs in ordered_obs]
        issues.extend(
            validate_correlation(
                matrix, f"{label}['{key}']",
                is_covariance=is_covariance, sigmas=sigmas,
                acknowledged=acknowledged,
            )
        )
        if len(matrix) != obs_total:
            issues.append(
                f"  {label}['{key}']: matrix dimension "
                f"({len(matrix)}x{len(matrix)}) does not match the "
                f"{obs_total} observables of the group's channels"
            )
    return issues


def _validate_data_list(groups: list) -> list[str]:
    """Validate the ``[group, ...]`` ``data`` schema.

    Each group may carry one or more transition channels; a channel may
    appear in several groups to separate datasets, kinematic bins, or
    matrices.
    """
    issues = []
    if not groups:
        issues.append("  data array is empty")
        return issues
    for group_idx, group in enumerate(groups):
        issues.extend(_validate_data_group(group, f"data[{group_idx}]"))
    return issues


def validate_transition_mode(value: str) -> list[str]:
    """Check that transition-mode matches one of the valid hyphenated values."""
    issues = []
    if not isinstance(value, str) or not value.strip():
        issues.append("  transition-mode must be a non-empty string")
        return issues
    if value.lower() not in VALID_TRANSITION_MODES:
        issues.append(
            f"  transition-mode '{value}' is not in the allowed list: "
            f"{VALID_TRANSITION_MODES}; use hyphenated property names like "
            f"'semileptonic-decay', 'scattering', etc."
        )
    return issues


def validate_json(file_path: str) -> list[str]:
    """Validate a single flav-data JSON file."""
    # 1. Parse JSON. ``json.load`` silently keeps the last of a repeated
    # key, which would drop a channel or an observable without any error.
    duplicates: list[str] = []

    def _reject_duplicate_keys(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj and key not in duplicates:
                duplicates.append(key)
            obj[key] = value
        return obj

    all_issues = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f, object_pairs_hook=_reject_duplicate_keys)
        print("  [OK] JSON format correct")
    except json.JSONDecodeError as e:
        print(f"  [FAIL] JSON parse error: {e}")
        return [f"JSON parse error: {e}"]

    # Check top-level type before inspecting schema-specific fields.
    if not isinstance(data, dict):
        print(f"  [FAIL] Top-level JSON must be an object, got {type(data).__name__}")
        return [f"Top-level JSON must be an object, got {type(data).__name__}"]

    if duplicates:
        for key in duplicates:
            all_issues.append(
                f"  Duplicate JSON key '{key}': a repeated key silently "
                f"overwrites the earlier value; merge the entries or rename "
                f"one of them"
            )
        print(f"  [FAIL] Found {len(all_issues)} issue(s):")
        for issue in all_issues:
            print(issue)
        return all_issues

    # 2. Check top-level fields
    for field in REQUIRED_TOP_FIELDS:
        if field not in data:
            all_issues.append(f"  Missing required field: {field}")
        elif (field != 'arxiv' and isinstance(data[field], str)
              and not data[field].strip()):
            all_issues.append(f"  Top-level field '{field}' must not be empty")
    if 'collaboration' in data and (
        not isinstance(data['collaboration'], str)
        or not data['collaboration'].strip()
    ):
        all_issues.append(
            "  Top-level field 'collaboration' must be a non-empty string "
            "when present (omit it for individual/small-group papers)"
        )
    if not all_issues:
        print("  [OK] Top-level fields complete")

    # 2b. Check Unicode-free LaTeX in author, title and abstract (per
    # SKILL.md rule 4 and json-meta.md §"Key Constraints").
    for field in ('author', 'title', 'abstract'):
        if field in data and isinstance(data[field], str):
            all_issues.extend(validate_latex(data[field], field, '<top-level>'))

    # 3. Check for forbidden and unknown top-level fields
    for field in FORBIDDEN_FIELDS:
        if field in data:
            all_issues.append(f"  Forbidden field present: '{field}' (not supported)")
    for field in data:
        if field not in TOP_LEVEL_ALLOWED_FIELDS and field not in FORBIDDEN_FIELDS:
            all_issues.append(f"  Unknown top-level field: '{field}'")

    # 4. transition-mode must immediately precede data, which is the final key.
    if 'transition-mode' in data and 'data' in data:
        keys = list(data.keys())
        tm_idx = keys.index('transition-mode')
        if keys[tm_idx + 1:] != ['data']:
            all_issues.append(
                f"  expected 'transition-mode' immediately before final 'data'; "
                f"keys after transition-mode: {keys[tm_idx + 1:]}"
            )

    # 5. Check arxiv and inspire-hep field formats
    arxiv = data.get('arxiv')
    all_issues.extend(validate_arxiv_format(arxiv))
    if 'inspire-hep' in data:
        all_issues.extend(validate_inspire_format(data['inspire-hep']))

    # 6. Check transition-mode content
    if 'transition-mode' in data:
        all_issues.extend(validate_transition_mode(data['transition-mode']))

    # 7. Check data: an array of groups; each group maps transition
    # channels to their observables and optionally carries matrices.
    if 'data' not in data:
        all_issues.append("  Missing required field: data")
    elif isinstance(data['data'], list):
        all_issues.extend(_validate_data_list(data['data']))
    else:
        all_issues.append(
            "  data must be an array of data groups, e.g. "
            "[{'dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0': "
            "{'obs@1': {...}}, "
            "'correlation': [[1.0]]}]; "
            "channels sharing one matrix belong in the same group"
        )

    # Report results
    if all_issues:
        print(f"  [FAIL] Found {len(all_issues)} issue(s):")
        for issue in all_issues:
            print(issue)
    else:
        print("  [OK] All checks passed")

    return all_issues


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description=(
            "Validate a flav-data JSON file against the schema defined "
            "in references/json-meta.md. Pass one or more file paths."
        )
    )
    parser.add_argument(
        'paths', nargs='+',
        help='One or more JSON files to validate.'
    )
    parser.add_argument(
        '--quiet', '-q', action='store_true',
        help='Omit the per-file "Validating:" header and trailing blank '
             'line. Check results, issues and the summary are still printed.'
    )
    args = parser.parse_args()

    total_issues = 0
    for path in args.paths:
        if not os.path.exists(path):
            print(f"File not found: {path}")
            total_issues += 1
            continue
        if not args.quiet:
            print(f"Validating: {path}")
        issues = validate_json(path)
        total_issues += len(issues)
        if not args.quiet:
            print()

    if total_issues == 0:
        print("All files validated successfully.")
        sys.exit(0)
    else:
        print(f"Found {total_issues} issue(s) in total.")
        sys.exit(1)


if __name__ == '__main__':
    main()
