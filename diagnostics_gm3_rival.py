# Post-hoc structural diagnostic (NOT preregistered; disclosed as such in
# section 3.6): do arm GM3's rival-valued packings carry the rival
# CONSTRUCTION, not merely its value?
#
# The registered two-radius signature in arm_gm3_analysis.py is scoped to
# the PREDICTED order k*(N) (rg = 1/(2k*), rf = (sqrt(2)-1)/(2k*)), so it
# is structurally blind to the rival V(k*-1, m), whose radii use k*-1.
# This script re-runs the same two-radius-group test against the rival's
# radii on every valid row within 2e-3 of the rival value.
#
# Reads arm_gm3_candidates.jsonl. Read-only. No arguments.
import ast
import json
import math
import re

RIVALS = {13: (1.7761424, 3), 21: (2.2588835, 4), 31: (2.7485281, 5)}
PRED = {13: 1.6250000, 21: 2.1000000, 31: 2.5833333}

rows = [json.loads(l) for l in open("arm_gm3_candidates.jsonl", encoding="utf-8")]

tot_valid = tot_onpred = tot_rival = tot_rival_structured = 0
for n, (rv, k) in RIVALS.items():
    rg, rf = 1 / (2 * k), (math.sqrt(2) - 1) / (2 * k)
    valid = [x for x in rows if x["n"] == n and x["valid_1e6"]]
    onpred = [x for x in valid if abs(x["sum"] - PRED[n]) <= 2e-3]
    rival = [x for x in valid if abs(x["sum"] - rv) <= 2e-3]
    structured = 0
    for x in rival:
        m = re.search(r"\[\s*\[.*\]\s*\]", x["raw_text"], re.S)
        try:
            circles = ast.literal_eval(m.group(0))
        except Exception:
            continue
        groups = []
        for rad in sorted({round(c[2], 6) for c in circles}):
            for g in groups:
                if abs(g - rad) <= 1e-3:
                    break
            else:
                groups.append(rad)
        if (len(groups) == 2
                and any(abs(g - rg) <= 1e-3 for g in groups)
                and any(abs(g - rf) <= 1e-3 for g in groups)):
            structured += 1
    tot_valid += len(valid)
    tot_onpred += len(onpred)
    tot_rival += len(rival)
    tot_rival_structured += structured
    print(f"N={n}: valid={len(valid)} on_prediction={len(onpred)} "
          f"rival_valued={len(rival)} rival_structured={structured} "
          f"(rival k={k}: rg={rg:.7f} rf={rf:.7f})")

print(f"discriminating cells pooled: on_prediction {tot_onpred}/{tot_valid}, "
      f"rival_valued {tot_rival}/{tot_valid}, "
      f"rival_structured {tot_rival_structured}/{tot_rival}")
