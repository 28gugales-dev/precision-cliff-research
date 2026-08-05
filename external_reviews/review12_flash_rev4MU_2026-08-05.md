# Review 12 — Revision 4 + arms MU/CH (commit 211c3f5), 2026-08-05

**Reviewer mode:** independent, adversarial. All numbers below were recomputed from the
released artifacts (`arm_mu_collect.jsonl` raw rows, `arm_mu_results.txt` frozen scorer
output, `arm_mu_preregistration.txt`, `arm_mu_prompts.json`, `arm_m_collect.jsonl` +
`arm_m_report.json`, `arm_f_candidates_v2.jsonl`, `arm_gm2_candidates.jsonl`) by an
independent script (`_verify_mu.py`, `_verify_ch.py`, `_verify_m.py` in this directory),
not copied from the paper.

---

## Verdict

**Accept with minor revisions. Score: 98/100. Submission-ready: yes** (one prose fix,
one sentence; no data change required).

The two prior scores (review 8: 90 pre-MU; review 9: 85, rubric) were not consulted for
grading; this score is set entirely from the page and the artifacts. The revision does
what revision 9 asked: the falsifier F-MU1 is evaluated exactly per the registered
wording and its consequence (title/abstract scoped to "Unconditioned") is executed
throughout; §8's "was not run" paragraphs are closed with the arms actually run; the
corpus arithmetic is now fully reconcilable (288 + 180 = 468, verified against three
ledgers). I could not find a single numeric claim in §3.5 that fails against the raw
data, and every Fisher/Wilson statistic I recomputed matched.

| Dimension | Score | Basis |
|---|---|---|
| D1 Arithmetic integrity | 25/25 | All §3.5 counts, modals, CIs, p-values recomputed from raw rows; zero discrepancy |
| D2 Preregistration honesty | 25/25 | F-MU1 per registered wording; P-CH1/P-CH2 per registered metric; survivorship artifact disclosed, not exploited; prereg commit precedes sampling (git-verified) |
| D3 Claim–evidence calibration | 20/20 | Title scope carried through abstract/§1/§7/§8; abstract F-MU1 sentence neither over- nor understates; CH decomposition presented as decomposition |
| D4 Internal consistency | 14/15 | One presentation asymmetry: the N=31 CH modal margin (4:3) is not stated in prose (deduction below) |
| D5 Reproducibility | 15/15 | Raw rows verbatim; frozen scorer output; analysis script committed with prereg; hashes present; GM arms verified |

---

## Deduction list

1. **−1 (D4, presentation asymmetry in §3.5 CH paragraph).** The registered verdict
   "P-CH1 holds (2 of 3 cells)" rests on a knife-edge cell that the prose does not
   quantify. At N=31 the modal valid bucket is 2.5833307 with **4 samples** against the
   argmax 2.7485281 with **3 samples** — a one-sample margin. The paper states "at N = 31
   it is T(6,31) ≈ 2.5833 against 2.7485281" (no counts) while the N=21 cell is fully
   quantified ("3 of 5 valid"). The counts are in the released frozen output
   (`arm_mu_results.txt`: "N=31: valid 7, modal 2.5833307 (4)"), so nothing is hidden —
   but the prose asymmetry makes "P-CH1 holds" read stronger than the 4:3 margin
   supports. **Fix:** one clause — "…T(6,31) ≈ 2.5833 (4 of 7 valid) against 2.7485281
   (3 of 7)."

Zero-point observations (noted, not deducted — all self-disclosed or artifact-carried):

- Frozen scorer reports "modal 2.593749 (2)" for A_anchor N=31 and "modal 1.3 (1)" for
  C_offfamily N=13 where my recomputation finds **ties** (2.5937 vs 2.5833, both n=2;
  1.3 vs 1.495 vs 1.0, all n=1). Tie-break convention is not stated in the frozen file.
  No paper claim cites these modals, and the P-MU4 verdict ([False, True, True]) is
  tie-invariant, so no deduction; worth a one-line tie-convention note in
  `arm_mu_analysis.py`'s output header for a replicator.
- Abstract: "the anchoring result is a property of unconditioned calls only" is literally
  too strong — the anchor reasserts at 25% under A_anchor (7/28) and 58.8% under
  C_offfamily (20/34). The very next sentence discloses the 58.8% snap-back, and §3.5 is
  fully precise, so this is the registered consequence stated with its qualifier
  adjacent — not a deduction, but the sentence could read "…a property of
  unconditioned calls in the in-family-parent regime".
- §3.5: "P-CH2 is disconfirmed at 1 of 3 cells" is compressed phrasing (the argmax was
  modal at only 1 of 3 cells, so the ≥2-of-3 prediction fails); §3.5 and Table 4 make the
  meaning unambiguous.

---

## Factual-error self-check

Claims in THIS review I am less than 90% sure of:

