#!/usr/bin/env python
# ============================================================================
# WAVE 3 — PREREGISTERED PREDICTIONS, written and pushed BEFORE this run
# executed. (Kaggle version history timestamps this code prior to execution.)
#
# Task: Heilbronn triangle, n = 13 points in the unit square. Score = the
# minimum triangle area over all C(13,3) = 286 triples. Higher is better.
# Best known for n = 13 is ~0.0250. Deterministic, exact in floating point,
# no tolerance parameter, no scorer of ours anywhere in the loop.
#
# SEED PARENT (fixed, identical for every lineage and every rung; chosen
# non-degenerate and deliberately MEDIOCRE — 0.009087 is ~36% of best known,
# i.e. the lower half of what a competent proposer reaches, leaving headroom
# to climb and carrying no visible symmetry):
#
#   [[0.223341, 0.919137], [0.000000, 0.000000], [0.192827, 0.682068],
#    [0.711251, 1.000000], [0.938451, 0.958662], [1.000000, 0.014882],
#    [0.661960, 0.344964], [0.608847, 0.147190], [1.000000, 0.853188],
#    [0.809867, 0.345775], [0.345465, 0.982286], [0.932750, 0.557582],
#    [0.660363, 0.807716]]
#
#   SEED PARENT SCORE = 0.009087361292500006
#
# CONDITIONS (spec §3). Same pinned ladder, same inference stack, SHA-256
# recorded per weight file:
#     Q4_K_M  qwen2.5-coder-14b-instruct-q4_k_m.gguf   8 lineages x 15 gens = 120
#     Q2_K    qwen2.5-coder-14b-instruct-q2_k.gguf    25 lineages x 15 gens = 375
# Asymmetric BY DESIGN and registered rather than discovered: the primary in
# 5.3 needs departures at the 2-bit rung, and the observed 2-bit departure rate
# is 2-16% of calls. At 8% of 375 calls the expected departure count is 30; at
# the symmetric allocation it would be 10, which is the count that made the
# prior wave's conditional question unanswerable.
#
# SEEDS — a published fixed list of 33 values, none used in any prior wave
# (prior waves used 42, 123, 456, 789, 1111, 2222, 3333, 5555, 7777, 9999):
#     Q4_K_M (8):  3101 3102 3103 3104 3105 3106 3107 3108
#     Q2_K  (25):  3201 3202 3203 3204 3205 3206 3207 3208 3209 3210 3211
#                  3212 3213 3214 3215 3216 3217 3218 3219 3220 3221 3222
#                  3223 3224 3225
#
# Q8_0 IS NOT RUN. Both prior probe waves recorded it skipped for want of a
# second GPU, and registering a condition the hardware cannot serve is what
# produced wave 2's FAILED verdict. Its absence here is a design decision, not
# a failure, and is stated as such in advance.
#
# ---------------------------------------------------------------------------
# THE SIX REGISTERED PREDICTIONS AND DECISION RULES (spec §5, verbatim):
#
#  5.1 — PRIMARY. Accepted hill-climb steps per lineage.
#     Mean accepted steps per lineage will be <= 1.5 at Q2_K and >= 4.0 at
#     Q4_K_M. Refuted if either bound is violated. (§3.6 observed 0.6 and 3.2
#     on circle packing at ten generations; these bounds are stated for
#     fifteen and are deliberately not the observed values.)
#
#  5.2 — SECONDARY, the form that failed before. Fraction of lineages
#     improving past the seed parent at all: <= 0.45 at Q2_K, >= 0.85 at
#     Q4_K_M. Registered explicitly because its circle-packing analogue (F1)
#     was refuted; if 5.1 holds and 5.2 fails again, that is evidence the
#     binary form is the wrong instrument rather than evidence against the
#     effect, and the pair of outcomes says so without any post-hoc choice on
#     our part.
#
#  5.3 — PRIMARY. Conditional-on-departure improvement rate. Among valid
#     non-echo outputs, the fraction scoring above the running parent.
#     DECISION RULE, both branches informative:
#       - Q2_K rate >= 0.75 x Q4_K_M rate -> quantization gates the FREQUENCY
#         of departure and not its QUALITY. This is the repairable reading,
#         and it makes forced-departure interventions worth testing.
#       - Q2_K rate <= 0.50 x Q4_K_M rate -> quality degrades too; forced
#         departure would produce worse proposals, not better search.
#       - Between -> inconclusive, reported as such.
#       - POWER FLOOR: if fewer than 25 Q2_K departures are observed, the
#         verdict is UNDERPOWERED and no branch is claimed regardless of the
#         ratio. This clause exists because wave 2's addendum had to add one
#         after the fact.
#
#  5.4 — Echo. Coordinate-verified parent echo among valid outputs: >= 55% at
#     Q2_K, <= 30% at Q4_K_M. Lower than §3's circle-packing bound because the
#     seed parent here carries no template the proposer might emit for reasons
#     unrelated to copying.
#
#  5.5 — Template check, no analogue in prior waves. Fraction of valid outputs
#     scoring exactly 0 (three or more collinear points): reported per rung
#     with no bound. It has no prediction attached because we have no basis
#     for one; it exists to detect the failure mode this task was chosen to
#     expose, and reporting it unpredicted is honest about that.
#
#  5.6 — Outcome. Final best score per lineage, permutation-tested at lineage
#     level. NO BOUND IS REGISTERED. §3.6 found the outcome metric blind on
#     circle packing at ten generations and framed longer-horizon divergence
#     as a prediction; fifteen generations is not obviously long enough to
#     settle it, and registering a bound we cannot justify would be the error
#     this wave exists to avoid. It is reported as a descriptive with its
#     exact tail.
#
# DISCONFIRMATION (spec §6, verbatim):
#  If 5.1 and 5.4 both fail at Q2_K, the loop-level collapse does not
#  generalise beyond circle packing. §3.6 would then be rewritten as a
#  single-task observation and the paper's scope sentence amended, not
#  softened in place. We commit to that rewrite here so that the commitment
#  predates the outcome.
#  If 5.1 holds and 5.4 fails, the step collapse is not echo-driven on this
#  task, and the identity paragraph in §3.6 does not transfer — a more
#  interesting outcome than the confirmatory one, and the reason both are
#  registered separately.
# ============================================================================

