# Round 2 Verification — Review 6 (same adversarial pool as reviews 4 & 5)

Review 4 (full paper, 72/100) and Review 5 (compact, 80/100) issued 16 deductions across
two documents. The authors claim to have fixed them all; two refutations are claimed
(Review5 D1 and D3). This verification checks every deduction against the current text
and independently verifies the arithmetic behind both refutations.

---

## Review 4 Deductions — Full Paper (paper1_draft.md)

### D1 (-8): Abstract misrepresents rectangle transfer
**Verdict: FIXED**

Current abstract (line 24-27): "tested them out of sample on two containers, a square
and a rectangle, for which the rule was restated but never refitted; rectangle support is
partial — 5 of 11 valid samples on-prediction, not separable from a uniform-template null,
though 0 of 11 reached the provably higher-scoring rival construction."

Evidence: the qualification ("partial support", null stated, 5/11, 0/11 rival) is now in
the abstract. No mismatch with body §4.

### D2 (-5): Abstract-to-body mismatch — wave confound missing from elicitation summary
**Verdict: FIXED**

Current abstract (line 33-36): "p = 0.03 uncorrected — failing Holm over the registered
family, carried by one of three cells and confounded with a collection-wave split of
comparable size"

Evidence: "confounded with a collection-wave split of comparable size" is in the abstract.
Body §6.4 has the full diagnosis. No mismatch.

### D3 (-4): Appendix ordering cross-reference confusion
**Verdict: FIXED**

Evidence: Appendix B = Table 4 (Deviations, line 948), Appendix C = Table 5 (Corrections,
line 970). Preamble (line 6): "the deviations table is Table 4 (Appendix B), and the ledger
correction ... Table 5 (Appendix C)." All cross-references re-pointed. Table 4 precedes
Table 5 as requested.

### D4 (-3): N=26 deficit arithmetic — "precisely" + precision drop
**Verdict: FIXED**

Current text (line 146): "0.0946 at N = 26 (2.63598 − 2.5414214 = 0.0945586)"

Evidence: full subtraction shown to 7 decimals, "precisely" dropped, rounded value given
alongside the exact difference.

### D5 (-2): Abstract monotonicity ambiguity
**Verdict: FIXED**

Current abstract (line 27-31): "constructive ambition rises monotonically with nominal
tier while execution validity does not — it rises then collapses (78% → 100% → 13%)"

Evidence: "rises monotonically ... rises then collapses" — matches reviewer's suggested fix.

### D6 (-2): Opus_alias latency/token anomalies unreproducible
**Verdict: FIXED**

Current text (lines 437-439): "we therefore treat both as anecdotal context from an
unreleased session transcript, not as data-supported properties of the tier"

Evidence: anomalies downgraded to anecdotal. Transcript release remains a user decision,
not a paper requirement per the fix applied.

### D7 (-1): §1.1 penalty coverage gap understated
**Verdict: FIXED**

Current text (Figure 1 caption, lines 153-157): "These are family-internal arithmetic and
exact at every N, while the published-bound comparison (curve iii) is checkable only up to
N = 30, where the bound table stops."

Evidence: the distinction between family-internal penalties (exact at all N) and
published-bound comparison (stops at N=30) is explicit. Penalty values for N=43 and N=57
remain in the text because they are family-internal arithmetic, not bound-table-dependent.

### D8 (-1): Missing structural k-match in mode-ceiling table
**Verdict: FIXED**

Current text (§3.2 table, lines 256-271): column "k*-structure / valid†" added with the
post-hoc footnote: "All 50 of 50 on-prediction samples are k*-structured ... 64 of 69 valid
samples overall (93%) sit on the k* grid."

Evidence: structural verification column present, disclosed as post-hoc, strengthens the
template claim. Arithmetic verified: 50 on-pred = 10+3+12+13+3+3+6 ✓, 69 valid =
18+4+15+17+4+4+7 ✓, 64 k*-structured = 17+3+13+17+3+4+7 ✓.

