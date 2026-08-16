# Screen S runner — family competence screen over OpenRouter :free.
# Doc: screen_s_doc.md (must be committed before this executes; checked).
# Selection instrument only — see the doc's "what this can and cannot say".
#
# Prompt constructor, parser, evaluator byte-copied from
# supplementary_anonymized/sec3_artifacts/runners/kaggle_wave7b_phi4_14b.py
# and self-tested at startup. 50 one-shot gen-0 calls per model, baseline
# grid as parent. Key from OPENROUTER_API_KEY only; never written.
import ast
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "screen_s_raw.jsonl"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
RUN_DATE = "2026-08-16"

MODELS = [
    "google/gemma-4-31b-it:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
    "openai/gpt-oss-20b:free",
    "cohere/north-mini-code:free",
]
SAMPLES = 50
N = 26
EPS = 1e-6
TEMPERATURE = 0.8
TOP_P = 0.95
MAX_TOKENS = 4096
SPACING_S = 20      # per worker; 5 workers ~ 15 req/min < shared 20/min cap
TIMEOUT = 300

KEY = os.environ.get("OPENROUTER_API_KEY", "")
if not KEY:
    sys.exit("OPENROUTER_API_KEY not set; refusing to run")
log = subprocess.run(["git", "log", "--oneline", "--", "screen_s_doc.md"],
                     cwd=str(HERE), capture_output=True, text=True)
if not log.stdout.strip():
    sys.exit("screen_s_doc.md not committed; refusing to sample off-register")


# --- byte-copied evaluator/prompt block (kaggle_wave7b_phi4_14b.py) ---------

def parse_proposal(raw):
    if raw is None:
        return None, "no_output"
    text = raw.strip()
    text = re.sub(r"```(?:python|json)?", "", text).replace("```", "").strip()
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1 or end <= start:
        return None, "no_list_found"
    text = text[start:end + 1]
    try:
        obj = ast.literal_eval(text)
    except (ValueError, SyntaxError) as e:
        return None, f"literal_eval: {type(e).__name__}"
    if not isinstance(obj, (list, tuple)):
        return None, "not_a_list"
    circles = []
    for item in obj:
        if not isinstance(item, (list, tuple)) or len(item) != 3:
            return None, "bad_triple"
        try:
            circles.append(tuple(float(v) for v in item))
        except (TypeError, ValueError):
            return None, "non_numeric"
    return circles, None


def evaluate(circles):
    res = {"viable": False, "valid": False, "score": 0.0,
           "mean_radius": 0.0, "density": 0.0,
           "n": 0 if circles is None else len(circles)}
    if circles is None:
        return res
    if len(circles) != N or any(r <= 0 for (_, _, r) in circles):
        return res
    res["viable"] = True
    radii = [r for (_, _, r) in circles]
    res["mean_radius"] = sum(radii) / N
    res["density"] = sum(math.pi * r * r for r in radii)
    inside = all(x - r >= -EPS and x + r <= 1 + EPS and
                 y - r >= -EPS and y + r <= 1 + EPS for (x, y, r) in circles)
    overlap = False
    for i in range(N):
        xi, yi, ri = circles[i]
        for j in range(i + 1, N):
            xj, yj, rj = circles[j]
            if math.hypot(xi - xj, yi - yj) + EPS < ri + rj:
                overlap = True
                break
        if overlap:
            break
    if inside and not overlap:
        res["valid"] = True
        res["score"] = sum(radii)
    return res


def baseline_packing():
    r = round(0.9 / N, 6)
    pts = []
    for row in range(5):
        for col in range(6):
            if len(pts) >= N:
                break
            pts.append([round((col + 0.5) / 6.0, 6), round((row + 0.5) / 5.0, 6), r])
    return pts


def loop_prompt(best_circles, best_score):
    packing = json.dumps([[round(x, 6), round(y, 6), round(r, 6)]
                          for (x, y, r) in best_circles])
    return (
        "You are the proposal step of an evolutionary search for circle packings.\n"
        f"Current best packing (sum of radii = {best_score:.6f}):\n{packing}\n\n"
        f"Produce a packing of exactly {N} circles with a HIGHER sum of radii.\n"
        "MUST hold: exactly 26 circles; every circle fully inside the unit square "
        "[0,1]x[0,1] (x-r >= 0, x+r <= 1, same for y); no two circles overlap "
        "(distance between centers >= sum of the two radii; touching is allowed).\n"
        "Output ONLY the raw Python list of 26 [x, y, r] lists. No explanation, "
        "no code fences, no other text."
    )