# --- batch-kernel bootstrap: script kernels have no %pip -------------------
# Gated behind main() so that --dry-run can validate this file on a machine
# with no GPU and no llama-cpp-python: nothing here executes at import time.
import subprocess as _sp
import sys as _sys


def _pip(*a):
    return _sp.run([_sys.executable, "-m", "pip", "install", "-q", *a]).returncode


def bootstrap():
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
# ---------------------------------------------------------------------------
"""
PRECISION SWEEP 14B — WAVE 3, HEILBRONN TRIANGLE (n = 13).

Two conditions only (q4_k_m contrast rung, q2_k cliff rung), 33 lineage seeds
never sampled in any prior run, asymmetrically allocated 8/25 per §3. Protocol
otherwise IDENTICAL to the archived 14B runs (same repo, same sampling params,
generation-major order, durable logging: JSONL| console echo, per-candidate
coordinates, per-condition zip, resumable state files).

Differences vs the fresh-seed circle-packing runner:
  1. TASK: Heilbronn minimum-triangle-area, not circle packing. No grid
     attractor — a regular grid scores exactly 0 here, which self_test()
     asserts at startup because that property is the entire reason this task
     was chosen.
  2. FIXED SEED PARENT, hard-coded by literal coordinates above.
  3. Per-rung seed lists (asymmetric allocation), GENS = 15.
  4. Per-row `score_delta` (vs the FIXED seed parent) and `echo` (coordinate
     point-set equality against the lineage's RUNNING parent, order-
     insensitive, 6 dp) for the registered analyses.
  5. --dry-run mode: self_test + config print, no download, no llama_cpp.

Budget: 120 + 375 = 495 loop generations. Expected wall on T4 x2: ~6-8 h
including model downloads; the state files make the run resumable across
Kaggle's session limit.
"""

import ast
import gc
import hashlib
import itertools
import json
import math
import os
import re
import shutil
import subprocess
import time

# ----------------------------- configuration --------------------------------

