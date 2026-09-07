# Anonymized supplementary bundle

Code, ledgers and preregistrations backing every replayable figure in the
paper (see the claim-evidence map and HOW_TO_RUN.md). Built by
build_anon_bundle.py from the working corpus.

REDACTION DISCLOSURE. Identity strings (author name, e-mail, Kaggle owner
handle, GitHub owner handle and repository name, project web URL, local
paths) were replaced throughout: the Kaggle owner handle appears as
ANON-KAGGLE-OWNER, the GitHub owner as ANON-GITHUB-OWNER and the repository
as ANON-REPO. Some preregistration files are hash-locked -
their SHA-256 digests are quoted in the paper and were computed over the
ORIGINAL bytes, so the digests do not verify against the redacted copies in
this bundle. They verify against the public Kaggle datasets named in the
paper (owner handle withheld for review) and will verify against the
de-anonymized artifact released at camera-ready. Nothing else about those
files was changed.

LAYOUT. The corpus root holds every arm's runner, ledger, preregistration,
amendment and frozen report. paper_repo/loop/ and paper_repo/evidence/ hold
the scripts and outputs the papers cite as living in the paper repository
(recount_cl.py, arm_mu_ceiling.py, cl_recount.json and the rest). This
bundle serves both companion submissions; each ships it with its own
supplement PDF and an anonymized copy of the other paper.

COMPANION (TRANSFER) PAPER FILE MAP. Arm MU: arm_mu_*.py / .jsonl / .json
and paper_repo/loop/arm_mu_ceiling.py with paper_repo/evidence/
arm_mu_ceiling.json (the by_arm block separates MU from CH); the supplement's
per-row table of the eighteen MU outputs above the family argmax regenerates
from paper_repo/loop/r26_mu_rows.py (reads paper_repo/loop/round22e_facts.json
and arm_mu_prompts.json). Arm L:
arm_l_*.py, arm_l_prompts.json, arm_l_report.json. Arms P and P-D:
arm_p_*.py / .jsonl / .json, arm_pd_*.py / .jsonl / .json and their
preregistration and amendment files. Arms GM, GM2, GM3: arm_gm_*.py / .jsonl
/ .json, arm_gm_v2_report.json, arm_gm2_*, arm_gm3_*. Arm V:
arm_v_*.py / .jsonl / .json (arm_v_score.py imports arm_f_repro.py, the
companion's scorer). Post hoc ceiling ledgers: arm_ceiling_gm3_v.py writes
arm_ceiling_gm3_v.json (GM3 and V outputs against the family argmax at 1e-6
and 1e-9); arm_l_residuals.py writes arm_l_residuals.json (arm L residuals
per lineage and pooled, and the L3 Fisher test); diagnostics_gm3_rival.py is
the GM3 structural check of section 7; diagnostics_transfer_null.py writes
diagnostics_transfer_null.json (the template-shape null of supplement S5).
Independent re-score of the 135 cell-level counts that paper reports, 129 of
which agree, with the six differences and their causes listed under
disagreement_root_causes: arm_transfer_independent_rescore.py and its output
arm_transfer_independent_rescore.json (LP oracle from n_sweep_forecast.py).
Correction found by that re-score: corrections_ledger.md item 36. Evidence
gate: paper_repo/loop/evidence_gate.py checks each residual and clearance
sentence in paper_repo/paper/*.tex (the transfer paper's LaTeX source)
against the ledger field it cites, per paper_repo/loop/r27_evidence.json;
run it from any directory. paper_repo/loop/build_channel_table.py rebuilds
the anchoring paper's Table 1 from the frozen reports under paper_repo/
evidence/ and the corpus root.

REPLAY GATE. python -X utf8 replay_gate.py <this directory> runs every
script named in HOW_TO_RUN.md and this file from the packaged bundle and
writes replay_gate.json; runners, builders and live collectors (_run.py,
_build.py, arm_l_step.py, arm_g_rect.py) are listed as SKIP_LIVE because
they need a serving path or an argument naming a lineage.
