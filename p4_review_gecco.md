# Review — Paper 1 ("precision cliff" / template anchoring in circle packing)

**Reviewer:** GECCO / ALIFE-community domain reviewer (evolutionary computation + LLM-driven
discovery: FunSearch/AlphaEvolve lineage, quality-diversity, MAP-Elites).
**Materials reviewed:** `paper1_draft.md` (full), `fig1_trapzones.png`, `fig2_packings.png`,
`fig3_armT.png`. No author-side notes, logs, or state files consulted. Citation checks
performed against arXiv listings and the public record.
**Date:** 2026-08-01

---

## Summary of the submission

The paper asks what a language model emits when asked, zero-shot and without a code channel,
to place N non-overlapping circles in a unit square maximizing the sum of radii. It reports
that a weak-tier proposer reaches for a k×k grid with corner fillers, selects
k\* = round(√N), and *truncates* rather than dropping to k−1 and filling when k\*² > N. It
gives a value function V(k, m) = k/2 + m(√2−1)/(2k) and a truncation function
T(k, N) = N/(2k), preregisters exact-value point predictions with SHA-256 prompt hashes,
tests them out of sample on a square and a rectangle, adds a three-tier ladder and an
elicitation-as-intervention arm, and keeps a negative result (§3.4) where the closed form
fails to generalize.

## What is good, stated up front so the criticism below is read in proportion

The arithmetic that is reported is correct. I recomputed every closed-form anchor in §2.2
and §2.4 independently: V(5,1) = 2.5414214, V(5,2) = 2.5828427, V(4,7) = 2.3624369,
T(5,23) = 2.300, V(3,4) = 1.7761424, V(4,5) = 2.2588835, V(5,6) = 2.7485282,
V(6,7) = 3.2416246, V(6,1) = 3.0345178, V(4,1) = 2.0517767, T(6,35) = 2.9166667, and every
worst-in-zone penalty (8.51%, 7.03%, 6.01%, 5.25%) reproduces to the stated digits. The trap
zone formula N ∈ [k²−k+1, k²−1] and the primality refutation list in §2.3 (13, 23, 31, 43,
47, 59 trap; 11, 17, 19, 29, 37, 41, 53 converge) are both correct. §3.4 — keeping the
rectangle filler formula's failure in the paper, with the LP counterexample at 1.125 against
1.1545085 — is exactly the right instinct and is rarer than it should be. The LP oracle as
an independent value gate, the loose/exact dual scoring convention fixed in advance, and the
refusal to score the concurrency-cap rejections as model failures are all good practice.
The core artifact — a closed form that names a specific multi-decimal output before sampling
— is genuinely novel in this literature and is worth publishing once scoped honestly.

The problems below are almost all problems of **scope of claim** and **citation accuracy**,
not of measurement.

---

## MAJOR

### [MAJOR-1] The paper measures a distribution that no evolve system samples from, and the abstract claims otherwise

This is the central problem and it is the one the reviewer question anticipates. Naming it
precisely:

The abstract's closing sentence — "Our results characterize the proposal distribution that
LLM-driven discovery systems sample from" — and the §1 framing ("Those systems place a
language model in a proposal role inside an evolutionary loop... We test that assumption on
their own home benchmark") assert that the measured object is the same object those systems
query. It is not. The measured object is

    p(coordinates | task description, no parent, no code, no evaluator feedback, generation 0)

whereas FunSearch, AlphaEvolve, ShinkaEvolve, HELIX, GigaEvo and AdaEvolve query

    p(program | parent program(s) + their fitness scores + evaluator feedback +
                (in GigaEvo and ShinkaEvolve) archive/island context and generated
                "insights", at generation t > 0)

These differ along **four simultaneous axes**, not one:

1. **Parent conditioning.** In every system cited, the LLM call is a *mutation* or
   *crossover* operator with one or more parent programs in context. AdaEvolve's own abstract
   (2602.20133, verified) describes LLMs as "semantic mutation operators within evolutionary
   loops." A zero-shot call has no parent. Anchoring to a memorized template is precisely the
   behavior most plausibly *displaced* by an in-context parent — a parent that is a 4×4 grid
   plus fillers is itself an anchor, and the paper's own thesis (models drag toward the
   nearest available template) predicts that the in-loop distribution should be dominated by
   the parent, not by round(√N).
2. **Output modality.** The systems emit *programs*, typically programs that then invoke a
   numerical optimizer (SLSQP, annealing, gradient refinement). The paper emits literal
   coordinates.
3. **Feedback.** The systems condition on scores; the paper conditions on nothing.
4. **Generation index.** The systems run thousands of generations under selection; the paper
   runs one call.

**The §2.1 justification for axis 2 is self-undermining.** The paper writes: "Given a code
channel the model delegates to an optimizer and the distribution reflects the optimizer."
That is a statement that *the channel the target systems actually use produces a different
distribution than the one measured here* — offered as the reason for removing it. You cannot
remove the channel on the grounds that it changes the distribution and then claim to have
characterized the distribution of systems that use that channel. This sentence should be read
by the authors as the strongest argument against their own framing. (It is also asserted with
zero supporting data in this paper; see [MINOR-18].)

**The bridge rests on an uncitable result.** §2.1 and §8 both justify the loop substitution
with "paper 0 found the loop to perform comparably to best-of-N on this task." A reviewer
cannot see paper 0, it is not cited with an identifier, and it carries the paper's entire
external-validity argument. Even if true, "the loop performs comparably to best-of-N *in
final score*" does not entail "the loop's per-call proposal distribution equals the zero-shot
distribution" — two very different distributions can have the same max over N draws. The
inference as stated is a non sequitur.

**What survives the gap, in decreasing order of safety:**

