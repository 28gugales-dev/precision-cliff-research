# Served Precision Is Part of the Model: A Quantization Cliff in Proposal Variation, and the Limits of Reproducibility in Agent-Runtime LLM Studies

**Soham Shailesh Gugale**


## Abstract

Quantizing a proposer's weights can leave every metric a discovery loop watches unchanged
while collapsing the variation the loop depends on. On a constructive geometry task at 14B,
degrading served quantization moves viability and validity by no detectable amount —
non-rejection at n = 50 per rung, not demonstrated equivalence, and at 7B viability instead
*inverts* — while at the 2-bit rung the proposer very largely stops departing from its
parent. The registered bound is the load-bearing figure and leads here for that reason:
`q2_k >= 60%`, `q4_k_m <= 35%`, released in the runner's header block rather than described,
fixed before the run that tested it, and **held on five never-sampled seeds** —
coordinate-verified parent-echo among valid outputs at **79% (19/24)** at Q2_K against
6% (1/17) at Q4_K_M. The wider-looking contrast, 94% (17/18) against 14% (8/57) across the
upper three rungs, comes from the smaller coordinate-replayed cohort and is reported second
because it is a re-execution rather than the registered wave. On that wave it was a secondary
endpoint: the designated primary was an improvement-count prediction and it was refuted,
which §3 reports where it reports the replication. A registered must-differ probe
returned its registered branch, 5 of 5 valid outputs echoing under an explicit instruction
not to copy. The failed proposals are not garbage — they are coherent, well-formed
near-copies, which is why every pass/fail instrument reports health. Those two registered
outcomes are what the claim rests on; everything that follows in this abstract is
descriptive or post-hoc and §3 labels it so at each use. At the loop level the consequence
is a post-hoc measure: the 2-bit rung takes 1 accepted hill-climb step in 50 calls against
14-16 at the upper three, four of its five lineages never advancing at all — while final
best score after ten generations does not separate the rungs anywhere (six lineage-level
permutation tests across both scales, *p* = 0.12-0.94).
The outcome number a practitioner reports is blind
to an order-of-magnitude collapse in search activity. That measure is mostly the echo
result in complement, the registered form of it failed on the fresh wave, and it does not
replicate at 7B; §3.6 states all three. One post-hoc *exclusion* earns a place here, and its thinness is quantified below: pooled
over both fixed-parent waves, departures improve at 80% (8/10) at Q2_K against 81% (60/74) at
Q4_K_M. It has data at four of the probe's six parents and exceeds Q4_K_M at three of them
(2/2, 2/2, 3/4 against 91%, 89%, 67%) and falls below at the fourth, a 1/2 cell. That rules out a *collapse* in departure quality at 95% —
on ten departures, by 0.8 points against the least favourable comparator, and reversing if
one row flips. What that leaves standing, and does not confirm, is that the 2-bit rung loses
the occasion to depart rather than the quality of its departures. Instruction does not recover the occasion — the must-differ probe
demanded departure and got none.

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

Five further registered waves then attack the result's generality, and each verdict below
is the label its own locked rule printed. A capability-tier control runs three hosted
tiers through the identical lineage protocol and returns **DISSOCIATION**: 0/120
coordinate echoes against a registered ≤30% bound — stuck tiers emit zero-scoring
templates (97.5% at the strongest tier), stuck 2-bit rungs copy, so weakness alone does
not produce the failure mode. A harder-geometry transfer (Heilbronn triangles) holds the
2-bit echo bound (63.1% vs a registered ≥55%) but *refutes* the reference rung's ceiling
(46.9% vs ≤30%): the rung contrast survives off circle packing (*p* = 3.5e-3,
descriptive); the absolute bands do not, because echo is driven jointly by precision and
by whether the search has anywhere to go. A discrete-task wave (LABS) and two
model-family registrations (four non-Qwen models from 8B to 24B, the second a
competence-matched retry of the first) return UNINFORMATIVE and UNDERPOWERED by their
own floors — the tasks and models sat below the competence needed to test the question —
and are reported as such rather than shelved. The family-generality limitation is
therefore **unresolved**: every non-Qwen family we tested, at up to 24B, sat below the
task's format-competence floor, and the cliff's family scope is stated as an open
limitation rather than estimated.

This matters because studies using a language model as a proposal operator increasingly run
through managed agent runtimes that address models by *alias*. Which quantization is served
is one of several things an alias leaves unattested — and it is now a variable the dependent
measure is known to be sensitive to. Our ladder holds the inference stack fixed and varies
only the SHA-256-pinned weight file, so it measures served-weight precision, not a
decode-path effect; whether other serving-stack variables behave alike is a hypothesis we
raise, not a result we establish.

We then report a forensic case study of a top-tier arm addressed only as `opus_alias`, whose
serving signature (2.8-9 s completions across all thirty against 75-250 s and 150-1170 s
for the other tiers on the same harness) and behavioral signature (validity 4/30 against 30/30 and 50/60,
recomputable in full) together *mildly favour* an unattested serving path without deciding
it. The latency figures are working-log ranges the released artifact cannot check — itself
an instance of what we argue for. Serving-path degradation and a genuine property of
whichever weights the alias resolved to are not separable by any experiment that can
*attest* the serving path, because no observable the runtime exposes reports which decode
path served a call. That unattestability, not a blanket impossibility of behavioral
discrimination, is what the case study establishes. We then run the two experiments the
case study names, under a decision rule locked before sampling. Re-issuing the
byte-identical prompts to the same alias six days later returns **10/10, 10/10 and 10/10
valid against the original 3/10, 1/10 and 0/10**, against a registered bound of ≤ 12/30 —
disconfirmed at the widest margin the design allows, with nothing in the runtime's response
surface reporting that anything had changed. The consequence is not that one hypothesis
wins. Both concern the call we sampled in 2026-08; they remain well posed about it and
become **untestable**, because the only handle the runtime offers no longer addresses the
thing they are about, and a later call through the same alias is a sample of an unknown
condition rather than a second sample of the same one. The repair probe, run alongside,
returns 59/60 exact and flat in perturbation size across two orders of magnitude — a result
the locked rule forbids us to read as evidence, for that same reason. We close on what is and is not repairable from inside an agent harness —
including where this paper fails its own standard — and endorse an existing reporting
checklist, and on a proposal of our own that we tested against our own rows and
withdrew — its firing condition fires on a fixed serving path, and its obvious repair fails
across waves, across warm-up and across hardware. What replaces it is one narrower check
and a negative result about the whole instrument class.

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
the numbers they disqualify. Five later registered waves bound the claim's generality
(§6, §8): a hosted capability ladder does not reproduce the failure mode (0/120, verdict
DISSOCIATION), the rung *contrast* transfers to a second geometry while the absolute
bands do not, and the transfers that could not be evaluated — two tasks and four model
families that sat below the required competence — are reported under their own registered
floor labels.

**C2 — a forensic case study.** A thirty-invocation arm addressed only by alias, in which
serving-signature and behavioral evidence together *mildly favour* an unattested serving
path without deciding it — and in which the favouring evidence, the latency gap, is a
working-log observation the released artifact cannot check. §4.1 adds that the favouring
is unrecoverable: the alias drifted within six days, so no later call can re-test it.

**C3 — a non-identifiability argument, conditioned on the runtime we observed.** For the
agent runtime studied here, the observable set exposed per invocation does not contain
any variable that attests the serving path. We state the observable set explicitly, show
which hypothesis pairs it separates and which it does not, and name the experiments that
would discriminate the two readings behaviorally — two runnable inside the runtime, one
requiring a pinned endpoint outside it. We ran both of the runnable two (§4.1), under a
rule locked beforehand, and report a result that constrains the argument rather than
confirming it: the alias's behaviour and serving signature both moved within six days,
unannounced, so the hypothesis pair the discriminator was built to separate turns out to
presuppose a stable referent it does not have.
The claim is conditioned on one vendor and one runtime (§8); a runtime that exposes a
serving-path flag or a weights digest would falsify it for that runtime.

**C4 — a repair protocol, including its own failures.** The maximal reproducibility such
a study *can* achieve — prompt hashing before sampling, verbatim raw storage, dated alias
maps, deterministic local scoring, hash-locked preregistration — specified, implemented,
and audited against itself: three of the five repairs are fully implemented in the
released artifact, and we name the two that are not. The audit extends to the one
*instrument* we proposed rather than restated: run against §3's own rows, on a stack where
the serving path is fixed by construction, its firing condition fires anyway, and its
obvious repair fails across waves, across warm-up and across hardware. We withdraw it and
report the three mechanisms that broke it, which is the transferable part.

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

**What carries this section, stated once and up front.** This section reports a great many
numbers and labels most of them descriptive. That is deliberate and it is easy to misread as
a section with no claim in it, so here is the spine. **Two registered predictions held, and
they are what the claim rests on.** The first is the fresh-seed echo bound — `q2_k >= 60%`,
`q4_k_m <= 35%`, written into `kaggle_precision_sweep_14b_fresh.py`'s header and pushed
before that run executed, then observed at **79% (19/24) against 6% (1/17)** on five seeds
never sampled in any prior run. The second is the must-differ decision rule, which specified
both branches in advance and returned the copying-is-instruction-insensitive one at **5 of 5**
valid outputs echoing under an explicit prohibition. Around those sit two descriptive
replications that point the same way and are labelled descriptive wherever they appear: an
independently produced imatrix Q2_K echoing at 75% against IQ2_M's 43%, and a fixed-parent
control preserving the direction and the 2-bit endpoint at 92% against 33% in the matched
band.

**And here is what failed, in the same place, so the two are read together.** The fresh
wave's *designated primary* — F1, an improvement-count prediction — was refuted. The
dispersion probe's wave-1 decision rule returns **no category** and wave 2's returns
**FAILED**, its ceiling rung never having run for want of a second GPU. The registered
scheme-versus-bit-width control returns its **inconclusive** branch. The 7B ladder refutes
the project's founding hypothesis outright and §3 says so. Every other figure in this
section falls into two further classes and neither is a confirmation. **One post-hoc
exclusion is claimed**, and claimed narrowly: the conditional-quality analysis of §3.6 rules
out a *collapse* in departure quality at 95%, on ten departures, against a threshold we wrote
ourselves and by 0.8 points against the least favourable comparator. It appears in the
abstract and in §8 with those qualifications attached and should never appear without them.
**Everything else — the search-progress statistic, the decomposition, the horizon model, all
twenty-nine *p*-values — is descriptive or post-hoc and carries no claim at all.** A reader
who wants to know what this paper would have to be wrong about should look at the two
predictions in the paragraph above; a reader looking for where it is thinnest should look at
the exclusion.

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
7B paragraph are replayed by a second script, `sec3_7b_repro.py`, which loads the 7B run
(`sec3_artifacts/precision_sweep/`) and recomputes the viability vector, its Wilson
intervals, all three 7B contrasts, the count distribution behind the format-lottery
argument, the truncation check, the probe count and the best score. **No figure in §3 now
requires a reader to compute a tail themselves.** Two things that script prints deserve
naming here rather than in its output alone. The *p* = 0.001 figure is a **pooled** contrast
— fifteen upper-rung lineages against Q2_K's five, not a rung-versus-rung comparison; the
paired Q4_K_M-versus-Q2_K form of it is *p* = 0.048, and the script prints both so the
pooling is visible rather than implied. And the 7B count *ranges* do not support the
"broader distribution" reading as cleanly as the modes do: Q4_K_M and Q3_K_M each carry a
single 45-circle outlier, so what is broader at Q2_K is where the mass sits, not the
extreme.

