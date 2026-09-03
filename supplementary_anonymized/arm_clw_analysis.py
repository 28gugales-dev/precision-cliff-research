# ============================================================================
# Arm CL-W analysis -- arm CL's registered pipeline (arm_cl_analysis.py,
# imported unmodified: fence-tolerant extraction, AST gate math/numpy/scipy,
# python -I -S under the fixed driver, 120 s, one core, arm-F scoring,
# same taxonomy) applied to the top-up ledger AND, under the pooling rule
# registered in arm_clw_preregistration.txt, to arm CL's weak-tier rows, so
# the pooled 90 are scored in one pass by one scorer. Two readings of every
# row are reported: the registered parser (primary, the arm's verdict) and
# the lenient reading registered here as secondary (strip the numpy scalar
# wrapper `np.float64(...)`, nothing else). Writes arm_clw_report.json.
# ============================================================================
import json
import re
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import arm_cl_analysis as cl  # noqa: E402

CELLS = [13, 21, 31]
FLOOR = 5
WRAP = re.compile(r"np\.float64\(([^()]*)\)")


def score_both(raw, n):
    """Registered pipeline step by step, plus the lenient reading of the same stdout."""
    source = cl.strip_fences(raw) if raw else ""
    if not source.strip():
        return {"bin": "no_program", "lenient": None}
    ok, gate_bin = cl.ast_gate(source)
    if not ok:
        return {"bin": gate_bin, "lenient": None}
    err_bin, stdout = cl.run_program(source, 120)
    if err_bin:
        return {"bin": err_bin, "lenient": None}

    def read(text):
        packing, why = cl.parse_packing(text)
        if packing is None:
            return {"bin": "stdout_parse_fail", "why": why}
        ok6, why6 = cl.validate(packing, n, tol=1e-6)
        ok9, _ = cl.validate(packing, n, tol=1e-9)
        if not ok6:
            return {"bin": "geom_invalid", "why": why6, "valid_1e9": ok9}
        s = cl.score(packing)
        return {"bin": "valid", "sum": round(s, 9), "valid_1e6": ok6, "valid_1e9": ok9,
                "cleared": bool(ok9 and s > cl.ARGMAX[n] + cl.WINDOW_9),
                "n_distinct_radii": len({round(r, 6) for _, _, r in packing})}

    reg = read(stdout)
    reg["lenient"] = read(WRAP.sub(r"\1", stdout)) if reg["bin"] == "stdout_parse_fail" else None
    reg["uses_scipy_optimize"] = cl.uses_scipy_optimize(source)
    return reg


