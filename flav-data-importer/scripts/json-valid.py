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
    'inspire-hep', 'author', 'title',
    'arxiv', 'time', 'abstract', 'transition-mode', 'data'
]

# ``collaboration`` is required only for named collaborations (experiments
# and large theory groups). Individual/small-group papers omit it entirely.
CONDITIONAL_TOP_FIELDS = ['collaboration']

# Fields that must NOT appear in the JSON
FORBIDDEN_FIELDS = ['year', 'pdf']

# Snapshot (HFLAV/PDG) observable fields. Unknown keys are rejected so
# the per-paper error formats (type@N_error, ref, ...) cannot leak into a
# snapshot. See references/json-meta.md §"Non-Standard Schemas".
SNAPSHOT_OBS_ALLOWED_FIELDS = {
    'name', 'value',
    'error', 'error_upper', 'error_lower',
    'unit', 'limit',
}

# Standard measurement error labels (json-meta.md §"Standard error type
# labels"). Labels outside this set are rejected.
STANDARD_ERROR_LABELS = {
    'stat', 'syst', 'lumi', 'norm', 'theo', 'expe',
}

# Per-paper observable fields. ``type@N_*`` keys are matched by pattern;
# everything else must match exactly.
OBS_EXACT_FIELDS = {
    'name', 'value', 'unit', 'ref',
    'error_upper', 'error_lower',
    # Optional provenance metadata carried over from imported papers.
    'method', 'dataset', 'note',
}
_OBS_KEY_RE = re.compile(
    r'type@\d+_(?:error|upper|lower|upper_limit|level)$'
)
_NUMERIC_OBS_KEY_RE = re.compile(
    r'(?:value|type@\d+_(?:upper|lower|upper_limit)|'
    r'error_upper|error_lower)$'
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
    parts = _split_top_level(body, '/')
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


def validate_observable_name(name: str) -> list[str]:
    """Check that the observable name does not embed a transition channel.

    The channel is carried by the ``data`` key. Names are the observable
    symbol, optionally followed by a condition or a method/parameter tag:
    ``OBS``, ``OBS[condition]``, ``OBS(method)``, ``f+.Vcs``.
    """
    issues = []
    for _, _, body in _parenthetical_blocks(name):
        if _looks_like_transition(body):
            issues.append(
                f"  Observable '{name}': name must not embed the transition "
                f"channel ('{body}'); the data key already carries it"
            )
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


def _validate_channel_entry(
    channel, label: str, channel_key: str
) -> tuple[list[str], int]:
    """Validate one channel entry: ``[latex, obs@N object]``.

    The first element is the channel's LaTeX expression, empty only for
    ``no-transition``. The second element holds only ``obs@N`` entries;
    kinematic bounds belong inside the observable. Returns the issues and
    the observable count, which feeds the group matrix dimension check.
    """
    issues = []
    if not isinstance(channel, list) or len(channel) != 2:
        return [
            f"  {label}: must be a 2-element array "
            f"[latex, obs@N object]"
        ], 0

    channel_latex, obs_bundle = channel
    if not isinstance(channel_latex, str):
        issues.append(f"  {label}[0]: channel LaTeX must be a string")
    elif channel_key == 'no-transition':
        if channel_latex.strip():
            issues.append(
                f"  {label}[0]: channel LaTeX must be empty for "
                f"'no-transition'"
            )
    elif not channel_latex.strip():
        issues.append(f"  {label}[0]: channel LaTeX must not be empty")
    else:
        issues.extend(validate_latex(channel_latex, 'latex', f"{label}[0]"))

    if not isinstance(obs_bundle, dict):
        issues.append(f"  {label}[1]: must be an object of obs@N entries")
        return issues, 0

    obs_keys = []
    for key in obs_bundle:
        if not re.fullmatch(r'obs@\d+', key):
            issues.append(
                f"  {label}[1]: disallowed field '{key}'; the channel's "
                f"second element holds only obs@N entries — put kinematic "
                f"bounds inside the observable and matrices at the group "
                f"level"
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
            obs_bundle[obs_key], f"{label}[1].{obs_key}",
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
    """Every ``type@N_error`` label needs the full
    ``_error/_upper/_lower`` triplet and a whitelisted label."""
    issues = []
    tags = sorted({
        key.split('_', 1)[0]
        for key in obs
        if re.fullmatch(r'type@\d+_(?:error|upper|lower)', key)
    })
    for tag in tags:
        base, up, down = f'{tag}_error', f'{tag}_upper', f'{tag}_lower'
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
    has_component = any(re.fullmatch(r'type@\d+_error', key) for key in obs)
    has_total = 'error_upper' in obs or 'error_lower' in obs
    has_upper = any(key.endswith('_upper_limit') for key in obs)

    if has_component and has_total:
        issues.append(
            f"  {label}: mixes component errors (type@N_error) with "
            f"error_upper/error_lower; use exactly one error scheme"
        )
    if has_upper and not has_value and (has_component or has_total):
        issues.append(
            f"  {label}: upper-limit-only entries must not carry value or "
            f"errors; use the combined format (value + errors) when a fit "
            f"result is also reported"
        )
    if has_value and has_upper and not (has_component or has_total):
        issues.append(
            f"  {label}: value + upper limit requires component errors "
            f"(type@N_error) or error_upper/error_lower"
        )
    if has_value and not (has_component or has_total or has_upper):
        issues.append(
            f"  {label}: measurement has no error; add a type@N_error triplet "
            f"or error_upper/error_lower"
        )
    if not has_value and not has_upper:
        issues.append(
            f"  {label}: missing 'value' or type@N_upper_limit"
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
                f"type@N_error/type@N_upper/type@N_lower/"
                f"type@N_upper_limit/type@N_level"
            )
    if 'name' not in obs:
        issues.append(f"  {label}: missing required field: name")
    issues.extend(_validate_error_triplets(obs, label))
    issues.extend(_validate_upper_limit_pairs(obs, label))
    has_tot_up = 'error_upper' in obs
    if has_tot_up != ('error_lower' in obs):
        missing = 'error_lower' if has_tot_up else 'error_upper'
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

    for key in ('method', 'dataset', 'note'):
        if key in obs and (
            not isinstance(obs[key], str) or not obs[key].strip()
        ):
            issues.append(f"  {label}.{key}: must be a non-empty string")

    if 'name' in obs and isinstance(obs['name'], str):
        issues.extend(validate_observable_name(obs['name']))

    return issues


def _validate_data_group(group, label: str) -> list[str]:
    """Validate one data group: channel bundles plus group-level matrices.

    A group is an object whose non-matrix keys are transition channels
    (each mapping to a ``[latex, obs@N object]`` pair) and whose optional
    ``correlation``/``covariance`` matrix aligns with the observables of
    all channels, flattened in channel order then ``obs@N`` order.
    """
    issues = []
    if not isinstance(group, dict):
        return [f"  {label}: must be an object"]

    matrix_keys = []
    channel_count = 0
    obs_total = 0
    saw_matrix = False
    for key in group:
        if is_group_matrix_key(key):
            matrix_keys.append(key)
            saw_matrix = True
            continue
        if saw_matrix:
            issues.append(
                f"  {label}: channel '{key}' appears after a matrix key; "
                f"keep all channel keys first so the matrix ordering is "
                f"unambiguous"
            )
        channel_count += 1
        issues.extend(validate_transition_key(key))
        channel_issues, obs_count = _validate_channel_entry(
            group[key], f"{label}['{key}']", key,
        )
        issues.extend(channel_issues)
        obs_total += obs_count

    if not channel_count:
        issues.append(
            f"  {label}: no transition channel; every data group needs at "
            f"least one channel key (or 'no-transition')"
        )

    for key in matrix_keys:
        matrix = group[key]
        if matrix is None:
            continue  # null means no matrix — acceptable
        if not isinstance(matrix, list):
            issues.append(f"  {label}['{key}']: expected 2D array")
            continue
        issues.extend(
            validate_correlation(
                matrix, f"{label}['{key}']",
                is_covariance='covariance' in key,
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
    appear in several groups to separate fit methods, kinematic bins, or
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

    # Snapshot observables use exactly one error form, never the
    # per-paper type@N_error triplets.
    has_error = 'error' in obs
    has_error_pair = 'error_upper' in obs and 'error_lower' in obs
    if sum((has_error, has_error_pair)) > 1:
        issues.append(
            f"  {label}: use exactly one error form "
            f"('error' or 'error_upper'/'error_lower')"
        )

    # Snapshot numbers are JSON numbers, not float-strings (json-meta.md
    # §"Shared rules for both snapshots").
    for field in (
        'value', 'error', 'error_upper', 'error_lower',
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

    if not (has_error or has_error_pair):
        if 'error_upper' in obs:
            issues.append(f"  {label}: 'error_upper' present but missing 'error_lower'")
        elif 'error_lower' in obs:
            issues.append(f"  {label}: 'error_lower' present but missing 'error_upper'")
        else:
            issues.append(
                f"  {label}: missing 'error' or "
                f"'error_upper'/'error_lower'"
            )

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

    # 7. Check data: an array of groups; each group maps transition
    # channels to their observables and optionally carries one matrix.
    if 'data' not in data:
        all_issues.append("  Missing required field: data")
    elif isinstance(data['data'], list):
        all_issues.extend(_validate_data_list(data['data']))
    else:
        all_issues.append(
            "  data must be an array of data groups, e.g. "
            "[{'B0.2.Kst0.mu+.mu-': ['$B^{0}\\\\to K^{*0}\\\\mu^{+}"
            "\\\\mu^{-}$', {'obs@1': {...}}], 'correlation': [[1.0]]}]; "
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
