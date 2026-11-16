# Channel Keys and Observable Naming

This document defines the naming conventions for all channel keys and observables in the flav-data database. It is the authoritative reference for constructing the observable `name` and the channel keys in JSON entries.

## 1. Channel Keys: `.2.` Transitions

Every decay or scattering process is a channel key: registered pids joined
by `.`, with `.2.` marking the arrow. The pid spelling, the registry, and
the antiparticle rules live in `particle-naming.md`; this section only
fixes how pids are joined and ordered.

### 1.1 Ordering rules

1. **Separator `.2.`** — `A.B.2.C.D` is $A+B\to C+D$; the marker always
   splits the initial from the final state. Cascades repeat it:
   `uud_I1?_1+n_0.uud_I1?_1+n_0.2.WB_I??_1??_0.2.mu_I??_1+n_0.VMU_I??_1+n_0`
   is $pp\to W^-\to\mu^-\bar\nu_\mu$.
2. **Particle type** — within each state, write
   **baryon → meson → charged lepton → neutral lepton**. A lighter baryon
   still precedes a heavier meson; the four ranks are absolute.
3. **Mass within a type** — same-type pids go **heaviest → lightest**,
   using the registry masses in `particle-naming.md`.
4. **Charge for equal masses** — same-type pids of equal mass go
   **`+` → `-` → `0`**. Mass ordering takes precedence, so charge only
   breaks ties: `E_I??_1+n_0.e_I??_1+n_0` ($e^+e^-$).
5. **Ratios and differences** — an observable comparing two transitions
   joins the two **full** keys with `/`; each side is ordered
   independently. There is no shared-part key: `l+`/`l-` is only for a
   single lepton-averaged transition, never for a comparison.
6. **`no-transition`** — the only key without `.2.`, for observables that
   involve no process.
7. **Vacuum final state** — a quantity whose final state has no hadron
   (a decay constant) writes the vacuum as `0`, e.g.
   `Db_I1?_0-n_0.2.0` is $\bar B^0\to$ vacuum. `0` is its own stage and
   only the last one; `no-transition` stays reserved for intrinsic
   properties (masses, bag parameters) and other quantities without a
   channel.

The rules are enforced by `scripts/json-valid.py` against the registry:
an unregistered token, a non-canonical order, or a missing `.2.` is a
validation failure. The validator also checks the final-state physics —
the inclusive token must follow the parent's $b$ flavour and a charged
lepton must carry its matching neutrino (`particle-naming.md` §2.1, §2.7).
Ordering is skipped for non-orderable tokens — the
placeholders of `particle-naming.md` §2.7 (`l`, `v`, `q`, `Xs`, ...),
exotics without a registered mass (`particle-naming.md` §2.5), and
nuclei. Quarks, gauge bosons and the Higgs carry no type rank, so a state
mixing them with hadrons or leptons is only mass/charge-ordered within
each same-rank run. Use a placeholder for an inclusive state.

Several $D_0^*$ labels are one channel (`Dc_I1?_0+n_0`): an alternative
mass, a fit scenario, or a second pole belongs in the group `note`. The
key never encodes a mass label, a resonance decay, or a measurement
suffix.

### 1.2 Examples

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
| $R_{K^*}$ | `dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0/dB_I1?_0-n_0.2.dS_I1?_1-n_0.E_I??_1+n_0.e_I??_1+n_0` |

### 1.3 Form-factor transitions (theory data)

A form factor belongs to one hadron transition, $A\to B$; every other
final-state particle is a spectator. Channel keys under `theo-data/`
therefore name **only the hadrons**: drop the lepton pair (or neutrino
pair) of the measured decay, and keep every hadron of the final state.
A ratio keeps the hadron transitions on both sides.

| Form factors of | Key |
|-----------------|-----|
| $\bar B\to D^*$ | `Db_I1?_0-n_0.2.Dc_I1?_1-n_0` |
| $\bar B\to D$ | `Db_I1?_0-n_0.2.Dc_I1?_0-n_0` |
| $\bar B\to \pi$ | `Db_I1?_0-n_0.2.uD_I2-_0-n_0` |
| $\bar B_s\to \phi$ | `sB_I0?_0-n_0.2.qQ_I0-_1--_1` |
| $\Lambda_b\to\Lambda_c$ | `udb_I0?_1+n_0.2.udc_I0?_1+n_0` |
| $\bar B^0\to$ vacuum (a decay constant) | `Db_I1?_0-n_0.2.0` |

