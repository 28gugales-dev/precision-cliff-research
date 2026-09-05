# Arm B2 runner (registration arm_b2_preregistration.txt, committed 00a1b69 before sampling).
# Builds rows from arm_b_baseline.py with N, SEED and RESTARTS substituted, and scores them
# through arm CL's registered pipeline. No model is called.
#
#   primary   budget-matched, in-pipeline: N = 57 (7 restarts), 59 (5), 120 s wall
#   secondary restart-matched, off-pipeline: N = 57, 73, 91 at the published 50 restarts,
#             wall lifted to 3600 s
#
# Two mechanical notes, neither a change to the scorer. First, arm_cl_analysis.ARGMAX is built
# for the original cells only, so the new cells' closed-form argmaxes are inserted before
# scoring -- same function, same closed form. Second, that closed form takes the drop-and-fill
# branch at k = isqrt(N); this file checks it against an independent maximum over every
# admissible (k, m) and every truncation, and refuses to run if they disagree, which is what
# excludes cells like N = 63 where truncation wins.
#
# Usage: python arm_b2_run.py primary | secondary [workers]
#
# Mechanical note, added after the primary reading ran and before the secondary finished:
# the secondary is scored cell by cell with a partial report written after each cell, and the
# worker count is a command-line argument. The primary ran with this file's earlier version
# (corpus 9fc6e34) at the pipeline's 4 workers; the secondary's first launch at 4 workers was
# stopped in its N = 73 cell after two hours (heavy seeds fill the 3600 s wall, so 45 rows on
# 4 workers projected to eight hours) and relaunched at 12 workers on the 22-core machine, one
# core per subprocess, no core shared. Rows, seeds, program, wall and scorer are unchanged;
# the worker count is disclosed in the report.
import hashlib
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import arm_cl_analysis as cl  # noqa: E402

READINGS = {
    "primary": {"cells": {57: 7, 59: 5}, "timeout_s": 120, "in_pipeline": True},
    "secondary": {"cells": {57: 50, 73: 50, 91: 50}, "timeout_s": 3600, "in_pipeline": False},
}
SEEDS = list(range(1, 16))
FLOOR = 5
TEMPLATE = (HERE / "arm_b_baseline.py").read_text(encoding="utf-8")
TEMPLATE_SHA = hashlib.sha256(TEMPLATE.encode("utf-8")).hexdigest()
assert TEMPLATE_SHA.startswith("298ba71c9f20"), "template is not the registered arm B program"
S2 = math.sqrt(2) - 1


def family_best(n):
    """Independent maximum over the whole family: every drop-and-fill V(k, m) with
    N = k^2 + m and m <= (k-1)^2, and every truncation T(k, N) = N/(2k) with k^2 >= N."""
    best = -1.0
    for k in range(1, n + 1):
        if k * k <= n and n - k * k <= (k - 1) ** 2:
            best = max(best, k / 2 + (n - k * k) * S2 / (2 * k))
        if k * k >= n:
            best = max(best, n / (2 * k))
    return best


