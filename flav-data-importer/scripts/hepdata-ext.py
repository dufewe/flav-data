#!/usr/bin/env python3
"""
从 HEPData 提取论文数据信息。

Usage:
    python3 hepdata-ext.py <inspire_id> [--output_dir /path/to/dir]

Example:
    python3 hepdata-ext.py 1409497
    python3 hepdata-ext.py 1409497 -o /tmp/hepdata_out --table "Table 1"
"""

import json
import os
import subprocess
import sys
import argparse
import urllib.request

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

HEPDATA_CLI = "/hepdata-cli"


def fetch_table_names(inspire_id):
    """获取 HEPData 可用的表格名称列表。"""
    result = subprocess.run(
        [HEPDATA_CLI, 'fetch-names', '-i', 'inspire', str(inspire_id)],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Warning: Could not parse table names as JSON")
        return result.stdout.strip().split('\n') if result.stdout.strip() else []


def download_metadata(inspire_id, output_dir):
    """下载 HEPData 元数据 JSON。"""
    os.makedirs(output_dir, exist_ok=True)
    result = subprocess.run(
        [HEPDATA_CLI, 'download', '-f', 'json', '-i', 'inspire', str(inspire_id), '-d', output_dir],
        capture_output=True, text=True, timeout=120
    )
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None

    for f in os.listdir(output_dir):
        if f.endswith('.json'):
            return os.path.join(output_dir, f)
    return None


def download_table_yaml(inspire_id, table_name):
    """下载指定表格的 YAML 数据。"""
    # 完整 URL 编码表格名 (处理空格、+、# 等特殊字符)
    from urllib.parse import quote
    encoded_name = quote(table_name, safe='')
    url = f'https://www.hepdata.net/download/table/ins{inspire_id}/{encoded_name}/yaml'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req, timeout=30)
    return response.read().decode('utf-8')


