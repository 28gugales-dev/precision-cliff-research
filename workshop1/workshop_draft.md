# A Closed Form for What the Model Emits: Template Anchoring in Zero-Shot Circle Packing

*Workshop submission — 4-page format. Full technical report, preregistration hashes,
ledgers, and deviations table available in the long version and accompanying repository.*

## Abstract

Language models are increasingly placed in the proposal role of discovery loops such as
FunSearch and AlphaEvolve, on the assumption that their outputs explore a diverse solution
space. We characterize one component of that assumption: the *unconditioned* proposal — a
single zero-shot, code-free call with no parent program, no fitness feedback, and no evaluator
in context. On a classic constructive-geometry benchmark (maximize the sum of radii of N
circles in a unit square), a weak-tier proposer does not search: it emits a grid-with-
corner-fillers template and truncates it, even when a provably better construction is one
parameter away. The behavior admits a closed form: a nearest-square order k\* = round(√N) with
a value function V(k, m) identifies the *empirical modal output* at all seven tested N, to
seven decimals. Per-sample agreement equals that modal frequency — 56–86% by cell — while a
round-number baseline hits 2 of 69 valid samples. We preregistered these point predictions with
prompt hashes before sampling and tested them out of sample on two new containers (square and
rectangle), restating but never refitting the rule. Across three nominal tiers we find an
inversion: constructive ambition rises with tier while execution validity does not (78% →
100% → 13% at the primary 10⁻⁶ tolerance; the top-tier arm ran through an unattributable
serving alias, `opus_alias`, flagged throughout). Requesting a method-naming trace line
concentrates output onto the anchor (87% vs 70% on-prediction, p = 0.03 uncorrected — failing
Holm over the registered family, carried by one of three cells) with no detectable validity
change. Our contribution relative to a growing diversity-collapse literature is not that
collapse occurs — it is the expected default — but that, in this regime, its mode is
predictable in closed form *before* sampling.

## 1. Introduction

Ask a language model to place 21 circles in a unit square to maximize the sum of their radii,
and it will not search. It reaches for the nearest square grid — five by five, radius
1/(2k) — then truncates it to 21 circles, leaving four cells empty. A better construction is
one parameter away: drop to a 4×4 grid and add corner fillers of radius (√2−1)/(2k); the sum
rises. The model does neither, on this sample or the next.

The behavior is not just observable — it is computable in advance. With k\*(N) = round(√N) as
the nearest-square order, a value function V(k, m) over grid order k and filler count m
identifies the *modal output* of the proposal distribution — the value the model emits most
often at a given N — to seven decimals, from the problem parameters alone. The rule also
predicts where the behavior costs value: when k\*² ≤ N the model extends the grid with fillers
(converge); when k\*² > N it truncates instead of dropping to k\*−1 and filling (trap). Trap
zones — N ∈ [13,15], [21,24], [31,35], [43,48], [57,63] — are a property of the branch
behavior, not of the packing problem. "Trap" names the branch, not a guaranteed value loss: at
N = 35 (and every N = k² − 1 with k ≥ 6) truncation is value-optimal within the family; the
largest losses are at N = 13, 21, 31, 43 (gaps 0.15–0.17), with a small residual at N = 24
(0.014, i.e. 0.59%).

Circle packing is the showcase benchmark of the LLM-driven discovery lineage FunSearch opened,
carried forward by AlphaEvolve, ShinkaEvolve, and successors. Those systems query
p(program | parent programs, fitness scores, evaluator feedback, archive context, generation
t > 0). We query p(coordinates | task description, no parent, no code channel, no feedback,
generation 0). These differ on four axes at once, and we do not claim to have measured the
in-loop distribution. What we characterize is the *unconditioned* call. A source
audit finds no loop stage in the cited systems that makes precisely this call — FunSearch
reseeds islands by cloning a best surviving program, ShinkaEvolve's stagnation restart re-seeds
from its archive, OpenEvolve islands copy the user seed; every in-loop call is
program-conditioned. The nearest relatives are initializations conditioned on a seed that "can
be trivial" (FunSearch) or "rudimentary" (AlphaEvolve), plus AlphaEvolve's "No evolution"
ablation. The unconditioned call is the limiting case these approach as seed information goes
to zero; finding that this limit is a template lookup, computable in advance, is actionable for
loop builders: seed diversification, forced-k initialization, trap-N avoidance in benchmark
selection. Nothing here
is a claim about what the loop samples at t > 0.

