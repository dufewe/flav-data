"""Apply the 4 rules from Test/improve.md to all Experimental/ data files.

Run with ``--apply`` to actually write changes (default is dry run).

The 4 rules are:

1. **Matrix format**: Each matrix row is on a single line; do NOT
   put each element on its own line.

   ``\u201c``_correlation``\u201d: [
        [1.0, 0.5, 0.3],
        [0.5, 1.0, 0.2],
        [0.3, 0.2, 1.0]
    ]``

2. **Abstract multi-line formula conversion**: arXiv abstracts may
   contain multi-line ``\\\\begin{align*} ... \\\\end{align*}`` blocks.
   Convert to single-line LaTeX so the abstract is one line.

3. **Author format**: Authors must follow InspireHEP BibTeX format:
   ``\"Aaij, R. and others\"``.

4. **Unicode \u2192 LaTeX**: Any Unicode character in extracted data
   (\\u03bc \\u2192 \\\\mu, \u0394 \\u2192 \\\\Delta, etc.) must be
   replaced with its LaTeX equivalent.

The script is idempotent: re-running on already-fixed files is a no-op.
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path("/Users/dufewe/Backup/Selia/projects/2HDM-SMEFT/Fitting/Streamlit/flav-data")
APPLY = "--apply" in sys.argv

# ---------------------------------------------------------------------------
# Rule 1: matrix format
# ---------------------------------------------------------------------------

# Match any *matrix-shaped* nested list. The data is JSON, and matrices
# are 2D float lists under a "*_correlation" or "*_covariance" key. We
# always re-serialize them as compact row-per-line.
MATRIX_KEY_RE = re.compile(r"^(tot_)?(type@\d+_)?(correlation|covariance)$")


def fix_matrix_format(matrix):
    """Recursively normalize matrix to row-per-line JSON layout.

    Returned as a Python nested list (caller re-serializes).
    """
    if not isinstance(matrix, list):
        return matrix
    if not matrix or not all(isinstance(row, list) for row in matrix):
        return matrix
    return [[float(x) if isinstance(x, (int, float)) else x for x in row] for row in matrix]


# ---------------------------------------------------------------------------
# Rule 2: multi-line formula conversion (abstracts)
# ---------------------------------------------------------------------------

# Match \begin{align*} ... \end{align*} (or align, equation, eqnarray,
# gather, etc.) and replace with single-line.
ENV_BLOCK_RE = re.compile(
    r"\$\\begin\{(align\*?|eqnarray\*?|gather\*?|equation\*?|multline\*?)\}(.*?)\\end\{\1\}\$",
    re.DOTALL,
)


def convert_multiline_formula(text: str) -> str:
    """Replace ``\\begin{X} ... \\end{X}`` (with $$ delimiters) with single-line.

    Joins lines with `, ` separators and adds the `and` conjunction
    before the last entry for natural English. If the LaTeX structure
    is unknown, just collapse newlines to spaces.
    """
    def _collapse(m):
        env_name = m.group(1)
        body = m.group(2)
        # Remove TeX line breaks (\\)
        body = re.sub(r"\\\\(?:\\[a-z]+\b)?", r", ", body)
        # Collapse whitespace
        body = re.sub(r"\s+", " ", body).strip()
        # Strip trailing commas/whitespace
        body = body.rstrip(",").rstrip()
        return f"${body}$"

    text = ENV_BLOCK_RE.sub(_collapse, text)
    # Also handle bare multi-line display blocks (not wrapped in $$...$$)
    # e.g. \begin{align*} ... \end{align*} without $$ delimiters
    BARE_ENV_RE = re.compile(
        r"\\begin\{(align\*?|eqnarray\*?|gather\*?|equation\*?|multline\*?)\}(.*?)\\end\{\1\}",
        re.DOTALL,
    )
    text = BARE_ENV_RE.sub(_collapse, text)
    return text


# ---------------------------------------------------------------------------
# Rule 3: author format (InspireHEP BibTeX)
# ---------------------------------------------------------------------------

# BibTeX format: "Surname, F.M. and others"  (initials, NOT full first name)
# Examples:
#   Aaij, R. and others
#   Aaboud, M. and others
#   Sirunyan, A.M. and others


def is_bibtex_format(author: str) -> bool:
    """Check if author is in InspireHEP BibTeX format.

    A BibTeX author has form ``"Surname, F.M."`` or
    ``"Surname, F."`` (initials with periods, no spaces within the
    initials). Multiple authors are separated by ``" and "``.
    """
    if not author or not isinstance(author, str):
        return False
    # Strip " and others" suffix for analysis
    base = re.sub(r"\s+and\s+others\s*$", "", author).strip()
    if not base:
        return False
    # Check first author format: "Surname, Initials."
    # Initials can be single letter (e.g. "R.") or multi-letter (e.g. "A.M.")
    m = re.match(r"^([A-Z][a-zA-Z'\-]+),\s*([A-Z]\.([A-Z]\.)*)$", base)
    if not m:
        return False
    return True


def convert_to_bibtex_format(author: str) -> str:
    """Convert full-name author to BibTeX initials form.

    Input: ``"Aaij, Roel and others"`` or ``"Aaij, Roel"`` (full first name)
    Output: ``"Aaij, R. and others"`` (initials)
    """
    if not author:
        return author
    # Take only the first author (before any " and ")
    first = author.split(" and ")[0].strip()
    has_others = " and others" in author
    # Split on last comma
    if "," not in first:
        return author  # can't parse
    surname, given = first.rsplit(",", 1)
    surname = surname.strip()
    given = given.strip()
    if not given:
        return author
    # Convert given names to initials
    # e.g. "Roel" -> "R.", "Anne Marie" -> "A.M.", "A M" -> "A.M."
    parts = re.split(r"[\s\-]+", given)
    initials = ".".join(p[0].upper() for p in parts if p) + "."
    result = f"{surname}, {initials}"
    if has_others:
        result += " and others"
    return result


# ---------------------------------------------------------------------------
# Rule 4: Unicode \u2192 LaTeX
# ---------------------------------------------------------------------------

# Common Unicode characters seen in HEP data and their LaTeX equivalents.
# Note: this is intentionally conservative. Only the most common ones
# are mapped; for exotic chars, manual review is required.
UNICODE_TO_LATEX = {
    # Greek letters (lowercase)
    "\u03b1": r"\alpha", "\u03b2": r"\beta", "\u03b3": r"\gamma",
    "\u03b4": r"\delta", "\u03b5": r"\epsilon", "\u03b6": r"\zeta",
    "\u03b7": r"\eta", "\u03b8": r"\theta", "\u03b9": r"\iota",
    "\u03ba": r"\kappa", "\u03bb": r"\lambda", "\u03bc": r"\mu",
    "\u03bd": r"\nu", "\u03be": r"\xi", "\u03bf": r"\o",
    "\u03c0": r"\pi", "\u03c1": r"\rho", "\u03c3": r"\sigma",
    "\u03c4": r"\tau", "\u03c5": r"\upsilon", "\u03c6": r"\phi",
    "\u03c7": r"\chi", "\u03c8": r"\psi", "\u03c9": r"\omega",
    # Greek letters (uppercase)
    "\u0391": r"A", "\u0392": r"B", "\u0393": r"\Gamma",
    "\u0394": r"\Delta", "\u0395": r"E", "\u0396": r"Z",
    "\u0397": r"H", "\u0398": r"\Theta", "\u0399": r"I",
    "\u039a": r"K", "\u039b": r"\Lambda", "\u039c": r"M",
    "\u039d": r"N", "\u039e": r"\Xi", "\u039f": r"O",
    "\u03a0": r"\Pi", "\u03a1": r"R", "\u03a3": r"\Sigma",
    "\u03a4": r"T", "\u03a5": r"\Upsilon", "\u03a6": r"\Phi",
    "\u03a7": r"X", "\u03a8": r"\Psi", "\u03a9": r"\Omega",
    # Common math symbols
    "\u00b1": r"\pm", "\u2213": r"\mp", "\u00d7": r"\times",
    "\u00f7": r"\div", "\u221e": r"\infty", "\u2202": r"\partial",
    "\u2207": r"\nabla", "\u2208": r"\in", "\u2209": r"\notin",
    "\u2200": r"\forall", "\u2203": r"\exists", "\u2229": r"\cap",
    "\u222a": r"\cup", "\u2282": r"\subset", "\u2283": r"\supset",
    "\u2286": r"\subseteq", "\u2287": r"\supseteq", "\u2264": r"\leq",
    "\u2265": r"\geq", "\u2260": r"\neq", "\u2248": r"\approx",
    "\u2261": r"\equiv", "\u2192": r"\to", "\u2190": r"\leftarrow",
    "\u21d2": r"\Rightarrow", "\u21d0": r"\Leftarrow", "\u2194": r"\leftrightarrow",
    "\u21d4": r"\Leftrightarrow", "\u2191": r"\uparrow", "\u2193": r"\downarrow",
    # Common typographic
    "\u2013": r"--",  # en-dash
    "\u2014": r"---",  # em-dash
    "\u2018": r"`",  # left single quote
    "\u2019": r"'",  # right single quote
    "\u201c": r"``",  # left double quote
    "\u201d": r"''",  # right double quote
    "\u00b0": r"^{\circ}",  # degree
    "\u00a0": r"~",  # non-breaking space
    # Particle names with bar
    "\u00af": r"\bar{}",  # macron (often used for \bar{p} etc.)
}

# Compile a single regex for efficient replacement
_UNICODE_PATTERN = re.compile("|".join(re.escape(k) for k in UNICODE_TO_LATEX.keys()))


def unicode_to_latex(text: str) -> str:
    if not text or not isinstance(text, str):
        return text
    return _UNICODE_PATTERN.sub(lambda m: UNICODE_TO_LATEX[m.group(0)], text)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

class CompactMatrixEncoder(json.JSONEncoder):
    """JSON encoder that keeps matrix rows on a single line.

    Detects 2D numeric lists (rows of equal-length number lists) and
    serializes each row as ``[a, b, c, ...]`` on one line. Falls back
    to default for non-matrix nested lists.
    """

    def _is_matrix(self, obj):
        if not isinstance(obj, list) or not obj:
            return False
        if not all(isinstance(row, list) for row in obj):
            return False
        if not all(row for row in obj):
            return False
        n_cols = len(obj[0])
        if n_cols < 2:
            return False
        if not all(len(row) == n_cols for row in obj):
            return False
        if not all(
            all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in row)
            for row in obj
        ):
            return False
        return True

    def encode(self, o):
        return self._encode(o, indent_level=0)

    def _encode(self, o, indent_level):
        if self._is_matrix(o):
            # Render as: [ [a, b, c],\n  [d, e, f] ]
            indent = "    " * (indent_level + 1)
            closing = "    " * indent_level
            rows = [",\n".join(
                indent + "[" + ", ".join(self.format(x) for x in row) + "]"
                for row in o
            )]
            # Actually we need to put commas BETWEEN rows not after.
            # Reformat properly:
            formatted_rows = [
                indent + "[" + ", ".join(self.format(x) for x in row) + "]"
                for row in o
            ]
            return "[\n" + ",\n".join(formatted_rows) + "\n" + closing + "]"

        # Default behavior
        if isinstance(o, list):
            if not o:
                return "[]"
            indent = "    " * (indent_level + 1)
            closing = "    " * indent_level
            items = [self._encode(item, indent_level + 1) for item in o]
            return "[\n" + ",\n".join(indent + i for i in items) + "\n" + closing + "]"
        if isinstance(o, dict):
            if not o:
                return "{}"
            indent = "    " * (indent_level + 1)
            closing = "    " * indent_level
            items = []
            for k, v in o.items():
                key = self.format(k) if isinstance(k, str) else json.dumps(k)
                val = self._encode(v, indent_level + 1)
                items.append(f"{indent}{key}: {val}")
            return "{\n" + ",\n".join(items) + "\n" + closing + "}"
        return json.dumps(o, ensure_ascii=self.ensure_ascii)

    def format(self, o):
        return json.dumps(o, ensure_ascii=self.ensure_ascii)


def fix_file(path: Path) -> tuple[dict | None, list[str]]:
    """Apply rules 1-4 to one file. Returns (modified_data, warnings)."""
    warnings = []
    try:
        with open(path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, ["JSON parse error"]

    if not isinstance(data, dict):
        return None, [f"top-level is {type(data).__name__}, not object"]

    # Rule 2: abstract multi-line formula conversion
    if "abstract" in data and isinstance(data["abstract"], str):
        new_abstract = convert_multiline_formula(data["abstract"])
        if new_abstract != data["abstract"]:
            warnings.append("abstract: converted multi-line formula to single-line")
            data["abstract"] = new_abstract

    # Rule 3: author format
    if "author" in data and isinstance(data["author"], str):
        author = data["author"]
        # If author uses full first name and not "and others", convert
        if author and not is_bibtex_format(author) and "," in author:
            new_author = convert_to_bibtex_format(author)
            if new_author != author:
                warnings.append(f"author: {author!r} -> {new_author!r}")
                data["author"] = new_author

    # Rule 4: Unicode -> LaTeX (apply to all string fields recursively)
    def _fix_unicode(obj):
        if isinstance(obj, str):
            new = unicode_to_latex(obj)
            return new, new != obj
        if isinstance(obj, dict):
            changed = False
            for k, v in list(obj.items()):
                new_v, c = _fix_unicode(v)
                if c:
                    obj[k] = new_v
                    changed = True
            return obj, changed
        if isinstance(obj, list):
            changed = False
            for i, v in enumerate(obj):
                new_v, c = _fix_unicode(v)
                if c:
                    obj[i] = new_v
                    changed = True
            return obj, changed
        return obj, False

    new_data, u_changed = _fix_unicode(data)
    if u_changed:
        warnings.append("Unicode -> LaTeX substitutions applied")
    data = new_data

    # Rule 1: matrix format (apply in data block matrices)
    if "data" in data and isinstance(data["data"], list):
        for entry in data["data"]:
            if not isinstance(entry, dict):
                continue
            for k, v in list(entry.items()):
                if MATRIX_KEY_RE.match(k) and isinstance(v, list):
                    new_v = fix_matrix_format(v)
                    if new_v != v:
                        warnings.append(f"matrix {k}: normalized to row-per-line")
                    entry[k] = new_v

    return data, warnings


def main():
    files = [f for f in (ROOT / "Experimental").rglob("*.json")
             if "@" not in f.name and "correlation" not in f.name]
    print(f"Scanning {len(files)} data files...")
    print(f"Mode: {'APPLY' if APPLY else 'DRY RUN'}")
    print()

    fixed = 0
    warnings_by_file = defaultdict(list)

    for f in files:
        if APPLY:
            original = f.read_text()
        modified, warnings = fix_file(f)
        if modified is None:
            continue
        if warnings:
            warnings_by_file[str(f)] = warnings
        if APPLY:
            encoder = CompactMatrixEncoder(ensure_ascii=False, indent=4)
            new_text = encoder.encode(modified) + "\n"
            if new_text != original:
                with open(f, "w") as fp:
                    fp.write(new_text)
                fixed += 1
        else:
            disk_text = f.read_text()
            encoder = CompactMatrixEncoder(ensure_ascii=False, indent=4)
            new_text = encoder.encode(modified) + "\n"
            if new_text != disk_text:
                fixed += 1

    print(f"\n{'Fixed' if APPLY else 'Would fix'}: {fixed} files")
    if warnings_by_file:
        print(f"Files with warnings: {len(warnings_by_file)}")
        sample_count = 0
        for path, warns in warnings_by_file.items():
            for w in warns[:3]:
                if sample_count < 15:
                    rel = Path(path).relative_to(ROOT)
                    print(f"  {rel}: {w[:120]}")
                    sample_count += 1
            if sample_count >= 15:
                break


if __name__ == "__main__":
    main()
