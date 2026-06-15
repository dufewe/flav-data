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
]


def unicode_to_latex(text):
    """Replace all supported Unicode characters in *text* with LaTeX equivalents.

    Applies the mapping defined in SKILL.md "Import Conventions" rule 4:
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
# Rule 3 (SKILL.md "Import Conventions"):
#   Author field must use InspireHEP BibTeX format:
#       "Surname, Initials."
#   Example: "Aaij, Roel" → "Aaij, R."
#   Already-initials form ("A.M.") passes through unchanged.
#   Fallback (no person names): "{group} collaboration".

def to_bibtex(full_name):
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
