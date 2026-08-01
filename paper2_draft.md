# The Serving Stack Is Part of the Model: Precision Cliffs and the Limits of Reproducibility in Agent-Runtime LLM Studies

## Abstract

Studies that use a language model as a proposal operator inside a selection loop
increasingly run through managed agent runtimes rather than pinned inference endpoints.
Such runtimes address models by *alias*. We show that this addressing mode is a
measurement hazard, not a bookkeeping inconvenience, because the task class is
demonstrably sensitive to serving precision. We condense a controlled quantization
ladder on a constructive geometry task, where degrading the serving path leaves surface
competence intact while removing the ability to propose a novel construction. We then
report a forensic case study of a top-tier arm addressed only as `opus_alias`, whose
serving signature (completions of 2.8-5.9 s against 75-250 s and 150-1170 s for the
other tiers on the same harness; reported token counts uniform at 49,902-49,906 across
all thirty invocations) and behavioral signature (validity 4/30 against 32/45 and
30/30) jointly indicate an unattested serving path. Two hypotheses — serving-path
degradation, and a genuine property of whichever weights the alias resolved to — cannot
be separated by any experiment runnable from inside the runtime. That impossibility is
the finding. We give an account of what is and is not repairable from inside an agent
harness, and propose a minimum disclosure standard sufficient to surface such cases.

---

## 1. Introduction

The same alias, the same prompt text, the same harness, days apart, produced a
different attractor family, a different validity rate, and reported token counts
uniform to within four tokens across thirty completions. Nobody asked for uniform token
counts and nothing in the experimental design predicts them. They are a property of the
serving path, not of the study, and they were visible only because the harness happened
to log per-invocation duration and usage.

The weights behind an alias are a promise, not a hash. An alias such as `opus` or
`haiku` is resolved at request time by infrastructure the experimenter cannot inspect.
It may resolve to different weights on different days, to the same weights served
through a different decode path, or to a mixture, none of it observable from inside the
runtime. For most applications this does not matter. For a study whose dependent
variable is sensitive to serving precision it matters completely — and the sensitivity
is not hypothetical: we measured it directly.

This paper makes four contributions.

**C1 — the precision cliff.** On a value-sensitive constructive task, serving
precision measurably moves outputs. Degrading a quantization ladder does not degrade
output along a single quality axis; at a specific rung it removes the ability to
propose a *novel* construction while leaving format and geometry intact, a failure
mode invisible to viability and validity metrics.

**C2 — a forensic case study.** A thirty-invocation arm addressed only by alias, in
which serving-signature and behavioral evidence jointly indicate an unattested serving
path, undetectable from inside the runtime that produced it.

**C3 — an impossibility argument.** An agent runtime cannot be made reproducible from
inside itself. We list what is and is not repairable, and show that the irreducible
residue is exactly the class of variables the precision cliff makes consequential.

**C4 — a repair protocol.** The maximal reproducibility such a study *can* achieve —
prompt hashing before sampling, verbatim raw storage, dated alias maps, deterministic
local scoring, hash-locked preregistration — specified and implemented.

---

## 2. Background and task

The benchmark is circle packing: place exactly *N* non-overlapping circles inside the
unit square (or a 1 × *a* rectangle) so that the sum of radii is maximized. It is a
standard target for LLM-guided search systems, and its value for our purpose is that
candidates are *scored by an exact local evaluator* — no model, no judge, no rubric. A
proposal is a list of `[x, y, r]` triples; validity is a finite set of arithmetic
inequalities; the objective is a sum. The evaluator is deterministic and runs offline,
so every source of run-to-run variance lives on the model side of the interface.

*Companion paper.* Our companion paper establishes why this task is precision-sensitive
rather than merely difficult. Proposals concentrate on a small family of
*constructible* templates — a k × k grid of radius 1/(2k), optionally extended with
fillers of radius (√2 − 1)/(2k) — whose values are exact rationals and algebraic
numbers, not approximations reached by optimization. The template a proposer reaches
for is predicted in closed form by k*(N) = ⌊√N + ½⌋, the sign of N − k*² deciding
extension versus truncation; across every held-out cell where that rule and the true
optimum disagree, the rival optimum was reached in 2 of 34 valid samples. Because the
predicted values are exact, a proposal either sits on an anchored construction to
within rendering precision or it does not, and the difference is detectable at 1e-6 —
three orders of magnitude below the ~1e-2 gap between competing constructions. These
behaviors are also tier-dependent: one tier truncates templates, another perturbs and
mixes radii. A study that cannot attest which weights served it cannot attest which
regime it measured.

