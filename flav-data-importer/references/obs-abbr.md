# Transition Symbols and Observable Naming

This document defines the naming conventions for all transitions and observables in the flav-data database. It is the authoritative reference for constructing the observable `name` and the channel keys in JSON entries.

## 1. Transition Symbols: `A.B.2.C.D`

Every decay or scattering process is encoded as a transition symbol using the format `A.B.2.C.D`, representing $A + B \to C + D$. The number `2` replaces the arrow $\to$ to provide a clear, machine-parseable separator between initial and final states.

### Naming Rules

1. **State separator `2`**: `A.B.2.C.D` represents $A+B \to C+D$. The `2`
   always separates the initial state from the final state. Cascades repeat
   the separator: `p+.p+.2.W+.2.mu+.v` = $pp \to W^+ \to \mu^+\nu$.
2. **Particle-type order**: Within each state (initial or final), write
   particles left to right by type: **baryon → meson → charged lepton →
   neutral lepton**. Example: $\Lambda_b^0 \to p\,J/\psi\,\pi^-$ is
   `Lambdab0.2.p+.J/psi0.pi-` (baryon, then mesons).
3. **Mass order within a type**: Among particles of the same type, write
   **heaviest → lightest**. Example: the same $\Lambda_b^0$ decay is
   `Lambdab0.2.p+.J/psi0.pi-` ($J/\psi$ = 3.10 GeV before $\pi^-$ = 0.14 GeV);
   $B^0 \to K^{*0}\tau^- e^+$ is `B0.2.K*0.tau-.e+` ($\tau$ = 1.78 GeV
   before $e$ = 0.0005 GeV). Mass ordering is applied **within each type**:
   a lighter baryon still precedes a heavier meson.
4. **Charge order for equal masses**: When same-type particles have equal
   mass, write **`+` → `-` → `0`**. Example: $B^0 \to e^+ e^-$ is
   `B0.2.e+.e-`; $\tau^+ \tau^-$ is `tau+.tau-`. Mass ordering takes
   precedence, so charge only breaks equal-mass ties.
5. **Particle-state grammar**: every particle state is
   `<name>[*]<charge>[Bar]`:
   - `name` is the particle symbol (`e`, `mu`, `tau`, `Bs`, `B`, `D`,
     `K`, `pi`, `J/psi`, ...), with the letter case of Rule 7.
   - `*` marks a vector meson (`K*`, `D*`, `Ds*`) and sits between the
     name and the charge.
   - `charge` is **mandatory** and is `+`, `-`, or `0`: charged states
     take their sign (`B+`, `B-`, `D*+`, `p+`, `W-`), neutral states
     take `0` (`B0`, `K*0`, `pi0`, `phi0`, `J/psi0`, `Lambda0`, `n0`,
     `H0`). The only charge-less states are neutrinos (`v`, `vBar`,
     `ve`, `vmu`, `vtau`, ...) and the neutral gauge bosons `Z`,
     `gamma`, and `g`.
   - `Bar` is the antiparticle marker of a neutral state or a baryon
     (`B0Bar`, `K*0Bar`, `n0Bar`, `p+Bar`, `Lambda0Bar`). Charged
     mesons, leptons, and bosons use the opposite charge sign instead
     (`B+`/`B-`, `mu+`/`mu-`, `W+`/`W-`) and do not take `Bar`.
   There is no other charge syntax: `p`/`m` suffixes (`Bp`, `pip`, `ep`)
   are rejected. A charge-agnostic token such as `B`, `D`, `K*`, `pi`,
   `e`, `mu`, or `tau` is no longer a valid particle state; a
   charge-averaged measurement is written with a concrete
   charge-conjugate representative. Generic placeholders (`l`, `q`,
   `q1`, `q2`) and non-particle labels (`all`, `had`, `med`, `world`,
   `CDF`, `kappa`) are exempt because they are not particle states;
   placeholders are allowed only in shared multi-transition keys
   (§2.2.2).
6. **Antiparticles**: the marker is always capital `Bar`, placed last.
   Neutral states insert it after the charge (`B0Bar`, `K*0Bar`,
   `n0Bar`); baryons keep it after the charge (`p+Bar`,
   `Lambdac+Bar`, `Lambda0Bar`). Lowercase `bar` is not accepted.
7. **Particle-name case follows the handwritten symbol**: keep the letter
   case of the particle symbol itself. Latin hadrons and capital Greek
   letters stay capital (`B0`, `K+`, `D*0`, `K*0`, `Lambdab0`, `Sigma-`,
   `Omega-`); lower-case Greek letters stay lower case (`pi0`, `pi+`,
   `rho+`, `phi0`, `eta0`, `omega0`, `gamma`). Subscripts stay lower case and
   a superscript is appended as a plain digit: $\pi^0$ → `pi0`,
   $\Lambda_b^0$ → `Lambdab0`, $D_s^{*+}$ → `Ds*+`, $K_S^0$ → `KS0`.
8. **Neutrinos**: Write the handwritten $\nu$ as the letter `v`: use `v` or
   `vBar` with no flavor indicator. **Exception**: when the experimental
   signature is flavor-specific (e.g. tagging a muon-neutrino via inverse
   muon decay, or reconstructing a $\tau^\pm$ from a $\nu_\tau$), append
   the flavor (`ve`, `vmu`, `vtau`, plus `Bar` for the antiparticle:
   `veBar`, `vmuBar`, `vtauBar`). The old spellings `nu`, `nuBar`,
   `nubar`, `nue`, `numu`, `nutau`, and the lowercase-`bar` forms are
   rejected by the validator.
9. **Intermediate resonances**: When an intermediate state decays to a
   dilepton pair, append `(2.l+.l-)` to the resonance name:
   `B0.2.J/psi0.K*0(2.l+.l-)` for $B^0 \to K^{*0} J/\psi(\to \ell^+\ell^-)$
   (mesons heavy to light: $J/\psi$ before $K^{*0}$).
10. **PDG mass labels**: A trailing `(NNNN)` after the charge is the PDG
    mass label in MeV, e.g. `D0*+(2300)` for $D_0^*(2300)^+$. Use it for
    states whose PDG symbol carries a mass label, and follow the PDG
    notation for the spin-parity: $J^P=0^+$ states keep the star
    ($D_0^*$, $D_{s0}^*$), $1^+$ states do not ($D_1$). The label only
    identifies the state; the mass used in the calculation belongs in the
    group note.

