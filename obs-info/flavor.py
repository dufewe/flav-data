# ---------------------------------------------------------
# Flavor observable guide for the flav-data Streamlit app.
#
# Mirrors flav-data-importer/references/obs-abbr.md, which is the
# authoritative reference. Keep the two in sync when conventions
# change.
# ---------------------------------------------------------

import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

with open(os.path.join(PROJECT_ROOT, 'defs.py'), 'r', encoding='utf-8') as f:
    exec(f.read())

# ---------------------------------------------------------
# Transition Symbols
# ---------------------------------------------------------
st.markdown(r'''
# Transition Symbols: `A.B.2.C.D`

Every decay or scattering process is encoded as a transition symbol
`A.B.2.C.D`, representing $A + B \to C + D$. The digit `2` replaces the
arrow $\to$ and separates the initial state from the final state.

Cascades repeat the separator: `p.p.2.W+.2.mu+.v` is
$pp \to W^+ \to \mu^+\nu$.

## Naming Rules

1. **State separator** — `A.B.2.C.D` means $A+B \to C+D$; each additional
   `2` starts the next step of a cascade.
2. **Particle-type order** — within a state, write particles as
   **baryon → meson → charged lepton → neutral lepton**.
   $\Lambda_b^0 \to p\,J/\psi\,\pi^-$ is `Lambdab0.2.p.J/psi.pi-`.
3. **Mass order within a type** — among particles of the same type, write
   **heaviest → lightest**. In `Lambdab0.2.p.J/psi.pi-`,
   $J/\psi$ (3.10 GeV) precedes $\pi^-$ (0.14 GeV); in
   $B^0 \to K^{*0}\tau^- e^+$ the leptons are ordered
   `B0.2.K*0.tau-.e+`. Mass ordering is applied inside each type: a
   lighter baryon still precedes a heavier meson.
4. **Charge order for equal masses** — when same-type particles have equal
   mass, write **`+` → `-` → `0`**: $B^0 \to e^+e^-$ is `B0.2.e+.e-`.
   Mass ordering takes precedence; charge only breaks equal-mass ties.
5. **Charge indicators** — a charge is written `+`, `-`, or `0` (`B+`,
   `B-`, `B0`, `D*+`). There is no other charge syntax: `p`/`m` suffixes
   (`Bp`, `pip`, `ep`) are rejected. A token omits the charge only when
   the source does not fix it, as in ratios and flavor comparisons (`B`,
   `D`, `K*`, `pi`, `tau`, `e`, `mu`, `l`).
6. **Antiparticles** — neutral antiparticles append `Bar` (`B0Bar`,
   `K*0Bar`). For baryons, `Bar` goes at the very end, after any charge
   indicator (`Lambdac+Bar`, `Lambdab0Bar`, `pBar`). For charged mesons,
   leptons, and bosons the charge sign already marks the antiparticle
   (`B+`/`B-`, `W+`/`W-`, `mu+`/`mu-`) — do **not** add `Bar`. The marker
   is always capital `Bar`; lowercase `bar` is invalid.
7. **Particle-name case follows the handwritten symbol** — Latin hadrons
   and capital Greek letters stay capital (`B0`, `K+`, `D*0`, `K*0`,
   `Lambdab0`, `Sigma-`, `Omega-`); lower-case Greek letters stay lower
   case (`pi0`, `pi+`, `rho+`, `phi`, `eta`, `omega`, `gamma`).
   Subscripts precede superscripts: $\pi^0$ is `pi0`, $\Lambda_b^0$ is
   `Lambdab0`, $D_s^{*+}$ is `Ds*+`, $K_S^0$ is `KS0`, $K_L^0$ is `KL0`.
8. **Neutrinos** — write the handwritten $\nu$ as `v`: use `v` or `vBar`
   without a flavor tag. If the signature is flavor-specific (for example
   a $\nu_\mu$ tagged through inverse muon decay), append the flavor:
   `ve`, `vmu`, `vtau`, with `Bar` for antiparticles (`veBar`, ...). The
   old spellings `nu`, `nuBar`, `nue`, `numu`, `nutau`, and lowercase
   `bar` are rejected.
9. **Intermediate resonances** — when an intermediate state decays to a
   dilepton pair, append `(2.l+.l-)` to the resonance name:
   `B0.2.J/psi.K*0(2.l+.l-)` for
   $B^0 \to K^{*0} J/\psi(\to \ell^+\ell^-)$.

Rules 1–5 are enforced by `flav-data-importer/scripts/json-valid.py`:
every key is `A.B.2.C.D` (`no-transition` is the only exception, and a
ratio joins two full keys with `/`), non-canonical order fails, and
`p`/`m` charge suffixes and lowercase `bar` are rejected. States with
particles outside the four listed types (W/Z/$\gamma$, quarks, generic
placeholders such as `l` or `q`) are not order-checked.

## Examples

| Process | Type | Symbol | Notes |
|---------|------|--------|-------|
| $B^0 \to e^+ e^-$ | Leptonic decay | `B0.2.e+.e-` | Charged leptons: `+` then `-` |
| $\bar{B}^0 \to e^+ e^-$ | Leptonic decay | `B0Bar.2.e+.e-` | Neutral antiparticle uses `Bar` |
| $B^+ \to K^+ \mu^+ \mu^-$ | Semileptonic | `B+.2.K+.mu+.mu-` | Meson first, then leptons |
| $W^- \to \mu^- \bar{\nu}_\mu$ | Leptonic decay | `W-.2.mu-.vBar` | Charged lepton before neutral lepton |
| $B_s^0 \to \phi \mu^+ \mu^-$ | Semileptonic | `Bs0.2.phi.mu+.mu-` | |
| $\Lambda_b^0 \to J/\psi\, p\, \pi^-$ | Non-leptonic | `Lambdab0.2.p.J/psi.pi-` | Baryon first; mesons heavy to light |
| $pp \to Z \to \mu^+ \mu^-$ | Scattering | `p.p.2.Z.2.mu+.mu-` | Two-step process |
| $e^+ e^- \to \mu^+ \mu^-$ | Scattering | `e+.e-.2.mu+.mu-` | Collider process |

## Rejected Forms

Compact keys without `.2.` (`B02K*mumu`), `p`/`m` charge suffixes (`Bp`,
`pip`, `ep`), and lowercase `bar` (`B0bar`) are all invalid.
''')

