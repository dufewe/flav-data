# Transition Symbols and Observable Naming

This document defines the naming conventions for all transitions and observables in the flav-data database. It is the authoritative reference for constructing `name` and `latex` fields in JSON entries.

## 1. Transition Symbols: `A.B.2.C.D`

Every decay or scattering process is encoded as a transition symbol using the format `A.B.2.C.D`, representing $A + B \to C + D$. The number `2` replaces the arrow $\to$ to provide a clear, machine-parseable separator between initial and final states.

### Naming Rules

1. **Particle names**: Use English names or standard abbreviations (see particle table below).
2. **Charge indicators**: Every particle must carry its charge: `+`, `-`, or `0`. This applies to all particles without exception.
3. **Ordering**: Within each state (initial or final), particles are ordered by charge: `+` first, then `-`, then `0`.
4. **Antiparticles**: Append `Bar` to the particle name (e.g., `B0Bar`, `Kst0Bar`). **Exception**: charged particles use their charge directly instead of `Bar` (e.g., `W-` not `WBar`, `B-` not `BBar`).
5. **Neutrinos**: No flavor indicator — always use `nu` or `nuBar` regardless of the specific neutrino type ($\nu_e$, $\nu_\mu$, $\nu_\tau$).
6. **Multi-step processes**: Use additional `2` separators for cascade processes: `p.p.2.W+.2.mu+.nu` represents $pp \to W^+ \to \mu^+ \nu$.
7. **Intermediate resonances**: When an intermediate state decays to a dilepton pair, append `(2.l+.l-)` to the resonance name: `B0.2.Kst0.J/psi(2.l+.l-)` for $B^0 \to K^{*0} J/\psi(\to \ell^+\ell^-)$.

### Examples

| Process | LaTeX | Symbol | Notes |
|---------|-------|--------|-------|
| $B^0 \to e^+ e^-$ | Leptonic decay | `B0.2.e+.e-` | Standard: + then - |
| $\bar{B}^0 \to e^+ e^-$ | Leptonic decay | `B0Bar.2.e+.e-` | Antiparticle uses Bar |
| $B^+ \to K^+ \mu^+ \mu^-$ | Semileptonic | `B+.2.K+.mu+.mu-` | Final state: K+, mu+, mu- (same-charge particles ordered by appearance) |
| $W^- \to \mu^- \bar{\nu}_\mu$ | Leptonic decay | `W-.2.mu-.nuBar` | Charged W uses own charge |
| $B_s^0 \to \phi \mu^+ \mu^-$ | Semileptonic | `Bs0.2.phi.mu+.mu-` | Bs meson notation |
| $\Lambda_b^0 \to J/\psi\, p\, \pi^-$ | Non-leptonic | `Lambdab0.2.J/psi.p.pi-` | Baryon decay, final: + 0 - |
| $pp \to Z \to \mu^+ \mu^-$ | Scattering | `p.p.2.Z.2.mu+.mu-` | Two-step process |
| $e^+ e^- \to \mu^+ \mu^-$ | Scattering | `e+.e-.2.mu+.mu-` | Collider process |

### Particle Abbreviations

#### Mesons

| Particle | Symbol | Notes |
|----------|--------|-------|
| $B^0$, $B^+$, $B^-$ | `B0`, `B+`, `B-` | Charged particles always use charge indicator |
| $\bar{B}^0$ | `B0Bar` | Neutral antiparticles use Bar |
| $B_s^0$, $\bar{B}_s^0$ | `Bs0`, `Bs0Bar` | |
| $K^+$, $K^0$, $K_S^0$ | `K+`, `K0`, `KS0` | |
| $K^{*0}$, $\bar{K}^{*0}$ | `Kst0`, `Kst0Bar` | K-star resonance |
| $D^0$, $D^+$ | `D0`, `D+` | |
| $D^{*0}$, $D^{*+}$ | `Dst0`, `Dst+` | D-star resonance |
| $\pi^0$, $\pi^+$, $\pi^-$ | `pi0`, `pi+`, `pi-` | |
| $\rho^0$, $\rho^+$, $\rho^-$ | `rho0`, `rho+`, `rho-` | |
| $\phi$ | `phi` | Neutral vector meson |
| $J/\psi$ | `J/psi` | Charmonium |
| $\psi(2S)$ | `psi(2S)` | Charmonium excited state |
| $\eta$, $\eta'$ | `eta`, `etaprime` | |
| $D_s^+$, $D_s^{*+}$ | `Ds+`, `Dsst+` | Strange charmed meson |
| $B_c^+$ | `Bc+` | Bottom-charmed meson |
| $X_s$ | `Xs` | Inclusive strange hadronic system |