---

## Review 5 Deductions — Compact (compact3_draft.md)

### D1 (-6): "100 new invocations" contradicts denominators
**Verdict: AUTHORS-REFUTED-CORRECTLY**

Reviewer's claim: 53/60 + 50/60 implies 120 sampled, not 100.

Authors' response: 100 new = 40 new bare + 60 new trace; 20 of 60 analyzed bare rows are
pre-existing arm-F samples (disclosed in full paper §6.1).

**Independent arithmetic verification:**
- New invocations: 40 bare + 60 trace = 100 ✓
- Analyzed bare: 20 old + 40 new = 60 ✓
- Analyzed trace: 60 new = 60 ✓
- Total analyzed: 120 rows, of which 100 are new ✓
- The statement "100 new invocations" is correct; the 20 pre-existing rows were known and
  disclosed.

Current compact text (line 155-157): "A preregistered scaled arm (100 new invocations:
40 bare + 60 trace; 20 of the 60 analyzed bare rows are pre-existing arm-F samples,
disclosed in the preregistration)"

Evidence: decomposition now inline, making the relationship explicit.

### D2 (-4): "46% pooled rate" not reproducible from page
**Verdict: FIXED**

Current compact text (line 117): "Pooled across every tier and container the on-prediction
rate is 46% (47/102 valid samples)"

Evidence: fraction restored. The 47/102 matches the full paper's disclosure.

### D3 (-3): "genuinely left on the table" — N=15/N=24 also lose value
**Verdict: AUTHORS-REFUTED-CORRECTLY (N=15) + FIXED (N=24)**

**N=15 refutation — independent arithmetic:**
- k* = round(√15) = 4, k*² = 16 > 15 → trap branch
- Alternative: drop to k=3 (9 grid circles), need m = 15−9 = 6 fillers
- Filler cap on 3×3 grid: (3−1)² = 4
- 6 > 4 → NO reachable family alternative. Drop-and-fill is impossible at N=15.

**N=24 residual:**
- T(5,24) = 2.4000000; V(4,8) = 2.4142136; gap = 0.0142136 = 0.59%
- This loss is real and now acknowledged.

Current compact text (line 49-50): "the largest losses are at N = 13, 21, 31, 43
(gaps 0.15–0.17), with a small residual at N = 24 (0.014, i.e. 0.59%)"

Evidence: N=15 correctly excluded (impossible in family), N=24 residual acknowledged,
"genuinely" hedging dropped.

### D4 (-2): "rules out a tolerance artifact" too strong for n=26
**Verdict: FIXED**

Current compact text (line 143-144): "A post-hoc diagnostic ... finds no evidence of a
tolerance artifact behind that 13% in this sample"

Evidence: "finds no evidence ... in this sample" matches reviewer's suggested fix.

### D5 (-2): Rectangle rule formulas cut
**Verdict: FIXED**

Current compact text (line 122): "q* = round(√(N/a)) rows of p* = round(√(N·a)) columns,
collapsing to round(√N) at a = 1"

Evidence: full formulas restored inline.

### D6 (-1): "not primality" assertion-only; prime lists cut
**Verdict: FIXED**

Current compact text (lines 50-52): "Trap and converge zones both contain primes (trap:
13, 23, 31, 43, 47, 59; converge: 11, 17, 19, 29, 37, 41, 53), which is what rules
primality out as the driver."

Evidence: both lists restored inline. Membership re-verified: 6 trap primes, 7 converge
primes. All correct.

### D7 (-1): No figure in 3-page format
**Verdict: FIXED**

Current compact text (lines 99-101): "Figure 1 (repository asset `workshop1/figs/fig1.png`)
plots the prediction against the best-in-family value ... Figure 2 (`fig2.png`) shows the
tier ladder of §3."

Evidence: figure pointer paragraph added. Assets committed.

### D8 (-1): Rival-value suppression (P-T2) cut from compact
**Verdict: FIXED**

