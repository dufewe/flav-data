# ---------------------------------------------------------
# Electroweak precision observable guide for the flav-data
# Streamlit app. Uses the same naming rules as the flavor page;
# symbols come from flav-data-importer/references/observable-naming.md.
# ---------------------------------------------------------

import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

with open(os.path.join(PROJECT_ROOT, 'defs.py'), 'r', encoding='utf-8') as f:
    exec(f.read())

# ---------------------------------------------------------
# Naming conventions
# ---------------------------------------------------------
st.markdown(r'''
# Electroweak Precision Observables (EWPO)

EWPO entries use the same schema and naming rules as flavor entries.
The observable is a bare symbol (`OBS`), the process is the `data` key,
and `[condition]` is reserved for multi-transition ratios or differences.

| Component | Meaning |
|-----------|---------|
| `OBS` | Abbreviation from `flav-data-importer/references/observable-naming.md` §3 |
| `data` key | pid transition (pids joined by `.2.`) or `no-transition` for intrinsic properties |
| `[condition]` | Flavor mapping for multi-transition observables only |
| `(parameter)` | Non-transition tag, e.g. `R1(CLN)` |

Measurement settings such as collision energy or a mass hypothesis are
**not** part of `name`. Data sources shared by a group go in its
`dataset` field; different datasets or kinematic regions use separate
data groups, as do fit choices.

## Intrinsic Observables — `no-transition`

Masses, running masses, and lifetimes describe a particle rather than a
process, so they sit under the `no-transition` key in a data group:

| Quantity | Symbol | Notes |
|----------|--------|-------|
| $Z$ mass | `Mass(Z)` | On-shell mass |
| $W$ mass | `Mass(W)` | On-shell mass |
| Higgs mass | `Mass(H)` | On-shell mass |
| Top mass | `Mass(t)` | On-shell mass |
| $\overline{\text{MS}}$ mass | `mass(t)` | Running mass (lowercase `mass`) |
| Lifetime | `Tau(f)` | `f` is the particle symbol, e.g. `Tau(Bs0)` |

The argument is the PDG particle label, not a pid. Single-token
shortcuts (`MZ`, `MW`, `Mtop`, `MH`, `Mh`) are rejected by the
validator.

Some EWPO quantities are bare names without any transition or particle
argument:

| Symbol | Meaning |
|--------|---------|
| `R_b` | $Z \to b\bar{b}$ partial-width ratio $\Gamma_b/\Gamma_{\rm had}$ |
| `R_c` | $Z \to c\bar{c}$ partial-width ratio $\Gamma_c/\Gamma_{\rm had}$ |
| `fs/fd` | $B_s/B^0$ fragmentation ratio |
| `ge/gmu`, `ge/gtau` | Lepton coupling ratios at the $Z$ |

## Process Observables

When the quantity belongs to a specific process, keep the bare symbol
and put the transition in the `data` key:

| Quantity | Symbol | Data key |
|----------|--------|----------|
| Branching fraction | `Br` | `H_I??_0++_0.2.ph_I??_1--_0.ph_I??_1--_0` |
| Decay fraction | `f` | `Z_I??_1??_0.2.MU_I??_1+n_0.mu_I??_1+n_0` |
| Partial or total width | `Gamma` | `Z_I??_1??_0.2.MU_I??_1+n_0.mu_I??_1+n_0` |
| Forward-backward asymmetry | `AFB` | `E_I??_1+n_0.e_I??_1+n_0.2.Z_I??_1??_0.2.MU_I??_1+n_0.mu_I??_1+n_0` |
| Cross section | `Sigma` | `uud_I1?_1+n_0.uud_I1?_1+n_0.2.W_I??_1??_0.2.MU_I??_1+n_0.v` |
| Differential cross section in $p_T$ | `dSigma/dpT` | `uud_I1?_1+n_0.uud_I1?_1+n_0.2.W_I??_1??_0.2.MU_I??_1+n_0.v` |
| Differential cross section in $\eta$ | `dSigma/deta` | `uud_I1?_1+n_0.uud_I1?_1+n_0.2.W_I??_1??_0.2.MU_I??_1+n_0.v` |
| Charge asymmetry | `AC` | `uB_I1?_0-n_0.2.cC_I0-_1--_0.uS_I1?_0-n_0` |
| Direct CP asymmetry | `ACP` | channel of the decay |

Transition keys follow the full rules used everywhere else in the
database: pids, initial state, `2`, final state, with cascades repeating
`2` (`uud_I1?_1+n_0.uud_I1?_1+n_0.2.W_I??_1??_0.2.MU_I??_1+n_0.v`). See
the **Flavor** guide for pid grammar and ordering; a compact key without
`.2.` is rejected.

## Ratios and Differences

| Type | Symbol | Example |
|------|--------|---------|
| Difference | `DeltaOBS[condition]` | `DeltaACP[mu-e]` |
| Ratio | `ROBS[condition]` | `RFL[mu/e]` |
| Canonical LFU ratio | `R` | `R` under a channel that fixes the final state |

The canonical LFU ratio is bare `R` when the channel key already carries
the final state; do not repeat that state in the name.

## Names Not Yet in the Reference

The importer reference is the contract. Quantities without an entry in
`observable-naming.md` §3 — for example the effective weak mixing angle, Higgs
signal strengths, or coupling modifiers — must first be given a symbol
and added to that table (see §5 of the reference), then used in JSON.
Do not invent a page-only spelling that the importer does not validate.

The same applies to new particles or intermediate states: register the
pid in `particle-naming.md` before using it in a transition key.
''')

# ---------------------------------------------------------
# transition-mode classification
# ---------------------------------------------------------
st.markdown(r'''
# `transition-mode` Classification

`transition-mode` is a required top-level field that immediately precedes
`data`. Values are hyphenated property names; non-property descriptors
such as "rare decay" or "BSM search" are invalid.

| Value | Use for | Examples |
|-------|---------|----------|
| `electroweak-precision` | Z-pole, W mass, weak mixing angle | LEP/SLC Z-pole |
| `w-production` | W production and decay | Tevatron/LHC W cross sections |
| `higgs-decay` | Higgs boson decays | $H \to \gamma\gamma$, $H \to ZZ^*$ |
| `higgs-production` | Higgs boson production | $pp \to H$, VBF, $t\bar{t}H$ |
| `low-energy` | Low-energy precision measurements | $g-2$, atomic parity violation |
| `oblique-corrections` | $S$, $T$, $U$ parameter fits | New-physics constraints |
| `scattering` | Scattering and production processes | $pp \to W$, $e^+e^- \to \mu^+\mu^-$ |
| `mixing` | Mixing, oscillation, lifetime measurements | $\Delta m_s$, $\tau(B_s^0)$ |
| `world-average` | Compiled averages of many processes | PDG Review, HFLAV averages |

The complete list (including the decay categories `leptonic-decay`,
`semileptonic-decay`, `non-leptonic-decay`, `radiative-decay`,
`neutron-beta-decay`) is maintained in
`flav-data-importer/references/json-meta.md` §"transition-mode Values".
''')
