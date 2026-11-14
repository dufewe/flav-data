#!/usr/bin/env python3
"""
Extract paper data from HEPData.

Usage:
    python3 hepdata-ext.py <inspire_id> [--output_dir /path/to/dir] [--table NAME]

Example:
    python3 hepdata-ext.py 1409497
    python3 hepdata-ext.py 1409497 -o /tmp/hd --table "Table 1"
"""

import json
import os
import re
import subprocess
import sys
import argparse
import shutil
import tempfile

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# Shared JSON writer; see common.py.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import write_json  # noqa: E402

def _resolve_hepdata_cli() -> str:
    """Locate the ``hepdata-cli`` executable.

    Search order: $PATH, active venv bin/, ~/.local/bin/, Homebrew prefixes.
    Returns absolute path or empty string.
    """
    found = shutil.which('hepdata-cli')
    if found:
        return found
    candidates = [
        os.path.join(sys.prefix, 'bin', 'hepdata-cli'),
        os.path.join(os.path.expanduser('~/.local/bin'), 'hepdata-cli'),
        '/opt/homebrew/bin/hepdata-cli',
        '/usr/local/bin/hepdata-cli',
    ]
    for candidate in candidates:
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return ''


# Resolved once at import time. Empty string means "not installed".
HEPDATA_CLI: str = _resolve_hepdata_cli()


def _require_hepdata_cli() -> None:
    """Raise :class:`RuntimeError` with install instructions if CLI is missing."""
    if HEPDATA_CLI:
        return
    raise RuntimeError(
        "hepdata-cli not found on PATH or in common install prefixes.\n"
        "Install it with:\n"
        "    pip install hepdata-cli\n"
        "Then re-run this script. See references/hepdata-cli.md for details."
    )


def fetch_table_names(inspire_id: str) -> list[str] | None:
    """Get available table names from HEPData for a given Inspire recid.

    Returns list of table names, or None on CLI failure.
    Raises RuntimeError if hepdata-cli is not installed.
    """
    _require_hepdata_cli()
    try:
        result = subprocess.run(
            [HEPDATA_CLI, 'fetch-names', '-i', 'inspire', str(inspire_id)],
            capture_output=True, text=True, timeout=60
        )
    except subprocess.TimeoutExpired:
        print(
            "Error: hepdata-cli fetch-names timed out after 60s. "
            "Check your network connection and retry."
        )
        return None
    if result.returncode != 0:
        if not result.stdout.strip() and not result.stderr.strip():
            print(f"Error: hepdata-cli returned no output (rc={result.returncode}). "
                  f"Verify '{HEPDATA_CLI} fetch-names -i inspire {inspire_id}' works manually.")
        else:
            print(f"Error: {result.stderr or result.stdout}")
        return None
    try:
        tables = json.loads(result.stdout)
    except json.JSONDecodeError:
        # hepdata-cli 0.3.x outputs Python repr (single quotes), not JSON
        try:
            import ast
            tables = ast.literal_eval(result.stdout)
        except (ValueError, SyntaxError):
            print("Warning: Could not parse table names")
            return result.stdout.strip().split('\n') if result.stdout.strip() else []
    # Flatten nested list if hepdata-cli wraps output in extra array
    if isinstance(tables, list) and tables and isinstance(tables[0], list):
        tables = tables[0]
    return tables


def _metadata_matches(path: str, inspire_id: str) -> bool:
    """Return True if a HEPData metadata JSON belongs to ``inspire_id``.

    hepdata-cli stores the Inspire recid under ``record.inspire_id``; older
    exports also put it at the top level.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    except (OSError, json.JSONDecodeError):
        return False
    if str(metadata.get('inspire_id', '')) == str(inspire_id):
        return True
    record = metadata.get('record') or {}
    return str(record.get('inspire_id', '')) == str(inspire_id)


def _is_raw_metadata(path: str) -> bool:
    """True for raw HEPData metadata (carries ``data_tables``), not the
    derived ``hepdata_summary.json`` output, which lacks that field."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return False
    return isinstance(data, dict) and 'data_tables' in data


