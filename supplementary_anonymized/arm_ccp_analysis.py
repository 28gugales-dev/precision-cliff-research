# ============================================================================
# Arm CCP analysis -- arm CL's registered pipeline (arm_cl_analysis.py,
# imported unmodified) with the import allowlist narrowed to arm CC's:
# math only. Everything else is arm CL's: fence-tolerant extraction, the
# forbidden-name gate, python -I -S under the fixed driver, 120-second
# wall clock, one core, arm-F scoring, the same failure taxonomy. The
# driver's site-packages insertion is inert here because the AST gate
# rejects every numpy/scipy import before execution (binned
# blocked_import, as arm CC does). Reads arm_ccp_collect.jsonl, writes
# arm_ccp_report.json, prints the registered quantities and verdict.
# ============================================================================
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import arm_cl_analysis as cl  # noqa: E402

cl.ALLOWED_MODULES = {"math"}  # registered: arm CC's allowlist
CELLS = [13, 21, 31]
FLOOR = 5


def main():
    rows = [r for r in cl.load_rows(HERE / "arm_ccp_collect.jsonl") if r["tier"] == "sonnet"]
    print(f"scoring {len(rows)} rows, 120 s timeout, allowlist {sorted(cl.ALLOWED_MODULES)}")
    scored = cl.score_all(rows, timeout_s=120)
    by_key = {(r["n"], r["sample_id"]): s for r, s in zip(rows, scored)}
    report = {"allowlist": ["math"], "timeout_s": 120, "cells": {}}
    pooled_valid = pooled_clear = 0
    cells_at_20 = 0
    for n in CELLS:
        cell_rows = [r for r in rows if r["n"] == n]
        sc = [by_key[(n, r["sample_id"])] for r in cell_rows]
        bins = Counter(s["bin"] for s in sc)
        valid = [s for s in sc if s["bin"] == "valid"]
        cleared = [s for s in valid if s["cleared"]]
        v9 = sum(1 for s in valid if s["valid_1e9"])
        under = len(valid) < FLOOR
        rate = len(cleared) / len(valid) if valid else None
        if not under and rate is not None and rate >= 0.20:
            cells_at_20 += 1
        pooled_valid += len(valid)
        pooled_clear += len(cleared)
        report["cells"][str(n)] = {
            "sampled": len(cell_rows), "bins": dict(bins), "n_valid": len(valid),
            "n_valid_1e9": v9, "n_cleared": len(cleared), "clear_rate": rate,
            "argmax_closed_form": round(cl.ARGMAX[n], 9), "underpowered": under,
            "sums": sorted(round(s["sum"], 9) for s in valid),
            "cleared_sums": sorted(round(s["sum"], 9) for s in cleared),
            "k_struct_dist": dict(Counter(s["k_struct"] for s in valid)),
        }
        print(f"n={n}: sampled {len(cell_rows)}, bins {dict(bins)}, valid {len(valid)} "
              f"(1e-9: {v9}), cleared {len(cleared)}{' UNSCOREABLE' if under else ''}")
    if pooled_valid == 0:
        verdict = "UNSCOREABLE (no valid outputs)"
    elif pooled_clear == 0:
        verdict = "P-CCP1 holds (no valid output clears; the library is what clears)"
    elif cells_at_20 >= 2:
        verdict = "P-CCP2 holds (clearance at >= 20% of valid at >= 2 of 3 cells); F-CCP1 fires"
    else:
        verdict = f"neither (cleared {pooled_clear} of {pooled_valid}; compare per cell with arm CL)"
    report["pooled"] = {"sampled": len(rows), "valid": pooled_valid, "cleared": pooled_clear,
                        "cells_at_20pct": cells_at_20, "verdict": verdict,
                        "falsifier_F_CCP1": cells_at_20 >= 2}
    print(f"POOLED: valid {pooled_valid}/{len(rows)}, cleared {pooled_clear}; cells at >=20%: {cells_at_20}")
    print("VERDICT:", verdict)
    (HERE / "arm_ccp_report.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print("written arm_ccp_report.json")


if __name__ == "__main__":
    main()
