# Served Precision Is Part of the Model: A Quantization Cliff in Proposal Variation, and the Limits of Reproducibility in Agent-Runtime LLM Studies


## Abstract

Quantizing a proposer's weights can leave every metric a discovery loop watches unchanged
while collapsing the variation the loop depends on. On a constructive geometry task at 14B,
degrading served quantization moves viability and validity by no detectable amount —
non-rejection at n = 50 per rung, not demonstrated equivalence, and at 7B viability instead
*inverts* — while at the 2-bit rung the proposer very largely stops departing from its
parent. Coordinate-verified parent-echo among valid outputs runs 14% (8/57) across the upper
three rungs against **94% (17/18)** at Q2_K. That contrast was preregistered before the run
that tested it, and the registration is released rather than described: the bound
`q2_k >= 60%`, `q4_k_m <= 35%` sits in the runner's header block, and it **held on five
never-sampled seeds** — 79% (19/24) against 6% (1/17). A registered must-differ probe
returned its registered branch, 5 of 5 valid outputs echoing under an explicit instruction
not to copy. The failed proposals are not garbage — they are coherent, well-formed
near-copies, which is why every pass/fail instrument reports health. At the loop level the
consequence is a post-hoc measure we label as such: the 2-bit rung takes **1 accepted
hill-climb step in 50 calls against 14-16** at the upper three, four of its five lineages
never advancing at all — while **final best score after ten generations does not separate
the rungs anywhere** (*p* = 0.32-0.94). The outcome number a practitioner reports is blind
to an order-of-magnitude collapse in search activity. That measure is mostly the echo
result in complement, the registered form of it failed on the fresh wave, and it does not
replicate at 7B; §3.6 states all three.

A fixed-parent control we run against ourselves **bounds** that result rather than extending
it. It shows the loop comparison is inflated by parent quality, putting the matched contrast
at 33% (6/18) against 92% (11/12) — direction and 2-bit endpoint survive, spread does not —
and its six parents share a single lattice, so it can speak to radius variation and not to
constructive novelty at all. Run against their own locked decision rules, neither wave
returns a usable verdict — wave 1 no category, wave 2 FAILED for want of a ceiling rung that
never ran — so the probe is reported as descriptive throughout, every registered outcome
with its label, and no claim rests on it. A registered scheme-versus-bit-width control returns
its inconclusive branch, so what is established is an effect of *this file's* quantization,
replicated on an independently produced Q2_K.

This matters because studies using a language model as a proposal operator increasingly run
through managed agent runtimes that address models by *alias*. Which quantization is served
is one of several things an alias leaves unattested — and it is now a variable the dependent
measure is known to be sensitive to. Our ladder holds the inference stack fixed and varies
only the SHA-256-pinned weight file, so it measures served-weight precision, not a
decode-path effect; whether other serving-stack variables behave alike is a hypothesis we
raise, not a result we establish.

We then report a forensic case study of a top-tier arm addressed only as `opus_alias`, whose
serving signature (2.8-5.9 s completions against 75-250 s and 150-1170 s for the other tiers
on the same harness) and behavioral signature (validity 4/30 against 30/30 and 50/60,
recomputable in full) together *mildly favour* an unattested serving path without deciding
it. The latency figures are working-log ranges the released artifact cannot check — itself
an instance of what we argue for. Serving-path degradation and a genuine property of
whichever weights the alias resolved to are not separable by any experiment that can
*attest* the serving path, because no observable the runtime exposes reports which decode
path served a call. That unattestability, not a blanket impossibility of behavioral
discrimination, is what the case study establishes, and we name the experiments that would
narrow it. We close on what is and is not repairable from inside an agent harness —
including where this paper fails its own standard — and endorse an existing reporting
checklist with one addition aimed at this hazard.

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

**C1 — the precision cliff, in variation rather than viability.** On a value-sensitive
constructive task, served-weight quantization measurably moves outputs — but not along the
axis the founding hypothesis predicted. Degrading a quantization ladder moves viability and
validity by no amount detectable at n = 50 per rung — non-rejection rather than
equivalence, and at 7B viability instead *inverts* — while at the 2-bit rung it collapses
the variation a proposal carries, leaving format and geometry intact. The failure mode is
invisible to viability and validity metrics, which is why it went unreported until the
antecedent study looked at coordinates rather than scores. What carries the claim is
registered and replicated: the echo bound `q2_k >= 60%`, `q4_k_m <= 35%` was written into
the runner before execution and held on five never-sampled seeds (19/24 against 1/17), and a
registered must-differ probe returned its registered branch. Two controls in §3 then bound
the claim rather than extending it: a fixed-parent probe cuts the effect's magnitude while
leaving its direction and 2-bit endpoint intact, and on that probe's registered centre-only
measures the presented lattice is reproduced at 92-98% at *every* rung. Because the probe's
parents all share one lattice it can speak to radius variation only, and whether a
better-served proposer would have moved to a different construction is a question that
design cannot reach. Both waves' registered decision rules return unusable
verdicts — unclassified on wave 1, FAILED on wave 2 — and §3 reports both labels alongside
the numbers they disqualify.

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

**Every 14B figure in this section is recomputed from the raw candidate ledgers, not copied
from the antecedent prose — and the 7B figures are not.** `sec3_ladder_repro.py`, released
with this paper, replays each `(quantization, seed)` lineage from the coordinate-logged
jsonl, reconstructs the running parent under the loop's own hill-climb rule, and re-derives
the 14B viability, validity, echo, per-seed, must-differ and invalid-row figures below,
together with five of this section's nine Fisher tails (*p* = 1.7e-7, 3.4e-6, 0.007, 0.017,
0.056). The ledgers are `sec3_artifacts/**/candidates_precision_14b.jsonl` (re-execution,
200 rows), `..._fresh.jsonl` (100), `..._iq2.jsonl` (100) and the two `mustdiffer_*.jsonl`
files, each with a `provenance.json` recording the SHA-256 and byte length of every weight
file served. The remaining four Fisher tails (*p* = 5.7e-10, 0.001, 0.44, 1.0) and the whole
7B paragraph are **not** replayed by that script: their counts come from the 7B run
(`sec3_artifacts/precision_sweep/`, vendored and openable, but not loaded by any released
script) and from the parent-echo contrast, and a reader who wants them checked must compute
them from those rows directly. We state the boundary rather than let the bolded sentence
above cover ground it does not.