**Contributions.** (1) A closed form — k\*(N), V(k, m), T(k, N) — that names the modal weak-tier
output in advance, verified against a linear-programming oracle to within 10⁻⁹ and tested out
of sample on a rectangle container whose rule (q\* = round(√(N/a)), p\* = round(√(N·a))) was
restated but never refitted. (2) A tier boundary condition: three attractor families, with
ambition rising monotonically across tiers while validity does not. (3) Trace elicitation as an
*intervention*: requesting a method line perturbs the sampled distribution rather than merely
observing it, and we report that result with the fragility it carries, not as a demonstrated
effect.

**Non-claim guard.** Everything here is a behavioral regularity over emitted outputs. We make
no claim about mechanism inside the weights: the model *emits*, the distribution
*concentrates*, the formula *identifies the modal output*. A mechanism-free alternative
(arithmetic tractability — a grid is close to the only construction whose coordinates can be
emitted from mental arithmetic without error accumulation) predicts the same observations and
was not tested.

## 2. The recipe family and the closed form

A k×k grid places one circle per cell center with r_grid = 1/(2k); m fillers sit on interior
grid vertices tangent to their four neighbors, r_filler = (√2 − 1)/(2k), 0 ≤ m ≤ (k−1)². Hence
V(k, m) = k/2 + m(√2 − 1)/(2k). When N < k² the observed behavior is not to drop to a smaller
grid and fill it but to *truncate*: occupy N cells of the k×k lattice at unchanged radius,
giving T(k, N) = N/(2k). Every closed-form value is checked against an independent LP oracle
that knows nothing about the recipe (83 configurations, both branches, drift below 10⁻⁹).

The order rule k\*(N) = round(√N) is a *definition*, not a discovered law — two natural
formalizations of "nearest square" coincide exactly on the integers. The falsifiable content is
the *branch rule*: whether the model extends-and-fills or truncates. The governing quantity is
the signed distance N − k\*²; primality is not the variable (13, 23, 31, 43, 47, 59 trap while
11, 17, 19, 29, 37, 41, 53 converge).

## 3. Preregistered forecast, out of sample

Prompts were pinned and SHA-256-hashed before sampling; predictions were registered in advance
with an explicit falsifier. Validity is scored at both 10⁻⁹ and 10⁻⁶ (10⁻⁶ primary), fixed
before data collection.

**Square container, held out.** Sampling a weak-tier (Haiku-class) proposer at seven N values
(13, 17, 21, 31, 35, 37, 43), the predicted value equals the **empirical modal output at all
seven tested N**, and per-sample agreement equals the modal frequency to within one sample:

| N | predicted | gap to best-in-family | modal freq | on-prediction / valid |
|---|---|---|---|---|
| 13 | 1.6250000 | +0.1511 | 10/18 | 56% |
| 17 | 2.0517767 | 0 | 3/4 | 75% |
| 21 | 2.1000000 | +0.1589 | 12/15 | 80% |
| 31 | 2.5833333 | +0.1652 | 13/17 | 76% |
| 35 | 2.9166667 | 0 | 3/4 | 75% |
| 37 | 3.0345178 | 0 | 3/4 | 75% |
| 43 | 3.0714286 | +0.1702 | 6/7 | 86% |

