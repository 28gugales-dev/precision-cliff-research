# Served Precision Is Part of the Model: A Quantization Cliff in Novelty, and the Limits of Reproducibility in Agent-Runtime LLM Studies


## Abstract

Quantizing a proposer's weights can leave every metric a discovery loop watches unchanged
while removing the one capability the loop exists to exercise. On a constructive geometry
task, degrading served quantization moves viability and validity by no detectable amount at
14B — non-rejection at n = 50 per rung, not demonstrated equivalence, and at 7B viability
instead *inverts* — while at the 2-bit rung the model very largely stops proposing anything
new: coordinate-verified parent-echo among valid outputs reaches 94% (17/18), replicates at
79% (19/24) on five never-sampled seeds, and survives an explicit instruction not to copy in
5 of 5 valid probe outputs. The failed proposals are not garbage — they are coherent, well-formed near-copies,
which is why every pass/fail instrument reports health. A fixed-parent control we run
against ourselves shows the loop comparison is inflated by parent quality and puts the
matched contrast at 33% (6/18) against 92% (11/12); the effect's direction and its 2-bit endpoint survive
that control, its spread does not, and a registered scheme-versus-bit-width control returns
its inconclusive branch, so what is established is an effect of *this file's* quantization,
replicated on an independently produced Q2_K.

This matters for measurement because studies that use a language model as a proposal
operator increasingly run through managed agent runtimes rather than pinned inference
endpoints, and such runtimes address models by *alias*. Which quantization is served is one
of several things an alias leaves unattested — and it is now a variable the dependent
measure is known to be sensitive to. Our ladder holds the inference stack fixed and varies
only the SHA-256-pinned weight file, so it measures served-weight precision, not a
decode-path effect; whether other serving-stack variables behave alike is a hypothesis we
raise rather than a result we establish.

We then report a forensic case study of a top-tier arm addressed only as `opus_alias`,
whose serving signature (2.8-5.9 s completions over the first twenty invocations and 3-9 s
across all thirty, against 75-250 s and 150-1170 s for the other tiers on the same harness)
and behavioral signature (validity 4/30 against 30/30 and 50/60, recomputable in full)
together *mildly favour* an unattested serving path without deciding it. The latency
figures are working-log ranges and cannot be checked against the released artifact, which
is itself an instance of what we argue for. Two hypotheses — serving-path degradation, and
a genuine property of whichever weights the alias resolved to — are not separable by any
experiment that can *attest* the serving path, because no observable the runtime exposes
reports which decode path served a call. That unattestability, not a blanket impossibility
of behavioral discrimination, is what the case study establishes, and we name the
experiments that would still narrow it. We close with an account of what is and is not repairable from inside an agent
harness, including the places where this paper fails its own standard, and endorse an
existing reporting checklist with one addition aimed at exactly this hazard.

---

## 1. Introduction

The same alias, the same prompt text, the same harness, days apart, returned completions
one to two orders of magnitude faster than nominally *smaller* models on the same task,
and produced valid geometry in 4 of 30 attempts where those smaller models produced it in
30 of 30 and 50 of 60. Nothing in the experimental design predicts either. They are
properties of the serving path, not of the study, and the first was visible only because
the harness happened to log per-invocation duration.

The weights behind an alias are a promise, not a hash. An alias such as `opus` or
`haiku` is resolved at request time by infrastructure the experimenter cannot inspect.
It may resolve to different weights on different days, to the same weights served
through a different decode path, or to a mixture, none of it observable from inside the
runtime. For most applications this does not matter. For a study whose dependent
variable is sensitive to which quantization is served it matters completely — and the
sensitivity is not hypothetical: the antecedent study measured it directly, and found it on an axis
that pass/fail metrics cannot see.

This paper makes four contributions.

**C1 — the precision cliff, in novelty rather than viability.** On a value-sensitive
constructive task, served-weight quantization measurably moves outputs — but not along the axis
the founding hypothesis predicted. Degrading a quantization ladder leaves viability and
validity statistically flat; at a specific rung it removes the ability to propose a
*novel* construction while leaving format and geometry intact. The failure mode is
invisible to viability and validity metrics, which is why it went unreported until the
antecedent study looked at coordinates rather than scores.

**C2 — a forensic case study.** A thirty-invocation arm addressed only by alias, in which
serving-signature and behavioral evidence together *mildly favour* an unattested serving
path without deciding it — and in which the favouring evidence, the latency gap, is a
working-log observation the released artifact cannot check.

**C3 — a non-identifiability argument, conditioned on the runtime we observed.** For the
agent runtime studied here, the observable set exposed per invocation does not contain
any variable that attests the serving path. We state the observable set explicitly, show
which hypothesis pairs it separates and which it does not, and name the experiments that
would discriminate the two readings behaviorally — two runnable inside the runtime, one
requiring a pinned endpoint outside it — none of which we ran.
The claim is conditioned on one vendor and one runtime (§8); a runtime that exposes a
serving-path flag or a weights digest would falsify it for that runtime.

**C4 — a repair protocol, including its own failures.** The maximal reproducibility such
a study *can* achieve — prompt hashing before sampling, verbatim raw storage, dated alias
maps, deterministic local scoring, hash-locked preregistration — specified, implemented,
and audited against itself: three of the five repairs are fully implemented in the
released artifact, and we name the two that are not.

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

*The instrument, and why the tolerance is registered.* The companion's evaluator scores
every row at **two** tolerances and declares the primary one in advance. Proposers print
six to eight decimals, so an eight-decimal tangency misses exactness by roughly 5e-9 and
a strict 1e-9 gate reports a correct construction as invalid on rendering grounds alone.
Both tolerances are logged for every row (`valid`, `valid_strict_1e9` in
`arm_f_repro.py`), with 1e-6 primary because it sits far below the ~1e-2 separation
between rival constructions and so cannot manufacture a prediction hit. Choosing between
them after seeing results would have been the easiest way to fabricate a result table,
which is why the choice is registered rather than argued — and why §4 reports its
validity figures at both.

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

This section condenses the executed quantization results of the antecedent study
(`precision-cliff-paper-combined.md`: protocol in its §3.4, results in its §5.9,
summary in its contribution 6, scope caveats in its §6). No new *ladder* data is reported
here: every rung figure comes from the antecedent's runs. One dataset appears here that the
antecedent does not analyse — the fixed-parent dispersion probe reported below, which we
bring in because it controls a confound in the antecedent's own echo measurement.

**Every figure in this section is recomputed from the raw candidate ledgers, not copied
from the antecedent prose.** `sec3_ladder_repro.py`, released with this paper, replays
each `(quantization, seed)` lineage from the coordinate-logged jsonl, reconstructs the
running parent under the loop's own hill-climb rule, and re-derives the viability,
validity, echo, per-seed, must-differ, invalid-row and Fisher figures below. The ledgers
are `candidates_precision_14b.jsonl` (re-execution, 200 rows), `..._fresh.jsonl` (100),
`..._iq2.jsonl` (100) and the two `mustdiffer_*.jsonl` files, each with a
`provenance.json` recording the SHA-256 and byte length of every weight file served.

**Inferential status of every *p*-value in this section.** All are two-sided Fisher exact
tests. All candidate-level contrasts — *p* = 0.007, 1.7e-7, 3.4e-6 and 0.017 — treat rows
as independent when they are nested within lineages sharing five seeds across rungs, so
each overstates the evidence; the antecedent study's appendix declares them not part of
any claim, and we adopt that status here for all four rather than for one. The seed-level
tests (*p* = 0.001, 0.44) do not have that defect but run on five seeds. No multiplicity
correction is applied across the section's eight tests and none should be read as
implied: at the nine tests this section reports, a Bonferroni threshold is 0.05/9 = 0.0056,
which neither *p* = 0.017 nor *p* = 0.007 meets.
The figures are reported as descriptive effect sizes with exact tails attached, not as
hypothesis tests supporting the claims, which rest on the registered predictions instead.

