# Anonymization report — TMLR double-blind submission

Scan date: 2026-08-12. Surface scanned: `paper2_short.md` (canonical source,
git 3c52e40) for author name, email, Kaggle owner handle, and absolute
Windows paths.

## Identifiers found and their replacements in latex-tmlr/

| Line | Identifier | Replacement in submission |
|---|---|---|
| 3 | `Soham Shailesh Gugale` (author block) | `\author{\name Anonymous authors ...}` placeholder; tmlr.sty additionally hides the block pre-acceptance. Real block restored only at camera-ready |
| 5 | `28gugales@gmail.com` | removed with author block |
| 77 | `sohamgugalet/precision-redetermin` | `\texttt{precision-redetermin}` (public Kaggle kernel; owner handle withheld for double-blind review) |
| 245 | `sohamgugalet/wave8-seed-pilot` | same pattern |
| 281 | `sohamgugalet/wave4-prereg-tiers-heilbronn` | same pattern |
| 284 | `sohamgugalet/precision-sweep-14b-heilbronn-wave3` | same pattern |
| 285 | `sohamgugalet/precision-sweep-14b-labs-wave5` | same pattern |
| 286 | `sohamgugalet/wave7-prereg-families` | same pattern |
| 287 | `sohamgugalet/wave7b-prereg-families-14b` | same pattern |
| 288 | `sohamgugalet/precision-redetermin` (repeat) | same pattern |

No absolute `C:\Users\...` paths appear in the manuscript body (all artifact
paths are repo-relative, e.g. `sec3_artifacts/...`). No other personal names,
emails, ORCIDs, or institution strings found.

## Rationale for keeping kernel names

The Kaggle kernel/dataset *names* are evidence (external timestamping of
preregistrations, external re-execution of digests). Deleting them would
delete claims; only the owner handle identifies the author. Withholding the
handle and noting "available via anonymized supplementary artifact" preserves
the claim and the blind.

## Supplementary artifact plan (USER ACTION — do not automate)

TMLR requires supplementary material to be anonymized too. Before submission:

1. Export the repro surface (scripts + jsonl ledgers + preregistration files
   named in the claim-evidence map, HOW_TO_RUN.md) to a clean folder.
2. Scrub: `git log` history (export files, not the .git dir), any `soham`
   string (grep before zipping), notebook metadata.
3. Upload to https://anonymous.4open.science/ (or attach as anonymized zip in
   OpenReview supplementary). This is an outward-facing publish step —
   user performs it, not the assistant.
4. Kaggle kernels stay public under the real handle — that is allowed
   (reviewers are told not to search for authors); the *submission* must not
   link the handle. TMLR/OpenReview policy treats pre-existing public
   artifacts like arXiv preprints: permitted, just not referenced
   de-anonymizingly from the paper.

## Residual de-anonymization risk (accepted, disclose to no one)

- A reviewer who searches a quoted kernel name on Kaggle will find the
  handle. Same class of risk as an arXiv preprint of the paper; TMLR
  tolerates it. Mitigation if desired: mirror the kernels into the anonymized
  artifact and drop names to "kernel A/B/C" — costs external-timestamp
  verifiability in-text. Current choice: keep names, withhold handle.
- The phrase "companion paper" plus "antecedent study
  (`precision-cliff-paper-combined.md`)" is self-citation-shaped. TMLR
  convention: cite as third person or as anonymized supplementary. The
  combined report is unpublished, so it MUST ship inside the anonymized
  supplementary bundle or the claim chain breaks.
