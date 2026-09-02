# Sync the paper-1 atlas to the round-14 paper: abstract read from the paper source (TeX
# stripped), two new arm nodes (CCP, CL-W) with links, revision tag. Run from paper-explorer/.
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
assert "0 of 35" in ABSTRACT and "0 of 19" in ABSTRACT and "Twenty-four" in ABSTRACT

arms_p = HERE / "arms.json"
a = json.loads(arms_p.read_text(encoding="utf-8"))
paper = next(p for p in a["papers"] if p["id"] == "paper1")
paper["claim"] = ABSTRACT

ids = {x["id"] for x in a["arms"]}
new_arms = [
    {"id": "p1_arm_ccp", "paper": "paper1", "label": "Arm CCP - the isolating arm (math-only prompt, pinned path, 120 s, Sonnet)",
     "kind": "extension",
     "design": "Arm CC's math-only program prompt, byte-identical, on arm CL's serving path (Sonnet via the pinned API, temperature 1.0, no system prompt) under arm CL's 120-second budget, numpy/scipy blocked by the AST gate. 3 N x 15 = 45 invocations, registered at corpus commit ebf213e and pushed before the first call. P-CCP1: no valid output clears (the library is what clears). P-CCP2: clearance at 20% or more of valid at 2 of 3 cells (path or budget explain arm CL). F-CCP1 rewrites contribution 1 if P-CCP2 holds.",
     "result": "35 valid of 45 (10, 14, 11 by cell), 0 clear, none reaches the argmax; best per cell 1.625, 2.1, 2.673 - at N = 13 and 21 the template anchor itself. P-CCP1 holds. Within the Sonnet tier the library, not the path or the budget, is what clears the family. Corpus 1428."},
    {"id": "p1_arm_clw", "paper": "paper1", "label": "Arm CL-W - weak-tier numpy/scipy top-up, pooled with arm CL",
     "kind": "extension",
     "design": "Arm CL's weak-tier prompt byte-identical, same path and decoding, 45 more invocations (credit-limited from a drafted 90, disclosed), pooled with arm CL's 45 under a rule fixed before sampling (commit f73222a). Two readings per row registered in advance: the registered parser (primary) and a lenient reading that strips the numpy scalar wrapper np.float64(...) the weak tier prints, which the registered parser rejects. P-CLW1: 0 clear. P-CLW2: 20% or more clear. Dead zone between.",
     "result": "Pooled 90: 19 valid (6, 3, 10 by cell), 0 clear under the registered parser, Wilson 95% upper bound 16.8%, so the weak library cell now excludes the registered 20% bar (the N = 21 cell stays under the five-valid floor). Lenient reading: 41 valid, 4 clear (9.8%, upper bound 22.5%), inside the dead zone. The weak tier clears never under the registered parser and rarely under the lenient one; not at rate under either. Corpus 1473."},
]
for x in new_arms:
    if x["id"] not in ids:
        a["arms"].append(x)
new_links = [
    {"source": "p1_arm_ccp", "target": "p1_arm_cl", "type": "contrasts_with", "note": "Same path, same budget, no libraries: 0 of 35 against 23 of 25. The library is the factor within the Sonnet tier."},
    {"source": "p1_arm_ccp", "target": "p1_arm_ccs", "type": "extends", "note": "Same math-only prompt moved from the agent runtime (10 s) to the pinned path (120 s): 0 of 37 stays 0 of 35."},
    {"source": "p1_arm_clw", "target": "p1_arm_cl", "type": "extends", "note": "Weak-tier top-up pooled with arm CL under a pre-stated rule: 0 of 19 registered, 4 of 41 lenient."},
]
have = {(l["source"], l["target"]) for l in a["links"]}
for l in new_links:
    if (l["source"], l["target"]) not in have:
        a["links"].append(l)
arms_p.write_text(json.dumps(a, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

meta_p = HERE / "meta.json"
m = json.loads(meta_p.read_text(encoding="utf-8"))
m["site_updated"] = "2026-09-02"
m["paper1_pdf_updated"] = "2026-09-02"
m["paper1_revision"] = "Revision 5.14 (round 14: arms CCP and CL-W, twenty-four arms, 48 pp), 2026-09-02"
m["arms_updated"] = "2026-09-02"
meta_p.write_text(json.dumps(m, indent=2) + "\n", encoding="utf-8")
print("atlas synced to round 14:", len(a["arms"]), "arms,", len(a["links"]), "links")