Experimental groups keep the full process, because the measured rate is
tied to one lepton mode. A hadron with no hadronic final state (a decay
constant) ends in the vacuum `0` (§1.1 rule 7), and a ratio of decay
constants keeps `.2.0` on both sides. Intrinsic properties and
quantities with no channel (masses, bag parameters, HQET functions) stay
under `no-transition`. The validator enforces the rule for files under
`theo-data/`.

## 2. Observable Naming: `OBS` / `OBS[condition]`

Every measured quantity is named by its observable symbol only. The
transition is the enclosing `data` key (Section 1), so `name` must not
repeat it:

- **OBS**: a symbolic abbreviation representing the physical observable (see §3 for the full abbreviation table). Use only symbols — never write full expression definitions.
- **condition**: an optional qualifier in square brackets. It may name the
  two sides of a comparison (`[mu/e]`, `[mu-e]`, `[pi/K]`), a confidence
  level (`[90%@CL]`), a model or parameter point (`[composite_SSM]`,
  `[k_Mpl_0.01]`), a data set (`[13TeV]`, `[World.Average]`) or a fitting
  prescription (`[bayes]`). It must **never** carry a kinematic bin or
  threshold: q² ranges go to `q2min`/`q2max`, lepton-energy thresholds to
  `emin`/`emax`, and any other window (a $K\pi$ mass range, say) to the
  group `note`. The validator rejects `<`, `>`, `q2`, and bare numeric
  ranges or pairs inside a condition.
- **parameter tags**: optional parentheses for non-transition qualifiers, e.g. `Vcb(CLN)`, `R1(CLN)`, `f+.Vcs`. A transition inside parentheses is invalid.

Examples: `FL`, `Br`, `dBr/dq2`, `DeltaP6p[mu-e]`, `R`, `RBr[pi/K]`, `Vcb(CLN)`.

### 2.1 Basic Observables (No Transition)

**Basic observables** describe intrinsic particle properties — they do not involve a decay or scattering process. The naming format is `OBS(particle)` and the `data` key is `no-transition`:

| Observable | LaTeX | Symbol | Notes |
|------------|-------|--------|-------|
| Mass $M_t$ | $M_f$ | `Mass(t)` | On-shell mass |
| Mass $M_Z$ | $M_Z$ | `Mass(Z)` | On-shell mass of a resonance |
| $\overline{\text{MS}}$ mass $m_t$ | $m_t$ | `mass(t)` | Running mass |
| Lifetime $\tau_{e^-}$ | $\tau_f$ | `Tau(e-)` | Particle lifetime |
| Width $\Gamma_Z$ | $\Gamma_f$ | `Gamma(Z)` | Total decay width |

The argument is the **PDG particle label** (`t`, `Z`, `W`, `H`, `B0`,
`Bs0`, `BsL0`, `BsH0`, `Bc+`, `Lambdab0`, `pi+`, `K*`, `mu`, `e-`, ...),
not a pid — the registry spelling is only for channel keys. An isospin or
charge average uses one label (`Mass(K*)`, `Tau(Bs0)`) and records the
averaging in the group `note`. Single-token shortcuts (`MZ`, `MW`,
`Mtop`, `MH`, `Mh`) are rejected; write `Mass(Z)`, `Mass(W)`, `Mass(t)`,
`Mass(H)`.

**Bare names** (no transition) — `GF`, `alphas(MZ)`, `lambda`, `A`,
`rhobar`, `etabar`, `gammaCKM`, `r`, `delta`, `|Vtd|`, `|Vts|`, `|Vub|`,
`|Vcb|`, `R_b`, `R_c`, `S_phigamma`, `C_phigamma`, `ADelta_phigamma`,
`fs/fd`, `ge/gmu`, `ge/gtau`, and the running quark masses `mu`, `md`,
`ms`, `mc`, `mb`, `mud`, `ms/mud`. Meanings and LaTeX are in the §3
tables (CKM Parameters, Electroweak and Other Pseudo-Observables, Bare
Ratios, Decay Constants and Quark Masses).