REPO = "Qwen/Qwen2.5-Coder-14B-Instruct-GGUF"
PRECISIONS = [  # (label, filename, min_gpus_required)
    ("q4_k_m", "qwen2.5-coder-14b-instruct-q4_k_m.gguf", 1),
    ("q2_k",   "qwen2.5-coder-14b-instruct-q2_k.gguf",   1),
]
# 33 fresh seeds, disjoint per rung. None appears in any prior wave
# (prior: 42, 123, 456, 789, 1111, 2222, 3333, 5555, 7777, 9999).
SEEDS_BY_QUANT = {
    "q4_k_m": [3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108],
    "q2_k":   [3201, 3202, 3203, 3204, 3205, 3206, 3207, 3208, 3209,
               3210, 3211, 3212, 3213, 3214, 3215, 3216, 3217, 3218,
               3219, 3220, 3221, 3222, 3223, 3224, 3225],
}
ALL_SEEDS = SEEDS_BY_QUANT["q4_k_m"] + SEEDS_BY_QUANT["q2_k"]
GENS = 15
# Wave 3 registers NO must-differ allocation (spec §3: 120 + 375 calls only).
# The probe plumbing and prompt are retained per the adaptation spec but the
# count is 0 so the executed call budget is exactly the registered one.
MUSTDIFFER_PER_PRECISION = 0
N = 13                       # points
N_TRIPLES = 286              # C(13,3)
COORD_DP = 6                 # canonicalisation / identity precision
N_CTX = 4096
MAX_TOKENS = 1200
TEMPERATURE = 0.8
TOP_P = 0.95
RUNNER_VERSION = "14b_heilbronn_wave3_v1"

# Fixed seed parent — literal coordinates, published in the header above.
# Produced by a seeded random restart + hill climb, stopped inside a
# pre-set mediocrity band; the literals below (not the generator) are the
# registered object.
SEED_PARENT = [
    [0.223341, 0.919137],
    [0.000000, 0.000000],
    [0.192827, 0.682068],
    [0.711251, 1.000000],
    [0.938451, 0.958662],
    [1.000000, 0.014882],
    [0.661960, 0.344964],
    [0.608847, 0.147190],
    [1.000000, 0.853188],
    [0.809867, 0.345775],
    [0.345465, 0.982286],
    [0.932750, 0.557582],
    [0.660363, 0.807716],
]
SEED_PARENT_SCORE = 0.009087361292500006

WORK = "/kaggle/working/precision_sweep_14b_heilbronn"
MODELS_DIR = "/kaggle/tmp/models"
ZIP_BASE = "/kaggle/working/precision_sweep_14b_heilbronn_partial"
STATE_DIR = os.path.join(WORK, "state")
CAND_LOG = os.path.join(WORK, "candidates_precision_14b_heilbronn.jsonl")
MUSTDIFFER_LOG = os.path.join(WORK, "mustdiffer_14b_heilbronn.jsonl")
PROVENANCE = os.path.join(WORK, "provenance.json")
RESULTS = os.path.join(WORK, "results_precision_14b_heilbronn.json")

if not os.path.isdir("/kaggle"):
    WORK = os.path.abspath("./precision_sweep_14b_heilbronn")
    MODELS_DIR = os.path.abspath("./models")
    ZIP_BASE = os.path.abspath("./precision_sweep_14b_heilbronn_partial")
    STATE_DIR = os.path.join(WORK, "state")
    CAND_LOG = os.path.join(WORK, "candidates_precision_14b_heilbronn.jsonl")
    MUSTDIFFER_LOG = os.path.join(WORK, "mustdiffer_14b_heilbronn.jsonl")
    PROVENANCE = os.path.join(WORK, "provenance.json")
    RESULTS = os.path.join(WORK, "results_precision_14b_heilbronn.json")

_TRIPLES = list(itertools.combinations(range(N), 3))

# ------------------------- evaluator (mirrors harness.py) --------------------


def parse_proposal(raw):
    """Extract a list of [x, y] pairs. Viability = a list of pairs of ANY
    length; length is checked by evaluate(), not here."""
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
    """Minimum triangle area over all C(n,3) triples. Exactly 0.0 when any
    three points are collinear — the property this task was chosen for."""
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
    """viable = parsed as a list of pairs of any length.
    valid   = exactly 13 pairs, every coordinate in [0,1], no two points
              identical to 6 dp. A valid configuration may score exactly 0.0
              (collinear triple) — prediction 5.5 counts precisely those."""
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
    """Order-insensitive identity of a point set at 6 dp."""
    return frozenset((round(x, COORD_DP), round(y, COORD_DP)) for (x, y) in points)


