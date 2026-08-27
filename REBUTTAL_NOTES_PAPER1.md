# Rebuttal notes — paper 1 (anchoring), prepared against the simulated TMLR review (2026-08-27)

Internal preparation only; not part of any submission artifact. The simulated review
(opus, zero-context, TMLR two-criteria rubric) returned **leaning accept, conditional**.
Status of each requested change as of Rev 4.7 / 4.7b (tag `v4.7-fresh-eyes` + follow-up):

## Critical — all addressed in text

1. **Abstract scope (m ≤ 1, F-M1 3/3, denominator).** FIXED. Abstract now carries the
   falsifier restriction and the 8-of-11 pooled denominator alongside 7-of-7. §8's
   "sharper scope the abstract now carries" is now true.
2. **"Reduced concentration" unsupported.** FIXED. Abstract, contribution 5, §3.6 and the
   §3.6 heading all state the ranges overlap (61–67 sits inside 56–76) and that the
   reduction is directional, not separated, at these n. CI-includes-bar caveat retained.
3. **Contribution 1 post-hoc labeling.** FIXED. Contribution 1 and §3.5 both label the
   attempt-level reading as a disclosed post-hoc decomposition; classifier named (family
   filler radius); registered P-CH2 outcome (1 of 3 cells) stated in the contribution.
4. **Validity conditioning beyond CH.** ADDRESSED (disclosure route). A global scoring
   convention now states every on-prediction rate conditions on validity, names CH as the
   only arm where the attempt-level decomposition is measurable, and points at per-cell
   validity denominators for bounding. A full attempt-level re-analysis of F/GM3/V/CN is
   not possible under the registered instruments (invalid rows there lack the CH arm's
   structured attempt evidence); if a reviewer insists, offer the decomposition as a
   supplementary table computed under the CH classifier with that limitation stated.
5. **Anonymized artifact link.** ADDRESSED. §9 provenance item now states the full
   artifact accompanies the submission as anonymized supplementary material
   (`supplementary_anonymized.zip`, 520 entries, 0 identity leaks in audit).

## Minor — status and prepared responses

6. **Uniform-template null for the square arm.** DEFERRED. New analysis; if requested,
   compute P(on-prediction | uniform choice among plausible template shapes) per square
   discriminating cell and report headline per-sample rates against it. Note for response:
   the 7/7 mode-identity claim survives this null by the reviewer's own reading.
7. **CN reconstructed rows as sensitivity, not primary.** ALREADY THE CASE — respond by
   pointing at §3.8: the eleven flagged rows are discarded from the primary analysis;
   P-CN1 reads 3 of 4 with them excluded. The review misread direction here.
8. **Demote contribution 3 / drop opus_alias leg.** DECLINED with rationale: the alias
   caveat is attached at every occurrence, the ladder is reported both with and without
   the leg (§5), and the boundary-condition framing is exactly the demotion requested.
9. **"Mode ceiling" wording + round-number baseline.** DEFERRED. Cheap wording softening
   possible on request; a construction-family baseline is new analysis. Both text-only.
10. **§1 "behaves the same way on the next sample."** FIXED — now "more often than not
    the next sample repeats the same move" (supported: per-sample on-prediction 56–86%).

## Standing evidence for the response

- Fresh-clone reproducibility: all 14 pipeline scripts, byte-identical reports (CRLF-only
  diff on two arm-M files, content identical).
- Independent ledger re-audit: ~330 numeric assertions recomputed from raw ledgers with an
  independent parser/validator; 3 findings, all fixed or glossed exactly in 4.7
  (`corrections_ledger.md` item 33).
- The only further validation that moves the claims is running the pre-staged arm_cp
  (perturbed container) / arm_rp (direct recall) registrations — author's call, needs API
  spend; DRAFT registrations already committed and shipped in the bundle.
