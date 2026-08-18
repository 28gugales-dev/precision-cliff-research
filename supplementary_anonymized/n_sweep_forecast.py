# ============================================================================
# Precision-cliff Future Work item 3: map the recipe's parameter space.
#
# Paper (S5.10) established, on three data points, that the Claude attractor is
# not a memorised packing but a PARAMETRIC RECIPE:
#
#     k x k grid of circles, r_grid = 1/(2k), one per cell of a unit square,
#     plus m tangent fillers at interior grid vertices, r_fill = (sqrt2-1)/(2k).
#
#     V(k, m) = k^2 * 1/(2k)  +  m * (sqrt2-1)/(2k)
#             = k/2 + m*(sqrt2-1)/(2k),        0 <= m <= (k-1)^2
#
# and that when the count does not reach k^2 the model TRUNCATES the grid rather
# than dropping to k-1 and filling:
#
#     T(k, N) = N / (2k)                       N < k^2
#
# Three anchors from the paper, all reproduced exactly below:
#     N=26  V(5,1) = 2.5414214   (Arm B converged value)
#     N=27  V(5,2) = 2.5828427   (Arm E, H1, six decimals)
#     N=23  T(5,23) = 2.300      (Arm E, H2, the trap, 4/5 seeds)
#     N=23  V(4,7) = 2.3624369   (Arm E, the one escaping seed)
#
# THIS FILE'S JOB is the open extension the paper names: sweep N, decide in
# closed form which N converge and which trap, and say by how much. That turns a
# 3-point observation into a forecast that a later run can falsify.
#
# WHAT IS BEING PREDICTED, precisely: the paper's own account is that the model
# picks ONE k and then either extends it (if k^2 <= N) or truncates it (if
# k^2 > N). The forecast therefore needs a selection rule k*(N). Four candidate
# rules are enumerated in RULES below and scored against the three anchors; only
# one survives. Three anchors is thin evidence and is labelled as such in the
# output - the point is that the surviving rule makes falsifiable predictions at
# every other N, which is what makes it worth running.
#
# VERIFICATION DISCIPLINE (rule 1: no reference is trusted to validate itself)
# Every closed-form value is recomputed by an independent method - an LP over the
# actual constructed coordinates, which knows nothing about the recipe - and the
# script aborts if any pair disagrees. See verify_against_lp().
# ============================================================================
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parent
SQRT2 = math.sqrt(2.0)
FILLER_FACTOR = SQRT2 - 1.0

# Best known sum-of-radii in a unit square, copied verbatim from
# https://erich-friedman.github.io/packing/cirRsqu/ via kink-test/square_family.py.
# Published as 3-decimal LOWER bounds ("2.301+"), so a recipe value ABOVE one of
# these would be a contradiction and is checked for.
PUBLISHED = {
    10: 1.591, 11: 1.680, 12: 1.765, 13: 1.829, 14: 1.905, 15: 1.980,
    16: 2.053, 17: 2.111, 18: 2.178, 19: 2.236, 20: 2.301, 21: 2.362,
    22: 2.420, 23: 2.478, 24: 2.530, 25: 2.587, 26: 2.63598, 27: 2.685,
    28: 2.737, 29: 2.790, 30: 2.842,
}


# ---------------------------------------------------------------- the recipe

def recipe_value(k, m):
    """V(k, m): full k x k grid plus m interior fillers, in a unit square."""
    return k / 2.0 + m * FILLER_FACTOR / (2.0 * k)


def truncated_value(k, n):
    """T(k, n): k x k grid with only n of the k^2 cells occupied."""
    return n / (2.0 * k)


def max_fillers(k):
    """Interior vertices of a k x k cell grid: (k-1)^2 of them."""
    return (k - 1) ** 2


def recipe_coords(k, m, n):
    """Actual circle centres the recipe places, for independent LP checking.

    Grid cell centres row-major, then filler positions at interior vertices,
    also row-major. When n < k^2 this is the TRUNCATED construction and m must
    be 0 - the paper's trap places no fillers.
    """
    cells = [((j + 0.5) / k, (i + 0.5) / k) for i in range(k) for j in range(k)]
    if n < k * k:
        assert m == 0, "truncated construction takes no fillers"
        return cells[:n]
    verts = [(j / k, i / k) for i in range(1, k) for j in range(1, k)]
    return cells + verts[:m]


