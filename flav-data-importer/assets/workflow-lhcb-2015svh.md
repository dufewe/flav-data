# 工作流案例: 添加 LHCb:2015svh (B0->K*mumu 角分析)

## 案例概述

- **论文**: Angular analysis of the B0→K*0μ+μ- decay (LHCb:2015svh)
- **arXiv**: 1512.04442
- **Inspire**: 1409497
- **HEPData**: ins1409497 (83 张表)
- **发表**: JHEP 02 (2016) 104

---

## 完整执行流程

### 步骤 1: 文件搜索 (检查是否已存在)

```python
# 搜索索引文件
import json, os
base = 'Experimental/LHCb'
for year in sorted(os.listdir(base)):
    if year.isdigit():
        idx = os.path.join(base, year, f'LHCb@{year}.json')
        if os.path.exists(idx):
            with open(idx) as f:
                data = json.load(f)
            for m, files in data.items():
                if 'LHCb:2015svh' in files:
                    print(f"已存在: {year}/{m}/LHCb:2015svh.json")
```

结果: 未发现 → 需要添加

### 步骤 2: 获取元数据 (InspireHEP API)

```bash
curl -s -H 'Accept: application/json' \
  'https://inspirehep.net/api/literature?q=eprint:1512.04442'
```

提取关键信息:
- `texkey`: `"LHCb:2015svh"`
- `control_number`: `1409497`
- `preprint_date`: `"2015-12-14"` → `time: "2015.12.14"`
- `collaborations`: `[{"value": "LHCb"}]`
- `authors`: 500+ 人 → `"Aaij, Roel and others"`
- `titles` (arXiv source): `"Angular analysis of the $B^{0}\\to K^{*0}\\mu^{+}\\mu^{-}$ decay"`
- `abstracts` (arXiv source): "An angular analysis of the..."

### 步骤 3: 获取提交日期 (arXiv API)

```bash
curl -sL "https://export.arxiv.org/api/query?id_list=1512.04442"
```

提取:
- `published`: `"2015-12-14T16:00:00Z"` → 确认 `time: "2015.12.14"`

### 步骤 4: 获取实验数据 (HEPData)

```bash
HEPDATA_CLI="/hepdata-cli"

# 获取表格列表
$HEPDATA_CLI fetch-names -i inspire 1409497
# 返回: ["Table 1", "Table 2", ..., "Table 83"]

# 下载元数据
$HEPDATA_CLI download -f json -i inspire 1409497 -d /tmp/hepdata_1512
```

识别表格类型:
- Table 1-8: 各 q² bin 的观测值 (FL, S3-S9, A3-A9, P1-P3, P'4, P'5, P'8)
- Table 9-18: Likelihood correlation matrices (Appendix C)
- Table 19-28: Likelihood correlation matrices (Appendix D)
- Table 29-38: Likelihood correlation matrices (Appendix E)
- Table 39-53: Bootstrap correlation matrices (Appendix F)
- Table 54-68: Bootstrap correlation matrices (Appendix G)
- Table 69-83: Bootstrap correlation matrices (Appendix H)

### 步骤 5: 下载具体数据

```bash
# 下载 Table 1 (观测值，低 q² bin)
curl -sL -A "Mozilla/5.0" \
  "https://www.hepdata.net/download/table/ins1409497/Table%201/yaml" \
  > /tmp/table1.yaml

# 下载 Table 9 (关联矩阵, 0.1 < q² < 0.98)
curl -sL -A "Mozilla/5.0" \
  "https://www.hepdata.net/download/table/ins1409497/Table%209/yaml" \
  > /tmp/table9.yaml
```

### 步骤 6: 解析并构建 JSON

从 YAML 解析为 flav-data JSON 格式:

```json
{
    "inspire-hep": "[LHCb:2015svh](https://inspirehep.net/literature/1409497)",
    "author": "Aaij, Roel and others",
    "collaboration": "LHCb",
    "title": "Angular analysis of the $B^0\\to K^{*0}\\mu^+\\mu^-$ decay",
    "arxiv": "[1512.04442v1](https://arxiv.org/pdf/1512.04442)",
    "time": "2015.12.14",
    "abstract": "An angular analysis of the $B^{0}\\rightarrow K^{*0}(\\rightarrow K^{+}\\pi^{-})\\mu^{+}\\mu^{-}$ decay...",
    "pdf": "https://arxiv.org/pdf/1512.04442",
    "data": [
        {
            "obs@1": {
                "name": "FL(B0.2.Kst0.mu+.mu-)",
                "latex": "$F_L(B^0\\to K^{*0}\\mu^+\\mu^-)$",
                "value": "0.69",
                "type@1_err": "stat",
                "type@1_err_up": "0.035",
                "type@1_err_down": "0.036",
                "type@2_err": "syst",
                "type@2_err_up": "0.017",
                "type@2_err_down": "0.017",
                "q2min": "0.1",
                "q2max": "1.1"
            },
            "obs@2": {
                "name": "S3(B0.2.Kst0.mu+.mu-)",
                "latex": "$S_3(B^0\\to K^{*0}\\mu^+\\mu^-)$",
                "value": "0.012",
                "type@1_err": "stat",
                "type@1_err_up": "0.038",
                "type@1_err_down": "0.038",
                "type@2_err": "syst",
                "type@2_err_up": "0.004",
                "type@2_err_down": "0.004",
                "q2min": "0.1",
                "q2max": "1.1"
            },
            "...": "...",
            "tot_correlation": [[1.0, 0.06, ...], [0.06, 1.0, ...], ...]
        }
    ],
    "transition-mode": "semi-leptonic decay"
}
```

### 步骤 7: 写入文件并更新索引

```bash
# 创建目录
mkdir -p Experimental/LHCb/2015/12

# 写入 JSON 文件
# → Experimental/LHCb/2015/12/LHCb:2015svh.json

# 更新年度索引文件
# 编辑 Experimental/LHCb/2015/LHCb@2015.json，添加月份键和 file_id:
```

索引文件更新后 (`LHCb@2015.json`):
```json
{
    "12": ["LHCb:2015svh"]
}
```

手动更新索引时的注意事项:
- 键为零填充月份字符串 ("01" 到 "12")
- 值为 file_id 数组（不含 `.json` 后缀）
- 月份内 file_id 按 arXiv v1 提交日期排序
- 如果该月份已存在，将新 file_id 追加到对应数组并重新排序

### 步骤 8: 验证

```bash
python3 scripts/json-valid.py Experimental/LHCb/2015/12/LHCb:2015svh.json
```

期望输出:
```
验证: Experimental/LHCb/2015/12/LHCb:2015svh.json
  [OK] JSON 格式正确
  [OK] 顶层字段完整
  [OK] 所有检查通过
所有文件验证通过。
```

### 步骤 9: 清除缓存

```bash
rm -rf /tmp/hepdata_1512 /tmp/table*.yaml
```

---

## 关键经验

1. **HEPData 有 83 张表** — 需要区分观测值表和关联矩阵表
2. **多个附录的关联矩阵** — Appendix C/H 分别对应不同的拟合方法 (likelihood vs bootstrap)
3. **q² bin 很多** — 需要为每个 bin 创建一个 data entry
4. **观测值名称** — 使用新规范 `FL(B0.2.Kst0.mu+.mu-)`: 观测量缩写 + (跃迁道)
5. **LaTeX 双反斜杠** — JSON 文件中 `$B^0\\to K^{*0}\\mu^+\\mu^-$`
