# Decay Mode Abbreviations and Observable Naming Conventions

## Decay Mode Abbreviations

Used in the `name` field of observables: `OBS(decay_abbreviation)`

| Full Decay | Abbreviation | Notes |
|-----------|-------------|-------|
| B⁺ → K⁺μ⁺μ⁻ | Bp2Kpmumu | |
| B⁺ → K⁺e⁺e⁻ | Bp2Kpee | |
| B⁰ → K*⁰μ⁺μ⁻ | B02Kstmumu | K*⁰ → K⁺π⁻ |
| B⁰ → K*⁰e⁺e⁻ | B02Kstee | |
| B⁰ₛ → φμ⁺μ⁻ | Bs0.2.phimumumu | φ → K⁺K⁻ |
| B⁰ₛ → φe⁺e⁻ | Bs0.2.phi.e+.e- | |
| Λb⁰ → Λμ⁺μ⁻ | Lb2Lmumu | Λ → pπ⁻ |
| B⁺ → π⁺μ⁺μ⁻ | Bp2pimumu | |
| B⁺ → π⁺e⁺e⁻ | Bp2piee | |
| B⁰ → K⁰Sμ⁺μ⁻ | B02KS0mumu | K⁰ₛ → π⁺π⁻ |
| B⁰ → K⁰Se⁺e⁻ | B02KS0ee | |
| B⁺ → K⁺τ⁺τ⁻ | Bp2Kptautau | Rare |
| B⁰ → K*⁰τ⁺τ⁻ | B02Ksttautau | Rare |
| W⁺ → μ⁺ν | Wp2munu | |
| W⁻ → μ⁻ν̄ | Wm2munu_bar | |

## Observable Types

### CP-averaged Angular Observables (B → K*ℓℓ)
| Symbol | Full Name | Range |
|--------|-----------|-------|
| FL | Longitudinal polarization fraction | [0, 1] |
| S3 | T-odd angular coefficient | [-0.5, 0.5] |
| S4 | Angular coefficient | [-1, 1] |
| S5 | Angular coefficient | [-1, 1] |
| AFB_CP | CP-averaged forward-backward asymmetry | [-1, 1] |
| S7 | T-odd angular coefficient | [-1, 1] |
| S8 | T-odd angular coefficient | [-1, 1] |
| S9 | T-odd angular coefficient | [-0.5, 0.5] |

### CP-asymmetric Observables
| Symbol | Full Name |
|--------|-----------|
| A3 | CP asymmetry of S3 |
| A4 | CP asymmetry of S4 |
| A5 | CP asymmetry of S5 |
| A6s | S6 CP asymmetry |
| A7 | CP asymmetry of S7 |
| A8 | CP asymmetry of S8 |
| A9 | CP asymmetry of S9 |

### Optimised Observables (P observables)
| Symbol | Full Name |
|--------|-----------|
| P1 | = S3 / (1 - FL) |
| P2 | = S4 / (1 - FL) (some conventions) |
| P3 | = S5 / (1 - FL) (some conventions) |
| P'4 | Optimised S4 |
| P'5 | Optimised S5 |
| P'6 | Optimised S6 |
| P'8 | Optimised S8 |

### Bs → φℓℓ Observables
| Symbol | Full Name |
|--------|-----------|
| FL | Longitudinal polarization fraction |
| A'6 | Reduced forward-backward asymmetry = A6/(1-FL) |
| S3 | Angular coefficient |
| A9 | CP-odd angular coefficient |

### B → Kℓℓ Observables
| Symbol | Full Name |
|--------|-----------|
| FH | Flat term in angular distribution |
| AFB | Forward-backward asymmetry |

### Branching Fractions
| Type | Units | Notes |
|------|-------|-------|
| dBr/dq² | 10⁻⁸ GeV⁻² | Differential branching fraction |
| Br (relative) | 10⁻⁵ | Relative to normalization mode |

## Common q² Bin Boundaries (GeV²)

### Low q²
- [0.1, 0.98]
- [1.1, 2.0] / [1.1, 2.5] / [1.1, 4.0] / [1.1, 6.0]
- [2.0, 3.0], [2.0, 4.0]
- [3.0, 4.0]
- [4.0, 5.0], [4.0, 6.0]
- [5.0, 6.0]
- [6.0, 7.0], [6.0, 8.0]
- [7.0, 8.0]

### Charm resonance region
- [8.0, 11.0] (usually excluded from fits)
- [11.0, 11.75], [11.0, 12.5]
- [11.75, 12.5]

### High q²
- [15.0, 16.0], [15.0, 17.0], [15.0, 18.9], [15.0, 19.0]
- [16.0, 17.0]
- [17.0, 18.0]
- [18.0, 19.0]

### Very low q² (electron mode)
- [0.0008, 0.257]
- [0.002, 1.12]

## LaTeX Representations

```python
OBSERVABLE_LATEX = {
    # CP-averaged
    'FL': '$F_L$',
    'S3': '$S_3$', 'S4': '$S_4$', 'S5': '$S_5$',
    'S7': '$S_7$', 'S8': '$S_8$', 'S9': '$S_9$',
    'AFB_CP': '$A_{\\rm FB}^{\\rm CP}$',

    # CP-asymmetric
    'A3': '$A_3$', 'A4': '$A_4$', 'A5': '$A_5$',
    'A6s': '$A_{6s}$', 'A7': '$A_7$', 'A8': '$A_8$', 'A9': '$A_9$',

    # Optimised
    'P1': '$P_1$', 'P2': '$P_2$', 'P3': '$P_3$',
    "P4'": "$P_4'$", "P5'": "$P_5'$", "P6'": "$P_6'$", "P8'": "$P_8'$",

    # Bs->phi ll
    "A6'": "$A'_6$",  # Reduced FB asymmetry

    # B->K ll
    'FH': '$F_H$',
    'AFB': '$A_{\\rm FB}$',
}
```
