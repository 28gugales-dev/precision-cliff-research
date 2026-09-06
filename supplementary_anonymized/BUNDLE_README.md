# Anonymized supplementary bundle

Code, ledgers and preregistrations backing every replayable figure in the
paper (see the claim-evidence map and HOW_TO_RUN.md). Built by
build_anon_bundle.py from the working corpus.

REDACTION DISCLOSURE. Identity strings (author name, e-mail, Kaggle owner
handle, local paths) were replaced throughout: the Kaggle owner handle
appears as ANON-KAGGLE-OWNER. Some preregistration files are hash-locked -
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
arm_mu_ceiling.json (the by_arm block separates MU from CH). Arm L:
arm_l_*.py, arm_l_prompts.json, arm_l_report.json. Arms P and P-D:
arm_p_*.py / .jsonl / .json, arm_pd_*.py / .jsonl / .json and their
preregistration and amendment files. Arms GM, GM2, GM3: arm_gm_*.py / .jsonl
/ .json, arm_gm_v2_report.json, arm_gm2_*, arm_gm3_*. Arm V:
arm_v_*.py / .jsonl / .json (arm_v_score.py imports arm_f_repro.py, the
companion's scorer). Independent recount of every count that paper reports:
arm_transfer_independent_rescore.py and its output
arm_transfer_independent_rescore.json (LP oracle from n_sweep_forecast.py).
Correction found by that recount: corrections_ledger.md item 36.
