#!/usr/bin/env python3
"""Unicode→LaTeX, BibTeX-author formatting, and shared I/O helpers.

Canonical implementations for the extraction scripts (SKILL.md rules 3 & 4).
"""

import contextlib
import json
import os
import unicodedata
import urllib.error
import urllib.request

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
    # ---- Latin letters with no NFD decomposition (author names) ----
    '\u00b5': '\\mu',         # µ (micro sign)
    '\u00c6': '\\AE',         # Æ
    '\u00e6': '\\ae',         # æ
    '\u0152': '\\OE',         # Œ
    '\u0153': '\\oe',         # œ
    '\u00d8': '\\O',          # Ø
    '\u00f8': '\\o',          # ø
    '\u0141': '\\L',          # Ł
    '\u0142': '\\l',          # ł
    '\u0110': '\\DJ',         # Đ
    '\u0111': '\\dj',         # đ
    '\u00d0': '\\DH',         # Ð
    '\u00f0': '\\dh',         # ð
    '\u00de': '\\TH',         # Þ
    '\u00fe': '\\th',         # þ
    '\u00df': '\\ss',         # ß
    '\u0131': '\\i',          # ı (dotless i)
    '\u0130': '\\.{I}',       # İ
}

# Typographic replacements (applied before the single-char map)
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


# Combining diacritical marks → LaTeX accent commands (applied after NFD
# decomposition, so any precomposed accented Latin letter is covered).
_COMBINING_TO_LATEX = {
    '\u0300': '`',   # grave
    '\u0301': "'",   # acute
    '\u0302': '^',   # circumflex
    '\u0303': '~',   # tilde
    '\u0304': '=',   # macron
    '\u0306': 'u',   # breve
    '\u0307': '.',   # dot above
    '\u0308': '"',   # diaeresis
    '\u030a': 'r',   # ring above
    '\u030b': 'H',   # double acute
    '\u030c': 'v',   # caron
    '\u0323': 'd',   # dot below
    '\u0327': 'c',   # cedilla
    '\u0328': 'k',   # ogonek
    '\u0331': 'b',   # macron below
}


def _apply_latex_accents(text: str) -> str:
    """Render accented Latin letters as LaTeX accents via NFD decomposition.

    ``é`` → ``\\\'{e}``, ``č`` → ``\\v{c}``, ``ç`` → ``\\c{c}``. Marks without a
    known command are left untouched rather than dropped.
    """
    decomposed = unicodedata.normalize('NFD', text)
    out = []
    i = 0
    n = len(decomposed)
    while i < n:
        base = decomposed[i]
        j = i + 1
        marks = []
        while j < n and unicodedata.combining(decomposed[j]):
            marks.append(decomposed[j])
            j += 1
        if marks and not unicodedata.combining(base):
            rendered = base
            for mark in marks:
                command = _COMBINING_TO_LATEX.get(mark)
                if command is None:
                    rendered = None
                    break
                rendered = f'\\{command}{{{rendered}}}'
            if rendered is not None:
                out.append(rendered)
                i = j
                continue
        out.append(base)
        i += 1
    return ''.join(out)


def unicode_to_latex(text: str) -> str:
    """Replace supported Unicode characters with LaTeX (SKILL.md rule 4).

    Covers Greek letters, math symbols, dashes, smart quotes, ligatures,
    invisible characters, and accented Latin letters. Anything else passes
    through unchanged.
    """
    if not isinstance(text, str):
        return text
    result = text
    for char, replacement in _MULTI_CHAR_REPLACEMENTS:
        result = result.replace(char, replacement)
    for char, replacement in _UNICODE_TO_LATEX_MAP.items():
        result = result.replace(char, replacement)
    return _apply_latex_accents(result)


# ---------------------------------------------------------------------------
# BibTeX author-name formatting (SKILL.md rule 3)
# ---------------------------------------------------------------------------

