# ---------------------------------------------------------
# Electroweak precision observable guide for the flav-data
# Streamlit app. Uses the same naming rules as the flavor page;
# symbols come from flav-data-importer/references/obs-abbr.md.
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
| `OBS` | Abbreviation from `flav-data-importer/references/obs-abbr.md` §3 |
| `data` key | Transition (`A.B.2.C.D`) or `no-transition` for intrinsic properties |
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
| $Z$ mass | `Mass(Z)` | Legacy shortcut `MZ` |
| $W$ mass | `Mass(W)` | Legacy shortcut `MW` |
| Higgs mass | `Mass(H)` | Legacy shortcut `MH`; light Higgs `Mh` |
| Top mass | `Mass(t)` | Legacy shortcut `Mtop` |
| $\overline{\text{MS}}$ mass | `mass(t)` | Running mass (lowercase `mass`) |
| Lifetime | `Tau(f)` | `f` is the particle symbol, e.g. `Tau(Bs0)` |

Legacy shortcuts remain valid for existing files, but new imports should
use the generic `Mass(f)` form.

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
| Branching fraction | `Br` | `H.2.gamma.gamma` |
| Decay fraction | `f` | `Z.2.mu+.mu-` |
| Partial or total width | `Gamma` | `Z.2.mu+.mu-` |
| Forward-backward asymmetry | `AFB` | `e+.e-.2.Z.2.mu+.mu-` |
| Cross section | `Sigma` | `p.p.2.W+.2.mu+.nu` |
| Differential cross section in $p_T$ | `dSigma/dpT` | `p.p.2.W+.2.mu+.nu` |
| Differential cross section in $\eta$ | `dSigma/deta` | `p.p.2.W+.2.mu+.nu` |
| Charge asymmetry | `AC` | `B+.2.J/psi.K+` |
| Direct CP asymmetry | `ACP` | channel of the decay |

Transition keys follow the full rules used everywhere else in the
database: initial state, `2`, final state, with cascades repeating `2`
(`p.p.2.W+.2.mu+.nu`). See the **Flavor** guide for particle ordering,
charge indicators, antiparticle `Bar`, and the compact legacy form.

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
`obs-abbr.md` §3 — for example the effective weak mixing angle, Higgs
signal strengths, or coupling modifiers — must first be given a symbol
and added to that table (see §7 of the reference), then used in JSON.
Do not invent a page-only spelling that the importer does not validate.

The same applies to new particles or intermediate states: add them to
the particle tables in `obs-abbr.md` §1 before using them in a
transition key.
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

The complete list (including the decay categories `leptonic-decay`,
`semileptonic-decay`, `non-leptonic-decay`, `radiative-decay`,
`neutron-beta-decay`) is maintained in
`flav-data-importer/references/json-meta.md` §"transition-mode Values".
''')
