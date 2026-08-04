# A Closed Form for What the Model Emits: Template Anchoring in Zero-Shot Circle Packing

*Workshop submission — 3-page compact version. Full technical report, preregistration hashes,
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
round-number baseline hits 2 of 69 valid samples. We preregistered these point predictions and
tested them out of sample on two new containers (square and rectangle), restating but never
refitting the rule. Across three nominal tiers we find an inversion: constructive ambition
rises with tier while execution validity does not (78% → 100% → 13% at the primary 10⁻⁶
tolerance; the top-tier arm ran through an unattributable serving alias, `opus_alias`, flagged
throughout). Requesting a method-naming trace line concentrates output onto the anchor (87% vs
70% on-prediction, p = 0.03 uncorrected — failing Holm over the registered family) with no
detectable validity change. Our contribution relative to a growing diversity-collapse
literature is not that collapse occurs — it is the expected default — but that its mode is
predictable in closed form *before* sampling.

## 1. Introduction and closed form

Ask a language model to place 21 circles in a unit square to maximize the sum of their radii,
and it will not search. It reaches for the nearest square grid — five by five, radius
1/(2k) — then truncates it to 21 circles, leaving four cells empty. A better construction is
one parameter away: drop to a 4×4 grid and add corner fillers of radius (√2−1)/(2k); the sum
rises. The model does neither.

The behavior is computable in advance. A k×k grid places one circle per cell center with
r_grid = 1/(2k); m fillers sit on interior grid vertices tangent to their four neighbors,
r_filler = (√2 − 1)/(2k), 0 ≤ m ≤ (k−1)². Hence V(k, m) = k/2 + m(√2 − 1)/(2k), with
k\*(N) = round(√N) the nearest-square order. When N < k\*² the model does not drop to a smaller
grid and fill it but *truncates*, giving T(k, N) = N/(2k). k\*(N) is a definition, not a
discovered law; the falsifiable content is the *branch rule* — extend-and-fill (converge,
k\*² ≤ N) versus truncate (trap, k\*² > N). Trap zones — N ∈ [13,15], [21,24], [31,35], [43,48],
[57,63] — track the signed distance N − k\*², not primality. Every value is checked against an
independent LP oracle (83 configurations, both branches, drift below 10⁻⁹).

Circle packing is the showcase benchmark of the LLM-driven discovery lineage FunSearch opened,
carried forward by AlphaEvolve, ShinkaEvolve, and successors. Those systems query
p(program | parent programs, fitness scores, evaluator feedback, generation t > 0). We query
p(coordinates | task description, no parent, no feedback, generation 0) — the *unconditioned*
call underlying a generation-0 population, an island reseed, a restart after stagnation, or a
fresh-sample-instead-of-mutate branch, all of which demonstrably exist inside the cited systems.
We do not claim to have measured the in-loop distribution. Finding this call to be a template
lookup, computable in advance, is actionable for loop builders: seed diversification, forced-k
initialization, trap-N avoidance in benchmark selection.

**Contributions.** (1) A closed form — k\*(N), V(k, m), T(k, N) — naming the modal weak-tier
output in advance, tested out of sample on a rectangle container whose rule was restated but
never refitted. (2) A tier boundary: three attractor families, ambition rising monotonically
while validity does not. (3) Trace elicitation as an *intervention*: a method line perturbs the
sampled distribution rather than merely observing it — reported with the fragility it carries,
not as a demonstrated effect.

**Non-claim guard.** This is a behavioral regularity over emitted outputs, not a claim about
mechanism inside the weights. A mechanism-free alternative, arithmetic tractability, predicts
the same observations and was not tested.

## 2. Preregistered forecast, out of sample

Prompts were pinned and SHA-256-hashed before sampling; predictions were registered with an
explicit falsifier. Validity is scored at both 10⁻⁹ and 10⁻⁶ (10⁻⁶ primary), fixed before data
collection.

**Square container, held out.** Sampling a weak-tier (Haiku-class) proposer at seven N values,
the predicted value equals the **empirical modal output at all seven tested N**:

| N | predicted | modal freq | on-prediction / valid |
|---|---|---|---|
| 13 | 1.6250000 | 10/18 | 56% |
| 17 | 2.0517767 | 3/4 | 75% |
| 21 | 2.1000000 | 12/15 | 80% |
| 31 | 2.5833333 | 13/17 | 76% |
| 35 | 2.9166667 | 3/4 | 75% |
| 37 | 3.0345178 | 3/4 | 75% |
| 43 | 3.0714286 | 6/7 | 86% |

No predictor of a single value can exceed the modal frequency, and this one attains it at all 7
cells: the residual is dispersion, not misprediction. A naive "round number" baseline hits 2 of
the same 69 valid samples. Pooled across every tier and container the on-prediction rate is
46% — higher tiers are almost never on-prediction, so the closed form is a weak-tier law.

