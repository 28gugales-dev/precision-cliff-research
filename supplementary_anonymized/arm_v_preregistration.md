# Arm V preregistration — cross-vendor zero-shot template anchoring

Registered: 2026-08-12, BEFORE any sampling. This file's git commit must be
an ancestor of every Arm V sampling run.

## Motivation

Every proposer arm to date (A–D, F, opus_wave2) is a single vendor's model
family behind a single vendor's agent runtime. The closed-form selection
rule k*(N) = floor(sqrt(N) + 1/2) and the anchored construction values were
derived and tested inside that family. Arm V asks whether the anchoring
phenomenon and the rule's predictions survive a change of BOTH vendor and
runtime — the cheapest available attack on the single-vendor limitation.

## Proposers (alias-addressed, disclosed as such)

Via the opencode CLI (v1.18.3), zen free tier, run date 2026-08-12:

1. `opencode/deepseek-v4-flash-free`   (DeepSeek)
2. `opencode/nemotron-3-ultra-free`    (NVIDIA Nemotron)
3. `opencode/hy3-free`                 (Tencent Hunyuan)

Disclosures, per the paper's own repair protocol: these are ALIASES on a
managed free-tier serving path. Served quantization, decode path, sampling
parameters and the runtime's injected system prompt are not exposed and
not attested; `sampling_params: null` is recorded on every row. This is
the same observability class as Arms A–D/F and is the point: same
addressing mode, different vendor.

## Task and prompts — byte-identical to Arm F

Zero-shot statement (paper 1 appendix A.5) with the A.10 no-code line,
N parameterized. Prompt SHA-256 (from `arm_f_prompts.json`, pinned
2026-07-30, restated here):

| N | sha256 |
|---|--------|
| 13 | 32db485bea625ff9f39f4723ebf1a01f337559a9e2cf567fb486928f71f7f8df |
| 17 | 8437df753f98cf7c263869a6f6813f19a6e8a2cda206affab8d7ef7ad1c6d942 |
| 31 | a664d003cbf1c0eca51bae5b3a1d072071eb34756725a7491d6a2e8fa3b78e92 |
| 35 | 3b08c56e587df8700a5db0be38bbca680eb8d1ea1ad138eb0768fead69a6b22c |
| 37 | 2c0a88191cb280e9105949b6f76d442da40c7ad6661cb584bf9f546225fcc516 |

The runner recomputes each hash from `arm_f_prompts.json` at call time and
aborts on mismatch.

## Design

5 samples per (model, N): 3 x 5 x 5 = 75 invocations. Every invocation is
written to `arm_v_candidates_raw.jsonl` live, failures and refusals
included; nothing is dropped. Scoring uses `arm_f_repro.py`'s
parse/validate/classify unchanged: validity at 1e-6 (primary) and 1e-9
(logged), construction identity at 2e-3, exact rendering at 2e-6 — all
tolerances registered in Arm F before its sampling and reused verbatim.

## Predictions (closed form, from `arm_f_repro.py` PREDICTIONS, unchanged)

| N | branch | predicted sum | rival argmax | discriminates? |
|---|--------|--------------|--------------|----------------|
| 13 | truncate | 1.6250000 | 1.7761424 | yes |
| 17 | extend   | 2.0517767 | 2.0517767 | no |
| 31 | truncate | 2.5833333 | 2.7485281 | yes |
| 35 | truncate | 2.9166667 | 2.9166667 | no (zero-gap trap) |
| 37 | extend   | 3.0345178 | 3.0345178 | no |

## Registered outcomes and decision rules

Floor (per model): at least 10 of that model's 25 invocations valid at
1e-6. A model below floor is labelled BELOW-FLOOR; no anchoring claim of
any direction may be made from it (wave-7 convention).

V1 — anchoring transfer (primary, per model clearing floor): at least 50%
of the model's valid outputs lie within 2e-3 of the predicted construction
value (pooled over its Ns). Branches: >= 50% -> TRANSFERS;
< 50% -> DOES-NOT-TRANSFER. Both reportable.

V2 — rule-selection strong form (per model clearing floor, discriminating
Ns 13 and 31 only): rival-argmax emissions (within 2e-3 of the rival,
which is farther than 1e-9 from the prediction) at most 10% of valid
outputs on those Ns. Claude arms observed 0/21. Branches: <= 10% -> HOLDS;
> 10% -> FAILS.

Everything else — per-N breakdowns, structure taxonomies, cross-model
comparisons, echo behaviour — is descriptive and will be labelled so.

## What would falsify what

- All three models TRANSFER + HOLD: anchoring is not a Claude-family
  artifact; paper 1's scope caveat weakens to runtime-generality only.
- Any model clearing floor with DOES-NOT-TRANSFER: template anchoring is
  family-specific; paper 1's closed form is a family property, and its
  limitation section says so with data instead of a caveat.
- All models BELOW-FLOOR: no evidence either way (floor label), consistent
  with wave-7's competence-floor finding at small open models.