def download_metadata(inspire_id: str, output_dir: str) -> str | None:
    """Download HEPData metadata JSON.

    Parameters
    ----------
    inspire_id : int or str
        InspireHEP control number (recid).
    output_dir : str
        Directory to write the metadata file into (created if missing).

    Returns
    -------
    str or None
        Absolute path to the downloaded JSON file, or ``None`` on failure.
    """
    _require_hepdata_cli()
    os.makedirs(output_dir, exist_ok=True)

    # Reuse an existing download for the same record (idempotent re-runs).
    for filename in sorted(os.listdir(output_dir)):
        path = os.path.join(output_dir, filename)
        if (filename.endswith('.json') and _metadata_matches(path, inspire_id)
                and _is_raw_metadata(path)):
            return path

    existing_json = {
        f for f in os.listdir(output_dir) if f.endswith('.json')
    }
    try:
        result = subprocess.run(
            [HEPDATA_CLI, 'download', '-f', 'json', '-i', 'inspire',
             str(inspire_id), '-d', output_dir],
            capture_output=True, text=True, timeout=120
        )
    except subprocess.TimeoutExpired:
        print(
            "Error: hepdata-cli download timed out after 120s. "
            "Check your network connection and retry."
        )
        return None

    if result.returncode != 0:
        if not result.stdout.strip() and not result.stderr.strip():
            print(f"Error: hepdata-cli returned no output (rc={result.returncode}).")
        else:
            print(f"Error: {result.stderr or result.stdout}")
        return None

    downloaded = sorted(
        f for f in os.listdir(output_dir)
        if f.endswith('.json') and f not in existing_json
    )
    if downloaded:
        return os.path.join(output_dir, downloaded[0])

    # Some hepdata-cli versions overwrite an existing metadata filename.
    for filename in sorted(os.listdir(output_dir)):
        path = os.path.join(output_dir, filename)
        if (filename.endswith('.json') and _metadata_matches(path, inspire_id)
                and _is_raw_metadata(path)):
            return path
    return None


def download_table_yaml(inspire_id: str, table_name: str) -> str:
    """Download YAML data for a specific table via ``hepdata-cli``.

    Direct HTTP access to hepdata.net is blocked by Cloudflare, so the CLI
    is the supported path (see references/hepdata-cli.md).
    """
    _require_hepdata_cli()
    with tempfile.TemporaryDirectory() as tmp:
        try:
            result = subprocess.run(
                [HEPDATA_CLI, 'download', '-f', 'yaml', '-i', 'inspire',
                 str(inspire_id), '-t', table_name, '-d', tmp],
                capture_output=True, text=True, timeout=180
            )
        except subprocess.TimeoutExpired as e:
            raise ValueError(
                f"HEPData table '{table_name}' download timed out "
                f"after {e.timeout}s"
            ) from e
        if result.returncode != 0:
            detail = (result.stderr or result.stdout or 'unknown error').strip()
            raise ValueError(
                f"HEPData table '{table_name}' download failed: {detail}"
            )
        yaml_files = sorted(
            f for f in os.listdir(tmp) if f.endswith(('.yaml', '.yml'))
        )
        if not yaml_files:
            raise ValueError(
                f"HEPData table '{table_name}' download produced no YAML file"
            )
        with open(os.path.join(tmp, yaml_files[0]), 'r', encoding='utf-8') as f:
            return f.read()