**Out-of-sample transfer.** For a 1×a rectangle the template gains an aspect-corrected pair of
parameters (q\*, p\*, collapsing to round(√N) at a = 1), restated but never refitted. Probing two
sharpest cells in a container none had seen before (N = 19 at a = 3; N = 25 at a = 2), **5 of 11
valid proposals landed on the predicted value and 0 of 11 reached the rival argmax**: partial
out-of-sample support, not confirmation — 5/11 = 45%, Wilson 95% CI [21%, 72%], and a proposer
choosing uniformly among a few plausible template shapes would land on-prediction roughly a
third of the time, so 5/11 does not cleanly separate from that null. The closed-form value
function itself does not survive the move to rectangles; what transfers is the rule, evaluated
against an LP oracle rather than a closed expression.

## 3. The tier ladder: three attractor families

Holding prompt, container, and scoring fixed, we varied only the nominal proposer tier at the
three hardest-discriminating cells (N = 13, 21, 31). The weak tier truncates uniform grids: 35
of 45 invocations valid at 10⁻⁶ (78%), 29 of 45 at 10⁻⁹ (64%). A middle tier (Sonnet-class)
perturbs and mixes templates — enlarged edge rows, hexagonal interior rows, multi-radius
packings — valid 30/30 at 10⁻⁶ (100%), 27/30 (90%) at 10⁻⁹, but almost never on-prediction. A
third arm, addressed only through a bare serving alias with no attestable weights binding
(`opus_alias`, flagged with that caveat throughout and never referred to as any specific dated
model), attempts recursive gasket-style constructions and is valid in 4 of 30 invocations (13%)
at both tolerances, failing mostly on geometric overlap rather than numerical error. The
ladder: 78% → 100% → 13% (64% → 90% → 13% at the stricter tolerance). "Monotone" applies to
ambition only, while validity rises then collapses — a boundary condition on the main result:
the branch rule is a weak-tier law, holding at the tier furthest from what discovery-loop
proposers typically use.

## 4. Trace elicitation as an intervention

A preregistered scaled arm (100 new invocations) compared a bare prompt against a
near-minimal variant requesting a leading `METHOD:` line. Validity showed no detectable change
(53/60 trace vs 50/60 bare, p = 0.30, a failure to detect rather than evidence of no effect).
Anchor concentration met its registered directional criterion — **87% (46/53) of trace-arm
valid samples landed on the predicted construction against 70% (35/50) of bare samples** — but
this is inferentially fragile: the p-value (p = 0.0325, one-sided, uncorrected) fails the Holm
threshold (0.0167) over the registered family of three tested predictions, and the pooled gap is
driven almost entirely by one of three cells (N = 13); a post hoc comparison further shows the
bare arm's own between-wave drift is comparable in size to the effect attributed to the
manipulation. We report this finding as *met as registered*, never as a confirmed or
demonstrated effect. Method lines are independently checkable against emitted coordinates: a
blind hand-adjudication finds 54 of 56 scoreable claims (96.4%) describe the object actually
built, Wilson 95% CI [88%, 99%].

## 5. Limitations

All tiers come from a single vendor. Two preregistered cross-vendor extensions are in progress:
arm GM (gemini-2.5-flash-lite) is quota-throttled and incomplete, no output analyzed; arm GM2
(gemma-4-26b-a4b-it) completed 140/140 invocations
with a null-compliance outcome — 0 of 140 responses parseable under the registered pipeline —
ambiguous between format inability and budget truncation; a follow-up with an enlarged budget
(arm GM3) is running, cause deferred until it reports. Sampling parameters are not exposed by
the runtime, so every effect is a distributional claim over an unpinned regime. Contamination
is not probed: N = 26 is plausibly in training data, no canary-string test was run.

## 6. Related work and positioning

Collapse onto a narrow output mode under an unconditioned or weakly-conditioned LLM call is a
known default, not a novel observation: "Artificial Hivemind" (2510.22954) documents the same
homogeneity across open-ended domains at survey scale; "The Price of Format" (2505.18949) shows
format constraints collapsing generation diversity; "Mutation Without Variation" (2606.05408)
finds iterated LLM mutation loops collapsing onto previously seen templates; and "Measuring the
Gap Between Human and LLM Research Ideas" (2607.01233) reports the same collapse one level up,
in idea space. Our contribution is not that collapse occurs — it is the expected default — but
that, here, the collapsed mode's value is predictable to seven decimals *before* sampling.
Relative to AlphaEvolve/ShinkaEvolve: those systems measure what a search loop converges to
under parent conditioning, fitness feedback, and an evaluator in context; we measure the
unconditioned proposal such loops implicitly assume is diverse when reseeding, restarting, or
branching away from mutation — a different, load-bearing, quantity.

---

*Full preregistration protocol, prompt hashes, raw ledgers, the deviations table, and
reproduction scripts are available in the long version of this paper and its accompanying
repository.*