Rules 1–5 are **enforced by `scripts/json-valid.py`**: every data key is
`A.B.2.C.D`, and `no-transition` is the only key without `.2.` (a
multi-transition ratio joins two full keys with `/`, e.g.
`B0.2.K*0.e+.e-/B0.2.K*0.mu+.mu-`). Non-canonical order is a validation
failure, as are `p`/`m` charge suffixes, lowercase `bar`, a missing
charge marker, and a `Bar`/`*` in the wrong position. Ordering is
skipped for states containing particles outside the four listed types
(Z/$\gamma$/gluon, quarks, generic placeholders such as `l`/`q`); a
particle missing from `particle-masses.json` is still an error unless it
is listed under `non_orderable`. The charge markers of the exempt
neutrinos and neutral gauge bosons are not required. HFLAV/PDG snapshots
keep their own subgroup names (`HFLAV@B02pilnu`); those are not channel
keys and are not order-checked.

### Examples

| Process | LaTeX | Symbol | Notes |
|---------|-------|--------|-------|
| $B^0 \to e^+ e^-$ | Leptonic decay | `B0.2.e+.e-` | Charged leptons: + then - |
| $\bar{B}^0 \to e^+ e^-$ | Leptonic decay | `B0Bar.2.e+.e-` | Neutral antiparticle uses Bar |
| $B^+ \to K^+ \mu^+ \mu^-$ | Semileptonic | `B+.2.K+.mu+.mu-` | Meson first, then leptons (+ then -) |
| $W^- \to \mu^- \bar{\nu}_\mu$ | Leptonic decay | `W-.2.mu-.vBar` | Charged lepton before neutral lepton |
| $B_s^0 \to \phi \mu^+ \mu^-$ | Semileptonic | `Bs0.2.phi0.mu+.mu-` | Neutral $\phi$ takes `0` |
| $\Lambda_b^0 \to J/\psi\, p\, \pi^-$ | Non-leptonic | `Lambdab0.2.p+.J/psi0.pi-` | Baryon first; mesons heavy to light (`J/psi0` before `pi-`) |
| $pp \to Z \to \mu^+ \mu^-$ | Scattering | `p+.p+.2.Z.2.mu+.mu-` | Two-step process; `Z` is an exempt gauge boson |
| $e^+ e^- \to \mu^+ \mu^-$ | Scattering | `e+.e-.2.mu+.mu-` | Collider process |

### 1.5 Rejected Forms

Compact keys without `.2.` (`B02K*mumu`), `p`/`m` charge suffixes (`Bp`,
`pip`, `ep`), lowercase `bar` (`B0bar`), and particles without a charge
marker (`B.2.D.l.v`, `B0.2.phi.mu+.mu-`, `Lambdab0.2.p.J/psi.pi-`) are
all invalid. New imports use the spellings in the tables below.

### Particle Abbreviations

#### Mesons
| Particle | Symbol | Notes |
|----------|--------|-------|
| $B^0$, $B^+$, $B^-$ | `B0`, `B+`, `B-` | `B` is the $B_u$ particle token; no `Bu` prefix is used |
| $\bar{B}^0$ | `B0Bar` | Neutral antiparticles use Bar |
| $B_s^0$, $\bar{B}_s^0$ | `Bs0`, `Bs0Bar` | |
| $K^+$, $K^0$ | `K+`, `K0` | |
| $K_S^0$, $K_L^0$ | `KS0`, `KL0` | Subscript before superscript; variants such as `K0S`, `K0s`, `K0L` are rejected |
| $K^{*0}$, $\bar{K}^{*0}$ | `K*0`, `K*0Bar` | K* resonance |
| $D^0$, $D^+$ | `D0`, `D+` | |
| $D^{*0}$, $D^{*+}$, $D^{*-}$ | `D*0`, `D*+`, `D*-` | D* resonance (anti-particle is the charged `D*-`) |
| $\pi^0$, $\pi^+$, $\pi^-$ | `pi0`, `pi+`, `pi-` | |
| $\rho^0$, $\rho^+$, $\rho^-$ | `rho0`, `rho+`, `rho-` | |
| $\phi$ | `phi0` | Neutral vector meson |
| $\omega$ | `omega0` | Neutral vector meson (no charged $\omega^\pm$ exists) |
| $J/\psi$ | `J/psi0` | Charmonium |
| $\psi(2S)$ | `psi(2S)0` | Charmonium excited state |
| $\eta$, $\eta'$ | `eta0`, `etaprime0` | |
| $D_s^+$, $D_s^{*+}$ | `Ds+`, `Ds*+` | Strange charmed meson |
| $B_c^+$ | `Bc+` | Bottom-charmed meson |
| $D_0^*(2300)^+$ | `D0*+(2300)` | Scalar $0^+$; the trailing label is the PDG mass in MeV |
| $D_{s0}^*(2317)^+$ | `Ds0*+(2317)` | Scalar $0^+$; PDG mass label in MeV |
| $X_s$ | `Xs` | Inclusive strange hadronic system |

#### Baryons

| Particle | Symbol | Notes |
|----------|--------|-------|
| $\Lambda$, $\Lambda_c^+$, $\Lambda_b^0$ | `Lambda0`, `Lambdac+`, `Lambdab0` | Anti-baryons append `Bar` after the charge: `Lambda0Bar`, `Lambdac+Bar`, `Lambdab0Bar` (Rule 5: charged mesons/leptons use the opposite charge instead, never `Bar`) |
| $\Sigma^+$, $\Sigma^0$, $\Sigma^-$ | `Sigma+`, `Sigma0`, `Sigma-` | Anti-baryons: `Sigma-Bar`, `Sigma0Bar`, `Sigma+Bar` |
| $\Xi_c^0$, $\Xi_b^0$ | `Xic0`, `Xib0` | Anti-baryons: `Xic0Bar`, `Xib0Bar` |
| $\Omega_c^0$ | `Omegac0` | Anti-baryon: `Omegac0Bar` |
| $p$, $n$ | `p+`, `n0` | Anti-baryons: `p+Bar`, `n0Bar` |

#### Leptons and Bosons

| Particle | Symbol | Notes |
|----------|--------|-------|
| $e^+$, $e^-$ | `e+`, `e-` | |
| $\mu^+$, $\mu^-$ | `mu+`, `mu-` | |
| $\tau^+$, $\tau^-$ | `tau+`, `tau-` | |
| $\nu$ (any flavor), $\bar{\nu}$ | `v`, `vBar` | No flavor tag; flavor-specific signatures use `ve`, `vmu`, `vtau` (antiparticles append `Bar`) |
| $W^+$, $W^-$, $Z$ | `W+`, `W-`, `Z` | |
| $\gamma$ | `gamma` | Photon |
| $t$, $\bar{t}$ | `t`, `tBar` | Top quark; quarks keep PDG parton symbols without a charge slot |