No predictor of a single value can exceed the modal frequency, and this one attains it at 7 of
7 cells: the residual is dispersion, not misprediction. The prediction itself is categorical —
which template, and hence its computed value; the seven-decimal match verifies the
identification rather than adding evidential strength. Two baselines: a naive "the model emits
a round number" floor hits 2 of the same 69 valid samples, and the stronger null we use for
the rectangle — a proposer uniform over a few plausible template shapes, roughly one third
on-prediction — is cleared by each of the three powered cells (56%, 80%, 76% at n ≥ 15 valid).
The four cells with n ≤ 7 valid are individually underpowered (Wilson 95% CI on 3/4 spans
roughly [30%, 95%]) and count as replications of the pattern, not independent confirmations.
Pooled across every tier and container the on-prediction rate is 46%, since higher tiers are
almost never on-prediction — the closed form is a weak-tier law.

**Out-of-sample transfer.** For a 1×a rectangle the template gains an aspect-corrected pair of
parameters, q\* = round(√(N/a)) columns and p\* = round(√(N·a)) rows; at a = 1 both collapse to
round(√N) — the same rule with aspect put back, restated but never refitted, verified against
an independent LP at 213 configurations (drift below 10⁻⁹). Probing two sharpest cells in a
container none had seen before (N = 19 at a = 3; N = 25 at a = 2) with sixteen proposers, **5 of
11 valid proposals landed on the predicted value and 0 of 11 reached the rival argmax**. We
report this as partial out-of-sample support, not confirmation: 5/11 = 45%, Wilson 95% CI
[21%, 72%] — a proposer choosing uniformly among a few plausible template shapes would land
on-prediction roughly a third of the time, so 5/11 does not cleanly separate from that null. The
closed-form *value function* itself does not survive the move to rectangles (adjacent-filler
spacing constraints appear that the square case cannot reveal); what transfers is the rule,
evaluated against an LP oracle rather than a closed expression.

## 4. The tier ladder: three attractor families

Holding prompt, container, and scoring fixed, we varied only the nominal proposer tier at the
three hardest-discriminating cells (N = 13, 21, 31). The weak tier truncates uniform grids: 35
of 45 invocations valid at 10⁻⁶ (78%), 29 of 45 at 10⁻⁹ (64%). A middle tier (Sonnet-class)
perturbs and mixes templates — enlarged edge rows, hexagonal interior rows, multi-radius
packings — and is valid 30/30 at 10⁻⁶ (100%), 27/30 (90%) at 10⁻⁹, but is almost never
on-prediction. A third arm, addressed only through a bare serving alias with no attestable
weights binding (`opus_alias`, flagged with that caveat throughout and never referred to as any
specific dated model), attempts recursive gasket-style constructions and is valid in 4 of 30
invocations (13%) at both tolerances, failing mostly on geometric overlap rather than
numerical error. A post-hoc diagnostic (not preregistered; labeled as such in the repository)
finds no evidence of a tolerance artifact behind that 13% in this sample: 24 of 26 invalid samples overlap grossly
(median maximum overlap 3.3×10⁻²; radius-shrink repair costs a median 15% of sum-of-radii),
while tolerance-scale near-misses (< 2.5×10⁻⁵) occur instead in 5 of 7 geometry-scored
weak-tier failures — the exact-tangency grids, not the ambitious constructions. The ladder,
reported both with and without this arm: 78% → 100% → 13% (64% →
90% → 13% at the stricter tolerance). "Monotone" applies to ambition only — truncated template,
perturbed hybrid, recursive gasket — while validity rises then collapses. This is a boundary
condition on the main result: the branch rule is a weak-tier law, and it happens to hold at the
tier furthest from what discovery-loop proposers typically use.

## 5. Trace elicitation as an intervention

