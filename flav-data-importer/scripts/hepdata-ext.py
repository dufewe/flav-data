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
import subprocess
import sys
import argparse
import urllib.request
import urllib.error
import shutil

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# Re-export shared helpers so callers can
# `from hepdata_ext import to_bibtex, unicode_to_latex`.
# See common.py for the canonical implementations and SKILL.md
# "Import Conventions" rules 3 + 4 for the policies.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import unicode_to_latex, to_bibtex  # noqa: E402,F401

def _resolve_hepdata_cli():
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


def _require_hepdata_cli():
    """Raise :class:`RuntimeError` with install instructions if CLI is missing."""
    if HEPDATA_CLI:
        return
    raise RuntimeError(
        "hepdata-cli not found on PATH or in common install prefixes.\n"
        "Install it with:\n"
        "    pip install hepdata-cli\n"
        "Then re-run this script. See references/hepdata-cli.md for details."
    )


def fetch_table_names(inspire_id):
    """Get available table names from HEPData for a given Inspire recid.

    Returns list of table names, or None on CLI failure.
    Raises RuntimeError if hepdata-cli is not installed.
    """
    _require_hepdata_cli()
    result = subprocess.run(
        [HEPDATA_CLI, 'fetch-names', '-i', 'inspire', str(inspire_id)],
        capture_output=True, text=True, timeout=60
    )
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


def download_metadata(inspire_id, output_dir):
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
    result = subprocess.run(
        [HEPDATA_CLI, 'download', '-f', 'json', '-i', 'inspire',
         str(inspire_id), '-d', output_dir],
        capture_output=True, text=True, timeout=120
    )
    if result.returncode != 0:
        if not result.stdout.strip() and not result.stderr.strip():
            print(f"Error: hepdata-cli returned no output (rc={result.returncode}).")
        else:
            print(f"Error: {result.stderr or result.stdout}")
        return None

    for f in os.listdir(output_dir):
        if f.endswith('.json'):
            return os.path.join(output_dir, f)
    return None


def download_table_yaml(inspire_id, table_name):
    """Download YAML data for a specific table via direct HTTP."""
    from urllib.parse import quote
    encoded_name = quote(table_name, safe='')
    url = (
        f'https://www.hepdata.net/download/table/'
        f'ins{inspire_id}/{encoded_name}/yaml'
    )
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req, timeout=30)
    except urllib.error.HTTPError as e:
        raise ValueError(
            f"HEPData table download failed (HTTP {e.code}): {e.reason}"
        ) from e
    except urllib.error.URLError as e:
        raise ValueError(
            f"HEPData table download connection failed: {e.reason}"
        ) from e
    return response.read().decode('utf-8')


def parse_metadata(meta_path):
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
        'inspire_id': data.get('inspire_id') or '',
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


def parse_yaml_observables(yaml_text):
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
    global_qualifiers = data.get('independent_variables', [])

    for var in data.get('dependent_variables', []):
        header = var.get('header', {}).get('name', '')
        table_qualifiers = var.get('qualifiers', [])

        values = []
        for val in var.get('values', []):
            raw_value = val.get('value')
            point = {
                'value': str(raw_value) if raw_value is not None else '',
                'errors': [],
                'qualifiers': val.get('qualifiers', []),
            }

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

    return observables, {'global': global_qualifiers}


def parse_yaml_correlation(yaml_text):
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

    # Extract matrix values (row-major order)
    values = []
    qualifiers = {}
    for var in data.get('dependent_variables', []):
        for val in var.get('values', []):
            v = val.get('value', '')
            if v == '-':
                continue
            try:
                values.append(float(v))
            except (ValueError, TypeError):
                print(f"Warning: Skipping non-numeric matrix value: {v!r}")
                continue
        for q in var.get('qualifiers', []):
            qualifiers[q.get('name', '')] = q.get('value', '')

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


def main():
    """CLI entry point.

    Fails fast with an actionable ``pip install hepdata-cli`` message if
    the CLI is not installed.

    Examples
    --------
    >>> python3 scripts/hepdata-ext.py 1409497
    >>> python3 scripts/hepdata-ext.py 1409497 --output_dir /tmp/hd
    >>> python3 scripts/hepdata-ext.py 1409497 --table "Table 1"
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
        '--output_dir', '-o', default=None, help='Output directory (default: <cwd>/hepdata_out)'
    )
    parser.add_argument(
        '--table', '-t', help='Download only the specified table'
    )
    args = parser.parse_args()

    inspire_id = args.inspire_id
    output_dir = args.output_dir or os.path.join(os.getcwd(), 'hepdata_out')

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
        print(f"\n=== Step 4: Downloading {args.table} ===")
        yaml_data = download_table_yaml(inspire_id, args.table)
        yaml_path = os.path.join(
            output_dir, f'{args.table.replace(" ", "_")}.yaml'
        )
        with open(yaml_path, 'w', encoding='utf-8') as f:
            f.write(yaml_data)
        print(f"YAML saved to: {yaml_path}")

        # Attempt to parse
        if 'correlation' in args.table.lower() or 'covariance' in args.table.lower():
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
                print(
                    f"  {obs['header']}: {n_points} data point(s); "
                    f"first value={first.get('value', 'N/A')!r} "
                    f"(errors: {len(first.get('errors', []))})"
                )

    # Save JSON summary
    summary_path = os.path.join(output_dir, 'hepdata_summary.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=4, ensure_ascii=False)
    print(f"\nSummary saved to: {summary_path}")


if __name__ == '__main__':
    try:
        main()
    except RuntimeError as e:
        # Surface actionable install / config errors without a traceback.
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