#### Baryons

| Particle | Symbol | Notes |
|----------|--------|-------|
| $\Lambda$, $\Lambda_c^+$, $\Lambda_b^0$ | `Lambda`, `Lambdac+`, `Lambdab0` | Anti-baryons: `LambdaBar`, `LambdacBar-`, `LambdabBar0` |
| $\Sigma^+$, $\Sigma^0$, $\Sigma^-$ | `Sigma+`, `Sigma0`, `Sigma-` | |
| $\Xi_c^0$, $\Xi_b^0$ | `Xic0`, `Xib0` | |
| $\Omega_c^0$ | `Omegac0` | |
| $p$, $n$ | `p`, `n` | Proton and neutron |

#### Leptons and Bosons

| Particle | Symbol | Notes |
|----------|--------|-------|
| $e^+$, $e^-$ | `e+`, `e-` | |
| $\mu^+$, $\mu^-$ | `mu+`, `mu-` | |
| $\tau^+$, $\tau^-$ | `tau+`, `tau-` | |
| $\nu$ (any flavor), $\bar{\nu}$ | `nu`, `nuBar` | No flavor tag |
| $W^+$, $W^-$, $Z$ | `W+`, `W-`, `Z` | |
| $\gamma$ | `gamma` | Photon |
| $t$, $\bar{t}$ | `t`, `tBar` | Top quark |

## 2. Observable Naming: `OBS(transition)[condition]`

Every measured quantity is named using the pattern `OBS(transition)[condition]`:

- **OBS**: a symbolic abbreviation representing the physical observable (see tables below). Use only symbols — never write full expression definitions.
- **transition**: the `A.B.2.C.D` transition symbol from Section 1.
- **condition**: an optional qualifier in square brackets, used ONLY for multi-transition observables such as ratios or differences between different lepton flavors. Do NOT use `[condition]` to distinguish measurements at different q² bins — use separate `data[]` entries with `q2min`/`q2max` instead.

### Single-Transition Observables

For observables measuring a single process, no condition is needed:

| Observable | LaTeX | Symbol | Notes |
|------------|-------|--------|-------|
| Branching fraction $\mathcal{B}(B^0 \to e^+ e^-)$ | $\mathcal{B}$ | `Br(B0.2.e+.e-)` | Standard decay |
| Decay width $\Gamma(K^{*0} \to K^+ \pi^-)$ | $\Gamma$ | `Gamma(Kst0.2.K+.pi-)` | Partial width |
| Differential branching fraction | $d\mathcal{B}/dq^2$ | `dBr/dq2(B0.2.Xs.gamma)` | |
| Mass $M_t$ | $M_f$ | `Mass(t)` | On-shell mass |
| Mass $M_Z$ | $M_Z$ | `Mass(Z)` | On-shell mass of a resonance |
| Lifetime $\tau_{e^-}$ | $\tau$ | `Tau(e-)` | |
| Cross section $\sigma(pp \to e^+ e^-)$ | $\sigma$ | `Sigma(p.p.2.e+.e-)` | |
| Charge asymmetry $A_C(B^+ \to J/\psi K^+)$ | $A_C$ | `AC` | Single-particle observable (no transition needed) |
| Mass difference $\Delta M_s$ | $\Delta M$ | `DeltaMass(Bs0.2.Bs0Bar)` | |
| Decay fraction $f(Z \to \mu^+ \mu^-)$ | $f$ | `f(Z.2.mu+.mu-)` | Branching fraction of a resonance |

### Multi-Transition Observables

For observables comparing two or more transitions (e.g., lepton flavor universality tests):

- **transition** uses the shared part of the multi-transition process.
- Shared particles are denoted generically: `l1`/`l2` (leptons), `q1`/`q2` (quarks), `nu1`/`nu2` (neutrinos), `h1`/`h2` (hadrons).
- **condition** encodes the flavor mapping, e.g., `[mu/e]` means l1 = μ, l2 = e.
  - **`/` (slash)** in condition → ratio: `R(B0.2.Kst0.l+.l-)[mu/e]` = $\mathcal{B}(\mu\mu)/\mathcal{B}(ee)$.
  - **`-` (dash)** in condition → difference: `DeltaACP(B-.2.l-.nuBar)[mu-e]` = $A_{CP}(\mu) - A_{CP}(e)$.

