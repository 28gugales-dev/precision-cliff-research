# Two questions the first per-seed probe raised, both unscored (stdout discarded):
#   1. N = 73 seed 3 cost 224.969 s for ONE restart against a 17.1 s median -- a 13x outlier.
#      Seeds are deterministic, so re-timing it says whether that is the program's path or
#      machine noise. If it is the path, no restart count makes N = 73 fit a 120 s wall.
#   2. Cells 59 and 61 are the next discriminating cells of the same trap zone as 57. If their
#      worst seed fits, the primary reading keeps three cells and its "2 of 3" verdict map.
import contextlib
import io
import json
import time
from pathlib import Path

SRC = Path(r"C:\Users\soham\AppData\Local\hermes\research-corpus\precision-cliff\arm_b_baseline.py")
OUT = Path(__file__).with_name("armb_seed_timing2.json")
BUDGET, MARGIN = 120.0, 0.75
src = SRC.read_text(encoding="utf-8")


def one_restart(n, seed):
    body = (src.replace("__N__", str(n)).replace("__SEED__", str(seed))
               .replace("RESTARTS = 50", "RESTARTS = 1"))
    t0 = time.perf_counter()
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(body, "arm_b_baseline.py", "exec"), {"__name__": "__probe__"})
    return round(time.perf_counter() - t0, 3)


out = {"budget_s": BUDGET, "margin": MARGIN}
out["n73_seed3_retime"] = [one_restart(73, 3) for _ in range(2)]
print("N=73 seed 3 re-timed:", out["n73_seed3_retime"], "(first probe: 224.969)", flush=True)

out["cells"] = {}
for n in (59, 61):
    per = {s: one_restart(n, s) for s in range(1, 16)}
    worst = max(per.values())
    out["cells"][n] = {"per_seed_s": per, "worst_s": worst,
                       "median_s": sorted(per.values())[len(per) // 2],
                       "restarts_worst_case": int(MARGIN * BUDGET / worst)}
    print(n, "worst", worst, "median", out["cells"][n]["median_s"],
          "restarts", out["cells"][n]["restarts_worst_case"], flush=True)

OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
print("wrote", OUT)
