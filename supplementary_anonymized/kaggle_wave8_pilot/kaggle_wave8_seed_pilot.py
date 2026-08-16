#!/usr/bin/env python
# ============================================================================
# WAVE 8 SEED-CALIBRATION PILOT — DISCLOSED, NOT A REGISTERED WAVE.
#
# Purpose: three registered waves (3, 5, and every 7/7b arm) died on control
# floors because their seed parents sat above what the reference rung reaches.
# This pilot calibrates the TASK, not the hypothesis: Q4_K_M ONLY (the control
# rung), four graded Heilbronn n=13 seed parents (best-of-K seeded random,
# K = 1/10/100/1000, scores 0.000308 / 0.000857 / 0.001855 / 0.003544 against
# wave 3's unreachable 0.009087), ten single-shot proposals each. The wave-8
# registration will pick the hardest candidate the control rung improves on
# at >= 30% of attempts, cite this pilot by kernel slug, and only then lock
# the Q2_K contrast. No Q2_K row is sampled here, so no echo-contrast data
# exists before the lock. Prompt text is byte-identical to the wave-3 runner.
# ============================================================================

import subprocess as _sp
import sys as _sys

def _pip(*a):
    return _sp.run([_sys.executable, "-m", "pip", "install", "-q", *a]).returncode

_pip("huggingface_hub")
_pip("llama-cpp-python",
     "--extra-index-url", "https://abetlen.github.io/llama-cpp-python/whl/cu122")
try:
    import llama_cpp  # noqa: F401
except Exception:
    print("[bootstrap] prebuilt wheel failed; building from source (slow)...")
    import os as _os
    _env = dict(_os.environ, CMAKE_ARGS="-DGGML_CUDA=on")
    _sp.run([_sys.executable, "-m", "pip", "install", "-q",
             "--force-reinstall", "--no-cache-dir", "llama-cpp-python"],
            env=_env, check=True)
    import llama_cpp  # noqa: F401
print("[bootstrap] llama_cpp ready:", llama_cpp.__version__)

import ast
import hashlib
import json
import os
import re
import time
from itertools import combinations

REPO = "Qwen/Qwen2.5-Coder-14B-Instruct-GGUF"
FNAME = "qwen2.5-coder-14b-instruct-q4_k_m.gguf"
N = 13
COORD_DP = 6
_TRIPLES = list(combinations(range(N), 3))
N_TRIPLES = len(_TRIPLES)
N_CTX = 4096
MAX_TOKENS = 1200
TEMPERATURE = 0.8
TOP_P = 0.95
PROBES_PER_CANDIDATE = 10

# Graded candidates: best-of-K seeded random draws (rng seed 880808, generator
# script gen_pilot_seeds.py in the repo). Literals are the registered objects.
CANDIDATES = {
    "k1": [[0.276777, 0.181308], [0.028426, 0.428431], [0.421556, 0.99674], [0.934531, 0.978081], [0.944796, 0.046278], [0.569292, 0.189953], [0.354614, 0.298812], [0.462318, 0.895681], [0.675116, 0.416617], [0.168178, 0.339043], [0.778825, 0.596823], [0.973814, 0.85417], [0.261979, 0.590312]],
    "k10": [[0.698801, 0.278591], [0.309192, 0.684238], [0.22528, 0.42852], [0.019812, 0.796958], [0.816078, 0.212183], [0.385926, 0.074933], [0.018424, 0.144938], [0.258504, 0.093093], [0.078444, 0.661617], [0.482097, 0.386543], [0.951377, 0.269625], [0.591136, 0.76788], [0.415216, 0.609383]],
    "k100": [[0.146131, 0.709704], [0.648809, 0.994407], [0.855882, 0.048908], [0.348861, 0.863168], [0.995976, 0.007908], [0.847294, 0.566787], [0.463581, 0.253226], [0.097897, 0.155968], [0.124653, 0.083407], [0.001195, 0.16079], [0.458881, 0.727877], [0.006621, 0.686082], [0.475218, 0.795478]],
    "k1000": [[0.736841, 0.960496], [0.818815, 0.39718], [0.079488, 0.604837], [0.800515, 0.143815], [0.522646, 0.708316], [0.981987, 0.422443], [0.242216, 0.830866], [0.81805, 0.889348], [0.209786, 0.074546], [0.614931, 0.173958], [0.076106, 0.735437], [0.704171, 0.671296], [0.292799, 0.973712]],
}
EXPECTED = {"k1": 0.0003081623880000217, "k10": 0.0008565663840000015,
            "k100": 0.0018554421234999903, "k1000": 0.00354419586599998}

WORK = "/kaggle/working/wave8_pilot" if os.path.isdir("/kaggle") else os.path.abspath("./wave8_pilot")
MODELS_DIR = "/kaggle/tmp/models" if os.path.isdir("/kaggle") else os.path.abspath("./models")
LOG = os.path.join(WORK, "pilot_rows.jsonl")
SUMMARY = os.path.join(WORK, "pilot_summary.json")


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
    points = []
    for item in obj:
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            return None, "bad_pair"
        try:
            points.append(tuple(round(float(v), COORD_DP) for v in item))
        except (TypeError, ValueError):
            return None, "non_numeric"
    return points, None


def min_triangle_area(points):
    m = float("inf")
    for i, j, k in _TRIPLES:
        ax, ay = points[i]
        bx, by = points[j]
        cx, cy = points[k]
        a = abs((bx - ax) * (cy - ay) - (cx - ax) * (by - ay)) / 2.0
        if a < m:
            m = a
    return m