**Inferential status of every *p*-value in this section.** Twenty-nine are reported and they
fall into four families that must not be pooled. **Nine are two-sided Fisher exact tests**
on counts (*p* = 5.7e-10, 1.7e-7, 3.4e-6, 0.001, 0.007, 0.017, 0.056, 0.44, 1.0). **Six are
permutation tests belonging to the two dispersion probes' preregistrations** — wave 1's
spread JT (*p* = 0.030), echo JT (0.686), quality fork (0.454) and rarefaction trend
(0.953), and wave 2's rarefaction JT (0.0081) and score fork (0.3526). **Two are Spearman
correlations** run as wave 1's orthogonality diagnostic (*p* = 0.032 and 0.032), which test
no claim of ours and exist only to check whether a descriptor is confounded by score. Wave 1's
preregistration prespecifies the |rho| criterion for that diagnostic but not a *p*-value
threshold, and wave 2's preregistration contains no orthogonality clause at all; the two
tails are reported here for completeness, not because either was registered as a test. Within the Fisher family, all
candidate-level contrasts — *p* = 5.7e-10, 0.007, 1.7e-7, 3.4e-6 and 0.017 — treat rows as
independent when they are nested within lineages sharing five seeds across rungs, so each
overstates the evidence; the antecedent study's appendix declares them not part of any
claim, and we adopt that status here for all of them rather than for one. The seed-level
tests (*p* = 0.001, 0.44) do not have that defect but run on five seeds. No multiplicity
correction is applied to the Fisher family and none should be read as implied: across its
nine tests a Bonferroni threshold is 0.05/9 = 0.0056, which neither *p* = 0.017 nor
*p* = 0.007 meets. The six permutation tests are not folded into that family and get no
correction of their own for a different reason — each is a named primary or fork inside a
locked decision rule, and both of those rules returned unusable verdicts (unclassified on
wave 1, FAILED on wave 2), so no claim rests on any of the six whatever threshold is
applied to them. The two Spearman diagnostics are likewise uncorrected and support no claim.
The figures are reported as descriptive effect sizes with exact tails attached, not as
hypothesis tests supporting the claims, which rest on the registered predictions instead.

**Twelve are exact lineage-level permutation tests on the post-hoc search-progress
statistic** — six on accepted improvements (*p* = 0.0008, 0.0079, 0.0079, 0.135, 0.116,
0.238) and six on final best score (0.593, 0.937, 0.421, 0.318, 0.158, 0.119). This family
is the newest and the least protected: it was specified after the data existed, it is
largely the echo contrast in complement, and it carries no registration. A Bonferroni
threshold across its twelve tests is 0.05/12 = 0.0042, which only *p* = 0.0008 meets;
neither fresh-seed nor within-ladder tail at 0.0079 survives it, and we state that rather
than reporting the tails unqualified. Those two tails are additionally *at the floor* of a
five-versus-five enumeration (2/252), so no design at this lineage count could have cleared
the threshold — the correction is not merely unmet here, it is unmeetable without more
lineages. These twelve do not have the nesting defect the
candidate-level Fisher tests have, because the permutation unit is the lineage — but five
lineages per cell is a small pool and the exact enumeration (252 splits for a 5-versus-5
comparison) bounds how small any tail can be. We additionally computed a call-level Fisher
tail on the IQ2 control's step counts (*p* = 0.028) and report it here only to record that
we do not use it: calls within a lineage are not exchangeable, the lineage-level tail on
the same counts is 0.135, and the more favourable number is the wrong one.

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
("26 of 27 circles unchanged") and affects no claim. We record it rather than quietly
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

