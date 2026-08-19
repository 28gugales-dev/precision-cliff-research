# ============================================================================
# Arms CC2 (weak-tier fresh-draw replication) and CCS (Sonnet tier) analysis.
# Reuses arm CC's registered scoring pipeline unmodified (score_row import).
# Reads arm_cc2_collect.jsonl and arm_ccs_collect.jsonl; writes
# arm_cc2_report.json and arm_ccs_report.json; prints registered verdicts.
# Committed with arm_cc2_preregistration.txt, before sampling. No arguments.
# ============================================================================
import json
from collections import Counter
from pathlib import Path

from arm_cc_analysis import score_row, ANCHOR, RIVAL, WINDOW, CELLS

HERE = Path(__file__).parent


def bucket(v):
    return round(v / WINDOW)


def analyse(ledger_name, report_name):
    rows = [json.loads(line) for line in
            (HERE / ledger_name).read_text(encoding="utf-8").splitlines()
            if line.strip()]
    report = {"cells": {}, "pooled": {}}
    pooled_valid = 0
    pooled_above_rival = 0
    pooled_anchor = 0
    modal_anchor_cells = 0
    evaluable_cells = 0
    for n in CELLS:
        cell_rows = [r for r in rows if r["cell"] == n]
        scored = [score_row(r["raw"], n) for r in cell_rows]
        bins = Counter(s["bin"] for s in scored)
        valid = [s for s in scored if s["bin"] == "valid"]
        pooled_valid += len(valid)
        pooled_above_rival += sum(s["above_rival"] for s in valid)
        pooled_anchor += sum(s["on_anchor"] for s in valid)
        cell = {"sampled": len(cell_rows), "bins": dict(bins),
                "n_valid": len(valid), "underpowered": len(valid) < 5}
        if valid:
            buckets = Counter(bucket(s["sum"]) for s in valid)
            top = buckets.most_common()
            modal_bucket, modal_count = top[0]
            tie = len(top) > 1 and top[1][1] == modal_count
            modal_val = modal_bucket * WINDOW
            cell.update({
                "modal_value_approx": round(modal_val, 4),
                "modal_count": modal_count, "modal_tie": tie,
                "modal_margin": modal_count - (top[1][1] if len(top) > 1 else 0),
                "anchor_rate": f"{sum(s['on_anchor'] for s in valid)}/{len(valid)}",
                "argmax_rate": f"{sum(s['on_argmax'] for s in valid)}/{len(valid)}",
                "above_rival_rate": f"{sum(s['above_rival'] for s in valid)}/{len(valid)}",
                "k_struct_dist": dict(Counter(s["k_struct"] for s in valid)),
                "sums": sorted(round(s["sum"], 7) for s in valid),
            })
            if not cell["underpowered"]:
                evaluable_cells += 1
                if not tie and abs(modal_val - ANCHOR[n]) <= WINDOW:
                    modal_anchor_cells += 1
        report["cells"][str(n)] = cell
        print(f"  n={n}: sampled {len(cell_rows)}, bins {dict(bins)}")
        if valid:
            print(f"    modal ~{cell['modal_value_approx']} x{cell['modal_count']}"
                  f" (tie={cell['modal_tie']}, margin={cell['modal_margin']})"
                  f" anchor {cell['anchor_rate']}"
                  f" above-rival {cell['above_rival_rate']}"
                  f"{' UNDERPOWERED' if cell['underpowered'] else ''}")
    report["pooled"] = {
        "valid": pooled_valid, "above_rival": pooled_above_rival,
        "anchor": pooled_anchor, "modal_anchor_cells": modal_anchor_cells,
        "evaluable_cells": evaluable_cells,
    }
    (HERE / report_name).write_text(json.dumps(report, indent=1),
                                    encoding="utf-8")
    return report


def main():
    print("=== ARM CC2 (weak tier, fresh draws) ===")
    cc2 = analyse("arm_cc2_collect.jsonl", "arm_cc2_report.json")
    p = cc2["pooled"]
    r1 = p["above_rival"] <= 1              # 0 predicted; 1 = one-off exception
    falsifier = p["above_rival"] >= 2
    r2 = p["modal_anchor_cells"] >= 2
    if falsifier:
        verdict = "FAILED (F-CC2.1 fired: >=2 above-rival)"
    elif r1 and r2:
        verdict = "REPLICATED"
    elif r1:
        verdict = ("PARTIAL: the ceiling replicates; the modal identity "
                   "does not")
    print(f"CC2 pooled: valid {p['valid']}, above-rival {p['above_rival']}, "
          f"anchor {p['anchor']}, modal-anchor cells {p['modal_anchor_cells']}"
          f"/{p['evaluable_cells']}")
    print(f"CC2 VERDICT: {verdict}")

    print("=== ARM CCS (Sonnet tier) ===")
    ccs = analyse("arm_ccs_collect.jsonl", "arm_ccs_report.json")
    q = ccs["pooled"]
    rate = (q["above_rival"] / q["valid"]) if q["valid"] else 0.0
    if q["valid"] < 15:
        sverdict = f"UNDERPOWERED (pooled valid {q['valid']} < 15)"
    elif q["above_rival"] == 0:
        sverdict = "P-CCS2 holds (ceiling is a channel property here)"
    elif rate > 0.20 + 1e-12:   # exact tie on the threshold counts against
        sverdict = "P-CCS1 holds (escape is capability-gated)"
    else:
        sverdict = ("PARTIAL: the ceiling leaks at the Sonnet tier without "
                    "the escape prediction holding")
    print(f"CCS pooled: valid {q['valid']}, above-rival {q['above_rival']} "
          f"({rate:.1%}), anchor {q['anchor']}")
    print(f"CCS VERDICT: {sverdict}")


if __name__ == "__main__":
    main()
