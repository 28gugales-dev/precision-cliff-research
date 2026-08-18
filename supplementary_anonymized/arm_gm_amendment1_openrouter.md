# Arm GM — amendment 1 (serving-path deviation, registered before resumption)

Registered 2026-08-16, before any resumed sampling. No rule, threshold,
prompt, sample-count or scorer changes. Mirrors arm GM3's amendment 1
(arm_gm3_amendment1_openrouter.md) — same deviation class, same accounting.

## What happened

Arm GM (arm_gm_preregistration.txt, commit 37b3adb: gemini-2.5-flash-lite,
7 N x 20 samples, temperature 1.0, maxOutputTokens 4096, byte-identical
arm-F bare prompts) stalled on first-party free-tier quota at 55 of 140
content rows (N=13 complete; N=17, 35, 37 partial; N=21, 31, 43 unsampled).
The stall is the API key's daily quota, not a model or design failure.

## Repair (mechanical)

The remaining 85 cells are collected through openrouter.ai with model id
`google/gemini-2.5-flash-lite` — a proprietary model: OpenRouter routes to
Google's own serving (AI Studio / Vertex) rather than to third-party hosts,
so the underlying server-side model is the vendor's own, addressed through
one additional alias layer. Request parameters are the prereg's exactly
(temperature 1.0, max_tokens 4096). Resumed rows are tagged
serving_path=openrouter, store the raw OpenRouter response verbatim
including the reported provider string, and append to the same ledger
(arm_gm_checkpoint.jsonl) under the same resume rule (content rows final,
transport errors re-runnable).

## Accounting rule

As GM3: the analysis reports BOTH accountings — first-party-only (the 55
pre-stall rows) and mixed-path (all 140) — and any verdict that differs
between them is reported as path-sensitive rather than claimed. Per-row
serving path makes both computable by any reader.