def main(reading, workers):
    spec = READINGS[reading]
    for n in spec["cells"]:
        closed = cl.argmax_closed_form(n)
        assert abs(closed - family_best(n)) < 1e-12, \
            f"N={n}: closed form {closed} is not the family maximum {family_best(n)}"
        cl.ARGMAX[n] = closed

    rows = []
    for n, restarts in spec["cells"].items():
        for seed in SEEDS:
            src = (TEMPLATE.replace("__N__", str(n)).replace("__SEED__", str(seed))
                           .replace("RESTARTS = 50", f"RESTARTS = {restarts}"))
            rows.append({"tier": "baseline", "n": n, "sample_id": seed, "raw": src,
                         "restarts": restarts, "reading": reading,
                         "template_sha256": TEMPLATE_SHA})
    collect = HERE / f"arm_b2_collect_{reading}.jsonl"
    with collect.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

    print(f"{reading}: {len(rows)} rows, {spec['timeout_s']} s wall, "
          f"cells {spec['cells']}, sha {TEMPLATE_SHA[:12]}, {workers} workers", flush=True)
    scored = [None] * len(rows)
    partial = HERE / f"arm_b2_partial_{reading}.json"
    done = {}
    for n in spec["cells"]:
        idx = [i for i, r in enumerate(rows) if r["n"] == n]
        t0 = time.time()
        out = cl.score_all([rows[i] for i in idx], timeout_s=spec["timeout_s"], max_workers=workers)
        for i, s in zip(idx, out):
            scored[i] = s
        done[str(n)] = {"rows": len(idx), "wall_s": round(time.time() - t0),
                        "bins": dict(Counter(s["bin"] for s in out)),
                        "cleared": sum(1 for s in out if s["bin"] == "valid" and s["cleared"])}
        partial.write_text(json.dumps({"reading": reading, "workers": workers, "cells_done": done},
                                      indent=1), encoding="utf-8")
        print(f"cell {n} scored: {done[str(n)]}", flush=True)

    report = {"reading": reading, "in_pipeline": spec["in_pipeline"],
              "timeout_s": spec["timeout_s"], "template_sha256": TEMPLATE_SHA,
              "restarts_per_cell": spec["cells"], "workers": workers,
              "wall_s_per_cell": {k: v["wall_s"] for k, v in done.items()}, "cells": {}}
    cells_at_20 = pooled_valid = pooled_clear = 0
    for n in spec["cells"]:
        sc = [s for r, s in zip(rows, scored) if r["n"] == n]
        valid = [s for s in sc if s["bin"] == "valid"]
        cleared = [s for s in valid if s["cleared"]]
        rate = len(cleared) / len(valid) if valid else None
        under = len(valid) < FLOOR
        if not under and rate is not None and rate >= 0.20:
            cells_at_20 += 1
        pooled_valid += len(valid)
        pooled_clear += len(cleared)
        best = max((s["sum"] for s in valid), default=None)
        anchor = n / (2 * round(math.sqrt(n)))
        report["cells"][str(n)] = {
            "restarts": spec["cells"][n], "sampled": len(sc), "bins": dict(Counter(s["bin"] for s in sc)),
            "n_valid": len(valid), "n_valid_1e9": sum(1 for s in valid if s["valid_1e9"]),
            "n_cleared": len(cleared), "clear_rate": rate, "underpowered": under,
            "argmax_closed_form": round(cl.ARGMAX[n], 9), "anchor_truncate": round(anchor, 9),
            "best_sum": round(best, 9) if best is not None else None,
            "best_exceeds_anchor": (best is not None and best > anchor),
            "sums": sorted(round(s["sum"], 9) for s in valid),
        }
        print(f"n={n}: {report['cells'][str(n)]['bins']}, valid {len(valid)}, "
              f"cleared {len(cleared)}, best {best}, argmax {cl.ARGMAX[n]:.7f}", flush=True)

    n_cells = len(spec["cells"])
    if reading == "primary":
        verdict = ("P-B2-1 holds (clears at >= 20% at 2 of 2 cells)" if cells_at_20 == 2
                   else f"P-B2-2 holds (clears at {cells_at_20} of {n_cells} cells): "
                        "contribution 1 is scoped to the measured cells")
    else:
        verdict = ("S-B2-1 holds (>= 2 of 3 cells at 50 restarts)" if cells_at_20 >= 2
                   else f"S-B2-1 does not hold ({cells_at_20} of {n_cells} cells)")
    report["pooled"] = {
        "sampled": len(rows), "valid": pooled_valid, "cleared": pooled_clear,
        "cells_at_20pct": cells_at_20, "verdict": verdict,
        "S_B2_2_best_exceeds_anchor_cells": [n for n in spec["cells"]
                                             if report["cells"][str(n)]["best_exceeds_anchor"]],
    }
    print("POOLED:", report["pooled"], flush=True)
    (HERE / f"arm_b2_report_{reading}.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"written arm_b2_report_{reading}.json")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else cl.MAX_EXEC_WORKERS)