Neutrinos and the neutral gauge bosons `Z`, `gamma`, and `g` are the only
charge-less particle states. Quarks/partons (`b`, `c`, `t`, `q`), generic
placeholders (`l`, `q1`, `q2`), inclusive systems (`Xs`, `Xce`, `Xcl`),
nuclei (`Au`, `Ca`, `Ti`), and detector/BSM pseudo-labels (`all`, `had`,
`med`, `world`, `CDF`, `kappa`) are not single particle states; they
carry no charge slot and appear only in legacy keys or shared
multi-transition keys.

## 2. Observable Naming: `OBS` / `OBS[condition]`

Every measured quantity is named by its observable symbol only. The
transition is the enclosing `data` key (Section 1), so `name` must not
repeat it:

- **OBS**: a symbolic abbreviation representing the physical observable (see §3 for the full abbreviation table). Use only symbols — never write full expression definitions.
- **condition**: an optional qualifier in square brackets, used ONLY for multi-transition observables such as ratios or differences between different lepton flavors. Do NOT use `[condition]` to distinguish measurements at different q² bins — use separate groups with `q2min`/`q2max` instead.
- **parameter tags**: optional parentheses for non-transition qualifiers, e.g. `Vcb(CLN)`, `R1(CLN)`, `f+.Vcs`. A transition inside parentheses is invalid.

Examples: `FL`, `Br`, `dBr/dq2`, `DeltaP6p[mu-e]`, `RBr[mu/e]`, `Vcb(CLN)`.

### 2.1 Basic Observables (No Transition)

**Basic observables** describe intrinsic particle properties — they do not involve a decay or scattering process. The naming format is `OBS(particle)` (no transition symbol needed):

| Observable | LaTeX | Symbol | Notes |
|------------|-------|--------|-------|
| Mass $M_t$ | $M_f$ | `Mass(t)` | On-shell mass |
| Mass $M_Z$ | $M_Z$ | `Mass(Z)` | On-shell mass of a resonance |
| $\overline{\text{MS}}$ mass $m_t$ | $m_t$ | `mass(t)` | Running mass |
| Lifetime $\tau_{e^-}$ | $\tau_f$ | `Tau(e-)` | Particle lifetime |

**Short particle-mass shortcuts** — accepted by the validator for legacy data; new imports should use the generic `Mass(f)` form:

| Symbol | Particle | Replaces |
|--------|----------|----------|
| `MZ` | $Z$ boson | `Mass(Z)` |
| `MW` | $W$ boson | `Mass(W)` |
| `Mtop`, `MH`, `Mh` | top quark, Higgs, light Higgs | `Mass(t)`, `Mass(H0)`, `Mass(h0)` |

**Bare names** (no transition) — `gammaCKM`, `r`, `delta`, `|Vtd|`,
`|Vts|`, `|Vub|`, `|Vcb|`, `R_b`, `R_c`, `S_phigamma`, `C_phigamma`,
`ADelta_phigamma`, `fs/fd`, `ge/gmu`, `ge/gtau`. Meanings and LaTeX are in
the §3 tables (CKM Parameters, Electroweak and Other Pseudo-Observables,
Bare Ratios).

### 2.2 Decay and Scattering Observables

Decay or scattering observables use the same bare symbol; the process is
the `data` key. The key follows the full `A.B.2.C.D` format (scattering)
or `A.2.C.D` format (decay).

#### 2.2.1 Single-Transition Observables

For observables measuring a single process, no condition is needed:

| Observable | LaTeX | Symbol | Data key |
|------------|-------|--------|----------|
| Branching fraction $\mathcal{B}(B^0 \to e^+ e^-)$ | $\mathcal{B}$ | `Br` | `B0.2.e+.e-` |
| Decay width $\Gamma(K^{*0} \to K^+ \pi^-)$ | $\Gamma$ | `Gamma` | `K*0.2.K+.pi-` |
| Differential branching fraction | $d\mathcal{B}/dq^2$ | `dBr/dq2` | `B0.2.Xs.gamma` |
| Cross section $\sigma(pp \to e^+ e^-)$ | $\sigma(pp \to e^+ e^-)$ | `Sigma` | `p+.p+.2.e+.e-` |
| Charge asymmetry $A_C(B^+ \to J/\psi K^+)$ | $A_C(B^+ \to J/\psi K^+)$ | `AC` | `B+.2.J/psi0.K+` |
| Mass difference $\Delta M_s$ | $\Delta M_s$ | `DeltaMass` | `Bs0.2.Bs0Bar` |
| Decay fraction $f(Z \to \mu^+ \mu^-)$ | $f(Z \to \mu^+ \mu^-)$ | `f` | `Z.2.mu+.mu-` |

#### 2.2.2 Multi-Transition Observables

For observables comparing two or more transitions (e.g., lepton flavor universality tests):

- The **data key** uses the shared part of the multi-transition process.
- Shared particles are written generically: `l+`/`l-` (or `l`) and
  `q1`/`q2` (or `q`), which are listed under `non_orderable` in
  `particle-masses.json` and skip the order check. Neutrinos are not
  placeholders: `v`/`vBar` (and `ve`, `vmu`, `vtau`, ...) carry mass 0 in
  `masses` and sort as neutral leptons. Numbered lepton, neutrino, or
  hadron placeholders (`l1`, `v1`, `h1`) are rejected.
- **condition** encodes the flavor mapping, e.g. `[mu/e]` means the muon
  mode over the electron mode.
  - **`/` (slash)** in condition → `R` ratio: `RBr[mu/e]` = $\mathcal{B}(B^0\to K^{*0}\mu^+\mu^-)/\mathcal{B}(B^0\to K^{*0}e^+e^-)$.
  - **`-` (dash)** in condition → `Delta` difference: `DeltaACP[mu-e]` = $A_{CP}(B^-\to\mu^- \bar{\nu}) - A_{CP}(B^-\to e^-\bar{\nu})$.

| Observable | LaTeX | Symbol | Data key |
|------------|-------|--------|----------|
| $R_{K^*} = \frac{\mathcal{B}(B^0 \to K^{*0}\mu^+\mu^-)}{\mathcal{B}(B^0 \to K^{*0}e^+e^-)}$ | $R_{K^*}$ | `RBr[mu/e]` | `B0.2.K*0.l+.l-` |
| $R_K = \frac{\mathcal{B}(B^+ \to K^+\mu^+\mu^-)}{\mathcal{B}(B^+ \to K^+e^+e^-)}$ | $R_K$ | `RBr[mu/e]` | `B+.2.K+.l+.l-` |
| $\Delta A_{CP} = A_{CP}(\mu) - A_{CP}(e)$ | $\Delta A_{CP}$ | `DeltaACP[mu-e]` | `B-.2.l-.vBar` |
| $r = \frac{A(B^- \to \bar{D}^0 K^-)}{A(B^- \to D^0 K^-)}$ | $r$ | `r` | `B-.2.D0.K-` |
| $\delta = \arg \frac{A(B^- \to \bar{D}^0 K^-)}{A(B^- \to D^0 K^-)}$ | $\delta$ | `delta` | `B-.2.D0.K-` |