def main():
    new = cl.load_rows(HERE / "arm_clw_collect.jsonl")
    old = [r for r in cl.load_rows(HERE / "arm_cl_collect.jsonl") if r["tier"] == "weak"]
    for r in new:
        r["source_ledger"] = "arm_clw_collect.jsonl"
    for r in old:
        r["source_ledger"] = "arm_cl_collect.jsonl"
    rows = old + new
    print(f"scoring {len(old)} arm CL weak rows + {len(new)} CL-W rows, 120 s, 4 workers")
    with ThreadPoolExecutor(max_workers=4) as ex:
        scored = list(ex.map(lambda r: score_both(r["raw"], r["n"]), rows))
    report = {"pooling": "arm CL weak tier + CL-W, registered before CL-W sampled", "cells": {}, "per_ledger": {},
              "rows": [dict(ledger=r["source_ledger"], n=r["n"], sample_id=r["sample_id"], bin=s["bin"],
                            sum=s.get("sum"), valid_1e9=s.get("valid_1e9"), cleared=s.get("cleared"),
                            lenient=s.get("lenient")) for r, s in zip(rows, scored)]}
    for ledger in ("arm_cl_collect.jsonl", "arm_clw_collect.jsonl"):
        sc = [s for r, s in zip(rows, scored) if r["source_ledger"] == ledger]
        report["per_ledger"][ledger] = {"sampled": len(sc), "bins": dict(Counter(s["bin"] for s in sc)),
                                        "valid": sum(s["bin"] == "valid" for s in sc),
                                        "cleared": sum(s.get("cleared", False) for s in sc),
                                        "by_cell": {str(n): {"bins": dict(Counter(s["bin"] for r, s in zip(rows, scored)
                                                                                  if r["source_ledger"] == ledger and r["n"] == n)),
                                                             "valid": sum(s["bin"] == "valid" for r, s in zip(rows, scored)
                                                                          if r["source_ledger"] == ledger and r["n"] == n),
                                                             "lenient_valid": sum(1 for r, s in zip(rows, scored)
                                                                                  if r["source_ledger"] == ledger and r["n"] == n
                                                                                  and s["lenient"] and s["lenient"]["bin"] == "valid"),
                                                             "lenient_cleared": sum(1 for r, s in zip(rows, scored)
                                                                                    if r["source_ledger"] == ledger and r["n"] == n
                                                                                    and s["lenient"] and s["lenient"].get("cleared"))}
                                                    for n in CELLS}}
    pv = pc = lv = lc = 0
    for n in CELLS:
        sc = [s for r, s in zip(rows, scored) if r["n"] == n]
        valid = [s for s in sc if s["bin"] == "valid"]
        cleared = [s for s in valid if s["cleared"]]
        len_rec = [s["lenient"] for s in sc if s["lenient"] and s["lenient"]["bin"] == "valid"]
        len_clear = [s for s in len_rec if s["cleared"]]
        pv += len(valid); pc += len(cleared); lv += len(len_rec); lc += len(len_clear)
        report["cells"][str(n)] = {
            "sampled": len(sc), "bins": dict(Counter(s["bin"] for s in sc)),
            "n_valid": len(valid), "n_valid_1e9": sum(s["valid_1e9"] for s in valid),
            "n_cleared": len(cleared), "underpowered": len(valid) < FLOOR,
            "argmax_closed_form": round(cl.ARGMAX[n], 9),
            "sums": sorted(s["sum"] for s in valid), "cleared_sums": sorted(s["sum"] for s in cleared),
            "lenient_recovered_valid": len(len_rec), "lenient_recovered_cleared": len(len_clear),
            "lenient_recovered_sums": sorted(s["sum"] for s in len_rec),
            "lenient_recovered_cleared_sums": sorted(s["sum"] for s in len_clear),
        }
        print(f"n={n}: sampled {len(sc)}, bins {dict(Counter(s['bin'] for s in sc))}, valid {len(valid)}, "
              f"cleared {len(cleared)}; lenient +{len(len_rec)} valid, +{len(len_clear)} clear")
    rate = pc / pv if pv else None
    lrate = (pc + lc) / (pv + lv) if pv + lv else None
    if pv == 0:
        verdict = "UNSCOREABLE"
    elif rate >= 0.20:
        verdict = "P-CLW2 holds (>= 20% of valid clear under the registered parser); F-CLW1 fires"
    elif pc == 0:
        verdict = "P-CLW1 holds (0 clear under the registered parser)"
    else:
        verdict = f"dead zone: {pc} of {pv} clear under the registered parser"
    report["pooled"] = {"sampled": len(rows), "valid": pv, "cleared": pc, "clear_rate": rate,
                        "wilson_upper_95": cl_wilson(pc, pv) if pv else None,
                        "lenient_valid": pv + lv, "lenient_cleared": pc + lc, "lenient_rate": lrate,
                        "verdict": verdict, "falsifier_F_CLW1": bool(rate is not None and rate >= 0.20)}
    print("POOLED:", report["pooled"])
    (HERE / "arm_clw_report.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print("written arm_clw_report.json")


def cl_wilson(x, n, z=1.96):
    import math
    p = x / n
    return round((p + z * z / (2 * n) + z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / (1 + z * z / n), 4)


if __name__ == "__main__":
    main()
