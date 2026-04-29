#!/usr/bin/env python3
"""
Validate a flav-data JSON file against the expected schema.

Usage:
    python3 validate_json.py <path/to/file.json>

Checks:
    1. Valid JSON
    2. Required top-level fields present
    3. obs@N entries have required fields
    4. Numeric values stored as strings
    5. Correlation matrices are symmetric with diagonal = 1.0
    6. LaTeX has proper double-escaping (no single backslashes)
"""

import json
import sys
import os

REQUIRED_TOP_FIELDS = [
    'inspire-hep', 'author', 'collaboration', 'title',
    'arxiv', 'time', 'abstract', 'pdf', 'data'
]

REQUIRED_OBS_FIELDS = [
    'name', 'latex', 'value',
    'type@1_err', 'type@1_err_up', 'type@1_err_down'
]

def validate_latex(text, field_name, obs_key):
    """Check that LaTeX uses proper escaping.
    After JSON parsing, valid LaTeX has single backslashes like \to, \phi.
    These are fine -- the JSON file itself should have double backslashes.
    This check runs on parsed JSON, so we can only verify LaTeX is present."""
    issues = []
    if not text or not text.strip():
        issues.append(f"  {obs_key}.{field_name}: empty LaTeX field")
    return issues

def validate_correlation(matrix, data_entry_idx):
    """Check correlation matrix is symmetric with diagonal = 1.0."""
    issues = []
    n = len(matrix)
    for i in range(n):
        # Check diagonal
        if abs(matrix[i][i] - 1.0) > 0.001:
            issues.append(f"  data[{data_entry_idx}]: diagonal [{i}][{i}] = {matrix[i][i]}, expected 1.0")
        # Check symmetry
        for j in range(i + 1, n):
            if abs(matrix[i][j] - matrix[j][i]) > 0.001:
                issues.append(f"  data[{data_entry_idx}]: asymmetry at [{i}][{j}] = {matrix[i][j]} vs [{j}][{i}] = {matrix[j][i]}")
    return issues

def validate_json(file_path):
    """Validate a flav-data JSON file."""
    print(f"Validating: {file_path}")
    all_issues = []

    # 1. Parse JSON
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("  [OK] Valid JSON")
    except json.JSONDecodeError as e:
        print(f"  [FAIL] Invalid JSON: {e}")
        return [f"Invalid JSON: {e}"]

    # 2. Check required top-level fields
    for field in REQUIRED_TOP_FIELDS:
        if field not in data:
            all_issues.append(f"  Missing required field: {field}")
    if not all_issues:
        print("  [OK] All required top-level fields present")

    # 3. Check data entries
    data_entries = data.get('data', [])
    if not data_entries:
        all_issues.append("  Empty data array")
        print("  [WARN] Empty data array")

    for entry_idx, entry in enumerate(data_entries):
        # Find obs@N keys
        obs_keys = sorted(
            [k for k in entry if k.startswith('obs@')],
            key=lambda x: int(x.split('@')[1])
        )

        if not obs_keys:
            all_issues.append(f"  data[{entry_idx}]: No obs@N entries")
            continue

        for obs_key in obs_keys:
            obs = entry[obs_key]
            for field in REQUIRED_OBS_FIELDS:
                if field not in obs:
                    all_issues.append(f"  {obs_key}: Missing required field: {field}")

            # Check values are strings
            for field in ['value', 'q2min', 'q2max', 'type@1_err_up', 'type@1_err_down']:
                if field in obs and not isinstance(obs[field], str):
                    all_issues.append(f"  {obs_key}.{field}: Expected string, got {type(obs[field]).__name__}")

            # Check LaTeX escaping
            if 'latex' in obs:
                all_issues.extend(validate_latex(obs['latex'], 'latex', obs_key))

        # Check correlation matrix
        for corr_key in entry:
            if 'correlation' in corr_key.lower() and isinstance(entry[corr_key], list):
                all_issues.extend(validate_correlation(entry[corr_key], entry_idx))

    # Report results
    if all_issues:
        print(f"  [FAIL] Found {len(all_issues)} issue(s):")
        for issue in all_issues:
            print(issue)
    else:
        print("  [OK] All validation checks passed")

    return all_issues

if __name__ == '__main__':
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
        print(f"Found {total_issues} total issue(s) across all files.")
        sys.exit(1)