Relatedly, "viability is flat" and "validity does not move" throughout this section report
*non-rejection*, not demonstrated equivalence. No equivalence test was run and n = 50 per
rung is not powered for one: the Wilson interval on 7/50 is [0.070, 0.262], compatible
with a fourfold ratio to the highest rung. The claim these support is only that the
degradation is not *visible* on those axes at this sample size — which is the paper's
point about instruments, but it is not proof of invariance.

Two notes for a replicator. First, the running parent advances only on *strict* score
improvement; advancing it on ties instead lets it drift and undercounts echo by roughly a
quarter at the 2-bit rung, which is the one place a reimplementation is likely to diverge.
Several Q2_K lineages never improve at all, so their parent remains the seeded 6 × 5 grid
for all ten generations. Second, one figure below does not reproduce exactly: the
near-copy fraction among invalid IQ2_M rows is reported as 2/22 and our replay of the
stated definition returns 1/22. The discrepancy is one row at a definitional boundary
("26 of 27 circles unchanged"), affects no claim, and we record it rather than quietly
restating the number.

**Ladder and protocol** (combined §3.4). Proposers: **Qwen2.5-Coder-7B-Instruct** and
**Qwen2.5-Coder-14B-Instruct**, official Qwen GGUF releases, served locally through
llama.cpp on 2 × NVIDIA T4, with a SHA-256 hash of each weight file recorded in the run's
provenance log. Task: the same benchmark as §2 at **N = 26 in the unit square**; every
lineage starts from the same seeded valid parent, a trivial 6 × 5 grid scoring 0.900, so
every lineage has a floor. Sampling: temperature 0.8, top-p 0.95, a deterministic
per-call seed, at most 1,200 new tokens in a 4,096-token context, one bare chat
completion per proposal — this condition is *not* agentic, which removes the
orchestration layer as a confound. Per rung: 5 seeds × 10 generations (50 loop
candidates) plus 6 zero-shot probes. The 7B ladder ran five rungs — FP16 (16.0 effective
bits per weight), Q8_0 (8.5), Q4_K_M (4.85), Q3_K_M (3.91), Q2_K (3.35) — for 250 loop
rows and 30 probes; the 14B ladder ran the four quantized rungs (FP16 omitted: the
~29.5 GB file does not fit 2 × T4) for 200 loop rows and 24 probes. Every candidate is
logged live at evaluation time (`reconstructed:false`) and scored by the same
deterministic evaluator, at the 1e-6 boundary and overlap tolerance used study-wide
(combined §3.1). The main ladder is a single quantization family — llama.cpp K-quants,
never mixed; the sole deliberate departure is the IQ2 control below.

Effective bits per weight are llama.cpp's nominal figures, and they *co-vary with the
quantization algorithm* rather than indexing it independently. Everything in this section
is therefore a **Q2_K claim, not yet a bit-width claim** — a distinction the IQ2 control
below turns from a caveat into a measurement.

**At 7B the founding hypothesis failed, and the antecedent study says so** (combined
§5.9). Viability — a proposal that parses and emits exactly the requested count — was
flat from FP16 down through Q3_K_M, a 4× compression: 7/50, 6/50, 9/50, 7/50, with all
pairwise Wilson intervals overlapping and FP16 versus Q3_K_M at Fisher *p* = 1.0. The
precision threshold the project was founded on is absent over the entire usable GGUF
range at this scale. The 2-bit rung *inverted*, at 16/50; the comparator that produces
its *p*-value is the pooled upper four rungs (16/50 versus 29/200, *p* = 0.007
uncorrected, candidate-level), not FP16 alone (16/50 versus 7/50 gives *p* = 0.056, not
significant). Both contrasts are post-hoc and disclosed as such. The mechanism is
arithmetic rather than semantic and was measured directly: viability here reduces almost
entirely to count accuracy — of 250 proposals only 45 contained exactly 26 circles and
153 contained 24-25 — and the modal count from FP16 through Q3_K_M is one or two short of
the parent shown to the model, while Q2_K's count distribution is *broader* (tail out to
30-36) and happens to center on the target. Quantization noise did not improve the model;
it widened a distribution that was biased just below an arbitrary acceptance point. Token
truncation is ruled out directly: no 24-25-circle proposal came near the 1,200-token cap
(maximum 687 tokens, all closing their list bracket naturally). The antecedent study
names this the **format lottery** and flags it rather than claiming it. No probe was
valid at any rung (0/30) and the canonical anchored value was never emitted in 280
opportunities (250 loop rows + 30 probes); the best score in the whole 7B sweep, 1.800,
sits 29% below the canonical anchored value for this benchmark, 2.5414, which the
frontier-tier arms treat as a floor. At this scale the
proposer sits below the floor at which precision could matter.

**At 14B, a cliff — in novelty, not in viability** (combined §5.9). Scaling lifts the
format floor: viability runs 22/50, 22/50, 24/50, 19/50 across Q8_0 / Q4_K_M / Q3_K_M /
Q2_K, all four intervals overlapping, against 87/200 versus 38/200 pooled for the
scale contrast (Fisher *p* = 1.7e-7). That 38/200 is **rung-matched** to the 14B ladder —
the 7B sweep's four quantized rungs, excluding FP16 and including Q2_K — and is a
different subset from the 29/200 used for the format-lottery comparator above; the two
pooled denominators are not interchangeable. Validity likewise does not move (18/50,
20/50, 19/50, 18/50), and recall stays absent (probes 0/24; best score 1.625, 36% below
that same 2.5414 anchor). What moved was the capacity to depart from the parent. **Coordinate-verified
parent echo** — a valid output whose emitted circle set is identical, order-insensitive at
the logs' six-decimal precision, to its lineage's running parent — ran 2/18, 3/20, 3/19
across the upper three rungs (8/57 pooled, 14%) against **17/18 (94%) at Q2_K** (two-sided
Fisher *p* = 5.7e-10, carrying the same nesting caveat as every candidate-level figure in
this section, and superseded in magnitude by the fixed-parent control below), i.e.
between 3.91 and 3.35 nominal effective bits. Every Q2_K seed echoes at or above half its
valid rows (per-seed 7/7, 4/4, 4/4, 1/1, 1/2 — the last is 50%, not a majority, and we
state the vector rather than round it up) against at most 2 echoes per seed on any upper
rung. The effect is therefore not carried by one lineage, though it is thinly spread: 15
of the 17 echoes come from three seeds, and the remaining two seeds contribute only 1 and
2 valid rows, so the per-seed denominators are too small to support more than the
qualitative point. The seed-level improvement contrast (15/15 seeds improving
above the boundary versus 1/5 below, Fisher *p* = 0.001) is post-hoc and comes from a
single sampling run; the candidate-level echo contrast is descriptive only, because rows
are nested within lineages and the same five seeds recur across rungs.

**Data loss, and a coordinate-verified re-execution** (combined §3.4, §5.9). The original
14B run completed but its hosting session expired before the output directory was
retrieved, destroying the per-candidate jsonl, probe texts and checkpoints. What survived
was the verbatim live console log — one line per candidate, printed at evaluation time —
which records scores and viability flags but never recorded emitted coordinates, so the
original echo metric could only be *inferred* from exact score identity with the parent.
The rung was therefore re-executed end to end against the same SHA-256-pinned weights,
seeds, prompts, sampling parameters and generation order, as a platform batch job that
saves its output automatically, with three logging-only additions: per-candidate
coordinates, redundant console echo, and quantitative predictions embedded in the runner
source before execution. This is a **re-execution, not a replication**: llama.cpp's seeded
sampling is deterministic on fixed weights and hardware, so it regenerates the same 224
outcomes rather than drawing fresh ones — which means predictions about console-logged
quantities were guaranteed to hold and carry no evidential weight. The only falsifiable
predictions were the coordinate-level ones, about information the console log never
contained: whether score-matches were verbatim copies or same-sum rearrangements. Both
held (Q2_K echo ≥ 60%: observed 94%; each upper rung ≤ 35%: observed 11-16%), and the
check had visible discriminating power — it *refuted* the original score-inferred
estimates on the upper rungs, reclassifying 4 of 12 presumed echoes as rearrangements and
making the verified cliff sharper (14% → 94%) than the inferred one (21% → 94%). We
return to this episode in §5: it is the cleanest illustration in the corpus of a repair
that works because the pinned side of the stack *is* pinnable.