# ------------------------------------------------- independent LP verifier

def lp_sum_of_radii(centres):
    """Max sum of radii for FIXED centres in the unit square.

    Lifted from kink-test/aspect_family.py (width=height=1). This is the
    independent check: it is a generic optimiser over the coordinates and has no
    knowledge of grids, fillers, or the closed form. If the recipe's closed form
    is right, the LP must return the same number - and if the LP returns MORE,
    the recipe is not even optimal on its own centres, which would itself be a
    finding rather than a bug.
    """
    pts = np.asarray(centres, dtype=float)
    n = len(pts)
    walls = np.minimum.reduce([pts[:, 0], 1.0 - pts[:, 0], pts[:, 1], 1.0 - pts[:, 1]])
    if np.any(walls <= 0):
        return 0.0
    if n < 2:
        # No pair constraints exist, so linprog has nothing to build A_ub from.
        # A lone circle is capped by its nearest wall.
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


def verify_against_lp(max_n=42, tol=1e-9):
    """Recompute every closed form by LP on its own coordinates. Abort on drift.

    Covers both branches (clean fill and truncation) at every k that the sweep
    can reach, and every filler count, not a sampled subset.
    """
    checks = 0
    for k in range(2, 8):
        for m in range(0, max_fillers(k) + 1):
            n = k * k + m
            if n > max_n:
                break
            want = recipe_value(k, m)
            got = lp_sum_of_radii(recipe_coords(k, m, n))
            if abs(want - got) > tol:
                sys.exit(f"ABORT clean k={k} m={m}: closed form {want!r} vs LP {got!r}")
            checks += 1
        for n in range(max(1, (k - 1) ** 2), k * k):
            if n > max_n:
                break
            want = truncated_value(k, n)
            got = lp_sum_of_radii(recipe_coords(k, 0, n))
            if abs(want - got) > tol:
                sys.exit(f"ABORT trunc k={k} n={n}: closed form {want!r} vs LP {got!r}")
            checks += 1
    return checks


ANCHORS = [
    ("N=26 Arm B converged", lambda: recipe_value(5, 1), 2.5414214, 1e-7),
    ("N=27 Arm E H1", lambda: recipe_value(5, 2), 2.5828427, 1e-7),
    ("N=23 Arm E trap", lambda: truncated_value(5, 23), 2.300, 1e-9),
    ("N=23 Arm E escape", lambda: recipe_value(4, 7), 2.3624369, 1e-7),
    ("N=25 bare grid", lambda: recipe_value(5, 0), 2.500, 1e-9),
]


def verify_anchors():
    """The closed form must reproduce every number the paper reports. No fitting."""
    for name, fn, want, tol in ANCHORS:
        got = fn()
        if abs(got - want) > tol:
            sys.exit(f"ABORT anchor {name}: got {got!r}, paper says {want!r}")
    return len(ANCHORS)


# ------------------------------------------------------- the selection rule

def _round_half_away(x):
    return math.floor(x + 0.5)


RULES = {
    # k anchored on the NEAREST square. Extends when k^2 <= N, truncates when not.
    "nearest": lambda n: _round_half_away(math.sqrt(n)),
    # k anchored on the next square up. Always truncates unless N is a square.
    "ceil": lambda n: math.ceil(math.sqrt(n)),
    # k anchored on the largest square that fits. Never truncates.
    "floor": lambda n: math.floor(math.sqrt(n)),
    # k chosen to maximise the resulting value - a rational agent, not this model.
    "argmax": None,  # handled specially in predict()
}


def branch_value(k, n):
    """What the recipe yields at this k and n, and which branch it took.

    Returns (value, branch, m) or None when k cannot host n at all (n exceeds
    grid plus every interior vertex).
    """
    if k < 1:
        return None
    if n < k * k:
        return truncated_value(k, n), "truncate", 0
    m = n - k * k
    if m > max_fillers(k):
        return None
    return recipe_value(k, m), "extend", m


