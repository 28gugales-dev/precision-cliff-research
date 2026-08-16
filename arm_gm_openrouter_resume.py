# Arm GM OpenRouter resume runner. Prereg: arm_gm_preregistration.txt (37b3adb);
# deviation registered in arm_gm_amendment1_openrouter.md, which must be
# COMMITTED before this executes (checked below). Key comes ONLY from the
# OPENROUTER_API_KEY environment variable; never printed, never written.
#
# Fills the 85 cells missing from arm_gm_checkpoint.jsonl via
# openrouter.ai with the exact prereg model id. Same ledger, same resume
# rule as arm_gm_run.py; resumed rows are tagged serving_path=openrouter
# and store the raw OpenRouter response (provider name included).
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CKPT = HERE / "arm_gm_checkpoint.jsonl"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
MODEL = sys.argv[1] if len(sys.argv) > 1 else "google/gemini-2.5-flash-lite"
NS = [13, 17, 21, 31, 35, 37, 43]
SAMPLES = 20
MAX_TOKENS = 4096  # GM prereg (37b3adb)
TEMPERATURE = 1.0
TIMEOUT = 420

KEY = os.environ.get("OPENROUTER_API_KEY", "")
if not KEY:
    sys.exit("OPENROUTER_API_KEY not set; refusing to run")

log = subprocess.run(
    ["git", "log", "--oneline", "--", "arm_gm_amendment1_openrouter.md"],
    cwd=str(HERE), capture_output=True, text=True)
if not log.stdout.strip():
    sys.exit("amendment 1 not committed; refusing to sample off-register")

tmpl13 = json.loads((HERE / "arm_f_prompts.json").read_text())["13"]["prompt"]
PROMPTS = {n: tmpl13.replace("13", str(n)) for n in NS}
reg = json.loads((HERE / "arm_f_prompts.json").read_text())
for n_str, obj in reg.items():
    n = int(n_str)
    if n in PROMPTS:
        assert hashlib.sha256(PROMPTS[n].encode()).hexdigest() == obj["sha256"], n

done = set()
for line in CKPT.read_text().splitlines():
    if line.strip():
        r = json.loads(line)
        if "transport_error" not in r["response"]:
            done.add((r["n"], r["sample_idx"]))
todo = [(n, i) for n in NS for i in range(SAMPLES) if (n, i) not in done]
print(f"resume: {len(done)} content rows on disk, {len(todo)} cells to sample")


def call(prompt):
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
    }).encode()
    last_err = ""
    for attempt in range(6):
        req = urllib.request.Request(ENDPOINT, data=body, headers={
            "Authorization": f"Bearer {KEY}",
            "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return json.loads(r.read()), attempt
        except urllib.error.HTTPError as e:
            detail = e.read()[:300].decode(errors="replace")
            last_err = f"HTTP {e.code}: {detail}"
            if e.code in (408, 429, 500, 502, 503):
                time.sleep(45 if e.code == 429 else min(60, 5 * 2 ** attempt))
                continue
            return {"transport_error": last_err}, attempt
        except Exception as e:
            last_err = str(e)
            time.sleep(10)
    return {"transport_error": last_err or "retries exhausted"}, 6


count = 0
for n, i in todo:
    time.sleep(4)
    resp, retries = call(PROMPTS[n])
    row = {
        "n": n, "sample_idx": i,
        "prompt_sha256": hashlib.sha256(PROMPTS[n].encode()).hexdigest(),
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "transport_retries": retries,
        "serving_path": "openrouter",
        "openrouter_model": MODEL,
        "request_params": {"temperature": TEMPERATURE, "max_tokens": MAX_TOKENS},
        "response": resp,
    }
    with CKPT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
    ok = "transport_error" not in resp
    provider = resp.get("provider", "?") if ok else resp["transport_error"][:80]
    count += 1 if ok else 0
    print(f"N={n:>2} s{i:>2} {'ok' if ok else 'ERR'} provider={provider} "
          f"retries={retries} ({len(done) + count}/140)", flush=True)

print(f"done: {len(done) + count}/140 content rows"
      + ("" if len(done) + count == 140 else " — rerun to retry failures"))
