#!/usr/bin/env python
# ============================================================================
# RE-EXECUTION DETERMINISM RE-TEST (external, self-contained) — paper 2 §3.4/§5.9
#
# Claim under test: "llama.cpp's seeded sampling is deterministic on fixed
# weights and hardware, so it regenerates the same 224 outcomes rather than
# drawing fresh ones" (paper2_draft.md, re-execution paragraph). This kernel
# re-runs the pinned configuration of the 14B v2 durable rerun
# (runner_version 14b_v2_durable, original run 2026-07-18 on Kaggle T4 x2)
# for the two cliff-endpoint rungs Q4_K_M and Q2_K — 112 of the 224
# generations (2 rungs x (5 seeds x 10 gens + 6 probes)) — and compares each
# regenerated output against SHA-256 digests embedded below.
#
# SELF-CONTAINED BY CONSTRUCTION: this kernel downloads NOTHING from the
# research repo. The expected digests were computed at build time from the
# vendored ledger sec3_artifacts/precision_sweep_14b_v2_output/
# precision_sweep_14b/{candidates,probes}_precision_14b.jsonl and hard-coded
# here. Comparison is byte-level over a canonical serialization.
#
# DIGEST CANONICALIZATION (a documented deviation from "raw output string"):
# the v2 ledger stores the raw model text ONLY when parsing failed (candidates
# truncate raw to 3000 chars; probes always store raw, truncated to 4000).
# For successfully parsed candidate rows the ledger kept the parsed circles
# (rounded to 6 dp) and discarded the raw text, so a raw-text digest is not
# computable from the artifact. The digest is therefore over the canonical
# JSON of exactly what the ledger preserved, reproduced here with the
# identical parser, rounding and truncation:
#   candidate row: sha256(json.dumps({"circles": C, "parse_error": E,
#                  "raw": R}, sort_keys=True, separators=(",", ":")))
#     where C = [[round(x,6),round(y,6),round(r,6)], ...] or None,
#           R = None if parsed else (text or "")[:3000]
#   probe row:     sha256(json.dumps({"parse_error": E, "raw": R}, ...))
#     where R = (text or "")[:4000]
# A candidate digest match still pins the output to coordinate-level identity
# at 6-dp resolution (or byte identity of the first 3000 raw chars on parse
# failure); it is weaker than full-raw-byte identity only in discarded
# whitespace/fencing of successfully parsed outputs.
#
# PINNED STACK, WITH ONE UNRECOVERABLE PIN: weights are pinned by repo +
# filename + SHA-256 (verified after download; mismatch => VOID_WEIGHTS).
# Seeds, prompts, sampling params, context size and generation order are
# byte-identical to kaggle_precision_sweep_14b_v2_pushed.py. The original
# llama-cpp-python build, however, is UNRECOVERABLE: the v2 runner installed
# unpinned from the cu122 wheel index, its console log was lost (0-byte
# archive) and provenance.json records no version. We pin ==0.3.34 (the
# current maximum of the same index the original resolved against). The
# original runner's own preregistration block states "llama.cpp sampling is
# not bit-reproducible across builds", so the paper's determinism claim is
# conditioned on build+hardware: if the installed version differs from the
# pin, rows are recorded BUILD_UNVERIFIED context (summary flag), and any
# wholesale mismatch under a different build is AMBIGUOUS, not a refutation.
#
# HARDWARE GATE: the original ran on 2x Tesla T4 and passed split_mode=1
# (layer split across both cards) for EVERY rung, including single-card-sized
# ones — a single-GPU run is a different compute graph. Determinism across
# GPU architectures is NOT expected (different kernels/reduction orders), so:
#   - exactly 2x Tesla T4 detected  -> rows scored MATCH/MISMATCH
#   - anything else (e.g. P100)     -> rows recorded VOID_ARCH, never MISMATCH
#
# ROW STATUSES: MATCH, MISMATCH, CASCADE (same-seed rows after a candidate
# MISMATCH: the lineage prompt chain may have diverged, so their digests are
# no longer independently comparable), VOID_ARCH, VOID_WEIGHTS, SKIP.
# Skipped rungs (recorded, not run): q8_0 (15.7 GB — exceeds single-GPU
# memory, needs both T4s for weights alone) and q3_k_m (interior rung,
# redundant for testing the claim at the cliff endpoints).
#
# USAGE
#   python kaggle_wave_redetermin.py --dry-run   # digest-list integrity, no GPU
#   python kaggle_wave_redetermin.py             # full re-test (Kaggle T4 x2)
# Resumable: per-(rung,seed) state under redetermin_state/; completed rows are
# never regenerated. Budget ~1.5-2.5 h on T4 x2 (original: 25-50 s/gen).
# ============================================================================

