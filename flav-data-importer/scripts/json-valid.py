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

# Fields that must NOT appear in a per-paper JSON. HFLAV/PDG snapshots
# have their own schema and do allow ``year`` (see _validate_snapshot).
FORBIDDEN_FIELDS = ['year', 'pdf']

# Snapshot (HFLAV/PDG) observable fields. Unknown keys are rejected so
# the per-paper error formats (type@N_error, ref, ...) cannot leak into a
# snapshot. See references/json-meta.md §"Non-Standard Schemas".
SNAPSHOT_OBS_ALLOWED_FIELDS = {
    'name', 'value',
    'total_upper', 'total_lower',
    'unit', 'limit',
}

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
_SCALE_UNIT_RE = re.compile(
    r'(?:1e[+-]?\d+|10\^\{?[+-]?\d+\}?)$', re.IGNORECASE
)


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
]

# Top-level fields allowed in the standard (per-paper) schema.
TOP_LEVEL_ALLOWED_FIELDS = set(REQUIRED_TOP_FIELDS) | set(CONDITIONAL_TOP_FIELDS)

# Snapshot schemas (json-meta.md §"Non-Standard Schemas").
PDG_SUBGROUP_ALLOWED_FIELDS = {'correlation'}
HFLAV_SUBGROUP_ALLOWED_FIELDS = {
    'group', 'arxiv', 'inspire-hep', 'description',
    'observables', 'correlation',
}

