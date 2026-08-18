# Anonymization report — TMLR double-blind submission (paper 1)

Scan date: 2026-08-17. Surface scanned: `paper1_draft.md` (canonical source,
current v62, 1284 lines) for author name, email, Kaggle owner handle
(`sohamgugalet`), and absolute Windows paths (`C:\Users`, `C:/Users`).

## Identifiers found and their replacements in latex-tmlr-paper1/

| Line | Identifier | Replacement in submission |
|---|---|---|
| 3 | `Soham Shailesh Gugale` (author block) | `\author{\name Anonymous authors ...}` placeholder; tmlr.sty additionally hides the block pre-acceptance. Real block restored only at camera-ready |
| 5 | `28gugales@gmail.com` | removed with author block |
| 4 | `Independent Researcher` (affiliation line) | removed with author block (`\addr Withheld for double-blind review`) |

That is the complete hit list. Unlike paper 2, paper 1 contains **no**
`sohamgugalet/<kernel-or-dataset>` references (its artifacts are repo-local
files, e.g. `arm_f_candidates_v2.jsonl`, not public Kaggle kernels), and no
absolute `C:\Users\...` / `C:/Users/...` paths appear anywhere in the
manuscript body. Verified by grep over the source and re-verified by grep
over every emitted `.tex` file (0 hits for `Soham`, `Gugale`, `28gugales`,
`sohamgugalet`, `C:\Users`, `C:/Users`).

## Items reviewed and deliberately kept

- Git commit hashes (`e528c6b`, `2b7d202`, `37b3adb`, `3019aab`, `e181d2a`,
  `e77bb0e`-style) and file SHA-256 digests: local-repository provenance,
  not identity-bearing; they are evidence for registration ordering.
- The revision note after `\maketitle` (source lines 7-10): references
  internal review files (`p4_review_*.md`, `p6_cruxes.md`) that ship in the
  anonymized supplementary; nothing identifying.
- `deepseek-v4-pro`, `deepseek-v4-flash`, Gemini, Claude tier names in the
  S9 AI-use disclosure: vendor/model names, not author identity. The
  disclosure states models are not authors; TMLR permits this.
- Kaggle is not referenced in paper 1 at all, so paper 2's
  "owner handle withheld" pattern has no application here.

## Supplementary artifact plan (USER ACTION — do not automate)

Same as paper 2's (see latex-tmlr/ANONYMIZATION_REPORT.md): export the
repro surface named in S9 (preregistration files, `arm_*_collect.jsonl` /
`arm_f_candidates_v2.jsonl` ledgers, analysis scripts, `HOW_TO_RUN.md`,
`p7_blind_labels.json`, the three referee reports and `p6_cruxes.md`) to a
clean folder, grep for any `soham` string before zipping, strip notebook
metadata and the `.git` dir, upload via anonymous.4open.science or the
OpenReview supplementary. Outward-facing publish step — user performs it.

## Residual de-anonymization risk

- The companion paper (paper 2) cites public Kaggle kernels under the
  author's handle; a reviewer who reads both submissions and searches those
  kernel names can link them. Same accepted-risk class as an arXiv
  preprint; the submission itself does not link the handle.
- S9's "Use of AI systems" bullet names the assistant model family used for
  drafting. This describes tooling, not authorship, and is standard
  disclosure; it does not identify the author.
