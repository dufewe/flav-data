#!/usr/bin/env python3
"""Unicode→LaTeX and BibTeX-author formatting (SKILL.md rules 3 & 4).

Shared helpers re-exported by all extraction scripts; import from any of them.
"""

import re

# ---------------------------------------------------------------------------
# Unicode → LaTeX mapping (SKILL.md rule 4)
# ---------------------------------------------------------------------------

_UNICODE_TO_LATEX_MAP = {
    # ---- Greek lowercase ----
    '\u03b1': '\\alpha',       # α
    '\u03b2': '\\beta',        # β
    '\u03b3': '\\gamma',       # γ
    '\u03b4': '\\delta',       # δ
    '\u03b5': '\\varepsilon',  # ε
    '\u03b6': '\\zeta',        # ζ
    '\u03b7': '\\eta',         # η
    '\u03b8': '\\theta',       # θ
    '\u03b9': '\\iota',        # ι
    '\u03ba': '\\kappa',       # κ
    '\u03bb': '\\lambda',      # λ
    '\u03bc': '\\mu',          # μ
    '\u03bd': '\\nu',          # ν
    '\u03be': '\\xi',          # ξ
    '\u03bf': 'o',             # ο (omicron — same as Latin o)
    '\u03c0': '\\pi',          # π
    '\u03c1': '\\rho',         # ρ
    '\u03c2': '\\varsigma',    # ς (final sigma)
    '\u03c3': '\\sigma',       # σ
    '\u03c4': '\\tau',         # τ
    '\u03c5': '\\upsilon',     # υ
    '\u03c6': '\\phi',         # φ
    '\u03c7': '\\chi',         # χ
    '\u03c8': '\\psi',         # ψ
    '\u03c9': '\\omega',       # ω
    # ---- Greek uppercase ----
    '\u0391': 'A',             # Α (same as Latin A)
    '\u0392': 'B',             # Β (same as Latin B)
    '\u0393': '\\Gamma',       # Γ
    '\u0394': '\\Delta',       # Δ
    '\u0395': 'E',             # Ε (same as Latin E)
    '\u0396': 'Z',             # Ζ (same as Latin Z)
    '\u0397': 'H',             # Η (same as Latin H)
    '\u0398': '\\Theta',       # Θ
    '\u0399': 'I',             # Ι (same as Latin I)
    '\u039a': 'K',             # Κ (same as Latin K)
    '\u039b': '\\Lambda',      # Λ
    '\u039c': 'M',             # Μ (same as Latin M)
    '\u039d': 'N',             # Ν (same as Latin N)
    '\u039e': '\\Xi',          # Ξ
    '\u039f': 'O',             # Ο (same as Latin O)
    '\u03a0': '\\Pi',          # Π
    '\u03a1': 'P',             # Ρ (same as Latin P)
    '\u03a3': '\\Sigma',       # Σ
    '\u03a4': 'T',             # Τ (same as Latin T)
    '\u03a5': '\\Upsilon',     # Υ
    '\u03a6': '\\Phi',         # Φ
    '\u03a7': 'X',             # Χ (same as Latin X)
    '\u03a8': '\\Psi',         # Ψ
    '\u03a9': '\\Omega',       # Ω
    # ---- Math symbols ----
    '\u00b1': '\\pm',          # ±
    '\u00d7': '\\times',       # ×
    '\u2192': '\\to',          # →
    '\u2190': '\\leftarrow',   # ←
    '\u2264': '\\leq',         # ≤
    '\u2265': '\\geq',         # ≥
    '\u2248': '\\approx',      # ≈
    '\u2260': '\\neq',         # ≠
    '\u00b0': '^{\\circ}',     # °
    '\u2032': "'",             # ′ (prime → plain apostrophe)
    '\u2033': "''",            # ″ (double prime)
    '\u00b7': '\\cdot',        # ·
    '\u00f7': '/',             # ÷ → plain slash
    '\u2212': '-',             # − (minus sign → hyphen)
    '\u2211': '\\Sigma',       # ∑
    '\u220f': '\\Pi',          # ∏
    '\u222b': '\\int',         # ∫
    '\u2202': '\\partial',     # ∂
    '\u221e': '\\infty',       # ∞
    '\u2191': '\\uparrow',     # ↑
    '\u2193': '\\downarrow',   # ↓
    # ---- Bar / overline ----
    '\u00af': '\\bar{}',       # ¯
    # ---- Superscripts ----
    '\u2070': '^{0}',
    '\u00b9': '^{1}',
    '\u00b2': '^{2}',
    '\u00b3': '^{3}',
    '\u2074': '^{4}',
    '\u2075': '^{5}',
    '\u2076': '^{6}',
    '\u2077': '^{7}',
    '\u2078': '^{8}',
    '\u2079': '^{9}',
    '\u207a': '^{+}',        # ⁺
    '\u207b': '^{-}',        # ⁻
    '\u207c': '^{=',         # ⁼
    '\u207d': '^{(}',        # ⁽
    '\u207e': '^{)}',        # ⁾
}