**Fresh seeds replicate the echo cliff, and a registered prediction fails** (combined
§5.9). The same protocol was then run on five never-before-sampled seeds (2222, 3333,
5555, 7777, 9999) at the two decisive rungs, 100 new coordinate-logged candidates, with
every registered prediction falsifiable because the draws are genuinely new. Echo
replicates: **19/24 (79%) at Q2_K against 1/17 (6%) at Q4_K_M** (Fisher *p* = 3.4e-6,
candidate-level and descriptive), every fresh Q2_K seed again majority-echo (4/5, 4/5,
5/6, 2/2, 4/6), both registered echo bounds held. The registered *improvement-count*
prediction failed: it forecast ≤ 2/5 Q2_K seeds improving past the seeded baseline, and
3/5 did, against 5/5 at Q4_K_M — a seed-level Fisher exact test on 3/5 versus 5/5, two
sided, giving *p* = 0.44. The antecedent study reports the failure plainly and demotes the
improvement collapse to a fragile correlate: the **echo rate**, not the binary improvement
count, is the cliff's replicable signature. The *p* = 0.001 seed-level figure quoted
earlier in this section is the superseded one, and no claim in this paper rests on it.

**Mechanism: the cliff survives an explicit prohibition** (combined §5.9). A registered
must-differ probe held the parent fixed and appended one demand to the otherwise-identical
prompt: the output must not be identical to the parent, at least three circles must
change, and returning it unchanged counts as failure. At Q2_K the model returned a
coordinate-identical copy in **5 of 5 valid outputs**; at Q4_K_M, 1 of 5, with all four
non-echo outputs scoring above the parent. Under the decision rule registered before the
run (≥ 50% echo → instruction-insensitive; ≤ 20% → instruction-sensitive; between,
inconclusive — both bounds inclusive, and the rule's registered subject is Q2_K alone, so
Q4_K_M's 1/5 is reported without a branch rather than assigned one) Q2_K falls in the
instruction-insensitive branch at the maximum possible rate, while format adherence
stays intact — the model is not ignoring instructions wholesale, it is specifically unable
to produce a differing valid packing. At n = 5 valid outputs per rung this is strongly
suggestive rather than definitive, and the antecedent study labels it so.

**Scheme-graded, not bit-graded: the IQ2 control** (combined §5.9). Because effective bits
co-vary with the algorithm, a registered control ran two independently produced 2-bit-class
quantizations from a third-party imatrix-calibrated repository, SHA-256-pinned, under the
identical protocol: **imatrix Q2_K** (~3.4 b/w) and **IQ2_M** (~2.7 b/w — *fewer* bits,
different scheme family, same calibration). Echo: 24/32 (75%) for imatrix Q2_K against
12/28 (43%) for IQ2_M (*p* = 0.017), with must-differ echoes 6/8 versus 0/2 and seeds
improving 3/5 versus 5/5. Three readings, all as registered. The cliff replicates on an
independently produced Q2_K at essentially the official file's matched-seed rate (75%
versus 79%), so it is not an artifact of one weight file. The registered bit-width
question returns its **inconclusive branch** — 43% falls between the thresholds that would
have generalized the cliff to the 2-bit class (≥ 60%) or cleanly attributed it to
algorithm quality (≤ 35%) — and neither registered conclusion is claimed. But the
direction points away from raw bit width: on matched runs the echo rate is *graded*,
6% (Q4_K_M) → 43% (IQ2_M, ~2.7 b/w) → 75-79% (imatrix and official Q2_K). The original-seed
figures (14% upper rungs, 94% Q2_K) come from a different seed set and are not stacked
into that ladder. A lower-bit quantization from a different family preserves more
constructive novelty than a higher-bit K-quant.

**Closing the selection-effect loophole** (combined §5.9). Echo rates are computed among
*valid* outputs, and a verbatim copy is valid by construction while a botched mutation
usually is not — so a high echo rate among valid rows is in principle compatible with a
model attempting many mutations that all break. Classifying every non-valid row in the
three coordinate-logged runs rules this out. There is no garbage: every failed 14B output
at every rung is a fully parsed, malformed circle list, never truncation or non-coordinate
text. And at official Q2_K the *invalid* rows are themselves majority near-copies of the
running parent (18/32 in the re-execution, 15/26 on fresh seeds; typically 26 of 27
circles unchanged with one added or dropped). Counted over the whole output distribution
rather than the valid slice, official Q2_K emits copies or near-copies in roughly 70% of
attempts. The scheme gradient reappears in the failures — near-copy fraction among invalid
rows runs 0/33 (fresh Q4_K_M) → 2/22 (IQ2_M) → 5/18 (imatrix Q2_K) → 15/26 and 18/32
(official Q2_K). A validity-filter explanation predicts mutation-dominated invalid rows;
the invalid rows are copy-dominated.

**A fixed-parent control narrows the contrast, and it governs every echo figure above.**
The echo rates just reported are measured against each lineage's *running* parent, and
those parents are not distributed alike across rungs: Q2_K lineages rarely improve, so
their parent mostly remains the seeded 0.900 grid, while upper rungs climb away from it.
Parent quality is therefore confounded with rung, and the confound runs in the direction
that flatters the result.

A fixed-parent dispersion probe measures the same quantity without that confound. It runs
the same Qwen2.5-Coder-14B at the same three rungs, holding the parent constant at each of
six preset scores from 0.88 to 1.65, and logs coordinates and an echo flag per row
(`dispersion_probe/probe_samples.jsonl`, 288 rows: 165 valid, 123 invalid; the table counts
valid rows, as elsewhere in this section).

*What this probe was registered to test, and what we use it for.* The probe carries its own
analysis preregistration (`dispersion_probe/analysis_prereg.md`, written before any metric
was read, with an amendment timestamped before any output file was downloaded). Its
registered primaries are **not** echo: they are a Jonckheere-Terpstra trend test on
per-parent mean pairwise normalized edit distance over valid samples, and a
rarefaction-matched count of unique behaviour cells on a centers-only descriptor, under a
locked four-way decision rule (SURVIVES / PARTIAL / FALSIFIED / UNDERPOWERED). **We do not
report those outcomes here, and this paper draws no conclusion from them.** What we use is
the quantity the same registration explicitly retains for this purpose — the kernel's
existing coordinate echo, kept unchanged so that "the comparison against the 14B
score-inferred echo rate remains possible". Using it as a cross-check on §3's echo figures
is therefore the anticipated use, but it is a *secondary* measure in that document, and a
reader should treat the probe's registered mechanism verdict as unreported rather than as
supporting anything below. The probe also does not cover the IQ2 files.

| rung | echo, fixed parent (all) | echo, parent 0.88-0.90 | echo, loop |
|---|---|---|---|
| Q4_K_M | 34/65 (52%) | 6/18 (33%) | 3/20 (15%) |
| Q3_K_M | 31/51 (61%) | 7/16 (44%) | 3/19 (16%) |
| Q2_K | 46/49 (94%) | 11/12 (92%) | 17/18 (94%) |

At the 2-bit rung the designs agree. At the upper rungs they do not: held to a fixed
parent, Q4_K_M and Q3_K_M echo far more often than the loop suggests. Restricted to the
0.88-0.90 band the loop actually occupies, the contrast is **6/18 versus 11/12 — 33%
against 92%**, not 15% against 94%.

The per-parent vectors, in full, because the relationship is not clean enough to summarize:

| parent | 0.88 | 0.90 | 1.04 | 1.30 | 1.55 | 1.65 |
|---|---|---|---|---|---|---|
| Q4_K_M | 4/12 (33%) | 2/6 (33%) | 9/14 (64%) | 4/11 (36%) | 9/11 (82%) | 6/11 (55%) |
| Q3_K_M | 5/10 (50%) | 2/6 (33%) | 4/7 (57%) | 5/11 (45%) | 9/10 (90%) | 6/7 (86%) |
| Q2_K | 7/8 (88%) | 4/4 (100%) | 8/8 (100%) | 12/12 (100%) | 8/8 (100%) | 7/9 (78%) |

