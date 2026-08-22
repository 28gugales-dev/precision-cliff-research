# ============================================================================
# Arm CN scoring — preregistered in arm_cn_preregistration.txt, committed BEFORE
# sampling. Reads arm_cn_collect.jsonl (raw verbatim rows) and
# arm_cn_prompts.json (registered predictions). Arm-F conventions via the
# arm M functions, unchanged: fence-strip, ast.literal_eval, validity 1e-9/1e-6
# (1e-6 primary), 2e-3 value window, structural k from dominant radius.
# Deterministic, no network. Run once on the complete ledger.
# ============================================================================
import json
import math
from collections import Counter
from pathlib import Path

from arm_m_analysis import parse, geom, dominant_k

ROOT = Path(__file__).resolve().parent
WINDOW = 2e-3
FLOOR = 5


def wilson(k, n, z=1.959964):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(c - h, 3), round(c + h, 3))


def score_cell(n, spec, rows):
    pred, argmax, ks = spec["prediction"], spec["argmax"], spec["kstar"]
    recs = []
    for r in rows:
        circles, perr = parse(r["raw"])
        rec = {"slot": r["slot"], "parse_error": perr}
        if circles is not None:
            ok6, why6 = geom(circles, n, 1e-6)
            ok9, _ = geom(circles, n, 1e-9)
            s = sum(c[2] for c in circles)
            k_emp, r_dom = dominant_k(circles)
            rec.update(valid6=ok6, why6=why6, valid9=ok9, sum=round(s, 7), k_emp=k_emp, r_dom=r_dom,
                       on_pred=ok6 and abs(s - pred) < WINDOW,
                       rival=ok6 and spec["discriminating"] and abs(s - argmax) < WINDOW,
                       above_argmax=ok6 and s > argmax + WINDOW)
        recs.append(rec)
    valid = [r for r in recs if r.get("valid6")]
    buckets = Counter(round(r["sum"] / WINDOW) for r in valid)
    ranked = buckets.most_common()
    modal_bucket, modal_n = ranked[0] if ranked else (None, 0)
    runner_n = ranked[1][1] if len(ranked) > 1 else 0
    modal_vals = [r["sum"] for r in valid if ranked and round(r["sum"] / WINDOW) == modal_bucket]
    modal_value = round(sum(modal_vals) / len(modal_vals), 7) if modal_vals else None
    tie = bool(ranked) and modal_n == runner_n
    hit = bool(modal_vals) and abs(modal_value - pred) < WINDOW and not tie
    evaluable = len(valid) >= FLOOR
    k_major = sum(1 for r in valid if r.get("k_emp") == ks)
    return dict(
        N=n, kstar=ks, branch=spec["branch"], discriminating=spec["discriminating"],
        prediction=pred, argmax=argmax,
        sampled=len(recs), parse_fail=sum(1 for r in recs if r["parse_error"]),
        valid6=len(valid), valid9=sum(1 for r in recs if r.get("valid9")),
        validity_ci=wilson(len(valid), len(recs)),
        on_pred=sum(1 for r in valid if r["on_pred"]),
        modal_value=modal_value, modal_count=modal_n, runner_up_count=runner_n,
        margin=(modal_n - runner_n) if ranked else None, tie=tie,
        evaluable=evaluable, hit=(hit if evaluable else None),
        k_star_structure=f"{k_major}/{len(valid)}", s_cn1=(k_major * 2 > len(valid)) if valid else None,
        rival=sum(1 for r in valid if r.get("rival")),
        above_argmax=sum(1 for r in valid if r.get("above_argmax")),
        k_emp_dist=dict(Counter(str(r.get("k_emp")) for r in valid)),
        invalid_reasons=dict(Counter(r.get("why6") or r.get("parse_error") for r in recs if not r.get("valid6"))),
        detail=recs,
    )


def main():
    specs = json.loads((ROOT / "arm_cn_prompts.json").read_text(encoding="utf-8"))
    rows = [json.loads(l) for l in (ROOT / "arm_cn_collect.jsonl").read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    print(f"rows collected: {len(rows)}")
    res = {}
    for ns, spec in specs.items():
        n = int(ns)
        res[n] = score_cell(n, spec, [r for r in rows if int(r["cell"]) == n])
    print("| N | k* | branch | disc | sampled | valid 1e-6 [Wilson] | on-pred | modal (count, margin) | hit | k*-struct | rival | above |")
    for n, v in res.items():
        print(f"| {n} | {v['kstar']} | {v['branch']} | {'yes' if v['discriminating'] else 'no'} | {v['sampled']} | "
              f"{v['valid6']} {v['validity_ci']} | {v['on_pred']} | {v['modal_value']} ({v['modal_count']}, +{v['margin']}) | "
              f"{'UNDERPOWERED' if not v['evaluable'] else ('HIT' if v['hit'] else 'MISS')} | {v['k_star_structure']} | {v['rival']} | {v['above_argmax']} |")
    evaluable = [v for v in res.values() if v["evaluable"]]
    hits = [v for v in evaluable if v["hit"]]
    disc_hits = [v for v in hits if v["discriminating"]]
    if len(evaluable) < 4:
        verdict = "UNDERPOWERED"
    elif len(hits) >= 4 and len(disc_hits) >= 2:
        verdict = "P-CN1 HOLDS (construction): rule predicts the mode at held-out N"
    elif len(hits) <= 2:
        verdict = "P-CN2 SUPPORTED / F-CN1 FIRES (recall): rule does not predict the mode at held-out N"
    else:
        verdict = "PARTIAL"
    s_cn1 = sum(1 for v in evaluable if v["s_cn1"])
    rival_pool = sum(v["rival"] for v in res.values() if v["discriminating"])
    print(f"evaluable cells: {len(evaluable)}/5; hits: {len(hits)} (discriminating {len(disc_hits)}/3)")
    print(f"S-CN1 k*-structure majority: {s_cn1}/{len(evaluable)} (predicted >= 4)")
    print(f"S-CN2 rival at discriminating cells: {rival_pool} (predicted <= 1)")
    print(f"ARM CN VERDICT: {verdict}")
    out = {"verdict": verdict, "evaluable": len(evaluable), "hits": len(hits), "disc_hits": len(disc_hits),
           "s_cn1": s_cn1, "s_cn2_rival": rival_pool,
           "cells": {str(n): {k: v for k, v in r.items() if k != "detail"} for n, r in res.items()}}
    (ROOT / "arm_cn_report.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    (ROOT / "arm_cn_scored.json").write_text(json.dumps({str(n): r for n, r in res.items()}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
