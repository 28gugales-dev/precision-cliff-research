## Score (0-100) and one-line verdict

**80/100 — A dense, unusually honest 3-pager: every major caveat (alias, underpowered cells, branch-neutral trap framing, Holm failure) is on the page, but one real numeric inconsistency (100 vs 120 trace-arm invocations) and an unreproducible pooled statistic keep it from clean acceptance.**

## Deductions (numbered, points each, one-line fix each)

**Spot-check (5, arithmetic shown):**

1. N=13 → k\* = round(√13) = round(3.606) = 4; k\*² = 16 > 13 → truncate; T(4,13) = 13/(2·4) = 13/8 = **1.6250000** ✓ (table row matches; gap +0.1511 > 0 consistent with trap).
2. N=17 → k\* = round(√17) = round(4.123) = 4; 16 ≤ 17 → extend, m = 1; V(4,1) = 4/2 + 1·(√2−1)/8 = 2 + 0.4142136/8 = **2.0517767** ✓ (table row matches, gap 0 consistent with converge).
3. N=35 → k\* = round(√35) = round(5.916) = 6; 36 > 35 → trap; T(6,35) = 35/12 = **2.9166667** ✓ (gap 0 correctly reported — branch-neutral framing holds; N=35 is k²−1, k=6 ≥ 6, truncation value-optimal).
4. N=43 → k\* = round(√43) = round(6.557) = 7; 49 > 43 → trap; T(7,43) = 43/14 = **3.0714286** ✓ (table row matches).
5. Trace arm §4: 53/60 + 50/60 = **120 invocations**, but the text says "100 new invocations" ✗ (secondary arithmetic inside the same numbers checks out: 46/53 = 86.8% → 87% ✓, 35/50 = 70% ✓, 54/56 = 96.4% ✓, 5/11 = 45.5% → 45% ✓, Wilson intervals [30%, 95%] on 3/4 and [21%, 72%] on 5/11 both recompute exactly ✓).

1. **−6 — "100 new invocations" contradicts its own denominators.** Spot-check 5: 53/60 + 50/60 implies 120 sampled, not 100. Fix: state 120 (or correct the fractions); the inconsistency is inherited from the long version, so fix it in the ledger first.
2. **−4 — "Pooled across every tier and container the on-prediction rate is 46%" is not reproducible from the page.** Sample-weighted from the numbers given (square 50/69, rect 5/11, trace 81/103, tier 35/45 + ~0/34) gives ~65%; 46% only reproduces as an unweighted mean of the six arm-level rates. Fix: name the pooling (or cite the ledger line) or the claim reads stronger than the page supports.
3. **−3 — "the cells where value is genuinely left on the table are N = 13, 21, 31, 43" is categorical with no threshold.** N=15 and N=24 also lose value to the drop-and-fill alternative (≈0.04 and ≈0.01 by the same V/T arithmetic) — "genuinely" is doing unstated threshold work, and N=24's loss (0.014) is only ~6× the margin by which truncation wins at N=35 (0.0025). Fix: "the largest gaps (0.15–0.17) are at N = 13, 21, 31, 43".
4. **−2 — "rules out a tolerance artifact behind that 13%" is too strong for a post-hoc diagnostic on n=26.** Fix: "finds no evidence of a tolerance artifact in this sample".
5. **−2 — Rectangle rule reduced to symbol names.** The out-of-sample claim is that the *restated* rule transfers; the compact says "(q\*, p\*, collapsing to round(√N) at a = 1)" but never states q\* = round(√(N/a)), p\* = round(√(N·a)). Fix: one line restores the rule the reader is being asked to evaluate.
6. **−1 — "not primality" is now assertion-only.** The long version's exemplar lists (13, 23, 31, 43, 47, 59 trap vs 11, 17, 19, 29, 37, 41, 53 converge) were the single most convincing falsifier of the primality alternative and were cut. Fix: restore one of the two lists inline.
7. **−1 — No figure in a 3-page format.** fig1 (prediction vs family, gap segments) and fig2 (tier ladder) exist as committed assets; a compact whose page budget can absorb one figure ships none. Fix: embed fig1 — it carries the trap-zone story at a glance.
8. **−1 — Rival-value suppression (1/53 vs 2/50), reported as "confirmed as registered" in the long version, is cut.** A preregistered outcome silently absent makes the registered-outcome accounting look incomplete. Fix: one clause.

**Required checks that PASS (no deduction):** underpowered n=4 cells are flagged explicitly with Wilson [30%, 95%] and "replications, not independent confirmations" (§2) ✓; opus_alias caveat present in abstract and §3 ("no attestable weights binding", "never referred to as any specific dated model") ✓; trap-zone framing is branch-neutral — "Trap names the branch, not a guaranteed value loss", N=35 gap 0 ✓; Holm failure (0.0167 vs 0.0325) reported, finding "met as registered, never demonstrated" ✓; abstract "identifies the modal output" is hedged as categorical-identification-not-evidence ✓; out-of-sample reported as "partial support, not confirmation" against the 1/3 null ✓.

## What the 3-page version cut that it should not have

1. **The rectangle rule's formulas** (q\* = round(√(N/a)), p\* = round(√(N·a))). The transfer claim rests on a rule that was "restated but never refitted" — naming the parameters without the rule makes the strongest claim in §2 uncheckable by the reader.
2. **The primality counterexample lists.** "Trap zones track signed distance, not primality" is the paper's best falsification move against a natural confound, and the compact kept the assertion but cut its only concrete support.
3. **Rival-value suppression (1/53 vs 2/50).** A registered outcome from the trace arm; its absence weakens the completeness of the preregistration narrative.
4. **The rectangle LP-oracle grounding (213 configurations).** The square keeps its 83-configuration oracle note; the rectangle's oracle check disappears entirely, so the out-of-sample section's strongest verification line is asymmetric where it matters most.
5. **One figure.** 3-page workshop papers are judged on first-glance evidence transfer; the committed fig1/fig2 assets are unused.

## Top 2 actions

1. **Fix the 100/120 invocation inconsistency and pin the 46% pooled rate to a defined pooling (or the ledger line)** — these are the only two numbers a hostile reader can break, and both are one-line fixes that currently force a "can I trust the rest?" moment.
2. **Restore the rectangle formulas and one primality exemplar list** — one line each, both load-bearing for the two claims (out-of-sample transfer; branch rule vs primality) that a workshop reviewer will attack first.