### 2.2 Decay and Scattering Observables

Decay or scattering observables use the same bare symbol; the process is
the `data` channel key (§1).

#### 2.2.1 Single-Transition Observables

For observables measuring a single process, no condition is needed:

| Observable | LaTeX | Symbol | Data key |
|------------|-------|--------|----------|
| Branching fraction $\mathcal{B}(B^0 \to e^+ e^-)$ | $\mathcal{B}$ | `Br` | `dB_I1?_0-n_0.2.E_I??_1+n_0.e_I??_1+n_0` |
| Decay width $\Gamma(K^{*0} \to K^+ \pi^-)$ | $\Gamma$ | `Gamma` | `dS_I1?_1-n_0.2.uS_I1?_0-n_0.Ud_I2-_0-n_0` |
| Differential branching fraction | $d\mathcal{B}/dq^2$ | `dBr/dq2` | `dB_I1?_0-n_0.2.XsBar.ph_I??_1--_0` |
| Cross section $\sigma(pp \to e^+ e^-)$ | $\sigma(pp \to e^+ e^-)$ | `Sigma` | `uud_I1?_1+n_0.uud_I1?_1+n_0.2.E_I??_1+n_0.e_I??_1+n_0` |
| Charge asymmetry $A_C(B^+ \to J/\psi K^+)$ | $A_C(B^+ \to J/\psi K^+)$ | `AC` | `uB_I1?_0-n_0.2.cC_I0-_1--_0.uS_I1?_0-n_0` |
| Mass difference $\Delta M_s$ | $\Delta M_s$ | `DeltaMass` | `sB_I0?_0-n_0.2.Sb_I0?_0-n_0` |
| Decay fraction $f(Z \to \mu^+ \mu^-)$ | $f(Z \to \mu^+ \mu^-)$ | `f` | `Z_I??_1??_0.2.MU_I??_1+n_0.mu_I??_1+n_0` |

#### 2.2.2 Multi-Transition Observables

For observables comparing two transitions (lepton-flavour universality
tests, hadron-mode ratios, CP-asymmetry differences):

- The **data key** is the two full transitions joined by `/`, numerator
  (or minuend) first. A `/` key is still **one** channel, so a correlation
  matrix spanning several comparisons keeps its dimensions.
- Each side spells out its own leptons. `l+`/`l-`/`l` and `q`/`qBar` are
  placeholders for a genuinely averaged single transition, never a way to
  shorten a comparison. Neutrinos are not placeholders when the flavour is
  known: `ve_I??_1+n_0`, `vmu_I??_1+n_0` and `vtau_I??_1+n_0` (antiparticles
  swap the case) carry mass 0 in the registry and sort as neutral leptons;
  only the generic `v`/`vBar` is non-orderable. Numbered placeholders
  (`q1`, `l1`, `v1`, `h1`) are not registered and are rejected.
- **condition** encodes the flavour mapping, e.g. `[mu/e]` means the muon
  mode over the electron mode.
  - **`/` (slash)** in condition → ratio: `R` for an LFU ratio, otherwise
    `ROBS[condition]` such as `RBr[pi/K]`.
  - **`-` (dash)** in condition → `Delta` difference: `DeltaACP[mu-e]` = $A_{CP}(B^-\to\mu^- \bar{\nu}) - A_{CP}(B^-\to e^-\bar{\nu})$.