| Observable | LaTeX | Symbol | Notes |
|------------|-------|--------|-------|
| $R_{K^*} = \frac{\mathcal{B}(B^0 \to K^{*0}\mu^+\mu^-)}{\mathcal{B}(B^0 \to K^{*0}e^+e^-)}$ | $R$ | `R(B0.2.Kst0.l+.l-)[mu/e]` | Lepton flavor ratio |
| $R_K = \frac{\mathcal{B}(B^+ \to K^+\mu^+\mu^-)}{\mathcal{B}(B^+ \to K^+e^+e^-)}$ | $R$ | `R(B+.2.K+.l+.l-)[mu/e]` | |
| $A_{CP}(\mu) - A_{CP}(e)$ | $\Delta A_{CP}$ | `DeltaACP(B-.2.l-.nuBar)[mu-e]` | CP asymmetry difference |
| $r = \frac{A(B^- \to \bar{D}^0 K^-)}{A(B^- \to D^0 K^-)}$ | $r$ | `r(B-.2.D0.K-)` | Amplitude ratio (GLW/ADS) |
| $\delta = \arg \frac{A(B^- \to \bar{D}^0 K^-)}{A(B^- \to D^0 K^-)}$ | $\delta$ | `delta(B-.2.D0.K-)` | Strong phase difference |

**CKM parameters**: $r$ and $\delta$ are defined via $B^-$ decay amplitude ratios ($b \to u$ suppressed relative to $b \to c$ favored). The B meson and final-state meson in the transition must carry **negative charge**: `B-.2.D0.K-`, `B-.2.D0.pi-`.

### Observable Differences and Ratios (Unified Convention)

Unless otherwise specified, differences and ratios between observables follow these patterns:

| Type | Symbol | LaTeX | Example |
|------|--------|-------|---------|
| Difference | `DeltaOBS(transition)[condition]` | $\Delta_{OBS}^{condition}(transition)$ | `DeltaBr(B0.2.Kst0.l+.l-)[mu/e]` |
| Ratio | `ROBS(transition)[condition]` | $R_{OBS}^{condition}(transition)$ | `RFL(B0.2.Kst0.l+.l-)[mu/e]` |

Examples:
| LaTeX | Symbol | Description |
|-------|--------|-------------|
| $\Delta_{ACP}^{\mu/e}(B^0 \to K^{*0} \ell^+\ell^-)$ | `DeltaACP(B0.2.Kst0.l+.l-)[mu/e]` | CP asymmetry difference |
| $R_{FL}^{\mu/e}(B^0 \to K^{*0} \ell^+\ell^-)$ | `RFL(B0.2.Kst0.l+.l-)[mu/e]` | Longitudinal polarization ratio |
| $\Delta_{Br}^{\mu/e}(B^0 \to K^{*0} \ell^+\ell^-)$ | `DeltaBr(B0.2.Kst0.l+.l-)[mu/e]` | Branching fraction difference |

## 3. Observable Abbreviations

### Branching Fractions and Decay Widths

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `Br` | $\mathcal{B}$ | Branching fraction |
| `dBr/dq2` | $d\mathcal{B}/dq^2$ | Differential branching fraction |
| `Gamma` | $\Gamma$ | Decay width (partial or total) |

### Lifetimes

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `Tau` | $\tau$ | Particle lifetime |

### Masses and Mixing Parameters

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `Mass` | $M_f$ | On-shell mass (uppercase). Written as `Mass(f)` where $f$ is the particle symbol. |
| `mass` | $m$ | $\overline{\text{MS}}$ mass (lowercase) |
| `DeltaMass` | $\Delta M$ | Mass difference / neutral meson mixing parameter |

### Scattering Cross Sections

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `Sigma` | $\sigma$ | Total or fiducial cross section |
| `dSigma/dpT` | $d\sigma/dp_T$ | Differential cross section (transverse momentum) |
| `dSigma/deta` | $d\sigma/d\eta$ | Differential cross section (pseudorapidity) |

### Angular Coefficients (CP-averaged)

