# Sync the paper-1 atlas to the round-12 paper: headline title and abstract, and the three arms
# the atlas never had (L, P, CL). graph.json is the corpus concept graph and is left alone.
# Run from paper-explorer/. Idempotent.
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TITLE = ("A Computable Floor for Weak-Tier and Math-Only Circle-Packing Proposals, "
         "and the Library-Enabled Search That Clears It")
ABSTRACT = (
    "Language models in the proposal role of discovery loops are usually characterized zero-shot. "
    "We built one on circle packing (sum of radii of N circles in a unit square) and measured how "
    "far it reaches. "
    "A weak-tier proposer does not search: it emits a grid template whose value follows in closed "
    "form from N, modal at all seven tested cells (five registered as point predictions) and at "
    "four of five held-out cells (a separate arm). It is bound to its setting: it dissolves after "
    "one parent-conditioning step, and the same prompt sent bare to the vendor's pinned API yields "
    "0 valid packings in 105 where the agent runtime yields the template in 4 of 6. "
    "The family's best expressible value is a computable floor: across six arms (math-only programs "
    "at two tiers, held-out cells, one-step conditioning, five loop generations) 0 of 290 valid "
    "outputs clear it, including 0 of 37 from Sonnet-tier search. It holds for every weak-tier "
    "output measured, with or without numpy and scipy; a Sonnet-tier program with those libraries "
    "clears it at every cell, 23 of 25 valid cases, by 2.5–4.2%. The floor is the number the weak "
    "tier never beats and the deployed one does."
)
DASH = " — "
NEW_ARMS = [
    {
        "id": "p1_arm_l", "paper": "paper1",
        "label": "Arm L" + DASH + "iterated loop (five generations, two archives)",
        "kind": "extension",
        "design": "Weak-tier proposer run as a registered loop: 2 N x 2 archive seeds x 6 rounds x 5 "
                  "samples, 120 invocations, four predictions L1-L4 and falsifier F-L1 registered at "
                  "commit c9645fe before sampling. L2: the one-step dissolution survives iteration. "
                  "L1: the anchor returns on a diverse archive. L3: value climbs across rounds. "
                  "L4: some conditioned output clears the family argmax.",
        "result": "L2 confirmed; L1 and L3 not met, L3 reversed (a 2-2 tie at n = 4 decided against "
                  "the prediction by the registered tie rule). L4 open: 0 of 49 valid conditioned "
                  "outputs clear the family argmax, so the loop moves the anchor but not the ceiling. "
                  "Corpus 1068.",
    },
    {
        "id": "p1_arm_p", "paper": "paper1",
        "label": "Arm P" + DASH + "pinned-temperature rerun on the vendor's bare API",
        "kind": "control",
        "design": "The same bare prompt sent to the pinned serving path (anthropic/claude-haiku-4.5 "
                  "through OpenRouter, temperature 1.0), 15 per cell at the seven square cells and "
                  "the five held-out cells, registered at corpus commit aa473ad before sampling with "
                  "P-P1 to P-P4 and F-P1. A post-hoc temperature sweep (0.0, 0.5, 1.0) and a "
                  "same-day agent-runtime control were added and disclosed.",
        "result": "Validity collapsed to 0 of 105 at the square cells and 4 of 75 held-out, so every "
                  "point prediction is unscoreable; F-P1 fired. Temperature excluded (0 of 6 at "
                  "all three settings). The agent-runtime control yields 6 of 6 valid and the "
                  "template in 4 of 6: the anchor is a property of the agent runtime as an "
                  "instrument, not of the model weights alone. Corpus 1293.",
    },
    {
        "id": "p1_arm_cl", "paper": "paper1",
        "label": "Arm CL" + DASH + "library-enabled code channel (numpy/scipy)",
        "kind": "extension",
        "design": "Program-emitting proposals allowed numpy and scipy, two tiers (Haiku, Sonnet) x "
                  "3 N x 15, 90 invocations, registered at corpus commit aa473ad before sampling. "
                  "P-CL1: no valid output clears the family argmax. P-CL2: at least 20% do. F-CL1: "
                  "the ceiling falls at every cell for a tier, which triggers a registered "
                  "integration rule for the abstract, the title and the pooled ceiling.",
        "result": "Weak tier: 0 of 11 valid clear, P-CL1 holds. Sonnet tier: 23 of 25 valid clear at "
                  "3 of 3 cells, by 2.5-4.2%, F-CL1 fired. Sonnet's best per cell sits 0.5% (N = 13) "
                  "and 0.9% (N = 21) below the published best-known sums. The family ceiling is a "
                  "property of the math-only channel; it is not a bound on library-enabled search. "
                  "Corpus 1383.",
    },
]
NEW_LINKS = [
    {"source": "p1_arm_l", "target": "p1_arm_mu", "type": "extends",
     "note": "One-step dissolution (MU) survives five generations; 0 of 49 conditioned outputs clear the family argmax."},
    {"source": "p1_arm_p", "target": "p1_arm_f", "type": "contrasts_with",
     "note": "The bare arm's anchor does not reproduce on the pinned API (0/105 valid); it does in the agent runtime (4/6)."},
    {"source": "p1_arm_cl", "target": "p1_mode_ceiling", "type": "contrasts_with",
     "note": "Sonnet with numpy/scipy clears the family ceiling at 3/3 cells; the 290-pool ceiling is scoped to the math-only channel."},
    {"source": "p1_arm_cl", "target": "p1_arm_ccs", "type": "extends",
     "note": "Same Sonnet tier, same cells, libraries allowed: 0/37 clear in CCS becomes 23/25 clear in CL."},
]

arms_p = HERE / "arms.json"
a = json.loads(arms_p.read_text(encoding="utf-8"))
paper = next(p for p in a["papers"] if p["id"] == "paper1")
paper["title"] = TITLE
paper["claim"] = ABSTRACT
have = {x["id"] for x in a["arms"]}
for arm in NEW_ARMS:
    if arm["id"] not in have:
        a["arms"].append(arm)
ids = {x["id"] for x in a["arms"]}
for l in NEW_LINKS:
    assert l["target"] in ids, l["target"]
    if not any(x["source"] == l["source"] and x["target"] == l["target"] for x in a["links"]):
        a["links"].append(l)
arms_p.write_text(json.dumps(a, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"arms.json: {len(a['arms'])} arms, {len(a['links'])} links, title set")

app_p = HERE / "app.js"
s = app_p.read_text(encoding="utf-8")
old = "'<h3>A Closed Form for What the Model Emits</h3>',"
new = "'<h3>" + TITLE + "</h3>',"
assert s.count(old) + s.count(new) == 1
s = s.replace(old, new)
app_p.write_text(s, encoding="utf-8")
print("app.js: about-page title set")

meta_p = HERE / "meta.json"
m = json.loads(meta_p.read_text(encoding="utf-8"))
m["arms_updated"] = "2026-09-02"
meta_p.write_text(json.dumps(m, indent=2) + "\n", encoding="utf-8")
print("meta.json: arms_updated 2026-09-02")
