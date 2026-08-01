# ============================================================================
# Second domain for the template-anchoring forecast: 1 x a rectangles.
#
# WHY THIS EXISTS. n_sweep_forecast.py established, and arm_f_repro.py confirmed
# out of sample, that in the UNIT SQUARE the proposer anchors on the nearest
# square template k* = round(sqrt(N)) and TRUNCATES it when k*^2 > N, instead of
# dropping to k-1 and adding fillers. One benchmark, one objective - the single
# biggest hole in the result. This file tests whether the same rule survives a
# structurally different container.
#
# WHY A RECTANGLE IS A REAL TEST, not the same problem in a hat. In a square the
# template has ONE free parameter (k). In a 1 x a rectangle it has TWO (p rows,
# q columns) and the correct choice depends on a. The rule has to be restated:
#
#     q* = round(sqrt(N / a))          columns across the width 1
#     p* = round(sqrt(N * a))          rows across the height a
#
# At a = 1 both collapse to round(sqrt(N)), so this is the SAME rule with the
# aspect ratio put back in, not a new rule fitted to new data. It can fail, and
# failure is the informative outcome: it would mean square-container anchoring
# was a coincidence of the 1-parameter case.
#
# GEOMETRY. With hx = 1/(2q) and hy = a/(2p) the grid circles are capped at
# r = min(hx, hy), and a filler dropped on an interior vertex is capped by three
# separate things - the diagonal gap to the four surrounding grid circles, and
# the horizontal and vertical spacing to its neighbouring fillers:
#
#     rf = min( sqrt(hx^2 + hy^2) - r,  hx,  hy )
#
# The second and third terms are inactive in the unit square (where hx = hy) and
# become binding as a moves away from 1 - which is exactly why the square case
# could not have revealed them. Every value below is nonetheless recomputed by
# an LP over the actual coordinates, which knows none of this, and the script
# aborts on any disagreement.
# ============================================================================
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parent
ASPECTS = (1.0, 1.5, 2.0, 3.0)
N_LO, N_HI = 10, 45


def half_spacings(p, q, a):
    return 1.0 / (2.0 * q), a / (2.0 * p)


def grid_radius(p, q, a):
    hx, hy = half_spacings(p, q, a)
    return min(hx, hy)


def full_grid_value(p, q, a):
    """Exact when m = 0: every circle is capped at min(hx, hy)."""
    return p * q * grid_radius(p, q, a)


def square_recipe_value(k, m):
    """n_sweep_forecast.py's unit-square closed form, imported by re-derivation.

    Used ONLY as a cross-domain check: at a = 1 with p = q = k this must equal
    the LP. Two files, two derivations, one number.
    """
    return k / 2.0 + m * (math.sqrt(2.0) - 1.0) / (2.0 * k)


_LP_CACHE = {}


def recipe_value(p, q, m, a):
    """Value of the extend branch, from the LP over the actual coordinates.

    NO closed form is used here, and that is a result rather than a shortcut.
    In the unit square every filler sits on a vertex whose four neighbours are
    identical, so one formula covers all of them. In a rectangle a filler is
    capped by three competing things - the diagonal gap to the grid circles, and
    the horizontal and vertical spacing to ADJACENT fillers - and the last two
    only bind when those neighbouring vertices are actually occupied. So the cap
    depends on m and on which vertices the construction happens to use, and no
    single expression in (p, q, m, a) reproduces it. Caught by the LP gate: at
    a=1, p=2, q=4, m=1 a naive unconditional min(diag, hx, hy) gives 1.125 while
    the true value is 1.1545085, because with one filler placed there is no
    neighbouring filler to cap against.
    """
    key = (p, q, m, a)
    if key not in _LP_CACHE:
        _LP_CACHE[key] = lp_sum_of_radii(coords(p, q, m, p * q + m, a), a)
    return _LP_CACHE[key]


def truncated_value(p, q, n, a):
    return n * grid_radius(p, q, a)


def max_fillers(p, q):
    return (p - 1) * (q - 1)


def coords(p, q, m, n, a):
    cells = [((j + 0.5) / q, a * (i + 0.5) / p) for i in range(p) for j in range(q)]
    if n < p * q:
        return cells[:n]
    verts = [(j / q, a * i / p) for i in range(1, p) for j in range(1, q)]
    return cells + verts[:m]


def lp_sum_of_radii(pts, a):
    pts = np.asarray(pts, dtype=float)
    n = len(pts)
    walls = np.minimum.reduce([pts[:, 0], 1.0 - pts[:, 0], pts[:, 1], a - pts[:, 1]])
    if np.any(walls <= 0):
        return 0.0
    if n < 2:
        return float(walls.sum())
    rows, rhs = [], []
    for i in range(n):
        for j in range(i + 1, n):
            row = np.zeros(n)
            row[i] = row[j] = 1.0
            rows.append(row)
            rhs.append(float(np.hypot(*(pts[i] - pts[j]))))
    res = linprog(c=-np.ones(n), A_ub=np.array(rows), b_ub=np.array(rhs),
                  bounds=[(0.0, w) for w in walls], method="highs")
    return float(-res.fun) if res.success else 0.0