def seed_parent():
    """The fixed parent every lineage and every rung starts from."""
    return [[x, y] for (x, y) in SEED_PARENT]


def regular_grid():
    """4x4 lattice truncated to 13 points. Coordinates .125/.375/.625/.875 are
    exactly representable in binary, so collinear rows give area EXACTLY 0.0
    and the self_test equality below is not a floating-point accident."""
    pts = []
    for row in range(4):
        for col in range(4):
            if len(pts) >= N:
                break
            pts.append((round((col + 0.5) / 4.0, COORD_DP),
                        round((row + 0.5) / 4.0, COORD_DP)))
    return pts


def self_test():
    parent = [tuple(p) for p in seed_parent()]
    ev = evaluate(parent)
    assert ev["valid"], "seed parent must be valid"
    assert abs(ev["score"] - SEED_PARENT_SCORE) < 1e-12, \
        f"seed parent score {ev['score']!r} != {SEED_PARENT_SCORE!r}"
    assert not ev["collinear"], "seed parent must be non-degenerate"
    assert len(_TRIPLES) == N_TRIPLES, "must be C(13,3) = 286 triples"

    # THE reason this task was chosen: a regular grid — the configuration the
    # circle-packing proposer reproduced verbatim at the 2-bit rung — is a
    # structurally VALID answer here that scores exactly zero.
    grid = regular_grid()
    gev = evaluate(grid)
    assert gev["valid"], "regular grid is structurally valid"
    assert gev["score"] == 0.0, f"regular grid must score exactly 0.0, got {gev['score']!r}"
    assert gev["collinear"], "grid must be flagged collinear"

    # Length, range and duplicate rules.
    assert not evaluate(parent[:12])["valid"], "12 points must be invalid"
    assert evaluate(parent[:12])["viable"], "12 points are still viable"
    oob = list(parent)
    oob[0] = (1.5, 0.5)
    assert not evaluate(oob)["valid"], "out-of-range coordinate must invalidate"
    dup = list(parent)
    dup[1] = dup[0]
    assert not evaluate(dup)["valid"], "duplicate point must invalidate"

    # Parser: pairs, not triples; any length is viable.
    p, err = parse_proposal("junk before [[0.1, 0.1], [0.2, 0.9]] junk after")
    assert err is None and len(p) == 2, "parser must extract bracketed pair list"
    assert parse_proposal("[[0.1, 0.1, 0.05]]")[0] is None, "triples must not parse"

    # Echo identity is order-insensitive at 6 dp.
    shuffled = list(reversed(parent))
    assert point_key(shuffled) == point_key(parent), "echo key must ignore order"
    print("[selftest] evaluator + parser + grid-zero property OK")


# ------------------------------ prompts --------------------------------------

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


def must_differ_prompt(best_points, best_score):
    """Identical to loop_prompt except the appended must-differ constraint —
    the single manipulated variable of the mechanism probe. Retained from the
    prior runner; wave 3 allocates zero probes (MUSTDIFFER_PER_PRECISION = 0)
    because spec §3 registers none."""
    return (
        loop_prompt(best_points, best_score) + "\n"
        "IMPORTANT: your configuration MUST NOT be identical to the current "
        "best configuration shown above. Move at least three points. "
        "Returning the same configuration again counts as failure."
    )

# ------------------------------ plumbing -------------------------------------


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


def append_jsonl(path, row):
    """Append to file AND echo to console ("JSONL|" prefix) — console echo is
    the durability layer (version history survives /kaggle/working wipes)."""
    line = json.dumps(row)
    with open(path, "a") as f:
        f.write(line + "\n")
        f.flush()
        os.fsync(f.fileno())
    print("JSONL|" + line, flush=True)


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
            "repo": REPO, "gens": GENS, "seeds_by_quant": SEEDS_BY_QUANT,
            "task": "heilbronn_triangle_n13",
            "seed_parent": SEED_PARENT,
            "seed_parent_score": SEED_PARENT_SCORE,
            "temperature": TEMPERATURE, "top_p": TOP_P,
            "runner_version": RUNNER_VERSION,
            "purpose": "wave 3 — registered loop-level primaries on a second task",
            "q8_0": "not run by design; hardware cannot serve a second GPU",
            "conditions": {}}


