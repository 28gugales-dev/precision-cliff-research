# Wave 7b preregistration — family generality, second attempt, competence-matched

Status: LOCKED at push time; lock = SHA-256 of this file published as public Kaggle
dataset `ANON-KAGGLE-OWNER/wave7b-prereg-families-14b` before any row is sampled. Author
field open, same caveat as every prior wave.

## 1. Why a 7b exists

Wave 7 (`wave7_prereg_families.md`) returned **UNDERPOWERED in both families**: the
8-9B class cannot reliably emit a valid 26-circle packing at any precision (llama 1/50
and 5/50 valid; gemma 14/50 and 4/50, every valid gemma row a parent echo at both
rungs). Its power floor converted that into "could not test", not "no difference".
Wave 7b raises the model class to match the family where the cliff is established —
Qwen2.5-Coder-**14B** — instead of lowering the task. Everything else is unchanged:
byte-identical prompts, evaluator, sampling parameters, 5 seeds x 10 generations
per rung, must-differ probes, the same runner template by mechanical substitution.

Wave-7's outcome is disclosed prior state, and it cuts both ways: we now know 8-9B
models fail the *format*, and we do not know whether any non-Qwen model passes it.
Choosing two larger models is a bet that competence, not family, was wave 7's binding
constraint. If they also miss the power floor, that too is reportable: it would mean
the task's competence floor sits unusually close to Qwen-Coder's ability, which is
itself evidence that §3's substrate is narrow — and §8 would say so.

## 2. Conditions

| kernel | repo (verified ungated 2026-08-08, unauthenticated HfApi listing) | files |
|---|---|---|
| phi4 | `bartowski/phi-4-GGUF` (14.7B) | `phi-4-Q2_K.gguf`, `phi-4-Q4_K_M.gguf` |
| mistral24 | `bartowski/Mistral-Small-24B-Instruct-2501-GGUF` (24B) | `Mistral-Small-24B-Instruct-2501-Q2_K.gguf`, `Mistral-Small-24B-Instruct-2501-Q4_K_M.gguf` |

Weight SHA-256 + byte length recorded in provenance at download time. Seeds: phi4
`[7301, 7302, 7303, 7304, 7305]`, mistral24 `[7401, 7402, 7403, 7404, 7405]` — never
sampled in any prior run (grep of `sec3_artifacts/runners/` and both wave-7 runners).
Budget per family: 120 generations (100 loop + 20 must-differ).

## 3. External timestamp

Kernels `ANON-KAGGLE-OWNER/precision-sweep-phi4-14b-wave7b` and
`ANON-KAGGLE-OWNER/precision-sweep-mistral24b-wave7b`, public, pushed before sampling; this
file as public dataset `ANON-KAGGLE-OWNER/wave7b-prereg-families-14b`.

## 4. Prior state, disclosed

No Phi-4 or Mistral-Small output exists anywhere in this corpus. Qwen priors and
wave-7's two underpowered arms are the only relevant history, both published.

## 5. Registered predictions

Identical to wave 7 §5, verbatim, applied per family with NO POOLING and the same
FAMILY-DEPENDENT split-outcome rule:

- **7b.1 PRIMARY, NOT floor-gated:** among valid rows, echo(Q2_K) − echo(Q4_K_M) ≥ 15
  percentage points AND echo(Q2_K) ≥ 30% → **HELD**; gap ≤ 5 points → **REFUTED**;
  otherwise INCONCLUSIVE. Power floor: < 20 valid rows at either rung → UNDERPOWERED.
- **7b.2 SECONDARY, floor-gated:** control floor = mean accepted steps at Q4_K_M ≥ 1.0;
  floor met → HELD if Q2_K mean accepted ≤ 0.5x Q4_K_M, REFUTED if ≥ 1.0x, else
  INCONCLUSIVE.
- **7b.3 must-differ decision rule** as wave 7 (≥50% echo-under-differ =
  instruction-insensitive; ≤20% = instruction-sensitive; <5 valid = UNDERPOWERED).
- **7b.4 descriptives, no bounds.**

## 6. Disconfirmation

As wave 7 §6 verbatim: both families evaluable and 7b.1 REFUTED in both → the cliff is
Qwen-family-specific, §3 and the abstract are qualified accordingly. Additionally,
registered now: if wave 7b is ALSO underpowered in both families, §8 reports that the
task's competence floor excludes every non-Qwen family tested at up to 24B, and the
family-generality limitation is stated as unresolved in the abstract's scope sentence.

## 7. Analysis

`wave7_analysis.py`'s registered logic, extended to the 7b output directories by a
`wave7b_analysis.py` that differs only in paths and family names; no-argument replay,
validity recomputed from coordinates, verdict labels printed by the script.

## 8. Scope

Two more families, one task, one toolchain, one date. Whatever 7b returns, no absolute
band measured here transports anywhere else.
