# ---------------------------------------------------------
# Flavor observable guide for the flav-data Streamlit app.
#
# Mirrors flav-data-importer/references/observable-naming.md, which is the
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
# Channel Keys: `.2.` Transitions

Every decay or scattering process is a channel key: particle pids joined by
`.`, with `.2.` marking the arrow. A pid is
`<core>_<ig>_<jpc>_<serial>`, e.g. `dB_I1?_0-n_0` for $B^0$ or
`Ud_I2-_0-n_0` for $\pi^-$; the full grammar and registry are in the
importer reference `particle-naming.md`.

## Ordering rules

1. **Separator `.2.`** — `A.B.2.C.D` means $A+B\to C+D$; a cascade repeats
   it: `uud_I1?_1+n_0.uud_I1?_1+n_0.2.WB_I??_1??_0.2.mu_I??_1+n_0.VMU_I??_1+n_0`
   is $pp\to W^-\to\mu^-\bar\nu_\mu$.
2. **Particle type** — within a state:
   **baryon → meson → charged lepton → neutral lepton**. A lighter baryon
   still precedes a heavier meson.
3. **Mass within a type** — same-type pids go **heaviest → lightest**,
   using the registry masses.
4. **Charge for equal masses** — same-type pids of equal mass go
   **`+` → `-` → `0`**: `E_I??_1+n_0.e_I??_1+n_0` is $e^+e^-$.
5. **Ratios** — join two full transitions with `/`, each side ordered
   independently.
6. **`no-transition`** — the only key without `.2.`, for intrinsic
   quantities.

The rules are enforced by `flav-data-importer/scripts/json-valid.py`
against the registry. Ordering is skipped for placeholders
(`l`, `v`, `q`, `Xs`, ...), exotics without a registered mass, and nuclei.
The key never encodes a mass label, a fit scenario, or a measurement
suffix — those belong in the group `note`.

## Examples

| Process | Key |
|---------|-----|
| $B^0\to e^+e^-$ | `dB_I1?_0-n_0.2.E_I??_1+n_0.e_I??_1+n_0` |
| $\bar B^0\to e^+e^-$ | `Db_I1?_0-n_0.2.E_I??_1+n_0.e_I??_1+n_0` |
| $B^+\to K^+\mu^+\mu^-$ | `uB_I1?_0-n_0.2.uS_I1?_0-n_0.MU_I??_1+n_0.mu_I??_1+n_0` |
| $W^-\to\mu^-\bar\nu_\mu$ | `WB_I??_1??_0.2.mu_I??_1+n_0.VMU_I??_1+n_0` |
| $B_s^0\to\phi\mu^+\mu^-$ | `sB_I0?_0-n_0.2.qQ_I0-_1--_1.MU_I??_1+n_0.mu_I??_1+n_0` |
| $\Lambda_b^0\to J/\psi\,p\,\pi^-$ | `udb_I0?_1+n_0.2.uud_I1?_1+n_0.cC_I0-_1--_0.Ud_I2-_0-n_0` |
| $pp\to Z\to\mu^+\mu^-$ | `uud_I1?_1+n_0.uud_I1?_1+n_0.2.Z_I??_1??_0.2.MU_I??_1+n_0.mu_I??_1+n_0` |
| $e^+e^-\to\mu^+\mu^-$ | `E_I??_1+n_0.e_I??_1+n_0.2.MU_I??_1+n_0.mu_I??_1+n_0` |
''')

# ---------------------------------------------------------
# Common pids
# ---------------------------------------------------------
st.markdown(r'''
# Common pids

`<core>` is the valence content in increasing quark mass (lowercase quark,
uppercase antiquark); `<ig>` is $I^G$ as `I<2I><G>`; `<jpc>` is
`<2J><P><C>` (`n` = not defined); `<serial>` separates poles. The
antiparticle swaps letter case in place. Full grammar, registry, masses,
and widths: `particle-naming.md`.

