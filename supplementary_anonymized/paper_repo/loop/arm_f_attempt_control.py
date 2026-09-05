# The control arm 3.5's attempt-level reading never had.
#
# Arm CH hands the model the higher-valued rival with its score, and 30 of the 31 invalid
# attempts come back at the rival's own grid order k*-1. The paper reads that as the model
# selecting the argmax and failing to build it. A round-2 reviewer pointed out the missing
# comparison: if the BARE arm's invalid rows also come back at k*-1, with no score table in
# the prompt, then the CH reading is uncontrolled and 30/31 says nothing about selection.
#
# Same estimator as diagnostics_kmatch.py -- back the order out of the dominant radius,
# r_main = 1/(2k) -- applied to invalid rows instead of valid ones.
import json
from collections import Counter
from pathlib import Path

SRC = Path(r"~\AppData\Local\hermes\research-corpus\precision-cliff"
           r"\arm_f_candidates_v2.jsonl")
OUT = Path(__file__).resolve().parent.parent / "evidence" / "arm_f_attempt_control.json"

KSTAR = {13: 4, 17: 4, 21: 5, 31: 6, 35: 6, 37: 6, 43: 7}
# Arm CH ran at these three cells; the comparison is only meaningful on the same ones.
CH_CELLS = (13, 21, 31)


def dominant_k(circles):
    radii = [round(c[2], 6) for c in circles]
    if not radii:
        return None
    r_dom, _ = Counter(radii).most_common(1)[0]
    return round(1.0 / (2.0 * r_dom)) if r_dom > 0 else None


rows = [json.loads(l) for l in SRC.read_text(encoding="utf-8").splitlines() if l.strip()]
bare = [r for r in rows if r.get("arm") == "bare" and r.get("n") in KSTAR]
invalid = [r for r in bare if not r.get("valid")]

report = {"source": SRC.name, "estimator": "dominant radius, r_main = 1/(2k)",
          "cells": {}, "ch_cells": list(CH_CELLS)}
tot = Counter()
for n in sorted(KSTAR):
    sel = [r for r in invalid if r["n"] == n]
    ks = [dominant_k(r["circles"]) for r in sel if r.get("circles")]
    at_anchor = sum(1 for k in ks if k == KSTAR[n])
    at_rival = sum(1 for k in ks if k == KSTAR[n] - 1)
    other = sum(1 for k in ks if k is not None and k not in (KSTAR[n], KSTAR[n] - 1))
    unevaluable = len(sel) - len(ks) + sum(1 for k in ks if k is None)
    report["cells"][str(n)] = {
        "invalid": len(sel), "kstar": KSTAR[n],
        "at_anchor_order": at_anchor, "at_rival_order": at_rival,
        "at_other_order": other, "unevaluable": unevaluable,
        "k_distribution": dict(Counter(k for k in ks if k is not None)),
    }
    if n in CH_CELLS:
        tot["invalid"] += len(sel)
        tot["anchor"] += at_anchor
        tot["rival"] += at_rival
        tot["other"] += other
        tot["unevaluable"] += unevaluable

report["pooled_over_ch_cells"] = dict(tot)
evaluable = tot["anchor"] + tot["rival"] + tot["other"]
report["pooled_over_ch_cells"]["evaluable"] = evaluable
report["rival_order_rate_bare"] = (tot["rival"] / evaluable) if evaluable else None
# Arm CH's own figure, for the contrast the reviewer asked for.
report["rival_order_rate_ch"] = 30 / 30

"""Contrast the two arms on the same three cells.

Fisher's exact test on the 2x2 of (arm) x (attempted order is the rival's), computed from
the hypergeometric tail directly so this script depends on nothing. The bare arm has few
invalid rows -- arm F is mostly valid, which is the whole reason arm CH exists -- so the
control is small and the interval is wide. Reported as it comes out.
"""
from math import comb

ch_rival, ch_n = 30, 30
a, b = tot["rival"], evaluable - tot["rival"]      # bare: rival order, other order
c, d = ch_rival, ch_n - ch_rival                   # CH: same


def fisher_greater(a, b, c, d):
    """One-sided P(as or more extreme in the direction of a higher CH rate)."""
    row1, row2 = a + b, c + d
    col1, tot_n = a + c, a + b + c + d
    p = 0.0
    for x in range(0, min(row1, col1) + 1):
        if col1 - x > row2:
            continue
        term = comb(row1, x) * comb(row2, col1 - x) / comb(tot_n, col1)
        if x <= a:
            p += term
    return p


p_one_sided = fisher_greater(a, b, c, d)
report["contrast"] = {
    "bare_invalid_at_rival_order": [a, evaluable],
    "ch_invalid_at_rival_order": [ch_rival, ch_n],
    "fisher_one_sided_p": p_one_sided,
    "note": ("post-hoc, like the CH reading it controls; the bare arm's invalid rows are "
             "few because arm F is mostly valid"),
}

OUT.write_text(json.dumps(report, indent=1), encoding="utf-8")

print("bare-arm invalid rows, grid order backed out of the dominant radius")
print(f"{'N':>4} {'invalid':>8} {'at k*':>7} {'at k*-1':>8} {'other':>6} {'unevaluable':>12}")
for n in sorted(KSTAR):
    c = report["cells"][str(n)]
    print(f"{n:>4} {c['invalid']:>8} {c['at_anchor_order']:>7} {c['at_rival_order']:>8}"
          f" {c['at_other_order']:>6} {c['unevaluable']:>12}   {c['k_distribution']}")
print()
print(f"pooled over the three arm CH cells: {evaluable} evaluable invalid rows, "
      f"{tot['rival']} at the rival order, {tot['anchor']} at the anchor order")
if evaluable:
    print(f"bare arm attempts the rival order in {tot['rival']}/{evaluable} "
          f"= {tot['rival']/evaluable:.0%} of evaluable invalid rows")
    print(f"arm CH, handed the rival with its score:  30/30 = 100%")
    print(f"Fisher exact, one-sided:                  p = {p_one_sided:.2e}")
print(f"\nwrote {OUT}")
