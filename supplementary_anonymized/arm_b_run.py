# Arm B runner: builds the 45 baseline "rows" (arm_b_baseline.py with N and SEED substituted,
# seeds 1..15 per cell, cells 13/21/31) and scores them through arm CL's registered pipeline
# unmodified (arm_cl_analysis.score_all: python -I -S, the fixed driver, 120 s wall clock, one
# core per subprocess, arm-F scoring, section 2.4's clearance rule). No model is called. Writes
# arm_b_collect.jsonl (the substituted sources, verbatim) and arm_b_report.json.
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import arm_cl_analysis as cl  # noqa: E402

CELLS = [13, 21, 31]
SEEDS = list(range(1, 16))
FLOOR = 5
TEMPLATE = (HERE / "arm_b_baseline.py").read_text(encoding="utf-8")
TEMPLATE_SHA = hashlib.sha256(TEMPLATE.encode("utf-8")).hexdigest()
# Sonnet-tier best program per cell in arm CL (arm_cl_report.json), for the secondary S-B1.
SONNET_BEST = {13: 1.820699211, 21: 2.340549845, 31: 2.864990189}


def main():
    rows = []
    for n in CELLS:
        for seed in SEEDS:
            src = TEMPLATE.replace("__N__", str(n)).replace("__SEED__", str(seed))
            rows.append({"tier": "baseline", "n": n, "sample_id": seed, "raw": src,
                         "template_sha256": TEMPLATE_SHA})
    with open(HERE / "arm_b_collect.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print(f"template sha256 {TEMPLATE_SHA[:12]}; scoring {len(rows)} rows, 120 s wall clock, "
          f"{cl.MAX_EXEC_WORKERS} concurrent subprocesses (one core each)")
    scored = cl.score_all(rows, timeout_s=120)
    report = {"template_sha256": TEMPLATE_SHA, "timeout_s": 120, "cells": {}}
    pooled_valid = pooled_clear = cells_at_20 = 0
    for n in CELLS:
        sc = [s for r, s in zip(rows, scored) if r["n"] == n]
        bins = Counter(s["bin"] for s in sc)
        valid = [s for s in sc if s["bin"] == "valid"]
        cleared = [s for s in valid if s["cleared"]]
        v9 = sum(1 for s in valid if s["valid_1e9"])
        rate = len(cleared) / len(valid) if valid else None
        under = len(valid) < FLOOR
        if not under and rate is not None and rate >= 0.20:
            cells_at_20 += 1
        pooled_valid += len(valid)
        pooled_clear += len(cleared)
        best = max((s["sum"] for s in valid), default=None)
        report["cells"][str(n)] = {
            "sampled": len(sc), "bins": dict(bins), "n_valid": len(valid), "n_valid_1e9": v9,
            "n_cleared": len(cleared), "clear_rate": rate, "underpowered": under,
            "argmax_closed_form": round(cl.ARGMAX[n], 9),
            "sums": sorted(round(s["sum"], 9) for s in valid),
            "cleared_sums": sorted(round(s["sum"], 9) for s in cleared),
            "best_sum": round(best, 9) if best is not None else None,
            "sonnet_best_arm_cl": SONNET_BEST[n],
            "best_exceeds_sonnet_best": (best is not None and best > SONNET_BEST[n]),
            "k_struct_dist": dict(Counter(s["k_struct"] for s in valid)),
        }
        print(f"n={n}: bins {dict(bins)}, valid {len(valid)} (1e-9: {v9}), cleared {len(cleared)}, "
              f"best {best}, Sonnet best {SONNET_BEST[n]}")
    if pooled_valid == 0:
        verdict = "UNSCOREABLE (no valid outputs)"
    elif cells_at_20 >= 2:
        verdict = "P-B1 holds (the reference program clears at >= 20% at >= 2 of 3 cells): the optimizer alone clears the family"
    elif pooled_clear == 0:
        verdict = "P-B2 holds (the reference program never clears): the Sonnet programs' design carries the clearance"
    else:
        verdict = f"neither (cleared {pooled_clear} of {pooled_valid}, cells at >= 20%: {cells_at_20})"
    report["pooled"] = {"sampled": len(rows), "valid": pooled_valid, "cleared": pooled_clear,
                        "cells_at_20pct": cells_at_20, "verdict": verdict,
                        "S_B1_cells_where_baseline_best_exceeds_sonnet_best":
                            [n for n in CELLS if report["cells"][str(n)]["best_exceeds_sonnet_best"]]}
    print("POOLED:", report["pooled"])
    print("VERDICT:", verdict)
    (HERE / "arm_b_report.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print("written arm_b_report.json")


if __name__ == "__main__":
    main()
