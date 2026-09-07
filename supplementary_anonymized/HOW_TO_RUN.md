## How to run the reproduction scripts

Two companion submissions share this bundle: the anchoring paper (paper 1)
and the transfer paper (paper 2). Every count, table and figure either paper
reports regenerates from the ledgers shipped here by one of the commands
below. Install once with `pip install -r requirements.txt` (numpy, scipy,
rapidfuzz; matplotlib only for the three figure scripts). Run every command
from the bundle root unless the table says otherwise; none needs a network
connection, an API key or a GPU.

Runners and builders (`arm_*_run.py`, `arm_*_build.py`, `arm_l_step.py`,
`arm_g_rect.py`, `arm_b_baseline.py`, `arm_b_bridge_run.py`) are shipped so
the collection procedure is inspectable. They need a serving path, so they
are documented as how each ledger was collected, not as replays.

### Replay gate

```
python -X utf8 replay_gate.py <bundle root> --timeout 3600
```

runs every script named in this file and in `BUNDLE_README.md` from the
packaged bundle, in a clean directory, and writes `replay_gate.json` with a
status per script (OK, FAIL, TIMEOUT, MISSING, or SKIP_LIVE for the runners
above). The four code-channel scorers execute the model-written programs
they score, under the registered 120 s per-program limit, so a full replay
takes tens of minutes rather than seconds.

### Paper 2 (transfer): "Characterize Before You Loop"

| Paper section | Command | Reads | Writes |
|---|---|---|---|
| §2 independent re-score (135 cell-level counts) | `python -X utf8 arm_transfer_independent_rescore.py` | every arm ledger below, `n_sweep_forecast.py` | `arm_transfer_independent_rescore.json` |
| §4 arm MU, Table 2 | `python -X utf8 arm_mu_analysis.py` | `arm_mu_collect.jsonl` | `arm_mu_results.txt` |
| §4 arm MU clearance re-read (post hoc), the 18 / 9 / 61 split | `python -X utf8 paper_repo/loop/arm_mu_ceiling.py` | `arm_mu_collect.jsonl`, `arm_mu_scored.json` | `paper_repo/evidence/arm_mu_ceiling.json` |
| Supplement S2 per-row table of the 18 MU outputs | `python -X utf8 paper_repo/loop/r26_mu_rows.py` | `paper_repo/loop/round22e_facts.json`, `arm_mu_prompts.json` | `paper_repo/loop/r26_mu_rows.json` |
| §5 arm L, Table 3 | `python -X utf8 arm_l_analysis.py` | `arm_l_collect.jsonl` | `arm_l_report.json` |
| §5 arm L residuals and the L3 Fisher test (post hoc) | `python -X utf8 arm_l_residuals.py` | `arm_l_collect.jsonl`, `arm_l_report.json` | `arm_l_residuals.json` |
| §6 arm P | `python -X utf8 arm_p_analysis.py` | `arm_p_collect.jsonl` | `arm_p_report.json` |
| §6 arm P-D | `python -X utf8 arm_pd_analysis.py` | `arm_pd_collect.jsonl` | `arm_pd_report.json` |
| §7 arms GM, GM2 | `python -X utf8 arm_gm_analysis.py`, `python -X utf8 arm_gm2_analysis.py` | `arm_gm_*checkpoint.jsonl`, `arm_gm2_*` | `arm_gm_v2_report.json`, `arm_gm2_report.json` |
| §7 arm GM3, Figure 1 | `python -X utf8 arm_gm3_analysis.py` then `python -X utf8 fig_gm3_anchoring.py` | `arm_gm_gm3_checkpoint.jsonl` | `arm_gm3_report.json`, `fig_gm3_anchoring.png` |
| §7 GM3 structural check, 27 of 27 at the argmax value (post hoc) | `python -X utf8 diagnostics_gm3_rival.py` | `arm_gm3_candidates.jsonl` | stdout |
| §7 arm V, Table 4 | `python -X utf8 arm_v_score.py` | `arm_v_candidates_raw.jsonl` | `arm_v_scored.jsonl` (verdicts frozen in `arm_v_score_final.txt`) |
| §7 GM3 and V clearance re-read (post hoc), Supplement S4 | `python -X utf8 arm_ceiling_gm3_v.py` | `arm_gm3_candidates.jsonl`, `arm_v_scored.jsonl` | `arm_ceiling_gm3_v.json` |
| Supplement S5 template-shape null | `python -X utf8 diagnostics_transfer_null.py` | `arm_v_scored.jsonl`, `arm_gm_gm3_checkpoint.jsonl` | `diagnostics_transfer_null.json` |
| Evidence gate: every residual and clearance sentence against its ledger field | `python -X utf8 paper_repo/loop/evidence_gate.py` | `paper_repo/paper/*.tex`, `paper_repo/loop/r27_evidence.json`, the ledgers it names | stdout (exit 1 on any mismatch) |