**CKM parameters**: $r$ and $\delta$ are defined via $B^-$ decay amplitude ratios ($b \to u$ suppressed relative to $b \to c$ favored). The B meson and final-state meson in the transition must carry **negative charge**: `B-.2.D0.K-`, `B-.2.D0.pi-` (canonical order: mesons heaviest to lightest, so `D0` before `K-`/`pi-`).

### 2.3 Observable Differences and Ratios (Unified Convention)

Unless otherwise specified, differences and ratios between observables follow these patterns:

| Type | Symbol | LaTeX | Example |
|------|--------|-------|---------|
| Difference | `DeltaOBS[condition]` | $\Delta_{OBS}^{condition}$ | `DeltaBr[mu-e]` |
| Ratio | `ROBS[condition]` | $R_{OBS}^{condition}$ | `RFL[mu/e]` |
| LFU ratio | `R` | $R(X)$ | `R` |

The canonical LFU ratio $R(X)=\mathcal{B}(B\to X\tau\nu)/\mathcal{B}(B\to X\ell\nu)$ is the **bare symbol `R`** whenever the channel key already fixes the final state $X$ (e.g. `R` under `B0Bar.2.D+.tau-.vBar` is \(R(D)\)); in that case do not repeat $X$ in the name (no `RD`, `RD*`). Ratios that compare other observables still use `ROBS[condition]`.

Examples:
| LaTeX | Symbol | Description |
|-------|--------|-------------|
| $\Delta_{A_{CP}}^{\mu-e}(B^0 \to K^{*0} \ell^+\ell^-)$ | `DeltaACP[mu-e]` | CP asymmetry difference |
| $R_{F_L}^{\mu/e}(B^0 \to K^{*0} \ell^+\ell^-)$ | `RFL[mu/e]` | Longitudinal polarization ratio |
| $\Delta_{\mathcal{B}}^{\mu-e}(B^0 \to K^{*0} \ell^+\ell^-)$ | `DeltaBr[mu-e]` | Branching fraction difference |
| $R(D)$ | `R` | LFU ratio (channel carries $D$) |

### 2.4 Form-Factor Expansion Coefficients: `aN_FF`

Coefficients of a form-factor expansion (z-expansion, BCL, ...) are
named `aN_FF`:

- `N` — expansion order: 0, 1, 2, ...
- `FF` — form-factor symbol from the table below.

Examples: `a0_F+`, `a1_F0`, `a2_Fv`, `a0_Gv`. When the source quotes one
number for several form factors, write one observable per symbol and
repeat the value/errors (`a0_Gv` and `a0_G+`), never joined into a
single name such as `a0_Gv_G+`.

The prefix always marks the expansion order, even when the paper labels its
coefficients differently: a BCL fit that writes `b_i^+`, `b_i^0`, `b_i^T`
becomes `a0_f+`, `a1_f+`, ..., `a0_f0`, ..., `a0_fT`, ... .

Fit choices (nominal, higher-order, ...) are **not** part of the name and
are not stored in the group metadata; keep such variants as separate
groups. The group-level `dataset` records data sources only.

Every group holding `aN_FF` coefficients must also carry a group-level
`scheme` naming the expansion form. The JSON stores only the short code;
the full name and defining paper live in this table:

| Scheme | Parametrization | Source |
|--------|-----------------|--------|
| `BK` | Becirevic-Kaidalov | arXiv:hep-ph/9904490 |
| `BGL` | Boyd-Grinstein-Lebed | arXiv:hep-ph/9504235 |
| `BCL` | Bourrely-Caprini-Lellouch | arXiv:0807.2722 |
| `BSZ` | Bharucha-Straub-Zwicky | arXiv:1503.05534 |
| `DLM` | Detmold-Lehner-Meinel | arXiv:1503.01421 |
| `MR` | Meinel-Rendon $w$-expansion, $f(q^2)=[1-q^2/(m_{\rm pole}^f)^2]^{-1}\sum_n a_n^f (w-1)^n$ (pole factor omitted where the source does not use one) | arXiv:2009.09313, arXiv:2107.13140 |

The key sits beside the channel keys, after `dataset` and before any
matrix: channel keys → `dataset` → `scheme` → matrices. The validator
rejects any other scheme spelling and rejects a coefficient group
without `scheme`.

**Form-factor symbols** (use the notation of the paper's own
decomposition; these are the standard symbols):