| Observable | Symbol | Data key |
|------------|--------|----------|
| $R_{K^*}$ | `R` | `dB_I1?_0-n_0.2.dS_I1?_1-n_0.MU_I??_1+n_0.mu_I??_1+n_0/dB_I1?_0-n_0.2.dS_I1?_1-n_0.E_I??_1+n_0.e_I??_1+n_0` |
| $R_K$ | `R` | `uB_I1?_0-n_0.2.uS_I1?_0-n_0.MU_I??_1+n_0.mu_I??_1+n_0/uB_I1?_0-n_0.2.uS_I1?_0-n_0.E_I??_1+n_0.e_I??_1+n_0` |
| $R(D)$ | `R` | `Db_I1?_0-n_0.2.Dc_I1?_0-n_0.tau_I??_1+n_0.vBar/Db_I1?_0-n_0.2.Dc_I1?_0-n_0.l-.vBar` |
| $\Delta A_{CP} = A_{CP}(\mu) - A_{CP}(e)$ | `DeltaACP[mu-e]` | `Ub_I1?_0-n_0.2.mu_I??_1+n_0.VMU_I??_1+n_0/Ub_I1?_0-n_0.2.e_I??_1+n_0.VE_I??_1+n_0` |

Amplitude ratios that the source quotes as one parameter (`r`, `delta` in
$B \to DK$) and form-factor ratios (`R1`, `R2`, `r1`, `r2`) stay under the
single channel they parametrize; they are not `/` pairs.

**CKM parameters**: $r$ and $\delta$ are defined via $B^-$ decay amplitude ratios ($b \to u$ suppressed relative to $b \to c$ favored). The B meson and final-state meson in the transition must carry **negative charge**: `Ub_I1?_0-n_0.2.Uc_I1?_0-n_0.Us_I1?_0-n_0`, `Ub_I1?_0-n_0.2.Uc_I1?_0-n_0.Ud_I2-_0-n_0` (canonical order: mesons heaviest to lightest, so `Uc` before `Us`/`Ud`).

### 2.3 Observable Differences and Ratios (Unified Convention)

Unless otherwise specified, differences and ratios between observables follow these patterns:

| Type | Symbol | LaTeX | Example |
|------|--------|-------|---------|
| Difference | `DeltaOBS[condition]` | $\Delta_{OBS}^{condition}$ | `DeltaBr[mu-e]` |
| Ratio | `ROBS[condition]` | $R_{OBS}^{condition}$ | `RFL[mu/e]` |
| LFU ratio | `R` | $R(X)$ | `R` |

The canonical LFU ratio $R(X)=\mathcal{B}(B\to X\tau\nu)/\mathcal{B}(B\to X\ell\nu)$ is the **bare symbol `R`**: the `/` channel key already fixes both the final state $X$ and the two lepton modes, so the name repeats neither (no `RD`, `RD*`, `RK`, `RK*`, `Rmue`). The same holds for any ratio whose two sides differ only by lepton flavour, including $R_{K^{(*)}}$. Ratios that compare other observables keep `ROBS[condition]` (e.g. `RBr[pi/K]`, `RFL[mu/e]`). The validator rejects a channel-bearing ratio symbol, and rejects a lepton-flavour condition on any symbol that is not `R`, `DeltaOBS`, or `ROBS` with a non-rate observable (`RBr[mu/e]` and `FL[mu/e]` fail; `RFL[mu/e]` passes).

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
| `A2` | $A_2$ |
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
| `V1` | CLN-basis helicity amplitude $V_1$ ($\bar B \to D^{(*)}$) |
| `S1` | CLN-basis helicity amplitude $S_1$ ($\bar B \to D$) |
| `A5` | CLN-basis helicity amplitude $A_5$ ($\bar B \to D^*$) |
| `V4` | CLN-basis helicity amplitude $V_4$ ($\bar B \to D^*$) |
| `P1` | CLN-basis helicity amplitude $P_1$ ($\bar B \to D^*$) |

For a BGL $z$-series fit of the $\bar B_{(s)} \to D_{(s)}^{(*)}
\ell\bar\nu_\ell$ form factors, the basis is $f_+, f_0$ for the
pseudoscalar channel and $g, f, F_1, F_2$ for the vector channel, so the
coefficients are named `aN_f+`, `aN_f0`, `aN_g`, `aN_f`, `aN_F1`,
`aN_F2` (e.g. `a0_f+`, `a2_F1`).

