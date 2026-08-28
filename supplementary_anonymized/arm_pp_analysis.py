# Arm PP scorer. Arm-F conventions verbatim via arm_f_repro. Registered rules
# of arm_pp_preregistration.txt; committed before sampling.
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arm_f_repro as A

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
COLLECT = ROOT / "arm_pp_collect.jsonl"
PROMPTS = json.loads((ROOT / "arm_pp_prompts.json").read_text(encoding="utf-8"))
WINDOW = 2e-3
FLOOR = 5


def bucket(v):
    return round(v / WINDOW)


def main():
    rows = [json.loads(l) for l in COLLECT.read_text(encoding="utf-8").splitlines() if l.strip()]
    report = {"cells": {}, "pooled": {}}
    evaluable = modal_hits = 0
    rival_total = valid_total = scored_total = 0
    kstar_cells = 0
    for key, meta in PROMPTS.items():
        tag, n = meta["paraphrase"], meta["n"]
        sub = [r for r in rows if r["paraphrase"] == tag and r["n"] == n]
        scored = [r for r in sub if not r.get("runtime_rejection")]
        sums, kvals, fails = [], [], Counter()
        for r in scored:
            circles, err = A.parse_packing(r.get("raw_output"))
            if circles is None:
                fails[f"parse:{err}"] += 1
                continue
            if len(circles) != n:
                fails["count_mismatch"] += 1
                continue
            ok, why = A.validate(circles, n, tol=1e-6)
            if not ok:
                fails[f"invalid:{str(why)[:30]}"] += 1
                continue
            sums.append(sum(c[2] for c in circles))
            dom = Counter(round(c[2], 4) for c in circles).most_common(1)[0][0]
            kvals.append(round(1.0 / (2.0 * dom)) if dom > 0 else None)
        nv = len(sums)
        valid_total += nv
        scored_total += len(scored)
        pred, rv = meta["predicted"], meta["rival"]
        on_pred = sum(abs(s - pred) < WINDOW for s in sums)
        on_rival = sum(abs(s - rv) < WINDOW for s in sums)
        rival_total += on_rival
        cell_ok = nv >= FLOOR
        modal_is_pred = None
        if cell_ok:
            evaluable += 1
            counts = Counter(bucket(s) for s in sums)
            top = counts.most_common()
            best = top[0][1]
            modal_is_pred = {b for b, c in top if c == best} == {bucket(pred)}
            modal_hits += bool(modal_is_pred)
        kstar = round((n) ** 0.5)
        kmaj = (sum(k == kstar for k in kvals) > len(kvals) / 2) if kvals else False
        kstar_cells += bool(kmaj and cell_ok)
        report["cells"][key] = {
            "paraphrase": tag, "n": n, "launched": len(sub), "scored": len(scored),
            "valid_1e6": nv, "on_prediction": on_pred, "on_rival": on_rival,
            "modal_is_pred": modal_is_pred, "evaluable": cell_ok,
            "k_star_majority": kmaj, "fails": dict(fails),
            "best": max(sums, default=None),
        }
        print(f"PP-{tag} N={n:>2} valid {nv}/{len(scored)} on-pred {on_pred} "
              f"on-rival {on_rival} modal_is_pred {modal_is_pred} k*maj {kmaj} "
              f"fails {dict(fails)}")
    pooled_validity = valid_total / scored_total if scored_total else 0.0
    p_pp1 = evaluable >= 4 and modal_hits >= 4
    p_pp2 = (evaluable >= 4 and modal_hits <= 2) or pooled_validity < 0.40
    verdict = ("UNDERPOWERED" if evaluable < 4 else
               "P-PP1" if p_pp1 else "P-PP2" if p_pp2 else "PARTIAL")
    report["pooled"] = {
        "evaluable_cells": evaluable, "modal_hits": modal_hits,
        "pooled_validity": round(pooled_validity, 4),
        "S_PP1_rival_leq_2": rival_total <= 2, "rival_total": rival_total,
        "valid_total": valid_total, "S_PP2_kstar_cells": kstar_cells,
        "verdict": verdict,
    }
    (ROOT / "arm_pp_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nmodal at prediction: {modal_hits}/{evaluable} evaluable paraphrase-cells; "
          f"pooled validity {pooled_validity:.0%}; rival {rival_total}/{valid_total}")
    print(f"VERDICT: {verdict} | S-PP1 rival<=2: {rival_total <= 2} | "
          f"S-PP2 k*-majority cells: {kstar_cells}/{evaluable}")
    print("report frozen in arm_pp_report.json")


if __name__ == "__main__":
    main()
