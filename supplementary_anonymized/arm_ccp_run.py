# ============================================================================
# Arm CCP collection runner. Prereg: arm_ccp_preregistration.txt (2026-09-02).
# Prompts/hashes frozen in arm_ccp_prompts.json (arm_ccp_build.py output),
# committed before this executes.
#
# arm_cl_run.py's call shape, unchanged except: one tier (Sonnet), and a
# row whose call failed with HTTP 402 (credit exhausted) is NOT treated as
# done on resume, and the run stops launching new calls once a 402 is seen,
# so an interrupted arm resumes to its registered n instead of ending short.
#
# The API key comes ONLY from the OPENROUTER_API_KEY environment variable.
# It is never written to disk, logged, or printed -- not even in --dry-run,
# which prints the request body (no Authorization header) and exits.
#
# One tier x three cells (N=13,21,31) x n=15 = 45 rows. Serial per cell
# with 3s spacing between calls in that group; up to 3 groups concurrently.
# Registered decoding: temperature 1.0, max_tokens 16384, no system prompt,
# one user turn = the registered prompt verbatim.
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
PROMPTS_PATH = ROOT / "arm_ccp_prompts.json"
OUT = ROOT / "arm_ccp_collect.jsonl"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

CELLS = [13, 21, 31]
N_SAMPLES = 15
TEMPERATURE = 1.0
MAX_TOKENS = 16384
CALL_TIMEOUT = 300
INTRA_GROUP_SPACING_S = 3
# Was 3 for rows 1-23 (2026-09-02 19:22-19:23 UTC). OpenRouter then refused new calls with 402
# "in_flight_budget_exhausted": three concurrent 16384-token reservations exceeded the
# account's remaining credit, which was not itself exhausted. Set to 1 for the resumed run
# so one reservation at a time fits; the request body, prompt and decoding are unchanged.
MAX_GROUP_WORKERS = 1
MAX_RETRIES = 3  # on 429/5xx

_data = json.loads(PROMPTS_PATH.read_text(encoding="utf-8"))
TIERS = _data["tiers"]  # {"sonnet": "anthropic/claude-sonnet-4.5"}
CCP = _data["ccp"]

_write_lock = threading.Lock()
_stop = threading.Event()  # set on HTTP 402; no new calls after that


def now_utc():
    return datetime.now(timezone.utc).isoformat()


def load_prompts():
    prompts = {}
    for n in CELLS:
        rec = CCP[str(n)]
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
            if e.code == 402:
                _stop.set()
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
    """(tier, n, sample_id) -> done, latest state wins. A row with raw_len 0
    and no call_error is not done; neither is a row whose call_error is a
    402 (credit), which is retried on the next run."""
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
            err = r.get("call_error") or ""
            done = bool(r.get("raw_len", 0) > 0 or (err and "HTTPError 402" not in err))
            state[key] = done
    return {k for k, v in state.items() if v}


def append_row(row):
    line = json.dumps(row) + "\n"
    with _write_lock:
        with OUT.open("a", encoding="utf-8") as fh:
            fh.write(line)
            fh.flush()
            os.fsync(fh.fileno())
        print("JSONL|" + line[:160].rstrip(), flush=True)


def group_worker(tier, model, n, prompt, sha, key, done):
    for sid in range(1, N_SAMPLES + 1):
        if (tier, n, sid) in done:
            continue
        if _stop.is_set():
            print(f"stop: credit exhausted before {tier} N={n} sample {sid}", flush=True)
            return
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
    tier = "sonnet"
    model = TIERS[tier]
    p, h = prompts[CELLS[0]]
    print(f"\nexample request body (tier={tier}, model={model}, N={CELLS[0]}):")
    print(json.dumps(build_body(model, p), indent=1))
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
    print("stopped on 402; rerun after top-up" if _stop.is_set() else "done")


if __name__ == "__main__":
    main()
