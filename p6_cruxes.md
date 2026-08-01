# P6 arbitration cruxes (2026-08-01, after 3-reviewer panel: 102 findings)

Reviews: p4_review_reviewer2.md (33: 18M/11m/4n, reject), p4_review_stats.md
(24: 12M/9m/3n, major revision), p4_review_gecco.md (45: 15M/23m/7n, major revision,
venue = GECCO LLM-EC workshop; ALIFE rejected).

## Fable's objective recomputes (done, trust these)
- Bare-arm wave drift (R2 #6): on-pred old-wave vs new-wave: N=13 3/4 vs 7/14;
  N=21 2/4 vs 10/11; N=31 5/5 vs 8/12. Drift real, direction inconsistent.
  SAME-WAVE (paired) comparison: new-wave bare pooled 25/37 (68%) vs trace_v2 46/53
  (87%) — gap survives restriction. Revision must report this stratified comparison.
- F1 confirmed: 71% irreproducible; correct = 35/45 (78%) primary tol; ladder triple
  becomes 78→100→13 (or 64→90→13 strict). Fix abstract+§1+§4+kill_check quotes.
- Original 2.75 slack + rectangle 5/11 + all closed-form anchors: bit-exact clean
  (stats referee table lines 19-44).

## Cruxes for council (judgment calls, not arithmetic)
C-A. P-T3 significance framing: prereg registered NO alpha for P-T3 (directional only).
     Options: (i) report directional-confirmed + p uncorrected + Holm-corrected fails,
     abstract downgrades to "concentrates (87% vs 70%, driven by N=13; stratified
     estimate survives same-wave restriction)"; (ii) drop significance language
     entirely; (iii) keep p=0.0325 headline. Stats F5/F6/F7 + R2 #5 say (iii) dead.
C-B. Falsifier tie handling (stats F8): registered "<=" fires at 2/3 N (two exact
     ties). Options: report triggered-under-literal-reading + both readings + P-T1
     failed anyway (self-correction narrative); or argue ties ambiguous. Honesty
     favors first.
C-C. P-T2 asymmetry (stats F7): registered criterion MET directionally (1/53 vs 2/50).
     Paper must report P-T2 confirmed-directional (n too small), symmetric standard.
C-D. Faithfulness scorer (stats F9/F10/F11): extend regex to observed forms
     ("3 by 4", "5 columns and 4 rows", "4-4-4-1"), rescore all 60 trace_v2 incl.
     invalid rows, re-report; state false-positive-rate caveat; fix "all the same
     case" (1 of 3 only). If rescored rate <90%: report honestly, P-T4 flips.
C-E. Abstract calibration (R2 #2/#8/#15): "predicts the exact sum" at 46-52% hit
     rate = overclaim; rewrite as "predicts the modal output value" + state hit rate;
     "leaving validity unchanged" = null, phrase as "no detectable validity change
     (p=0.30)".
C-F. Ledger metadata regeneration (stats F2/F3/F4, R2 #9): produce
     arm_f_candidates_v2.jsonl with corrected prompt_sha256 (trace_v2 hashes from
     prereg), per-wave run_date, per-arm alias/dated_id from actual dispatch records.
     v1 stays untouched (git + read-only rule). Analysis scripts point at v2.
     Disclose correction in §9.
C-G. Serving-signature artifacts (R2 #10, paper 2 too): durations/token counts live
     only in session transcript. Export machine-readable extract (task usage blocks)
     to corpus as serving_signature.json; cite as released artifact.
C-H. Venue: GECCO reviewer says LLM-EC workshop now, TMLR expanded later; ALIFE out.

## Non-negotiables (prereg protection — reject any finding demanding these)
- Do NOT re-run or alter registered tests post-hoc beyond disclosed corrections.
- Do NOT drop the pilot or its died-at-scale story (it is the honesty spine).
- Evidence files v1 immutable.