Q4_K_M's rate rises with parent score overall but **not monotonically** — 1.30 drops back
to 36% and 1.65 to 55% — so we report the vector rather than a trend, and no trend test is
claimed. Q2_K is high at every parent but not uniformly so: 78% at 1.65 and 88% at 0.88 are
its two lowest cells, and an earlier phrasing of ours that put it "at or above 88%
everywhere" was wrong on both. What the table supports is narrow and sufficient: at every
one of the six parents, Q2_K echoes more than either upper rung, and the gap between them
is much smaller than the loop comparison implies.

Three consequences, which we state here rather than leave to a reader.

*The cliff's direction and its 2-bit endpoint survive; its spread does not.* The headline
"14% to 94%" is partly an artifact of where each rung's running parent sits. The
fresh-seed 79%-versus-6% figure and the invalid-row near-copy gradient carry the same
confound and should be read with the same discount.

*The scheme-gradient ladder in the IQ2 paragraph above is weakened.* That ladder — 6%
(Q4_K_M) → 43% (IQ2_M) → 75-79% (Q2_K) — is built from loop-measured upper-rung rates. If
Q4_K_M's matched rate is 33-52% rather than 6%, the ladder's low anchor is wrong and
IQ2_M's 43% may not be separated from Q4_K_M at all. The registered bit-width question
already returned its inconclusive branch; this control means the *direction* that paragraph
reads off the gradient is weaker than it presents, so we withdraw the gradient as evidence
about bit width and keep it only as a description of the loop-condition numbers. In
particular its closing sentence — that a lower-bit quantization from a different family
preserves more constructive novelty than a higher-bit K-quant — does not survive the
control, and should be read as a statement about the loop condition alone.

*The registered upper-rung bound is design-specific.* The prediction "each upper rung ≤
35%" held at 11-16% under the loop condition and would have **failed** under fixed parents
at 52-61%. It was registered against the loop design and is correctly scored there, but a
reader should not carry it as a general property of those rungs.

The probe is not a substitute for the loop measurement: a fixed parent removes the lineage
history the loop includes, so the two conditions are not interchangeable, and the loop is
the condition this paper's argument is about. It is, however, the better-controlled
comparison on the one axis where the loop design is confounded.

**What varied, and what did not.** This distinction is load-bearing for the rest of the
paper, so we state it before drawing the transfer. Across every run in this section the
inference stack was *constant*: the same llama.cpp build, the same 2 × T4 hardware, the
same sampling parameters, the same harness. The only thing that changed was which
SHA-256-pinned weight file was loaded. What is measured here is therefore the effect of
**served-weight quantization**, not of a decode path, a kernel, a batching regime, or a
speculative-decoding scheme.

Served quantization is a genuine element of a serving stack — a deployer chooses which
quantization to serve, and an alias does not report that choice — which is why the finding
bears on alias opacity at all. But it is *one* element. That degrading it selectively
removes constructive novelty does not establish that other serving-stack variables do the
same, and we do not claim it. The generalization from this variable to the stack is the
hypothesis this paper raises and §4 finds an unattestable instance of; it is not a result
established here. Readers should hold us to the narrower claim.

The transfer this paper needs from §3 is therefore narrow and should be read narrowly: a
degraded *served quantization* can leave every pass/fail axis intact while removing
constructive competence. It was measured at N = 26 on locally served open weights, at one
scale pair, on a single quantization family plus one control — not at §4's cells and not
inside the agent runtime (§8).

---

## 4. Forensic case study: the `opus_alias` arm

**Setup.** The study's third tier was requested by the study owner as a specific dated
top-tier model. The agent runtime through which every arm was invoked accepts a model
*alias* only — no dated identifiers — so the request was unsatisfiable and, more
importantly, *undetectably* unsatisfiable: nothing in the runtime's response surface
reports which weights served a call. We therefore label the arm `opus_alias` throughout
and never attach a version number to it. Thirty invocations were run, ten each at three
held-out cells (N = 13, 21, 31), under a bare prompt identical to the other tiers, with
predictions registered in `arm_o_preregistration.txt` before any sampling — full digest
`211718c6b58d627f17e34aa73ad6142b89c7f39048e5e19a8cc864d63c281738`.

**Serving signature — a session-log observation, not artifact data.** Completions
returned in 2.8-5.9 s across the first twenty invocations (N = 13 and 21) and 3-9 s once
N = 31 was added, i.e. 2.8-9 s across all thirty. On the same harness and task the Haiku
tier returned in 75-250 s and the Sonnet tier in 150-1170 s — one to two orders of
magnitude slower for nominally smaller models. The anomaly is consistent rather than
intermittent, holding for all thirty invocations across all three cells. We state the
evidence class plainly rather than in a limitations section: these are ranges carried in
the working log (`STATE.md` §8, §8b). The per-invocation duration vector was **not**
captured into the released artifact — `arm_f_raw.json` rows carry exactly four keys
(`arm`, `n`, `raw`, `sample_id`), with no duration, no usage, no timestamp — and
`arm_f_repro.py` contains no timing or usage capture at all. A reader can recompute every
validity figure in this section and cannot check a single latency figure. This is also the
one item of §6's disclosure standard that this paper does not itself implement, and §6
says so.

*A second apparent anomaly, withdrawn.* Reported-token counts are uniform at ~49.9k across
all thirty invocations, and that tightness invites reading as a second serving signature.
It does not survive definition, and we report it here as a non-finding rather than omit
it, because the reasoning generalizes to any study reading a single usage integer. The harness log records a single per-invocation usage figure that is
not disaggregated into input, output and cache-read. The thirty stored completions are
215-1283 characters (mean 578), i.e. roughly 61-367 output tokens, so ~49.9k cannot be an
output count; the reading it supports is a total/context counter over a large fixed system
prompt, inherited user-level instruction files (§5), and a task prompt that is
byte-identical in length across all three cells (520 characters — the template substitutes
a two-digit N). Under that reading near-uniformity is exactly what the experimental design
predicts, and the residual few-token spread is plausibly tokenizer-level variation between
`"13"`, `"21"` and `"31"`. We withdraw the observation rather than hedge it. The latency
evidence is unaffected; the behavioral evidence below is recomputable from the released
raws.

*No contemporaneous control.* The three tiers were not interleaved in a single window —
the `opus_alias` cells were sampled in their own batch, with N = 31 added later still —
and load conditions demonstrably varied within the study, since five invocations elsewhere
were rejected by a concurrency cap before reaching a model (§6, item 3). We therefore
cannot exclude load or queueing as a contributor to the latency gap. What a same-window
interleaved control would establish, this design does not, and a systems reader should
discount the two-orders-of-magnitude figure accordingly.

**Behavioral signature — recomputable, and reported at both tolerances.** Validity was
**4/30 (13%)** at the primary 1e-6 tolerance and **4/30 at the strict 1e-9 tolerance**:
the collapse is tolerance-invariant, per cell 3/10, 1/10, 0/10. The comparators on the
same three cells, recomputed from the released file with the released scorer: the Sonnet
arm **30/30 at 1e-6 and 27/30 at 1e-9** (three rows fail on overlap at the strict
tolerance and pass at the primary), and the Haiku (`bare`) slice **50/60 at 1e-6 and
47/60 at 1e-9**. §2 declares 1e-6 primary in advance, so both figures are printed rather
than one chosen. *Disclosure on the comparator.* A 45-row Haiku slice from a prior sampling
wave once served as this comparator. `arm_f_raw.json` was subsequently overwritten in place
by a 100-invocation wave that reuses the same arm labels with colliding `sample_id` values
and carries no batch or run-date field, so that slice cannot be reconstructed from the
released artifact. The comparator above is therefore stated against the slice that exists,
and the schema defect that destroyed the other one is recorded in §5 — it is the concrete
case that motivates §6's item 3.

