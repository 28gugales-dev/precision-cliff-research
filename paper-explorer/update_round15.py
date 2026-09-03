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
if "p1_arm_b" not in {x["id"] for x in a["arms"]}:
    a["arms"].append({
        "id": "p1_arm_b", "paper": "paper1",
        "label": "Arm B - the optimizer alone (fixed SLSQP reference program, no model)",
        "kind": "extension",
        "design": "A fixed random-restart SLSQP program (analytic gradients, uniform random starts, radius shrink by the largest violation, 50 restarts), written before the run and never tuned, executed through arm CL's pipeline unmodified (python -I -S, 120 s wall clock, one core, arm-F scoring, section 2.4 clearance) at N = 13, 21, 31, 15 seeds each. Registered at corpus commit 1932cc0 after a blind review asked for the optimizer-alone control; amendment 1 (c486843): version 1 imported time and sys, blocked 45/45 by the allowlist, run kept. P-B1: clears >= 20% at >= 2 cells (the optimizer alone clears; contribution 1 rewritten). P-B2: never clears. S-B1: best vs arm CL's Sonnet best.",
        "result": "45 of 45 valid at both tolerances, 45 clear, 15 of 15 at every cell. Best per cell 1.829542412, 2.359585843, 2.883035274 against the Sonnet best 1.820699211, 2.340549845, 2.864990189: S-B1 at 3 of 3. P-B1 holds: the library optimizer clears the family with no model at all; the Sonnet programs clear because they invoke it and land below the fixed reference; the weak tier's 19 valid programs invoke it and clear nothing. No model invocations; corpus stays at 1500."})
have = {(l["source"], l["target"]) for l in a["links"]}
for l in [
    {"source": "p1_arm_b", "target": "p1_arm_cl", "type": "extends", "note": "Same pipeline, no model: 45/45 clear vs the Sonnet tier's 23/25; the optimizer is sufficient."},
    {"source": "p1_arm_b", "target": "p1_arm_ccp", "type": "extends", "note": "CCP: Sonnet without the library, 0/35. B: the library without any model, 45/45."},
]:
    if (l["source"], l["target"]) not in have and any(x["id"] == l["target"] for x in a["arms"]):
        a["links"].append(l)
arms_p.write_text(json.dumps(a, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
m = json.loads((HERE / "meta.json").read_text(encoding="utf-8"))
m["paper1_revision"] = ("Revision 5.15 (round 15: cut by thread; elicitation, rectangle, cross-vendor detail, "
                        "arm M extend branch and the pooled-zero table moved to a supplement PDF; "
                        "twenty-six arms incl. arm B, the optimizer-alone baseline: 45 of 45 clear, program listed in Supplement S7; "
                        "round 15c: arm B authorship and restart count stated, weak-library cell reported as a gap under both parsers; "
                        "round 16: bound table extended to N = 40, Sonnet best 0.8% and arm B 0.2% below the record at N = 31), 2026-09-02")
(HERE / "meta.json").write_text(json.dumps(m, indent=2) + "\n", encoding="utf-8")
print("atlas synced to round 15:", len(a["arms"]), "arms,", len(a["links"]), "links")
