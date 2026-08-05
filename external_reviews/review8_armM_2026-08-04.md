# External Review 8 — Arm M Delta + Full Paper, 90/100

Reviewers 4 and 6, post-arm-M addition. Verdict: 90/100, submission-ready YES, top remaining action: one-parent mutation arm (§8).

---

## 1. Scoring claims independently verified

Ran `arm_m_analysis.py` over `arm_m_collect.jsonl`:

| N | sampled | parse fail | valid 1e-6 | valid 1e-9 | on-pred | modal value (count) | modal=pred? |
|---|---------|-----------|-----------|-----------|---------|--------------------|------------|
| 20 | 15 | 0 | 15 | 15 | 1 | 2.0 (12) | False |
| 30 | 15 | 1 | 14 | 11 | 0 | 2.499989 (11) | False |
| 41 | 12 | 0 | 7 | 6 | 0 | 2.9285714 (6) | False |
| 57 | 15 | 0 | 10 | 8 | 6 | 3.5625 (6) | True |

N=57 rival hits: 0. F-M1: 3/3 TRIGGERED. F-M2: not triggered.

All match paper §3.4 exactly.

### Arithmetic on modal values

- T(5,20) = 20/10 = **2.0** (12 of 15 valid; 5×4 rectangle exact fill)
- T(6,30) = 30/12 = **2.5** (11 of 14; 6×5 exact fill; report 2.499989 is empirical bucket-mean, within 2e-3 window)
- T(7,41) = 41/14 = **2.9285714** (6 of 7; 7×6 minus one)
- T(8,57) = 57/16 = **3.5625** (6 of 10; 8×8 truncated to 57)
- V(4,4) = 2 + 4(√2−1)/8 = **2.2071068**
- V(5,5) = 2.5 + 5(√2−1)/10 = **2.7071068**
- V(6,5) = 3 + 5(√2−1)/12 = **3.1725890**
- V(7,8) = 3.5 + 8(√2−1)/14 = **3.7366935**

All correct. The one on-pred sample at N=20 (slot s4, sum=2.2071068) is a textbook V(4,4): k_emp=4, fillers=4, r_dom=0.125 — the only sample in 36 valid converge rows that emitted the registered construction.

Paper claims 0/10 rival at N=57: confirmed (rival hits=0).

Paper claims "filler count 0 in 35 of 36 valid converge rows": confirmed from filler_dist — N=20 {0:14, 4:1}, N=30 {0:14}, N=41 {0:7}. Total 35 of 36. ✓

---

## 2. Falsifier applied honestly

**Registered F-M1** (from `arm_m_preregistration.txt` line 37-41): "if at 2 or more of the 3 converge cells (N = 20, 30, 41) the modal valid output is NOT the registered V(k*, m) value (ties for mode count as NOT) ... Modal = most frequent 2e-3 bucket among valid samples at 1e-6."

The analysis code uses `modal_is_pred` which checks `abs(modal_vals[0] - PRED[n]) < WINDOW` where WINDOW=2e-3. All three cells return `modal_is_pred=false`. F-M1 fires at 3/3 → TRIGGERED. The paper reports "triggered at 3 of 3 cells" (line 333). Honest.

No ties occurred in the data, so the tie convention ("ties count as NOT") is not exercised. No wiggle room exploited.

**Registered F-M2**: N=57 modal = 3.5625 = T(8,57) → not triggered. Correct.

**Partial-filler outcome** (prereg line 45-46): registered intermediate "if modal samples place 1 ≤ fillers < m, report as filler branch truncates." Actual data: fillers=0 in 35/36. This exceeds the registered intermediate case — stronger than anticipated. The paper reports the stronger result honestly (§3.4 lines 342-346), noting the (k*+1) grid shift and the rectangle-factorization pattern. Legitimate.

**One edge note**: the preregistration didn't explicitly cover "model moves to (k*+1) grid and fills/truncates it" as an outcome. The data exceeded the registration's vocabulary. The paper reports it as observation, not as preregistered prediction. No foul, but the registration could have been more exhaustive. Minor.

---

## 3. Cross-section consistency on arm M scope

**Abstract** (lines 41-46): m>1 disconfirmation at 3/3 cells, N=57 k=8 confirmed, 0/10 rival, scope restricted to m≤1.

**§1.1** (lines 137-140): trap zones include [57,63] — now sampled, consistent.

**§2.3** (lines 214-220): extend arm confirmed only at m≤1, disconfirmed at m≥4. Consistent.

**§3.4** (lines 322-360): full detail, all numbers match the scored JSON.

**§8** (lines 890-898): "five confirmed k (4,5,6,7,8 — last added by arm M), extend arm confirmed only at m≤1, disconfirmed at m≥4." Consistent.

No numeric contradictions between the abstract and body. One minor imprecision: the abstract says the model "truncates the (k*+1) grid" for N=20/30/41 (§3.4 has the nuance that N=20 and N=30 are exact-fill rectangles, not truncations — the abstract oversimplifies a two-word phrase that the body corrects on the same page). Recommended: change abstract to "moves to the (k*+1) grid" to cover both exact-fill and truncate-minus-one patterns.

