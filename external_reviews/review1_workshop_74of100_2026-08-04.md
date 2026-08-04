# External review 1 — workshop compact version, scored 74/100

Received 2026-08-04 (user-supplied, external model). Target: workshop1/compact3_draft.md (pre-fix revision).

---

74 / 100

Solid, unusually honest workshop paper with a real falsifiable core. The deductions are mostly about what the result actually licenses, plus one arithmetic problem you should fix before submitting.

What's working: I checked your closed form against all seven cells and it's internally consistent to the decimals you report. The preregistration, the dual tolerance thresholds fixed in advance, the LP oracle cross-check, and especially Section 4 (reporting a result as "met as registered" while explicitly saying it fails Holm and is driven by one cell) are better practice than most of what lands at workshops. The "we do not claim to have measured the in-loop distribution" guard and the non-claim guard on mechanism are the right instincts.

Deduction 1: N = 35 is not a trap, and it's one of your seven cells (−8). Your own value function proves this. At N = 35, truncation gives 35/12 = 2.9166667. The best available extend-and-fill alternative is V(5,10) = 2.9142136. Truncation wins by 0.0025. Same at N = 48 and N = 63, and at N = 14, 15 the alternative isn't even reachable because fillers cap at (k−1)². The general condition: at N = k²−1, truncation beats the alternative whenever k ≥ 6. So the top of every trap zone from k = 6 up is not a trap at all. Gaps: 13 +0.151, 21 +0.159, 31 +0.165, 43 +0.170, 17/35/37 0.000. Fix: rename "trap" to something branch-neutral or restrict zones; put the gap column in the table.

Deduction 2: the baseline is a strawman in the arm that matters (−7). "Round numbers hit 2 of 69" tells a reviewer nothing. You already know the right null (uniform over template shapes, ~1/3) — you use it for the rectangle. Apply it to the square cells; 56-86% still beats it.

Deduction 3: four of seven cells have n = 4 (−6). Wilson on 3/4 is roughly [30%, 95%]. Three genuinely powered cells (13, 21, 31). Top up to n≈15 or report CIs and say plainly four cells are underpowered.

Deduction 4: external validity gap bigger than acknowledged (−5). FunSearch island reset seeds from best program of surviving island; AlphaEvolve always conditions on parents. "Demonstrably exist inside the cited systems" needs citation or softening. Larger: those systems sample programs, you sample coordinates — a code-emitting arm might not template at all. 30-invocation code arm at N = 13, 21, 31 would close most of this.

Deduction 5: 10⁻⁶ tolerance may measure decimal precision, not geometry (−4). Grid template survives rounding because 1/(2k) is a clean decimal; gasket radii are irrational, so the same emitted precision produces overlap — tolerance penalizes the ambitious arm. Fix: report overlap magnitude distribution + shrink-repair rescoring. If opus_alias failures are 10⁻⁵ overlaps, the ladder story changes.

Deduction 6: unattributable number in the abstract (−3). "78% → 100% → 13%" headline includes the alias arm. Move to appendix or state as two attributable tiers plus flagged observation.

Deduction 7: "predictable to seven decimals" oversells (−2). Prediction is categorical (which template); decimals are free once template known.

Deduction 8: presentation (−1). Zero figures in three pages. One plot: N on x, predicted / empirical mode / best-in-family.

No-points flags: GM2 0/140 should update you on your parser (single format-convention limitation); and lead with "0 of 11 reached the rival argmax" — negative claim needs no null baseline.

If you only fix three things: the N = 35 arithmetic, the baseline, and the tolerance confound.