# ---------------------------------------------------------
# Particle Abbreviations
# ---------------------------------------------------------
st.markdown(r'''
# Particle Abbreviations

## Mesons

| Particle | Symbol | Notes |
|----------|--------|-------|
| $B^0$, $B^+$, $B^-$ | `B0`, `B+`, `B-` | Charged particles always use a charge indicator |
| $\bar{B}^0$ | `B0Bar` | Neutral antiparticles use `Bar` |
| $B_s^0$, $\bar{B}_s^0$ | `Bs0`, `Bs0Bar` | |
| $K^+$, $K^0$ | `K+`, `K0` | |
| $K_S^0$, $K_L^0$ | `KS0`, `KL0` | Subscript before superscript; never `K0S`/`K0s`/`K0L` |
| $K^{*0}$, $\bar{K}^{*0}$ | `K*0`, `K*0Bar` | $K^*$ resonance |
| $D^0$, $D^+$ | `D0`, `D+` | |
| $D^{*0}$, $D^{*+}$, $D^{*-}$ | `D*0`, `D*+`, `D*-` | Charged antiparticle is `D*-` |
| $D^{*\pm}$ (generic) | `D*` | Charge left unspecified |
| $\pi^0$, $\pi^+$, $\pi^-$ | `pi0`, `pi+`, `pi-` | |
| $\rho^0$, $\rho^+$, $\rho^-$ | `rho0`, `rho+`, `rho-` | |
| $\phi$ | `phi` | Neutral vector meson |
| $\omega$ | `omega` | Neutral vector meson (no charged $\omega^\pm$) |
| $J/\psi$ | `J/psi` | Charmonium |
| $\psi(2S)$ | `psi(2S)` | Charmonium excited state |
| $\eta$, $\eta'$ | `eta`, `etaprime` | |
| $D_s^+$, $D_s^{*+}$ | `Ds+`, `Ds*+` | Strange charmed meson |
| $B_c^+$ | `Bc+` | Bottom-charmed meson |
| $X_s$ | `Xs` | Inclusive strange hadronic system |

## Baryons

| Particle | Symbol | Notes |
|----------|--------|-------|
| $\Lambda$, $\Lambda_c^+$, $\Lambda_b^0$ | `Lambda`, `Lambdac+`, `Lambdab0` | Anti-baryons: `LambdaBar`, `Lambdac+Bar`, `Lambdab0Bar` |
| $\Sigma^+$, $\Sigma^0$, $\Sigma^-$ | `Sigma+`, `Sigma0`, `Sigma-` | Anti-baryons: `Sigma+Bar`, `Sigma0Bar`, `Sigma-Bar` |
| $\Xi_c^0$, $\Xi_b^0$ | `Xic0`, `Xib0` | Anti-baryons: `Xic0Bar`, `Xib0Bar` |
| $\Omega_c^0$ | `Omegac0` | Anti-baryon: `Omegac0Bar` |
| $p$, $n$ | `p`, `n` | Anti-baryons: `pBar`, `nBar` |

## Leptons and Bosons

| Particle | Symbol | Notes |
|----------|--------|-------|
| $e^+$, $e^-$ | `e+`, `e-` | |
| $\mu^+$, $\mu^-$ | `mu+`, `mu-` | |
| $\tau^+$, $\tau^-$ | `tau+`, `tau-` | |
| $\nu$ (any flavor), $\bar{\nu}$ | `v`, `vBar` | No flavor tag; flavor-specific signatures use `ve`, `vmu`, `vtau` (+`Bar`) |
| $W^+$, $W^-$, $Z$ | `W+`, `W-`, `Z` | |
| $\gamma$ | `gamma` | Photon |
| $t$, $\bar{t}$ | `t`, `tBar` | Top quark |
''')

