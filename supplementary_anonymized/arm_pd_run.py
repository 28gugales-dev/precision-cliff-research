# ============================================================================
# Arm P-D collection runner. Prereg: arm_pd_preregistration.txt (2026-09-02).
# arm_p_run.py's call shape (direct OpenRouter chat-completions, urllib,
# live-appended fsync'd JSONL, resume-by-skip) with two conditions:
#   D1  extended thinking on ("reasoning": {"enabled": true}), no system prompt
#   D2  thinking off, one-line system prompt
# One worker; rows alternate D1, D2 by sample id so an interrupted run leaves
# both conditions with matched counts. A row whose call failed with HTTP 402
# is not done on resume, and the run stops launching after the first 402.
# The API key comes ONLY from OPENROUTER_API_KEY; never written or printed.
# ============================================================================
import hashlib
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = json.loads((ROOT / "arm_pd_prompts.json").read_text(encoding="utf-8"))
OUT = ROOT / "arm_pd_collect.jsonl"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
MODEL = SPEC["model"]
TEMPERATURE = SPEC["decoding"]["temperature"]
MAX_TOKENS = SPEC["decoding"]["max_tokens"]
N = SPEC["n"]
SAMPLES = SPEC["n_per_condition"]
SPACING_S = 3.0
CALL_TIMEOUT = 300
MAX_RETRIES = 3


def now_utc():
    return datetime.now(timezone.utc).isoformat()


def prompt_and_hash():
    p = SPEC["prompt"]
    h = hashlib.sha256(p.encode("utf-8")).hexdigest()
    if h != SPEC["sha256"]:
        sys.exit("prompt hash mismatch; refusing to sample")
    return p, h


def request_body(cond, prompt):
    c = SPEC["conditions"][cond]
    msgs = []
    if c["system_prompt"]:
        msgs.append({"role": "system", "content": c["system_prompt"]})
    msgs.append({"role": "user", "content": prompt})
    body = {"model": MODEL, "messages": msgs, "temperature": TEMPERATURE, "max_tokens": MAX_TOKENS}
    if c["reasoning"]:
        body["reasoning"] = c["reasoning"]
    return body


def call(cond, prompt, key):
    data = json.dumps(request_body(cond, prompt)).encode("utf-8")
    attempt, last_err = 0, None
    while True:
        attempt += 1
        t0 = time.time()
        req = urllib.request.Request(ENDPOINT, data=data,
                                     headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=CALL_TIMEOUT) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            choice = (payload.get("choices") or [{}])[0]
            msg = choice.get("message") or {}
            text = msg.get("content") or ""
            reasoning = msg.get("reasoning") or ""
            meta = {"served_model": payload.get("model"), "generation_id": payload.get("id"),
                    "finish_reason": choice.get("finish_reason"), "usage": payload.get("usage"),
                    "reasoning_len": len(reasoning), "attempts": attempt}
            return text, None, meta, time.time() - t0
        except urllib.error.HTTPError as e:
            detail = ""
            try:
                detail = e.read().decode("utf-8", "replace")[:800]
            except Exception:
                pass
            last_err = f"HTTPError {e.code}: {e.reason} {detail}"[:1000]
            if e.code == 402:
                return "", last_err, {"attempts": attempt, "http_status": 402}, time.time() - t0
            if (e.code == 429 or 500 <= e.code < 600) and attempt <= MAX_RETRIES:
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
    state = {}
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            err = r.get("call_error") or ""
            state[(r["condition"], r["sample_id"])] = bool(r.get("raw_len", 0) > 0 or (err and "HTTPError 402" not in err))
    return {k for k, v in state.items() if v}


def append_row(row):
    with OUT.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row) + "\n")
        fh.flush()
        os.fsync(fh.fileno())
    print("JSONL|" + json.dumps(row)[:150], flush=True)


def main():
    prompt, sha = prompt_and_hash()
    if "--dry-run" in sys.argv:
        for cond in ("D1", "D2"):
            print(f"\n{cond} request body:")
            print(json.dumps(request_body(cond, prompt), indent=1)[:900])
        print("\n(no Authorization header printed; no HTTP call made)")
        return
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY not set")
    done = existing_done()
    if done:
        print(f"resume: {len(done)} completed invocations skipped")
    for sid in range(1, SAMPLES + 1):
        for cond in ("D1", "D2"):
            if (cond, sid) in done:
                continue
            raw, err, meta, dur = call(cond, prompt, key)
            assert hashlib.sha256(prompt.encode("utf-8")).hexdigest() == sha
            append_row({"condition": cond, "n": N, "sample_id": sid, "prompt_sha256": sha, "raw": raw,
                        "raw_len": len(raw), "reasoning_len": meta.get("reasoning_len"),
                        "served_model": meta.get("served_model"), "finish_reason": meta.get("finish_reason"),
                        "usage": meta.get("usage"),
                        "request_params": {"model": MODEL, "temperature": TEMPERATURE, "max_tokens": MAX_TOKENS,
                                           "condition": SPEC["conditions"][cond], "path": "openrouter chat-completions"},
                        "latency_s": round(dur, 2), "call_error": err, "timestamp_utc": now_utc()})
            if meta.get("http_status") == 402:
                print("stopped on 402; rerun after top-up", flush=True)
                return
            time.sleep(SPACING_S)
    print("done")


if __name__ == "__main__":
    main()
