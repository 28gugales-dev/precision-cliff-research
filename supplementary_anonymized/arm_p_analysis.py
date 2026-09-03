# ============================================================================
# Arm P analysis — scores arm_p_collect.jsonl against the predictions
# registered in arm_p_preregistration.txt. Run once, deterministic, no
# network. Reuses scoring machinery rather than reimplementing it:
#   - direct-emission cells (square + held-out): parse_packing, validate,
#     score, classify, recipe_value, truncated_value from arm_f_repro.py
#   - code cells: the AST gate / sandbox / stdout taxonomy from
#     arm_cc_analysis.py (score_row and its helpers), imported directly
#   - Wilson interval: arm_cn_analysis.wilson (same formula arm CN reports)
#
# Predictions:
#   square    -> value/rival from arm_f_repro.PREDICTIONS (T(k*,N) / V(k*,m))
#   held-out  -> value/rival/kstar/discriminating from arm_cn_prompts.json
#   code      -> anchor/rival/kstar from arm_p_prompts.json (== arm_cc_prompts.json)
# ============================================================================
import argparse
import json
from collections import Counter
from pathlib import Path

from arm_f_repro import (parse_packing, validate, score, classify,
                         recipe_value, truncated_value,
                         PREDICTIONS as F_PREDICTIONS)
from arm_cc_analysis import score_row as cc_score_row
from arm_cn_analysis import wilson

ROOT = Path(__file__).resolve().parent
WINDOW = 2e-3
FLOOR = 5

SQUARE_N = [13, 17, 21, 31, 35, 37, 43]
HELDOUT_N = [50, 58, 62, 65, 75]
CODE_N = [13, 21, 31]
DISCRIMINATING_N = [13, 21, 31, 43]

# Section 2.4 clearance rule: valid at 1e-9 AND sum > family argmax + 1e-6.
# argmax recomputed in closed form (registered, higher precision than the
# 2e-3-window RIVAL constants arm_cc_analysis uses for its own reporting).
CLEARANCE_ARGMAX = {13: 1.776142375, 21: 2.258883476, 31: 2.748528137}
CLEARANCE_EPS = 1e-6


def infer_kstar_square(n, target_value):
    """Recovers k* for a square cell by reusing recipe_value/truncated_value
    rather than hard-coding a second copy of the table arm_f_repro already
    encodes implicitly in PREDICTIONS."""
    for k in range(2, 10):
        if n < k * k:
            if abs(truncated_value(k, n) - target_value) < 1e-6:
                return k
        else:
            m = n - k * k
            if 0 <= m <= (k - 1) ** 2 and abs(recipe_value(k, m) - target_value) < 1e-6:
                return k
    return None


KSTAR_SQUARE = {n: infer_kstar_square(n, F_PREDICTIONS[n]["value"]) for n in SQUARE_N}


def load_rows(path):
    rows = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


def dominant_k_emp(circles):
    radii = [round(r, 4) for _, _, r in circles]
    r_dom, _ = Counter(radii).most_common(1)[0]
    return round(1.0 / (2.0 * r_dom)) if r_dom > 0 else None


def score_direct_row(raw, n):
    """arm_f_repro conventions: fence-strip + literal_eval, 1e-6 primary /
    1e-9 logged validity, classify() for structure."""
    circles, perr = parse_packing(raw)
    rec = {"parse_error": perr, "valid6": False, "valid9": False}
    if circles is None:
        return rec
    ok6, why6 = validate(circles, n, tol=1e-6)
    ok9, why9 = validate(circles, n, tol=1e-9)
    rec.update(valid6=ok6, why6=why6, valid9=ok9, why9=why9)
    if ok6:
        s = score(circles)
        cls = classify(circles, n)
        rec.update(sum=round(s, 7), structure=cls["structure"],
                   k_emp=dominant_k_emp(circles))
    return rec