import ast
import gc
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import time

# ----------------------- pinned configuration (v2-identical) -----------------

REPO = "Qwen/Qwen2.5-Coder-14B-Instruct-GGUF"
LLAMA_CPP_PIN = "0.3.34"  # inferred pin; original unrecoverable (see header)
RUNGS = [  # (label, filename, expected sha256 from v2 provenance.json)
    ("q4_k_m", "qwen2.5-coder-14b-instruct-q4_k_m.gguf",
     "c1e659736d89ac1065fb495330fb824d94001974a4bfa78e7270e43476a8d940"),
    ("q2_k", "qwen2.5-coder-14b-instruct-q2_k.gguf",
     "4542a8bb0c0ae6fb3dafeb305c61a8d6b2f894e96bb667d60cda105a1f313176"),
]
SKIPPED_RUNGS = {
    "q8_0": "15.7 GB exceeds single-GPU memory (weights alone need both T4s); "
            "outside minimal rung set for the claim",
    "q3_k_m": "interior rung; Q4_K_M + Q2_K bracket the cliff and suffice",
}
SEEDS = [42, 123, 456, 789, 1111]
GENS = 10
PROBES_PER_PRECISION = 6
N = 26
EPS = 1e-6
N_CTX = 4096
MAX_TOKENS = 1200
TEMPERATURE = 0.8
TOP_P = 0.95
EXPECTED_GPUS = ["Tesla T4", "Tesla T4"]

WORK = "/kaggle/working/redetermin" if os.path.isdir("/kaggle") \
    else os.path.abspath("./redetermin")
STATE_DIR = os.path.join(WORK, "redetermin_state")
MODELS_DIR = "/kaggle/tmp/models" if os.path.isdir("/kaggle") \
    else os.path.abspath("./models")
RESULTS_LOG = os.path.join(WORK, "redetermin_rows.jsonl")
SUMMARY = os.path.join(WORK, "redetermin_summary.json")

# ------------------- embedded expected digests (build-time) ------------------
# Computed from the vendored v2 ledger; see header. 112 entries.
# Keys: "cand|<quant>|<seed>|<gen>" and "probe|<quant>|<k>".

