# Round 15/15b: abstract re-read from the paper source (the pooled 0-of-290 sentence left it);
# revision string; no new arms. Run from paper-explorer/.
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAIN = Path(r"C:\Users\soham\AppData\Local\hermes\research-corpus\paper1-accept-loop\paper\main.tex")
t = MAIN.read_text(encoding="utf-8")
abs_ = t[t.find(r"\begin{abstract}") + len(r"\begin{abstract}"):t.find(r"\end{abstract}")]
abs_ = re.sub(r"\\texttt\{([^}]*)\}", r"\1", abs_)
abs_ = abs_.replace("\\%", "%").replace("$N$", "N").replace("---", " - ").replace("--", "-")
abs_ = re.sub(r"\$([^$]*)\$", r"\1", abs_)
ABSTRACT = " ".join(abs_.split())
assert "45 of 45" in ABSTRACT and "Twenty-six" in ABSTRACT and "290" not in ABSTRACT

arms_p = HERE / "arms.json"
a = json.loads(arms_p.read_text(encoding="utf-8"))
next(p for p in a["papers"] if p["id"] == "paper1")["claim"] = ABSTRACT
arms_p.write_text(json.dumps(a, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
m = json.loads((HERE / "meta.json").read_text(encoding="utf-8"))
m["paper1_revision"] = ("Revision 5.15 (round 15: cut by thread; elicitation, rectangle, cross-vendor detail, "
                        "arm M extend branch and the pooled-zero table moved to a supplement PDF; "
                        "twenty-six arms incl. arm B, the optimizer-alone baseline: 45 of 45 clear; 37 pp + 12 pp supplement), 2026-09-02")
(HERE / "meta.json").write_text(json.dumps(m, indent=2) + "\n", encoding="utf-8")
print("atlas synced to round 15:", len(a["arms"]), "arms,", len(a["links"]), "links")
