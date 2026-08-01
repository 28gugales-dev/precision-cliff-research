# Paper 1 — full draft

*(Merged 2026-08-01 from `paper1_abstract.md`, `paper1_draft_sec1-7-9.md`,
`paper1_draft_sec2-3.md` and `paper1_draft_sec4-6.md`. Section numbering, math notation,
spelling and cross-reference style unified at merge; `[SLOT: related-work]` placeholders
resolved to §7 cross-references. Source files unmodified.)*

---

## Abstract

Large language models are increasingly used as proposal generators in scientific-discovery
loops such as FunSearch and AlphaEvolve, on the assumption that their outputs explore a
diverse solution space. We show that on a classic constructive-geometry benchmark —
maximizing the sum of radii of N circles packed in a unit square — this assumption fails in
a strikingly predictable way. Across hundreds of zero-shot invocations, models do not
search: they recall a single grid-with-corner-fillers template and truncate it, even when a
provably better construction is one parameter away. The behavior is regular enough to admit
a closed form: a selection rule k\* = round(√N) together with a value function V(k, m)
predicts the exact sum-of-radii the model will emit, to seven decimal places, including
"trap zones" of N where the rule provably costs value. We preregistered these predictions
with cryptographic prompt hashes before sampling and confirmed them out of sample in two
containers (square and rectangle), the latter with a rule restated but never refitted.
Across three model tiers we find three attractor families with a consistent inversion:
constructive ambition rises with tier while execution validity collapses (71% → 100% → 13%).
Finally, we show trace elicitation is an intervention, not an observation: asking the model
to name its method before answering concentrates outputs onto the template anchor (87% vs
70% on-prediction, p = 0.033) while leaving validity unchanged, and the emitted method
lines are verifiable against output coordinates (93% faithful). Our results characterize
the proposal distribution that LLM-driven discovery systems sample from: not a searcher,
but a template memorizer whose outputs a formula can anticipate.

---

## 1. Introduction

Ask a language model to place 21 circles in a unit square so as to maximize the sum of
their radii, and it will not search. It will reach for the nearest square grid — five by
five, every circle of radius 1/(2k) — and then truncate that grid to the 21 circles it
was asked for, leaving the four freed cells empty and their area unclaimed. The four
discarded cells are not a rounding artifact; they are where the value went. A better
construction is one parameter away: drop to a four-by-four grid and add corner fillers of
radius (√2−1)/(2k), or keep the five-by-five spacing and enlarge, and the sum of radii
rises. The model does neither. It emits the truncated template, and it does so again on
the next sample, and on the sample after that.

The behavior is regular enough to be written down. A selection rule k\* = round(√N),
combined with a value function V(k, m) over grid order k and filler count m, predicts the
exact sum of radii the model will emit — to seven decimal places, from the problem
parameters alone, before any sampling occurs. The rule also predicts where it will hurt.
When k\*² ≤ N the model extends the grid with fillers and converges toward a reasonable
construction; when k\*² > N it truncates, and value is lost. These *trap zones* —
N ∈ [13,15], [21,24], [31,35], [43,48], [57,60] — are a property of the rounding rule, not
of the packing problem, and they are visible in the output before a single token is drawn.

This matters because circle packing is not an arbitrary probe. It is the showcase
benchmark of the LLM-driven discovery literature — the lineage FunSearch (Romera-Paredes
et al., *Nature* 2023) opened by placing a language model in the proposal role of a
program-search loop and reporting new constructions in combinatorics. Circle packing is
the task on which AlphaEvolve reported 2.635 for n = 26 and on which a succession of
systems have since reported essentially the same number — ShinkaEvolve at 2.635983283,
HELIX at 2.63598308 (2603.07642), GigaEvo at 2.636 (2511.17592), AdaEvolve at 2.636
(2602.20133), with SeaEvo (2604.24372) and ThetaEvolve (2511.23473) in the same band.
Those systems place a language model in a proposal role inside an evolutionary loop, on
the working assumption that its outputs constitute a diverse exploration of the solution
space. We test that assumption on their own home benchmark, in the simplest possible
setting — a single zero-shot call, no code execution, no loop — and find the proposal
distribution to be a template lookup with a closed-form output.

Three framing commitments deserve stating up front, because they are context for the
result rather than parts of it. First, behavioral anchoring in language models is
established territory: the literature documents numeric priming and estimate-dragging in
scalar settings (2505.15392; 2412.06593; 2410.15413), and we inherit that vocabulary
rather than extend it. What differs is the modality — the anchor is a *construction
template*, not a number, and the quantity dragged toward it is a geometric layout. Second,
the benchmark choice is strategic rather than novel: we run on the task the
discovery-systems literature already treats as its exemplar, so that a negative
characterization of the proposal distribution lands where it is load-bearing. Third,
preregistration is by now an adopted standard for LLM experiments rather than a
contribution (2606.27687; 2607.07184; 2606.11217; 2607.00276); our only twist is what is
locked — we hash-lock exact-output point predictions derived from a closed form, on a
held-out container, rather than the directional or aggregate hypotheses that concurrent
work such as HindsightBench (2607.18867) freezes.

**Contributions.**

1. **A closed form that predicts exact model output.** We give a selection rule
   k\* = round(√N) and a value function V(k, m) that predict the precise sum of radii a
   model will emit for a given N, verified against a linear-programming oracle on 83
   configurations to within 1e-9, and confirmed out of sample on two containers — a
   square, and a rectangle to which the rule was restated (q\* = round(√(N/a)),
   p\* = round(√(N·a))) but never refitted. To our knowledge no prior work predicts a
   specific multi-decimal model output from problem parameters ahead of sampling.
