# A Closed Form for What the Model Emits: Template Anchoring in Zero-Shot Circle Packing

*(Revision 2, 2026-08-01. Implements `p4_review_stats.md`, `p4_review_reviewer2.md` and
`p4_review_gecco.md`, plus the arbitration in `p6_cruxes.md`. Every claim that changed relative
to revision 1 is itemized in Table 5 (Appendix C); the deviations table is Table 4 (Appendix B),
and the ledger correction, the review-process disclosure and the stopping rule are in §9.)*

---

## Abstract

Language models are increasingly placed in the proposal role of discovery loops such as
FunSearch and AlphaEvolve, on the assumption that their outputs explore a diverse solution
space. We characterize one component of that assumption: the *unconditioned* proposal — a
single zero-shot, code-free call with no parent program, no fitness feedback and no evaluator
in context. On a classic constructive-geometry benchmark, maximizing the sum of radii of N
circles in a unit square, a weak-tier proposer does not search. It emits a
grid-with-corner-fillers template and truncates it, even when a provably better construction is
one parameter away. The behavior admits a closed form: a nearest-square order k\* = round(√N)
with a value function V(k, m) identifies the *empirical modal output* at all seven tested N and
matches it to seven decimals. Per-sample agreement equals that modal frequency — 56–86% by
cell — while a round-number baseline hits 2 of 69 valid samples: the formula captures
everything short of sampling entropy. We preregistered these point predictions with prompt
hashes before sampling and tested them out of sample on two containers, a square and a
rectangle, for which the rule was restated but never refitted; rectangle support is partial —
5 of 11 valid samples on-prediction, not separable from a uniform-template null, though 0 of 11
reached the provably higher-scoring rival construction. Across three tiers we find three
attractor families and an inversion: constructive ambition rises monotonically with nominal
tier while execution validity does not — it rises then collapses (78% → 100% → 13% at the
primary 10⁻⁶ tolerance; the third arm is
an unattributable serving alias, reported with that caveat throughout). Trace elicitation is an
intervention rather than an observation: requesting a method line concentrates outputs onto the
anchor (87% vs 70% on-prediction, p = 0.03 uncorrected — failing Holm over the registered
family, carried by one of three cells and confounded with a collection-wave split of comparable
size), with no detectable validity change (p = 0.30,
n = 60/arm; not powered to exclude an effect of the observed size). Method lines are checkable
against emitted coordinates: 54 of 56 scoreable claims (96.4%) describe the object actually
built. Two scope conditions are load-bearing: the closed form is a weak-tier regularity,
established so far within a single vendor lineage (§8), that does not describe the two higher
tiers sampled; and it describes what an *unconditioned* call emits, not what a loop converges
to.

---

## 1. Introduction

Ask a language model to place 21 circles in a unit square so as to maximize the sum of their
radii, and it will not search. It reaches for the nearest square grid — five by five, radius
1/(2k) — then truncates it to 21 circles, leaving four cells empty and their area unclaimed.
Those cells are where the value went. A better construction is one parameter away: drop to a
four-by-four grid and add corner fillers of radius (√2−1)/(2k), and the sum rises. The model
does neither, and behaves the same way on the next sample.

The behavior can be written down. Writing k\*(N) = round(√N) for the nearest-square order, a
value function V(k, m) over grid order k and filler count m identifies the modal output of the
proposal distribution — the value the model emits most often at each N, to seven decimals, from
the problem parameters alone, before sampling. The empirical mode equals the predicted value at
all seven N tested, and per-sample agreement is bounded by the modal frequency itself, 56–86%
by cell (§3.2). The rule also predicts where the behavior costs value: when k\*² ≤ N the model
extends the grid with fillers; when k\*² > N it truncates instead of dropping to k\*−1 and
filling. These *trap zones* — N ∈ [13,15], [21,24], [31,35], [43,48], [57,63] (clipped to
[57,60] by our sweep bound) — are a property of the branch behavior, not of the packing problem.

Circle packing is the showcase benchmark of the LLM-driven discovery literature, the lineage
FunSearch (Romera-Paredes et al., *Nature* 625(7995):468–475, 2024) opened. It is the task on
which AlphaEvolve (Google DeepMind technical report, 2025) reported 2.63586276 for n = 26 and
on which later systems report a narrow band — ShinkaEvolve (Sakana AI, 2025) 2.635983283, HELIX
2.63598308 (2603.07642), GigaEvo 2.636 (2511.17592), AdaEvolve 2.636 (2602.20133) — with
ThetaEvolve (2511.23473) claiming new best-known bounds rather than matching it.

**What we measure, and what we do not.** Those systems query p(program | parent programs +
fitness scores + evaluator feedback + archive context, at generation t > 0). We query
p(coordinates | task description, no parent, no code channel, no feedback, generation 0). These
differ on four axes at once — parent conditioning, output modality, feedback, generation index
— and we do not claim to have measured the in-loop distribution. What we characterize is the
*unconditioned* call. A source audit finds no loop stage in the cited systems that makes
precisely this call: FunSearch reseeds emptied islands by cloning a best surviving program,
ShinkaEvolve's stagnation restart re-seeds from its own archive ("initial", "best" or
"archive_random"), and OpenEvolve islands copy the user-provided seed — every in-loop call is
program-conditioned. The nearest deployed relatives are initializations conditioned on a seed
that "can be trivial" (FunSearch) or "rudimentary", single-line functions returning constants
(AlphaEvolve), plus AlphaEvolve's "No evolution" ablation, which re-prompts from the same
rudimentary program throughout. The unconditioned call is the limiting case these approach as
seed information goes to zero, and finding that this limit is a template lookup, its value
computable in advance, is actionable for the people who build these loops — seed
diversification, forced-k initialization, trap-N avoidance in benchmark selection. Anything about what the loop samples at t > 0 is a
hypothesis here. The one published result bearing directly on the substitution —
"Dictionaries, Not Darwin" (2607.04108, Pan Li), reporting parent-conditioned evolution
indistinguishable from fresh independent sampling at equal budget — is warrant from equation
discovery, not geometry. §8 names the experiment that would close the gap.

Three framing commitments. Behavioral anchoring is established territory (2505.15392;
2412.06593; 2410.15413) and we inherit its vocabulary; what differs is modality — the anchor is
a *construction template*, not a number. The benchmark choice is strategic rather than novel.
Preregistration is an adopted standard rather than a contribution (2606.27687; 2607.07184;
2606.11217; 2607.00276); our twist is what is locked — exact-output point predictions from a
closed form, on a held-out container.

**Contributions.** (1) *A closed form that names the modal model output in advance.* k\*(N) with
V(k, m) and T(k, N) identify the value a weak-tier proposer emits most often at a given N,
verified against a linear-programming oracle on 83 configurations to within 10⁻⁹ and tested out
of sample on two containers, the rectangle rule restated (q\* = round(√(N/a)),
p\* = round(√(N·a))) but never refitted. Prior work publishes functional forms predicting
*aggregate* metrics ahead of a run (2001.08361; 2203.15556; 2411.16035); to our knowledge none
predicts a specific multi-decimal *individual emitted output value* ahead of sampling. The claim
is scoped to the weak tier (§5). (2) *A tier boundary condition, as three attractor families.*
Ambition rises monotonically with nominal tier; validity does not — 78% → 100% → 13% at the
primary tolerance, 64% → 90% → 13% at 10⁻⁹. The most ambitious tier attempts recursive gaskets
and mostly fails to produce a valid packing; it was addressed through a bare serving alias and
appears as `opus_alias` with that caveat everywhere. (3) *Trace elicitation as an intervention.*
Requesting a method line concentrates output onto the anchor (87% vs 70%, p = 0.0325
uncorrected) with no detectable validity change. The result is inferentially fragile — it fails
multiplicity correction and is carried by one of three cells (§6.4) — so we report it as
met-as-registered, not as a demonstrated effect. Studies collecting process descriptors *by
request* are nonetheless measuring a perturbed distribution.

**Non-claim guard.** Everything here is a behavioral regularity over emitted outputs. We make
no claim about mechanism inside the weights, and the paper uses that vocabulary throughout: the
model *emits*, the distribution *concentrates*, the formula *identifies the modal output*
(storage-and-retrieval vocabulary corrected; Table 5, item 1). §8 states the leading
mechanism-free alternative, arithmetic tractability, and records that we did not test it.

### 1.1 Trap zones

Substituting k\*(N) into the branch condition: TRAP N ∈ [k²−k+1, k²−1], CONVERGE
N ∈ [k², k²+k]. Over N = 10…60: [13,15], [21,24], [31,35], [43,48] and [57,63] clipped to
[57,60] by the sweep bound.

Inside a zone the rule generally loses value against the best construction available *within the
recipe family*. Worst-in-zone penalties fall as N grows: 8.51% at N = 13, 7.03% at 21, 6.01% at
31, 5.25% at 43, 4.66% at 57. The penalty reaches zero at N = 35, 48, 14 and 15, but **not** at
N = 24, where truncation gives T(5,24) = 2.4000000 against V(4,8) = 2.4142136, a residual 0.59%
(Table 5, item 3). Branch label and penalty are therefore not coextensive: 4 of the 22
trap-branch N in range cost nothing, so "trap" names the branch, not a guaranteed loss. Where
the penalty is zero, truncation is separable from convergence only by structure; §3.3 uses
N = 35 as that control.

