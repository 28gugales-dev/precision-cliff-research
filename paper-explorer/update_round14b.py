# Round 14e: arm P-D node and links; abstract re-read from the paper source. Run from paper-explorer/.
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
assert "12 of 14" in ABSTRACT and "Twenty-five" in ABSTRACT

arms_p = HERE / "arms.json"
a = json.loads(arms_p.read_text(encoding="utf-8"))
next(p for p in a["papers"] if p["id"] == "paper1")["claim"] = ABSTRACT
if "p1_arm_pd" not in {x["id"] for x in a["arms"]}:
    a["arms"].append({
        "id": "p1_arm_pd", "paper": "paper1", "label": "Arm P-D - which component of the agent runtime carries the template",
        "kind": "extension",
        "design": "Arm P's N = 13 square prompt (== arm F, hash 32db485b), Haiku 4.5 on the pinned OpenRouter path, temperature 1.0, two one-line manipulations, 15 each: D1 extended thinking on (routing-layer default effort), no system prompt; D2 thinking off, one system line 'You are a careful assistant. Think before you answer.' Registered at corpus commit 5554cc0 and pushed before the first call. P-PD1: D1 valid >= 8/15 and D2 <= 3/15 (reasoning budget is the cause). P-PD2: the mirror (context is). P-PD3: anything else.",
        "result": "Interim at 27 of 30 rows (credit): D1 valid 12 of 14 (11 at 1e-9), modal value T(4,13) = 1.625 in 5 of 12, k = 4 modal, one output at the family argmax 1.7761424; D2 valid 0 of 13, all overlaps. P-PD1 holds and the three missing rows cannot change it. The reasoning budget is the component of the runtime that carries the template; the runtime's inherited context is not. Corpus 1500."})
have = {(l["source"], l["target"]) for l in a["links"]}
for l in [
    {"source": "p1_arm_pd", "target": "p1_arm_p", "type": "extends", "note": "Same prompt, same pinned path: thinking on restores 12/14 valid with the template modal; a system line restores 0/13."},
]:
    if (l["source"], l["target"]) not in have and any(x["id"] == l["target"] for x in a["arms"]):
        a["links"].append(l)
arms_p.write_text(json.dumps(a, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
m = json.loads((HERE / "meta.json").read_text(encoding="utf-8"))
m["paper1_revision"] = "Revision 5.14e (round 14: arms CCP, CL-W, P-D interim; twenty-five arms, 49 pp), 2026-09-02"
(HERE / "meta.json").write_text(json.dumps(m, indent=2) + "\n", encoding="utf-8")
print("atlas synced to round 14e:", len(a["arms"]), "arms,", len(a["links"]), "links")
