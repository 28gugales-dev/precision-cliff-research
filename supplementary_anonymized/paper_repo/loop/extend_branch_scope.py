# A round-3 reviewer's strongest objection, checked rather than accepted.
#
# The claim: every discriminating cell is a trap cell by construction, so the extend branch
# -- the one the abstract says "survives at m <= 1" -- has no discriminating evidence
# anywhere in the study. If true, the paper's falsifiable in-family content reduces to the
# truncate arm, and the abstract must say so.
#
# This exhausts the sweep range and reports what it finds, including the nuance the
# objection understates: an extend cell cannot separate anchoring from in-family search,
# but it can still separate anchoring from OUT-of-family behaviour, which is exactly what
# arm M's falsifier tested and what killed the branch at m >= 4.
import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "evidence" / "extend_branch_scope.json"
R2 = math.sqrt(2.0) - 1.0
SWEEP = range(10, 81)  # the paper's stated sweep bound is N = 10..60; 80 overshoots on purpose


def family_argmax(N):
    best = (0.0, None, None)
    for k in range(1, N + 1):
        if k * k > N:
            v, m = N / (2.0 * k), 0
        else:
            m = min(N - k * k, (k - 1) ** 2)
            v = k / 2.0 + m * R2 / (2.0 * k)
        if v > best[0]:
            best = (v, k, m)
    return best


def prediction(N):
    """The registered rule: nearest-square order, truncate above it, extend below."""
    ks = round(math.sqrt(N))
    if ks * ks > N:
        return N / (2.0 * ks), "T", ks, 0
    m = min(N - ks * ks, (ks - 1) ** 2)
    return ks / 2.0 + m * R2 / (2.0 * ks), "V", ks, m


rows = []
for N in SWEEP:
    p, branch, ks, m = prediction(N)
    a, ak, am = family_argmax(N)
    rows.append({"N": N, "branch": branch, "m": m, "prediction": p, "argmax": a,
                 "discriminating": abs(p - a) > 1e-12})

extend = [r for r in rows if r["branch"] == "V"]
truncate = [r for r in rows if r["branch"] == "T"]
extend_disc = [r for r in extend if r["discriminating"]]
truncate_disc = [r for r in truncate if r["discriminating"]]

report = {
    "sweep": [SWEEP.start, SWEEP.stop - 1],
    "extend_cells": len(extend),
    "extend_cells_discriminating": len(extend_disc),
    "truncate_cells": len(truncate),
    "truncate_cells_discriminating": len(truncate_disc),
    "objection_holds": len(extend_disc) == 0,
    "extend_cells_sampled_in_paper": [17, 37, 50, 65],
    "note": ("At an extend cell the registered prediction IS the family argmax, so an "
             "on-prediction result there cannot separate anchoring from in-family search. "
             "It can still separate anchoring from out-of-family behaviour, which is what "
             "arm M's F-M1 tested at m >= 4 and what disconfirmed the branch there."),
}
OUT.write_text(json.dumps(report, indent=1), encoding="utf-8")

print(f"sweep N = {SWEEP.start}..{SWEEP.stop - 1}")
print(f"extend cells   {len(extend):3d}, of which discriminating {len(extend_disc)}")
print(f"truncate cells {len(truncate):3d}, of which discriminating {len(truncate_disc)}")
print()
if extend_disc:
    print("the objection FAILS; discriminating extend cells exist:",
          [r["N"] for r in extend_disc])
else:
    print("the objection HOLDS: no extend cell in the sweep is discriminating.")
    print("Every cell where prediction and family argmax differ is a truncate cell.")
print(f"\nwrote {OUT}")