- **Fully survives.** "Zero-shot, code-free, single-call proposals from a weak-tier model on
  max-sum-of-radii circle packing concentrate on a nearest-square grid-plus-filler template;
  the emitted value is predictable in closed form to seven decimals from N alone, ahead of
  sampling, out of sample, on two containers." This is the paper's real result and it is a
  good one.
- **Survives with explicit hedging.** "Any *unconditioned* LLM call inside such a loop — the
  generation-0 population, an island reseed, a restart after stagnation, a
  fresh-sample-instead-of-mutate branch — inherits this anchor, so the initial population of
  these systems is far less diverse than assumed." This is legitimate because such calls
  demonstrably exist in the cited systems, and it is a *sharper and more useful* claim for
  the GECCO audience than the current one: it tells implementers where the collapse enters.
- **Survives only as a stated hypothesis.** Everything about what the loop samples from at
  t > 0, what selection pressure is filtering, and the "mechanism-free account of the loop"
  in §7.1's closing sentence.
- **Does not survive.** The abstract's final sentence, the §1 sentence "We test that
  assumption," and Contribution 1's implied generality. These must be rewritten.

**What would close the gap, cheaply, with the existing harness.** A one-parent mutation arm:
same cells (N = 13, 21, 31, 43), prompt = the bare template plus one parent packing plus its
score plus "propose a modification that increases the sum of radii." Run three parent
conditions — (a) the on-prediction truncated grid, (b) the higher-value rival from the
recipe family, (c) an off-family parent. Measure whether k\*(N) still predicts, whether the
model inherits the parent's k, and whether it escapes. This is ~120 invocations and it would
convert the paper's central claim from analogical to demonstrated. Without it, the title and
abstract must not mention what loops sample from. **I would accept the rescoped paper; I
would not accept the current framing.**

### [MAJOR-2] The closed form is falsified for two of the paper's own three tiers, and the abstract does not say so