Every closed-form value is recomputed over the constructed coordinates by an independent linear
program that knows nothing about the recipe; the script aborts on disagreement. 83
configurations, both branches, every k in 2…7, drift below 10⁻⁹.

Our bound table (`n_sweep_forecast.json`) covers N = 10…30 only, and its N = 26 entry, 2.63598,
*is* ShinkaEvolve's figure truncated, so the LLM-driven systems are the record on this problem
(Table 5, item 4). What survives is that the recipe family is never competitive with that
record: deficit 0.02–0.26 across N = 10…30, and 0.0946 at N = 26
(2.63598 − 2.5414214 = 0.0945586). Above N = 30 there is no bound table, so both the deficit claim and the LP
gate's "never exceeds a published bound" abort are unchecked there, covering three of five trap
zones and four of our seven square cells.

**[FIGURE 1]** *Predicted versus optimal value, N = 10…50.* (i) the rule's prediction; (ii) the
best value in the recipe family; (iii, dotted) published best-known values, terminating at
N = 30 because the bound table stops there. Shaded bands are the trap zones, the last being
[57,63] clipped by `sweep(10,60)`. Worst-in-zone penalties 8.51%, 7.03%, 6.01%, 5.25%; these are
family-internal arithmetic and exact at every N, while the published-bound comparison (curve iii)
is checkable only up to N = 30, where the bound table stops. The gap
closes to zero at N = 35 and N = 48 but **not** at N = 24, where 0.59% remains — curve (ii)
sits strictly above (i) across [21,24].

---

## 2. Task and recipe family

### 2.1 The benchmark

Maximize the sum of radii of N non-overlapping circles in the unit square. Feasibility is
decidable exactly from emitted coordinates, so proposals score with no human in the loop.

All invocations are zero-shot and code-free. The prompt (Appendix A) fixes the count, states
containment and non-overlap, forbids writing or executing code, and demands only a raw Python
list of `[x, y, r]` triples. Our reason for the code-free design is that a code channel routes
the task to a numerical optimizer, so the distribution would reflect the optimizer. That reason
is asserted, not measured — we ran no code-enabled arm (§8) — and it also means the measured
object is not the object the code-channel systems query, which is why §1 scopes the claim to
unconditioned calls.

### 2.2 The recipe family

Three terms, used consistently: the **recipe family** is the parametric set of grid-plus-filler
constructions; a **template** is one member; the **anchor** is the template the distribution
concentrates on at a given N.

A k×k grid places one circle per cell center with r_grid = 1/(2k); m fillers sit on interior
grid vertices, tangent to their four surrounding grid circles, with r_filler = (√2 − 1)/(2k),
0 ≤ m ≤ (k−1)². Hence V(k, m) = k/2 + m(√2 − 1)/(2k). When N < k² the observed behavior is not
to drop to a smaller grid and fill it but to *truncate* — lay out the k×k lattice, occupy N
cells, leave the radius unchanged — giving T(k, N) = N/(2k). These reproduce every previously
reported anchor with no fitting: V(5,1) = 2.5414214, V(5,2) = 2.5828427, V(5,0) = 2.500,
T(5,23) = 2.300, V(4,7) = 2.3624369.

The finding that 94 of 95 valid proposals in prior arms were grid-plus-filler is retained only as
motivation, since those arms are not reported here; the self-contained version is §5's
observation that across 155 weak-tier rows only two exceeded the family best, both by ~10⁻⁷.

### 2.3 The order rule is a definition; the branch rule is the hypothesis

We write k\*(N) = ⌊√N + ½⌋ = round(√N) for the nearest-square order. This is a *definition*
(Table 5, item 2). Given that the model emits some k×k grid from this family, "the nearest
square lattice" yields round(√N) by construction; and argmin_k |k² − N| switches at
N = k² + k + ½ where round(√N) switches at k² + k + ¼, so on the integers the two coincide
exactly — two formalizations of "nearest" agreeing is a symptom that no substantive hypothesis
is being selected. Scoring four candidate orders against the three fitting anchors gave
`nearest` 3/3, `floor` 2/3, `argmax` 2/3, `ceil` 1/3; under a null where each candidate matches
each anchor with probability ½, some candidate among four goes 3/3 about 40% of the time, so
this is a weakly identified discrete selection, not a zero-parameter law.

The falsifiable content is the **branch rule**: k\*² ≤ N → extend with m = N − k\*² fillers
(converge); k\*² > N → truncate the k\*-grid (trap). Nothing about "nearest" forces truncation —
a proposer with any local search would drop to k\*−1 and fill, which is why the trap zones exist
and why a higher-valued rival is reachable inside them. Truncate-versus-drop-and-fill is a
genuine dichotomy, and it is what §3 and §4 test. The governing quantity is the signed distance
N − k\*². Primality is not the variable — 13, 23, 31, 43, 47 and 59 trap while 11, 17, 19, 29,
37, 41 and 53 converge — refuting the prior work's conjecture about primes near 30 before any
model is queried.

---

## 3. Preregistered forecast, out of sample

### 3.1 Registration protocol

For each cell the prompt is pinned and its SHA-256 digest written to disk first — the N = 13
square prompt hashes to `32db485b…`. Predictions P1–P5 are registered in the header of
`arm_f_repro.py`, with standalone files for the parallel arms (`arm_s_preregistration.txt`,
`arm_o_preregistration.txt`, `arm_t_preregistration.txt`). Raw outputs are stored verbatim,
failures included; scoring is deterministic and local.

Four properties are disclosed rather than repaired. Temperature, top-p and top-k are not exposed
by the runtime. The alias-to-weights binding is a promise, not a hash. The subagent inherits
instruction files outside the task prompt, so the digests lock a *fragment* of the conditioning
context — they are prompt-fragment hashes, and a replicator cannot reconstruct the inherited
files from what we release. Finally, hash coverage is incomplete (§9).

Two scoring conventions were fixed in advance. Validity is reported at 10⁻⁹ and 10⁻⁶, both
logged, 10⁻⁶ primary: proposers print six to eight decimals, so an eight-decimal tangency misses
contact by ~5×10⁻⁹, while 10⁻⁶ sits far below the ~10⁻² gap between rival constructions. Both
tolerances appear in every validity figure below, as registered. Value matching uses a 2×10⁻³
window; §5 records where that window is too loose for the distinction it was asked to carry.

> **Reproducibility posture.** Prompt hashes were registered before sampling in the
> preregistration files for arms F, S, O and T (`arm_f_repro.py` header, `arm_s_preregistration.txt`,
> `arm_o_preregistration.txt`, `arm_t_preregistration.txt`); what is hashed is the task prompt
> only, not the harness, so the dispatch wrapper and the inherited instruction files sit outside
> the digest; what is not attestable at all is the `opus_alias` alias-to-weights binding, a vendor
> promise rather than a hash; hash-coverage gaps, the unhashed pilot prompt and the ledger
> provenance corrections are itemized in §9 and Appendix A.

### 3.2 The formula sits at the mode ceiling

An exact point prediction invites a fair objection: a per-sample hit rate well short of 100% is
not "predicting the exact output", which is what revision 1's abstract claimed (Table 5, item
7). The number should be read against the sampling entropy of the distribution, computed in
`p11_mode_baseline.json` (bare arm, 2×10⁻³ buckets). At **all seven tested N the predicted
value is the empirical modal output**, and the on-prediction rate equals the modal frequency to
within one sample:

| N | predicted | empirical mode | modal freq | on-prediction / valid | k\*-structure / valid† |
|---|---|---|---|---|---|
| 13 | 1.6250000 | 1.6250 | 10/18 | 10/18 (56%) | 17/18 |
| 17 | 2.0517767 | 2.0518 | 3/4 | 3/4 (75%) | 3/4 |
| 21 | 2.1000000 | 2.1000 | 12/15 | 12/15 (80%) | 13/15 |
| 31 | 2.5833333 | 2.5833 | 12/17 | 13/17 (76%) | 17/17 |
| 35 | 2.9166667 | 2.9167 | 3/4 | 3/4 (75%) | 3/4 |
| 37 | 3.0345178 | 3.0345 | 3/4 | 3/4 (75%) | 4/4 |
| 43 | 3.0714286 | 3.0714 | 6/7 | 6/7 (86%) | 7/7 |

† Post-hoc structural check, not preregistered, prompted by an external review of this
revision (`diagnostics_kmatch.py`): the grid order backed out of each sample's dominant radius
(k = round(1/2r)) equals k\*(N). All 50 of 50 on-prediction samples are k\*-structured — the
value match is not an accounting coincidence — and 64 of 69 valid samples overall (93%) sit on
the k\* grid, so most value misses are k\*-grid variants (perturbed radii or filler counts), not
different constructions.

No predictor of a single value can exceed the modal frequency, and this one attains it at 7 of
7 cells: the residual is dispersion, not misprediction. As a floor, a naive "the model emits a
round number" baseline hits 2 of the same 69 valid samples (3%). Two scope conditions: this is
the bare weak-tier arm — pooled across every tier and container the on-prediction rate is 46%
(47/102), because §5's higher tiers are almost never on-prediction — and "modal" is a property
of the observed sampling regime, not of a pinned decoding configuration (§8).

### 3.3 Square container