The failures are geometric, not formatting. **All 26 invalid rows overlap**; 2 of them
additionally contain zero-radius circles. Those 2 are labelled `nonpositive_radius` only
because that gate fires before the overlap gate in the released scorer — both still
overlap once the zero-radius entries are removed — so the earlier "24 overlap, 2 padded"
split described gate ordering, not disjoint failure modes. One of the two (N = 21, sample
5) has 12 of its 21 radii at zero and is better described as mostly degenerate than as
padded to count. The geometric errors sit far outside rounding noise: in one N = 31 row
(sample 3), edge strips at r = 0.03 sit 0.1367 from a grid circle of radius 1/6 that
requires 0.19667 — a deficit of 0.06, nearly five orders of magnitude above the tolerance
(0.06 / 1e-6 = 6 × 10⁴). That
row is an example, not a cell characterization: 2 of the 10 N = 31 rows use an r = 0.03
strip, the other eight use filler radii between 0.006 and 0.052.

The attempted constructions also shifted family. At N = 13, all ten rows place four
circles of radius exactly 0.25 in the corners — ordinary circles, not quarter-disc
sectors — plus one to three smaller filler radii in an Apollonius-like arrangement; the
released classifier returns `structure: other` for all ten, meaning none of them is a
grid or grid-plus-filler of the kind both other tiers produce. At N = 21 the rows are
mixed-radius grids with corner and edge fillers; at N = 31, a coarse grid at r ≈ 1/6 with
border strips and interior fillers. Each is *more* ambitious than the grid-plus-filler
templates the other tiers produce, and each is executed with broken tangencies most of
the time. The four valid samples score below the registered trap value the weak tier
reliably hits — but by very different margins, which matters: at N = 13 the three valid
rows score 1.2646, 1.2873 and 1.4142 against a trap of 1.625 (13-22% below), while the
single N = 21 valid scores 2.07 against a trap of 2.1 (1.4% below, effectively at it).
The registered disconfirmation condition — regression toward the trap — did not occur; the
arm fell off a validity cliff attempting a harder family.

*The registered scorecard.* The working log marked P-O1, P-O2 and P-O4 NOT EVALUABLE on
the reasoning that scoring a tier comparison across a validity collapse would be
dishonest. That verdict is too conservative for P-O1, which is arithmetically evaluable
and **held**: it registered that the `opus_alias` on-trap rate
pooled across the three cells would be at most Sonnet's 1/30, and the observed rate is
**0/30** — no valid row falls within the registered 2e-3 window of 1.625, 2.1 or 2.5833,
the nearest miss being 2.07 against a 2.1 trap, off by 0.03 or fifteen times the window.
P-O3 (multi-radii fraction ≥ 0.9 of valid samples) also held, at 4/4, though on four rows
it carries little weight. P-O2 and P-O4 failed outright: zero rival-argmax outputs against
Sonnet's 6/30, and a best valid score of 2.07 against the 2.2588835 the prediction
required. The scorecard is therefore two held, two failed, none unevaluable — a weaker
outcome than the registration hoped for on P-O2 and P-O4, and a stronger one than "not
evaluable" on P-O1.

**Two hypotheses.** The first is *serving-path degradation*: a fast decode path erodes
the arithmetic precision needed to close a tangency while leaving the choice of
construction — the ambition — intact. That would echo §3's finding from a new
direction, since it is precisely the quantization cliff's signature: surface competence
preserved, constructive competence removed. The second is a *genuine tier property*:
whatever weights the alias resolved to really do attempt harder constructions and
really do execute them less reliably — an inverted U in constructive reliability as
nominal capability rises.

**What the observable set can and cannot separate.** The runtime exposes, per invocation,
exactly four things: the completion text, wall-clock duration, a single aggregate usage
figure, and error codes. Call that set *O*. On the text channel the two hypotheses induce
the same distribution — both predict ambitious families executed with broken tangencies —
so no amount of text observation separates them. On the timing channel they are *not*
symmetric, and we decline to flatten the asymmetry: H1 predicts the latency observation
directly, while H2 is silent on it. To cover *O*, H2 must be conjoined with an auxiliary —
"a fast serving path was in use but had no behavioral effect" — which is H1's mechanism
minus its causal claim, and therefore strictly more complex. The observations mildly
favour H1. What they cannot do is *decide*, because that auxiliary is not itself testable
through *O*: no element of *O* reports which decode path served a call. **The
irreducible residue is the unattestability of the serving path, not a blanket
impossibility of behavioral discrimination**, and we state it that way because the two
are not the same claim and the stronger one is false. That residue is the finding *of this
section*; the paper's headline result is §3's cliff, and the two should not be conflated.

Within that narrowed claim, two routes genuinely fail. More sampling does not separate
them: the anomaly is uniform, so more of it is more of the same. Timing instrumentation
does not, because the serving path is not a variable we can set *from inside the runtime*.

*A pinned dated endpoint — not run, and not impossible.* It is tempting to say that direct
separation requires an interface the runtime does not expose, and stop there. That
conflates the runtime's interface with the experimenter's options. The same thirty
hash-pinned prompts can be issued to a dated model identifier on
a pinned inference endpoint, which several vendors sell, entirely outside the agent
runtime, and the result would be informative in both directions: if the dated endpoint
reproduces the ambitious-family, broken-tangency signature at a comparable validity rate,
H2 gains substantially; if it returns the 30/30-class competence the other tiers show, H1
does. What such a run still cannot do is attest what the *alias* resolved to on the day
we sampled it — the counterfactual is gone, and that is the sense in which C3 survives.
C3 is a claim about attesting a past call, not about the practical question being closed;
the second does not follow from the first. We did not run this experiment, and its absence
is a limitation of this paper rather than a property of the problem.

Two further routes also do *not* fail, and both are easier to dismiss than they deserve.

*Prompt variation.* The earlier dismissal — that prompt variation cannot help because
both hypotheses act on execution rather than intent — ruled out an entire experiment class
in one clause, and it is wrong for at least one design. Hand the alias a *fixed,
known-valid* packing and ask it to verify or repair the tangencies. The model did not
choose that construction, so arithmetic execution is decoupled from constructive ambition:
failure to verify tangencies it did not select is execution degradation independent of
ambition, which is exactly an H1/H2 discriminator. We did not run it. It is registered as
this paper's named follow-up (§8), and its existence narrows C3 to what is stated above.

*A dated re-snapshot.* §8 proposes re-sampling the same alias at a later date and treats
the result as informative either way. That experiment is runnable from inside the runtime,
so the earlier flat claim that no within-runtime experiment could bear on the question
contradicted our own follow-up section. It is narrowed accordingly: a re-snapshot can
detect a *change* in the serving signature without ever attesting the serving path in
either snapshot.

The arm is logged in full, excluded from the tier ladder, and carries the alias caveat in
every mention.

---

## 5. What is repairable and what is not

The repairs below are implemented in `arm_f_repro.py` and its companions, not merely
proposed — and where they are *not*, this section says so rather than leaving a reader to
find out from the artifact.

**Implemented.** Prompt text is pinned and SHA-256 hashed *before any sampling*, one hash
per problem size, so it cannot be silently edited after seeing outputs. The digests for
the three cells of §4 are published here, which is the step that makes the hash a
disclosure rather than a private check:

| cell | prompt SHA-256 |
|---|---|
| N = 13 | `32db485bea625ff9f39f4723ebf1a01f337559a9e2cf567fb486928f71f7f8df` |
| N = 21 | `a415425b4ed5a57ea9b6f09c2328508f12370e1624734e1c5ed32913741795a9` |
| N = 31 | `a664d003cbf1c0eca51bae5b3a1d072071eb34756725a7491d6a2e8fa3b78e92` |

(Each prompt is 520 characters, the template with a two-digit N substituted.
`arm_f_prompts.json` carries the prompt text and digest for five cells — N = 13, 17, 31,
35, 37 — so the N = 13 and N = 31 digests above verify against it directly. **N = 21 is
absent from that file**, and the digest printed here for it comes from the working record
rather than the released artifact; a reader cannot check it. Since N = 21 is one of the
three cells §4 reports, this is a gap in exactly the repair this section claims, and it is
recorded in the claim map rather than smoothed over. Re-releasing the file with all seven
cells is the obvious fix and requires no new sampling.) Every raw output is
stored verbatim, parsed or not. Scoring, validity and construction classification are
deterministic, local, and computed at both tolerances per row. Predictions with explicit
falsifiers and a disconfirmation rule are written before the first invocation and
externally timestamped; §4 publishes the full registration digest rather than an
eight-character abbreviation, which is not an identifier.