Several serving-stack variables sit between "the model" as named in a paper and the
tokens that arrive: weight quantization and activation precision; fast-mode or
speculative decode paths; alias rebinding as new dated ids are released; sampling
defaults chosen by the runtime rather than the experimenter; and, in agent runtimes
specifically, an inherited system prompt plus user-level instruction files that are not
part of the task prompt and are not held fixed across time. Only the last is even
nominally under the experimenter's control, and only if they never edit their own
configuration.

---

## 3. The precision cliff

This section condenses the antecedent study's quantization results; no new data.

**Ladder and protocol.** A single quantization family (llama.cpp K-quants, never
mixed) was swept across a fixed proposer with sha256-pinned weight files, five seeds ×
ten generations plus six zero-shot probes per rung, every row live-logged and
integrity-checked locally. The 7B ladder ran fp16 / q8_0 / q4_k_m / q3_k_m / q2_k (250
loop rows + 30 probe rows); the 14B ladder ran q8_0 / q4_k_m / q3_k_m / q2_k and was
re-executed as a batch job with per-candidate coordinates logged.

<!-- CONFLICT: outline names Qwen3-Coder-30B with a 7B "fallback"; executed sweeps used
Qwen2.5-Coder-7B and -14B. Executed ladders are more specific; used here. -->

<!-- CONFLICT: outline's precision table gives Q3_K_M "~3.5" and Q2_K "~2.5" bpw; the
executed run places the cliff between 3.91 and 3.35 bpw for those same rungs. Measured
file figures are more specific; used here. -->

**At 7B, no cliff — a capability floor.** Viability (a proposal that parses and emits
exactly the requested count) was flat across fp16 7/50, q8_0 6/50, q4_k_m 9/50, q3_k_m
7/50, fp16-versus-q3_k_m Fisher *p* = 1.0. The 2-bit rung *inverted*, at 16/50, a
post-hoc effect (*p* = 0.007 uncorrected) attributable to a broader count distribution
that happens to center on the requested count — a format lottery, not a capability
gain. No probe was valid (0/30) and the canonical anchored value was never emitted in
280 opportunities. The mechanism is arithmetic, not semantic: viability reduces to
count accuracy, only 45 of 250 proposals emitted exactly the requested number of
circles, and the modal count from fp16 to q3_k_m was one short. At this scale the
proposer sits below the floor at which precision could matter.

**At 14B, a cliff — in novelty, not in viability.** Viability again did not move
(22 / 22 / 24 / 19 per 50, overlapping intervals) though the scale effect against 7B was
large (87/200 versus 38/200, Fisher *p* = 1.7e-7). What moved was the capacity to depart
from the parent. Coordinate-verified parent echo — a valid proposal whose coordinates
reproduce its lineage's running parent — ran 2/18, 3/20, 3/19 across the upper three
rungs (14% pooled) against 17/18 (94.4%) at 2-bit. A fresh-seed run reproduced the echo
cliff (19/24, 79%, versus 1/17, 6%; Fisher 3.4e-6) while a companion prediction about
improvement counts *failed* at the same rung (3/5 seeds improved, *p* = 0.44). The echo
rate, not the improvement count, is the cliff's replicable signature; we report the
failed prediction rather than the passing one.

