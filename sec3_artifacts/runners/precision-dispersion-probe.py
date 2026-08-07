#!/usr/bin/env python
# ============================================================================
# PREREGISTERED PREDICTIONS — written and committed BEFORE this run executes.
# Kaggle version history timestamps this code prior to execution.
#
# RUN DESIGN: Fixed-parent dispersion probe. Six circle-packing configurations
# are frozen as byte-identical JSON constants. Every rung feeds the same six
# parents through the same prompt template at the same temperature and top_p,
# varying only the sampling seed. Input identity is the experiment: any
# difference in output distribution across rungs is attributable to precision.
#
# PREDICTION A (mechanism claim holds): text dispersion and unique-cell count
# fall monotonically with precision while mean score among valid samples stays
# flat.
#
# PREDICTION B (capability floor dominates): viability falls and every other
# metric moves with it in lockstep.
#
# Disconfirmation: if both text dispersion AND viability fall monotonically,
# the data cannot distinguish mechanism from floor — the probe is inconclusive.
# If text dispersion stays flat while viability falls, the mechanism claim is
# falsified (quantization harms capability, not exploration).
# ============================================================================

# --- batch-kernel bootstrap: script kernels have no %pip -------------------
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
    import os as _os
    _env = dict(_os.environ, CMAKE_ARGS="-DGGML_CUDA=on")
    _sp.run([_sys.executable, "-m", "pip", "install", "-q",
             "--force-reinstall", "--no-cache-dir", "llama-cpp-python"],
            env=_env, check=True)
    import llama_cpp  # noqa: F401
print("[bootstrap] llama_cpp ready:", llama_cpp.__version__)
# ---------------------------------------------------------------------------

"""
FIXED-PARENT DISPERSION PROBE — precision-cliff mechanism test.

Tests whether quantization damages exploration (dispersion) independently of
exploitation (score among valids). Six frozen parent circle packings are fed
to Qwen2.5-Coder-14B at four quantization rungs with 16 independent samples
each. No evolutionary loop — every sample is a single-shot proposal from the
same frozen parent. This design kills the confound that sank the loop design:
inside an evolutionary loop, a weaker model's lower coverage is
indistinguishable from its lower viability.

Rung execution order (deliberate): q4_k_m → q2_k → q8_0 → q3_k_m (if time).
If the session dies early, the decisive mid-versus-cliff contrast (q4_k_m vs
q2_k) is already complete; q8_0 is the expendable ceiling condition.

Budget: 4 rungs x 6 parents x 16 samples = 384 generations.
Expected wall on T4 x2: ~3h including model loads.

Behaviour descriptor (fallback — no existing definition found in codebase):
20x20 binned 2D descriptor: radius coefficient-of-variation vs mean pairwise
center distance normalized by container size.
"""

import ast
import gc
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import time

# ----------------------------- configuration --------------------------------

REPO = "Qwen/Qwen2.5-Coder-14B-Instruct-GGUF"

# Rung execution order (v2): q2_k first (quick, decisive contrast-completing),
# q4_k_m second (upper mid), q8_0 third (ceiling, memory-risky),
# q3_k_m fourth (lower mid). This puts the q2_k-vs-q4_k_m contrast in the bag
# before the memory-risky q8_0 rung, and finishes with the least-informative rung.
#
# If q8_0 cannot load (needs 2 GPUs), substitute q6_k as ceiling.
# Verify q6_k filename exists in REPO before relying on it.
# A run reaching the end with no ceiling rung at all is a FAILED run.
RUNGS = [
    ("q2_k",   "qwen2.5-coder-14b-instruct-q2_k.gguf",   1),
    ("q4_k_m", "qwen2.5-coder-14b-instruct-q4_k_m.gguf", 1),
    ("q8_0",   "qwen2.5-coder-14b-instruct-q8_0.gguf",   2),
    ("q3_k_m", "qwen2.5-coder-14b-instruct-q3_k_m.gguf", 1),
]

N_PARENTS = 6
N_SAMPLES = 24  # per parent per rung (raised from 16 for v2)
N = 26           # circles
EPS = 1e-6
N_CTX = 4096
MAX_TOKENS = 1200
TEMPERATURE = 0.8   # from precision-sweep-14b-v2
TOP_P = 0.95        # from precision-sweep-14b-v2
RUNNER_VERSION = "dispersion_probe_v2"

# Q6_K fallback filename (must exist in REPO if q8_0 cannot load)
Q6_K_FNAME = "qwen2.5-coder-14b-instruct-q6_k.gguf"

# SIZING (revised from v1 observation: ~6 s/generation for echo outputs,
# q8_0 slower):
# 6p x 24s x 4r = 576 generations
# At ~6s/gen: 576*6 + (4 loads+downloads) ~ 3456+200 = ~3656s = 1.0h for q2_k/q4_k_m/q3_k_m
# q8_0 slower, budget ~2-3h wall. FITS within 4h budget.