The abstract states, unqualified: "models do not search: they recall a single
grid-with-corner-fillers template and truncate it" and "a selection rule k\* = round(√N)
together with a value function V(k, m) predicts the exact sum-of-radii the model will emit."
§4 then reports that the Sonnet-tier proposer is on-prediction **1 time in 30** at the same
cells where Haiku is 12/16, and that the third tier is not evaluable at all. So the closed
form predicts the output of exactly one of three tested tiers. §4 does concede this ("the
nearest-square rule of §2 is therefore a weak-tier law"), but the abstract, the introduction
and Contribution 1 do not carry the scoping, and a reader who stops at the abstract will take
away a false claim.

This is not a presentational nit, because of where the failure falls. The systems in §7.1 do
not run weak-tier models in the proposal role — AlphaEvolve, ShinkaEvolve and GigaEvo run
frontier or mid-tier models, and ThetaEvolve's contribution is specifically that an 8B
open-source model can be made to work via test-time learning. The tier at which the paper's
law holds is the tier the target literature does not use, and the tier closest to what they
use (Sonnet) *escapes the trap in the paper's own data* — 30/30 valid, all N = 21 values in
[2.14, 2.25], strictly above the 2.1 trap, and one N = 31 sample leaving the recipe family
upward at 2.75. Combined with [MAJOR-1], the honest reading of §4 is: **the phenomenon
weakens monotonically as you move toward the models the discovery systems actually deploy.**
The paper should say this itself rather than let a reviewer say it. Rewrite the abstract to
scope every closed-form claim to the weak tier, and treat §4 as a *boundary condition on the
result* rather than as a second finding.

### [MAJOR-3] §7.1 inverts the record on circle packing, and the record source is never cited

Three connected problems in the same paragraph.

(a) §7.1 states: "the published best-known lower bounds that §2.1 scores against sit above
all of them." This is false. The public record for n = 26 max-sum-of-radii runs
**2.634 (Friedman, 2012) → 2.63586276 (AlphaEvolve) → 2.635983283 (ShinkaEvolve)**, with
ThetaEvolve (2511.23473, verified) claiming *new best-known bounds* on this problem. The
LLM-driven systems **are** the published record; they did not fall short of it. Worse, the
paper's own arithmetic gives it away: §2.4's "deficit ... is 0.0946 at N = 26" is exactly
2.635983283 − 2.5414214, i.e. the bound being scored against **is ShinkaEvolve's number.**
The paper is therefore simultaneously using an LLM-system result as the record and telling
the reader that the records sit above the LLM systems. Fix the sentence, and state plainly
which value is used as the record at each N and who produced it.

(b) The record table has **no citation anywhere in the paper.** §2.1 says "published
best-known lower bounds exist for small N (see §7.1)" and §7.1 contains no table, no
Packomania reference, no Friedman reference, no Specht reference. Every "deficit against
published lower bounds" number in §2.4, and the LP gate's abort condition ("any predicted
value exceeding a published lower bound"), depend on a source the reader cannot check. This
must be cited explicitly, per N, with a retrieval date.

(c) **AlphaEvolve and ShinkaEvolve are the only two systems in the list given no
identifier**, while HELIX, GigaEvo, AdaEvolve, SeaEvo and ThetaEvolve all receive arXiv ids.
These are the two most load-bearing citations in the paper. Additionally, AlphaEvolve's value
is given as "2.635" when the reported figure is 2.63586276; the truncation makes the
"essentially the same number" claim look tighter than it is, since AlphaEvolve and
ShinkaEvolve differ at the fourth decimal and the ordering is what "saturated" turns on.

### [MAJOR-4] SeaEvo (2604.24372) does not evaluate circle packing

§1 and §7.1 both place SeaEvo among the systems reporting a ~2.636 circle-packing value
("with SeaEvo (2604.24372) and ThetaEvolve (2511.23473) in the same band"). I checked the
abstract and the full PDF: SeaEvo ("Advancing Algorithm Discovery with Strategy Space
Evolution") does not use circle packing as a benchmark and reports no sum-of-radii figure.
Either the citation is wrong or the claim is. Remove it or replace it with the system
actually intended.

### [MAJOR-5] 2605.29268 is misattributed, and it is the paper's nearest claimed corroboration

§7.2 states: "Nearer still in benchmark terms, 2605.29268 reports asymmetric proposal mass on
this same task in program space — corroborating evidence in a different modality, which is
why our zero-shot, no-code setting is worth reporting separately: the anchoring is not an
artifact of the code-generation channel."

2605.29268 is **"Compute Allocation in Evolutionary Search: From Depth–Breadth to..."** — a
paper about distributing LLM calls across parallel trajectories using multi-armed bandits. It
does not study circle packing and does not report asymmetric proposal mass. This is the
single citation in the paper that would otherwise partially bridge [MAJOR-1] (anchoring
observed in the *program* modality, i.e. the loop's actual channel), and it does not say what
it is claimed to say. Either find the correct reference or delete the sentence — and note
that deleting it removes the paper's only cited evidence that the anchoring survives the code
channel, which strengthens [MAJOR-1].

### [MAJOR-6] The §7.4 disambiguation rests on a partition that two of its members do not belong to

§6 and §7.4 partition the faithfulness literature into (i) a "causal decoupling" cluster
(Reasoning Theater 2603.05488, Project Ariadne 2601.02314) and (ii) a cluster that
"estimate[s] faithfulness by counterfactual perturbation, hint-insertion and consistency
probing, because no ground truth for the described process exists in their settings"
(2503.08679, 2606.13603, 2605.29087). Checked:

- **2606.13603** = "Beyond the Commitment Boundary: Probing Epiphenomenal Chain-of-Thought in
  Large Reasoning Models." It uses early-exit and attention probes to show later reasoning
  steps are epiphenomenal. That is cluster (i), not (ii) — it is doing the same thing
  Reasoning Theater does.
- **2605.29087** = "The Chain Holds, the Answer Folds: Trace-Answer Dissociation in Reasoning
  Models Under Adversarial Pressure." It studies answer flips under multi-turn adversarial
  pressure while traces stay accurate. Also a dissociation result, not a
  hint-insertion/consistency-probing faithfulness estimator.

Only 2503.08679 ("Chain-of-Thought Reasoning In The Wild Is Not Always Faithful") is where
the paper puts it. Since §7.4's entire positioning argument is that the paper's contribution
sits at a *third* intervention point distinct from two existing clusters, and two of three
members of cluster (ii) are actually in cluster (i), the positioning argument needs rebuilding
on correct citations. The underlying positioning (we vary whether a trace is *requested*,
not what it *contains*) is sound and worth keeping — it just needs references that support
the partition.

### [MAJOR-7] 2407.10873 is filed under skepticism but concludes the opposite, and its conclusion cuts against the paper's own design

§7.2 lists "2407.10873 isolates how much of the performance is attributable to evolutionary
search rather than the proposer" inside a paragraph explicitly framed as "a broader skeptical
literature." The paper is Zhang, Liu, Lin, Wang, Lu & Zhang, "Understanding the Importance of
Evolutionary Search in Automated Heuristic Design with Large Language Models," and its stated
conclusion is that it provides "empirical grounding for the **importance** of evolutionary
search in LLM-based AHD approaches." It is evidence *for* the loop.

This matters beyond citation hygiene: it is direct published evidence against the paper's
substitution of a single zero-shot call for the loop ([MAJOR-1]). Citing it as an ally while
its conclusion contradicts the paper's key methodological assumption is the kind of thing a
GECCO reviewer will notice immediately. Recite it correctly and engage with it in §8.

Conversely, **"Dictionaries, Not Darwin" (2607.04108, verified: Pan Li) is the paper's best
friend and is buried.** Its finding — "parent-conditioned evolution is indistinguishable from
fresh independent sampling" at equal budget — is the single strongest published support for
treating the zero-shot distribution as informative about the in-loop one. It is currently one
clause in a six-item list characterized as "question whether the model contributes search or
retrieval." It should be promoted into §2.1 or §8 as the explicit external warrant for the
loop substitution, with its scope limits (equation discovery, not geometry) stated.

### [MAJOR-8] k\* = round(√N) is close to analytic given the recipe family; the falsifiable content is the branch rule, not the selection rule

The paper presents the selection rule as the empirical discovery ("supplying that turns
description into forecast," "Zero free parameters"). But consider what the four candidates
actually are. Given that the model emits *some* k×k grid from this family, "pick the nearest
square lattice" yields k = round(√N) by construction. Note further that the other natural
formalization, argmin_k |k² − N|, switches at N = k² + k + 0.5 and round(√N) switches at
N = (k + ½)² = k² + k + ¼; on integers these are **identical** (both give k for
N ∈ [k²−k+1, k²+k]). Two independent formalizations of "nearest" coincide, which is a
symptom that the rule is not selecting between substantive hypotheses — it is a restatement of
"nearest," which is also how §2.3 names it ("nearest integer square root").

The genuinely non-trivial, falsifiable content is the **branch behavior**: when k\*² > N, the
model *truncates* the k\*-grid rather than dropping to k\*−1 and filling. Nothing about
"nearest" forces that; a model with any local search would drop and fill, which is why the
trap zones exist and why the rival value is reachable. §2.2 already says this ("the observed
behavior is not to drop to a smaller grid and fill it, but to truncate"), but the paper's
rhetoric consistently foregrounds the selection rule.

**Recommendation:** demote k\*(N) to a definition ("we write k\*(N) for the nearest-square
order"), and promote *truncate-vs-drop-and-fill* to the tested hypothesis. This is a strictly
stronger paper: the tested claim becomes a genuine dichotomy with a clear alternative, and
the "zero free parameters" framing stops overselling something that is definitional.

### [MAJOR-9] On-prediction is scored as a binary; the alternative rules are never fitted to the full sample, and the rectangle claim rests on 5/11 with no null model

Three connected evidence problems, all bearing on the reviewer question "does the model apply
the rule, or does the rule happen to fit at three tested N?"

(a) **Every discriminating N is a trap N, by construction.** floor and round disagree exactly
when frac(√N) ≥ ½, i.e. exactly on N ∈ [k²−k+1, k²−1]; ceil and round disagree on the
converge branch; argmax and round disagree where the family optimum differs from the
prediction, i.e. again inside trap zones. So the rule's discriminating evidence lives entirely
in trap zones, and the tested trap cells are k = 4, 5, 6, 7 (N = 13, 21, 31, 43) plus two
rectangle cells. Four values of k is real evidence but thin for an integer rule, and the
paper should say that its confirmatory power is concentrated on four points, not on "every
other N becomes out-of-sample" (§2.3) which reads as if the whole sweep were tested.

(b) **The k = 8 zone is never tested.** N ∈ [57, 60] appears in the abstract, in §1, in §2.4
and as a shaded band in Figure 1, but no cell in that zone was sampled. It is the largest-k
test available in the swept range, the rule predicts a 4.66% penalty there, and its absence
is conspicuous given every other zone was probed. Run N = 57.

(c) **The rectangle result is weaker than the sentence it supports.** §3.3 reports 5 of 11
valid proposals on-prediction and concludes "Nearest-template anchoring is not an artifact of
the one-parameter square case." 5/11 = 45%, exact binomial 95% CI roughly [0.17, 0.77]. No
null model is stated: if a proposer picking uniformly among ~3 plausible template shapes
would land on-prediction ~33% of the time, 5/11 is not distinguishable from that null. State
the null explicitly, give the CI, and soften the conclusion.

(d) **The decisive missing analysis, and it is cheap.** For every valid sample in the corpus,
back out the *empirical* k (and (p, q) in the rectangle) from the emitted radii and layout,
and tabulate the distribution of empirical k against round/floor/ceil/argmax predictions
across the whole sample — not the binary on-prediction indicator. Right now the reader cannot
tell whether the 6 off-prediction rectangle samples and the 5 off-prediction square samples
were floor-consistent, ceil-consistent, or unstructured. If the misses cluster on floor(√N),
the rule is wrong and the paper would know it. If they are unstructured, the rule survives
much more convincingly than 18/23 does. This single table is the difference between "the rule
fits at the tested N" and "the model applies the rule," and it is computable from data already
on disk.

### [MAJOR-10] Four preregistered tests, one significant at p = 0.0325, reported as "confirmed" without multiplicity correction

§5 registers P-T1 through P-T4 and reports P-T1 not confirmed (p = 0.30), P-T2 not confirmed
(p = 0.48), P-T3 confirmed (p = 0.0325), P-T4 confirmed against a fixed 90% threshold. The
abstract elevates P-T3 to a headline. With four preregistered hypotheses of which three are
tested for significance, Holm at the smallest p requires 0.05/3 = 0.0167 (Bonferroni across
all four: 0.0125). **p = 0.0325 does not survive either.** Preregistration fixes the
hypothesis set; it does not exempt a family of tests from multiplicity, and the fact that the
family is preregistered is precisely what makes the correction computable and mandatory.

This does not mean the effect is absent — 46/53 vs 35/50 is a plausible real effect — but the
word "confirmed," the abstract's "(87% vs 70% on-prediction, p = 0.033)," and Contribution 3's
"measurably concentrates" all need to become "nominally significant, uncorrected for the
registered family of four; not significant under Holm correction." Given the paper's whole
methodological pitch is preregistration rigor, getting multiplicity wrong is more damaging
here than it would be in an ordinary paper.

### [MAJOR-11] The bare arm mixes collection windows and reuses samples across sections; the P-T3 comparison is confounded and the §4/§5 denominators are non-independent

Reconstructing the invocation bookkeeping from the text: §5 says the scaled arm ran **100 new
invocations**, "bringing both arms to 20 samples per cell" at three cells — i.e. 60 bare + 60
trace_v2 = 120. The pilot (20) is explicitly excluded from pooling. So 20 of the 60 bare
samples are **pre-existing** and can only be arm-F bare samples at N = 13/21/31. That has
three consequences the paper never states:

(a) **The bare arm is a mixture of two collection windows; trace_v2 is a single window.**
The paper's own companion paper (§8) treats runtime nondeterminism as a first-class object,
and §3.1 discloses that decoding parameters are unpinned and that the subagent inherits
instruction files outside the prompt. Under the authors' own model of their runtime, an
old-plus-new bare arm versus an all-new trace arm is a live alternative explanation for the
87%-vs-70% gap that has nothing to do with the METHOD: line. This must be addressed — at
minimum by reporting P-T3 restricted to the 40 same-window bare samples.

(b) **§3.2, §4 and §5 report overlapping samples under different denominators without saying
so.** §3.2 gives 18/23 on-prediction at four discriminating cells; §4 gives 12/16 at three
cells; §5 gives 35/50 at the same three cells. If the 16 are inside the 50, the paper has
three different "on-prediction rate" figures for nested subsets of the same data, and a reader
comparing 75% (§4) with 70% (§5) has no way to know they are not independent estimates.
Publish a single invocation ledger: one row per invocation with cell, arm, tier, collection
date, prompt hash, valid/invalid, emitted value, classified structure.

(c) The stated corpus total of "215 logged invocations" does not reconcile against the
component counts given elsewhere (45 Haiku bare + 30 Sonnet + 30 opus_alias + 100 new + 20
pilot + 16 rectangle). Whatever the correct accounting, it should be derivable from the text.

### [MAJOR-12] The preregistered prompt hash does not cover the model's actual input

§3.1 discloses, to its credit, that "the subagent inherits instruction files outside the task
prompt." The consequence is not drawn: the SHA-256 digests lock a *substring* of the model's
conditioning context, not the context. The abstract says "We preregistered these predictions
with cryptographic prompt hashes before sampling," which a reader will take to mean the input
was cryptographically pinned. It was not.

This is materially risky here, not merely pedantic, because (i) inherited instruction files
can be long and opinionated and could plausibly bias toward or against structured/grid
answers, (ii) they are not reported, so a replicator cannot reconstruct them, and (iii) they
may have changed between the arm-F window and the arm-T window, which is the confound in
[MAJOR-11a]. Minimum fix: hash and publish the *full* resolved context for at least one
invocation per arm, state whether the inherited files changed across windows, and soften the
abstract to "prompt-fragment hashes" or equivalent.

### [MAJOR-13] The opus_alias arm shows signatures of not having run as intended, yet its number is in the abstract

§4 reports, as caveats: completion times of 2.8–9 s against 75–250 s (Haiku) and 150–1170 s
(Sonnet), and a **uniform** reported token count of 49,906 across the first 20 completions,
"≈49.9k" thereafter, described as "consistent, not intermittent." An identical token count
across 20 stochastic completions is not a serving-path curiosity; it is a strong signal that
the reported metadata is not per-completion, or that the arm hit a cache, a router fallback,
or a context-truncation path. Combined with a 1–2 order-of-magnitude latency drop, the most
economical explanation is that this arm did not exercise the model it was addressed to.

The paper's own working notes (visible in a retained HTML comment at §4) record that an
earlier decision excluded this arm from the tier ladder and a later one included it. I would
resolve it the other way: **report the arm as a diagnostic anomaly in an appendix, and remove
13% from the abstract.** "(71% → 100% → 13%)" as a headline number, when the 13% comes from an
arm the authors themselves cannot attribute to a model, is the weakest sentence in the
abstract. The tier-inversion story does not need it: 71% → 100% with a qualitative shift from
truncation to perturbed multi-radius hybrids is already a publishable contrast.

### [MAJOR-14] "The worst-in-zone penalty ... hits exactly zero at the top of each zone" is false at N = 24

§2.4: "The worst-in-zone penalty falls as N grows — 8.51% at N = 13, 7.03% at 21, 6.01% at
31, 5.25% at 43, 4.66% at 57 — and hits exactly zero at the top of each zone (N = 35, 48),
where truncation happens to *be* the recipe optimum."

Check the k = 5 zone, whose top is N = 24. The rule truncates: T(5, 24) = 24/10 = **2.4000000**.
The family alternative is a 4×4 grid plus 8 fillers, m = 8 ≤ (4−1)² = 9, giving
V(4, 8) = 2 + 8(√2−1)/8 = **2.4142136**. The family is better by 0.0142136, a residual penalty
of **0.59%** — not zero. (The claim does hold at N = 15: T(4,15) = 1.875 > V(3,4) = 1.7761424,
since m = 6 exceeds the cap (k−1)² = 4. And it holds at N = 35 and N = 48 as stated.)

Your own Figure 1 agrees with me and against the text: the green recipe-family-best curve sits
strictly above the blue prediction across the entire [21, 24] band, while it closes to the blue
at the right edge of [31, 35] and [43, 48]. In a paper whose entire credibility rests on exact
arithmetic verified against an LP, an incorrect universal quantifier in the closed-form
discussion is disproportionately costly. The fix is one clause ("at the top of the k = 4, 6
and 7 zones"), but it must be made, and the Figure 1 caption ("Mark N = 35 and N = 48, where
the gap closes to zero") should say why N = 24 does not.

### [MAJOR-15] The 93% faithfulness figure is confounded by the paper's own §5 result

§6's contribution is that faithfulness can be *measured* rather than inferred, because the
emitted coordinates are ground truth for what was built. The setup is genuinely nice. But the
statistic is computed on the trace arm — the arm §5 has just shown concentrates 87% of valid
outputs onto a single template. A model that emits the same nameable object almost every time
and names it correctly is not demonstrating faithfulness in any interesting sense; correct
description of a near-degenerate output distribution is close to free. Faithfulness is
informative precisely on the **off-template** outputs, where the model built something unusual
and had to describe it — and the paper reports one such case anecdotally (the
triangular-hexagonal 6+5+4+3+2+1 sample, which is exactly the informative kind).

Report faithfulness split two ways: on-prediction samples versus off-prediction samples. The
off-prediction n will be small (~7 by my reading of 46/53), and if it holds up there the claim
is much stronger than 93% pooled. If it does not, the paper needs to say so. As it stands, §6
and §5 are measuring partly the same thing and the paper presents them as independent results.

---

## MINOR

### [MINOR-1] "Mutation Without Variation" statistics misquoted

§7.2 says the paper finds "87% of chains and 93% of mutations revisit prior form." The source
(2606.05408, Gurkan, Stonedahl & Wilensky — title, authors and numbers verified) states: "in
87% of chains, over 93% of mutations revisit a previously seen structural form." The two
figures are nested, not parallel: it is not that 87% of chains revisit, but that within 87% of
chains, >93% of mutations do. Restate.

### [MINOR-2] FunSearch is Nature 2024, not 2023

Cited twice (§1, §7.1) as "Romera-Paredes et al., *Nature* 2023." The paper is Nature 625
(7995), 468–475, **2024** (online December 2023). Use the volume/year of record.

### [MINOR-3] Language Model Crossover venue year

§7.1 gives "Meyerson et al., ACM TELO 2023." The arXiv preprint is 2023; the ACM TELO
publication is 2024. Give both or use the journal year consistently with how FunSearch is
cited.

### [MINOR-4] "EvoDiverse (2606.10587)" — the name does not appear in the source

2606.10587 is "Towards Diverse Scientific Hypothesis Search with Large Language Models" (Wang,
Shojaee, Meidani et al.). The abstract refers to the method with an unrendered LaTeX macro and
gives no name matching "EvoDiverse." Verify the method name or cite by title.

### [MINOR-5] 2604.19440 mischaracterized

§7.2 groups "What Makes an LLM a Good Optimizer" with work that "question[s] whether the model
contributes search or retrieval." Its actual finding (verified) is that strong LLM optimizers
act as *local refiners* producing consistent incremental improvement, and that solution
novelty does not predict final performance. That is a characterization of *how* the model
contributes, arguably supportive of the proposer's role — and its "local refiner" finding is
directly relevant to [MAJOR-1], since a local refiner is exactly what a parent-conditioned
call would be. Recite and, better, use.

### [MINOR-6] Project Ariadne: Ariadne Score and Causal Sensitivity are conflated

§7.4 says interventions are "quantified by the Ariadne Score, a measure of Causal
Sensitivity." In 2601.02314 these are distinct constructs: Causal Sensitivity (φ) is the
per-intervention measure of terminal-answer movement; the Ariadne Score is proposed as a
benchmark for aligning stated logic with model action; a third quantity, violation density
(ρ), carries the decoupling result. Separate them.

### [MINOR-7] HindsightBench "under SHA-256" is unsupported

§1 and §7.5 say HindsightBench (2607.18867) "freezes directional aggregate hypotheses under
SHA-256." The paper (Haozhe Jia) describes releasing "frozen preregistrations" but I found no
statement that hashing is SHA-256 or cryptographic at all. Since the paper's own
differentiator is *what* is locked relative to this work, the comparison needs to be accurate.

### [MINOR-8] 2607.07184 "files OSF preregistrations" is unsupported

The paper is "Predicting LLM Safety Before Release by Simulating Deployment" and describes
"registered, outcome-blinded predictions"; I found no mention of OSF. Drop the platform claim
or cite where it is stated.

### [MINOR-9] 2505.15392 is general anchoring, not numeric anchoring

§1 and §7.2 use it to support "irrelevant numeric primes dragging model point estimates" and
"in all three the anchor is a scalar." 2505.15392 is "Understanding the Anchoring Effect of
LLM with Synthetic Data: Existence, Mechanism, and Potential Mitigations," which treats
anchoring as a general cognitive bias over initial information, not specifically numeric. The
paper's modality contrast (scalar anchor vs construction-template anchor) is a good one and
does not need this citation over-specified to work.

### [MINOR-10] ThetaEvolve is not "in the same band"

ThetaEvolve's claim (verified) is *new best-known bounds* on circle packing achieved by an 8B
open-source model under test-time learning. Placing it "in the same band" as 2.636 both
misstates its result and removes the strongest counterexample to the paper's "the benchmark is
saturated at the reporting precision these papers use" claim. If the number is still moving,
say so; the saturation argument can be made on the AlphaEvolve→ShinkaEvolve→HELIX cluster
without it.

### [MINOR-11] HELIX's value is below ShinkaEvolve's and the ordering is unremarked

2.63598308 (HELIX) < 2.635983283 (ShinkaEvolve), yet HELIX's abstract describes its result as
state-of-the-art. Reporting both without comment inside a "the spread is smaller than the
architectural differences" argument invites the reader to check, and the check is unflattering
to the argument. One clause resolves it.

### [MINOR-12] Figure 1 does not match its own caption

The caption specifies: worst-in-zone percentages labeled on each band (8.51%, 7.03%, 6.01%,
5.25%), and marks at N = 35 and N = 48. The rendered figure has **neither**. It also shades a
fifth band at [57, 60] that the caption does not list, and plots a "published best known"
curve — the caption never mentions this curve, and it silently terminates near N = 30 with no
explanation. Reconcile figure and caption, and put the sweep-clipping note about [57, 63] vs
[57, 60] in the caption (it currently exists only as an internal HTML comment).

### [MINOR-13] Figures 2 and 3 are never referenced or captioned

`fig2_packings.png` (three-panel Haiku/Sonnet/opus_alias comparison) and `fig3_armT.png`
(bare vs trace_v2 bars) exist and are informative — fig2 in particular is the best single
argument for the "three attractor families" framing, and fig3 carries the only reported
pooled validity percentages (83% vs 88%). Neither appears anywhere in the draft. Add
`[FIGURE 2]` and `[FIGURE 3]` blocks with captions and in-text callouts.

### [MINOR-14] P5 (N = 35) is called confirmed on n = 4

"three of four valid samples landed there" is reported as confirming a registered prediction.
n = 4 supports "consistent with" at best. The control's logic is good — a top-of-zone cell
where truncation and family optimum coincide, separable only structurally — so it is worth
running to n = 20 rather than defending at n = 4.

### [MINOR-15] Data-exclusion reporting for the concurrency-cap rejections

§3.2 excludes five invocations rejected "before reaching a model." The decision is defensible
and disclosed, which is good. Two fixes: report the table both ways (with and without), since
the exclusion was not preregistered; and disambiguate "would have understated validity by
17%" — percentage points or relative? At 32/45 = 71%, 32/50 = 64%, which is 7 points or ~10%
relative; neither is 17%, so the sentence's basis is unclear.

### [MINOR-16] "94 of 95 valid coordinate-space proposals" is sourced to unreported prior arms

This figure (§2.2) is the sole evidence for the claim that the recipe family covers essentially
the whole valid output space, and it comes from "prior arms" not reported in this paper. Either
include those arms in the ledger or restate the claim from data in this paper (§4's "no Haiku
sample [left the family] in 101 invocations" is closer to self-contained, though that
denominator is invocations while the other is valid proposals).

### [MINOR-17] The trace_v2 diff is not purely a method-line manipulation

§5 describes trace_v2 as "one inserted `METHOD:` line and three words prepended to the output
line." The three prepended words are a change to the *output-format* line — and §7.4 cites
"The Price of Format" (2505.18949, verified: format constraints collapse generation diversity)
as the closest cousin. The paper thus commits, in miniature, the confound it cites. Either
run a third arm isolating the method line with the output line untouched, or state explicitly
that the measured effect is method-line-plus-three-words and cannot be attributed to the
method line alone. Given the pilot was already discarded for exactly this reason
(method-line-plus-rewording, bundled), the standard the paper set for itself should apply here.

### [MINOR-18] The "code channel delegates to an optimizer" claim has no data

§2.1's justification for the code-free design is asserted, not measured, and it is load-bearing
for [MAJOR-1]. A ten-invocation arm with the code channel enabled, reporting how many
completions call an optimizer versus emit a hand-constructed layout, would cost almost nothing
and would either support the design choice or reveal that the in-loop channel behaves
differently in a way the paper needs to know about.

### [MINOR-19] The QD implication in §5 never reaches the one in-scope system that instantiates it

§5 and §7.5 argue that descriptor-driven quality-diversity pipelines obtaining behavioral
descriptors by self-report are measuring a perturbed distribution, and cite QDAIF (2310.13032).
GigaEvo (2511.17592) — already cited for a score — explicitly runs "MAP-Elites
quality-diversity algorithms" with "LLM-driven mutation operators with insight generation."
That is the concrete, current, in-scope system where the §5 claim bites hardest, and it is a
GECCO-audience system. Connect them.

### [MINOR-20] OpenEvolve is absent

The open-source AlphaEvolve reproduction that most practitioners actually run reports its own
circle-packing figure (~2.635977) on this benchmark and is the artifact a GECCO reader is most
likely to have used. Its absence from a related-work section built around the circle-packing
scoreboard is conspicuous.

### [MINOR-21] "Monotone inversion" is not what the data show

Contribution 2 says "a monotone inversion: constructive ambition rises with nominal tier while
execution validity collapses," and the abstract gives "71% → 100% → 13%." §4 itself says
validity "does not" rise monotonically. Ambition is (claimed) monotone; validity is
non-monotone — it rises then collapses. Drop "monotone," or apply it only to the ambition axis.

### [MINOR-22] Contribution 1's novelty claim needs a tighter boundary

"To our knowledge no prior work predicts a specific multi-decimal model output from problem
parameters ahead of sampling." Kaplan et al. and Chinchilla — cited two sections later —
publish functional forms that predict multi-decimal loss values ahead of the run, and
2411.16035 preregisters a threshold. The defensible distinction is *individual emitted output
value* versus *aggregate performance metric*, and the sentence should make that distinction
rather than rely on the reader supplying it.

### [MINOR-23] Tables 1–3 are unrendered

Table 1's numbers are at least recoverable from its caption. Tables 2 and 3 specify columns
and sources but contain no values, so §4's tier ladder and §5's paired grid cannot be checked
by a reviewer. For any real submission these must be rendered; several of the findings above
(notably [MAJOR-11]) would be resolved or refuted by Table 2 and Table 3 existing.

---

## NIT

### [NIT-1] Working comments still in the draft

`<!-- CONFLICT: ... -->` (§4 opus_alias inclusion, §5 p-value rounding), `<!-- VERIFIED ... -->`
(§3.3 recount, §4 slack recomputation), `<!-- NOTE (not a conflict) ... -->` (§2.4) and the
`<!-- Numbers sourced from ... -->` block at §2 all reference internal state files and must be
stripped. Note that two of them are load-bearing for the paper (the k = 8 clipping caveat, the
p-value convention) and should be promoted into the text rather than deleted.

### [NIT-2] The merge-provenance header must go

The block at the top ("Merged 2026-08-01 from `paper1_abstract.md`, ...") is authoring
metadata.

### [NIT-3] p = 0.033 vs p = 0.0325

Abstract and Contribution 3 give 0.033; §5 gives 0.0325. Pick one and use it everywhere
(0.0325 in the abstract, since three significant figures cost nothing and the number is
borderline — see [MAJOR-10]).

### [NIT-4] The "exactly zero slack at tolerance zero" claim deserves one sentence of explanation

§4's Sonnet N = 31 sample is reported with "minimum pairwise slack and minimum wall slack ...
both exactly zero at tolerance zero" while the emitted sum is 2.7499999991, i.e. the radii are
truncated decimals. §3.1 argues at length that an eight-decimal tangency misses contact by
~5e-9, which is why 1e-6 is the primary tolerance. A reader will notice the tension. The
resolution is presumably that the exactly-tangent pair involves the binary-exact r = 1/8
circles while the r = 1/12 circles carry positive slack — say so, and name which pair achieves
zero.

### [NIT-5] §2.1's forward reference points at nothing

"published best-known lower bounds exist for small N (see §7.1)" — §7.1 contains no bounds,
no table, and no source. See [MAJOR-3b].

### [NIT-6] Trap zone [57,60] appears in the abstract and §1 without the clipping caveat

The formula gives [57, 63]; [57, 60] is the sweep-clipped version. Currently explained only in
a stripped HTML comment. One parenthetical in §1 fixes it.

### [NIT-7] "Recipe family" vs "template" vs "attractor" are used interchangeably

Three terms for what appear to be two distinct objects (the parametric family; the specific
member the model lands on). Fix the vocabulary once in §2.2 and use it consistently — it
matters in §3.3 and §4 where "the recipe is an attractor, not a ceiling" appears twice with
slightly different meanings.

---

## Reviewer answers to the four framed questions

**(1) Does the paper fairly represent the evolve-system literature?** Partially. The lineage
(LMX → ELM → EvoPrompt → LLaMEA → FunSearch → AlphaEvolve) is correctly identified and the
critique attribution in §7.1 (Gideoni/Risi/Gal on simple baselines, 2602.16805 — verified;
Berthold et al. on classical global solvers, 2605.04850 — verified) is careful and explicitly
disambiguated, which I appreciated. But the scoreboard paragraph misrepresents the record in
the paper's own favour ([MAJOR-3]), includes a system that does not run the benchmark
([MAJOR-4]), flattens ThetaEvolve's new-bound claim into "the same band" ([MINOR-10]), leaves
the two most important systems unidentified ([MAJOR-3c]), and files a pro-loop result under
skepticism ([MAJOR-7]). Individually these are fixable; collectively they all lean the same
direction, which a GECCO reviewer will read as motivated. Fix them together.

**(2) Is the "proposal distribution these loops sample from" implication earned?** No — see
[MAJOR-1] for the precise statement of the gap and the exact list of what survives it. Short
version: the paper measures the *generation-0, parent-free, code-free* proposal distribution;
the loops sample a *parent-conditioned, code-channel, feedback-conditioned* distribution at
t > 0. The claim that survives without new experiments is about unconditioned calls —
initialization, restart, island reseed — which is a real and useful claim for this audience and
should become the framing. The claim that requires the one-parent mutation arm is anything
about what the loop samples from during evolution.

**(3) Is k\* = round(√N) distinguished from "the rule happens to fit at three trap N"?** Not
yet, and the paper is closer to the second reading than it thinks — but for a different reason
than the reviewer question supposes. The rule is not underdetermined by the data so much as
under-contentful given the family ([MAJOR-8]): "nearest square lattice" implies round(√N)
definitionally, and two natural formalizations of "nearest" coincide on the integers. The
empirical content is the truncate-vs-drop-and-fill branch, which *is* well supported at four
values of k in the square. To move from "fits" to "the model applies it," the paper needs
(a) empirical-k back-out on every valid sample rather than a binary on-prediction indicator,
(b) the untested k = 8 zone at N = 57, and (c) a stated null for the rectangle's 5/11
([MAJOR-9]).

**(4) Venue.** See below.

---

## Venue verdict

**GECCO LLM-EC workshop — first choice, conditional on rescoping. TMLR as the destination for
the expanded version. ALIFE 2026 is the wrong room.**

*Why GECCO's LLM-EC workshop.* The audience is exactly the population that builds and runs the
systems in §7.1, and the finding they can act on — that the unconditioned proposal step is a
template lookup whose value is computable in advance, so seeding/restart/reseed is far less
diverse than assumed — is directly actionable for them (seed diversification, forced-k
initialization, trap-N avoidance in benchmark selection). Workshop scope tolerates a
single-benchmark, single-vendor characterization result and treats negative results as
first-class, which suits §3.4 and §5. The closed form plus preregistered exact-value point
predictions is a genuinely novel artifact in that room. Length is the main constraint: at
workshop page limits the paper must choose, and it should keep §2–§3 (the closed form and the
out-of-sample test), compress §4 to the Haiku/Sonnet contrast with the opus_alias arm demoted
to an appendix anomaly ([MAJOR-13]), and either keep §5 or §6 but probably not both, since §6's
statistic is confounded by §5 ([MAJOR-15]).

*Why not ALIFE 2026.* There is no artificial-life content: no population dynamics, no
open-endedness measurement, no novelty search, no ecology, no agent interaction. The word
"attractor" is used metaphorically. An ALIFE audience would ask what is alive about a
single-call behavioral probe, and the answer would be nothing. The open-endedness community
would engage with an in-loop version of this work — which is another argument for running the
mutation arm — but not with the current design.

*Why TMLR is the right eventual home, not the right immediate one.* TMLR's criterion is
"are the claims supported by the evidence," with no novelty bar, unlimited length for the
preregistration and LP-verification material, and reviewers who will reward keeping §3.4. That
is a good match for this paper's virtues. But TMLR reviewers will apply exactly the pressure in
[MAJOR-1], [MAJOR-2] and [MAJOR-10] without the tolerance a workshop extends, and the paper as
submitted would draw a rejection on the loop claim alone. Submit to TMLR once the one-parent
mutation arm and a second-vendor arm exist; at that point the paper is substantially stronger
than a workshop paper and TMLR is the better venue.

---

## Recommendation

**Major revision.** The measurement is sound, the arithmetic checks out, the preregistration is
real, and the central artifact is worth publishing. The paper is not currently claiming what it
measured. Required before acceptance anywhere:

1. Rescope the abstract, title framing and Contribution 1 to the zero-shot / unconditioned
   proposal distribution, and to the weak tier ([MAJOR-1], [MAJOR-2]).
2. Correct the citations: SeaEvo, 2605.29268, 2606.13603, 2605.29087, 2407.10873, the record
   inversion in §7.1, and the missing bound source ([MAJOR-3] through [MAJOR-7]).
3. Fix the N = 24 arithmetic claim ([MAJOR-14]) and reconcile Figure 1 with its caption
   ([MINOR-12]).
4. Apply multiplicity correction to the registered family and soften "confirmed"
   ([MAJOR-10]).
5. Publish the invocation ledger and disclose the arm-F/arm-T overlap and window mixing
   ([MAJOR-11]); render Tables 2 and 3 ([MINOR-23]).
6. Demote the opus_alias arm out of the abstract ([MAJOR-13]).

Strongly recommended, and what would move this from "worth publishing" to "worth citing":

7. The one-parent mutation arm ([MAJOR-1]) — the single highest-value experiment available.
8. The empirical-k back-out table and N = 57 ([MAJOR-9]).
9. Faithfulness split by on-/off-prediction ([MAJOR-15]).

---

**Finding counts: 15 MAJOR, 23 MINOR, 7 NIT (45 total).**