Angular coefficients parameterize the angular distribution of decay products. They are the coefficients in the Legendre polynomial expansion of the differential decay rate.

For $B^0 \to K^{*0}(\to K^+ \pi^-) \mu^+ \mu^-$, the standard basis uses 12 angular observables per q² bin (plus S-wave and CP-asymmetric extensions).

| Abbr | LaTeX | Description | Typical Range |
|------|-------|-------------|--------------|
| `S1c` | $S_1^c$ | Longitudinal amplitude coefficient | [0, 1] |
| `S2c` | $S_2^c$ | Transverse amplitude coefficient | [-1, 0] |
| `S2s` | $S_2^s$ | Transverse amplitude coefficient (sine component) | [-1, 0] |
| `S3` | $S_3$ | T-odd angular coefficient | [-0.5, 0.5] |
| `S4` | $S_4$ | Angular coefficient | [-1, 1] |
| `S5` | $S_5$ | Angular coefficient | [-1, 1] |
| `S6c` | $S_{6c}$ | Angular coefficient (c-component) | [-1, 1] |
| `AFB` | $A_{FB}$ | Forward-backward asymmetry of the dilepton system | [-1, 1] |
| `S7` | $S_7$ | T-odd angular coefficient | [-1, 1] |
| `S8` | $S_8$ | T-odd angular coefficient | [-1, 1] |
| `S9` | $S_9$ | T-odd angular coefficient | [-0.5, 0.5] |
| `FL` | $F_L$ | Longitudinal polarization fraction of the vector meson | [0, 1] |
| `FS` | $F_S$ | S-wave fraction | [0, 1] |
| `FH` | $F_H$ | Angular distribution flat term (B → Kℓℓ) | [-1, 1] |
| `S1ac` | $S_{1a}^c$ | Additional longitudinal coefficient | — |
| `S1bcre` | $S_{1bc}^{\mathrm{Re}}$ | Interference coefficient (real part) | — |
| `S1bcim` | $S_{1bc}^{\mathrm{Im}}$ | Interference coefficient (imaginary part) | — |

### S-wave Observables

When the $K^+ \pi^-$ system includes non-resonant S-wave contributions (not purely $K^{*0}$), additional observables are measured:

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `SS1re` | $S_{S1}^{\mathrm{Re}}$ | S-wave interference (real part) |
| `SS1im` | $S_{S1}^{\mathrm{Im}}$ | S-wave interference (imaginary part) |
| `SS2re` | $S_{S2}^{\mathrm{Re}}$ | S-wave interference (real part) |
| `SS2im` | $S_{S2}^{\mathrm{Im}}$ | S-wave interference (imaginary part) |
| `SS3re` | $S_{S3}^{\mathrm{Re}}$ | S-wave interference (real part) |
| `SS3im` | $S_{S3}^{\mathrm{Im}}$ | S-wave interference (imaginary part) |
| `SS4re` | $S_{S4}^{\mathrm{Re}}$ | S-wave interference (real part) |
| `SS4im` | $S_{S4}^{\mathrm{Im}}$ | S-wave interference (imaginary part) |
| `SS5re` | $S_{S5}^{\mathrm{Re}}$ | S-wave interference (real part) |
| `SS5im` | $S_{S5}^{\mathrm{Im}}$ | S-wave interference (imaginary part) |

### CP Asymmetry Observables

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `ACP` | $A_{CP}$ | Direct CP asymmetry |
| `DeltaACP` | $\Delta A_{CP}$ | Difference in CP asymmetry between two modes |
| `AFB_CP` | $A_{CP}^{FB}$ | CP asymmetry of forward-backward asymmetry |
| `AFS` | $A_{CP}^{FS}$ | CP asymmetry of S-wave fraction |
| `A1c` | $A_{1c}$ | CP asymmetry of $S_1^c$ |
| `A2s` | $A_{2s}$ | CP asymmetry of $S_2^s$ |
| `A3` | $A_3$ | CP asymmetry of $S_3$ |
| `A4` | $A_4$ | CP asymmetry of $S_4$ |
| `A5` | $A_5$ | CP asymmetry of $S_5$ |
| `A6c` | $A_{6c}$ | CP asymmetry of $S_{6c}$ |
| `A7` | $A_7$ | CP asymmetry of $S_7$ |
| `A8` | $A_8$ | CP asymmetry of $S_8$ |
| `A9` | $A_9$ | CP asymmetry of $S_9$ |