**Implemented partially, and named.** The run date is recorded with the alias → dated-id
mapping in force on that date (`RUN_DATE` and `ALIAS_MAP` in the harness header) —
provenance without being a pin. But the released map contains a single entry, for the
Haiku proposer, and `RUN_DATE` is a single hard-coded date that is *not* the
`opus_alias` arm's run date (its registration is dated later, and the N = 31 cell ran
later still). The paper's headline provenance repair is therefore unimplemented for
precisely the arm the paper is about. We state that rather than back-fill a map we cannot
attest. Raw storage has a matching defect: rows carry no batch, wave or run-date field and
`sample_id` collides across arms and sampling waves, so the released file cannot be sliced
back into the arms as originally reported (§4, comparator disclosure). Verbatim storage
without a row key is weaker than the §5 table previously claimed.

**Not repairable from inside.** Sampling parameters are not exposed, so temperature,
top-p and top-k are unknown and unfixable — and they are the parameters that shift the
output distribution most. The alias → weights binding is a promise, not a hash: the alias
can be repointed at any time and past runs cannot be re-executed against the weights that
produced them. The subagent inherits a system prompt and user-level instruction files that
are not part of the task prompt and not held fixed across time. And the serving path is
not attested at all — no flag distinguishes a fast-mode decode from a standard one, the
exact variable §4 needed and could not obtain.

**Does output-text fingerprinting close the gap?** Wimbauer et al. (arXiv:2605.29979) show
that serving-stack differences — inference engine, attention backend, GPU type — are
detectable from output text alone. If that transfers, fingerprinting is a candidate
within-runtime discriminator and C3 would be narrower still, so we engage it directly
rather than filing it as related work. Three reasons it does not settle §4 as run, none of
them a dismissal of the method. First, fingerprinting is a *classification* method: it
assigns an output to one of a set of stacks for which reference signatures have been
collected. No reference signatures exist for this vendor's closed serving paths, and
collecting them would require the pinned-endpoint access whose absence is the problem.

*Second, a tempting objection that does not hold.* One might observe that the arm is only
thirty completions averaging 578 characters, well below the text volume these methods use,
and conclude the corpus is too thin. That treats the stored corpus as setting the budget,
which it does not: these methods issue *fresh* probes
against a live alias, which an agent runtime permits freely, so the relevant budget is how
many new queries one is willing to spend rather than how much text the completed arm
happens to contain. Leshin et al. (arXiv:2603.19022) fingerprint from fixed-prompt output
distributions and detect changes of inference stack and quantization; Bruckner
(arXiv:2607.10252) recovers model identity from roughly a hundred single-token queries.
Both are affordable, so the volume objection fails.
What survives of it is only retrospective: those probes cannot be sent to the serving path
that answered our thirty calls in the past, because that path is no longer addressable —
which is a statement about *this* arm's irrecoverability, not about the method's cost.

Third, and most fundamental, a positive fingerprint would identify a
*stack*, not attest *weights* — it could strengthen H1's antecedent without touching the
auxiliary that H2 needs. This third reason is the only one of the three that survives
intact. The honest statement is that fingerprinting is the most promising
published route to narrowing this class of question, that it is not runnable on this
corpus, and that a study designed around it from the start — banking reference signatures
while the endpoint is still available — would be a genuine advance over what we did.

| Item | Repairable? | Mechanism | Residual risk |
|---|---|---|---|
| Prompt text | Yes | SHA-256 pre-sampling, one hash per cell, digests published above | None |
| Raw outputs | Partial | Verbatim storage of every invocation, failures included | No batch key; `sample_id` collides across waves, so reported slices are not reconstructible |
| Scoring / classification | Yes | Deterministic local evaluator, offline, both tolerances per row | None; dual reporting removes the tolerance degree of freedom |
| Predictions | Yes | Hash-locked prereg with falsifiers, externally timestamped, full digest published | Registration errors — disclose, do not amend |
| Model identity | Partial | Alias + run date + dated-id map in force that date | Map covers the Haiku arm only; `RUN_DATE` is not the `opus_alias` arm's date; alias may have been repointed |
| Serving-signature stats | Not implemented here | — | §6 item 4 is advocacy in this paper, not demonstration |
| Sampling parameters | No | — | Unknown distribution shift between runs |
| Alias → weights binding | No | — | Silent model substitution; past runs unrepeatable |
| Serving path (fast-mode) | No | — | §4-class confound; output-text fingerprinting is the most promising route and is not runnable on this corpus |
| Inherited system / user prompt | No | — | Unlogged context drift across time |

---

**The scorer is model-written, and that is a circularity worth naming here rather than in
back matter.** This paper's integrity argument rests on deterministic local scoring: every
validity, echo and near-copy figure is produced by code, not judgement. That code was
written with assistance from models in the same family as the runtime §4 studies (see *Use
of AI systems*). A reader is entitled to ask whether the instrument shares a blind spot
with the object.

The available answer is reimplementation, and it has been done. `sec3_ladder_repro.py` was
written independently of the original collection and scoring code, from the definitions in
the text rather than from the original implementation, and it re-derives §3's viability,
validity, echo, per-seed, must-differ and Fisher figures from the raw ledgers; §4 was
likewise re-scored from `arm_f_raw.json` by a separately written geometric checker.
Agreement is exact except for one invalid-row near-copy count reported above. That is not
independence in the strong sense — the same author directed both implementations — but it
does establish that the figures follow from the released rows under the stated definitions
rather than from a particular scorer's quirks, which is the specific failure the
circularity would produce. The one place reimplementation *did* diverge, the running-parent
tie rule, is documented in §3 precisely because it is where a third implementation would
also diverge.

---

## 6. Implications

Every LLM-evolution, best-of-N and iterative-refinement study run through a managed
agent harness inherits this list — FunSearch-style program-evolution loops,
self-refinement pipelines, and any tier-ladder comparison naming "the model" by alias.
Such studies are not thereby wrong. They are unrepeatable in a specific and
now-demonstrable way, and §3 establishes that the unrepeatable variables are ones the
outcome is sensitive to. The correct response is disclosure, not retraction.