**Inferential status of every *p*-value in this section.** Twenty-nine are reported in four
families that must not be pooled: nine Fisher exact tests on counts, six permutation tests
belonging to the dispersion probes' preregistrations, two Spearman orthogonality
diagnostics, and twelve post-hoc lineage-level permutation tests on §3.6's search-progress
statistic. **No claim in this paper rests on any of the twenty-nine.** The claims rest on
the registered predictions and their pass/fail outcomes; the tails are reported as
descriptive effect sizes. The candidate-level Fisher tests treat rows as independent when
they are nested within lineages, and so overstate their evidence; the six registered
permutation tests belong to decision rules that both returned unusable verdicts; the twelve
post-hoc tails are unstratified against a seed-crossed design and two of them sit on the
arithmetic floor of their enumeration. **Appendix A.4 gives every value, its family, the
multiplicity threshold that applies, and the specific defect each family carries.**

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
that works because the pinned side of the stack *is* pinnable. The determinism premise
itself was then exercised externally rather than asserted: a public Kaggle kernel
(`sohamgugalet/precision-redetermin`) re-ran 112 of the 224 generations — the Q4_K_M and
Q2_K rungs that bracket the cliff — from the released seeds on the original hardware
class, and **all 112 reproduced their archived per-row digests exactly** (verdict
SUPPORTED, printed by the kernel). Two caveats travel with it, both recorded in the
output: the original llama-cpp-python build is unrecoverable so the wheel is
version-pinned (0.3.34) rather than build-verified, and two earlier executions of the
same kernel drew a P100 and correctly returned VOID_ARCH for every row instead of
comparing across architectures — cross-hardware nondeterminism is the finding of Yuan et
al. (§7), not a defect to explain away.

**Fresh seeds replicate the echo cliff, and a registered prediction fails** (combined
§5.9). The same protocol was then run on five never-before-sampled seeds (2222, 3333,
5555, 7777, 9999) at the two decisive rungs, 100 new coordinate-logged candidates, with
every registered prediction falsifiable because the draws are genuinely new. Echo
replicates: **19/24 (79%) at Q2_K against 1/17 (6%) at Q4_K_M** (Fisher *p* = 3.4e-6,
candidate-level and descriptive), every fresh Q2_K seed again majority-echo (4/5, 4/5,
5/6, 2/2, 4/6), both registered echo bounds held. **The wave's designated primary was not
the echo bound but the improvement count, and it failed**: the runner header labels F1
"Improvement (seed-level, primary)" and gives the echo bound F2 no such label, so what
replicated here is a registered secondary on a wave whose primary was refuted. That
prediction forecast ≤ 2/5 Q2_K seeds improving past the seeded baseline, and
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
copied" is *identically* the legacy echo count, in all six cells — a row copying both fields
is an echo by definition — so the decomposition adds no evidence there. All it adds is a
partition of the *non-echo* rows into "varied the radii" and "varied the centres", which at
Q2_K on wave 1 is three rows split 2 and 1.

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

**Under the registered replacement rule this returns no category.** SURVIVES, PARTIAL and
FALSIFIED each require a combination the outcomes do not supply, and UNDERPOWERED does not
apply; the honest label is unclassified. That disqualifies the *registered mechanism
verdict* specifically and we make no use of it. It does not disqualify the probe's counts,
which are reported here as descriptive throughout. Two things cut against reading the
favourable half alone and both are set out in **Appendix A.3**: the NED decline is not
monotone — Q3_K_M sits above Q4_K_M and the whole effect is Q2_K collapsing — and the
rarefaction instrument is ceiling-saturated, 159 of 165 valid rows sitting at exactly zero
displacement, so its *p* = 0.953 is saturation rather than evidence of flatness. The
registered orthogonality criterion passes and A.3 states the residual association it leaves.

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

**The fresh wave's designated primary was a prediction about this quantity, and it failed.**
This needs stating in the runner's own words, because the paper has been strict about primary
designation elsewhere and the strictness costs something here. The fresh-seed runner's header
labels F1 "**Improvement (seed-level, primary)**": ≤ 2/5 Q2_K seeds and ≥ 4/5 Q4_K_M seeds
improving past the seeded baseline. **F1 failed** — 3/5 Q2_K seeds improved, Fisher
*p* = 0.44 against 5/5. The echo bound F2, which held and which §3 and the abstract lean on,
carries **no primary label in the registration**; on that wave it was one of three
registered endpoints and not the designated one. So the honest summary of the fresh wave is:
*its registered primary was refuted and a registered secondary held*, and every use we make
of the fresh replication is a use of the secondary. We say so here rather than reporting the
surviving endpoint alone, which is the failure mode this paper's §3 spends its length
guarding against. The statistic in this subsection is computed from the same rows: F1 asks
*whether* a lineage improved at all, this asks *how many times* it did. On the fresh wave
the coarse registered form gives 3/5 versus 5/5 and does not separate the rungs; the finer
post-hoc form gives 3 steps versus 14 and does, at *p* = 0.0079. That gap is an instance of
analytic flexibility and we treat it as one, not as a repair of F1, and a
reader is entitled to weigh the two accordingly: the registration made the coarse choice,
the coarse choice failed, and the finer choice that succeeds was made by us with the
ledgers open. We report the count statistic because it is the quantity a loop's cost is
denominated in and because withholding it would be its own distortion — but it does not
inherit F1's registration, it does not repair F1's failure, and no claim in this paper
rests on it. The most this paper claims for the fresh wave is what the secondary establishes:
the echo bound held on never-sampled seeds, and its designated primary did not.

**The part not implied by the echo result: quantization gates the frequency of departure,
and the collapse of departure *quality* is excluded.** The consequential question the echo
result leaves open is whether a degraded proposer's rare departures are also *worse* ones. A
frequency-only effect is in principle repairable by forcing departure; a quality effect is
not. The loop ladders cannot settle it — their 2-bit departure counts are 1, 5 and 8, and
reading the 1/1 cell as "flat" would be an inference off a single observation. The
fixed-parent probe can do better and is the cleaner instrument besides: the parent is held
constant so "improved" is a comparison against a fixed target rather than a drifting best,
`score_delta` is logged per row, the two waves share a design so pooling within the family is
legitimate where pooling a ladder with a probe would not be, and six parents spanning 0.88 to
1.65 permit the per-parent breakdown this question needs. Pooled across both waves
(`sec3_conditional_quality.py`, post-hoc, in neither registration):

| rung | valid | departures | improved | 95% CI |
|---|---|---|---|---|
| Q4_K_M | 164 | 74 | 60/74 (81%) | [70%, 89%] |
| Q3_K_M | 142 | 70 | 61/70 (87%) | [77%, 94%] |
| Q2_K | 133 | 10 | **8/10 (80%)** | [44%, 97%] |

Fisher on 8/10 against 60/74 returns *p* = 1.00. Per parent, the 2-bit rung matches
everywhere it has data — 2/2 at 0.880, 1/2 at 0.900, 2/2 at 1.040, 3/4 at the hardest parent
1.650 against 6/9 and 4/6 there — and its departures are **not** drawn from easier parents:
4 of its 10 sit at that hardest parent, 40% of its sample against 12% of Q4_K_M's.

Scored against a decision rule we wrote for this quantity in an unlocked design note
(`wave3_prereg_heilbronn.md`), the verdict is **not a confirmation**, and three things about
that rule have to be said before its output is quoted. **It is ours and it is not a
registration.** We wrote it on the same day this analysis became computable, from data
already in the repository; the note says of itself that nothing in this paper may cite it as
a registration, and we do not. It is a threshold we specify, fixed in advance of *reporting*
rather than in advance of *seeing*, which is a materially weaker thing. **Its power floor is
not met**: twenty-five 2-bit departures required, ten observed, so no branch is confirmed.
**And the exclusion it does yield is one observation wide.** The collapse branch requires the
Q2_K rate to fall at or below half the reference rate, and which reference is chosen moves
the line: half of Q4_K_M's 81% is 40.5%, half of the pooled upper rungs' 84% is 42.0%, and
half of Q3_K_M's 87% — the *better*-performing comparator, sitting in the same table — is
43.6%. The 95% Clopper-Pearson lower bound on 8/10 is **44.4%**. The branch is excluded
against all three, but by 3.8, 2.4 and **0.8** points respectively; and had one of those ten
departures failed to improve, 7/10 gives a lower bound of 34.8% and the exclusion fails
against every comparator. We state the margin against the least favourable reference and the
sensitivity to a single row, because an exclusion this thin reported against only its
friendliest comparator would be the selective reporting §6 exists to indict.

What that supports is narrow: on this evidence a *collapse* in departure quality is not the
explanation of the echo cliff. The reading it leaves standing — that what the 2-bit rung
loses is the occasion to depart, 10 departures in 133 valid outputs against 74 in 164 — is
**unconfirmed**, not established, and confirming it needs departures this design lacks.
(The wave designed to supply them has since been locked and run; its control-arm floor
fired — no rung improved on the seed at all — so its conditional-quality primary returned
UNINFORMATIVE and the question stays open. §8 reports that wave in full.)

That points at a repair and immediately complicates it. If frequency is the gated quantity,
forcing departure should recover the search — but the registered must-differ probe did
exactly that, instructing the proposer that its output must not be identical to the parent
and that at least three circles must change, and returned 5 of 5 echoes anyway. Whatever
gates departure at 2 bits is not reachable by instruction, which makes the intervention worth
testing an architectural one — decoding constraints, sampling temperature, explicit
diversity penalties — rather than a prompt.

