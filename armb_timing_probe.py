# UNSCORED timing probe, outside the gate, exactly the precedent of arm B amendment 1
# ("80 restarts fit in 95 s at N = 31 on one core"). Measures restarts-per-120 s for the
# frozen arm B program at candidate trap cells. No model, no serving path, no scoring:
# nothing here can become a result, it only sizes the RESTARTS constant for a registration.
import contextlib
import io
import json
import time
from pathlib import Path

SRC = Path(r"C:\Users\soham\AppData\Local\hermes\research-corpus\precision-cliff\arm_b_baseline.py")
OUT = Path(__file__).with_name("armb_timing_probe.json")
CELLS = [31, 57, 63, 75, 80]
PROBE_RESTARTS = 3
BUDGET = 120.0

src = SRC.read_text(encoding="utf-8")
rows = []
for n in CELLS:
    body = (src.replace("__N__", str(n)).replace("__SEED__", "0")
               .replace("RESTARTS = 50", f"RESTARTS = {PROBE_RESTARTS}"))
    t0 = time.perf_counter()
    ns = {"__name__": "__probe__"}
    buf = io.StringIO()  # the program prints the whole packing; only the clock matters here
    with contextlib.redirect_stdout(buf):
        exec(compile(body, "arm_b_baseline.py", "exec"), ns)
    dt = time.perf_counter() - t0
    per = dt / PROBE_RESTARTS
    rows.append({"n": n, "probe_restarts": PROBE_RESTARTS, "seconds_total": round(dt, 2),
                 "seconds_per_restart": round(per, 3),
                 "restarts_in_120s": int(BUDGET / per)})
    print(rows[-1], flush=True)

OUT.write_text(json.dumps({"budget_s": BUDGET, "rows": rows}, indent=2), encoding="utf-8")
print("wrote", OUT)