def best_over_k(n, k_hi=12):
    """The best value ANY parameterisation of the recipe reaches at this n."""
    best = None
    for k in range(1, k_hi + 1):
        b = branch_value(k, n)
        if b is None:
            continue
        if best is None or b[0] > best[0]:
            best = (b[0], k, b[1], b[2])
    return best  # (value, k, branch, m)


def predict(n, rule):
    """Forecast for one n under one selection rule."""
    if rule == "argmax":
        v, k, branch, m = best_over_k(n)
        return {"k": k, "value": v, "branch": branch, "m": m}
    k = RULES[rule](n)
    b = branch_value(k, n)
    if b is None:
        # Selected k cannot host n. Under the paper's account the model does not
        # search for another k, so this is a genuine "no natural parameterisation"
        # case rather than something to silently repair.
        return {"k": k, "value": None, "branch": "unfittable", "m": None}
    return {"k": k, "value": b[0], "branch": b[1], "m": b[2]}


def score_rules():
    """Which selection rule survives the three N=23/26/27 anchors?

    Anchor semantics: at N=26 and N=27 the model EXTENDED a 5x5 grid; at N=23 it
    TRUNCATED a 5x5 grid. A rule must reproduce both k and branch at all three.
    """
    observed = {
        26: (5, "extend"),
        27: (5, "extend"),
        23: (5, "truncate"),
    }
    table = {}
    for rule in RULES:
        hits = []
        for n, (want_k, want_branch) in sorted(observed.items()):
            p = predict(n, rule)
            hits.append(p["k"] == want_k and p["branch"] == want_branch)
        table[rule] = {"hits": sum(hits), "of": len(hits),
                       "per_anchor": dict(zip(sorted(observed), hits))}
    return table


# ------------------------------------------------------------------- sweep

def sweep(n_lo=10, n_hi=60, rule="nearest"):
    rows = []
    for n in range(n_lo, n_hi + 1):
        pred = predict(n, rule)
        best = best_over_k(n)
        rec_best = best[0] if best else None
        gap = None if (pred["value"] is None or rec_best is None) else rec_best - pred["value"]
        pub = PUBLISHED.get(n)
        row = {
            "n": n,
            "k_star": pred["k"],
            "branch": pred["branch"],
            "m": pred["m"],
            "predicted": pred["value"],
            "recipe_best": rec_best,
            "recipe_best_k": best[1] if best else None,
            "recipe_best_branch": best[2] if best else None,
            "trap_gap": gap,
            "trap_gap_pct": None if not gap else 100.0 * gap / rec_best,
            "published_best_known": pub,
            "deficit_vs_published": None if (pub is None or pred["value"] is None)
                                    else pub - pred["value"],
            "dist_to_nearest_square": n - pred["k"] ** 2,
            "is_prime": all(n % d for d in range(2, int(math.isqrt(n)) + 1)) and n > 1,
        }
        # A recipe value above a published LOWER bound would mean one of the two
        # is wrong. Never silently.
        if pub is not None and row["predicted"] is not None and row["predicted"] > pub:
            sys.exit(f"ABORT n={n}: predicted {row['predicted']!r} exceeds "
                     f"published lower bound {pub!r} - recheck the recipe.")
        rows.append(row)
    return rows


def trap_zones(rows):
    """Contiguous runs of predicted traps, reported as intervals."""
    zones, run = [], []
    for r in rows:
        if r["branch"] == "truncate":
            run.append(r)
        elif run:
            zones.append(run)
            run = []
    if run:
        zones.append(run)
    out = []
    for run in zones:
        worst = max(run, key=lambda r: r["trap_gap"] or 0.0)
        out.append({
            "n_from": run[0]["n"], "n_to": run[-1]["n"], "k": run[0]["k_star"],
            "worst_n": worst["n"], "worst_gap": worst["trap_gap"],
            "worst_gap_pct": worst["trap_gap_pct"],
        })
    return out