The square arm sampled Haiku-tier proposers at N = 13, 17, 21, 31, 35, 37 and 43. The rule was
fitted on N = 23/26/27 only, so every cell is out of sample. Four cells are *discriminating*:
rule and family optimum disagree, so a proposer that searched the family would return a higher
number. Across those cells (N = 13, 21, 31, 43), **18 of 23 valid invocations landed on the
predicted construction** and the rival-argmax value was reached **2 times in 23** — both at
N = 21, both the 4×4 grid plus five fillers at 2.2588835.

Those figures cover the **original 45-invocation bare arm only** (ids ≤ 5 at N = 13/31, ≤ 10 at
N = 21, all rows at N = 17/35/37/43), the corpus that existed when §3 was written. §6 later
added 40 bare rows at N = 13/21/31 under the same arm label; over the full shipped ledger the
same four cells give **41/57 on-prediction and 2/57 rival**. Both are reported. §3 and §6 are
computed on nested subsets of one arm, not on independent samples (Table 5, item 28), and
Table 1 carries the split.

That the anchor first breaks at N = 21 is suggestive — it is the bottom of a zone carrying a
7.03% penalty, so the anchor looks weak where obeying it costs — but that is a hypothesis, not
a finding. **P4** registered N = 37 as converging on 3.0345178, a prime predicted clean,
contradicting the prior work's guess; it confirmed. **P5** registered N = 35 at 2.9166667, the
top-of-zone control; three of four valid samples landed there, separable from convergence only
because the structure classifier reads radii rather than totals; the fourth used a 7×7
lattice truncated to 35 (sum 2.5), outside the rule. At n = 4 this is "consistent with" rather
than confirmed, and deserves running to n = 20.

Bookkeeping. Five invocations were rejected by the runtime's 20-subagent concurrency cap
*before reaching a model*. We excluded them under a rule that was not preregistered, so the arm
is reported both ways — 35/45 = 77.8%, or 35/50 = 70.0% had the rejections been scored as model
failures (Table 5, item 5) — and the five records appear in the ledger in no form (§9). The arm
also contains three parse failures (Table 5, item 6), and one N = 37 proposer derived
r = (√2−1)/12 correctly in prose, then transcribed 0.03571429.

---

## 4. Rectangle transfer

### 4.1 Transfer of the rule

For a 1 × a rectangle the template has two parameters: q\* = round(√(N/a)) columns across the
width, p\* = round(√(N·a)) rows across the height. At a = 1 both collapse to round(√N) — the
same rule with the aspect ratio put back, not a new rule fitted to new data, and no rectangle
model output existed when it was written. It was verified against an independent LP at 213
configurations, drift below 10⁻⁹, including a cross-domain check: at a = 1 with p = q = k the
square file's closed form must equal this file's LP. Shape mismatch grows as a leaves 1 — over
N = 10…45 the count of N whose predicted shape differs from the optimal one rises from 12 at
a = 1.0 to 23 at a = 1.5, 20 at a = 2.0 and 23 at a = 3.0.

We probed the two sharpest cells with sixteen proposers in a container none had been given
before: N = 19 at a = 3 (predicted 3.1666667, rival 3.5749194) and N = 25 at a = 2 (predicted
3.1250000, rival 3.4832492). With all sixteen scored, **5 of 11 valid proposals landed on the
predicted value and 0 of 11 reached the rival**.

We characterize all eleven here, since a referee objected that the majority were left
undescribed. On-prediction: two
at N = 19/a = 3 (3.1666666667 and 3.16666673, the latter agreeing to six decimals not seven) and
three at N = 25/a = 2 (3.125 exactly). Off-prediction at N = 25/a = 2: two samples emitted a
uniform 5×5 grid at r = 0.1 summing to 2.5000000 — the *square* rule with no aspect correction,
k = round(√25) = 5 — plus one at 3.0 and one at 3.151875. At N = 19/a = 3, **two** samples
exceeded the prediction from outside the family, 3.45 and 3.5, both below the rival (Table 5,
item 8).

We therefore report the rectangle as **partial out-of-sample support, not confirmation**:
5/11 = 45%, Wilson 95% CI [21%, 72%], and a proposer choosing uniformly among the three or so
plausible template shapes would land on-prediction about a third of the time, so 5/11 does not
separate cleanly from that null. Two qualifications: validity degrades in the tall container
(4/8 at a = 3 against 7/8 at a = 2, three of four a = 3 failures being overlaps), a separate
finding and a confound on that cell at n = 8; and the rectangle ledger carries no prompt hashes,
no run dates and no proposer fields, so the arm with the strongest transfer claim has the least
provenance (§9).

### 4.2 Negative result: the closed form does not survive the move to rectangles

The rectangle generalizes the *rule* but not the *formula*, and we keep the failure because it
is what a verification gate is for. In the square every interior vertex has four identical
neighbors, so one expression covers every filler. In a 1 × a rectangle, with half-spacings
hₓ = 1/(2q) and hᵧ = a/(2p), a filler is also capped by horizontal and vertical spacing to
*adjacent fillers*. Those constraints are inactive when hₓ = hᵧ — why the square case could not
have revealed them — and bind only when neighboring vertices are occupied, so the cap depends
on m and on which vertices a construction uses, and no expression in (p, q, m, a) reproduces
it. The LP gate caught this on the first run: at a = 1, p = 2, q = 4, m = 1 the natural
generalization `rf = min(diag, hₓ, hᵧ)` returns **1.125** against a true **1.1545085**, capping
against a neighboring filler that does not exist. We retain closed forms only where provably
exact — full grid and truncated grid — and use the LP as the value oracle for the extend branch,
so what §4.1 tests is the LP-backed prediction.

**Table 1 — Forecast versus outcome, both containers.**

| Cell | Branch | Predicted | Rival argmax | Valid / sampled | On-pred / valid | Rival |
|---|---|---|---|---|---|---|
| N=13 (sq) | truncate | 1.6250000 | 1.7761424 | 4/5 · **18/20** | 3/4 · **10/18** | 0 |
| N=17 (sq) | extend | 2.0517767 | † | 4/5 | 3/4 | † |
| N=21 (sq) | truncate | 2.1000000 | 2.2588835 | 7/10 · **15/20** | 4/7 · **12/15** | 2 |
| N=31 (sq) | truncate | 2.5833333 | 2.7485281 | 5/5 · **17/20** | 5/5 · **13/17** | 0 |
| N=35 (sq) | truncate | 2.9166667 | † | 4/5 | 3/4 | † |
| N=37 (sq) | extend | 3.0345178 | † | 4/5 | 3/4 | † |
| N=43 (sq) | truncate | 3.0714286 | 3.2416246 | 7/10 | 6/7 | 0 |
| N=19, a=3 | truncate | 3.1666667 | 3.5749194 | 4/8 | 2/4 | 0 |
| N=25, a=2 | truncate | 3.1250000 | 3.4832492 | 7/8 | 3/7 | 0 |