def save_provenance(p):
    with open(PROVENANCE, "w") as f:
        json.dump(p, f, indent=2)


def spath(quant, seed):
    return os.path.join(STATE_DIR, f"{quant}_seed_{seed}.json")


def load_state(quant, seed):
    p = spath(quant, seed)
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return {"quant": quant, "seed": seed, "gen": 0,
            "best_points": seed_parent(), "best_score": SEED_PARENT_SCORE}


def save_state(st):
    with open(spath(st["quant"], st["seed"]), "w") as f:
        json.dump(st, f)


def count_mustdiffer_done(quant):
    if not os.path.exists(MUSTDIFFER_LOG):
        return 0
    with open(MUSTDIFFER_LOG) as f:
        return sum(1 for l in f if json.loads(l)["quant"] == quant)


# --------------------------- model management --------------------------------

def download_model(fname):
    from huggingface_hub import hf_hub_download
    os.makedirs(MODELS_DIR, exist_ok=True)
    print(f"[download] {fname} ...")
    t0 = time.time()
    path = hf_hub_download(repo_id=REPO, filename=fname, local_dir=MODELS_DIR)
    print(f"[download] done in {time.time()-t0:.0f}s -> {path}")
    return path


def load_llm(path, n_gpus):
    from llama_cpp import Llama
    kwargs = dict(model_path=path, n_gpu_layers=-1, n_ctx=N_CTX, verbose=False)
    if n_gpus > 1:
        kwargs["split_mode"] = 1
    print(f"[load] {os.path.basename(path)} (gpus={n_gpus})")
    t0 = time.time()
    llm = Llama(**kwargs)
    print(f"[load] ready in {time.time()-t0:.0f}s")
    return llm


def generate(llm, prompt, seed_val):
    t0 = time.time()
    try:
        out = llm.create_chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=MAX_TOKENS, temperature=TEMPERATURE, top_p=TOP_P,
            seed=seed_val)
        text = out["choices"][0]["message"]["content"]
        usage = out.get("usage", {})
    except Exception as e:
        return None, f"gen_error: {type(e).__name__}: {e}", 0, time.time() - t0
    return text, None, usage.get("completion_tokens", 0), time.time() - t0


# ------------------------------ main sweep -----------------------------------