**Mechanism, and the cliff is graded.** A must-differ probe held the parent fixed and
explicitly forbade copying: at 2-bit, 5/5 valid outputs were verbatim copies anyway; at
4-bit, 1/5. Instruction-insensitivity, not mere similarity, is what the cliff names. A
parse-only classifier over *invalid* rows found that failing 2-bit rows are majority
near-copies (18/32 and 15/26 across two runs; 26 of 27 circles unchanged) with zero
garbage or truncation at any rung, ruling out a validity-filter explanation of the echo
rate. An independent-weights control — an imatrix-calibrated 2-bit quantization from a
different provider, plus an intermediate IQ2 scheme — placed echo at 75% and 43%,
giving a seed-matched gradient of 6% → 43% → 75-79%. The cliff is therefore
*scheme-mediated*, tracking quantization quality rather than nominal bit width, and
graded rather than binary.

**The instrument that sees it.** All of the above depends on scoring at two tolerances
and declaring the primary one in advance. Proposers print six to eight decimals, so an
eight-decimal tangency misses exactness by roughly 5e-9 and a strict 1e-9 tolerance
reports a valid construction as invalid on rendering grounds alone. Both tolerances are
logged for every row, with 1e-6 primary because it sits far below the ~1e-2 separation
between rival constructions and so cannot manufacture a prediction hit. Choosing
between them after seeing results would have been the easiest way to fabricate the
entire result table, which is why the choice is registered rather than argued.

---

## 4. Forensic case study: the `opus_alias` arm

**Setup.** The study's third tier was requested by the study owner as a specific dated
top-tier model. The agent runtime through which every arm was invoked accepts a model
*alias* only — no dated identifiers — so the request was unsatisfiable and, more
importantly, *undetectably* unsatisfiable: nothing in the runtime's response surface
reports which weights served a call. We therefore label the arm `opus_alias` throughout
and never attach a version number to it. Thirty invocations were run, ten each at three
held-out cells (N = 13, 21, 31), under a bare prompt identical to the other tiers, with
predictions registered in `arm_o_preregistration.txt` (sha256 21171…738) before any
sampling.

**Serving signature.** Completions returned in 2.8-5.9 s. On the same harness and task
the other two tiers returned in 75-250 s and 150-1170 s — one to two orders of
magnitude slower for nominally smaller models. Reported token counts were uniform at
49,902-49,906 across all thirty completions: a four-token spread over thirty
independent generations at three different problem sizes. Neither observation is
explicable by the experimental design; both are consistent with a fast-mode serving
path, which at the run date was offered on three other top-tier versions and *not* on
the version the study owner asked for. The anomaly is consistent rather than
intermittent, holding for all thirty invocations across all three cells.

**Behavioral signature.** Validity was 4/30 (13%), against 32/45 (71%) and 30/30
(100%) for the two other tiers on overlapping cells. The failures are geometric, not
formatting: 24 of 26 invalid rows overlap, with errors far outside rounding noise — at
N = 31, edge strips at r = 0.03 sitting 0.138 from a grid circle of radius 1/6 that
requires 0.197 — and two rows padded to the requested count with zero-radius circles,
caught by a non-positive-radius gate. The attempted constructions also shifted family:
quarter-circle corners with Apollonius-style fillers at N = 13 (10/10 the same
family), mixed-radius grids with corner and edge fillers at N = 21, a coarse grid with
border strips and interior fillers at N = 31. Each is *more* ambitious than the
grid-plus-filler templates the other tiers produce, and each is executed with broken
tangencies most of the time. The four valid samples score below the trap value the weak
tier reliably hits. The registered disconfirmation condition — regression toward the
trap — did not occur; the arm fell off a validity cliff attempting a harder family.
Three of four registered predictions are marked NOT EVALUABLE, because scoring a tier
comparison across a validity collapse would be dishonest.

**Two hypotheses.** The first is *serving-path degradation*: a fast decode path erodes
the arithmetic precision needed to close a tangency while leaving the choice of
construction — the ambition — intact. That would echo §3's finding from a new
direction, since it is precisely the quantization cliff's signature: surface competence
preserved, constructive competence removed. The second is a *genuine tier property*:
whatever weights the alias resolved to really do attempt harder constructions and
really do execute them less reliably — an inverted U in constructive reliability as
nominal capability rises.

