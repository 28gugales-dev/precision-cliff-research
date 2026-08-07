"""Structural pre-compile check for main.tex.

No TeX engine is installed on the authoring machine, so main.tex has never been
run through pdflatex. This script catches the defect classes that would break a
compile -- unbalanced environments/braces/math delimiters, undefined or duplicate
labels, uncited bibliographies, inconsistent tabular column counts, and non-ASCII
characters -- without needing one. It is a compile *proxy*, not a substitute:
it cannot detect missing packages, overfull boxes, or float placement problems.

Known-good patterns it is taught to accept (verified by hand 2026-08-06):
  - \\nocite{*} in place of \\cite keys (this manuscript cites inline by venue;
    see the comment above \\nocite in main.tex)
  - user \\newcolumntype like L{19mm} in tabular/longtable specs
  - \\caption* as the first row of a longtable (spans, needs no & separators)

Usage: python texlint.py [path/to/main.tex]
"""
import re, sys, os, collections

p = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.tex")
src = open(p, encoding="utf-8").read()
lines = src.split("\n")
issues = []

# strip comments (unescaped %)
def strip_comments(s):
    out = []
    for ln in s.split("\n"):
        r = ""
        i = 0
        while i < len(ln):
            if ln[i] == "\\" and i + 1 < len(ln):
                r += ln[i:i+2]; i += 2; continue
            if ln[i] == "%":
                break
            r += ln[i]; i += 1
        out.append(r)
    return "\n".join(out)

code = strip_comments(src)
clines = code.split("\n")

# 1. environment balance
stack = []
for i, ln in enumerate(clines, 1):
    for m in re.finditer(r"\\(begin|end)\{([^}]+)\}", ln):
        kind, env = m.group(1), m.group(2)
        if kind == "begin":
            stack.append((env, i))
        else:
            if not stack:
                issues.append(f"L{i}: \\end{{{env}}} with empty stack")
            elif stack[-1][0] != env:
                issues.append(f"L{i}: \\end{{{env}}} closes \\begin{{{stack[-1][0]}}} from L{stack[-1][1]}")
                stack.pop()
            else:
                stack.pop()
for env, i in stack:
    issues.append(f"L{i}: \\begin{{{env}}} never closed")

# 2. brace balance per line-region (report net drift)
depth = 0
for i, ln in enumerate(clines, 1):
    j = 0
    while j < len(ln):
        if ln[j] == "\\" and j + 1 < len(ln):
            j += 2; continue
        if ln[j] == "{": depth += 1
        elif ln[j] == "}":
            depth -= 1
            if depth < 0:
                issues.append(f"L{i}: brace depth went negative")
                depth = 0
        j += 1
if depth != 0:
    issues.append(f"EOF: unbalanced braces, net depth {depth}")

# 3. inline math $ parity (per line, ignoring \$ and $$)
for i, ln in enumerate(clines, 1):
    t = ln.replace("\\$", "").replace("$$", "")
    if t.count("$") % 2:
        issues.append(f"L{i}: odd number of $ -> {ln.strip()[:90]}")

# 4. refs vs labels
labels = set(re.findall(r"\\label\{([^}]+)\}", code))
refs = set(re.findall(r"\\(?:eq)?ref\{([^}]+)\}", code))
for r in sorted(refs - labels):
    issues.append(f"undefined \\ref{{{r}}}")
dupes = [l for l, c in collections.Counter(re.findall(r"\\label\{([^}]+)\}", code)).items() if c > 1]
for d in dupes:
    issues.append(f"duplicate \\label{{{d}}}")

# 5. cites vs bibitems
cites = set()
for m in re.finditer(r"\\cite[tp]?\{([^}]+)\}", code):
    cites |= {c.strip() for c in m.group(1).split(",")}
bibs = set(re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}", code))
has_bibtex = "\\bibliography{" in code
nocite_all = "\\nocite{*}" in code
if (bibs or not has_bibtex) and not nocite_all:
    for c in sorted(cites - bibs):
        issues.append(f"undefined \\cite{{{c}}}")

