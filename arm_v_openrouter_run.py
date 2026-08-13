# Arm V OpenRouter runner. Prereg: arm_v_preregistration.md (5444f10) +
# amendment 2 (must be committed before this executes; ancestry-checked).
#
# Direct chat-completions API. The API key comes ONLY from the
# OPENROUTER_API_KEY environment variable and is never written anywhere.
# Same live ledger as the opencode runner; rows are distinguishable by the
# runtime field. Resume: completed (model, n, sample_id) rows are skipped.
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "arm_v_candidates_raw.jsonl"
RUN_DATE = "2026-08-12"
PREREG_COMMIT = "5444f10"
AMENDMENT = "amendment2"

MODELS = [
    "google/gemma-4-31b-it:free",
    "openai/gpt-oss-20b:free",
    "cohere/north-mini-code:free",
    "liquid/lfm-2.5-2.6b:free",
    "nvidia/nemotron-3-ultra-550b-a55b:free",
]
TARGET_N = [13, 17, 31, 35, 37]
SAMPLES = 5
CALL_TIMEOUT = 240
MAX_WORKERS = 3
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"


def load_prompts():
    d = json.loads((ROOT / "arm_f_prompts.json").read_text(encoding="utf-8"))
    prompts = {}
    for n in TARGET_N:
        p = d[str(n)]["prompt"]
        h = hashlib.sha256(p.encode("utf-8")).hexdigest()
        if h != d[str(n)]["sha256"]:
            sys.exit(f"prompt hash mismatch for N={n}; refusing to sample")
        prompts[n] = (p, h)
    return prompts


def call(model, prompt, key):
    body = {"model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 8192}
    req = urllib.request.Request(
        ENDPOINT, data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}",
                 "Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=CALL_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        dur = time.time() - t0
        choice = (data.get("choices") or [{}])[0]
        text = (choice.get("message") or {}).get("content") or ""
        meta = {"served_model": data.get("model"),
                "generation_id": data.get("id"),
                "finish_reason": choice.get("finish_reason"),
                "usage": data.get("usage")}
        return text, None, meta, dur
    except Exception as e:
        detail = ""
        if hasattr(e, "read"):
            try:
                detail = e.read().decode("utf-8", "replace")[:500]
            except Exception:
                pass
        return "", f"{type(e).__name__}: {e} {detail}"[:800], {}, time.time() - t0


def existing_keys():
    done = set()
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("raw_len", 0) > 0:
                done.add((r["proposer_alias"], r["n"], r["sample_id"]))
    return done


def worker(model, prompts, key, lock, done):
    short = model.split("/")[-1]
    for n in TARGET_N:
        prompt, sha = prompts[n]
        for sid in range(1, SAMPLES + 1):
            if (model, n, sid) in done:
                continue
            raw, err, meta, dur = call(model, prompt, key)
            row = {
                "reconstructed": False,
                "run_date": RUN_DATE,
                "prereg_commit": PREREG_COMMIT,
                "prereg_amendment": AMENDMENT,
                "proposer_alias": model,
                "runtime": "openrouter-chat-completions",
                "request_params": {"max_tokens": 8192,
                                   "note": "temperature/top_p provider defaults, unattested"},
                "sampling_params": None,
                "n": n,
                "arm": "vendor",
                "sample_id": sid,
                "prompt_sha256": sha,
                "raw_output": raw,
                "raw_len": len(raw),
                "call_error": err,
                "serving_meta": meta,
                "duration_s": round(dur, 1),
            }
            with lock:
                with OUT.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(row) + "\n")
                print(f"{short:34s} N={n:>2} s{sid}  len={len(raw):5d} "
                      f"{dur:5.1f}s {err or ''}", flush=True)
            time.sleep(3)  # stay under the free-model per-minute limit


def main():
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY not set")
    head = subprocess.run(["git", "merge-base", "--is-ancestor", PREREG_COMMIT, "HEAD"],
                          cwd=str(ROOT), capture_output=True)
    if head.returncode != 0:
        sys.exit("prereg commit is not an ancestor of HEAD; refusing to sample")
    amend = subprocess.run(["git", "log", "--oneline", "--all"],
                           cwd=str(ROOT), capture_output=True, text=True)
    if "amendment 2" not in amend.stdout and "amendment2" not in amend.stdout:
        sys.exit("amendment 2 not committed; refusing to sample")
    models = sys.argv[1:] or MODELS
    prompts = load_prompts()
    done = existing_keys()
    if done:
        print(f"resume: {len(done)} completed invocations skipped")
    import threading
    lock = threading.Lock()
    with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(models))) as ex:
        for m in models:
            ex.submit(worker, m, prompts, key, lock, done)
    print("done")


if __name__ == "__main__":
    main()
