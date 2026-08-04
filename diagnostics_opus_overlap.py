# POST-HOC DIAGNOSTIC - not preregistered, prompted by external review deduction 5.
#
# Question from the reviewer: are the opus_alias arm's invalid samples failing by
# tolerance-scale margins (exact-tangency constructions with irrational radii that
# miss 1e-6 by rounding), or by gross geometric error? If the former, the 1e-6 gate
# penalises ambition and the tier-ladder reading changes.
#
# Geometry checks below replicate arm_f_repro.validate() exactly (same parser, same
# count gate, same wall/overlap predicates), but instead of returning the FIRST
# failure reason it measures the magnitude of every violation.
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import arm_f_repro as A  # noqa: E402

CAND = ROOT / "arm_f_candidates_v2.jsonl"
OUT = ROOT / "diagnostics_opus_overlap_2026-08-04.md"
MATCHED_N = (13, 21, 31)


def load(arm, ns=MATCHED_N):
    rows = []
    for line in CAND.open(encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        if r["arm"] == arm and r["n"] in ns:
            rows.append(r)
    return rows


def max_overlap(circles):
    """max over pairs of (r_i + r_j - dist_ij); <=0 means no pair overlaps."""
    worst, pair = 0.0, None
    for i in range(len(circles)):
        xi, yi, ri = circles[i]
        for j in range(i + 1, len(circles)):
            xj, yj, rj = circles[j]
            d = ri + rj - math.hypot(xi - xj, yi - yj)
            if pair is None or d > worst:
                worst, pair = d, (i, j)
    return worst, pair


def max_wall(circles):
    """max over circles of how far the disc pokes outside the unit square."""
    worst, idx = 0.0, None
    for k, (x, y, r) in enumerate(circles):
        v = max(r - x, r - y, x + r - 1.0, y + r - 1.0)
        if idx is None or v > worst:
            worst, idx = v, k
    return worst, idx


def valid_1e6(circles, n):
    return A.validate(circles, n, tol=1e-6)[0]


def shrink_eps(circles, n, hi=0.5, iters=200):
    """Minimal eps such that scaling every radius by (1-eps) passes the 1e-6 gate.

    Scaling is monotone for both predicates (walls and pair gaps both improve as
    radii shrink, centres fixed), so bisection is exact to machine precision.
    Returns None when even eps=hi fails - i.e. the failure is not a radius-scale
    failure at all (wrong count, nonpositive radius, centre outside the square).
    """
    def ok(e):
        return valid_1e6([(x, y, r * (1.0 - e)) for x, y, r in circles], n)

    if ok(0.0):
        return 0.0
    if not ok(hi):
        return None
    lo = 0.0
    for _ in range(iters):
        mid = (lo + hi) / 2.0
        if ok(mid):
            hi = mid
        else:
            lo = mid
    return hi


def band(v):
    if v < 1e-4:
        return "tolerance-scale"
    if v <= 1e-2:
        return "intermediate"
    return "gross"


def analyse(arm):
    out = []
    for r in load(arm):
        if r["valid"]:
            continue
        rec = {"n": r["n"], "sample_id": r["sample_id"],
               "parse_error": r.get("parse_error"),
               "invalid_reason": r.get("invalid_reason")}
        circles = r.get("circles")
        if not circles:
            rec["kind"] = "parse_failure"
            out.append(rec)
            continue
        rec["n_circles"] = len(circles)
        rec["count_ok"] = (len(circles) == r["n"])
        rec["min_radius"] = min(c[2] for c in circles)
        ov, pair = max_overlap(circles)
        wl, widx = max_wall(circles)
        rec["max_overlap"] = ov
        rec["overlap_pair"] = pair
        rec["max_wall"] = wl
        rec["wall_circle"] = widx
        rec["max_violation"] = max(ov, wl, 0.0)
        rec["band"] = band(rec["max_violation"])
        rec["kind"] = "geometry"
        rec["eps"] = shrink_eps(circles, r["n"])
        rec["sum_radii"] = sum(c[2] for c in circles)
        if rec["eps"] is not None:
            rec["sum_radii_repaired"] = rec["sum_radii"] * (1.0 - rec["eps"])
            rec["sum_radii_delta_pct"] = -100.0 * rec["eps"]
        rec["distinct_radii"] = len({round(c[2], 12) for c in circles})
        out.append(rec)
    return out


def fmt(recs, title, fh):
    fh.write(f"\n## {title}\n\n")
    fh.write("| N | s | n_circles | count_ok | max_overlap | max_wall | "
             "max_violation | band | eps_repair | sum_r | sum_r_repaired |\n")
    fh.write("|---|---|---|---|---|---|---|---|---|---|---|\n")
    for r in sorted(recs, key=lambda z: (z["n"], z["sample_id"])):
        if r["kind"] == "parse_failure":
            fh.write(f"| {r['n']} | {r['sample_id']} | - | - | - | - | - | "
                     f"PARSE FAIL ({r['parse_error']}) | - | - | - |\n")
            continue
        e = r["eps"]
        es = "not radius-repairable" if e is None else f"{e:.6e}"
        sr = f"{r['sum_radii']:.9f}"
        srr = "-" if e is None else f"{r['sum_radii_repaired']:.9f}"
        fh.write(f"| {r['n']} | {r['sample_id']} | {r['n_circles']} | "
                 f"{r['count_ok']} | {r['max_overlap']:.6e} | "
                 f"{r['max_wall']:.6e} | {r['max_violation']:.6e} | "
                 f"{r['band']} | {es} | {sr} | {srr} |\n")


def summarise(recs, fh, label):
    geo = [r for r in recs if r["kind"] == "geometry"]
    parse = [r for r in recs if r["kind"] == "parse_failure"]
    counts = {"tolerance-scale": 0, "intermediate": 0, "gross": 0}
    for r in geo:
        counts[r["band"]] += 1
    bad_count = [r for r in geo if not r["count_ok"]]
    eps = [r["eps"] for r in geo if r["eps"] is not None]
    fh.write(f"\n### {label} summary\n\n")
    fh.write(f"- invalid samples: {len(recs)} "
             f"(geometry-scored {len(geo)}, parse failures {len(parse)})\n")
    bc = ", ".join("N=%d s%d: %d" % (r["n"], r["sample_id"], r["n_circles"])
                   for r in bad_count) or "none"
    fh.write(f"- wrong circle count: {len(bad_count)} ({bc})\n")
    for b in ("tolerance-scale", "intermediate", "gross"):
        fh.write(f"- {b} (max violation {'<1e-4' if b=='tolerance-scale' else '1e-4..1e-2' if b=='intermediate' else '>1e-2'}): {counts[b]}\n")
    if geo:
        v = sorted(r["max_violation"] for r in geo)
        fh.write(f"- max violation: min {v[0]:.6e}, median {v[len(v)//2]:.6e}, max {v[-1]:.6e}\n")
    fh.write(f"- radius-shrink repairable at all: {len(eps)}/{len(geo)}\n")
    fh.write(f"- repairable at eps <= 1e-3: {sum(1 for e in eps if e <= 1e-3)}/{len(geo)}\n")
    fh.write(f"- repairable at eps <= 1e-2: {sum(1 for e in eps if e <= 1e-2)}/{len(geo)}\n")
    if eps:
        es = sorted(eps)
        fh.write(f"- eps: min {es[0]:.6e}, median {es[len(es)//2]:.6e}, max {es[-1]:.6e}\n")
    return counts, eps, geo, parse


def main():
    opus = analyse("opus_alias")
    haiku = analyse("bare")
    with OUT.open("w", encoding="utf-8") as fh:
        fh.write("# POST-HOC DIAGNOSTIC - not preregistered, "
                 "prompted by external review deduction 5\n\n")
        fh.write("Generated 2026-08-04 by `diagnostics_opus_overlap.py`. "
                 "Analysis only; no paper text or arm data was modified.\n\n")
        fh.write("Source: `arm_f_candidates_v2.jsonl`. Validity predicates "
                 "replicate `arm_f_repro.validate()` (primary tol 1e-6). "
                 "`max_overlap` = max over pairs of (r_i+r_j-dist_ij); "
                 "`max_wall` = max over circles of how far the disc exits the "
                 "unit square; `max_violation` = max of the two, floored at 0. "
                 "`eps_repair` = minimal eps (bisection, 200 iters) such that "
                 "scaling all radii by (1-eps) with centres fixed passes 1e-6.\n")
        fmt(opus, "opus_alias arm - every invalid sample (N=13/21/31)", fh)
        o = summarise(opus, fh, "opus_alias")
        fmt(haiku, "weak tier (haiku bare) - invalid samples, matched cells N=13/21/31", fh)
        h = summarise(haiku, fh, "weak tier (haiku bare)")
        fh.write("\n## Structure of the opus invalid samples\n\n")
        fh.write("Bears directly on the reviewer's 'ambitious gasket' hypothesis: a "
                 "tangency-driven near-miss should show many distinct radii and a "
                 "violation at rounding scale. Column `not radius-repairable` means "
                 "even eps=0.5 (halving every radius) still fails 1e-6, i.e. two "
                 "centres are close enough that no uniform shrink separates them.\n\n")
        fh.write("| N | s | distinct_radii | min_radius | max_violation | eps_repair |\n")
        fh.write("|---|---|---|---|---|---|\n")
        for r in sorted([z for z in opus if z["kind"] == "geometry"],
                        key=lambda z: (z["n"], z["sample_id"])):
            e = r["eps"]
            es = "n/a (>0.5)" if e is None else f"{e:.6e}"
            fh.write(f"| {r['n']} | {r['sample_id']} | {r['distinct_radii']} | "
                     f"{r['min_radius']:.9f} | {r['max_violation']:.6e} | {es} |\n")
        fh.write("\n## Verdict inputs\n\n")
        fh.write(f"- opus tolerance-scale fraction: {o[0]['tolerance-scale']}/{len(o[2])}\n")
        fh.write(f"- weak-tier tolerance-scale fraction: {h[0]['tolerance-scale']}/{len(h[2])}\n")
    print(OUT)


if __name__ == "__main__":
    main()