**At 14B, a cliff — in proposal variation, not in viability** (combined §5.9). Scaling lifts the
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
source before execution. Those runners are released — `sec3_artifacts/runners/` — so the
registrations are readable where they were written rather than only as our description of
them: `kaggle_precision_sweep_14b_fresh.py` opens "PREREGISTERED PREDICTIONS — written and
pushed BEFORE this run executed" and states the fresh-seed bound as `q2_k >= 60%;
q4_k_m <= 35%`, and `kaggle_precision_sweep_14b_iq2.py` carries the must-differ decision
rule the same way. Earlier drafts asserted this without shipping the file, which left the
one registered support §3's surviving claim leans on unverifiable from the artifact.
This is a **re-execution, not a replication**: llama.cpp's seeded
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
into that ladder. Read at face value this says a lower-bit quantization from a different
family preserves more proposal variation than a higher-bit K-quant — but the fixed-parent
control below withdraws that reading, and we flag the withdrawal here rather than 240 lines
later so the sentence is never read on its own.

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

**A fixed-parent control narrows the contrast on the three rungs it covers.** Q8_0 was
*registered* as a fourth condition — both waves list it under `rungs` in `provenance.json` —
and in both waves it was never attempted: each `provenance.json` records the reason verbatim
as `"q8_0": {"skipped": "needs 2 gpus, have 1"}`. The 8-bit weight file did not fit the
single P100 the kernels were allocated. We name the mechanism rather than saying "the
condition failed," because the two are not equivalent for a reader deciding what the gap
costs: a hardware ceiling is recoverable on a larger allocation, whereas a run that produced
unusable output would not be. Its ladder figure, 2/18 inside the pooled 8/57, is therefore
uncontrolled and stays as measured, and a reader should treat the probe as covering three of
the ladder's four rungs. This is also the fact that decides the second wave's registered
verdict, below.
The echo rates just reported are measured against each lineage's *running* parent, and
those parents are not distributed alike across rungs: Q2_K lineages rarely improve, so
their parent mostly remains the seeded 0.900 grid, while upper rungs climb away from it.
Parent quality is therefore confounded with rung, and the confound runs in the direction
that flatters the result.

A fixed-parent dispersion probe measures the same quantity without that confound. It runs
the same Qwen2.5-Coder-14B at the same three rungs, holding the parent constant at each of
six preset scores from 0.88 to 1.65, and logs coordinates and an echo flag per row
(`sec3_artifacts/dispersion_probe/probe_samples.jsonl`, 288 rows: 165 valid, 123 invalid; the table counts
valid rows, as elsewhere in this section). Of those 123 invalid rows, **18 are harness
failures, not model failures** — `gen_error: ValueError: logprobs is not supported`, exactly
six per rung, so they neither bias between rungs nor belong in a denominator of model
behaviour. The v2 wave has **none**: its rows carry no `gen_error` field at all, and of its
158 invalid rows exactly one records a parse failure (`parse_error: bad_triple`), which is a
model failure and stays in the denominator. An earlier draft of this section said the v2
wave had one harness row; that was wrong. We report the split because §6 item 3 asks
everyone else to.

*The probe's own registration, reported in full.* The probe carries an analysis
preregistration (`sec3_artifacts/dispersion_probe/analysis_prereg.md`, written before any metric was read,
with an amendment timestamped before any output file was downloaded). The second wave
(`sec3_artifacts/dispersion_probe_v2/`, 432 rows on out-of-sample salted seeds) is not merely a repeat run:
it carries a preregistration of its own (`analysis_prereg_v2.md`) plus a truncated-run
addendum, and therefore a registered verdict of its own.

**That verdict is FAILED, and it belongs before any v2 number we quote.** Addendum rule R2
requires a ceiling rung to land; q8_0 did not land, for the hardware reason given above.
Under the wave's own rule no trend test is reportable and every descriptive it produces is
*exploratory*. The released analyser prints the label unprompted —
`python sec3_artifacts/dispersion_probe_v2/analyze_v2.py` ends in
`VERDICT: FAILED / addendum R2: ceiling rung q8_0 did not land; no trend test reportable`.
Earlier drafts omitted both this label and the wave's registered primary test — the
selective-reporting failure §6 item 3 asks of everyone else, committed here by us.
Appendix A.1 records what was omitted and in which direction each omission cut.

*The v2 registered primary, now reported.* The registered primary is the pooled rarefied
distinct-solution count at matched depth, with a per-parent Jonckheere-Terpstra over 10,000
shuffles. At m = 84 it returns 38.31 ± 1.64 / 46.78 ± 1.30 / **13.00 ± 0.00** distinct
solutions across Q4_K_M / Q3_K_M / Q2_K, with JT = 83.50 against a null mean of 53.92 and
permutation *p* = **0.0081**. Its registered score fork returns JT *p* = 0.3526 — no monotone
decline in quality, so this is a variation effect and not general degradation. Two
qualifications attach and neither is optional. First, the wave is FAILED by its own rule, so
this number is exploratory and cannot carry confirmatory weight however favourable it looks.
Second, it is **non-monotone in exactly the way v1's spread test is**: 46.78 at Q3_K_M sits
*above* 38.31 at Q4_K_M, so the whole effect is Q2_K collapsing to 13.00. Across both waves
the replicable statement is "distinct solutions collapse at the 2-bit rung," never "distinct
solutions decline with quantization."

The three registered echo-family measures, on both waves
(`sec3_dispersion_registered.py`) — the probe registers three, not one, and reporting only
the third would be the same failure again:

| measure | Q4_K_M | Q3_K_M | Q2_K |
|---|---|---|---|
| registered centers-only echo (max index-wise centre displacement < 1e-3) | 64/65 (98%) | 47/51 (92%) | 48/49 (98%) |
| registered **primary echo measure** (median per-circle centre displacement; §2 of Amendment 1 designates this the primary and requires a JT test — reported below) | 0.000000 | 0.000000 | 0.000000 |
| retained legacy echo (1e-5, all three fields) | 34/65 (52%) | 31/51 (61%) | 46/49 (94%) |
| legacy echo, v2 replication | 56/99 (57%) | 41/91 (45%) | 77/84 (92%) |

**The registered centres measures show no cliff** — but the design limits what that can
mean, and the limit is severe enough to state before the number. All six of the probe's
"parents" share **identical centres**; they differ only in their radius assignments, from a
uniform 0.900 grid up to a 1.65 packing with 26 distinct radii. The probe therefore shows
the model one lattice in every condition. Centre-echo measures whether the model reproduces
*that* lattice, and cannot observe what would happen to a proposer that moved to a
different one. It runs 92-98% across all three rungs on both waves, with median per-circle
centre displacement exactly zero everywhere — but "the lattice is copied throughout" is a
statement about the only lattice ever presented, not a general finding about constructive
novelty, and we do not use it as one.

What the design *can* measure is radius variation, because radii are what the parents
actually vary. On that axis the cliff appears, and the correct statement of what degrades
is narrower than "the ability to propose a novel construction": within this fixed lattice,
the upper rungs perturb radii and Q2_K does not.

That reframing is not favourable to the original wording and we adopt it. It also locates
the effect rather than dissolving it. Decompose the valid rows by what each one copies. This
decomposition is **post-hoc** — it appears in no preregistration, it was constructed after
the registered centre measures came back flat, and we label it as such everywhere it is
used. Both waves, so that its stability can be judged rather than assumed:

| rung | centres copied **and radii varied** | centres copied and radii copied | centres varied |
|---|---|---|---|
| Q4_K_M, v1 | **30/65 (46%)** | 34/65 (52%) | 1/65 |
| Q3_K_M, v1 | **16/51 (31%)** | 31/51 (61%) | 4/51 |
| Q2_K, v1 | **2/49 (4%)** | 46/49 (94%) | 1/49 |
| Q4_K_M, v2 | **39/99 (39%)** | 56/99 (57%) | 4/99 |
| Q3_K_M, v2 | **46/91 (51%)** | 41/91 (45%) | 4/91 |
| Q2_K, v2 | **5/84 (6%)** | 77/84 (92%) | 2/84 |

**Before reading the table, note what its middle column is.** "Centres copied and radii
copied" is not a new quantity: it is *identically* the legacy echo count, in all six cells —
34/65, 31/51, 46/49 on v1 and 56/99, 41/91, 77/84 on v2, the same numbers as the legacy row
of the previous table. A row that copies both fields is an echo by definition, so the
decomposition cannot and does not add evidence there. All it adds is a partition of the
*non-echo* rows into "varied the radii" and "varied the centres". At Q2_K on v1 that is
three rows, split 2 and 1. We state this because the alternative is to present a
re-partition of an already-reported statistic as if it were a second, independent result,
and that is the failure §6 exists to indict.

With that understood, read down the first column, and read the two waves against each other
rather than quoting one. **The 2-bit endpoint replicates and the ordering above it does
not.** Radius perturbation stands at 4% and 6% at Q2_K on the two waves independently; between
the upper rungs the ordering *reverses*, 46% above 31% on v1 and 39% below 51% on v2. An
earlier draft quoted v1's 46% as "the upper rungs," which both overstated a single rung's
rate as a pair's and rested on the one contrast the second wave contradicts. And the
endpoint's replication is the **echo** replication — 94% and 92% — restated in its
complement, not a separate confirmation of it. What the probe supports is therefore this,
and no more: within the lattice it presents, upper-rung proposals perturb radii in 31-51% of
valid rows with no stable ordering between the rungs, while at Q2_K almost every valid row
is an outright copy, leaving 2 of 49 and 5 of 84 that perturb radii. That contrast is
within-design — radii are the dimension the parents vary. It is very nearly the echo
statistic seen from its complement rather than a second result, and should be read that way;
what it genuinely adds beyond the echo count is only the split of the non-echo rows into
radius-varying and centre-varying, which at Q2_K on wave 1 is three rows divided 2 and 1.
That split is real and it is thin, and we claim it at that size.

The honest scope is then this. On the one lattice presented, the proposer's realised
variation is radius perturbation, and quantization to 2 bits removes it. Whether a
better-served proposer would have moved to a *different* lattice is a question this design
cannot answer, because it never offers one — so we cannot say from this probe whether
quantization removes constructive novelty or only the last dimension of a search that was
already narrow. Both readings are consistent with the table, and the loop condition
(§3 above) is the setting where the broader question would have to be asked.

The registered quality fork is satisfied on both waves — it is tabled with its test
statistic below for wave 1 and reported above for wave 2 — so what the probe shows is a
variation effect and not general degradation.

*The registered decision rule, run.* The remaining two registered analyses are computable
from the released rows — `raw_text` is present in all 165 valid rows and the Amendment 1
descriptor is defined on centres, i.e. on `circles` — so we ran them rather than leaving
them out.

One disclosure must precede the table, because it limits how the first row reads. **The
spread statistic is reconstructed, not replayed.** The preregistration names it by the
generating kernel's field, that kernel is absent from the corpus, and its one surviving
logged value is negative, so its definition is unrecoverable; we substituted an explicit
Levenshtein-based definition of our own. Row 1's *p* = 0.030 is therefore the registered test
run on our reconstruction, and a reader who rejects the reconstruction should treat it as
unavailable rather than as evidence either way. Appendix A.2 gives the numbers and why the
substitution was forced.

All outcomes, including those against us:

| registered analysis | result | direction |
|---|---|---|
| primary spread: JT on per-parent mean pairwise NED, valid only, 10,000 permutations | mean NED 0.0872 / 0.1060 / 0.0291; JT = 31.0, *p* = 0.030 | declines — **favourable** |
| primary **echo** measure: JT on per-sample median centre displacement, 10,000 permutations | medians 0.000000 / 0.000000 / 0.000000; JT = 4460.0 against null mean 4498.5 (sd 108.4), *p* = 0.686 | flat — **unfavourable**, and degenerate (below) |
| Amendment 1 rarefaction: unique cells on the centres-only descriptor at matched m = 49 | 1.774 ± 0.418 / 2.000 ± 0.000 / 2.000 ± 0.000; *p* = 0.953 | wrong sign — **unfavourable** |
| quality fork: JT on mean score among valid | 1.23855 / 1.22889 / 1.25966; *p* = 0.454 | no monotone decline |
| quality fork, registered second half: mean `score_delta` vs parent, bootstrap 95% CI | +0.00725 [+0.0018, +0.0139] / −0.00329 [−0.0254, +0.0113] / −0.00199 [−0.0211, +0.0151] | flat; only Q4_K_M excludes zero |
| power floor (rule 4) | m = 49, six defined parents per rung | not underpowered |

Rows 2 and 5 were unreported before this draft; row 2 is the measure §2 of Amendment 1
designates **the primary**, and its *p* = 0.686 is unfavourable. Both it and the rarefaction
row are **degenerate rather than flat** — 159 of 165 valid rows have a median displacement of
exactly zero, so each test is very nearly all ties and its *p*-value is saturation, not
evidence. The tie convention is also ours: the v1 preregistration names Jonckheere-Terpstra
and specifies none, and with 159 of 165 rows tied it is nearly the whole statistic.
Appendix A.3 gives the per-rung zero counts, the tie rule adopted, and what each omission
had cost.

**Under the registered replacement rule this returns no category.** SURVIVES needs both
spread measures at *p* < 0.05 and rarefaction is 0.953; PARTIAL needs score to decline
monotonically and it does not; FALSIFIED needs both spread measures flat and NED is 0.030;
UNDERPOWERED does not apply. The honest label is unclassified. That disqualifies the
*registered mechanism verdict* specifically, and we make no use of it; it does not
disqualify the probe's descriptive counts, which are reported above as descriptive and
labelled post-hoc where they are.

Two further caveats, both of which cut against reading the favourable half alone. The NED
decline is **not monotone** — Q3_K_M (0.1060) sits *above* Q4_K_M (0.0872), and the entire
effect is Q2_K collapsing — so "spread declines with quantization" overstates a result that
is really "spread drops at the 2-bit rung." And the rarefaction instrument had no resolving
power on this data: 159 of 165 valid rows have centre displacement exactly zero, so the
pooled quantile edges collapse and the 64-cell grid has **two** occupied cells, both
occupied by every rung. Its *p* = 0.953 is saturation, not evidence of flatness. That
degeneracy is a direct consequence of the single-lattice design noted above — the
descriptor was built to detect movement the design never gave the model an occasion to
make. The prespecified orthogonality check passes on its registered criterion — Spearman
rho = +0.1672 for the spread descriptor and −0.1675 for the displacement descriptor against
score, both far below the registered |rho| > 0.5 confounding threshold. Passing that
threshold is not the same as independence, and we do not report it as such: at n = 165 both
correlations are nominally non-zero (*p* = 0.032 and 0.032). The registered rule asks only
whether either descriptor is *confounded* by scoring, and neither is by its stated
criterion; a weak residual association remains and is stated rather than rounded away.

Because Q8_0's condition failed, the registered four-rung trend was run on three rungs, with
correspondingly less power than preregistered. The probe does not cover the IQ2 files.

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

Three consequences follow.

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
particular its closing reading — that a lower-bit quantization from a different family
preserves more proposal variation than a higher-bit K-quant — does not survive the
control, and should be read as a statement about the loop condition alone. (That sentence
was phrased in terms of "constructive novelty" in earlier drafts; §3 no longer uses the term
for anything this design measures, and the withdrawal applies to the claim under either
wording.)

*The registered upper-rung bound is design-specific.* The prediction "each upper rung ≤
35%" held at 11-16% under the loop condition and would have **failed** under fixed parents
at 52-61%. It was registered against the loop design and is correctly scored there, but a
reader should not carry it as a general property of those rungs.

The probe is not a substitute for the loop measurement: a fixed parent removes the lineage
history the loop includes, so the two conditions are not interchangeable, and the loop is
the condition this paper's argument is about. It is, however, the better-controlled
comparison on the one axis where the loop design is confounded.

**What the loop actually did: search progress at the lineage level.** Every measure to
this point is a property of a single call — was this output viable, valid, an echo of its
parent. None of them reports what the *loop* did with those calls, which is the quantity a
practitioner running a discovery loop is actually paying for. We close §3 with that
measurement. It is **post-hoc**: it appears in no preregistration on any wave, and it is
reported as a consequence of the registered echo result rather than as an independent test
of it. Released as `sec3_search_progress.py`.

Define an **accepted improvement** as a valid output scoring strictly above its lineage's
running best — one hill-climb step actually taken. On the registered 14B ladder, across
five lineages of ten generations each:

| rung | accepted steps per lineage | total | valid | echo | final best per lineage |
|---|---|---|---|---|---|
| Q2_K | 0, 0, 0, 0, 1 | **1/50** | 18 | 17 | 0.900, 0.900, 0.900, 0.900, 1.625 |
| Q3_K_M | 4, 3, 4, 2, 2 | 15/50 | 19 | 3 | 1.040, 1.300, 0.962, 1.625, 1.248 |
| Q4_K_M | 6, 3, 2, 3, 2 | 16/50 | 20 | 3 | 1.060, 1.300, 0.936, 1.040, 0.933 |
| Q8_0 | 2, 2, 5, 1, 4 | 14/50 | 18 | 2 | 0.936, 1.300, 0.926, 1.083, 1.040 |

Four of five Q2_K lineages take **zero** steps in ten generations: their running parent is
still the seeded 6 × 5 grid at generation nine.

**The identity this rests on, stated before the inference.** An echo reproduces the
parent's coordinates and therefore its score exactly, and the acceptance rule is strict, so
an echo can never be an accepted improvement: `accepted ≤ valid − echo` holds by
construction. The gap *k* between the two is 0, 1, 1 and 2 across the four rungs — rows
that did depart from the parent and still failed to beat it. **Most of the contrast in the
table above is therefore the echo contrast seen in complement, not a second independent
result**, and we do not present it as one. What the table adds is the *unit*: the echo
result is a rate over calls, this is a count of steps over a lineage, and the second is the
quantity a loop's cost is denominated in.

**A registered prediction on nearly this quantity failed, and the difference between the
two is an analytic choice we made after seeing the data.** The fresh-seed runner's F1 is a
registered improvement prediction: ≤ 2/5 Q2_K seeds and ≥ 4/5 Q4_K_M seeds improving past
the seeded baseline. It **failed** — 3/5 Q2_K seeds improved, Fisher *p* = 0.44 against
5/5 — and §3 reports that failure above and demotes the binary improvement count to a
fragile correlate. The statistic in this subsection is computed from the same rows: F1 asks
*whether* a lineage improved at all, this asks *how many times* it did. On the fresh wave
the coarse registered form gives 3/5 versus 5/5 and does not separate the rungs; the finer
post-hoc form gives 3 steps versus 14 and does, at *p* = 0.0079. That gap is an instance of
analytic flexibility and we treat it as one, not as a repair of F1, and a
reader is entitled to weigh the two accordingly: the registration made the coarse choice,
the coarse choice failed, and the finer choice that succeeds was made by us with the
ledgers open. We report the count statistic because it is the quantity a loop's cost is
denominated in and because withholding it would be its own distortion — but it does not
inherit F1's registration, it does not repair F1's failure, and no claim in this paper
rests on it. The registered signature of the cliff remains the echo rate.

**The part not implied by the echo result — and why we cannot resolve it.** Conditional on
*departing* from the parent (valid and not an echo), the fraction that improved is 1/1 at
Q2_K, 15/16 at Q3_K_M, 16/17 at Q4_K_M, 14/16 at Q8_0; on fresh seeds 3/5 against 14/16;
on the IQ2 control 6/8 against 16/16. This asks whether quantization degrades the *quality*
of departures or only their *frequency* — a mechanistically different claim, and the more
consequential one, since a frequency-only effect is in principle repairable by forcing
departure while a quality effect is not. Every 2-bit cell has a departure count under ten
and one has a count of **one**. The question is posed by these data and answered by none of
them; reading the 1/1 cell as "flat" would be an inference off a single observation. We
name it as the measurement the next wave should be powered for. It is also not obviously
repairable by instruction: the registered must-differ probe (above) instructed the proposer
explicitly not to copy and returned 5 of 5 echoes anyway.

**Replication is partial, and the level of the test decides it.** At lineage level, by
exact permutation over every split of the pooled lineages — the same machinery the
dispersion probes' registrations use — the registered ladder gives *p* = 0.0008 against
the pooled upper three (15 504 splits) and *p* = 0.0079 against Q4_K_M alone (252 splits).
The five never-sampled fresh seeds replicate: 3 steps against 14, *p* = 0.0079. **The IQ2
control does not**: imatrix Q2_K takes 6 steps against IQ2_M's 16, and the exact
lineage-level tail is *p* = 0.135. **Both 0.0079 figures sit exactly on the design's floor**:
a five-versus-five exact permutation enumerates 252 splits, so the smallest two-sided tail
it can return is 2/252 = 0.0079 whatever the effect size. Those two tests are maximally
extreme — no split of the observed lineages is more extreme than the observed one — and
that is the whole of what they establish. A design capable of distinguishing a large effect
from an enormous one needs more lineages per rung, not more generations per lineage; eight
per rung would lower the floor to 1.6e-4. A call-level Fisher test on the same counts returns
*p* = 0.028 and we report the lineage-level figure instead, because whether call *k* can
improve depends on which improvements landed at calls before it in the same lineage, so
calls within a lineage are not exchangeable and the call-level tail overstates the
evidence. That choice costs us the IQ2 replication; the alternative would have been to bank
a significance the design does not support.

**The outcome metric is blind to all of it.** Final best score after ten generations —
the number a practitioner would report from such a run — does not separate the rungs
anywhere. On the registered ladder Q2_K's mean final is 1.045 against 1.115 pooled
(*p* = 0.593) and 1.054 for Q4_K_M (*p* = 0.937); on fresh seeds Q2_K is *higher*, 1.153
against 0.999 (*p* = 0.421); on the IQ2 control 1.087 against 0.922 (*p* = 0.318). This is
**non-rejection at five lineages per cell, not demonstrated equivalence** — the same
discipline §3 applies to viability — and the per-lineage finals printed above show why the
means are weak summaries: the score support is lumpy and discrete (0.900, 0.936, 1.040,
1.300, 1.625), so one lucky jump in a Q2_K lineage lands on the same rung of that ladder
that four small Q4_K_M steps climb to. The finding is the *blindness*, not an absence of
harm: **an order-of-magnitude collapse in search activity, 1 step against 14–16, leaves the
reported outcome statistically indistinguishable at this horizon.** That is §3's instrument
argument one level up — viability and validity cannot see the echo collapse, and final best
score cannot see the search collapse either.

Whether the gap opens at longer horizons is the obvious next question and we register it
here as a **prediction rather than a result**: a process taking 1 step per 50 calls and one
taking 15 should diverge in final best score as the generation budget grows, and if a run
at 50 or 100 generations per lineage does *not* separate them, the practical significance
of the collapse is smaller than this section's framing implies. We did not run it.

**At 7B the statistic does not replicate, and reverses.** The 7B ladder stores no
coordinates, so echo is not computable there — but accepted improvements are, which gives
this measure a second scale at no cost. Across five rungs the step counts are FP16 6/50,
Q8_0 2/50, Q4_K_M 3/50, Q3_K_M 4/50, **Q2_K 7/50** — the 2-bit rung takes the *most* steps
of the five, and the permutation tail against the pooled others is *p* = 0.116, against
Q4_K_M *p* = 0.238. Neither direction is established. Validity at 7B runs 4–12 of 50 at
*every* rung, so no rung at this scale is searching enough for the statistic to have room
to separate, and the reversal sits with the viability inversion §3 already reports at 7B
rather than contradicting anything. What it does establish is the scope: **the search-step
collapse is a 14B observation and is not a property of the quantization ladder as such.**

**What varied, and what did not.** This distinction is load-bearing for the rest of the
paper, so it comes before the transfer. Across every run in this section the
inference stack was *constant*: the same llama.cpp build, the same 2 × T4 hardware, the
same sampling parameters, the same harness. The only thing that changed was which
SHA-256-pinned weight file was loaded. What is measured here is therefore the effect of
**served-weight quantization**, not of a decode path, a kernel, a batching regime, or a
speculative-decoding scheme.

Served quantization is a genuine element of a serving stack — a deployer chooses which
quantization to serve, and an alias does not report that choice — which is why the finding
bears on alias opacity at all. But it is *one* element. That degrading it selectively
collapses the variation a proposal carries does not establish that other serving-stack
variables do the same, and we do not claim it. The generalization from this variable to the stack is the
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
It does not survive definition. We report it as a non-finding because the reasoning
generalizes to any study reading a single aggregate usage integer. The harness log records a single per-invocation usage figure that is
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
35, 37 — so the N = 13 and N = 31 digests above verify against it directly. N = 21 is
absent from that file, but the digest above is still checkable: substituting `21` for `13`
in the released N = 13 prompt reproduces `a415425b…` byte-exactly, which is what the
fixed-template design guarantees. We note the omission because a reader should not have to
derive it, and re-releasing the file with all six sampled cells costs nothing.) Every raw output is
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
the text rather than from the original implementation, and it re-derives §3's 14B viability,
validity, echo, per-seed, must-differ and invalid-row figures from the raw ledgers, together
with five of the section's nine Fisher tails — the other four and the 7B paragraph it does
not touch, as §3 states where it reports them. §4 was
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
now-demonstrable way, and §3 establishes that **one** of the unrepeatable variables — served
weight precision — is one the outcome is sensitive to. Whether the others on this list
behave alike is the hypothesis §3 raises and does not test, and the plural should not be
read into it. The correct response is disclosure, not retraction.

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
is an uncomfortable position: the
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

5. **A parent-echo canary, runnable in under an hour before you trust a proposer.** Items
   1-4 are disclosure. This one is a check, and it is the one thing this paper's data
   supports as an instrument a practitioner can run today. The failure mode §3 documents is
   invisible to viability, validity and — per §3.6 — to final best score at a ten-generation
   horizon, so a loop can be degenerate for its whole budget while every dashboard reads
   healthy. The statistic that does see it costs nothing to compute:

   > **The screen.** Hold a parent configuration *fixed*. Issue 25-50 proposal calls
   > against it at your production settings. Log the emitted structure verbatim, not only
   > its score. Compute the fraction of *valid* outputs whose structure equals the parent's,
   > compared order-insensitively at the precision your logs carry (we use six decimals).
   > **A rate at or above 60% is a red flag**; at or below 30% the proposer is departing
   > normally.
   >
   > **The five-call version.** Append an explicit prohibition — the output must differ
   > from the parent, at least three elements must change, returning it unchanged counts as
   > failure — and issue five calls. Five echoes out of five is the signal. That is what we
   > observed at Q2_K, against 1 of 5 at Q4_K_M.

   The thresholds are not invented for this section: 60% and 30% are the bounds
   preregistered in the fresh-seed runner before that run executed, and they held at 79%
   against 6%. The screen needs no held-out set, no baseline model, and no scorer beyond the
   validity check a loop already runs — the whole cost is logging structures instead of
   scores.

   **What it is and is not.** It is a canary for a specific, severe endpoint, validated on
   one task, one model family, one scale and one quantization family. It is **not** a
   calibrated precision detector. Two limits decide how to read a reading in the middle of
   the band. First, the echo rate depends on the parent: §3's fixed-parent control moves the
   upper-rung baseline from 6% to 33-52% depending on parent quality, so a 40% reading tells
   you very little unless your parent is matched to ours, which it will not be. Second, the
   contrast is established at a 2-bit endpoint; §3's own scheme control returns its
   inconclusive branch, so a rate between the bounds does not localise the cause to
   quantization at all. Used as a tripwire — *something is wrong with what is serving this
   proposer* — the screen is supported by the data above. Used as a measurement of served
   precision, it is not. We state the distinction because the failure mode of a cheap screen
   is that it gets quoted as the second thing.

   Released as `echo_screen.py`, which takes a JSONL of proposals with their fixed parent
   and prints the rate, the count, an exact binomial interval and the verdict label.

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
filters against. What we claim is narrower and, we think, new: that the *rate* of it rises
sharply at the 2-bit rung of one quantization ladder on one task at one model scale — 14% to
94% in the loop condition, discounted to 33% against 92% once parent quality is
controlled — so a mitigation tuned at one precision may be asked to do a substantially
different amount of work at another, with no signal that the amount changed. We have not
shown this varies smoothly with bit width, and the fixed-parent control is the reason to
state the endpoint rather than a gradient.

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
inside a selection loop and finds the axis it moves — the variation a proposal carries away
from its parent — is not the axis any of these benchmarks score.

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

The fixed-parent dispersion probe, on which §3's strongest control rests, carries four
limits that we state here as well as in place. **Its design presents one lattice.** All six
"parents" share identical circle centres and differ only in radii, so the probe can measure
radius variation and cannot observe a proposer moving to a different construction; the
centre-echo result of 92-98% at every rung is a statement about the only lattice ever shown.
**Neither wave yields a usable registered verdict.** Wave 1's locked rule returns no
category, and wave 2's own addendum returns FAILED because the ceiling rung was never
attempted — both `provenance.json` files record it as skipped for want of a second GPU. Every
figure either wave produces is therefore descriptive, and no claim in this paper rests on
one. **The registered spread statistic is reconstructed, not replayed.** Its generating
kernel is absent from the corpus, so we substituted an explicit normalized edit distance
(§3); a reader who declines the substitution should treat that test as unavailable. **The
decomposition that carries the §3 result is post-hoc**, and only its 2-bit endpoint
replicates across waves — the ordering between the upper rungs reverses. What survives all
four is narrow and we state it as such: within the presented lattice, radius perturbation
collapses at the 2-bit rung, on two independently seeded waves.

The loop-level search-progress statistic of §3.6 carries three limits of its own. **It is
post-hoc and it is a finer form of a registered prediction that failed** — F1 forecast the
binary improvement count and was refuted on the fresh wave; the step count is our choice,
made with the ledgers open, and it does not inherit F1's registration. **Most of it is the
echo result in complement** (§3.6). **It does not replicate at the second scale or on the scheme
control.** At 7B the 2-bit rung takes the most steps of five rungs, and on the IQ2 pair the
exact lineage-level tail is *p* = 0.135. What survives is one ladder at one scale with a
fresh-seed replication that does not clear a Bonferroni threshold across its own family,
and an outcome-level null we report as non-rejection at five lineages per cell rather than
as evidence of no harm.

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

Every row names a file a reader can open **inside the released repository**. Earlier drafts
satisfied the first half of that sentence and not the second: every §3 row pointed into
`../agent-run/` or `../../handoff/`, sibling trees on the authoring host that no clone
contains, so a reader could see the path and not the data. The §3 artifacts — both
dispersion-probe waves with their preregistrations, provenance and analyser, and the four
ladder output trees — are now vendored under `sec3_artifacts/` (95 files, 1.8 MB), and the
released scripts default to those in-repo copies, so `python sec3_dispersion_registered.py`
and `python sec3_artifacts/dispersion_probe_v2/analyze_v2.py` both run in a fresh clone with
no arguments. Dependencies are declared in `requirements.txt`. Where a figure is *not*
checkable from the released artifacts, the row says so instead of pointing at a document
that merely repeats it.

| claim | source |
|---|---|
| §3 14B ladder: viability 22/22/24/19, validity 18/20/19/18, echo 2/18, 3/20, 3/19 and 17/18, per-seed vectors, invalid-row near-copy fractions | `sec3_artifacts/precision_sweep_14b_v2_output/**/candidates_precision_14b.jsonl` (200 rows), replayed by `sec3_ladder_repro.py` |
| §3 fresh-seed replication: 19/24 vs 1/17, per-seed 4/5, 4/5, 5/6, 2/2, 4/6 | `sec3_artifacts/precision_sweep_14b_fresh_output/**/candidates_precision_14b_fresh.jsonl` (100 rows), same script |
| §3 must-differ probe: 5/5 at Q2_K, 1/5 at Q4_K_M; 6/8 vs 0/2 on the IQ2 pair | `sec3_artifacts/**/mustdiffer_14b.jsonl`, `mustdiffer_14b_iq2.jsonl`; echo computed against the fixed seed parent, no echo flag in the ledger |
| §3 IQ2 control: 24/32 vs 12/28 | `sec3_artifacts/precision_sweep_14b_iq2_output/**/candidates_precision_14b_iq2.jsonl` (100 rows), same script |
| §3 fixed-parent dispersion control: 34/65, 31/51, 46/49 and the parent-score gradient | `sec3_artifacts/dispersion_probe/probe_samples.jsonl` (288 rows), `echo` field as labelled |
| §3 served weight files (SHA-256, byte length, repo, sampling parameters, GPUs) | `provenance.json` in each of the three ladder output directories |
| §3 seeded parent (26-circle 6 × 5 grid, score 0.89999) | `sec3_artifacts/precision_sweep_14b_v2_output/**/state/q2_k_seed_42.json`, a lineage that never improved |
| §3 Fisher figures **recomputed by a released script**: *p* = 1.7e-7, 3.4e-6, 0.007, 0.017, 0.056 | `sec3_ladder_repro.py` prints each as a `Fisher check` line beside the paper's rounded value |
| §3 Fisher figures **not replayed by any released script**: *p* = 5.7e-10 (17/18 vs 8/57), 0.001, 0.44, 1.0 | counts are in the vendored ledgers and the 7B `sec3_artifacts/precision_sweep/` outputs, but a reader must compute these four tails themselves; stated as a boundary in §3 |
| §3 inferential status of all twenty-nine *p*-values | §3: nine Fisher, six preregistered permutation tests, two Spearman orthogonality diagnostics and twelve post-hoc lineage-level permutation tests; the four families not pooled, the reason given for each, and the Bonferroni threshold stated for the Fisher and post-hoc families |
| §3.6 search progress: accepted steps per lineage (1/50, 15/50, 16/50, 14/50 on the registered ladder; 3/50 vs 14/50 fresh; 6/50 vs 16/50 IQ2; 7/50, 4/50, 3/50, 2/50, 6/50 at 7B), the identity gaps *k*, the conditional-on-departure rates, final best per lineage, and all twelve exact permutation tails | `sec3_search_progress.py`, run with no arguments; replays all four vendored ledgers. **Post-hoc** — labelled as such at every use, and §3.6 states that the registered form of this quantity (fresh-seed F1) failed |
| §3.6 the failed registered improvement prediction F1 (≤ 2/5 Q2_K, ≥ 4/5 Q4_K_M; observed 3/5 vs 5/5) | `sec3_artifacts/runners/kaggle_precision_sweep_14b_fresh.py` header, readable in the file that carried it; outcome computed by `sec3_search_progress.py` from the fresh ledger |
| §3 7B ladder | `sec3_artifacts/precision_sweep/`; narrative and scope caveats in `sec3_artifacts/precision-cliff-paper-combined.md` §3.4, §5.9, §6 |
| §3 IQ2_M invalid near-copy 2/22 | **not reproduced**: our replay of the stated definition returns 1/22 (§3) |
| §4 validity, failure taxonomy, families, scores, both tolerances | `arm_f_raw.json` `opus_alias` / `sonnet_bare` / `bare` rows, recomputed with `arm_f_repro.py` |
| §4 durations | `STATE.md` §8, §8b — session-log ranges; per-invocation vector not captured (§4, §5) |
| §4 registration digest | `arm_o_preregistration.txt`, SHA-256 published in §4 |
| §5 prompt digests, N = 13 and N = 31 | `arm_f_repro.py` `prompt_hash()`, `arm_f_prompts.json` |
| §5 prompt digest, N = 21 | absent from `arm_f_prompts.json` but derivable: substituting `21` into the released N = 13 prompt reproduces the digest exactly (§5) |
| §3 probe's registered centres-echo, the registered primary median-displacement measure, and the v2 wave's counts | `sec3_artifacts/dispersion_probe/`, `sec3_artifacts/dispersion_probe_v2/`, recomputed by `sec3_dispersion_registered.py`; the median measure's registered JT test is in `sec3_registered_echo_test.py` |
| §3 probe's registered JT/NED test (*p* = 0.030), rarefaction count (*p* = 0.953), quality fork (*p* = 0.454), and the rule's unclassified verdict | `analysis_prereg.md`; computed in §3 from `raw_text` and `circles` in the released rows. NED is a substituted definition, not the kernel's — see the disclosure in §3 |
| §3 wave-2 registered verdict **FAILED**, its primary rarefaction (38.31 / 46.78 / 13.00 at m = 84, JT *p* = 0.0081) and score fork (*p* = 0.3526) | `sec3_artifacts/dispersion_probe_v2/analysis_prereg_v2.md` + `analysis_prereg_v2_addendum.md`; printed by `sec3_artifacts/dispersion_probe_v2/analyze_v2.py`, run with no arguments, which emits the FAILED label with the numbers |
| §3 wave-1 registered **primary echo** JT (*p* = 0.686, 159/165 rows at exactly zero), registered `score_delta` CIs, and the orthogonality *p*-values | `sec3_registered_echo_test.py`, run with no arguments; §2 of `sec3_artifacts/dispersion_probe/analysis_prereg.md` Amendment 1 designates this measure the primary |
| §3 ladder registrations (fresh-seed bound `q2_k >= 60%`, `q4_k_m <= 35%`; must-differ decision rule; improvement-count prediction) | `sec3_artifacts/runners/kaggle_precision_sweep_14b_fresh.py` and `..._iq2.py`, in the header comment block that was pushed before the run executed — the registration is readable in the file that carried it, not only as our description of it |
| §3 post-hoc decomposition, both waves (46/31/4% and 39/51/6%) | emitted by `sec3_dispersion_registered.py`; labelled post-hoc at every use. Its middle column is identically the legacy-echo count, stated in §3 |
| §3 probe's design limit (six parents, one shared lattice) and Q8_0's skipped condition | `sec3_artifacts/dispersion_probe/probe_samples.jsonl` (parent centre lists identical across all six `parent_id` values) and both waves' `provenance.json`, which record `"q8_0": {"skipped": "needs 2 gpus, have 1"}` |
| §3 probe's 18 harness-error rows | `sec3_artifacts/dispersion_probe/probe_samples.jsonl`, rows whose `parse_error` reads `gen_error: ValueError: logprobs is not supported`; six per rung. The v2 ledger has no such rows |
| §5 alias-map provenance and its gap | `ALIAS_MAP`, `RUN_DATE`, `PROPOSER_ALIAS` in `arm_f_repro.py` |
| §4 latency ranges (2.8-9 s vs 75-250 s and 150-1170 s) | **not checkable**: `STATE.md` §8, §8b working-log ranges only; the per-invocation vector was never captured, and `arm_f_raw.json` rows carry no duration field (§4, §6 item 4) |
| §6 item 3 worked example (32/45 → 32/50) | **not checkable**: the 45-row slice was overwritten in place and cannot be reconstructed (§4, §6) |
| §7 systems citations | `p8_systems_citations.md` (nine verified by the authors; this is self-certification and a reader should treat it as such) |
| §7 hazard-literature citations (2307.09009, 2603.19022, 2607.10252, 2607.08734, 2604.19884, 2509.19349, GUIDE-LLM, 2508.15503, 2601.01954, 2512.00651) | each checked against its live arXiv or publisher page; titles and author lists as printed there |

---

## Appendix A — the dispersion probes' registered analyses, in full

Section 3 reports every registered outcome of both probe waves, with its status label
attached, in the tables where it belongs. This appendix holds the derivation narrative that
those tables point at: what was omitted from earlier drafts, what we reconstructed and why,
and which conventions are ours rather than registered. Nothing here is a result that section
3 does not already state — it is the working behind the labels.

### A.1 What earlier drafts omitted from wave 2, and in which direction

Wave 2 carries `analysis_prereg_v2.md` and a truncated-run addendum. Addendum rule R2
requires a ceiling rung to land; q8_0 never ran, so the wave's own verdict is FAILED and
every descriptive it produces is exploratory. Earlier drafts described the wave as "a
registered confirmatory replication", quoted two of its outputs as replicating, and reported
neither the label nor the wave's registered primary test.

Both omissions are now corrected, and they cut in opposite directions:

| omitted | direction |
|---|---|
| the registered FAILED label | **against us** — it disqualifies every v2 number we had quoted as confirmatory |
| the registered primary (rarefaction 38.31 / 46.78 / 13.00 at m = 84, JT = 83.50 vs null 53.92, *p* = 0.0081) | **for us** — the best-powered registered result in the section, and we had left it out |

That the suppressed material included our strongest number as well as our worst label is the
reason to state the correction rather than quietly absorb it: selective reporting is not
only the omission of unfavourable results, and a reader cannot check which kind occurred
unless both are named.

### A.2 The reconstructed spread statistic

The v1 preregistration names its spread quantity by the generating kernel's field,
`mean_pairwise_ned`. That kernel is not in the released corpus. What survives of it is a
single logged value in `provenance.json` — `text_dispersion_mean_pairwise_ned` = **−0.3558**
for Q3_K_M. It is negative, so the kernel's quantity is not a normalized edit distance in
the usual sense, and its definition is unrecoverable from the artifact.

We therefore substituted an explicit definition: Levenshtein distance over `raw_text`
divided by the longer of the two lengths, averaged over unordered within-cell pairs. On that
same cell it returns **+0.1060**.

The substitution is forced rather than chosen — the preregistration wants the statistic per
parent and the kernel logged it only per rung, so no replay was available at the registered
granularity even had the definition survived. It is defensible, and it is still a
substitution, not a replay. Section 3's *p* = 0.030 is the registered test run on a
reconstructed quantity; a reader who declines the reconstruction should treat that row as
unavailable rather than as evidence in either direction.

### A.3 The registered primary echo measure, its degeneracy, and the tie rule

Section 2 of Amendment 1 designates median per-circle centre displacement **the primary echo
measure** and specifies a Jonckheere-Terpstra test. Earlier drafts printed the medians as a
descriptive "graded companion" and never ran that test. In fairness to those drafts, the
registration is ambiguous against itself here: "graded companion" is the preregistration's
own bolded heading for this measure, and the designation as primary sits in the same
sentence — `**Graded companion:** median per-circle center displacement per sample — this is
the primary echo measure, tested with Jonckheere-Terpstra.` The heading invites exactly the
reading the drafts took. It is still the wrong reading, because the sentence under the
heading is explicit, and the test goes unrun either way. Run in
`sec3_registered_echo_test.py`:

| rung | n | median | mean | rows at exactly zero |
|---|---|---|---|---|
| Q4_K_M | 65 | 0.000000 | 0.002323 | 64/65 |
| Q3_K_M | 51 | 0.000000 | 0.020092 | 47/51 |
| Q2_K | 49 | 0.000000 | 0.002126 | 48/49 |

JT = 4460.0 against a null mean of 4498.54 (sd 108.41), permutation *p* = 0.686 over 10,000
shuffles. The outcome is unfavourable, and it had been left unreported while the favourable
spread test was reported beside it.

It is also degenerate, in the same way and for the same reason as the Amendment 1
rarefaction: 159 of the 165 valid rows have a median displacement of exactly zero, so the
statistic is very nearly all tie credit and *p* = 0.686 measures saturation rather than
flatness. Both degeneracies trace to the single-lattice design — the descriptors were built
to detect movement the probe never gave the model an occasion to make.

One convention is ours and not registered. The v1 preregistration names Jonckheere-Terpstra
but specifies no tie rule, and with 159 of 165 values tied the convention is nearly the whole
statistic. We adopt the 0.5 tie credit that wave 2's addendum states, for consistency across
the two waves, and flag it here as a choice rather than a registered instruction.

The registered second half of the quality fork — mean `score_delta` against the parent with
bootstrap 95% CIs — was likewise unreported and is now in section 3's table. Only Q4_K_M
excludes zero, and the direction is a small *improvement* over the parent, not a decline.