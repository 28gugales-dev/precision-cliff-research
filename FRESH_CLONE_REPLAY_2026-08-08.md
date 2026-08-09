# Fresh-clone replay verification — 2026-08-08

Independent pass by a separate agent context: the repository was copied to a scratch
directory (excluding `.git` and `paper2_drafts/`) and every released no-argument replay
script was run there. Purpose: exercise the claim-map preamble's sentence that the
scripts run in a fresh clone, which until this pass no one — including review 13, which
recomputed figures independently instead — had done end-to-end.

Result: **11/11 scripts exit 0; zero path breaks; zero dependency failures; every
checklist figure reproduced exactly.**

| script | verdict |
|---|---|
| sec3_ladder_repro.py | MATCHED (17/18 vs 8/57; 3.40e-06; 1.73e-07; 0.0068; 0.0559) |
| sec3_7b_repro.py | MATCHED (5.71e-10; F1 0.4444; Wilson [0.070, 0.262]) |
| sec3_dispersion_registered.py | MATCHED (288/432 rows; 46/49 vs 34/65) |
| sec3_search_progress.py | ran clean (permutation tails printed) |
| sec3_conditional_quality.py | MATCHED (8/10 vs 60/74, p=1.0000, CP 44.4%) |
| sec3_horizon_power.py | ran clean (projection table) |
| sec6_cv_canary_audit.py | ran clean (CV permutation both blocks) |
| sec4_independent_rescore.py | ran clean (4/30; 30/30 at both tolerances) |
| wave4_analysis.py | MATCHED (0/120, replay CLEAN, DISSOCIATION) |
| arm_r_analysis.py | MATCHED (7.843e-13; P-R0 DISCONFIRMED) |
| arm_t_analysis.py | MATCHED (0.3008; 0.0325; 38/41) |

`wave3_analysis.py` postdates the pass's brief and was run separately in-repo (exit 0,
labels as reported in §8). One labelling note from the pass: "0.44 (F1)" refers to the
F1 *forecast's* fresh-seed Fisher tail (5/5 vs 3/5), not an F1-score.
