#!/usr/bin/env python3
"""Validate flav-data JSON files against the schema in references/json-meta.md.

Usage:
    python3 json-valid.py <path/to/file.json> [path/to/file2.json ...] [--quiet]
"""

import json
import re
import sys
import os
import argparse

REQUIRED_TOP_FIELDS = [
    'inspire-hep', 'author', 'collaboration', 'title',
    'arxiv', 'time', 'abstract', 'pdf', 'transition-mode', 'data'
]

# Fields that must NOT appear in the JSON
FORBIDDEN_FIELDS = ['year']

# Standard measurement required fields
REQUIRED_OBS_FIELDS_WITH_VALUE = [
    'name', 'latex', 'value',
    'type@1_err', 'type@1_err_up', 'type@1_err_down'
]

# Upper limit format required fields
REQUIRED_OBS_FIELDS_WITH_UPPER = [
    'name', 'latex',
    'type@1_upper_limit', 'type@1_level'
]

# External reference format required fields
REQUIRED_OBS_FIELDS_WITH_REF = [
    'name', 'latex', 'value',
    'tot_err_up', 'tot_err_down', 'ref'
]

# Total error format required fields (without ref)
REQUIRED_OBS_FIELDS_WITH_TOT_ERR = [
    'name', 'latex', 'value',
    'tot_err_up', 'tot_err_down'
]

# Snapshot (HFLAV/PDG) observable fields. Unknown keys are rejected so
# the per-paper error formats (type@N_err, ref, ...) cannot leak into a
# snapshot. See references/json-meta.md §"Non-Standard Schemas".
SNAPSHOT_OBS_ALLOWED_FIELDS = {
    'name', 'latex', 'value',
    'error', 'error_up', 'error_down', 'tot_err_up', 'tot_err_down',
    'unit', 'limit',
}

# Standard measurement error labels (json-meta.md §"Standard error type
# labels"). Labels outside this set are rejected.
STANDARD_ERROR_LABELS = {
    'stat', 'syst', 'lumi', 'norm', 'theo', 'expe',
}

# Per-paper observable fields. ``type@N_*`` keys are matched by pattern;
# everything else must match exactly. Legacy-only spellings (``sta_err_up``,
# ``type@N_err_name``, ``method``, ``dataset``, ...) are rejected in the
# dict schema and tolerated only in legacy list-schema files.
OBS_EXACT_FIELDS = {
    'name', 'latex', 'value', 'unit', 'ref',
    'tot_err_up', 'tot_err_down',
}
_OBS_KEY_RE = re.compile(
    r'type@\d+_(?:err|err_up|err_down|upper_limit|level)$'
)
_NUMERIC_OBS_KEY_RE = re.compile(
    r'(?:value|type@\d+_(?:err_up|err_down|upper_limit)|'
    r'tot_err_up|tot_err_down)$'
)


def is_observable_field(key: str) -> bool:
    return (
        key in OBS_EXACT_FIELDS
        or key in DATA_ENTRY_KINEMATIC_FIELDS
        or bool(_OBS_KEY_RE.fullmatch(key))
    )

# transition-mode whitelist (json-meta.md §"transition-mode Values" table)
VALID_TRANSITION_MODES = [
    'leptonic decay',
    'semileptonic decay',
    'non-leptonic decay',
    'radiative decay',
    'neutron beta decay',
    'Higgs decay',
    'scattering',
]

# Basic observables that carry no transition (obs-abbr.md §2.1).
BASIC_OBSERVABLE_NAMES = {
    'MZ', 'MW', 'Mtop', 'MH', 'Mh',
    'R_b', 'R_c',
    '|Vtd|', '|Vts|', '|Vub|', '|Vcb|',
    'S_phigamma', 'C_phigamma', 'ADelta_phigamma',
    'gammaCKM', 'r', 'delta',
}

# Top-level fields allowed in the standard (per-paper) schema.
TOP_LEVEL_ALLOWED_FIELDS = set(REQUIRED_TOP_FIELDS)

# Snapshot schemas (json-meta.md §"Non-Standard Schemas").
PDG_SUBGROUP_ALLOWED_FIELDS = {'correlation'}
HFLAV_SUBGROUP_ALLOWED_FIELDS = {
    'group', 'arxiv', 'inspire-hep', 'description',
    'observables', 'correlation',
}

