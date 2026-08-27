# Arm CP scorer. Maps each emitted circle back to the unit square
# (x -> (x-3)/2, y -> (y-3)/2, r -> r/2) then applies arm-F conventions
# verbatim via arm_f_repro (parse, validity at 1e-6/1e-9, 2e-3 window,
# mode = most frequent 2e-3 bucket among valid, ties against prediction,
# structural k from dominant radius). Registered rules of
# arm_cp_preregistration.txt; committed before sampling.
import json
import math
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arm_f_repro as A

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
COLLECT = ROOT / "arm_cp_collect.jsonl"
PROMPTS = json.loads((ROOT / "arm_cp_prompts.json").read_text(encoding="utf-8"))
EVALUABLE_FLOOR = 5
WINDOW = 2e-3


def map_back(circles):
    return [[(x - 3.0) / 2.0, (y - 3.0) / 2.0, r / 2.0] for x, y, r in circles]


def bucket(v):
    return round(v / WINDOW)


def main():
    rows = [json.loads(l) for l in COLLECT.read_text(encoding="utf-8").splitlines() if l.strip()]
    report = {"cells": {}, "pooled": {}}
    modal_hits = evaluable = 0
    rival_hits_disc = disc_valid = 0
    kstar_majority_cells = 0
    pooled_valid = pooled_total = 0
    for key, meta in PROMPTS.items():
        n = meta["n"]
        sub = [r for r in rows if r["n"] == n]
        excluded = [r for r in sub if r.get("runtime_rejection")]
        scored = [r for r in sub if not r.get("runtime_rejection")]
        valid_sums, kvals = [], []
        fails = Counter()
        for r in scored:
            circles, err = A.parse_packing(r.get("raw_output"))
            if circles is None:
                fails[f"parse:{err}"] += 1
                continue
            if len(circles) != n:
                fails["count_mismatch"] += 1
                continue
            unit = map_back(circles)
            ok, why = A.validate(unit, n, tol=1e-6)
            ok9, _ = A.validate(unit, n, tol=1e-9)
            if not ok:
                fails[f"invalid:{str(why)[:30]}"] += 1
                continue
            s = sum(c[2] for c in unit)
            valid_sums.append((s, ok9))
            dom = Counter(round(c[2], 4) for c in unit).most_common(1)[0][0]
            kvals.append(round(1.0 / (2.0 * dom)) if dom > 0 else None)
        nv = len(valid_sums)
        pooled_valid += nv
        pooled_total += len(scored)
        pred = meta["predicted_unit"]
        rv = meta["rival_unit"]
        on_pred = sum(abs(s - pred) < WINDOW for s, _ in valid_sums)
        on_rival = sum(abs(s - rv) < WINDOW for s, _ in valid_sums)
        cell_evaluable = nv >= EVALUABLE_FLOOR
        modal_is_pred = None
        if cell_evaluable:
            evaluable += 1
            counts = Counter(bucket(s) for s, _ in valid_sums)
            top = counts.most_common()
            best_ct = top[0][1]
            modal_buckets = {b for b, c in top if c == best_ct}
            # ties count against the prediction: modal only if unique bucket
            modal_is_pred = modal_buckets == {bucket(pred)}
            modal_hits += bool(modal_is_pred)
        if meta["discriminating"]:
            disc_valid += nv
            rival_hits_disc += on_rival
        kmaj = (sum(k == meta["k_star"] for k in kvals) > len(kvals) / 2) if kvals else False
        kstar_majority_cells += bool(kmaj and cell_evaluable)
        report["cells"][key] = {
            "n": n, "launched": len(sub), "runtime_rejections": len(excluded),
            "scored": len(scored), "valid_1e6": nv,
            "valid_1e9": sum(1 for _, ok9 in valid_sums if ok9),
            "on_prediction": on_pred, "on_rival": on_rival,
            "modal_is_pred": modal_is_pred, "evaluable": cell_evaluable,
            "k_star_majority": kmaj, "fails": dict(fails),
            "best": max((s for s, _ in valid_sums), default=None),
        }
        print(f"N={n:>2} valid {nv}/{len(scored)} on-pred {on_pred} on-rival {on_rival} "
              f"modal_is_pred {modal_is_pred} k*-majority {kmaj} fails {dict(fails)}")
    pooled_validity = pooled_valid / pooled_total if pooled_total else 0.0
    p_cp1 = evaluable >= 4 and modal_hits >= 4
    p_cp2 = (evaluable >= 4 and modal_hits <= 2) or pooled_validity < 0.40
    verdict = ("UNDERPOWERED" if evaluable < 4 else
               "P-CP1" if p_cp1 else "P-CP2 (F-CP1 TRIGGERED)" if p_cp2 else "PARTIAL")
    s_cp1 = rival_hits_disc <= 1
    report["pooled"] = {
        "evaluable_cells": evaluable, "modal_hits": modal_hits,
        "pooled_validity": round(pooled_validity, 4), "verdict": verdict,
        "S_CP1_rival_leq_1": s_cp1, "rival_hits_disc": rival_hits_disc,
        "disc_valid": disc_valid, "S_CP2_kstar_cells": kstar_majority_cells,
    }
    (ROOT / "arm_cp_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nmodal at prediction: {modal_hits}/{evaluable} evaluable cells; "
          f"pooled validity {pooled_validity:.0%}")
    print(f"VERDICT: {verdict} | S-CP1 rival<=1: {s_cp1} ({rival_hits_disc}/{disc_valid}) "
          f"| S-CP2 k*-majority cells: {kstar_majority_cells}/{evaluable}")
    print("report frozen in arm_cp_report.json")


if __name__ == "__main__":
    main()
