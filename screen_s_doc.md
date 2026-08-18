# Screen S — family competence screen over OpenRouter free tier

Registered 2026-08-16, committed BEFORE any screen sampling (the runner
refuses to start unless this file is committed). This is a SELECTION
INSTRUMENT, not an evidential arm — see "what this can and cannot say".

## Purpose

Waves 7/7b left family generality unresolved: all four non-Qwen families
tested (llama-8B, gemma-9B, phi-4-14B, mistral-24B) fell below their
registered competence floors on the 26-circle packing task — too few
valid outputs to evaluate the echo contrast at all. The registered
disconfirmation branch fired: the limitation is stated in the abstract.

The fix requires a non-Qwen family that (a) clears the format-competence
floor and (b) has a locally runnable GGUF ladder. This screen finds
candidates for (a) cheaply before any GGUF is downloaded for (b).

## What this can and cannot say

The serving path is an unattested API alias (OpenRouter routing to
third-party providers). Served precision is unknown — which is this
project's own core finding. Therefore:

- A screen PASS means only: "advance this family to the local
  pinned-GGUF ladder." It is a gating decision, not a paper claim.
- A screen FAIL means only: "not selected for the ladder now." It is
  NOT evidence the family sits below a competence floor — the provider
  could be serving quantized or otherwise degraded weights.
- No number from this screen enters either paper as a result. If a
  screened family later runs the local ladder, the ladder's own
  registered floor rule applies from scratch.

## Design

One-shot generation-0 proposal calls: the wave-7b `loop_prompt` with
`baseline_packing()` (the registered 26-circle grid baseline, sum
0.89999) shown as parent. 50 calls per model. This deliberately mirrors
the wave-7/7b apparatus — same prompt constructor, same parser, same
evaluator (N=26, EPS=1e-6), byte-copied from
`supplementary_anonymized/sec3_artifacts/runners/kaggle_wave7b_phi4_14b.py`
(the runner self-tests them at startup). It is NOT the wave loop
protocol (no evolved parents, no seeds, no must-differ block); the
"20/50 valid" bar below is a heuristic borrowed from wave 7b's power
floor, not that registered floor itself.

Selection rule: >= 20/50 valid at EPS=1e-6 -> family advances to local
ladder consideration. Reported per model regardless: valid count,
viable count, finish_reason distribution, provider(s) observed.

## Models (all non-Qwen, all with GGUF repos verified on HF 2026-08-16)

| screen id (OpenRouter :free) | family | GGUF source seen |
|---|---|---|
| google/gemma-4-31b-it:free | Gemma (31B; 9B sibling failed wave 7) | unsloth/gemma-4-31B-it-GGUF |
| nvidia/nemotron-3-super-120b-a12b:free | Nemotron (120B MoE, A12B) | bartowski/nvidia_Nemotron-3-Super-120B-A12B-GGUF |
| nvidia/nemotron-3-nano-30b-a3b:free | Nemotron (30B MoE, A3B) | unsloth/Nemotron-3-Nano-30B-A3B-GGUF |
| openai/gpt-oss-20b:free | GPT-OSS (20B MoE) | unsloth/gpt-oss-20b-GGUF |
| cohere/north-mini-code:free | Cohere North (code) | bartowski/North-Mini-Code-1.0-GGUF |

Q2_K / Q4_K_M file presence inside those repos is re-verified before any
ladder run; the screen only requires that a repo exists.

## Sampling parameters

temperature 0.8, top_p 0.95 (wave-7/7b values, set explicitly in the
request), max_tokens 4096 (deliberately above wave-7b's 1200 so a
provider-side reasoning wrapper cannot silently censor output — the
amendment-3 lesson; finish_reason logged per row and any
finish_reason=length row is reported as truncated, not as a model
failure). One serial worker per model, 20 s spacing per worker (5
workers ~ 15 req/min, under the shared 20/min account cap). Launched
only after the GM3 OpenRouter resume completes.

## Ledger

`screen_s_raw.jsonl`, one row per call, appended live: model, provider
(as reported by OpenRouter), sample index, prompt SHA-256, request
params, finish_reason, raw text, parse/validity results, timing.
Failures and empty rows stay in the ledger. Analysis:
`screen_s_report.py` recomputes validity from coordinates, no-argument
replay.

## Prior state, disclosed

gpt-oss-20b, north-mini-code, and nemotron-3-ultra-550b have Arm-V rows
in this corpus on a DIFFERENT task (the arm-F geometry prompts). No
model has ever been sampled on the wave-7 26-circle task through any
API path. Screen S and Arm V share the OpenRouter account and its rate
limits but no data.