def score_group(rows, group, specs):
    """specs: {n: {"value":..., "rival":..., "kstar":..., "discriminating":bool}}"""
    cells = {}
    for n, spec in specs.items():
        cell_rows = [r for r in rows if r["cell_group"] == group and r["n"] == n]
        scored = []
        for r in cell_rows:
            if r.get("call_error") is not None or not r.get("raw"):
                scored.append({"parse_error": "call_error", "valid6": False, "valid9": False})
                continue
            scored.append(score_direct_row(r["raw"], n))
        valid = [s for s in scored if s["valid6"]]
        buckets = Counter(round(s["sum"] / WINDOW) for s in valid)
        ranked = buckets.most_common()
        modal_bucket, modal_count = ranked[0] if ranked else (None, 0)
        runner_count = ranked[1][1] if len(ranked) > 1 else 0
        tie = bool(ranked) and modal_count == runner_count
        modal_vals = [s["sum"] for s in valid
                      if ranked and round(s["sum"] / WINDOW) == modal_bucket]
        modal_value = round(sum(modal_vals) / len(modal_vals), 7) if modal_vals else None
        evaluable = len(valid) >= FLOOR
        on_pred = [s for s in valid if abs(s["sum"] - spec["value"]) < WINDOW]
        rival_distinct = abs(spec["rival"] - spec["value"]) > 1e-9
        rival_hits = [s for s in valid
                      if rival_distinct and abs(s["sum"] - spec["rival"]) < WINDOW]
        kstar_hits = [s for s in valid if s.get("k_emp") == spec["kstar"]]
        hit = (not tie) and modal_value is not None and abs(modal_value - spec["value"]) < WINDOW
        bins = Counter()
        for s in scored:
            if not s["valid6"]:
                bins[s.get("why6") or s.get("parse_error") or "unknown"] += 1
        cells[n] = {
            "kstar": spec["kstar"], "predicted_value": spec["value"],
            "rival_argmax": spec["rival"], "discriminating": spec.get("discriminating"),
            "sampled": len(cell_rows),
            "valid_1e6": len(valid), "valid_1e9": sum(1 for s in scored if s.get("valid9")),
            "evaluable": evaluable,
            "modal_value": modal_value, "modal_count": modal_count,
            "runner_up_count": runner_count, "modal_tie": tie,
            "hit": (hit if evaluable else None),
            "on_prediction": len(on_pred),
            "rival_emission": len(rival_hits),
            "kstar_structure": len(kstar_hits),
            "failure_bins": dict(bins),
        }
    return cells


def build_square_specs():
    return {n: {"value": F_PREDICTIONS[n]["value"],
                "rival": F_PREDICTIONS[n]["rival_argmax"],
                "kstar": KSTAR_SQUARE[n],
                "discriminating": n in DISCRIMINATING_N}
            for n in SQUARE_N}


def build_heldout_specs():
    cn = json.loads((ROOT / "arm_cn_prompts.json").read_text(encoding="utf-8"))
    return {int(k): {"value": v["prediction"], "rival": v["argmax"],
                     "kstar": v["kstar"], "discriminating": v["discriminating"]}
            for k, v in cn.items()}


def score_code(rows):
    cells = {}
    for n in CODE_N:
        cell_rows = [r for r in rows if r["cell_group"] == "code" and r["n"] == n]
        scored = []
        for r in cell_rows:
            if r.get("call_error") is not None or not r.get("raw"):
                scored.append({"bin": "call_error"})
                continue
            scored.append(cc_score_row(r["raw"], n))
        bins = Counter(s["bin"] for s in scored)
        valid = [s for s in scored if s["bin"] == "valid"]
        cleared = [s for s in valid
                   if s.get("valid_1e9")
                   and s["sum"] > CLEARANCE_ARGMAX[n] + CLEARANCE_EPS]
        cells[n] = {
            "sampled": len(cell_rows), "bins": dict(bins), "n_valid": len(valid),
            "sums": sorted(round(s["sum"], 7) for s in valid),
            "clearance_argmax": CLEARANCE_ARGMAX[n], "cleared": len(cleared),
            "evaluable": len(valid) >= FLOOR,
        }
    return cells


def pooled_discriminating_rate(square_cells):
    valid_total = sum(square_cells[n]["valid_1e6"] for n in DISCRIMINATING_N)
    on_pred_total = sum(square_cells[n]["on_prediction"] for n in DISCRIMINATING_N)
    rate = (on_pred_total / valid_total) if valid_total else 0.0
    ci = wilson(on_pred_total, valid_total)
    return {"valid": valid_total, "on_prediction": on_pred_total,
            "rate": round(rate, 4), "wilson_95ci": ci}