Both hypotheses predict every observation we have, and they are not separable by any
experiment runnable from inside this runtime. More sampling does not separate them: the
anomaly is uniform, so more of it is more of the same. Prompt variation does not, because
both act on execution rather than intent. Timing instrumentation does not, because the
serving path is not a variable we can set. Separation requires invocation against
*pinned weights*, which requires an interface the runtime does not expose. This is not
a gap in our design that a reviewer could ask us to close; it is a property of the
harness class. **That is the finding.** The arm is logged in full, excluded from the
tier ladder, and carries the alias caveat in every mention.

---

## 5. What is repairable and what is not

The repairs below are implemented in `arm_f_repro.py` and its companions, not merely
proposed. Prompt text is pinned and SHA-256 hashed *before any sampling*, one hash per
problem size, so it cannot be silently edited after seeing outputs. Every raw output is
stored verbatim, parsed or not. The run date is recorded with the alias → dated-id
mapping in force on that date (`RUN_DATE` and `ALIAS_MAP` in the harness header) —
provenance without being a pin. Scoring, validity and construction classification are
deterministic and local. Predictions with explicit falsifiers and a disconfirmation
rule are written into the harness header before the first invocation and externally
timestamped.

What cannot be repaired from inside is short and consequential. Sampling parameters are
not exposed, so temperature, top-p and top-k are unknown and unfixable — and they are
the parameters that shift the output distribution most. The alias → weights binding is
a promise, not a hash: the alias can be repointed at any time and past runs cannot be
re-executed against the weights that produced them. The subagent inherits a system
prompt and user-level instruction files that are not part of the task prompt and not
held fixed across time. And the serving path is not attested at all — no flag
distinguishes a fast-mode decode from a standard one, the exact variable §4 needed and
could not obtain.

| Item | Repairable? | Mechanism | Residual risk |
|---|---|---|---|
| Prompt text | Yes | SHA-256 pre-sampling, one hash per cell | None if hash published |
| Raw outputs | Yes | Verbatim storage of every invocation, failures included | Storage only; no inference risk |
| Scoring / classification | Yes | Deterministic local evaluator, offline | Tolerance choice — mitigated by dual reporting |
| Predictions | Yes | Hash-locked prereg with falsifiers, externally timestamped | Registration errors — disclose, do not amend |
| Model identity | Partial | Alias + run date + dated-id map in force that date | Alias may have been repointed; map is documentation, not a pin |
| Sampling parameters | No | — | Unknown distribution shift between runs |
| Alias → weights binding | No | — | Silent model substitution; past runs unrepeatable |
| Serving path (fast-mode) | No | — | §4-class confound, undetectable without side channels |
| Inherited system / user prompt | No | — | Unlogged context drift across time |

---

## 6. Implications

Every LLM-evolution, best-of-N and iterative-refinement study run through a managed
agent harness inherits this list — FunSearch-style program-evolution loops,
self-refinement pipelines, and any tier-ladder comparison naming "the model" by alias.
Such studies are not thereby wrong. They are unrepeatable in a specific and
now-demonstrable way, and §3 establishes that the unrepeatable variables are ones the
outcome is sensitive to. The correct response is disclosure, not retraction.

**A minimum disclosure standard.** Four items, all implemented here, none requiring
vendor cooperation, none exposing anything proprietary:

