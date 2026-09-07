"""Arm L residual ledger: conditioned validity at 1e-6 and 1e-9, rows above the family
argmax with their excess, the argmax-parent split, the L3 per-cell table and its post hoc
Fisher exact test. Reads arm_l_collect.jsonl (frozen merge written by arm_l_analysis.py),
scores with arm_f_repro exactly as arm_l_analysis.py does, writes arm_l_residuals.json.
Run from precision-cliff root: python -X utf8 arm_l_residuals.py"""
import json, math, sys
from collections import defaultdict
sys.path.insert(0, ".")
import arm_f_repro as A
from arm_l_analysis import family_argmax, CFG, WINDOW

rows = [json.loads(l) for l in open("arm_l_collect.jsonl", encoding="utf-8") if l.strip()]
out = {"lineages": {}, "l3_cells": {}}
pooled = defaultdict(int)
regime = {"greedy": [0, 0], "diverse": [0, 0]}
pool_max = None
for lineage in CFG["lineages"]:
    n = int(lineage.split("-")[0])
    pred = CFG["cells"][str(n)]["predicted"]
    am = family_argmax(n)
    d = {"conditioned_rows": 0, "valid6": 0, "valid9": 0, "on_prediction": 0,
         "valid9_above": 0, "valid9_max_excess": None, "max_excess_valid6": None,
         "argmax_parent_rows": 0, "argmax_parent_valid6": 0}
    for r in rows:
        if r.get("lineage") != lineage or r.get("generation", 0) == 0:
            continue
        d["conditioned_rows"] += 1
        ps = r.get("parent_score")
        at_am = ps is not None and abs(ps - am) < WINDOW
        if at_am:
            d["argmax_parent_rows"] += 1
        if r.get("runtime_rejection"):
            continue
        circles, _ = A.parse_packing(r.get("raw_output"))
        if circles is None or len(circles) != n:
            continue
        if not A.validate(circles, n, tol=1e-6)[0]:
            continue
        s = sum(c[2] for c in circles)
        ex = s - am
        d["valid6"] += 1
        if at_am:
            d["argmax_parent_valid6"] += 1
        if abs(s - pred) < WINDOW:
            d["on_prediction"] += 1
        d["max_excess_valid6"] = ex if d["max_excess_valid6"] is None else max(d["max_excess_valid6"], ex)
        if A.validate(circles, n, tol=1e-9)[0]:
            d["valid9"] += 1
            if ex > 0:
                d["valid9_above"] += 1
            d["valid9_max_excess"] = ex if d["valid9_max_excess"] is None else max(d["valid9_max_excess"], ex)
    d["clear"] = int(d["valid9_max_excess"] is not None and d["valid9_max_excess"] > 1e-6)
    out["lineages"][lineage] = d
    for k in ("conditioned_rows", "valid6", "valid9", "on_prediction", "valid9_above",
              "argmax_parent_rows", "argmax_parent_valid6", "clear"):
        pooled[k] += d[k]
    if d["valid9_max_excess"] is not None:
        pool_max = d["valid9_max_excess"] if pool_max is None else max(pool_max, d["valid9_max_excess"])
    reg = lineage.split("-")[1]
    regime[reg][0] += d["on_prediction"]
    regime[reg][1] += d["valid6"]
    out["l3_cells"][lineage] = [d["on_prediction"], d["valid6"]]
pooled["valid9_max_excess"] = pool_max
out["pooled"] = dict(pooled)

# post hoc Fisher exact, two-sided, on GREEDY vs DIVERSE pooled over both cells
a, n1 = regime["greedy"]
c, n2 = regime["diverse"]
k = a + c
N = n1 + n2
def hyp(x):
    return math.comb(n1, x) * math.comb(n2, k - x) / math.comb(N, k)
p_obs = hyp(a)
p = sum(hyp(x) for x in range(max(0, k - n2), min(n1, k) + 1) if hyp(x) <= p_obs * (1 + 1e-9))
odds = (a / (n1 - a)) / (c / (n2 - c)) if a and n1 - a and c and n2 - c else None
out["l3"] = {"greedy": [a, n1], "diverse": [c, n2], "fisher_two_sided_p": p, "odds_ratio": odds}
json.dump(out, open("arm_l_residuals.json", "w", encoding="utf-8"), indent=1)
print(json.dumps(out["pooled"]), "\nL3", out["l3"])
for lin, d in out["lineages"].items():
    print(lin, d)