EXPECTED = json.loads("""{
"cand|q2_k|1111|0": "0950f8e03db0cfc7dab13186d627a7592afb2c6305db61871442f404a91a74e1",
"cand|q2_k|1111|1": "c01e518ba6a10ff1b8ada7f31c9dc05e3f852d76dfcf73e89a18d9e1dc33c8f2",
"cand|q2_k|1111|2": "96d4d7d70e64eebeee2b57af27fa36546bfaeb442370443ac277f87cba13c51b",
"cand|q2_k|1111|3": "c01e518ba6a10ff1b8ada7f31c9dc05e3f852d76dfcf73e89a18d9e1dc33c8f2",
"cand|q2_k|1111|4": "8e2fa785cfcdba680eb5db7316c39cbb27f613c5da9905e14ca58ca0c103e538",
"cand|q2_k|1111|5": "77fe5bbeaa3b4e51c2c1b76229dcc1a1952f0e43d558d5c39765bfb30064f2a0",
"cand|q2_k|1111|6": "f1720563ab04bcfcc42b9d440466ab91cfb33b054fee38f74a742dc99dda64f1",
"cand|q2_k|1111|7": "56a36b1a7193f0a60f4a9bbb47f4d67426db69da5bc8b8beec3248c5a4e7716f",
"cand|q2_k|1111|8": "88806f032ae268f8c7ca916d497922142d2d1cb79deb1ae81ee09f000b8761d3",
"cand|q2_k|1111|9": "96d4d7d70e64eebeee2b57af27fa36546bfaeb442370443ac277f87cba13c51b",
"cand|q2_k|123|0": "f25248a7acdd8640071f956e085557333002082f2d3c58d70a18fda9845a4d3b",
"cand|q2_k|123|1": "f98ce2b35d67d72befa9fc365a9ba01610769edae951a2d0c75573f6d555ca2f",
"cand|q2_k|123|2": "2cd9eb33f386ce8ea3647c6b6dc307191bbc9c8ea932b02c1b922c55bde797ea",
"cand|q2_k|123|3": "bb66f1471464df9a0e8b05ff3cb818749a4778ce3b0561bb6657f30118ed10e8",
"cand|q2_k|123|4": "f98ce2b35d67d72befa9fc365a9ba01610769edae951a2d0c75573f6d555ca2f",
"cand|q2_k|123|5": "478a04603b5700c17bda892f4d285e659faa09933d3e984bd86e9c6fe8260134",
"cand|q2_k|123|6": "2cd9eb33f386ce8ea3647c6b6dc307191bbc9c8ea932b02c1b922c55bde797ea",
"cand|q2_k|123|7": "2cd9eb33f386ce8ea3647c6b6dc307191bbc9c8ea932b02c1b922c55bde797ea",
"cand|q2_k|123|8": "f98ce2b35d67d72befa9fc365a9ba01610769edae951a2d0c75573f6d555ca2f",
"cand|q2_k|123|9": "2cd9eb33f386ce8ea3647c6b6dc307191bbc9c8ea932b02c1b922c55bde797ea",
"cand|q2_k|42|0": "2cd9eb33f386ce8ea3647c6b6dc307191bbc9c8ea932b02c1b922c55bde797ea",
"cand|q2_k|42|1": "abbecb383a11de2c06b9295d3cdd8da99b2842e581e71567bed06bcf1a4562ee",
"cand|q2_k|42|2": "2cd9eb33f386ce8ea3647c6b6dc307191bbc9c8ea932b02c1b922c55bde797ea",
"cand|q2_k|42|3": "2cd9eb33f386ce8ea3647c6b6dc307191bbc9c8ea932b02c1b922c55bde797ea",
"cand|q2_k|42|4": "2cd9eb33f386ce8ea3647c6b6dc307191bbc9c8ea932b02c1b922c55bde797ea",
"cand|q2_k|42|5": "2cd9eb33f386ce8ea3647c6b6dc307191bbc9c8ea932b02c1b922c55bde797ea",
"cand|q2_k|42|6": "2cd9eb33f386ce8ea3647c6b6dc307191bbc9c8ea932b02c1b922c55bde797ea",
"cand|q2_k|42|7": "98017df0ce34af91e568dae9e043e238fa610356d276e3df44167bf979ef99d1",
"cand|q2_k|42|8": "495757bef5c0acb221733b29daa9d1b7e987e2caab244a01e2011f0f3cb3f084",
"cand|q2_k|42|9": "2cd9eb33f386ce8ea3647c6b6dc307191bbc9c8ea932b02c1b922c55bde797ea",
"cand|q2_k|456|0": "e0543ef7f3e6a5fa0d1f502c602f0e6cf960ceac0147549ba81f3e3a7e7954fb",
"cand|q2_k|456|1": "c5d84e02e816cc3e0bde6a9ad3186b4fc60496ae0706587bd06ae4af19b2b3fd",
"cand|q2_k|456|2": "2cd9eb33f386ce8ea3647c6b6dc307191bbc9c8ea932b02c1b922c55bde797ea",
"cand|q2_k|456|3": "7837af6216d7175140c97b45303173e1409d262854f8fb2141e950d39de89163",
"cand|q2_k|456|4": "2cd9eb33f386ce8ea3647c6b6dc307191bbc9c8ea932b02c1b922c55bde797ea",
"cand|q2_k|456|5": "babaebf9bdca1924aec82a0d8b2f389c24638e9dc938240d8ff8aee49ff240c4",
"cand|q2_k|456|6": "2cd9eb33f386ce8ea3647c6b6dc307191bbc9c8ea932b02c1b922c55bde797ea",
"cand|q2_k|456|7": "2cd9eb33f386ce8ea3647c6b6dc307191bbc9c8ea932b02c1b922c55bde797ea",
"cand|q2_k|456|8": "3d7b4dcfc0b5c8137fee31dd772ce5f878b4b2ecf5deda3e5ed0dc139716488b",
"cand|q2_k|456|9": "7468c6130ae912085c1668e355ea5bb241378772464ea7a657c099f726e84e66",
"cand|q2_k|789|0": "c3901e8ada132199cb61ca4d16e890f333ab283501b5f0e8e6f8f0d94d487da3",
"cand|q2_k|789|1": "d6e5b09407c17abf9801b63b5d645567585991b22f5c49d90e8be5f72c2e4f7f",
"cand|q2_k|789|2": "7468c6130ae912085c1668e355ea5bb241378772464ea7a657c099f726e84e66",
"cand|q2_k|789|3": "0e031534e6481ec6078bff3b226a7bb847e405a0551b728c3c9359b2abeceda8",
"cand|q2_k|789|4": "f98ce2b35d67d72befa9fc365a9ba01610769edae951a2d0c75573f6d555ca2f",
"cand|q2_k|789|5": "c462f14b1034fef6ead99775cba5ad7b5402a6cd8ce7feaf7806cfc5a1f3e423",
"cand|q2_k|789|6": "2cd9eb33f386ce8ea3647c6b6dc307191bbc9c8ea932b02c1b922c55bde797ea",
"cand|q2_k|789|7": "f98ce2b35d67d72befa9fc365a9ba01610769edae951a2d0c75573f6d555ca2f",
"cand|q2_k|789|8": "7837af6216d7175140c97b45303173e1409d262854f8fb2141e950d39de89163",
"cand|q2_k|789|9": "f98ce2b35d67d72befa9fc365a9ba01610769edae951a2d0c75573f6d555ca2f",
"cand|q4_k_m|1111|0": "c6e1512cedabde2a665ea6f89b3350a19d020f81fe3ab8fc03688b773142157e",
"cand|q4_k_m|1111|1": "a830ab5ff990276ef8ff14ebe691180cdd0c5fc86c9728bdeea38534e0da05e5",
"cand|q4_k_m|1111|2": "2e12cb6bd81eb14eb04b06d1afda09e31a6a6e832e93b72340483d886a7164ef",
"cand|q4_k_m|1111|3": "46311ec5d8a17e9a3defaca57d45660e1caae0904740f741f9d4bca82274777a",
"cand|q4_k_m|1111|4": "71d067ec7ddbd9b1ba87cad7997fbf34b8ea134f06d8a68ab68edc02961e2fac",
"cand|q4_k_m|1111|5": "8e2fa785cfcdba680eb5db7316c39cbb27f613c5da9905e14ca58ca0c103e538",
"cand|q4_k_m|1111|6": "b5e60c3d96e619377d45b370db23a752044c756db8a74a1fc5a441f1162d9a17",
"cand|q4_k_m|1111|7": "6e62e2bc76d5b9520a1a335d2b20eb9a32604cd8fb29b0d9b281e6070d93c563",
"cand|q4_k_m|1111|8": "36660eee9e717a4b7fd483b4a83d87dc0a72035d8dcce1055e2621284e7b992d",
"cand|q4_k_m|1111|9": "25d696a2ebd17240291b7ca93824e971ad6972a4ce37e2e13341cf1ac873f440",
"cand|q4_k_m|123|0": "5b9c6a1c1c6ac19b60cfec1fe5c314756bcae5abadd627a180ecb60a5775de38",
"cand|q4_k_m|123|1": "5c7e16d940d5bc3de364f19e96fdec63025de18b18890056c40de5ac436bf924",
"cand|q4_k_m|123|2": "53fc3e9883d3007792a4e373aa4ac67d2d157046c5409fbc29104e0f7b8104e4",
"cand|q4_k_m|123|3": "ad9c89ecde8f165b4b1960ecb28653b71e8d41682290ca981875424c19c1e458",
"cand|q4_k_m|123|4": "15b67ac746d1a980015a04bddbbbc3a3d6e057dcc5455ffcb51e80e78c45b470",
"cand|q4_k_m|123|5": "34870aed36c3ee3b3135a38c006adac435964dd3ad747caa39655abdf19afe2b",
"cand|q4_k_m|123|6": "74740cdf1dc95004b419262ac066cbc71be25bf4819b03550c24f42800d8cb6d",
"cand|q4_k_m|123|7": "06d77e86c04abe6bb77d6afe98125aee1976e9e5ce369276c7b5d7e890bdac43",
"cand|q4_k_m|123|8": "06d77e86c04abe6bb77d6afe98125aee1976e9e5ce369276c7b5d7e890bdac43",
"cand|q4_k_m|123|9": "06d77e86c04abe6bb77d6afe98125aee1976e9e5ce369276c7b5d7e890bdac43",
"cand|q4_k_m|42|0": "53fc3e9883d3007792a4e373aa4ac67d2d157046c5409fbc29104e0f7b8104e4",
"cand|q4_k_m|42|1": "4e5c7694a5340d8463c094e6df5aa955acd4efba3264e5e6906c099e6cd1339f",
"cand|q4_k_m|42|2": "b0a2134363bb5b653c08d50a3d3a33da65900e97144016439b3dbd5f2f2d0c18",
"cand|q4_k_m|42|3": "0545a8ce5ab92f6826212f05e1b2dc343ed292f1436feb08099b42696cc441b6",
"cand|q4_k_m|42|4": "db4273a31b18cba0f5754398f81b9e747e93f5c7fde438c2d3e5d909ad95720a",
"cand|q4_k_m|42|5": "f7da5a1b0eac301485c07c625cc74044f0055a8d26a6f61319380480244ae4a4",
"cand|q4_k_m|42|6": "0394328148d5d675616e18edee77e6805f1c1019f0413ef327f5c362a7345eb6",
"cand|q4_k_m|42|7": "5c679fc78cccffa8220c471cd83e12a4ee40355603a05bccac4c88e46550dd54",
"cand|q4_k_m|42|8": "692a17a1349b7cc63fbbc9f49516d4a77e676452a0cdb9a0ae77f023e5fbdaad",
"cand|q4_k_m|42|9": "74db39d0fa60e356c9282021e62bc087a2f915a5c94a57a0e3466897e63b80c9",
"cand|q4_k_m|456|0": "ab502c80e71b9c897a4fe32b342d08705cf5edd0cb0e07e06ac08c907e35373c",
"cand|q4_k_m|456|1": "c60bf47b10893be89890245bf74ee294e19c889d48616ef1670ea00ec3f820d5",
"cand|q4_k_m|456|2": "9d3cc0c72987f2f94e1d94bfc2ff6a3390bbab69d820854f85c3ca202cd5c09d",
"cand|q4_k_m|456|3": "b58689c3b254e37b2c82cdd4842c41fdc75927f0b36a78b7862d1eeb1cd8e06c",
"cand|q4_k_m|456|4": "2cd9eb33f386ce8ea3647c6b6dc307191bbc9c8ea932b02c1b922c55bde797ea",
"cand|q4_k_m|456|5": "9cd4284d71cdd2e9311b40979e5807bd57d6ccbf903ff0c1873227304a82537f",
"cand|q4_k_m|456|6": "2cd9eb33f386ce8ea3647c6b6dc307191bbc9c8ea932b02c1b922c55bde797ea",
"cand|q4_k_m|456|7": "53fc3e9883d3007792a4e373aa4ac67d2d157046c5409fbc29104e0f7b8104e4",
"cand|q4_k_m|456|8": "2656161ea88fd549306aee8a3e3c4cc03d6d50dd616d285f8007c6be25e2cd6c",
"cand|q4_k_m|456|9": "b0a2134363bb5b653c08d50a3d3a33da65900e97144016439b3dbd5f2f2d0c18",
"cand|q4_k_m|789|0": "f2b2e181990cfe06bfd3b365b15ebb8b169baeef927ac2e6e41db03b9dcef598",
"cand|q4_k_m|789|1": "862ede184331228a4986ee6f8e514796f887bf0352b4f27bbb23496003d50798",
"cand|q4_k_m|789|2": "ddc62879d9e1132911c5e5ea277da4b66225e0c05289a50ae03342982b8bebd3",
"cand|q4_k_m|789|3": "a4bd345f04268c8c341743c25ee16fc14dd36963b3e081003e44d5b308ecd7b8",
"cand|q4_k_m|789|4": "53fc3e9883d3007792a4e373aa4ac67d2d157046c5409fbc29104e0f7b8104e4",
"cand|q4_k_m|789|5": "db4273a31b18cba0f5754398f81b9e747e93f5c7fde438c2d3e5d909ad95720a",
"cand|q4_k_m|789|6": "0394328148d5d675616e18edee77e6805f1c1019f0413ef327f5c362a7345eb6",
"cand|q4_k_m|789|7": "0394328148d5d675616e18edee77e6805f1c1019f0413ef327f5c362a7345eb6",
"cand|q4_k_m|789|8": "34870aed36c3ee3b3135a38c006adac435964dd3ad747caa39655abdf19afe2b",
"cand|q4_k_m|789|9": "2da64138f81ea8a1872fbafc0999fa945e2a9e37f7f81a60cd323cf0b577cab1",
"probe|q2_k|0": "4bb7f3341553b1a2d4cf802780388c1faf8c725da6d6f2694b5fdf878e662565",
"probe|q2_k|1": "08da4538565eeeea3e0da149510115f6e4b485c8af0b1f187963ea8fc72186fa",
"probe|q2_k|2": "dee0e64f20554f6f57ea5eb690b9c194ee08d41f95c1d3693c01b6d6fc3c1398",
"probe|q2_k|3": "43d3214d0c86c89f882a909c677f1fbb2210a2c43604a2a7ad38686ef7e7b748",
"probe|q2_k|4": "085bc75ddc96b21c994d3be0e4586605695d608c8b54e4b62b51e5ef98c0463d",
"probe|q2_k|5": "1b055c2aae98e87124d293d70cd398fe1bbc84996d408f797b1c78541bc35306",
"probe|q4_k_m|0": "e2019b7f9f37f4ae4db1113fe8944999f9eefef423d3696ea8e2f76a544879c3",
"probe|q4_k_m|1": "9c9febe4fc3c6972359e9cea528c65a44d402ba9ffcc3304bf3efa55cdaffe2a",
"probe|q4_k_m|2": "7794862c1ced3fc72401a3af2812fb817f79057133521661f62279f6c75090da",
"probe|q4_k_m|3": "270168e061b53683b7370c16a339845fa3f4045d7fb7413fcae6edd8259fa7d5",
"probe|q4_k_m|4": "3200b44aaed8b81752cdf24d16b2005a0b401873c310dad249fa6a235e137b2e",
"probe|q4_k_m|5": "e8f7aba11cb1ff7e127cb382ffb8071f80e38ea183d95d9d484f71cdb47c66fc"
}""")
EXPECTED_META_SHA256 = "e1e8c7bee1f609e2cf2c8121b00bcde904d34165cd28527aabf124e2f35e5d92"
EXPECTED_N = 112

