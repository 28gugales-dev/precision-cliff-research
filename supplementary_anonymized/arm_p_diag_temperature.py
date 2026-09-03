# ============================================================================
# POST HOC, NOT PREREGISTERED. Diagnostic for arm P's validity collapse.
# Same registered prompt (byte-identical, hash asserted), same serving path
# and model, temperature varied. Not scored against any registered
# prediction.
#
# Samples ONLY the registered N=13 square prompt, through the same
# OpenRouter chat-completions path and anthropic/claude-haiku-4.5, at
# temperature in {0.0, 0.5, 1.0} (1.0 = same-day replication of arm P's
# registered setting). n=6 per temperature = 18 calls. max_tokens 8192, no
# system prompt, 3s spacing between calls. Rows appended live (fsync) to
# arm_p_diag_temperature.jsonl with the arm_p_run.py row fields plus
# "temperature".
#
# Scoring reuses arm_f_repro.py conventions unchanged: parse_packing,
# validate (1e-6 primary, 1e-9 logged), score, classify.
#
# Also summarizes (no re-sampling) the existing arm_p_collect.jsonl N=13
# square rows: circle-count and max-pairwise-overlap distribution, and a
# prose/code-fence check.
#
# Does NOT modify arm_p_run.py, arm_p_analysis.py, arm_p_collect.jsonl, or
# arm_p_report.json.
# ============================================================================
import hashlib
import json
import math
import os
import statistics
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from arm_f_repro import parse_packing, validate, score, classify

ROOT = Path(__file__).resolve().parent
PROMPTS_PATH = ROOT / "arm_p_prompts.json"
COLLECT_PATH = ROOT / "arm_p_collect.jsonl"
OUT = ROOT / "arm_p_diag_temperature.jsonl"

ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "anthropic/claude-haiku-4.5"
MAX_TOKENS = 8192
TEMPERATURES = [0.0, 0.5, 1.0]
SAMPLES_PER_TEMP = 6
SPACING_S = 3.0
CALL_TIMEOUT = 240
MAX_RETRIES = 3
PREDICTION_N13 = 1.625  # T(4,13), registered
WINDOW = 2e-3


def sha256_of(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_prompt():
    spec = json.loads(PROMPTS_PATH.read_text(encoding="utf-8"))
    rec = spec["square"]["13"]
    h = sha256_of(rec["prompt"])
    assert h == rec["sha256"], ("N=13 square prompt hash mismatch", h, rec["sha256"])
    return rec["prompt"], h


def request_body(prompt, temperature):
    return {"model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": MAX_TOKENS}


def call(prompt, key, temperature):
    body = request_body(prompt, temperature)
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


def existing_diag_keys():
    done = set()
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                if r.get("call_error") is None and r.get("raw_len", 0) > 0:
                    done.add((r["temperature"], r["sample_id"]))
    return done


def sample():
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY not set")
    prompt, prompt_hash = load_prompt()
    done = existing_diag_keys()
    if done:
        print(f"resume: {len(done)}/{len(TEMPERATURES) * SAMPLES_PER_TEMP} completed rows skipped")
    for temperature in TEMPERATURES:
        for sample_id in range(1, SAMPLES_PER_TEMP + 1):
            if (temperature, sample_id) in done:
                continue
            raw, served_model, finish_reason, usage, call_error, latency_s = call(
                prompt, key, temperature)
            row = {
                "cell_group": "square",
                "n": 13,
                "sample_id": sample_id,
                "temperature": temperature,
                "prompt_sha256": prompt_hash,
                "raw": raw,
                "raw_len": len(raw),
                "served_model": served_model,
                "request_params": {"model": MODEL, "temperature": temperature,
                                   "max_tokens": MAX_TOKENS, "top_p": "not set",
                                   "top_k": "not set"},
                "finish_reason": finish_reason,
                "usage": usage,
                "latency_s": round(latency_s, 3),
                "call_error": call_error,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            }
            with OUT.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(row) + "\n")
                fh.flush()
                os.fsync(fh.fileno())
            print(f"T={temperature:.1f} sample {sample_id}/6  len={len(row['raw']):4d}  "
                  f"{row['latency_s']:5.1f}s  {call_error or ''}", flush=True)
            time.sleep(SPACING_S)


