---
name: flav-data-importer
description: 用于从味物理实验组或理论组数据文章中抽取结构化数据并保存为完整的json文件。当用户说要从某篇文章或某个网站中提取、更新、删除、验证数据时使用该技能
category: data-science
tags: [flavor-physics, data-collecting, json-importer, lhcb, hepdata, streamlit]
---

# flav-data Importer

从味物理实验/理论论文中提取结构化数据，导入为 flav-data 标准 JSON 格式。

## 文件夹结构

```
flav-data-importer/
├── SKILL.md                              # 本文件 (主技能文档)
├── references/                           # 参考资料
│   ├── file-index.md                     # 目录结构和文件索引规则
│   ├── obs-abbr.md                       # 衰变模式缩写与观测量命名
│   ├── json-meta.md                      # JSON 元数据格式规范
│   ├── data-source.md                    # 数据源优先级与使用指南
│   ├── arxiv-api.md                      # arXiv API 使用方法
│   ├── inspirehep-api.md                 # InspireHEP API 使用方法
│   └── hepdata-cli.md                    # hepdata-cli 使用方法
├── scripts/                              # Python 脚本
│   ├── arxiv-ext.py                      # 从 arXiv 提取论文信息并下载 PDF
│   ├── hepdata-ext.py                    # 从 HEPData 提取数据
│   ├── inspirehep-ext.py                 # 从 InspireHEP 提取论文元数据
│   └── json-valid.py                     # 验证 JSON 文件格式
└── assets/                               # 工作流案例
    └── workflow-lhcb-2015svh.md          # B0->K*mumu 角分析数据导入完整流程
```

## 什么时候使用

- **数据添加**: 将新的实验/理论测量数据导入数据库
- **数据更新**: 用论文新版本或 HEPData 更新替换已有数据
- **数据删除**: 从数据库中移除错误/过时的数据文件
- **数据验证**: 检查已有 JSON 文件是否符合格式规范 (不修改文件)

## 数据库位置

实验数据存储在: `/Users/dufewe/Backup/Selia/projects/2HDM-SMEFT/Fitting/Streamlit/flav-data/Experimental/`

目录结构: `Experimental/{group}/{year}/{month}/{file_id}.json`
- `group`: ATLAS, BaBar, Belle, CMS, HFLAV, LEP, LHCb, PDG 等
- `file_id`: InspireHEP texkey (如 `LHCb:2015svh`)
- 年度索引: `Experimental/{group}/{year}/{group}@{year}.json`

详细索引规则参见 `references/file-index.md`。

## 工作流

### 步骤一: 搜索确认

1. 根据 arXiv ID / Inspire ID / 论文标题在数据库索引中搜索
2. 确认是否已存在该数据文件
3. 参考 `references/file-index.md` 进行索引查询

### 步骤二: 获取数据

按 `references/data-source.md` 中的数据源优先级获取数据:

1. **HEPData** (首选) → 使用 `scripts/hepdata-ext.py` 或 hepdata-cli
2. **CDS** → curl 搜索 CERN 文档服务器
3. **LHCb Public Pages** → 分析结果页面
4. **arXiv PDF** → 使用 pymupdf 从 PDF 提取 (作为备选)
5. **vision_analyze** → 用户提供表格截图时使用

同时获取论文元数据:
- **arXiv API** → v1 提交日期、标题、摘要、作者
  - 使用 `scripts/arxiv-ext.py`
  - 参考 `references/arxiv-api.md`
- **InspireHEP API** → Inspire ID、DOI、期刊信息、合作组
  - 使用 `scripts/inspirehep-ext.py`
  - 参考 `references/inspirehep-api.md`

### 步骤三: 数据操作

#### 数据添加
1. 按 `references/file-index.md` 确定文件路径
2. 按 `references/json-meta.md` 构建 JSON 元数据
3. 按 `references/obs-abbr.md` 命名观测量
4. 从数据源提取数值填充到 JSON
5. 写入文件到 `Experimental/{group}/{year}/{month}/`
6. 更新年度索引文件

#### 数据更新
1. 找到已有的 `xxxx.json` 文件
2. 对比新旧数据
3. 更新有变化的字段

#### 数据删除
1. 找到对应的 `xxxx.json` 文件并删除
2. 从年度索引文件中移除该 file_id

#### 数据验证
1. 找到 `xxxx.json` 文件
2. 使用 `scripts/json-valid.py` 验证
3. 与源论文数据对比 (不修改文件)

### 步骤四: 验证

```bash
python3 scripts/json-valid.py <path/to/file.json>
```

检查项:
- JSON 可解析
- 顶层字段完整 (inspire-hep, author, collaboration, title, arxiv, time, abstract, pdf, data, transition-mode)
- obs@N 有必填字段 (name, latex, value, type@1_err, type@1_err_up, type@1_err_down)
- 数值字段为字符串
- 关联矩阵对称且对角线 = 1.0
- LaTeX 非空

### 步骤五: 清除缓存

完成操作后清除所有临时文件，保持数据库整洁。

## JSON 格式要点

```json
{
    "inspire-hep": "[LHCb:2015svh](https://inspirehep.net/literature/1409497)",
    "author": "Aaij, Roel and others",
    "collaboration": "LHCb",
    "title": "Angular analysis of the $B^0\\to K^{*0}\\mu^+\\mu^-$ decay",
    "arxiv": "[1512.04442v1](https://arxiv.org/pdf/1512.04442)",
    "time": "2015.12.14",
    "abstract": "...",
    "pdf": "https://arxiv.org/pdf/1512.04442",
    "data": [
        {
            "obs@1": {
                "name": "FL(B02Kstmumu)",
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
            "tot_correlation": [[1.0, 0.06, ...], [0.06, 1.0, ...], ...]
        }
    ],
    "transition-mode": "semi-leptonic decay"
}
```

完整格式规范参见 `references/json-meta.md`。

## 必备工具

| 工具 | 用途 |
|------|------|
| arXiv API | 获取 v1 提交日期、标题、摘要 |
| InspireHEP API | 获取 Inspire ID、DOI、期刊信息 |
| hepdata-cli | 获取 HEPData 机器可读数据 |
| web-search / web-extract | 搜索和提取网页内容 |
| vision_analyze | 表格图片数据提取 |
| pymupdf | PDF 文本提取 |
| terminal | 运行 Python 脚本 |

## 常见问题

### 新观测量
当论文中出现 `obs-abbr.md` 中没有的新观测量时，按命名规则添加到 `references/obs-abbr.md`。

### 新数据信息
当论文中出现 `json-meta.md` 中没有的新字段时，总结归纳后添加到 `references/json-meta.md`。

### 关联矩阵不匹配
关联矩阵维度必须等于同一 data entry 中 obs@N 的数量，顺序也要一致。

### 理论论文无 HEPData
纯理论计算论文通常没有 HEPData 条目，需要从 PDF 中提取理论曲线数据。

### 数值必须为字符串
JSON 中所有数值字段 (`value`, `q2min`, `type@1_err_up` 等) 必须存储为字符串，如 `"0.69"` 而非 `0.69`。

### LaTeX 转义
JSON 文件中 LaTeX 使用双反斜杠，如 `\\to` 而非 `\to`。Python 解析后变成单反斜杠是正常的。

### 索引文件更新
每次添加新文件后必须更新年度索引文件 `LHCb@2025.json`，月份键必须零填充 ("01" 到 "12")。