def evaluate_predictions(square_cells, heldout_cells, code_cells, pooled_disc):
    square_hits = [n for n in SQUARE_N if square_cells[n]["hit"]]
    disc_hits = [n for n in DISCRIMINATING_N if square_cells[n]["hit"]]
    heldout_hits = [n for n in HELDOUT_N if heldout_cells[n]["hit"]]

    pp1 = (len(square_hits) >= 5 and len(disc_hits) >= 2 and len(heldout_hits) >= 4)
    pp2 = len(square_hits) <= 3
    dead_zone = len(square_hits) == 4

    total_cleared = sum(code_cells[n]["cleared"] for n in CODE_N)
    pp3 = total_cleared == 0
    pp4 = total_cleared >= 1

    fp1 = pooled_disc["valid"] > 0 and pooled_disc["rate"] < 0.40

    verdicts = {
        "P-P1 (anchor transfers to pinned path)": {
            "statement": "T(k*,N) modal at >=5/7 square cells, incl >=2/4 "
                        "discriminating, AND >=4/5 held-out cells",
            "observed": f"square {len(square_hits)}/7, discriminating "
                       f"{len(disc_hits)}/4, heldout {len(heldout_hits)}/5",
            "holds": pp1,
        },
        "P-P2 (anchor is agent-runtime artifact)": {
            "statement": "modal at <=3/7 square cells",
            "observed": f"square {len(square_hits)}/7",
            "holds": pp2,
        },
        "dead_zone (modal at exactly 4/7 square cells)": {
            "statement": "reported, not adjudicated as P-P1 or P-P2",
            "observed": f"square {len(square_hits)}/7",
            "fires": dead_zone,
        },
        "P-P3 (code-channel ceiling holds)": {
            "statement": "0 valid program outputs at N=13,21,31 clear "
                        "family argmax under section-2.4 rule",
            "observed": f"cleared {total_cleared}/3 cells "
                       f"({[code_cells[n]['cleared'] for n in CODE_N]})",
            "holds": pp3,
        },
        "P-P4 (code-channel ceiling breaks)": {
            "statement": ">=1 program output clears family argmax",
            "observed": f"cleared {total_cleared}",
            "holds": pp4,
        },
        "F-P1 (falsifier)": {
            "statement": "pooled on-prediction rate over the 4 discriminating "
                        "square cells < 40% of valid outputs",
            "observed": f"rate={pooled_disc['rate']:.4f} "
                       f"({pooled_disc['on_prediction']}/{pooled_disc['valid']}) "
                       f"95%CI={pooled_disc['wilson_95ci']}",
            "fires": fp1,
        },
    }
    return verdicts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="arm_p_collect.jsonl")
    ap.add_argument("--output", default="arm_p_report.json")
    args = ap.parse_args()

    in_path = ROOT / args.input
    out_path = ROOT / args.output

    rows = load_rows(in_path)
    print(f"rows read from {in_path.name}: {len(rows)}")

    square_cells = score_group(rows, "square", build_square_specs())
    heldout_cells = score_group(rows, "heldout", build_heldout_specs())
    code_cells = score_code(rows)
    pooled_disc = pooled_discriminating_rate(square_cells)
    verdicts = evaluate_predictions(square_cells, heldout_cells, code_cells, pooled_disc)

    print("\n--- square (direct emission) ---")
    for n in SQUARE_N:
        c = square_cells[n]
        tag = "UNSCOREABLE" if not c["evaluable"] else ("HIT" if c["hit"] else "MISS")
        print(f"N={n:>2} k*={c['kstar']} predicted {c['predicted_value']:.7f}  "
              f"valid {c['valid_1e6']}/{c['sampled']} (1e-9: {c['valid_1e9']})  "
              f"modal {c['modal_value']} x{c['modal_count']}  {tag}  "
              f"on-pred {c['on_prediction']} rival {c['rival_emission']} "
              f"k*-struct {c['kstar_structure']}")

    print("\n--- held-out (direct emission) ---")
    for n in HELDOUT_N:
        c = heldout_cells[n]
        tag = "UNSCOREABLE" if not c["evaluable"] else ("HIT" if c["hit"] else "MISS")
        print(f"N={n:>2} k*={c['kstar']} predicted {c['predicted_value']:.7f}  "
              f"valid {c['valid_1e6']}/{c['sampled']} (1e-9: {c['valid_1e9']})  "
              f"modal {c['modal_value']} x{c['modal_count']}  {tag}  "
              f"on-pred {c['on_prediction']} rival {c['rival_emission']} "
              f"k*-struct {c['kstar_structure']}")

    print("\n--- code channel ---")
    for n in CODE_N:
        c = code_cells[n]
        print(f"N={n:>2}: sampled {c['sampled']}, bins {c['bins']}, "
              f"valid {c['n_valid']}, cleared(>{c['clearance_argmax']:.6f}) "
              f"{c['cleared']}{'  UNDERPOWERED' if not c['evaluable'] else ''}")

    print(f"\npooled discriminating-cell (N=13,21,31,43) on-prediction rate: "
          f"{pooled_disc['on_prediction']}/{pooled_disc['valid']} "
          f"= {pooled_disc['rate']:.4f}  Wilson95%={pooled_disc['wilson_95ci']}")

    print("\n--- registered predictions ---")
    for name, v in verdicts.items():
        key = "holds" if "holds" in v else "fires"
        print(f"{name}\n  {v['statement']}\n  observed: {v['observed']}\n  "
              f"{key.upper()}: {v[key]}")

    report = {
        "input": str(in_path.name), "rows": len(rows),
        "square": {str(n): square_cells[n] for n in SQUARE_N},
        "heldout": {str(n): heldout_cells[n] for n in HELDOUT_N},
        "code": {str(n): code_cells[n] for n in CODE_N},
        "pooled_discriminating": pooled_disc,
        "predictions": verdicts,
    }
    out_path.write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"\nwritten {out_path.name}")


if __name__ == "__main__":
    main()
