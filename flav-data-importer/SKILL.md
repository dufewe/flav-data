---
name: flav-data-importer
description: 用于从味物理实验组或理论组数据文章中抽取结构化数据并保存为完整的 json 文件。当用户说要从某篇文章或某个网站中提取、更新、删除、验证数据时使用该技能
category: data-science
tags: [flavor-physics, data-collecting, json-importer, hepdata]
---

# flav-data Importer

从味物理实验/理论论文中提取结构化数据，导入为 flav-data 标准 JSON 格式。

## 文件夹结构

```
flav-data-importer/
├── SKILL.md                              # 本文件 (主技能文档)
├── references/                           # 参考资料
│   ├── file-index.md                     # 目录结构和文件索引规则
│   ├── obs-abbr.md                       # 跃迁符号约定、衰变模式缩写与观测量命名
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

> 注: 本目录树展示的是 `flav-data-importer` 工具自身结构。
> 数据库根目录为 `flav-data/`，数据文件存储在 `flav-data/Experimental/` 和 `flav-data/Theoretical/` 下。

## 什么时候使用

- **数据添加**: 将新的实验/理论测量数据导入数据库
- **数据更新**: 用论文新版本或 HEPData 更新替换已有数据
- **数据删除**: 从数据库中移除错误/过时的数据文件
- **数据验证**: 检查已有 JSON 文件是否符合格式规范 (不修改文件)

## 数据库位置

数据库根目录: `flav-data/`

实验数据存储在: `flav-data/Experimental/`
理论数据存储在: `flav-data/Theoretical/`

实验目录结构: `Experimental/{group}/{year}/{month}/{file_id}.json`
- `group`: ATLAS, BaBar, Belle, BESIII, CDF, CMS, HFLAV, LEP, LHCb, PDG 等
- `file_id`: InspireHEP texkey (如 `LHCb:2015svh`)
- 年度索引: `Experimental/{group}/{year}/{group}@{year}.json`

理论目录结构: `Theoretical/{group}/{year}/{month}/{file_id}.json`
- `group`: HPQCD, RBC/UKQCD, FNAL/MILC, JLQCD 等
- `file_id`: InspireHEP texkey (如 `LHCb:2015svh`)
- 年度索引: `Theoretical/{group}/{year}/{group}@{year}.json`

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
5. **ar5iv HTML** → `https://ar5iv.labs.arxiv.org/html/<arxiv_id>` 表格解析
6. **vision_analyze** → 用户提供表格截图时使用

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
2. 按 `references/obs-abbr.md` 确定跃迁符号和观测量命名
3. 按 `references/json-meta.md` 构建 JSON 元数据
4. 从数据源提取数值填充到 JSON
5. 写入文件到 `Experimental/{group}/{year}/{month}/` 或 `Theoretical/{group}/{year}/{month}/`
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
- obs@N 有必填字段: 标准值 (name, latex, value, type@1_err, type@1_err_up, type@1_err_down)、上限值 (name, latex, type@1_upper_limit, type@1_level)、总误差 (name, latex, value, tot_err_up, tot_err_down) 或外部参考值 (name, latex, value, tot_err_up, tot_err_down, ref)
- 数值字段为字符串
- 关联矩阵: 对角线必须为 1.0，矩阵必须对称
- 协方差矩阵: 只需对称（对角线为误差平方，需人工核对）
- LaTeX 非空
- 跃迁符号符合 `A.B.2.C.D` 约定
- 观测量命名符合 `OBS(transition)[condition]` 约定

### 步骤五: 清除缓存

完成操作后清除所有临时文件，保持数据库整洁。

## 核心规范摘要

### 跃迁符号约定 (`A.B.2.C.D`)

对于 $A + B \to C + D$ 跃迁模式，简写为 `A.B.2.C.D`，其中 $\to$ 写为 `2` 以区分初末态。

- 粒子按电荷 `+`、`-`、`0` 顺序排列
- 反粒子记为 `Bar` (如 `B0Bar`)，带电粒子直接用电荷标记
- 中微子不需要带味道
- 示例: `$B^0 \to e^+ e^-$` → `B0.2.e+.e-`，`$W^- \to \mu^- \bar{\nu}_\mu$` → `W-.2.mu-.nuBar`

详见 `references/obs-abbr.md` 第 1 节。

### 观测量命名 (`OBS(transition)[condition]`)

