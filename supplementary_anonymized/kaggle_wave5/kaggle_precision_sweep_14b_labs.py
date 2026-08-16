#!/usr/bin/env python
# ============================================================================
# WAVE 5 — PREREGISTERED PREDICTIONS, written and pushed BEFORE this run
# executed. (Kaggle version history timestamps this code prior to execution.)
#
# Task: LABS — low-autocorrelation binary sequence, n = 32. A candidate is a
# length-32 sequence s of +1/-1. With
#     C_k = sum_{i=1}^{n-k} s_i * s_{i+k}          for k = 1..n-1
#     E   = sum_{k=1}^{n-1} C_k^2                  (the "energy")
#     F   = n^2 / (2 * E)                          (the merit factor)
# the score is F and higher is better. C_k and E are INTEGERS: the evaluator
# performs no floating-point arithmetic at all, and the only division in the
# whole construction is the final n^2 / (2E). Acceptance in the hill-climbing
# loop compares ENERGIES as integers (child accepted iff E_child < E_parent),
# so no tolerance, no epsilon and no rounding exists anywhere in this runner.
#
# WHY THIS TASK EXISTS. Waves 1-4 are circle packing (§3) and Heilbronn
# triangle (wave 3). Both place real-valued points and both score by
# floating-point geometry. A referee can read the entire 2-bit result as
# "Q2_K erodes floating-point arithmetic, and those are float-arithmetic
# tasks." LABS removes the premise: the output alphabet is {+1, -1}, the
# objective is a sum of squares of integer correlations, and a proposer that
# has lost float precision loses nothing here. If the departure collapse
# survives on LABS, the float-arithmetic reading is dead. If it does not, the
# paper's claim narrows — and §5 registers that branch in advance.
#
# SEED PARENT (fixed, identical for every lineage and every rung; chosen
# non-degenerate and deliberately MEDIOCRE — F = 3.2821 is ~41% of the merit
# factor reported for the n = 32 optimum, i.e. the lower half of what a
# competent proposer reaches, leaving headroom to climb, carrying no
# palindromic or skew-symmetric structure, and having exactly three improving
# single-spin flips so the reference rung is not started inside a local
# optimum):
#
#   [-1, -1, -1, -1,  1,  1, -1,  1, -1, -1, -1,  1, -1,  1, -1,  1,
#     1,  1,  1, -1,  1, -1,  1,  1, -1, -1, -1,  1, -1, -1,  1,  1]
#
#   SEED PARENT ENERGY = 156          (exact integer)
#   SEED PARENT SCORE  = 1024/312 = 128/39 = 3.282051282051282
#
# CALIBRATION LADDER for n = 32, so the mediocrity claim is checkable and not
# asserted (energies; LOWER is better, F = 1024/(2E)):
#   all-+1 / all--1 / either alternating phase   E = 10416   F = 0.0492
#   median single uniform random draw            E ~ 556     F ~ 0.92
#   best of 4,000 seeded random draws            E = 160     F = 3.20
#   THIS SEED PARENT                             E = 156     F = 3.28
#   best of 100,000 seeded random draws          E = 120     F = 4.27
#   300-restart steepest-descent hill climb      E =  84     F = 6.10
#   optimum reported in the LABS literature      E =  64     F = 8.00
# The literature optimum is quoted for orientation only. Nothing in self_test()
# and no clause of any decision rule below depends on it.
#
# CONDITIONS (spec §3). Same pinned ladder as wave 3, same inference stack,
# same sampling parameters, SHA-256 recorded per weight file:
#     Q4_K_M  qwen2.5-coder-14b-instruct-q4_k_m.gguf   8 lineages x 15 gens = 120
#     Q2_K    qwen2.5-coder-14b-instruct-q2_k.gguf    25 lineages x 15 gens = 375
# Asymmetric BY DESIGN and registered rather than discovered, for the same
# reason wave 3 gives: prediction 5.3 needs departures at the 2-bit rung, and
# the observed 2-bit departure rate is 2-16% of calls. At 8% of 375 calls the
# expected departure count is 30; at the symmetric allocation it would be 10,
# the count that made the earlier conditional question unanswerable.
#
# SEEDS — a published fixed list of 33 values, none used in any prior wave.
# Prior lineage seeds anywhere in this repository: 42, 123, 456, 789, 1111,
# 2222, 3333, 5555, 7777, 9999 (waves 1-2 and the dispersion probes) and
# 3101-3108 / 3201-3225 (wave 3). The 5100/5200 block below is disjoint from
# all of them, and so is its DERIVED generation-seed window: this runner draws
# with seed = lineage*1000 + gen, giving 5,101,000-5,225,014, which does not
# meet wave 3's 3,101,000-3,225,014, does not meet 5555*1000 = 5,555,000, and
# does not meet the 880,000+k must-differ window.
#     Q4_K_M (8):  5101 5102 5103 5104 5105 5106 5107 5108
#     Q2_K  (25):  5201 5202 5203 5204 5205 5206 5207 5208 5209 5210 5211
#                  5212 5213 5214 5215 5216 5217 5218 5219 5220 5221 5222
#                  5223 5224 5225
#
# Q8_0 IS NOT RUN. Both prior probe waves recorded it skipped for want of a
# second GPU, and registering a condition the hardware cannot serve is what
# produced wave 2's FAILED verdict. Its absence here is a design decision, not
# a failure, and is stated as such in advance.
#
# HARDWARE CROSSING — registered, and new in this wave. §6 item 4 of paper 2
# documents per-file throughput orderings that INVERT across hardware on
# SHA-identical weight files (P100 against 2xT4). Kaggle serves 2 x T4 at
# 15360 MiB each; Q4_K_M (8.99 GB) and Q2_K (5.77 GB) each fit one card alone.
# A runner that pinned one rung per card — or that let n_gpu_layers=-1 split
# each rung differently — would make GPU COLLINEAR WITH RUNG, which is exactly
# the confound §6 item 4 documents. So the card is alternated PER LINEAGE and
# not per rung: odd lineage seeds run on GPU 0, even lineage seeds on GPU 1,
# with split_mode = LLAMA_SPLIT_MODE_NONE and main_gpu set explicitly so no
# layer of any model ever crosses cards. Both rungs therefore appear on both
# cards (Q4_K_M 4 lineages per card, Q2_K 13 on GPU 0 and 12 on GPU 1), and
# self_test() asserts that mapping before a model is downloaded. Every ledger
# row records `device` and `device_index`.
# IF ONLY ONE GPU IS VISIBLE AT RUNTIME the runner falls back to single-card
# sequential execution — wave 3's behaviour — records
# `gpu_crossing = "single_card_fallback"` in provenance.json, and stamps every
# row with device_index 0. The crossing is CONDITIONAL ON HARDWARE and the
# preregistration says so; it is not silently degraded.
# The registered measures are unaffected either way: echo is exact sequence
# equality and the merit factor is derived from an integer energy, neither of
# which depends on which card produced the tokens. No timing-derived quantity
# is registered in this wave, exactly as in wave 3; `wall_s` remains a
# descriptive.
#
# ---------------------------------------------------------------------------
# THE REGISTERED PREDICTIONS AND DECISION RULES (spec §5, verbatim):
#
#  5.1 — PRIMARY. Echo rate. Sequence-verified parent echo among valid
#     outputs: >= 50% at Q2_K, <= 30% at Q4_K_M. Refuted if either bound is
#     violated. This is the SAME primary every wave in this paper registers;
#     no new primary is invented for the discrete task. The 2-bit bound is 5
#     points below wave 3's 55% because on LABS a single flipped symbol is a
#     complete, well-formed departure with no numeric cost, so the floor on
#     accidental departure is higher here than on a task requiring 26 fresh
#     coordinates.
#
#     CONTROL-ARM FLOOR. If the mean number of accepted hill-climb steps per
#     lineage at Q4_K_M is below 1.0 over the 15 generations, the wave's
#     verdict is UNINFORMATIVE, no branch of the outcome rule in 5.7 is
#     claimed, and the echo comparison is reported as descriptive only. LABS
#     at n = 32 is a harder search than either geometric task and this floor
#     exists so that "the reference rung could not climb either" cannot be
#     mistaken for "the rungs do not differ."
#
#  5.2 — DESCRIPTIVE. Accepted hill-climb steps per lineage, reported per
#     rung with its exact permutation tail. NO BOUND IS REGISTERED. Wave 3's
#     bounds (<= 1.5 at Q2_K, >= 4.0 at Q4_K_M) are deliberately NOT imported:
#     they were calibrated on a task with an effectively continuous score, and
#     LABS energy moves in steps of 4 (see 5.6), so importing them would set
#     up a refutation caused by task hardness and read it as evidence about
#     quantization. Registering no bound is the honest option and is stated
#     before execution rather than discovered after it.
#
#  5.3 — SECONDARY. Conditional-on-departure improvement rate. Among valid
#     non-echo outputs, the fraction with STRICTLY LOWER energy than the
#     running parent.
#     DECISION RULE, both branches informative:
#       - Q2_K rate >= 0.75 x Q4_K_M rate -> quantization gates the FREQUENCY
#         of departure and not its QUALITY.
#       - Q2_K rate <= 0.50 x Q4_K_M rate -> quality degrades too.
#       - Between -> inconclusive, reported as such.
#       - POWER FLOOR: if fewer than 25 Q2_K departures are observed, the
#         verdict is UNDERPOWERED and no branch is claimed regardless of the
#         ratio.
#
#  5.4 — Template check, the direct analogue of wave 3's grid-scores-zero
#     clause. Fraction of valid outputs equal to one of the four degenerate
#     templates — all +1, all -1, and the two alternating phases — every one
#     of which has energy exactly 10416 and merit factor 0.0492, the worst
#     value any length-32 sequence attains. Reported per rung with NO bound.
#     It exists to separate "the proposer copies its parent" from "the
#     proposer emits the default template it always emits," which circle
#     packing could not separate because the seeded parent WAS the template.
#
#  5.5 — Symmetry-variant rate, no analogue in prior waves. Negation,
#     reversal and (-1)^i modulation each leave the energy exactly unchanged,
#     so every sequence sits in an orbit of at most 8 score-tied variants.
#     Fraction of valid NON-ECHO outputs lying in the running parent's orbit:
#     reported per rung with NO bound. A degraded proposer that emits the
#     negated parent has departed by the registered definition of echo and has
#     not searched; this metric makes that visible instead of burying it.
#
#  5.6 — Outcome. Final best merit factor per lineage, permutation-tested at
#     lineage level. NO BOUND IS REGISTERED, for wave 3's reason and one more:
#     flipping a single spin changes each C_k by exactly 0 or +-2, so every
#     energy difference is a multiple of 4 and the LABS score support is
#     LUMPY in precisely the way circle packing's was. This wave therefore
#     re-inherits the defect wave 3 was built to remove, and says so here
#     rather than being caught with it later. Waves 3 and 5 are complements:
#     wave 3 buys a fine-grained score and keeps float geometry, wave 5 buys
#     integer discreteness and gives the fine grain back.
#
#  5.7 — THREE-BRANCH OUTCOME RULE. Exactly one branch is claimed, chosen by
#     the registered arithmetic below and by nothing else. Write "echo2" for
#     the Q2_K echo rate among valid outputs and "echo4" for the Q4_K_M rate.
#
#     BRANCH A — GENERALISES. Control floor met AND echo2 >= 50% AND
#       echo4 <= 30%. The departure collapse is not an artefact of
#       floating-point arithmetic: it appears on a task whose entire output
#       and objective are integer. The paper's scope sentence extends from
#       "constructive geometric search" to "constructive search," and the
#       float-erosion reading of §3 is refuted rather than argued against.
#
#     BRANCH B — NARROWS, and this branch is real. Control floor met AND
#       echo4 <= 35% AND echo2 < 50% AND (echo2 - echo4) < 15 percentage
#       points. The reference rung climbed, the 2-bit rung did not collapse
#       into copying, and the two rungs are not separated. Then the collapse
#       is a property of continuous-coordinate tasks, the float-arithmetic
#       reading of §3 stands unrefuted, and THE PAPER'S CLAIM IS NARROWED IN
#       TEXT: §3.6 and the abstract are rewritten to say the effect is
#       observed on continuous-coordinate constructive search and is ABSENT on
#       a discrete combinatorial task of the same competence class. We commit
#       to that rewrite here so the commitment predates the outcome. This is
#       not a remote possibility: 7B already inverts on circle packing, so
#       the effect is known not to be universal across the axes tested.
#
#     BRANCH C — INCONCLUSIVE. Everything else, including every case where the
#       control floor is not met, where echo4 exceeds 35% (both rungs copy,
#       which is a statement about the task and not about precision), and
#       every mixed pattern. No scope change is made in either direction and
#       the wave is reported as inconclusive with its numbers.
#
# DISCONFIRMATION (spec §6, verbatim):
#  Branch B IS the disconfirmation clause and it is stated as a rewrite, not
#  as a softening. If it fires, the sentence "quantizing the proposer to two
#  bits largely stops it departing from its parent" acquires the qualifier
#  "on continuous-coordinate constructive tasks" everywhere it appears, and
#  the referee's float-arithmetic alternative is reported in the paper as
#  live and unrefuted.
#  If 5.1 holds at Q2_K but 5.3 returns the quality-collapse branch, the
#  repairable reading of the effect fails on a discrete task even though the
#  effect itself generalises; that is reported as its own result and not
#  folded into Branch A.
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
PRECISION SWEEP 14B — WAVE 5, LOW-AUTOCORRELATION BINARY SEQUENCE (n = 32).

