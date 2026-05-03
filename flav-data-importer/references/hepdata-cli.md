# hepdata-cli 使用方法

## 基本信息

- **路径**: `/hepdata-cli`
- **用途**: 通过 HEPData API 获取高能物理实验数据
- **优势**: 绕过 Cloudflare 防护，直接访问 HEPData 结构化数据

## 可用命令

```bash
hepdata-cli --help

Commands:
  download     下载 HEPData 记录数据
  fetch-names  获取表格名称列表
  find         搜索 HEPData 记录
  upload       上传数据到 HEPData
```

## fetch-names (获取表格列表)

```bash
hepdata-cli fetch-names -i inspire 1409497
```

返回 JSON 数组:
```json
["Table 1", "Table 2", "Table 3", ..., "Table 83"]
```

## download (下载元数据)

```bash
hepdata-cli download -f json -i inspire 1409497 -d /tmp/hepdata_out
```

下载的 metadata JSON 包含:

### 顶层字段

| 字段 | 说明 |
|------|------|
| `recid` | HEPData 记录 ID |
| `inspire_id` | 对应 InspireHEP 控制号 |
| `data_tables` | 表格列表 (含下载 URL) |
| `record` | 论文元数据 (标题、摘要、DOI、合作组等) |

### record 字段

```json
"record": {
  "title": "Angular analysis of the $B^{0}\\rightarrow K^{*0}\\mu^{+}\\mu^{-}$ decay",
  "arxiv_id": "arXiv:1512.04442",
  "doi": "10.1007/JHEP02(2016)104",
  "collaborations": ["LHCb"],
  "abstract": "...",
  "year": 2016,
  "hepdata_doi": "10.17182/hepdata.74247.v1"
}
```

### data_tables 字段

每个表格包含:

```json
{
  "name": "Table 1",
  "description": "CP-averaged angular observables...",
  "location": "Data from Appendix A, Table 3",
  "doi": "10.17182/hepdata.74247.v1/t1",
  "data": {
    "csv": "https://www.hepdata.net/download/table/ins1409497/Table 1/csv",
    "json": "https://www.hepdata.net/download/table/ins1409497/Table 1/json",
    "yaml": "https://www.hepdata.net/download/table/ins1409497/Table 1/yaml",
    ...
  }
}
```

## 下载具体表格数据

metadata 只包含 URL，需要额外 curl 下载:

> 注意: metadata 中的 URL 路径部分 (如 "Table 1") 含有空格等特殊字符，
> 用于 curl 时需要进行 URL 编码 (空格 → `%20`)。

```bash
# 下载观测值数据 (YAML 格式推荐)
curl -sL -A "Mozilla/5.0" "https://www.hepdata.net/download/table/ins1409497/Table%201/yaml"

# 下载关联矩阵
curl -sL -A "Mozilla/5.0" "https://www.hepdata.net/download/table/ins1409497/Table%209/yaml"
```

## YAML 数据格式

### 观测值数据

```yaml
dependent_variables:
- header: {name: '$F_L$'}          # 可观测量名
  qualifiers:
  - {name: RE, value: 'P P --> B0 < K*...'}
  - {name: SQRT(S), units: GeV, value: '7000.0'}
  values:
  - errors:
    - asymerror: {minus: -0.036, plus: 0.035}
      label: stat
    - {label: sys, symerror: 0.017}
    value: 0.69                          # 中心值
```

关键字段:
- `dependent_variables[].header.name` — 可观测量名 (LaTeX)
- `dependent_variables[].values[].value` — 中心值
- `dependent_variables[].values[].errors[].label` — 误差类型 (stat/sys)
- `dependent_variables[].values[].errors[].symerror` — 对称误差
- `dependent_variables[].values[].errors[].asymerror` — 非对称误差 (plus/minus)
- `qualifiers[].name` — 运动学变量名 (如 $q^2$)
- `qualifiers[].value` — 运动学变量值 (如 0.1-0.98)

### 关联矩阵

```yaml
dependent_variables:
- header: {name: ''}
  qualifiers:
  - {name: '$q^2$', units: GeV^2, value: 0.1-0.98}
  values:
  - {value: 1.0}    # [0,0]
  - {value: 0.06}   # [0,1]
  - {value: 0.0}    # [0,2]
  ...
```

- values 按行展开的矩阵元素
- 需要根据矩阵大小重组成二维数组

## 常见 LHCb 论文 HEPData 对照表

| arXiv | Inspire ID | HEPData Record | 说明 |
|-------|-----------|----------------|------|
| 1512.04442 | 1409497 | ins1409497 | B0->K*mumu 角分析 (LHCb:2015svh) |

## 注意事项

1. **必须使用 hepdata-cli** — 直接 curl hepdata.net 会被 Cloudflare 阻挡
2. **理论论文通常无 HEPData** — 纯理论论文没有实验数据条目
3. **URL 中的空格需要编码** — "Table 1" → "Table%201"
4. **units 字段** — 可能包含 "10^-8" 等字符串，需要转换
5. **"-" 值** — 某些 bin 的 `val` 可能为 `"-"` (无效值)，需跳过
6. **User-Agent** — curl 时需要设置 User-Agent 头