def evaluate(points):
    res = {"viable": False, "valid": False, "score": 0.0,
           "collinear": False, "n": 0 if points is None else len(points)}
    if points is None:
        return res
    res["viable"] = True
    if len(points) != N:
        return res
    if any(not (0.0 <= c <= 1.0) for p in points for c in p):
        return res
    if len({(round(x, COORD_DP), round(y, COORD_DP)) for (x, y) in points}) != N:
        return res
    res["valid"] = True
    res["score"] = min_triangle_area(points)
    res["collinear"] = (res["score"] == 0.0)
    return res


def point_key(points):
    return frozenset((round(x, COORD_DP), round(y, COORD_DP)) for (x, y) in points)


# Byte-identical to the wave-3 runner's loop_prompt.
def loop_prompt(best_points, best_score):
    config = json.dumps([[round(x, COORD_DP), round(y, COORD_DP)]
                         for (x, y) in best_points])
    return (
        "You are the proposal step of an evolutionary search for Heilbronn "
        "triangle configurations.\n"
        f"Current best configuration (minimum triangle area = {best_score:.9f}):\n"
        f"{config}\n\n"
        f"Produce a configuration of exactly {N} points with a LARGER minimum "
        "triangle area.\n"
        "The score of a configuration is the SMALLEST area among all "
        f"{N_TRIPLES} triangles formed by choosing 3 of the {N} points; "
        "maximise that smallest area.\n"
        f"MUST hold: exactly {N} points; every coordinate in [0,1]; no two "
        "points identical. Avoid placing any three points on a straight line "
        "— a collinear triple makes the score exactly 0.\n"
        f"Output ONLY the raw Python list of {N} [x, y] lists. No explanation, "
        "no code fences, no other text."
    )


def self_test():
    for name, cand in CANDIDATES.items():
        pts = [tuple(p) for p in cand]
        ev = evaluate(pts)
        assert ev["valid"], f"{name} must be valid"
        assert abs(ev["score"] - EXPECTED[name]) < 1e-15, \
            f"{name} score {ev['score']!r} != {EXPECTED[name]!r}"
    scores = [EXPECTED[k] for k in ("k1", "k10", "k100", "k1000")]
    assert scores == sorted(scores), "candidates must be graded ascending"
    p, err = parse_proposal("junk [[0.1, 0.1], [0.2, 0.9]] junk")
    assert err is None and len(p) == 2
    print("[selftest] evaluator + parser + all four candidates OK")


def append_jsonl(path, row):
    line = json.dumps(row)
    with open(path, "a") as f:
        f.write(line + "\n")
        f.flush()
        os.fsync(f.fileno())
    print("JSONL|" + line, flush=True)


def main():
    os.makedirs(WORK, exist_ok=True)
    self_test()
    from huggingface_hub import hf_hub_download
    os.makedirs(MODELS_DIR, exist_ok=True)
    print(f"[download] {FNAME} ...")
    path = hf_hub_download(repo_id=REPO, filename=FNAME, local_dir=MODELS_DIR)
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 22)
            if not b:
                break
            h.update(b)
    weight_sha = h.hexdigest()
    print(f"[hash] {weight_sha[:16]}...")

    from llama_cpp import Llama
    llm = Llama(model_path=path, n_gpu_layers=-1, n_ctx=N_CTX, verbose=False)
    smoke = llm.create_chat_completion(
        messages=[{"role": "user", "content": "Reply with the single word OK."}],
        max_tokens=8, temperature=0.0)
    assert smoke["choices"][0]["message"]["content"].strip(), "smoke empty"
    print("[load] smoke OK")

    summary = {"weight_sha256": weight_sha, "quant": "q4_k_m",
               "probes_per_candidate": PROBES_PER_CANDIDATE, "candidates": {}}
    SEED_BASE = {"k1": 991000, "k10": 992000, "k100": 993000, "k1000": 994000}
    for name, cand in CANDIDATES.items():
        parent = [tuple(p) for p in cand]
        pscore = EXPECTED[name]
        pkey = point_key(parent)
        improved = valid = echo = 0
        for k in range(PROBES_PER_CANDIDATE):
            prompt = loop_prompt(parent, pscore)
            t0 = time.time()
            try:
                out = llm.create_chat_completion(
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=MAX_TOKENS, temperature=TEMPERATURE, top_p=TOP_P,
                    seed=SEED_BASE[name] + k)
                text = out["choices"][0]["message"]["content"]
                gerr = None
            except Exception as e:
                text, gerr = None, f"gen_error: {type(e).__name__}"
            pts, perr = parse_proposal(text) if gerr is None else (None, gerr)
            ev = evaluate(pts)
            is_echo = ev["valid"] and point_key(pts) == pkey
            imp = ev["valid"] and ev["score"] > pscore
            valid += ev["valid"]
            echo += is_echo
            improved += imp
            append_jsonl(LOG, {
                "pilot": "wave8_seed_calibration", "candidate": name,
                "parent_score": pscore, "probe": k, "valid": ev["valid"],
                "score": ev["score"], "improved": bool(imp),
                "echo": bool(is_echo), "parse_error": perr,
                "wall_s": round(time.time() - t0, 2),
                "points": ([[x, y] for (x, y) in pts] if pts else None),
                "raw": (None if pts else (text or "")[:2000])})
            print(f"[{name}] probe {k}: valid={ev['valid']} "
                  f"score={ev['score']:.9f} improved={imp} echo={is_echo}")
        summary["candidates"][name] = {
            "parent_score": pscore, "valid": valid, "improved": improved,
            "echo": echo,
            "improve_rate": improved / PROBES_PER_CANDIDATE}
    with open(SUMMARY, "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))
    print("[done] wave-8 seed calibration pilot complete.")


if __name__ == "__main__":
    main()