def run_condition(quant, fname, min_gpus, provenance):
    seeds = SEEDS_BY_QUANT[quant]
    n_gpus = len(provenance["gpus"])
    if n_gpus < min_gpus:
        print(f"[skip] {quant}: needs {min_gpus} GPU(s), have {n_gpus}")
        provenance["conditions"].setdefault(quant, {})["skipped"] = \
            f"needs {min_gpus} gpus, have {n_gpus}"
        save_provenance(provenance)
        return

    states = {s: load_state(quant, s) for s in seeds}
    md_done = count_mustdiffer_done(quant)
    loop_done = all(st["gen"] >= GENS for st in states.values())
    if loop_done and md_done >= MUSTDIFFER_PER_PRECISION:
        print(f"[done] {quant}: already complete, skipping")
        return

    path = download_model(fname)
    cond = provenance["conditions"].setdefault(quant, {})
    if "sha256" not in cond:
        print(f"[hash] {quant} ...")
        cond["sha256"] = sha256_file(path)
        cond["bytes"] = os.path.getsize(path)
        cond["filename"] = fname
        cond["lineages"] = len(seeds)
        cond["seeds"] = seeds
        save_provenance(provenance)
        print(f"[hash] {cond['sha256'][:16]}... ({cond['bytes']/1e9:.2f} GB)")

    llm = load_llm(path, n_gpus)
    try:
        # Loop candidates: generation-major order so a dead session leaves every
        # lineage at a comparable depth.
        for gen in range(GENS):
            for s in seeds:
                st = states[s]
                if st["gen"] != gen:
                    continue
                parent_pts = [tuple(p) for p in st["best_points"]]
                prompt = loop_prompt(parent_pts, st["best_score"])
                text, gerr, ctoks, wall = generate(llm, prompt, s * 1000 + gen)
                points, perr = parse_proposal(text) if gerr is None else (None, gerr)
                ev = evaluate(points)
                # Echo is measured against the RUNNING parent that was shown in
                # the prompt, before any acceptance update below.
                echo = (None if points is None
                        else point_key(points) == point_key(parent_pts))
                row = {"arm": "precision_sweep_14b_heilbronn",
                       "task": "heilbronn_triangle_n13",
                       "proposer": f"qwen2.5-coder-14b-{quant}",
                       "quant": quant, "seed": s, "gen": gen,
                       "parent_score": round(st["best_score"], 12),
                       "score": round(ev["score"], 12),
                       "score_delta": round(ev["score"] - SEED_PARENT_SCORE, 12),
                       "seed_parent_score": SEED_PARENT_SCORE,
                       "echo": echo,
                       "collinear": ev["collinear"],
                       "viable": ev["viable"], "valid": ev["valid"],
                       "n_points": ev["n"],
                       "parse_error": perr, "completion_tokens": ctoks,
                       "wall_s": round(wall, 2), "reconstructed": False,
                       "points": ([[round(x, COORD_DP), round(y, COORD_DP)]
                                   for (x, y) in points]
                                  if points is not None else None),
                       "raw": (None if points is not None
                               else (text or "")[:3000])}
                append_jsonl(CAND_LOG, row)
                if ev["valid"] and ev["score"] > st["best_score"]:
                    st["best_score"] = ev["score"]
                    st["best_points"] = [list(p) for p in points]
                st["gen"] = gen + 1
                save_state(st)
                print(f"[{quant}] seed {s} gen {gen}: score={ev['score']:.9f} "
                      f"viable={ev['viable']} valid={ev['valid']} echo={echo} "
                      f"best={st['best_score']:.9f} ({wall:.0f}s)")

        # Must-differ mechanism probes: single-shot, seed parent, explicit
        # differ demand. Zero-allocated in wave 3 (see MUSTDIFFER_PER_PRECISION).
        base = [tuple(p) for p in seed_parent()]
        for k in range(md_done, MUSTDIFFER_PER_PRECISION):
            prompt = must_differ_prompt(base, SEED_PARENT_SCORE)
            text, gerr, ctoks, wall = generate(llm, prompt, 880000 + k)
            points, perr = parse_proposal(text) if gerr is None else (None, gerr)
            ev = evaluate(points)
            append_jsonl(MUSTDIFFER_LOG, {
                "kind": "must_differ_probe", "quant": quant, "probe": k,
                "parent_score": SEED_PARENT_SCORE,
                "score": round(ev["score"], 12),
                "score_delta": round(ev["score"] - SEED_PARENT_SCORE, 12),
                "echo": (None if points is None
                         else point_key(points) == point_key(base)),
                "collinear": ev["collinear"],
                "viable": ev["viable"], "valid": ev["valid"],
                "n_points": ev["n"], "parse_error": perr,
                "completion_tokens": ctoks, "wall_s": round(wall, 2),
                "reconstructed": False,
                "points": ([[round(x, COORD_DP), round(y, COORD_DP)]
                            for (x, y) in points]
                           if points is not None else None),
                "raw": (None if points is not None else (text or "")[:3000])})
            print(f"[{quant}] must-differ {k}: score={ev['score']:.9f} "
                  f"viable={ev['viable']} valid={ev['valid']}")
    finally:
        del llm
        gc.collect()
        try:
            os.remove(path)
            print(f"[cleanup] removed {fname}")
        except OSError:
            pass
    snapshot_zip()