WORK = "/kaggle/working/dispersion_probe"
MODELS_DIR = "/kaggle/tmp/models"
ZIP_BASE = "/kaggle/working/dispersion_probe_partial"
CAND_LOG = os.path.join(WORK, "probe_samples.jsonl")
PROVENANCE = os.path.join(WORK, "provenance.json")
RESULTS = os.path.join(WORK, "results_dispersion.json")
CIRCLES_DIR = os.path.join(WORK, "circles")  # per-sample circle dumps

if not os.path.isdir("/kaggle"):
    WORK = os.path.abspath("./dispersion_probe")
    MODELS_DIR = os.path.abspath("./models")
    ZIP_BASE = os.path.abspath("./dispersion_probe_partial")
    CAND_LOG = os.path.join(WORK, "probe_samples.jsonl")
    PROVENANCE = os.path.join(WORK, "provenance.json")
    RESULTS = os.path.join(WORK, "results_dispersion.json")
    CIRCLES_DIR = os.path.join(WORK, "circles")

# -------------------- frozen parent configurations --------------------------
# Generated deterministically, verified valid by self_test().
# Six parents span the score range observed in the 14B console log
# (0.88–1.80), giving roughly two low, two mid, two high.

FROZEN_PARENTS = [
    {
    "id": "p0_baseline",
    "score": 0.899990,
    "circles": [
        [0.083333, 0.100000, 0.034615],
        [0.250000, 0.100000, 0.034615],
        [0.416667, 0.100000, 0.034615],
        [0.583333, 0.100000, 0.034615],
        [0.750000, 0.100000, 0.034615],
        [0.916667, 0.100000, 0.034615],
        [0.083333, 0.300000, 0.034615],
        [0.250000, 0.300000, 0.034615],
        [0.416667, 0.300000, 0.034615],
        [0.583333, 0.300000, 0.034615],
        [0.750000, 0.300000, 0.034615],
        [0.916667, 0.300000, 0.034615],
        [0.083333, 0.500000, 0.034615],
        [0.250000, 0.500000, 0.034615],
        [0.416667, 0.500000, 0.034615],
        [0.583333, 0.500000, 0.034615],
        [0.750000, 0.500000, 0.034615],
        [0.916667, 0.500000, 0.034615],
        [0.083333, 0.700000, 0.034615],
        [0.250000, 0.700000, 0.034615],
        [0.416667, 0.700000, 0.034615],
        [0.583333, 0.700000, 0.034615],
        [0.750000, 0.700000, 0.034615],
        [0.916667, 0.700000, 0.034615],
        [0.083333, 0.900000, 0.034615],
        [0.250000, 0.900000, 0.034615]
    ]
},
    {
    "id": "p1_low",
    "score": 0.880168,
    "circles": [
        [0.083333, 0.100000, 0.033577],
        [0.250000, 0.100000, 0.033625],
        [0.416667, 0.100000, 0.034163],
        [0.583333, 0.100000, 0.034353],
        [0.750000, 0.100000, 0.033620],
        [0.916667, 0.100000, 0.033577],
        [0.083333, 0.300000, 0.034361],
        [0.250000, 0.300000, 0.033577],
        [0.416667, 0.300000, 0.033815],
        [0.583333, 0.300000, 0.033774],
        [0.750000, 0.300000, 0.033577],
        [0.916667, 0.300000, 0.033577],
        [0.083333, 0.500000, 0.034386],
        [0.250000, 0.500000, 0.034310],
        [0.416667, 0.500000, 0.033577],
        [0.583333, 0.500000, 0.033947],
        [0.750000, 0.500000, 0.033577],
        [0.916667, 0.500000, 0.033577],
        [0.083333, 0.700000, 0.033916],
        [0.250000, 0.700000, 0.033577],
        [0.416667, 0.700000, 0.033899],
        [0.583333, 0.700000, 0.033577],
        [0.750000, 0.700000, 0.033962],
        [0.916667, 0.700000, 0.034031],
        [0.083333, 0.900000, 0.033968],
        [0.250000, 0.900000, 0.034268]
    ]
},
    {
    "id": "p2_mid_a",
    "score": 1.040183,
    "circles": [
        [0.083333, 0.100000, 0.040714],
        [0.250000, 0.100000, 0.044463],
        [0.416667, 0.100000, 0.040257],
        [0.583333, 0.100000, 0.041115],
        [0.750000, 0.100000, 0.041698],
        [0.916667, 0.100000, 0.040387],
        [0.083333, 0.300000, 0.036561],
        [0.250000, 0.300000, 0.035583],
        [0.416667, 0.300000, 0.041492],
        [0.583333, 0.300000, 0.038720],
        [0.750000, 0.300000, 0.046061],
        [0.916667, 0.300000, 0.038042],
        [0.083333, 0.500000, 0.033024],
        [0.250000, 0.500000, 0.039474],
        [0.416667, 0.500000, 0.037109],
        [0.583333, 0.500000, 0.042728],
        [0.750000, 0.500000, 0.046792],
        [0.916667, 0.500000, 0.040535],
        [0.083333, 0.700000, 0.041335],
        [0.250000, 0.700000, 0.037026],
        [0.416667, 0.700000, 0.039404],
        [0.583333, 0.700000, 0.040483],
        [0.750000, 0.700000, 0.033347],
        [0.916667, 0.700000, 0.041650],
        [0.083333, 0.900000, 0.040593],
        [0.250000, 0.900000, 0.041590]
    ]
},
    {
    "id": "p3_mid_b",
    "score": 1.300050,
    "circles": [
        [0.083333, 0.100000, 0.048803],
        [0.250000, 0.100000, 0.046837],
        [0.416667, 0.100000, 0.067710],
        [0.583333, 0.100000, 0.049686],
        [0.750000, 0.100000, 0.045732],
        [0.916667, 0.100000, 0.044943],
        [0.083333, 0.300000, 0.054516],
        [0.250000, 0.300000, 0.043105],
        [0.416667, 0.300000, 0.044612],
        [0.583333, 0.300000, 0.045554],
        [0.750000, 0.300000, 0.056407],
        [0.916667, 0.300000, 0.044461],
        [0.083333, 0.500000, 0.053736],
        [0.250000, 0.500000, 0.050531],
        [0.416667, 0.500000, 0.045187],
        [0.583333, 0.500000, 0.047974],
        [0.750000, 0.500000, 0.050579],
        [0.916667, 0.500000, 0.051900],
        [0.083333, 0.700000, 0.053441],
        [0.250000, 0.700000, 0.044228],
        [0.416667, 0.700000, 0.049955],
        [0.583333, 0.700000, 0.045614],
        [0.750000, 0.700000, 0.052527],
        [0.916667, 0.700000, 0.047709],
        [0.083333, 0.900000, 0.062583],
        [0.250000, 0.900000, 0.051720]
    ]
},
    {
    "id": "p4_high_a",
    "score": 1.550450,
    "circles": [
        [0.083333, 0.100000, 0.066788],
        [0.250000, 0.100000, 0.060051],
        [0.416667, 0.100000, 0.062999],
        [0.583333, 0.100000, 0.061894],
        [0.750000, 0.100000, 0.060557],
        [0.916667, 0.100000, 0.053887],
        [0.083333, 0.300000, 0.068938],
        [0.250000, 0.300000, 0.053552],
        [0.416667, 0.300000, 0.056318],
        [0.583333, 0.300000, 0.061363],
        [0.750000, 0.300000, 0.062687],
        [0.916667, 0.300000, 0.066429],
        [0.083333, 0.500000, 0.052295],
        [0.250000, 0.500000, 0.056743],
        [0.416667, 0.500000, 0.052566],
        [0.583333, 0.500000, 0.061028],
        [0.750000, 0.500000, 0.064329],
        [0.916667, 0.500000, 0.052659],
        [0.083333, 0.700000, 0.049671],
        [0.250000, 0.700000, 0.061556],
        [0.416667, 0.700000, 0.054822],
        [0.583333, 0.700000, 0.062531],
        [0.750000, 0.700000, 0.059357],
        [0.916667, 0.700000, 0.063096],
        [0.083333, 0.900000, 0.068510],
        [0.250000, 0.900000, 0.055824]
    ]
},
    {
    "id": "p5_high_b",
    "score": 1.650407,
    "circles": [
        [0.083333, 0.100000, 0.069133],
        [0.250000, 0.100000, 0.065892],
        [0.416667, 0.100000, 0.054418],
        [0.583333, 0.100000, 0.071422],
        [0.750000, 0.100000, 0.052439],
        [0.916667, 0.100000, 0.066183],
        [0.083333, 0.300000, 0.064863],
        [0.250000, 0.300000, 0.056169],
        [0.416667, 0.300000, 0.063567],
        [0.583333, 0.300000, 0.054818],
        [0.750000, 0.300000, 0.057169],
        [0.916667, 0.300000, 0.055361],
        [0.083333, 0.500000, 0.064836],
        [0.250000, 0.500000, 0.049804],
        [0.416667, 0.500000, 0.066142],
        [0.583333, 0.500000, 0.056726],
        [0.750000, 0.500000, 0.070268],
        [0.916667, 0.500000, 0.062829],
        [0.083333, 0.700000, 0.062501],
        [0.250000, 0.700000, 0.064317],
        [0.416667, 0.700000, 0.084222],
        [0.583333, 0.700000, 0.071249],
        [0.750000, 0.700000, 0.063379],
        [0.916667, 0.700000, 0.083333],
        [0.083333, 0.900000, 0.057075],
        [0.250000, 0.900000, 0.062292]
    ]
}
]