# Allowed field patterns within data entries
# Exact data-block keys (no substring matching): obs@N, type@N matrices,
# total matrices, and kinematic boundaries.
DATA_ENTRY_KINEMATIC_FIELDS = {
    'q2min', 'q2max', 'pTmin', 'pTmax', 'etamin', 'etamax',
}
_DATA_ENTRY_KEY_RE = re.compile(
    r'(?:obs@\d+|type@\d+_(?:correlation|covariance)|'
    r'(?:tot_)?(?:correlation|covariance))$'
)


def is_data_entry_key(key: str) -> bool:
    return key in DATA_ENTRY_KINEMATIC_FIELDS or bool(_DATA_ENTRY_KEY_RE.fullmatch(key))


# Observable categories for the dictionary-shaped ``data`` schema.
# One category per dictionary; angular coefficients and differential
# widths must not share a dict (SKILL.md rule 6).
OBSERVABLE_CATEGORIES = (
    'angular', 'differential', 'branching', 'asymmetry',
    'ratio', 'lifetime', 'mass-mixing', 'cross-section', 'other',
)

_ANGULAR_ABBREVIATIONS = {
    'FL', 'FS', 'FH', 'FT', 'Ft', 'AFB', 'AFBh', 'AFBl', 'AFBlh',
    'A0', 'A1c', 'A2s', 'A3', 'A4', 'A5', 'A6', 'A6c', 'A6p', 'A6s',
    'A7', 'A8', 'A9', 'S1ac', 'S1bcre', 'S1bcim', 'S1c', 'S2c', 'S2s',
    'S3', 'S4', 'S5', 'S6c', 'S7', 'S8', 'S9',
    'P1', 'P2', 'P3', 'P4p', 'P5p', 'P6c', 'P6cp', 'P6p', 'P8p',
    'DeltaFL', 'DeltaP1', 'DeltaP2', 'DeltaP3', 'DeltaP4p',
    'DeltaP5p', 'DeltaP6p', 'DeltaP8p', 'DeltaAFB',
    'AT2', 'ATIm', 'ATRe', 'ATodd',
    'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q8', 'QFL',
}
_ASYMMETRY_ABBREVIATIONS = {
    'ACP', 'DeltaACP', 'AC', 'AFB_CP', 'AFS', 'C', 'S',
    'S_phigamma', 'C_phigamma', 'ADelta_phigamma',
}
_BRANCHING_ABBREVIATIONS = {
    'Br', 'BR', 'BrW2had', 'Bsmu_gamma', 'Bsmu_gamma_exp',
    'rel_BF_pwave',
}
_RATIO_ABBREVIATIONS = {
    'r', 'r1', 'r2', 'Re/mu', 'Rmue', 'Rtaumu', 'fs/fd', 'fS/f+',
    'fT/f+', 'ge/gmu', 'gtauoverge',
}
_LIFETIME_ABBREVIATIONS = {'Tau', 'tau'}
_MASS_MIXING_ABBREVIATIONS = {
    'Mass', 'mass', 'MZ', 'MW', 'MH', 'Mh', 'M1', 'M2', 'M3', 'M4',
    'mW', 'mZ', 'mpole', 'dmW', 'DeltaMd', 'DeltaMs', 'DeltaMdGd',
    'DeltaMsGs', 'DeltaGamma', 'Gamma', 'GammaZ', 'GammaW',
}
_CROSS_SECTION_ABBREVIATIONS = {
    'Sigma', 'SigmaAFB', 'sigmaWtaunu', 'sigma_Wmenu', 'sigma_Wpenu',
    'sigma_had0', 'sigma',
}


def _observable_category(name: str) -> str:
    """Return the category of one observable name (first safe fallback)."""
    abbr = name.split('(', 1)[0].split('[', 1)[0].strip()
    if abbr in _ANGULAR_ABBREVIATIONS:
        return 'angular'
    if abbr in _ASYMMETRY_ABBREVIATIONS:
        return 'asymmetry'
    if abbr in _BRANCHING_ABBREVIATIONS:
        return 'branching'
    if abbr in _RATIO_ABBREVIATIONS or abbr.startswith('R'):
        return 'ratio'
    if abbr in _LIFETIME_ABBREVIATIONS:
        return 'lifetime'
    if abbr in _MASS_MIXING_ABBREVIATIONS:
        return 'mass-mixing'
    if abbr in _CROSS_SECTION_ABBREVIATIONS:
        return 'cross-section'
    # Prefix families: S1.../P1.../A3.../SS.../AS... are angular.
    if re.fullmatch(r'(?:S\d.*|P\d.*|A\d.*|SS\d.*|AS\d.*)', abbr):
        return 'angular'
    # Differential dX/dY or dX forms (dBr, dBr/dq2, dGdw, ...).
    if (('/d' in abbr) or abbr.startswith('d')) and not abbr.startswith(('Delta', 'dm')):
        return 'differential'
    return 'other'