# ---------------------------------------------------------
# Observable Naming
# ---------------------------------------------------------
st.markdown(r'''
# Observable Naming: `OBS` / `OBS[condition]`

Every measurement is named by its observable symbol only. The transition
is the enclosing `data` key, so `name` must not repeat it.

| Component | Meaning |
|-----------|---------|
| `OBS` | Symbolic abbreviation from the tables below; never a full expression |
| `[condition]` | Optional qualifier used **only** for multi-transition observables (ratios or differences) |
| `(parameter)` | Optional non-transition tag, e.g. `Vcb(CLN)`, `R1(CLN)`, `f+.Vcs`; a transition inside parentheses is invalid |

Examples: `FL`, `Br`, `dBr/dq2`, `Q6[mu-e]`, `RBr[mu/e]`, `Vcb(CLN)`.

Do **not** use `[condition]` to separate q² bins — use separate data
groups with `q2min`/`q2max`. Fit choices (nominal, higher-order, ...) are
separate data groups, not part of the name.

## Basic Observables (No Transition)

Intrinsic particle properties use `OBS(particle)` under the
`no-transition` key:

| Observable | LaTeX | Symbol |
|------------|-------|--------|
| On-shell mass | $M_f$ | `Mass(t)`, `Mass(Z)` |
| Running ($\overline{\text{MS}}$) mass | $m_f$ | `mass(t)` |
| Lifetime | $\tau_f$ | `Tau(e-)` |

Legacy mass shortcuts are accepted by the validator, but new imports
should use `Mass(f)`:

| Symbol | Replaces |
|--------|----------|
| `MZ` | `Mass(Z)` |
| `MW` | `Mass(W)` |
| `Mtop` | `Mass(t)` |
| `MH`, `Mh` | `Mass(H)`, `Mass(h)` |

Bare names without a transition:

| Symbol | Meaning |
|--------|---------|
| `gammaCKM` | CKM unitarity-triangle angle $\gamma$ ($\phi_3$) |
| `r` | Amplitude ratio (channel implied by the surrounding data) |
| `delta` | Strong phase difference |
| `R_b`, `R_c` | LEP electroweak pseudo-observables |
| `S_phigamma`, `C_phigamma`, `ADelta_phigamma` | Time-dependent CP parameters in $B_s \to \phi\gamma$ |
| `fs/fd` | $B_s/B^0$ fragmentation ratio |
| `ge/gmu`, `ge/gtau` | Lepton-flavor ratios at the $Z$ |

CKM magnitudes are named `|Vtd|`, `|Vts|`, `|Vub|`, `|Vcb|` (magnitude
only).

## Single-Transition Observables

The bare symbol is used without a condition; the `data` key carries the
process:

| Quantity | Symbol | Data key |
|----------|--------|----------|
| Branching fraction | `Br` | `B0.2.e+.e-` |
| Decay width | `Gamma` | `K*0.2.K+.pi-` |
| Differential branching fraction | `dBr/dq2` | `B0.2.Xs.gamma` |
| Cross section | `Sigma` | `p.p.2.e+.e-` |
| Charge asymmetry | `AC` | `B+.2.J/psi.K+` |
| Mass difference | `DeltaMass` | `Bs0.2.Bs0Bar` |
| Decay fraction | `f` | `Z.2.mu+.mu-` |

## Multi-Transition Observables

For observables comparing several transitions, the `data` key holds the
shared part of the process and shared particles use generic names:
`l1`/`l2` (leptons), `q1`/`q2` (quarks), `v1`/`v2` (neutrinos),
`h1`/`h2` (hadrons).

`[condition]` encodes the flavor mapping (`[mu/e]`: `l1` = $\mu$,
`l2` = $e$):

- `/` means a ratio: `RBr[mu/e]` =
  $\mathcal{B}(B^0\to K^{*0}\mu^+\mu^-)/\mathcal{B}(B^0\to K^{*0}e^+e^-)$.
- `-` means a difference: `DeltaACP[mu-e]` =
  $A_{CP}(B^-\to\mu^-\bar{\nu}) - A_{CP}(B^-\to e^-\bar{\nu})$.

| Observable | Symbol | Data key |
|------------|--------|----------|
| $R_{K^*}$ | `RBr[mu/e]` | `B0.2.K*0.l+.l-` |
| $R_K$ | `RBr[mu/e]` | `B+.2.K+.l+.l-` |
| $\Delta A_{CP}(\mu-e)$ | `DeltaACP[mu-e]` | `B-.2.l-.vBar` |
| $r$ in $B \to DK$ | `r` | `B-.2.D0.K-` |
| $\delta$ in $B \to DK$ | `delta` | `B-.2.D0.K-` |

For the CKM amplitude ratio and strong phase, the transition must carry
negative charges: `B-.2.D0.K-`, `B-.2.D0.pi-` (mesons heaviest first, so
`D0` precedes `K-`/`pi-`).

## Differences and Ratios

| Type | Symbol | LaTeX | Example |
|------|--------|-------|---------|
| Difference | `DeltaOBS[condition]` | $\Delta_{OBS}^{condition}$ | `DeltaBr[mu-e]` |
| Ratio | `ROBS[condition]` | $R_{OBS}^{condition}$ | `RFL[mu/e]` |
| Canonical LFU ratio | `R` | $R(X)$ | `R` |

The canonical LFU ratio
$R(X)=\mathcal{B}(B\to X\tau\nu)/\mathcal{B}(B\to X\ell\nu)$ is the bare
`R` whenever the channel key fixes $X$: `R` under
`B0Bar.2.D+.tau-.vBar` is $R(D)$, so do not write `RD` or `RD*`.

## Form-Factor Expansion Coefficients: `aN_FF`

Coefficients of a form-factor expansion (z-expansion, BCL, ...) are
`aN_FF`, where `N` is the expansion order and `FF` a symbol from the
table below. Examples: `a0_Fp`, `a1_F0`, `a2_Fv`, `a0_Gv`.

When a source quotes one number for several form factors, write one
observable per symbol and repeat value/errors (`a0_Gv` and `a0_Gp`),
never `a0_Gv_Gp`.

Every group of `aN_FF` coefficients also declares a group-level `scheme`
short code (after `dataset`, before any matrix). The JSON stores only the
code:

| Scheme | Parametrization | Source |
|--------|-----------------|--------|
| `BGL` | Boyd-Grinstein-Lebed | arXiv:hep-ph/9504235 |
| `BCL` | Bourrely-Caprini-Lellouch | arXiv:0807.2722 |
| `BSZ` | Bharucha-Straub-Zwicky | arXiv:1503.05534 |
| `DLM` | Detmold-Lehner-Meinel | arXiv:1503.01421 |

| Symbol | Form factor | Symbol | Form factor |
|--------|-------------|--------|-------------|
| `fp` | $f_+$ | `f0` | $f_0$ |
| `fT` | $f_T$ | `V` | $V$ |
| `A0` | $A_0$ | `A1` | $A_1$ |
| `A12` | $A_{12}$ | `T1` | $T_1$ |
| `T2` | $T_2$ | `T23` | $T_{23}$ |
| `Fp` | helicity $f_+$ | `F0` | helicity $f_0$ |
| `Fv` | helicity $f_\perp$ | `Gp` | helicity $g_+$ |
| `G0` | helicity $g_0$ | `Gv` | helicity $g_\perp$ |
| `hp` | helicity $h_+$ | `hv` | helicity $h_\perp$ |
| `htp` | helicity $\tilde{h}_+$ | `htv` | helicity $\tilde{h}_\perp$ |
| `g` | BGL $g$ ($\bar{B}\to D^*$) | `f` | BGL $f$ ($\bar{B}\to D^*$) |
| `F1` | BGL $F_1$ ($\bar{B}\to D^*$) | `F2` | BGL $F_2$ ($\bar{B}\to D^*$) |

Baryon semileptonic decays use the helicity set with
$f_+ \to$ `Fp`, $f_0 \to$ `F0`, $f_\perp \to$ `Fv`, $g_+ \to$ `Gp`,
$g_0 \to$ `G0`, $g_\perp \to$ `Gv`, $h_+ \to$ `hp`, $h_\perp \to$ `hv`.
''')

