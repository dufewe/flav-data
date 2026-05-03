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
| `arxiv` | string | 是 | Markdown 链接: `[arxiv_id_with_version](https://arxiv.org/pdf/{id})`，**必须带版本号** | `[1512.04442v1](https://arxiv.org/pdf/1512.04442)` |
| `time` | string | 是 | arXiv v1 首次提交日期 YYYY.MM.DD | `2015.12.14` |
| `abstract` | string | 是 | 论文摘要 (LaTeX 格式) | `An angular analysis of the...` |
| `pdf` | string | 是 | PDF URL | `https://arxiv.org/pdf/1512.04442` |
| `data` | array | 是 | 数据条目数组 (每个 q² 区间或数据集一个条目) | 见下方 |
| `transition-mode` | string | 是 | 跃迁模式分类 | `semi-leptonic decay`, `leptonic decay` 等 |

## 数据条目 (data[])

`data` 数组包含多个条目，每个条目对应一个 q² 区间、数据集或测量组：

### 观测量条目 (obs@N)

#### 标准测量值格式 (有中心值和误差)

```json
{
    "obs@1": {
        "name": "FL(B0.2.Kst0.mu+.mu-)",
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
| `name` | string | 是 | 观测量标识符: `OBS(transition)[condition]` |
| `latex` | string | 是 | LaTeX 表示 (JSON 中双反斜杠) |
| `value` | string | 是 | 中心值 (必须为字符串!) |
| `type@1_err` | string | 是 | 误差类型1 (通常 "stat") |
| `type@1_err_up` | string | 是 | 上误差1 (字符串) |
| `type@1_err_down` | string | 是 | 下误差1 (字符串) |
| `type@2_err` | string | 否 | 误差类型2 (通常 "syst") |
| `type@2_err_up` | string | 否 | 上误差2 (字符串) |
| `type@2_err_down` | string | 否 | 下误差2 (字符串) |
| `type@N_err` | string | 否 | 第 N 种误差类型 (如 "lumi", "norm", "theo") |
| `type@N_err_name` | string | 视情况 | 当误差类型名与编号不一致时使用 |
| `q2min`/`q2max` | string | 视情况 | q² 区间 (或其他运动学变量) |
| `pTmin`/`pTmax` | string | 视情况 | pT 区间 |
| `etamin`/`etamax` | string | 视情况 | 赝快度区间 |
| `unit` | string | 视情况 | 单位 (有量纲量必须) |
| `ref` | string | 视情况 | 外部参考来源的 Markdown 链接 |

**注意**:
- 对称误差时 `err_up` = `err_down`
- 对于非 q² 分 bin 的数据 (如 W 截面)，使用 `pTmin/pTmax` 或 `etamin/etamax` 代替
- 误差类型: `stat`, `syst`, `lumi`, `norm`, `theo`, `expe`, `tot` 等

#### 上限格式 (Upper Limit)

当论文给出的是置信度上限而非中心值时:

```json
{
    "obs@1": {
        "name": "Br(B0.2.Kst0.tau-.e+)",
        "latex": "$\\mathcal{B}(B^0\\to K^{*0} \\tau^- e^+)$",
        "type@1_upper_limit": "5.9e-6",
        "type@1_level": "90%@CLs",
        "type@2_upper_limit": "7.1e-6",
        "type@2_level": "95%@CLs"
    }
}
```

| 字段 | 说明 |
|------|------|
| `type@N_upper_limit` | 第 N 种误差类型对应的上限值 (字符串) |
| `type@N_level` | 置信度水平，格式 `"xx%@CLs"` |

#### 总误差格式 (无外部参考)

当论文给出总误差 (统计+系统合并) 但不是来自外部参考时:

```json
{
    "name": "FL(B0.2.Kst0.mu+.mu-)",
    "latex": "$F_L(B^0\\to K^{*0}\\mu^+\\mu^-)$",
    "value": "0.69",
    "tot_err_up": "0.039",
    "tot_err_down": "0.039",
    "q2min": "0.1",
    "q2max": "1.1"
}
```

与外部参考值格式的区别: 没有 `ref` 字段，数据来自当前论文本身。

#### 外部参考值格式

来自 PDG 或其他论文的参考值使用不同的误差格式:

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

### 关联矩阵 (tot_correlation / type@N_correlation)

关联矩阵放在数据条目层级 (不在 obs@N 内):

```json
{
    "obs@1": { ... },
    "obs@2": { ... },
    "obs@3": { ... },
    "tot_correlation": [[1.0, 0.5, 0.1], [0.5, 1.0, 0.2], [0.1, 0.2, 1.0]]
}
```

按误差类型分别指定关联矩阵:

```json
{
    "obs@1": {
        ...,
        "type@1_err": "stat",
        "type@1_err_up": ...,
        "type@1_err_down": ...,
        ...
    },
    "obs@2": {
        ...,
        "type@1_err": "stat",
        "type@1_err_up": ...,
        "type@1_err_down": ...
    },
    "type@1_correlation": [[1.0, 0.015], [0.015, 1.0]]
}
```

**规则**:
- 压缩为单行数组格式
- 关联矩阵: 对角线必须为 1.0，矩阵必须对称
- 协方差矩阵: 对角线为各观测量对应误差类型的方差 (err²)
- 如果没有关联矩阵或协方差矩阵，省略该字段 (不要设为 null)
- 矩阵维度 = 同一条目中 obs@N 的数量
- 矩阵的顺序必须与 obs@N 的编号顺序一致
- 矩阵名称与误差类型对应: `tot_correlation` (总), `type@1_correlation` (stat), `type@2_correlation` (syst) 等; `tot_correlation` 用于总误差关联矩阵，`type@N_correlation` 用于按误差类型分别指定

### 协方差矩阵 (covariance)

当提供协方差而非关联矩阵时:

```json
{
    "obs@1": { ... },
    "obs@2": { ... },
    "covariance": [[0.01, 0.005], [0.005, 0.01]]
}
```

## transition-mode 常见值

| 值 | 说明 |
|----|------|
| `semi-leptonic decay` | 半轻衰变 (B → K(*)ℓℓ, Λ → pℓν 等) |
| `leptonic decay` | 纯轻衰变 (B → ℓℓ, τ → μμμ 等) |
| `non-leptonic decay` | 非轻衰变 (B → J/ψ p π 等) |
| `radiative decay` | 辐射衰变 (B → ργ, B → J/ψ γ 等) |
| `scattering` | 散射过程 (pp → W, pp → tt̄ 等) |

## 关键约束

1. **所有数值必须是字符串** — `"0.25"` 而不是 `0.25` (适用于 value/error/q2min/unit 等字段; 关联/协方差矩阵元素应为浮点数)
2. **LaTeX 双反斜杠** — JSON 文件中 `\\to` 而不是 `\to`
3. **4 空格缩进** — JSON 使用 4 空格缩进
4. **字段顺序** — 按照上述文档顺序排列字段
5. **关联矩阵** — 对称、对角线 = 1.0、维度匹配 obs 数量
6. **arxiv 必须带版本号** — `[1512.04442v1]` 而非 `[1512.04442]`
7. **跃迁符号** — 符合 `A.B.2.C.D` 约定，粒子按电荷 + - 0 排序
8. **观测量命名** — 符合 `OBS(transition)[condition]` 约定