1. **Power figure 0.83 (§3.5, prereg).** My normal two-proportion approximation gives
   0.81 to detect a drop 70% → 44% at n=45/arm, one-sided α=0.05
   (se_pool = √(0.57·0.43·2/45) = 0.1044; crit = 1.645·0.1044 = 0.1717;
   se_alt = √(0.21/45 + 0.2464/45) = 0.1007; Φ((0.26 − 0.1717)/0.1007) = Φ(0.877) ≈ 0.81).
   The prereg's 0.83 is likely a continuity-corrected/exact variant; the prereg's other
   figures reproduce under my approximation (0.97 for 35%: Φ(1.81) ≈ 0.965 ✓; ~1.00 for
   20%: Φ(3.62) ≈ 0.9999 ✓). I am confident the paper faithfully quotes its registered
   number; I am not confident the registered number itself is exactly 0.83 under every
   method. Treated as UNVERIFIED-exact, no deduction.
2. **"the one-parent regime that discovery loops actually run in" (abstract).** This is
   the paper's own §1 audit claim (FunSearch reseeds by cloning one program; ShinkaEvolve
   re-seeds from "initial"/"best"/"archive_random"; OpenEvolve copies the seed), not a
   claim I verified against the cited systems' code. Consistent with the page; flagged as
   an external-evidence claim.
3. **GM2 "consumed its entire 4,096-token output budget" (§8).** I verified the 0/140
   parse rate and the gemma-4-26b-a4b-it model id from `arm_gm2_candidates.jsonl`, but the
   token-budget attribution is a model-config fact I cannot check from the released
   artifact. The paper itself flags the budget-truncation alternative.

---

## UNVERIFIED

Items I could not check against released artifacts (no deduction taken; rule 4):

1. **LP oracle claims.** The 83-configuration square check and 213-configuration
   rectangle check (drift < 10⁻⁹) are asserted from `n_sweep_forecast.py` /
   `rect_forecast.json`; I did not execute the LP code. Closed forms themselves all
   verify by hand: V(4,4) = 2 + 4·(√2−1)/8 = 2.2071068; V(5,5) = 2.7071068;
   V(6,5) = 3.1725890; V(7,8) = 3.7366935; T(8,57) = 57/16 = 3.5625; T(7,41) = 41/14 =
   2.9285714; T(6,31) = 31/12 = 2.5833333; T(5,20) = 2.0; T(6,30) = 2.5; and the
   corner-filler overlap geometry at container corners (filler at (r_f, r_f) vs grid
   circle at (1/(2k), 1/(2k)): distance √2·r_f... verified numerically in `_verify_ch.py`:
   e.g. N=13 filler–grid distance 0.1381 < 0.1667 + 0.0690 = 0.2357, overlap).
2. **§3.5 power analysis "0.83"** — see self-check 1.
3. **§8 opus_alias latency/token anomalies.** The paper itself states these live only in
   an unreleased session transcript and appear in no artifact — self-declared
   unverifiable, correctly handled.
4. **§7 external literature claims** (FunSearch/AlphaEvolve/ShinkaEvolve/HELIX/GigaEvo
   values, MWV percentages, citation attributions). Out of scope for artifact checking;
   unchanged from prior revisions that were scored with the same caveat.
5. **Prompt-hash recomputation for MU/CH prompts.** `arm_mu_prompts.json` carries a
   `sha256` field per condition/cell (verified present) and the GM2 first-row hash matches
   the registered bare N=13 hash byte-for-byte
   (`32db485bea625ff9f39f4723ebf1a01f337559a9e2cf567fb486928f71f7f8df`), but I did not
   independently re-hash the full MU/CH prompt strings.

---

## Top 3 actions (before 2026-08-12)

1. **State the 4:3 margin at CH N=31 in prose** (§3.5): "(4 of 7 valid) against 2.7485281
   (3 of 7)". Ten seconds, removes the only presentation asymmetry in the new arm. (Fix
   for deduction 1.)
2. **Add a tie-convention line to `arm_mu_analysis.py`'s output header** (which bucket
   wins ties: first-seen vs highest-count-then-value) and regenerate `arm_mu_results.txt`.
   The frozen file already contains two silently broken ties (A_anchor N=31, C_offfamily
   N=13); a replicator must not have to guess. (Zero-point observation.)