def parse_metadata(meta_path: str) -> dict:
    """Parse HEPData metadata JSON, extracting key information."""
    with open(meta_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    record = data.get('record', {})
    tables = data.get('data_tables', [])

    observable_tables = []
    correlation_tables = []

    for t in tables:
        name = t.get('name', '')
        desc = t.get('description', '').lower()
        if 'correlation' in desc or 'covariance' in desc:
            correlation_tables.append(t)
        else:
            observable_tables.append(t)

    return {
        'recid': data.get('recid', ''),
        'inspire_id': data.get('inspire_id') or record.get('inspire_id') or '',
        'hepdata_doi': data.get('hepdata_doi', ''),
        'record': {
            'title': record.get('title', ''),
            'arxiv_id': record.get('arxiv_id', ''),
            'doi': record.get('doi', ''),
            'collaborations': record.get('collaborations', []),
            'year': record.get('year', ''),
        },
        'total_tables': len(tables),
        'observable_tables': observable_tables,
        'correlation_tables': correlation_tables,
    }


_RANGE_RE = re.compile(
    r'^\s*([+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)'
    r'\s*-\s*'
    r'([+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)\s*$'
)


def _independent_point(cell) -> tuple[str | None, str | None]:
    """Normalize a HEPData independent-variable cell to ``(low, high)``.

    HEPData uses ``{low, high}`` for binned variables and ``{value: ...}``
    for single points; legacy exports write ranges as ``"0.1-0.98"``.
    """
    if not isinstance(cell, dict):
        return None, None
    low = cell.get('low')
    high = cell.get('high')
    if low is None and high is None and 'value' in cell:
        raw = cell['value']
        if isinstance(raw, str):
            match = _RANGE_RE.match(raw)
            if match:
                low, high = match.group(1), match.group(2)
            else:
                low = high = raw.strip()
        else:
            low = high = raw
    return (
        str(low).strip() if low is not None else None,
        str(high).strip() if high is not None else None,
    )


def parse_yaml_observables(yaml_text: str) -> tuple[list[dict], dict]:
    """Parse observable YAML data from a HEPData ``dependent_variables`` table.

    A HEPData "observable table" describes one observable measured at one or
    more kinematic points (e.g. ``F_L`` measured in 10 q² bins). In the YAML
    schema, each ``dependent_variables`` entry is **one observable** whose
    ``values`` list contains the data points for that observable.

    This function preserves that structure: each returned entry represents
    one observable, with a ``values`` list of data points (each having its
    own value, errors, and per-point qualifiers). It is the caller's job to
    decide whether to flatten this into the per-``obs@N`` JSON model
    (one obs = one q² bin) or keep it as one obs = one observable.

    Parameters
    ----------
    yaml_text : str
        The raw YAML text of a HEPData table.

    Returns
    -------
    tuple[list[dict], dict]
        ``(observables, qualifiers)`` where:

        * ``observables`` is a list with one entry per
          ``dependent_variables`` element. Each entry has the shape::

              {
                "header": str,           # e.g. "$F_L$"
                "qualifiers": [..],      # table-level qualifiers (shared)
                "values": [              # one per data point / q² bin
                    {
                      "value": str,       # central value as string
                      "errors": [..],    # [{label, symerror/asymerror{plus,minus}}]
                      "qualifiers": [..] # per-point qualifiers (e.g. q² bin)
                    },
                    ...
                ]
              }

        * ``qualifiers`` is ``{"global": <independent_variables> }`` —
          currently a passthrough of the table-level independent variables.
    """
    if not HAS_YAML:
        print("Warning: PyYAML not installed. Install with: pip install pyyaml")
        return [], {}

    data = yaml.safe_load(yaml_text)
    if not data or 'dependent_variables' not in data:
        return [], {}

    observables = []
    independent_vars = data.get('independent_variables', [])

    for var in data.get('dependent_variables', []):
        header = var.get('header', {}).get('name', '')
        table_qualifiers = var.get('qualifiers', [])

        values = []
        for idx, val in enumerate(var.get('values', [])):
            raw_value = val.get('value')
            independent = []
            q2min = q2max = None
            q2_found = False
            for iv in independent_vars:
                iv_values = iv.get('values', [])
                if idx >= len(iv_values):
                    continue
                iv_header = iv.get('header', {}) or {}
                name = iv_header.get('name', '')
                units = iv_header.get('units', '')
                low, high = _independent_point(iv_values[idx])
                independent.append({
                    'name': name,
                    'units': units,
                    'low': low,
                    'high': high,
                })
                header_l = (
                    f'{name} {units}'.lower()
                    .replace('$', '').replace('{', '').replace('}', '')
                    .replace('²', '^2').replace(' ', '')
                )
                if not q2_found and (
                    'q^2' in header_l
                    or 'q2' in header_l
                    or 'q**2' in header_l
                    or 'gev^2' in header_l
                ):
                    q2_found = True
                    q2min, q2max = low, high

            point = {
                'value': str(raw_value) if raw_value is not None else '',
                'errors': [],
                'qualifiers': val.get('qualifiers', []),
                'independent': independent,
            }
            if q2_found:
                if q2min is not None:
                    point['q2min'] = q2min
                if q2max is not None:
                    point['q2max'] = q2max

            for err in val.get('errors', []):
                err_info = {'label': err.get('label', '')}
                if 'symerror' in err:
                    se = err['symerror']
                    err_info['symerror'] = str(se) if se is not None else ''
                elif 'asymerror' in err:
                    ae = err['asymerror']
                    err_info['plus'] = (
                        str(ae.get('plus', ''))
                        if ae.get('plus') is not None else ''
                    )
                    err_info['minus'] = (
                        str(ae.get('minus', ''))
                        if ae.get('minus') is not None else ''
                    )
                point['errors'].append(err_info)

            values.append(point)

        observables.append({
            'header': header,
            'qualifiers': table_qualifiers,
            'values': values,
        })

    return observables, {'global': independent_vars}


def parse_yaml_correlation(yaml_text: str) -> tuple[str, list[list[float]], dict]:
    """Parse correlation/covariance matrix YAML data.

    Returns: (matrix_type, matrix, qualifiers)
    matrix_type: 'correlation' or 'covariance'
    matrix: 2D list
    """
    if not HAS_YAML:
        return 'unknown', [], {}

    data = yaml.safe_load(yaml_text)
    if not data or 'dependent_variables' not in data:
        return 'unknown', [], {}

    # Determine matrix type from header
    matrix_type = 'correlation'
    for var in data.get('dependent_variables', []):
        header = var.get('header', {}).get('name', '').lower()
        if 'covariance' in header:
            matrix_type = 'covariance'
            break

    # Extract matrix values (row-major order). A '-' cell means the entry
    # was not reported; substituting 0.0 keeps the matrix square instead
    # of silently shifting every following element.
    values = []
    qualifiers = {}
    missing = 0
    for var in data.get('dependent_variables', []):
        for val in var.get('values', []):
            v = val.get('value', '')
            if v == '-':
                missing += 1
                values.append(0.0)
                continue
            try:
                values.append(float(v))
            except (ValueError, TypeError):
                print(f"Warning: non-numeric matrix value {v!r} treated as 0.0")
                values.append(0.0)
        for q in var.get('qualifiers', []):
            qualifiers[q.get('name', '')] = q.get('value', '')
    if missing:
        print(
            f"Warning: {missing} missing matrix entr(y/ies) ('-') "
            f"treated as 0.0"
        )

    # Reconstruct into 2D matrix
    n = int(len(values) ** 0.5)
    if n * n != len(values):
        print(f"Warning: Matrix size {len(values)} is not a perfect square")
        return matrix_type, [], qualifiers

    matrix = []
    for i in range(n):
        row = values[i * n:(i + 1) * n]
        matrix.append(row)

    return matrix_type, matrix, qualifiers


def detect_table_type(yaml_text: str) -> str:
    """Classify a HEPData table as ``correlation``, ``covariance``, or
    ``observable``.

    Table names ("Table 9") carry no type information, so the YAML
    structure must be inspected: a matrix table has "correlation"/
    "covariance" headers or repeated ``CORR``/``COV`` independent variables.
    """
    if not HAS_YAML:
        return 'unknown'
    data = yaml.safe_load(yaml_text) or {}

    for var in data.get('dependent_variables', []):
        header = str(var.get('header', {}).get('name', '')).lower()
        if 'covariance' in header:
            return 'covariance'
        if 'correlation' in header:
            return 'correlation'

    names = [
        str(var.get('header', {}).get('name', '')).lower()
        for var in data.get('independent_variables', [])
    ]
    if len(names) >= 2:
        if all('cov' in name for name in names):
            return 'covariance'
        if all('corr' in name for name in names):
            return 'correlation'

    # Structural fallback: a flattened square matrix carries a single
    # dependent variable, no independent kinematic axis, and n² row-major
    # values. A genuine observable table always has an independent axis,
    # so requiring none keeps this from misclassifying n-bin observables.
    dependent = data.get('dependent_variables', [])
    if len(dependent) == 1 and not data.get('independent_variables'):
        values = dependent[0].get('values', [])
        n = int(len(values) ** 0.5)
        if n >= 2 and n * n == len(values):
            return 'correlation'

    return 'observable'


def main() -> int:
    """CLI entry point.

    Fails fast with an actionable ``pip install hepdata-cli`` message if
    the CLI is not installed.

    Examples
    --------
    >>> python3 flav-data-importer/scripts/hepdata-ext.py 1409497
    >>> python3 flav-data-importer/scripts/hepdata-ext.py 1409497 --output_dir /tmp/hd
    >>> python3 flav-data-importer/scripts/hepdata-ext.py 1409497 --table "Table 1"
    """
    # Fail fast with a clear install message if the CLI is missing.
    if not HEPDATA_CLI:
        _require_hepdata_cli()  # always raises
        sys.exit(1)  # unreachable; satisfies type checkers
    parser = argparse.ArgumentParser(
        description='Extract HEPData paper data'
    )
    parser.add_argument('inspire_id', help='InspireHEP control number')
    parser.add_argument(
        '--output_dir', '-o', default=None,
        help='Output directory for downloaded YAML/JSON. If omitted, no '
             'files are written (only stdout summary). Specify a path '
             '(e.g. /tmp/hepdata) to enable file output.'
    )
    parser.add_argument(
        '--no-write', dest='no_write', action='store_true',
        help='Skip writing YAML/JSON files; print summary only.'
    )
    parser.add_argument(
        '--table', '-t', help='Download only the specified table'
    )
    args = parser.parse_args()

    inspire_id = args.inspire_id
    if not args.output_dir and not args.no_write:
        names = fetch_table_names(inspire_id)
        if names is None:
            print('Failed to fetch table names.')
            return 1
        print(f"Available tables ({len(names)}):")
        for name in names:
            print(f"  - {name}")
        return 0

    if args.no_write:
        temp_output = tempfile.TemporaryDirectory()
        output_dir = temp_output.name
        print('--no-write: temporary files will be removed')
    else:
        temp_output = None
        output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    print(f"Fetching HEPData for Inspire ID: {inspire_id}")

    # List tables
    print("\n=== Available Tables ===")
    tables = fetch_table_names(inspire_id)
    if tables:
        if isinstance(tables, list):
            print(f"Total tables: {len(tables)}")
            if len(tables) <= 20:
                print(", ".join(tables))
            else:
                print(
                    ", ".join(tables[:10]) + f", ... ({len(tables)} total)"
                )
        else:
            print(tables)

    print("\n=== Downloading Metadata ===")
    meta_path = download_metadata(inspire_id, output_dir)
    if not meta_path:
        print("Failed to download metadata.")
        sys.exit(1)

    if not args.no_write:
        print(f"Metadata saved to: {meta_path}")

    # Parse metadata
    print("\n=== Metadata Summary ===")
    info = parse_metadata(meta_path)

    print(f"Title: {info['record']['title']}")
    print(f"arXiv: {info['record']['arxiv_id']}")
    print(f"DOI: {info['record']['doi']}")
    print(f"Collaboration: {', '.join(info['record']['collaborations'])}")
    print(f"Total tables: {info['total_tables']}")
    print(f"  Observable tables: {len(info['observable_tables'])}")
    print(f"  Correlation tables: {len(info['correlation_tables'])}")

    # Print correlation matrix q² bins
    if info['correlation_tables']:
        print(f"\nCorrelation/Covariance matrix bins:")
        for t in info['correlation_tables'][:5]:
            print(f"  {t['name']}: {t['description'][:80]}...")
        if len(info['correlation_tables']) > 5:
            print(
                f"  ... and {len(info['correlation_tables']) - 5} more"
            )

    # Download specific table (optional)
    if args.table:
        print(f"\n=== Downloading {args.table} ===")
        yaml_data = download_table_yaml(inspire_id, args.table)
        yaml_path = os.path.join(
            output_dir, f'{args.table.replace(" ", "_")}.yaml'
        )
        with open(yaml_path, 'w', encoding='utf-8') as f:
            f.write(yaml_data)
        if not args.no_write:
            print(f"YAML saved to: {yaml_path}")

        # Attempt to parse. Table names ("Table 9") carry no type
        # information, so classify from the YAML structure.
        table_type = detect_table_type(yaml_data)
        print(f"Detected table type: {table_type}")
        if table_type in ('correlation', 'covariance'):
            mtype, matrix, quals = parse_yaml_correlation(yaml_data)
            print(f"Matrix type: {mtype}")
            print(
                f"Matrix size: {len(matrix)}x"
                f"{len(matrix[0]) if matrix else 0}"
            )
            print(f"Qualifiers: {quals}")
        else:
            observables, quals = parse_yaml_observables(yaml_data)
            print(f"Found {len(observables)} observables")
            for obs in observables[:3]:
                n_points = len(obs.get('values', []))
                first = obs['values'][0] if n_points else {}
                q2 = ''
                if first.get('q2min') is not None or first.get('q2max') is not None:
                    q2 = (
                        f", q2=[{first.get('q2min')}, "
                        f"{first.get('q2max')}]"
                    )
                print(
                    f"  {obs['header']}: {n_points} data point(s); "
                    f"first value={first.get('value', 'N/A')!r} "
                    f"(errors: {len(first.get('errors', []))}){q2}"
                )

    # Save JSON summary
    if not args.no_write:
        summary_path = os.path.join(output_dir, 'hepdata_summary.json')
        write_json(summary_path, info)
        print(f"\nSummary saved to: {summary_path}")

    if temp_output:
        temp_output.cleanup()
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except RuntimeError as e:
        # Surface actionable install / config errors without a traceback.
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