# --- Canonical transition ordering (obs-abbr.md §1) -------------------
# Particle tokens are classified into the four orderable types from the
# spec. Hadrons keep their conventional capitalisation; leptons and light
# mesons stay lowercase (e+, mu-, pi-, nu).
_BARYON_STEMS = (
    'Lambdac', 'Lambdab', 'Lambda', 'Sigma', 'Xic', 'Xib',
    'Omegac', 'Omega', 'Xi',
)
_MESON_STEMS = (
    'J/psi', 'psi', 'Kstar', 'Kst', 'Bc', 'Bs0', 'B0s', 'B0', 'B',
    'Dst', 'D*', 'Ds', 'D0', 'D', 'KS0', 'K0S', 'K0L', 'K0s', 'K0bar',
    'K0', 'K', 'pi', 'rho', 'phi', 'omega', 'eta', 'Xs', 'Xce', 'Xcl', 'f',
)
_MESON_CHARGED_STEMS = ('B', 'Bc', 'D', 'Dst', 'D*', 'Ds', 'K', 'Kst', 'Kstar', 'pi', 'rho')
_LEP_STEMS = ('mu', 'tau', 'e', 'l')
_NEUTRAL_MESONS = {
    'J/psi', 'psi', 'phi', 'omega', 'eta', 'etaprime', 'Xs', 'Xce', 'Xcl',
    'f', 'D0', 'B0', 'B0s', 'Bs0', 'K0', 'Kst0', 'Dst0', 'D*0', 'Bbar',
    'K0bar', 'K0S', 'K0L', 'KS0', 'K0s', 'B0Bar',
}
_NEUTRAL_LEPTONS = {
    'nu', 'nuBar', 'nubar', 'nue', 'numu', 'nutau',
    'nuebar', 'numubar', 'nutaubar',
}
_TYPE_NAMES = {
    1: 'baryon', 2: 'meson', 3: 'charged lepton', 4: 'neutral lepton',
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
    # Handles both ``K0Bar`` and the legacy ``LambdacBar-`` placement.
    return re.sub(r'(?:Bar|bar)(?=[+\-]?$)', '', token)


def _strip_resonance(token: str) -> str:
    """Drop the trailing ``(2.l+.l-)`` resonance-decay annotation."""
    return re.sub(r'\(2\.[^()]*\)$', '', token)


def _particle_mass(token: str) -> float | None:
    """Return the particle mass in GeV, or ``None`` when it is unknown."""
    stem = _strip_resonance(_strip_bar(token))
    if stem in _PARTICLE_MASS:
        return _PARTICLE_MASS[stem]
    # Antiparticles share the mass of their partner.
    if stem.endswith('-') and stem[:-1] + '+' in _PARTICLE_MASS:
        return _PARTICLE_MASS[stem[:-1] + '+']
    if stem.endswith('+') and stem[:-1] + '-' in _PARTICLE_MASS:
        return _PARTICLE_MASS[stem[:-1] + '-']
    if stem.endswith('p') and stem[:-1] + '+' in _PARTICLE_MASS:
        return _PARTICLE_MASS[stem[:-1] + '+']
    if stem.endswith('m') and stem[:-1] + '-' in _PARTICLE_MASS:
        return _PARTICLE_MASS[stem[:-1] + '-']
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


def _charge_rank(token: str, stem: str, charged_stems: tuple[str, ...]) -> int | None:
    """Return ordering rank for charge: + -> 0, - -> 1, 0 -> 2."""
    if token.endswith('+'):
        return 0
    if token.endswith('-'):
        return 1
    if stem in charged_stems:
        if token.endswith('p'):
            return 0
        if token.endswith('m'):
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

    stem = _strip_bar(token)
    if stem in _NON_ORDERABLE:
        return None, None
    if stem in ('p', 'n'):
        if token == 'p':
            return 1, 0
        if token in ('pBar', 'pbar'):
            return 1, 1
        if token in ('n', 'nBar', 'nbar'):
            return 1, 2
        return 1, None
    if stem.startswith(_BARYON_STEMS):
        charge = _charge_rank(token, stem, ())
        if charge is None and ('0' in stem or stem in ('Lambda', 'Lambdab')):
            charge = 2
        return 1, charge

    core = re.sub(r'[+\-]$', '', stem)
    if core.endswith(('p', 'm')) and core[:-1] in _LEP_STEMS:
        core = core[:-1]
    if core in _LEP_STEMS:
        if core == 'l' and not token.endswith(('+', '-', 'p', 'm')):
            # Bare generic lepton: its charge is unknown, so skip the state.
            return None, None
        return 3, _charge_rank(token, core, _LEP_STEMS)

    if stem.startswith(_MESON_STEMS):
        charge = _charge_rank(token, stem, _MESON_CHARGED_STEMS)
        if charge is None and (
            token in _NEUTRAL_MESONS
            or stem in _NEUTRAL_MESONS
            or '0' in stem
            or stem.endswith('bar')
        ):
            charge = 2
        return 2, charge

    return None, None


def _transition_body(name: str) -> str | None:
    """Return the text inside the first balanced ``(...)`` pair, sans condition."""
    start = name.find('(')
    if start < 0:
        return None
    depth = 0
    for index in range(start, len(name)):
        char = name[index]
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
            if depth == 0:
                return name[start + 1:index].split('[', 1)[0]
    return None


def _transition_order_issues(name: str) -> list[str]:
    """Flag non-canonical ordering inside dotted ``A.B.2.C.D`` transitions.

    Applies the obs-abbr.md §1 rules: within each state, order by particle
    type (baryon -> meson -> charged lepton -> neutral lepton), then by
    mass (heaviest -> lightest), and by charge (+ -> - -> 0) for particles
    of equal mass. Compact legacy forms without ``.2.`` are skipped.
    """
    body = _transition_body(name)
    if not body or '.2.' not in body:
        return []
    return _order_issues_for_body(body, f"Observable '{name}'")


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
    stages = _split_top_level(body, '.2.')
    for stage in stages:
        tokens = _split_top_level(stage, '.')
        classified = [_classify_particle(token) for token in tokens]
        types = [entry[0] for entry in classified]
        charges = [entry[1] for entry in classified]
        masses = [_particle_mass(token) for token in tokens]

        for token, (type_rank, _) in zip(tokens, classified):
            if _particle_mass(token) is None and token not in _NEUTRAL_LEPTONS:
                stem = _strip_bar(token)
                if stem in _NON_ORDERABLE or token in _NON_ORDERABLE:
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


def validate_transition_symbol(name: str) -> list[str]:
    """Check that the observable name has the expected OBS(transition)[condition] shape.

    Three shapes are accepted (see obs-abbr.md):

    1. **Basic observable** (no transition): ``OBS(particle)`` — e.g.
       ``Tau(e-)``, ``Mass(Z)``, ``MZ``, ``gammaCKM``, ``|Vtd|``.
    2. **Composite observable** (with transition): ``OBS(transition)`` —
       e.g. ``Br(B+2K+mumu)``, ``RBr(B+.2.K+.l+.l-)``. Dotted ``.2.``
       transitions must follow the canonical particle order
       (baryon -> meson -> charged lepton -> neutral lepton, then
       heaviest -> lightest within each type, then ``+`` -> ``-`` -> ``0``
       for equal masses); compact legacy forms are accepted.
    3. **Multi-transition observable** (with condition only):
       ``OBS[condition]`` — e.g. ``RK+[mu/e]``, ``RDst+[tau/mu]``,
       ``fs/fd``. The condition is given without a transition symbol.
    """
    issues = []
    # Extract OBS prefix (e.g. "Tau", "Mass", "Br", "FL")
    obs_prefix = name.split('(', 1)[0] if '(' in name else ''
    # Basic observables (no transition symbol needed): see obs-abbr.md §2.1
    if obs_prefix in ('Tau', 'Mass', 'mass'):
        return issues
    # Basic observables without OBS(particle) pattern but documented in
    # obs-abbr.md §2.1 (CKM elements, LEP pseudo-observables, etc.).
    if name in BASIC_OBSERVABLE_NAMES:
        return issues
    # Ratios without a transition (legacy compact form): fs/fd, ge/gmu, etc.
    if '/' in name and '(' not in name and '[' not in name:
        return issues
    # Composite observable (parens present) or multi-transition (brackets
    # present) — both valid. Only complain if neither is present.
    has_parens = bool(re.search(r'\([^)]+\)', name))
    has_brackets = bool(re.search(r'\[[^\]]+\]', name))
    if not (has_parens or has_brackets):
        issues.append(
            f"  Observable '{name}' has no transition symbol (expected "
            f"OBS(transition)) and no condition (expected OBS[condition])"
        )
        return issues

    issues.extend(_transition_order_issues(name))
    return issues


def validate_latex(text: str, field_name: str, obs_key: str) -> list[str]:
    """Check that the LaTeX field is non-empty and Unicode-free.

    Per SKILL.md rule 4 and json-meta.md §"Key Constraints" rule 12,
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


def validate_correlation(matrix: list, label: str, is_covariance: bool = False) -> list[str]:
    """Check correlation matrix: symmetric with diagonal = 1.0.
    Covariance matrix: only symmetry (diagonal = err², verified manually)."""
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
    # Check element types
    for i in range(n):
        for j in range(n):
            if not isinstance(matrix[i][j], (int, float)):
                issues.append(
                    f"  {label}: matrix element [{i}][{j}] "
                    f"is not numeric (type: {type(matrix[i][j]).__name__})"
                )
                return issues
    for i in range(n):
        if not is_covariance:
            if abs(matrix[i][i] - 1.0) > 0.001:
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


def validate_data_entry_fields(entry: dict, label: str) -> list[str]:
    """Check that the data block contains only allowed field patterns and that
    kinematic boundary fields are well-formed."""
    issues = []
    for key in entry:
        if not is_data_entry_key(key):
            issues.append(
                f"  {label}: disallowed field '{key}'; data entries may only "
                f"contain obs@N, type@N_correlation, type@N_covariance, "
                f"tot_correlation, tot_covariance, and kinematic boundaries "
                f"({sorted(DATA_ENTRY_KINEMATIC_FIELDS)})"
            )
    # Validate kinematic boundary fields (q2min/q2max, pTmin/pTmax, etamin/etamax)
    # must be float-string (or comma-separated float-strings, or '+inf' for
    # unbounded sides). Per json-meta.md §Combined Kinematic Bins.
    for key in entry:
        if key not in DATA_ENTRY_KINEMATIC_FIELDS:
            continue
        issues.extend(_kinematic_issues(entry[key], f"{label}.{key}"))
    return issues


def _is_float_string(text) -> bool:
    if not isinstance(text, str) or not text.strip():
        return False
    try:
        float(text)
    except ValueError:
        return False
    return True


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


def _validate_error_triplets(obs: dict, label: str) -> list[str]:
    """Every ``type@N_err`` label needs the full ``_err/_err_up/_err_down``
    triplet and a whitelisted label."""
    issues = []
    tags = sorted({
        key.split('_', 1)[0]
        for key in obs
        if re.fullmatch(r'type@\d+_err(?:_up|_down)?', key)
    })
    for tag in tags:
        base, up, down = f'{tag}_err', f'{tag}_err_up', f'{tag}_err_down'
        missing = [key for key in (base, up, down) if key not in obs]
        if missing:
            issues.append(
                f"  {label}: incomplete error triplet for '{tag}'; missing "
                f"{missing}; each component error requires '{base}', "
                f"'{up}' and '{down}' together"
            )
            continue
        value = obs[base]
        if not isinstance(value, str) or not value.strip():
            issues.append(
                f"  {label}.{base}: error label must be a non-empty string"
            )
        elif value.strip() not in STANDARD_ERROR_LABELS:
            issues.append(
                f"  {label}.{base}: unknown error label '{value}'; allowed "
                f"labels are {sorted(STANDARD_ERROR_LABELS)}"
            )
    return issues


def _validate_upper_limit_pairs(obs: dict, label: str) -> list[str]:
    issues = []
    for key in obs:
        match = re.fullmatch(r'(type@\d+)_(upper_limit|level)', key)
        if not match:
            continue
        tag, kind = match.groups()
        sibling = kind == 'upper_limit' and f'{tag}_level' or f'{tag}_upper_limit'
        if sibling not in obs:
            issues.append(
                f"  {label}: '{key}' present but missing '{sibling}'; every "
                f"upper limit needs both '_upper_limit' (value) and '_level' "
                f"(confidence level)"
            )
    return issues


def _validate_measurement_scheme(obs: dict, label: str) -> list[str]:
    """Enforce exactly one measurement format (SKILL.md checklist)."""
    issues = []
    has_value = 'value' in obs
    has_component = any(re.fullmatch(r'type@\d+_err', key) for key in obs)
    has_total = 'tot_err_up' in obs or 'tot_err_down' in obs
    has_upper = any(key.endswith('_upper_limit') for key in obs)
    has_ref = 'ref' in obs

    if has_component and has_total:
        issues.append(
            f"  {label}: mixes component errors (type@N_err) with "
            f"tot_err_up/tot_err_down; use exactly one error scheme"
        )
    if has_ref and not has_total:
        issues.append(
            f"  {label}: 'ref' is only valid together with "
            f"tot_err_up/tot_err_down (external reference format)"
        )
    if has_upper and not has_value and (has_component or has_total):
        issues.append(
            f"  {label}: upper-limit-only entries must not carry value or "
            f"errors; use the combined format (value + tot_err) when a fit "
            f"result is also reported"
        )
    if has_value and has_upper and not has_total:
        issues.append(
            f"  {label}: value + upper limit requires "
            f"tot_err_up/tot_err_down (combined fit + limit format)"
        )
    if has_value and not (has_component or has_total or has_upper):
        issues.append(
            f"  {label}: measurement has no error; add a type@N_err triplet "
            f"or tot_err_up/tot_err_down"
        )
    if not has_value and not has_upper:
        issues.append(
            f"  {label}: missing 'value' or type@N_upper_limit"
        )
    return issues


def _validate_observable(
    obs, label: str, *, transition_key: str | None = None,
    category: str | None = None, strict: bool = False,
) -> list[str]:
    """Validate one ``obs@N`` object.

    ``strict`` is used for the dict-shaped schema (new files): unknown
    fields are rejected, error triplets and labels are enforced, and
    exactly one measurement format is required. Legacy list-schema files
    keep the earlier permissive checks so they can be migrated later.
    """
    if not isinstance(obs, dict):
        return [f"  {label}: must be an object"]

    issues = []

    if strict:
        for key in obs:
            if not is_observable_field(key):
                issues.append(
                    f"  {label}: unknown observable field '{key}'; allowed "
                    f"fields are {sorted(OBS_EXACT_FIELDS)} plus "
                    f"type@N_err/type@N_err_up/type@N_err_down/"
                    f"type@N_upper_limit/type@N_level"
                )
        for field in ('name', 'latex'):
            if field not in obs:
                issues.append(f"  {label}: missing required field: {field}")
        issues.extend(_validate_error_triplets(obs, label))
        issues.extend(_validate_upper_limit_pairs(obs, label))
        has_tot_up = 'tot_err_up' in obs
        if has_tot_up != ('tot_err_down' in obs):
            missing = 'tot_err_down' if has_tot_up else 'tot_err_up'
            issues.append(
                f"  {label}: total error is one-sided; missing '{missing}'"
            )
        issues.extend(_validate_measurement_scheme(obs, label))
    else:
        # Legacy permissive format checks (priority-based).
        has_value = 'value' in obs
        has_upper = any(key.endswith('_upper_limit') for key in obs)
        has_ref = 'ref' in obs and 'tot_err_up' in obs
        has_tot_err = 'tot_err_up' in obs and 'tot_err_down' in obs
        if has_ref and has_value:
            required = REQUIRED_OBS_FIELDS_WITH_REF
        elif has_tot_err and has_upper and has_value:
            required = (
                REQUIRED_OBS_FIELDS_WITH_TOT_ERR
                + [f for f in REQUIRED_OBS_FIELDS_WITH_UPPER if f not in REQUIRED_OBS_FIELDS_WITH_TOT_ERR]
            )
        elif has_tot_err and has_value:
            required = REQUIRED_OBS_FIELDS_WITH_TOT_ERR
        elif has_upper:
            required = REQUIRED_OBS_FIELDS_WITH_UPPER
        elif has_value:
            required = REQUIRED_OBS_FIELDS_WITH_VALUE
        else:
            required = []
            issues.append(
                f"  {label}: missing 'value' or 'type@1_upper_limit' field"
            )
        for field in required:
            if field not in obs:
                issues.append(f"  {label}: missing required field: {field}")

        # Legacy: pair any *_err_up / *_err_down (including sta_/sys_).
        for key in obs:
            if key.endswith('_err_up'):
                sibling = key[:-7] + '_err_down'
            elif key.endswith('_err_down'):
                sibling = key[:-9] + '_err_up'
            else:
                continue
            if sibling not in obs:
                issues.append(
                    f"  {label}: '{key}' present but missing '{sibling}'"
                )

    if 'name' in obs and (
        not isinstance(obs['name'], str) or not obs['name'].strip()
    ):
        issues.append(f"  {label}.name: must be a non-empty string")

    for key in obs:
        if key == 'unit':
            if not isinstance(obs[key], str) or not obs[key].strip():
                issues.append(f"  {label}.{key}: must be a non-empty string")
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
        elif strict and not _is_float_string(obs[key]):
            issues.append(
                f"  {label}.{key}: expected a float-as-string, "
                f"got {obs[key]!r}"
            )

    for key in obs:
        if key in DATA_ENTRY_KINEMATIC_FIELDS:
            issues.extend(_kinematic_issues(obs[key], f"{label}.{key}"))

    if 'latex' in obs and isinstance(obs['latex'], str):
        issues.extend(validate_latex(obs['latex'], 'latex', label))

    if 'name' in obs and isinstance(obs['name'], str):
        issues.extend(validate_transition_symbol(obs['name']))
        if strict and transition_key is not None:
            body = _transition_body(obs['name'])
            dotted = body if body and '.2.' in body else None
            if transition_key == 'no-transition':
                if dotted is not None:
                    issues.append(
                        f"  {label}: observable '{obs['name']}' belongs to "
                        f"transition '{dotted}', not 'no-transition'"
                    )
            elif dotted != transition_key:
                issues.append(
                    f"  {label}: observable '{obs['name']}' transition "
                    f"'{dotted or 'none'}' does not match data key "
                    f"'{transition_key}'"
                )
        if strict and category is not None and category != 'other':
            inferred = _observable_category(obs['name'])
            if inferred != 'other' and inferred != category:
                issues.append(
                    f"  {label}: observable '{obs['name']}' looks like "
                    f"category '{inferred}' but is filed under '{category}'"
                )

    return issues


def _validate_data_entry(
    entry, label: str, *, transition_key: str | None = None,
    category: str | None = None, strict: bool = False,
) -> list[str]:
    """Validate one data group: allowed fields, obs@N numbering, matrices."""
    issues = []
    if not isinstance(entry, dict):
        return [f"  {label}: must be an object"]
    issues.extend(validate_data_entry_fields(entry, label))

    obs_keys = []
    for key in entry:
        if not key.startswith('obs@'):
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

    # Numbering must start at 1 and run 1..N with no gaps. A gap almost
    # always means an obs was deleted without updating the matrices.
    if obs_nums:
        expected = list(range(1, len(obs_nums) + 1))
        if obs_nums != expected:
            missing = [num for num in expected if num not in obs_nums]
            issues.append(
                f"  {label}: obs@N numbering is not contiguous; found "
                f"{obs_nums}, expected 1..{len(obs_nums)}; missing "
                f"obs@{missing}"
            )

    if not obs_keys:
        has_matrix = any(
            'correlation' in key.lower() or 'covariance' in key.lower()
            for key in entry
        )
        if not has_matrix:
            issues.append(f"  {label}: no obs@N entries")
        return issues

    for obs_key in obs_keys:
        issues.extend(_validate_observable(
            entry[obs_key], f"{label}.{obs_key}",
            transition_key=transition_key, category=category,
            strict=strict,
        ))

    for corr_key in entry:
        if 'correlation' not in corr_key.lower() and 'covariance' not in corr_key.lower():
            continue
        if entry[corr_key] is None:
            continue  # null means no matrix — acceptable
        if not isinstance(entry[corr_key], list):
            issues.append(f"  {corr_key}: expected 2D array")
            continue
        matrix = entry[corr_key]
        is_covariance = 'covariance' in corr_key.lower()
        issues.extend(validate_correlation(matrix, label, is_covariance))
        if len(matrix) != len(obs_keys):
            issues.append(
                f"  {label}: matrix dimension "
                f"({len(matrix)}x{len(matrix)}) does not match "
                f"observable count ({len(obs_keys)})"
            )
    return issues


def _validate_legacy_data_list(entries: list) -> list[str]:
    issues = []
    if not entries:
        issues.append("  data array is empty")
    for entry_idx, entry in enumerate(entries):
        issues.extend(_validate_data_entry(entry, f"data[{entry_idx}]"))
    return issues


def _validate_data_dict(data_map: dict) -> list[str]:
    """Validate the dict-shaped schema: transition -> category -> entries."""
    issues = []
    if not data_map:
        issues.append("  data dict is empty")
    for key, categories in data_map.items():
        if not isinstance(key, str):
            issues.append(f"  data key {key!r}: must be a string")
            continue
        issues.extend(validate_transition_key(key))
        if not isinstance(categories, dict):
            issues.append(
                f"  data['{key}']: must be an object mapping observable "
                f"categories to lists"
            )
            continue
        if not categories:
            issues.append(
                f"  data['{key}']: must contain at least one observable "
                f"category"
            )
            continue
        for category, entries in categories.items():
            if category not in OBSERVABLE_CATEGORIES:
                issues.append(
                    f"  data['{key}']: unknown category '{category}'; "
                    f"allowed categories are {list(OBSERVABLE_CATEGORIES)}"
                )
                continue
            if not isinstance(entries, list) or not entries:
                issues.append(
                    f"  data['{key}']['{category}']: must be a non-empty "
                    f"list of data entries"
                )
                continue
            for entry_idx, entry in enumerate(entries):
                issues.extend(_validate_data_entry(
                    entry,
                    f"data['{key}']['{category}'][{entry_idx}]",
                    transition_key=key, category=category, strict=True,
                ))
    return issues


def validate_transition_mode(value: str) -> list[str]:
    """Check that transition-mode matches one of the 7 valid values."""
    issues = []
    if not isinstance(value, str) or not value.strip():
        issues.append("  transition-mode must be a non-empty string")
        return issues
    normalized = {mode.lower() for mode in VALID_TRANSITION_MODES}
    if value.lower() not in normalized:
        issues.append(
            f"  transition-mode '{value}' is not in the allowed list: "
            f"{VALID_TRANSITION_MODES}; use property-based names like "
            f"'semileptonic decay', 'scattering', etc."
        )
    return issues


def _detect_snapshot(data: dict) -> str | None:
    """Return ``'pdg'``, ``'hflav'``, or ``None`` for a non-snapshot file.

    PDG: top-level ``data`` is a dict of subgroups whose keys are ``obs@N``
    (sparse) plus an optional ``correlation``. Standard dict-schema files
    have transitions (``A.B.2.C.D``) as their ``data`` keys, so the two
    shapes are unambiguous. HFLAV: no top-level ``data``; each top-level
    value is a subgroup containing an ``observables`` list.
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

    # Snapshot observables use exactly one error form, never the
    # per-paper type@N_err triplets.
    has_error = 'error' in obs
    has_error_pair = 'error_up' in obs and 'error_down' in obs
    has_tot_pair = 'tot_err_up' in obs and 'tot_err_down' in obs
    if sum((has_error, has_error_pair, has_tot_pair)) > 1:
        issues.append(
            f"  {label}: use exactly one error form "
            f"('error', 'error_up'/'error_down', or "
            f"'tot_err_up'/'tot_err_down')"
        )

    # Snapshot numbers are JSON numbers, not float-strings (json-meta.md
    # §"Shared rules for both snapshots").
    for field in (
        'value', 'error', 'error_up', 'error_down',
        'tot_err_up', 'tot_err_down',
    ):
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

    if not (has_error or has_error_pair or has_tot_pair):
        if 'error_up' in obs:
            issues.append(f"  {label}: 'error_up' present but missing 'error_down'")
        elif 'error_down' in obs:
            issues.append(f"  {label}: 'error_down' present but missing 'error_up'")
        elif 'tot_err_up' in obs:
            issues.append(f"  {label}: 'tot_err_up' present but missing 'tot_err_down'")
        elif 'tot_err_down' in obs:
            issues.append(f"  {label}: 'tot_err_down' present but missing 'tot_err_up'")
        else:
            issues.append(
                f"  {label}: missing 'error', 'error_up'/'error_down', "
                f"or 'tot_err_up'/'tot_err_down'"
            )

    if 'latex' in obs and isinstance(obs['latex'], str):
        issues.extend(validate_latex(obs['latex'], 'latex', label))


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
    all_issues = []

    # 1. Parse JSON
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("  [OK] JSON format correct")
    except json.JSONDecodeError as e:
        print(f"  [FAIL] JSON parse error: {e}")
        return [f"JSON parse error: {e}"]

    # Check top-level type before inspecting schema-specific fields.
    if not isinstance(data, dict):
        print(f"  [FAIL] Top-level JSON must be an object, got {type(data).__name__}")
        return [f"Top-level JSON must be an object, got {type(data).__name__}"]

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
    if not all_issues:
        print("  [OK] Top-level fields complete")

    # 2b. Check Unicode-free LaTeX in title and abstract (per SKILL.md rule 4
    # and json-meta.md §"Key Constraints" rule 12).
    for field in ('title', 'abstract'):
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

    # 7. Check data. New files use a dict keyed by transition channel
    # (transition -> category -> entries); the legacy list schema stays
    # accepted until the existing files are migrated.
    if 'data' not in data:
        all_issues.append("  Missing required field: data")
    elif isinstance(data['data'], dict):
        all_issues.extend(_validate_data_dict(data['data']))
    elif isinstance(data['data'], list):
        all_issues.extend(_validate_legacy_data_list(data['data']))
    else:
        all_issues.append(
            "  data must be an object keyed by transition channel "
            "(A.B.2.C.D or 'no-transition'); legacy files may still use "
            "an array of data groups"
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
