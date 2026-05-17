# ---------------------------------------------------------
# Load packages and definitions
# ---------------------------------------------------------
with open('./defs.py', 'r', encoding='utf-8') as f:
    exec(f.read())

# ---------------------------------------------------------
# Electroweak Precision Observable Descriptions
# ---------------------------------------------------------
st.markdown('''
# 电弱精确观测量 (EWPO)

本页面描述电弱精确观测量的符号约定与分类。与味物理观测量不同，EWPO 主要涉及 Z 玻色子极化观测量、W 玻色子参数、以及弱混合角等。

## 符号约定

EWPO 观测量使用 `OBS(particle_or_process)[condition]` 格式命名：
- **OBS**：观测量缩写（见下表）
- **particle_or_process**：相关粒子或过程标识
- **condition**：可选限定符（如能量标度、味道标签）
''')

# ---------------------------------------------------------
# Z-Pole Observables
# ---------------------------------------------------------
st.markdown('''
## Z 极点观测量

### 衰变宽度

| 缩写 | LaTeX | 说明 |
|------|-------|------|
| `Gamma_Z` | $\\Gamma_Z$ | Z 玻色子总宽度 |
| `Gamma_had` | $\\Gamma_{\\rm had}$ | Z 强子衰变宽度 |
| `Gamma_inv` | $\\Gamma_{\\rm inv}$ | Z 不可见衰变宽度 |
| `Gamma_l` | $\\Gamma_\\ell$ | Z 轻子衰变宽度（单味道） |

### 峰截面

| 缩写 | LaTeX | 说明 |
|------|-------|------|
| `sigma_had_0` | $\\sigma_{\\rm had}^0$ | Z 峰强子截面 |
| `R_l` | $R_\\ell$ | $\\Gamma_{\\rm had} / \\Gamma_\\ell$ |
| `R_b` | $R_b$ | $\\Gamma_b / \\Gamma_{\\rm had}$ |
| `R_c` | $R_c$ | $\\Gamma_c / \\Gamma_{\\rm had}$ |

### 前后不对称性

| 缩写 | LaTeX | 说明 |
|------|-------|------|
| `AFB_l` | $A_{FB}^{0,\\ell}$ | 轻子峰前后不对称性 |
| `AFB_b` | $A_{FB}^{0,b}$ | b 夸克峰前后不对称性 |
| `AFB_c` | $A_{FB}^{0,c}$ | c 夸克峰前后不对称性 |

### 极化不对称性

| 缩写 | LaTeX | 说明 |
|------|-------|------|
| `A_l` | $A_\\ell$ | 轻子不对称参数 $A_\\ell = 2g_V g_A / (g_V^2 + g_A^2)$ |
| `A_b` | $A_b$ | b 夸克不对称参数 |
| `A_c` | $A_c$ | c 夸克不对称参数 |
| `A_FB_b` | $A_{FB}^{0,b}$ | b 夸克峰前后不对称性 |
| `A_LR` | $A_{LR}$ | 左右不对称性 (SLD) |
''')

# ---------------------------------------------------------
# W Boson Observables
# ---------------------------------------------------------
st.markdown('''
## W 玻色子观测量

| 缩写 | LaTeX | 说明 |
|------|-------|------|
| `Mass_W` | $M_W$ | W 玻色子质量 |
| `Gamma_W` | $\\Gamma_W$ | W 玻色子总宽度 |
| `Br(W_lnu)` | $\\mathcal{B}(W \\to \\ell\\nu)$ | W 轻子衰变分支比 |
| `Br(W_had)` | $\\mathcal{B}(W \\to {\\rm had})$ | W 强子衰变分支比 |
''')

# ---------------------------------------------------------
# Weak Mixing Angle
# ---------------------------------------------------------
st.markdown('''
## 弱混合角

| 缩写 | LaTeX | 说明 |
|------|-------|------|
| `sin2theta_eff` | $\\sin^2\\theta_{\\rm eff}^{\\ell}$ | 有效弱混合角 |
| `sin2theta_W` | $\\sin^2\\theta_W$ | On-shell 弱混合角 |
''')

