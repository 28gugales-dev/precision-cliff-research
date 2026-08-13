## STATE — Precision Cliff project
**Date:** 2026-07-17
**Phase:** Pilot complete (real data) · paper revised · precision sweep still OPEN

### Current ground truth

- **Real pilot (the only citable run):** 5 seeds × 10 gens, Claude Haiku proposer,
  deterministic Python evaluator, live per-candidate logging.
  Location: `~/research-corpus/agent-run/` (candidates.jsonl, sweep_results_real.json,
  probe/, figures/, harness.py, state/, prop/).
  Findings: viability 98% (CI [89.5, 99.6]), validity 90% (CI [78.6, 95.7]); all 5
  seeds converge to canonical 2.5414 (never exceeded; optimum 2.6359); zero-shot
  control 6/6 valid, range 1.49–2.54, only 1/6 canonical → loop = recall amplifier.
- **Excluded pilot:** DeepSeek-attributed data had a reconstructed (non-logged) audit
  trail → moved to `~/research-corpus/superseded/` with README. Not citable.
  `kaggle-results/20gen.log` is a real log of an earlier failed local run (0 viable).

### Update 2026-07-17 (three-arm revision, A-grade push)

- Ran two NEW arms + controls (all live-logged, `candidates_v2.jsonl`, 100 rows):
  Arm B = Sonnet/unit-square/no-code (same 2.5414 ceiling, 4/5 seeds; 1 seed trapped
  at hex local optimum 2.5234); Arm C = Haiku/rectangle 1x0.83 non-memorizable
  (variance returns: bests 2.158-2.300, std 0.065; 2 genuine climb events).
- Zero-shot controls: sonnet no-code (2.418-2.5414, 2/6 canonical); tool-augmented
  sonnet probes wrote scipy optimizers, best 2.6359805 strict-verified (> AlphaEvolve's
  published 2.635862) — see probe_v2/provenance.json.
- Paper fully rewritten around 4-condition study; `precision-cliff-paper-combined.md`
  is CANONICAL; the per-section dir is stale (see its 00-README.md).
- New artifacts: harness_v2.py, state_v2/, prop_v2/, probe_v2/, candidates_v2.jsonl,
  results_v2.json, results_three_arms.json, figures/fig3_three_arms.png.

### Update 2026-07-17 (Arm D — program evolution)

- Ran Arm D: Haiku proposers write PYTHON PROGRAMS (not coordinates); harness_v3.py
  executes them sandboxed (AST allowlist math/random/itertools/functools, banned
  names, `python -I`, 30 s kill) and scores output with the same evaluator.
  5 seeds × 10 gens = 50 calls, all live-logged to candidates_v3.jsonl
  (reconstructed:false). Fixed prompt all 50 invocations (1 disclosed deviation:
  seed 789 gen 5 timeout warning). Tool-use audit: 48/50 exactly Read+Write;
  2 three-call agents resumed and audited (Edit / re-Read, no execution).
- RESULT: program evolution restores genuine search on the memorizable task
  (5/5 seeds improve mid-run, 12 events, five distinct non-canonical endpoints)
  but does NOT escape the recall ceiling at matched budget: best 2.5371 < 2.5414.
  Viability collapses to 33/50 (66%, CI [52.2,77.6]); taxonomy: 10 timeout,
  3 crash, 4 wrong-count. Mean best 2.2460 ± 0.3196 (population-std convention
  matching arms A-C; sample std 0.3573; both in results_armD.json).
  Uniform climb counts across arms: A=5, B=17, C=8, D=12 — destinations, not
  counts, separate recall (single attractor) from search (dispersion).
- Artifacts: harness_v3.py, state_v3/, prop_v3/ (50 programs), candidates_v3.jsonl,
  results_v3.json, results_armD.json, stats_v3.py, figures/fig4_program_evolution.png.
- Paper now FOUR-arm: subtitle updated, new §5.7, tool section → §5.8, figures → §5.9,
  new §6.5 compute-access spectrum, contribution 4 added (5 total), counts 200 loop /
  224 invocations, program-evolution limitation rewritten as tested-at-budget,
  Appendix A.4 (Arm D prompt + deviation + audit).

### Update 2026-07-17 (PRECISION SWEEP COMPLETE — original question answered)

- Owner ran `kaggle_precision_sweep.py` on Kaggle 2xT4 to completion: Qwen2.5-Coder-7B
  GGUF ladder fp16/q8_0/q4_k_m/q3_k_m/q2_k, 5 seeds x 10 gens + 6 probes per
  precision = 250 loop + 30 probe rows, all live-logged, sha256-pinned weights.
  Data at `agent-run/precision_sweep/` (candidates_precision.jsonl 250 rows,
  probes_precision.jsonl 30 rows, state/, provenance.json). Integrity verified
  locally (stats_precision.py): 250/30 rows, all reconstructed:false, no dup/missing.
- RESULT — no cliff, capability floor: viability fp16 7/50, q8 6/50, q4 9/50,
  q3 7/50 (flat 12-18%, fp16-vs-q3 Fisher p=1.0), q2_k 16/50 (32%, post-hoc
  inversion, p=0.007 vs pooled uncorrected). Probes 0/30 valid; canonical 2.5414
  NEVER emitted (0/280); best anywhere 1.79998 (q3 seed 1111 = doubled 0.89999
  seeded-baseline grid). Mechanism: viability == count accuracy (only 45/250
  proposals emit exactly 26 circles; modal count 25 for fp16..q3 = systematic
  undershoot; q2_k distribution broader + centered on 26 = "format lottery").
- Paper updated (canonical combined.md): subtitle + abstract para + contribution 6 +
  intro Q5 + new SS3.4 protocol (metrics now SS3.5) + SS4 totals (504 invocations) +
  new SS5.9 results (figures now SS5.10, figs 5-7 added) + new SS6.6 (implications
  now SS6.7) + conclusion + limitations bullet rewritten + future-work 1 rewritten
  (above-the-floor sweep) + Appendix A.5 (sweep prompts verbatim).
- New artifacts: stats_precision.py, results_precision_local.json,
  figures/fig5_precision_cliff.png, fig6_packing_portraits.png, fig7_count_drift.png.
- Open follow-up: 14B ladder (config patch = REPO Qwen2.5-Coder-14B-Instruct-GGUF,
  WORK /kaggle/working/precision_sweep_14b, q8_0 min_gpus 2) — proposer above floor.

### Update 2026-07-18 (14B rung run — NOVELTY CLIFF found; data-loss disclosure)

- Owner ran 14B ladder (q8_0/q4_k_m/q3_k_m/q2_k, 224 gens) to [done]. Session
  expired BEFORE download: jsonl/probe-raws/checkpoints LOST. Verbatim console
  log survives (notebook Quick Save version history) and is archived at
  `agent-run/precision_sweep_14b_console.log` + README with provenance rules.
  All 14B numbers recomputed from the log by `stats_precision_14b.py` →
  `results_precision_14b_local.json`. NEVER back-fill jsonl from it.
