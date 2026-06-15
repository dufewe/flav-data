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
    'arxiv', 'time', 'abstract', 'pdf', 'data', 'transition-mode'
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

# Numeric field patterns (checked for string type)
NUMERIC_FIELD_PATTERNS = [
    'value', 'unit',
    'q2min', 'q2max', 'pTmin', 'pTmax', 'etamin', 'etamax',
    'type@1_err_up', 'type@1_err_down', 'type@2_err_up', 'type@2_err_down',
    'type@3_err_up', 'type@3_err_down',
    'type@1_upper_limit', 'type@2_upper_limit', 'type@3_upper_limit',
    'tot_err_up', 'tot_err_down'
]

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

# Allowed field patterns within data entries
DATA_ENTRY_ALLOWED_PATTERNS = ['obs@', '_correlation', '_covariance']


def validate_transition_symbol(name):
    """Check that the observable name has the expected OBS(transition)[condition] shape.

    Three shapes are accepted (see obs-abbr.md):

    1. **Basic observable** (no transition): ``OBS(particle)`` — e.g.
       ``Tau(e-)``, ``Mass(Z)``, ``MZ``, ``gammaCKM``, ``|Vtd|``.
    2. **Composite observable** (with transition): ``OBS(transition)`` —
       e.g. ``Br(B+2K+mumu)``, ``RBr(B+.2.K+.l+.l-)``. Strict
       validation of the internal structure (e.g. ``.2.`` separator)
       is **disabled** to allow legacy data that uses a compact form;
       a future cleanup pass can tighten this once legacy files are
       rewritten.
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
    # Additional basic observables that don't follow the OBS(particle)
    # pattern but are still parameter/observable values (no decay or
    # scattering process involved). These come from the CKM Parameters,
    # Masses, and various ratio tables in obs-abbr.md.
    if name in (
        'gammaCKM', 'r', 'delta', 'R_b', 'R_c',  # CKM, EW pseudo-obs
        'MZ', 'MW', 'Mtop', 'MH', 'Mh',         # particle masses
        '|Vtd|', '|Vts|', '|Vub|', '|Vcb|',      # CKM matrix elements
        'S_phigamma', 'C_phigamma', 'ADelta_phigamma',  # phi_gamma
    ):
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


def validate_latex(text, field_name, obs_key):
    """Check that the LaTeX field is non-empty."""
    issues = []
    if not text or not text.strip():
        issues.append(f"  {obs_key}.{field_name}: LaTeX field is empty")
    return issues


def validate_correlation(matrix, data_entry_idx, is_covariance=False):
    """Check correlation matrix: symmetric with diagonal = 1.0.
    Covariance matrix: only symmetry (diagonal = err², verified manually)."""
    issues = []
    n = len(matrix)
    # Check rectangular
    for i, row in enumerate(matrix):
        if not isinstance(row, list) or len(row) != n:
            row_len = len(row) if isinstance(row, list) else 'N/A'
            issues.append(
                f"  data[{data_entry_idx}]: matrix row {i} length ({row_len}) "
                f"does not match column count ({n})"
            )
            return issues
    # Check element types
    for i in range(n):
        for j in range(n):
            if not isinstance(matrix[i][j], (int, float)):
                issues.append(
                    f"  data[{data_entry_idx}]: matrix element [{i}][{j}] "
                    f"is not numeric (type: {type(matrix[i][j]).__name__})"
                )
                return issues
    for i in range(n):
        if not is_covariance:
            if abs(matrix[i][i] - 1.0) > 0.001:
                issues.append(
                    f"  data[{data_entry_idx}]: correlation matrix diagonal "
                    f"[{i}][{i}] = {matrix[i][i]}, expected 1.0"
                )
        for j in range(i + 1, n):
            if abs(matrix[i][j] - matrix[j][i]) > 0.001:
                issues.append(
                    f"  data[{data_entry_idx}]: matrix not symmetric "
                    f"[{i}][{j}] = {matrix[i][j]} vs [{j}][{i}] = {matrix[j][i]}"
                )
    return issues


def validate_arxiv_format(arxiv):
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
        # importer / human notices (most modern papers should carry vN).
        issues.append(
            f"  arxiv field '{link_text}' is missing version suffix "
            f"(e.g. 'v1', 'v2') — consider adding it"
        )
    return issues


def validate_data_entry_fields(entry, entry_idx):
    """Check that the data block contains only allowed field patterns."""
    issues = []
    for key in entry:
        allowed = any(pattern in key for pattern in DATA_ENTRY_ALLOWED_PATTERNS)
        if not allowed:
            issues.append(
                f"  data[{entry_idx}]: disallowed field '{key}'; "
                f"data block may only contain obs@N, type@N_correlation, "
                f"type@N_covariance, tot_correlation, or tot_covariance"
            )
    return issues


def validate_transition_mode(value):
    """Check that transition-mode matches one of the 7 valid values."""
    issues = []
    if not isinstance(value, str) or not value.strip():
        issues.append("  transition-mode must be a non-empty string")
        return issues
    if value.lower() not in VALID_TRANSITION_MODES:
        issues.append(
            f"  transition-mode '{value}' is not in the allowed list: "
            f"{VALID_TRANSITION_MODES}; use property-based names like "
            f"'semileptonic decay', 'scattering', etc."
        )
    return issues


def validate_json(file_path):
    """Validate a single flav-data JSON file."""
    print(f"Validating: {file_path}")
    all_issues = []

    # 1. Parse JSON
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("  [OK] JSON format correct")
    except json.JSONDecodeError as e:
        print(f"  [FAIL] JSON parse error: {e}")
        return [f"JSON parse error: {e}"]

    # 1b. Check top-level type (must be dict, not list)
    if not isinstance(data, dict):
        print(f"  [FAIL] Top-level JSON must be an object, got {type(data).__name__}")
        return [f"Top-level JSON must be an object, got {type(data).__name__}"]

    # 2. Check top-level fields
    for field in REQUIRED_TOP_FIELDS:
        if field not in data:
            all_issues.append(f"  Missing required field: {field}")
    if not all_issues:
        print("  [OK] Top-level fields complete")

    # 3. Check for forbidden fields
    for field in FORBIDDEN_FIELDS:
        if field in data:
            all_issues.append(f"  Forbidden field present: '{field}' (not supported)")

    # 4. Check that transition-mode is the last field before 'data'.
    # Per json-meta.md §"Key Constraints" §8: "transition-mode last —
    # this field must always be the final key in the JSON object."
    # In practice the order is: ..., transition-mode, data — so we
    # require 'data' to follow 'transition-mode' (with nothing between
    # them) or transition-mode to be the final key.
    if 'transition-mode' in data:
        keys = list(data.keys())
        tm_idx = keys.index('transition-mode')
        # Nothing allowed between transition-mode and 'data' (or end of dict)
        next_keys = keys[tm_idx + 1:]
        # Only 'data' is allowed to follow transition-mode
        if next_keys and next_keys != ['data']:
            all_issues.append(
                f"  transition-mode is not followed by 'data'; "
                f"keys after transition-mode: {next_keys}"
            )

    # 5. Check arxiv field format
    arxiv = data.get('arxiv')
    all_issues.extend(validate_arxiv_format(arxiv))

    # 6. Check transition-mode content
    if 'transition-mode' in data:
        all_issues.extend(validate_transition_mode(data['transition-mode']))

    # 7. Check data array
    data_entries = data.get('data', [])
    if not data_entries:
        all_issues.append("  data array is empty")
        print("  [WARN] data array is empty")

    for entry_idx, entry in enumerate(data_entries):
        # Check allowed fields in data block
        all_issues.extend(validate_data_entry_fields(entry, entry_idx))

        # Find obs@N keys
        obs_keys = []
        for k in entry:
            if k.startswith('obs@'):
                try:
                    num = int(k.split('@')[1])
                    obs_keys.append((num, k))
                except (ValueError, IndexError):
                    all_issues.append(
                        f"  data[{entry_idx}]: invalid obs key '{k}'; "
                        f"expected obs@N format (N as integer)"
                    )
                    continue
        obs_keys.sort(key=lambda x: x[0])
        obs_nums = [n for n, _ in obs_keys]
        obs_keys = [k for _, k in obs_keys]

        # Check contiguity: numbering must start at 1 and run 1..N
        # with no gaps. A gap (e.g. obs@1, obs@3) almost always means
        # the middle obs was deleted but the surrounding references
        # (correlation/covariance matrix dimensions) were not updated.
        if obs_nums:
            expected = list(range(1, len(obs_nums) + 1))
            if obs_nums != expected:
                missing = [
                    n for n in expected if n not in obs_nums
                ]
                all_issues.append(
                    f"  data[{entry_idx}]: obs@N numbering is not "
                    f"contiguous; found {obs_nums}, expected "
                    f"1..{len(obs_nums)}; missing obs@{missing}"
                )

        if not obs_keys:
            has_matrix = any(
                'correlation' in k.lower() or 'covariance' in k.lower()
                for k in entry
            )
            if not has_matrix:
                all_issues.append(
                    f"  data[{entry_idx}]: no obs@N entries"
                )
            continue

        for obs_key in obs_keys:
            obs = entry[obs_key]

            # Determine format: standard, upper limit, external ref, or total error
            has_value = 'value' in obs
            has_upper = any(k.endswith('_upper_limit') for k in obs)
            has_ref = 'ref' in obs and 'tot_err_up' in obs
            has_tot_err = 'tot_err_up' in obs and 'tot_err_down' in obs

            # Priority:
            # 1. ref + tot_err + value → external reference
            # 2. tot_err + value + upper_limit → combined fit result + CLs limits
            # 3. tot_err + value (no ref, no upper) → total error (paper's own combined error)
            # 4. type@1_upper_limit → upper limit only
            # 5. value + type@1_err → standard measurement

            if has_ref and has_value:
                for field in REQUIRED_OBS_FIELDS_WITH_REF:
                    if field not in obs:
                        all_issues.append(f"  {obs_key}: missing required field: {field}")
            elif has_tot_err and has_upper and has_value:
                # Combined: profile likelihood fit result + CLs upper limits
                for field in REQUIRED_OBS_FIELDS_WITH_TOT_ERR:
                    if field not in obs:
                        all_issues.append(f"  {obs_key}: missing required field: {field}")
                for field in REQUIRED_OBS_FIELDS_WITH_UPPER:
                    if field not in obs:
                        all_issues.append(f"  {obs_key}: missing required field: {field}")
            elif has_tot_err and has_value:
                for field in REQUIRED_OBS_FIELDS_WITH_TOT_ERR:
                    if field not in obs:
                        all_issues.append(f"  {obs_key}: missing required field: {field}")
            elif has_upper:
                for field in REQUIRED_OBS_FIELDS_WITH_UPPER:
                    if field not in obs:
                        all_issues.append(f"  {obs_key}: missing required field: {field}")
            elif has_value:
                for field in REQUIRED_OBS_FIELDS_WITH_VALUE:
                    if field not in obs:
                        all_issues.append(f"  {obs_key}: missing required field: {field}")
            else:
                all_issues.append(
                    f"  {obs_key}: missing 'value' or 'type@1_upper_limit' field"
                )

            # Check numeric fields are strings
            for field in NUMERIC_FIELD_PATTERNS:
                if field in obs and not isinstance(obs[field], str):
                    all_issues.append(
                        f"  {obs_key}.{field}: expected string, "
                        f"got {type(obs[field]).__name__}"
                    )

            # Check LaTeX
            if 'latex' in obs:
                all_issues.extend(validate_latex(obs['latex'], 'latex', obs_key))

            # Check transition symbol
            if 'name' in obs:
                all_issues.extend(validate_transition_symbol(obs['name']))

            # Check err_up/down paired for each error type
            for key in list(obs.keys()):
                if key.endswith('_err_up'):
                    base = key[:-7]  # strip '_err_up'
                    down_key = f'{base}_err_down'
                    if down_key not in obs:
                        all_issues.append(
                            f"  {obs_key}: '{key}' present but missing '{down_key}'"
                        )
                elif key.endswith('_err_down'):
                    base = key[:-9]  # strip '_err_down'
                    up_key = f'{base}_err_up'
                    if up_key not in obs:
                        all_issues.append(
                            f"  {obs_key}: '{key}' present but missing '{up_key}'"
                        )

        # Check correlation/covariance matrices (null = no matrix)
        for corr_key in entry:
            if 'correlation' in corr_key.lower() or 'covariance' in corr_key.lower():
                if entry[corr_key] is None:
                    continue  # null means no matrix — acceptable
                if not isinstance(entry[corr_key], list):
                    all_issues.append(f"  {corr_key}: expected 2D array")
                    continue
                matrix = entry[corr_key]
                is_covariance = 'covariance' in corr_key.lower()
                all_issues.extend(
                    validate_correlation(matrix, entry_idx, is_covariance)
                )

                # Check matrix dimension matches obs count
                if len(matrix) != len(obs_keys):
                    all_issues.append(
                        f"  data[{entry_idx}]: matrix dimension "
                        f"({len(matrix)}x{len(matrix)}) does not match "
                        f"observable count ({len(obs_keys)})"
                    )

    # Report results
    if all_issues:
        print(f"  [FAIL] Found {len(all_issues)} issue(s):")
        for issue in all_issues:
            print(issue)
    else:
        print("  [OK] All checks passed")

    return all_issues


def main():
    """CLI entry point.

    Examples
    --------
    >>> python3 scripts/json-valid.py path/to/file.json
    >>> python3 scripts/json-valid.py a.json b.json c.json --quiet
    >>> python3 scripts/json-valid.py --help
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
