# Wave 7c — addendum 1: nemotron-3-super-120b-a12b ladder (registered before sampling)

Registered 2026-08-17, before any 120B ladder row exists anywhere in this
corpus. Extends wave7c_prereg_screened_families.md (SHA b1fc9ee9…, public
Kaggle dataset) by converting its ADVANCED-NOT-RUN (hardware) entry into a
run condition, hardware having become available. No prediction, threshold,
prompt, evaluator or seed-rule changes: predictions 7c.1/7c.2/7c.3 apply
verbatim, per family, NO POOLING, same 20-valid power floor, same
disconfirmation clauses.

## Condition

| family | repo | rungs (split GGUF; llama.cpp loads via first shard) | seeds |
|---|---|---|---|
| nemotron_super_120b | `bartowski/nvidia_Nemotron-3-Super-120B-A12B-GGUF` | `nvidia_Nemotron-3-Super-120B-A12B-Q2_K/...-00001-of-00002.gguf` (+1), `nvidia_Nemotron-3-Super-120B-A12B-Q4_K_M/...-00001-of-00003.gguf` (+2) | [7901, 7902, 7903, 7904, 7905] (grep-verified fresh) |

Screen record (selection only, prereg SS2): 34/50 valid, 16/50
truncation-censored, provider Nvidia throughout.

## Hardware and toolchain disclosure

This condition runs on a rented single H100-80GB (DigitalOcean), not the
Kaggle T4x2 of every prior wave. Same runner template, same llama.cpp
wheel-install path, same sampling parameters (temperature 0.8, top_p 0.95,
MAX_TOKENS 1200, N=26, EPS=1e-6, generation-major order, live JSONL with
console echo, per-file SHA-256 in provenance). llama.cpp seeded sampling is
deterministic only on fixed weights+hardware+build: rows from this condition
are STATISTICALLY comparable to the T4 waves and NOT bit-comparable; no
cross-hardware bit-identity claim is made or implied. The papers' §6
throughput-is-not-a-fingerprint caveat applies to any timing read across
this condition and the T4 conditions.

## MoE note

A12B active parameters over a 120B MoE total; the K-quant rungs quantize
the full expert set. This is the corpus's first MoE ladder alongside
gpt-oss-20b, whose MXFP4-conversion qualifier does NOT apply here —
nemotron-3-super's native release is BF16, so its Q2_K/Q4_K_M are
conversions of the same kind as every dense wave's.

## Analysis

`wave7c_analysis.py` FAMILIES map gains the nemotron_super_120b entry;
logic byte-identical, no-argument replay.