**Replication is partial, and the level of the test decides it.** The test is an exact
enumeration of every split of the pooled lineages, two-sided, on the difference of mean step
counts. It shares nothing but the word *permutation* with the dispersion probes' registered
tests, which use a one-sided Jonckheere-Terpstra trend statistic evaluated by Monte Carlo —
we name the difference because a post-hoc statistic should not borrow a registered one's
standing by resemblance. On this test the registered ladder gives *p* = 0.0008 against
the pooled upper three (15 504 splits) and *p* = 0.0079 against Q4_K_M alone (252 splits).
The five never-sampled fresh seeds replicate: 3 steps against 14, *p* = 0.0079 — which is
the floor of a five-versus-five enumeration, as the next paragraph sets out. **The IQ2
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
of the collapse is smaller than this section's framing implies. We did not run it. We did
price it, and the pricing is worth one paragraph because it changes how the null above
should be read.

`sec3_horizon_power.py` resamples the observed process: departure rate and empirical offer
distribution estimated per rung from the pooled 14B ledgers, a lineage of *T* calls drawing
Binom(*T*, *d*) offers, best-so-far the maximum of those and the seed. **We ran it, and we
report what it cannot support before what it can.**

It cannot support a power statement about our own design, and an earlier draft of this
section wrongly claimed one. A power figure is power *against a specific alternative*, and
the only alternative this model supplies is its own projection — which puts Q2_K **ahead** at
every horizon, widening with budget. That inversion comes from the estimation: the 2-bit
rung's six observed departure-offers are 0.867, 0.900, 1.040, 1.300, 1.625, 1.625, so the
maximum appears twice and one entry is the seed score itself, handing the resampler a
one-in-three jackpot and a hard ceiling. Six observations cannot carry a direction; they
therefore cannot carry the effect size a power number is defined against either. We withdraw
the figure rather than keep a number whose alternative we disown two sentences later. **The
outcome-level null of the previous paragraph stands as non-rejection at five lineages per
cell, with no quantitative statement about how underpowered that is.**

It cannot support "widen rather than lengthen" either, which the same draft asserted and the
script's own table refutes. Cost-equalised, lengthening wins: five lineages at 100
generations is 500 calls for 84%, twelve at 50 is 600 calls for 82%. And at the horizon this
section actually reports, *T* = 10, the simulated rejection rate *falls* as lineages are
added — 17%, 8%, 5%, 4% for 5, 8, 12 and 20 — which is not how power behaves and is a sign
the coarse permutation tail at five-versus-five is doing the work rather than any effect.
That row should be read as a warning about the instrument, not as a measurement.

What survives is structural and does not depend on the model's estimates. **Final best score
is a maximum**, so it is insensitive to the draw count by construction: multiplying effective
draws moves it by the distance between two upper quantiles of the same offer distribution,
not by anything proportional to the draw ratio. A wave that wants to demonstrate harm should
therefore not use final best score as its dependent variable at all — it should measure
time-to-threshold, area under the best-so-far curve, or the accepted-step count itself, which
is what this subsection measures and what the wave-3 design note names as its primary. That
is the paper's answer to "just run longer", and it is why the horizon run remains named as an
open gap rather than closed by arithmetic.

**At 7B the statistic does not replicate, and reverses.** The 7B ladder stores no
coordinates, so echo is not computable there — but accepted improvements are, which gives
this measure a second scale at no cost. Across five rungs the step counts are FP16 6/50,
Q8_0 2/50, Q4_K_M 3/50, Q3_K_M 4/50, **Q2_K 7/50** — the 2-bit rung takes the *most* steps
of the five, and the permutation tail against the pooled others is *p* = 0.116, against
Q4_K_M *p* = 0.238. Final best score does not separate the rungs at this scale either — *p* = 0.158 against the pooled others and 0.119 against Q4_K_M — which completes the six outcome-level tails the abstract's 0.12-0.94 range covers. Neither direction is established. Validity at 7B runs 4–12 of 50 at
*every* rung, so no rung at this scale is searching enough for the statistic to have room
to separate, and the reversal sits with the viability inversion §3 already reports at 7B
rather than contradicting anything. What it does establish is the scope: **the search-step
collapse is a 14B observation and is not a property of the quantization ladder as such.**

**What varied, and what did not.** This distinction is load-bearing for the rest of the
paper, so it comes before the transfer. Across every run in this section the
inference stack was *constant within each run*: the same llama.cpp build, the same
sampling parameters, the same harness, and one fixed hardware allocation — **2 × T4 for
all four ladders, a single Tesla P100 for both dispersion-probe waves**, per the `gpus`
field of each `provenance.json`. That difference is why the probe could not attempt Q8_0.
Ladder timings and probe timings are therefore never compared to each other anywhere in
this paper. The only thing that changed *inside* a run was which SHA-256-pinned weight
file was loaded. What is measured here is therefore the effect of
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
says so. §4.1's arms capture both fields per row, which closes the gap prospectively and
not for these thirty rows — the distinction §6 item 4 is about.

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

*Speed is not precision, and §3's own ladders show it.* The inference from "unusually
fast" to "cheaper or lower-precision serving path" passes through a step worth stating,
because on the one stack we fully control it does not hold. Across §3's ladders,
throughput does not order by bit-width: on the 14B ladder Q8_0 is the **slowest** of
four rungs at 14.9 tok/s against Q2_K's 22.5; on the 7B ladder FP16 is slower than every
quantized rung, and Q3_K_M sits below Q4_K_M at both scales (§6, `sec6_cv_canary_audit.py`
— reported there in the course of withdrawing item 4's firing condition, and independent of
that withdrawal). Those are tens of percent and this arm's gap is one to two
orders, so the magnitudes are not comparable and this does not overturn the reading. But
it does mean speed and precision are separate axes even on a fixed stack, and an
inference that treats them as one axis is doing work the data here do not license. What
the ladders *do* support is weaker still. Throughput separates the served files within a
single wave on fixed hardware once warm-up and degenerate outputs are excluded — but not
across waves, and **not across hardware, where the ordering between two SHA-pinned files
reverses** (§6 item 4). It is not a portable fingerprint and cannot attest a serving path
to anyone who does not control the machine, which is the whole of the case C3 is about.

**Behavioral signature — recomputable, and reported at both tolerances.** Validity was
**4/30 (13%)** at the primary 1e-6 tolerance and **4/30 at the strict 1e-9 tolerance**:
the collapse is tolerance-invariant, per cell 3/10, 1/10, 0/10. The comparators on the
same three cells, recomputed from the released file with the released scorer: the Sonnet
arm **30/30 at 1e-6 and 27/30 at 1e-9** (three rows fail on overlap at the strict
tolerance and pass at the primary), and the Haiku (`bare`) slice **50/60 at 1e-6 and
47/60 at 1e-9**. §2 declares 1e-6 primary in advance, so both figures are printed rather
than one chosen.

*A fourth comparator, present in the released file and not previously reported here.*
`arm_f_raw.json` also carries 70 rows labelled `trace` at exactly these three cells — 20,
30 and 20 at N = 13, 21 and 31. They belong to the companion paper's trace-elicitation arm
and paper 2 had not mentioned them, which is a gap in a paper that ships the file. Scored
by §4's own released checker they return **63/70 valid (90%)**, per cell 18/20, 28/30,
17/20. Against `opus_alias`'s 4/30 that is Fisher *p* = 1.1e-13; pooling all three
comparators, 143/160 against 4/30 gives *p* = 1.0e-16. The comparators do not differ
detectably from each other (`trace` vs `bare` *p* = 0.30, vs Sonnet *p* = 0.099), so the
arm that stands apart is the alias-addressed one and only that one.

This matters beyond an extra count, because `trace` varies the thing a sceptic would
reach for first. Its prompt is substantially different from the bare prompt — the
companion paper describes it as a bundled prompt-format-and-trace-request — while the
serving path is the same one the other local arms used. A large prompt change therefore
produces nothing resembling `opus_alias`'s collapse, which is a control §4 otherwise
lacks: the collapse does not follow from prompt variation as such.

*Two caveats on this arm, both of which cut against leaning on it.* First, it is a reuse:
these rows were collected for the companion paper's question, not this one, and its own
scope caveats travel with them. Second, and more serious, `arm_f_raw.json` does **not**
distinguish the companion paper's pilot rows from its `trace_v2` rows, and that paper
states explicitly that the two must never be pooled. The 63/70 above therefore pools rows
the companion paper forbids pooling, because the released file provides no field on which
to separate them. We report the figure with that defect named rather than omit an arm the
artifact contains, and no claim in §4 rests on it — the 4/30 against 30/30 and 50/60
contrast stands without it. The inability to reconstruct that split is the same class of
defect as the overwritten Haiku slice below, and it belongs in §6 item 3's evidence. *Disclosure on the comparator.* A 45-row Haiku slice from a prior sampling
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
favour H1 *within this snapshot*. What they cannot do is *decide*, and §4.1 leaves the
comparison worse off than undecided rather than better, because that auxiliary is not itself testable
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
Earlier drafts of this section named both and ran neither. Both have now been run, and
§4.1 reports what happened — including that the first of them destroyed the second's
interpretability, in a way the design anticipated and wrote down in advance.

*Prompt variation.* The earlier dismissal — that prompt variation cannot help because
both hypotheses act on execution rather than intent — ruled out an entire experiment class
in one clause, and it is wrong for at least one design. Hand the alias a *fixed,
known-valid* packing and ask it to verify or repair the tangencies. The model did not
choose that construction, so arithmetic execution is decoupled from constructive ambition:
failure to verify tangencies it did not select is execution degradation independent of
ambition, which is exactly an H1/H2 discriminator.

*A dated re-snapshot.* Re-sampling the same alias at a later date is informative either
way, and is runnable from inside the runtime — so the earlier flat claim that no
within-runtime experiment could bear on the question contradicted our own follow-up
section. It is narrowed accordingly: a re-snapshot can detect a *change* in the serving
signature without ever attesting the serving path in either snapshot.

The arm is logged in full, excluded from the tier ladder, and carries the alias caveat in
every mention.

### 4.1 Both follow-ups, run — and what the anchor arm did to this section

The two designs above were preregistered together in `arm_r_preregistration.md`, committed
before the first invocation, and run on 2026-08-07 through the same agent runtime and the
same alias. Ninety invocations: thirty re-issuing the byte-identical bare prompts at
*N* = 13, 21, 31 (**arm B2**), and sixty on the repair task (**arm R**), split across two
cells, a three-step precision ladder, and two tiers. Every figure below replays from
`arm_r_analysis.py` over the released ledgers in `arm_r_artifacts/`.

The registration is explicit about why the repair probe could not ship alone. The alias
resolves to whatever it resolves to on the day, the runtime reports nothing about which
weights served either call, and that is C3 applied to our own follow-up. A repair score
without an anchor is uninterpretable: a clean result would be equally consistent with
"repair is easy for the path that served 4/30" and with "the alias resolves to something
else this week." Arm B2 is the anchor. Which of those two it would turn out to be was
registered as P-R0, at **≤ 12/30 valid**, with the disconfirming branch written out in
advance.