# ------------------------- evaluator (mirrors v2) ---------------------------

def parse_proposal(raw):
    """Extract Python list of [x, y, r] floats from raw model output."""
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
    """Return {viable, valid, score, mean_radius, density, n_circles}."""
    res = {"viable": False, "valid": False, "score": 0.0,
           "mean_radius": 0.0, "density": 0.0,
           "n_circles": 0 if circles is None else len(circles)}
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


def self_test():
    """Verify all frozen parents are valid."""
    for p in FROZEN_PARENTS:
        circles = [tuple(c) for c in p["circles"]]
        ev = evaluate(circles)
        assert ev["valid"], f"{p['id']}: not valid"
        assert abs(ev["score"] - p["score"]) < 1e-5, \
            f"{p['id']}: score mismatch stored={p['score']} computed={ev['score']}"
    # Quick parse test
    c, err = parse_proposal("junk before [[0.1, 0.1, 0.05]] junk after")
    assert err is None and len(c) == 1, "parser broken"
    print("[selftest] all parents valid, parser OK")


# ------------------------------ prompts -------------------------------------

def probe_prompt(parent_circles, parent_score):
    """Fixed-parent prompt: 'Here is a packing, propose a variation.'
    Uses same template as loop_prompt from v2 but with single-shot framing."""
    packing = json.dumps([[round(x, 6), round(y, 6), round(r, 6)]
                          for (x, y, r) in parent_circles])
    return (
        "You are the proposal step of an evolutionary search for circle packings.\n"
        f"Current best packing (sum of radii = {parent_score:.6f}):\n{packing}\n\n"
        f"Produce a packing of exactly {N} circles with a HIGHER sum of radii.\n"
        "MUST hold: exactly 26 circles; every circle fully inside the unit square "
        "[0,1]x[0,1] (x-r >= 0, x+r <= 1, same for y); no two circles overlap "
        "(distance between centers >= sum of the two radii; touching is allowed).\n"
        "Output ONLY the raw Python list of 26 [x, y, r] lists. No explanation, "
        "no code fences, no other text."
    )


