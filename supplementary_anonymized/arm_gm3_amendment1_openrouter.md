# Arm GM3 — amendment 1 (serving-path deviation, registered before resumed sampling)

Registered 2026-08-16, after 99/140 cells were collected via
`generativelanguage.googleapis.com` (first-party Google API, per prereg
`arm_gm3_preregistration.txt`) and BEFORE any resumed sampling. No rule,
threshold, prompt, cell, sample count, temperature, token budget, scorer,
prediction or falsifier changes.

## What changes and why

The remaining 41 cells (N=35 one cell; N=37 and N=43, 20 cells each) are
sampled through OpenRouter (`openrouter.ai/api/v1/chat/completions`,
model id `google/gemma-4-26b-a4b-it`, the exact model the prereg names)
instead of the Google first-party endpoint. Reason: operational — the
free-tier Google key stalls on daily quota; the operator directed
completion through OpenRouter.

This is a SERVING-PATH deviation of exactly the kind the companion paper
analyzes: OpenRouter is an alias in front of third-party providers, so
the provider, its quantization, and its decode path are unattested for
these 41 rows. We disclose rather than hide it:

- Every resumed row carries `serving_path: "openrouter"`, the raw
  OpenRouter response verbatim (which includes the provider name
  OpenRouter reports for the call), and the request params used.
- The 99 first-party rows are unchanged and carry no `serving_path`
  field; the two eras are mechanically distinguishable forever.
- Both accountings are computable by any reader: (a) first-party-only
  (99 rows, N=37/N=43 cells absent → UNSCOREABLE under the registered
  <3-valid rule), and (b) mixed-path (140 rows, deviation disclosed).
  The report states both.

## Unchanged mechanics restated

- Prompts: byte-identical arm F prompts, SHA-256 re-verified at call
  time against `arm_f_prompts.json`; hash mismatch aborts the run.
- temperature 1.0, max output tokens 16384 (per GM3 prereg).
- Checkpoint ledger: same file (`arm_gm_gm3_checkpoint.jsonl`), same
  resume rule (content rows final; transport-error rows requeued).
- Scoring pipeline unchanged. One mechanical addition at analysis time:
  the text extractor gains a branch for the OpenAI-style `choices`
  response shape OpenRouter returns (the Gemini `candidates` branch is
  untouched). Extraction only; no scoring logic changes.

## Reporting rule

The paper reports GM3 with this deviation named in one sentence, in the
same style as the other disclosed deviations: 99/140 cells first-party,
41/140 via OpenRouter (provider as logged per row), predictions and
falsifier evaluated on the mixed set, first-party-only accounting also
stated.
