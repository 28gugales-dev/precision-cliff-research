# ============================================================================
# Arm P collection runner — pinned-temperature rerun on OpenRouter chat-
# completions. Prereg: arm_p_preregistration.txt. Mirrors the call shape of
# arm_v_openrouter_run.py (direct HTTP, no SDK).
#
# The API key comes ONLY from the OPENROUTER_API_KEY environment variable.
# It is never written to disk, never logged, never printed.
#
# Cells: 15 total (7 square, 5 held-out, 3 code), read from arm_p_prompts.json
# (written by arm_p_build.py, which asserts byte-identity against the
# registered source prompts). n = 15 invocations per cell, 225 rows total.
# Serial per cell with 3s spacing; up to 4 cells run concurrently.
#
# Rows are appended live to arm_p_collect.jsonl with fsync after every write,
# and echoed to stdout as "JSONL|<row>" so a console log alone reconstructs
# the dataset. Resume: a row counts as done only if call_error is null AND
# raw_len > 0 — a row with raw_len 0 and no error is a bug state and is
# re-attempted, never counted as done.
# ============================================================================
import hashlib
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROMPTS_PATH = ROOT / "arm_p_prompts.json"
OUT = ROOT / "arm_p_collect.jsonl"

ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "anthropic/claude-haiku-4.5"
TEMPERATURE = 1.0
MAX_TOKENS = 8192
SAMPLES = 15
CELL_SPACING_S = 3.0
MAX_WORKERS = 4
CALL_TIMEOUT = 240
MAX_RETRIES = 3  # additional attempts after the first, on 429/5xx only

_write_lock = threading.Lock()


def sha256_of(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_cells():
    """Returns an ordered list of dicts: cell_group, n, prompt, sha256."""
    spec = json.loads(PROMPTS_PATH.read_text(encoding="utf-8"))
    cells = []
    for group, key_order in (("square", ["13", "17", "21", "31", "35", "37", "43"]),
                              ("heldout", ["50", "58", "62", "65", "75"]),
                              ("code", ["13", "21", "31"])):
        for k in key_order:
            rec = spec[group][k]
            cells.append({"cell_group": group, "n": int(k),
                          "prompt": rec["prompt"], "sha256": rec["sha256"]})
    return cells


def request_body(prompt):
    return {"model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": TEMPERATURE,
            "max_tokens": MAX_TOKENS}


def request_params_record():
    return {"model": MODEL, "temperature": TEMPERATURE, "max_tokens": MAX_TOKENS,
            "top_p": "not set", "top_k": "not set"}


def call(prompt, key):
    """One full call including retries. Returns (raw, served_model,
    finish_reason, usage, call_error, latency_s)."""
    body = request_body(prompt)
    payload = json.dumps(body).encode("utf-8")
    t0 = time.time()
    last_err = None
    attempt = 0
    while True:
        attempt += 1
        req = urllib.request.Request(
            ENDPOINT, data=payload,
            headers={"Authorization": f"Bearer {key}",
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=CALL_TIMEOUT) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            choice = (data.get("choices") or [{}])[0]
            text = (choice.get("message") or {}).get("content") or ""
            return (text, data.get("model"), choice.get("finish_reason"),
                    data.get("usage"), None, time.time() - t0)
        except urllib.error.HTTPError as e:
            detail = ""
            try:
                detail = e.read().decode("utf-8", "replace")[:500]
            except Exception:
                pass
            last_err = f"HTTPError {e.code}: {e.reason} {detail}"[:800]
            retryable = e.code == 429 or 500 <= e.code < 600
            if retryable and attempt <= MAX_RETRIES:
                time.sleep(min(60, 5 * (2 ** (attempt - 1))))
                continue
            return "", None, None, None, last_err, time.time() - t0
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"[:800]
            return "", None, None, None, last_err, time.time() - t0


def existing_rows():
    rows = []
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


def done_keys(rows):
    done = set()
    for r in rows:
        if r.get("call_error") is None and r.get("raw_len", 0) > 0:
            done.add((r["cell_group"], r["n"], r["sample_id"]))
    return done


def write_row(row):
    line = json.dumps(row)
    with _write_lock:
        with OUT.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        print(f"JSONL|{line}", flush=True)


def worker(cell, key, done):
    group, n, prompt, reg_hash = cell["cell_group"], cell["n"], cell["prompt"], cell["sha256"]
    sent_hash = sha256_of(prompt)
    assert sent_hash == reg_hash, (
        f"prompt hash mismatch for {group} N={n}: sent {sent_hash} != registered {reg_hash}")
    for sample_id in range(1, SAMPLES + 1):
        if (group, n, sample_id) in done:
            continue
        raw, served_model, finish_reason, usage, call_error, latency_s = call(prompt, key)
        row = {
            "cell_group": group,
            "n": n,
            "sample_id": sample_id,
            "prompt_sha256": sent_hash,
            "raw": raw,
            "raw_len": len(raw),
            "served_model": served_model,
            "request_params": request_params_record(),
            "finish_reason": finish_reason,
            "usage": usage,
            "latency_s": round(latency_s, 3),
            "call_error": call_error,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        }
        write_row(row)
        time.sleep(CELL_SPACING_S)


def dry_run():
    cells = load_cells()
    print(f"{len(cells)} cells loaded from {PROMPTS_PATH.name}")
    for c in cells:
        h = sha256_of(c["prompt"])
        assert h == c["sha256"], (c["cell_group"], c["n"], "hash mismatch")
        print(f"{c['cell_group']:>7} N={c['n']:>2}  sha256={h}")
    print()
    example = cells[0]
    print(f"example request body for cell {example['cell_group']} N={example['n']}:")
    print(json.dumps(request_body(example["prompt"]), indent=2))


def main():
    if "--dry-run" in sys.argv:
        dry_run()
        return

    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY not set")

    cells = load_cells()
    rows = existing_rows()
    done = done_keys(rows)
    if done:
        print(f"resume: {len(done)}/{len(cells) * SAMPLES} completed invocations skipped")

    with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(cells))) as ex:
        futures = [ex.submit(worker, c, key, done) for c in cells]
        for f in futures:
            f.result()
    print("done")


if __name__ == "__main__":
    main()