### CP-Asymmetric S-wave Observables

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `AS1im` | $A_{S1}^{\mathrm{Im}}$ | CP asymmetry of S-wave interference |
| `AS1re` | $A_{S1}^{\mathrm{Re}}$ | CP asymmetry of S-wave interference |
| `AS2im` | $A_{S2}^{\mathrm{Im}}$ | CP asymmetry of S-wave interference |
| `AS2re` | $A_{S2}^{\mathrm{Re}}$ | CP asymmetry of S-wave interference |
| `AS3im` | $A_{S3}^{\mathrm{Im}}$ | CP asymmetry of S-wave interference |
| `AS3re` | $A_{S3}^{\mathrm{Re}}$ | CP asymmetry of S-wave interference |
| `AS4im` | $A_{S4}^{\mathrm{Im}}$ | CP asymmetry of S-wave interference |
| `AS4re` | $A_{S4}^{\mathrm{Re}}$ | CP asymmetry of S-wave interference |
| `AS5im` | $A_{S5}^{\mathrm{Im}}$ | CP asymmetry of S-wave interference |
| `AS5re` | $A_{S5}^{\mathrm{Re}}$ | CP asymmetry of S-wave interference |

### Optimized Observables (P)

These are constructed to reduce theoretical uncertainties from hadronic form factors by forming ratios that cancel leading form-factor dependencies.

| Abbr | LaTeX | Definition |
|------|-------|-----------|
| `P1` | $P_1$ | $S_3 / (1 - F_L)$ |
| `P2` | $P_2$ | $\beta / [2(1 - F_L)]$ where $\beta$ relates to AFB |
| `P3` | $P_3$ | $\mathrm{Im}(G_\perp G_\parallel^*) / (1 - F_L)$ |
| `P4p` | $P_4^\prime$ | Optimized version of S4 (prime denoted by `p`) |
| `P5p` | $P_5^\prime$ | Optimized version of S5 |
| `P6p` | $P_6^\prime$ | Optimized version of S6 |
| `P6cp` | $P_{6c}^\prime$ | Optimized version of S6c |
| `P8p` | $P_8^\prime$ | Optimized version of S8 |

### Reduced Asymmetry Observables

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `A6p` | $A_6^\prime$ | Reduced forward-backward asymmetry: $A_6/(1 - F_L)$ for $B_s \to \phi\ell\ell$ |

### Time-Dependent CP Parameters

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `C` | $C$ | Direct CP violation parameter in time-dependent analysis |
| `S` | $S$ | Mixing-induced CP violation parameter |

### LFU Difference Observables (Q)

Differences of angular coefficients between muon and electron modes: $Q_X = X^{\mu} - X^{e}$. Used to test lepton flavor universality with reduced theoretical uncertainties.

| Abbr | LaTeX | Definition |
|------|-------|-----------|
| `QFL` | $Q_{F_L}$ | $F_L^{\mu} - F_L^{e}$ |
| `Q1` | $Q_1$ | $P_1^{\mu} - P_1^{e}$ |
| `Q2` | $Q_2$ | $P_2^{\mu} - P_2^{e}$ |
| `Q3` | $Q_3$ | $P_3^{\mu} - P_3^{e}$ |
| `Q4` | $Q_4$ | $P_4^{\prime\mu} - P_4^{\prime e}$ |
| `Q5` | $Q_5$ | $P_5^{\prime\mu} - P_5^{\prime e}$ |
| `Q6` | $Q_6$ | $P_6^{\prime\mu} - P_6^{\prime e}$ |
| `Q8` | $Q_8$ | $P_8^{\prime\mu} - P_8^{\prime e}$ |

### Ratios and Normalizations

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `R` | $R$ | Branching fraction ratio for LFU tests |
| `r` | $r$ | Normalized ratio (e.g., $r_{J/\psi}$ for charmonium normalization) |
| `rel_BF_pwave` | $\mathcal{B}_P$ | Branching fraction relative to $B^0 \to J/\psi(\to \mu^+\mu^-) K^{*0}$ (P-wave) |

### Differential Observables

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `dBF/dq2` | $d\mathcal{B}/dq^2$ | Differential branching fraction (relative to normalization mode) |

### Asymmetries and Fractions

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `S1` | $S_1$ | General asymmetry parameter |
| `AC` | $A_C$ | Charge asymmetry |
| `f` | $f$ | Fraction or proportion (e.g., fragmentation fraction) |