| Particle | pid |
|----------|-----|
| $\pi^+$, $\pi^-$, $\pi^0$ | `uD_I2-_0-n_0`, `Ud_I2-_0-n_0`, `qQ_I2-_0-+_0` |
| $K^+$, $K^-$, $K^0$, $\bar K^0$ | `uS_I1?_0-n_0`, `Us_I1?_0-n_0`, `dS_I1?_0-n_0`, `Ds_I1?_0-n_0` |
| $K_S^0$, $K_L^0$, $K^{*0}$ | `qQ_I1?_0-n_0`, `qQ_I1?_0-n_1`, `dS_I1?_1-n_0` |
| $\rho^+$, $\rho^-$, $\rho^0$ | `uD_I2+_1--_0`, `Ud_I2+_1--_0`, `qQ_I2+_1--_0` |
| $\eta$, $\eta'$, $\omega$, $\phi$ | `qQ_I0+_0-+_0`, `qQ_I0+_0-+_1`, `qQ_I0-_1--_0`, `qQ_I0-_1--_1` |
| $J/\psi$, $\psi(2S)$ | `cC_I0-_1--_0`, `cC_I0-_1--_1` |
| $D^0$, $\bar D^0$, $D^+$, $D^-$ | `Uc_I1?_0-n_0`, `uC_I1?_0-n_0`, `Dc_I1?_0-n_0`, `dC_I1?_0-n_0` |
| $D^{*0}$, $D^{*+}$, $D_s^+$, $D_s^{*+}$ | `Uc_I1?_1-n_0`, `Dc_I1?_1-n_0`, `Sc_I0?_0-n_0`, `Sc_I0?_1-n_0` |
| $B^+$, $B^-$, $B^0$, $\bar B^0$ | `uB_I1?_0-n_0`, `Ub_I1?_0-n_0`, `dB_I1?_0-n_0`, `Db_I1?_0-n_0` |
| $B_s^0$, $\bar B_s^0$, $B_c^+$, $B_c^-$ | `sB_I0?_0-n_0`, `Sb_I0?_0-n_0`, `cB_I0?_0-n_0`, `Cb_I0?_0-n_0` |
| $p$, $n$, $\Lambda$, $\Lambda_c^+$, $\Lambda_b^0$ | `uud_I1?_1+n_0`, `udd_I1?_1+n_0`, `uds_I0?_1+n_0`, `udc_I0?_1+n_0`, `udb_I0?_1+n_0` |
| $e^-$, $\mu^-$, $\tau^-$ | `e_I??_1+n_0`, `mu_I??_1+n_0`, `tau_I??_1+n_0` |
| $\nu_e$, $\bar\nu_e$ | `ve_I??_1+n_0`, `VE_I??_1+n_0` |
| $W^+$, $W^-$, $Z$, $\gamma$, g, $H$ | `W_I??_1??_0`, `WB_I??_1??_0`, `Z_I??_1??_0`, `ph_I??_1--_0`, `g_I??_1--_0`, `H_I??_0++_0` |

Placeholders (not pids, never order-checked): `l`/`l+`/`l-`, `v`/`vBar`,
`q`/`qBar`, `f`/`fBar`, `kappa`, `Xs`/`XsBar`, `Xce`/`Xcl`, `had`,
`all`, `V`, `VH`, `gg`, `gamma+gamma`, `no-transition`.
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

Examples: `FL`, `Br`, `dBr/dq2`, `DeltaP6p[mu-e]`, `RBr[mu/e]`, `Vcb(CLN)`.

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