- `OBS` 为观测量缩写，按观测属性分为: 分支比、衰变宽度、寿命、质量、截面、角分布系数、CP 不对称、优化观测量、比值、CKM 参数等
- `transition` 为跃迁符号
- `condition` 为可选条件 (如 `[mu/e]` 表示轻子味比值), 单跃迁道过程一般不使用
- 多跃迁道共用粒子用 `l1`, `l2`, `q1`, `q2`, `nu1`, `nu2`, `h1`, `h2` 等表示
- 示例: `$\mathcal{B}(B^0 \to \mu^+\mu^-)/\mathcal{B}(B^0 \to e^+e^-)$` → `R(B0.2.l+.l-)[mu/e]`

详见 `references/obs-abbr.md` 第 2 节。

### 数值格式

- **所有数值必须为字符串** — `"0.69"` 而非 `0.69`
- 误差格式: `type@N_err`, `type@N_err_up`, `type@N_err_down` (N=1,2,3...)
- 上限格式: `type@N_upper_limit`, `type@N_level` (如 `"90%@CLs"`)
- 运动学条件: `q2min`/`q2max`, `pTmin`/`pTmax`, `etamin`/`etamax` 等
- 有量纲量必须有 `unit` 字段 (如 `"unit": "MeV"`, `"unit": "GeV"`, `"unit": "ps"`)
- 引用数据需加 `ref` 字段 (Markdown 链接)
- JSON 文件使用 **4 空格缩进**

### JSON 格式示例

```json
{
    "inspire-hep": "[LHCb:2015svh](https://inspirehep.net/literature/1409497)",
    "author": "Aaij, Roel and others",
    "collaboration": "LHCb",
    "title": "Angular analysis of the $B^{0}\\to K^{*0}\\mu^{+}\\mu^{-}$ decay",
    "arxiv": "[1512.04442v1](https://arxiv.org/pdf/1512.04442)",
    "time": "2015.12.14",
    "abstract": "...",
    "pdf": "https://arxiv.org/pdf/1512.04442",
    "data": [
        {
            "obs@1": {
                "name": "FL(B0.2.Kst0.mu+.mu-)",
                "latex": "$F_L(B^{0}\\to K^{*0}\\mu^{+}\\mu^{-})$",
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
            "obs@2": { ... },
            "tot_correlation": [[1.0, 0.06, ...], [0.06, 1.0, ...], ...]
        }
    ],
    "transition-mode": "semi-leptonic decay"
}
```

完整格式规范参见 `references/json-meta.md`。

## 必备工具

| 工具 | 用途 | 路径/说明 |
|------|------|----------|
| arXiv API | 获取 v1 提交日期、标题、摘要 | `https://export.arxiv.org/api/query` |
| InspireHEP API | 获取 Inspire ID、DOI、期刊信息 | `https://inspirehep.net/api/literature` |
| hepdata-cli | 获取 HEPData 机器可读数据 | `/hepdata-cli` |
| web-search / web-extract | 搜索和提取网页内容 | |
| vision_analyze | 表格图片数据提取 | |
| pymupdf | PDF 文本提取 | `/python/site-packages` (不在沙箱中，需 terminal 运行) |
| terminal | 运行 Python 脚本 | |

## 常见问题

### 新观测量
当论文中出现 `obs-abbr.md` 中没有的新观测量时，按命名规则添加到 `references/obs-abbr.md`。

### 新数据信息
当论文中出现 `json-meta.md` 中没有的新字段时，总结归纳后添加到 `references/json-meta.md`。

### 关联矩阵/协方差矩阵不匹配
矩阵维度必须等于同一 data entry 中 obs@N 的数量，顺序也要一致。关联矩阵对角线为 1.0，协方差矩阵为误差值的平方。

### 理论论文无 HEPData
纯理论计算论文通常没有 HEPData 条目，需要从 PDF 中提取理论曲线数据。

### ref 字段
当 data entry 需要 `ref` 字段引用来源文献 (如组合结果引用前期论文) 时，**必须**从论文原文的引用列表中找到该文献的 arXiv 号或 Inspire 编号，然后在 **InspireHEP 上搜索获取正确的 TexKey 和 Inspire ID**。**严禁凭空猜测** TexKey。

正确流程:
1. 从论文原文引用列表找到文献的 arXiv 号
2. 在 InspireHEP 搜索该 arXiv 号
3. 获取 TexKey 和 Inspire ID 
4. 写为 Markdown 链接

### LaTeX 转义
JSON 文件中 LaTeX 使用双反斜杠，如 `\\\\to` 而非 `\\to`。Python 解析后变成单反斜杠是正常的。

### 索引文件更新
每次添加新文件后必须更新年度索引文件，如 `LHCb@2025.json`，月份键必须零填充 ("01" 到 "12")。