**Arm B2 disconfirmed P-R0 at the widest margin the design allows.**

| cell | 2026-08-01 | 2026-08-07 | best valid score, 2026-08-07 |
|---|---|---|---|
| *N* = 13 | 3/10 | **10/10** | 1.776141 |
| *N* = 21 | 1/10 | **10/10** | 2.276800 |
| *N* = 31 | 0/10 | **10/10** | 2.794180 |
| pooled | 4/30 | **30/30** | Fisher *p* = 7.8e-13 |

The *p*-value states what it states and no more. It rejects the hypothesis that these two
sets of rows are draws from one success rate. It is **not** a test that the serving path
changed: there is one serving path per condition, so this is pseudoreplication with
respect to that question, and the 2026-08-01 arm entered the paper for being extreme. It
is also unregistered — the registration fixed the ≤ 12/30 band, not a test. The per-cell
counts above carry the result; a reader who prefers to ignore the pooled tail loses
nothing.

**Two further channels were logged, and only one of them survives scrutiny.** Wall clock
went from the 2.8-9 s window this section's serving-signature argument rests on to
**68.7-594.1 s**, median 228.2, overlapping the 75-1170 s comparator range it was once one
to two orders below. That comparison is *uncalibrated in both directions* and we decline to
lean on it: the 2026-08-01 figures are eyeballed session-log ranges, the 2026-08-07 ones
are a runtime-reported `duration_ms` field, no row exists on which the two instruments can
be compared, no contemporaneous comparator tier was sampled on 2026-08-07, and the
registration explicitly registered **no timing claim**. It is consistent with the validity
change and it is not evidence for it.

The usage channel does not survive at all, and the way it fails is worth reporting because
we walked into it. Reported usage went from uniform ~49.9k on 2026-08-01 to 58k-195k on
2026-08-07, a 3.35-fold spread, which reads as a second signature — until arm R supplies
the control. Arm R's alias rows ran **the same day through the same alias** on a different
task, and their usage is uniform to **1.01-fold (54,377-54,803)**. The spread tracks the
task, not the date. Within B2 itself usage and duration correlate at *r* = +0.69, so this
was never a second channel in the first place. §4 withdrew the ~49.9k observation on
exactly this reasoning — an aggregate counter over a large fixed prefix is not a serving
signature — and a draft of this subsection reproduced the withdrawn error inside the
paragraph that quotes the withdrawal. **The usage observation is withdrawn again, here,
and the single-day control that kills it is in the released ledger.**

*What the surviving result does not do.* It does not retract a single 2026-08-01
observation. Those thirty rows are in the released artifact and score what they score.

*What it does is take the section's question away rather than answer it.* The
registration's fourth branch says the words: *the paper's §4 hypothesis pair remains
unseparated, and we say so.* Precisely: H1 and H2 are hypotheses about the 2026-08-01
call, and they remain perfectly well-formed about it. What is gone is any route to testing
them, because the only handle the runtime offers — the alias — no longer addresses the
thing they are about, and no observable reports when that changed. A later call through
the same alias is not a second sample of the same condition; it is a sample of an unknown
one.

It is tempting to read the change as a natural experiment settling the matter. Fast-and-13%
then slow-and-100% is what H1 predicts, if the weights are fixed and only the decode path
moved. It is equally what H2 predicts if the weights themselves changed, because then it is
a genuine tier property of model A against model B. Two conditions, no randomization, and a
difference simultaneously in date, load, decode path and possibly identity distinguish
none of these. The comparison establishes that the referent is unstable. It does not
establish which hypothesis about a referent is right, and reading it as though it did would
be the same error as reading arm R below.

**Arm R ran anyway, because it was registered.** Six cells — *N* ∈ {13, 31} × δ ∈ {1e-2,
1e-3, 1e-4} — five invocations each at the alias tier and five at Sonnet. A grid-plus-
interstitial packing, exactly tangent everywhere so the injected displacement is the only
violation, with one circle slid by δ and the overlapping-pair set as an exact key.

| | δ = 1e-2 | δ = 1e-3 | δ = 1e-4 |
|---|---|---|---|
| *N* = 13, alias / Sonnet | 5/5, 5/5 | 5/5, 5/5 | 5/5, 5/5 |
| *N* = 31, alias / Sonnet | 5/5, 5/5 | **4/5**, 5/5 | 5/5, 5/5 |

**59/60 exact.** Recall over key pairs is 1.00 in every cell of every tier; the single
miss is a false positive naming a pair whose true clearance is 7.089e-04 — a near-miss,
not a wild answer. Detection is flat in δ across two orders of magnitude at both tiers,
and no invocation anywhere returned the empty list.

Of seven registered predictions, three held and four failed. P-R1 (exact ≥ 0.6 at
δ = 1e-2) held. P-R5 (Sonnet ≥ alias at δ = 1e-2) held. **P-R4 held vacuously** — it
predicted the empty response would not become rarer as δ shrank, and there were zero empty
responses anywhere, so it is reported as vacuous rather than counted as support. P-R2 was
registered as *"monotone non-increasing"*, which flat detection **satisfies**; it is scored
FAILED on one cell only, *N* = 31's 1.0 / 0.8 / 1.0, where the single false-positive row
makes the sequence rise at finer δ. That is a failure by the letter of a rule we wrote and
not evidence of anything. P-R3 (≥ 2/5 drop from δ = 1e-2 to δ = 1e-4) and P-R6 (Sonnet
beating the alias at δ = 1e-4) both failed outright.

**The H1 signature the probe was built to detect was not detected, which is weaker than
absent, and the gap matters at this sample size.** Five invocations per cell put the
one-sided 95% lower bound of a 5/5 cell at 0.549, so a true detection rate anywhere above
~55% produces these tables with unremarkable probability. The design excludes a precision
effect of roughly 45 points or more and says nothing about a smaller one. P-R6 became
structurally unreachable the moment Sonnet also hit ceiling: a comparator at 1.00 cannot be
beaten by 2/5. The registration called this arm a discriminator and not an estimator, and
its floor of five is why.

**And we may not read it.** P-R0's failure triggers the registration's fourth branch,
which was written for exactly this: arm R measures a serving path that cannot be tied to
the 2026-08-01 one, no H1/H2 conclusion is drawn from it, and the re-snapshot becomes the
finding. The branch binds even though — especially because — arm R's own result is clean
and would otherwise be readable as evidence against H1. Reporting the number and refusing
the inference is not scrupulosity; it is the content of C3 applied to a result we would
have liked.

Two things arm R does establish, on the path it actually measured and within the scope its
own registration fixes — one substrate family, two *N*, one displacement direction. First,
**repair-style probes are not where this path fails on this substrate**: at δ = 1e-4 at
*N* = 31, a violation four orders below the coordinate scale, printed at twelve decimal
places among thirty other circles, is found by 5/5 alias invocations and 5/5 Sonnet
invocations, scored separately because pooling the tiers would contradict this
subsection's own argument about referent stability. That is a reason for anyone designing a
verifier around hand-it-back-and-ask-for-the-arithmetic to test it on their own substrate
before relying on it, not a general result about verifiers. Second, there is **no tier
contrast left to measure** — both tiers are at ceiling on this task, so the comparator that
made the bare-task collapse legible has no discriminating power here.

*A note on the original registration's scorecard.* P-O2 registered zero rival-argmax
outputs and P-O4 required a best valid score of 2.2588835; both failed on 2026-08-01. On
2026-08-07 the same prompts produce a rival-argmax output at *N* = 21 (2.2768, above the
recipe value) and a best valid score of 2.794180 at *N* = 31. Those predictions are not
thereby rehabilitated. They were registered about a path that is no longer addressable,
and quoting a later path's numbers against them would be the precise error this subsection
exists to name.

*One disclosure item closes, and only prospectively.* §4 records that the 2026-08-01 arm
captured no per-invocation duration or usage into the released artifact, which is the one
item of §6's standard this paper did not itself implement. Arms B2 and R capture both, per
row, in the released ledgers. That closes the gap going forward and does nothing for the
rows where it mattered — which is what a schema defect costs, and why §6 item 4 asks for
the field to exist before it is needed rather than after.

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
| Serving-signature stats | Partial — absent from §4's arm, implemented in §4.1's | — | §6 item 4's firing condition was **tested against §3's own rows and withdrawn**; its disclosure half is retained and is already mandated by GUIDE-LLM. What §6 proposes on its own account is item 5, and §6 states the confound item 5 inherits |
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
with five of the section's nine Fisher tails; a second script, `sec3_7b_repro.py`, replays
the other four and the whole 7B paragraph, so §3 has no figure a reader must compute
unaided. §4 was
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

**The capability alternative, tested and bounded (wave 4, registered).** The strongest
alternative reading of §3 — *echo is what any sufficiently weak proposer does, so a weak
model, not a 2-bit rung, would suffice* — was left standing by every ladder, because no
experiment varied capability with precision out of the design. Wave 4 did
(`wave4_prereg_tiers_heilbronn.md`, SHA-256 `7b3e67dc…`, published to an
externally-timestamped host before any row was sampled): three hosted capability tiers,
requested by explicit model parameter, ran the identical Heilbronn n=13 lineage protocol —
same seed parent, extracted programmatically from the wave-3 runner rather than retyped;
same echo definition; tools forbidden and `tool_uses` recorded per row (0/120). The
registered primary asked whether any tier reaches Q2_K-class echo. **Result: 0/120
coordinate-verified echoes — every tier at 0% against a registered ≤30% bound — and the
analysis script recomputes every echo and score from the stored coordinates and prints
the verdict label itself: DISSOCIATION.** Over the sampled tier range, on this task, on
this date, through this harness, capability produced no parent-copying in 120 samples —
a bound of roughly 3% at this n, not an exclusion "at any rate" — far from Q2_K's band.

