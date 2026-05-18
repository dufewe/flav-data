#!/usr/bin/env python3
"""
Validate flav-data JSON file format and data completeness.

Usage:
    python3 json-valid.py <path/to/file.json> [path/to/file2.json ...]

Checks:
    1. JSON is parseable
    2. Required top-level fields are present
    3. obs@N entries have required fields (name, latex, value/upper_limit)
    4. Numeric fields must be strings
    5. Correlation matrix is symmetric with diagonal = 1.0
    6. Covariance matrix is symmetric
    7. LaTeX fields are non-empty
    8. Transition symbols conform to A.B.2.C.D format
    9. arxiv field includes primary category and version, or is null
    10. transition-mode contains only scattering/decay categories
    11. data block contains only obs@N, type@N_correlation, type@N_covariance, tot_correlation, tot_covariance fields
    12. err_up/down fields are paired for each error type
"""

import json
import re
import sys
import os

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
    'value', 'q2min', 'q2max', 'pTmin', 'pTmax', 'etamin', 'etamax',
    'type@1_err_up', 'type@1_err_down', 'type@2_err_up', 'type@2_err_down',
    'type@3_err_up', 'type@3_err_down',
    'type@1_upper_limit', 'type@2_upper_limit', 'type@3_upper_limit',
    'tot_err_up', 'tot_err_down'
]

# transition-mode must contain one of these keywords
VALID_TRANSITION_KEYWORDS = ['decay', 'scattering']

# Allowed field patterns within data entries
DATA_ENTRY_ALLOWED_PATTERNS = ['obs@', '_correlation', '_covariance']


def validate_transition_symbol(name):
    """Check that the observable name contains a valid transition symbol A.B.2.C.D.

    Single-particle observables (lifetimes, masses) use OBS(particle) format
    without transitions — e.g. Tau(e-), Mass(Z), Mass(t) — and are exempt.
    See obs-abbr.md Section 2, Single-Transition Observables table.
    """
    issues = []
    # Extract OBS prefix (e.g. "Tau", "Mass", "Br", "FL")
    obs_prefix = name.split('(', 1)[0] if '(' in name else ''
    # Single-particle observables: no transition symbol needed
    if obs_prefix in ('Tau', 'Mass', 'mass', 'dSigma', 'Sigma', 'dSigma/dpT', 'dSigma/deta', 'AC'):
        return issues

    match = re.search(r'\(([^)]+)\)', name)
    if match:
        transition = match.group(1)
        if '.2.' not in transition:
            issues.append(
                f"  Transition symbol '{transition}' missing '.2.' separator; "
                f"expected A.B.2.C.D format"
            )
        parts = transition.split('.')
        if len(parts) < 4:
            issues.append(
                f"  Transition symbol '{transition}' requires at least 4 parts "
                f"(A.B.2.C.D), found {len(parts)}"
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
    """Check arxiv field format:
    - null (allowed)
    - [primary_category/arxiv_id_with_version](url), version contains 'v'
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
    md_match = re.match(r'^\[([^\]]+)\]\(([^)]+)\)$', arxiv)
    if not md_match:
        issues.append(
            f"  arxiv field format error; expected "
            f"[primary_category/arxiv_idvN](url), got: {arxiv}"
        )
        return issues
    link_text = md_match.group(1)
    if '/' not in link_text:
        issues.append(
            f"  arxiv link text missing primary category prefix; "
            f"expected 'category/arxiv_idvN', got: {link_text}"
        )
    elif 'v' not in link_text.split('/', 1)[1]:
        issues.append(
            f"  arxiv link text missing version number; "
            f"expected 'category/arxiv_idvN', got: {link_text}"
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
    """Check that transition-mode contains 'decay' or 'scattering'."""
    issues = []
    if not isinstance(value, str) or not value.strip():
        issues.append("  transition-mode must be a non-empty string")
        return issues
    has_valid = any(kw in value.lower() for kw in VALID_TRANSITION_KEYWORDS)
    if not has_valid:
        issues.append(
            f"  transition-mode '{value}' does not contain 'decay' or "
            f"'scattering'; use property-based names like 'semileptonic decay', "
            f"'scattering', etc."
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

    # 4. Check that transition-mode is the last field
    if 'transition-mode' in data:
        keys = list(data.keys())
        if keys[-1] != 'transition-mode':
            all_issues.append(
                f"  transition-mode is not the last field; "
                f"last field is '{keys[-1]}'"
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
        obs_keys = [k for _, k in obs_keys]

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
            # 2. tot_err + value (no ref) → total error (paper's own combined error)
            # 3. type@1_upper_limit → upper limit
            # 4. value + type@1_err → standard measurement

            if has_ref and has_value:
                for field in REQUIRED_OBS_FIELDS_WITH_REF:
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

        # Check correlation/covariance matrices
        for corr_key in entry:
            if 'correlation' in corr_key.lower() or 'covariance' in corr_key.lower():
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
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <path/to/file.json> [path/to/file2.json ...]")
        sys.exit(1)

    total_issues = 0
    for path in sys.argv[1:]:
        if not os.path.exists(path):
            print(f"File not found: {path}")
            total_issues += 1
            continue
        issues = validate_json(path)
        total_issues += len(issues)
        print()

    if total_issues == 0:
        print("All files validated successfully.")
        sys.exit(0)
    else:
        print(f"Found {total_issues} issue(s) in total.")
        sys.exit(1)


if __name__ == '__main__':
    main()
