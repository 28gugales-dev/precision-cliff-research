# Template Anchoring & The Precision Cliff — research corpus

PRIVATE until submission. Two companion papers plus every artifact behind them.

## Papers
| file | paper | status |
|---|---|---|
| `paper1_draft.md` / `latex1/` | **The Nearest Square: Template Anchoring in Constructive Geometry** — closed form identifies the modal LLM output at 7/7 tested N; tier inversion; trace elicitation as intervention; triggered falsifier reported | revised post-panel, arXiv-ready LaTeX (compile on Overleaf/arXiv; no local TeX) |
| `paper2_draft.md` | **Served Precision Is Part of the Model: A Quantization Cliff in Proposal Variation** — at the 2-bit rung the proposer very largely stops departing from its parent while viability and validity stay flat, so pass/fail instruments report health; `opus_alias` forensics; attestation impossibility; minimum disclosure standard. §3 data is vendored in-repo under `sec3_artifacts/` and replays from the released scripts (see `HOW_TO_RUN.md` §0) | **`paper2_draft.md` is the only current manuscript.** `latex2/` is STALE — frozen at commit `6a36f85`, 19 revisions behind, and it still carries the withdrawn "novelty cliff" framing. Do not submit or cite it; regenerate from the markdown before submission |

Venue plan: paper 2 → TMLR now (MLRC 2026 window closes 2026-09-30); paper 1 → arXiv + GECCO 2027 (Krakow, deadline ~Jan 2027), TMLR fallback. ALIFE 2026 closed.

## Evidence chain (immutable files)
- `arm_f_raw.json`, `arm_f_candidates.jsonl` — v1 ledger, 215 invocations, never edited
- `arm_f_candidates_v2.jsonl` + `ledger_v2_corrections.md` — metadata-corrected ledger; every changed field keeps a `*_v1` sibling
- `arm_[sot]_preregistration.txt` — preregistrations (arm T sha256 ab7900a8…)
- `n_sweep_forecast.py/.json`, `rect_forecast.py`, `arm_g_*` — closed form + rectangle transfer
- `arm_f_repro.py`, `arm_t_analysis.py`, `collect_raw.py` — deterministic scoring; falsifier reported under BOTH tie readings
- `p7_faithfulness_rubric.md` (frozen at commit e181d2a) + `p7_blind_input.json` + `p7_blind_labels.json` — blind faithfulness adjudication, 54/56 = 96.4%
- `p11_mode_baseline.json` — prediction = empirical mode at 7/7 N; round-number baseline 2/69

## Review trail (all LLM-generated, disclosed in paper §9)
`p4_review_stats.md` (24 findings, 8 recomputation mismatches), `p4_review_reviewer2.md` (33),
`p4_review_gecco.md` (45), `p9_review_mlsys.md` (27, incl. 5 placeholder-leak catches),
`p6_cruxes.md` (council arbitration), `kill_check_2026-08-01.md` (adversarial novelty check, 0 kills),
`lit_sweep_2026-08-01.md`, `p8_systems_citations.md` (verified citations only).

## Figures
`fig_scripts.py` → `fig1_trapzones.png`, `fig2_packings.png`, `fig3_armT.png` (deterministic, no network).

## Process
`LOOP_PLAN.md` — the autonomous revision loop's plan, rules, and iteration log.
Backups: this repo (GitHub private) + OneDrive mirror + Google Drive folder.
