# Per-seed timing, one restart per seed, for the seeds arm B2 would actually use (1..15).
# The first probe timed seed 0 only and came out non-monotone in N (38.7 s/restart at N = 73
# against 19.7 at N = 75), which can only be SLSQP iteration count varying by seed: cost is
# not a function of N alone. A fixed restart count sized from one seed would therefore blow
# the 120 s wall on other seeds and turn live rows into timeouts. Sizes RESTARTS from the
# worst seed instead. Wall clock only: stdout is discarded, nothing is scored.
import contextlib
import io
import json
import time
from pathlib import Path

SRC = Path(r"C:\Users\soham\AppData\Local\hermes\research-corpus\precision-cliff\arm_b_baseline.py")
OUT = Path(__file__).with_name("armb_seed_timing.json")
CELLS = [57, 73, 91]
SEEDS = list(range(1, 16))
BUDGET = 120.0
MARGIN = 0.75

src = SRC.read_text(encoding="utf-8")
out = {"budget_s": BUDGET, "margin": MARGIN, "cells": {}}
for n in CELLS:
    per = {}
    for seed in SEEDS:
        body = (src.replace("__N__", str(n)).replace("__SEED__", str(seed))
                   .replace("RESTARTS = 50", "RESTARTS = 1"))
        t0 = time.perf_counter()
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(body, "arm_b_baseline.py", "exec"), {"__name__": "__probe__"})
        per[seed] = round(time.perf_counter() - t0, 3)
    worst = max(per.values())
    out["cells"][n] = {"per_seed_s": per, "worst_s": worst, "median_s": sorted(per.values())[len(per) // 2],
                       "restarts_worst_case": int(MARGIN * BUDGET / worst)}
    print(n, out["cells"][n]["worst_s"], out["cells"][n]["median_s"],
          out["cells"][n]["restarts_worst_case"], flush=True)

OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
print("wrote", OUT)