`arm_v_score.py` imports `arm_f_repro.py`, the anchoring paper's scorer,
unchanged. `arm_pd_analysis.py` imports `arm_p_analysis.py` unchanged.

### Paper 1 (anchoring): regenerating every table and figure

| Paper section | Command | Reads | Writes |
|---|---|---|---|
| §2.3 branch-rule scope, the admissible-order count | `python -X utf8 paper_repo/loop/extend_branch_scope.py` | none (closed form) | `paper_repo/evidence/extend_branch_scope.json` |
| §3.2 Table 1, who clears the family argmax | `python -X utf8 paper_repo/loop/build_channel_table.py` | `paper_repo/evidence/arm_{b,cc,ccp,cl,clw,p}_report.json`, `paper_repo/evidence/cl_lenient.json`, `arm_cc2_report.json`, `arm_ccs_report.json`, `arm_f_candidates_v2.jsonl`, `arm_m_scored.json` | `paper_repo/paper/tab_channel.tex`, `paper_repo/evidence/channel_table.json` |
| §3.3 direct emission, the falsifier | `python -X utf8 arm_f_repro.py` | `arm_f_candidates_v2.jsonl` | `arm_f_candidates.replay.jsonl`, MATCH/MISMATCH on stdout |
| §3.3 Figures 1, 2, 3 | `python -X utf8 fig_scripts.py` | ledgers above | `fig1_trapzones.png`, `fig2_packings.png`, `fig3_armT.png` |
| §3.4 arm CC, then CC2 and CCS together | `python -X utf8 arm_cc_analysis.py`, `python -X utf8 arm_cc2_analysis.py` | `arm_cc_collect.jsonl`, `arm_cc2_collect.jsonl`, `arm_ccs_collect.jsonl` | `arm_cc_report.json`, `arm_cc2_report.json`, `arm_ccs_report.json` |
| §3.5 arm CL (library programs) | `python -X utf8 arm_cl_analysis.py` | `arm_cl_collect.jsonl` | `arm_cl_report.json` |
| §3.5 arm CL lenient reparse and recount | `python -X utf8 paper_repo/loop/cl_lenient_reparse.py`, `python -X utf8 paper_repo/loop/recount_cl.py` | `arm_cl_collect.jsonl`, `arm_cl_report.json` | `paper_repo/evidence/cl_lenient.json`, `paper_repo/evidence/cl_recount.json` |
| §3.5 arms CCP and CLW | `python -X utf8 arm_ccp_analysis.py`, `python -X utf8 arm_clw_analysis.py` | `arm_ccp_collect.jsonl`, `arm_clw_collect.jsonl` | `arm_ccp_report.json`, `arm_clw_report.json` |
| §4.1 arm CH attempt counts | `python -X utf8 paper_repo/loop/arm_f_attempt_uncond.py`, `python -X utf8 paper_repo/loop/arm_f_attempt_control.py` | `arm_f_raw.json` | `paper_repo/evidence/arm_f_attempt_uncond.json`, `paper_repo/evidence/arm_f_attempt_control.json` |
| §4.1 arms MU and CH (one script, two papers) | `python -X utf8 arm_mu_analysis.py` | `arm_mu_collect.jsonl` | `arm_mu_results.txt` |
| Appendix C, Supplement S4: arm M | `python -X utf8 arm_m_analysis.py` | `arm_m_collect.jsonl` | `arm_m_report.json`, `arm_m_scored.json` |
| Appendix C: GM3 | `python -X utf8 arm_gm3_analysis.py` | `arm_gm_gm3_checkpoint.jsonl` | `arm_gm3_report.json` |
| Appendix C, Supplement S9.1 bound table, S5 rectangle, LP oracle | `python -X utf8 n_sweep_forecast.py`, `python -X utf8 rect_forecast.py` | none | `n_sweep_forecast.json`, `rect_forecast.json` |
| Appendix C, Supplement S6: arm T | `python -X utf8 arm_t_analysis.py` | `arm_f_candidates_v2.jsonl` | stdout |
| Supplement S1 pooled zero, the 1e-9 recount | `python -X utf8 paper_repo/loop/recount_1e9.py` | `arm_cc_collect.jsonl` and the other code-channel ledgers | `paper_repo/evidence/valid_1e9_counts.json` |
| Supplement S9 mode prediction, the k = 8, 9 extension | `python -X utf8 paper_repo/loop/lp_extend_k89.py` | `n_sweep_forecast.py` | `paper_repo/evidence/lp_extend_k89.json` |
| Supplement S9 structural column (post hoc) | `python -X utf8 diagnostics_kmatch.py` | `arm_f_candidates_v2.jsonl` | stdout |
| Supplement S9, S10 uniform-template null (post hoc) | `python -X utf8 diagnostics_template_null.py` | `arm_f_candidates_v2.jsonl` | stdout (frozen in `diagnostics_template_null_out.txt`) |
| Supplement S9.4 arm CN | `python -X utf8 arm_cn_analysis.py` | `arm_cn_collect.jsonl` | `arm_cn_report.json`, `arm_cn_scored.json` |
| Supplement S9.5 arm CP (perturbed container) | `python -X utf8 arm_cp_analysis.py` | `arm_cp_collect.jsonl`, `arm_cp_prompts.json` | `arm_cp_report.json` |
| Supplement S9.5 arm RP (direct recall) and its positive control | `python -X utf8 arm_rp_analysis.py`, `python -X utf8 arm_rp_control_analysis.py` | `arm_rp_collect.jsonl`, `arm_rp_control_collect.jsonl` | `arm_rp_report.json`, `arm_rp_control_report.json` |
| Supplement S9.5 arm PP (paraphrase probe) | `python -X utf8 arm_pp_analysis.py` | `arm_pp_collect.jsonl`, `arm_pp_prompts.json` | `arm_pp_report.json` |
| Supplement S10 ambition diagnostic (post hoc) | `python -X utf8 diagnostics_ambition.py` | `arm_f_candidates_v2.jsonl` | stdout |