# ---------------------------------------------------------
# Observable Abbreviations
# ---------------------------------------------------------
st.markdown(r'''
# Observable Abbreviations

## Branching Fractions and Widths

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `Br` | $\mathcal{B}$ | Branching fraction |
| `dBr/dq2` | $d\mathcal{B}/dq^2$ | Differential branching fraction |
| `Gamma` | $\Gamma$ | Decay width (partial or total) |

## Lifetimes

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `Tau` | $\tau$ | Particle lifetime |

## Masses and Mixing

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `Mass` | $M_f$ | On-shell mass; `Mass(f)`, shortcuts `MZ`, `MW`, `Mtop`, `MH`, `Mh` |
| `mass` | $m$ | $\overline{\text{MS}}$ mass |
| `DeltaMass` | $\Delta M$ | Mass difference / neutral-meson mixing |
| `DeltaGamma` | $\Delta\Gamma$ | Width difference / neutral-meson mixing |

## Cross Sections

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `Sigma` | $\sigma$ | Total or fiducial cross section |
| `dSigma/dpT` | $d\sigma/dp_T$ | Differential cross section in $p_T$ |
| `dSigma/deta` | $d\sigma/d\eta$ | Differential cross section in pseudorapidity |

## Angular Coefficients (CP-averaged)

For $B^0 \to K^{*0}(\to K^+\pi^-)\mu^+\mu^-$, the standard basis has 12
angular observables per q² bin, plus S-wave and CP-asymmetric extensions.

| Abbr | LaTeX | Description | Range |
|------|-------|-------------|-------|
| `S1c` | $S_1^c$ | Longitudinal amplitude coefficient | [0, 1] |
| `S2c` | $S_2^c$ | Transverse amplitude coefficient | [-1, 0] |
| `S2s` | $S_2^s$ | Transverse amplitude coefficient (sine) | [-1, 0] |
| `S3` | $S_3$ | T-odd angular coefficient | [-0.5, 0.5] |
| `S4`, `S5` | $S_4$, $S_5$ | Angular coefficients | [-1, 1] |
| `S6c` | $S_{6c}$ | Angular coefficient (c-component) | [-1, 1] |
| `AFB` | $A_{FB}$ | Forward-backward asymmetry of the dilepton system | [-1, 1] |
| `S7`, `S8` | $S_7$, $S_8$ | T-odd angular coefficients | [-1, 1] |
| `S9` | $S_9$ | T-odd angular coefficient | [-0.5, 0.5] |
| `FL` | $F_L$ | Longitudinal polarization fraction | [0, 1] |
| `FS` | $F_S$ | S-wave fraction | [0, 1] |
| `FH` | $F_H$ | Flat term ($B \to K\ell\ell$) | [-1, 1] |
| `S1ac` | $S_{1a}^c$ | Additional longitudinal coefficient | — |
| `S1bcre`, `S1bcim` | $S_{1bc}^{\mathrm{Re}}$, $S_{1bc}^{\mathrm{Im}}$ | Interference coefficient | — |

## S-wave Observables

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `SS1re`, `SS1im` | $S_{S1}^{\mathrm{Re}}$, $S_{S1}^{\mathrm{Im}}$ | S-wave interference |
| `SS2re`, `SS2im` | $S_{S2}^{\mathrm{Re}}$, $S_{S2}^{\mathrm{Im}}$ | S-wave interference |
| `SS3re`, `SS3im` | $S_{S3}^{\mathrm{Re}}$, $S_{S3}^{\mathrm{Im}}$ | S-wave interference |
| `SS4re`, `SS4im` | $S_{S4}^{\mathrm{Re}}$, $S_{S4}^{\mathrm{Im}}$ | S-wave interference |
| `SS5re`, `SS5im` | $S_{S5}^{\mathrm{Re}}$, $S_{S5}^{\mathrm{Im}}$ | S-wave interference |

## CP Asymmetries

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `ACP` | $A_{CP}$ | Direct CP asymmetry |
| `DeltaACP` | $\Delta A_{CP}$ | CP-asymmetry difference between two modes |
| `AFB_CP` | $A_{CP}^{FB}$ | CP asymmetry of the forward-backward asymmetry |
| `AFS` | $A_{CP}^{FS}$ | CP asymmetry of the S-wave fraction |
| `A1c` | $A_{1c}$ | CP asymmetry of $S_1^c$ |
| `A2s` | $A_{2s}$ | CP asymmetry of $S_2^s$ |
| `A3`–`A5` | $A_3$–$A_5$ | CP asymmetries of $S_3$–$S_5$ |
| `A6c` | $A_{6c}$ | CP asymmetry of $S_{6c}$ |
| `A7`–`A9` | $A_7$–$A_9$ | CP asymmetries of $S_7$–$S_9$ |
| `AS1re`–`AS5im` | $A_{S1}^{\mathrm{Re}}$–$A_{S5}^{\mathrm{Im}}$ | CP asymmetries of S-wave interference |

## Optimized Observables (P)

| Abbr | LaTeX | Definition |
|------|-------|------------|
| `P1` | $P_1$ | $S_3 / (1 - F_L)$ |
| `P2` | $P_2$ | $\beta / [2(1 - F_L)]$ |
| `P3` | $P_3$ | $\mathrm{Im}(G_\perp G_\parallel^*) / (1 - F_L)$ |
| `P4p` | $P_4^\prime$ | Optimized $S_4$ |
| `P5p` | $P_5^\prime$ | Optimized $S_5$ |
| `P6p` | $P_6^\prime$ | Optimized $S_6$ |
| `P6cp` | $P_{6c}^\prime$ | Optimized $S_{6c}$ |
| `P8p` | $P_8^\prime$ | Optimized $S_8$ |

## Reduced Asymmetry

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `A6p` | $A_6^\prime$ | $A_6/(1 - F_L)$, used for $B_s \to \phi\ell\ell$ |

## Time-Dependent CP Parameters

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `C` | $C$ | Direct CP violation in a time-dependent analysis |
| `S` | $S$ | Mixing-induced CP violation |

## LFU Differences

Differences between muon and electron angular coefficients, named with
the `Delta` prefix: $\Delta X = X^{\mu} - X^{e}$ (papers often label them
$Q_X$).

| Abbr | LaTeX | Definition |
|------|-------|------------|
| `DeltaFL` | $\Delta_{F_L}^{\mu-e}$ | $F_L^{\mu} - F_L^{e}$ |
| `DeltaP1` | $\Delta_{P_1}^{\mu-e}$ | $P_1^{\mu} - P_1^{e}$ |
| `DeltaP2` | $\Delta_{P_2}^{\mu-e}$ | $P_2^{\mu} - P_2^{e}$ |
| `DeltaP3` | $\Delta_{P_3}^{\mu-e}$ | $P_3^{\mu} - P_3^{e}$ |
| `DeltaP4p` | $\Delta_{P_4^\prime}^{\mu-e}$ | $P_4^{\prime\mu} - P_4^{\prime e}$ |
| `DeltaP5p` | $\Delta_{P_5^\prime}^{\mu-e}$ | $P_5^{\prime\mu} - P_5^{\prime e}$ |
| `DeltaP6p` | $\Delta_{P_6^\prime}^{\mu-e}$ | $P_6^{\prime\mu} - P_6^{\prime e}$ |
| `DeltaP8p` | $\Delta_{P_8^\prime}^{\mu-e}$ | $P_8^{\prime\mu} - P_8^{\prime e}$ |

## Ratios and Fractions

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `R` | $R$ | Canonical LFU ratio; bare when the channel key carries the final state |
| `r` | $r$ | Charmonium normalization ratio (CKM amplitude ratio uses `r` under `B-.2.D0.K-`) |
| `f` | $f$ | Generic fraction: decay, fragmentation, or dimensionless ratio |
| `AC` | $A_C$ | Charge asymmetry |
| `S1` | $S_1$ | Generic scalar asymmetry (not the `S1c` angular coefficient) |

## Electroweak and Other Pseudo-Observables

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `R_b` | $R_b$ | $Z \to b\bar{b}$ partial-width ratio |
| `R_c` | $R_c$ | $Z \to c\bar{c}$ partial-width ratio |
| `S_phigamma` | $S_{\phi\gamma}$ | CP-violating parameter in $B_s \to \phi\gamma$ |
| `C_phigamma` | $C_{\phi\gamma}$ | Direct CP asymmetry in $B_s \to \phi\gamma$ |
| `ADelta_phigamma` | $\mathcal{A}^{\Delta}_{\phi\gamma}$ | Time-dependent CP asymmetry in $B_s \to \phi\gamma$ |

## Legacy Ratios Without Transition

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `fs/fd` | $f_s/f_d$ | $B_s$ to $B^0$ fragmentation ratio |
| `ge/gmu` | $g_e/g_\mu$ | Lepton coupling ratio at the $Z$ |
| `ge/gtau` | $g_e/g_\tau$ | Lepton coupling ratio at the $Z$ |

## CKM Parameters

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `gammaCKM` | $\gamma_{CKM}$ | Unitarity-triangle angle ($\phi_3$) |
| `r` | $r$ | Amplitude ratio (channel specified by the transition) |
| `delta` | $\delta$ | Strong phase difference |

CKM matrix-element magnitudes are named `|Vtd|`, `|Vts|`, `|Vub|`,
`|Vcb|` (magnitudes only).

## Adding a New Observable

If a paper measures a quantity not listed here:

1. Confirm its physical meaning and the notation used in the literature.
2. Add the abbreviation, with its LaTeX symbol, to the appropriate table
   in `flav-data-importer/references/obs-abbr.md` §3.
3. Add any new particle to the particle tables in §1.
4. Keep `name` to the bare symbol plus an optional `[condition]`; the
   transition stays in the `data` key.

The importer reference is authoritative — do not introduce a name here
that the importer does not define.
''')