def summarize():
    """Descriptive only. The registered verdicts (5.1-5.6) are produced by the
    separate analysis script from the raw ledger, not here."""
    rows = [json.loads(l) for l in open(CAND_LOG)] if os.path.exists(CAND_LOG) else []
    md = [json.loads(l) for l in open(MUSTDIFFER_LOG)] if os.path.exists(MUSTDIFFER_LOG) else []
    out = {}
    for quant, _, _ in PRECISIONS:
        qr = [r for r in rows if r["quant"] == quant]
        if not qr:
            continue
        per = []
        for s in SEEDS_BY_QUANT[quant]:
            sr = sorted((r for r in qr if r["seed"] == s), key=lambda r: r["gen"])
            best = SEED_PARENT_SCORE
            accepted = 0
            for r in sr:
                if r["valid"] and r["score"] > best:
                    best = r["score"]
                    accepted += 1
            per.append({"seed": s, "best": round(best, 12), "gens": len(sr),
                        "accepted_steps": accepted,
                        "improved": best > SEED_PARENT_SCORE,
                        "viable": sum(1 for r in sr if r["viable"]),
                        "valid": sum(1 for r in sr if r["valid"]),
                        "echo": sum(1 for r in sr if r.get("echo") is True)})
        bests = [p["best"] for p in per]
        mean = sum(bests) / len(bests)
        acc = [p["accepted_steps"] for p in per]
        valid_rows = [r for r in qr if r["valid"]]
        departures = [r for r in valid_rows if r.get("echo") is False]
        qm = [p for p in md if p["quant"] == quant]
        out[quant] = {
            "lineages": len(per), "per_seed": per,
            "mean_best": round(mean, 12),
            "pop_std_best": round(math.sqrt(
                sum((b - mean) ** 2 for b in bests) / len(bests)), 12),
            "mean_accepted_steps": round(sum(acc) / len(acc), 4),
            "frac_improved": round(
                sum(1 for p in per if p["improved"]) / len(per), 4),
            "viability": f"{sum(1 for r in qr if r['viable'])}/{len(qr)}",
            "validity": f"{len(valid_rows)}/{len(qr)}",
            "echo_among_valid": (f"{sum(1 for r in valid_rows if r.get('echo') is True)}"
                                 f"/{len(valid_rows)}"),
            "departures": len(departures),
            "zero_score_among_valid": (
                f"{sum(1 for r in valid_rows if r.get('collinear'))}/{len(valid_rows)}"),
            "mustdiffer_n": len(qm),
            "mustdiffer_valid": sum(1 for p in qm if p["valid"]),
        }
    with open(RESULTS, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


def print_config():
    print(f"[config] runner_version = {RUNNER_VERSION}")
    print(f"[config] repo           = {REPO}")
    print(f"[config] task           = heilbronn_triangle_n13 "
          f"(N={N}, C(13,3)={N_TRIPLES})")
    for quant, fname, min_gpus in PRECISIONS:
        seeds = SEEDS_BY_QUANT[quant]
        print(f"[config] {quant:7s} {fname}  "
              f"lineages={len(seeds)} gens={GENS} calls={len(seeds)*GENS}")
        print(f"[config]         seeds = {seeds}")
    print(f"[config] total registered calls = "
          f"{sum(len(SEEDS_BY_QUANT[q]) * GENS for q, _, _ in PRECISIONS)}")
    print("[config] q8_0           = NOT RUN by design (no second GPU; spec sec 3)")
    print(f"[config] must-differ    = {MUSTDIFFER_PER_PRECISION} per rung "
          f"(wave 3 registers none)")
    print(f"[config] sampling       = T={TEMPERATURE} top_p={TOP_P} "
          f"max_tokens={MAX_TOKENS} n_ctx={N_CTX}")
    print(f"[config] work dir       = {WORK}")
    print("[config] seed parent:")
    for p in SEED_PARENT:
        print(f"           [{p[0]:.6f}, {p[1]:.6f}]")
    ev = evaluate([tuple(p) for p in SEED_PARENT])
    print(f"[config] seed parent score (recomputed) = {ev['score']!r}")
    print(f"[config] seed parent score (constant)   = {SEED_PARENT_SCORE!r}")
    print(f"[config] regular grid score             = "
          f"{evaluate(regular_grid())['score']!r}")


def main():
    dry = "--dry-run" in _sys.argv
    if dry:
        self_test()
        print_config()
        print("\n[dry-run] OK - no model downloaded, no GPU touched.")
        return
    bootstrap()
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(STATE_DIR, exist_ok=True)
    self_test()
    print_config()
    provenance = load_provenance()
    if not provenance["gpus"]:
        provenance["gpus"] = gpu_info()
    save_provenance(provenance)
    print(f"[gpus] {provenance['gpus'] or 'NONE DETECTED (will be very slow)'}")
    for quant, fname, min_gpus in PRECISIONS:
        print(f"\n===== condition: {quant} =====")
        run_condition(quant, fname, min_gpus, provenance)
        summarize()
    snapshot_zip()
    print("\n[done] wave 3 heilbronn sweep complete.")


if __name__ == "__main__":
    main()