# --------------------- text dispersion metrics ------------------------------

def text_ngrams(text, n=4):
    """Extract character-level n-grams from text."""
    t = text or ""
    return set(t[i:i+n] for i in range(len(t) - n + 1))


def normalized_edit_distance(a, b):
    """Normalized Levenshtein-like: (len(a)+len(b)-2*LCS) / max(len(a),len(b),1)."""
    if not a and not b:
        return 0.0
    if not a or not b:
        return 1.0
    # Simple LCS via DP
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(2)]
    for i in range(1, m + 1):
        cur = i % 2
        prev = 1 - cur
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]:
                dp[cur][j] = dp[prev][j-1] + 1
            else:
                dp[cur][j] = max(dp[prev][j], dp[cur][j-1])
    lcs = dp[m % 2][n]
    return 1.0 - (2.0 * lcs) / max(len(a), len(b), 1)


def text_dispersion(texts):
    """Return {distinct_4gram_ratio, mean_pairwise_ned}.
    Computed over all texts including empty/invalid outputs."""
    n = len(texts)
    if n <= 1:
        return {"distinct_4gram_ratio": 1.0, "mean_pairwise_ned": 0.0}

    # Distinct 4-gram ratio: union / (n * mean set size)
    all_ngrams = []
    for t in texts:
        all_ngrams.append(text_ngrams(t, 4))
    union = set.union(*all_ngrams) if all_ngrams else set()
    total_size = sum(len(s) for s in all_ngrams)
    ratio = len(union) / max(total_size, 1)

    # Mean pairwise normalized edit distance
    ned_sum = 0.0
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            ned_sum += normalized_edit_distance(texts[i], texts[j])
            count += 1
    mean_ned = ned_sum / max(count, 1)

    return {"distinct_4gram_ratio": round(ratio, 6),
            "mean_pairwise_ned": round(mean_ned, 6)}


# --------------------- behaviour descriptor ---------------------------------
# Fallback: no MAP-Elites cell definition exists in this codebase.
# Using 20x20 binned 2D descriptor: radius CV vs mean pairwise center distance
# normalized by container size.

def radius_cv(circles):
    """Coefficient of variation of radii."""
    if not circles or len(circles) < 2:
        return 0.0
    radii = [r for (_, _, r) in circles]
    mean_r = sum(radii) / len(radii)
    if mean_r < 1e-9:
        return 0.0
    stdev = math.sqrt(sum((r - mean_r) ** 2 for r in radii) / len(radii))
    return stdev / mean_r