Plain entries are the original 45-invocation bare arm (§3.3's corpus); **bold** the same cells
over the full 85-row bare ledger after §6 added 40 rows. † marks non-discriminating cells
(prediction equals family argmax), excluded from rival denominators. Square discriminating
cells: 18/23 and 2/23 on the original corpus; 41/57 and 2/57 on the full ledger. Rectangle:
5/11 and 0/11. Sources: `arm_f_repro.py` over `arm_f_candidates_v2.jsonl`, `arm_g_rect.py` over
`arm_g_candidates.jsonl`.

---

## 5. The tier ladder: three attractor families

Holding prompt, container and scoring fixed, we varied only the nominal proposer tier across
the three cells that discriminate hardest between prediction and family optimum — N = 13, 21
and 31, each inside a trap zone. The tiers do not merely differ in success rate: they attempt
qualitatively different constructions.

**The weak tier truncates templates.** The Haiku-tier proposer produces uniform grids of radius
1/(2k) truncated to N circles, with corner fillers only when the grid underfills. Across the 45
original bare invocations spanning N ∈ {13, 17, 21, 31, 35, 37, 43}, **35 were geometrically
valid at the primary 10⁻⁶ tolerance (77.8%), 29 at 10⁻⁹ (64.4%)** — recomputed from the ledger,
correcting the headline validity figure and the inversion triple in the abstract and
Contribution 2 (Table 5, item 9). At the three discriminating cells 12 of 16 valid samples
landed on the predicted value and the rival was reached twice, both at N = 21.

**The middle tier perturbs and mixes.** The Sonnet-tier arm was preregistered in
`arm_s_preregistration.txt`, disclosing that 5 of 20 samples at N = 13/21 had been seen before
registration and that N = 31 was fully blind. It was valid 30/30 at 10⁻⁶ and 27/30 (90%) at
10⁻⁹ — so the "100%" leg is tolerance-dependent and both numbers are stated. It was almost
never on-prediction: 0/10, 0/10, 1/10 — 1/30 pooled against the weak tier's 12/16 at the same
cells. Instead of truncating a uniform grid it perturbs one, with enlarged edge rows, hexagonal
interior rows and two or three distinct radii in the same packing (29/30 multi-radius).

One Sonnet sample at N = 31 emitted 27 circles at r = 1/12 with 4 corner circles at r = 1/8,
summing to 2.7499999991 — above 2.7485281, the best the family reaches at that N. Recomputed
from its stored coordinates, the construction is tangency-tight: minimum pairwise and wall slack
both exactly zero at tolerance zero, the exactly-tangent contacts involving the binary-exact
r = 1/8 corner circles while the r = 1/12 circles carry small positive slack. It is the only
sample in the study to leave the recipe family upward.

That sample also exposes a scoring defect. At N = 31 the family rival (2.7485281) and this
out-of-family value (2.75) differ by 1.47×10⁻³, *inside* the registered 2×10⁻³ window, so the
value classifier counted the escape as a hit on the construction it exceeded. The window was
chosen for the anchor comparison, where the nearest competing value is ~0.15 away, and reused
where it does not fit. Classified by structure instead, Sonnet's rival count at N = 31 is 2/10
and pooled 5/30 (Table 5, item 10). Every categorical claim in this paper about "reached the
rival" or "left the family" is made at structure level or at 10⁻⁶, never at 2×10⁻³.

**The top tier attempts recursive constructions and fails to build them.** The third arm was
invoked through a bare tier alias. We name it `opus_alias` throughout and make no claim about
which weights served it: the runtime accepts only the bare alias and exposes no dated
identifier, so the binding is a vendor promise rather than an attestable fact. No version number
appears anywhere in this paper.

Two anomalies make that caveat load-bearing. Completion times ran 2.8–9 s across all 30
invocations against 75–250 s for Haiku and 150–1170 s for Sonnet, and the reported token count
was uniform at 49,906 across the first 20 completions, ≈49.9k thereafter — a signal of metadata
that is not per-completion, or of a cache, router-fallback or truncation path. **Neither anomaly
appears in any released artifact** — we therefore treat both as anecdotal context from an
unreleased session transcript, not as data-supported properties of the tier: the ledger has no
latency and no token field, and both
figures come from the runtime session transcript, so a referee cannot check them.

Under those caveats the arm — preregistered fully blind in `arm_o_preregistration.txt` — was
valid in 4 of 30 invocations (13%) at both tolerances. At every cell it attempted a more
ambitious construction than either other tier: quarter-circle corners at r = 0.25 with
Apollonius-style fillers at N = 13 (10/10 samples), mixed-radius 4×4-ish grids at N = 21, and a
coarse 3×3 grid at r ≈ 1/6 with border strips at N = 31 (0/10 valid). Failures are geometric
rather than numerical — edge strips at r = 0.03 placed 0.138 from an r = 1/6 grid circle needing
0.197 — and twice the arm padded to count with zero-radius circles. Valid samples score *below*
the trap they were expected to fall into (1.26–1.41 at N = 13 against 1.625). A post-hoc
diagnostic (not preregistered; labeled as such in the repository) finds no evidence of a tolerance
artifact behind the 13% in this sample: 24 of 26 invalid samples overlap grossly (median maximum overlap
3.3×10⁻²; radius-shrink repair costs a median 15% of sum-of-radii), while tolerance-scale
near-misses (< 2.5×10⁻⁵) occur instead in 5 of 7 geometry-scored weak-tier failures — the
exact-tangency grids, not the ambitious constructions.

Two decisions here were made after seeing the data and are recorded as deviations (Table 4).
P-O1, P-O2 and P-O4 are reported **not evaluable**, on the grounds that a validity collapse of
this size makes an on-prediction tier comparison uninterpretable; P-O3 is trivially satisfied on
4/4 valid samples; the registered disconfirmation — regression toward the trap — did not occur.
De-registering three of four predictions in the one arm that disconfirmed is exactly the move
preregistration exists to constrain, which is why it is tabled rather than narrated. And the arm
was initially excluded from the ladder, then included once its results were known; we follow the
later decision and report the ladder both ways — with the arm 78% → 100% → 13%, without it
78% → 100% plus the qualitative shift from truncation to perturbed multi-radius hybrids, which
is already the publishable contrast.

**Table 2 — Three-attractor ladder.**

| Tier | Cells | n | Attempted family | Valid 10⁻⁶ | Valid 10⁻⁹ | On-pred | Rival | Failure mode |
|---|---|---|---|---|---|---|---|---|
| haiku (bare) | 13,17,21,31,35,37,43 | 45 | uniform grid, truncated; fillers when underfull | 35 (78%) | 29 (64%) | 12/16 (3 matched cells) | 2 | overlap 6, outside 1, parse 3 |
| haiku, matched cells | 13,21,31 | 60 | as above | 50 (83%) | — | 35/50 | 2 | overlap 5, outside 2, parse 3 |
| sonnet | 13,21,31 | 30 | perturbed grid, hexagonal rows, 2–3 radii | 30 (100%) | 27 (90%) | 1/30 | 5 (structure) | none |
| `opus_alias` ‡ | 13,21,31 | 30 | quarter-circle corners, Apollonius fillers, coarse grid + border strips | 4 (13%) | 4 (13%) | 0/4 | 0 | overlap 24, nonpositive radius 2 |

‡ Addressed through a bare serving alias; the alias-to-weights binding is not attestable, and
this row is not a statement about any released model version. Tier denominators are not matched
— the weak tier spans seven N against three — which is why the matched-cell row is given
separately, and it is the matched comparison (83% → 100% → 13%) that should be quoted across
tiers. Sources: `arm_f_candidates_v2.jsonl`, the three preregistration files.

**[FIGURE 2]** *Three attractor families at a single cell, N = 31.* One representative packing
per tier, ledger sample id in each panel title (weak tier `bare` id 1, on-prediction truncation
2.5833333; middle tier `sonnet_bare` id 1, mixed-radius rival 2.7485281; `opus_alias` id 1,
invalid, with only the offending circles highlighted). Source: `arm_f_candidates.jsonl` via
`fig_scripts.py`, deterministic.

"Monotone" applies to one axis only (Table 5, item 11): ambition rises monotonically —
truncated template, perturbed hybrid, recursive gasket — while validity rises then collapses. At
the canonical and plausibly contaminated cell N = 26 all tiers converge on the same 2.5414
attractor; they diverge only at withheld trap cells. The branch rule of §2 is therefore a
weak-tier regularity — single-vendor evidence until a cross-vendor arm completes (§8) — and
this is a **boundary condition on the main result**, not an independent
second finding. It also cuts against §1's framing: the discovery systems cited there run
frontier or mid-tier proposers, so the tier at which our regularity holds is the tier they do not use,
while the tier closest to what they use escapes the trap in our own data.

---

## 6. Elicitation and faithfulness

This section is explicitly secondary material and the result leans negative: the registered
validity prediction fails, the concentration effect survives only as a fragile directional
finding, and the faithfulness audit checks description against artifact, not against process.

### 6.1 Design and bundling disclosure

A ten-versus-ten pilot at N = 21 compared the bare prompt against a variant asking the proposer to
name its construction on a leading `METHOD:` line: validity rose from 7/10 to 10/10 and the
higher-scoring rival disappeared, from 2 of 7 valid bare samples to 0 of 10 trace samples. Before
any scaled sample was drawn we registered four predictions and an explicit falsifier in
`arm_t_preregistration.txt` (sha256 `ab7900a8…`), disclosing that the pilot's trace prompt had
drifted from the bare template beyond the method line — it omitted the `[0,1]x[0,1]` tokens and
reworded the output-format line — so the pilot's intervention was method-line-plus-rewording,
bundled. Pilot samples are never pooled with `trace_v2`.

The scaled prompt, `trace_v2`, is itself a **bundled prompt-format-and-trace-request**
intervention, though a near-minimal diff: one inserted `METHOD:` line, plus `"After the METHOD
line, "` prepended to the output line and `"no other text"` changed to `"no other text after the
list"`. That second change is not cosmetic — §6.2 shows it doing measurable work — so the measured
effect is *method-line-plus-output-line-rewording*, not the method line alone: a weaker version of
the confound for which the pilot was discarded, held to the same standard.

The scaled arm ran 100 new invocations, bringing both arms to 20 per cell at N ∈ {13, 21, 31} and
the corpus to 215 logged square invocations (85 bare = 45 original + 40 new; 70 trace = 10 pilot +
60 trace_v2; 30 sonnet; 30 `opus_alias`), plus 16 rectangle invocations, 231 total (Table 5, item
27). One disclosure revision 1 did not carry: **20 of the 60 bare samples are pre-existing arm-F
rows** (N = 13 ids 1–5, N = 21 ids 1–10, N = 31 ids 1–5) whose results were known when P-T1–P-T3
were written; only trace_v2 is fully fresh (§6.4). Scoring used `arm_f_repro.py` unchanged with
the registered 2×10⁻³ window; the Fisher exact test comes from the hypergeometric tail in
`arm_t_analysis.py`, checked against a reference.

### 6.2 Registered outcomes

Preregistered criteria are evaluated exactly as registered, and unregistered alpha thresholds are
applied nowhere; revision 1 applied one asymmetrically (Table 5, item 12).

**P-T1, validity: NOT confirmed.** P-T1 is the one prediction that registered an alpha ("validity
≥ bare at EACH N, and pooled one-sided Fisher p < 0.05"). Direction held at all three cells, but
the pooled test gives p = 0.30: 53/60 (88%) trace_v2 against 50/60 (83%) bare, a difference whose
detection needs several hundred samples per arm at 80% power — a failure to detect, not a
demonstration of no effect (Table 5, item 13). The direction that did hold is not geometric: bare
had **3 parse failures and 7 geometric failures**, trace_v2 **0 parse and 7 geometric**, so among
parsed samples geometric validity is 50/57 (87.7%) versus 53/60 (88.3%). The P-T1 direction is
format compliance, exactly what the reworded output-format line manipulates; validity is reported
split by cause from here on.

**P-T2, rival suppression: CONFIRMED as registered** (directional, no alpha): 1 of 53 valid
trace_v2 against 2 of 50 valid bare. Counts this near zero carry no inferential weight and we
claim none (Fisher p = 0.48, carrying no decision). One trace_v2 sample at N = 31 hit the rival
2.7485281 to within 3.6×10⁻⁸ — the first weak-tier rival hit at N = 31 in any arm, and formerly
one of the scorer's mismatches (§6.5).

**P-T3, anchor concentration: met as registered (directional), inferentially fragile.** Among
valid samples, 46 of 53 trace_v2 (87%) landed on the registered prediction against 35 of 50 (70%)
bare. The p-value it never carried is 0.0325, one-sided uncorrected (§6.4).

**P-T4, faithfulness: confirmed under a corrected scorer.** The registered scorer gives 38 of 41
scoreable claims matching (93%) against a 90% threshold; blind hand-adjudication under a rubric
frozen before rescoring gives 54 of 56 (96.4%). §6.5 reports both.

**Table 3 — Paired trace grid (scaled arm only).**

| N | Arm | n | Valid (parse / geom. fail) | On-pred / valid | Rival |
|---|---|---|---|---|---|
| 13 | bare | 20 | 18 (0 / 2) | 10 (56%) | 0 |
| 13 | trace_v2 | 20 | 18 (0 / 2) | 16 (89%) | 0 |
| 21 | bare | 20 | 15 (1 / 4) | 12 (80%) | 2 |
| 21 | trace_v2 | 20 | 18 (0 / 2) | 16 (89%) | 0 |
| 31 | bare | 20 | 17 (2 / 1) | 13 (76%) | 0 |
| 31 | trace_v2 | 20 | 17 (0 / 3) | 14 (82%) | 1 |
| **pooled** | bare | 60 | 50 (3 / 7) | 35 (70%) | 2 |
| **pooled** | trace_v2 | 60 | 53 (0 / 7) | 46 (87%) | 1 |

Per-cell one-sided Fisher on on-prediction: N = 13 p = 0.030; N = 21 p = 0.41; N = 31 p = 0.50.
Pooled p = 0.0325; Holm threshold over the registered family (m = 3 tested with p-values) is
0.0167. The pilot (10 invocations at N = 21, 10/10 valid, 9/10 on-prediction) is reported
separately and never summed into any total. Regenerated by `arm_t_analysis.py` over
`arm_f_candidates_v2.jsonl`.

**[FIGURE 3]** *Bare versus `trace_v2`, by cell and pooled.* Caption caveat: the bars pool the
bare arm's two collection waves, which §6.4 shows drift materially, so the pooled bare bar is a
mixture; the same-wave comparison in §6.4 is the wave-controlled picture.

### 6.3 The registered falsifier, both readings

The registered falsifier reads: *"if trace_v2 validity **<=** bare at 2+ of 3 N, the pilot effect
was the bundled rewording, not the method-line request — reported as such, not reframed."*
Observed validity: N = 13, 18/20 both arms — **tie**; N = 21, trace_v2 18/20 against bare 15/20 —
trace higher; N = 31, 17/20 both arms — **tie**. A tie satisfies `<=`, so under the registered
wording the falsifier is **triggered at 2 of 3 N**, and we report it as triggered; the code
instead evaluated direction as `t_rate >= b_rate`, strict `<`, under which it fires at 0 of 3
cells, which is what revision 1 reported (Table 5, item 14). That convention appears nowhere in
the preregistration, was chosen at analysis time, and read the same tie favorably twice — as
"direction held" for P-T1 and as "not a falsifier cell" here.

We name the failure mode **operationalization drift between preregistration text and analysis
code**: registered prose leaves boundary behavior — ties, inclusive versus exclusive bounds,
rounding — implicit, and the scorer must choose after the data exist; the preregistration
literature (§7) discusses what is locked, not this tie-handling layer. Remedies, free before
sampling and impossible afterward: register the comparison as executable code, or state the tie
convention in the registration text. `arm_t_analysis.py` now prints both readings and names the
registered tie-inclusive one authoritative. Under that reading **the pilot's validity effect is
attributed to the bundled rewording, not to the method-line request**, as the falsifier clause
instructed; the §6.2 parse-versus-geometric split points the same way, and P-T1 fails under both
readings regardless.

### 6.4 Limits of P-T3: what the concentration result will and will not carry

P-T3 met its registered directional criterion. It is not a flagship result.

*No registered alpha.* P-T3 registered direction only; the p-value is a post-hoc addition.

*Multiplicity.* Of four registered predictions, three are reported with p-values. Holm sets the
first threshold at 0.05/3 = 0.0167; p = 0.0325 fails it, as it fails Bonferroni at any m ≥ 2 and
Benjamini–Hochberg FDR at q = 0.05. Two-sided Fisher is p = 0.0537. P-T3 is nominally significant
uncorrected and is not under family-wise error control.

*Concentration in one cell.* Per-cell tests give p = 0.030, 0.41, 0.50 (Table 3); the pooled
17-point gap is a 33-point gap at N = 13 averaged with 9- and 6-point gaps elsewhere, driven by a
*low bare rate at N = 13* (10/18 = 56%) rather than a high trace rate — the trace rate there (89%)
equals that at N = 21. Dropping N = 13, the comparison is 30/35 vs 25/32, p = 0.31.

*Wave confound.* The bare arm mixes two collection waves; trace_v2 is one. Splitting bare on the
registered id boundary, with no intervention applied to either half, on-prediction is: N = 13, 3/4
old wave vs 7/14 new; N = 21, 2/4 vs 10/11; N = 31, 5/5 vs 8/12 — the control arm's own
between-wave drift is comparable to the effect attributed to the manipulation. Restricting to one
wave, new-wave bare is 25/37 (68%) against trace_v2's 46/53 (87%), but **this stratified
comparison is post hoc, not preregistered, no confirmatory weight** — a diagnosis, not a rescue:
wave is a confound *in the registered analysis*, which cannot separate it from the manipulation.
The design fix, interleaved collection in one session, was not run.

*What we therefore claim.* A minimal method-naming request does not make the proposer better at
geometry and does not measurably change which rare constructions it reaches; in the registered
direction it concentrates output onto the anchor, but that concentration fails correction, is
carried by one cell, is confounded with collection wave, and is bundled with an output-format
rewording that demonstrably affects parse compliance. Studies collecting process descriptors *by
asking for them*, including descriptor-driven quality-diversity pipelines where the descriptor is
a requested self-report, should treat this as a reason to check, not a coefficient to apply. The
pilot also showed a *third* effect in the P-T3 direction at the same cell (trace 9/10
on-prediction against bare N = 21 at 4/7, one-sided p = 0.16), so P-T3 replicated a pilot signal
rather than testing a blind prediction — a different status, and the prereg's pilot disclosure
covered the prompt drift only (Table 5, item 15).

### 6.5 Faithfulness with ground truth

Claim and artifact sit in the same completion and the artifact is fully determined, so a method
line is checkable against the emitted coordinates. `arm_f_repro.trace_faithfulness()` matches
numeric dimensions from the method line against the emitted layout signature, returning 38 of 41
scoreable claims matching (93%) against the registered 90% threshold. Its 12 exclusions are regex
coverage gaps, not claims without numeric content (Table 5, item 16): `DIMS_RE` matched only the
literal `NxN` form and `ROWSCOLS_RE` required rows before columns, so these fell through despite
carrying explicit checkable dimensions — "Regular 3 by 4 grid with one additional circle in row
4"; "3 complete rows of 4 circles and 1 centered circle in the top row"; "rectangular grid 4-4-4-1
with uniform radius 1/8"; "Four-row grid with 4 circles in the first row and 3 in each of the
remaining"; "Rectangular grid arrangement with 5 columns and 4 rows, plus one additional circle on
top edge"; "Square grid 5 columns 4 rows with 1 additional circle at top"; "Rectangular grid six
columns by six rows radius one-twelfth with five circles removed"; "Regular 5-column by 6-row grid
plus one additional circle in the right margin"; "Rectangular grid packing with five columns and
six rows plus one additional circle". Three further exclusions — "Uniform horizontal strips with
tight row spacing", "Regular rectangular grid packing with corner circle", "Equal-radius
rectangular grid with 4 rows stacked vertically" — are closer to genuinely unscoreable. The
excluded set is enriched for non-canonical phrasings, where a mismatch is a priori *more* likely,
so the exclusion was not conservative in a known direction; worst case, had all 12 been
unfaithful, the rate would have been 38/53 = 72%.

**Blind rescore under a frozen rubric.** The rubric (`p7_faithfulness_rubric.md`) — checkable
assertions in any surface form, plus match rules including a base-grid convention for "grid plus
additions" claims and a truncation convention for "with k removed" claims — was committed to git
as `e181d2a` at 03:56:56 on 2026-08-01, **before** any rescoring run, so the freeze is checkable,
and it pre-committed the reporting rule: below 90%, P-T4 reported not confirmed, full stop, no
consolation framing. Scoring was blind — claim text and circles only, no predicted or rival
values, no running tally, no threshold and no sight of the existing 38/41 result — with tallying
afterward; all 60 labels are released verbatim in `p7_blind_labels.json`.

**Result.** Over all 60 trace_v2 rows: **54 MATCH, 2 MISMATCH, 4 UNSCOREABLE** — a corrected rate
of **54/56 = 96.4%** of scoreable claims, Wilson 95% CI [88%, 99%], passed, and on 56 scoreable
claims rather than 41. The CI's lower bound sits just below the registered threshold, so "clears
90%" is a statement about the point estimate at this n. The two mismatches share a form: row 11
claims "alternating rows of 4 and 3 circles" over observed row sizes 4,3,3,3, row 33 claims "5
rows alternating between 5 and 4 circles" over observed 5,4,4,4,4 — both *mis-descriptions of
alternation*, a repeating pattern named and built for the first period only. The original scorer's
three mismatches were three different claim forms, not one (Table 5, item 17); the filler-adds-
rows mechanism revision 1 described was real, and the rubric's base-grid convention handles it, so
all three score MATCH under hand adjudication.

**Scope, three ways.** The blind pass covers *invalid* rows too: the original 93% conditioned on
completions that produced a correct packing — the wrong conditioning, since a method line attached
to an overlapping layout is where description and artifact are likeliest to diverge — while the
blind pass scored all 60 rows including the 7 invalid ones, 4 of the 60 unscoreable. Second, the
check verifies the description against the *artifact*, not the process: the non-claim guard
applies in full, and for a model already emitting grids, "5×5 grid" matching a 5×5 grid is closer
to a self-consistency check than to the causal question the chain-of-thought literature asks (§7).
Third, the audit is confounded with the elicitation arm, computed on the arm §6.2 shows
concentrates 87% of valid outputs onto one template, where correct description is close to free;
faithfulness is informative precisely on off-template outputs, such as the pilot's
triangular-hexagonal 6+5+4+3+2+1 sample, described exactly while summing to 1.75. The split by on-
versus off-prediction is not run here (§9, stopping rule). What survives is narrow: in a domain
where claims are checkable, the method lines this proposer emits are, at 54 of 56 scoreable
claims, true of the object it produced — and both failures are a model describing a pattern it
started and did not finish.

---

## 7. Related work

Citation errors in revision 1 are corrected here and itemized in Table 5 (items 18–26).

**LLM-driven discovery and the circle-packing scoreboard.** Language Model Crossover (Meyerson
et al., arXiv 2023, ACM TELO 2024), ELM (2206.08896), EvoPrompt and LLaMEA (2405.20132)
established the LLM call as an EC operator over prompts and programs; FunSearch turned the
pattern into a discovery claim, and every system in §1's scoreboard inherits it. Two orderings
in that scoreboard matter: HELIX's figure is marginally *below* ShinkaEvolve's while being
described as state of the art, and ThetaEvolve claims new best-known bounds, so the benchmark is
saturated only across the AlphaEvolve–ShinkaEvolve–HELIX cluster and the number is still moving.
OpenEvolve, the open-source AlphaEvolve reproduction most practitioners run, reports ≈2.635977.
§1.1 records the correction to our record comparison and its N > 30 coverage gap. Two critiques
bear on our framing and are frequently conflated, so we attribute them explicitly: Gideoni, Risi
and Gal (2602.16805) show simple baselines recover much of the reported advantage, and Berthold
et al. (2605.04850) show classical solvers do too.

**Template convergence and diversity collapse.** "Mutation Without Variation" (2606.05408,
Gurkan, Stonedahl and Wilensky) finds iterated LLM program mutation collapsing onto previously
seen structural templates — in 87% of chains, over 93% of mutations revisit a previously seen
form — which is the same bias family in a different regime: mutation loops, program space, no
closed form, no preregistration. On anchoring, 2505.15392 treats anchoring as a general bias
over initial information while 2412.06593 and 2410.15413 document numeric primes dragging point
estimates; our modality is the difference, since a construction template has a computable value
where a scalar anchor has only a measurable pull. Concurrently, "Measuring the Gap Between
Human and LLM Research Ideas" (2607.01233) reports the same collapse one level up, in idea
space: across 11,683 paired proposals, LLM research ideas concentrate on bridge-and-synthesis
framings (47–64% versus 12% for humans; normalized entropy down to 0.55 versus >0.92), and
chain-of-thought pushes the distribution *further* from the human one. That result is
distributional; ours is the limiting case where the collapsed distribution's mode is a single
closed-form-predictable object — narrowness measurable there, computable here. "Artificial
Hivemind" (2510.22954) documents the same homogeneity across open-ended domains at survey
scale, which makes cross-domain generality of the collapse the expected default; against that
backdrop our contribution is not that collapse occurs but that, in this regime, its mode is
predictable to seven decimals before sampling. Converging
skepticism about what the proposer contributes comes from "Dictionaries, Not Darwin" (2607.04108), 2606.10587, BehaveSim
(2603.02787), Strategy Diversity (2605.09292), the bin-packing critiques (2510.27353;
2501.11411) and MathConstruct (2502.10197). Two results cut the other way and belong on the
other side of the ledger: 2407.10873 (Zhang et al.) provides empirical grounding for the
*importance* of evolutionary search, which is evidence against our substitution of an
unconditioned call for the loop and is engaged in §8; and 2604.19440 finds strong LLM optimizers
act as *local refiners*, which is what a parent-conditioned call would be, so it bears on §8's
mutation arm.

**Scaling inversions.** Zhou et al. (*Nature*, 2024) show larger and more instructable models
becoming less reliable; the o3/o4-mini system card shows the same on PersonQA; 2506.06941
reports collapse past a complexity threshold; GeoBuildBench (2605.13167) finds geometric
construction a regime where nominal capability and executed correctness diverge. Our
instantiation is *attractor family* versus executability.

**Trace faithfulness, and what our result is not.** One cluster intervenes *on trace content*
and finds answers do not move — Reasoning Theater (2603.05488), Project Ariadne (2601.02314),
"Beyond the Commitment Boundary" (2606.13603) and "The Chain Holds, the Answer Folds"
(2605.29087) all report causal decoupling. A second cluster *estimates* faithfulness without
observing the process, represented here by 2503.08679; §6.5 reports the case where ground truth
for the described artifact exists. Our result sits at a third intervention point: we vary
whether a trace is *requested* rather than editing its content, which is measurement reactivity,
not causal faithfulness. The closest cousin is "The Price of Format" (2505.18949), showing
format constraints collapse generation diversity — and as §6.1 concedes, our manipulation
includes a small output-format change, so we commit a miniature version of the confound we cite.
Format-restriction performance costs are documented at scale in 2408.02442. Related:
2505.14617, 2510.01171, 2506.17630.

**Preregistration lineage.** 2606.27687, 2607.07184, 2606.11217 and 2607.00276 preregister
recipes, outcome-blinded predictions and agent protocols; HindsightBench (2607.18867) releases
frozen preregistrations of directional aggregate hypotheses. We adopt the standard rather than
claim it. What we add is the object locked — exact closed-form point predictions of specific
output values — and, from §6.3, the observation that locked prose and executing scorer can
disagree at the boundary. Structural precedents: 2001.08361 and 2203.15556 publish a functional
form then run the confirming instance; 2411.16035 is the closest structural twin. QDAIF
(2310.13032) is the QD-descriptor setting most affected by our §6 result, and GigaEvo
(2511.17592) the concrete in-scope system running MAP-Elites with LLM-driven mutation, where a
self-reported behavioral descriptor would be perturbed in practice.

---

## 8. Limitations and untested alternatives

**The measured distribution is not the in-loop distribution.** We sample generation-0,
parent-free, code-free, feedback-free calls; the systems in §7 sample parent-conditioned program
proposals under selection. The claim that survives is about unconditioned calls, and 2407.10873
is published evidence that evolutionary search contributes materially, cutting against any
stronger reading. The decisive cheap experiment is a one-parent mutation arm: same cells,
prompt = bare template plus one parent packing plus its score plus "propose a modification that
increases the sum of radii", under three parent conditions (the on-prediction truncated grid,
the higher-value family rival, an off-family parent), measuring whether the branch rule still
predicts and whether the model inherits the parent's k. That is ~120 invocations and the single
highest-value addition available. It was not run.

**A mechanism-free alternative we did not test.** Under an explicit "construct the packing by
reasoning alone" constraint, a k×k grid at r = 1/(2k) is close to the only construction whose
coordinates can be emitted from mental arithmetic without error accumulation, and round(√N) is
the arithmetically nearest such grid. That hypothesis predicts every observation in §2–§3
without appeal to stored templates, and predicts §5's inversion too: the more ambitious tier
attempts constructions whose coordinates it cannot compute by hand and overlaps — precisely the
observed failure mode (24 overlaps and 2 nonpositive radii out of 26 `opus_alias` failures). The
separating experiment — hand the model the recipe family explicitly, state V(k, m) and the
admissible k, and ask it to *choose* k; if it picks the argmax, the tractability reading stands
— was not run. This is why §1's vocabulary is behavioral and why no memorization claim is made.

**Contamination is not probed.** N = 26 is the canonical published cell and plausibly in
training data. We ran no canary-string test, no comparison against N values absent from the
literature, and no perturbed-container test preserving difficulty while destroying lexical
overlap. The rectangle arm is the nearest thing we have, at n = 11 valid.

**Single vendor.** All tiers in the main study come from one provider. Two preregistered
cross-vendor extensions are in progress at submission time, both registered before sampling and
disclosed regardless of outcome. Arm GM (gemini-2.5-flash-lite, direct vendor API,
prereg commit `37b3adb`) is quota-throttled and incomplete; no collected output has been
analyzed. Arm GM2 (gemma-4-26b-a4b-it, prereg `3019aab`) completed 140/140 invocations with a
null-compliance outcome: 0 of 140 responses were parseable under the registered pipeline —
the model consumed its entire 4,096-token output budget on visible deliberation and never
emitted the required coordinate list, under a prompt with which the weak-tier arm F model
complied at 100% parse rate. Per the registered rule, all cells are UNSCOREABLE and no
confirmatory claim is made in either direction; a follow-up with an enlarged output budget
(arm GM3, registered before sampling) is running. The anchoring law therefore remains
single-vendor evidence at this time — but the format-compliance cliff between families under
an identical prompt is itself a preregistered observation, and it is consistent with §6.1's
point that output-format constraints are load-bearing. We flag one reading the design cannot
yet exclude: a 0/140 parse rate at a 4,096-token cap is also the signature of budget
truncation — a verbose model cut off before its answer — rather than format inability. Arm
GM3's enlarged budget separates the two, and we defer any characterization of the cliff's
cause until it reports.

**Sampling parameters unpinned.** The runtime does not expose pinned decoding parameters, so
every effect is a distributional claim over the observed sampling regime, and §3.2's
mode-ceiling result inherits that scope. This is the subject of the companion paper.

**`opus_alias` provenance.** The label denotes the serving alias addressed, not an identified
model version. Without pinned weights we cannot separate a model-tier effect from a serving-path
effect, and the supporting anomalies live only in the runtime transcript.

**Thin confirmatory base for the branch rule.** floor and round disagree exactly on
N ∈ [k²−k+1, k²−1], so every discriminating cell is a trap cell by construction, and our
discriminating evidence is four values of k in the square (k = 4, 5, 6, 7) plus two rectangle
cells. The k = 8 zone appears in the abstract, §1, §1.1 and Figure 1 and was never sampled;
N = 57 is the missing cell. Further, on-prediction is scored as a binary: we do not report the
*empirical* k backed out of each emitted layout, so a reader cannot tell whether off-prediction
samples are floor-consistent, ceil-consistent or unstructured. That table is computable from
data already on disk and would distinguish "the rule fits at the tested N" from "the model
applies the rule"; it is named here rather than run, per the stopping rule below.

---

## 9. Reproducibility, deviations, and disclosures

Deviations from preregistration are tabled in Appendix B; every claim that changed relative to
revision 1 is tabled in Appendix C. Provenance, in list form:

- **Registration.** Prompts were hashed with SHA-256 and the hashes recorded before sampling,
  with the predicted values they were to be tested against: `arm_f_repro.py` (header, P1–P5,
  square arm), `arm_s_preregistration.txt`, `arm_o_preregistration.txt`,
  `arm_t_preregistration.txt` (prereg hash `ab7900a8…`). The rectangle transfer was registered
  before collection and never refitted.
- **Four limits on that claim.** (i) The digests cover the task prompt only; the subagent
  inherits instruction files outside it, so what is locked is a *fragment* of the conditioning
  context, a replicator cannot reconstruct those files, and we cannot establish they were
  identical across the arm-F and arm-T windows — the boundary §6.4 identifies as a confound.
  (ii) `arm_f_prompts.json` covers N = 13, 17, 31, 35 and 37; the N = 21 bare hash is registered
  in `arm_t_preregistration.txt`; the **N = 43 bare hash appears in no preregistration and no
  prompts file**, existing only in the ledger — it recomputes exactly from the bare template, but
  recomputation after the fact is not registration. (iii) **No hash was ever registered for the
  pilot prompt**, whose drift the preregistration describes only in prose; the ten pilot rows
  carry `prompt_sha256: null` in the corrected ledger with an explanatory note. (iv) The
  rectangle ledger (`arm_g_candidates.jsonl`) carries no prompt hashes, no run dates and no
  proposer fields at all.
- **Ledger metadata correction.** Three referee findings established that the shipped ledger's
  provenance fields contradicted the paper: trace rows carried the *bare* prompt hash for their
  cell, `run_date` was uniformly `2026-07-30` on all 215 rows, and the Sonnet and `opus_alias`
  rows were stamped with the Haiku alias and dated id. All three are corrected in
  `arm_f_candidates_v2.jsonl`; the correction is metadata only — every scored quantity, geometry,
  raw output, arm label and sample id is byte-identical to v1, verified field by field, each
  corrected field carrying a sibling `*_v1` field. `arm_f_candidates.jsonl` is unmodified
  (sha256 `02ecabcd…`); v2 is `9f845f78…`. Correction rules, sources, wave-boundary arithmetic
  and caveats — including that `run_date` has day granularity only — are in
  **`ledger_v2_corrections.md`**. Analysis scripts read v2.
- **Excluded and unreleased records.** The five concurrency-cap rejections appear in the ledger
  in no form, no `excluded_reason` field exists, and the exclusion rule was not preregistered;
  both rates are reported in §3.3. The `opus_alias` latency and token-count anomalies (§5) come
  from the runtime session transcript; no latency or token field exists in any released artifact.
- **Analysis artifacts.** Raw outputs are stored verbatim (`arm_f_raw.json`,
  `arm_f_candidates.jsonl`, `arm_f_candidates_v2.jsonl`, `arm_g_candidates.jsonl`) and scoring is
  deterministic and local. Value claims are gated on an independent LP oracle rather than on the
  closed form being tested: `n_sweep_forecast.py` with `verify_against_lp` checks 83
  configurations to within 10⁻⁹, and the same oracle produced §4.2's negative result. The
  faithfulness rubric (`p7_faithfulness_rubric.md`) was frozen by git commit `e181d2a`
  (2026-08-01 03:56:56) before any rescoring, and all 60 blind labels with justifications are in
  `p7_blind_labels.json`. `arm_t_analysis.py`, `n_sweep_forecast.json`, `rect_forecast.json`,
  `p11_mode_baseline.json` and `STATE.md` are included; every table regenerates from raw outputs
  by a command documented in `HOW_TO_RUN.md`.
- **Review process.** The three referee reports that drove this revision (`p4_review_stats.md`,
  `p4_review_reviewer2.md`, `p4_review_gecco.md`), the arbitration of their conflicting
  recommendations (`p6_cruxes.md`), and the blind faithfulness adjudication of §6.5 were produced
  by language models under written protocols, not by human referees. They independently
  recomputed the paper's statistics from the released ledger and found eight recomputation
  mismatches, all itemized in Appendix C, and their arithmetic was checkable and was checked. But
  the panel is not peer review, its verdicts carry no external authority, and it shares a family
  resemblance with the system under study — a blind-spot risk disclosed here rather than left
  implicit.
- **Stopping rule.** This revision closed after implementing the three named referee reports and
  the arbitration verdict; no further data-dependent analysis was performed. Analyses named but
  not run — the one-parent mutation arm, the recipe-family choice probe, N = 57, the empirical-k
  back-out, faithfulness split by on- versus off-prediction, a code-enabled probe, interleaved
  re-collection of the arm-T pair, and P5 at n = 20 — are recorded in §6.5 and §8 as future work,
  so that the reported statistics remain the ones the preregistrations governed.

---

## Appendix A — Prompts, verbatim

**A.1 Bare template** (`{n}` parameterized; the N = 13 instance hashes to
`32db485bea625ff9f39f4723ebf1a01f337559a9e2cf567fb486928f71f7f8df`):

```
Pack exactly {n} non-overlapping circles inside the unit square [0,1]x[0,1] so that the sum of their radii is as large as possible.
MUST hold: exactly {n} circles; every circle fully inside the unit square [0,1]x[0,1] (x-r >= 0, x+r <= 1, same for y); no two circles overlap (distance between centers >= sum of the two radii; touching is allowed).
Do not write or execute code - construct the packing by reasoning alone.
Output ONLY the raw Python list of {n} [x, y, r] lists. No explanation, no code fences, no other text.
```

**A.2 `trace_v2` template** — identical to A.1 through line 3, then:

```
First write one line beginning "METHOD:" naming the construction you used. Do not use square brackets anywhere in that line.
After the METHOD line, output ONLY the raw Python list of {n} [x, y, r] lists. No explanation, no code fences, no other text after the list.
```

**A.3 Dispatch wrapper** (both arms; *not* part of the hashed task prompt, hence an instance of
the fragment-hashing limitation in §3.1): `Do not use any tools. Your entire final message must
be the answer and nothing else.`

**A.4 Registered prompt hashes.** bare N=13 `32db485b…`, N=17 `8437df75…`, N=21 `a415425b…`,
N=31 `a664d003…`, N=35 `3b08c56e…`, N=37 `2c0a8819…`; trace_v2 N=13 `a920f1c9…`, N=21
`91205727…`, N=31 `bd490b7b…`. The N=43 bare hash `1208e7d2…` is ledger-only, and the pilot
prompt was never hashed (§9).

**A.5 Parser.** Completions are parsed with `ast.literal_eval` after stripping code fences; a
completion failing to yield a list of N numeric triples is recorded `literal_eval_failed` and
scored invalid, with the failure mode logged (§6.2 reports parse and geometric failures
separately). Radii must be strictly positive; containment and pairwise non-overlap are checked
at the two registered tolerances.

---

## Appendix B — Deviations and disclosure table

**Table 4 — Deviations from preregistration.**

| Prediction | Registered rule | As registered? | Outcome / reason |
|---|---|---|---|
| P1–P3 | exact-value point predictions | yes | §3.3, Table 1 |
| P4 (N=37) | converge, 3.0345178 | yes | confirmed |
| P5 (N=35) | truncate, 2.9166667, structural separation | yes | 3/4 valid; n = 4, "consistent with" |
| P-S1…P-S4 | directional tier comparisons | yes | §5 |
| P-O1, P-O2, P-O4 | tier comparisons on on-prediction / rival rates | **no** | declared not evaluable post hoc after a 13% validity collapse; the registered disconfirmation (regression toward the trap) did not occur |
| P-O3 | multi-radius fraction ≥ 0.9 of valid | yes | trivially satisfied on 4/4 valid |
| P-T1 | direction at each N **and** pooled p < 0.05 | yes | not confirmed, p = 0.30 |
| P-T2 | directional, no alpha | yes | confirmed as registered (1/53 vs 2/50); no inferential weight claimed |
| P-T3 | directional, no alpha | yes | met as registered; p = 0.0325 uncorrected fails Holm; carried by N = 13 (§6.4) |
| P-T4 | ≥ 90% of scoreable claims match | yes, plus corrected scorer | 38/41 (93%) original; 54/56 (96.4%) blind, frozen rubric |
| Falsifier | trace_v2 validity `<=` bare at 2+ of 3 N | **both readings reported** | **triggered** under the registered tie-inclusive reading (2/3 cells); not triggered under the strict `<` the code implemented (§6.3) |
| Ladder inclusion | — | **post hoc** | `opus_alias` initially excluded, later included after results known; ladder reported both ways (§5) |
| Cap exclusion | — | **not registered** | five records excluded; both rates reported (§3.3) |

---

## Appendix C — Corrections ledger

**Table 5 — Corrections to revision 1.** Every claim that changed between the reviewed draft and
this one, with the finding that forced it. `stats` = `p4_review_stats.md`, `R2` =
`p4_review_reviewer2.md`, `GECCO` = `p4_review_gecco.md`, `council` = `p6_cruxes.md`.

| # | § | Revision-1 claim | Corrected | Source |
|---|---|---|---|---|
| 1 | Abs, 1 | "recall" a template; "template memorizer" | behavioral vocabulary only: emits / concentrates / modal output | R2 #2; R-E |
| 2 | 2.3 | round(√N) an empirical discovery; "zero free parameters" | a definition — two formalizations of "nearest" coincide on the integers; weakly identified selection among four | GECCO M8; R2 #24 |
| 3 | 1.1, F1 | penalty "hits exactly zero at the top of each zone" | zero at N = 14, 15, 35, 48; **0.59% residual at N = 24**; 4 of 22 trap N cost nothing, so branch ≠ penalty | GECCO M14; R2 #19 |
| 4 | 1.1, 7 | "published bounds sit above all of them" | withdrawn: the N = 26 bound (2.63598) *is* ShinkaEvolve's, so the LLM systems are the record; table stops at N = 30, leaving the LP abort gate unchecked above it | GECCO M3; R2 #20–21 |
| 5 | 3.3 | cap exclusions "understated validity by 17%" | 77.8% vs 70.0% — 7.8 points, 10% relative; exclusion unregistered, both rates reported | R2 #13; GECCO m15 |
| 6 | 3.3, 6 | "two parse failures"; "two fraction-literal samples" | three in each case | stats F14, F15 |
| 7 | Abs, 1, 3.2 | "predicts the exact sum-of-radii the model will emit" | predicts the **empirical modal output** at 7/7 N; per-sample rate = modal frequency, 56–86% by cell, 46% pooled; round-number baseline 2/69 | R2 #15; R-E |
| 8 | 4.1 | one a = 3 sample left the family; rectangle "confirmed" | two (3.45, 3.5); all 11 valid samples characterized; partial support, CI [21%, 72%], null stated | stats F16; R2 #17; GECCO M9c |
| 9 | Abs, 1, 5 | 32/45 = 71%; inversion 71 → 100 → 13 | **35/45 = 77.8%** at 10⁻⁶, 64.4% at 10⁻⁹; inversion 78 → 100 → 13 (64 → 90 → 13 strict); matched-cell 83 → 100 → 13 given separately | stats F1; R2 #3; R-F |
| 10 | 5 | Sonnet rival 6/30, 3/10 at N = 31 | 5/30 and 2/10 — the 2.75 escape sits 1.47×10⁻³ from the rival, inside the window; categorical claims now structural or at 10⁻⁶ | stats F12; R2 #14 |
| 11 | 1 | "a monotone inversion" | monotone in ambition only; validity rises then collapses | GECCO m21 |
| 12 | 6.2 | P-T2 "not confirmed" (p = 0.48); P-T3 "confirmed" (p = 0.0325) | one rule applied symmetrically: P-T2 **confirmed as registered** (1/53 vs 2/50, no inferential weight); P-T3 met as registered but fragile | stats F7; R-C |
| 13 | Abs, 1, 6.2 | "leaving validity unchanged" | no *detectable* change (p = 0.30, n = 60/arm, underpowered); the P-T1 direction is entirely parse compliance — 3 vs 0 parse failures, 7 vs 7 geometric | R2 #7–8 |
| 14 | 6.3 | "the registered falsifier was not triggered" | **triggered at 2 of 3 N** under the registered `<=`; not under the code's strict `<`; both reported, registered reading authoritative; pilot validity effect attributed to the bundled rewording | stats F8; R-B |
| 15 | 6.4 | pilot produced two effects, both died at scale | a third ran in the P-T3 direction at the same cell (9/10 vs 4/7, p = 0.16): P-T3 replicated a pilot signal | stats F18 |
| 16 | 6.5 | 12 claims excluded as "no numeric content" | regex coverage gaps; 9 of 12 carry checkable dimensions, quoted verbatim in §6.5; worst case 38/53 = 72% | stats F9 |
| 17 | 6.5 | the three mismatches "are all the same case" | one of three; all three score MATCH under blind adjudication; the two remaining mismatches are alternation mis-descriptions (rows 11, 33) | stats F10; R-D |
| 18 | 1, 7 | SeaEvo (2604.24372) reports a ~2.636 packing value | removed: SeaEvo does not evaluate circle packing | GECCO M4 |
| 19 | 7 | 2605.29268 reports asymmetric proposal mass in program space | deleted — that paper is on bandit compute allocation; removing it leaves no cited evidence that the anchoring survives the code channel | GECCO M5 |
| 20 | 7 | 2606.13603, 2605.29087 estimate faithfulness by perturbation / probing | both are causal-decoupling results; only 2503.08679 is an estimator | GECCO M6 |
| 21 | 7, 8 | 2407.10873 and 2604.19440 filed as loop skepticism | 2407.10873 grounds the *importance* of evolutionary search — evidence against our substitution, engaged in §8; 2604.19440 recites as "local refiner" | GECCO M7, m5 |
| 22 | 1, 7 | AlphaEvolve "2.635"; FunSearch *Nature* 2023; LMX TELO 2023; AlphaEvolve/ShinkaEvolve unidentified | 2.63586276; *Nature* 625(7995):468–475, 2024; arXiv 2023 / TELO 2024; both systems identified | GECCO M3c, m2, m3 |
| 23 | 1, 7 | ThetaEvolve "in the same band"; HELIX ordering unremarked | ThetaEvolve claims new best-known bounds; HELIX sits below ShinkaEvolve while claiming SOTA | GECCO m10, m11 |
| 24 | 7 | "EvoDiverse (2606.10587)"; 2505.15392 as numeric anchoring | cited by title, method name unverified; 2505.15392 is general anchoring | GECCO m4, m9 |
| 25 | 7 | HindsightBench freezes "under SHA-256"; 2607.07184 "files OSF preregistrations" | both unsupported by the sources; restated as frozen preregistrations and registered outcome-blinded predictions | GECCO m7, m8 |
| 26 | 7 | "Mutation Without Variation": 87% of chains and 93% of mutations | nested, not parallel: in 87% of chains, over 93% of mutations revisit a prior form | GECCO m1 |
| 27 | Abs, 6.1 | "hundreds of invocations"; corpus arithmetic unreconcilable | 231 invocations, itemized in §6.1 | R2 #30; GECCO M11c |
| 28 | 3.3, 6 | 18/23 and 35/50 given without stating they are nested subsets | subsets defined in §3.3 and Table 1; full-ledger 41/57 and 2/57 alongside | stats F13; R2 #4; GECCO M11b |
| 29 | 5 | Sonnet multi-radius "against a Haiku baseline of 13/35" | dropped; that baseline reproduces at no denominator | R2 #23a |
| 30 | 5 | "no Haiku sample did [this] in 101 invocations" | 155 weak-tier rows; two exceeded the family best, both by ~10⁻⁷ | stats F17; R2 #23b |
| 31 | 3.1, 9 | dual-tolerance reporting promised, never delivered; "cryptographic prompt hashes" | both tolerances in every validity figure; hashes restated as prompt-fragment hashes with coverage gaps itemized above | stats F21; GECCO M12 |
| 32 | all | five HTML working comments and a merge-provenance header shipped | removed; the two load-bearing ones (k = 8 clipping, p-value convention) promoted into §1.1, Fig 1 and §6 | stats F22; R2 #29; GECCO NIT-1–2 |