def parse_metadata(meta_path):
    """解析 HEPData 元数据 JSON，提取关键信息。"""
    with open(meta_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # record 信息
    record = data.get('record', {})
    tables = data.get('data_tables', [])

    # 分类表格
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
        'inspire_id': data.get('inspire_id', ''),
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
    """解析观测值 YAML 数据。
    
    返回: (observables, qualifiers)
    observables: list of {header, value, errors, qualifiers}
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
        qualifiers = var.get('qualifiers', [])
        
        for val in var.get('values', []):
            raw_value = val.get('value')
            obs = {
                'header': header,
                'value': str(raw_value) if raw_value is not None else '',
                'errors': [],
                'qualifiers': qualifiers,
            }
            
            for err in val.get('errors', []):
                err_info = {
                    'label': err.get('label', ''),
                }
                if 'symerror' in err:
                    se = err['symerror']
                    err_info['symerror'] = str(se) if se is not None else ''
                elif 'asymerror' in err:
                    ae = err['asymerror']
                    err_info['plus'] = str(ae.get('plus', '')) if ae.get('plus') is not None else ''
                    err_info['minus'] = str(ae.get('minus', '')) if ae.get('minus') is not None else ''
                obs['errors'].append(err_info)
            
            observables.append(obs)
    
    return observables, {'global': global_qualifiers}


def parse_yaml_correlation(yaml_text):
    """解析关联/协方差矩阵 YAML 数据。
    
    返回: (matrix_type, matrix, qualifiers)
    matrix_type: 'correlation' 或 'covariance'
    matrix: 二维列表
    """
    if not HAS_YAML:
        return 'unknown', [], {}
    
    data = yaml.safe_load(yaml_text)
    if not data or 'dependent_variables' not in data:
        return 'unknown', [], {}
    
    # 判断矩阵类型
    matrix_type = 'correlation'
    for var in data.get('dependent_variables', []):
        header = var.get('header', {}).get('name', '').lower()
        if 'covariance' in header:
            matrix_type = 'covariance'
            break
    
    # 提取矩阵值 (按行展开)
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
    
    # 重组为二维矩阵
    n = int(len(values) ** 0.5)
    if n * n != len(values):
        print(f"Warning: Matrix size {len(values)} is not a perfect square")
        return matrix_type, [], qualifiers
    
    matrix = []
    for i in range(n):
        row = values[i*n:(i+1)*n]
        matrix.append(row)
    
    return matrix_type, matrix, qualifiers


def main():
    parser = argparse.ArgumentParser(description='提取 HEPData 论文数据')
    parser.add_argument('inspire_id', help='InspireHEP control number')
    parser.add_argument('--output_dir', '-o', default='/tmp/hepdata_out', help='输出目录')
    parser.add_argument('--table', '-t', help='只下载指定表格')
    args = parser.parse_args()

    inspire_id = args.inspire_id
    output_dir = args.output_dir

    print(f"Fetching HEPData for Inspire ID: {inspire_id}")

    # Step 1: 获取表格列表
    print("\n=== Step 1: Available Tables ===")
    tables = fetch_table_names(inspire_id)
    if tables:
        if isinstance(tables, list):
            print(f"Total tables: {len(tables)}")
            if len(tables) <= 20:
                print(", ".join(tables))
            else:
                print(", ".join(tables[:10]) + f", ... ({len(tables)} total)")
        else:
            print(tables)

    # Step 2: 下载元数据
    print("\n=== Step 2: Downloading Metadata ===")
    meta_path = download_metadata(inspire_id, output_dir)
    if not meta_path:
        print("Failed to download metadata.")
        sys.exit(1)

    print(f"Metadata saved to: {meta_path}")

    # Step 3: 解析元数据
    print("\n=== Step 3: Metadata Summary ===")
    info = parse_metadata(meta_path)

    print(f"Title: {info['record']['title']}")
    print(f"arXiv: {info['record']['arxiv_id']}")
    print(f"DOI: {info['record']['doi']}")
    print(f"Collaboration: {', '.join(info['record']['collaborations'])}")
    print(f"Total tables: {info['total_tables']}")
    print(f"  Observable tables: {len(info['observable_tables'])}")
    print(f"  Correlation tables: {len(info['correlation_tables'])}")

    # 打印关联矩阵的 q² 区间
    if info['correlation_tables']:
        print(f"\nCorrelation/Covariance matrix bins:")
        for t in info['correlation_tables'][:5]:
            print(f"  {t['name']}: {t['description'][:80]}...")
        if len(info['correlation_tables']) > 5:
            print(f"  ... and {len(info['correlation_tables']) - 5} more")

    # Step 4: 下载指定表格 (可选)
    if args.table:
        print(f"\n=== Step 4: Downloading {args.table} ===")
        yaml_data = download_table_yaml(inspire_id, args.table)
        yaml_path = os.path.join(output_dir, f'{args.table.replace(" ", "_")}.yaml')
        with open(yaml_path, 'w') as f:
            f.write(yaml_data)
        print(f"YAML saved to: {yaml_path}")
        
        # 尝试解析
        if 'correlation' in args.table.lower() or 'covariance' in args.table.lower():
            mtype, matrix, quals = parse_yaml_correlation(yaml_data)
            print(f"Matrix type: {mtype}")
            print(f"Matrix size: {len(matrix)}x{len(matrix[0]) if matrix else 0}")
            print(f"Qualifiers: {quals}")
        else:
            observables, quals = parse_yaml_observables(yaml_data)
            print(f"Found {len(observables)} observables")
            for obs in observables[:3]:
                print(f"  {obs['header']}: {obs['value']} (errors: {len(obs['errors'])})")

    # 输出 JSON 摘要
    summary_path = os.path.join(output_dir, 'hepdata_summary.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=4, ensure_ascii=False)
    print(f"\nSummary saved to: {summary_path}")


if __name__ == '__main__':
    main()
