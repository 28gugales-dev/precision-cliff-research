# Wave 7 preregistration — does the echo cliff survive a change of model family?

Status: LOCKED at push time. The lock is the SHA-256 of this file published beside the
runners in the public Kaggle kernels named in §3, pushed before any row is sampled.
Author field open, same caveat and same cost as waves 3-5.

## 1. What this wave exists to kill

Every GGUF result in paper 2 — the §3 ladders, the fresh-seed replication, the IQ2 pair,
the dispersion probes, waves 3 and 5 — comes from **one model family**: Qwen2.5-Coder
(14B, with a 7B contrast). The referee's cheapest remaining sentence is: *the echo cliff
is a Qwen artifact — one family's tokenizer, one family's instruction tuning, one
quantization interaction — not a property of 2-bit inference.* No experiment in either
paper touches this. Wave 7 does, with the only manipulated variable being the model
family: two new families run the **byte-identical** circle-packing protocol of the
fresh-seed wave (`kaggle_precision_sweep_14b_fresh.py`) — same prompt text, same
sampling parameters, same 5-seeds-x-10-generations generation-major loop, same
6-decimal-place order-insensitive echo definition, same evaluator, same must-differ
probe block.

Circle packing, not Heilbronn or LABS, deliberately: it is the one task in this corpus
where the reference rung has **demonstrated** it can climb (15/50 and 14/50 accepted
steps on the registered and fresh Qwen ladders). Waves 3 and 5 both died on their
control-arm floors because their tasks were too hard for the proposer at any precision.
Wave 7 does not re-test task generality; it tests family generality on the task where
the phenomenon is best established.

## 2. Conditions

Two families, two rungs each, chosen before any sampling:

| kernel | repo | files (verified present and ungated 2026-08-08 via unauthenticated HfApi listing) |
|---|---|---|
| llama | `bartowski/Meta-Llama-3.1-8B-Instruct-GGUF` | `Meta-Llama-3.1-8B-Instruct-Q2_K.gguf`, `Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf` |
| gemma | `bartowski/gemma-2-9b-it-GGUF` | `gemma-2-9b-it-Q2_K.gguf`, `gemma-2-9b-it-Q4_K_M.gguf` |

SHA-256 and byte length of each weight file are recorded in provenance at download
time, as in every prior ladder. Seeds: llama `[7101, 7102, 7103, 7104, 7105]`, gemma
`[7201, 7202, 7203, 7204, 7205]` — grep of every runner in `sec3_artifacts/runners/`
confirms no prior run sampled any of them. Budget per family: 2 rungs x 5 seeds x 10
generations = 100 loop calls + 2 x 10 must-differ probes = 120 generations.

**These are 8B/9B models, not 14B.** The paper's own 7B ladder shows the cliff is not
monotone in model size (viability inverts). Wave 7 therefore registers **within-family
contrasts only**: each family is its own control, Q4_K_M against Q2_K under identical
everything. No cross-family comparison and no comparison against Qwen's absolute rates
is registered; §5's rule against pooling is part of this registration.

## 3. External timestamp

Each family's runner is pushed as a **public Kaggle kernel** (account `ANON-KAGGLE-OWNER`,
kernels `precision-sweep-llama31-8b-wave7` and `precision-sweep-gemma2-9b-wave7`)
before any row is sampled. This file's SHA-256 is printed in each runner's header
region and the file itself is pushed as a public Kaggle dataset
(`ANON-KAGGLE-OWNER/wave7-prereg-families`) before execution. Version history is the
timestamp.

## 4. Prior state, disclosed before sampling

No Llama-3.1 or Gemma-2 output of any kind exists anywhere in this corpus: no pilot,
no draft rows, no discarded run. Every prediction below is written blind to how these
families behave on this task at any precision. The only priors are Qwen's: Q2_K
coordinate echo 94% / 60% / 51% across the three 14B circle-packing waves against
15% / 10% / 24% at Q4_K_M, and a 7B family member whose Q2_K rung went *more* viable,
not less. Given that inversion, family transfer is genuinely uncertain — which is why
this wave exists.

## 5. Registered predictions and decision rules

All computed per family, independently. **No pooling across families**, and the
reporting rule for a split outcome is fixed here: one family showing the contrast and
the other not is reported as **FAMILY-DEPENDENT**, verbatim, in §3.6 and wherever the
cliff's generality is discussed — not as a replication with a caveat.