Two conditions only (q4_k_m contrast rung, q2_k cliff rung), 33 lineage seeds
never sampled in any prior run, asymmetrically allocated 8/25. Protocol
otherwise IDENTICAL to the archived 14B runs and to wave 3 (same repo, same
sampling params, generation-major order, durable logging: JSONL| console echo,
per-candidate output, per-condition zip, resumable state files).

Differences vs the wave-3 Heilbronn runner:
  1. TASK: LABS merit factor at n = 32, not Heilbronn triangle. The output is
     a length-32 sequence of +1/-1 and the objective is a sum of squares of
     integer autocorrelations. No floating-point arithmetic occurs anywhere in
     the construction or the evaluation; the single division producing the
     merit factor is the only non-integer operation in the file.
  2. FIXED SEED PARENT, hard-coded by literal symbols above, with its exact
     integer energy 156 and its merit factor 128/39.
  3. ECHO IS EXACT SEQUENCE EQUALITY against the lineage's RUNNING parent.
     Because the alphabet is discrete there is no tolerance parameter and no
     rounding step: two sequences are either the same list of 32 integers or
     they are not. Waves 1-4 had to canonicalise coordinates to 6 dp before
     comparing point sets and therefore carried a rounding convention inside
     their primary; this wave's primary carries none. That is the single
     largest methodological advantage of moving to a discrete task.
  4. Per-row `score_delta` (merit factor vs the FIXED seed parent),
     `energy_delta` (integer, vs the fixed seed parent), `template` (one of
     the four degenerate sequences) and `symmetry_variant` (in the running
     parent's 8-element score-tied orbit) for the registered analyses.
  5. GPU CROSSED WITH RUNG, not nested in it. Card alternates per LINEAGE
     (odd seed -> GPU 0, even seed -> GPU 1) with split_mode = NONE and
     main_gpu pinned, so no model is ever split across cards and both rungs
     appear on both cards. `device` and `device_index` are logged per row.
     Single-visible-GPU hosts fall back to sequential single-card execution
     and record that fact in provenance.json.
  6. --dry-run mode: self_test + config print, no download, no llama_cpp,
     no directories created.

Budget: 120 + 375 = 495 loop generations. Expected wall on T4 x2: ~6-8 h
including model downloads; the state files make the run resumable across
Kaggle's session limit.
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
PRECISIONS = [  # (label, filename, min_gpus_required)
    ("q4_k_m", "qwen2.5-coder-14b-instruct-q4_k_m.gguf", 1),
    ("q2_k",   "qwen2.5-coder-14b-instruct-q2_k.gguf",   1),
]
# 33 fresh seeds, disjoint per rung. None appears in any prior wave (prior:
# 42, 123, 456, 789, 1111, 2222, 3333, 5555, 7777, 9999 and wave 3's
# 3101-3108 / 3201-3225). See the header for the derived-seed disjointness.
SEEDS_BY_QUANT = {
    "q4_k_m": [5101, 5102, 5103, 5104, 5105, 5106, 5107, 5108],
    "q2_k":   [5201, 5202, 5203, 5204, 5205, 5206, 5207, 5208, 5209,
               5210, 5211, 5212, 5213, 5214, 5215, 5216, 5217, 5218,
               5219, 5220, 5221, 5222, 5223, 5224, 5225],
}
ALL_SEEDS = SEEDS_BY_QUANT["q4_k_m"] + SEEDS_BY_QUANT["q2_k"]
GENS = 15
# Wave 5 registers NO must-differ allocation (120 + 375 calls only). The probe
# plumbing and prompt are retained for parity with wave 3 but the count is 0 so
# the executed call budget is exactly the registered one.
MUSTDIFFER_PER_PRECISION = 0
N = 32                       # sequence length
N_CTX = 4096
MAX_TOKENS = 1200
TEMPERATURE = 0.8
TOP_P = 0.95
RUNNER_VERSION = "14b_labs_wave5_v1"

# Fixed seed parent — literal symbols, published in the header above. Produced
# by a seeded random restart plus a truncated integer hill climb, stopped
# inside a pre-set mediocrity band and filtered for: no palindromic or
# skew-symmetric structure, longest run <= 4, |sum| <= 4, and at least three
# improving single-spin flips. The literals below (not the generator) are the
# registered object.
SEED_PARENT = [-1, -1, -1, -1, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1, -1, 1,
               1, 1, 1, -1, 1, -1, 1, 1, -1, -1, -1, 1, -1, -1, 1, 1]
SEED_PARENT_ENERGY = 156                        # exact integer
SEED_PARENT_SCORE = 3.282051282051282           # = 1024 / 312 = 128 / 39

# The four degenerate templates. Each has energy exactly 10416 — the maximum
# attainable at n = 32 — and merit factor 1024/20832 = 0.049155...
CONSTANT_ENERGY = 10416

WORK = "/kaggle/working/precision_sweep_14b_labs"
MODELS_DIR = "/kaggle/tmp/models"
ZIP_BASE = "/kaggle/working/precision_sweep_14b_labs_partial"
STATE_DIR = os.path.join(WORK, "state")
CAND_LOG = os.path.join(WORK, "candidates_precision_14b_labs.jsonl")
MUSTDIFFER_LOG = os.path.join(WORK, "mustdiffer_14b_labs.jsonl")
PROVENANCE = os.path.join(WORK, "provenance.json")
RESULTS = os.path.join(WORK, "results_precision_14b_labs.json")

if not os.path.isdir("/kaggle"):
    WORK = os.path.abspath("./precision_sweep_14b_labs")
    MODELS_DIR = os.path.abspath("./models")
    ZIP_BASE = os.path.abspath("./precision_sweep_14b_labs_partial")
    STATE_DIR = os.path.join(WORK, "state")
    CAND_LOG = os.path.join(WORK, "candidates_precision_14b_labs.jsonl")
    MUSTDIFFER_LOG = os.path.join(WORK, "mustdiffer_14b_labs.jsonl")
    PROVENANCE = os.path.join(WORK, "provenance.json")
    RESULTS = os.path.join(WORK, "results_precision_14b_labs.json")

# ------------------------- evaluator (exact integers) ------------------------


def parse_proposal(raw):
    """Extract a list of +1/-1 symbols. Viability = a list of numbers of ANY
    length; length and alphabet are checked by evaluate(), not here.

    Accepts ints and floats that are exactly +-1 (a model may emit 1.0). The
    float is compared for exact equality and then cast, which is a conversion
    and not arithmetic — no rounding and no tolerance enters the evaluator.
    Booleans are rejected explicitly because bool is a subclass of int in
    Python and True would otherwise silently read as +1."""
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
    except (ValueError, SyntaxError, MemoryError, RecursionError) as e:
        return None, f"literal_eval: {type(e).__name__}"
    if not isinstance(obj, (list, tuple)):
        return None, "not_a_list"
    seq = []
    for item in obj:
        if isinstance(item, bool):
            return None, "boolean_symbol"
        if isinstance(item, int):
            seq.append(int(item))
        elif isinstance(item, float):
            if item != 1.0 and item != -1.0:
                return None, "non_unit_float"
            seq.append(int(item))
        else:
            return None, "non_numeric"
    return seq, None


def autocorrelations(s):
    """C_k for k = 1..n-1. Every term is a product of +-1 and every sum is an
    integer; there is no floating-point operation in this function."""
    n = len(s)
    out = []
    for k in range(1, n):
        c = 0
        for i in range(n - k):
            c += s[i] * s[i + k]
        out.append(c)
    return out


def energy(s):
    """E = sum_k C_k^2. Exact integer. Minimum attainable is bounded below by
    1 because C_{n-1} = s_1 * s_n = +-1 is never zero, so the merit factor
    below never divides by zero."""
    return sum(c * c for c in autocorrelations(s))


def merit_factor(e):
    """F = n^2 / (2E). The ONLY division in the construction."""
    return (N * N) / (2 * e)


def is_template(s):
    """The four degenerate sequences: all +1, all -1, and both alternating
    phases. Each has energy exactly CONSTANT_ENERGY."""
    if len(s) < 2:
        return False
    if all(v == s[0] for v in s):
        return True
    return all(s[i] != s[i - 1] for i in range(1, len(s)))


def symmetry_orbit(s):
    """Negation, reversal and (-1)^i modulation each preserve E exactly, so a
    sequence sits in an orbit of at most 8 score-tied variants. Used only for
    the descriptive in 5.5; the registered echo test is plain equality."""
    n = len(s)
    orbit = set()
    for base in (tuple(s), tuple(reversed(s))):
        for neg in (1, -1):
            for mod in (0, 1):
                orbit.add(tuple(neg * base[i] * ((-1) ** (i * mod))
                                for i in range(n)))
    return orbit


def evaluate(seq):
    """viable = parsed as a list of numbers of any length.
    valid   = exactly 32 symbols, every one of them +1 or -1.
    A valid sequence may be a degenerate template scoring 0.0492 — prediction
    5.4 counts precisely those."""
    res = {"viable": False, "valid": False, "energy": None, "score": 0.0,
           "template": False, "n": 0 if seq is None else len(seq)}
    if seq is None:
        return res
    res["viable"] = True
    if len(seq) != N:
        return res
    if any(v != 1 and v != -1 for v in seq):
        return res
    res["valid"] = True
    res["energy"] = energy(seq)
    res["score"] = merit_factor(res["energy"])
    res["template"] = is_template(seq)
    return res


def seed_parent():
    """The fixed parent every lineage and every rung starts from."""
    return list(SEED_PARENT)


# --------------------------- hardware assignment -----------------------------

def assign_device(seed, n_devices):
    """Which card a LINEAGE runs on. Odd lineage seed -> GPU 0, even -> GPU 1.

    The assignment is by lineage and never by rung, so GPU is CROSSED with the
    quantization rung instead of nested inside it. Paper 2 §6 item 4 records
    per-file throughput orderings that invert across hardware on SHA-identical
    weight files; pinning one rung per card would reproduce exactly that
    confound in the wave that is supposed to settle a different question.

    With fewer than two visible devices every lineage returns 0 and the run is
    single-card sequential — wave 3's behaviour — which run_condition records
    in provenance as `gpu_crossing = "single_card_fallback"`."""
    if n_devices < 2:
        return 0
    return 0 if (seed % 2 == 1) else 1


def device_plan(n_devices):
    """{quant: {device_index: [seeds]}} for the given visible-device count."""
    plan = {}
    for quant, seeds in SEEDS_BY_QUANT.items():
        per = {}
        for s in seeds:
            per.setdefault(assign_device(s, n_devices), []).append(s)
        plan[quant] = per
    return plan


def self_test():
    # (a) Hand-computed cases, derived by hand and reproduced here so a reader
    #     can check the evaluator without running anything.
    #
    #     n = 3, s = [1, 1, -1]:
    #       C_1 = s1s2 + s2s3 = 1 + (-1) = 0
    #       C_2 = s1s3        = -1
    #       E   = 0^2 + (-1)^2 = 1 ;  F = 9 / 2 = 4.5
    assert autocorrelations([1, 1, -1]) == [0, -1], "n=3 autocorrelations"
    assert energy([1, 1, -1]) == 1, "n=3 energy must be 1"
    assert (3 * 3) / (2 * energy([1, 1, -1])) == 4.5, "n=3 merit factor 4.5"
    #
    #     n = 4, s = [1, 1, -1, 1]:
    #       C_1 = 1*1 + 1*(-1) + (-1)*1 = -1
    #       C_2 = 1*(-1) + 1*1          =  0
    #       C_3 = 1*1                   =  1
    #       E   = 1 + 0 + 1 = 2 ;  F = 16 / 4 = 4.0
    assert autocorrelations([1, 1, -1, 1]) == [-1, 0, 1], "n=4 autocorrelations"
    assert energy([1, 1, -1, 1]) == 2, "n=4 energy must be 2"
    assert (4 * 4) / (2 * energy([1, 1, -1, 1])) == 4.0, "n=4 merit factor 4.0"
    #
    #     n = 5, s = [1, 1, 1, -1, 1] (the length-5 Barker sequence):
    #       C_1 = 1 + 1 - 1 - 1 = 0
    #       C_2 = 1 - 1 + 1     = 1
    #       C_3 = -1 + 1        = 0
    #       C_4 = 1             = 1
    #       E   = 0 + 1 + 0 + 1 = 2 ;  F = 25 / 4 = 6.25
    assert autocorrelations([1, 1, 1, -1, 1]) == [0, 1, 0, 1], "n=5 autocorrelations"
    assert energy([1, 1, 1, -1, 1]) == 2, "n=5 energy must be 2"
    assert (5 * 5) / (2 * energy([1, 1, 1, -1, 1])) == 6.25, "n=5 merit factor 6.25"

    # (b) THE reason this task was chosen. The constant sequence — the discrete
    #     analogue of the regular grid that the circle-packing proposer emitted
    #     verbatim at the 2-bit rung — is a structurally VALID answer that
    #     scores the WORST value any length-32 sequence can attain. For all-+1,
    #     C_k = n - k, so E = sum_{j=1}^{31} j^2 = 31*32*63/6 = 10416 exactly.
    #     Negating or alternating leaves |C_k| unchanged, so all four degenerate
    #     templates tie at that value. A template-emitting proposer is therefore
    #     visible immediately and cannot be confused with a parent-copying one.
    assert sum(j * j for j in range(1, N)) == CONSTANT_ENERGY, \
        "closed form for the constant sequence must be 10416"
    for tpl in ([1] * N, [-1] * N,
                [(-1) ** i for i in range(N)],
                [-((-1) ** i) for i in range(N)]):
        ev = evaluate(tpl)
        assert ev["valid"], "degenerate template must still be structurally valid"
        assert ev["energy"] == CONSTANT_ENERGY, \
            f"template energy {ev['energy']!r} != {CONSTANT_ENERGY}"
        assert ev["template"], "template must be flagged"
        assert abs(ev["score"] - (N * N) / (2 * CONSTANT_ENERGY)) < 1e-15, \
            "template merit factor"
    assert abs((N * N) / (2 * CONSTANT_ENERGY) - 0.04915514592933948) < 1e-15, \
        "template merit factor literal"

    # (c) Seed parent against its hard-coded literals.
    parent = seed_parent()
    pev = evaluate(parent)
    assert pev["valid"], "seed parent must be valid"
    assert pev["energy"] == SEED_PARENT_ENERGY, \
        f"seed parent energy {pev['energy']!r} != {SEED_PARENT_ENERGY!r}"
    assert abs(pev["score"] - SEED_PARENT_SCORE) < 1e-12, \
        f"seed parent score {pev['score']!r} != {SEED_PARENT_SCORE!r}"
    assert not pev["template"], "seed parent must not be a degenerate template"
    assert pev["energy"] < CONSTANT_ENERGY, "seed parent must beat the template"
    # Registered non-degeneracy of the parent, checked rather than asserted in
    # prose: it is neither a palindrome nor skew-symmetric, and at least three
    # single-spin flips strictly improve it, so the reference rung does not
    # start inside a local optimum.
    assert parent != parent[::-1], "seed parent must not be palindromic"
    assert parent != [-v for v in reversed(parent)], "seed parent must not be skew-symmetric"
    improving = [i for i in range(N)
                 if energy([-v if j == i else v for j, v in enumerate(parent)])
                 < SEED_PARENT_ENERGY]
    assert len(improving) >= 3, \
        f"seed parent must have >= 3 improving flips, has {len(improving)}"

    # Length and alphabet rules.
    assert not evaluate(parent[:31])["valid"], "31 symbols must be invalid"
    assert evaluate(parent[:31])["viable"], "31 symbols are still viable"
    bad = list(parent)
    bad[0] = 0
    assert not evaluate(bad)["valid"], "a 0 symbol must invalidate"
    bad[0] = 2
    assert not evaluate(bad)["valid"], "a 2 symbol must invalidate"

    # Parser: brackets, floats that are exactly +-1, and the bool trap.
    p, err = parse_proposal("junk before [1, -1, 1, -1] junk after")
    assert err is None and p == [1, -1, 1, -1], "parser must extract bracketed list"
    assert parse_proposal("[1.0, -1.0]")[0] == [1, -1], "exact unit floats accepted"
    assert parse_proposal("[0.5, -1]")[0] is None, "non-unit float must not parse"
    assert parse_proposal("[True, False]")[0] is None, "booleans must not parse"

    # Echo identity is EXACT sequence equality. Discrete alphabet, so order
    # matters and no rounding convention exists: reversing the parent is a
    # different sequence even though it has the same energy.
    assert list(reversed(parent)) != parent, "reversal must be a distinct sequence"
    assert energy(list(reversed(parent))) == SEED_PARENT_ENERGY, \
        "reversal is score-tied — this is why 5.5 exists"
    orbit = symmetry_orbit(parent)
    assert len(orbit) == 8, f"symmetry orbit must have 8 members, has {len(orbit)}"
    assert all(energy(list(v)) == SEED_PARENT_ENERGY for v in orbit), \
        "every orbit member must be score-tied"

    # (d) Hardware crossing. On a two-card host BOTH rungs must appear on BOTH
    #     cards, or GPU becomes collinear with rung and §6 item 4's inversion
    #     confound is reproduced inside the wave meant to remove a confound.
    plan2 = device_plan(2)
    for quant in SEEDS_BY_QUANT:
        assert set(plan2[quant]) == {0, 1}, \
            f"{quant} must be assigned to BOTH cards, got {sorted(plan2[quant])}"
        for dev in (0, 1):
            assert len(plan2[quant][dev]) >= 1, \
                f"{quant} has no lineage on GPU {dev}"
    # Every lineage lands on exactly one card and no lineage is lost.
    for quant, seeds in SEEDS_BY_QUANT.items():
        flat = sorted(s for d in plan2[quant] for s in plan2[quant][d])
        assert flat == sorted(seeds), f"{quant} device plan must partition its seeds"
    # Single-card fallback collapses to GPU 0 and loses no lineage.
    plan1 = device_plan(1)
    for quant, seeds in SEEDS_BY_QUANT.items():
        assert set(plan1[quant]) == {0}, "single-card fallback must use GPU 0 only"
        assert sorted(plan1[quant][0]) == sorted(seeds), \
            "single-card fallback must keep every lineage"

    print("[selftest] evaluator + parser + template-worst-value property OK")
    print("[selftest] GPU crossing: both rungs mapped onto both cards OK")


# ------------------------------ prompts --------------------------------------

def loop_prompt(best_seq, best_energy, best_score):
    config = json.dumps(list(best_seq))
    return (
        "You are the proposal step of an evolutionary search for "
        "low-autocorrelation binary sequences (the LABS problem).\n"
        f"Current best sequence (energy E = {best_energy}, merit factor "
        f"F = {best_score:.6f}):\n"
        f"{config}\n\n"
        f"Produce a sequence of exactly {N} values, each either 1 or -1, with a "
        "LARGER merit factor.\n"
        "The merit factor of a sequence s is F = n^2 / (2E), where "
        "E = sum over k = 1..n-1 of C_k^2 and "
        "C_k = sum over i = 1..n-k of s_i * s_(i+k). "
        "Maximising F means making every aperiodic autocorrelation C_k as "
        "close to zero as possible.\n"
        f"MUST hold: exactly {N} values; every value is 1 or -1. Avoid the "
        "constant sequence and the strictly alternating sequence — both give "
        "the worst possible merit factor.\n"
        f"Output ONLY the raw Python list of {N} values. No explanation, no "
        "code fences, no other text."
    )


def must_differ_prompt(best_seq, best_energy, best_score):
    """Identical to loop_prompt except the appended must-differ constraint —
    the single manipulated variable of the mechanism probe. Retained from the
    prior runner; wave 5 allocates zero probes (MUSTDIFFER_PER_PRECISION = 0)
    because the spec registers none."""
    return (
        loop_prompt(best_seq, best_energy, best_score) + "\n"
        "IMPORTANT: your sequence MUST NOT be identical to the current best "
        "sequence shown above. Change at least three positions. Returning the "
        "same sequence again counts as failure."
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
            "task": "labs_n32",
            "seed_parent": SEED_PARENT,
            "seed_parent_energy": SEED_PARENT_ENERGY,
            "seed_parent_score": SEED_PARENT_SCORE,
            "temperature": TEMPERATURE, "top_p": TOP_P,
            "runner_version": RUNNER_VERSION,
            "purpose": "wave 5 — registered echo primary on a DISCRETE task",
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
            "best_seq": seed_parent(),
            "best_energy": SEED_PARENT_ENERGY,
            "best_score": SEED_PARENT_SCORE}


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


def load_llm(path, device_index, n_gpus):
    """Load one instance PINNED to a single card.

    split_mode = 0 is LLAMA_SPLIT_MODE_NONE: the whole model goes on
    `main_gpu` and no layer crosses cards. Both rungs fit one 15360 MiB T4
    alone (Q4_K_M 8.99 GB, Q2_K 5.77 GB), so pinning costs nothing and buys
    a clean device label per row. With a single visible card this reduces to
    main_gpu = 0, which is wave 3's configuration."""
    from llama_cpp import Llama
    kwargs = dict(model_path=path, n_gpu_layers=-1, n_ctx=N_CTX, verbose=False)
    if n_gpus > 1:
        kwargs["split_mode"] = 0        # LLAMA_SPLIT_MODE_NONE
        kwargs["main_gpu"] = device_index
    print(f"[load] {os.path.basename(path)} -> GPU {device_index} "
          f"(visible={n_gpus}, pinned={n_gpus > 1})")
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

    # One pinned instance per visible card, so a lineage's card is fixed by
    # assign_device() and never by which rung it belongs to.
    devices = sorted(device_plan(n_gpus)[quant])
    gpu_names = provenance["gpus"]
    cond["device_plan"] = {str(d): device_plan(n_gpus)[quant][d] for d in devices}
    cond["gpu_crossing"] = ("lineage_alternating" if n_gpus > 1
                            else "single_card_fallback")
    provenance["gpu_crossing"] = cond["gpu_crossing"]
    save_provenance(provenance)
    print(f"[plan] {quant}: " + "; ".join(
        f"GPU {d} <- {len(cond['device_plan'][str(d)])} lineages" for d in devices))

    llms = {d: load_llm(path, d, n_gpus) for d in devices}
    try:
        # Loop candidates: generation-major order so a dead session leaves every
        # lineage at a comparable depth.
        for gen in range(GENS):
            for s in seeds:
                st = states[s]
                if st["gen"] != gen:
                    continue
                dev = assign_device(s, n_gpus)
                parent_seq = list(st["best_seq"])
                parent_orbit = symmetry_orbit(parent_seq)
                prompt = loop_prompt(parent_seq, st["best_energy"],
                                     st["best_score"])
                text, gerr, ctoks, wall = generate(llms[dev], prompt,
                                                   s * 1000 + gen)
                seq, perr = parse_proposal(text) if gerr is None else (None, gerr)
                ev = evaluate(seq)
                # ECHO. Exact list equality against the RUNNING parent that was
                # shown in the prompt, evaluated before the acceptance update
                # below. The alphabet is discrete, so this comparison has no
                # tolerance and no rounding step — unlike the 6 dp point-set
                # keys the circle-packing and Heilbronn waves had to use, this
                # primary carries no numerical convention at all.
                echo = None if seq is None else (seq == parent_seq)
                sym = (None if not ev["valid"]
                       else (tuple(seq) in parent_orbit and seq != parent_seq))
                row = {"arm": "precision_sweep_14b_labs",
                       "task": "labs_n32",
                       "proposer": f"qwen2.5-coder-14b-{quant}",
                       "quant": quant, "seed": s, "gen": gen,
                       # Hardware, recorded per row so the crossing is auditable
                       # from the ledger alone and not only from provenance.
                       "device_index": dev,
                       "device": (gpu_names[dev] if dev < len(gpu_names)
                                  else "unknown"),
                       "gpu_crossing": cond["gpu_crossing"],
                       "parent_energy": st["best_energy"],
                       "parent_score": round(st["best_score"], 12),
                       "energy": ev["energy"],
                       "score": round(ev["score"], 12),
                       "energy_delta": (None if ev["energy"] is None
                                        else ev["energy"] - SEED_PARENT_ENERGY),
                       "score_delta": round(ev["score"] - SEED_PARENT_SCORE, 12),
                       "seed_parent_energy": SEED_PARENT_ENERGY,
                       "seed_parent_score": SEED_PARENT_SCORE,
                       "echo": echo,
                       "symmetry_variant": sym,
                       "template": ev["template"],
                       "viable": ev["viable"], "valid": ev["valid"],
                       "n_symbols": ev["n"],
                       "parse_error": perr, "completion_tokens": ctoks,
                       "wall_s": round(wall, 2), "reconstructed": False,
                       "sequence": (list(seq) if seq is not None else None),
                       "raw": (None if seq is not None
                               else (text or "")[:3000])}
                append_jsonl(CAND_LOG, row)
                # Acceptance is an EXACT INTEGER comparison on energies. There
                # is no epsilon anywhere in this branch.
                if ev["valid"] and ev["energy"] < st["best_energy"]:
                    st["best_energy"] = ev["energy"]
                    st["best_score"] = ev["score"]
                    st["best_seq"] = list(seq)
                st["gen"] = gen + 1
                save_state(st)
                print(f"[{quant}] seed {s} gen {gen} gpu{dev}: "
                      f"E={ev['energy']} F={ev['score']:.6f} "
                      f"viable={ev['viable']} valid={ev['valid']} echo={echo} "
                      f"tpl={ev['template']} best_E={st['best_energy']} "
                      f"({wall:.0f}s)")

        # Must-differ mechanism probes: single-shot, seed parent, explicit
        # differ demand. Zero-allocated in wave 5 (MUSTDIFFER_PER_PRECISION).
        base = seed_parent()
        base_orbit = symmetry_orbit(base)
        for k in range(md_done, MUSTDIFFER_PER_PRECISION):
            dev = devices[k % len(devices)]
            prompt = must_differ_prompt(base, SEED_PARENT_ENERGY,
                                        SEED_PARENT_SCORE)
            text, gerr, ctoks, wall = generate(llms[dev], prompt, 880000 + k)
            seq, perr = parse_proposal(text) if gerr is None else (None, gerr)
            ev = evaluate(seq)
            append_jsonl(MUSTDIFFER_LOG, {
                "kind": "must_differ_probe", "quant": quant, "probe": k,
                "device_index": dev,
                "device": (gpu_names[dev] if dev < len(gpu_names) else "unknown"),
                "gpu_crossing": cond["gpu_crossing"],
                "parent_energy": SEED_PARENT_ENERGY,
                "parent_score": SEED_PARENT_SCORE,
                "energy": ev["energy"],
                "score": round(ev["score"], 12),
                "energy_delta": (None if ev["energy"] is None
                                 else ev["energy"] - SEED_PARENT_ENERGY),
                "score_delta": round(ev["score"] - SEED_PARENT_SCORE, 12),
                "echo": (None if seq is None else seq == base),
                "symmetry_variant": (None if not ev["valid"]
                                     else (tuple(seq) in base_orbit
                                           and seq != base)),
                "template": ev["template"],
                "viable": ev["viable"], "valid": ev["valid"],
                "n_symbols": ev["n"], "parse_error": perr,
                "completion_tokens": ctoks, "wall_s": round(wall, 2),
                "reconstructed": False,
                "sequence": (list(seq) if seq is not None else None),
                "raw": (None if seq is not None else (text or "")[:3000])})
            print(f"[{quant}] must-differ {k} gpu{dev}: E={ev['energy']} "
                  f"viable={ev['viable']} valid={ev['valid']}")
    finally:
        for d in list(llms):
            del llms[d]
        del llms
        gc.collect()
        try:
            os.remove(path)
            print(f"[cleanup] removed {fname}")
        except OSError:
            pass
    snapshot_zip()


def summarize():
    """Descriptive only. The registered verdicts (5.1-5.7) are produced by the
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
            best_e = SEED_PARENT_ENERGY
            accepted = 0
            for r in sr:
                if r["valid"] and r["energy"] < best_e:
                    best_e = r["energy"]
                    accepted += 1
            per.append({"seed": s, "best_energy": best_e,
                        "best_score": round(merit_factor(best_e), 12),
                        "gens": len(sr), "accepted_steps": accepted,
                        "improved": best_e < SEED_PARENT_ENERGY,
                        "viable": sum(1 for r in sr if r["viable"]),
                        "valid": sum(1 for r in sr if r["valid"]),
                        "echo": sum(1 for r in sr if r.get("echo") is True)})
        bests = [p["best_score"] for p in per]
        mean = sum(bests) / len(bests)
        acc = [p["accepted_steps"] for p in per]
        valid_rows = [r for r in qr if r["valid"]]
        departures = [r for r in valid_rows if r.get("echo") is False]
        improving_dep = [r for r in departures
                         if r["energy"] < r["parent_energy"]]
        qm = [p for p in md if p["quant"] == quant]
        out[quant] = {
            "lineages": len(per), "per_seed": per,
            "mean_best_score": round(mean, 12),
            "pop_std_best_score": round(math.sqrt(
                sum((b - mean) ** 2 for b in bests) / len(bests)), 12),
            "mean_accepted_steps": round(sum(acc) / len(acc), 4),
            "frac_improved": round(
                sum(1 for p in per if p["improved"]) / len(per), 4),
            "viability": f"{sum(1 for r in qr if r['viable'])}/{len(qr)}",
            "validity": f"{len(valid_rows)}/{len(qr)}",
            "echo_among_valid": (f"{sum(1 for r in valid_rows if r.get('echo') is True)}"
                                 f"/{len(valid_rows)}"),
            "departures": len(departures),
            "improving_departures": len(improving_dep),
            "template_among_valid": (
                f"{sum(1 for r in valid_rows if r.get('template'))}/{len(valid_rows)}"),
            "symmetry_variant_among_departures": (
                f"{sum(1 for r in departures if r.get('symmetry_variant'))}"
                f"/{len(departures)}"),
            "echo_by_device": {
                str(d): (f"{sum(1 for r in valid_rows if r.get('device_index') == d and r.get('echo') is True)}"
                         f"/{sum(1 for r in valid_rows if r.get('device_index') == d)}")
                for d in sorted({r.get("device_index") for r in qr
                                 if r.get("device_index") is not None})},
            "mustdiffer_n": len(qm),
            "mustdiffer_valid": sum(1 for p in qm if p["valid"]),
        }
    with open(RESULTS, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


def print_config():
    print(f"[config] runner_version = {RUNNER_VERSION}")
    print(f"[config] repo           = {REPO}")
    print(f"[config] task           = labs_n32 (N={N}, integer objective)")
    for quant, fname, min_gpus in PRECISIONS:
        seeds = SEEDS_BY_QUANT[quant]
        print(f"[config] {quant:7s} {fname}  "
              f"lineages={len(seeds)} gens={GENS} calls={len(seeds)*GENS}")
        print(f"[config]         seeds = {seeds}")
    print(f"[config] total registered calls = "
          f"{sum(len(SEEDS_BY_QUANT[q]) * GENS for q, _, _ in PRECISIONS)}")
    print("[config] q8_0           = NOT RUN by design (no second GPU)")
    print(f"[config] must-differ    = {MUSTDIFFER_PER_PRECISION} per rung "
          f"(wave 5 registers none)")
    print(f"[config] sampling       = T={TEMPERATURE} top_p={TOP_P} "
          f"max_tokens={MAX_TOKENS} n_ctx={N_CTX}")
    print(f"[config] work dir       = {WORK}")
    print(f"[config] seed parent    = {SEED_PARENT}")
    ev = evaluate(seed_parent())
    print(f"[config] seed parent energy (recomputed) = {ev['energy']!r}")
    print(f"[config] seed parent energy (constant)   = {SEED_PARENT_ENERGY!r}")
    print(f"[config] seed parent score  (recomputed) = {ev['score']!r}")
    print(f"[config] seed parent score  (constant)   = {SEED_PARENT_SCORE!r}")
    print(f"[config] constant-sequence energy        = "
          f"{evaluate([1]*N)['energy']!r}  (worst attainable)")
    print(f"[config] constant-sequence score         = "
          f"{evaluate([1]*N)['score']!r}")
    print(f"[config] alternating-sequence energy     = "
          f"{evaluate([(-1)**i for i in range(N)])['energy']!r}")
    print(f"[config] echo test       = EXACT sequence equality (no tolerance)")
    plan2 = device_plan(2)
    print("[config] gpu crossing   = lineage-alternating (odd seed -> GPU 0, "
          "even seed -> GPU 1), split_mode=NONE, main_gpu pinned")
    for quant in SEEDS_BY_QUANT:
        print(f"[config]   {quant:7s} planned on 2 cards: " + ", ".join(
            f"GPU {d}: {len(plan2[quant][d])} lineages" for d in sorted(plan2[quant])))
    print("[config] fallback       = 1 visible GPU -> all lineages on GPU 0, "
          "recorded as gpu_crossing=single_card_fallback")
    print("[config] timing         = wall_s is DESCRIPTIVE; no timing-derived "
          "quantity is registered (as in wave 3)")


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
    print("\n[done] wave 5 LABS sweep complete.")


if __name__ == "__main__":
    main()