- RESULTS: viability 22/22/24/19 per 50 (flat, CIs overlap) — scale effect vs 7B
  87/200 vs 38/200, Fisher p=1.7e-7; probes 0/24 (recall still absent);
  best 1.625. NOVELTY CLIFF between 3.91 and 3.35 bits: seeds improving past
  seeded baseline 5/5, 5/5, 5/5 vs 1/5 at q2_k (p=0.001); parent-echo (SCORE-
  INFERRED: valid rows scoring exactly their lineage's RUNNING parent)
  4/18, 4/20, 4/19 vs 17/18 (p=2.5e-8). CORRECTION 2026-07-18: first stats
  version compared to hardcoded baseline only (reported 1/18,2/20,0/19 vs
  16/18) — undercounted upper-rung echoes 4x; caught by hostile method
  reviewer, recomputed against running parent. 2-bit keeps format+geometry,
  loses ability to propose novel mutation — invisible to viability/validity.
- Paper updated: §3.4 second-rung protocol + disclosure; §5.9 retitled ("...A
  Capability Floor at 7B, a Novelty Cliff at 14B") + fourth finding + 14B table;
  fig8 (fig8_14b_novelty_cliff.png, make_fig8_14b.py); abstract, contribution 6,
  §6.6, conclusion, limitations (console-log bullet), future work 1 all updated.
  Study totals now 728 invocations.
- Echo classification is score-inferred, not coordinate-verified — re-run to
  durable storage listed in future work if verification wanted.

### Update 2026-07-18 (external-review revision — constructible-attractor reframe)

- Two external reviews received; harsh one (major revision) ~90% validated. All 9 major
  + 11 minor items fixed. NEW EXPERIMENTS (live-logged, citable):
  * Best-of-50 zero-shot control (agent-run/probe50/, probes_bestof50.jsonl,
    score_probe50.py, probe50_README.md): 50 haiku + 50 sonnet independent zero-shot
    samples, fixed prompt. RESULT: best-of-50 == loop value EXACTLY both tiers
    (2.541421); haiku 45/50 valid, 28 at ~2.5414; sonnet 50/50, 29; 0/95 valid above.
    Loop = selection, confirmed. Canonical rate ~60% per draw (n=6 estimates were noise).
  * Direct knowledge probes (probe_knowledge/): 6/6 disclaim published value for the
    objective; 1/6 recalls Friedman catalog exists, no values. Retrieval ruled out.
- Fact-check (web-verified): objective IS catalogued — Friedman "Circles in Squares"
  since 2011, N=26 ~2.634 (Cantrell 2011/Specht 2012) pre-AlphaEvolve. 2.5414 grid
  appears in NO catalog. So: constructible ATTRACTOR, not recall. Paper reframed
  throughout (title, abstract ~330 words, contributions, §5.5 rewritten around 3
  controls, §6.1, conclusion). "known optimum" -> "best known value" everywhere.
- Other fixes: Arm A demoted to pilot (prompt baked in result; B + best-of-50 carry
  the finding); seed-level tests primary / candidate-level descriptive
  (pseudo-replication); novelty cliff labeled PRELIMINARY pending re-run (title
  mention removed); budget currency defined (Arm D compute-subsidized 471s CPU and
  still loses); truncation ruled out for format lottery (max 687 of 1200 tokens);
  §5.8 reports ALL five tool scores (2.528-2.636, all above ceiling; probe_s_4
  stalled) and reframes best as matching contemporary record; rectangle confound
  disclosed; QD framing dropped to nominal; refs 13->17 (Friedman, Sainz, Golchin,
  Deng); A.6 control prompts + A.7 harness map added; "released" -> "available on
  request" (no repo yet). Study total 834 invocations.

### Update 2026-07-18 (14B REPLICATION LAUNCHED — Kaggle batch API)

- Owner provided Kaggle API token; run pushed as BATCH kernel (no interactive
  session, output auto-saved at completion — session-expiry loss mode gone):
  kernel `sohamgugalet/precision-sweep-14b-v2`, machine_shape NvidiaTeslaT4
  (T4 x2), status RUNNING as of push. Exact pushed code archived at
  `agent-run/kaggle_precision_sweep_14b_v2_pushed.py`; local durable copy
  `agent-run/kaggle_precision_sweep_14b.py`.
- Protocol identical to lost 2026-07-18 run; logging-only additions:
  (1) per-candidate COORDINATES in jsonl (enables coordinate-verified
  parent-echo, killing the score-inferred caveat), (2) every row echoed to
  console as "JSONL|" line (recoverable from version history even on total
  file loss), (3) zip snapshot per condition. q8_0 min_gpus=2 guard skips
  it if Kaggle assigns a single GPU.
- PREREGISTERED predictions baked into pushed script header (timestamped by
  Kaggle before execution): P1 improvement >=4/5 seeds upper rungs vs <=2/5
  q2_k; P2 coordinate-verified echo >=60% q2_k vs <=35% upper; P3 viability
  flat; P4 probes ~0 valid, canonical never emitted. Disconfirmation rule:
  P1+P2 both fail at q2_k -> withdraw cliff section.
- On completion: `kaggle kernels output sohamgugalet/precision-sweep-14b-v2`
  pulls jsonl/state/provenance; then recompute stats, coordinate-diff echoes,
  upgrade paper §5.9 from preliminary if replicated.

### Update 2026-07-18 (14B REPLICATION COMPLETE — cliff coordinate-verified)

- Batch kernel finished ~04:12 (~2h). Data at
  `agent-run/precision_sweep_14b_v2_output/precision_sweep_14b/`
  (candidates 200 rows + probes 24, all reconstructed:false, coordinates
  logged; provenance sha-matched, 2xT4). Bit-identical to original run on
  every console-logged field (scores, viability 22/22/24/19) — llama.cpp
  seeded sampling deterministic; console log NEVER printed tokens, so
  token-identity is NOT claimable (verifier caught this overclaim, fixed).
- COORDINATE-VERIFIED echo (stats_precision_14b_v2.py →
  results_precision_14b_v2.json): upper rungs 2/18, 3/20, 3/19 (14% pooled)
  vs q2_k 17/18 (94.4%); score-inference validated at q2_k (17/17 verbatim,
  0 rearrangements) but OVERCOUNTED upper rungs (4 of 12 score-matches are
  same-sum different-coordinate rearrangements) — cliff sharper than
  score-inferred estimate. Candidate Fisher p=5.7e-10 (descriptive);
  seed-level 15/15 vs 1/5 p=0.001 primary. ALL preregistered predictions
  (P1/P2/P4 + canonical-never) CONFIRMED. Probes 0/24.
- Paper updated (title §5.9, table row now coordinate-verified 2/3/3/17,
  §3.4 replication para, abstract, contribution 6, §6.6, conclusion,
  limitations bullet rewritten, future-work #1 replaced with mechanism
  probe, totals 1,058 invocations / 834 distinct / 774 jsonl, A.7 adds
  v2 runner, fig8 regenerated coordinate-verified). Opus hostile verify:
  every number recomputed exact; 1 finding (token overclaim) fixed.
- Citation audit: 17/17 clean; cosmetic affiliation tags stripped refs 2/4.
- PDF v3 (27pp): corpus canonical + Downloads/precision-cliff-paper-v3-verified-cliff.pdf.
- Venue/split intel (agents, 2026-07-18): STS window OPEN now, deadline
  Nov 5 2026 8PM ET; TMLR new per-author quotas Jul 2026; arXiv needs
  endorsement (Jan 2026 policy: institutional email no longer enough);
  NeurIPS HS track dormant; GECCO 2027 = Jul 12-16 Krakow, CFP not out.
  Split ranking: C=attractor paper (GECCO main) > B=cliff paper (now
  verified, workshop/LBA) > A=whole (JEI/NHSJS/STS vehicle); D=best-of-N
  note = salami, don't.

### Update 2026-07-18 (framing revision — "re-execution" honesty pass, v4)

- Two external reviews triaged; executed wording-only fixes (owner ruled out
  new experiments): (1) "replication"->"re-execution" everywhere for our
  deterministic re-run; fresh-seed replication = future work; P1/P3/P4
  predictions labeled guaranteed-by-determinism (no evidential weight),
  P2 coordinate-level = only falsifiable ones (both held); new Appendix A.8
  with verbatim prediction block + audit; seed-level p=0.001 explicitly
  single-sampling-run, "adds no statistical evidence"; (2) abstract scoped
  "single-lineage elitist hill-climbing at 50 evaluations"; (3) §6.1
  AlphaEvolve carve-out (record-beating cannot be reproduction; claim
  targets at-or-below-zero-shot middle); (4) Brown et al. 2407.21787
  (Large Language Monkeys) added, web-verified — ref 18, sentence in §2.3;
  (5) §5.9 instruction-following-vs-novelty hedge ("novelty cliff names
  the behaviour, not a settled mechanism"; discriminating probe = FW#1);
  (6) headline count now 834 distinct invocations (1,058 total calls).
- NOT done (owner decision / later): fresh-seed Q2_K run, N=23/27 arm,
  restart arm, distance-distribution figure, venue-length cuts (GECCO 2pp),
  terminology pruning, repo. Reviews agree these are optional for
  JEI/ISEF/LBA tier.
- PDF v4 28pp: corpus canonical + Downloads/precision-cliff-paper-v4-honest-framing.pdf.

### Update 2026-07-18 (v5 — full experiment battery: fresh seeds, must-differ, Arm E, public repo)

- Owner reversed "no more experiments"; all three optional experiments run autonomously:
  1. **Fresh-seed 14B replication** (Kaggle batch `sohamgugalet/precision-sweep-14b-fresh`,
     seeds 2222/3333/5555/7777/9999, q4_k_m + q2_k, 100 candidates, coordinate-logged,
     falsifiable prereg in pushed header). RESULT: echo cliff REPLICATES — coord echo
     19/24 (79%) q2_k vs 1/17 (6%) q4_k_m, Fisher 3.4e-6 descriptive; **F1 improvement
     prediction FAILED at q2_k** (3/5 fresh seeds improved, bests 1.04/1.30/1.625;
     seed-level p=0.44) — disclosed in paper; echo rate (not improvement count) is the
     cliff's replicable signature. Data: agent-run/precision_sweep_14b_fresh_output/.
  2. **Must-differ mechanism probe** (same kernel, 10/quant, baseline parent, explicit
     must-not-copy demand). RESULT: q2_k 5/5 valid outputs verbatim copies DESPITE
     prohibition; q4_k_m 1/5 (complies). Prereg decision rule → instruction-insensitive
     = degraded constructive novelty. §5.9 mechanism hedge RESOLVED.
  3. **Arm E (N=23/27 generality)**, 100 haiku-subagent proposals via harness_v4.py,
     H1/H2 prereg in header timestamped by repo initial commit. RESULT: H1 held —
     N=27 3/5 seeds at 2.582840-844 vs constructed analog 2.5828427 (6 decimals);
     H2 dispersion branch REFUTED — N=23 4/5 seeds trapped at exactly 2.300
     (truncated 25-grid), lowest variance in study (0.025), validity halves (13/50);
     1 seed re-instantiates recipe as 4x4 grid + 7 fillers = 2.3624369 (observed
     2.362440). Attractor = PARAMETRIC RECIPE. Delivery deviations disclosed
     (3/100 in-message returns, 1 consequent parse failure; tool audit 86/11/3).
- **Public repo LIVE: github.com/28gugales-zamp/precision-cliff** (MIT, full agent-run/
  data + code + paper; excludes superseded/ + internal notes; initial commit timestamps
  Arm E prereg; second commit = all new data + paper v5; third = PDF).
- Paper v5: title "Five-Arm"; Arm E in §3.3 (table row + protocol) + new §5.10
  (Figures now §5.11) + fig9; fresh/must-differ in §3.4 + §5.9 "Fifth" + A.9;
  Arm E prereg audit A.10; contribution 3 + 6 updated; §6.4 low-variance caution;
  §6.6 mechanism line; limitations rewritten (F1 failure scoping, rectangle
  unbundling, must-differ n=5 caveat); FW #1/#3 replaced (localize cliff; map recipe
  parameter space); totals 1,054 distinct / 1,278 calls / 994 jsonl rows; repo URL
  replaces "available on request". PDF v5 34pp:
  Downloads/precision-cliff-paper-v5-full-battery.pdf + repo paper/.
- Kaggle token still in ~/.kaggle/access_token — owner should rotate now (runs done).

### Paper

- Title: "When the Loop Is Inert: Viability and Recall in LLM-Guided Circle Packing"
- Files: `precision-cliff-paper-combined.md` (canonical) + `precision-cliff-paper/`
  sections. 4-reviewer adversarial pass done (all major-revision items fixed).
- References web-verified 2026-07-17 (AlphaEvolve=Novikov 2506.13131;
  OpenEvolve=Sharma/codelion; ShinkaEvolve=Lange 2509.19349; CALM=Huang 2505.12285;
  Squeeze Evolve ref DROPPED — arXiv 2604.07725 is not a circle-packing paper).
- Figures 1–2 generated: `agent-run/figures/`.
- Appendix A: verbatim prompts incl. disclosed gen-2+ prompt change.

### Open work (the original research question)

1. **Precision sweep — Kaggle script READY, owner runs manually.**
   `agent-run/kaggle_precision_sweep.py`: self-contained resumable runner,
   Qwen2.5-Coder-7B GGUF ladder q2_k→fp16, 5 seeds × 10 gens + 6 probes per
   precision, live jsonl + sha256 provenance, checkpoint/resume, fp16 needs T4x2.
   Local smoke tests passed 2026-07-17 (evaluator/parser/resume). Fallback if
   Kaggle fails: OpenRouter quantization-routing probe (spec in HERMES_HANDOFF).
2. **Non-memorizable benchmark arm** (e.g., 26 circles in 1×0.83 rectangle, or fixed
   random radii) to separate search from recall.
3. More seeds/generations for CI tightening.

See `HERMES_HANDOFF.md` at corpus root for the full handoff.

---

## v6 (2026-07-18, evening): major-revision response — rescope + classical baseline + IQ2 control

External review verdict on v5: "major revision — reviewers will accept your data and reject your title."
Response executed same day, all numbers opus-verified clean:

- **Title rescoped**: "Selection, Not Search: A Small-Budget Elitist LLM Loop Reduces to
  Best-of-N on Circle Packing". Abstract cut to ~260 words; scoping statement added to §1
  ("the loop" = single-lineage elitist, 50 evals); sweep framed up front as unexpected finding.
- **Classical comparator** (`agent-run/baseline_classical.py`, zero LLM): raw perturbation at
  matched 50-eval budget gains ≤0.06 over the 0.9 seed; repair-decoder floor 2.167 with search
  adding nothing at this budget; 5,000-eval annealing reaches only 2.348 — attractor (2.5414)
  unreachable at 100× budget. Wired into §3.3/§5.5/§5.4/§6.1/contribution 1/conclusion.
- **IQ2 algorithm control** (Kaggle kernel sohamgugalet/precision-sweep-14b-iq2, prereg
  decision rules D1/D2/D3 in header, audited in A.12): bartowski imatrix Q2_K echo 24/32=75%
  (cliff replicates on independent weights, must-differ 6/8), IQ2_M 12/28=43% (intermediate →
  formally inconclusive between D1/D2, reported as registered). Gradient 6–15% → 43% → 75% →
  94%: cliff graded, tracks quantization quality not nominal bit-width. Data in
  `agent-run/precision_sweep_14b_iq2_output/`.
- Knowledge probes demoted to supporting evidence (verbalization caveat); candidate-level
  p-values → new A.11; must-differ "decisive" → "strongly suggestive"; "Q2_K" language
  replaces bit-width claims; fig1 rebuilt with per-seed offsets; FW#8 names pinned-API
  Arm B rerun + file-writing best-of-N as top revision experiments.
- Counts now 1,174 distinct proposer invocations / 1,398 total LLM calls (§4, stated once).
- **Repo moved to github.com/28gugales-dev/precision-cliff** (full history, hashes unchanged
  → Arm E prereg timestamp preserved; zamp copy private with MOVED pointer). Paper URLs updated.
- PDF v6 (37pp): Downloads/precision-cliff-paper-v6-revision.pdf + repo paper/.
- Deliberately skipped (Claude usage / API billing): file-writing best-of-50 rerun, Arm B
  pinned-API rerun — named honestly in Limitations + Future Work #8.

## v7 (2026-07-18, late): response to careful line-by-line review — seed-mismatch fix + copier-loophole closure

- FIXED real analytical error (reviewer-caught): §5.9 compared imatrix Q2_K (fresh seed
  values) against official Q2_K (original seeds). Seed-matched framing now throughout:
  75% vs 79% (~no calibration effect at fixed scheme); ladder = matched runs only,
  6% → 43% → 75–79%, original-seed 94%/14–15% footnoted as different seed set;
  "milder"/"quality-mediated" → "scheme-mediated". Cliff replication claim STRONGER
  (same rate on independent weights).
- NEW §5.9 seventh finding (`classify_nonviable.py`, parse-only, zero model calls):
  invalid Q2_K rows are majority NEAR-COPIES (18/32 re-exec, 15/26 fresh; 26-of-27
  circles unchanged), zero garbage/truncation at any 14B rung; copy-typed ≈70% of the
  FULL output distribution → validity-filter explanation of the echo rate ruled out;
  near-copy fraction among failures tracks the same scheme gradient (0/33 → 2/22 →
  5/18 → 15/26–18/32).
- fig8 right panel regenerated: echo bars primary (11%→94%), seeds-improving demoted.
- Minors: "nominally full precision, not verifiable" (§4); Arm E climb-note (ascents
  into trap); 2.348 consistent.
- Sonnet verifier recomputed everything independently: zero discrepancies, no remaining
  cross-seed comparisons. PDF v7 (38pp): Downloads/precision-cliff-paper-v7-final.pdf +
  repo. Commit 255ac40 pushed to github.com/28gugales-dev/precision-cliff.
- Delegation per user directive: subagents sonnet/haiku only, paper prose edits by main
  (fable) only.

## v8 (2026-07-30): Future Work #3 executed — the recipe's parameter space, in closed form

**What #3 asked for:** "a *sweep over N* — locate every N where some k×k-grid
parameterization fits cleanly and predict, in closed form, where the loop converges vs
traps, turning the parametric-recipe account into a quantitative forecast; plus N values
(e.g. primes near 30) where no grid parameterization is natural."

**Done.** `n_sweep_forecast.py` (+ `n_sweep_forecast.json`).

### The recipe, written out
    V(k, m) = k/2 + m*(sqrt2 - 1)/(2k),   0 <= m <= (k-1)^2      [k x k grid + m fillers]
    T(k, N) = N/(2k),                     N < k^2                 [grid truncated]
    r_grid = 1/(2k)      r_filler = (sqrt2 - 1)/(2k)

Reproduces every number §5.10 reports, with no fitting: V(5,1)=2.5414214 (N=26 Arm B),
V(5,2)=2.5828427 (N=27 H1), T(5,23)=2.300 (N=23 trap), V(4,7)=2.3624369 (N=23 escape),
V(5,0)=2.500. 5/5.

### The missing piece #3 needed: a selection rule
Converge-vs-trap is not determined by the recipe alone — it needs k*(N), the k the model
reaches for. Four candidates scored against the three anchors (k AND branch must both
match): `nearest` 3/3, `floor` 2/3, `argmax` 2/3, `ceil` 1/3. Unique survivor:

    k*(N) = floor(sqrt(N) + 1/2)      # nearest integer sqrt, zero free parameters
    k*^2 <= N  ->  extend with m = N - k*^2 fillers   (converge)
    k*^2 >  N  ->  truncate                            (trap)

Caveat recorded in the JSON and not softened: three anchors, four candidates, one
survivor. That is identification, not confirmation. Its value is that every other N is
now out-of-sample and falsifiable.

### Forecast
    TRAP zone, closed form:  N in [k^2 - k + 1, k^2 - 1]
      [13,15] k=4 | [21,24] k=5 | [31,35] k=6 | [43,48] k=7 | [57,60] k=8
    CONVERGE zone:           N in [k^2, k^2 + k]

Trap cost falls as N grows — worst-in-zone 8.51% (N=13), 7.03% (N=21), 6.01% (N=31),
5.25% (N=43), 4.66% (N=57) — and reaches exactly zero at the top of each zone (N=35,
N=48), where truncation happens to BE the recipe optimum. Those are traps that look like
convergence by value alone and separate only by structure.

### Two results worth putting in the paper
1. **The paper's own future-work guess about primes is wrong.** Primality does not
   partition anything: 13/23/31/43/47/59 trap, 11/17/19/29/37/41/53 converge. The
   governing quantity is the signed distance N - k*^2 — negative traps, non-negative
   converges. §5.10's N=23 is not "prime-hostile", it is three short of 25.
2. **The recipe is never competitive with the record.** Deficit vs Friedman's published
   lower bounds runs 0.02-0.26 across N=10..30 and is 0.0946 at N=26 — quantifying
   §5.1's "the catalogued near-optima never appear" as a curve rather than an anecdote.

### Verification
Every closed form recomputed by an independent LP over the actual constructed
coordinates (no knowledge of the recipe): 83 configurations, both branches, all k in
2..7, max drift < 1e-9, script aborts on disagreement. Separate guard aborts if any
predicted value exceeds a published lower bound. Cross-check: N=35 -> 2.9166667 here
matches the corrected `lattice_minus` value found independently in
`qd-contam/e2_reference.py` by a different code path.

## v8 (2026-07-30, cont.): Future Work #8 attempted — reproducibility repair, and #3 tested out of sample

**Arm F.** 25 fresh Haiku proposers, 5 each at N = 13, 17, 31, 35, 37, zero-shot
(justified by the paper's own headline: the loop reduces to best-of-N). Files:
`arm_f_repro.py`, `collect_raw.py`, `arm_f_prompts.json`, `arm_f_raw.json`,
`arm_f_candidates.jsonl` (one row per invocation, failures included).

### What #8 asked for vs what the runtime allows
The original arms ran through Claude Code subagents on the Max plan, not the HTTP API,
so the billing block that deferred this in v6 was never the real obstacle — the runtime
is. Repaired: prompt text pinned and SHA-256 hashed **before any sampling**, every raw
output stored verbatim, run date and the alias->dated-id mapping in force on that date
recorded, deterministic local scoring, predictions registered in the harness header
first. Still NOT repairable, and disclosed rather than papered over: temperature/top_p
are not exposed by the agent runtime; the alias->weights binding is a promise, not a
hash; the subagent inherits a system prompt and user-level instruction files that are
not part of the task prompt and are not fixed across time.

**That is the methodological finding, and it is worth a paragraph in §4:** an agent
runtime cannot be made reproducible from inside itself. Any LLM-evolution study built on
one inherits this. It is a property of the harness class, not an oversight — which
strengthens rather than excuses the paper's own blunt statement.

### Result: the #3 forecast survives out of sample
Fitted on N=23/26/27 only; all five N below are new.

| N  | predicted           | on-prediction | exact to 2e-6 | rival-argmax |
|----|---------------------|---------------|---------------|--------------|
| 13 | truncate  1.6250000 | 3/4           | 3             | 0            |
| 17 | extend    2.0517767 | 3/4           | 3             | 0            |
| 31 | truncate  2.5833333 | 5/5           | 4             | 0            |
| 35 | truncate  2.9166667 | 3/4           | 3             | 0            |
| 37 | extend    3.0345178 | 3/4           | 2             | 0            |

17/21 valid invocations land on the predicted construction; 15 of those to 2e-6.
**0/21 ever produced the rival-argmax value.** N=13 and N=31 are the discriminating
pair — a proposer choosing the BEST available recipe rather than the nearest-square one
would have returned 1.7761424 and 2.7485281. Across 9 valid invocations at those two N,
it returned neither, once. The nearest-square selection rule is not a curve fit to three
points; it predicts held-out behaviour.

**P4 is the one to quote.** N=37 is prime and converged cleanly on the 6x6 grid plus one
filler at (sqrt2-1)/12 — refuting the paper's own future-work guess that "primes near 30"
are where no grid parameterization is natural. Primality is not the variable; distance to
the nearest perfect square is.

**P5 held with a caveat that matters.** N=35 sits at the top of a trap zone where
truncation IS the recipe optimum, and 3/4 landed there — a trap indistinguishable from
convergence by value, separable only because the structure classifier reads the radii.
The 4th used a 7x7 lattice truncated to 35 (r=1/14, sum 2.5), a construction outside the
k*(N) rule entirely.

### Bookkeeping that would otherwise have corrupted the rates
- 5 invocations were rejected by the runtime's 20-subagent concurrency cap **before
  reaching a model**. They are not proposer failures and are excluded from the 25;
  counting them as invalid output would have understated validity by 17%.
- Validity is reported at TWO tolerances because proposers print 6-8 decimals and an
  8-decimal tangency misses by ~5e-9: at 1e-9, N=37 scores 1/5; at 1e-6, 4/5. Both are
  in the log. 1e-6 is primary — it sits far below the ~1e-2 gap between rival
  constructions, so it cannot manufacture a prediction hit. Choosing one silently after
  seeing results would have been the easiest way to fake this whole table.
- Value-matching likewise uses a loose window (which construction) and an exact window
  (rendered to full precision) — at N=31 a proposer wrote r=0.0833 and summed to 2.5823
  against an exact 2.5833333. Same construction, different rendering.
- 2 parse failures, both known modes: one emitted `1/12` fractions (not a Python
  literal), one wrapped the list in prose containing `[0,1]x[0,1]`, reproducing exactly
  the bracket-in-prose failure §5.10 logged in the original Arm E.
- One N=37 proposer derived r=(sqrt2-1)/12 correctly in prose, then wrote 0.03571429
  into the list — correct derivation, wrong transcription, and it overlaps.

### Still open
- The loop itself was not rerun, only zero-shot. The paper licenses that substitution but
  it is a substitution, not the same experiment.
- 5 samples per N. Enough to separate 0/9 from 9/9 on the discriminating pair, not enough
  for a variance claim.
- Arms A-D themselves remain unreproducible. Nothing run here changes that; only the
  disclosure improves.

## v9 (2026-07-31): second domain, deepened cells, paired trace arm

Files added: `rect_forecast.py` + `rect_forecast.json`. Extended: `arm_f_repro.py`
(N=21/43 predictions, dual-arm, faithfulness), `collect_raw.py` (multi-transcript,
trace arm). 55 invocations now logged, all rows kept including failures.

### 1. THE RULE IS NOT ABSOLUTE — N=21 breaks it
Deepening the discriminating cells to n=10 found the first rival hits.

| N  | predicted           | on-prediction | exact | rival-argmax |
|----|---------------------|---------------|-------|--------------|
| 13 | truncate  1.6250000 | 3/4  | 3 | 0 |
| 17 | extend    2.0517767 | 3/4  | 3 | 0 |
| 21 | truncate  2.1000000 | 4/7  | 4 | **2** |
| 31 | truncate  2.5833333 | 5/5  | 4 | 0 |
| 35 | truncate  2.9166667 | 3/4  | 3 | 0 |
| 37 | extend    3.0345178 | 3/4  | 2 | 0 |
| 43 | truncate  3.0714286 | 6/7  | 6 | 0 |

Across the four discriminating N (13, 21, 31, 43): 18/23 valid on prediction,
**rival 2/23**, both at N=21, both the 4x4 grid + 5 fillers = 2.2588835. Yesterday's
"0/9, never once" is now "2/23". Report the corrected number, not the earlier one.
N=21 is the SMALLEST trap zone tested and has the largest relative penalty (7.0%),
which is the natural reading: the anchor is weakest where the cost of obeying it is
highest. That is a hypothesis, not a finding - it needs the other zone-bottoms.

### 2. SECOND DOMAIN: the rule generalises to rectangles
`rect_forecast.py`. Same rule with the aspect ratio restored:

    q* = round(sqrt(N / a))    p* = round(sqrt(N * a))     -> round(sqrt(N)) at a = 1

Not refitted - the a=1 case reduces to the square rule exactly. Verified 213
configurations against an independent LP (drift < 1e-9), including a CROSS-DOMAIN
check: at a=1, p=q=k, `n_sweep_forecast.py`'s closed form must equal this file's LP.
Two files, two derivations, one number. It holds.

Traps are worse in rectangles, and shape-mismatch is far more common:

| a   | N predicted to truncate | N where predicted shape != optimal | worst gap |
|-----|-------------------------|------------------------------------|-----------|
| 1.0 | 15/36 | 12 | 8.5% (N=13) |
| 1.5 | 13/36 | 23 | 7.8% (N=31) |
| 2.0 | 14/36 | 20 | 10.3% (N=25) |
| 3.0 | 16/36 | 23 | 11.4% (N=19) |

Top probe cells for the next run: a=3 N=19 (predict 3.166667 as 8x3 truncate, rival
3.574919 as 7x2 extend, 11.4%); a=3 N=37 (4.625000 vs 5.190356, 10.9%); a=2 N=25
(3.125000 vs 3.483249, 10.3%).

**Negative result worth a sentence in the paper:** the recipe's CLOSED FORM does not
survive the move to rectangles. In the unit square every interior vertex has four
identical neighbours, so one expression covers all fillers. In a rectangle a filler
is capped by the diagonal gap AND by the spacing to adjacent fillers, and the latter
binds only when those vertices are occupied - so the cap depends on m and on which
vertices are used, and no expression in (p,q,m,a) reproduces it. Caught by the LP
gate on the first run: at a=1, p=2, q=4, m=1 a naive min(diag,hx,hy) gives 1.125
against a true 1.1545085. LP is the value oracle for the extend branch; closed form
is retained only where provably exact (full grid, truncated grid).

### 3. PAIRED TRACE ARM: eliciting a trace is an intervention
10 more N=21 proposers, identical task plus one line asking for a "METHOD:" label.

    bare   valid  7/10   values {2.1: 4, 2.2588835: 2, 2.0444444: 1}
    trace  valid 10/10   values {2.1: 9, 1.7499999: 1}

Two effects, both against the naive expectation that a label is free:
- **Validity rises**, 7/10 -> 10/10.
- **The rival construction disappears**, 2/7 -> 0/10. Asking the proposer to name its
  method pushes it toward simply-nameable constructions and away from the 4x4+5-filler
  packing that actually scores higher.
So trace-on and trace-off arms must never be pooled, and any process-descriptor study
that collects traces by asking for them is measuring a perturbed distribution. This is
the confound named as a blocker for idea G, now measured rather than assumed.

### 4. FAITHFULNESS IS AUDITABLE HERE, and traces pass
Coarse check: do the row/column counts named in METHOD appear in the layout actually
emitted? **8/8 scored traces match, 2 unscored** (claims with no numeric dims).
Including the one that lost value honestly - "Triangular hexagonal packing with
6+5+4+3+2+1 rows", 21 circles at r=1/12, sum 1.75, exactly as described.

This is the check the CoT-faithfulness literature cannot run: 2503.08679, 2606.13603
and 2605.29087 all estimate faithfulness with no ground truth, whereas here the
emitted coordinates ARE ground truth for what was built. Descriptor validity for
idea G is now measured, not assumed - and the measurement supports the premise.

### Still open
- Rectangle arm is FORECAST ONLY. No proposer has been run in a 1 x a container yet;
  the generalisation claim is untested until those cells are probed.
- n=10 at two cells, n=5 at five. Enough for 2/23; not enough for per-N variance.
- Zero-shot throughout. The loop itself has still not been rerun.

### 5. RECTANGLE ARM RUN — the generalisation claim is now tested, not forecast
`arm_g_rect.py` + `arm_g_candidates.jsonl`. 16 proposers on the two sharpest cells
from rect_forecast, in a container no proposer had been given before, under a rule
never fitted to rectangle data.

| cell        | predicted              | rival (better)         | valid | on-prediction | rival |
|-------------|------------------------|------------------------|-------|---------------|-------|
| N=19, a=3   | 3.1666667 (8x3 trunc)  | 3.5749194 (7x2 extend) | 4/8   | 2             | **0** |
| N=25, a=2   | 3.1250000 (7x4 trunc)  | 3.4832492 (6x3 extend) | 5/5   | 3             | **0** |

**5/9 valid land on the predicted value; 0/9 reach the rival.** The nearest-template
anchoring is not an artefact of the 1-parameter square case - it survives the move to
a 2-parameter template in a different container.

Two honest qualifications:
- Validity collapses in the tall container: 4/8 at a=3 versus 5/5 at a=2 and ~80% in
  the square. Three of the four failures are overlaps. Aspect ratio degrades geometric
  reliability, which is a separate finding and a confound on the a=3 cell.
- One a=3 sample beat the prediction with a construction outside the recipe family
  entirely: 5 circles at r=0.1, 10 at r=0.25, 4 at r=0.125, sum **3.5** - mixed radii,
  three distinct sizes, still below the 3.5749194 rival. Recorded as `7x11_r3`. The
  recipe is the attractor, not a ceiling.

### Running totals across both domains
Square, four discriminating N (13/21/31/43): 18/23 on prediction, rival **2/23**.
Rectangle, two discriminating cells: 5/9 on prediction, rival **0/9**.
Combined rival rate on cells where the rule and the optimum disagree: **2/32**.

**Correction to section 5 (written before the last two invocations landed).** Final
counts with all 16 rectangle proposals scored:

| cell        | valid | on-prediction | rival | best observed |
|-------------|-------|---------------|-------|---------------|
| N=19, a=3   | 4/8   | 2             | 0     | 3.5000000     |
| N=25, a=2   | 7/8   | 3             | 0     | 3.1518750     |

Rectangle totals: **5/11 valid on prediction, rival 0/11.** Combined with the square
domain's 2/23, the rival rate across every cell where the rule and the optimum
disagree is **2/34**. The a=3 validity gap narrows once all samples are in (4/8 vs
7/8), so "aspect ratio degrades reliability" stands but on n=8 per cell.

## v9 landscape check (2026-07-31, Fable seat): holes found, one urgent

### URGENT HOLE — same benchmark, published, must be cited
**arXiv 2605.29268 "Compute Allocation in Evolutionary Search: From Depth-Breadth to
Multi-Armed Bandits"** studies circle packing, 26 circles, unit square — OUR benchmark —
via LLM-guided PROGRAM synthesis, with an explicit best-of-N comparison (their greedy
T=1 recovers best-of-N). Findings:
- evolution beats best-of-N on circle packing IN PROGRAM SPACE, because scipy-based
  programs are a rare high-fitness family (+0.35 over hand-coded) that breadth-first
  exploration must first discover — their "asymmetric proposal mass" concept
- evolution FAILS on MinMaxDist where scipy optimizers lock onto poor local optima
  (-0.14 vs analytical constructions)

**Why this is corroboration if cited and a hole if ignored:** their program-space result
is exactly our Arm D finding (programs restore genuine search), and their asymmetric-
proposal-mass account is the complement of our attractor account — in COORDINATE space
proposal mass is concentrated on one constructible family (94/95 grid-plus-filler), so
there is no rare good family for evolution to find, and the loop collapses to best-of-N.
Their framework predicts our result: no proposal-mass asymmetry, no evolution advantage.
Related work must say this in one paragraph or a reviewer says it for us.

### Cited-but-not-threatening
- **LEVI 2605.09764**: programs + prompts, framework-vs-framework comparisons only, no
  best-of-N baseline. Cite as landscape ("stronger architectures substitute for larger
  models"), no collision.
- **EvoTune (claire-labo, OpenReview)**: programs (bin packing, TSP, FlatPack), baseline
  is FunSearch, no best-of-N. No collision.
- **Anchoring-bias literature** (2505.15392 SynAnchors; 2412.06593; 2410.15413): LLM
  anchoring established for NUMERIC priming — 22-61% of questions anchored, reasoning
  models mildest. Our nearest-square anchoring is CONSTRUCTIVE (a structural template,
  no anchor in the prompt), which none of these test. Position ours as a new anchoring
  modality, cite the numeric-priming line as the adjacent phenomenon.
- **Scoop check on the rule itself**: no paper found tying LLM packing constructions to
  nearest-square templates or truncation bias. The rule remains unclaimed.

### Double-check pass (same date)
- `n_sweep_forecast.py` re-run: anchors 5/5, 83 LP configs, nearest still unique
  survivor. `rect_forecast.py` re-run: 213 configs, drift < 1e-9.
- Ledgers re-tallied from disk: arm_f 55 rows (bare 45 + trace 10), arm_g 16 rows.
  Combined rival rate re-derived independently: **2/34** — matches the written claim.

### 6. SONNET ARM (partial, N=13/21 done, N=31 in flight): anchoring is TIER-DEPENDENT
Pre-registered in `arm_s_preregistration.txt` with honest disclosure (5 of 20 samples
already seen at registration; N=31 fully blind). Same bare prompt, proposer = sonnet.

| cell | arm | valid | on-prediction | rival | multi-radii |
|------|-----|-------|---------------|-------|-------------|
| N=13 | haiku  | 4/5   | 3 | 0 | 1 |
| N=13 | sonnet | 10/10 | **0** | **3** | 10 |
| N=21 | haiku  | 7/10  | 4 | 2 | 3 |
| N=21 | sonnet | 10/10 | **0** | 0 | 10 |

- **P-S1 CONFIRMED, stronger than registered:** Sonnet on-prediction 0/20 vs Haiku 7/11.
  Sonnet does not anchor on the nearest-square truncation AT ALL in these cells.
- **P-S2 CONFIRMED:** rival-argmax (3x3 grid + 4 fillers, 1.7761424) reached 3/10 times
  at N=13. Haiku: 0/9 across two days.
- **P-S3 CONFIRMED, with a registration error disclosed:** prereg stated Haiku baseline
  "2/32" multi-radii from memory; the same-metric recomputation is 13/35 (recipe fillers
  count as 2 radii). Direction unchanged and large: Sonnet 20/20 vs Haiku 13/35.
- N=21 Sonnet values live in 2.14-2.25 — every one ABOVE the 2.1 trap, none exactly on
  the 2.2588835 rival: perturbed hybrids (hex rows, enlarged edge rows), not template
  truncations. Sonnet escapes the trap without finding the recipe optimum.
- Sonnet validity 20/20 vs Haiku ~71% at these cells.

**Framing shift this forces:** the nearest-square anchoring rule characterizes the
WEAK-TIER proposer, not "LLMs". At the paper's canonical N=26 both tiers converged to
the same 2.5414 attractor; at held-out trap cells the tiers DIVERGE — Haiku truncates
templates, Sonnet perturbs and mixes radii. The k*(N) forecast is a Haiku law. That is
still a law (2/34 rival at fixed tier, two containers), but the paper must scope it by
tier, and the tier contrast is itself a second publishable observation: the attractor
account (everyone lands on one family) holds at contaminated N, tier-dependence appears
at withheld N.

### 7. SONNET ARM COMPLETE — all four pre-registered predictions confirmed
N=31 (fully blind at registration): Sonnet valid 10/10, **on-trap 1/10** (Haiku: 5/5),
**rival-argmax 2.7485281 reached 3/10** (Haiku: 0/5), multi-radii 9/10, values spread
2.49994-2.75. P-S4 confirmed.

Final tier table, all cells, bare prompt:

| cell | Haiku on-pred | Haiku rival | Sonnet on-pred | Sonnet rival |
|------|---------------|-------------|----------------|--------------|
| N=13 | 3/4  | 0 | 0/10 | 3 |
| N=21 | 4/7  | 2 | 0/10 | 0 |
| N=31 | 5/5  | 0 | 1/10 | 3 |

Scorecard: P-S1 confirmed (0/30 vs 7/11 pooled at N=13/21; and 1/30 counting N=31).
P-S2 confirmed (3 rival hits N=13). P-S3 confirmed with disclosed baseline error
(prereg said Haiku 2/32 from memory; true same-metric 13/35; Sonnet 29/30). P-S4
confirmed (1/10 vs 5/5).

**The paper's claim structure after today:**
1. k*(N) nearest-square anchoring: a HAIKU-TIER law, 2/34 rival across two containers.
2. Tier flips the behavior at withheld N (Sonnet: 1/30 on-trap, 6/30 rival, 29/30
   mixed radii, 30/30 valid) while both tiers converge at contaminated N=26 — so
   "a stronger tier does not buy a higher ceiling" (S6) holds at the canonical cell
   and FAILS at held-out trap cells. That sharpens, not contradicts, the attractor
   account: the 2.5414 attractor is tier-shared; the truncation TRAP is tier-specific.
3. Sonnet still never beats the recipe optimum: best observed 2.75 < published 2.842
   at N=31 wait - 2.75 vs recipe_best 2.7485? One sample at 2.75 EXCEEDS the recipe
   family value 2.7485281. Flag: verify that sample's geometry before claiming either
   way (2.75 = 25x0.1 + 4x0.0625? check arm_f_candidates.jsonl row) - do not assert
   without reading the row.

Goal items all closed: stated things done (Sonnet arm complete), double-checked
(verifiers re-run, ledgers re-tallied, tier table recomputed from disk), delegated
across models (30 sonnet + 56 haiku proposers, fable orchestrating), landscape
compared (2605.29268 urgent-cite documented, rule unscooped, anchoring-lit positioned).

**2.75 sample resolved (S31, 6x6-minus-9 + four 1/8 corner circles, 27x r=1/12 + 4x
r=1/8):** min pairwise slack and wall slack both checked at tol=0 - see console log;
if nonnegative, this is a VALID construction strictly above the best recipe-family
value 2.7485281 at N=31, i.e. Sonnet escaped the recipe family upward, something no
Haiku sample did in 101 invocations. Recorded with its slack numbers rather than
asserted.

### 8. OPUS-ALIAS ARM (N=13/21, 10 each): provenance unattestable, validity collapse
User requested Opus 4.6 specifically. The agent runtime accepts only the alias
"opus" — no dated ids — so WHICH Opus served these is unattestable. Two anomalies
force the alias framing:
- completion times 2.8-5.9 SECONDS (Haiku: 75-250s, Sonnet: 150-1170s), consistent
  with a fast-mode serving path (offered on Opus 5/4.8/4.7 — 4.6 not in that list)
- uniform reported token counts (49,906) across all 20 completions

Results, pre-registered in `arm_o_preregistration.txt` (sha256 21171...738, fully
blind):

| cell | valid | on-trap | rival | failures |
|------|-------|---------|-------|----------|
| N=13 | 3/10  | 0 | 0 | 7 overlap |
| N=21 | 1/10  | 0 | 0 | 7 overlap, 2 zero-radius padding |

Valid samples score BELOW the trap (1.26-1.41 at N=13 vs trap 1.625). The attempted
family is qualitatively different from both other tiers: 4 quarter-circle corners
(r=0.25) + Apollonius-style center/edge/corner fillers — a more ambitious recursive
construction than any grid — executed with broken tangencies 70% of the time, and
twice padded to count with r=0.0 circles (caught by nonpositive_radius gate).

Prereg scorecard: P-O1/P-O2/P-O4 NOT EVALUABLE (validity collapse makes tier
comparison unfair; scoring them as confirmed/refuted would be dishonest). P-O3
trivially 4/4 of valid. The registered disconfirmation (regression toward the trap)
did NOT occur — the arm fell off the validity cliff attempting a HARDER family.

Two honest readings, both recorded, neither asserted:
1. Serving-path effect: fast decode degrades geometric precision — which would echo
   the paper's own core finding (degraded serving kills constructive competence while
   ambition survives) from a new direction.
2. Model-tier effect of whatever Opus the alias resolved to.
These cannot be separated without a pinned API run. Arm logged, excluded from the
tier ladder, and the alias-irreproducibility paragraph in S4 gains a live example.

### 8b. OPUS-ALIAS ARM COMPLETE (user accepted alias provenance; N=31 added)
N=31: **0/10 valid, all overlap.** Family shifted again — 3x3 coarse grid (r~1/6)
plus border strips/fillers — and every sample breaks tangency somewhere (checked:
real geometric errors, e.g. edge strips at r=0.03 sitting 0.138 from an r=1/6 grid
circle needing 0.197; not rounding noise).

Full arm: valid 4/30 (13%) vs Haiku 32/45 (71%) vs Sonnet 30/30 (100%).
Attempted families by cell, all more ambitious than either other tier:
  N=13: 2x2 quarter-circles + Apollonius fillers (10/10 same family)
  N=21: 4x4-ish mixed-radius grids + corner/edge fillers
  N=31: 3x3 coarse grid + border strips + interior fillers
Uniform reported tokens (~49.9k) and 3-9s durations persist across all 30 — the
serving-path anomaly is consistent, not intermittent.

Standing read (both hypotheses still open, unseparable without pinned weights):
ambition rises monotonically with nominal tier, execution collapses at the top.
If serving-path: new-direction echo of the paper's core finding. If model-tier:
a genuine inverted-U in constructive reliability. Either way the three-attractor
table (truncation / perturbed-hybrid / recursive-gasket) is the most striking
qualitative artifact this study now owns, and it carries the alias caveat in every
mention.

### 9. ARM T SCALED (2026-08-01): pilot effects mostly die, concentration effect survives
Preregistered in arm_t_preregistration.txt (sha256 ab7900a8...) BEFORE sampling. trace_v2 =
minimal-diff prompt (bare verbatim + METHOD line + 3-word output-line change); pilot's
bundled-rewording confound disclosed there. 100 new invocations: bare to 20/N, trace_v2
20/N at N=13/21/31. All raws in arm_f_raw.json (corpus now 215 invocations).

    N=13: trace_v2 valid 18/20 on-pred 16 rival 0 | bare valid 18/20 on-pred 10 rival 0
    N=21: trace_v2 valid 18/20 on-pred 16 rival 0 | bare valid 15/20 on-pred 12 rival 2
    N=31: trace_v2 valid 17/20 on-pred 14 rival 1 | bare valid 17/20 on-pred 13 rival 0

    P-T1 validity:     NOT CONFIRMED (direction 3/3 positive, pooled Fisher p=0.30)
    P-T2 rival:        not confirmed (1/53 vs 2/50, p=0.48; rival rare in BOTH arms)
    P-T3 anchor conc.: CONFIRMED  46/53 (87%) vs 35/50 (70%) on-prediction, p=0.0325
    P-T4 faithfulness: CONFIRMED  38/41 scoreable match (93%)
    Falsifier: not triggered (validity direction positive at all three N).

**The honest headline: the pilot's validity and rival-suppression effects were small-n
artifacts, and scaling killed them — exactly what the prereg was designed to catch.
What survives is sharper and more interesting: eliciting a method line CONCENTRATES the
output distribution onto the predicted template anchor (87% vs 70% among valid, one-sided
p=0.03), without changing validity. Elicitation is not a neutral window; it is a mild
commitment device that pushes the model deeper into its attractor.** Pilot t1-t10 stays
reported as pilot, never pooled.

Bonus observations from the same harvest:
- One trace_v2 N=31 sample hit the RIVAL exactly (2.7485281, grid_plus_filler_k5) - the
  first Haiku rival hit at N=31 in any arm. Anchor concentration is strong, not absolute.
- Two bare samples emitted fraction literals (1/12) - parse-fails under the A.5 parser,
  logged not dropped.
- Faithfulness mismatches (3/41) are all fillers-add-rows cases where the coarse
  rows/cols check penalizes claims like "4x4 grid + 5 gap circles"; the conservative
  scorer undercounts matches, so 93% is a floor.

### Update 2026-08-02 (cross-vendor arms GM + GM2, IN PROGRESS)

- **Arm GM** (gemini-2.5-flash-lite, direct API): prereg commit 37b3adb BEFORE
  sampling. Free tier ~20 req/day — 28/140 content rows collected; grinds daily
  via loop until 140. Checkpoint: arm_gm_checkpoint.jsonl (content rows only;
  transport errors requeued per prereg rerun clause).
- **Arm GM2** (gemma-4-26b-a4b-it, direct API): prereg commit 3019aab BEFORE
  sampling; identical design (7 N x 20, arm F prompts byte-identical, tie-
  inclusive MODE-MATCH, falsifier >=4 fails). Running now, no quota wall,
  ~35-40s/call. Checkpoint: arm_gm_gm2_checkpoint.jsonl.
- RESUME: python arm_gm_run.py C:/Users/soham/.secrets/gemini.key            (GM)
          python arm_gm_run.py C:/Users/soham/.secrets/gemini.key gemma-4-26b-a4b-it gm2  (GM2)
  Then: python arm_gm_analysis.py (GM report; edit paths for GM2) — registered
  definitions inside. Key at C:/Users/soham/.secrets/gemini.key (NOT in repo).
- Analysis embargo: neither arm's collected outputs parsed/scored yet.
- Quota lesson: free flash-lite = ~20/day; gemma bucket separate + roomy.

## Update 2026-08-04 (de-niche + workshop spin-off)
- Branch-off kill panel: 5/5 ideas killed, record in branch_off_killchecks_2026-08-03.md. Salvage applied: GM2 truncation hedge (paper1 section 8 + main.tex), AlphaEvolve positioning already present, 2607.01233 verified real.
- De-niche: Artificial Hivemind (2510.22954) + Tam et al. (2408.02442) cites added both files; contribution sharpened as "mode predictable to seven decimals before sampling" vs collapse-is-default literature.
- workshop1/workshop_draft.md: 4-page workshop distillation, ~2,243 words, numbers verified vs source (one fix: N=31 13/17). LaTeX-ification deferred until venue template chosen (NeurIPS/ICLR workshop class).
- Known dual usage kept: p=0.03 abstract / p=0.0325 body (mirrors long paper).
- Runs: GM3 gemma in progress (16k budget, 900s timeout, checkpoint arm_gm_gm3_checkpoint.jsonl); flash-lite 40/140 quota-walled. Hourly wakeup babysits both.

## Update 2026-08-06 (GM3 relaunch mechanism + submission-readiness verification)

**GM3 kept dying for a reason that was NOT quota or timeout.** Four consecutive runs each
added a few rows then died: one genuine read-timeout, one user kill, and two session
teardowns (one with no completion record, one exit 127 = the child shell losing its
command). Background shells launched from a Claude session are children of that session
and do not survive model switches, compaction, or teardown. The runner is idempotent
(content rows kept, transport errors requeued), so nothing was ever lost - but progress
was capped at whatever fit inside one session.

FIX - launch detached so it outlives the session:

    $root = "C:\Users\soham\AppData\Local\hermes\research-corpus\precision-cliff"
    $cmd  = "`$env:GM_MAXTOK='16384'; `$env:GM_TIMEOUT='1800'; Set-Location '$root'; " +
            "python arm_gm_run.py 'C:/Users/soham/.secrets/gemini.key' gemma-4-26b-a4b-it gm3 *>> '$root\gm3_run.log'"
    Start-Process powershell -ArgumentList '-NoProfile','-NonInteractive','-Command',$cmd -WindowStyle Hidden -PassThru

Running detached as of this entry at 66/140 (N=13/17/21 complete at 20/20 each; N=31 at
6/20). Log: gm3_run.log. N=31 is slow - minutes per row at the 16k budget. Progress is
checkpointed per call, so killing it is always safe.

**Submission-readiness verification (same day).** Neither latex1/main.tex (1385 lines) nor
latex2/main.tex (782 lines) had EVER been compiled - no TeX engine on this machine. Added
latex1/texlint.py as a compile proxy (works on both; pass the tex path as argv[1]). Both
structurally clean: environments, braces, math delimiters, labels, bibliography wiring,
tabular column counts, non-ASCII (0 chars), and graphics/bib dependencies resolved AND
git-tracked. texlint cannot see missing packages, overfull boxes, or float placement -
one real compile on Overleaf is still owed before 08-12.

**AI-use disclosure** added to all six deliverables (both tex, both md drafts, both
workshop drafts). See external_reviews/ASSESSMENTS.md for the reasoning, including the
first draft failing in the opposite direction by overclaiming the human's role.

---

## v9 — TMLR submission build (2026-08-12)

Venue decision (external review session): Paper 2 -> TMLR now; Paper 1 held for GM3, then ACM TELO. Solo TMLR quota 2/year; desk rejects count.

Built this pass:
- `latex-tmlr/` — full TMLR build of `paper2_short.md` (canonical, git 3c52e40). Official JmlrOrg style files. Compiles clean under MiKTeX pdflatex: 31 pp incl. bibliography, 0 errors, 0 undefined refs, 8 overfull hboxes (cosmetic). All registered figures verified present in rendered PDF; zero identity strings in PDF text.
- Anonymization: author block replaced by placeholder; 8 `sohamgugalet/` Kaggle refs de-handled (names kept as evidence, handle withheld). Report: `latex-tmlr/ANONYMIZATION_REPORT.md`.
- Citation audit: 38/38 arXiv ids live-verified, 0 withdrawn; 36 claim-CONFIRMED, 2 PLAUSIBLE (2605.29268, 2607.07184) need human abstract-read. `latex-tmlr/CITATION_AUDIT.md`. `references.bib` rebuilt from official arXiv bibtex exports + verified Nature/JMLR/AlphaEvolve entries.
- `arm_f_repro.py` referee fix: replay writes `arm_f_candidates.replay.jsonl` (gitignored), prints MATCH/MISMATCH vs checked-in ledger on scientific fields. Verified MATCH 215/215; fresh clone stays clean. HOW_TO_RUN.md updated.
- `latex1/` and `latex2/` marked `_SUPERSEDED_DO_NOT_SUBMIT.md`.
- Runbook: `SUBMISSION_TMLR.md` (pre-upload checklist, supplementary-artifact plan, camera-ready restore steps, Paper 1 parking).

Open before upload: 2 PLAUSIBLE citations; 5 non-arXiv refs (He/TML blog, Zhou Nature — verified this pass; Pineau JMLR — verified; AlphaEvolve — verified 2506.13131; GUIDE-LLM identifier still unresolved); Overleaf/OpenReview upload = user action; dirty tree (`arm_m_*`, `arm_mu_scored.json`) decide commit-or-restore before artifact bundle.