# ---------------------------------------------------------
# Common q² Intervals
# ---------------------------------------------------------
st.markdown(r'''
# Common q² Intervals (GeV²)

Frequently used bin boundaries in $B \to K^{(*)}\ell\ell$ analyses.
**Always use the exact values reported in the paper** — this is only a
quick reference.

| Region | Intervals |
|--------|-----------|
| Very low (electron mode) | [0.0008, 0.257], [0.002, 1.12] |
| Low q² | [0.06, 0.98], [0.1, 1.1], [1.1, 2.5], [1.1, 4.0], [1.1, 6.0], [2.0, 3.0], [2.0, 4.0], [3.0, 4.0], [4.0, 5.0], [4.0, 6.0], [5.0, 6.0], [6.0, 7.0], [6.0, 8.0] |
| Fine binning | [0.06, 0.54], [0.54, 0.98], [1.1, 1.8], [1.8, 2.5], [2.5, 3.25], [3.25, 4.0], [4.0, 5.0], [5.0, 6.0], [6.0, 7.0], [7.0, 8.0], [11.0, 11.75], [11.75, 12.5], [15.0, 16.0], [16.0, 17.0], [17.0, 18.0], [18.0, 19.0] |
| Charmonium veto | [8.0, 11.0], [11.0, 12.5] — usually excluded because of resonances |
| High q² | [14.0, 22.0], [14.3, ∞], [15.0, 17.0], [15.0, 19.0], [16.0, 17.0], [17.0, 19.0], [18.0, 19.0] |

Non-contiguous regions are written as comma-separated paired strings:
`"q2min": "11.0,17.5"` with `"q2max": "15.0,+inf"`. Use `"+inf"` for an
open upper bound; symbolic endpoints are invalid.
''')