The argument is the PDG particle label, not a pid. Single-token
shortcuts (`MZ`, `MW`, `Mtop`, `MH`, `Mh`) are rejected by the
validator.

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
| Branching fraction | `Br` | `dB_I1?_0-n_0.2.E_I??_1+n_0.e_I??_1+n_0` |
| Decay width | `Gamma` | `dS_I1?_1-n_0.2.uS_I1?_0-n_0.Ud_I2-_0-n_0` |
| Differential branching fraction | `dBr/dq2` | `dB_I1?_0-n_0.2.XsBar.ph_I??_1--_0` |
| Cross section | `Sigma` | `uud_I1?_1+n_0.uud_I1?_1+n_0.2.E_I??_1+n_0.e_I??_1+n_0` |
| Charge asymmetry | `AC` | `uB_I1?_0-n_0.2.cC_I0-_1--_0.uS_I1?_0-n_0` |
| Mass difference | `DeltaMass` | `sB_I0?_0-n_0.2.Sb_I0?_0-n_0` |
| Decay fraction | `f` | `Z_I??_1??_0.2.MU_I??_1+n_0.mu_I??_1+n_0` |

## Multi-Transition Observables

For observables comparing several transitions, the `data` key holds the
shared part of the process. Shared charged leptons are written `l+`/`l-`
(or `l`) and shared quarks `q1`/`q2` (or `q`); these are listed as
non-orderable in the registry tables of `particle-naming.md` and skip
the order check.
Neutrinos are written `ve`, `vmu`, `vtau` (and `Bar` forms) and are
order-checked as neutral leptons; the generic `v`/`vBar` is a
non-orderable placeholder.
Numbered lepton, neutrino, or hadron placeholders (`l1`, `v1`, `h1`) are
rejected.

`[condition]` encodes the flavor mapping (`[mu/e]` = the muon mode over
the electron mode):

- `/` means a ratio: `RBr[mu/e]` =
  $\mathcal{B}(B^0\to K^{*0}\mu^+\mu^-)/\mathcal{B}(B^0\to K^{*0}e^+e^-)$.
- `-` means a difference: `DeltaACP[mu-e]` =
  $A_{CP}(B^-\to\mu^-\bar{\nu}) - A_{CP}(B^-\to e^-\bar{\nu})$.

| Observable | Symbol | Data key |
|------------|--------|----------|
| $R_{K^*}$ | `RBr[mu/e]` | `dB_I1?_0-n_0.2.dS_I1?_1-n_0.l+.l-` |
| $R_K$ | `RBr[mu/e]` | `uB_I1?_0-n_0.2.uS_I1?_0-n_0.l+.l-` |
| $\Delta A_{CP}(\mu-e)$ | `DeltaACP[mu-e]` | `Ub_I1?_0-n_0.2.l-.vBar` |
| $r$ in $B \to DK$ | `r` | `Ub_I1?_0-n_0.2.Uc_I1?_0-n_0.Us_I1?_0-n_0` |
| $\delta$ in $B \to DK$ | `delta` | `Ub_I1?_0-n_0.2.Uc_I1?_0-n_0.Us_I1?_0-n_0` |

For the CKM amplitude ratio and strong phase, the transition must carry
negative charges: `Ub_I1?_0-n_0.2.Uc_I1?_0-n_0.Us_I1?_0-n_0` and
`Ub_I1?_0-n_0.2.Uc_I1?_0-n_0.Ud_I2-_0-n_0` (mesons heaviest first, so
`Uc` precedes `Us`/`Ud`).

## Differences and Ratios

| Type | Symbol | LaTeX | Example |
|------|--------|-------|---------|
| Difference | `DeltaOBS[condition]` | $\Delta_{OBS}^{condition}$ | `DeltaBr[mu-e]` |
| Ratio | `ROBS[condition]` | $R_{OBS}^{condition}$ | `RFL[mu/e]` |
| Canonical LFU ratio | `R` | $R(X)$ | `R` |

The canonical LFU ratio
$R(X)=\mathcal{B}(B\to X\tau\nu)/\mathcal{B}(B\to X\ell\nu)$ is the bare
`R` whenever the channel key fixes $X$: `R` under
`Db_I1?_0-n_0.2.Dc_I1?_0-n_0.tau_I??_1+n_0.vBar` is $R(D)$, so do not write
`RD` or `RD*`.

## Common Paper Notation → flav-data Name

Papers use a variety of symbols for the same quantity. The JSON `name`
always uses the canonical flav-data abbreviation; this table maps the
most common paper notations to it.