# ---------------------------------------------------------
# Higgs Observables
# ---------------------------------------------------------
st.markdown('''
## Higgs 玻色子观测量

| 缩写 | LaTeX | 说明 |
|------|-------|------|
| `Mass_H` | $M_H$ | Higgs 玻色子质量 |
| `Br(H_bb)` | $\\mathcal{B}(H \\to b\\bar{b})$ | Higgs → bb 分支比 |
| `Br(H_tau)` | $\\mathcal{B}(H \\to \\tau^+\\tau^-)$ | Higgs → ττ 分支比 |
| `Br(H_mumu)` | $\\mathcal{B}(H \\to \\mu^+\\mu^-)$ | Higgs → μμ 分支比 |
| `Br(H_gg)` | $\\mathcal{B}(H \\to gg)$ | Higgs → gg 分支比 |
| `Br(H_gammagamma)` | $\\mathcal{B}(H \\to \\gamma\\gamma)$ | Higgs → γγ 分支比 |
| `Br(H_ZZ)` | $\\mathcal{B}(H \\to ZZ^*)$ | Higgs → ZZ* 分支比 |
| `Br(H_WW)` | $\\mathcal{B}(H \\to WW^*)$ | Higgs → WW* 分支比 |
| `Sigma(pp_H)` | $\\sigma(pp \\to H)$ | Higgs 产生截面 |
| `kappa_f` | $\\kappa_f$ | Higgs-费米子耦合修正因子 |
| `kappa_V` | $\\kappa_V$ | Higgs-矢量玻色子耦合修正因子 |
''')

# ---------------------------------------------------------
# Other EWPO
# ---------------------------------------------------------
st.markdown('''
## 其他电弱观测量

### 低能观测量

| 缩写 | LaTeX | 说明 |
|------|-------|------|
| `g_mu_2` | $g-2$ | 缪子反常磁矩 $a_\\mu = (g-2)/2$ |
| `Delta_alpha_had` | $\\Delta\\alpha_{\\rm had}^{(5)}(M_Z^2)$ | 强子真空极化贡献 |
| `Q_W` | $Q_W$ | 原子宇称破坏弱荷 |

### S, T, U 参数

| 缩写 | LaTeX | 说明 |
|------|-------|------|
| `S` | $S$ | Oblique 修正参数 S |
| `T` | $T$ | Oblique 修正参数 T |
| `U` | $U$ | Oblique 修正参数 U |

### Fermi 常数

| 缩写 | LaTeX | 说明 |
|------|-------|------|
| `G_F` | $G_F$ | Fermi 耦合常数 |
| `alpha_em` | $\\alpha_{\\rm em}$ | 精细结构常数 |
| `alpha_s` | $\\alpha_s$ | 强耦合常数 |
''')

# ---------------------------------------------------------
# Transition-mode classification for EWPO
# ---------------------------------------------------------
st.markdown('''
## EWPO 跃迁模式分类

与味物理类似，EWPO 数据条目也使用 `transition-mode` 字段分类：

| transition-mode 值 | 适用范围 | 示例 |
|-------------------|---------|------|
| `electroweak precision` | Z 极点、W 质量、弱混合角 | LEP/SLC Z-pole |
| `W production` | W 玻色子产生与衰变 | Tevatron/LHC W cross sections |
| `Higgs decay` | Higgs 玻色子衰变 | $H \\to \\gamma\\gamma$, $H \\to ZZ^*$ |
| `Higgs production` | Higgs 玻色子产生 | $pp \\to H$, VBF, ttH |
| `low energy` | 低能精确测量 | $g-2$, 原子宇称破坏 |
| `oblique corrections` | S, T, U 参数拟合 | New physics constraints |
| `scattering` | 电弱散射过程 | $e^+e^- \\to f\\bar{f}$ |
''')
