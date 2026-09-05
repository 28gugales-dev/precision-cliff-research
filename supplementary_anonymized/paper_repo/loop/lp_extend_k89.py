# A round-4 reviewer found that section 1.1's "Every closed-form value is recomputed ...
# every k in 2...7" does not cover the k at which two arms registered: arm M's T(8,57) is
# k=8, and arm CN's predictions span k = 7, 8 and 9. The claim was false as written.
#
# This extends the existing oracle to k = 8 and 9 rather than scoping the claim down. The LP
# is the study's own: it takes the constructed coordinates and maximizes the sum of radii
# subject to containment and pairwise non-overlap, knowing nothing about the recipe. If the
# recipe value and the LP optimum agree at these k too, the sentence becomes true.
import json
import sys
from pathlib import Path

SRC = Path(r"~\AppData\Local\hermes\research-corpus\precision-cliff")
OUT = Path(__file__).resolve().parent.parent / "evidence" / "lp_extend_k89.json"
sys.path.insert(0, str(SRC))

from n_sweep_forecast import (  # noqa: E402
    recipe_value, truncated_value, max_fillers, recipe_coords, lp_sum_of_radii)

TOL = 1e-9
rows = []
for k in (8, 9):
    mmax = max_fillers(k)
    # Both branches at each k: the truncated grid below k^2, and the filler extension above.
    for m in range(0, mmax + 1):
        n = k * k + m
        centres = recipe_coords(k, m, n)
        if centres is None:
            continue
        want = recipe_value(k, m)
        got = lp_sum_of_radii(centres)
        rows.append({"k": k, "m": m, "N": n, "branch": "V", "recipe": want,
                     "lp": got, "drift": abs(want - got)})
    for n in range(k * k - k + 1, k * k):
        centres = recipe_coords(k, 0, n)
        if centres is None:
            continue
        want = truncated_value(k, n)
        got = lp_sum_of_radii(centres)
        rows.append({"k": k, "m": 0, "N": n, "branch": "T", "recipe": want,
                     "lp": got, "drift": abs(want - got)})

worst = max((r["drift"] for r in rows), default=0.0)
bad = [r for r in rows if r["drift"] > TOL]
report = {"tolerance": TOL, "configurations": len(rows), "k_values": [8, 9],
          "worst_drift": worst, "disagreements": len(bad),
          "registered_cells_now_covered": ["arm M T(8,57)", "arm CN T(8,58)",
                                           "arm CN T(8,62)", "arm CN V(8,1)",
                                           "arm CN T(9,75)"]}
OUT.write_text(json.dumps(report, indent=1), encoding="utf-8")

print(f"configurations checked at k = 8, 9: {len(rows)}")
print(f"worst drift: {worst:.3e}  (tolerance {TOL:.0e})")
print("disagreements:", len(bad) if bad else "none")
for r in bad:
    print(f"  k={r['k']} m={r['m']} N={r['N']} recipe={r['recipe']:.10f} lp={r['lp']:.10f}")
print(f"\nwrote {OUT}")