The registered secondary (5.2, echo monotonicity across tiers) returned **NOT
EVALUATED**: its own 10-echo floor was unmet because no tier echoed at all, and the
analysis script prints that label rather than skipping it. The unregistered structure of
the failures says something sharper: **the tiers fail differently, not less.** No proposal in any tier improved on
the seed parent (0/120 — and wave 3's GPU ladder later went 0/495 on the same task and
parent, so the stall is substrate-independent; trajectory measures from both waves are
reported as descriptives only). The same-task, same-parent, same-stall comparison is the
sharp one: stuck GGUF rungs echo at 46.9-63.1% (§8), stuck hosted tiers at 0% — though
on LABS, a third task where nothing climbed, the same rungs' stall-echo rates *reversed*
(§8), so this contrast is Heilbronn-specific, not a law of stalls. What the
tiers emitted instead was their own material: the registered template check (5.3, no
bound) finds valid outputs scoring *exactly zero* — three-plus collinear points — at
52.5% for the weakest tier, 27.5% for the middle, and **97.5% for the strongest**, whose
39/40 zero-scoring outputs are family-similar symmetric lattices, pairwise distinct at
6 dp (zero exact self-copies; post-hoc uniqueness count, disclosed as such). So the
2-bit rung's signature failure is *copying the parent it was shown*, while the hosted
tiers' signature failure is *ignoring the parent and emitting a template* — and the task
chosen because a template scores zero on it (§3.6's transfer rationale) separates the
two failure modes on a second substrate exactly as designed. A capability ladder does
not reproduce the quantization ladder's failure mode even where it fails more often.

![Heilbronn n=13, identical seed parent, zero improvements anywhere: quantized rungs
copy (solid), hosted tiers emit zero-score templates (hatched). GGUF counts from
`wave3_analysis.py`, tier counts from `wave4_analysis.py`; drawing script
`figures/make_figures.py` computes nothing.](figures/fig_two_failure_modes.pdf) The
scope limits are the prereg's own: served precision, sampling parameters, and serving
path per tier are all unattested (C3); one date; one harness wrapper around a
byte-identical prompt body; and the dissociation bounds the capability confound over the
tiers sampled — it does not exclude it below them.

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

**Item 4 is the addition**, and the artifact that motivated §4 does not implement it. That
is an uncomfortable position: the
only element of the standard we can claim as new is the element our own artifact lacked,
which is precisely why §4's central evidence is a working-log observation rather than a
checkable file. §4.1's arms implement it — per-invocation duration and usage are in the
released ledgers — and the value of having done so is visible there: the serving-signature
change those arms document is a *checkable* claim in a way §4's original one is not.

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
   not currently do, and the one that surfaced §4. §4's own arm did not implement it;
   §4.1's arms do, and doing so immediately paid: the single-day usage control in §4.1
   caught a draft of this paper re-committing the very error the withdrawal above
   describes. We still present the firing condition as a proposal to be tested rather than
   a demonstrated instrument. Thresholds above are a starting point, not calibrated values.

   **We then ran item 4 against our own data, and it has a false-positive mode.**
   Item 4 is the one element of this standard we claim as new, so it is the one
   element that most needs auditing, and §3's ledgers make the audit possible: they
   carry per-invocation `wall_s` on every row, across weight files pinned by SHA-256
   on a *fixed* inference stack — for the probe rows below, same llama.cpp build, a
   single Tesla P100, same sampling parameters, same harness. Whatever the canary reports there, it is not reporting a
   serving-path change, because there was none. Released as
   `sec6_cv_canary_audit.py`.

   **It fires.** On the fixed-parent probe, duration CV among valid rows is 0.0603 at
   Q4_K_M and **0.0143 at Q2_K** — a ratio of 0.237, below the one-third threshold the
   item names. Wave 2 replicates on independent seeds: 0.0692 against **0.0200**, ratio
   0.289. A permutation test on the CV ratio returns *p* < 0.0001 on both. Q3_K_M does
   not fire on either wave (ratios 0.949 and 1.066), so the canary is not simply noisy
   — it is selectively wrong at exactly the rung §3 is about.

   **The mechanism is output degeneracy, not serving.** Splitting the same rows by
   whether the output echoes its parent:

   | rung | echo *n* | echo CV | non-echo *n* | non-echo CV |
   |---|---|---|---|---|
   | Q4_K_M | 34 | 0.0210 | 31 | 0.0783 |
   | Q3_K_M | 31 | 0.0141 | 20 | 0.0778 |
   | Q2_K | 46 | 0.0113 | 3 | 0.0294 |

   Duration CV is low among echo rows at **every** rung and high among non-echo rows at
   every rung. An echo re-emits its parent verbatim, lands on the same token count, and
   takes very nearly the same time. Q2_K's aggregate CV is low because 46 of its 49
   valid rows are echoes — a property of the *output*, not of the path that served it.

   **Item 4 therefore needs a control it did not carry, and we add it here:** report
   duration dispersion *conditioned on output identity*, or exclude repeated outputs
   before computing CV. Without that control a degenerate proposer looks exactly like a
   fast serving path on the one statistic the standard asks a reader to watch — and the
   two call for opposite responses. This does not overturn §4, whose serving-signature
   evidence is an absolute latency gap of one to two orders of magnitude rather than a
   dispersion ratio, and whose arm was not echoing at all: its failure mode was invalid
   geometry, 4 of 30 valid. But it is a competing explanation §4 never named for the
   *class* of evidence it relies on, and a standard that proposes a statistic without
   naming that mode is proposing a trap. We found this by running our own proposal
   against our own rows, which is the check item 4 asks every reader to be able to make
   and which we could not have made before §3's ledgers were vendored.

   **We then tried to repair it, and the repair fails in a way that matters more than
   the repair would have.** Remove the confound: compute **throughput over non-echo valid
   rows only**. On probe wave 2 the three rungs' observed ranges are disjoint — Q4_K_M
   [17.911, 18.126], Q3_K_M [15.731, 15.938], Q2_K [16.596, 16.718] tok/s, separable per
   invocation. That is where an earlier draft of this section stopped, and it was wrong to
   stop there. Three things break it, each computed in the released script:

   - **Wave 1 is not disjoint.** Its Q4_K_M range, [16.455, 18.188], *entirely contains*
     Q2_K's [16.703, 16.753]. The earlier draft quoted wave 1 by its medians alone
     (18.06, 15.88, 16.74), which hid the overlap — the same selective reporting this
     section exists to indict. Pooled across waves, the bands overlap.
   - **A cold-start effect silently did the filtering.** The first invocation against each
     parent runs at ~92% of that rung's steady-state throughput, uniformly across all
     twelve rung × wave cells (0.918-0.929), consistent with prefill or cache warm-up. On
     wave 2 every cold row happens to be an echo or invalid, so the echo filter removed
     them *by accident* and the "non-echo" set is silently a **warm** set. Wave 1's cold
     Q4_K_M row leaked through at 16.455 tok/s — and it is precisely the row that destroys
     wave-1 disjointness. A verifier's fresh probe is always a cold invocation, so a
     verifier would read the 92% band, not the published one.
   - **The band does not survive a hardware change, and the order inverts.** The same
     SHA-256-pinned Q2_K file runs at 16.62 tok/s on the probe's single P100 and 22.48 on
     the ladder's 2 × T4; Q4_K_M runs at 17.94 and 21.45. On the P100, Q4_K_M is *faster*
     than Q2_K. On the T4s, Q2_K is faster than Q4_K_M. Not a shifted scale — the ordering
     reverses.

   (Throughput is also length-dependent — within-rung correlation between completion
   length and tok/s is about −0.9 — so seconds-per-token is the stable form and is what
   the script reports alongside. That fixes none of the three above.)

   **So the conclusion is negative, and the three mechanisms are the transferable part.**
   Anyone attempting timing-based attestation inherits them regardless of what happens to
   item 4: (i) dispersion statistics are confounded by output identity, and a degenerate
   proposer mimics a fast path exactly; (ii) an ordinary warm-up gradient of about 8% can
   masquerade as a between-condition effect and can be removed *by accident* by an
   unrelated filter, as it was here; (iii) a per-file timing band does not survive a
   hardware change — on two SHA-identical files the ordering **inverts** between a P100
   and 2 × T4. (iii) is structural rather than sample-limited, and it is the one that
   matters most, because attestation is precisely the case where the verifier does not
   control the hardware the calibration would need.

   **What this licenses about C3 (§5), stated narrowly because the over-reach is
   available.** It does **not** show that no observable attests the served file:
   output-side methods exist and §7 cites them, and a search of size two over coarse
   aggregates proves nothing about the space of instruments. What it shows is that **the
   one instrument class a verifier can compute from what an agent runtime already returns
   — timing — is ruled out**, and ruled out for a reason that worsens when the verifier
   loses the hardware. That forecloses the objection a reader raises first, which is that
   the serving path could be inferred from latency without any new field. It does not make
   C3 true, and C3 does not need it.

   What survives is narrower and still worth stating. **Throughput does not order by
   bit-width**, on either ladder: at 14B, Q8_0 — the highest-precision rung run — is the
   *slowest* of four at 14.91 tok/s against Q2_K's 22.48; at 7B, FP16 is slower than every
   quantized rung, and Q3_K_M sits below Q4_K_M at both scales. This is robust to matching
   token counts. It bears on §4, which reads an unusually fast arm as evidence of a
   cheaper or lower-precision serving path: on the one stack we fully control, speed and
   precision are not the same axis. The magnitudes are not comparable — §4's gap is one to
   two orders and these are tens of percent — so this does not overturn that reading, but
   it is a step the inference passes through without stating, and §4 now states it.

   **Item 4 as published is therefore withdrawn in its dispersion form and not replaced.**
   We keep the *disclosure* half — log per-invocation duration and disaggregated usage,
   report distributions — because that costs nothing and enables exactly the audit we just
   ran. We withdraw the firing condition. Proposing a threshold we have now shown fires on
   a fixed serving path, and whose obvious repair fails three ways, would be worse than
   proposing none.

5. **A parent-echo canary, runnable in under an hour before you trust a proposer.** Items
   1-3 are disclosure and item 4's firing condition is withdrawn above, so this is the
   only *instrument* the paper still proposes — and it inherits item 4's failure class,
   which we state before the proposal rather than after it: **its firing condition is
   confounded by a variable the verifier cannot observe.** For item 4 that variable was
   output degeneracy; here it is parent quality, and the table below is the measurement of
   how badly. We publish it anyway, with the precondition that makes it usable, because
   unlike item 4 the confound is one a practitioner *can* control by choosing the parent. The failure mode §3 documents is
   invisible to viability, validity and — per §3.6 — to final best score at a ten-generation
   horizon, so a loop can be degenerate for its whole budget while every dashboard reads
   healthy. The statistic that does see it costs nothing to compute:

   > **The screen.** Hold a parent configuration *fixed*, and make it a **weak**
   > one — in practice your loop's seed configuration. Issue 25-50 proposal calls
   > against it at your production settings. Log the emitted structure verbatim, not
   > only its score. Compute the fraction of *valid* outputs whose structure equals
   > the parent's, compared order-insensitively at the precision your logs carry (we
   > use six decimals). **A rate at or above 60% is a red flag**; at or below 35% the
   > proposer is departing normally.
   >
   > **The five-call version.** Append an explicit prohibition — the output must
   > differ from the parent, at least three elements must change, returning it
   > unchanged counts as failure — and issue five calls. Five echoes out of five is
   > the signal. That is what we observed at Q2_K, against 1 of 5 at Q4_K_M.

   The thresholds are not invented for this section: 60% and 35% are the bounds
   preregistered in the fresh-seed runner before that run executed, and they held at
   79% against 6%. The screen needs no held-out set, no baseline model, and no scorer
   beyond the validity check a loop already runs — the whole cost is logging structures
   instead of scores.

   **Why the parent must be weak, and what happens if it is not.** Those bounds were
   registered for the *loop* condition. Held against a fixed parent the echo rate
   depends heavily on that parent's quality, and §3's probe measures how heavily —
   pooled over both waves, echo among valid outputs by parent score:

   | parent | Q4_K_M | Q3_K_M | Q2_K |
   |---|---|---|---|
   | 0.880 | 7/30 (23%) | 8/26 (31%) | 19/21 (90%) |
   | 0.900 | 8/19 (42%) | 5/20 (25%) | 14/16 (88%) |
   | 1.040 | 21/30 (70%) | 14/25 (56%) | 22/24 (92%) |
   | 1.300 | 16/30 (53%) | 13/28 (46%) | 30/30 (100%) |
   | 1.550 | 23/31 (74%) | 18/23 (78%) | 19/19 (100%) |
   | 1.650 | 15/24 (62%) | 14/20 (70%) | 19/23 (83%) |

   Read the bottom half. **Against a good parent a perfectly healthy Q4_K_M proposer
   echoes at 62-74% and Q3_K_M at 70-78% — past the red line.** Run the screen there
   and it returns RED on a healthy proposer. Only at the weak end is the separation
   clean: 23-42% healthy against 88-90% degenerate. We state this as a precondition
   rather than a caveat because the tool cannot detect the violation, and a screen
   whose false-positive condition is undocumented is worse than no screen. Even at the
   weak end one healthy cell reaches 42%, above the 35% line, so an AMBIGUOUS reading
   does not imply a degraded proposer.

   **What it is and is not.** A canary for a specific, severe endpoint, validated on
   one task, one model family, one scale and one quantization family. **Not** a
   calibrated precision detector: §3's own scheme control returns its inconclusive
   branch, so even a clean RED at a weak parent does not localise the cause to
   quantization. Used as a tripwire — *something is wrong with what is serving this
   proposer* — the screen is supported by the data above. Used as a measurement of
   served precision, it is not.

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