# Multi-character replacements (applied after single-char map)
_MULTI_CHAR_REPLACEMENTS = [
    # en-dash, em-dash → LaTeX escape (write as literal ---/--)
    ('\u2013', '--'),    # en-dash
    ('\u2014', '---'),   # em-dash
    # Smart quotes (must be handled in order to avoid partial matches)
    ('\u201c', '``'),    # left double quote
    ('\u201d', "''"),    # right double quote
    ('\u2018', '`'),     # left single quote
    ('\u2019', "'"),     # right single quote
    # Invisible / zero-width characters
    ('\u200b', ''),      # zero-width space
    ('\ufeff', ''),      # BOM
    # Latin ligatures (common in PDF text extraction)
    ('\ufb00', 'ff'),
    ('\ufb01', 'fi'),
    ('\ufb02', 'fl'),
    ('\ufb03', 'ffi'),
    ('\ufb04', 'ffl'),
]


def unicode_to_latex(text: str) -> str:
    """Replace all supported Unicode characters in *text* with LaTeX equivalents.

    Applies the mapping defined in SKILL.md "Core Conventions" rule 4:
    Greek letters, math symbols, smart quotes, dashes, and common
    typographic characters are converted. Unrecognised characters pass
    through unchanged.

    Parameters
    ----------
    text : str
        The input string, possibly containing Unicode characters.

    Returns
    -------
    str
        The converted string with LaTeX escape sequences.
    """
    if not isinstance(text, str):
        return text
    result = text
    # Multi-char replacements first (so e.g. smart quotes aren't
    # corrupted by single-char Greek substitutions).
    for char, replacement in _MULTI_CHAR_REPLACEMENTS:
        result = result.replace(char, replacement)
    # Single-char replacements
    for char, replacement in _UNICODE_TO_LATEX_MAP.items():
        result = result.replace(char, replacement)
    return result


# ---------------------------------------------------------------------------
# BibTeX author-name formatting
# ---------------------------------------------------------------------------
# Rule 3 (SKILL.md "Core Conventions"):
#   Author field must use InspireHEP BibTeX format:
#       "Surname, Initials."
#   Example: "Aaij, Roel" → "Aaij, R."
#   Already-initials form ("A.M.") passes through unchanged.
#   Fallback (no person names): "{group} collaboration".

def to_bibtex(full_name: str) -> str:
    """Convert an InspireHEP full author name to BibTeX initials form.

    InspireHEP stores authors as ``"Surname, Full First Name"``
    (e.g. ``"Aaij, Roel"``).  This function shortens the given/first
    names to initials only: ``"Aaij, R."``.  If the name is already
    in initials form (e.g. ``"A.M."``) it passes through unchanged.

    Parameters
    ----------
    full_name : str
        Author name in any of these forms:

        - ``"Surname, Full First Name"`` (most common from InspireHEP)
        - ``"Surname, F."`` (already initials — pass through)
        - ``"Surname"`` (no comma — pass through)
        - ``"Collaboration collaboration"`` (fallback — pass through)

    Returns
    -------
    str
        The BibTeX-formatted name string.
    """
    if not isinstance(full_name, str) or not full_name.strip():
        return full_name or ''

    name = full_name.strip()
    
    # No comma → surname-only or group name; return as-is.
    if ',' not in name:
        return name

    parts = name.split(',', 1)
    surname = parts[0].strip()
    first_part = parts[1].strip()

    # If first_part is a single letter or already dotted initials
    # (e.g. "R." or "A.M." or "R"), pass through as-is.
    first_clean = first_part.replace('.', '').replace(' ', '')
    if len(first_clean) <= 3 and all(c.isupper() for c in first_clean):
        # Already initials form — normalise spacing
        # "R" → "R.",  "A M" → "A.M.",  "A. M." → "A.M."
        initials = first_part.replace(' ', '')
        if not initials.endswith('.'):
            initials += '.'
        return f'{surname}, {initials}'

    # Full first name → extract initials
    # "Roel" → "R.",  "John Paul" → "J.P."
    tokens = first_part.split()
    initials_list = []
    for token in tokens:
        # Handle hyphenated first names: "Jean-Luc" → "J.-L."
        sub_tokens = token.split('-')
        sub_initials = [st[0].upper() + '.' for st in sub_tokens if st]
        initials_list.append('-'.join(sub_initials))
    initials = ''.join(initials_list)

    return f'{surname}, {initials}'


def format_authors(full_names: list[str]) -> str:
    """Format an author list per SKILL.md rule 3.

    Tiers: 1 author → ``"Surname, I."``; 2–3 → comma-separated BibTeX
    names with ``and``; 4+ → ``"Surname, I. and others"``. An empty list
    returns ``''``; the caller substitutes a collaboration fallback.
    """
    names = [name for name in (full_names or []) if name]
    if not names:
        return ''
    bibtex = [to_bibtex(name) for name in names]
    if len(bibtex) == 1:
        return bibtex[0]
    if len(bibtex) == 2:
        return f'{bibtex[0]} and {bibtex[1]}'
    if len(bibtex) == 3:
        return f'{bibtex[0]}, {bibtex[1]}, and {bibtex[2]}'
    return f'{bibtex[0]} and others'