| Symbol | Form factor |
|--------|-------------|
| `f+` | $f_+$ |
| `f-` | $f_-$ |
| `f0` | $f_0$ |
| `fT` | $f_T$ |
| `V` | $V$ |
| `A0` | $A_0$ |
| `A1` | $A_1$ |
| `A12` | $A_{12}$ |
| `T1` | $T_1$ |
| `T2` | $T_2$ |
| `T23` | $T_{23}$ |
| `F+` | helicity $f_+$ |
| `F0` | helicity $f_0$ |
| `Fv` | helicity $f_\perp$ |
| `Fv'` | helicity $f_{\perp'}$ ($J^P=3/2^-$) |
| `G+` | helicity $g_+$ |
| `G0` | helicity $g_0$ |
| `Gv` | helicity $g_\perp$ |
| `Gv'` | helicity $g_{\perp'}$ ($J^P=3/2^-$) |
| `h+` | helicity $h_+$ |
| `hv` | helicity $h_\perp$ |
| `hv'` | helicity $h_{\perp'}$ ($J^P=3/2^-$) |
| `ht+` | helicity $\tilde{h}_+$ |
| `htv` | helicity $\tilde{h}_\perp$ |
| `htv'` | helicity $\tilde{h}_{\perp'}$ ($J^P=3/2^-$) |
| `g` | BGL $g$ ($\bar B \to D^*$) |
| `f` | BGL $f$ ($\bar B \to D^*$) |
| `F1` | BGL $F_1$ ($\bar B \to D^*$) |
| `F2` | BGL $F_2$ ($\bar B \to D^*$) |

For a BGL $z$-series fit of the $\bar B_{(s)} \to D_{(s)}^{(*)}
\ell\bar\nu_\ell$ form factors, the basis is $f_+, f_0$ for the
pseudoscalar channel and $g, f, F_1, F_2$ for the vector channel, so the
coefficients are named `aN_f+`, `aN_f0`, `aN_g`, `aN_f`, `aN_F1`,
`aN_F2` (e.g. `a0_f+`, `a2_F1`).

Baryon semileptonic decays ($\Lambda_b \to \Lambda_c \ell^- \bar{\nu}$,
$\Lambda_b \to p \ell^- \bar{\nu}$) use the helicity set, with the
mapping $f_+ \to$ `F+`, $f_0 \to$ `F0`, $f_\perp \to$ `Fv`,
$g_+ \to$ `G+`, $g_0 \to$ `G0`, $g_\perp \to$ `Gv`,
$h_+ \to$ `h+`, $h_\perp \to$ `hv`. The $J^P=3/2^-$ final states carry
four additional primed form factors, mapped with a trailing apostrophe:
$f_{\perp'} \to$ `Fv'`, $g_{\perp'} \to$ `Gv'`,
$h_{\perp'} \to$ `hv'`, $\tilde{h}_{\perp'} \to$ `htv'`.

Papers that work directly in the HQET basis, rather than the helicity
set, keep their own symbols:

| Symbol | Form factor |
|--------|-------------|
| `f1` | Dirac vector form factor $f_1$ ($\Lambda_b \to p,\Lambda$) |
| `f2` | Dirac tensor form factor $f_2$, in GeV$^{-1}$ |
| `g2` | Dirac axial form factor $g_2$ ($\Lambda_b \to \Lambda$) |
| `F1` | HQET-basis form factor $F_1$ |
| `F2` | HQET-basis form factor $F_2$ |

`F1` and `F2` also name the BGL vector-channel coefficients; the
transition key disambiguates the two bases. These symbols name
form-factor values at a fixed kinematic point, not expansion
coefficients, so such a group carries no `scheme`; record the basis and
the kinematic point in the group `note`.

The fraction spellings `fp`, `Fp`, `Gp`, `hp`, and `htp` are obsolete and
rejected by the validator; write the plus charge explicitly (`f+`, `F+`,
`G+`, `h+`, `ht+`). `Fv`, `Gv`, `hv`, and `htv` keep their existing
spelling.

### 2.5 Zero-Recoil Form-Factor Normalization: `hA1(1)`

The zero-recoil normalization of the $\bar B \to D^*$ axial form factor is
written `hA1(1)`:
$h_{A_1}(1)=(M_B+M_{D^*})A_1(q^2_\mathrm{max})/(2\sqrt{M_BM_{D^*}})$.
The transition key selects the channel: `B0Bar.2.D*+.l-.vBar` carries
$h_{A_1}(1)$ and `Bs0Bar.2.Ds*+.l-.vBar` carries the $B_s$ value
$h^s_{A_1}(1)$. The parenthetical `(1)` is a parameter tag, not a
multi-transition condition. This symbol names a form-factor value, not an
expansion coefficient, so the group does not need `scheme`.

### 2.6 Form-Factor Values at Fixed `q2`

A form-factor value at a fixed momentum transfer uses the bare symbol from
the table in §2.4 (`V`, `A0`, `A1`, `A2`, `A12`, `f+`, `f-`, ...), not the
`aN_FF` coefficient form. Each `obs@N` sets `q2min` and `q2max` to the same
value when the source quotes a point, so repeated symbols at different
`q2` stay distinguishable; a value group carries no `scheme`. The group
`note` records how the values were obtained (fit, sum rule, ...) and
whether correlations were published.

## 3. Observable Abbreviations

Each observable is listed with its flav-data abbreviation, LaTeX symbol, typical paper notation, and description.

The tables below group abbreviations by observable type for reference
only. The JSON has no category layer: a group's channel keys map straight
to `obs@N` objects (json-meta.md §"Data Entries"), and angular and
differential observables share a group only when the source matrix
genuinely couples them (SKILL.md rule 6).

### Branching Fractions and Decay Widths

| Abbr | LaTeX | Paper Notation | Description |
|------|-------|---------------|-------------|
| `Br` | $\mathcal{B}$ | $\mathcal{B}$ | Branching fraction |
| `dBr/dq2` | $d\mathcal{B}/dq^2$ | $d\mathcal{B}/dq^2$ | Differential branching fraction |
| `Gamma` | $\Gamma$ | $\Gamma$ | Decay width (partial or total) |

### Lifetimes

| Abbr | LaTeX | Paper Notation | Description |
|------|-------|---------------|-------------|
| `Tau` | $\tau$ | $\tau$ | Particle lifetime |

### Masses and Mixing Parameters

| Abbr | LaTeX | Paper Notation | Description |
|------|-------|---------------|-------------|
| `Mass` | $M_f$ | $M$ | On-shell mass (uppercase). Written as `Mass(f)` where $f$ is the particle symbol. Common single-token forms: `MZ`, `MW`, `Mtop`, `MH`, `Mh`. |
| `mass` | $m$ | $m$ | $\overline{\text{MS}}$ mass (lowercase) |
| `DeltaMass` | $\Delta M$ | $\Delta M_s$, $\Delta M_d$ | Mass difference / neutral meson mixing parameter |
| `DeltaGamma` | $\Delta\Gamma$ | $\Delta\Gamma_s$, $\Delta\Gamma_d$ | Decay width difference / neutral meson mixing parameter |

### Scattering Cross Sections

| Abbr | LaTeX | Paper Notation | Description |
|------|-------|---------------|-------------|
| `Sigma` | $\sigma$ | $\sigma$ | Total or fiducial cross section |
| `dSigma/dpT` | $d\sigma/dp_T$ | $d\sigma/dp_T$ | Differential cross section (transverse momentum) |
| `dSigma/deta` | $d\sigma/d\eta$ | $d\sigma/d\eta$ | Differential cross section (pseudorapidity) |

### Angular Coefficients (CP-averaged)

Angular coefficients parameterize the angular distribution of decay products. They are the coefficients in the Legendre polynomial expansion of the differential decay rate.

For $B^0 \to K^{*0}(\to K^+ \pi^-) \mu^+ \mu^-$, the standard basis uses 12 angular observables per q² bin (plus S-wave and CP-asymmetric extensions).

| Abbr | LaTeX | Paper Notation | Description | Typical Range |
|------|-------|---------------|-------------|--------------|
| `S1c` | $S_1^c$ | $S_1^c$ | Longitudinal amplitude coefficient | [0, 1] |
| `S2c` | $S_2^c$ | $S_2^c$ | Transverse amplitude coefficient | [-1, 0] |
| `S2s` | $S_2^s$ | $S_2^s$ | Transverse amplitude coefficient (sine component) | [-1, 0] |
| `S3` | $S_3$ | $S_3$ | T-odd angular coefficient | [-0.5, 0.5] |
| `S4` | $S_4$ | $S_4$ | Angular coefficient | [-1, 1] |
| `S5` | $S_5$ | $S_5$ | Angular coefficient | [-1, 1] |
| `S6c` | $S_{6c}$ | $S_{6c}$ | Angular coefficient (c-component) | [-1, 1] |
| `AFB` | $A_{FB}$ | $A_{FB}$ | Forward-backward asymmetry of the dilepton system | [-1, 1] |
| `S7` | $S_7$ | $S_7$ | T-odd angular coefficient | [-1, 1] |
| `S8` | $S_8$ | $S_8$ | T-odd angular coefficient | [-1, 1] |
| `S9` | $S_9$ | $S_9$ | T-odd angular coefficient | [-0.5, 0.5] |
| `FL` | $F_L$ | $F_L$ | Longitudinal polarization fraction of the vector meson | [0, 1] |
| `FS` | $F_S$ | $F_S$ | S-wave fraction | [0, 1] |
| `FH` | $F_H$ | $F_H$ | Angular distribution flat term (B → Kℓℓ) | [-1, 1] |
| `S1ac` | $S_{1a}^c$ | $S_{1a}^c$ | Additional longitudinal coefficient | — |
| `S1bcre` | $S_{1bc}^{\mathrm{Re}}$ | $S_{1bc}^{\mathrm{Re}}$ | Interference coefficient (real part) | — |
| `S1bcim` | $S_{1bc}^{\mathrm{Im}}$ | $S_{1bc}^{\mathrm{Im}}$ | Interference coefficient (imaginary part) | — |

### S-wave Observables

When the $K^+ \pi^-$ system includes non-resonant S-wave contributions (not purely $K^{*0}$), additional observables are measured:

| Abbr | LaTeX | Paper Notation | Description |
|------|-------|---------------|-------------|
| `SS1re` | $S_{S1}^{\mathrm{Re}}$ | $S_{S1}^{\mathrm{Re}}$ | S-wave interference (real part) |
| `SS1im` | $S_{S1}^{\mathrm{Im}}$ | $S_{S1}^{\mathrm{Im}}$ | S-wave interference (imaginary part) |
| `SS2re` | $S_{S2}^{\mathrm{Re}}$ | $S_{S2}^{\mathrm{Re}}$ | S-wave interference (real part) |
| `SS2im` | $S_{S2}^{\mathrm{Im}}$ | $S_{S2}^{\mathrm{Im}}$ | S-wave interference (imaginary part) |
| `SS3re` | $S_{S3}^{\mathrm{Re}}$ | $S_{S3}^{\mathrm{Re}}$ | S-wave interference (real part) |
| `SS3im` | $S_{S3}^{\mathrm{Im}}$ | $S_{S3}^{\mathrm{Im}}$ | S-wave interference (imaginary part) |
| `SS4re` | $S_{S4}^{\mathrm{Re}}$ | $S_{S4}^{\mathrm{Re}}$ | S-wave interference (real part) |
| `SS4im` | $S_{S4}^{\mathrm{Im}}$ | $S_{S4}^{\mathrm{Im}}$ | S-wave interference (imaginary part) |
| `SS5re` | $S_{S5}^{\mathrm{Re}}$ | $S_{S5}^{\mathrm{Re}}$ | S-wave interference (real part) |
| `SS5im` | $S_{S5}^{\mathrm{Im}}$ | $S_{S5}^{\mathrm{Im}}$ | S-wave interference (imaginary part) |

### CP Asymmetry Observables

| Abbr | LaTeX | Paper Notation | Description |
|------|-------|---------------|-------------|
| `ACP` | $A_{CP}$ | $A_{CP}$ | Direct CP asymmetry |
| `DeltaACP` | $\Delta A_{CP}$ | $\Delta A_{CP}$ | Difference in CP asymmetry between two modes |
| `AFB_CP` | $A_{CP}^{FB}$ | $A_{CP}^{FB}$ | CP asymmetry of forward-backward asymmetry |
| `AFS` | $A_{CP}^{FS}$ | $A_{CP}^{FS}$ | CP asymmetry of S-wave fraction |
| `A1c` | $A_{1c}$ | $A_{1c}$ | CP asymmetry of $S_1^c$ |
| `A2s` | $A_{2s}$ | $A_{2s}$ | CP asymmetry of $S_2^s$ |
| `A3` | $A_3$ | $A_3$ | CP asymmetry of $S_3$ |
| `A4` | $A_4$ | $A_4$ | CP asymmetry of $S_4$ |
| `A5` | $A_5$ | $A_5$ | CP asymmetry of $S_5$ |
| `A6c` | $A_{6c}$ | $A_{6c}$ | CP asymmetry of $S_{6c}$ |
| `A7` | $A_7$ | $A_7$ | CP asymmetry of $S_7$ |
| `A8` | $A_8$ | $A_8$ | CP asymmetry of $S_8$ |
| `A9` | $A_9$ | $A_9$ | CP asymmetry of $S_9$ |

### CP-Asymmetric S-wave Observables

| Abbr | LaTeX | Paper Notation | Description |
|------|-------|---------------|-------------|
| `AS1im` | $A_{S1}^{\mathrm{Im}}$ | $A_{S1}^{\mathrm{Im}}$ | CP asymmetry of S-wave interference |
| `AS1re` | $A_{S1}^{\mathrm{Re}}$ | $A_{S1}^{\mathrm{Re}}$ | CP asymmetry of S-wave interference |
| `AS2im` | $A_{S2}^{\mathrm{Im}}$ | $A_{S2}^{\mathrm{Im}}$ | CP asymmetry of S-wave interference |
| `AS2re` | $A_{S2}^{\mathrm{Re}}$ | $A_{S2}^{\mathrm{Re}}$ | CP asymmetry of S-wave interference |
| `AS3im` | $A_{S3}^{\mathrm{Im}}$ | $A_{S3}^{\mathrm{Im}}$ | CP asymmetry of S-wave interference |
| `AS3re` | $A_{S3}^{\mathrm{Re}}$ | $A_{S3}^{\mathrm{Re}}$ | CP asymmetry of S-wave interference |
| `AS4im` | $A_{S4}^{\mathrm{Im}}$ | $A_{S4}^{\mathrm{Im}}$ | CP asymmetry of S-wave interference |
| `AS4re` | $A_{S4}^{\mathrm{Re}}$ | $A_{S4}^{\mathrm{Re}}$ | CP asymmetry of S-wave interference |
| `AS5im` | $A_{S5}^{\mathrm{Im}}$ | $A_{S5}^{\mathrm{Im}}$ | CP asymmetry of S-wave interference |
| `AS5re` | $A_{S5}^{\mathrm{Re}}$ | $A_{S5}^{\mathrm{Re}}$ | CP asymmetry of S-wave interference |

### Optimized Observables (P)

These are constructed to reduce theoretical uncertainties from hadronic form factors by forming ratios that cancel leading form-factor dependencies.

| Abbr | LaTeX | Paper Notation | Definition |
|------|-------|---------------|-----------|
| `P1` | $P_1$ | $P_1$ | $S_3 / (1 - F_L)$ |
| `P2` | $P_2$ | $P_2$ | $\beta / [2(1 - F_L)]$ where $\beta$ relates to AFB |
| `P3` | $P_3$ | $P_3$ | $\mathrm{Im}(G_\perp G_\parallel^*) / (1 - F_L)$ |
| `P4p` | $P_4^\prime$ | $P_4^\prime$ | Optimized version of S4 (prime denoted by `p`) |
| `P5p` | $P_5^\prime$ | $P_5^\prime$ | Optimized version of S5 |
| `P6p` | $P_6^\prime$ | $P_6^\prime$ | Optimized version of S6 |
| `P6cp` | $P_{6c}^\prime$ | $P_{6c}^\prime$ | Optimized version of S6c |
| `P8p` | $P_8^\prime$ | $P_8^\prime$ | Optimized version of S8 |

### Reduced Asymmetry Observables

| Abbr | LaTeX | Paper Notation | Description |
|------|-------|---------------|-------------|
| `A6p` | $A_6^\prime$ | $A_6^\prime$ | Reduced forward-backward asymmetry: $A_6/(1 - F_L)$ for $B_s \to \phi\ell\ell$ |

### Time-Dependent CP Parameters

| Abbr | LaTeX | Paper Notation | Description |
|------|-------|---------------|-------------|
| `C` | $C$ | $C$ | Direct CP violation parameter in time-dependent analysis |
| `S` | $S$ | $S$ | Mixing-induced CP violation parameter |

### LFU Difference Observables

Differences of angular coefficients between muon and electron modes, used to test lepton flavor universality with reduced theoretical uncertainties: $\Delta X = X^{\mu} - X^{e}$. The JSON `name` always uses the unified `DeltaOBS` form with the `[mu-e]` condition tag (§2.3), e.g. `DeltaFL[mu-e]`, `DeltaP5p[mu-e]`. Papers label these $Q_X$ ($Q_i \equiv \Delta P_i$, $Q_{F_L} \equiv \Delta F_L$); the table maps that notation to the flav-data name. The $Q$ spelling is rejected by the validator.

| Abbr | LaTeX | Paper Notation | Definition |
|------|-------|---------------|-----------|
| `DeltaFL` | $\Delta_{F_L}^{\mu-e}$ | $Q_{F_L}$ | $F_L^{\mu} - F_L^{e}$ |
| `DeltaP1` | $\Delta_{P_1}^{\mu-e}$ | $Q_1$ | $P_1^{\mu} - P_1^{e}$ |
| `DeltaP2` | $\Delta_{P_2}^{\mu-e}$ | $Q_2$ | $P_2^{\mu} - P_2^{e}$ |
| `DeltaP3` | $\Delta_{P_3}^{\mu-e}$ | $Q_3$ | $P_3^{\mu} - P_3^{e}$ |
| `DeltaP4p` | $\Delta_{P_4^{\prime}}^{\mu-e}$ | $Q_4$ | $P_4^{\prime\mu} - P_4^{\prime e}$ |
| `DeltaP5p` | $\Delta_{P_5^{\prime}}^{\mu-e}$ | $Q_5$ | $P_5^{\prime\mu} - P_5^{\prime e}$ |
| `DeltaP6p` | $\Delta_{P_6^{\prime}}^{\mu-e}$ | $Q_6$ | $P_6^{\prime\mu} - P_6^{\prime e}$ |
| `DeltaP8p` | $\Delta_{P_8^{\prime}}^{\mu-e}$ | $Q_8$ | $P_8^{\prime\mu} - P_8^{\prime e}$ |

### Ratios and Normalizations

| Abbr | LaTeX | Paper Notation | Description |
|------|-------|---------------|-------------|
| `R` | $R$ | $R_X$ | Canonical LFU ratio, written bare when the channel key carries the final state (e.g. `R` under `B0Bar.2.D+.tau-.vBar` is \(R(D)\)); do not repeat the final state in the name. Ratios of other observables use `ROBS[condition]` (e.g. `RFL[mu/e]`). See §2.3. |
| `r` | $r$ | $r_{J/\psi}$ | Charmonium normalization ratio (e.g., $R_K = r_{J/\psi} \cdot R_{K,J/\psi}$). For the CKM amplitude ratio in $B \to DK$ decays, see **CKM Parameters** below. |

### Asymmetries and Fractions

| Abbr | LaTeX | Paper Notation | Description |
|------|-------|---------------|-------------|
| `S1` | $S_1$ | $S_1$ | Generic scalar asymmetry parameter (not the same as the specific `S1c` angular coefficient) |
| `AC` | $A_C$ | $A_C$ | Charge asymmetry |
| `f` | $f$ | $f$ | Generic fraction or proportion: decay fraction, fragmentation fraction, or any dimensionless ratio |

### Electroweak and Other Pseudo-Observables

| Abbr | LaTeX | Paper Notation | Description |
|------|-------|---------------|-------------|
| `R_b` | $R_b$ | $R_b$ | $Z \to b\bar{b}$ partial width ratio |
| `R_c` | $R_c$ | $R_c$ | $Z \to c\bar{c}$ partial width ratio |
| `S_phigamma` | $S_{\phi\gamma}$ | $S$ | CP-violating parameter in $B_s \to \phi\gamma$ |
| `C_phigamma` | $C_{\phi\gamma}$ | $C$ | Direct CP asymmetry in $B_s \to \phi\gamma$ |
| `ADelta_phigamma` | $\mathcal{A}^{\Delta}_{\phi\gamma}$ | $\mathcal{A}^{\Delta}$ | Time-dependent CP asymmetry in $B_s \to \phi\gamma$ |

### Bare Ratios (No Transition)

Conventional LEP/PDG ratios whose underlying process is implied; they sit
under the `no-transition` channel key.

| Abbr | LaTeX | Paper Notation | Description |
|------|-------|---------------|-------------|
| `fs/fd` | $f_s/f_d$ | $f_s/f_d$ | Fragmentation ratio of $B_s$ to $B^0$ |
| `ge/gmu` | $g_e/g_\mu$ | $g_e/g_\mu$ | Lepton coupling ratio at the $Z$ |
| `ge/gtau` | $g_e/g_\tau$ | $g_e/g_\tau$ | Lepton coupling ratio at the $Z$ |

### CKM Parameters

| Abbr | LaTeX | Paper Notation | Description |
|------|-------|---------------|-------------|
| `gammaCKM` | $\gamma_{CKM}$ | $\gamma$, $\phi_3$ | CKM unitarity triangle angle |
| `\|Vtd\|` | $\|V_{td}\|$ | $\|V_{td}\|$ | CKM matrix element magnitude |
| `\|Vts\|` | $\|V_{ts}\|$ | $\|V_{ts}\|$ | CKM matrix element magnitude |
| `\|Vub\|` | $\|V_{ub}\|$ | $\|V_{ub}\|$ | CKM matrix element magnitude |
| `\|Vcb\|` | $\|V_{cb}\|$ | $\|V_{cb}\|$ | CKM matrix element magnitude |
| `r` | $r$ | $r_B$, $r_D$ | Amplitude ratio (decay channel specified in transition) |
| `delta` | $\delta$ | $\delta_B$, $\delta_D$ | Strong phase difference |

### Decay Constants, Quark Masses, and Bag Parameters (No Transition)

Intrinsic QCD quantities reported by lattice or sum-rule calculations sit
under `no-transition`. Quark masses are $\overline{\text{MS}}$ masses at
2 GeV unless the paper states another scale; the scale belongs in the
group-level `note`, not in the name.

| Abbr | LaTeX | Paper Notation | Description |
|------|-------|---------------|-------------|
| `fpi` | $f_\pi$ | $f_\pi$ | Pion decay constant |
| `fK` | $f_K$ | $f_K$ | Kaon decay constant |
| `fK/fpi` | $f_K/f_\pi$ | $f_K/f_\pi$ | Decay-constant ratio |
| `fD` | $f_D$ | $f_D$ | $D$ decay constant |
| `fDs` | $f_{D_s}$ | $f_{D_s}$ | $D_s$ decay constant |
| `fDs/fD` | $f_{D_s}/f_D$ | $f_{D_s}/f_D$ | Decay-constant ratio |
| `fB0` | $f_{B^0}$ | $f_{B^0}$ | $B^0$ decay constant |
| `fB+` | $f_{B^+}$ | $f_{B^+}$ | $B^+$ decay constant |
| `fBs` | $f_{B_s}$ | $f_{B_s}$ | $B_s$ decay constant |
| `fBs/fB` | $f_{B_s}/f_B$ | $f_{B_s}/f_B$ | Decay-constant ratio (isospin average) |
| `fBs/fB0` | $f_{B_s}/f_{B^0}$ | $f_{B_s}/f_{B^0}$ | Decay-constant ratio |
| `fBs/fB+` | $f_{B_s}/f_{B^+}$ | $f_{B_s}/f_{B^+}$ | Decay-constant ratio |
| `xi` | $\xi$ | $\xi$ | $SU(3)$-breaking ratio $\xi=f_{B_s}\sqrt{B_{B_s}}/(f_B\sqrt{B_{B_d}})$ |
| `mud` | $m_{ud}$ | $m_{ud}$ | Average light-quark mass, $m_{ud}=(m_u+m_d)/2$ |
| `ms` | $m_s$ | $m_s$ | Strange-quark mass |
| `ms/mud` | $m_s/m_{ud}$ | $m_s/m_{ud}$ | Quark-mass ratio |
| `BK` | $B_K$ | $B_K$ | Kaon bag parameter |
| `BhatK` | $\hat{B}_K$ | $\hat{B}_K$ | Renormalization-group-invariant kaon bag parameter |
| `BBs/BBd` | $B_{B_s}/B_{B_d}$ | $B_{B_s}/B_{B_d}$ | Bag-parameter ratio |

## 4. LaTeX Notation

The LaTeX symbol for each abbreviation is listed in §3 tables (column
"LaTeX") as a notation reference for papers and plots. JSON data stores
no LaTeX for transitions or observables: the channel key carries the
transition and each observable carries only its bare `name`.

**JSON escaping**: In top-level `title`/`abstract` LaTeX, a single backslash (e.g., the `\t` in `\to`) must be written as a double backslash (`\\to`) in JSON file text. Python's `json.load()` restores the single backslash automatically.

## 5. Common q² Intervals (GeV²)

These are the most frequently used q² bin boundaries in B → K(*)ℓℓ analyses. **Always use the exact values reported in the paper** — this table is a quick reference only; paper-specific binning takes precedence.

| Region | Intervals |
|--------|-----------|
| Very low (electron mode) | [0.0008, 0.257], [0.002, 1.12] |
| Low q² | [0.06, 0.98], [0.1, 1.1], [1.1, 2.5], [1.1, 4.0], [1.1, 6.0], [2.0, 3.0], [2.0, 4.0], [3.0, 4.0], [4.0, 5.0], [4.0, 6.0], [5.0, 6.0], [6.0, 7.0], [6.0, 8.0] |
| Fine binning (comprehensive analyses) | [0.06, 0.54], [0.54, 0.98], [1.1, 1.8], [1.8, 2.5], [2.5, 3.25], [3.25, 4.0], [4.0, 5.0], [5.0, 6.0], [6.0, 7.0], [7.0, 8.0], [11.0, 11.75], [11.75, 12.5], [15.0, 16.0], [16.0, 17.0], [17.0, 18.0], [18.0, 19.0] |
| Charmonium veto | [8.0, 11.0], [11.0, 12.5] — usually excluded due to resonances |
| High q² | [14.0, 22.0], [14.3, ∞], [15.0, 17.0], [15.0, 19.0], [16.0, 17.0], [17.0, 19.0], [18.0, 19.0] |

## 6. Adding New Observables

When a paper introduces an observable not listed in this document:

1. **Confirm the physical meaning** and identify the standard notation used in the literature.
2. **Choose or create an abbreviation** following §2 and add it to the matching §3 table with its LaTeX symbol.
3. **Add new particles** to the §1 tables *and* their PDG mass to `particle-masses.json` (or `non_orderable` when the token cannot be ordered); the validator rejects an unknown particle in a channel key.
4. **Verify the naming**: `name` is the bare symbol plus an optional `[condition]` or parameter tag; the transition is the `data` key. Use symbols only, never full expression definitions.
5. **Update the validator** when the new pattern needs a structural check (see json-meta.md §"Extending This Specification").
