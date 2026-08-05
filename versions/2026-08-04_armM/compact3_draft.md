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
a value function V(k, m) identifies the *empirical modal output* — which template, and hence
its computed value — at all seven tested N, stated before sampling. Per-sample agreement equals that modal frequency — 56–86% by cell — while a
round-number baseline hits 2 of 69 valid samples. We preregistered these point predictions and
tested them out of sample on two new containers (square and rectangle), restating but never
refitting the rule; on the rectangle the informative result is negative — 0 of 11 valid
samples reached the provably higher-scoring rival — while on-prediction support is partial
(5 of 11, not separable from a uniform-template null). Across three nominal tiers we find an inversion: constructive ambition
rises monotonically with tier while execution validity rises then collapses (78% → 100% → 13% at the primary 10⁻⁶
tolerance; the top-tier arm ran through an unattributable serving alias, `opus_alias`, flagged
throughout). Requesting a method-naming trace line concentrates output onto the anchor (87% vs
70% on-prediction, p = 0.03 uncorrected — failing Holm over the registered family, carried by
one of three cells and confounded with a collection-wave split of comparable size) with no
detectable validity change. A preregistered extension run after external review sharpens the
scope both ways: the branch rule's fifth k confirmed at N = 57 (modal T(8,57) = 3.5625000,
0/10 rival), while the filler branch's registered falsifier triggered 3/3 — at N = 20, 30, 41
the model moves to the (k\*+1) grid instead of extend-and-fill, so V(k, m) holds only on the
m ≤ 1 support. Our contribution relative to a growing diversity-collapse
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
[57,63] — track the signed distance N − k\*², not primality. "Trap" names the branch, not a
guaranteed value loss: at N = 35 (and every N = k² − 1 with k ≥ 6) truncation is value-optimal
within the family; the largest losses are at N = 13, 21, 31, 43 (gaps 0.15–0.17), with a small
residual at N = 24 (0.014, i.e. 0.59%). Trap and converge zones both contain primes (trap: 13,
23, 31, 43, 47, 59; converge: 11, 17, 19, 29, 37, 41, 53), which is what rules primality out as
the driver. Every value is checked against an independent LP oracle (83
configurations, both branches, drift below 10⁻⁹).

Circle packing is the showcase benchmark of the LLM-driven discovery lineage FunSearch opened,
carried forward by AlphaEvolve, ShinkaEvolve, and successors. Those systems query
p(program | parent programs, fitness scores, evaluator feedback, generation t > 0). We query
p(coordinates | task description, no parent, no feedback, generation 0) — the *unconditioned*
call. A source audit finds no loop stage in the cited systems making precisely this call —
FunSearch reseeds islands by cloning a best surviving program, ShinkaEvolve's stagnation
restart re-seeds from its archive, OpenEvolve islands copy the user seed; every in-loop call is
program-conditioned. The nearest relatives are initializations conditioned on a seed that "can
be trivial" (FunSearch) or "rudimentary" (AlphaEvolve), plus AlphaEvolve's "No evolution"
ablation; the unconditioned call is the limiting case these approach as seed information goes
to zero. We do not claim to have measured the in-loop distribution. Finding this limit to be a
template lookup, computable in advance, is actionable for loop builders: seed diversification,
forced-k initialization, trap-N avoidance in benchmark selection.

**Contributions.** (1) A closed form — k\*(N), V(k, m), T(k, N) — naming the modal weak-tier
output in advance, tested out of sample on a rectangle container whose rule was restated but
never refitted. (2) A tier boundary: three attractor families, ambition rising monotonically
while validity does not — with ambition measured, not asserted (§3). (3) Checkable
faithfulness, and trace requests as interventions: 54 of 56 scoreable method-line claims
(96.4%) describe the object actually built, while requesting the line at all perturbs the
sampled distribution — the concentration shift is reported with the fragility it carries
(§4), not as a demonstrated effect.

**Non-claim guard.** This is a behavioral regularity over emitted outputs, not a claim about
mechanism inside the weights. A mechanism-free alternative, arithmetic tractability, predicts
the same observations and was not tested.

## 2. Preregistered forecast, out of sample

Prompts were pinned and SHA-256-hashed before sampling; predictions were registered with an
explicit falsifier. Validity is scored at both 10⁻⁹ and 10⁻⁶ (10⁻⁶ primary), fixed before data
collection.

**Square container, held out.** Sampling a weak-tier (Haiku-class) proposer at seven N values,
the predicted value equals the **empirical modal output at all seven tested N**:

| N | predicted | gap to best-in-family | modal freq | on-prediction / valid |
|---|---|---|---|---|
| 13 | 1.6250000 | +0.1511 | 10/18 | 56% |
| 17 | 2.0517767 | 0 | 3/4 | 75% |
| 21 | 2.1000000 | +0.1589 | 12/15 | 80% |
| 31 | 2.5833333 | +0.1652 | 13/17 | 76% |
| 35 | 2.9166667 | 0 | 3/4 | 75% |
| 37 | 3.0345178 | 0 | 3/4 | 75% |
| 43 | 3.0714286 | +0.1702 | 6/7 | 86% |

*Figure 1 (repository asset `workshop1/figs/fig1.png`) plots the prediction against the
best-in-family value across all seven cells, with the four gap segments marked; Figure 2
(`fig2.png`) shows the tier ladder of §3.*

