## How to Run the Precision Cliff Experiment

### 0. Reproduce the paper's figures (no GPU, no downloads)

Everything section 3 and section 4 report regenerates from the artifacts vendored in
this repository. Install dependencies once (`pip install -r requirements.txt`), then
run any of these from the repository root with **no arguments**:

| script | what it reproduces |
|---|---|
| `sec3_ladder_repro.py` | 14B ladder viability, validity, echo, per-seed and must-differ counts, and five of section 3's nine Fisher tails |
| `sec3_dispersion_registered.py` | both dispersion-probe waves: registered echo measures, the post-hoc decomposition, quality forks |
| `sec3_dispersion_prereg_rule.py` | wave 1's locked decision rule (returns *unclassified*) |
| `sec3_registered_echo_test.py` | wave 1's registered primary echo JT, `score_delta` CIs, orthogonality diagnostic |
| `sec3_search_progress.py` | §3.6 loop-level search progress: accepted hill-climb steps per lineage across all four ladders (14B ×3 plus 7B), the echo-complement identity gaps, conditional-on-departure rates, final best score, and ten of the twelve exact lineage-level permutation tests (the other two, the 7B outcome tails, print here but appear in the paper only in §3's inferential-status paragraph). Post-hoc throughout |
| `sec3_7b_repro.py` | the four Fisher tails no other script replays (5.7e-10, 0.001, 0.44, 1.0) and the whole 7B paragraph: viability with Wilson intervals, all three contrasts, the format-lottery count distribution, the truncation check, probes and best score |
| `sec3_conditional_quality.py` | §3.6 conditional-on-departure improvement rate, pooled over both fixed-parent probe waves, with the per-parent breakdown and the verdict scored against the wave-3 registered decision rule and its power floor |
| `sec3_horizon_power.py` | §3.6's structural argument that final best score is a maximum statistic and therefore the wrong dependent variable. Prints a resampling projection whose direction is discarded in-paper, and a power table whose use as a power statement is **withdrawn** — the script's closing block says why |
| `sec3_artifacts/dispersion_probe_v2/analyze_v2.py` | wave 2's registered analysis and its `VERDICT: FAILED` label |
| `sec6_cv_canary_audit.py` | §6 item 4's self-audit: runs the paper's own duration-CV serving canary against rows where the serving path is fixed, shows it fires at the 2-bit rung on both probe waves, and decomposes the firing into output degeneracy via the echo split |
| `sec4_independent_rescore.py`, `arm_f_repro.py` | section 4's validity, taxonomy, scores and prompt digests. `arm_f_repro.py` writes its replay to `arm_f_candidates.replay.jsonl` (gitignored) and prints MATCH/MISMATCH against the checked-in `arm_f_candidates.jsonl` on the scientific fields — it never modifies the ledger, so a fresh clone stays clean after replay |

Section 3's raw rows live under `sec3_artifacts/`. Every figure in section 3 is
now replayed by one of the scripts above; no tail is left for the reader to compute.

The sections below describe re-running the *experiment*, which needs a GPU.

### 1. Upload to Kaggle (recommended, free GPU)

1. Go to kaggle.com → Notebooks → New Notebook
2. File → Import Notebook → upload `precision-cliff-kaggle.ipynb`
3. In the notebook, set `RUN_PILOT = True` in Cell 8
4. Run all cells (Runtime → Run All)
5. Kaggle gives you a T4 x2 GPU automatically
6. First run downloads ~4.5GB GGUF model, then runs 50 generations
7. Results appear in the output + saved to /kaggle/working/

### 2. Upload to Google Colab

1. Go to colab.research.google.com → File → Upload Notebook
2. Upload `precision-cliff-kaggle.ipynb`
3. Runtime → Change runtime type → T4 GPU
4. Set `RUN_PILOT = True` in Cell 8
5. Run all

### 3. Full Sweep (after pilot succeeds)

Modify the precision list in Cell 7 to iterate over:
- FP16, Q8_0, Q4_K_M, Q3_K_M, Q2_K

Run 5 seeds per precision. Expect ~50 min per seed on T4.
Total: ~25 hours GPU time. Kaggle gives 30h/week free.

### File Locations

Only files actually in this repository are listed. Anything named in sections 1-3
above (`precision-cliff-kaggle.ipynb` and the older `*-paper.md` /
`*-future-papers.md` / `findings.md` / `overview.md` drafts) lived on the
authoring host and is **not** in the release; those sections describe how the
experiment was originally run, not a procedure a reader can follow from a clone.
Reproducing the *figures* needs none of them — see section 0.

- `paper2_draft.md` — the current manuscript, and the only one
- `paper1_draft.md` / `latex1/` — companion paper
- `latex2/` — STALE conversion of paper 2, frozen 19 revisions back; see README
- `sec3_artifacts/` — every section 3 ledger, preregistration and provenance file
- `sec3_*.py`, `sec4_independent_rescore.py`, `arm_f_repro.py` — reproduction scripts
- `requirements.txt` — dependencies for those scripts
- `STATE.md` — project status
- `paper2_drafts/` — every revision of paper 2, one file per version

## Paper 1 (anchoring): regenerating every table and figure

All scripts run from the repository root with no arguments and read only the
ledgers named in the paper. Each prints the table it backs and, where noted,
freezes a JSON/TXT report beside the ledger.

| Paper section | Command | Reads | Writes |
|---|---|---|---|
| 3.2 square arm, 3.3 falsifier, Table 1 | `python arm_f_repro.py` | `arm_f_candidates_v2.jsonl` | stdout |
| 3.2 structural column (post hoc) | `python diagnostics_kmatch.py` | `arm_f_candidates_v2.jsonl` | stdout |
| 3.2 uniform-template null (post hoc) | `python diagnostics_template_null.py` | `arm_f_candidates_v2.jsonl` | stdout (frozen in `diagnostics_template_null_out.txt`) |
| 3.4 arm M | `python arm_m_analysis.py` | `arm_m_collect.jsonl` | `arm_m_report.json`, `arm_m_scored.json` |
| 3.5 arms MU and CH (one script, two sections) | `python arm_mu_analysis.py` | `arm_mu_collect.jsonl` | `arm_mu_results.txt` |
| 3.6 GM chain / GM3, Figure 2 | `python arm_gm3_analysis.py` then `python fig_gm3_anchoring.py` | `arm_gm_gm3_checkpoint.jsonl` | `arm_gm3_report.json`, `fig_gm3_anchoring.png` |
| 3.6 arm V | `python arm_v_score.py` | `arm_v_candidates_raw.jsonl` | `arm_v_scored.jsonl` (stdout verdicts frozen in `arm_v_score_final.txt`) |
| 3.7 code channel: CC, then CC2 and CCS together | `python arm_cc_analysis.py`, `python arm_cc2_analysis.py` | `arm_cc_collect.jsonl`, `arm_cc2_collect.jsonl`, `arm_ccs_collect.jsonl` | `arm_cc_report.json`, `arm_cc2_report.json`, `arm_ccs_report.json` |
| 3.8 arm CN | `python arm_cn_analysis.py` | `arm_cn_collect.jsonl` | `arm_cn_report.json`, `arm_cn_scored.json` |
| 3.9 arm CP (perturbed container) | `python arm_cp_analysis.py` (prompts/values: `python arm_cp_build.py`) | `arm_cp_collect.jsonl`, `arm_cp_prompts.json` | `arm_cp_report.json` |
| 3.9 arm RP (direct recall) | `python arm_rp_analysis.py` (prompts/values: `python arm_rp_build.py`) | `arm_rp_collect.jsonl`, `arm_rp_prompts.json` | `arm_rp_report.json` |
| 3.9 arm RP positive control (amendment 1) | `python arm_rp_control_analysis.py` | `arm_rp_control_collect.jsonl` | `arm_rp_control_report.json` |
| 3.9 arm PP (paraphrase probe) | `python arm_pp_analysis.py` (prompts/hashes: `python arm_pp_build.py`) | `arm_pp_collect.jsonl`, `arm_pp_prompts.json` | `arm_pp_report.json` |
| 1.1 bound table, 4.2 rectangle, LP oracle | `python n_sweep_forecast.py`, `python rect_forecast.py` | none | `n_sweep_forecast.json`, `rect_forecast.json` |
| 6.2 arm T, Table 3 | `python arm_t_analysis.py` | `arm_f_candidates_v2.jsonl` | stdout |
| Figures 1, 3, 4 | `python fig_scripts.py` | ledgers above | `fig1_trapzones.png`, `fig2_packings.png`, `fig3_armT.png` |

Script names that differ from this table on your checkout are listed by
`ls arm_*_analysis.py arm_*_score.py`; the paper's Appendix B names the
exact file behind each number.