def verify(tol=1e-9, cap=30):
    """Three independent checks against the LP. Abort on any drift.

    1. full grid, m = 0, every aspect  - closed form p*q*min(hx,hy)
    2. truncated grid                  - closed form n*min(hx,hy)
    3. CROSS-DOMAIN: at a = 1 with p = q = k, the unit-square closed form from
       n_sweep_forecast.py must reproduce this file's LP. This is the check that
       ties the two domains together - if the rectangle machinery disagreed with
       the square machinery at their shared boundary, everything downstream
       would be suspect.
    """
    checks = 0
    for a in ASPECTS:
        for p in range(2, 7):
            for q in range(2, 7):
                if p * q > cap:
                    continue
                want, got = full_grid_value(p, q, a), lp_sum_of_radii(coords(p, q, 0, p * q, a), a)
                if abs(want - got) > tol:
                    sys.exit(f"ABORT full a={a} p={p} q={q}: {want!r} vs LP {got!r}")
                checks += 1
                n = p * q - 1
                if n >= 2:
                    want, got = truncated_value(p, q, n, a), lp_sum_of_radii(coords(p, q, 0, n, a), a)
                    if abs(want - got) > tol:
                        sys.exit(f"ABORT trunc a={a} p={p} q={q} n={n}: {want!r} vs LP {got!r}")
                    checks += 1
    for k in range(2, 6):
        for m in range(0, min(max_fillers(k, k), 6) + 1):
            want = square_recipe_value(k, m)
            got = lp_sum_of_radii(coords(k, k, m, k * k + m, 1.0), 1.0)
            if abs(want - got) > tol:
                sys.exit(f"ABORT cross-domain k={k} m={m}: square form {want!r} vs rect LP {got!r}")
            checks += 1
    return checks


def branch(p, q, n, a):
    if p < 1 or q < 1:
        return None
    if n < p * q:
        return truncated_value(p, q, n, a), "truncate", 0
    m = n - p * q
    if m > max_fillers(p, q):
        return None
    return recipe_value(p, q, m, a), "extend", m


def predicted(n, a):
    q = max(1, int(math.floor(math.sqrt(n / a) + 0.5)))
    p = max(1, int(math.floor(math.sqrt(n * a) + 0.5)))
    b = branch(p, q, n, a)
    if b is None:
        return {"p": p, "q": q, "value": None, "branch": "unfittable", "m": None}
    return {"p": p, "q": q, "value": b[0], "branch": b[1], "m": b[2]}


def best(n, a, hi=14):
    out = None
    for p in range(1, hi + 1):
        for q in range(1, hi + 1):
            b = branch(p, q, n, a)
            if b is None:
                continue
            if out is None or b[0] > out[0]:
                out = (b[0], p, q, b[1], b[2])
    return out


def main():
    print(f"closed form vs independent LP: {verify()} configurations, drift < 1e-9")
    rows = []
    for a in ASPECTS:
        for n in range(N_LO, N_HI + 1):
            pr, bs = predicted(n, a), best(n, a)
            gap = None if (pr["value"] is None or bs is None) else bs[0] - pr["value"]
            rows.append({
                "a": a, "n": n, "p": pr["p"], "q": pr["q"], "branch": pr["branch"],
                "m": pr["m"], "predicted": pr["value"],
                "best": None if bs is None else bs[0],
                "best_p": None if bs is None else bs[1],
                "best_q": None if bs is None else bs[2],
                "best_branch": None if bs is None else bs[3],
                "gap": gap,
                "gap_pct": None if not gap else 100.0 * gap / bs[0],
                "shape_differs": bs is not None and (pr["p"], pr["q"]) != (bs[1], bs[2]),
            })

    for a in ASPECTS:
        sub = [r for r in rows if r["a"] == a]
        traps = [r for r in sub if r["branch"] == "truncate"]
        diff = [r for r in sub if r["shape_differs"]]
        print(f"\na={a}:  {len(traps)}/{len(sub)} N predicted to truncate, "
              f"{len(diff)} where predicted shape != optimal shape")
        top = sorted([r for r in sub if r["gap"]], key=lambda r: -r["gap"])[:4]
        for r in top:
            print(f"   N={r['n']:>3}  pred ({r['p']}x{r['q']},{r['branch']}) "
                  f"{r['predicted']:.6f}   opt ({r['best_p']}x{r['best_q']},"
                  f"{r['best_branch']}) {r['best']:.6f}   gap {r['gap']:.6f} "
                  f"({r['gap_pct']:.1f}%)")

    disc = sorted([r for r in rows if r["gap"] and r["a"] != 1.0],
                  key=lambda r: -r["gap_pct"])[:8]
    print("\nDISCRIMINATING CELLS to probe (a != 1, largest relative gap):")
    for r in disc:
        print(f"   a={r['a']}  N={r['n']:>3}  predict {r['predicted']:.6f} "
              f"({r['p']}x{r['q']} {r['branch']})   rival {r['best']:.6f} "
              f"({r['best_p']}x{r['best_q']} {r['best_branch']})   {r['gap_pct']:.1f}%")

    (ROOT / "rect_forecast.json").write_text(json.dumps(
        {"aspects": list(ASPECTS), "rows": rows,
         "rule": "q*=round(sqrt(N/a)), p*=round(sqrt(N*a)); reduces to round(sqrt(N)) at a=1"},
        indent=2))
    print(f"\nwrote {ROOT / 'rect_forecast.json'}")


if __name__ == "__main__":
    main()