def mean_pairwise_center_distance(circles):
    """Mean pairwise center distance normalized by container size (1.0)."""
    if not circles or len(circles) < 2:
        return 0.0
    total = 0.0
    count = 0
    for i in range(len(circles)):
        xi, yi, _ = circles[i]
        for j in range(i + 1, len(circles)):
            xj, yj, _ = circles[j]
            total += math.hypot(xi - xj, yi - yj)
            count += 1
    return total / max(count, 1)


def behaviour_descriptor(circles):
    """20x20 binned (radius_cv, mean_center_dist). Returns (bin_x, bin_y)."""
    if circles is None or len(circles) < 2:
        return None
    cv = radius_cv(circles)
    dist = mean_pairwise_center_distance(circles)
    # cv typically 0-1, dist typically 0-0.8. Bin into 20x20.
    bin_x = min(19, int(cv * 20.0))
    bin_y = min(19, int(dist / 0.8 * 20.0))
    return (bin_x, bin_y)


def coordinate_echo(sample_circles, parent_circles, tolerance=1e-5):
    """Check if sample geometry matches parent within tolerance.
    Order-insensitive: sorts both and compares element-wise."""
    if sample_circles is None or parent_circles is None:
        return False
    if len(sample_circles) != len(parent_circles):
        return False
    # Sort by (x, y, r)
    s_sorted = sorted(sample_circles)
    p_sorted = sorted(parent_circles)
    for (sx, sy, sr), (px, py, pr) in zip(s_sorted, p_sorted):
        if (abs(sx - px) > tolerance or abs(sy - py) > tolerance or
                abs(sr - pr) > tolerance):
            return False
    return True


# Global flag: set after first generation attempt
LOGPROBS_AVAILABLE = None  # None=unknown, True, False


def logprobs_status_str():
    if LOGPROBS_AVAILABLE is None:
        return "unknown (will check on first generation)"
    return "available" if LOGPROBS_AVAILABLE else "NOT AVAILABLE on this build"


# ------------------------------ plumbing ------------------------------------

def sha256_file(path, buf=1 << 22):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(buf)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def gpu_info():
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
            capture_output=True, text=True, timeout=30).stdout.strip()
        return [l.strip() for l in out.splitlines() if l.strip()]
    except Exception:
        return []


def append_probe(path, row):
    """Append row to jsonl AND echo PROBE| to stdout for durability."""
    line = json.dumps(row)
    with open(path, "a") as f:
        f.write(line + "\n")
        f.flush()
        os.fsync(f.fileno())
    print("PROBE|" + line, flush=True)


def snapshot_zip():
    try:
        shutil.make_archive(ZIP_BASE, "zip", WORK)
        print(f"[zip] snapshot -> {ZIP_BASE}.zip")
    except Exception as e:
        print(f"[zip] FAILED (non-fatal): {type(e).__name__}: {e}")


def load_provenance():
    if os.path.exists(PROVENANCE):
        with open(PROVENANCE) as f:
            return json.load(f)
    return {"created": time.strftime("%Y-%m-%d %H:%M:%S"), "gpus": gpu_info(),
            "repo": REPO, "rungs": [r[0] for r in RUNGS],
            "n_parents": N_PARENTS, "n_samples": N_SAMPLES,
            "temperature": TEMPERATURE, "top_p": TOP_P,
            "runner_version": RUNNER_VERSION,
            "behaviour_descriptor": "20x20 binned radius_CV vs mean_pairwise_center_distance (fallback — no existing descriptor found in codebase)",
            "parent_ids": [p["id"] for p in FROZEN_PARENTS],
            "parent_scores": [p["score"] for p in FROZEN_PARENTS],
            "conditions": {}}


def save_provenance(p):
    with open(PROVENANCE, "w") as f:
        json.dump(p, f, indent=2)


# --------------------------- model management -------------------------------

def download_model(fname):
    from huggingface_hub import hf_hub_download
    os.makedirs(MODELS_DIR, exist_ok=True)
    print(f"[download] {fname} ...")
    t0 = time.time()
    path = hf_hub_download(repo_id=REPO, filename=fname, local_dir=MODELS_DIR)
    print(f"[download] done in {time.time()-t0:.0f}s -> {path}")
    return path