# ------------------------- evaluator (v2-identical) --------------------------


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
    res = {"viable": False, "valid": False, "score": 0.0, "n": 0 if circles is None else len(circles)}
    if circles is None:
        return res
    if len(circles) != N or any(r <= 0 for (_, _, r) in circles):
        return res
    res["viable"] = True
    radii = [r for (_, _, r) in circles]
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


def self_test():
    base = baseline_packing()
    ev = evaluate([tuple(c) for c in base])
    assert ev["valid"], "baseline must be valid"
    assert abs(ev["score"] - 0.89999) < 1e-4, f"baseline score {ev['score']}"
    c, err = parse_proposal("junk before [[0.1, 0.1, 0.05]] junk after")
    assert err is None and len(c) == 1, "parser must extract bracketed list"
    print("[selftest] evaluator + parser OK")


# ------------------------------ prompts (v2-identical) -----------------------


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


PROBE_PROMPT = (
    f"Pack exactly {N} non-overlapping circles inside the unit square [0,1]x[0,1] "
    "so that the sum of their radii is as large as possible. Every circle must lie "
    "fully inside the square; circles may touch but not overlap.\n"
    "Output ONLY the raw Python list of 26 [x, y, r] lists. No explanation, "
    "no code fences, no other text."
)

# ------------------------------ digests --------------------------------------


