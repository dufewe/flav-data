#!/usr/bin/env python3
"""
验证 flav-data JSON 文件的格式和数据完整性。

Usage:
    python3 json-valid.py <path/to/file.json> [path/to/file2.json ...]

Checks:
    1. JSON 可解析
    2. 顶层必填字段完整
    3. obs@N 条目有必填字段
    4. 数值字段必须是字符串
    5. 关联矩阵对称且对角线 = 1.0
    6. LaTeX 字段非空
"""

import json
import sys
import os

REQUIRED_TOP_FIELDS = [
    'inspire-hep', 'author', 'collaboration', 'title',
    'arxiv', 'time', 'abstract', 'pdf', 'data', 'transition-mode'
]

REQUIRED_OBS_FIELDS = [
    'name', 'latex', 'value',
    'type@1_err', 'type@1_err_up', 'type@1_err_down'
]


def validate_latex(text, field_name, obs_key):
    """检查 LaTeX 字段非空。
    JSON 解析后单反斜杠是正常的，原文件应有双反斜杠。"""
    issues = []
    if not text or not text.strip():
        issues.append(f"  {obs_key}.{field_name}: LaTeX 字段为空")
    return issues


def validate_correlation(matrix, data_entry_idx):
    """检查关联矩阵: 对称且对角线 = 1.0。"""
    issues = []
    n = len(matrix)
    for i in range(n):
        # 对角线
        if abs(matrix[i][i] - 1.0) > 0.001:
            issues.append(
                f"  data[{data_entry_idx}]: 对角线 [{i}][{i}] = {matrix[i][i]}, 应为 1.0"
            )
        # 对称性
        for j in range(i + 1, n):
            if abs(matrix[i][j] - matrix[j][i]) > 0.001:
                issues.append(
                    f"  data[{data_entry_idx}]: 不对称 [{i}][{j}] = {matrix[i][j]} vs [{j}][{i}] = {matrix[j][i]}"
                )
    return issues


def validate_json(file_path):
    """验证单个 flav-data JSON 文件。"""
    print(f"验证: {file_path}")
    all_issues = []

    # 1. 解析 JSON
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("  [OK] JSON 格式正确")
    except json.JSONDecodeError as e:
        print(f"  [FAIL] JSON 解析错误: {e}")
        return [f"JSON 解析错误: {e}"]

    # 2. 检查顶层字段
    for field in REQUIRED_TOP_FIELDS:
        if field not in data:
            all_issues.append(f"  缺少必填字段: {field}")
    if not all_issues:
        print("  [OK] 顶层字段完整")

    # 3. 检查数据条目
    data_entries = data.get('data', [])
    if not data_entries:
        all_issues.append("  data 数组为空")
        print("  [WARN] data 数组为空")

    for entry_idx, entry in enumerate(data_entries):
        # 找 obs@N 键
        obs_keys = sorted(
            [k for k in entry if k.startswith('obs@')],
            key=lambda x: int(x.split('@')[1])
        )

        if not obs_keys:
            # 检查是否有 correlation matrix 但没有 obs
            has_corr = any('correlation' in k.lower() for k in entry)
            if not has_corr:
                all_issues.append(f"  data[{entry_idx}]: 没有 obs@N 条目")
            continue

        for obs_key in obs_keys:
            obs = entry[obs_key]
            for field in REQUIRED_OBS_FIELDS:
                if field not in obs:
                    all_issues.append(f"  {obs_key}: 缺少必填字段: {field}")

            # 检查数值为字符串
            for field in ['value', 'q2min', 'q2max', 'type@1_err_up', 'type@1_err_down']:
                if field in obs and not isinstance(obs[field], str):
                    all_issues.append(
                        f"  {obs_key}.{field}: 应为字符串，实际为 {type(obs[field]).__name__}"
                    )

            # 检查 LaTeX
            if 'latex' in obs:
                all_issues.extend(validate_latex(obs['latex'], 'latex', obs_key))

        # 检查关联矩阵
        for corr_key in entry:
            if 'correlation' in corr_key.lower() and isinstance(entry[corr_key], list):
                matrix = entry[corr_key]
                all_issues.extend(validate_correlation(matrix, entry_idx))

                # 检查矩阵维度是否匹配 obs 数量
                if len(matrix) != len(obs_keys):
                    all_issues.append(
                        f"  data[{entry_idx}]: 关联矩阵维度 ({len(matrix)}x{len(matrix)}) "
                        f"与观测量数量 ({len(obs_keys)}) 不匹配"
                    )

    # 报告结果
    if all_issues:
        print(f"  [FAIL] 发现 {len(all_issues)} 个问题:")
        for issue in all_issues:
            print(issue)
    else:
        print("  [OK] 所有检查通过")

    return all_issues


def main():
    if len(sys.argv) < 2:
        print(f"用法: python3 {sys.argv[0]} <path/to/file.json> [path/to/file2.json ...]")
        sys.exit(1)

    total_issues = 0
    for path in sys.argv[1:]:
        if not os.path.exists(path):
            print(f"文件不存在: {path}")
            total_issues += 1
            continue
        issues = validate_json(path)
        total_issues += len(issues)
        print()

    if total_issues == 0:
        print("所有文件验证通过。")
        sys.exit(0)
    else:
        print(f"共发现 {total_issues} 个问题。")
        sys.exit(1)


if __name__ == '__main__':
    main()
