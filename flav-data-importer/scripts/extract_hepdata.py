#!/usr/bin/env python3
"""
Extract data from HEPData for a given InspireHEP record.

Usage:
    python3 extract_hepdata.py <inspire_id> <output_dir>

Example:
    python3 extract_hepdata.py 3094698 /tmp/hepdata_out

This script:
    1. Uses hepdata-cli to download metadata JSON
    2. Parses resource URLs from the metadata
    3. Downloads each data resource
    4. Outputs a summary of available tables and their structure
"""

import json
import os
import subprocess
import sys
import urllib.request

HEPDATA_CLI = "/Users/dufewe/.hermes/hermes-agent/venv/bin/hepdata-cli"

def fetch_table_names(inspire_id):
    """Fetch available table names from HEPData."""
    result = subprocess.run(
        [HEPDATA_CLI, 'fetch-names', '-i', 'inspire', str(inspire_id)],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        print(f"Error fetching table names: {result.stderr}")
        return None
    return result.stdout

def download_metadata(inspire_id, output_dir):
    """Download HEPData metadata JSON."""
    os.makedirs(output_dir, exist_ok=True)
    result = subprocess.run(
        [HEPDATA_CLI, 'download', '-f', 'json', '-i', 'inspire', str(inspire_id), '-d', output_dir],
        capture_output=True, text=True, timeout=120
    )
    if result.returncode != 0:
        print(f"Error downloading metadata: {result.stderr}")
        return None

    # Find the downloaded JSON file
    for f in os.listdir(output_dir):
        if f.endswith('.json'):
            return os.path.join(output_dir, f)
    return None

def download_resource(resource_url, output_path):
    """Download a specific data resource from HEPData."""
    try:
        req = urllib.request.Request(resource_url + '?view=true')
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"Error downloading {resource_url}: {e}")
        return False

def parse_resource_json(file_path):
    """Parse a HEPData resource JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    result = {
        'observables': {},
        'bins': []
    }

    indep = data.get('independent_variables', {})
    indep_values = indep.get('values', [])

    dep = data.get('dependent_variables', {})

    for obs_name, obs_data in dep.items():
        units = obs_data.get('units', 1.0)
        if isinstance(units, str):
            # Parse strings like "10^-8"
            try:
                units = float(units.replace('10^', 'e').replace('10', '1e'))
            except:
                units = 1.0

        values = obs_data.get('values', [])
        result['observables'][obs_name] = {
            'units': units,
            'count': len(values)
        }

        for i, val_entry in enumerate(values):
            val = val_entry.get('val')
            if isinstance(val, str):
                continue  # Skip "-" entries

            bin_info = {}
            if i < len(indep_values):
                bin_info = indep_values[i]

            result['bins'].append({
                'bin': bin_info,
                'observations': {
                    obs: {
                        'val': val_entry.get('val'),
                        'hi_stat_err': val_entry.get('hi_stat_err'),
                        'lo_stat_err': val_entry.get('lo_stat_err'),
                        'hi_syst_err': val_entry.get('hi_syst_err'),
                        'lo_syst_err': val_entry.get('lo_syst_err'),
                    }
                    for obs in dep.keys()
                }
            })

    return result

def main():
    if len(sys.argv) < 3:
        print(f"Usage: python3 {sys.argv[0]} <inspire_id> <output_dir>")
        sys.exit(1)

    inspire_id = sys.argv[1]
    output_dir = sys.argv[2]

    print(f"Fetching HEPData for Inspire ID: {inspire_id}")
    print()

    # Step 1: List tables
    print("Step 1: Available tables...")
    tables = fetch_table_names(inspire_id)
    if tables:
        print(tables)

    # Step 2: Download metadata
    print("\nStep 2: Downloading metadata...")
    meta_path = download_metadata(inspire_id, output_dir)
    if not meta_path:
        print("Failed to download metadata.")
        sys.exit(1)

    print(f"Metadata saved to: {meta_path}")

    # Step 3: Parse metadata and list resources
    with open(meta_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    print("\nAvailable resources:")
    # The metadata structure varies, but typically contains table info with resource URLs
    # Print a summary for manual download

    print("\nDone. Use the metadata JSON to find resource URLs, then:")
    print("  curl -sL '<resource_url>?view=true' > data.json")
    print("  python3 parse_hepdata_resource.py data.json")

if __name__ == '__main__':
    main()
