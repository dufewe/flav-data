# 数据源优先级与使用指南

## 数据源优先级 (从高到低)

### 1. HEPData (首选 — 机器可读)

- **适用**: 有 HEPData 条目的实验论文
- **数据格式**: YAML/JSON，结构化，可直接解析
- **工具**: `hepdata-cli` (绕过 Cloudflare)
- **限制**: 纯理论论文通常没有 HEPData 条目

```bash
HEPDATA_CLI="/Users/dufewe/.hermes/hermes-agent/venv/bin/hepdata-cli"
$HEPDATA_CLI fetch-names -i inspire <inspire_id>
$HEPDATA_CLI download -f json -i inspire <inspire_id> -d /tmp/out
```

### 2. CDS (CERN Document Server)

- **适用**: 论文在 CDS 有补充材料
- **数据格式**: YAML/JSON/ROOT
- **URL**: `https://cds.cern.ch/record/<RECORD_ID>/`
- **搜索**: 按 arXiv ID 或论文标题搜索

```bash
curl -s "https://cds.cern.ch/search?f1=reportnumber&p1=<arxiv_id>&c=LHCb"
```

### 3. LHCb Public Analysis Pages

- **适用**: LHCb 官方分析结果页面
- **URL**: `https://lbfence.cern.ch/alcm/public/analysis/full-details/<ANALYSIS_ID>/`
- **数据格式**: YAML/JSON，含关联矩阵

### 4. arXiv PDF (最后手段)

- **适用**: 以上数据源都没有数据时
- **工具**: `pymupdf` (文本型 PDF) 或 `marker-pdf` (扫描型 PDF)
- **限制**: 需要从表格文本中解析数值，容易出错

```bash
python3 -c "
import pymupdf
doc = pymupdf.open('paper.pdf')
for page in doc:
    print(page.get_text())
"
```

**注意**: `pymupdf` 不在 execute_code 沙箱中，需要用 terminal 运行。
pymupdf 路径: `/Users/dufewe/Library/Python/3.9/lib/python/site-packages`

### 5. ar5iv HTML (替代方案)

- **适用**: HTML 格式比 PDF 更容易解析表格时
- **URL**: `https://ar5iv.labs.arxiv.org/html/<arxiv_id>`

```bash
curl -sL "https://ar5iv.labs.arxiv.org/html/<arxiv_id>" | grep -A 50 "Table"
```

### 6. InspireHEP API (仅元数据)

- **适用**: 获取论文元数据 (标题、作者、日期等)，不获取实验数据
- **工具**: `curl` + JSON 解析

### 7. 视觉模型 (表格图片)

- **适用**: 用户提供论文中的表格截图
- **工具**: `vision_analyze`
- **输出**: 直接解析为结构化数据

## 各数据源适用场景

| 场景 | 首选数据源 |
|------|-----------|
| LHCb 角分析论文 | HEPData |
| LHCb 分支比测量 | HEPData 或 CDS |
| Belle/BaBar 数据 | HEPData 或论文 PDF |
| PDG 综合值 | PDG 网站或 HEPData |
| HFLAV 平均 | HFLAV 网站 |
| 理论计算值 | 论文 PDF (pymupdf) |
| 表格截图 | vision_analyze |