# Kinematic boundary fields, valid inside an ``obs@N`` object.
DATA_ENTRY_KINEMATIC_FIELDS = {
    'q2min', 'q2max', 'pTmin', 'pTmax', 'etamin', 'etamax',
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
# unified Delta form; see references/obs-abbr.md §"LFU Difference
# Observables" for the correspondence.
_DEPRECATED_LFU_Q_NAMES = {
    'Q1': 'DeltaP1', 'Q2': 'DeltaP2', 'Q3': 'DeltaP3',
    'Q4': 'DeltaP4p', 'Q5': 'DeltaP5p', 'Q6': 'DeltaP6p',
    'Q8': 'DeltaP8p', 'QFL': 'DeltaFL',
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


# --- Canonical transition ordering (obs-abbr.md §1) -------------------
# Particle tokens are classified into the four orderable types from the
# spec. Hadrons keep their conventional capitalisation; leptons and light
# mesons stay lowercase (e+, mu-, pi-, v).
_BARYON_STEMS = (
    'Lambdac', 'Lambdab', 'Lambda', 'Sigma', 'Xic', 'Xib',
    'Omegac', 'Omega', 'Xi',
)
_MESON_STEMS = (
    'J/psi', 'psi', 'K*', 'Bc', 'Bs0', 'B0', 'B',
    'D*', 'Ds', 'D0', 'D', 'KS0', 'KL0',
    'K0', 'K', 'pi', 'rho', 'phi', 'omega', 'eta', 'Xs', 'Xce', 'Xcl', 'f',
)
_MESON_CHARGED_STEMS = ('B', 'Bc', 'D', 'D*', 'Ds', 'K', 'K*', 'pi', 'rho')
_LEP_STEMS = ('mu', 'tau', 'e', 'l')
_NEUTRAL_MESONS = {
    'J/psi', 'psi', 'phi', 'omega', 'eta', 'etaprime', 'Xs', 'Xce', 'Xcl',
    'f', 'D0', 'B0', 'Bs0', 'K0', 'K*0', 'D*0',
    'KL0', 'KS0', 'B0Bar',
}
_NEUTRAL_LEPTONS = {
    'v', 'vBar', 've', 'veBar', 'vmu', 'vmuBar', 'vtau', 'vtauBar',
}
_TYPE_NAMES = {
    1: 'baryon', 2: 'meson', 3: 'charged lepton', 4: 'neutral lepton',
}

# Particle-state grammar: <name>[*]<charge>[Bar].  Neutrinos keep the
# conventional ``v``/``vBar`` spelling without a charge slot, and neutral
# gauge bosons stay bare.  The remaining tokens are not single PDG
# particle states (placeholders, partons, nuclei, inclusive systems, or
# experimental/BSM pseudo-labels) and therefore have no charge slot.
_CHARGE_EXEMPT_TOKENS = _NEUTRAL_LEPTONS | {
    'Z', 'gamma', 'g', 'gg', 'gamma+gamma',
    'l', 'l+', 'l-', 'q', 'q1', 'q2', 'qBar',
    'b', 'bBar', 'c', 'cBar', 's', 'sBar', 't', 'tBar',
    'u', 'uBar', 'd', 'dBar', 'bs', 'cb', 'uds', '0+',
    'Xs', 'XsBar', 'Xce', 'Xcl',
    'all', 'had', 'med', 'world', 'CDF', 'kappa',
    'Au', 'Ca', 'Ti', 'V', 'VH', 'Zp', 'emup',
    'f', 'fBar',
}
# Neutral or charged states outside ``particle-masses.json`` that still
# need an explicit charge marker.
_CHARGE_REQUIRED_EXTRA = {
    'H', 'W', 'Wp', 'WKK', 'Gstar', 'sneutrino', 'omegal',
}

# Masses come from the PDG-backed reference file, not from guesses in
# this script. See references/particle-masses.json for values and source.
def _load_mass_reference() -> tuple[dict[str, float], set[str]]:
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, '..', 'references', 'particle-masses.json')
    with open(os.path.abspath(path), 'r', encoding='utf-8') as handle:
        payload = json.load(handle)
    masses = payload.get('masses', {})
    if not isinstance(masses, dict) or not masses:
        raise RuntimeError(
            f'{path}: missing non-empty "masses" object'
        )
    non_orderable = set(payload.get('non_orderable', []))
    return masses, non_orderable


_PARTICLE_MASS, _NON_ORDERABLE = _load_mass_reference()


def _strip_bar(token: str) -> str:
    # Only the canonical capital ``Bar`` at the very end is stripped;
    # lowercase ``bar`` and the legacy mid-symbol placement are invalid.
    return re.sub(r'Bar$', '', token)


def _strip_resonance(token: str) -> str:
    """Drop the trailing ``(2.l+.l-)`` resonance-decay annotation."""
    return re.sub(r'\(2\.[^()]*\)$', '', token)


def _split_mass_tag(token: str) -> tuple[str, float | None]:
    """Split a trailing PDG mass label in MeV, e.g. ``D0*+(2300)``."""
    match = re.fullmatch(r'(.*)\((\d{3,4})\)', token)
    if not match:
        return token, None
    return match.group(1), float(match.group(2)) / 1000.0


def _particle_mass(token: str) -> float | None:
    """Return the particle mass in GeV, or ``None`` when it is unknown."""
    base, tagged_mass = _split_mass_tag(_strip_resonance(token))
    if tagged_mass is not None:
        return tagged_mass
    stem = _strip_bar(base)
    if stem in _PARTICLE_MASS:
        return _PARTICLE_MASS[stem]
    # Antiparticles share the mass of their partner.
    if stem.endswith('-') and stem[:-1] + '+' in _PARTICLE_MASS:
        return _PARTICLE_MASS[stem[:-1] + '+']
    if stem.endswith('+') and stem[:-1] + '-' in _PARTICLE_MASS:
        return _PARTICLE_MASS[stem[:-1] + '-']
    # A charge marker appended to a bare particle name (``phi0``,
    # ``Lambda0``, ``p+``) shares the bare particle's mass.
    if stem.endswith(('+', '-', '0')) and stem[:-1] in _PARTICLE_MASS:
        return _PARTICLE_MASS[stem[:-1]]
    return None


def _split_top_level(text: str, separator: str) -> list[str]:
    """Split on *separator* only outside balanced parentheses.

    Keeps resonance tokens such as ``psi(2S)(2.l+.l-)`` intact.
    """
    parts, buffer, depth = [], [], 0
    index = 0
    while index < len(text):
        char = text[index]
        if char == '(':
            depth += 1
        elif char == ')':
            depth = max(0, depth - 1)
        if depth == 0 and text.startswith(separator, index):
            parts.append(''.join(buffer))
            buffer = []
            index += len(separator)
            continue
        buffer.append(char)
        index += 1
    parts.append(''.join(buffer))
    return [part for part in parts if part]


# Particle names that contain the ratio separator (``J/psi``).
_SLASH_PARTICLE_TOKENS = tuple(sorted(
    (token for token in _PARTICLE_MASS if '/' in token),
    key=len, reverse=True,
))


def _split_ratio(body: str) -> list[str]:
    """Split a ratio key on ``/`` without cutting particle names.

    ``J/psi`` carries a slash of its own, so the separator is masked out
    before splitting. The slash-bearing names come from the mass
    reference rather than a hard-coded list.
    """
    masked = body
    for token in _SLASH_PARTICLE_TOKENS:
        masked = masked.replace(token, token.replace('/', '\x00'))
    return [
        part.replace('\x00', '/')
        for part in _split_top_level(masked, '/')
    ]


def _charge_rank(token: str) -> int | None:
    """Return ordering rank for an explicit charge: + -> 0, - -> 1."""
    if token.endswith('+'):
        return 0
    if token.endswith('-'):
        return 1
    return None


def _classify_particle(token: str) -> tuple[int | None, int | None]:
    """Classify a transition token as ``(type_rank, charge_rank)``.

    ``None`` means the token is not part of the four orderable types or its
    charge is implicit — such states are left unchecked rather than guessed.
    """
    if token in _NON_ORDERABLE:
        return None, None
    if token in _NEUTRAL_LEPTONS:
        return 4, 0

    base, _ = _split_mass_tag(_strip_resonance(token))
    stem = _strip_bar(base)
    if stem in _NON_ORDERABLE:
        return None, None
    name_core = re.sub(r'[+\-0]$', '', stem)
    if name_core in ('p', 'n'):
        charge = _charge_rank(stem)
        if charge is None:
            charge = 2 if name_core == 'n' or '0' in stem else 0
        if base.endswith('Bar'):
            charge = 1
        return 1, charge
    if stem.startswith(_BARYON_STEMS):
        charge = _charge_rank(base)
        if charge is None and ('0' in stem or stem in ('Lambda', 'Lambdab')):
            charge = 2
        return 1, charge

    core = re.sub(r'[+\-]$', '', stem)
    if core in _LEP_STEMS:
        if core == 'l' and not base.endswith(('+', '-')):
            # Bare generic lepton: its charge is unknown, so skip the state.
            return None, None
        return 3, _charge_rank(base)

    if stem.startswith(_MESON_STEMS):
        charge = _charge_rank(base)
        if charge is None and (
            base in _NEUTRAL_MESONS
            or stem in _NEUTRAL_MESONS
            or '0' in stem
        ):
            charge = 2
        return 2, charge

    return None, None


def _particle_grammar_issues(token: str, label: str) -> list[str]:
    """Check one particle state against ``<name>[*]<charge>[Bar]``."""
    issues = []
    bare, _ = _split_mass_tag(_strip_resonance(token))
    if bare.count('*') > 1:
        issues.append(
            f"  {label}: particle '{token}' has more than one vector marker "
            f"'*'; the grammar is <name>[*]<charge>[Bar]"
        )
    elif '*' in bare:
        tail = bare.split('*', 1)[1]
        if not re.fullmatch(r'(?:\+|-|0)(?:Bar)?', tail):
            issues.append(
                f"  {label}: particle '{token}' places characters around the "
                f"vector marker '*'; write <name>[*]<+|-|0>[Bar] "
                f"(e.g. 'D*0', 'D*+Bar')"
            )
    if 'Bar' in bare and not bare.endswith('Bar'):
        issues.append(
            f"  {label}: particle '{token}' places 'Bar' inside the symbol; "
            f"the antiparticle marker goes last, after the charge"
        )

    stem = _strip_bar(bare)
    name_core = re.sub(r'[+\-0]$', '', stem)
    if (stem in _CHARGE_EXEMPT_TOKENS
            or name_core in _CHARGE_EXEMPT_TOKENS):
        return issues
    if stem in _PARTICLE_MASS or name_core in _CHARGE_REQUIRED_EXTRA:
        if not re.search(r'[+\-0]$', stem):
            issues.append(
                f"  {label}: particle '{token}' has no charge marker; write "
                f"<name>[*]<+|-|0>[Bar] (e.g. 'phi0', 'p+', 'W-'); only "
                f"neutrinos and neutral gauge bosons are exempt"
            )
    return issues


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
    if '.2.' in text:
        return True
    return bool(re.search(r'[A-Za-z0-9][+\-]?2[A-Za-z0-9(]', text))


def validate_transition_key(key: str) -> list[str]:
    """Validate a bare transition used as a ``data`` dictionary key."""
    if key == 'no-transition':
        return []
    if '.2.' not in key:
        return [
            f"  data key '{key}' is not a transition channel; expected "
            f"A.B.2.C.D (or 'no-transition' for observables without one)"
        ]
    return _order_issues_for_body(key, f"data key '{key}'", require_known=True)


def _order_issues_for_body(
    body: str, label: str, require_known: bool = False,
) -> list[str]:
    """Check one transition body (``A.B.2.C.D``) and return order issues.

    With ``require_known=True`` (new dict-schema keys) every particle token
    must be in ``references/particle-masses.json`` or listed as
    non-orderable; otherwise the state would silently escape the ordering
    check.
    """
    issues = []
    parts = _split_ratio(body)
    if len(parts) > 1 and all('.2.' in part for part in parts):
        for part in parts:
            if '.2.' in part:
                issues.extend(
                    _order_issues_for_body(part, label, require_known)
                )
        return issues
    stages = _split_top_level(body, '.2.')
    for stage in stages:
        tokens = _split_top_level(stage, '.')
        classified = [_classify_particle(token) for token in tokens]
        types = [entry[0] for entry in classified]
        charges = [entry[1] for entry in classified]
        masses = [_particle_mass(token) for token in tokens]

        for token, (type_rank, _) in zip(tokens, classified):
            if 'Bar' not in token and 'bar' in token:
                issues.append(
                    f"  {label}: particle '{token}' uses lowercase 'bar'; "
                    f"write the antiparticle marker as capital 'Bar'"
                )
                continue
            issues.extend(_particle_grammar_issues(token, label))
            if _particle_mass(token) is None and token not in _NEUTRAL_LEPTONS:
                stem = _strip_bar(token)
                if stem in _NON_ORDERABLE or token in _NON_ORDERABLE:
                    continue
                if token[-1:] in ('p', 'm') and _particle_mass(token[:-1]):
                    sign = '+' if token[-1] == 'p' else '-'
                    issues.append(
                        f"  {label}: particle '{token}' writes its charge with "
                        f"'{token[-1]}'; write '{token[:-1]}{sign}' instead"
                    )
                    continue
                if token == 'K0L':
                    issues.append(
                        f"  {label}: particle 'K0L' is written 'KL0' "
                        f"(subscript before superscript)"
                    )
                    continue
                if type_rank is not None:
                    issues.append(
                        f"  {label}: state '{stage}' particle '{token}' has no "
                        f"mass in references/particle-masses.json; add its PDG "
                        f"mass so the ordering can be checked"
                    )
                elif require_known:
                    issues.append(
                        f"  {label}: state '{stage}' particle '{token}' is not "
                        f"a known particle; add its PDG mass to "
                        f"references/particle-masses.json (or list it under "
                        f"'non_orderable' if it cannot be ordered)"
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
                        issues.append(
                            f"  {label}: state '{stage}' breaks "
                            f"charge order in '{'.'.join(group_tokens)}'; "
                            f"expected "
                            f"'{'.'.join(token for _, token in sorted(zip(group_charges, group_tokens), key=lambda item: item[0]))}' "
                            f"(equal masses: + -> - -> 0)"
                        )
                        break
            index = end
    return issues


def _observable_symbol(name: str) -> str:
    """Return the bare symbol, dropping a ``[condition]``/``(parameter)`` tag."""
    return re.split(r'[\[(]', name, maxsplit=1)[0]


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
    # Check rectangular
    for i, row in enumerate(matrix):
        if not isinstance(row, list) or len(row) != n:
            row_len = len(row) if isinstance(row, list) else 'N/A'
            issues.append(
                f"  {label}: matrix row {i} length ({row_len}) "
                f"does not match column count ({n})"
            )
            return issues
    # Check element types and finiteness
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
    """Check arxiv field format. Accepted forms:

    - ``null`` (no preprint available, e.g. journal-only paper)
    - ``[primary_category/arxiv_id](url)`` (any arXiv ID form, with or
      without version suffix)
    - ``[non-arxiv-id](url)`` (e.g. ``[LHCb-NOTE-2015-001]``,
      ``[LHCb-ANA-2015-001]`` — LHC note numbers, journal
      citations, conference proceedings)
    - legacy bare string like ``"hep-ex/1512.04442"`` (will be
      normalized to markdown form on import)
    """
    issues = []
    if arxiv is None:
        return issues  # null is allowed
    if not isinstance(arxiv, str):
        issues.append(
            f"  arxiv field must be a string or null, "
            f"got {type(arxiv).__name__}"
        )
        return issues
    # The string ``"null"`` is almost always a hand-written mistake:
    # JSON's actual null is the bare value ``null``, not the 4-char
    # literal. Reject so the file is auto-fixable.
    if arxiv == "null":
        issues.append(
            f"  arxiv field is the string '\"null\"'; use JSON null instead"
        )
        return issues
    if not arxiv.strip():
        issues.append("  arxiv field is empty; use JSON null instead")
        return issues
    # Bare string (no brackets) — legacy form, accepted as-is. Caller
    # can normalize to markdown form when importing.
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
    # If the text contains a slash, it's a real arXiv ID — require
    # version. Otherwise it's a non-arXiv ID (CERN note etc.) and is
    # accepted as-is.
    if '/' in link_text and 'v' not in link_text.split('/', 1)[1]:
        # Real arXiv ID without version (legacy): accept but warn so the
        # importer / human notices. This is not a validation failure —
        # legacy files are valid inputs and are normalized on re-import.
        print(
            f"  [WARN] arxiv field '{link_text}' is missing version suffix "
            f"(e.g. 'v1', 'v2') — consider adding it"
        )
    return issues


def _validate_channel_entry(channel, label: str) -> tuple[list[str], int]:
    """Validate one channel entry: an object of ``obs@N`` entries.

    The channel key carries the transition; the value holds only
    ``obs@N`` entries. Kinematic bounds belong inside the observable and
    matrices at the group level. Returns the issues and the observable
    count, which feeds the group matrix dimension check.
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
    else:
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


def _scale_unit_issue(unit, label: str) -> list[str]:
    """Reject scientific-notation scale factors stored in ``unit``."""
    if isinstance(unit, str) and _SCALE_UNIT_RE.fullmatch(unit.strip()):
        return [
            f"  {label}.unit: {unit!r} is a pure scale factor, not a unit; "
            f"multiply it into value/total_upper/total_lower/bounds and "
            f"omit unit"
        ]
    return []


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


def _validate_observable(obs, label: str) -> list[str]:
    """Validate one ``obs@N`` object."""
    if not isinstance(obs, dict):
        return [f"  {label}: must be an object"]

    issues = []

    for key in obs:
        if not is_observable_field(key):
            issues.append(
                f"  {label}: unknown observable field '{key}'; allowed "
                f"fields are {sorted(OBS_EXACT_FIELDS)} plus "
                f"type@N_error/type@N_upper/type@N_lower/type@N_level"
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

    if 'name' in obs and (
        not isinstance(obs['name'], str) or not obs['name'].strip()
    ):
        issues.append(f"  {label}.name: must be a non-empty string")

    for key in obs:
        if key == 'unit':
            if not isinstance(obs[key], str) or not obs[key].strip():
                issues.append(f"  {label}.{key}: must be a non-empty string")
            else:
                issues.extend(_scale_unit_issue(obs[key], label))
            continue
        if not _NUMERIC_OBS_KEY_RE.fullmatch(key):
            continue
        if not isinstance(obs[key], str):
            issues.append(
                f"  {label}.{key}: expected string, "
                f"got {type(obs[key]).__name__}"
            )
        elif not obs[key].strip():
            issues.append(f"  {label}.{key}: must not be empty")
        elif not _is_float_string(obs[key]):
            issues.append(
                f"  {label}.{key}: expected a float-as-string, "
                f"got {obs[key]!r}"
            )

    for key in obs:
        if key in DATA_ENTRY_KINEMATIC_FIELDS:
            issues.extend(_kinematic_issues(obs[key], f"{label}.{key}"))

    for key in ('dataset', 'note'):
        if key in obs and (
            not isinstance(obs[key], str) or not obs[key].strip()
        ):
            issues.append(f"  {label}.{key}: must be a non-empty string")

    if 'name' in obs and isinstance(obs['name'], str):
        issues.extend(validate_observable_name(obs['name']))

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
    any matrix key. The optional ``correlation``/``covariance`` matrix
    aligns with the observables of all channels, flattened in channel
    order then ``obs@N`` order.
    """
    issues = []
    if not isinstance(group, dict):
        return [f"  {label}: must be an object"]

    matrix_keys = []
    channel_count = 0
    obs_total = 0
    ordered_obs = []
    saw_dataset = False
    saw_scheme = False
    saw_note = False
    saw_matrix = False
    has_coefficients = False
    for key in group:
        if key in ('dataset', 'scheme', 'note'):
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
                saw_dataset = True
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
        if saw_dataset:
            issues.append(
                f"  {label}: channel '{key}' appears after 'dataset'; "
                f"keep all channel keys first"
            )
        elif saw_scheme:
            issues.append(
                f"  {label}: channel '{key}' appears after 'scheme'; "
                f"keep all channel keys first"
            )
        elif saw_note:
            issues.append(
                f"  {label}: channel '{key}' appears after 'note'; "
                f"keep all channel keys first"
            )
        if saw_matrix:
            issues.append(
                f"  {label}: channel '{key}' appears after a matrix key; "
                f"keep all channel keys first so the matrix ordering is "
                f"unambiguous"
            )
        channel_count += 1
        issues.extend(validate_transition_key(key))
        channel_issues, obs_count = _validate_channel_entry(
            group[key], f"{label}['{key}']",
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
            continue  # null means no matrix — acceptable
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
    normalized = {mode.lower() for mode in VALID_TRANSITION_MODES}
    if value.lower() not in normalized:
        issues.append(
            f"  transition-mode '{value}' is not in the allowed list: "
            f"{VALID_TRANSITION_MODES}; use hyphenated property names like "
            f"'semileptonic-decay', 'scattering', etc."
        )
    return issues


def _detect_snapshot(data: dict) -> str | None:
    """Return ``'pdg'``, ``'hflav'``, or ``None`` for a non-snapshot file.

    PDG: top-level ``data`` is a dict of subgroups whose keys are ``obs@N``
    (sparse) plus an optional ``correlation``. Standard per-paper files
    have ``transition-mode`` and a ``data`` array of groups, so the two
    shapes are unambiguous. HFLAV: no top-level ``data``;
    each top-level value is a subgroup containing an ``observables`` list.
    """
    if 'transition-mode' not in data and isinstance(data.get('data'), dict):
        subgroups = data['data']
        if subgroups and all(
            isinstance(sub, dict)
            and all(
                key == 'correlation' or re.fullmatch(r'obs@\d+', str(key))
                for key in sub
            )
            for sub in subgroups.values()
        ):
            return 'pdg'
        return None
    if 'data' not in data and 'transition-mode' not in data:
        if any(
            isinstance(value, dict)
            and isinstance(value.get('observables'), list)
            for value in data.values()
        ):
            return 'hflav'
    return None


def _validate_snapshot_obs(obs, label: str, issues: list[str]) -> None:
    """Validate one snapshot observable (shared by PDG and HFLAV)."""
    if not isinstance(obs, dict):
        issues.append(f"  {label}: must be an object")
        return
    for key in obs:
        if key not in SNAPSHOT_OBS_ALLOWED_FIELDS:
            issues.append(
                f"  {label}: unknown observable field '{key}'; snapshots "
                f"allow {sorted(SNAPSHOT_OBS_ALLOWED_FIELDS)}"
            )
    for field in ('name', 'value'):
        if field not in obs:
            issues.append(f"  {label}: missing required field: {field}")

    if 'name' in obs and (
        not isinstance(obs['name'], str) or not obs['name'].strip()
    ):
        issues.append(f"  {label}.name: must be a non-empty string")

    # Snapshot observables use the total error pair only, never the
    # per-paper type@N_error triplets.
    for field in ('total_upper', 'total_lower'):
        if field not in obs:
            issues.append(f"  {label}: missing required field: {field}")

    # Snapshot numbers are JSON numbers, not float-strings (json-meta.md
    # §"Shared rules for both snapshots").
    for field in ('value', 'total_upper', 'total_lower'):
        if field in obs and (
            isinstance(obs[field], bool)
            or not isinstance(obs[field], (int, float))
        ):
            issues.append(
                f"  {label}.{field}: must be a number, "
                f"got {type(obs[field]).__name__}"
            )
    if 'unit' in obs and not isinstance(obs['unit'], str):
        issues.append(f"  {label}.unit: must be a string")
    elif 'unit' in obs:
        issues.extend(_scale_unit_issue(obs['unit'], label))

def _validate_snapshot_correlation(
    sub: dict, label: str, n_obs: int, issues: list[str]
) -> None:
    """Validate an optional subgroup-level correlation matrix."""
    correlation = sub.get('correlation')
    if correlation is None:
        return
    if not isinstance(correlation, list):
        issues.append(f"  {label}.correlation: expected a 2D array or null")
        return
    if len(correlation) != n_obs:
        issues.append(
            f"  {label}.correlation: dimension ({len(correlation)}x"
            f"{len(correlation)}) does not match observable count ({n_obs})"
        )
    issues.extend(
        validate_correlation(correlation, f"{label}.correlation")
    )


def _validate_pdg_subgroup(name: str, sub, issues: list[str]) -> None:
    label = f"data['{name}']"
    if not isinstance(sub, dict):
        issues.append(f"  {label}: must be an object of obs@N entries")
        return

    obs_keys = []
    for key in sub:
        if isinstance(key, str) and key.startswith('obs@'):
            try:
                int(key.split('@', 1)[1])
            except (ValueError, IndexError):
                issues.append(
                    f"  {label}: invalid obs key '{key}'; "
                    f"expected obs@N format (N as integer)"
                )
                continue
            obs_keys.append(key)
        elif key not in PDG_SUBGROUP_ALLOWED_FIELDS:
            issues.append(
                f"  {label}: unexpected key '{key}' "
                f"(only obs@N and 'correlation' allowed)"
            )

    if not obs_keys:
        issues.append(f"  {label}: no obs@N entries")
    for key in obs_keys:
        _validate_snapshot_obs(sub[key], f"{label}.{key}", issues)
    _validate_snapshot_correlation(sub, label, len(obs_keys), issues)


def _validate_hflav_subgroup(name: str, sub, issues: list[str]) -> None:
    label = f"'{name}'"
    if not isinstance(sub, dict):
        issues.append(f"  {label}: must be an object")
        return

    for key in sub:
        if key not in HFLAV_SUBGROUP_ALLOWED_FIELDS:
            issues.append(f"  {label}: unexpected key '{key}'")
    for field in ('group', 'observables'):
        if field not in sub:
            issues.append(f"  {label}: missing required field: {field}")
    if not sub.get('inspire-hep') and not sub.get('arxiv'):
        issues.append(f"  {label}: missing citation ('inspire-hep' or 'arxiv')")

    observables = sub.get('observables')
    if not isinstance(observables, list) or not observables:
        issues.append(f"  {label}.observables: must be a non-empty array")
        observables = []
    for idx, obs in enumerate(observables):
        _validate_snapshot_obs(
            obs, f"{label}.observables[{idx}]", issues
        )
    _validate_snapshot_correlation(sub, label, len(observables), issues)


def _validate_snapshot(data: dict, file_path: str, kind: str) -> list[str]:
    """Validate an HFLAV or PDG snapshot.

    See references/json-meta.md §"Non-Standard Schemas".
    """
    print(f"Validating (snapshot: {kind}): {file_path}")
    all_issues = []

    if kind == 'pdg':
        for field in (
            'inspire-hep', 'author', 'collaboration', 'title', 'year', 'data',
        ):
            if field not in data:
                all_issues.append(f"  Missing required field: {field}")
        year = data.get('year')
        if year is not None and not (
            isinstance(year, str) and re.fullmatch(r'\d{4}', year)
        ):
            all_issues.append("  year must be a four-digit string, e.g. '2024'")
        subgroups = data.get('data')
        if not isinstance(subgroups, dict):
            all_issues.append("  data: must be an object of subgroup entries")
        elif not subgroups:
            all_issues.append("  data dict is empty")
        else:
            for sub_name, sub in subgroups.items():
                _validate_pdg_subgroup(str(sub_name), sub, all_issues)
    else:
        if not data:
            all_issues.append("  snapshot is empty")
        for sub_name, sub in data.items():
            _validate_hflav_subgroup(str(sub_name), sub, all_issues)

    if all_issues:
        print(f"  [FAIL] Found {len(all_issues)} issue(s):")
        for issue in all_issues:
            print(issue)
    else:
        print("  [OK] Snapshot validated")
    return all_issues


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

    # Detect non-standard schema (HFLAV / PDG snapshots).
    snapshot_kind = _detect_snapshot(data)
    if snapshot_kind:
        return _validate_snapshot(data, file_path, snapshot_kind)

    # 2. Check top-level fields
    for field in REQUIRED_TOP_FIELDS:
        if field not in data:
            all_issues.append(f"  Missing required field: {field}")
        elif field != 'arxiv' and isinstance(data[field], str) and not data[field].strip():
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

    # 5. Check arxiv field format
    arxiv = data.get('arxiv')
    all_issues.extend(validate_arxiv_format(arxiv))

    # 6. Check transition-mode content
    if 'transition-mode' in data:
        all_issues.extend(validate_transition_mode(data['transition-mode']))

    # 7. Check data: an array of groups; each group maps transition
    # channels to their observables and optionally carries one matrix.
    if 'data' not in data:
        all_issues.append("  Missing required field: data")
    elif isinstance(data['data'], list):
        all_issues.extend(_validate_data_list(data['data']))
    else:
        all_issues.append(
            "  data must be an array of data groups, e.g. "
            "[{'B0.2.K*0.mu+.mu-': {'obs@1': {...}}, "
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
    """CLI entry point.

    Examples
    --------
    >>> python3 flav-data-importer/scripts/json-valid.py path/to/file.json
    >>> python3 flav-data-importer/scripts/json-valid.py a.json b.json c.json --quiet
    >>> python3 flav-data-importer/scripts/json-valid.py --help
    """
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
        help='Suppress per-file OK/FAIL banners; only print issues + summary.'
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