# Mapping from compact observable abbreviation to its LaTeX symbol.
# Covers the most common observables used in B → K(*)ℓℓ and B → DK analyses.
# For full canonical list see references/obs-abbr.md §3.
#
# IMPORTANT: This dict does NOT cover transition-symbol expansion
# (e.g. "B0.2.Kst0.mu+.mu-" → "B^{0} \\to K^{*0} \\mu^{+}\\mu^{-}"). That
# expansion follows the rules in references/obs-abbr.md §1 and §4 and must
# be applied separately, either by hand or via a more specialised parser.
# latex_for_obs() below applies this dict for the OBSERVABLE ABBREVIATION
# only; transition rendering falls through to the transition form verbatim.
OBSERVABLE_LATEX = {
    # Branching fractions and ratios
    'Br': '\\mathcal{B}',
    'RBr': '\\mathcal{R}',  # ratio of branching fractions
    'dBr/dq2': 'd\\mathcal{B}/dq^2',
    'ACP': 'A_{CP}',
    'Sigma': '\\sigma',
    'Gamma': '\\Gamma',
    'DeltaMass': '\\Delta M',

    # Angular coefficients (LHCb B → K* μμ angular analysis)
    'FL': 'F_L',
    'S3': 'S_3',
    'S4': 'S_4',
    'S5': 'S_5',
    'S7': 'S_7',
    'S8': 'S_8',
    'S9': 'S_9',
    'AFB': 'A_{FB}',
    'P1': 'P_1',
    'P2': 'P_2',
    'P3': 'P_3',
    'P4p': 'P_4^{\\prime}',
    'P5p': 'P_5^{\\prime}',
    'P6p': 'P_6^{\\prime}',
    'P8p': 'P_8^{\\prime}',

    # Asymmetries
    'ASL': 'A_{SL}',

    # CKM parameters (no transition needed)
    'gammaCKM': '\\gamma',
    'gamma': '\\gamma',
    'r': 'r',
    'delta': '\\delta',

    # Masses, lifetimes, mixing (no transition)
    'Mass': 'M',  # e.g. Mass(Bs) → "$M_{B_s}$"
    'Tau': '\\tau',
    'Width': '\\Gamma',
    'dGamma_s': '\\Delta\\Gamma_s',
    'dMs': '\\Delta M_s',
    'dMd': '\\Delta M_d',

    # EW parameters (no transition)
    'MZ': 'M_Z',
    'MW': 'M_W',
    'Mtop': 'm_t',
    'MH': 'M_H',
    'sin2theta': '\\sin 2\\theta',
    'alphaS': '\\alpha_s',
    'alpha': '\\alpha_{\\rm QED}',
    'GFermi': 'G_F',
}


def latex_for_obs(obs_name: str) -> str:
    """Build the LaTeX symbol for an observable name.

    Kept as a standalone formatting helper: the flav-data schema stores
    LaTeX only at the channel level (``[latex, obs@N object]``), so this
    is not used when assembling JSON. It renders the bare observable
    symbol and any ``[condition]`` it carries. For example::

        latex_for_obs("gammaCKM")                  # → "$\\gamma$"
        latex_for_obs("Mass(B0)")                  # → "$M_{B0}$"
        latex_for_obs("FL")                        # → "$F_L$"

    **Limitations.** This helper applies the OBSERVABLE ABBREVIATION table
    (e.g. ``FL`` → ``F_L``) and renders a parenthesized particle as a
    subscript (``Mass(B0)`` → ``M_{B0}``). Method tags such as
    ``Vcb(CLN)`` are not special-cased. If you need fully expanded LaTeX,
    see ``references/obs-abbr.md`` §4 for the LaTeX mapping and write the
    field by hand, or extend this helper.

    For an unknown abbreviation, falls back to wrapping the bare ``obs_name``
    in ``$...$``.
    """
    import re

    # Bare form (no transition): "gammaCKM", "Mass", "MZ" etc.
    if obs_name in OBSERVABLE_LATEX:
        return f'${OBSERVABLE_LATEX[obs_name]}$'

    # Particle bare form: "Mass(B0)", "Tau(Bs)", "Mass(Z)" — the inner
    # content is a single particle name (no '.2.' separator, no '+'/'−'/'*').
    bare = re.match(r'^([A-Za-z][A-Za-z0-9]*)\(([^)]+)\)$', obs_name)
    if bare:
        inner = bare.group(2)
        # Heuristic: bare form has no transition indicators
        is_bare = ('.' not in inner and '+' not in inner and '-' not in inner
                   and '*' not in inner and 'nu' not in inner)
        if is_bare:
            abbr, particle = bare.group(1), bare.group(2)
            sym = OBSERVABLE_LATEX.get(abbr, abbr)
            return f'${sym}_{{{particle}}}$'

    return f'${obs_name}$'  # last-ditch fallback