def canon_digest(obj):
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def cand_digest(circles, parse_error, text):
    c = ([[round(x, 6), round(y, 6), round(r, 6)] for (x, y, r) in circles]
         if circles is not None else None)
    raw = None if circles is not None else (text or "")[:3000]
    return canon_digest({"circles": c, "parse_error": parse_error, "raw": raw})


def probe_digest(parse_error, text):
    return canon_digest({"parse_error": parse_error, "raw": (text or "")[:4000]})


def verify_digest_table():
    assert isinstance(EXPECTED, dict)
    assert len(EXPECTED) == EXPECTED_N, f"expected {EXPECTED_N}, got {len(EXPECTED)}"
    hexre = re.compile(r"^[0-9a-f]{64}$")
    for k, v in EXPECTED.items():
        assert hexre.match(v), f"bad digest for {k}"
        kind = k.split("|")[0]
        assert kind in ("cand", "probe"), k
    for quant, _, _ in RUNGS:
        for s in SEEDS:
            for g in range(GENS):
                assert f"cand|{quant}|{s}|{g}" in EXPECTED
        for p in range(PROBES_PER_PRECISION):
            assert f"probe|{quant}|{p}" in EXPECTED
    meta = hashlib.sha256(
        "\n".join(f"{k}={EXPECTED[k]}" for k in sorted(EXPECTED)).encode()
    ).hexdigest()
    assert meta == EXPECTED_META_SHA256, \
        f"digest table corrupted: meta {meta} != {EXPECTED_META_SHA256}"
    print(f"[digests] {len(EXPECTED)} entries, meta-sha OK ({meta[:16]}...)")


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