Current compact text (line 166): "A second registered outcome, rival-value suppression, was
also met as registered (1 of 53 valid trace samples hit the rival vs 2 of 50 bare;
directional, no inferential weight claimed)."

Evidence: P-T2 clause restored with numerator/denominator and caveat.

---

## New-problem scan

### Cross-references between abstract and body

- Full paper abstract (line 24): "rectangle support is partial — 5 of 11 valid samples"
  matches body §4.1 (line 342): "5/11 = 45%". ✓
- Full paper abstract (line 28): "78% → 100% → 13%" matches body Table 2 and §5. ✓
- Full paper abstract (line 31): "an unattributable serving alias" matches body §5
  opus_alias caveats. ✓
- Compact abstract (line 23): "78% → 100% → 13%" matches compact §3 (line 147). ✓
- Compact abstract (line 20): "5 of 11 valid samples on-prediction" matches compact §2
  (line 124). ✓
- Compact abstract (line 26): "p = 0.03 uncorrected — failing Holm" matches compact §4
  (line 161-162). ✓

**No abstract-body contradictions found.**

### Table/footnote consistency

- Full paper Table 1 (line 369-384): N=13 valid 4/5·18/20 matches §3.3 original 45-invocation
  vs full-ledger split. Full-ledger 41/57 and 2/57 stated in table legend. ✓
- Full paper Table 3 (line 565-572): bare 60/trace_v2 60 denominators consistent with §6.1's
  decomposition (85 bare = 45 orig + 40 new; 60 analyzed = 20 pre-existing + 40 new). ✓
- Compact §2 table: on-prediction rates match full paper to 1 significant digit after
  rounding. Minor: N=31 compact says 76% (13/17) while full paper also says 76%. ✓
- Compact says "56–86% by cell" — range matches table (56% at N=13, 86% at N=43). ✓
- Full paper "46% (47/102 valid samples)" vs compact "46% (47/102 valid samples)". ✓

### k-match paragraph numbers
**Verified independently above:** 50 on-pred = 10+3+12+13+3+3+6 = 50. 69 valid =
18+4+15+17+4+4+7 = 69. 64 k*-structured = 17+3+13+17+3+4+7 = 64. All correct.

### Trace arm cross-document consistency

- Compact (line 158): "53/60 trace vs 50/60 bare, p = 0.30"
- Full paper (line 539): "53/60 (88%) trace_v2 against 50/60 (83%) bare ... p = 0.30"
  **Consistent.** ✓

- Compact (line 161): "87% (46/53) of trace-arm valid samples"
- Full paper (line 554): "46 of 53 trace_v2 (87%)"
  **Consistent.** ✓

- Compact (line 170): "54 of 56 scoreable claims (96.4%)"
- Full paper (line 559): "54 of 56 (96.4%)"
  **Consistent.** ✓

### Potential minor issues found

1. **Compact §2 table N=31 on-prediction rate**: The table says "13/17" (76%) but the
   paragraph above says the predicted value equals the empirical modal output. The
   predicted value is T(7,31) = 31/14 = 2.2142857... wait no. 31/14 ≈ 2.2143. But the
   table row shows 2.5833333.

   Let me re-check: N=31, k* = round(√31) = round(5.568) = 6. k*² = 36 > 31 → trap.
   T(6,31) = 31/12 = 2.5833333. That's the value in the table. ✓. The gap column
   says "+0.1652". The best-in-family value at N=31 would be V(5,6) = 5/2 + 6(√2−1)/10 =
   2.5 + 6×0.4142136/10 = 2.5 + 0.248528 = 2.748528. Gap: 2.748528 − 2.583333 = 0.165195.
   Rounding: 0.1652. ✓.

   On-prediction: 13/17 = 76.47%. Table says 76%. ✓. But the full paper table says 13/17
   with on-prediction rate 76% — same. ✓.

   Actually, 13/17 = 0.7647... which rounds to 76%. But wait — the full paper §3.2 table
   says 76% for N=31 but the on-prediction/valid is 13/17. 13/17 = 76.47%, rounds to 76%.
   That's correct.

