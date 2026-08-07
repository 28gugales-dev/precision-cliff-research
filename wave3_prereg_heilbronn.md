# Wave 3 preregistration — search progress as a registered primary, on a second task

**Status: DRAFT, NOT YET LOCKED.** This document becomes a registration only when its
SHA-256 is published and the runner carrying these predictions is pushed to an
externally-timestamped host *before* any row is sampled. Until then it is a design note.
Nothing in the paper may cite it as a registration.

**Author:** *(unresolved — see the outstanding item in `PAPER2_AND_SCOPE_PLAN.md`)*
**Written:** 2026-08-07, against paper 2 at commit `6b56467` (v23).

---

## 1. What this wave exists to fix

Paper 2 §3.6 reports a loop-level statistic — accepted hill-climb steps per lineage — on
which the 2-bit rung takes 1 step per 50 calls against 14–16 at the upper three. Four things
are wrong with that result as it stands, and this wave is designed against all four:

| defect in §3.6 | wave 3's answer |
|---|---|
| **Post-hoc.** The statistic appears in no registration. | It is this wave's **registered primary**, with a closed-form bound written into the runner header before execution. |
| **The registered form failed.** Fresh-seed F1 forecast the *binary* improvement count and was refuted (3/5 against a predicted ≤ 2/5). | Wave 3 registers the **count**, states the bound in count units, and registers the binary form alongside it as a secondary so the two cannot be swapped after the fact. |
| **Mostly the echo result in complement.** `accepted ≤ valid − echo` by construction; the residual gap was 0, 1, 1, 2. | The task is chosen so that echo and improvement come apart (§2), and the **conditional-on-departure rate is registered as its own primary** with an allocation powered for it (§4). |
| **One task, one lattice, one scale.** Circle packing at N = 26; the dispersion probe's six parents share one lattice; 7B does not replicate. | A **second constructive task with no lattice attractor**, run on the same pinned ladder. |

The design also fixes the power floor §3.6 discloses: a five-versus-five exact permutation
cannot return a tail below 2/252 = 0.0079, which is exactly where two of §3.6's tails sit.

## 2. Task: Heilbronn triangle, n = 13 in the unit square

Place 13 points in \[0,1\]². Score = the **minimum triangle area** over all C(13,3) = 286
triples. Higher is better. Best known for n = 13 is ≈ 0.0250. Deterministic, exact in
floating point, no tolerance parameter, no scorer of ours anywhere in the loop.

Why this task and not another packing variant:

1. **It has no grid attractor, and grids are actively catastrophic on it.** Any three
   collinear points give area exactly 0. A regular grid — the configuration the circle-packing
   proposer reproduced verbatim at the 2-bit rung — scores **0** here. Circle packing could not
   distinguish "the proposer copies its parent" from "the proposer emits the template it
   always emits," because the seeded parent *was* that template. Heilbronn separates them: a
   template-emitting proposer scores zero and is visible immediately; a parent-copying
   proposer reproduces whatever non-template configuration it was handed.
2. **Echo and non-improvement come apart.** On circle packing the score support is lumpy
   (0.900, 1.040, 1.300, 1.625) so many distinct configurations tie, and the strict-improvement
   rule turned most non-echo departures into non-improvements too. Minimum triangle area is
   effectively continuous: a departure that moves any point changes the score almost surely.
   The identity `accepted ≤ valid − echo` still holds, but the gap becomes informative
   instead of near-zero.
3. **It is in the same competence class.** Constructive, geometric, value-sensitive,
   expressible in the same output format (a list of coordinate pairs), scorable in a few lines.
   It is not a harder task dressed up as a generalisation.

**Validity** = parses as exactly 13 pairs, every coordinate in \[0, 1\], no two points
identical to 6 dp. **Viability** = parses as a list of pairs of any length. **Echo** =
the emitted point set equals the lineage's running parent, order-insensitive, at 6 dp —
the same definition §3 uses, transposed from circles to points.

**Seed parent.** A single fixed 13-point configuration, published by its coordinates and
its score in the runner header, identical for every lineage and every rung. It is chosen to
be non-degenerate and *mediocre*: scoring in the lower half of what a competent proposer
reaches, so there is headroom to climb, and carrying no visible symmetry, so copying it is
not disguised as producing a canonical answer.

## 3. Conditions

Same pinned ladder as §3, same inference stack, SHA-256 recorded per weight file:

| rung | file | lineages | generations | calls |
|---|---|---|---|---|
| Q4_K_M | `qwen2.5-coder-14b-instruct-q4_k_m.gguf` | 8 | 15 | 120 |
| Q2_K | `qwen2.5-coder-14b-instruct-q2_k.gguf` | 25 | 15 | 375 |

Asymmetric by design, and the asymmetry is registered rather than discovered: the primary
in §5.3 needs departures at the 2-bit rung, and the 2-bit departure rate observed across
§3's three ladders is 2%, 10% and 16% of calls. At 8% of 375 calls the expected departure
count is 30. At the symmetric allocation it would be 10, which is the count that made §3.6's
conditional question unanswerable.

Seeds are drawn from a published list of 33 values never used in any prior wave and are
fixed in the runner before execution. Q8_0 is **not** run: both prior probe waves recorded
it skipped for want of a second GPU, and registering a condition the hardware cannot serve
is what produced wave 2's FAILED verdict. Its absence is a design decision here, not a
failure, and is stated as such.

## 4. Power