def gpu_names():
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True, text=True, timeout=30).stdout.strip()
        return [l.strip() for l in out.splitlines() if l.strip()]
    except Exception:
        return []


def append_jsonl(path, row):
    line = json.dumps(row)
    with open(path, "a") as f:
        f.write(line + "\n")
        f.flush()
        os.fsync(f.fileno())
    print("JSONL|" + line, flush=True)


def spath(quant, seed):
    return os.path.join(STATE_DIR, f"{quant}_seed_{seed}.json")


def load_state(quant, seed):
    p = spath(quant, seed)
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    base = baseline_packing()
    ev = evaluate([tuple(c) for c in base])
    return {"quant": quant, "seed": seed, "gen": 0, "tainted": False,
            "best_circles": base, "best_score": ev["score"]}


def save_state(st):
    with open(spath(st["quant"], st["seed"]), "w") as f:
        json.dump(st, f)


def done_keys():
    if not os.path.exists(RESULTS_LOG):
        return set()
    with open(RESULTS_LOG) as f:
        return {json.loads(l)["key"] for l in f}


# --------------------------- model / generation ------------------------------


def bootstrap_llama_cpp():
    """Lazy: nothing installs at import time (keeps --dry-run GPU-free)."""
    def _pip(*a):
        return subprocess.run([sys.executable, "-m", "pip", "install", "-q", *a]
                              ).returncode
    _pip("huggingface_hub")
    _pip(f"llama-cpp-python=={LLAMA_CPP_PIN}",
         "--extra-index-url", "https://abetlen.github.io/llama-cpp-python/whl/cu122")
    try:
        import llama_cpp  # noqa: F401
    except Exception:
        print("[bootstrap] pinned wheel failed; building pinned from source (slow)...")
        env = dict(os.environ, CMAKE_ARGS="-DGGML_CUDA=on")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                        "--force-reinstall", "--no-cache-dir",
                        f"llama-cpp-python=={LLAMA_CPP_PIN}"],
                       env=env, check=True)
        import llama_cpp  # noqa: F401
    import llama_cpp
    print("[bootstrap] llama_cpp ready:", llama_cpp.__version__)
    return llama_cpp.__version__


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
        kwargs["split_mode"] = 1  # v2 passed this for every rung on T4 x2
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
    except Exception as e:
        return None, f"gen_error: {type(e).__name__}: {e}", time.time() - t0
    return text, None, time.time() - t0