A preregistered scaled arm (100 new invocations, `arm_t_preregistration.txt`) compared a bare
prompt against a near-minimal variant requesting a leading `METHOD:` line. Evaluated exactly as
registered: validity showed no detectable change (53/60 trace vs 50/60 bare, pooled Fisher
p = 0.30 — a failure to detect, not evidence of no effect, at this sample size). Rival-value
suppression was confirmed as registered but carries no inferential weight at these counts (1/53
vs 2/50). Anchor concentration met its registered directional criterion — **87% (46/53) of
trace-arm valid samples landed on the predicted construction against 70% (35/50) of bare
samples** — but this result is inferentially fragile: the p-value (p = 0.0325, one-sided,
uncorrected) fails the Holm threshold (0.0167) over the registered family of three tested
predictions, and the pooled gap is driven almost entirely by one of three cells (N = 13); a
post hoc, non-preregistered same-wave comparison further shows the bare arm's own between-wave
drift is comparable in size to the effect attributed to the manipulation. We report this
finding as *met as registered*, never as a confirmed or demonstrated effect. Method lines are
independently checkable against emitted coordinates: a blind hand-adjudication under a
pre-frozen rubric finds 54 of 56 scoreable claims (96.4%) describe the object actually built,
Wilson 95% CI [88%, 99%].

## 6. Limitations

All tiers in the main study come from a single vendor. Two preregistered cross-vendor
extensions are in progress at submission time: arm GM (gemini-2.5-flash-lite) is
quota-throttled and incomplete, no output analyzed; arm GM2 (gemma-4-26b-a4b-it) completed
140/140 invocations with a null-compliance outcome — 0 of 140 responses were parseable under
the registered pipeline, with no confirmatory claim made in either direction. We flag one
reading the design cannot yet exclude: a 0/140 parse rate at a fixed output-token cap is also
the signature of budget truncation rather than format inability; a follow-up with an enlarged
budget (arm GM3) is running, and any characterization of the cause is deferred until it
reports. Sampling parameters (temperature, top-p, top-k) are not exposed by the runtime, so
every effect here is a distributional claim over an unpinned sampling regime. Contamination is
not probed: the canonical N = 26 cell is plausibly in training data, and no canary-string test
was run.

**Use of AI systems.** This paper studies language-model behaviour and was written with
language-model assistance. Claude models wrote the collection, scoring and analysis scripts and
drafted the prose; the referee reports came from `deepseek-v4-pro`, `deepseek-v4-flash` and Gemini
under written protocols. The human author directed the programme, approved each preregistration
before sampling, made the final inclusion, stopping and submission decisions, and is solely
responsible for the content; no language model is an author — what a reader can check is the
ordering, each preregistration commit being a git ancestor of the sampling it governs, not the
authorship of those texts, which was model-assisted like the rest of the repository. The authoring
models share a family with arms under study, so the released scripts, raw ledgers and frozen
scorer outputs, rather than the authorship, are what the claims rest on.

## 7. Related work and positioning

Collapse onto a narrow output mode under an unconditioned or weakly-conditioned LLM call is a
known default, not a novel observation: "Artificial Hivemind" (2510.22954) documents the same
homogeneity across open-ended domains at survey scale; "The Price of Format" (2505.18949) shows
format constraints collapsing generation diversity; "Mutation Without Variation" (2606.05408)
finds iterated LLM mutation loops collapsing onto previously seen structural templates; and
"Measuring the Gap Between Human and LLM Research Ideas" (2607.01233) reports the same collapse
one level up, in idea space. Against that backdrop, our contribution is not that collapse
occurs — it is the expected default — but that, in this regime, the collapsed distribution's
mode is a single object whose value is predictable to seven decimals *before* sampling, rather
than merely observed to be narrow after the fact. Relative to the AlphaEvolve/ShinkaEvolve
lineage: those systems measure what an LLM-driven *search* loop converges to under parent
conditioning, fitness feedback, and an evaluator in context. We measure the unconditioned
proposal that such loops implicitly assume is diverse when initialized from trivial seeds — a
different, and in the systems' own terms, load-bearing, quantity.

---

*Full preregistration protocol, prompt hashes, raw ledgers, the deviations table, and
reproduction scripts are available in the long version of this paper and its accompanying
repository.*
