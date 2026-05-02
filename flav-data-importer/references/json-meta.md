# JSON 元数据结构

## 顶层结构

每个实验数据论文对应一个 JSON 文件，结构如下：

```json
{
    "inspire-hep": "[LHCb:2015svh](https://inspirehep.net/literature/1409497)",
    "author": "Aaij, Roel and others",
    "collaboration": "LHCb",
    "title": "Angular analysis of the $B^{0}\\to K^{*0}\\mu^{+}\\mu^{-}$ decay",
    "arxiv": "[1512.04442v1](https://arxiv.org/pdf/1512.04442)",
    "time": "2015.12.14",
    "abstract": "An angular analysis of the $B^{0}\\to K^{*0}(\\to K^{+}\\pi^{-})\\mu^{+}\\mu^{-}$ decay...",
    "pdf": "https://arxiv.org/pdf/1512.04442",
    "data": [
        {
            "obs@1": { ... },
            "obs@2": { ... },
            "tot_correlation": [[1.0, 0.5], [0.5, 1.0]]
        }
    ],
    "transition-mode": "semi-leptonic decay"
}
```

## 顶层元数据字段

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `inspire-hep` | string | 是 | Markdown 链接: `[TexKey](https://inspirehep.net/literature/{recid})` | `[LHCb:2015svh](https://inspirehep.net/literature/1409497)` |
| `author` | string | 是 | 第一作者 + " and others" | `Aaij, Roel and others` |
| `collaboration` | string | 是 | 实验合作组名称 | `LHCb`, `ATLAS`, `CMS`, `Belle` |
| `title` | string | 是 | 论文标题 (LaTeX 格式，双反斜杠转义) | `Angular analysis of the $B^{0}\\to K^{*0}\\mu^{+}\\mu^{-}$ decay` |
| `arxiv` | string | 是 | Markdown 链接: `[arxiv_id](https://arxiv.org/pdf/{id})` | `[1512.04442v1](https://arxiv.org/pdf/1512.04442)` |
| `time` | string | 是 | v1 提交日期 YYYY.MM.DD | `2015.12.14` |
| `abstract` | string | 是 | 论文摘要 (LaTeX 格式) | `An angular analysis of the...` |
| `pdf` | string | 是 | PDF URL | `https://arxiv.org/pdf/1512.04442` |
| `data` | array | 是 | 数据条目数组 (每个 q² 区间一个条目) | 见下方 |
| `transition-mode` | string | 是 | Streamlit 过滤用的跃迁类型 | `semi-leptonic decay` |

## 数据条目 (data[])

`data` 数组包含多个条目，每个条目对应一个 q² 区间或数据集：

### 观测量条目 (obs@N)

```json
{
    "obs@1": {
        "name": "FL(B02Kstmumu)",
        "latex": "$F_L(B^0\\to K^{*0}\\mu^+\\mu^-)$",
        "value": "0.69",
        "type@1_err": "stat",
        "type@1_err_up": "0.12",
        "type@1_err_down": "0.12",
        "type@2_err": "syst",
        "type@2_err_up": "0.06",
        "type@2_err_down": "0.06",
        "q2min": "0.1",
        "q2max": "1.1"
    }
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 观测量标识符: `OBS(decay_abbreviation)` |
| `latex` | string | 是 | LaTeX 表示 (JSON 中双反斜杠) |
| `value` | string | 是 | 中心值 (必须为字符串!) |
| `type@1_err` | string | 是 | 误差类型1 (通常 "stat") |
| `type@1_err_up` | string | 是 | 上统计误差 (字符串) |
| `type@1_err_down` | string | 是 | 下统计误差 (字符串) |
| `type@2_err` | string | 否 | 误差类型2 (通常 "syst") |
| `type@2_err_up` | string | 否 | 上系统误差 (字符串) |
| `type@2_err_down` | string | 否 | 下系统误差 (字符串) |
| `q2min` | string | 视情况 | q² 下界 (或其他运动学变量) |
| `q2max` | string | 视情况 | q² 上界 (或其他运动学变量) |

**注意**: 对于非 q² 分 bin 的数据 (如 W 截面)，使用 `pTmin/pTmax` 或 `eta_min/eta_max` 代替。

### 外部参考值格式

来自 PDG 或其他论文的参考值使用不同的误差格式：

```json
{
    "name": "R(Lambda.2.p)[mu/e]",
    "latex": "$\\mathcal{R}_{\\Lambda \\to p}^{\\mu/e}$",
    "value": "0.175",
    "tot_err_up": "0.012",
    "tot_err_down": "0.012",
    "ref": "[ParticleDataGroup:2024cfk](https://inspirehep.net/literature/2817040)"
}
```

| 字段 | 说明 |
|------|------|
| `tot_err_up` | 总上误差 (对称误差时上=下) |
| `tot_err_down` | 总下误差 |
| `ref` | 外部参考来源的 Markdown 链接 |

### 关联矩阵 (tot_correlation)

关联矩阵放在数据条目层级 (不在 obs@N 内)：

```json
{
    "obs@1": { ... },
    "obs@2": { ... },
    "obs@3": { ... },
    "tot_correlation": [[1.0, 0.5, 0.1], [0.5, 1.0, 0.2], [0.1, 0.2, 1.0]]
}
```

**规则**:
- 压缩为单行数组格式
- 对角线必须为 1.0
- 矩阵必须对称
- 如果没有关联矩阵，省略该字段 (不要设为 null)
- 矩阵维度 = 同一条目中 obs@N 的数量
- 关联矩阵的顺序必须与 obs@N 的编号顺序一致

## transition-mode 常见值

| 值 | 说明 |
|----|------|
| `semi-leptonic decay` | B 介子半轻衰变 |
| `W boson production` | W 玻色子产生截面 |
| `top quark production` | 顶夸克产生截面 |
| `Higgs boson production` | 希格斯玻色子测量 |
| `lepton flavor universality` | 轻子味普适性检验 |
| `baryonic decay` | 重子衰变 |

## 关键约束

1. **所有数值必须是字符串** — `"0.25"` 而不是 `0.25`
2. **LaTeX 双反斜杠** — JSON 文件中 `\\to` 而不是 `\to`
3. **4 空格缩进** — JSON 使用 4 空格缩进
4. **字段顺序** — 按照上述文档顺序排列字段
5. **关联矩阵** — 对称、对角线 = 1.0、维度匹配 obs 数量