| Paper notation | flav-data `name` | Notes |
|----------------|------------------|-------|
| $\mathcal{B}$, BR, BF | `Br` | Branching fraction |
| $d\mathcal{B}/dq^2$ | `dBr/dq2` | Differential branching fraction |
| $F_L$ | `FL` | Longitudinal polarization fraction |
| $A_{FB}$ | `AFB` | Forward-backward asymmetry |
| $A_{CP}$ | `ACP` | Direct CP asymmetry |
| $P_1$, $P_2$, $P_3$ | `P1`, `P2`, `P3` | Optimized angular observables |
| $P_4'$, $P_5'$, $P_6'$, $P_8'$ | `P4p`, `P5p`, `P6p`, `P8p` | Prime $\prime$ → `p` |
| $Q_i$ ($=P_i^\mu-P_i^e$) | `DeltaP1` … `DeltaP8p` | LFU difference; see **LFU Differences** |
| $Q_{F_L}$ | `DeltaFL` | LFU difference of $F_L$ |
| $R_K$, $R_{K^*}$ | `R` | Bare; channel key carries $K^{(*)}$ and both lepton modes |
| $R(D)$, $R(D^*)$ | `R` | Bare; channel key carries $D^{(*)}$ |
| $\Delta m_s$, $\Delta m_d$ | `DeltaMass` | Neutral-meson mass difference |

The $Q$ spelling is never stored: the validator rejects it in favor of
the `Delta` form.

## Form-Factor Expansion Coefficients: `aN_FF`

Coefficients of a form-factor expansion (z-expansion, BCL, ...) are
`aN_FF`, where `N` is the expansion order and `FF` a symbol from the
table below. Examples: `a0_F+`, `a1_F0`, `a2_Fv`, `a0_Gv`.

When a source quotes one number for several form factors, write one
observable per symbol and repeat value/errors (`a0_Gv` and `a0_G+`),
never `a0_Gv_G+`.

Every group of `aN_FF` coefficients also declares a group-level `scheme`
short code (after `dataset`, before any matrix). The JSON stores only the
code:

| Scheme | Parametrization | Source |
|--------|-----------------|--------|
| `BK` | Becirevic-Kaidalov | arXiv:hep-ph/9904490 |
| `BGL` | Boyd-Grinstein-Lebed | arXiv:hep-ph/9504235 |
| `BCL` | Bourrely-Caprini-Lellouch | arXiv:0807.2722 |
| `BSZ` | Bharucha-Straub-Zwicky | arXiv:1503.05534 |
| `DLM` | Detmold-Lehner-Meinel | arXiv:1503.01421 |
| `MR` | Meinel-Rendon $w$-expansion (with or without a pole factor) | arXiv:2009.09313, arXiv:2107.13140 |