# ------------------------------------------------------------ scoring stage

def score_diag():
    rows = []
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    print("\n--- diagnostic: temperature sweep, N=13 square, registered prompt ---")
    for temperature in TEMPERATURES:
        sub = [r for r in rows if r["temperature"] == temperature]
        bins = Counter()
        valid_reports = []
        for r in sub:
            if r.get("call_error") is not None or not r.get("raw"):
                bins["call_error"] += 1
                continue
            circles, perr = parse_packing(r["raw"])
            if circles is None:
                bins[perr or "parse_error"] += 1
                continue
            ok6, why6 = validate(circles, 13, tol=1e-6)
            ok9, _ = validate(circles, 13, tol=1e-9)
            if not ok6:
                bins[why6] += 1
                continue
            s = score(circles)
            classify(circles, 13)  # reused per spec; structure not printed here
            on_pred = abs(s - PREDICTION_N13) < WINDOW
            valid_reports.append((r["sample_id"], round(s, 7), ok9, on_pred))
        print(f"\nT={temperature:.1f}: valid {len(valid_reports)}/{len(sub)}  "
              f"failure_bins={dict(bins)}")
        for sid, s, ok9, on_pred in valid_reports:
            print(f"  sample {sid}: sum={s:.7f}  valid_1e9={ok9}  "
                  f"on-prediction(T(4,13)=1.625)={on_pred}")


# --------------------------------------------------- existing-data summary

def summarize_existing_collect():
    if not COLLECT_PATH.exists():
        print(f"\n{COLLECT_PATH.name} not found; skipping existing-data summary")
        return
    rows = [json.loads(l) for l in COLLECT_PATH.read_text(encoding="utf-8").splitlines()
            if l.strip()]
    sub = [r for r in rows if r["cell_group"] == "square" and r["n"] == 13]
    counts = []
    max_overlaps = []
    non_bracket = 0
    for r in sub:
        raw = r.get("raw") or ""
        if not raw.strip().startswith("["):
            non_bracket += 1
        circles, perr = parse_packing(raw)
        if circles is None:
            continue
        counts.append(len(circles))
        worst = None
        for i in range(len(circles)):
            xi, yi, ri = circles[i]
            for j in range(i + 1, len(circles)):
                xj, yj, rj = circles[j]
                d = math.hypot(xi - xj, yi - yj)
                overlap = (ri + rj) - d  # positive = overlapping
                if worst is None or overlap > worst:
                    worst = overlap
        if worst is not None:
            max_overlaps.append(worst)
    print(f"\n--- existing arm_p_collect.jsonl, N=13 square, {len(sub)} rows "
          f"(no re-sampling) ---")
    if counts:
        print(f"circle count emitted: median={statistics.median(counts)}  "
              f"max={max(counts)}")
    else:
        print("circle count emitted: no parseable rows")
    if max_overlaps:
        print(f"max pairwise overlap per row (positive=overlapping): "
              f"median={statistics.median(max_overlaps):.6f}  "
              f"max={max(max_overlaps):.6f}")
    else:
        print("max pairwise overlap per row: no parseable rows")
    print(f"rows whose raw text does not start with '[' "
          f"(prose/code-fence/other): {non_bracket}/{len(sub)}")


def main():
    if os.environ.get("OPENROUTER_API_KEY"):
        sample()
    else:
        print("OPENROUTER_API_KEY not set; skipping sampling, scoring existing "
              f"{OUT.name} if present")
    score_diag()
    summarize_existing_collect()


if __name__ == "__main__":
    main()
