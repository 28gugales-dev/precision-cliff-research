# A round-4 reviewer showed the arm-CH control is conditioned on a collider: both sides of
# the 3/7-against-30/30 contrast condition on invalidity, whose base rate differs enormously
# between the arms (CH 69 percent invalid, arm F 17 percent at the same cells). The odds
# ratio is then not interpretable as an effect of the manipulation, whatever its p-value.
#
# The unconditioned contrast conditions on nothing and is already in the ledgers: over ALL
# evaluable rows at the same three cells, how often does each arm reach for the argmax order?
import json
from collections import Counter
from math import comb
from pathlib import Path

SRC = Path(r"~\AppData\Local\hermes\research-corpus\precision-cliff")
OUT = Path(__file__).resolve().parent.parent / "evidence" / "arm_f_attempt_uncond.json"

CELLS = (13, 21, 31)
KSTAR = {13: 4, 21: 5, 31: 6}   # argmax order is k* - 1 at each of these trap cells


def dominant_k(circles):
    radii = [round(c[2], 6) for c in circles]
    if not radii:
        return None
    r_dom, _ = Counter(radii).most_common(1)[0]
    return round(1.0 / (2.0 * r_dom)) if r_dom > 0 else None


# --- arm F: every bare row at the three cells, valid and invalid alike -------
rows = [json.loads(l) for l in
        (SRC / "arm_f_candidates_v2.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
bare = [r for r in rows if r.get("arm") == "bare" and r.get("n") in CELLS]
f_eval, f_argmax = 0, 0
per_cell = {}
for n in CELLS:
    sel = [r for r in bare if r["n"] == n]
    ks = [dominant_k(r["circles"]) for r in sel if r.get("circles")]
    ks = [k for k in ks if k is not None]
    hit = sum(1 for k in ks if k == KSTAR[n] - 1)
    per_cell[str(n)] = {"rows": len(sel), "evaluable": len(ks), "at_argmax_order": hit}
    f_eval += len(ks)
    f_argmax += hit

# --- arm CH: 36 of 45 invocations reach the argmax order, one row unevaluable -
CH_ARGMAX, CH_EVAL = 36, 44


def fisher_greater(a, b, c, d):
    row1, row2, col1, tot = a + b, c + d, a + c, a + b + c + d
    return sum(comb(row1, x) * comb(row2, col1 - x) / comb(tot, col1)
               for x in range(0, min(row1, col1) + 1)
               if 0 <= col1 - x <= row2 and x <= a)


p = fisher_greater(f_argmax, f_eval - f_argmax, CH_ARGMAX, CH_EVAL - CH_ARGMAX)
report = {
    "cells": list(CELLS), "per_cell": per_cell,
    "arm_F_unconditioned": [f_argmax, f_eval],
    "arm_CH_unconditioned": [CH_ARGMAX, CH_EVAL],
    "fisher_one_sided_p": p,
    "note": ("conditions on nothing downstream of the manipulation, unlike the invalid-row "
             "contrast it replaces; still a post-hoc comparison"),
}
OUT.write_text(json.dumps(report, indent=1), encoding="utf-8")

print("reaching for the argmax grid order, all evaluable rows at N = 13, 21, 31")
print(f"  arm F  (no score table)   {f_argmax}/{f_eval} = {f_argmax/f_eval:.0%}")
print(f"  arm CH (score table)     {CH_ARGMAX}/{CH_EVAL} = {CH_ARGMAX/CH_EVAL:.0%}")
print(f"  Fisher exact, one-sided  p = {p:.2e}")
print(f"\nper cell (arm F): {per_cell}")
print(f"wrote {OUT}")