# 6. tabular column-count sanity
def grab_braced(s, i):
    """s[i] must be '{'; return (inner, index_after_close) with brace matching."""
    assert s[i] == "{"
    d, j = 0, i
    while j < len(s):
        if s[j] == "\\": j += 2; continue
        if s[j] == "{": d += 1
        elif s[j] == "}":
            d -= 1
            if d == 0:
                return s[i+1:j], j + 1
        j += 1
    return s[i+1:], len(s)

tab_specs = []
for m in re.finditer(r"\\begin\{(tabular|longtable)\}", code):
    j = m.end()
    while j < len(code) and code[j] in " \n\t": j += 1
    if j < len(code) and code[j] == "[":      # optional [t]/[b] pos arg
        j = code.index("]", j) + 1
        while j < len(code) and code[j] in " \n\t": j += 1
    if j >= len(code) or code[j] != "{": continue
    spec, after = grab_braced(code, j)
    endtok = "\\end{" + m.group(1) + "}"
    e = code.find(endtok, after)
    tab_specs.append((spec, code[after:e if e > 0 else len(code)], m.start()))

for spec, body, startpos in tab_specs:
    m = type("M", (), {"start": lambda self, p=startpos: p})()
    # collapse arg-taking column types (p{..}, and user \newcolumntype like L{..}) to one token
    spec_n = re.sub(r"[A-Za-z]\{[^}]*\}", "X", spec)
    spec_n = re.sub(r"@\{[^}]*\}|\||>\{[^}]*\}|<\{[^}]*\}", "", spec_n)
    ncol = len(re.findall(r"[lcrXmbp]", spec_n))
    ln0 = code[:m.start()].count("\n") + 1
    for row in body.split("\\\\"):
        row_ = re.sub(r"\\multicolumn\{(\d+)\}\{[^}]*\}\{[^}]*\}", lambda mm: "&" * (int(mm.group(1)) - 1), row)
        rs = row_.strip()
        # rule/spacing rows and full-width caption rows carry no & separators
        if not rs or rs.startswith(("\\hline", "\\toprule", "\\midrule", "\\bottomrule",
                                    "\\caption", "\\endfirsthead", "\\endhead",
                                    "\\endfoot", "\\endlastfoot", "\\multicolumn")):
            continue
        cells = row_.count("&") + 1
        if cells != ncol:
            issues.append(f"~L{ln0}: tabular({ncol} cols) row has {cells}: {row.strip()[:70]}")

# 7. unicode that pdflatex chokes on
BAD = {"—": "---", "–": "--", "≈": "$\\approx$", "≥": "$\\ge$", "≤": "$\\le$",
       "×": "$\\times$", "√": "$\\sqrt{}$", "²": "$^2$", "⁻": "$^-$", "'": "'",
       "'": "'", '"': "``", '"': "''", "…": "\\dots", "→": "$\\to$", "≠": "$\\ne$",
       "α": "$\\alpha$", "Φ": "$\\Phi$", "·": "$\\cdot$", "≪": "$\\ll$", "∼": "$\\sim$"}
uni = collections.Counter()
for i, ln in enumerate(clines, 1):
    for ch in ln:
        if ord(ch) > 127:
            uni[ch] += 1
if uni:
    issues.append("NON-ASCII chars present (pdflatex needs inputenc/utf8 or replacement): " +
                  ", ".join(f"{repr(c)}x{n}" + (f" ->{BAD[c]}" if c in BAD else " ->UNKNOWN") for c, n in uni.most_common()))

# 8. preamble facts
docclass = re.search(r"\\documentclass(\[[^\]]*\])?\{([^}]+)\}", code)
print("documentclass:", docclass.group(2) if docclass else "MISSING")
print("packages:", ", ".join(re.findall(r"\\usepackage(?:\[[^\]]*\])?\{([^}]+)\}", code)))
print("inputenc/utf8:", "yes" if re.search(r"usepackage\[.*utf8.*\]\{inputenc\}", code) else "no")
print("bibliography:", "bibtex" if has_bibtex else (f"{len(bibs)} bibitems" if bibs else "NONE"))
print("labels:", len(labels), "refs:", len(refs), "cites:", len(cites))
print("lines:", len(lines))
print()
if issues:
    print(f"=== {len(issues)} ISSUES ===")
    for x in issues:
        print(" -", x)
else:
    print("=== structurally clean ===")
