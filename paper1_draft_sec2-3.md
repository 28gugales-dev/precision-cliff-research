# Sections 2–3 (draft)

<!-- Numbers sourced from n_sweep_forecast.py/.json, rect_forecast.py/.json, arm_f_repro.py,
     arm_f_prompts.json, arm_g_rect.py, STATE.md §§v8–v9. Citations left as [SLOT]. -->

## 2. Task and recipe family

### 2.1 The benchmark

The benchmark is maximizing the sum of radii of *N* non-overlapping circles in the unit square.
Feasibility is decidable exactly from the emitted coordinates, and published best-known lower
bounds exist for small *N* [SLOT: related-work], so proposals score with no human in the loop.

All invocations are zero-shot and code-free. The prompt (Appendix A.5, verbatim) fixes the count,
states containment and non-overlap, forbids writing or executing code ("construct the packing by
reasoning alone"), and demands only a raw Python list of `[x, y, r]` triples. Given a code channel
the model delegates to an optimizer and the distribution reflects the optimizer. Zero-shot
sampling substitutes for the evolutionary loop on the prior finding that the loop reduces to
best-of-N here; Section 8 flags the substitution.

### 2.2 The recipe family

In prior arms, 94 of 95 valid coordinate-space proposals were grid-plus-filler constructions. The
family is parametric, not memorized, and admits an exact value function. A *k×k* grid places one
circle per cell centre with *r*_grid = 1/(2*k*); *m* fillers sit on interior grid vertices, each
tangent to its four surrounding grid circles, with *r*_filler = (√2 − 1)/(2*k*),
0 ≤ *m* ≤ (*k*−1)². Hence

    V(k, m) = k/2 + m(√2 − 1)/(2k).

When *N* < *k*² the observed behaviour is not to drop to a smaller grid and fill it, but to
*truncate*: lay out the *k×k* lattice, occupy only *N* cells, leave the radius unchanged.

    T(k, N) = N/(2k),   N < k².

These reproduce every previously reported anchor with no fitting: V(5,1) = 2.5414214,
V(5,2) = 2.5828427, V(5,0) = 2.500, T(5,23) = 2.300 (the observed trap at *N* = 23) and
V(4,7) = 2.3624369 (the one escaping seed there). Five of five.

### 2.3 The selection rule

The recipe does not say which *k* the model reaches for, and supplying that turns description into
forecast. Four candidates — nearest integer square root, floor, ceiling, value-argmax over the
family — were scored against the three anchors, requiring both *k* and branch to match. One
survived (`nearest` 3/3, `floor` 2/3, `argmax` 2/3, `ceil` 1/3):

    k*(N) = ⌊√N + ½⌋ = round(√N)
    k*² ≤ N  →  extend with m = N − k*² fillers   (converge)
    k*² > N  →  truncate                          (trap)

Zero free parameters. Three anchors against four candidates is *identification*, not confirmation,
and we do not soften that; its value is that every other *N* becomes out-of-sample.

The rule ignores whether a better member of the family exists. The governing quantity is the
signed distance *N* − *k*², non-negative converging and negative trapping. Primality is not the
variable — 13, 23, 31, 43, 47 and 59 trap while 11, 17, 19, 29, 37, 41 and 53 converge — refuting
the prior work's conjecture about primes near 30 before any model is queried.

### 2.4 Trap zones and their cost

Substituting *k**(*N*) into the branch condition gives the zones in closed form:

    TRAP:     N ∈ [k² − k + 1, k² − 1]
    CONVERGE: N ∈ [k², k² + k]

Over the swept range *N* = 10…60: [13,15] (*k*=4), [21,24] (*k*=5), [31,35] (*k*=6), [43,48]
(*k*=7), [57,60] (*k*=8).

<!-- NOTE (not a conflict): the k=8 zone is [57,63] by the formula; [57,60] is that zone clipped
     by the sweep bound, sweep(10, 60) at n_sweep_forecast.py:340. Worth a clause in the caption
     so a reader checking the formula does not think it disagrees. -->

Inside a zone the rule loses value against the best construction available *within the recipe
family itself*. The worst-in-zone penalty falls as *N* grows — 8.51% at *N* = 13, 7.03% at 21,
6.01% at 31, 5.25% at 43, 4.66% at 57 — and hits exactly zero at the top of each zone (*N* = 35,
48), where truncation happens to *be* the recipe optimum. Those traps are indistinguishable from
convergence by value, separable only by structure; Section 3.2 uses one as a control. The family
is also never competitive with the record: its deficit against published lower bounds runs
0.02–0.26 across *N* = 10…30 and is 0.0946 at *N* = 26.

Every closed-form value is recomputed by an independent linear program over the constructed
coordinates, which knows nothing about the recipe; the script aborts on disagreement, and on any
predicted value exceeding a published lower bound. 83 configurations, both branches, every *k* in
2…7, drift below 1e-9.

[FIGURE 1: Predicted-versus-optimal value, N = 10…50. Curve (i): the rule's prediction — V(k*, m)
on the converge branch, T(k*, N) on the trap branch. Curve (ii): the best value attainable
anywhere in the recipe family. Shade trap zones [13,15], [21,24], [31,35], [43,48]; the gap inside
each band is the self-inflicted penalty, labelled with its worst-in-zone percentage (8.51%, 7.03%,
6.01%, 5.25%). Mark N = 35 and N = 48, where the gap closes to zero. Data:
n_sweep_forecast.json.]

## 3. Preregistered forecast, out of sample

### 3.1 Registration protocol

Because the rule was identified on three points, everything downstream depends on predictions
being fixed before sampling. For each cell the prompt is pinned and its SHA-256 digest written to
disk first — the *N* = 13 square prompt hashes to `32db485b…` in `arm_f_prompts.json`. Predictions
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
and an exact one — at *N* = 31, *r* = 0.0833 summing to 2.5823 against an exact 2.5833333.

### 3.2 Square container

The square arm sampled Haiku-tier proposers at *N* = 13, 17, 21, 31, 35, 37 and 43. The rule was
fitted on *N* = 23/26/27 only, so every cell is out of sample.

Four cells are *discriminating*: rule and family optimum disagree, so a proposer that searched the
family rather than recalling the nearest square would return a higher number. Across those cells
(*N* = 13, 21, 31, 43), **18 of 23 valid invocations landed on the predicted construction**, and
the rival-argmax value was reached **2 times in 23** — both at *N* = 21, both the 4×4 grid plus
five fillers at 2.2588835. Pooled with the rectangle cells below, the rival rate wherever rule and
optimum disagree is **2/34**.

That the anchor first breaks at *N* = 21 is informative: it is the smallest trap zone tested and
carries the largest relative penalty (7.0%), so the anchor looks weakest where obeying it costs
most — a hypothesis, not a finding, pending the other zone-bottoms.

**P4** registered *N* = 37 as converging cleanly on 3.0345178, a 6×6 grid plus one filler at
(√2−1)/12 — a prime predicted clean, contradicting the prior work's own guess. It confirmed.
**P5** registered *N* = 35 at 2.9166667, the top-of-zone control where truncation is also the
recipe optimum; three of four valid samples landed there, separable from convergence only because
the structure classifier reads the radii rather than the total. The fourth used a 7×7 lattice
truncated to 35 (*r* = 1/14, sum 2.5), outside the rule entirely.

Bookkeeping that would otherwise corrupt these rates: five invocations were rejected by the
runtime's 20-subagent concurrency cap *before reaching a model*, and scoring them invalid would
have understated validity by 17%; two parse failures occurred in previously logged modes (`1/12`
fractions, a list wrapped in prose containing `[0,1]x[0,1]`); one *N* = 37 proposer derived
*r* = (√2−1)/12 correctly in prose, then transcribed 0.03571429.

### 3.3 Rectangle transfer

One container with a one-parameter template is the obvious weakness, so we restated the rule for a
1 × *a* rectangle, where the template has two free parameters:

    q* = round(√(N/a))    columns across the width 1
    p* = round(√(N·a))    rows across the height a

At *a* = 1 both collapse to round(√N): the same rule with the aspect ratio put back in, not a new
rule fitted to new data, and no rectangle model output existed when it was written. It was
verified against an independent LP at 213 configurations, drift below 1e-9, including a
cross-domain check — at *a* = 1 with *p* = *q* = *k* the square file's closed form must equal this
file's LP. Two files, two derivations, one number.

Shape mismatch grows sharply as *a* leaves 1: over *N* = 10…45 the count of *N* whose predicted
shape differs from the optimal one rises from 12 at *a* = 1.0 to 23 at *a* = 1.5, 20 at *a* = 2.0
and 23 at *a* = 3.0, worst gaps 8.5% (*N* = 13), 7.8% (*N* = 31), 10.3% (*N* = 25), 11.4%
(*N* = 19).

We probed the two sharpest cells with sixteen proposers, in a container none had been given
before: *N* = 19 at *a* = 3 (predicted 3.1666667, an 8×3 truncation; rival 3.5749194, a 7×2 grid
extended with five fillers) and *N* = 25 at *a* = 2 (predicted 3.1250000, a 7×4 truncation; rival
3.4832492, a 6×3 grid extended with seven fillers). With all sixteen scored, **5 of 11 valid
proposals landed on the predicted value and 0 of 11 reached the rival**. Nearest-template
anchoring is not an artefact of the one-parameter square case.

<!-- CONFLICT: skeleton §3 states "5/9 valid on-prediction, 0/9 rival" for the rectangle arm.
     That is STATE.md §5, written before the last two invocations landed. STATE.md "Running
     totals across both domains" supersedes it with all 16 scored: N=19/a=3 → 4/8 valid, 2
     on-prediction, 0 rival; N=25/a=2 → 7/8 valid, 3 on-prediction, 0 rival; totals 5/11 and
     0/11. The skeleton's own combined figure of 2/34 already assumes the corrected denominator,
     so 5/9 and 2/34 cannot both hold. Draft uses 5/11, 0/11. -->

Two qualifications are recorded rather than smoothed. Validity degrades in the tall container —
4/8 at *a* = 3 against 7/8 at *a* = 2, three of the four *a* = 3 failures being overlaps — a
separate finding and a confound on that cell, on *n* = 8. And one *a* = 3 sample beat the
prediction from outside the family altogether: five circles at *r* = 0.1, ten at *r* = 0.25, four
at *r* = 0.125, summing to 3.5, still below the 3.5749194 rival. The recipe is the attractor, not
a ceiling.

### 3.4 Negative result: the closed form does not survive the move to rectangles

The rectangle generalizes the *rule* but not the *formula*. We keep the failure because it is what
a verification gate is for.

In the unit square every interior vertex has four identical neighbours, so one expression covers
every filler. In a 1 × *a* rectangle, with half-spacings *h*ₓ = 1/(2*q*) and *h*ᵧ = *a*/(2*p*), a
filler is capped by three competing quantities: the diagonal gap to the four surrounding grid
circles, and the horizontal and vertical spacing to *adjacent fillers*. The latter two are
inactive when *h*ₓ = *h*ᵧ — why the square case could not have revealed them — and bind only when
the neighbouring vertices are occupied. The cap therefore depends on *m* and on which vertices a
construction uses, and no expression in (*p*, *q*, *m*, *a*) reproduces it.

The LP gate caught this on the first run. At *a* = 1, *p* = 2, *q* = 4, *m* = 1 the natural
generalization `rf = min(diag, hₓ, hᵧ)` returns **1.125** against a true **1.1545085**: it caps
against a neighbouring filler that, with one filler placed, does not exist. We retain closed forms
only where provably exact — full grid and truncated grid — and use the LP as the value oracle for
the extend branch. The pipeline aborted on drift rather than propagating a plausible formula, so
what Section 3.3 tests is the LP-backed prediction.

[TABLE 1: Forecast versus outcome, both containers, one row per cell. Columns: cell | predicted
branch and value | rival-argmax | valid/sampled | on-prediction/valid | rival hits. Square rows:
N=13 truncate 1.6250000 (rival 1.7761424); N=17 extend 2.0517767†; N=21 truncate 2.1000000
(2.2588835); N=31 truncate 2.5833333 (2.7485281); N=35 truncate 2.9166667†; N=37 extend
3.0345178†; N=43 truncate 3.0714286 (3.2416246). Rectangle rows: N=19/a=3 truncate 3.1666667
(3.5749194); N=25/a=2 truncate 3.1250000 (3.4832492). Footer: square discriminating cells 18/23
on-prediction, rival 2/23; rectangle 5/11, rival 0/11; combined 2/34. † non-discriminating
(predicted equals family argmax), excluded from rival denominators. Data: arm_f_repro.py over
arm_f_candidates.jsonl and arm_g_rect.py over arm_g_candidates.jsonl.]