### CKM Parameters

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `gammaCKM` | $\gamma_{CKM}$ | CKM unitarity triangle angle $\gamma$ (also denoted $\phi_3$) |
| `r` | $r$ | Amplitude ratio (decay channel must be specified in transition) |
| `delta` | $\delta$ | Strong phase difference (decay channel must be specified) |

## 4. LaTeX Mapping

Use this mapping to construct the `latex` field from the observable abbreviation. The `$...$` delimiters are added when constructing the full `latex` field, wrapping the complete expression including the transition.

**JSON escaping**: Backslashes in LaTeX must be doubled in JSON. For example, `\to` becomes `\\to` in the JSON file. After `json.load()`, Python sees `\to`.

```python
# Abbreviation → LaTeX symbol (no $ delimiters)
# Use raw strings (r'...') in Python source for clarity.
OBSERVABLE_LATEX = {
    'Br': r'\mathcal{B}',        'dBr/dq2': r'd\mathcal{B}/dq^2',
    'Gamma': r'\Gamma',
    'rel_BF_pwave': r'\mathcal{B}_P',
    'dBF/dq2': r'd\mathcal{B}/dq^2',
    # Lifetimes
    'Tau': r'\tau',
    # Masses and mixing
    'Mass': 'M_f',              'mass': 'm',
    'DeltaMass': r'\Delta M',
    # Cross sections
    'Sigma': r'\sigma',
    'dSigma/dpT': r'd\sigma/dp_T', 'dSigma/deta': r'd\sigma/d\eta',
    # Angular coefficients (CP-averaged)
    'S1c': r'S_1^c',  'S2c': r'S_2^c',  'S2s': r'S_2^s',
    'S3': 'S_3',     'S4': 'S_4',     'S5': 'S_5',
    'S6c': r'S_{6c}', 'AFB': r'A_{FB}',
    'S7': 'S_7',     'S8': 'S_8',     'S9': 'S_9',
    'FL': 'F_L',     'FS': 'F_S',     'FH': 'F_H',
    'S1ac': r'S_{1a}^c',
    'S1bcre': r'S_{1bc}^{\mathrm{Re}}',
    'S1bcim': r'S_{1bc}^{\mathrm{Im}}',
    # S-wave interference
    'SS1re': r'S_{S1}^{\mathrm{Re}}', 'SS1im': r'S_{S1}^{\mathrm{Im}}',
    'SS2re': r'S_{S2}^{\mathrm{Re}}', 'SS2im': r'S_{S2}^{\mathrm{Im}}',
    'SS3re': r'S_{S3}^{\mathrm{Re}}', 'SS3im': r'S_{S3}^{\mathrm{Im}}',
    'SS4re': r'S_{S4}^{\mathrm{Re}}', 'SS4im': r'S_{S4}^{\mathrm{Im}}',
    'SS5re': r'S_{S5}^{\mathrm{Re}}', 'SS5im': r'S_{S5}^{\mathrm{Im}}',
    # CP asymmetries
    'ACP': r'A_{CP}', 'DeltaACP': r'\Delta A_{CP}',
    'AFB_CP': r'A_{CP}^{FB}', 'AFS': r'A_{CP}^{FS}',
    'A1c': r'A_{1c}', 'A2s': r'A_{2s}',
    'A3': 'A_3', 'A4': 'A_4', 'A5': 'A_5',
    'A6c': r'A_{6c}', 'A7': 'A_7', 'A8': 'A_8', 'A9': 'A_9',
    # CP-asymmetric S-wave
    'AS1re': r'A_{S1}^{\mathrm{Re}}', 'AS1im': r'A_{S1}^{\mathrm{Im}}',
    'AS2re': r'A_{S2}^{\mathrm{Re}}', 'AS2im': r'A_{S2}^{\mathrm{Im}}',
    'AS3re': r'A_{S3}^{\mathrm{Re}}', 'AS3im': r'A_{S3}^{\mathrm{Im}}',
    'AS4re': r'A_{S4}^{\mathrm{Re}}', 'AS4im': r'A_{S4}^{\mathrm{Im}}',
    'AS5re': r'A_{S5}^{\mathrm{Re}}', 'AS5im': r'A_{S5}^{\mathrm{Im}}',
    # Optimized observables
    'P1': 'P_1', 'P2': 'P_2', 'P3': 'P_3',
    'P4p': r"P_4^{\prime}", 'P5p': r"P_5^{\prime}",
    'P6p': r"P_6^{\prime}", 'P6cp': r"P_{6c}^{\prime}",
    'P8p': r"P_8^{\prime}",
    # Reduced asymmetry
    'A6p': r"A_6^{\prime}",
    # Time-dependent CP
    'C': 'C', 'S': 'S',
    # LFU differences (Q)
    'QFL': r'Q_{F_L}', 'Q1': 'Q_1', 'Q2': 'Q_2', 'Q3': 'Q_3',
    'Q4': 'Q_4', 'Q5': 'Q_5', 'Q6': 'Q_6', 'Q8': 'Q_8',
    # Ratios and normalizations
    'R': 'R', 'r': 'r',
    # Asymmetries and fractions
    'S1': 'S_1', 'AC': 'A_C', 'f': 'f',
    # CKM
    'gammaCKM': r'\gamma_{CKM}', 'delta': r'\delta',
}

# Usage: wrap the full expression with $...$
# latex = f"${OBSERVABLE_LATEX[abbr]}({transition_latex})$"
# Example: "$F_L(B^{0}\\to K^{*0}\\mu^{+}\\mu^{-})$"
```