2. **Compact §2 says "gap to best-in-family" for N=35 is 0, N=37 is 0, N=17 is 0.**
   Let me verify: N=17, k*=4, extend, m=1. V(4,1)=2.0517767. Is 2.0517767 the family
   optimum? k*²=16 ≤ 17, extend with m=1 filler. The family optimum at N=17 with k=4 and
   max m=(4-1)²=9 would be V(4,9)=2+9×0.4142136/8=2+0.46599=2.46599 > 2.0518. So why is
   the gap 0?

   The gap is from the predicted value to the best-in-family value. For N=17, the
   prediction is V(4,1). But the family best is V(4,9) — using all possible fillers on a
   4×4 grid. That's a different construction. The paper's terminology: "gap to
   best-in-family" means the gap from the predicted construction to the best value
   achievable within the recipe family. For N=17, the prediction is extend-and-fill with 1
   filler. The best-in-family would be... hmm.

   Actually, re-reading §2.2: the recipe family with k*(N) grid uses m = N − k*² fillers
   (up to (k−1)²). For N=17, k*=4, m=1, that's within cap. The value is V(4,1)=2.0517767.
   The rival argmax within the family would try different k. At k=3, V(3,8)=1.5+8×
   0.4142136/6=1.5+0.5523=2.0523... wait that's close. But the paper says N=17 is
   non-discriminating — prediction equals family argmax.

   Actually, this is about the gap from prediction to rival within the *same* branch. For
   non-discriminating cells, the prediction equals the best the family can do at that N,
   so gap=0. For discriminating cells (trap zones), the prediction is truncation and the
   rival is drop-and-fill. N=17 is extend-and-fill, so the branch rule produces the optimal
   family construction. The gap=0 is correct under the paper's definition.

   Actually, I realize I'm overthinking this. The gap column is "gap to best-in-family"
   meaning best value achievable by any construction in the recipe family. For converging
   cells (extend-and-fill), the prediction IS the family optimum because the branch rule
   picks the right k and fills to capacity. gap=0. For trap cells (truncate), the
   prediction is truncation and the family optimum is drop-and-fill. gap > 0. This is
   consistent throughout the paper. ✓

**No new problems found.** All cross-references consistent, all arithmetic verified, no
contradictions introduced.

---

## Revised Scores

### Full paper (paper1_draft.md): 88/100

All 8 deductions addressed. The mode-ceiling result is now structurally verified (k-match
column). The abstract properly scopes the rectangle as partial support. The wave confound
is disclosed in the abstract. Appendix ordering is logical. The opus_alias anomalies are
properly downgraded.

Remaining weaknesses are acknowledged limitations, not fixable errors: rectangle transfer
is weak (5/11, CI [21%,72%]), the trace result is fragile (fails Holm, one-cell driver,
wave confound), single-vendor scope, opus_alias provenance. These are properly disclosed
and do not block submission.

### Compact (compact3_draft.md): 93/100

All 8 deductions addressed. Two were refuted (D1: 100 new is correct; D3: N=15 has no
family alternative). The remaining six are fixed. The 3-pager is unusually honest for its
format — every major caveat is on the page, all numbers are internally consistent, and
the core mode-ceiling result is well-supported.

### Submission readiness

**Both documents are submission-ready.** The full paper is suitable for arXiv or a venue
that accepts technical reports with self-disclosed limitations. The compact is
workshop-ready — dense, honest, with the strongest result (mode-ceiling identification)
leading and properly scoped.

The compact benefits from being tested against a hostile reviewer: no number on the page
can be broken. The single improvement worth considering pre-submission is whether the
compact should carry a one-line disclosure of the trace arm's wave confound (the abstract
has it at line 27, but §4 does not restate it — the full paper's §6.4 diagnosis is
compressed to "confounded with a collection-wave split" in the abstract only). Minor.