No predictor of a single value can exceed the modal frequency, and this one attains it at all 7
cells: the residual is dispersion, not misprediction. A post-hoc structural check (disclosed as
such; `diagnostics_kmatch.py`) backs the grid order out of each sample's dominant radius: all
50 of 50 on-prediction samples are k\*-structured, and 64 of 69 valid samples overall (93%) sit
on the k\* grid — most value misses are k\*-grid variants, not different constructions. The
prediction itself is categorical —
which template, and hence its computed value; the seven-decimal match verifies the
identification rather than adding evidential strength. Two baselines: a naive "round number"
null hits 2 of the same 69 valid samples, and the stronger null we use for the rectangle — a
proposer uniform over a few plausible template shapes, roughly one third on-prediction — is
cleared by each of the three powered cells (56%, 80%, 76% at n ≥ 15 valid). The four cells
with n ≤ 7 valid are individually underpowered (Wilson 95% CI on 3/4 spans roughly [30%, 95%])
and count as replications of the pattern, not independent confirmations. Pooled across every
tier and container the on-prediction rate is 46% (47/102 valid samples) — higher tiers are
almost never on-prediction, so the closed form is a weak-tier regularity (single-vendor so
far, §5).

**Preregistered extension (arm M).** After external review flagged that the filler branch was
supported only at m ∈ {0, 1} and that k = 8 was never sampled, we registered and ran four new
cells (n = 15 each, hashes + tie-stated falsifiers committed before sampling). Outcome, both
directions: **P-M4 confirmed** — N = 57 modal output is T(8,57) = 3.5625000 (6/10 valid on
prediction, 0/10 rival), the truncate arm's fifth confirmed k. **Falsifier F-M1 triggered
3/3** — at N = 20/30/41 (m = 4, 5, 5) the modal outputs are T(5,20) = 2.0, T(6,30) = 2.5 and
T(7,41) = 2.9285714: the model moves up to the (k\*+1) grid and truncates or exactly fills it
(20 = 5×4, 30 = 6×5) rather than extending with fillers — 1 of 36 valid converge samples
emitted the registered V(k\*, m). V(k, m) is therefore restricted to the m ≤ 1 support, and
the rectangle-factorization preference is further evidence for the untested
arithmetic-tractability alternative (§5).

**Out-of-sample transfer.** For a 1×a rectangle the template gains an aspect-corrected pair of
parameters — q\* = round(√(N/a)) rows of p\* = round(√(N·a)) columns, collapsing to round(√N)
at a = 1 — restated but never refitted. Probing two
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
at both tolerances, failing mostly on geometric overlap rather than numerical error. A
post-hoc diagnostic (not preregistered; labeled as such in the repository) finds no evidence
of a tolerance artifact behind that 13% in this sample: 24 of 26 invalid samples overlap grossly (median maximum
overlap 3.3×10⁻²; radius-shrink repair costs a median 15% of sum-of-radii), while
tolerance-scale near-misses (< 2.5×10⁻⁵) occur instead in 5 of 7 geometry-scored weak-tier
failures — the exact-tangency grids, not the ambitious constructions. The
ladder: 78% → 100% → 13% (64% → 90% → 13% at the stricter tolerance). "Monotone" applies to
ambition only, and ambition is measured rather than asserted: a disclosed post-hoc diagnostic
(`diagnostics_ambition.py`, all samples with emitted geometry, invalid included) gives median
distinct radii 1 → 2 → 3 and median off-lattice center fraction 0.08 → 0.43 → 0.95 across the
tiers, monotone on both. Validity instead rises then collapses — a boundary condition on the main result:
the branch rule is a weak-tier regularity, holding at the tier furthest from what discovery-loop
proposers typically use.

## 4. Trace elicitation as an intervention

A preregistered scaled arm (100 new invocations: 40 bare + 60 trace; 20 of the 60 analyzed
bare rows are pre-existing arm-F samples, disclosed in the preregistration) compared a bare
prompt against a near-minimal variant requesting a leading `METHOD:` line — itself a bundled
prompt-format-and-trace-request intervention. Validity showed no detectable change
(53/60 trace vs 50/60 bare, p = 0.30, a failure to detect rather than evidence of no effect).
Anchor concentration met its registered directional criterion — **87% (46/53) of trace-arm
valid samples landed on the predicted construction against 70% (35/50) of bare samples** — but
this is inferentially fragile: the p-value (p = 0.0325, one-sided, uncorrected) fails the Holm
threshold (0.0167) over the registered family of three tested predictions, and the pooled gap is
driven almost entirely by one of three cells (N = 13); a post hoc comparison further shows the
bare arm's own between-wave drift is comparable in size to the effect attributed to the
manipulation. A second registered outcome, rival-value suppression, was also met as registered
(1 of 53 valid trace samples hit the rival vs 2 of 50 bare; directional, no inferential weight
claimed). We report both findings as *met as registered*, never as confirmed or
demonstrated effects. Method lines are independently checkable against emitted coordinates: a
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
that, here, the collapsed mode is a single closed-form-computable object, stated *before* sampling.
Relative to AlphaEvolve/ShinkaEvolve: those systems measure what a search loop converges to
under parent conditioning, fitness feedback, and an evaluator in context; we measure the
unconditioned proposal such loops implicitly assume is diverse when initialized from trivial
seeds — a different, load-bearing, quantity.

---

*Full preregistration protocol, prompt hashes, raw ledgers, the deviations table, and
reproduction scripts are available in the long version of this paper and its accompanying
repository.*
