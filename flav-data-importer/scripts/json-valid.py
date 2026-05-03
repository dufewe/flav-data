#!/usr/bin/env python3
"""
验证 flav-data JSON 文件的格式和数据完整性。

Usage:
    python3 json-valid.py <path/to/file.json> [path/to/file2.json ...]

Checks:
    1. JSON 可解析
    2. 顶层必填字段完整
    3. obs@N 条目有必填字段 (name, latex, value/upper_limit)
    4. 数值字段必须是字符串
    5. 关联矩阵对称且对角线 = 1.0
    6. 协方差矩阵对称
    7. LaTeX 字段非空
    8. 跃迁符号符合 A.B.2.C.D 格式
    9. arxiv 字段包含版本号
"""

import json
import re
import sys
import os

REQUIRED_TOP_FIELDS = [
    'inspire-hep', 'author', 'collaboration', 'title',
    'arxiv', 'time', 'abstract', 'pdf', 'data', 'transition-mode'
]

# 标准测量值必填字段
REQUIRED_OBS_FIELDS_WITH_VALUE = [
    'name', 'latex', 'value',
    'type@1_err', 'type@1_err_up', 'type@1_err_down'
]

# 上限格式必填字段
REQUIRED_OBS_FIELDS_WITH_UPPER = [
    'name', 'latex',
    'type@1_upper_limit', 'type@1_level'
]

# 外部参考值格式必填字段
REQUIRED_OBS_FIELDS_WITH_REF = [
    'name', 'latex', 'value',
    'tot_err_up', 'tot_err_down', 'ref'
]

# 总误差格式必填字段 (无 ref)
REQUIRED_OBS_FIELDS_WITH_TOT_ERR = [
    'name', 'latex', 'value',
    'tot_err_up', 'tot_err_down'
]

# 数值字段模式（用于检查是否应为字符串）
NUMERIC_FIELD_PATTERNS = [
    'value', 'q2min', 'q2max', 'pTmin', 'pTmax', 'etamin', 'etamax',
    'type@1_err_up', 'type@1_err_down', 'type@2_err_up', 'type@2_err_down',
    'type@3_err_up', 'type@3_err_down',
    'type@1_upper_limit', 'type@2_upper_limit', 'type@3_upper_limit',
    'tot_err_up', 'tot_err_down'
]


def validate_transition_symbol(name):
    """检查观测量 name 是否包含正确的跃迁符号格式 A.B.2.C.D。"""
    issues = []
    # 提取括号中的跃迁部分
    match = re.search(r'\(([^)]+)\)', name)
    if match:
        transition = match.group(1)
        if '.2.' not in transition:
            issues.append(f"  跃迁符号 '{transition}' 缺少 '.2.' 分隔符，应为 A.B.2.C.D 格式")
        # 检查是否有多余的 .2. (如 A.2.B.2.C.D 多道)
        # 允许多道格式 (如 p.p.2.W+.2.mu+.nu)
        parts = transition.split('.')
        if len(parts) < 4:
            issues.append(f"  跃迁符号 '{transition}' 至少需要 A.B.2.C.D (4 部分)，实际只有 {len(parts)} 部分")
    return issues


def validate_latex(text, field_name, obs_key):
    """检查 LaTeX 字段非空。
    JSON 解析后单反斜杠是正常的，原文件应有双反斜杠。"""
    issues = []
    if not text or not text.strip():
        issues.append(f"  {obs_key}.{field_name}: LaTeX 字段为空")
    return issues