## 5. Common q² Intervals (GeV²)

These are the most frequently used q² bin boundaries in B → K(*)ℓℓ analyses. **Always use the exact values reported in the paper** — this table is a quick reference only; paper-specific binning takes precedence.

| Region | Intervals |
|--------|-----------|
| Very low (electron mode) | [0.0008, 0.257], [0.002, 1.12] |
| Low q² | [0.06, 0.98], [0.1, 1.1], [1.1, 2.5], [1.1, 4.0], [1.1, 6.0], [2.0, 3.0], [2.0, 4.0], [3.0, 4.0], [4.0, 5.0], [4.0, 6.0], [5.0, 6.0], [6.0, 7.0], [6.0, 8.0] |
| Fine binning (comprehensive analyses) | [0.06, 0.54], [0.54, 0.98], [1.1, 1.8], [1.8, 2.5], [2.5, 3.25], [3.25, 4.0], [4.0, 5.0], [5.0, 6.0], [6.0, 7.0], [7.0, 8.0], [11.0, 11.75], [11.75, 12.5], [15.0, 16.0], [16.0, 17.0], [17.0, 18.0], [18.0, 19.0] |
| Charmonium veto | [8.0, 11.0], [11.0, 12.5] — usually excluded due to resonances |
| High q² | [14.0, 22.0], [14.3, ∞], [15.0, 17.0], [15.0, 19.0], [16.0, 17.0], [17.0, 19.0], [18.0, 19.0] |

## 6. B⁰ → K*⁰μ⁺μ⁻ Comprehensive Analysis Structure

For comprehensive angular analyses (e.g., LHCb:2025mqb), the data is typically organized across multiple `data[]` entries:

| Entry | Content | Observable Count | Notes |
|-------|---------|-----------------|-------|
| data[0] | CP-averaged S observables (coarse bins) | ~225 | 10 q² bins × ~22-27 obs/bin |
| data[1] | CP-averaged P observables (coarse bins) | ~225 | Same bins, different observable basis |
| data[2] | CP-averaged with S2s (coarse bins) | ~243 | Extended basis including S2s |
| data[3] | CP-asymmetric observables + S-wave | ~422 | 10 bins × ~41-53 obs/bin |
| data[4] | Alternative P parameterization | ~210 | Different observable set |
| data[5] | CP-averaged (fine bins) | ~362 | 16 q² bins × ~22-27 obs/bin |

Each entry has its own `tot_correlation` matrix. Fine binning (data[5]) splits the standard bins into sub-intervals for higher resolution.

## 7. Adding New Observables

When a paper introduces an observable not listed in this document:

1. **Confirm the physical meaning** and identify the standard notation used in the literature.
2. **Choose or create an abbreviation** following the conventions in Section 3. Add it to the appropriate category.
3. **Add the LaTeX mapping** to Section 4.
4. **Add new particles** to the particle table in Section 1 if the observable involves a particle not yet listed.
5. **Verify the naming** follows `OBS(transition)[condition]` format.
6. **Remember**: use symbolic notation only, not full expression definitions.
