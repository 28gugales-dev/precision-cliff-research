"""Arm GM runner — Gemini flash-lite cross-vendor replication.

Preregistration: arm_gm_preregistration.txt (commit 37b3adb), registered before
any task sampling. 20 samples x 7 N, byte-identical arm F bare prompts.
Key read from file passed as argv[1]; never printed, never committed.
"""
import json, sys, time, hashlib, threading, queue
import urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).parent
KEY = Path(sys.argv[1]).read_text().strip()
MODEL = sys.argv[2] if len(sys.argv) > 2 else "gemini-2.5-flash-lite"
SUFFIX = ("_" + sys.argv[3]) if len(sys.argv) > 3 else ""
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
NS = [13, 17, 21, 31, 35, 37, 43]
SAMPLES = 20

tmpl13 = json.loads((HERE / "arm_f_prompts.json").read_text())["13"]["prompt"]
PROMPTS = {n: tmpl13.replace("13", str(n)) for n in NS}
# verify registered hashes for the cells present in arm_f_prompts.json
reg = json.loads((HERE / "arm_f_prompts.json").read_text())
for n_str, obj in reg.items():
    n = int(n_str)
    if n in PROMPTS:
        assert hashlib.sha256(PROMPTS[n].encode()).hexdigest() == obj["sha256"], n

def call(prompt):
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 1.0, "maxOutputTokens": 4096},
    }).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "x-goog-api-key": KEY, "Content-Type": "application/json"})
    for attempt in range(8):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read()), attempt
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503):
                time.sleep(min(60, 5 * 2 ** attempt))
                continue
            return {"transport_error": f"HTTP {e.code}: {e.read()[:300].decode(errors='replace')}"}, attempt
        except Exception as e:  # timeout etc.
            time.sleep(5)
            err = str(e)
    return {"transport_error": err if 'err' in dir() else "retries exhausted"}, 8

# Checkpoint: one JSON row per line, appended immediately after each call.
# Restart skips (n, sample_idx) pairs already on disk. Interruptions discard
# only unsaved in-flight responses, unobserved (disclosed in ledger note).
CKPT = HERE / f"arm_gm{SUFFIX}_checkpoint.jsonl"
done_pairs = set()
if CKPT.exists():
    kept = []
    requeued = 0
    for line in CKPT.read_text().splitlines():
        if line.strip():
            r = json.loads(line)
            # transport errors are re-runnable per prereg (verbatim rerun,
            # disclosed); content responses are final.
            if "transport_error" in r["response"]:
                requeued += 1
                continue
            kept.append(line)
            done_pairs.add((r["n"], r["sample_idx"]))
    CKPT.write_text("\n".join(kept) + ("\n" if kept else ""))
    print(f"resuming: {len(done_pairs)} content rows kept, "
          f"{requeued} transport-error rows requeued", flush=True)

results = []
lock = threading.Lock()
jobs = queue.Queue()
for n in NS:
    for i in range(SAMPLES):
        if (n, i) not in done_pairs:
            jobs.put((n, i))

quota_dead = threading.Event()

def worker():
    while not quota_dead.is_set():
        try:
            n, i = jobs.get_nowait()
        except queue.Empty:
            return
        time.sleep(3.2)  # stay under free-tier RPM cap
        resp, retries = call(PROMPTS[n])
        if "transport_error" in resp:
            # quota exhausted for the day — stop burning the queue; the loop
            # reruns this script after reset and resumes from checkpoint
            print(f"quota dead at n={n} idx={i}: {resp['transport_error'][:100]}",
                  flush=True)
            quota_dead.set()
            return
        row = {"n": n, "sample_idx": i,
               "prompt_sha256": hashlib.sha256(PROMPTS[n].encode()).hexdigest(),
               "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "transport_retries": retries, "response": resp}
        with lock:
            results.append(row)
            with CKPT.open("a") as f:
                f.write(json.dumps(row) + "\n")
            done = len(results) + len(done_pairs)
            if done % 10 == 0:
                print(f"{done}/140", flush=True)

# Single worker: free tier = 20 requests/min for this model; 4 parallel
# threads exhausted retry budgets against the RPM cap on the first attempt.
threads = [threading.Thread(target=worker) for _ in range(1)]
[t.start() for t in threads]
[t.join() for t in threads]

# Final assembly from checkpoint (single source of truth).
all_rows = [json.loads(l) for l in CKPT.read_text().splitlines() if l.strip()]
all_rows.sort(key=lambda r: (r["n"], r["sample_idx"]))
if len(all_rows) == len(NS) * SAMPLES:
    (HERE / f"arm_gm{SUFFIX}_raw.json").write_text(json.dumps(
        {"model": MODEL, "endpoint": URL, "prereg_commit": "37b3adb",
         "temperature": 1.0,
         "note": "assembled from arm_gm_checkpoint.jsonl; run was "
                 "interruptible — in-flight responses at interruption were "
                 "discarded unobserved and their cells re-called",
         "rows": all_rows}, indent=1))
    errs = sum(1 for r in all_rows if "transport_error" in r["response"])
    print(f"COMPLETE: {len(all_rows)} rows, {errs} transport errors")
else:
    print(f"partial: {len(all_rows)}/{len(NS) * SAMPLES} rows — rerun to resume")