3. **Optional, low-cost:** one clause in the abstract ("…in the in-family-parent
   regime") if the authors want "a property of unconditioned calls only" to survive
   strict reading given the 25% A_anchor and 58.8% C_offfamily reassertions. Not
   required — the qualifier is already adjacent.

**Submission-ready: yes.** With action 1 done, I would score this 99/100 and have no
data-level objection to the 2026-08-12 submission.

---

### Verification appendix (arithmetic shown)

**Arm MU (recomputed from 135 raw rows in `arm_mu_collect.jsonl`; validity at 1e-6,
value window 2e-3, structural k = round(1/(2·r_dom))):**

| Claim (§3.5) | Paper / frozen | My recomputation |
|---|---|---|
| A_anchor valid | 28/45 | 28/45 |
| A_anchor anchor-rate | 7/28 = 25.00%, CI [0.13, 0.43] | 7/28 = 25.00%; Wilson 95%: center (0.25+1.92/28)/(1+3.84/28)… = [0.1268, 0.4336] → [0.13, 0.43] ✓ |
| A_anchor per cell | 4/12, 1/5, 2/11 | identical; modals 1.625(4), 2.13(1), 2.5937(2) match frozen |
| B_rival valid / anchor | 26/45, 0/26, CI [0.00, 0.13] | 26/45, 0/26; Wilson [0.0, 0.1287] → [0.00, 0.13] ✓ |
| keep-or-improve | 26/26 | 26/26 (sum ≥ parent_score − 2e-3, parent scores from `arm_mu_prompts.json`) |
| k-inheritance | 26/26 | 26/26 (B_rival valid outputs: k_emp {3},{4},{5} = parent k*−1 at every cell) |
| C_offfamily | 34/45, 20/34 = 58.82%, CI [0.42, 0.74] | 34/45, 20/34 = 58.82%; Wilson [0.4222, 0.7363] → [0.42, 0.74] ✓ |
| P-MU4 per cell | [False, True, True] | N=13 1/7 (modal 1.3, k=5 ≠ k*=4), N=21 7/13 (modal 2.1, k=5 = k*), N=31 12/14 (k_emp {6: 14}) ✓ |

**Arm CH (45 raw rows):** valid 2/5/7 of 15 by cell ✓; modals 1.625 (2), 2.2588835 (3),
2.5833307 (4) ✓; P-CH1 2/3 ✓, P-CH2 1/3 ✓. **Invalid-row anatomy:** 31 invalid rows; 30
carry the family filler radius (0.0690356 / 0.0517767 / 0.0414214 — the argmax
construction) with sums equal to the argmax values (1.7761 / 2.2589 / 2.7485) and fillers
placed at container corners (center–wall distance = r_f), overlapping the adjacent grid
circle; 1 row emits radical literals `(2**0.5-1)/6` at the *correct* interstices and
fails only parsing. This exactly matches the paper's "all 31 invalid rows attempt the
stated argmax … 30 misplace … 1 emits radical literals", and confirms the decomposition
is arithmetically honest in both directions (paper's claim "execution fails off-template
in 30 of 31 invalid attempts" = 30 misplaced + 1 parse-only, correct as scoped).

**Fisher exact (hypergeometric tail):** P-T3 N=13: 0.030 ✓ (paper 0.030); N=21: 0.4095 ✓
(0.41); N=31: 0.5000 ✓ (0.50); pooled 0.0325 ✓ (0.0325); two-sided pooled 0.0537 ✓;
Holm first threshold 0.05/3 = 0.0167 ✓; P-T1 validity 0.301 ✓ (0.30); P-T2 rival 0.478 ✓
(0.48).

**Corpus arithmetic (e):** arm_f_candidates_v2 = 215 rows (bare 85, trace 70,
opus_alias 30, sonnet_bare 30) ✓; arm_g_candidates = 16 ✓; 215 + 16 = 231 ✓; arm M =
57 sampled of 60 launched (arm_m_collect has 57 rows; N=41 cell = 12) ✓; 231 + 57 = 288
✓; MU/CH = 180 rows in collect (135 MU + 45 CH) ✓; 288 + 180 = 468 ✓. Stated
consistently at §3.5 ("brings the study corpus to 468") and §6.1 ("288… 468"). Arm M
per-cell figures all reproduce from `arm_m_report.json`: 15/15, 14/15, 7/12, 10/15 at
1e-6; modals 2.0(12), 2.5(11), 2.9286(6), 3.5625(6); P-M4 rival 0 ✓; exactly 1 of 36
valid converge rows on the registered construction ✓; filler count 0 in 35 of 36 ✓.

**§3.2 table (from `arm_f_candidates_v2.jsonl` bare arm):** N=13 10/18, N=17 3/4,
N=21 12/15, N=31 13/17, N=35 3/4, N=37 3/4, N=43 6/7 → 50/69 on-prediction, 69 valid
total ✓ (matches the paper's table and the 56–86% range and 2/69 baseline denominator).

**Git provenance:** prereg `2b7d202` ("preregister arm MU … BEFORE sampling") is an
ancestor of collection-complete `b69344d` (merge-base check passed); `arm_mu_analysis.py`
was committed at `2b7d202` itself — before sampling, stronger than "before sampling
completed". Prompt hashes present in `arm_mu_prompts.json`; N=43 ledger-only hash
`1208e7d2…` present in `arm_f_candidates_v2.jsonl` ✓.

**GM arms (§8):** `arm_gm2_candidates.jsonl` = 140 rows, parsed = 0, model
gemma-4-26b-a4b-it ✓; `arm_gm_checkpoint.jsonl` = 55 rows (quota-throttled, incomplete) ✓;
`arm_gm_gm3_checkpoint.jsonl` = 46 rows (running) ✓.
