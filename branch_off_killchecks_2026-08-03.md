# Branch-off kill-check panel — 2026-08-03

Five expansion ideas adversarially reviewed (independent web-searching reviewers, KILL default under uncertainty). All five killed.

## 1. Discrete geometry angle (LLM vs Packomania) — KILL
- AlphaEvolve lineage (OpenEvolve, ShinkaEvolve, ThetaEvolve, SeaEvo, optimize_anything, Helix) already published LLM-vs-solver on our exact objective (max sum-of-radii, n=26 = 2.63586–2.63598; n=21 in their set).
- Packomania/Specht tables are the wrong objective: equal circles max-min-separation or prescribed integer radii, not free-radii max-Σr. No proven-optimal table exists for our variant at any N.
- Salvage: positioning sentence — ALREADY IN PAPER (§ bound-table discussion cites ShinkaEvolve record + per-N deficits).

## 2. Standalone structured-output eval — KILL
- Scooped: Tam et al. EMNLP 2024 (format vs performance), Format Sensitivity Index (arXiv 2607.09665, 140k generations, token-controlled), StructEval/JSONSchemaBench lineage.
- Our 0/140 GM2 result carries a live truncation confound (4,096-token cap, deliberation cut off) until GM3 (16k budget, finishReason logged) reports.
- Salvage: GM3 doubles as the confound-resolving rerun; paper 2 keeps format lottery as one paragraph, not a paper.

## 3. Human-anchoring comparison — KILL
- Scooped: arXiv 2408.09656 (human vs LLM random-number attractors), 2412.06593, 2511.05766, IEEE MIS 2025 anchoring index work.
- Task not administrable to humans in comparable format (numeric radii list has no human analogue; GUI version = interface confound).
- IRB hard gate for HS author + Prolific; ISEF SRC pre-approval non-retroactive.
- Power: hundreds of paid subjects needed vs 20-sample LLM cells.

## 4. Contamination-proof benchmark reframe — KILL
- LP bound is upper bound, not ground truth; published LP-relaxation gaps grow with N — the knob we vary.
- Dynamic-eval space saturated + surveyed (DyVal, DARG, TreeEval, VAR-MATH, LiveBench, MMLU-CF).
- Our task family is the MOST-contaminated instance in the space (canonical AlphaEvolve benchmark).
- DMLR/NeurIPS D&B require hosting/maintenance/leaderboard commitments a reframe cannot meet.

## 5. Cross-domain entropy link (2607.01233 joint framing) — KILL
- Diversity-collapse literature saturated (Artificial Hivemind 2510.22954; Price of Format 2505.18949 — template prompting collapses diversity, i.e. our finding already published in general form).
- Binned scalar entropy vs semantic-cluster entropy share a symbol, not a scale — "substrate-independent" claim unmeasurable as proposed.
- Paper 1 stopping rule blocks in-paper analysis anyway.
- Note: reviewer could not find 2607.01233 in index; VERIFIED REAL post-panel via arxiv.org/abs/2607.01233 ("Measuring the Gap Between Human and LLM Research Ideas", Chen, Zhao, Cohan). Citation stands.

## Net actions taken
1. §8 hedge added to paper1_draft.md: GM2 0/140 explicitly flagged as truncation-vs-format-inability ambiguous, resolution deferred to GM3.
2. No branch papers started. Effort stays on: GM/GM3 completion, paper 1 submission ladder (arXiv → workshop → TMLR/JEI).