All tests are exact lineage-level permutations on the difference of means, two-sided,
enumerating every split of the pooled lineages. Floors:

| comparison | splits | smallest attainable two-sided *p* |
|---|---|---|
| 25 vs 8 (accepted steps, primary) | 13 884 156 | 1.4e-7 |
| 8 vs 8 (any within-rung subgroup check) | 12 870 | 1.6e-4 |

Bonferroni across the six registered tests below is 0.05/6 = 0.0083. Both floors clear it
by orders of magnitude, which is the specific defect §3.6 discloses and this wave removes.

## 5. Registered predictions and decision rules

Each is a closed-form bound. All six go in the runner header verbatim, before execution.

**5.1 — PRIMARY. Accepted hill-climb steps per lineage.**
Mean accepted steps per lineage will be **≤ 1.5 at Q2_K** and **≥ 4.0 at Q4_K_M**.
*Refuted if either bound is violated.* (§3.6 observed 0.6 and 3.2 on circle packing at ten
generations; these bounds are stated for fifteen and are deliberately not the observed
values.)

**5.2 — SECONDARY, the form that failed before.** Fraction of lineages improving past the
seed parent at all: **≤ 0.45 at Q2_K**, **≥ 0.85 at Q4_K_M**. Registered explicitly because
its circle-packing analogue (F1) was refuted; if 5.1 holds and 5.2 fails again, that is
evidence the binary form is the wrong instrument rather than evidence against the effect,
and the pair of outcomes says so without any post-hoc choice on our part.

**5.3 — PRIMARY. Conditional-on-departure improvement rate.** Among valid non-echo outputs,
the fraction scoring above the running parent. **DECISION RULE, both branches informative:**

- Q2_K rate **≥ 0.75 × Q4_K_M rate** → quantization gates the *frequency* of departure and
  not its *quality*. This is the repairable reading, and it makes forced-departure
  interventions worth testing.
- Q2_K rate **≤ 0.50 × Q4_K_M rate** → quality degrades too; forced departure would produce
  worse proposals, not better search.
- Between → inconclusive, reported as such.
- **Power floor:** if fewer than 25 Q2_K departures are observed, the verdict is
  **UNDERPOWERED** and no branch is claimed regardless of the ratio. This clause exists
  because wave 2's addendum had to add one after the fact.

*Prior state of this question, stated here so the wave is not credited with settling more
than it settles.* Applying this rule post-hoc to the pooled fixed-parent waves (§3.6,
`sec3_conditional_quality.py`) gives Q2_K 8/10 = 80% against Q4_K_M 60/74 = 81%, with a 95%
lower bound of 44% against the 41% the collapse branch requires. **The collapse branch is
therefore already excluded on circle packing, and this wave is not testing it fresh.** What
remains open, and what this wave is powered for, is (a) whether the *frequency-only* branch
can be confirmed rather than merely left standing — the ≥ 61%-equivalent bound needs the 25
departures the existing data lack — and (b) whether either holds on a second task. The
asymmetric allocation in §3 exists to supply exactly the departures (a) needs.

**5.4 — Echo.** Coordinate-verified parent echo among valid outputs: **≥ 55% at Q2_K**,
**≤ 30% at Q4_K_M**. Lower than §3's circle-packing bound because the seed parent here
carries no template the proposer might emit for reasons unrelated to copying.

**5.5 — Template check, no analogue in prior waves.** Fraction of valid outputs scoring
exactly 0 (three or more collinear points): reported per rung with no bound. It has no
prediction attached because we have no basis for one; it exists to detect the failure mode
this task was chosen to expose, and reporting it unpredicted is honest about that.

**5.6 — Outcome.** Final best score per lineage, permutation-tested at lineage level.
**No bound is registered.** §3.6 found the outcome metric blind on circle packing at ten
generations and framed longer-horizon divergence as a prediction; fifteen generations is
not obviously long enough to settle it, and registering a bound we cannot justify would be
the error this wave exists to avoid. It is reported as a descriptive with its exact tail.

## 6. Disconfirmation

**If 5.1 and 5.4 both fail at Q2_K, the loop-level collapse does not generalise beyond
circle packing.** §3.6 would then be rewritten as a single-task observation and the paper's
scope sentence amended, not softened in place. We commit to that rewrite here so that the
commitment predates the outcome.

If 5.1 holds and 5.4 fails, the step collapse is not echo-driven on this task, and the
identity paragraph in §3.6 does not transfer — a more interesting outcome than the
confirmatory one, and the reason both are registered separately.

## 7. Analysis, fixed in advance

Computed by a script released with the wave, no arguments, from the raw ledger only:
per-lineage accepted-step vectors, echo counts, departure counts, conditional rates, the
zero-score fraction, final best per lineage, and every exact permutation tail with its split
count printed beside it. **Every registered outcome is reported with its verdict label —
held, refuted, inconclusive, or underpowered — including outcomes unfavourable to the
paper's claim, and the labels are printed by the script rather than written by us.** Two
prior waves in this paper returned unusable verdicts and both are reported; that is the
standard this one inherits.

## 8. What this wave does *not* answer

A second task at one scale in one vendor's 14B model is not generality. The cross-vendor
question — whether the collapse appears in a non-Qwen lineage at all — is untouched, and
7B's non-replication (§3.6) means scale-dependence is live. This wave answers "one task"
and nothing else, and the paper must not be edited to imply otherwise.