| Symbol | Form factor | Symbol | Form factor |
|--------|-------------|--------|-------------|
| `f+` | $f_+$ | `f0` | $f_0$ |
| `fT` | $f_T$ | `V` | $V$ |
| `A0` | $A_0$ | `A1` | $A_1$ |
| `A12` | $A_{12}$ | `T1` | $T_1$ |
| `T2` | $T_2$ | `T23` | $T_{23}$ |
| `F+` | helicity $f_+$ | `F0` | helicity $f_0$ |
| `Fv` | helicity $f_\perp$ | `G+` | helicity $g_+$ |
| `G0` | helicity $g_0$ | `Gv` | helicity $g_\perp$ |
| `h+` | helicity $h_+$ | `hv` | helicity $h_\perp$ |
| `ht+` | helicity $\tilde{h}_+$ | `htv` | helicity $\tilde{h}_\perp$ |
| `Fv'` | helicity $f_{\perp'}$ | `Gv'` | helicity $g_{\perp'}$ |
| `hv'` | helicity $h_{\perp'}$ | `htv'` | helicity $\tilde{h}_{\perp'}$ |
| `g` | BGL $g$ ($\bar{B}\to D^*$) | `f` | BGL $f$ ($\bar{B}\to D^*$) |
| `F1` | BGL $F_1$ ($\bar{B}\to D^*$) | `F2` | BGL $F_2$ ($\bar{B}\to D^*$) |

Baryon semileptonic decays use the helicity set with
$f_+ \to$ `F+`, $f_0 \to$ `F0`, $f_\perp \to$ `Fv`, $g_+ \to$ `G+`,
$g_0 \to$ `G0`, $g_\perp \to$ `Gv`, $h_+ \to$ `h+`, $h_\perp \to$ `hv`.
$J^P=3/2^-$ final states add the primed set
$f_{\perp'} \to$ `Fv'`, $g_{\perp'} \to$ `Gv'`,
$h_{\perp'} \to$ `hv'`, $\tilde{h}_{\perp'} \to$ `htv'`.
The obsolete spellings `fp`, `Fp`, `Gp`, `hp`, and `htp` are rejected;
`Fv`, `Gv`, `hv`, and `htv` keep their existing spelling.

## Zero-Recoil Sum-Rule Integrals: `I0A`, `I0V`

A zero-recoil OPE sum rule bounds a form-factor combination from above
through the dimensionless integrals $I_{0,A}$ and $I_{0,V}$, written
`I0A` and `I0V`. The transition key selects the channel, and the group
`note` records the scale $\epsilon_M=\mu$ and which combination each
integral bounds; no `scheme` is needed.
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
| `Mass` | $M_f$ | On-shell mass; written `Mass(f)` with the PDG particle label |
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

Differences between muon and electron angular coefficients:
$\Delta X = X^{\mu} - X^{e}$. The JSON `name` always uses the unified
`Delta` form with the `[mu-e]` condition; papers label these $Q_X$
($Q_i \equiv \Delta P_i$, $Q_{F_L} \equiv \Delta F_L$), mapped in the
Paper Notation column. The $Q$ spelling is rejected by the validator.

| Abbr | LaTeX | Paper Notation | Definition |
|------|-------|----------------|------------|
| `DeltaFL` | $\Delta_{F_L}^{\mu-e}$ | $Q_{F_L}$ | $F_L^{\mu} - F_L^{e}$ |
| `DeltaP1` | $\Delta_{P_1}^{\mu-e}$ | $Q_1$ | $P_1^{\mu} - P_1^{e}$ |
| `DeltaP2` | $\Delta_{P_2}^{\mu-e}$ | $Q_2$ | $P_2^{\mu} - P_2^{e}$ |
| `DeltaP3` | $\Delta_{P_3}^{\mu-e}$ | $Q_3$ | $P_3^{\mu} - P_3^{e}$ |
| `DeltaP4p` | $\Delta_{P_4^\prime}^{\mu-e}$ | $Q_4$ | $P_4^{\prime\mu} - P_4^{\prime e}$ |
| `DeltaP5p` | $\Delta_{P_5^\prime}^{\mu-e}$ | $Q_5$ | $P_5^{\prime\mu} - P_5^{\prime e}$ |
| `DeltaP6p` | $\Delta_{P_6^\prime}^{\mu-e}$ | $Q_6$ | $P_6^{\prime\mu} - P_6^{\prime e}$ |
| `DeltaP8p` | $\Delta_{P_8^\prime}^{\mu-e}$ | $Q_8$ | $P_8^{\prime\mu} - P_8^{\prime e}$ |

## Ratios and Fractions

| Abbr | LaTeX | Description |
|------|-------|-------------|
| `R` | $R$ | Canonical LFU ratio; bare when the channel key carries the final state |
| `r` | $r$ | Charmonium normalization ratio (CKM amplitude ratio uses `r` under `Ub_I1?_0-n_0.2.Uc_I1?_0-n_0.Us_I1?_0-n_0`) |
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
   in `flav-data-importer/references/observable-naming.md` §3.
3. Add any new particle to the registry in
   `flav-data-importer/references/particle-naming.md`.
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
