# Sync the paper-1 atlas headline to the round-13 paper: new title, new abstract, revision tag.
# Arms L, P, CL were added by update_round12.py and are left alone. Run from paper-explorer/.
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TITLE = "Capability or Optimizer? What Lets an LLM Proposer Leave Its Template Family on Circle Packing"
ABSTRACT = (
    "Zero-shot LLM proposers on circle packing (sum of radii of N circles in a unit square) concentrate on a "
    "grid-plus-filler family whose best value follows in closed form from N. We cross two proposer tiers with "
    "three output channels (direct emission, math-only code, code with numpy and scipy) and ask what lets a "
    "proposer leave that family. "
    "One cell clears at rate. A Sonnet-tier program with the libraries beats the family in 23 of 25 valid cases "
    "at every cell, by 0.7–4.2%, still below the published bounds where they exist. A weak-tier program with the "
    "same libraries clears 0 of 11; a Sonnet-tier program without them clears 0 of 37, on a different serving path "
    "and execution budget, so the design does not isolate the library; every weak-tier trap cell is 0; and under "
    "one clearance rule 0 of 290 valid outputs across six math-only, held-out and conditioned arms clear. "
    "Handed the better in-family construction with its score, the weak tier keeps the template modal at 2 of 3 "
    "cells as registered; a disclosed post-hoc attempt count shows it reaching for the better construction in 36 "
    "of 45 invocations and building it in 6 of 14 valid outputs. The bottleneck is execution, not preference. The "
    "zero-shot characterization itself does not survive one parent-conditioning step, five loop generations, or a "
    "change of serving path. All twenty-two preregistered arms are reported."
)

arms_p = HERE / "arms.json"
a = json.loads(arms_p.read_text(encoding="utf-8"))
paper = next(p for p in a["papers"] if p["id"] == "paper1")
paper["title"] = TITLE
paper["claim"] = ABSTRACT
arms_p.write_text(json.dumps(a, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

app_p = HERE / "app.js"
s = app_p.read_text(encoding="utf-8")
old = "<h3>A Computable Floor for Weak-Tier and Math-Only Circle-Packing Proposals, and the Library-Enabled Search That Clears It</h3>"
new = "<h3>" + TITLE + "</h3>"
assert s.count(old) + s.count(new) == 1
app_p.write_text(s.replace(old, new), encoding="utf-8")

meta_p = HERE / "meta.json"
m = json.loads(meta_p.read_text(encoding="utf-8"))
m["site_updated"] = "2026-09-02"
m["paper1_pdf_updated"] = "2026-09-02"
m["paper1_revision"] = "Revision 5.13 (round 13: tier x channel table, body 19 pp), 2026-09-02"
m["arms_updated"] = "2026-09-02"
meta_p.write_text(json.dumps(m, indent=2) + "\n", encoding="utf-8")
print("atlas synced to round 13")