def to_bibtex(full_name: str) -> str:
    """Shorten an InspireHEP name to BibTeX initials: ``"Aaij, Roel"`` → ``"Aaij, R."``.

    Already-initials forms (``"R."``, ``"A.M."``), surname-only strings, and
    group fallbacks pass through. Hyphenated given names keep both initials
    (``"Jean-Luc"`` → ``"J.-L."``).
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

    # Up to three uppercase letters means the name is already initials.
    first_clean = first_part.replace('.', '').replace(' ', '')
    if len(first_clean) <= 3 and all(c.isupper() for c in first_clean):
        # Normalise spacing: "R" → "R.", "A. M." → "A.M."
        initials = first_part.replace(' ', '')
        if not initials.endswith('.'):
            initials += '.'
        return f'{surname}, {initials}'

    tokens = first_part.split()
    initials_list = []
    for token in tokens:
        sub_tokens = token.split('-')
        sub_initials = [st[0].upper() + '.' for st in sub_tokens if st]
        initials_list.append('-'.join(sub_initials))
    initials = ''.join(initials_list)

    return f'{surname}, {initials}'


# Surname particles kept with the family name when converting arXiv
# "First Last" names (e.g. "Danny van Dyk" → "van Dyk, D.").
_SURNAME_PARTICLES = {
    'van', 'von', 'de', 'del', 'della', 'di', 'da', 'dos', 'das', 'du',
    'le', 'la', 'ter', 'ten', 'bin', 'al', 'el', 'den', 'der', 'het', 'te',
}


def arxiv_name_to_bibtex(full_name: str) -> str:
    """Normalise an arXiv ``"First Last"`` name to ``"Last, First"`` form.

    InspireHEP names already carry a comma and pass through. Single-token
    names (mononyms / collaborations) are returned unchanged. The family
    name absorbs preceding particles (``van``, ``de``, ...); ``to_bibtex``
    then shortens the given names to initials.
    """
    if not isinstance(full_name, str) or not full_name.strip():
        return full_name or ''
    name = full_name.strip()
    if ',' in name:
        return name
    tokens = name.split()
    if len(tokens) == 1:
        return name
    surname_start = len(tokens) - 1
    while (surname_start > 1
           and tokens[surname_start - 1].lower() in _SURNAME_PARTICLES):
        surname_start -= 1
    surname = ' '.join(tokens[surname_start:])
    given = ' '.join(tokens[:surname_start])
    return f'{surname}, {given}'


def format_authors(full_names: list[str]) -> str:
    """Format an author list per SKILL.md rule 3.

    Tiers: 1 → ``"Surname, I."``; 2 → ``"A and B"``; 3 → ``"A, B, and C"``;
    4+ → ``"A and others"``. An empty list returns ``''``; the caller
    substitutes a collaboration fallback.
    """
    names = [name for name in (full_names or []) if name]
    if not names:
        return ''
    bibtex = [to_bibtex(name) for name in names]
    if len(bibtex) == 1:
        result = bibtex[0]
    elif len(bibtex) == 2:
        result = f'{bibtex[0]} and {bibtex[1]}'
    elif len(bibtex) == 3:
        result = f'{bibtex[0]}, {bibtex[1]}, and {bibtex[2]}'
    else:
        result = f'{bibtex[0]} and others'
    return unicode_to_latex(result)


# ---------------------------------------------------------------------------
# Shared I/O helpers
# ---------------------------------------------------------------------------

@contextlib.contextmanager
def open_url(url: str, *, label: str, headers: dict[str, str] | None = None,
             timeout: int = 15):
    """GET ``url`` and yield the open response, closing it afterwards.

    ``label`` names the caller in the error message ("arXiv API", ...).
    HTTP and connection failures become ``ValueError`` so callers have a
    single exception type to handle.
    """
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            yield response
    except urllib.error.HTTPError as e:
        raise ValueError(
            f"{label} request failed (HTTP {e.code}): {e.reason}"
        ) from e
    except urllib.error.URLError as e:
        raise ValueError(f"{label} connection failed: {e.reason}") from e


def write_json(path: str, payload: dict) -> None:
    """Write ``payload`` as 4-space-indented JSON, creating parent directories."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=4, ensure_ascii=False)