1. **Alias, run date, and the alias → dated-id map in force on that date.** Two lines
   of the harness header. It pins nothing, but converts an unfalsifiable claim ("we
   used model X") into a dated, checkable one.
2. **Prompt hashes computed before sampling.** One SHA-256 per prompt variant, in the
   artifact that runs the study, closing the largest silent degree of freedom in LLM
   experiments at zero cost.
3. **Verbatim raw outputs, including failures.** Parse failures, malformed rows and
   runtime rejections are data; dropping them silently is how validity rates get
   inflated. In our own logs, five invocations rejected by a concurrency cap *before
   reaching a model* would have understated validity by 17% had they been counted as
   proposer failures.
4. **Serving-signature statistics as an anomaly canary.** Per-invocation wall-clock
   duration and reported token counts, logged and reported as distributions. This is
   the item the field does not currently do, and the one that caught §4. A four-token
   spread across thirty completions is visible in a histogram; latency an order of
   magnitude off the neighbouring tier is visible in a sorted list. Neither reveals
   anything about the vendor's infrastructure; both are already returned to the caller.

**What vendors could expose.** A weights digest returned with each completion would
make the alias → weights binding attestable. A sampling-parameter echo would make an
unset temperature auditable rather than unknown. A serving-path flag — one boolean
distinguishing a fast or speculative decode from the standard path — would have
separated §4's two hypotheses outright. Each is a single field in a response object.

---

## 7. Related work

The reproducibility-in-ML line establishes that reported results depend on undocumented
implementation and environment detail, and the numerical-nondeterminism and
batch-invariance literature establishes that even a fixed model on fixed hardware does
not return bit-identical outputs under varying batch composition [SLOT: systems-lit].
Our contribution there is not the observation of variance but the *addressing mode*:
the alias interface makes the relevant variable unaddressable rather than merely
uncontrolled. The quantization-effects literature measures degradation on static
single-shot benchmarks [SLOT: systems-lit]; §3 places that gradient inside a selection
loop and finds the axis it moves — novelty — is not the axis those benchmarks score.
Evaluation-variance studies quantify seed and prompt sensitivity [SLOT: systems-lit];
§5's residue is orthogonal to both, because it cannot be averaged out by more seeds.

For benchmark lineage, arXiv 2605.29268 studies the same objective (26 circles in the
unit square) under LLM-guided program synthesis with an explicit best-of-N comparator;
its asymmetric-proposal-mass account is the complement of our companion paper's
attractor account. The saturation of reported values here — AlphaEvolve at 2.635 and a
cluster of later systems at 2.635983283, 2.63598308 and 2.636 (ShinkaEvolve; HELIX,
2603.07642; GigaEvo, 2511.17592; AdaEvolve, 2602.20133; SeaEvo, 2604.24372;
ThetaEvolve, 2511.23473) — is itself an argument for this paper: a field reporting
agreement at the eighth decimal while addressing its models by alias is reporting
agreement it cannot attest.

On the tier behavior in §4, Zhou et al. (Nature, 2024) report that larger and more
instructable models attempt more and err more in question answering; our observation
is a constructive-regime instantiation of the same shape, cited as corroboration
rather than precedent. On preregistration, hash-locked externally-timestamped
registration of LLM experiments is an emerging standard (HindsightBench, 2607.18867,
concurrent; 2607.07184; 2606.27687; 2606.11217); we claim only the combination —
hash-locked registration of *exact closed-form point predictions* evaluated in a
held-out container.

---

## 8. Limitations

We observed a single vendor and a single agent runtime. Whether other managed runtimes
expose more (a dated identifier, a sampling echo) is an empirical question we did not
test; a runtime that exposes more would weaken §5's generality without touching §4's
specific case.

The serving-signature evidence is circumstantial *by construction*. That is the thesis,
but it deserves plain statement rather than a hedge: we infer a serving path from
latency and token-count distributions because no direct observation is available. Were
one available, §4 would be a bug report rather than a paper. A reader who declines the
inference is left with the second hypothesis, which is equally unattestable, and §5's
impossibility argument stands either way.

The `opus_alias` arm is n = 30, and the anomaly, though uniform across all thirty
invocations and all three cells, comes from one batch window. A second serving-signature
snapshot of the same alias at a later date is the highest-value follow-up: if the
signature shifts with no alias change, §4 gains a second independent data point; if it
does not, the constancy is itself informative. Finally, §3's data comes from a
locally-served open-weights ladder, not from the alias-addressed runtime. The bridge is
an inference — that serving precision matters for this task — supported by §3's
mechanism rather than measured inside the runtime, which is exactly the measurement §5
says cannot be made.

---

## Claim → evidence map

| claim | source |
|---|---|
| cliff data | paper-0 combined md §5.x [condensed in §3] |
| opus_alias forensics | arm_f_raw.json opus rows, STATE.md §8-8b |
| durations/token uniformity | task usage blocks in session transcript, logged STATE.md §8b |
| repair protocol | arm_f_repro.py header + prereg files |
| alias-map provenance | ALIAS_MAP + RUN_DATE in arm_f_repro.py |
