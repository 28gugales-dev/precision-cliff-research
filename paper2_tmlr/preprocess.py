"""Build body.md (anonymized, pandoc-ready) from ../paper2_short.md.

Steps, in order:
1. Drop the title/author/abstract block (reproduced by main.tex instead).
2. Redact the author's Kaggle handle for double-blind review.
3. Insert the diversity-measurement related-work paragraph after the
   ShinkaEvolve paragraph in section 7 (single flagged content addition).
4. Map unicode math symbols pdflatex cannot take from gfm input to math mode.
"""
import re
from pathlib import Path

HERE = Path(__file__).parent
src = (HERE.parent / "paper2_short.md").read_text(encoding="utf-8")

# 1. body starts at section 1 (title/author/abstract handled in main.tex)
body = src[src.index("## 1. Introduction"):]

# 2. anonymization: kaggle handle only — kernel/dataset slugs stay, the
#    handle is what names the author. main.tex carries the redaction notice.
body = body.replace("sohamgugalet", "REDACTED")

# 3. (removed) the diversity-measurement related-work paragraph now lives in
#    paper2_short.md / paper2_draft.md directly, not injected here.

# 4. unicode -> latex-safe (outside backticks pandoc treats these literally;
#    inside backticks they'd break \texttt too, so map globally to text forms
#    that survive both). Math-mode forms are safe in prose; for code spans
#    pandoc escapes $ inside \texttt, so use plain-text fallbacks there.
# First: handle code spans separately — replace >=, <= already ASCII there.
REPL = {
    "≥": "$\\geq$",   # ≥
    "≤": "$\\leq$",   # ≤
    "≈": "$\\approx$",# ≈
    "×": "$\\times$", # ×
    "→": "$\\rightarrow$",  # →
    "≠": "$\\neq$",   # ≠
    "±": "$\\pm$",    # ±
    "…": "\\dots{}",  # …
    "√": "$\\sqrt{}$",# √ (rare; check context)
    "∈": "$\\in$",
    "−": "$-$",       # U+2212 minus
    "⌊": "$\\lfloor$",
    "⌋": "$\\rfloor$",
    "δ": "$\\delta$",
    "⁴": "$^{4}$",
}
# code spans must not receive $..$: split on backtick-delimited spans
parts = re.split(r"(`[^`]*`)", body)
for i, p in enumerate(parts):
    if i % 2 == 0:
        for k, v in REPL.items():
            p = p.replace(k, v)
    else:
        p = (p.replace("≥", ">=").replace("≤", "<=")
               .replace("→", "->").replace("…", "...")
               .replace("×", "x").replace("≈", "~")
               .replace("∈", "in").replace("−", "-")
               .replace("⌊", "floor(").replace("⌋", ")")
               .replace("δ", "delta").replace("⁴", "^4"))
    parts[i] = p
body = "".join(parts)

# 5. headings: strip manual numbering (LaTeX renumbers), map appendices to
#    \appendix letters, keep "Use of AI systems" unnumbered (it follows §8's
#    limitations block as a statement, not a section of the argument).
out_lines = []
appendix_started = False
for line in body.splitlines():
    m = re.match(r"^## (\d+)\. (.*)$", line)
    if m:
        out_lines.append(f"# {m.group(2)}")
        continue
    m = re.match(r"^### (\d+)\.(\d+) (.*)$", line)
    if m:
        out_lines.append(f"## {m.group(3)}")
        continue
    m = re.match(r"^### ([A-D])\.(\d+) (.*)$", line)
    if m:
        out_lines.append(f"## {m.group(3)}")
        continue
    if line.startswith("## Claim → evidence map"):
        out_lines.append("# Claim → evidence map")
        continue
    m = re.match(r"^## Appendix ([A-D]) — (.*)$", line)
    if m:
        # gfm carries no raw latex; fix_tables.py inserts \appendix before
        # the first of these titles in body.tex
        title = m.group(2)
        out_lines.append("# " + title[0].upper() + title[1:])
        continue
    out_lines.append(line)
body = "\n".join(out_lines) + "\n"

(HERE / "body.md").write_text(body, encoding="utf-8")
leftover = sorted({c for c in body if ord(c) > 0x2100})
print("body.md written;", len(body.splitlines()), "lines; symbols left:", leftover)