The attestation side of C3 is a crowded line, and our position in it is confirmatory
rather than novel. Cai et al. (arXiv:2504.04715) audit model substitution in commercial
LLM APIs directly, show that software-only detection is unreliable against exactly the
substitution class that includes quantized serving, and arrive at trusted execution
environments as the only route to provable model integrity; Zhang et al.
(arXiv:2607.20860) extend the audit to gateway routing dilution under a query budget;
Schnabl et al. (arXiv:2506.23706) build the TEE half, running verifiable benchmarks
inside enclaves so that neither provider nor auditor need trust the other. Item 4 of §6's
standard — attestation of the served decode path — is therefore not our invention: it is
this line's conclusion restated as a reporting obligation, and what §§3-4 add to it is a
measured demonstration, inside a selection loop, of how much the unattested variable can
matter.

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

The LLM-evolution literature has meanwhile begun cataloguing its own failure modes, and
the catalogue does not contain ours. PACEvolve (Yan et al., arXiv:2601.10657) names three
— context pollution, mode collapse in sampling, and weak inter-generation collaboration —
all observed at full precision and all addressed with orchestration machinery; a
degraded-proposer failure in which the *model itself* silently returns its parent appears
nowhere in the taxonomy, which is consistent with our reading that it is a property of
the serving substrate, not of the evolutionary scaffold. Lin et al. (arXiv:2606.21090)
document a rise-and-collapse failure in self-*training* loops; the mechanism (reward
over-optimization) is unrelated, but it is the nearest published precedent for a
selection loop degrading through a variable its own metrics do not surface.

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

Four 2026 entries sharpen that gap without closing it. Kurt (arXiv:2601.14277) evaluates
the same llama.cpp quantization ladder we sweep — on the same Llama-3.1-8B-Instruct our
wave 7 registration adopts — across standard benchmarks and hardware metrics, one-shot
throughout; it is the closest published instrument to ours and it does not run a loop.
The "Quantization Meets Reasoning" line (Li et al., arXiv:2501.03035 and its expanded
companion arXiv:2505.11574) localizes low-bit damage to mathematical reasoning and shows
targeted fine-tuning recovers it, and Lv et al. (arXiv:2601.14888) systematize when
quantization-aware training rescues reasoning at low bit widths — both establishing that
*reasoning-shaped* capability is disproportionately fragile under compression, which is
the static-benchmark shadow of the effect §3 measures dynamically. Chang et al.
(arXiv:2506.12044) explain *which inputs* break low-bit models via residual-stream
magnitudes, a mechanistic thread a future account of parent-echo would need to engage.
Closest to our setting, Mix-Quant (Lu et al., arXiv:2605.20315) is to our knowledge the
only published treatment of quantization specifically for *agentic* inference — and its
finding that the decode phase, not prefill, is the precision-sensitive one is convergent
with a proposal loop failing at generation time. None of these places a quantized
proposer inside an iterative search and measures what happens to novelty; that remains
the gap this paper occupies.

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
equally unattestable, and C3 (§5) stands either way. The
token-count observation is withdrawn in §4 as a non-finding, and that withdrawal is the
clearest single illustration of why §6 item 4 demands disaggregated usage figures: an
aggregate counter looked like a signature until it was defined.

The `opus_alias` arm is n = 30, and the anomaly, though uniform across all thirty
invocations and all three cells, comes from one batch window. Both follow-ups this paper
named — the **repair probe** and a **second serving-signature snapshot** — have now been
run and are reported in §4.1. Neither converts an inference about the serving path into an
observation of it; that residue is what C3 names, and running them did not touch it. What
they did instead is worth stating as a limitation rather than a result, because it limits
§4 more than it advances it: the snapshot showed the alias's behaviour, latency and usage
spread all moving together within six days, so the hypothesis pair §4 poses — both of
which presuppose the alias names one thing — cannot be settled by any experiment addressed
through that alias, including the discriminator we built for it. **§4's H1/H2 question is
not open pending more data; it is unaskable in the form §4 asks it.** The limitation is
general: any study whose treatment is a vendor alias inherits it.

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
as evidence of no harm. The conditional-quality analysis that accompanies it carries the same
kind of limit and worse. It rests on **ten** 2-bit departures against a floor of
twenty-five that we set ourselves, in an unlocked note, on the day the analysis became
computable — so it confirms nothing, and the threshold it is scored against is not
independent of the data scoring it. The exclusion it does return holds by **0.8 points**
against the least favourable comparator in its own table and reverses entirely if one of the
ten departures flips. It is also a fixed-parent measurement, and §3 says elsewhere that a
fixed parent removes the lineage history the loop includes; whether departure quality holds
up inside the loop is not established by it. This is the thinnest load-bearing thing in the
paper and we would rather a reader learn that from us.

**A rival reading we do not screen: recall rather than construction.** The
template-anchoring story throughout this paper is a claim about what the proposer reaches
for. A sceptic can read the same rows the other way: the nearest-square truncation is
pretraining contamination, and the anchor is recall of packings the model saw rather than
construction. Nothing in this paper rules that out. The cells the anchoring argument leans
on — *N* = 13, 21, 26, 31, 35 — all correspond to grid or grid-plus-filler recipes with
closed forms, which is exactly the population most likely to appear in a training corpus,
so the design gives the rival reading its best case rather than its worst.

We specify a three-probe screen for it in `arm_canary_contamination_audit.py` and **do not
run it**, and the file is more useful for what it gets wrong than for what it would
measure. Its first probe injects a marker at *sampling* time and asks whether the output
echoes it; a canary bears on contamination only when the canary was in the *training*
corpus, so that probe measures instruction-following and is mislabelled. Its second fires
only if every radius is identical, so a memorised template plus one filler passes. Its
third counts distinct coordinate values rather than rows, so any packing with non-lattice
fillers trips it — the same false-positive mode that made us withdraw §6 item 4. All three
defects are recorded in the file's own header. **A contamination screen for this task is
open work, and the version we wrote is not it.** We would rather ship a named gap and a
failed design than a screen whose GREEN verdict a reader could not trust.

**The wave these limits specified has now been run, and its verdict is mixed — reported
here branch by branch, in the registration's own labels.** `wave3_prereg_heilbronn.md`
set the task (Heilbronn triangle at n = 13, chosen because a regular grid scores *exactly
zero* on it, so a proposer emitting its default template is distinguishable from a
proposer copying its parent — a separation circle packing cannot make, its seeded parent
having *been* the template), the allocation (25 lineages at Q2_K against 8 at Q4_K_M),
six closed-form predictions including a control-arm floor, and a disconfirmation clause.
The runner was pushed as a **public Kaggle kernel before any row was sampled** — the first
externally-timestamped registration in either paper, a practice waves 4 and 5 then
repeated (author field open at lock time — the registrations predate the byline this
draft now carries, and the lock section states exactly what that caveat costs). 495 calls ran; `wave3_analysis.py` replays every
count from the raw ledger in exact arithmetic and prints each label.

- **Control-arm floor: TRIGGERED.** No proposal at any rung scored above the seed parent
  in 495 attempts — mean accepted steps 0.0 at Q4_K_M against the registered ≥1.0 floor.
  The search-progress primaries (5.1, 5.2) and the conditional-quality primary (5.3) are
  therefore **UNINFORMATIVE**, exactly as the floor clause was written to force: a
  reference rung that cannot climb cannot separate "the rungs do not differ" from "the
  task is too hard". The seed parent — placed above a 4,000-configuration random-search
  baseline by design — turned out to sit above what this 14B model reaches in one step
  from it, at any precision. The conditional question §3.6 needed 25 departures for
  remains open; this wave produced 109 Q2_K departures and zero improving ones anywhere,
  which answers a different and harsher question about the task than about the rungs.
  A disclosed seed-calibration pilot (`kaggle_wave8_pilot/`, public kernel
  `sohamgugalet/wave8-seed-pilot`, Q4_K_M only, no Q2_K rows) then tested whether an
  easier seed would repair this: four graded best-of-K random parents, scores 0.000308
  to 0.003544 against this wave's 0.009087. **The control rung improved on 1 of 40
  probes** — even from a best-of-1 random configuration — and echoed 6 of 8 valid
  outputs at the easiest seed. The floor is the task, not the seed: no seed choice
  makes Heilbronn a search-progress instrument for this model, so the search-progress
  hypotheses stay tested on circle packing alone, and the recalibrated wave the pilot
  was scoped for is not run. The pilot also shows, on 40 disclosed unregistered rows,
  that the reference rung's regression toward copying on this task (46.9% above) is
  not an artifact of the registered seed's difficulty.