def load_llm(path, n_gpus, provenance, quant):
    """Load model. If q8_0 fails (or only 1 GPU), try q6_k fallback."""
    from llama_cpp import Llama
    kwargs = dict(model_path=path, n_gpu_layers=-1, n_ctx=N_CTX, verbose=False)
    if n_gpus > 1:
        kwargs["split_mode"] = 1
    print(f"[load] {os.path.basename(path)} (gpus={n_gpus})")
    t0 = time.time()
    try:
        llm = Llama(**kwargs)
    except Exception as e:
        if quant == "q8_0" and Q6_K_FNAME:
            # q8_0 failed — try q6_k ceiling substitution
            print(f"[load] q8_0 failed: {type(e).__name__}: {e}")
            print(f"[load] substituting q6_k as ceiling rung")
            # Verify q6_k exists in the repo
            from huggingface_hub import hf_hub_download
            try:
                q6k_path = hf_hub_download(repo_id=REPO, filename=Q6_K_FNAME, local_dir=MODELS_DIR)
            except Exception as e2:
                print(f"[load] FATAL: q6_k download also failed: {type(e2).__name__}: {e2}")
                provenance["conditions"].setdefault("ceiling_substitution", {})[
                    "error"] = f"q8_0 raised {e}, q6_k download raised {e2}"
                provenance["conditions"]["q8_0"]["skipped"] = f"load failed: {e}; q6_k download failed: {e2}"
                save_provenance(provenance)
                raise RuntimeError("No ceiling rung available — run FAILED") from e
            cond_sub = provenance["conditions"].setdefault("ceiling_substitution", {})
            cond_sub["original"] = "q8_0"
            cond_sub["substitute"] = "q6_k"
            cond_sub["q8_0_error"] = f"{type(e).__name__}: {e}"
            cond_sub["q6_k_sha256"] = sha256_file(q6k_path)
            cond_sub["q6_k_filename"] = Q6_K_FNAME
            cond_sub["q6_k_bytes"] = os.path.getsize(q6k_path)
            save_provenance(provenance)
            llm = Llama(model_path=q6k_path, n_gpu_layers=-1, n_ctx=N_CTX, verbose=False)
        else:
            raise
    print(f"[load] ready in {time.time()-t0:.0f}s")
    return llm


def generate(llm, prompt, seed_val, capture_logprobs=False):
    """Generate text from prompt. Returns (text, error, completion_tokens, wall_s, logprobs_or_none).

    When capture_logprobs=True and the call raises, retry without logprobs
    so no sample is ever lost to logprob capture failure."""
    t0 = time.time()
    try:
        kwargs = dict(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=MAX_TOKENS, temperature=TEMPERATURE, top_p=TOP_P,
            seed=seed_val)
        if capture_logprobs:
            kwargs["logprobs"] = 8
            kwargs["top_logprobs"] = 8
        out = llm.create_chat_completion(**kwargs)
        text = out["choices"][0]["message"]["content"]
        usage = out.get("usage", {})
        logprobs = out["choices"][0].get("logprobs", None)
    except Exception as e:
        if capture_logprobs:
            # Retry without logprobs — never lose a sample to logprob failure
            print(f"  [retry] logprobs failed ({type(e).__name__}), retrying without logprobs")
            try:
                kwargs.pop("logprobs", None)
                kwargs.pop("top_logprobs", None)
                out = llm.create_chat_completion(**kwargs)
                text = out["choices"][0]["message"]["content"]
                usage = out.get("usage", {})
                logprobs = None
            except Exception as e2:
                return None, f"gen_error: {type(e2).__name__}: {e2}", 0, time.time() - t0, None
        else:
            return None, f"gen_error: {type(e).__name__}: {e}", 0, time.time() - t0, None
    return text, None, usage.get("completion_tokens", 0), time.time() - t0, logprobs


def set_logprobs_available(result):
    """Update global flag based on whether logprobs were returned."""
    global LOGPROBS_AVAILABLE
    if LOGPROBS_AVAILABLE is None and result is not None:
        LOGPROBS_AVAILABLE = True


# ------------------------------ main probe ----------------------------------