def self_test():
    base = baseline_packing()
    ev = evaluate([tuple(c) for c in base])
    assert ev["valid"], "baseline must be valid"
    assert abs(ev["score"] - 0.89999) < 1e-4, f"baseline score {ev['score']}"
    bad = [tuple(c) for c in base]
    bad[0] = (bad[0][0], bad[0][1], 0.5)
    assert not evaluate(bad)["valid"], "overlap must invalidate"
    c, err = parse_proposal("junk before [[0.1, 0.1, 0.05]] junk after")
    assert err is None and len(c) == 1, "parser must extract bracketed list"
    print("[selftest] evaluator + parser OK", flush=True)

# --- end byte-copied block --------------------------------------------------


BASE = baseline_packing()
BASE_SCORE = evaluate([tuple(c) for c in BASE])["score"]
PROMPT = loop_prompt([tuple(c) for c in BASE], BASE_SCORE)
PROMPT_SHA = hashlib.sha256(PROMPT.encode("utf-8")).hexdigest()


def call(model):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "max_tokens": MAX_TOKENS,
    }).encode()
    last_err = ""
    for attempt in range(5):
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
    return {"transport_error": last_err or "retries exhausted"}, 5


def existing():
    done = set()
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                if not r.get("transport_error"):
                    done.add((r["model"], r["sample_idx"]))
    return done


lock = threading.Lock()


def worker(model, done):
    short = model.split("/")[-1]
    for i in range(SAMPLES):
        if (model, i) in done:
            continue
        time.sleep(SPACING_S)
        t0 = time.time()
        resp, retries = call(model)
        err = resp.get("transport_error")
        text, finish = "", None
        if not err:
            try:
                text = resp["choices"][0]["message"]["content"] or ""
                finish = resp["choices"][0].get("finish_reason")
            except (KeyError, IndexError, TypeError):
                text = ""
        circles, perr = parse_proposal(text if text else None)
        ev = evaluate(circles)
        row = {
            "screen": "S", "run_date": RUN_DATE, "model": model,
            "provider": resp.get("provider"), "sample_idx": i,
            "prompt_sha256": PROMPT_SHA,
            "request_params": {"temperature": TEMPERATURE, "top_p": TOP_P,
                               "max_tokens": MAX_TOKENS},
            "finish_reason": finish, "transport_error": err,
            "transport_retries": retries,
            "raw_text": text, "raw_len": len(text),
            "parse_error": perr, "viable": ev["viable"], "valid": ev["valid"],
            "n_circles": ev["n"], "score": round(ev["score"], 6),
            "duration_s": round(time.time() - t0, 1),
        }
        with lock:
            with OUT.open("a", encoding="utf-8") as f:
                f.write(json.dumps(row) + "\n")
            print(f"{short:34s} s{i:>2} valid={ev['valid']} viable={ev['viable']} "
                  f"finish={finish} provider={resp.get('provider')} "
                  f"len={len(text)}", flush=True)


def main():
    self_test()
    done = existing()
    if done:
        print(f"resume: {len(done)} completed calls skipped")
    threads = [threading.Thread(target=worker, args=(m, done)) for m in MODELS]
    [t.start() for t in threads]
    [t.join() for t in threads]
    # per-model tally
    rows = [json.loads(l) for l in OUT.read_text(encoding="utf-8").splitlines()
            if l.strip()]
    print("\n--- screen S tally (selection rule: >=20/50 valid) ---")
    for m in MODELS:
        mr = [r for r in rows if r["model"] == m and not r.get("transport_error")]
        seen = {}
        for r in mr:                       # last attempt per sample wins
            seen[r["sample_idx"]] = r
        v = sum(1 for r in seen.values() if r["valid"])
        vi = sum(1 for r in seen.values() if r["viable"])
        tr = sum(1 for r in seen.values() if r["finish_reason"] == "length")
        provs = sorted({r["provider"] for r in seen.values() if r["provider"]})
        print(f"{m:44s} valid {v}/{len(seen)}  viable {vi}  truncated {tr}  "
              f"{'ADVANCE' if v >= 20 else 'not selected'}  providers={provs}")


if __name__ == "__main__":
    main()