- **Echo (5.4, registered as a conjunction and not floor-gated): REFUTED as registered,
  with one side held.** Q2_K echo among valid: 186/295 = **63.1%**, against the ≥55%
  bound — held; the parent-copying signature transfers to a task whose parent is not a
  template. Q4_K_M: 53/113 = **46.9%**, against the ≤30% bound — refuted, and this is
  the wave's informative surprise: on a task where nothing climbs, the *upper* rung also
  regresses toward copying, at three times its circle-packing rate. The rung separation
  survives descriptively (63.1% vs 46.9%, two-sided Fisher *p* = 3.5e-3, unregistered),
  but the clean "Q2_K-class vs upper-class" echo bands of §3 do not transfer intact:
  echo rate is jointly driven by precision *and* by whether the search has anywhere to
  go. §3's bands were measured on a task with headroom; wave 3 shows what the same
  ladder does without it.
- **The disconfirmation clause does not fire** — it required both 5.1 and 5.4 failing at
  Q2_K, and 5.4's Q2_K side held. The rewrite it would have forced is not owed. What is
  owed, and done here, is scoping: the echo *cliff* (a large between-rung gap among
  valid outputs) is established on circle packing and directionally present on
  Heilbronn; the echo *bands* (≤30% healthy, ≥55% collapsed) are circle-packing
  figures and this paragraph is their correction.

![Echo among valid outputs across tasks, Q2_K vs Q4_K_M on the same 14B GGUF ladder.
The rung contrast transfers; the absolute bands do not, and LABS reverses under a
fired control floor (descriptive only). Every count is printed by a released replay
script; `figures/make_figures.py` only draws.](figures/fig_echo_transfer.pdf)
- **Template check (5.5, no bound): 15.3% of Q2_K and 23.9% of Q4_K_M valid outputs
  score exactly zero** — the GGUF ladder does emit some template-like collinear output,
  at a fraction of the 97.5% rate the strongest hosted tier produced on the identical
  task and seed parent (§6). Same task, same parent, same stall: the quantized ladder's
  dominant failure is copying; the hosted tiers' is template emission. That contrast is
  the two-substrate version of the separation this task was chosen to make.
- **One defect in our own tooling, caught by the released analysis.** The kernel's
  in-flight summary counted a phantom "1 accepted step" per lineage: the ledger logs
  scores at 12 dp (a convention the registration itself sets in §6b), and an echo row's
  rounded score sits 5e-13 above the unrounded seed constant. The exact recomputation
  and all 33 kernel state files agree the true count is zero everywhere. We report the
  bug because the number it fabricated — an accepted step that never happened — is
  precisely the class of artifact this paper exists to make checkable.

**A second transfer wave returned UNINFORMATIVE by its own floor and is reported, not
shelved.** `wave5_prereg_labs.md` (low-autocorrelation binary sequences, n = 32 — a
discrete task with no float arithmetic, registered to test the "echo is float-rounding"
reading) ran 495 calls on the same ladder; its Q4_K_M rung also accepted zero steps, its
control floor fired, and no branch of its decision rule is claimed. Its unclaimable
descriptives (echo 4.3% at Q2_K vs 20.0% at Q4_K_M — *reversed*, on a task where a
single flipped symbol is a complete departure) are recorded in `wave5_output/` with the
verdict label attached. Two of the three transfer tasks we designed were too hard for
the model that had to climb them; that is a fact about our task calibration, disclosed
as such, and the LABS registration predicted its own failure mode in §8b before running.

**The family axis was then tested and returned UNDERPOWERED in both arms — reported
here in its registration's labels.** Every GGUF figure above comes from a single model
family, and the referee's cheapest sentence is that the cliff is a Qwen artifact.
`wave7_prereg_families.md` (SHA-256 `44244005…`, published as a public Kaggle dataset
before sampling) registered the same circle-packing protocol, byte-identical prompts
and evaluator, on Llama-3.1-8B-Instruct and Gemma-2-9B-it — per-family directional
contrasts only, no absolute band imported from any prior task or family, echo primary
not floor-gated, a 20-valid-row power floor per rung, and a disconfirmation clause
committing us to qualify §3's claims as Qwen-family-specific if the contrast was
refuted in both families. Neither family reached its power floor. Llama produced 1
valid packing in 50 at Q4_K_M and 5 in 50 at Q2_K, failing by the same wrong-count
lottery the 7B Qwen ladder shows (counts scattered 18-30 around the demanded 26);
Gemma produced 14 and 4 — and, as an unclaimable descriptive, **all 18 of Gemma's
valid outputs at both rungs are coordinate-exact parent echoes**, while none of
Llama's 6 are. `wave7_analysis.py` prints UNDERPOWERED for both families, the control
floors also fire, and the disconfirmation clause — which requires both families
*evaluable* and refuted — does not. One defect in the locked registration itself,
caught after the fact and disclosed here because the file is public and immutable: its
informational prior-state section quotes Qwen echo figures from working notes
("94% / 60% / 51% against 15% / 10% / 24%") where ledger replay gives 94%/15% for the
registered wave but **79% (19/24) against 6% (1/17)** for the fresh wave and 75%
against 43% for the IQ2 pair. The discrepancy sits in a section that states priors,
not in any registered bound, floor, or verdict — none of which reference those
figures — and the correct values are the ones the figures in this paper draw from. What wave 7 establishes is therefore a scope
fact, not a transfer fact: the 8-9B open-weight class sits below this task's
competence floor at every precision tested. The power floor exists precisely so that
this outcome reads as "could not test" rather than "no difference".