A fit that instead expands the CLN-basis helicity amplitudes,
$F_i(w)=p_i(w)/[B_i(z)\varphi_i(z)]\sum_n a_n z^n$, uses the same `aN_FF`
form with `V1`/`S1` for $\bar B \to D$ and `A1`, `A5`, `V4`, `P1` for
$\bar B \to D^*$ (e.g. `a0_A1`, `a1_V4`). These symbols collide with the
bare angular-observable tokens `S1`, `A5`, `P1` of the §3 table; only the
`aN_` prefix marks the coefficient. A normalisation related to another
one by a fixed kinematic or heavy-quark identity (such as
$a_0^{A_5}=0.1675\,a_0^{A_1}$) is not stored; the group `note` records
the relation.

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

### 2.5 Zero-Recoil Form-Factor Normalization: `hA1(1)`, `G(1)`

The zero-recoil normalization of the $\bar B \to D^*$ axial form factor is
written `hA1(1)`:
$h_{A_1}(1)=(M_B+M_{D^*})A_1(q^2_\mathrm{max})/(2\sqrt{M_BM_{D^*}})$.
The transition key selects the channel: `Db_I1?_0-n_0.2.Dc_I1?_1-n_0.l-.vBar` carries
$h_{A_1}(1)$ and `Sb_I0?_0-n_0.2.Sc_I0?_0-n_0.l-.vBar` carries the $B_s$ value
$h^s_{A_1}(1)$. The parenthetical `(1)` is a parameter tag, not a
multi-transition condition. This symbol names a form-factor value, not an
expansion coefficient, so the group does not need `scheme`.

A Caprini-Lellouch-Neubert (CLN) fit of the same channel returns the slope
`rho2(CLN)` and the zero-recoil ratios `R1(CLN)`, `R2(CLN)` together with
`hA1(1)`. Store only the parameters the paper itself determines; a
normalization or ratio fixed to a lattice or HQET input goes in the group
`note`. CLN is a parameterization of $h_{A_1}(w)$ and $R_{1,2}(w)$, not a
$z$-expansion basis, so such a group carries no `scheme`.

The pseudoscalar channel $\bar B_{(s)}\to D_{(s)}\ell\bar\nu$ has the
analogous normalization `G(1)`, the zero-recoil value of the HQET
combination ${\cal G}(w)\propto f_+(q^2)$. The transition key separates
$B_s\to D_s$ (`Sb_I0?_0-n_0.2.Sc_I0?_0-n_0.l-.vBar`) from $B\to D$, and the
`note` records the lattice action and the continuum extrapolation. As for
`hA1(1)`, the value carries no `scheme`.

### 2.6 Form-Factor Values at Fixed `q2`

A form-factor value at a fixed momentum transfer uses the bare symbol from
the table in §2.4 (`V`, `A0`, `A1`, `A2`, `A12`, `f+`, `f-`, ...), not the
`aN_FF` coefficient form. Each `obs@N` sets `q2min` and `q2max` to the same
value when the source quotes a point, so repeated symbols at different
`q2` stay distinguishable; a value group carries no `scheme`. The group
`note` records how the values were obtained (fit, sum rule, ...) and
whether correlations were published.

### 2.7 Zero-Recoil Sum-Rule Integrals: `I0A`, `I0V`

A zero-recoil OPE sum rule bounds a form-factor combination from above
through the dimensionless integrals $I_{0,A}$ and $I_{0,V}$, written
`I0A` and `I0V`. The transition key selects the channel, and the group
`note` records the scale $\epsilon_M=\mu$ and which combination each
integral bounds; no `scheme` is needed because these are sum-rule
integrals, not expansion coefficients.

### 2.8 HQET Universal Form Factors: `chi_2`, `chi_3`, `eta`, `Sigma_1`, `a0Sigma_2`