2. **A tier inversion in constructive ambition versus execution.** Across three model
   tiers we observe three distinct attractor families and a monotone inversion:
   constructive ambition rises with nominal tier while execution validity collapses
   (71% → 100% → 13%). The most ambitious tier attempts recursive gaskets and
   quarter-circle constructions and mostly fails to produce a non-overlapping packing at
   all.
3. **Trace elicitation as an intervention, not an observation.** Asking a model to name
   its method before answering measurably concentrates its output onto the memorized
   template (87% vs 70% on-prediction, p = 0.0325) while leaving validity statistically
   unchanged. Any study that collects process descriptors *by request* is therefore
   measuring a perturbed distribution, and we name the confound rather than assume it away.

**Non-claim guard.** Everything reported here is a behavioral regularity over emitted
outputs. We make no claim about mechanism inside the weights — no assertion that a
template is stored, retrieved, or represented in any particular way, and no claim that a
prompt constraint acts on internal coordinates. The closed form describes what comes out,
not what happens inside.

---

## 2. Task and recipe family

<!-- Numbers sourced from n_sweep_forecast.py/.json, rect_forecast.py/.json, arm_f_repro.py,
     arm_f_prompts.json, arm_g_rect.py, STATE.md §§v8–v9. Citation slots resolved to §7
     cross-references at merge. -->

### 2.1 The benchmark

The benchmark is maximizing the sum of radii of N non-overlapping circles in the unit square.
Feasibility is decidable exactly from the emitted coordinates, and published best-known lower
bounds exist for small N (see §7.1), so proposals score with no human in the loop.