**7.1 — PRIMARY, echo contrast, NOT floor-gated.** Among valid rows (exactly 26
circles, all inside, no overlap), with echo = 6 dp order-insensitive coordinate-set
equality against the lineage's **running parent**:

- **HELD** if echo(Q2_K) − echo(Q4_K_M) ≥ **15 percentage points** AND echo(Q2_K) ≥ 30%.
- **REFUTED** if echo(Q2_K) − echo(Q4_K_M) ≤ **5 percentage points**.
- Otherwise **INCONCLUSIVE**.
- **Power floor:** fewer than **20 valid rows at either rung** → **UNDERPOWERED**, no
  branch claimed. (An 8B model at Q2_K may fail by emitting garbage rather than by
  copying; tiny valid denominators must not pass bounds by noise. The Qwen 7B ladder's
  worst rung produced 7 valid rows in 50 — this floor is set above that failure mode.)

The wave-3 lesson is applied structurally: **no absolute band imported from another
task or family.** The 15-point gap is the within-family directional signature; the 30%
conjunct exists so that a 16%-vs-1% pattern — real gap, negligible copying — is not
claimed as a cliff.

**7.2 — SECONDARY, search progress, floor-gated.** Mean accepted hill-climb steps per
lineage (strict improvement of sum-of-radii over running parent):

- **CONTROL-ARM FLOOR:** if mean accepted steps at Q4_K_M < **1.0** for a family, 7.2
  is **UNINFORMATIVE for that family** — the reference rung could not climb, and "the
  rungs do not differ" cannot be separated from "the model is too weak for the task".
  7.1 is expressly NOT gated by this floor (wave 3 precedent: echo stayed informative
  through a fired floor).
- Floor met: **HELD** if Q2_K mean accepted ≤ **0.5 x** Q4_K_M mean accepted; **REFUTED**
  if Q2_K mean accepted ≥ Q4_K_M mean accepted; otherwise INCONCLUSIVE.

**7.3 — Must-differ probe, decision rule, both outcomes informative.** 10 single-shot
invocations per rung per family, baseline parent shown, prompt explicitly forbidding
an unchanged packing (byte-identical to the fresh wave's probe). At Q2_K:

- echo rate under the must-differ instruction ≥ **50%** → copying is
  instruction-insensitive (degraded novelty), matching Qwen's 5/5.
- ≤ **20%** → instruction-sensitive; that family's loop echo is better explained as
  default behaviour, and §3.6's mechanism discussion says so for that family.
- Between: inconclusive. Fewer than 5 valid probe outputs: UNDERPOWERED.

**7.4 — Descriptives, no bounds:** viability and validity per rung, zero-score/template
fraction, per-seed best scores, completion-token distributions, wall-clock. Reported
whatever they show.

## 6. Disconfirmation clause

If **both** families are evaluable on 7.1 (no UNDERPOWERED) and 7.1 is **REFUTED in
both**, then the echo cliff is a Qwen-family phenomenon until shown otherwise, and
paper 2 is edited accordingly: §3's cliff claims acquire the qualifier "in the
Qwen2.5-Coder family" **including in the abstract**, and §3.6's generality discussion
opens with this wave's result. We commit to that edit before knowing the outcome.

A split outcome (one HELD, one REFUTED) triggers the FAMILY-DEPENDENT reporting rule
of §5 — scope narrows to "some model families", not to Qwen alone, and neither family
is dropped from the report.

## 7. Analysis, fixed in advance

A no-argument replay script (`wave7_analysis.py`) recomputes every echo, validity
verdict and score from the stored coordinate lists — the ledger's convenience fields
are never load-bearing — verifies agreement with the kernel state files, computes each
label above per family, and prints it. Verdict labels are printed by the script, not
written by us. Descriptive two-sided Fisher tests on the echo contrasts are reported
as unregistered descriptives.

## 8. Scope: what this wave cannot say

Two families at one size class each, one task, one quantization toolchain (llama.cpp
GGUF, bartowski conversions), one date, Kaggle T4/P100 hardware. A held 7.1 in both
families supports "the cliff is not Qwen-specific"; it does not establish universality
across sizes, toolchains (GPTQ/AWQ), or tasks — and after wave 3, no band measured
here will be treated as transportable anywhere else.
