# Reviewer 1's objection O3: the ceiling accounting reports arm L's 49 conditioned
# outputs and omits arm MU's, which is the larger conditioned corpus. This script
# answers it from arm MU's frozen scored rows.
#
# The family argmax is recomputed from the closed form here rather than read from a
# literal, so a wrong seven-decimal constant in the analysis script cannot manufacture
# or hide an excess. Both validity tolerances are reported, because the answer differs
# between them and the difference is the finding.
import json
import math
from pathlib import Path

SRC = Path(r"~\AppData\Local\hermes\research-corpus\precision-cliff"
           r"\arm_mu_scored.json")
OUT = Path(__file__).resolve().parent.parent / "evidence" / "arm_mu_ceiling.json"

R2 = math.sqrt(2.0) - 1.0


def family_argmax(N):
    """Best value the grid-plus-filler family can express at N, over all orders k.

    A k-grid places k^2 circles of radius 1/(2k) and up to (k-1)^2 filler circles of
    radius (sqrt2-1)/(2k) in the interstices. When k^2 > N the grid is truncated and
    the value is N/(2k). Ties are resolved by taking the max, so this is an upper
    bound on anything the family can produce.
    """
    best, best_k, best_m = 0.0, None, None
    for k in range(1, N + 1):
        if k * k > N:
            v, m = N / (2.0 * k), 0
        else:
            m = min(N - k * k, (k - 1) ** 2)
            v = k / 2.0 + m * R2 / (2.0 * k)
        if v > best:
            best, best_k, best_m = v, k, m
    return best, best_k, best_m


# The scored file carries arm MU's three parent conditions and arm CH's choice condition
# in one ledger. The paper accounts for them as separate arms (MU is 135 invocations, CH
# is 45), so they are kept apart here too.
MU_CONDITIONS = ("A_anchor", "B_rival", "C_offfamily")

rows = json.loads(SRC.read_text(encoding="utf-8"))
cells = sorted({r["cell"] for r in rows})
conds = sorted({r["condition"] for r in rows})
argmax = {n: family_argmax(n) for n in cells}

TOL = 1e-6  # the arm's own primary validity tolerance, reused as the excess margin

report = {"source": SRC.name, "family_argmax": {}, "cells": {}, "pooled": {}}
for n in cells:
    v, k, m = argmax[n]
    report["family_argmax"][str(n)] = {"value": v, "k": k, "m": m}

tot = {"valid6": 0, "valid9": 0, "above6_strict": 0, "above6_margin": 0, "above9": 0}
for c in conds:
    for n in cells:
        sel = [r for r in rows if r["condition"] == c and r["cell"] == n]
        v6 = [r for r in sel if r.get("valid6")]
        v9 = [r for r in sel if r.get("valid9")]
        a = argmax[n][0]
        strict = [r for r in v6 if r["sum"] > a]
        margin = [r for r in v6 if r["sum"] > a + TOL]
        above9 = [r for r in v9 if r["sum"] > a]
        report["cells"][f"{c}_N{n}"] = {
            "invocations": len(sel), "valid6": len(v6), "valid9": len(v9),
            "above_argmax_strict": len(strict), "above_argmax_margin": len(margin),
            "above_argmax_valid9": len(above9),
            "max_valid6": max((r["sum"] for r in v6), default=None),
            "max_excess": max((r["sum"] - a for r in strict), default=0.0),
        }
        tot["valid6"] += len(v6)
        tot["valid9"] += len(v9)
        tot["above6_strict"] += len(strict)
        tot["above6_margin"] += len(margin)
        tot["above9"] += len(above9)

"""Bucket every nominal excess.

Sums are recorded to seven decimals, so a row can sit above an argmax whose exact
value is irrational by as much as 5e-8 purely from the rounding of its own recorded
sum. Those rows are the argmax, written down. Separating them from real excesses is
the whole question, so the split is computed rather than asserted.
"""
ROUNDING = 5e-8
over = [r for r in rows if r.get("valid6") and r["sum"] > argmax[r["cell"]][0]]
excesses = [r["sum"] - argmax[r["cell"]][0] for r in over]
rounding_only = [r for r in over if r["sum"] - argmax[r["cell"]][0] <= ROUNDING]
real = [r for r in over if r["sum"] - argmax[r["cell"]][0] > ROUNDING]
report["excess_buckets"] = {
    "recorded_sum_granularity": ROUNDING,
    "within_rounding": len(rounding_only),
    "within_rounding_valid9": sum(1 for r in rounding_only if r.get("valid9")),
    "beyond_rounding": len(real),
    "beyond_rounding_valid9": sum(1 for r in real if r.get("valid9")),
}
report["pooled"] = dict(tot, invocations=len(rows),
                        largest_excess=max(excesses, default=0.0),
                        every_real_excess_fails_valid9=all(
                            not r.get("valid9") for r in real))