# ------------------------------ re-test --------------------------------------


def run_rung(quant, fname, want_sha, ctx, done):
    n_gpus = len(ctx["gpus"])
    states = {s: load_state(quant, s) for s in SEEDS}
    probe_keys_left = [k for k in range(PROBES_PER_PRECISION)
                       if f"probe|{quant}|{k}" not in done]
    if all(st["gen"] >= GENS for st in states.values()) and not probe_keys_left:
        print(f"[done] {quant}: already complete, skipping")
        return

    path = download_model(fname)
    got_sha = sha256_file(path)
    weights_ok = got_sha == want_sha
    print(f"[hash] {quant}: {got_sha[:16]}... "
          f"({'OK' if weights_ok else 'MISMATCH vs provenance'})")

    llm = load_llm(path, n_gpus)
    try:
        for gen in range(GENS):
            for s in SEEDS:
                st = states[s]
                if st["gen"] != gen:
                    continue
                key = f"cand|{quant}|{s}|{gen}"
                prompt = loop_prompt([tuple(c) for c in st["best_circles"]],
                                     st["best_score"])
                text, gerr, wall = generate(llm, prompt, s * 1000 + gen)
                circles, perr = parse_proposal(text) if gerr is None else (None, gerr)
                ev = evaluate(circles)
                got = cand_digest(circles, perr, text)
                if not ctx["arch_ok"]:
                    status = "VOID_ARCH"
                elif not weights_ok:
                    status = "VOID_WEIGHTS"
                elif st["tainted"]:
                    status = "CASCADE"
                elif got == EXPECTED[key]:
                    status = "MATCH"
                else:
                    status = "MISMATCH"
                    st["tainted"] = True  # lineage prompt chain may diverge
                append_jsonl(RESULTS_LOG, {
                    "key": key, "status": status, "digest": got,
                    "expected": EXPECTED[key], "score": round(ev["score"], 6),
                    "valid": ev["valid"], "parse_error": perr,
                    "wall_s": round(wall, 2)})
                print(f"[{status}] {key} score={ev['score']:.6f} ({wall:.0f}s)")
                if ev["valid"] and ev["score"] > st["best_score"]:
                    st["best_score"] = ev["score"]
                    st["best_circles"] = [list(c) for c in circles]
                st["gen"] = gen + 1
                save_state(st)

        for k in range(PROBES_PER_PRECISION):
            key = f"probe|{quant}|{k}"
            if key in done:
                continue
            text, gerr, wall = generate(llm, PROBE_PROMPT, 900000 + k)
            circles, perr = parse_proposal(text) if gerr is None else (None, gerr)
            got = probe_digest(perr, text)
            if not ctx["arch_ok"]:
                status = "VOID_ARCH"
            elif not weights_ok:
                status = "VOID_WEIGHTS"
            elif got == EXPECTED[key]:
                status = "MATCH"
            else:
                status = "MISMATCH"  # probes are chain-free: independent rows
            append_jsonl(RESULTS_LOG, {
                "key": key, "status": status, "digest": got,
                "expected": EXPECTED[key], "parse_error": perr,
                "wall_s": round(wall, 2)})
            print(f"[{status}] {key} ({wall:.0f}s)")
    finally:
        del llm
        gc.collect()
        try:
            os.remove(path)
            print(f"[cleanup] removed {fname}")
        except OSError:
            pass