**A minimum disclosure standard — mostly an endorsement, with one addition.** Reporting
standards for LLM research already exist and we are not proposing a rival. GUIDE-LLM
(Feuerriegel et al., "A reporting checklist for large language models in behavioural
science", *Nature Human Behaviour* 10:1182-1186, 2026) is a 14-item consensus checklist
from an 80-expert panel that already mandates exact model version and access method,
prompts and system instructions, sampling parameters, and validation. The
software-engineering community has parallel guidance (Baltes et al., arXiv:2508.15503;
Korn et al., arXiv:2601.01954), and Siddiq et al. (arXiv:2512.00651) supply the prevalence
evidence across 640 papers, finding that artifact badges do not guarantee reproducibility.
Items 1-3 below are our restatement of requirements those documents already impose, with
the agent-runtime specifics filled in; a reader who adopts GUIDE-LLM has them.

**Item 4 is the addition**, and it is the one this paper does not itself implement. That
is an uncomfortable position and we state it rather than let a reader discover it: the
only element of the standard we can claim as new is the element our own artifact lacks,
which is precisely why §4's central evidence is a working-log observation rather than a
checkable file.

1. **Alias, run date, and the alias → dated-id map in force on that date.** Two lines
   of the harness header. It pins nothing, but converts an unfalsifiable claim ("we
   used model X") into a dated, checkable one. Implemented here for one proposer only,
   which is the failure mode to avoid: a map that omits the arm under study is not
   provenance (§5).
2. **Prompt hashes computed before sampling.** One SHA-256 per prompt variant, in the
   artifact that runs the study, closing the largest silent degree of freedom in LLM
   experiments at zero cost — *and published in the paper*, since a digest kept in a
   private file is a check, not a disclosure (§5 publishes ours).
3. **Verbatim raw outputs, including failures, with a batch key.** Parse failures,
   malformed rows and runtime rejections are data; dropping them silently is how validity
   rates get inflated. In our own logs, five invocations were rejected by a concurrency cap
   *before reaching a model* in the Haiku wave; scoring them as proposer failures would have
   moved that arm's reported validity from 32/45 (71.1%) to 32/50 (64.0%) — 7.1 points
   *(this worked example uses the superseded 45-row slice, which §4 records as no longer
   reconstructible from the released artifact after an in-place overwrite. We keep the
   example because the arithmetic illustrates the item and the overwrite is itself an
   instance of the defect item 3 exists to prevent, but a reader cannot check these two
   numbers against the released file, and that is the point rather than an oversight)* —
   absolute, 10.0% relative. The batch key is the part we got wrong: without it a later
   sampling wave written into the same file destroys the ability to reconstruct the slice a
   paper reported (§4, §5).
4. **Serving-signature statistics, with a firing condition.** Per-invocation wall-clock
   duration and reported usage, logged per row and reported as distributions — and, because
   "report a distribution" is not a decision rule, with an explicit canary condition. We
   propose: publish per-arm, per-cell duration median, IQR and coefficient of variation,
   and flag an arm when its duration CV falls below one third of the neighbouring tier's on
   the same cells, or when its median duration differs from the neighbouring tier's by more
   than an order of magnitude under a *same-window interleaved* schedule. For usage fields,
   disaggregate input, output and cache-read counts before reporting any spread — our own
   withdrawn token observation (§4) is the argument for that clause, since an aggregate
   counter made a predicted uniformity look like an anomaly. This is the item the field does
   not currently do, and the one that surfaced §4; it is also the item this paper does not
   implement, so we present it as a proposal to be tested rather than a demonstrated
   instrument. Thresholds above are a starting point, not calibrated values.

**What vendors could expose.** A weights digest returned with each completion would
make the alias → weights binding attestable. A sampling-parameter echo would make an
unset temperature auditable rather than unknown. A serving-path flag — one boolean
distinguishing a fast or speculative decode from the standard path — would have
separated §4's two hypotheses outright. Each is a single field in a response object.

---

## 7. Related work

The reproducibility-in-ML line establishes that reported results depend on undocumented
implementation and environment detail; Pineau et al. (JMLR 22(164), 2021;
arXiv:2003.12206) document the NeurIPS reproducibility program and the code-submission
checklist now carried across ICML, ICLR and AAAI, and it is the canonical anchor for the
claim. A separate and more recent line establishes that even a fixed model on fixed
hardware does not return identical outputs under varying batch composition: Yuan et al.
(arXiv:2506.09501, NeurIPS 2025) study numerical sources of nondeterminism systematically
and report accuracy swings of up to 9% on a 7B reasoning model under bf16 as batch size,
GPU count and GPU version change, with He et al. (Thinking Machines Lab, 2025) as the
practitioner companion that locates the cause in the absence of batch-invariance in
matmul, RMSNorm and attention kernels and ships batch-invariant replacements. Our
contribution against that background is not the observation of variance but the
*addressing mode*: batch-invariance work assumes you can name and control the stack, and
the alias interface makes the relevant variable unaddressable rather than merely
uncontrolled.

Between those two lines sits the literature this paper is most directly downstream of:
**behavioral change behind a stable identifier**. Chen,
Zaharia and Zou (arXiv:2307.09009) is the canonical precedent — the same GPT-3.5 and GPT-4
identifiers returned substantially different behavior across snapshots months apart, which
established that a stable alias does not denote a stable model and that deployed systems
need continuous monitoring. That paper is the origin of our premise, and our contribution
against it is not that aliases drift but what the drift does to a *specific measured
capability* inside a selection loop — and that the axis it moves is invisible to the
pass/fail instruments such a loop already runs.

Leshin, Shah, Timmis and Kang (arXiv:2603.19022) state our hazard more completely than we
do: an endpoint can remain "healthy" while its effective model identity changes through
weights, tokenizers, **quantization**, inference engines, kernels, caching, routing or
hardware. Their Stability Monitor black-box-fingerprints an endpoint from fixed-prompt
output distributions with a summed energy-distance statistic and permutation tests, and
detects changes of model family, version, inference stack *and quantization*, reporting
large provider-to-provider differences for the same nominal model. This obliges us to
narrow C3 explicitly, and §5 now does: such methods **detect change** between snapshots;
none of them **attests which decode path served a particular past call**. That is the
whole of what C3 claims, and it is a much smaller claim than "the question is closed."
Bruckner (arXiv:2607.10252) fingerprints model identity under opaque serving chains from
roughly a hundred single-token queries; we note it as the cheapest available change
detector, while recording that it addresses identity rather than quantization, so it does
not substitute for the preceding work on our axis.

Two 2026 quantization studies bracket §3's result and sharpen it by contrast. Rababah,
Akcora and Leung (arXiv:2607.08734) introduce *correctness agreement* — the overlap of
correct predictions between base and quantized model — and show behavioral divergence
persisting while accuracy and perplexity stay stable. That is §3's thesis in generic form
and a closer fit than Marchisio; our addition is the loop setting and a coordinate-exact
echo metric rather than a decision-overlap one. Zhou et al. (arXiv:2604.19884) separate
two 2-bit failure modes, signal degradation and computation collapse, the first
training-free repairable and the second not — and their collapse mode is *incoherence*,
outputs decaying into stop-words. Our Q2_K failure is the opposite surface signature at the
same nominal rung: fully coherent, format-valid, geometry-valid output that happens to be a
copy. A failure mode that passes every legibility check is the harder one to notice, which
is the point §3 is making.

Finally, copying is not a phenomenon we discovered. ShinkaEvolve (Lange et al.,
arXiv:2509.19349) ships two-tier novelty rejection sampling — embedding cosine followed by
an LLM novelty judge — precisely because LLM proposals are routinely near-duplicates of
their parent. Near-duplicate proposals are a known engineering nuisance the field already
filters against. What we claim is narrower and, we think, new: that the *rate* of it is
sharply dependent on served quantization, so a mitigation tuned at one precision is being
asked to do a different amount of work at another, with no signal that the amount changed.

The quantization-effects literature measures degradation on static single-shot benchmarks.
The substantive fit is Marchisio et al. (arXiv:2407.03211), whose multilingual study finds
that automatic metrics systematically *understate* quantization harm — a 1.7% average drop
on Japanese by automatic metrics against 16.0% under human evaluation — which is §3's
thesis arriving from a different domain: the instrument decides whether the damage is
visible. GPTQ (Frantar et al., arXiv:2210.17323) and AWQ (Lin et al., arXiv:2306.00978)
are cited as method references for post-training quantization, not as measurement studies,
and with an explicit family caveat: §3 sweeps llama.cpp K-quants and one i-quant, a
different scheme family from GPTQ/AWQ, and the antecedent study lists GPTQ, AWQ and
bitsandbytes among the schemes it did *not* test. §3 places the quantization gradient
inside a selection loop and finds the axis it moves — novelty — is not the axis any of
these benchmarks score.

Evaluation-variance studies quantify seed and prompt sensitivity: Madaan et al.
(arXiv:2406.10229) measure seed variance and benchmark noise across 280 models on 13
benchmarks, and Miller (arXiv:2411.00640) supplies the statistical machinery — a
super-population framing with formulas for uncertainty and power — for deciding when a
reported delta clears noise. Both matter here in a specific way: §5's residue is
orthogonal to both, because it cannot be averaged out by more seeds. A serving-path change
is not a draw from a noise distribution the experimenter is sampling; it is a change in
which distribution is being sampled, and error bars computed within a run cannot see it.
The engagement with Wimbauer et al. (arXiv:2605.29979) on output-text stack fingerprinting
is in §5, where it bears on the identifiability claim rather than serving as background.

For benchmark lineage, arXiv 2605.29268 studies the same objective (26 circles in the
unit square) under LLM-guided program synthesis with an explicit best-of-N comparator;
its asymmetric-proposal-mass account is the complement of our companion paper's
attractor account. The saturation of reported values here — AlphaEvolve at 2.635 and a
cluster of later systems at 2.635983283 (ShinkaEvolve), 2.63598308 (HELIX,
2603.07642) and 2.636 (GigaEvo, 2511.17592; AdaEvolve, 2602.20133), with further
systems on the same benchmark whose reported values we have not independently
verified (SeaEvo, 2604.24372; ThetaEvolve, 2511.23473) — is itself an argument for
this paper: a field reporting agreement at the eighth decimal while addressing its
models by alias is reporting agreement it cannot attest.

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
expose more (a dated identifier, a sampling echo, a serving-path flag) is an empirical
question we did not test; a runtime that exposes more would falsify C3 for that runtime
without touching §4's specific case. C3 is stated conditionally throughout for that
reason.

The serving-signature evidence is circumstantial *by construction*, and it is also
unshipped. Its evidence class is a working session log, not the released artifact (§4),
and the arms were not interleaved, so load is not excluded as a contributor to the
latency gap. We infer a serving path from a latency distribution because no direct
observation is available; were one available, §4 would be a bug report rather than a
paper. A reader who declines the inference is left with the second hypothesis, which is
equally unattestable, and §4's non-identifiability argument stands either way. The
token-count observation is withdrawn in §4 as a non-finding, and that withdrawal is the
clearest single illustration of why §6 item 4 demands disaggregated usage figures: an
aggregate counter looked like a signature until it was defined.

The `opus_alias` arm is n = 30, and the anomaly, though uniform across all thirty
invocations and all three cells, comes from one batch window. Two follow-ups are named
rather than gestured at. First, the **repair probe** of §4: hand the alias a fixed,
known-valid packing and ask it to verify or repair the tangencies, decoupling arithmetic
execution from constructive ambition. It is a genuine H1/H2 discriminator, it is runnable
from inside the runtime, and we did not run it. Second, a **second serving-signature
snapshot** of the same alias at a later date: if the signature shifts with no alias change,
§4 gains a second independent data point; if it does not, the constancy is itself
informative. Neither converts an inference about the serving path into an observation of
it — that is the residue C3 names — but both bear on which hypothesis to prefer, and a
paper claiming impossibility owes the distinction.

Finally, §3's data comes from a locally-served open-weights ladder at N = 26, not from
the alias-addressed runtime and not at §4's cells (N = 13, 21, 31). Two gaps, both real.
The mechanism gap — that served quantization matters for this task — is supported by §3's
measurement rather than measured inside the runtime, which is exactly the measurement §5
says cannot be made. The instance gap — that a cliff observed at N = 26 transfers to
N = 13/21/31 — is supported by the companion paper's finding that the same constructible
template family governs proposals across N, but it is an inference, not a replication. A
reader should treat §3 as establishing that the failure mode *exists and is invisible to
pass/fail metrics*, and treat its quantitative rungs as belonging to the sweep, not to §4.

### Use of AI systems

This paper studies language-model behaviour and was written with language-model assistance; both
facts are stated here so a reader can weigh them together. Claude models (principally the Opus,
Fable and Sonnet tiers) wrote the collection, scoring and analysis scripts and drafted the
manuscript prose; the referee reports came from `deepseek-v4-pro`, `deepseek-v4-flash` and Gemini
under written protocols. The human author directed the programme, approved each preregistration
before sampling, made the final inclusion, stopping and submission decisions, and is solely
responsible for the content; no language model is an author. What a reader can check is the
ordering — each preregistration commit is a git ancestor of the sampling it governs — not the
authorship of those texts, which was model-assisted like the rest of the repository. The authoring
models share a family with the runtime under study in §4, so the released scripts, raw ledgers and
frozen outputs, rather than the authorship, are what the claims rest on.

---

## Claim → evidence map

Every row names a file a reader can open. Where a figure is *not* checkable from the
released artifacts, the row says so instead of pointing at a document that merely repeats
it.

| claim | source |
|---|---|
| §3 14B ladder: viability 22/22/24/19, validity 18/20/19/18, echo 2/18, 3/20, 3/19 and 17/18, per-seed vectors, invalid-row near-copy fractions | `../agent-run/precision_sweep_14b_v2_output/**/candidates_precision_14b.jsonl` (200 rows), replayed by `sec3_ladder_repro.py` |
| §3 fresh-seed replication: 19/24 vs 1/17, per-seed 4/5, 4/5, 5/6, 2/2, 4/6 | `../agent-run/precision_sweep_14b_fresh_output/**/candidates_precision_14b_fresh.jsonl` (100 rows), same script |
| §3 must-differ probe: 5/5 at Q2_K, 1/5 at Q4_K_M; 6/8 vs 0/2 on the IQ2 pair | `../agent-run/**/mustdiffer_14b.jsonl`, `mustdiffer_14b_iq2.jsonl`; echo computed against the fixed seed parent, no echo flag in the ledger |
| §3 IQ2 control: 24/32 vs 12/28 | `../agent-run/precision_sweep_14b_iq2_output/**/candidates_precision_14b_iq2.jsonl` (100 rows), same script |
| §3 fixed-parent dispersion control: 34/65, 31/51, 46/49 and the parent-score gradient | `../agent-run/dispersion_probe/probe_samples.jsonl` (288 rows), `echo` field as labelled |
| §3 served weight files (SHA-256, byte length, repo, sampling parameters, GPUs) | `provenance.json` in each of the three ladder output directories |
| §3 seeded parent (26-circle 6 × 5 grid, score 0.89999) | `../agent-run/precision_sweep_14b_v2_output/**/state/q2_k_seed_42.json`, a lineage that never improved |
| §3 all eight Fisher figures (*p* = 0.007, 1.7e-7, 3.4e-6, 0.001, 0.44, 0.017, 0.056, 1.0) | recomputed two-sided in `sec3_ladder_repro.py` from the counts above; inferential status and the absence of multiplicity correction stated in §3 |
| §3 7B ladder | `../agent-run/precision_sweep/`; narrative and scope caveats in `../precision-cliff-paper-combined.md` §3.4, §5.9, §6 |
| §3 IQ2_M invalid near-copy 2/22 | **not reproduced**: our replay of the stated definition returns 1/22 (§3) |
| §4 validity, failure taxonomy, families, scores, both tolerances | `arm_f_raw.json` `opus_alias` / `sonnet_bare` / `bare` rows, recomputed with `arm_f_repro.py` |
| §4 durations | `STATE.md` §8, §8b — session-log ranges; per-invocation vector not captured (§4, §5) |
| §4 registration digest | `arm_o_preregistration.txt`, SHA-256 published in §4 |
| §5 prompt digests, N = 13 and N = 31 | `arm_f_repro.py` `prompt_hash()`, `arm_f_prompts.json` |
| §5 prompt digest, N = 21 | **not checkable**: absent from `arm_f_prompts.json`, which carries N = 13, 17, 31, 35, 37 only (§5) |
| §3 fixed-parent probe's registered primaries (Jonckheere-Terpstra on NED, rarefaction on the centers-only descriptor) and its locked decision rule | `../agent-run/dispersion_probe/analysis_prereg.md` — **registered but not reported here**; this paper uses only the probe's retained coordinate-echo measure and claims nothing from the mechanism verdict (§3) |
| §5 alias-map provenance and its gap | `ALIAS_MAP`, `RUN_DATE`, `PROPOSER_ALIAS` in `arm_f_repro.py` |
| §4 latency ranges (2.8-9 s vs 75-250 s and 150-1170 s) | **not checkable**: `STATE.md` §8, §8b working-log ranges only; the per-invocation vector was never captured, and `arm_f_raw.json` rows carry no duration field (§4, §6 item 4) |
| §6 item 3 worked example (32/45 → 32/50) | **not checkable**: the 45-row slice was overwritten in place and cannot be reconstructed (§4, §6) |
| §7 systems citations | `p8_systems_citations.md` (nine verified by the authors; this is self-certification and a reader should treat it as such) |
| §7 hazard-literature citations (2307.09009, 2603.19022, 2607.10252, 2607.08734, 2604.19884, 2509.19349, GUIDE-LLM, 2508.15503, 2601.01954, 2512.00651) | each checked against its live arXiv or publisher page; titles and author lists as printed there |