The spin-symmetry-violating HQET functions $\chi_2(v\cdot v')$ and
$\chi_3(v\cdot v')$, which enter the $1/m_Q$ expansion through the
chromo-magnetic operator, are written `chi_2` and `chi_3`. They are
universal — independent of the heavy meson and of the decay — and belong
to neither the helicity set nor the HQET-basis set of §2.4, so the
`data` key is `no-transition`. The argument is a parameter tag, as for
`hA1(1)`: `chi_2(1)` is the zero-recoil value, `chi_2(1.3)` a point at
$v\cdot v'=1.3$. These are form-factor values, not expansion
coefficients, so the group carries no `scheme`; the `note` records the
method and its inputs. The leading Isgur-Wise function $\xi(y)$, which is
normalized to unity at zero recoil, is not stored. When a paper publishes
the functions only graphically, the group keeps an empty `no-transition`
channel and a `note` saying so (`json-meta.md` §"Data Entries").

The ratio $\eta\equiv\xi_3(v\cdot v',\mu)/\xi(v\cdot v',\mu)$ of the
subleading $\xi_3$ to the leading Isgur-Wise function is written `eta`.
It is renormalization-group invariant, so it takes neither a `scheme` nor
a parameter tag: when a source quotes a single value valid over a recoil
range, the group stores one `eta` and the `note` records that range and
that $\xi_3$ itself is not stored. `eta` is not the CKM parameter
`etabar`.

The leading and subleading universal form factors of a heavy-to-heavy
doublet in the HQET trace formalism, $\Sigma_1(w)$ and
$a_0\Sigma_2(w)$, are written `Sigma_1` and `a0Sigma_2`. The product is
stored as one symbol because the source fits and tabulates $a_0\Sigma_2$
itself rather than separating the Bohr radius $a_0$ from $\Sigma_2$:
`Sigma_1` is dimensionless and `a0Sigma_2` carries
`unit: "GeV-1"`. Taylor coefficients around zero recoil mark the
derivative order with apostrophes — `Sigma_1'(1)`, `Sigma_1''(1)`,
`a0Sigma_2'(1)`, `a0Sigma_2''(1)` — with the parameter tag `(1)` naming
the expansion point $w=1$, as for `chi_2(1)`. Because the expansion is
$\Sigma_i(w)=\Sigma_i(1)+\Sigma_i'(w-1)+\tfrac12\Sigma_i''(w-1)^2$,
`Sigma_i''(1)` is the second derivative, not the coefficient of
$(w-1)^2$. These functions are universal within the doublet, so the
`data` key is `no-transition`; the group `note` records which transition
they belong to and what the fit used, and the group carries no `scheme`.

## 3. Observable Abbreviations

The tables below are reference only; the JSON has no category layer
(json-meta.md §"Data Entries").

### Branching Fractions and Decay Widths

| Abbr | LaTeX | Paper Notation | Description |
|------|-------|---------------|-------------|
| `Br` | $\mathcal{B}$ | $\mathcal{B}$ | Branching fraction |
| `dBr/dq2` | $d\mathcal{B}/dq^2$ | $d\mathcal{B}/dq^2$ | Differential branching fraction |
| `Gamma` | $\Gamma$ | $\Gamma$ | Decay width (partial or total) |
| `dGamma/dq2` | $d\Gamma/dq^2$ | $d\Gamma/dq^2$ | Differential decay width |

### Lifetimes

| Abbr | LaTeX | Paper Notation | Description |
|------|-------|---------------|-------------|
| `Tau` | $\tau$ | $\tau$ | Particle lifetime |

### Masses and Mixing Parameters

| Abbr | LaTeX | Paper Notation | Description |
|------|-------|---------------|-------------|
| `Mass` | $M_f$ | $M$ | On-shell mass (uppercase). Written as `Mass(f)` with the PDG particle label $f$ (§2.1). |
| `mass` | $m$ | $m$ | $\overline{\text{MS}}$ mass (lowercase), written `mass(f)` |
| `DeltaMass` | $\Delta M$ | $\Delta M_s$, $\Delta M_d$ | Mass difference / neutral meson mixing parameter |
| `DeltaGamma` | $\Delta\Gamma$ | $\Delta\Gamma_s$, $\Delta\Gamma_d$ | Decay width difference / neutral meson mixing parameter |

### Scattering Cross Sections

| Abbr | LaTeX | Paper Notation | Description |
|------|-------|---------------|-------------|
| `Sigma` | $\sigma$ | $\sigma$ | Total or fiducial cross section |
| `dSigma/dpT` | $d\sigma/dp_T$ | $d\sigma/dp_T$ | Differential cross section (transverse momentum) |
| `dSigma/deta` | $d\sigma/d\eta$ | $d\sigma/d\eta$ | Differential cross section (pseudorapidity) |

### Angular Coefficients (CP-averaged)

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
| `R` | $R$ | $R_X$, $R_{K^{(*)}}$ | LFU ratio, written bare `R`; see §2.3. |
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
| `A` | $A_f$ | $A_e$, $A_b$, $\mathcal{A}_f$ | $Z$-pole asymmetry parameter; the channel key selects $f$ (`Z_I??_1??_0.2.b_I??_1+n_0.B_I??_1+n_0` for $A_b$). Under `no-transition` it is the Wolfenstein parameter instead — see **CKM Parameters**. |
| `AFB0` | $A_{FB}^{0,f}$ | $A_{FB}^{0,\ell}$, $A_{FB}^{0,b}$ | Pole forward-backward asymmetry; the channel key selects $f$ (`Z_I??_1??_0.2.b_I??_1+n_0.B_I??_1+n_0` for $A_{FB}^{0,b}$) |
| `GF` | $G_F$ | $G_F$ | Fermi constant |
| `alphas` | $\alpha_s$ | $\alpha_s(M_Z)$ | Strong coupling; the scale goes in a parameter tag, `alphas(MZ)` |
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
| `lambda` | $\lambda$ | $\lambda$ | Wolfenstein parameter (bare, `no-transition`) |
| `A` | $A$ | $A$ | Wolfenstein parameter (bare, `no-transition`) |
| `rhobar` | $\bar{\rho}$ | $\bar{\rho}$ | Wolfenstein parameter (bare, `no-transition`) |
| `etabar` | $\bar{\eta}$ | $\bar{\eta}$ | Wolfenstein parameter (bare, `no-transition`) |
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
group-level `note`, not in the name. They use the bare symbols below
rather than the generic `mass(f)` form.

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
| `mu` | $m_u$ | $m_u$ | Up-quark mass |
| `md` | $m_d$ | $m_d$ | Down-quark mass |
| `mud` | $m_{ud}$ | $m_{ud}$ | Average light-quark mass, $m_{ud}=(m_u+m_d)/2$ |
| `ms` | $m_s$ | $m_s$ | Strange-quark mass |
| `mc` | $m_c$ | $m_c$ | Charm-quark mass |
| `mb` | $m_b$ | $m_b$ | Bottom-quark mass |
| `ms/mud` | $m_s/m_{ud}$ | $m_s/m_{ud}$ | Quark-mass ratio |
| `BK` | $B_K$ | $B_K$ | Kaon bag parameter |
| `BhatK` | $\hat{B}_K$ | $\hat{B}_K$ | Renormalization-group-invariant kaon bag parameter |
| `BBs/BBd` | $B_{B_s}/B_{B_d}$ | $B_{B_s}/B_{B_d}$ | Bag-parameter ratio |

## 4. LaTeX Notation

The §3 tables list each abbreviation's LaTeX symbol (column "LaTeX") and
the notation papers typically use (column "Paper Notation") — a reference
for papers and plots only. JSON data stores no LaTeX for transitions or
observables; the escaping rule for `title`/`abstract` is in `json-meta.md`
§"Key Constraints".

## 5. Adding New Observables

When a paper introduces an observable not listed in this document:

1. **Confirm the physical meaning** and identify the standard notation used in the literature.
2. **Choose or create an abbreviation** following §2 and add it to the matching §3 table with its LaTeX symbol.
3. **Add new particles** to the registry in `particle-naming.md` with their pid, mass, and width (or mark exotic states as non-orderable); the validator rejects an unregistered pid in a channel key.
4. **Verify the naming**: `name` is the bare symbol plus an optional `[condition]` or parameter tag; the transition is the `data` key. Use symbols only, never full expression definitions.
5. **Update the validator** when the new pattern needs a structural check (see json-meta.md §"Extending This Specification").