def summarize(ctx):
    raw_rows = [json.loads(l) for l in open(RESULTS_LOG)] \
        if os.path.exists(RESULTS_LOG) else []
    rows = list({r["key"]: r for r in raw_rows}.values())  # dedupe crash-resume
    counts = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    out = {
        "claim": "pinned stack regenerates the same outcomes (paper 2 s3)",
        "rows_tested": len(rows), "rows_expected": EXPECTED_N,
        "coverage": "112 of 224 original generations (q4_k_m + q2_k)",
        "counts": counts,
        "skipped_rungs": SKIPPED_RUNGS,
        "gpus": ctx["gpus"], "arch_ok": ctx["arch_ok"],
        "llama_cpp_version": ctx.get("llama_cpp_version"),
        "llama_cpp_pin": LLAMA_CPP_PIN,
        "build_unverified": True,  # original build unrecoverable; see header
        "verdict": (
            "VOID (hardware arch differs from original T4 x2)" if not ctx["arch_ok"]
            else "SUPPORTED" if counts.get("MISMATCH", 0) == 0
            and counts.get("MATCH", 0) > 0
            else "AMBIGUOUS (build pin unverifiable; see header) or REFUTED — "
                 "inspect MISMATCH rows"),
    }
    with open(SUMMARY, "w") as f:
        json.dump(out, f, indent=2)
    print("\n[summary]", json.dumps(out, indent=2))


def main():
    dry = "--dry-run" in sys.argv
    self_test()
    verify_digest_table()
    if dry:
        print("[dry-run] digest table intact; evaluator/parser self-test passed; "
              "no GPU work performed.")
        return 0

    os.makedirs(WORK, exist_ok=True)
    os.makedirs(STATE_DIR, exist_ok=True)
    gpus = gpu_names()
    arch_ok = gpus == EXPECTED_GPUS
    print(f"[gpus] {gpus or 'NONE'} -> arch_ok={arch_ok} "
          f"(original: {EXPECTED_GPUS})")
    if not arch_ok:
        print("[warn] different hardware than the original run; rows will be "
              "recorded VOID_ARCH — determinism across GPU archs is not "
              "expected, so this is not evidence either way.")
    ver = bootstrap_llama_cpp()
    ctx = {"gpus": gpus, "arch_ok": arch_ok, "llama_cpp_version": ver}
    if ver != LLAMA_CPP_PIN:
        print(f"[warn] llama_cpp {ver} != pin {LLAMA_CPP_PIN}; results ambiguous")

    done = done_keys()
    for quant, fname, want_sha in RUNGS:
        print(f"\n===== rung: {quant} =====")
        run_rung(quant, fname, want_sha, ctx, done)
    for quant, reason in SKIPPED_RUNGS.items():
        print(f"[skip] {quant}: {reason}")
    summarize(ctx)
    return 0


if __name__ == "__main__":
    sys.exit(main())