def validate_correlation(matrix, data_entry_idx, is_covariance=False):
    """检查关联矩阵: 对称且对角线 = 1.0。
    协方差矩阵只检查对称性 (对角线应为 err²，但误差值分散在不同字段中，需人工核对)。"""
    issues = []
    n = len(matrix)
    # 检查矩形
    for i, row in enumerate(matrix):
        if not isinstance(row, list) or len(row) != n:
            issues.append(f"  data[{data_entry_idx}]: 矩阵第 {i} 行长度 ({len(row) if isinstance(row, list) else 'N/A'}) 与列数 ({n}) 不一致")
            return issues
    # 检查元素类型
    for i in range(n):
        for j in range(n):
            if not isinstance(matrix[i][j], (int, float)):
                issues.append(f"  data[{data_entry_idx}]: 矩阵元素 [{i}][{j}] 不是数值 (实际为 {type(matrix[i][j]).__name__})")
                return issues
    for i in range(n):
        if not is_covariance:
            # 关联矩阵: 对角线应为 1.0
            if abs(matrix[i][i] - 1.0) > 0.001:
                issues.append(
                    f"  data[{data_entry_idx}]: 关联矩阵对角线 [{i}][{i}] = {matrix[i][i]}, 应为 1.0"
                )
        # 对称性
        for j in range(i + 1, n):
            if abs(matrix[i][j] - matrix[j][i]) > 0.001:
                issues.append(
                    f"  data[{data_entry_idx}]: 矩阵不对称 [{i}][{j}] = {matrix[i][j]} vs [{j}][{i}] = {matrix[j][i]}"
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

    # 3. 检查 arxiv 版本号
    arxiv = data.get('arxiv', '')
    if arxiv and 'v' not in arxiv.split(']')[0]:
        all_issues.append(f"  arxiv 字段缺少版本号，应为 [arxiv_idvN](url) 格式")

    # 4. 检查 data 数组
    data_entries = data.get('data', [])
    if not data_entries:
        all_issues.append("  data 数组为空")
        print("  [WARN] data 数组为空")

    for entry_idx, entry in enumerate(data_entries):
        # 找 obs@N 键
        obs_keys = []
        for k in entry:
            if k.startswith('obs@'):
                try:
                    num = int(k.split('@')[1])
                    obs_keys.append((num, k))
                except (ValueError, IndexError):
                    # obs@ 后面不是数字，跳过或报告
                    all_issues.append(f"  data[{entry_idx}]: 无效的 obs 键 '{k}'，应为 obs@N 格式 (N 为整数)")
                    continue
        obs_keys.sort(key=lambda x: x[0])
        obs_keys = [k for _, k in obs_keys]

        if not obs_keys:
            # 检查是否有 correlation/covariance 矩阵但没有 obs
            has_matrix = any('correlation' in k.lower() or 'covariance' in k.lower() for k in entry)
            if not has_matrix:
                all_issues.append(f"  data[{entry_idx}]: 没有 obs@N 条目")
            continue

        for obs_key in obs_keys:
            obs = entry[obs_key]

            # 判断是标准值格式、上限格式、外部参考值格式还是总误差格式
            has_value = 'value' in obs
            has_upper = any(k.endswith('_upper_limit') for k in obs)
            has_ref = 'ref' in obs and 'tot_err_up' in obs
            has_tot_err = 'tot_err_up' in obs and 'tot_err_down' in obs

            # 格式判定优先级:
            # 1. 有 ref + tot_err + value → 外部参考值格式
            # 2. 有 tot_err + value (无 ref) → 总误差格式 (论文自身合并误差)
            # 3. 有 type@1_upper_limit → 上限格式
            # 4. 有 value + type@1_err → 标准测量值格式

            if has_ref and has_value:
                # 外部参考值格式
                for field in REQUIRED_OBS_FIELDS_WITH_REF:
                    if field not in obs:
                        all_issues.append(f"  {obs_key}: 缺少必填字段: {field}")
            elif has_tot_err and has_value:
                # 总误差格式 (无 ref)
                for field in REQUIRED_OBS_FIELDS_WITH_TOT_ERR:
                    if field not in obs:
                        all_issues.append(f"  {obs_key}: 缺少必填字段: {field}")
            elif has_upper:
                # 上限格式
                for field in REQUIRED_OBS_FIELDS_WITH_UPPER:
                    if field not in obs:
                        all_issues.append(f"  {obs_key}: 缺少必填字段: {field}")
            elif has_value:
                # 标准测量值格式
                for field in REQUIRED_OBS_FIELDS_WITH_VALUE:
                    if field not in obs:
                        all_issues.append(f"  {obs_key}: 缺少必填字段: {field}")
            else:
                all_issues.append(f"  {obs_key}: 缺少 'value' 或 'type@1_upper_limit' 字段")

            # 检查数值为字符串
            for field in NUMERIC_FIELD_PATTERNS:
                if field in obs and not isinstance(obs[field], str):
                    all_issues.append(
                        f"  {obs_key}.{field}: 应为字符串，实际为 {type(obs[field]).__name__}"
                    )

            # 检查 LaTeX
            if 'latex' in obs:
                all_issues.extend(validate_latex(obs['latex'], 'latex', obs_key))

            # 检查跃迁符号
            if 'name' in obs:
                all_issues.extend(validate_transition_symbol(obs['name']))

        # 检查关联矩阵/协方差矩阵
        for corr_key in entry:
            if 'correlation' in corr_key.lower() or 'covariance' in corr_key.lower():
                if not isinstance(entry[corr_key], list):
                    all_issues.append(f"  {corr_key}: 应为二维数组")
                    continue
                matrix = entry[corr_key]
                is_covariance = 'covariance' in corr_key.lower()
                all_issues.extend(validate_correlation(matrix, entry_idx, is_covariance))

                # 检查矩阵维度是否匹配 obs 数量
                if len(matrix) != len(obs_keys):
                    all_issues.append(
                        f"  data[{entry_idx}]: 矩阵维度 ({len(matrix)}x{len(matrix)}) "
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
