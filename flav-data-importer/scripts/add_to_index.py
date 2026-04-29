#!/usr/bin/env python3
"""
Add a new paper to the flav-data index file.

Usage:
    python3 add_to_index.py <group> <year> <month> <file_id>

Example:
    python3 add_to_index.py LHCb 2025 04 LHCb:2025xxx
"""

import json
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def add_to_index(group, year, month, file_id):
    """Add a file_id to the year index file."""
    index_path = os.path.join(BASE_DIR, 'Experimental', group, str(year), f'{group}@{year}.json')

    # Load or create index
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)
    except FileNotFoundError:
        # Create parent directory if needed
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        index = {}

    # Zero-pad month
    month_key = f"{int(month):02d}"

    # Add file_id if not already present
    if month_key not in index:
        index[month_key] = []
    if file_id not in index[month_key]:
        index[month_key].append(file_id)
        print(f"Added {file_id} to {group}@{year}.json under month {month_key}")
    else:
        print(f"{file_id} already exists in {group}@{year}.json under month {month_key}")

    # Sort keys
    index = dict(sorted(index.items()))

    # Write back
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=4)
        f.write('\n')

    print(f"Index updated: {index_path}")

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print(f"Usage: python3 {sys.argv[0]} <group> <year> <month> <file_id>")
        sys.exit(1)

    add_to_index(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
