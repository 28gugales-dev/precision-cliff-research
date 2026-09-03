# ============================================================================
# Arm CL collection runner. Prereg: arm_cl_preregistration.txt (2026-09-02).
# Prompts/hashes frozen in arm_cl_prompts.json (arm_cl_build.py output),
# committed before this executes.
#
# Mirrors arm_v_openrouter_run.py's call shape: direct OpenRouter
# chat-completions HTTP call via urllib, live-appended JSONL ledger,
# resume-by-skip, ThreadPoolExecutor for concurrency.
#
# The API key comes ONLY from the OPENROUTER_API_KEY environment variable.
# It is never written to disk, logged, or printed -- not even in --dry-run,
# which prints the request body (no Authorization header) and exits.
#
# Two tiers x three cells (N=13,21,31) x n=15 = 90 rows. Serial per
# (tier, cell) with 3s spacing between calls in that group; up to 4 worker
# groups run concurrently. Registered decoding: temperature 1.0, max_tokens
# 16384, no system prompt, one user turn = the registered prompt verbatim.
# ============================================================================
import hashlib
import json
import os
import sys
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROMPTS_PATH = ROOT / "arm_cl_prompts.json"
OUT = ROOT / "arm_cl_collect.jsonl"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

CELLS = [13, 21, 31]
N_SAMPLES = 15
TEMPERATURE = 1.0
MAX_TOKENS = 16384
CALL_TIMEOUT = 300  # HTTP timeout per attempt; generous for optimizer-heavy output
INTRA_GROUP_SPACING_S = 3
MAX_GROUP_WORKERS = 4
MAX_RETRIES = 3  # on 429/5xx, per the registration

_data = json.loads(PROMPTS_PATH.read_text(encoding="utf-8"))
TIERS = _data["tiers"]  # {"weak": "anthropic/claude-haiku-4.5", "sonnet": "anthropic/claude-sonnet-4.5"}
CL = _data["cl"]  # {"13": {prompt, sha256, ...}, ...}

_write_lock = threading.Lock()


def now_utc():
    return datetime.now(timezone.utc).isoformat()


def load_prompts():
    prompts = {}
    for n in CELLS:
        rec = CL[str(n)]
        p = rec["prompt"]
        h = hashlib.sha256(p.encode("utf-8")).hexdigest()
        if h != rec["sha256"]:
            sys.exit(f"prompt hash mismatch for N={n}; refusing to sample")
        prompts[n] = (p, h)
    return prompts


def build_body(model, prompt):
    return {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
    }


def call(model, prompt, key):
    """One OpenRouter call with retry on 429/5xx up to MAX_RETRIES extra
    attempts. Returns (raw_text, call_error, meta, latency_s)."""
    body = build_body(model, prompt)
    data = json.dumps(body).encode("utf-8")
    last_err = None
    attempt = 0
    while True:
        attempt += 1
        t0 = time.time()
        req = urllib.request.Request(
            ENDPOINT, data=data,
            headers={"Authorization": f"Bearer {key}",
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=CALL_TIMEOUT) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            choice = (payload.get("choices") or [{}])[0]
            text = (choice.get("message") or {}).get("content") or ""
            meta = {
                "served_model": payload.get("model"),
                "generation_id": payload.get("id"),
                "finish_reason": choice.get("finish_reason"),
                "usage": payload.get("usage"),
                "attempts": attempt,
            }
            return text, None, meta, time.time() - t0
        except urllib.error.HTTPError as e:
            detail = ""
            try:
                detail = e.read().decode("utf-8", "replace")[:800]
            except Exception:
                pass
            last_err = f"HTTPError {e.code}: {e.reason} {detail}"[:1000]
            retryable = e.code == 429 or 500 <= e.code < 600
            if retryable and attempt <= MAX_RETRIES:
                time.sleep(min(60, 5 * (2 ** (attempt - 1))))
                continue
            return "", last_err, {"attempts": attempt, "http_status": e.code}, time.time() - t0
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"[:1000]
            if attempt <= MAX_RETRIES:
                time.sleep(min(60, 5 * (2 ** (attempt - 1))))
                continue
            return "", last_err, {"attempts": attempt}, time.time() - t0


def existing_done():
    """(tier, n, sample_id) -> considered done, latest state wins.
    raw_len 0 with no call_error is NOT done (needs a retry pass)."""
    state = {}
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            key = (r.get("tier"), r.get("n"), r.get("sample_id"))
            done = bool(r.get("raw_len", 0) > 0 or r.get("call_error"))
            state[key] = done
    return {k for k, v in state.items() if v}


def append_row(row):
    line = json.dumps(row) + "\n"
    with _write_lock:
        with OUT.open("a", encoding="utf-8") as fh:
            fh.write(line)
            fh.flush()
            os.fsync(fh.fileno())
        print("JSONL|" + line, end="", flush=True)


def group_worker(tier, model, n, prompt, sha, key, done):
    for sid in range(1, N_SAMPLES + 1):
        if (tier, n, sid) in done:
            continue
        raw, err, meta, dur = call(model, prompt, key)
        recomputed = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
        assert recomputed == sha, ("prompt hash drifted mid-run", tier, n, sid)
        row = {
            "tier": tier,
            "n": n,
            "sample_id": sid,
            "prompt_sha256": recomputed,
            "raw": raw,
            "raw_len": len(raw),
            "served_model": meta.get("served_model"),
            "request_params": {"model": model, "temperature": TEMPERATURE,
                               "max_tokens": MAX_TOKENS, "system_prompt": None,
                               "path": "openrouter chat-completions"},
            "finish_reason": meta.get("finish_reason"),
            "usage": meta.get("usage"),
            "latency_s": round(dur, 2),
            "call_error": err,
            "timestamp_utc": now_utc(),
        }
        append_row(row)
        time.sleep(INTRA_GROUP_SPACING_S)


def dry_run(prompts):
    print("dry-run: prompt hashes")
    for n in CELLS:
        p, h = prompts[n]
        print(f"  N={n}: {h}")
    tier = "weak"
    model = TIERS[tier]
    p, h = prompts[CELLS[0]]
    body = build_body(model, p)
    print(f"\nexample request body (tier={tier}, model={model}, N={CELLS[0]}):")
    print(json.dumps(body, indent=1))
    print("\n(no Authorization header printed; no HTTP call made)")


def main():
    prompts = load_prompts()
    if "--dry-run" in sys.argv:
        dry_run(prompts)
        return
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY not set")
    done = existing_done()
    if done:
        print(f"resume: {len(done)} completed invocations skipped")
    groups = [(tier, model, n) for tier, model in TIERS.items() for n in CELLS]
    with ThreadPoolExecutor(max_workers=MAX_GROUP_WORKERS) as ex:
        futs = []
        for tier, model, n in groups:
            prompt, sha = prompts[n]
            futs.append(ex.submit(group_worker, tier, model, n, prompt, sha, key, done))
        for f in futs:
            f.result()
    print("done")


if __name__ == "__main__":
    main()