def main():
    n_checks = verify_anchors()
    print(f"anchors reproduced: {n_checks}/{n_checks} "
          f"(N=26, N=27, N=23 trap, N=23 escape, N=25 bare grid)")

    lp_checks = verify_against_lp()
    print(f"closed form vs independent LP on constructed coordinates: "
          f"{lp_checks} configurations, max drift < 1e-9")

    print("\nselection rule k*(N), scored on the three S5.10 anchors:")
    scores = score_rules()
    for rule, s in scores.items():
        marks = "".join("Y" if v else "n" for _, v in sorted(s["per_anchor"].items()))
        print(f"  {rule:8s} {s['hits']}/{s['of']}  (N=23,26,27 -> {marks})")
    survivors = [r for r, s in scores.items() if s["hits"] == s["of"]]
    print(f"  survivors: {survivors}")
    if len(survivors) != 1:
        sys.exit("ABORT: selection rule is not identified by the anchors; "
                 "the forecast below would be arbitrary.")
    rule = survivors[0]
    print(f"  -> k*(N) = {rule} integer sqrt(N). Fitted on 3 points, 0 free "
          f"parameters. Everything below is out-of-sample.")

    rows = sweep(10, 60, rule=rule)

    print("\n   N  k*  branch     m   predicted   recipe_best  trap_gap   "
          "published  deficit  prime")
    for r in rows:
        pv = f"{r['predicted']:.7f}" if r["predicted"] is not None else "    ---    "
        rb = f"{r['recipe_best']:.7f}" if r["recipe_best"] is not None else "    ---    "
        tg = f"{r['trap_gap']:.7f}" if r["trap_gap"] else "     .     "
        pb = f"{r['published_best_known']:.5f}" if r["published_best_known"] else "   .   "
        df = f"{r['deficit_vs_published']:.4f}" if r["deficit_vs_published"] else "  .   "
        mm = f"{r['m']:>2}" if r["m"] is not None else " -"
        star = "*" if r["n"] in (23, 26, 27) else " "
        print(f" {r['n']:>3}{star} {r['k_star']:>2}  {r['branch']:<9} {mm}  "
              f"{pv}  {rb}  {tg}  {pb}  {df}  {'P' if r['is_prime'] else ' '}")

    zones = trap_zones(rows)
    print("\npredicted TRAP zones (model truncates instead of re-parameterising):")
    for z in zones:
        print(f"  N in [{z['n_from']}, {z['n_to']}]  k={z['k']}  "
              f"worst at N={z['worst_n']}: gives up {z['worst_gap']:.7f} "
              f"({z['worst_gap_pct']:.2f}% below what the recipe itself reaches)")

    conv = [r["n"] for r in rows if r["branch"] == "extend"]
    print(f"\npredicted CONVERGE N (clean fit, six-decimal agreement expected): "
          f"{conv}")

    primes_in_trap = [r["n"] for r in rows if r["is_prime"] and r["branch"] == "truncate"]
    primes_in_conv = [r["n"] for r in rows if r["is_prime"] and r["branch"] == "extend"]
    print(f"\nprimality is NOT the relevant variable, contra the paper's own "
          f"future-work guess:")
    print(f"  primes predicted to trap:    {primes_in_trap}")
    print(f"  primes predicted to converge:{primes_in_conv}")
    print(f"  the governing quantity is N - k*^2, i.e. signed distance to the "
          f"nearest perfect square: negative traps, non-negative converges.")

    out = ROOT / "n_sweep_forecast.json"
    out.write_text(json.dumps({
        "recipe": {
            "value": "V(k,m) = k/2 + m*(sqrt2-1)/(2k), 0 <= m <= (k-1)^2",
            "truncated": "T(k,N) = N/(2k) for N < k^2",
            "r_grid": "1/(2k)", "r_filler": "(sqrt2-1)/(2k)",
        },
        "selection_rule": {
            "chosen": rule,
            "definition": "k*(N) = floor(sqrt(N) + 1/2)",
            "fitted_on": ["N=23 truncate k=5", "N=26 extend k=5", "N=27 extend k=5"],
            "free_parameters": 0,
            "candidates_scored": scores,
            "caveat": "three anchors only; the rule is the unique survivor of four "
                      "candidates, not an independently confirmed law.",
        },
        "verification": {
            "anchors_reproduced": n_checks,
            "lp_configurations_checked": lp_checks,
            "lp_tolerance": 1e-9,
        },
        "rows": rows,
        "trap_zones": zones,
    }, indent=2))
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
