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
MODEL = "gemini-2.5-flash-lite"
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

results = []
lock = threading.Lock()
jobs = queue.Queue()
for n in NS:
    for i in range(SAMPLES):
        jobs.put((n, i))

def worker():
    while True:
        try:
            n, i = jobs.get_nowait()
        except queue.Empty:
            return
        resp, retries = call(PROMPTS[n])
        row = {"n": n, "sample_idx": i,
               "prompt_sha256": hashlib.sha256(PROMPTS[n].encode()).hexdigest(),
               "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "transport_retries": retries, "response": resp}
        with lock:
            results.append(row)
            done = len(results)
            if done % 10 == 0:
                print(f"{done}/140", flush=True)

threads = [threading.Thread(target=worker) for _ in range(4)]
[t.start() for t in threads]
[t.join() for t in threads]

results.sort(key=lambda r: (r["n"], r["sample_idx"]))
(HERE / "arm_gm_raw.json").write_text(json.dumps(
    {"model": MODEL, "endpoint": URL, "prereg_commit": "37b3adb",
     "temperature": 1.0, "rows": results}, indent=1))
errs = sum(1 for r in results if "transport_error" in r["response"])
print(f"done: {len(results)} rows, {errs} transport errors")