**Verdict on claimed scope**: the paper does not overclaim N=57 (it's one cell at k=8, modestly framed as "fifth k confirmed"). It does not underclaim the m>1 disconfirmation — the falsifier trigger is in the abstract, the failure occupies most of §3.4, and the scope restriction propagates to §2.3 and §8. Both arms of the result receive appropriate prominence.

---

## 4. "Sharpening, not a rescue" — legitimate

The pre-arm-M claim: k* = round(√N), k*² ≤ N → extend with fillers, k*² > N → truncate. Post-arm-M: extend arm restricted to m≤1. This is a scope *narrowing* — the formula describes less behavior than previously claimed. Calling it "sharpening" is accurate: the boundaries are more precisely delineated. The alternative framing ("the closed form was partially wrong") would also be accurate, but the paper chooses the former.

The falsifier is given equal prominence to the confirmation in the abstract. The negative result is not buried. The paper does not attempt to salvage the filler branch with post-hoc explanations (it notes the arithmetic-tractability alternative in §8, explicitly marked as untested). No spin detected.

---

## 5. Review 7's deduction 1 — RESOLVED

Review 7 (71/100): "m never tested above 1. Converge cells are 17 and 37, both m=1." Requested N=20 (m=4), N=30 (m=5), N=41 (m=5). Arm M ran exactly these cells, preregistered. Results: filler branch disconfirmed at m≥4. The question is ANSWERED.

Review 7's deduction 2 (ambition unmeasured): paper now has post-hoc operationalizations (distinct radius count, off-lattice fraction). Not registered metrics, but disclosed as post-hoc. Partial fix.

Review 7's deduction 3 (trace not contribution #3): contribution #3 is now "Checkable faithfulness, and trace requests as interventions" — faithfulness leads, trace-as-intervention is secondary. The faithfulness result (96.4%) is clean; the concentration result is correctly caveated. Essentially adopted.

Review 7's deduction 4 (opus_alias): caveats strengthened, anomalies downgraded to anecdotal. Still unreproducible, but the caveat is load-bearing.

**Estimated review 7 revised score**: 78–82 (up from 71). Deduction 1 resolved with honest negative result; deductions 2-4 partially addressed.

---

## 6. New contradictions — NONE

Verified cross-references:
- Validity counts (15/15, 14/15, 7/12, 10/15) match report JSON → ✓
- Modal values (2.0, 2.5, 2.9285714, 3.5625) match report → ✓
- On-pred counts (1, 0, 0, 6) match report → ✓
- Rival count (0/10) matches report → ✓
- "One sample in 36" (line 338): 15+14+7=36 valid, on_pred=1 across converge cells → ✓
- "Three N=41 invocations died" (line 352): sampled=12, launched=15, 3 excluded → ✓
- "five confirmed k" (§8): N=13(k=4), N=21(k=5), N=31(k=6), N=43(k=7), N=57(k=8) = five → ✓
- k_emp distributions: N=20 {5:14, 4:1}, N=30 {6:13, 5:1}, N=41 {7:7}, N=57 {8:10} — all k*+1 for converge cells (except the one V(4,4)), all k* for N=57 → consistent with paper's narrative → ✓

The abstract's "truncates the (k*+1) grid" for N=20 is imprecise (it's an exact 5×4 fill) but the body corrects this within the same section. Not a contradiction, just abstract-level compression. Recommend: s/truncates/moves to/ in the abstract.

---

## Revised Score: 90/100

**Starting from 88** (review 6, round 2).

**Additions (+)**:
- +2: preregistered extension, falsifier triggered correctly, no spin — exceptional scientific hygiene
- +2: N=57 (k=8) closes the Figure 1 gap; truncate arm now has five confirmed k — genuine new positive evidence
- +1: three converging cells' negative result honestly reported — strengthens credibility

**Subtractions (−)**:
- −1: filler branch scope narrows to m≤1; the closed form is less general than revision 2 claimed
- −1: remainders unchanged — single vendor, rectangle weak (5/11), trace fragile, opus_alias provenance
- −1: abstract's "truncates the (k*+1) grid" imprecision for N=20/30 (minor)

**Net**: +4 − 2 = +2. Rounded: 90.

---

## Submission readiness: YES

The paper is honest about its negative result, the scope is now precisely stated, the core mode-ceiling finding with k-match structural verification is robust, and every caveat is disclosed. The arm M addition makes the paper stronger at the cost of a narrower claim — the right tradeoff.

## Top remaining action

Run the one-parent mutation arm (§8): 120 invocations, same discriminating cells, bare prompt + one parent packing + score + "propose a modification." This is the single highest-value experiment to test whether the branch rule survives conditioning — the gap between the measured unconditioned distribution and the in-loop distribution the discovery systems actually sample.