**A competence-matched retry (wave 7b) then fired the branch its registration wrote
for this exact outcome.** `wave7b_prereg_families_14b.md` (SHA-256 `cd043d63…`, public
Kaggle dataset pushed before sampling) re-ran the identical protocol on Phi-4 (14.7B)
and Mistral-Small-24B — the same size class as, and larger than, the Qwen model where
the cliff lives. Both arms again miss the 20-valid-row floor: Phi-4 produced 9 valid
packings in 100 loop calls, Mistral 2. The registered both-underpowered branch
therefore holds: **the task's format-competence floor excluded every non-Qwen family
we tested, at up to 24B**, and the family-generality limitation is stated as
unresolved in the abstract's scope sentence, as that branch requires. Two unclaimable
descriptives are still worth the ink. First, the competence-matched arms — unlike the
8-9B ones — *climbed*: four of Phi-4's five Q2_K lineages improved past the seed (best
1.30, one Q4_K_M lineage reaching 2.1667), and Mistral improved in one lineage per
rung, its Q2_K best of 2.1667 the largest climb any non-Qwen arm produced. Neither
model echoed even once at either rung; Phi-4's must-differ probe returned the
instruction-sensitive branch (vacuously so: that branch exists to explain loop echo,
and Phi-4 produced none for instruction to explain). Second, across all four non-Qwen
arms the 35 valid outputs split into Gemma's 18 (every one a parent echo, at both
rungs) and the other three families' 17 (not one echo). Whatever governs
parent-copying, it is not bit-width alone: on these small samples it looks
family-shaped, which is precisely what the registered FAMILY-DEPENDENT reporting rule
anticipated and precisely what remains untested at adequate power. A family ladder at
this task needs either a coder-tuned non-Qwen 14B that can hold the output format, or
a format-forgiving task — both are named as open work, and no absolute figure from
any arm above transports anywhere.

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
| §3 Fisher figures *p* = 5.7e-10 (17/18 vs 8/57), 0.001 (15/15 vs 1/5, **pooled**), 0.44 (F1's outcome), 1.0 (FP16 vs Q3_K_M viability) | `sec3_7b_repro.py`, run with no arguments. It also prints the paired form of the 0.001 contrast, *p* = 0.048, so the pooling is visible |
| §3 inferential status of all twenty-nine *p*-values (accounting in Appendix A.4) | §3: nine Fisher, six preregistered permutation tests, two Spearman orthogonality diagnostics and twelve post-hoc lineage-level permutation tests; the four families not pooled, the reason given for each, and the Bonferroni threshold stated for the Fisher and post-hoc families |
| §3.6 search progress: accepted steps per lineage (1/50, 15/50, 16/50, 14/50 on the registered ladder; 3/50 vs 14/50 fresh; 6/50 vs 16/50 IQ2; 7/50, 4/50, 3/50, 2/50, 6/50 at 7B), the identity gaps *k*, the conditional-on-departure rates, final best per lineage, and all twelve exact permutation tails | `sec3_search_progress.py`, run with no arguments; replays all four vendored ledgers. Ten are stated in §3.6; the two 7B final-best tails, 0.158 and 0.119, are stated in §3.6's 7B paragraph. **Post-hoc** — labelled as such at every use, and §3.6 states that the fresh wave's registered *primary* (F1) failed |
| §3.6 conditional quality: 60/74, 61/70, **8/10** improved among departures pooled over both probe waves, the per-parent breakdown, Fisher *p* = 1.00, and the exclusion of the collapse branch (95% lower bound 44.4% against 40.5 / 42.0 / 43.6% depending on comparator) | `sec3_conditional_quality.py`, run with no arguments, from `score_delta` and `echo` in the two vendored probe ledgers. **Post-hoc**, in neither wave's preregistration, and UNDERPOWERED against a 25-departure floor we specify ourselves in an unlocked design note, not a registration; §3.6 states the exclusion's margin against the least favourable comparator (0.8 points) and its reversal if one row flips |
| §3.6 horizon argument: the departure rates and offer distributions (6 vs 33 observations), the discarded directional projection, and the **withdrawn** power figure | `sec3_horizon_power.py`, run with no arguments. A **resampling projection**, not a measurement. §3.6 states that an earlier draft's "17% power" claim is withdrawn — the only alternative this model supplies is the projection it disowns — and that the surviving content is structural: final best score is a maximum and is therefore the wrong dependent variable for this effect |
| §3.6 the failed registered improvement prediction F1 (≤ 2/5 Q2_K, ≥ 4/5 Q4_K_M; observed 3/5 vs 5/5) and its **primary** designation | `sec3_artifacts/runners/kaggle_precision_sweep_14b_fresh.py` header, which reads `F1 Improvement (seed-level, primary)`; F2, the echo bound the paper leans on, carries no such label. Outcome computed by `sec3_search_progress.py` from the fresh ledger |
| §6 wave 4 capability-tier control: echo 0/120 (0% per tier vs registered ≤30% bound, verdict DISSOCIATION), secondary 5.2 NOT EVALUATED (10-echo floor unmet), template rates 52.5% / 27.5% / 97.5%, zero improvements past seed, `tool_uses` 0/120 | `wave4_artifacts/wave4_tiers.jsonl` (120 rows), replayed by `wave4_analysis.py` with no arguments, which recomputes every echo and score from stored coordinates and prints each verdict label. Registration `wave4_prereg_tiers_heilbronn.md` (SHA-256 `7b3e67dc…`, public Kaggle dataset `sohamgugalet/wave4-prereg-tiers-heilbronn`, pushed before sampling — author field open, and the file retains its pre-lock draft header: the lock is the published SHA plus the dataset's creation timestamp, and prereg and rows share one date, so push-before-sampling ordering rests on the dataset timestamp alone). All-distinct uniqueness count is **post-hoc, from `wave4_artifacts/MODEL_IDS_NOTE.md`, not computed by the replay script**; model-ID caveats same file |
| §3 7B ladder: viability 7/6/9/7/16 per 50 with Wilson intervals, all three contrasts, the format-lottery counts (45 of 250 at exactly 26, 153 at 24-25, modal count per rung), the truncation check (687 tokens against a 1200 cap among the 24-25 rows), probes 0/30, best score 1.79998 | `sec3_7b_repro.py`, run with no arguments, from `sec3_artifacts/precision_sweep/`. Narrative and scope caveats in `sec3_artifacts/precision-cliff-paper-combined.md` §3.4, §5.9, §6 |
| §3 IQ2_M invalid near-copy 2/22 | **not reproduced**: our replay of the stated definition returns 1/22 (§3) |
| §8 wave 3 (Heilbronn): control floor TRIGGERED → 5.1/5.2/5.3 UNINFORMATIVE; 5.4 echo Q2_K 186/295 = 63.1% HELD vs ≥55%, Q4_K_M 53/113 = 46.9% REFUTED vs ≤30%, conjunction REFUTED; Fisher 3.5e-3 (descriptive); template 15.3%/23.9%; 0/495 improvements; phantom-step rounding artifact | `wave3_output/precision_sweep_14b_heilbronn/candidates_precision_14b_heilbronn.jsonl` (495 rows), replayed by `wave3_analysis.py` with no arguments in exact arithmetic; agreement with all 33 kernel state files printed. Registration `wave3_prereg_heilbronn.md` + runner SHA `101b298c…`, pushed as public Kaggle kernel `sohamgugalet/precision-sweep-14b-heilbronn-wave3` before sampling — externally timestamped, author field open |
| §8 wave 5 (LABS): control floor TRIGGERED → verdict UNINFORMATIVE, Branch C, no branch claimed; unclaimable descriptives echo 10/233 = 4.3% Q2_K vs 12/60 = 20.0% Q4_K_M (reversed), 0 improving departures anywhere, 0 symmetry variants | `wave5_output/precision_sweep_14b_labs/` ledger (495 rows), replayed by `wave5_analysis.py` with no arguments in exact integer arithmetic — every energy and echo recomputed from stored sequences, agreement with all 33 kernel state files printed (`gpu_crossing: single_card_fallback` recorded). Registration `wave5_prereg_labs.md` SHA `a1336cfd…`, runner SHA `d1739f6c…`, pushed as public kernel `sohamgugalet/precision-sweep-14b-labs-wave5` before sampling |
| §8 wave 7 (family generality): UNDERPOWERED both families (valid rows, Q2_K then Q4_K_M: llama 5/50 and 1/50; gemma 4/50 and 14/50, all under the registered 20-valid floor); control floors fired; disconfirmation clause does not fire; unclaimable descriptives — gemma 18/18 valid outputs are parent echoes at both rungs, llama 0/6 | `wave7_output/wave7_{llama31_8b,gemma2_9b}/` ledgers (100 rows each), replayed by `wave7_analysis.py` with no arguments (validity recomputed from coordinates, 10/10 state files agree per family). Registration `wave7_prereg_families.md` SHA `44244005…`, public Kaggle dataset `sohamgugalet/wave7-prereg-families` pushed before sampling; kernels `precision-sweep-llama31-8b-wave7`, `precision-sweep-gemma2-9b-wave7` public |
| §8 wave 7b (competence-matched retry): UNDERPOWERED both families (valid rows, Q2_K then Q4_K_M: phi-4 6/50 and 3/50; mistral-24B 1/50 and 1/50) → registered both-underpowered branch holds; unclaimable descriptives — phi-4 0 echoes, 4/5 Q2_K lineages improved (best 1.30), must-differ instruction-sensitive (vacuously); mistral 0 echoes, 1 lineage improved per rung, Q2_K best 2.1667 | `wave7b_output/wave7b_{phi4_14b,mistral24b}/` ledgers (100 rows each), replayed by `wave7b_analysis.py` with no arguments, 10/10 state files agree per family. Registration `wave7b_prereg_families_14b.md` SHA `cd043d63…`, public Kaggle dataset `sohamgugalet/wave7b-prereg-families-14b` pushed before sampling; kernels `precision-sweep-phi4-14b-wave7b`, `precision-sweep-mistral24b-wave7b` public |
| §3 re-execution determinism, externally exercised: 112/112 per-row digest MATCH on T4 x2 (verdict SUPPORTED); two prior P100 draws returned 112/112 VOID_ARCH each, not compared | `kaggle_redetermin/` runner (SHA `58d9a4c8…`, 112 embedded per-row digests from the vendored v2 ledger) + `output_v3/redetermin_summary.json`; public kernel `sohamgugalet/precision-redetermin`. Caveats in-file: `build_unverified: true` (wheel version-pinned 0.3.34, original build unrecoverable); q8_0/q3_k_m skipped with reasons printed |
| §6 item 4 self-audit and the failed repair: duration CV 0.0603 vs **0.0143** (wave 1) and 0.0692 vs **0.0200** (wave 2), ratios below the item's own one-third threshold, permutation *p* < 0.0001; the echo/non-echo CV split; wave-2 throughput ranges disjoint **and wave-1 ranges overlapping**; the ~92% cold-start ratio in all twelve rung × wave cells; the same-SHA hardware inversion (Q2_K 16.62 tok/s on P100 vs 22.48 on 2 × T4); the length dependence; and the bit-width non-monotonicity §4 cites | `sec6_cv_canary_audit.py`, run with no arguments. It reads both probe ledgers **and both 14B/7B ladder ledgers** — every figure above is computed there, including the ladder throughputs §4 cites, none quoted. The serving path is fixed by construction across the probe rows, so the firing is a **false positive** by design of the comparison |
| §4 validity, failure taxonomy, families, scores, both tolerances | `arm_f_raw.json` `opus_alias` / `sonnet_bare` / `bare` rows, recomputed with `arm_f_repro.py` |
| §4 fourth comparator: `trace` 63/70 valid (18/20, 28/30, 17/20), Fisher 1.1e-13 against `opus_alias` and 1.0e-16 pooled, comparator-vs-comparator *p* = 0.30 and 0.099 | `arm_f_raw.json` rows with `arm == "trace"`, scored by `sec4_independent_rescore.py`'s checker. **Pools the companion paper's pilot and `trace_v2` rows, which that paper forbids pooling**, because the released file carries no field separating them — stated in §4, and no claim rests on the arm |
| §4 durations | `STATE.md` §8, §8b — session-log ranges; per-invocation vector not captured (§4, §5) |
| §4 registration digest | `arm_o_preregistration.txt`, SHA-256 published in §4 |
| §4.1 arm B2 re-snapshot: 10/10, 10/10, 10/10 against 3/10, 1/10, 0/10; pooled 30/30 vs 4/30, Fisher *p* = 7.8e-13; best valid 1.776141, 2.276800, 2.794180; latency 68.7-594.1 s; usage 58k-195k | `arm_r_artifacts/b2_alias_n{13,21,31}.jsonl`, replayed by `arm_r_analysis.py` with no arguments; scored by `arm_f_repro.py`'s own validator against the 2026-08-01 rows in `arm_f_raw.json`. Per-invocation duration and usage are **in the ledger**, unlike the 2026-08-01 arm |
| §4.1 arm R repair probe: 59/60 exact, per-cell 5/5 everywhere except alias `n31_d0.001` at 4/5, recall 1.00 in every cell, zero empty responses, and the single miss's 7.089e-04 true clearance | `arm_r_artifacts/r_n{13,31}.jsonl` against the exact key in `arm_r_key.json`, both replayed by `arm_r_analysis.py`. The key and the six prompt digests are generated by `arm_r_build.py`, committed before the first invocation |
| §4.1 registered scorecard: P-R1, P-R4, P-R5 held (P-R4 **vacuously**); P-R0, P-R2, P-R3, P-R6 failed | `arm_r_preregistration.md`, committed in `e77bb0e` before any sampling; every prediction re-scored line by line in `arm_r_analysis.py`'s scorecard block. A **local** commit, not an external timestamp — the file says so and the paper does not call it more than it is |
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

**The registered replacement rule, adjudicated in full, and the two caveats §3 points
here for.** §3 states the verdict and the direction of each caveat; the working is here.

**Under the registered replacement rule this returns no category.** SURVIVES needs both
spread measures at *p* < 0.05 and rarefaction is 0.953; PARTIAL needs score to decline
monotonically and it does not; FALSIFIED needs both spread measures flat and NED is 0.030;
UNDERPOWERED does not apply. The honest label is unclassified. That disqualifies the
*registered mechanism verdict* specifically, and we make no use of it; it does not
disqualify the probe's descriptive counts, which §3 reports as descriptive and labels
post-hoc where they are.

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

### A.4 Every *p*-value reported in §3 and §3.6, its family, and the defect that family carries

Section 3 states the summary of this appendix and points here. Nothing below is new evidence; it is the accounting behind the four-family statement, moved out of the body because six rounds of correction had grown it past the length its role justifies.

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
lineages. These twelve do not have the *calls-within-lineage* nesting defect the
candidate-level Fisher tests have, because the permutation unit is the lineage — but two
weaknesses remain and neither should be read as absent. Five lineages per cell is a small
pool, and the exact enumeration (252 splits for a 5-versus-5 comparison) bounds how small any
tail can be. And **the design is seed-crossed while the test is not stratified**: the same
five seeds appear at every rung of a ladder, so the twenty lineages of the pooled comparison
are five matched quadruples rather than twenty exchangeable draws, and the enumeration
permutes them as though they were. Ignoring positive pairing is conservative for a difference
of means, so this bounds the tails rather than reversing them; the matched alternative — a
stratified test permuting rungs within each seed — has a minimum attainable *p* of 1/16 on
five pairs and so could not have produced any of the values above. We report the unstratified
tails and name the pairing rather than leave it implied absent. We additionally computed a call-level Fisher
tail on the IQ2 control's step counts (*p* = 0.028) and report it here only to record that
we do not use it: calls within a lineage are not exchangeable, the lineage-level tail on
the same counts is 0.135, and the more favourable number is the wrong one.
