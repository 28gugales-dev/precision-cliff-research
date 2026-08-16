"""Rewrite pandoc's non-wrapping longtable specs into wrapped p-columns.

Pandoc renders gfm pipe tables without width hints as all-`l` longtables,
which overflow the TMLR text width badly (the claim->evidence map by
~3900pt). Column budgets below share \linewidth per column count; the
2-column map gets an asymmetric split because its right column (artifact
paths + replay commands) runs longer than the claim column. Small numeric
tables (4+ short columns) wrap fine at equal shares.
"""
import re
from pathlib import Path

HERE = Path(__file__).parent
tex = (HERE / "body.tex").read_text(encoding="utf-8")

P = ">{{\\raggedright\\arraybackslash}}p{{{w:.3f}\\linewidth}}"

def spec_for(ncols: int) -> str:
    if ncols == 2:
        widths = [0.40, 0.56]
    else:
        gap = 0.03
        w = (0.97 - gap * ncols) / ncols
        widths = [w] * ncols
    return "@{}" + "".join(P.format(w=w) for w in widths) + "@{}"

def repl(m: re.Match) -> str:
    ncols = len(m.group(1))
    return "\\begin{longtable}[]{" + spec_for(ncols) + "}"

new, n = re.subn(r"\\begin\{longtable\}\[\]\{@\{\}(l+)@\{\}\}", repl, tex)
# small font for all longtables so 6-7 column tables fit
new = new.replace("\\begin{longtable}", "\\small\n\\begin{longtable}")
new = new.replace("\\end{longtable}", "\\end{longtable}\n\\normalsize")

# long artifact paths in \texttt never wrap; permit breaks after / and _
def breakable(m: re.Match) -> str:
    inner = m.group(1)
    if len(inner) > 40:
        inner = inner.replace("/", "/\\allowbreak ")
        inner = inner.replace("\\_", "\\_\\allowbreak ")
    return "\\texttt{" + inner + "}"

new = re.sub(r"\\texttt\{([^{}]*)\}", breakable, new)

# appendix boundary: letters instead of numbers from Appendix A onward
FIRST_APPENDIX = "\\section{The dispersion probes\\textquotesingle{} registered analyses, in full}"
assert new.count(FIRST_APPENDIX) == 1
new = new.replace(FIRST_APPENDIX, "\\appendix\n" + FIRST_APPENDIX)

# the AI-use statement is a statement, not a numbered section of the argument
new = re.sub(r"\\(sub)*section\{Use of AI systems\}",
             "\\\\subsection*{Use of AI systems}", new)
(HERE / "body.tex").write_text(new, encoding="utf-8")
print(f"rewrote {n} longtable specs")