def slice_totals(conditions):
    sel = [r for r in rows if r["condition"] in conditions]
    v6 = [r for r in sel if r.get("valid6")]
    v9 = [r for r in sel if r.get("valid9")]
    a = lambda r: argmax[r["cell"]][0]
    over_s = [r for r in v6 if r["sum"] > a(r)]
    real_s = [r for r in over_s if r["sum"] - a(r) > ROUNDING]
    return {
        "invocations": len(sel), "valid6": len(v6), "valid9": len(v9),
        "nominally_above": len(over_s),
        "above_within_rounding": len(over_s) - len(real_s),
        "above_beyond_rounding": len(real_s),
        "above_beyond_rounding_valid9": sum(1 for r in real_s if r.get("valid9")),
        "largest_excess": max((r["sum"] - a(r) for r in over_s), default=0.0),
    }


report["by_arm"] = {"MU": slice_totals(MU_CONDITIONS), "CH": slice_totals(("CH",))}

"""Arm CH's attempt-level reading, recomputed at the grid order rather than the filler radius.

The paper originally classified the 31 invalid CH attempts by "the family's filler radius",
which does not identify which order was attempted. The emitted order is recorded per row as
k_emp, so the stronger statement -- the attempts carry the argmax's own order -- is
checkable, and is what section 3.5 now claims.
"""
ch_invalid = [r for r in rows if r["condition"] == "CH" and not r.get("valid6")]
ch = {"invalid_attempts": len(ch_invalid), "by_cell": {}, "at_argmax_order": 0,
      "unevaluable": 0}
for n in cells:
    sel = [r for r in ch_invalid if r["cell"] == n]
    k_arg = argmax[n][1]
    hit = sum(1 for r in sel if r.get("k_emp") == k_arg)
    none = sum(1 for r in sel if r.get("k_emp") is None)
    ch["by_cell"][str(n)] = {"invalid": len(sel), "argmax_order": k_arg,
                            "at_argmax_order": hit, "unevaluable": none}
    ch["at_argmax_order"] += hit
    ch["unevaluable"] += none
"""How often the model actually BUILDS the argmax it was handed.

A round-2 reviewer showed that "cannot build it" is contradicted by the paper's own
tables -- at N=21 the argmax is the modal valid output. The attempt-level and build-level
rates are both computable, so both are computed here rather than characterized in prose.
"""
ch_valid = [r for r in rows if r["condition"] == "CH" and r.get("valid6")]
built = [r for r in ch_valid if r.get("on_argmax")]
ch["valid"] = len(ch_valid)
ch["built_argmax"] = len(built)
ch["invocations"] = sum(1 for r in rows if r["condition"] == "CH")
ch["attempted_argmax"] = ch["at_argmax_order"] + len(built)
ch["built_by_cell"] = {
    str(n): [sum(1 for r in built if r["cell"] == n),
             sum(1 for r in ch_valid if r["cell"] == n)] for n in cells}
report["arm_CH_attempts"] = ch

OUT.write_text(json.dumps(report, indent=1), encoding="utf-8")

for label, t in report["by_arm"].items():
    print(f"arm {label}: {t['invocations']} invocations, "
          f"valid {t['valid6']} at 1e-6 and {t['valid9']} at 1e-9; "
          f"{t['above_beyond_rounding']} above the argmax beyond recorded-sum rounding, "
          f"of which {t['above_beyond_rounding_valid9']} survive 1e-9 "
          f"(largest excess {t['largest_excess']:.2e})")
print()

for n in cells:
    v, k, m = argmax[n]
    print(f"N={n:3d} family argmax {v:.9f}  (k={k}, m={m})")
print()
print(f"invocations                          {len(rows)}")
print(f"valid at 1e-6                        {tot['valid6']}")
print(f"  strictly above the family argmax   {tot['above6_strict']}")
print(f"  above it by more than 1e-6         {tot['above6_margin']}")
print(f"  largest excess                     {max(excesses, default=0.0):.2e}")
print(f"valid at 1e-9                        {tot['valid9']}")
print(f"  above the family argmax            {tot['above9']}")
b = report["excess_buckets"]
print(f"\nof the {len(over)} rows nominally above the argmax:")
print(f"  within recorded-sum rounding (<={ROUNDING:.0e})  {b['within_rounding']}"
      f"  (valid at 1e-9: {b['within_rounding_valid9']})")
print(f"  beyond it                                {b['beyond_rounding']}"
      f"  (valid at 1e-9: {b['beyond_rounding_valid9']})")
print(f"every real excess fails 1e-9         "
      f"{report['pooled']['every_real_excess_fails_valid9']}")
print(f"\nwrote {OUT}")
