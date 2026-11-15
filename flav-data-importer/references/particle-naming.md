# Particle Naming and Registry

This document defines the internal particle identity (`pid`) and registers
every state used by the database. The pids are the spelling used in the
JSON transition keys. The registry tables are also the validator's mass
source, so a new state is added here, never in a script.

## 1. Grammar

```
pid      := particle | nucleus
particle := core "_" ig "_" jpc "_" serial
core     := fundamental | content | "qQ" | "x"
ig       := "I" <2I> <G>
jpc      := <2J><P><C>
serial   := "0" | [1-9][0-9]*
nucleus  := "n~Z~A[~L~I]"
```

1. A particle is a pole. The quantum numbers fix the channel, the serial
   separates poles inside it, and mass and width never enter the pid.
2. A registered pid is immutable and never reused. A `?` stays in the pid
   even after the quantum number is measured.
3. A pid contains no `.`, `/`, `*`, `+`/`-` (outside `ig` and `jpc`),
   spaces or `Bar`; nuclei use `~`. The placeholders of §2.7 are the only
   non-pid tokens.
4. A channel joins pids with `.` and the arrow marker `.2.`:

```
dB_I1?_0-n_0.2.dC_I1?_0-n_0.E_I??_1+n_0.ve_I??_1+n_0
```

which reads $B^0 \to D^- e^+ \nu_e$.

### 1.1 `jpc`

Three characters: $2J$, $P$, $C$.

- **$2J$**: `0`–`4`, `6`, `8` (even for bosons, odd for fermions), or `?`.
- **$P$**: `+`, `-`, or `?`.
- **$C$**: `+`, `-`, `n`, or `?`. `n` means *not defined*: all fermions,
  all charged states, and neutral states that are not $C$ eigenstates
  ($K^0$, $D^0$, $K_S^0$, $K_L^0$). `+`/`-` is used only for neutral
  $C$ eigenstates ($\pi^0$, $\eta$, $\rho^0$, $\omega$, $\phi$, $J/\psi$,
  $\gamma$, g).
- **`?` is frozen**: it is used only when neither measurement nor the PDG
  review assigns the quantum number ($W/Z$ parity and charge parity, most
  BSM states).

### 1.2 `ig`

`<ig>` is $I^G$, written `I<2I><G>` — doubled isospin and G parity, with
no `G` letter.

- **$2I$**: twice the isospin (`0`, `1`, `2`, ...), or `?` when the
  isospin is unknown or is not a quantum number of the state.
- **$G$**: `+` or `-`; `?` when G parity is not defined or not measured.
  G parity exists only for a meson multiplet that is its own antiparticle
  (integer $I$): $\pi$, $\rho$, $\eta$, $\eta'$, $\omega$, $\phi$,
  $J/\psi$, $\psi(2S)$. It is not defined for $K$, heavy mesons, baryons,
  leptons, quarks or gauge bosons, and is unknown for most BSM states.
- `I??` marks a state with neither a known isospin nor G parity:
  fundamental states, $Z$, $H$ and most exotics.

