# ============================================================================
# Arm M scoring — preregistered in arm_m_preregistration.txt (committed e528c6b
# BEFORE sampling). Reads arm_m_collect.jsonl (raw verbatim rows), applies the
# arm-F conventions unchanged: ast.literal_eval parse after stripping fences,
# validity at 1e-9 and 1e-6 (1e-6 primary), value window 2e-3, structural k
# from dominant radius. Deterministic, no network.
# ============================================================================
import ast
import json
import math
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
S2 = math.sqrt(2)

PRED = {20: 2.2071068, 30: 2.7071068, 41: 3.1725890, 57: 3.5625000}
KSTAR = {20: 4, 30: 5, 41: 6, 57: 8}
M_REG = {20: 4, 30: 5, 41: 5}           # registered filler counts (converge cells)
RIVAL57 = 3.7366935                      # V(7,8)
WINDOW = 2e-3


def parse(raw):
    t = raw.strip()
    t = re.sub(r"^```[a-zA-Z]*", "", t).replace("```", "").strip()
    try:
        v = ast.literal_eval(t)
    except (ValueError, SyntaxError):
        return None, "literal_eval_failed"
    if not isinstance(v, list) or not all(
            isinstance(c, (list, tuple)) and len(c) == 3 and
            all(isinstance(u, (int, float)) for u in c) for c in v):
        return None, "shape"
    return [list(map(float, c)) for c in v], None


def geom(circles, n, tol):
    if len(circles) != n:
        return False, "count"
    for x, y, r in circles:
        if r <= 0:
            return False, "nonpositive_radius"
        if min(x - r, y - r, 1 - x - r, 1 - y - r) < -tol:
            return False, "outside"
    for i in range(len(circles)):
        xi, yi, ri = circles[i]
        for j in range(i + 1, len(circles)):
            xj, yj, rj = circles[j]
            if math.hypot(xi - xj, yi - yj) - ri - rj < -tol:
                return False, "overlap"
    return True, None


def dominant_k(circles):
    radii = [round(c[2], 6) for c in circles]
    r_dom, _ = Counter(radii).most_common(1)[0]
    return (round(1.0 / (2.0 * r_dom)) if r_dom > 0 else None), r_dom


def filler_count(circles, k):
    """Circles whose radius matches the filler radius (sqrt(2)-1)/(2k) within 1e-3."""
    rf = (S2 - 1) / (2 * k)
    return sum(1 for c in circles if abs(c[2] - rf) < 1e-3)


def main():
    rows = [json.loads(l) for l in
            (ROOT / "arm_m_collect.jsonl").read_text(encoding="utf-8-sig").splitlines()
            if l.strip()]
    print(f"rows collected: {len(rows)}")
    results = {}
    for n in sorted(PRED):
        cell = [r for r in rows if r["cell"] == n]
        recs = []
        for r in cell:
            circles, perr = parse(r["raw"])
            rec = {"slot": r["slot"], "parse_error": perr}
            if circles is not None:
                ok6, why6 = geom(circles, n, 1e-6)
                ok9, why9 = geom(circles, n, 1e-9)
                s = sum(c[2] for c in circles)
                k_emp, r_dom = dominant_k(circles)
                rec.update(valid6=ok6, why6=why6, valid9=ok9, sum=round(s, 7),
                           k_emp=k_emp, r_dom=r_dom,
                           on_pred=ok6 and abs(s - PRED[n]) < WINDOW,
                           fillers=filler_count(circles, KSTAR[n]))
                if n == 57:
                    rec["rival"] = ok6 and abs(s - RIVAL57) < WINDOW
            recs.append(rec)
        valid = [r for r in recs if r.get("valid6")]
        onp = [r for r in valid if r["on_pred"]]
        buckets = Counter(round(r["sum"] / WINDOW) for r in valid)
        modal_bucket, modal_n = (buckets.most_common(1)[0] if buckets else (None, 0))
        # modal value = mean of sums in the modal bucket
        modal_vals = [r["sum"] for r in valid
                      if buckets and round(r["sum"] / WINDOW) == modal_bucket]
        results[n] = dict(
            sampled=len(recs),
            parse_fail=sum(1 for r in recs if r["parse_error"]),
            valid6=len(valid),
            valid9=sum(1 for r in recs if r.get("valid9")),
            on_pred=len(onp),
            modal_value=(round(sum(modal_vals) / len(modal_vals), 7) if modal_vals else None),
            modal_count=modal_n,
            modal_is_pred=(modal_vals and abs(modal_vals[0] - PRED[n]) < WINDOW) or False,
            k_emp_dist=dict(Counter(str(r.get("k_emp")) for r in valid)),
            filler_dist=dict(Counter(r.get("fillers") for r in valid)),
            rival=sum(1 for r in valid if r.get("rival")) if n == 57 else None,
            detail=recs,
        )
    out = {"predictions": PRED, "kstar": KSTAR, "results": {str(k): {kk: vv for kk, vv in v.items() if kk != "detail"} for k, v in results.items()}}
    (ROOT / "arm_m_report.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    (ROOT / "arm_m_scored.json").write_text(
        json.dumps({str(k): v for k, v in results.items()}, indent=2), encoding="utf-8")

    print("| N | sampled | parse fail | valid 1e-6 | valid 1e-9 | on-pred | modal value (count) | modal=pred? | k_emp dist | filler dist |")
    for n, v in results.items():
        print(f"| {n} | {v['sampled']} | {v['parse_fail']} | {v['valid6']} | {v['valid9']} | "
              f"{v['on_pred']} | {v['modal_value']} ({v['modal_count']}) | {v['modal_is_pred']} | "
              f"{v['k_emp_dist']} | {v['filler_dist']} |")
    if 57 in results:
        print(f"N=57 rival hits: {results[57]['rival']}")
    # Falsifier F-M1: modal valid output NOT V(k*,m) at 2+ of 3 converge cells
    fm1 = sum(1 for n in (20, 30, 41)
              if n in results and not results[n]["modal_is_pred"])
    print(f"F-M1 cells where modal != registered prediction: {fm1}/3 -> "
          f"{'TRIGGERED' if fm1 >= 2 else 'not triggered'}")
    if 57 in results:
        print(f"F-M2 (N=57 modal != T(8,57)): {'TRIGGERED' if not results[57]['modal_is_pred'] else 'not triggered'}")


if __name__ == "__main__":
    main()