def run_rung(quant, fname, min_gpus, provenance):
    n_gpus = len(provenance["gpus"])
    if n_gpus < min_gpus:
        print(f"[skip] {quant}: needs {min_gpus} GPU(s), have {n_gpus}")
        # Reload provenance from disk to avoid overwriting previous rungs' metrics
        prov = load_provenance()
        prov["conditions"].setdefault(quant, {})["skipped"] = \
            f"needs {min_gpus} gpus, have {n_gpus}"
        save_provenance(prov)
        return

    path = download_model(fname)
    # Reload provenance from disk so every rung's block persists
    prov = load_provenance()
    cond = prov["conditions"].setdefault(quant, {})
    if "sha256" not in cond:
        print(f"[hash] {quant} ...")
        cond["sha256"] = sha256_file(path)
        cond["bytes"] = os.path.getsize(path)
        cond["filename"] = fname
        save_provenance(prov)
        print(f"[hash] {cond['sha256'][:16]}... ({cond['bytes']/1e9:.2f} GB)")

    llm = load_llm(path, n_gpus, prov, quant)
    # After load_llm may have rewritten provenance (q6_k substitution), reload
    prov = load_provenance()
    logprobs_obtainable = None  # None=unknown, True=yes, False=no
    try:
        # For each parent, generate N_SAMPLES independent draws
        for parent in FROZEN_PARENTS:
            pid = parent["id"]
            parent_score = parent["score"]
            parent_circles = [tuple(c) for c in parent["circles"]]

            for sample_idx in range(N_SAMPLES):
                # v2 seed salt ensures out-of-sample from v1
                seed_val = int(hashlib.sha256(
                    f"{quant}_{pid}_{sample_idx}_v2".encode()).hexdigest()[:8], 16)
                prompt = probe_prompt(parent_circles, parent_score)

                # Request logprobs only for sample 0 of each parent (expensive)
                capture_lp = (sample_idx == 0)
                text, gerr, ctoks, wall, logprobs = generate(
                    llm, prompt, seed_val, capture_logprobs=capture_lp)
                if capture_lp and logprobs is not None:
                    set_logprobs_available(logprobs)
                if capture_lp and gerr is None:
                    # Generation succeeded — logprobs may or may not be present
                    if logprobs_obtainable is None:
                        logprobs_obtainable = (logprobs is not None)
                circles, perr = parse_proposal(text) if gerr is None else (None, gerr)
                ev = evaluate(circles)

                # Behaviour descriptor
                bd = behaviour_descriptor(circles)

                # Coordinate-verified echo
                is_echo = coordinate_echo(circles, parent_circles)

                # Score delta vs parent
                score_delta = round(ev["score"] - parent_score, 6) if ev["valid"] else None

                # Coordinates (mandatory — makes every downstream descriptor recomputable)
                coords = ([[round(x, 6), round(y, 6), round(r, 6)]
                            for (x, y, r) in circles]
                          if circles is not None else None)

                row = {
                    "arm": "fixed_parent_dispersion_probe",
                    "proposer": f"qwen2.5-coder-14b-{quant}",
                    "rung": quant,
                    "parent_id": pid,
                    "parent_score": round(parent_score, 6),
                    "sample_idx": sample_idx,
                    "parse_ok": perr is None,
                    "parse_error": perr,
                    "n_circles": ev["n_circles"],
                    "circles": coords,
                    "valid": ev["valid"],
                    "viable": ev["viable"],
                    "score": round(ev["score"], 6),
                    "score_delta": score_delta,
                    "mean_radius": round(ev["mean_radius"], 6),
                    "density": round(ev["density"], 6),
                    "echo": is_echo,
                    "behaviour_bin": list(bd) if bd else None,
                    "raw_text": (text or "")[:3000],
                    "completion_tokens": ctoks,
                    "wall_s": round(wall, 2),
                    "seed_val": seed_val,
                }

                # Logprobs for first 32 tokens of sample 0 per parent
                if sample_idx == 0 and logprobs is not None:
                    try:
                        top_logprobs = []
                        for lp in logprobs.get("content", [])[:32]:
                            top8 = sorted(lp.get("top_logprobs", []),
                                          key=lambda x: x.get("logprob", -999),
                                          reverse=True)[:8]
                            top_logprobs.append([{"token": t.get("token", ""),
                                                  "logprob": t.get("logprob", 0)}
                                                 for t in top8])
                        row["logprobs_top8_first32"] = top_logprobs
                    except Exception:
                        row["logprobs_top8_first32"] = None

                append_probe(CAND_LOG, row)

                print(f"[{quant}] {pid} sample {sample_idx}: "
                      f"score={ev['score']:.6f} valid={ev['valid']} "
                      f"echo={is_echo} ({wall:.0f}s)")

        # After all samples for this rung: compute and emit per-rung metrics
        # Also record the logprobs flag in provenance
        prov = load_provenance()
        prov["conditions"].setdefault(quant, {})["logprobs_obtainable"] = logprobs_obtainable
        save_provenance(prov)
        emit_rung_metrics(quant)

    finally:
        del llm
        gc.collect()
        try:
            os.remove(path)
            print(f"[cleanup] removed {fname}")
        except OSError:
            pass
    snapshot_zip()


def load_probe_rows(quant):
    """Load all probe rows for a given rung from the jsonl log."""
    if not os.path.exists(CAND_LOG):
        return []
    rows = []
    with open(CAND_LOG) as f:
        for line in f:
            try:
                r = json.loads(line)
                if r.get("rung") == quant:
                    rows.append(r)
            except json.JSONDecodeError:
                pass
    return rows