Examples: `I2-` ($\pi$, $G=-$), `I2+` ($\rho$, $G=+$), `I0+` ($\eta$),
`I0-` ($\omega$), `I1?` ($K$, $D$, p), `I??` ($e^-$, $Z'$).

### 1.3 `serial`

- Mandatory; fundamental states always use `0`.
- Within one `(core, ig, jpc)` class, `0` is the lightest **registered**
  state and serials increase with mass; include the ground state even when
  it is not otherwise used ($\eta$ is registered because $\eta'$ is).
  Equal masses are ordered by shorter lifetime first ($K_S^0$ = 0,
  $K_L^0$ = 1).
- Serials are dense. Adding a lighter state renumbers the class; old pids
  stay valid as aliases and are never reused. A mass scan, fit scenario or
  alternative pole mass is a `note`, not a new serial: the three
  $D_0^*$ labels share `Dc_I1?_0+n_0`. An antiparticle shares the serial
  of its particle.

### 1.4 Antiparticles

| state | rule |
|---|---|
| quarks, leptons, flavored hadrons | case swap in place (`uD`/`Ud`, `dB`/`Db`) |
| $W^\pm$ | `W`/`WB` (the only non-case-swap pair) |
| $Z$, $\gamma$, g, $H$ | self-conjugate, one pid |
| $\pi^0$, $\eta$, $\eta'$, $\rho^0$, $\omega$, $\phi$, $J/\psi$, $\psi(2S)$ | self-conjugate, one pid |
| $K_S^0$, $K_L^0$ | self-conjugate, one pid each |
| `x` states | charge-specific rows |
| nuclei | no antiparticle entry |

## 2. Core

### 2.1 Fundamental states

The core of a fundamental state is fixed; charge and antiparticle are part
of the core. The table is closed: a new fundamental state requires an
extension of this document. All fundamental fermions use
`<core>_I??_1+n_0`. Masses and widths are in GeV; `—` means PDG gives no
value.

| pid | antiparticle pid | Q | mass | width |
|---|---|---|---|---|
| `u_I??_1+n_0` | `U_I??_1+n_0` | $+2/3$ | 0.00216 | — |
| `d_I??_1+n_0` | `D_I??_1+n_0` | $-1/3$ | 0.0047 | — |
| `s_I??_1+n_0` | `S_I??_1+n_0` | $-1/3$ | 0.0929 | — |
| `c_I??_1+n_0` | `C_I??_1+n_0` | $+2/3$ | 1.273 | — |
| `b_I??_1+n_0` | `B_I??_1+n_0` | $-1/3$ | 4.186 | — |
| `t_I??_1+n_0` | `T_I??_1+n_0` | $+2/3$ | 172.6 | 1.42 |
| `e_I??_1+n_0` | `E_I??_1+n_0` | $-1$ | 0.00051099895069 | 0 |
| `mu_I??_1+n_0` | `MU_I??_1+n_0` | $-1$ | 0.1056583755 | 2.9959847e-19 |
| `tau_I??_1+n_0` | `TAU_I??_1+n_0` | $-1$ | 1.77693 | 2.265e-12 |
| `ve_I??_1+n_0` | `VE_I??_1+n_0` | $0$ | 0 | 0 |
| `vmu_I??_1+n_0` | `VMU_I??_1+n_0` | $0$ | 0 | 0 |
| `vtau_I??_1+n_0` | `VTAU_I??_1+n_0` | $0$ | 0 | 0 |
| `ph_I??_1--_0` | `ph_I??_1--_0` | $0$ | 0 | 0 |
| `g_I??_1--_0` | `g_I??_1--_0` | $0$ | 0 | 0 |
| `W_I??_1??_0` | `WB_I??_1??_0` | $+1$ | 80.362 | 2.14 |
| `Z_I??_1??_0` | `Z_I??_1??_0` | $0$ | 91.1879 | 2.4955 |
| `H_I??_0++_0` | `H_I??_0++_0` | $0$ | 125.13 | 0.003 |

Quark masses are scheme-dependent and neutrino masses are below the quoted
sensitivity; the `0` in that column only fixes the ordering. A width of
`0` marks a stable state or a width below the PDG sensitivity.

A charged lepton fixes its neutrino: $\ell^-$ goes with an antineutrino
(`VE`/`VMU`/`VTAU`, or generic `vBar`), $\ell^+$ with a neutrino
(`ve`/`vmu`/`vtau`, or `v`), and the flavour must match. The validator
checks the final state of every transition; scattering (a neutrino
already in the initial state), exotic `x_` cascades and the ambiguous
`l` are exempt.

### 2.2 Content hadrons

Valence quarks are written in **increasing quark mass**
(`u < d < s < c < b < t`): lowercase is a quark, uppercase an antiquark.
The position depends on flavor only, not on which state is the particle;
for equal flavor the quark precedes its antiquark (`cC` for $J/\psi$).
The letter count is the quark number: 2 = meson, 3 = baryon; 4 or 5 only
when the content is established, otherwise use `x` (§2.5). Examples:
`uD` ($\pi^+$), `dS` ($K^0$), `Dc` ($D^+$), `dB` ($B^0$).

Baryons write the valence content only; the isospin is carried by `<ig>`
(§2.4): `uud_I1?_1+n_0` (p), `uds_I0?_1+n_0` ($\Lambda$),
`udc_I0?_1+n_0` ($\Lambda_c^+$). The antiparticle swaps the case of every
letter in place, so the mass order does not change: `uD`↔`Ud`, `Dc`↔`dC`,
`uud`↔`UUD`.

### 2.3 Mixed cores

A state that is not a single flavor eigenstate uses the literal core
`qQ`: $\pi^0$, $\rho^0$, $\eta$, $\eta'$, $\omega$, $\phi$, $K_S^0$ and
$K_L^0$. The same core is reused across channels; `ig`, `jpc` and the
serial keep the pids apart, e.g. `qQ_I2-_0-+_0` ($\pi^0$),
`qQ_I1?_0-n_0` ($K_S^0$) and `qQ_I1?_0-n_1` ($K_L^0$).

### 2.4 Baryon isospin

The valence content does not fix the isospin; `<ig>` does. $\Lambda$ and
$\Sigma^0$ share content and spin ($uds$, $1/2^+$) but differ in
isospin, so they become `uds_I0?_1+n_0` and `uds_I2?_1+n_0`. The serial
class is `(core, ig, jpc)`, so the residual $\Xi_c/\Xi_c'$ degeneracy
(both `usc`, `I1?`) is absorbed by the serial: `usc_I1?_1+n_0` and
`usc_I1?_1+n_1`.

### 2.5 Exotic states

A state with no conventional content assignment uses the literal core
`x`. It is charge-specific: a charged exotic and its antiparticle are
separate rows, ordered by mass (or first registration when unknown).
These pids carry no mass and are not order-checked.

| pid | PDG | $J^{PC}$ |
|---|---|---|
| `x_I0+_1++_0` | $X(3872)^0$ | $1^{++}$ |
| `x_I1?_??n_0` | $P_c(4312)^+$ | ? |
| `x_I??_1??_0` | $Z'$ | $1$ |
| `x_I??_1?n_0` | $W'^+$ | $1$ |
| `x_I??_1?n_1` | $W_{KK}^+$ | $1$ |
| `x_I??_2??_0` | $G^*$ | $2$ |
| `x_I??_0??_0` | sneutrino | $0$ |
| `x_I??_???_0` | mediator | ? |

PDG lists $X(3872)$ as $\chi_{c1}(3872)$ with content `cC`, but its
internal structure is unresolved, so it uses `x`.

### 2.6 Nuclei

Nuclei are not particles and use a `~` namespace that cannot collide with
a pid: `n~Z~A` or `n~Z~A~L~I`. Masses are atomic masses in GeV from
`nuclei2026.csv`; the width column is `—` because nuclear widths are not
registered.

| pid | PDG | mass | width |
|---|---|---|---|
| `n~20~40` | $^{40}$Ca | 37.224917747 | — |
| `n~22~48` | $^{48}$Ti | 44.6632240289 | — |
| `n~79~197` | $^{197}$Au | 183.4731986778 | — |

### 2.7 Non-particle tokens

These placeholders are the only tokens that are not pids. They are never
order-checked and are not registered in any other table.

| token | meaning |
|---|---|
| `l`, `l+`, `l-`; `v`, `vBar` | generic lepton; generic neutrino |
| `q`, `qBar` | generic quark |
| `f`, `fBar`; `kappa` | generic fermion; coupling modifier |
| `B` | $B^+/B^0$ charge-averaged $B$ meson |
| `Xs`, `XsBar`; `Xc`, `XcBar`; `Xu` | inclusive strange, charm, up systems |
| `had`, `all`; `V`, `VH` | hadronic system; all final states; vector boson, $VH$ |
| `gg`, `gamma+gamma` | gluon/photon initial state |
| `no-transition` | observable without a transition |

An inclusive system is always its own token: $B^-\to X_c e^-\bar\nu_e$ is
`Ub_I1?_0-n_0.2.Xc.e_I??_1+n_0.vBar`, never a merged `Xce` that swallows the
charged lepton.

The inclusive token follows the parent's $b$ flavour, because $b\to c/s$
and $\bar b\to\bar c/\bar s$ produce conjugate systems:

| Parent | Quark | Inclusive token |
|---|---|---|
| `Ub`, `Db`, `Sb`, `Cb` ($B^-$, $\bar B^0$, $\bar B_s^0$, $B_c^-$) | $b$ | `Xc`, `Xs` |
| `uB`, `dB`, `sB`, `cB` ($B^+$, $B^0$, $B_s^0$, $B_c^+$) | $\bar b$ | `XcBar`, `XsBar` |

`Xu` has no barred variant and the charge-averaged `B` fixes no flavour;
both are exempt. The validator rejects a mismatch.

## 3. Registry

Masses and widths are PDG 2026 as bundled in `particle` 1.1.0
(`particle2026.csv`, version 17, 2026-10-26) and are in GeV. `—` means
PDG gives no value. $Q$ is the electric charge in units of $e$; the
validator uses it only to order equal-mass states.

### 3.1 Light mesons

| pid | PDG | Q | mass | width |
|---|---|---|---|---|
| `uD_I2-_0-n_0` | $\pi^+$ | $+1$ | 0.13957039 | 2.5284e-17 |
| `Ud_I2-_0-n_0` | $\pi^-$ | $-1$ | 0.13957039 | 2.5284e-17 |
| `qQ_I2-_0-+_0` | $\pi^0$ | $0$ | 0.1349768 | 7.81e-9 |
| `uS_I1?_0-n_0` | $K^+$ | $+1$ | 0.493677 | 5.317e-17 |
| `Us_I1?_0-n_0` | $K^-$ | $-1$ | 0.493677 | 5.317e-17 |
| `dS_I1?_0-n_0` | $K^0$ | $0$ | 0.497611 | — |
| `Ds_I1?_0-n_0` | $\bar K^0$ | $0$ | 0.497611 | — |
| `qQ_I1?_0-n_0` | $K_S^0$ | $0$ | 0.497611 | 7.3508e-15 |
| `qQ_I1?_0-n_1` | $K_L^0$ | $0$ | 0.497611 | 1.287e-17 |
| `uS_I1?_1-n_0` | $K^{*+}$ | $+1$ | 0.89188 | 0.0485 |
| `dS_I1?_1-n_0` | $K^{*0}$ | $0$ | 0.89556 | 0.0471 |
| `Ds_I1?_1-n_0` | $\bar K^{*0}$ | $0$ | 0.89556 | 0.0471 |
| `uD_I2+_1--_0` | $\rho^+$ | $+1$ | 0.77511 | 0.1491 |
| `Ud_I2+_1--_0` | $\rho^-$ | $-1$ | 0.77511 | 0.1491 |
| `qQ_I2+_1--_0` | $\rho^0$ | $0$ | 0.77526 | 0.1474 |
| `qQ_I0+_0-+_0` | $\eta$ | $0$ | 0.547862 | 1.31e-9 |
| `qQ_I0+_0-+_1` | $\eta'$ | $0$ | 0.95778 | 0.000188 |
| `qQ_I0-_1--_0` | $\omega$ | $0$ | 0.78266 | 0.00868 |
| `qQ_I0-_1--_1` | $\phi$ | $0$ | 1.01946 | 0.004249 |
| `cC_I0-_1--_0` | $J/\psi$ | $0$ | 3.0969 | 9.26e-5 |
| `cC_I0-_1--_1` | $\psi(2S)$ | $0$ | 3.686097 | 0.000293 |

$K_S^0$ and $K_L^0$ share the $K^0$ mass and differ only by width.

### 3.2 Heavy mesons

| pid | PDG | Q | mass | width |
|---|---|---|---|---|
| `Uc_I1?_0-n_0` | $D^0$ | $0$ | 1.86484 | 1.604e-12 |
| `uC_I1?_0-n_0` | $\bar D^0$ | $0$ | 1.86484 | 1.604e-12 |
| `Dc_I1?_0-n_0` | $D^+$ | $+1$ | 1.86966 | 6.37e-13 |
| `dC_I1?_0-n_0` | $D^-$ | $-1$ | 1.86966 | 6.37e-13 |
| `Uc_I1?_1-n_0` | $D^{*0}$ | $0$ | 2.00686 | 0.0021 |
| `uC_I1?_1-n_0` | $\bar D^{*0}$ | $0$ | 2.00686 | 0.0021 |
| `Dc_I1?_1-n_0` | $D^{*+}$ | $+1$ | 2.01027 | 8.34e-5 |
| `dC_I1?_1-n_0` | $D^{*-}$ | $-1$ | 2.01027 | 8.34e-5 |
| `Sc_I0?_0-n_0` | $D_s^+$ | $+1$ | 1.96835 | 1.313e-12 |
| `Sc_I0?_1-n_0` | $D_s^{*+}$ | $+1$ | 2.1122 | — |
| `Dc_I1?_0+n_0` | $D_0^*(2300)^+$ | $+1$ | 2.343 | 0.229 |
| `Sc_I0?_0+n_0` | $D_{s0}^*(2317)^+$ | $+1$ | 2.3178 | 0.010 |
| `uB_I1?_0-n_0` | $B^+$ | $+1$ | 5.27941 | 4.021e-13 |
| `Ub_I1?_0-n_0` | $B^-$ | $-1$ | 5.27941 | 4.021e-13 |
| `dB_I1?_0-n_0` | $B^0$ | $0$ | 5.27972 | 4.355e-13 |
| `Db_I1?_0-n_0` | $\bar B^0$ | $0$ | 5.27972 | 4.355e-13 |
| `sB_I0?_0-n_0` | $B_s^0$ | $0$ | 5.36693 | 4.345e-13 |
| `Sb_I0?_0-n_0` | $\bar B_s^0$ | $0$ | 5.36693 | 4.345e-13 |
| `cB_I0?_0-n_0` | $B_c^+$ | $+1$ | 6.27447 | 1.291e-12 |
| `Cb_I0?_0-n_0` | $B_c^-$ | $-1$ | 6.27447 | 1.291e-12 |

PDG leaves the $D_s^{*+}$ parity blank, so the registry uses the
established $1^-$ assignment. The three $D_0^*$ labels are scenarios of
the scalar `Dc` channel: 2343 and 2105 MeV are alternative ground-state
masses and 2451 MeV is the second pole of a two-resonance fit. They share
`Dc_I1?_0+n_0`; the scenario belongs in the group `note`.

### 3.3 Baryons

| pid | PDG | Q | mass | width |
|---|---|---|---|---|
| `uud_I1?_1+n_0` | p | $+1$ | 0.93827208943 | 0 |
| `UUD_I1?_1+n_0` | $\bar p$ | $-1$ | 0.93827208943 | 0 |
| `udd_I1?_1+n_0` | n | $0$ | 0.9395654219 | 7.494e-28 |
| `uds_I0?_1+n_0` | $\Lambda$ | $0$ | 1.115683 | 2.515e-15 |
| `uus_I2?_1+n_0` | $\Sigma^+$ | $+1$ | 1.18937 | 8.209e-15 |
| `uds_I0?_3-n_0` | $\Lambda(1520)$ | $0$ | 1.519 | 0.016 |
| `udc_I0?_1+n_0` | $\Lambda_c^+$ | $+1$ | 2.28646 | 3.248e-12 |
| `UDC_I0?_1+n_0` | $\bar\Lambda_c^-$ | $-1$ | 2.28646 | 3.248e-12 |
| `udc_I0?_1-n_0` | $\Lambda_c(2595)^+$ | $+1$ | 2.59225 | 0.0026 |
| `udc_I0?_3-n_0` | $\Lambda_c(2625)^+$ | $+1$ | 2.628 | — |
| `udb_I0?_1+n_0` | $\Lambda_b^0$ | $0$ | 5.61957 | 4.493e-13 |

Only the baryons present in the database are registered. $\Xi$, $\Omega$,
$\Xi_c$, $\Omega_c$ and $\Xi_b$ are absent because no JSON entry uses them;
add a row here before using one.
