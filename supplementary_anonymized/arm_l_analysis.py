# Arm L scorer. Registered rules of arm_l_preregistration.txt; run once on the
# complete ledger. Reuses arm_f_repro parse/validate verbatim.
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
CFG = json.loads((ROOT / "arm_l_prompts.json").read_text(encoding="utf-8"))
WINDOW = 2e-3
S2 = math.sqrt(2)

# POST-SAMPLING CORRECTION, disclosed (corrections_ledger.md item 34). The
# registered config stores the family argmax to seven decimals (2.7485281 for
# N = 31). The clearance test compares at 1e-9, so a proposal landing exactly on
# the rival, 2.748528137423857, tested as "above" the truncated constant by
# 3.7e-8 -- an artifact of the literal, not a result. The family argmax is
# recomputed here in closed form; every other comparison uses the 2e-3 window
# and is unaffected by the truncation.
def family_argmax(n):
    best = None
    for k in range(1, int(math.isqrt(n)) + 3):
        if n < k * k:
            v = n / (2 * k)
        elif n - k * k <= (k - 1) ** 2:
            v = k / 2 + (n - k * k) * (S2 - 1) / (2 * k)
        else:
            continue
        best = v if best is None else max(best, v)
    return best


def load_rows():
    """Merge the four per-lineage ledgers, and freeze the merge for release."""
    rows = []
    for lineage in CFG["lineages"]:
        path = ROOT / f"arm_l_collect_{lineage}.jsonl"
        if not path.exists():
            continue
        rows += [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    merged = ROOT / "arm_l_collect.jsonl"
    with merged.open("w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    return rows


def main():
    rows = load_rows()
    report = {"lineages": {}, "pooled": {}}
    per_cell_gen0, per_cell_cond = {}, {}
    regime_cond = {"greedy": [0, 0], "diverse": [0, 0]}  # [on_pred, valid]

    for lineage in CFG["lineages"]:
        n_str, regime = lineage.split("-")
        n = int(n_str)
        cell = CFG["cells"][n_str]
        pred = cell["predicted"]
        argmax = family_argmax(n)  # exact; see correction note above
        sub = [r for r in rows if r.get("lineage") == lineage]
        gens = {}
        for r in sub:
            g = r["generation"]
            gens.setdefault(g, {"launched": 0, "rejected": 0, "valid": [], "fails": Counter()})
            gens[g]["launched"] += 1
            if r.get("runtime_rejection"):
                gens[g]["rejected"] += 1
                continue
            circles, err = A.parse_packing(r.get("raw_output"))
            if circles is None:
                gens[g]["fails"][f"parse:{err}"] += 1
                continue
            if len(circles) != n:
                gens[g]["fails"]["count_mismatch"] += 1
                continue
            ok, why = A.validate(circles, n, tol=1e-6)
            ok9, _ = A.validate(circles, n, tol=1e-9)
            if not ok:
                gens[g]["fails"][f"invalid:{str(why)[:28]}"] += 1
                continue
            gens[g]["valid"].append((sum(c[2] for c in circles), ok9))

        lin = {"n": n, "regime": regime, "archive_size": CFG["regimes"][regime],
               "generations": {}}
        g0_on = g0_valid = 0
        cond_on = cond_valid = cond_gens_with_valid = 0
        best_overall = None
        for g in sorted(gens):
            d = gens[g]
            sums = [s for s, _ in d["valid"]]
            on = sum(abs(s - pred) < WINDOW for s in sums)
            rival = sum(abs(s - argmax) < WINDOW for s in sums)
            above = sum(s > argmax + 1e-9 for s in sums)
            best = max(sums, default=None)
            if best is not None:
                best_overall = best if best_overall is None else max(best_overall, best)
            modal_is_pred = None
            if sums:
                counts = Counter(round(s / WINDOW) for s in sums)
                top = counts.most_common()
                bestct = top[0][1]
                modal_is_pred = {b for b, c in top if c == bestct} == {round(pred / WINDOW)}
            lin["generations"][str(g)] = {
                "launched": d["launched"], "runtime_rejections": d["rejected"],
                "valid_1e6": len(sums), "valid_1e9": sum(1 for _, o in d["valid"] if o),
                "on_prediction": on, "rival": rival, "above_family_argmax": above,
                "best": None if best is None else round(best, 7),
                "modal_is_pred": modal_is_pred, "fails": dict(d["fails"]),
            }
            if g == 0:
                g0_on, g0_valid = on, len(sums)
            else:
                cond_on += on
                cond_valid += len(sums)
                cond_gens_with_valid += 1 if sums else 0
        evaluable = g0_valid >= 3 and cond_gens_with_valid >= 3
        lin.update({
            "gen0_on_prediction": g0_on, "gen0_valid": g0_valid,
            "gen0_rate": round(g0_on / g0_valid, 4) if g0_valid else None,
            "conditioned_on_prediction": cond_on, "conditioned_valid": cond_valid,
            "conditioned_rate": round(cond_on / cond_valid, 4) if cond_valid else None,
            "best_of_run": None if best_overall is None else round(best_overall, 7),
            "cleared_family_argmax": bool(best_overall is not None and best_overall > argmax + 1e-9),
            "evaluable": evaluable,
        })
        report["lineages"][lineage] = lin
        per_cell_gen0.setdefault(n, [0, 0])
        per_cell_cond.setdefault(n, [0, 0])
        per_cell_gen0[n][0] += g0_on
        per_cell_gen0[n][1] += g0_valid
        per_cell_cond[n][0] += cond_on
        per_cell_cond[n][1] += cond_valid
        regime_cond[regime][0] += cond_on
        regime_cond[regime][1] += cond_valid
        print(f"{lineage:>12}  gen0 {g0_on}/{g0_valid}"
              f"  cond {cond_on}/{cond_valid}"
              f"  best {lin['best_of_run']}  cleared_argmax {lin['cleared_family_argmax']}"
              f"  evaluable {evaluable}")

    def rate(pair):
        return pair[0] / pair[1] if pair[1] else None

    l1 = all(report["lineages"][f"{n}-{r}"]["generations"].get("0", {}).get("modal_is_pred")
             for n in sorted(CFG["cells"], key=int) for r in CFG["regimes"])
    l2 = all(rate(per_cell_cond[int(n)]) is not None and rate(per_cell_gen0[int(n)]) is not None
             and rate(per_cell_cond[int(n)]) < rate(per_cell_gen0[int(n)])
             for n in CFG["cells"])
    gr, dv = rate(regime_cond["greedy"]), rate(regime_cond["diverse"])
    l3 = gr is not None and dv is not None and gr > dv
    f_l1 = all(rate(per_cell_cond[int(n)]) is not None and rate(per_cell_gen0[int(n)]) is not None
               and rate(per_cell_cond[int(n)]) >= rate(per_cell_gen0[int(n)])
               for n in CFG["cells"])
    report["pooled"] = {
        "per_cell_gen0_rate": {str(n): rate(v) for n, v in per_cell_gen0.items()},
        "per_cell_conditioned_rate": {str(n): rate(v) for n, v in per_cell_cond.items()},
        "greedy_conditioned_rate": gr, "diverse_conditioned_rate": dv,
        "L1_gen0_modal_all_lineages": bool(l1),
        "L2_dissolution_survives_iteration": bool(l2),
        "L3_greedy_above_diverse": bool(l3),
        "L4_any_lineage_cleared_family_argmax":
            any(v["cleared_family_argmax"] for v in report["lineages"].values()),
        "F_L1_triggered": bool(f_l1),
        "evaluable_lineages": sum(1 for v in report["lineages"].values() if v["evaluable"]),
    }
    (ROOT / "arm_l_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    p = report["pooled"]
    print(f"\ngen0 rates by cell {p['per_cell_gen0_rate']}; "
          f"conditioned {p['per_cell_conditioned_rate']}")
    print(f"conditioned rate greedy {gr} vs diverse {dv}")
    print(f"L1 {p['L1_gen0_modal_all_lineages']} | L2 {p['L2_dissolution_survives_iteration']} "
          f"| L3 {p['L3_greedy_above_diverse']} | L4 cleared-argmax "
          f"{p['L4_any_lineage_cleared_family_argmax']} | F-L1 {p['F_L1_triggered']}")
    print("report frozen in arm_l_report.json")


if __name__ == "__main__":
    main()