def emit_rung_metrics(quant):
    """Compute and print per-rung metrics table from logged rows."""
    rows = load_probe_rows(quant)
    if not rows:
        print(f"[metrics] {quant}: no rows yet")
        return

    # Partition by parent
    by_parent = {}
    for r in rows:
        by_parent.setdefault(r["parent_id"], []).append(r)

    # --- viability rate ---
    viable_n = sum(1 for r in rows if r["viable"])
    valid_n = sum(1 for r in rows if r["valid"])
    total_n = len(rows)
    viability_rate = viable_n / max(total_n, 1)
    validity_rate = valid_n / max(total_n, 1)

    # --- mean and max score among valid, score delta vs parent ---
    valid_rows = [r for r in rows if r["valid"]]
    mean_score = sum(r["score"] for r in valid_rows) / max(len(valid_rows), 1) if valid_rows else 0.0
    max_score = max((r["score"] for r in valid_rows), default=0.0)
    mean_delta = sum(r["score_delta"] for r in valid_rows if r["score_delta"] is not None) / max(len(valid_rows), 1) if valid_rows else 0.0

    # --- text-level dispersion over all 16 samples per parent ---
    text_disp_by_parent = {}
    for pid, prows in by_parent.items():
        raw_texts = [r.get("raw_text", "") or "" for r in prows]
        text_disp_by_parent[pid] = text_dispersion(raw_texts)
    mean_4gram = sum(d["distinct_4gram_ratio"] for d in text_disp_by_parent.values()) / max(len(text_disp_by_parent), 1)
    mean_ned = sum(d["mean_pairwise_ned"] for d in text_disp_by_parent.values()) / max(len(text_disp_by_parent), 1)

    # --- behaviour-descriptor spread ---
    all_bins = set()
    valid_rows_with_bins = 0
    for r in rows:
        if r["behaviour_bin"] and r["valid"]:
            all_bins.add(tuple(r["behaviour_bin"]))
            valid_rows_with_bins += 1
    unique_cells = len(all_bins)
    cells_per_valid = unique_cells / max(valid_rows_with_bins, 1) if valid_rows_with_bins > 0 else 0.0

    # --- coordinate-verified echo rate ---
    echo_n = sum(1 for r in rows if r["echo"])
    echo_rate = echo_n / max(total_n, 1)

    metrics = {
        "rung": quant,
        "total_samples": total_n,
        "viable": viable_n,
        "valid": valid_n,
        "viability_rate": round(viability_rate, 4),
        "validity_rate": round(validity_rate, 4),
        "mean_score_valid": round(mean_score, 6),
        "max_score_valid": round(max_score, 6),
        "mean_score_delta_vs_parent": round(mean_delta, 6),
        "text_dispersion_mean_4gram_ratio": round(mean_4gram, 4),
        "text_dispersion_mean_pairwise_ned": round(mean_ned, 4),
        "behaviour_unique_cells": unique_cells,
        "behaviour_cells_per_valid": round(cells_per_valid, 4),
        "coordinate_echo_rate": round(echo_rate, 4),
        "echo_count": echo_n,
    }

    print(f"\n[METRICS] {'='*14} {quant} {'='*14}")
    print(json.dumps(metrics, indent=2))

    # Save to provenance
    provenance = load_provenance()
    provenance["conditions"].setdefault(quant, {})["metrics"] = metrics
    save_provenance(provenance)


def main():
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(CIRCLES_DIR, exist_ok=True)
    self_test()
    provenance = load_provenance()
    if not provenance["gpus"]:
        provenance["gpus"] = gpu_info()
    save_provenance(provenance)
    print(f"[gpus] {provenance['gpus'] or 'NONE DETECTED (will be very slow)'}")
    print(f"[logprobs] {logprobs_status_str()}")
    print(f"[parents] {len(FROZEN_PARENTS)} parents, scores: "
          f"{[p['score'] for p in FROZEN_PARENTS]}")
    print(f"[budget] {len(RUNGS)} rungs x {N_PARENTS}p x {N_SAMPLES}s = "
          f"{len(RUNGS) * N_PARENTS * N_SAMPLES} samples")

    rungs_to_run = RUNGS  # all four rungs

    for quant, fname, min_gpus in rungs_to_run:
        print(f"\n===== rung: {quant} =====")
        run_rung(quant, fname, min_gpus, provenance)

    # Final summary
    print("\n===== FINAL SUMMARY =====")
    provenance = load_provenance()
    for quant, _, _ in rungs_to_run:
        cond = provenance["conditions"].get(quant, {})
        m = cond.get("metrics", {})
        if m:
            print(f"  {quant}: valid={m.get('valid',0)}/{m.get('total_samples',0)} "
                  f"viability={m.get('viability_rate',0):.3f} "
                  f"echo_rate={m.get('coordinate_echo_rate',0):.3f} "
                  f"4gram={m.get('text_dispersion_mean_4gram_ratio',0):.3f} "
                  f"ned={m.get('text_dispersion_mean_pairwise_ned',0):.3f} "
                  f"cells={m.get('behaviour_unique_cells',0)}")
        else:
            print(f"  {quant}: no metrics (skipped or failed)")

    snapshot_zip()
    print("\n[done] dispersion probe complete.")


if __name__ == "__main__":
    main()