All invocations are zero-shot and code-free. The prompt (Appendix A.5, verbatim) fixes the count,
states containment and non-overlap, forbids writing or executing code ("construct the packing by
reasoning alone"), and demands only a raw Python list of `[x, y, r]` triples. Given a code channel
the model delegates to an optimizer and the distribution reflects the optimizer. Zero-shot
sampling substitutes for the evolutionary loop on the prior finding that the loop reduces to
best-of-N here; §8 flags the substitution.

### 2.2 The recipe family

In prior arms, 94 of 95 valid coordinate-space proposals were grid-plus-filler constructions. The
family is parametric, not memorized, and admits an exact value function. A k×k grid places one
circle per cell center with r_grid = 1/(2k); m fillers sit on interior grid vertices, each
tangent to its four surrounding grid circles, with r_filler = (√2 − 1)/(2k),
0 ≤ m ≤ (k−1)². Hence

    V(k, m) = k/2 + m(√2 − 1)/(2k).

When N < k² the observed behavior is not to drop to a smaller grid and fill it, but to
*truncate*: lay out the k×k lattice, occupy only N cells, leave the radius unchanged.

    T(k, N) = N/(2k),   N < k².

These reproduce every previously reported anchor with no fitting: V(5,1) = 2.5414214,
V(5,2) = 2.5828427, V(5,0) = 2.500, T(5,23) = 2.300 (the observed trap at N = 23) and
V(4,7) = 2.3624369 (the one escaping seed there). Five of five.

### 2.3 The selection rule

The recipe does not say which k the model reaches for, and supplying that turns description into
forecast. Four candidates — nearest integer square root, floor, ceiling, value-argmax over the
family — were scored against the three anchors, requiring both k and branch to match. One
survived (`nearest` 3/3, `floor` 2/3, `argmax` 2/3, `ceil` 1/3):

    k*(N) = ⌊√N + ½⌋ = round(√N)
    k*² ≤ N  →  extend with m = N − k*² fillers   (converge)
    k*² > N  →  truncate                          (trap)

Zero free parameters. Three anchors against four candidates is *identification*, not confirmation,
and we do not soften that; its value is that every other N becomes out-of-sample.

The rule ignores whether a better member of the family exists. The governing quantity is the
signed distance N − k\*², non-negative converging and negative trapping. Primality is not the
variable — 13, 23, 31, 43, 47 and 59 trap while 11, 17, 19, 29, 37, 41 and 53 converge — refuting
the prior work's conjecture about primes near 30 before any model is queried.

### 2.4 Trap zones and their cost

Substituting k\*(N) into the branch condition gives the zones in closed form:

    TRAP:     N ∈ [k² − k + 1, k² − 1]
    CONVERGE: N ∈ [k², k² + k]

Over the swept range N = 10…60: [13,15] (k=4), [21,24] (k=5), [31,35] (k=6), [43,48]
(k=7), [57,60] (k=8).

<!-- NOTE (not a conflict): the k=8 zone is [57,63] by the formula; [57,60] is that zone clipped
     by the sweep bound, sweep(10, 60) at n_sweep_forecast.py:340. Worth a clause in the caption
     so a reader checking the formula does not think it disagrees. -->

Inside a zone the rule loses value against the best construction available *within the recipe
family itself*. The worst-in-zone penalty falls as N grows — 8.51% at N = 13, 7.03% at 21,
6.01% at 31, 5.25% at 43, 4.66% at 57 — and hits exactly zero at the top of each zone (N = 35,
48), where truncation happens to *be* the recipe optimum. Those traps are indistinguishable from
convergence by value, separable only by structure; §3.2 uses one as a control. The family
is also never competitive with the record: its deficit against published lower bounds runs
0.02–0.26 across N = 10…30 and is 0.0946 at N = 26.

Every closed-form value is recomputed by an independent linear program over the constructed
coordinates, which knows nothing about the recipe; the script aborts on disagreement, and on any
predicted value exceeding a published lower bound. 83 configurations, both branches, every k in
2…7, drift below 1e-9.

[FIGURE 1: Predicted-versus-optimal value, N = 10…50. Curve (i): the rule's prediction — V(k\*, m)
on the converge branch, T(k\*, N) on the trap branch. Curve (ii): the best value attainable
anywhere in the recipe family. Shade trap zones [13,15], [21,24], [31,35], [43,48]; the gap inside
each band is the self-inflicted penalty, labeled with its worst-in-zone percentage (8.51%, 7.03%,
6.01%, 5.25%). Mark N = 35 and N = 48, where the gap closes to zero. Data:
n_sweep_forecast.json.]

---

## 3. Preregistered forecast, out of sample

### 3.1 Registration protocol

Because the rule was identified on three points, everything downstream depends on predictions
being fixed before sampling. For each cell the prompt is pinned and its SHA-256 digest written to
disk first — the N = 13 square prompt hashes to `32db485b…` in `arm_f_prompts.json`. Predictions
P1–P5 are registered in the header of `arm_f_repro.py`, with standalone files for the parallel
arms (`arm_s_preregistration.txt`, `arm_o_preregistration.txt`, `arm_t_preregistration.txt`).
Raw outputs are stored verbatim, failures included; scoring is deterministic and local.

Three properties are not repairable and are disclosed rather than papered over: temperature, top-p
and top-k are not exposed by the agent runtime; the alias-to-weights binding is a promise, not a
hash; and the subagent inherits instruction files outside the task prompt. We record the run date
(2026-07-30, square arm) and the alias-to-dated-id mapping then in force. An agent runtime cannot
be made reproducible from inside itself.

Two scoring conventions were fixed in advance, since choosing either afterwards is the easiest way
to fabricate the table. Validity is reported at 1e-9 and 1e-6, both logged, 1e-6 primary:
proposers print six to eight decimals, so an eight-decimal tangency misses contact by ~5e-9, while
1e-6 sits far below the ~1e-2 gap between rival constructions. Value matching uses a loose window
and an exact one — at N = 31, r = 0.0833 summing to 2.5823 against an exact 2.5833333.

### 3.2 Square container

The square arm sampled Haiku-tier proposers at N = 13, 17, 21, 31, 35, 37 and 43. The rule was
fitted on N = 23/26/27 only, so every cell is out of sample.

Four cells are *discriminating*: rule and family optimum disagree, so a proposer that searched the
family rather than recalling the nearest square would return a higher number. Across those cells
(N = 13, 21, 31, 43), **18 of 23 valid invocations landed on the predicted construction**, and
the rival-argmax value was reached **2 times in 23** — both at N = 21, both the 4×4 grid plus
five fillers at 2.2588835. Pooled with the rectangle cells below, the rival rate wherever rule and
optimum disagree is **2/34**.

That the anchor first breaks at N = 21 is informative: it is the bottom of a trap zone carrying a
large relative penalty (7.03%), so the anchor looks weak where obeying it costs — a hypothesis,
not a finding, pending the other zone-bottoms.

**P4** registered N = 37 as converging cleanly on 3.0345178, a 6×6 grid plus one filler at
(√2−1)/12 — a prime predicted clean, contradicting the prior work's own guess. It confirmed.
**P5** registered N = 35 at 2.9166667, the top-of-zone control where truncation is also the
recipe optimum; three of four valid samples landed there, separable from convergence only because
the structure classifier reads the radii rather than the total. The fourth used a 7×7 lattice
truncated to 35 (r = 1/14, sum 2.5), outside the rule entirely.

Bookkeeping that would otherwise corrupt these rates: five invocations were rejected by the
runtime's 20-subagent concurrency cap *before reaching a model*, and scoring them invalid would
have understated validity by 17%; two parse failures occurred in previously logged modes (`1/12`
fractions, a list wrapped in prose containing `[0,1]x[0,1]`); one N = 37 proposer derived
r = (√2−1)/12 correctly in prose, then transcribed 0.03571429.

### 3.3 Rectangle transfer

One container with a one-parameter template is the obvious weakness, so we restated the rule for a
1 × a rectangle, where the template has two free parameters:

    q* = round(√(N/a))    columns across the width 1
    p* = round(√(N·a))    rows across the height a

At a = 1 both collapse to round(√N): the same rule with the aspect ratio put back in, not a new
rule fitted to new data, and no rectangle model output existed when it was written. It was
verified against an independent LP at 213 configurations, drift below 1e-9, including a
cross-domain check — at a = 1 with p = q = k the square file's closed form must equal this
file's LP. Two files, two derivations, one number.

Shape mismatch grows sharply as a leaves 1: over N = 10…45 the count of N whose predicted
shape differs from the optimal one rises from 12 at a = 1.0 to 23 at a = 1.5, 20 at a = 2.0
and 23 at a = 3.0, worst gaps 8.5% (N = 13), 7.8% (N = 31), 10.3% (N = 25), 11.4%
(N = 19).

We probed the two sharpest cells with sixteen proposers, in a container none had been given
before: N = 19 at a = 3 (predicted 3.1666667, an 8×3 truncation; rival 3.5749194, a 7×2 grid
extended with five fillers) and N = 25 at a = 2 (predicted 3.1250000, a 7×4 truncation; rival
3.4832492, a 6×3 grid extended with seven fillers). With all sixteen scored, **5 of 11 valid
proposals landed on the predicted value and 0 of 11 reached the rival**. Nearest-template
anchoring is not an artifact of the one-parameter square case.

<!-- VERIFIED 2026-08-01 recount: 5/11 on-pred, 0/11 rival -->

Two qualifications are recorded rather than smoothed. Validity degrades in the tall container —
4/8 at a = 3 against 7/8 at a = 2, three of the four a = 3 failures being overlaps — a
separate finding and a confound on that cell, on n = 8. And one a = 3 sample beat the
prediction from outside the family altogether: five circles at r = 0.1, ten at r = 0.25, four
at r = 0.125, summing to 3.5, still below the 3.5749194 rival. The recipe is the attractor, not
a ceiling.

### 3.4 Negative result: the closed form does not survive the move to rectangles

The rectangle generalizes the *rule* but not the *formula*. We keep the failure because it is what
a verification gate is for.

In the unit square every interior vertex has four identical neighbors, so one expression covers
every filler. In a 1 × a rectangle, with half-spacings hₓ = 1/(2q) and hᵧ = a/(2p), a
filler is capped by three competing quantities: the diagonal gap to the four surrounding grid
circles, and the horizontal and vertical spacing to *adjacent fillers*. The latter two are
inactive when hₓ = hᵧ — why the square case could not have revealed them — and bind only when
the neighboring vertices are occupied. The cap therefore depends on m and on which vertices a
construction uses, and no expression in (p, q, m, a) reproduces it.

The LP gate caught this on the first run. At a = 1, p = 2, q = 4, m = 1 the natural
generalization `rf = min(diag, hₓ, hᵧ)` returns **1.125** against a true **1.1545085**: it caps
against a neighboring filler that, with one filler placed, does not exist. We retain closed forms
only where provably exact — full grid and truncated grid — and use the LP as the value oracle for
the extend branch. The pipeline aborted on drift rather than propagating a plausible formula, so
what §3.3 tests is the LP-backed prediction.

[TABLE 1: Forecast versus outcome, both containers, one row per cell. Columns: cell | predicted
branch and value | rival-argmax | valid/sampled | on-prediction/valid | rival hits. Square rows:
N=13 truncate 1.6250000 (rival 1.7761424); N=17 extend 2.0517767†; N=21 truncate 2.1000000
(2.2588835); N=31 truncate 2.5833333 (2.7485281); N=35 truncate 2.9166667†; N=37 extend
3.0345178†; N=43 truncate 3.0714286 (3.2416246). Rectangle rows: N=19/a=3 truncate 3.1666667
(3.5749194); N=25/a=2 truncate 3.1250000 (3.4832492). Footer: square discriminating cells 18/23
on-prediction, rival 2/23; rectangle 5/11, rival 0/11; combined 2/34. † non-discriminating
(predicted equals family argmax), excluded from rival denominators. Data: arm_f_repro.py over
arm_f_candidates.jsonl and arm_g_rect.py over arm_g_candidates.jsonl.]

---

## 4. The tier ladder: three attractor families

The selection rule of §2 was identified on, and confirmed out of sample against, a single
proposer tier. Does it describe language models, or one model? Holding prompt, container and
scoring machinery fixed, we varied only the nominal proposer tier across the three cells that
discriminate hardest between the rule's prediction and the recipe family's own optimum —
N = 13, N = 21 and N = 31, each inside a predicted trap zone. The rule turns out to be
tier-scoped, and the tiers do not merely differ in how often they succeed: they attempt
qualitatively different constructions. We report them as three attractor families rather than
three points on an accuracy axis.

**The weak tier truncates templates.** The Haiku-tier proposer produces uniform grids of
radius 1/(2k) truncated to N circles, with corner fillers added only when the grid
underfills. Across the 45 bare invocations logged in the arm-F ledger — spanning
N ∈ {13, 17, 21, 31, 35, 37, 43} — 32 were geometrically valid (71%). At the three
discriminating cells, 12 of 16 valid samples landed on the predicted value and the
higher-scoring rival was reached twice, both times at N = 21 — the behavior the closed form
of §2 anticipates, and the baseline for the other two tiers.

**The middle tier perturbs and mixes.** The Sonnet-tier proposer was preregistered in
`arm_s_preregistration.txt`, disclosing that 5 of 20 samples at N = 13/21 had been seen
before registration and that N = 31 was fully blind. It was valid in 30 of 30 invocations
and almost never on-prediction: 0/10 at N = 13, 0/10 at N = 21, 1/10 at N = 31 — 1/30
pooled, against the Haiku tier's 12/16 at the same cells. Instead of truncating a uniform
grid it perturbs one, with enlarged edge rows, hexagonal interior rows and two or three
distinct radii in the same packing (29/30 multi-radius, against a same-metric Haiku baseline
of 13/35). It reaches the higher-scoring rival 6 times in 30, including 3/10 at N = 13 and
3/10 at N = 31, where Haiku reached it zero times in nine invocations. At N = 21 its values
lie between 2.14 and 2.25 — all above the 2.1 trap, none on the 2.2588835 rival: it escapes
the trap without finding the recipe family's optimum.

One Sonnet sample at N = 31 emitted 27 circles at r = 1/12 with 4 corner circles at r = 1/8,
summing to 2.75 — above 2.7485281, the best value the recipe family reaches at that N.

<!-- Slack verified 2026-08-01 by direct recomputation from arm_f_candidates.jsonl
(sonnet_bare, N=31, sid=2): min pairwise slack 0.000e+00, min wall slack 0.000e+00,
sum of radii 2.7499999991. Tangency-tight, zero violations at tol=0. -->

Recomputed directly from its stored coordinates, the construction is tangency-tight: minimum
pairwise slack and minimum wall slack are both exactly zero at tolerance zero, with sum of
radii 2.7499999991. It is the only sample in the study to leave the recipe family upward,
something no Haiku sample did in 101 invocations. The recipe is an attractor, not a ceiling.

**The top tier attempts recursive constructions and fails to build them.** The third arm was
invoked through a bare tier alias. We name it `opus_alias` throughout and make no claim about
which weights served it: the agent runtime accepts only the bare alias and exposes no dated
model identifier, so the alias-to-weights binding is a vendor promise rather than an
attestable fact, and this arm must not be read as a statement about any specific model
version. Two anomalies make the caveat load-bearing. Completion times ran 2.8–9 seconds
across all 30 invocations, against 75–250 s for Haiku and 150–1170 s for Sonnet, a profile
consistent with a fast-decode serving path; and the reported token count was uniform at
49,906 across the first 20 completions and stayed at ≈49.9k for the rest. Both are
consistent, not intermittent.

Under those caveats, the arm — preregistered fully blind in `arm_o_preregistration.txt`
(sha256 21171…738) — was valid in 4 of 30 invocations (13%). At every cell it attempted a
construction more ambitious than either other tier: at N = 13, four quarter-circle corners
at r = 0.25 with Apollonius-style center, edge and corner fillers, the same family in 10/10
samples; at N = 21, mixed-radius 4×4-ish grids with corner and edge fillers; at N = 31, a
coarse 3×3 grid at r ≈ 1/6 with border strips and interior fillers, 0/10 valid, every sample
breaking tangency somewhere. The failures are geometric rather than numerical — edge strips
at r = 0.03 placed 0.138 from an r = 1/6 grid circle needing 0.197 — and twice the arm padded
to the required count with zero-radius circles, caught by the nonpositive-radius gate. Valid
samples score *below* the trap they were expected to fall into (1.26–1.41 at N = 13 against a
trap value of 1.625). Registered predictions P-O1, P-O2 and P-O4 are reported as not
evaluable: a validity collapse of this size makes a tier comparison on on-prediction rates
dishonest rather than merely noisy, and P-O3 is trivially satisfied on 4/4 valid samples. The
registered disconfirmation — regression toward the trap — did not occur; the arm fell off a
validity cliff attempting a harder family.

[TABLE 2: three-attractor ladder. Columns: `tier` (haiku / sonnet / opus_alias — footnote
the alias-provenance caveat on the third row) | `cells` | `n invocations` | `attempted
construction family` | `valid / n (%)` | `on-prediction` | `rival-argmax hits` |
`characteristic failure mode`. Sources: `STATE.md` §§6–8b, `arm_f_candidates.jsonl`,
`arm_s_preregistration.txt`, `arm_o_preregistration.txt`.]

<!-- CONFLICT: STATE.md §8 states the opus_alias arm is "excluded from the tier ladder";
§8b, written after the arm completed, tabulates it directly against the other two tiers
("valid 4/30 (13%) vs Haiku 32/45 (71%) vs Sonnet 30/30 (100%)"). Following the later
entry: included in Table 2, with the caveat carried in the row label. -->

Two asymmetries carry through to §8: the Haiku denominator spans seven values of N against
three for the other tiers, and the serving-path and model-tier readings of the third arm are
inseparable without a pinned-weights run the runtime does not permit.

The ladder shows one inversion. Constructive ambition rises monotonically with nominal tier —
truncated template, perturbed hybrid, recursive gasket — while execution validity does not:
71%, then 100%, then a collapse to 13%. At the canonical, plausibly contaminated cell N = 26
all tiers converge on the same 2.5414 attractor; they diverge only at withheld trap cells.
The nearest-square rule of §2 is therefore a weak-tier law, and the tier contrast is a second
observation rather than a caveat on the first: the 2.5414 attractor is tier-shared, the
truncation trap tier-specific.

---

## 5. Elicitation as intervention

The cleanest result in this section is a negative one, and we lead with it because the
design was built to produce exactly this outcome if the pilot had been noise.

A ten-versus-ten pilot at N = 21 compared the bare prompt against a variant asking the
proposer to name its construction on a leading `METHOD:` line. It showed two effects, both
against the naive expectation that a label is free: validity rose from 7/10 to 10/10, and
the higher-scoring rival construction disappeared entirely, from 2 of 7 valid bare samples
to 0 of 10 trace samples. Taken at face value, that pair would have supported a strong
claim — that asking for a method statement makes a proposer both more reliable and more
conservative.

We did not take it at face value. Before any scaled sample was drawn we registered four
predictions and an explicit falsifier in `arm_t_preregistration.txt` (sha256 ab7900a8…),
together with a disclosure that the pilot's trace prompt had drifted from the bare template
beyond the method line itself: it omitted the `[0,1]x[0,1]` tokens and reworded the
output-format line, so the pilot's intervention was method-line-plus-rewording, bundled.
The scaled trace prompt, `trace_v2`, is a minimal diff against the bare template — one
inserted `METHOD:` line and three words prepended to the output line. Pilot samples are
never pooled with `trace_v2`, and the pilot is reported as a pilot.

At scale the pilot's two headline effects died.

The scaled arm ran 100 new invocations, bringing both arms to 20 samples per cell at
N ∈ {13, 21, 31}; all six prompt variants were SHA-256 hashed before sampling and the raw
completions stored verbatim, taking the corpus to 215 logged invocations. Scoring used
`arm_f_repro.py` unchanged with the registered 2 × 10⁻³ value window, and the Fisher exact
test is computed directly from the hypergeometric tail in `arm_t_analysis.py` rather than
imported, so the analysis cannot drift with a library version.

**P-T1, validity: not confirmed.** The direction held at all three cells — trace_v2 at least
as valid as bare at 13, 21 and 31 — but the pooled one-sided Fisher test gives p = 0.30. The
registered falsifier (trace_v2 validity at or below bare at two or more cells) was not
triggered, so we do not conclude that the pilot's validity effect was purely the bundled
rewording, only that it is not detectable at 20 per arm per cell.

**P-T2, rival suppression: not confirmed.** Rival hits were 1 of 53 valid trace_v2 samples
against 2 of 50 valid bare samples, p = 0.48: the pilot's apparent suppression was an
artifact of how rare the rival is in *both* arms at this sample size. One trace_v2 sample at
N = 31 hit the rival value 2.7485281 exactly — the first Haiku-tier rival hit at N = 31 in
any arm of the study.

**P-T3, anchor concentration: confirmed.** Among valid samples, 46 of 53 trace_v2
invocations (87%) landed on the registered nearest-square prediction, against 35 of 50
(70%) in the bare arm; one-sided Fisher p = 0.0325.

<!-- CONFLICT: skeleton §5 and paper1_abstract.md both give p = 0.033; STATE.md §9 gives
p = 0.0325. Same test, same table — this is rounding, not disagreement. Evidence-file
value used here; the abstract's rounded form is consistent. -->

**P-T4, faithfulness: confirmed.** 38 of 41 scoreable method claims matched the emitted
layout (93%), against a registered threshold of 90%. §6 treats this result on its
own terms.

[TABLE 3: paired trace grid. Columns: `N` | `arm` (bare / trace_v2) | `n invocations` |
`valid` | `on-prediction` | `rival-argmax`, with pooled totals and the P-T1/P-T2/P-T3
Fisher p-values as table notes; the pilot reported in a separate, clearly-labeled block
that is never summed into the totals. Source: `STATE.md` §9, regenerated by
`arm_t_analysis.py`.]

The claim we draw is narrower than the pilot's and, we think, more interesting. A minimal
method-naming request does not make the proposer better at geometry and does not measurably
change which rare constructions it reaches. What it does is concentrate the output
distribution onto the template anchor, making the model more likely to emit the very
construction the closed form of §2 predicts. Eliciting a trace is a mild commitment device:
a request for a nameable method selects for nameable constructions, and the nearest-square
truncated grid is the most nameable object in this space.

Two implications follow. Trace-on and trace-off samples must never be pooled, here or in any
study mixing prompts that differ by a reasoning-elicitation line. And any work collecting
process descriptors *by asking for them* — including descriptor-driven quality-diversity
pipelines, where a behavioral descriptor is often obtained by requesting a self-report — is
measuring a perturbed distribution, perturbed in a direction that specifically favors the
memorized template (see §7.5). We name this confound because our own pipeline was going to
rely on it; it is now measured rather than assumed, and the measurement says the window is
not neutral glass.

One bookkeeping note from the same harvest: two bare samples emitted fraction literals
(`1/12`) and failed the §A.5 parser, logged rather than dropped.

---

## 6. Faithfulness with ground truth

The trace arm creates an unusual auditing opportunity. When a proposer writes
`METHOD: 5x5 grid plus 2 corner fillers` and then emits 27 coordinate triples, claim and
artifact sit in the same completion, and the artifact is fully determined: the radii and
centers say exactly how many rows, how many columns and how many distinct radii were
actually built. The method line is checkable against ground truth rather than against a
plausibility judgment. Our check is deliberately coarse:
`arm_f_repro.trace_faithfulness()` extracts the numeric dimensions named in the method
line — row and column counts, grid order, filler counts — and asks whether the emitted
layout signature contains them, recording claims with no numeric content as unscoreable
rather than scoring them generously.

In the pilot, 8 of 8 scoreable traces matched, 2 unscoreable for lack of numeric dimensions.
The most informative match cost the proposer value: a sample claiming `Triangular hexagonal
packing with 6+5+4+3+2+1 rows` emitted exactly that — 21 circles at r = 1/12, summing to
1.75, below both the 2.1 trap and the 2.2588835 rival. The model described what it built,
including when what it built was bad.

At scale the result holds: 38 of 41 scoreable method claims match the emitted layout, 93%,
clearing the registered 90% threshold. The three mismatches are all the same case, and the
case runs against us in a useful direction. Each is a claim of the form "4×4 grid + 5 gap
circles", where the fillers add coordinate rows that the coarse row/column signature reads as
a violation of the stated grid dimensions. The scorer penalizes a claim that is, in fact,
accurate. The conservative scorer therefore undercounts matches, and 93% should be read as a
floor on faithfulness in this setting rather than a point estimate.

This is the check that the chain-of-thought faithfulness literature cannot run. That line of
work must estimate whether a stated reasoning process corresponds to the process that produced
the answer without ever observing the latter, and its methods are consequently indirect —
counterfactual perturbation, hint-insertion, consistency probing (2503.08679; 2606.13603;
2605.29087; see §7.4). In constructive geometry the emitted coordinates *are* the ground truth
for what was built. Faithfulness becomes a measurement rather than an inference, and on this
task, at this tier, under this elicitation, the traces pass.

We claim no more than the setting supports. The check is coarse and can only falsify claims
carrying explicit numeric dimensions; it verifies that the description matches the artifact,
not that it matches whatever internal process produced the artifact — the non-claim guard of
§1 applies in full. The audit covers one proposer tier and one elicitation prompt, and §5 has
just shown that the prompt itself shifts the distribution being described. What survives is
narrow and load-bearing: in a domain where claims are checkable, the method lines this model
emits are, to at least 93%, true of the object it produced.

---

## 7. Related work

### 7.1 LLM-driven discovery systems and the saturation of circle packing

Placing a language model in the proposal role of an evolutionary loop has an established
lineage in the evolutionary-computation community: Language Model Crossover (Meyerson et
al., ACM TELO 2023) framed the LLM call as an EC operator, ELM (2206.08896) paired LLM
mutation with MAP-Elites, EvoPrompt realized GA and DE operators through model calls, and
LLaMEA (2405.20132) carried the pattern into algorithm design. FunSearch (Romera-Paredes et
al., *Nature* 2023) is the entry that made the pattern a discovery claim rather than an
operator study — an LLM proposer paired with a deterministic evaluator, iterated over
program space, reporting new constructions in extremal combinatorics and bin packing — and
it is the template every system below inherits. Circle packing became the public scoreboard
of this line. AlphaEvolve's 2.635 at n = 26 was followed by ShinkaEvolve's 2.635983283,
HELIX's 2.63598308 (2603.07642), GigaEvo's 2.636 (2511.17592), AdaEvolve's 2.636
(2602.20133), and further entries from SeaEvo (2604.24372) and ThetaEvolve (2511.23473).
The spread across systems is smaller than the systems' architectural differences, which is
itself informative: the benchmark is saturated at the reporting precision these papers use,
and the published best-known lower bounds that §2.1 scores against sit above all of them.

Two critiques of that scoreboard bear on our framing. Gideoni, Risi and Gal (2602.16805)
show that simple baselines recover much of the reported advantage, and Berthold et al.
(2605.04850) show that classical solvers do so as well — independent critiques that are
frequently conflated, so we note the attribution explicitly. Both ask whether the *system*
adds what its headline number implies. We ask a prior question: what does the LLM component
propose when queried directly? Our answer — a truncated grid template whose value a formula
anticipates — gives a mechanism-free account of what the loop's selection pressure is
filtering.

### 7.2 Template convergence and diversity collapse

The closest cousin to our result is "Mutation Without Variation" (2606.05408), which finds
that iterated LLM program mutation collapses onto previously seen structural templates —
87% of chains and 93% of mutations revisit prior form. That is the same bias family in a
different regime: mutation loops rather than single calls, program space rather than
geometry, and no closed form or preregistration. It corroborates rather than scoops.
Nearer still in benchmark terms, 2605.29268 reports asymmetric proposal mass on this same
task in program space — corroborating evidence in a different modality, which is why our
zero-shot, no-code setting is worth reporting separately: the anchoring is not an artifact
of the code-generation channel.

The vocabulary we inherit comes from the numeric-anchoring lineage. 2505.15392 and
2412.06593 document irrelevant numeric primes dragging model point estimates, and
2410.15413 measures how far a stated reference value pulls a subsequent judgment. In all
three the anchor is a scalar and the dragged quantity is a scalar. Our modality is the
difference that matters: the anchor is a construction template and the dragged quantity is
a geometric layout, which is what makes the anchor's value computable in closed form rather
than only measurable as a shift.

A broader skeptical literature converges on the same worry from several directions.
"What Makes an LLM a Good Optimizer" (2604.19440) and "Dictionaries Not Darwin"
(2607.04108) question whether the model contributes search or retrieval; EvoDiverse
(2606.10587) measures diversity directly; BehaveSim (2603.02787) scores behavioral
similarity between model-generated candidates and finds populations far more alike than
their surface form suggests; Strategy Diversity (2605.09292) counts how few distinct
strategies a batch of LLM proposals actually contains; the bin-packing critiques
(2510.27353; 2501.11411) show reported gains on a second combinatorial showcase to be
fragile; and 2407.10873 isolates how much of the performance is attributable to
evolutionary search rather than the proposer. MathConstruct (2502.10197) makes the
complementary point in the constructive-mathematics setting, where a model must *build* an
object rather than select an answer. Our contribution to this cluster is specificity: not
that diversity is low, but that the concentration point is identifiable in advance and its
value computable.

### 7.3 Scaling inversions

The tier inversion we report has precedent outside constructive geometry. Zhou et al.
(*Nature*, 2024) show that larger and more instructable models become less reliable —
attempting more and erring more in a QA regime — and the o3/o4-mini system card documents
the same shape on PersonQA, where more claims accompany more hallucinations. "The Illusion
of Thinking" (2506.06941) reports capability collapse past a complexity threshold, and
GeoBuildBench (2605.13167) finds geometric construction to be a regime where nominal
capability and executed correctness diverge. Our contribution is the constructive
instantiation: the inversion is not merely accuracy versus attempt rate but *attractor
family* versus executability — the more capable tier reaches for recursive gaskets and
quarter-circle constructions and then fails to produce a valid layout, while the middle
tier produces perturbed grid hybrids that always validate.

### 7.4 Trace faithfulness, and what our elicitation result is not

**Disambiguation.** A substantial recent literature intervenes *on trace content* and
finds that answers do not move. Reasoning Theater (2603.05488) shows the answer is
decodable from activations before the trace completes; Project Ariadne (2601.02314)
applies hard interventions to trace content and finds answers largely unchanged, quantified
by the Ariadne Score, a measure of Causal Sensitivity. The shared conclusion is causal
decoupling: the trace is not the computation. A parallel line asks the narrower question of
whether a stated process can be certified at all without observing the process —
2503.08679, 2606.13603 and 2605.29087 estimate faithfulness by counterfactual perturbation,
hint-insertion and consistency probing, because no ground truth for the described process
exists in their settings; §6 reports the case where one does. Our result operates at a
different intervention point from either line. We do not edit the trace; we vary whether one
is *requested*, and we find that the request itself shifts the output distribution toward
the memorized template (87% vs 70% on-prediction, p = 0.0325). That is measurement
reactivity, not causal faithfulness, and the two findings are complementary: the decoupling
literature says the trace does not drive the answer, while our result says that asking for a
trace nonetheless changes what is answered. Both must hold for a process-descriptor study to
be interpreted correctly, and neither substitutes for the other.

The closest cousin is "The Price of Format" (2505.18949), which shows that imposing an
output format collapses generation diversity. The differentiator is what is imposed: a
format constraint restricts the *shape* of the answer, whereas our manipulation adds a
one-line request to name a method, leaves the answer format untouched, and still
concentrates the output. Related reactivity results include the Hawthorne effect in
reasoning models (2505.14617), where test-awareness steers behavior; Verbalized Sampling
(2510.01171) on mode collapse; and Latent Memory Anchor (2506.17630). Our setting adds what
these lack: the emitted method line is auditable against the emitted coordinates, so
faithfulness is checked against ground truth rather than estimated.

### 7.5 Preregistration lineage

Preregistration of LLM experiments is established practice. Thomas, Gligoric and Shah
(2606.27687) preregister the experimental recipe; "Predicting LLM Safety Before Release"
(2607.07184) files OSF preregistrations of prevalence rates; 2606.11217 adapts the protocol
to AI-agent experiments; 2607.00276 applies it in a physics-literacy study. Concurrently,
HindsightBench (2607.18867) freezes directional aggregate hypotheses under SHA-256. We adopt
this standard rather than claim it; what we add is the object locked — exact closed-form
point predictions of specific output values, hashed with the prompts, tested on a container
the rule was never fitted to. The structural precedents come from outside the prereg
literature: Kaplan et al. (2001.08361) and Chinchilla (2203.15556) publish a functional form
and then run the confirming instance, and "Predicting Emergent Capabilities by Finetuning"
(2411.16035) is the closest structural twin — a timestamped preregistered threshold tested
on deliberately excluded models. Related in spirit, MatLLMSearch (2502.20933) reports
crowding in an LLM-driven materials search, and QDAIF (2310.13032) is the QD-descriptor
setting most directly affected by our §5 reactivity finding: its behavioral descriptors are
obtained by asking the model for them, which is exactly the request §5 shows is not neutral.

---

## 8. Limitations

**Single vendor.** All model tiers sampled here come from one provider. A cross-vendor arm
was scoped and is blocked on credit rather than on design; we disclose this rather than
generalize past it. The closed form is stated over problem parameters, not over any
vendor's architecture, so it is testable elsewhere — but it has not been, and the
tier-inversion result in particular should be read as a within-family observation until
it is.

**Zero-shot only.** We characterize the single-call proposal distribution and do not rerun
an evolutionary loop. This is a deliberate scope choice — paper 0 found the loop to perform
comparably to best-of-N on this task, so the single-call distribution is the object of
interest — but it means our claims describe what the loop *samples from*, not what the loop
converges to. Selection pressure over many generations may escape the attractor in ways a
single call cannot show.

**Sampling parameters unpinned.** The agent runtime used for collection does not expose
pinned decoding parameters, so temperature and related settings are not fixed across
invocations. Every effect we report is a distributional claim over the observed sampling
regime, not over a specified one. This limitation is the direct subject of the companion
paper (paper 2), which treats runtime nondeterminism as its object; we cross-cite rather
than re-litigate it here.

**opus_alias serving-path confound.** The highest tier is referred to throughout as
`opus_alias` and never by a version number. The label denotes the serving alias we
addressed, not an identified model version: without pinned weights we cannot separate a
model-tier effect from a serving-path effect, and the 13% validity figure is a property of
what that alias returned during our collection window. Any reading of the tier inversion as
a statement about a specific released model would exceed the provenance we have.

---

## 9. Reproducibility statement

Every prompt was hashed with SHA-256 and the hashes were recorded *before* any sampling
occurred, together with the predicted values they were to be tested against. The
preregistration files are in the repository and named: `arm_f_repro.py` (header, predictions
P1–P5, square arm), `arm_s_preregistration.txt` (Sonnet tier), `arm_o_preregistration.txt`
(opus_alias tier), and `arm_t_preregistration.txt` (elicitation arm, prereg hash
`ab7900a8…`). The rectangle transfer was registered before collection and never refitted to
rectangle data (`rect_forecast.py`, `arm_g_rect.py`).

All raw model outputs are stored verbatim in the repository (`arm_f_raw.json`,
`arm_f_candidates.jsonl`, `arm_g_candidates.jsonl`), so any scoring decision can be
re-derived from the original text rather than trusted. Scoring is deterministic and local:
layouts are parsed into coordinates and radii, overlap and containment are checked at fixed
tolerance, and the sum of radii is computed without model involvement at any stage.

Value claims are gated on an independent linear-programming oracle rather than on the
closed form being tested. The forecast pipeline (`n_sweep_forecast.py`, with
`verify_against_lp`) checks 83 recipe-family configurations against LP-computed values to
within 1e-9, and the same oracle is what produced the negative result we report in §3.4: the
rectangle filler closed form does not exist, with an LP counterexample at 1.125 against
1.1545085. We keep that negative in the paper because it demonstrates the gate working —
the pipeline aborts on drift rather than fitting through it.

Analysis scripts (`arm_t_analysis.py`), forecast artifacts (`n_sweep_forecast.json`,
`rect_forecast.json`), and a running experimental log (`STATE.md`) are included, so every
table in this paper regenerates from the raw outputs by a single command documented in
`HOW_TO_RUN.md`.