The prompt and hash files behind arms CP, RP and PP regenerate with
`arm_cp_build.py`, `arm_rp_build.py` and `arm_pp_build.py`; these are
builders, listed above as not replayed. Supplement S5's rectangle arm G was
collected by `arm_g_rect.py`, which takes lineage arguments and a serving
path; its ledger is scored by `arm_f_repro.py`.

### Earlier project: the precision-cliff quantization ladder

The scripts below belong to the earlier project this corpus grew from and
stay bundled because their ledgers live under `sec3_artifacts/`. None of
either companion paper's numbers depends on them. All run from the bundle
root with no arguments.

| script | what it reproduces |
|---|---|
| `sec3_ladder_repro.py` | 14B ladder viability, validity, echo, per-seed and must-differ counts, and five Fisher tails |
| `sec3_dispersion_registered.py` | both dispersion-probe waves: registered echo measures, the post hoc decomposition, quality forks |
| `sec3_dispersion_prereg_rule.py` | wave 1's locked decision rule (returns *unclassified*) |
| `sec3_registered_echo_test.py` | wave 1's registered primary echo JT, `score_delta` CIs, orthogonality diagnostic |
| `sec3_search_progress.py` | loop-level search progress: accepted hill-climb steps per lineage across all four ladders, echo-complement identity gaps, conditional-on-departure rates, lineage-level permutation tests |
| `sec3_7b_repro.py` | the four Fisher tails no other script replays and the whole 7B paragraph |
| `sec3_conditional_quality.py` | conditional-on-departure improvement rate over both fixed-parent probe waves |
| `sec3_horizon_power.py` | the argument that final best score is a maximum statistic; its power table is withdrawn in the script's closing block |
| `sec3_artifacts/dispersion_probe_v2/analyze_v2.py` | wave 2's registered analysis and its `VERDICT: FAILED` label |
| `sec6_cv_canary_audit.py` | the duration-CV serving canary self-audit |
| `sec4_independent_rescore.py` | that project's validity, taxonomy, scores and prompt digests, an independent re-score of `arm_f_raw.json` |

The GPU experiment those scripts analyze ran from a Kaggle notebook that is
not part of this release; the sections above need none of it.
