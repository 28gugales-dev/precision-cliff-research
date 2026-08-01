# Paper 1 skeleton — Template Anchoring

Working title: **"The Nearest Square: LLMs Anchor on Templates in Constructive Geometry,
and a Closed Form Predicts Where"**

Audience: LLM evaluation / reasoning community; GECCO LLM-EC track viable alternate.
Target length: 9-10 pages + appendix. Status of every claim: evidence file in this directory.

---

## 1. Introduction
- Hook: ask an LLM to pack 21 circles in a square; it does not search — it recalls the
  nearest grid template and truncates it, even when a provably better construction is
  one parameter away. Behavior so regular a closed form predicts the exact value emitted.
- Contributions (each one sentence):
  C1 selection rule k* = round(√N) + closed form V(k,m); trap zones where rule costs value.
  C2 preregistered out-of-sample confirmation, two containers (square + rectangle).
  C3 tier ladder: three model tiers, three attractor families, ambition↑ execution↓.
  C4 trace elicitation is an intervention, not observation (paired arms).
  C5 faithfulness auditable against emitted coordinates; traces pass.
- Non-claim guard: no claim about mechanism inside weights; behavioral regularity only.

## 2. Task and recipe family
- Benchmark: max sum-of-radii, N circles, unit square, zero-shot, no code (A.5 prompt verbatim).
- Recipe family: k×k grid r=1/(2k); m corner fillers r=(√2−1)/(2k), m≤(k−1)²;
  truncated grid T(k,N)=N/(2k). Evidence: n_sweep_forecast.py, 83 LP-verified configs <1e-9.
- Selection rule: k*=round(√N); k*²≤N extend (converge), k*²>N truncate (trap).
  Trap zones: [13,15],[21,24],[31,35],[43,48],[57,60].
- Figure 1: predicted-vs-optimal value over N=10..50, trap zones shaded.

## 3. Preregistered forecast, out of sample
- Registration protocol: predictions + SHA-256 prompt hashes BEFORE sampling
  (arm_f_repro.py header P1-P5; arm_s/arm_o/arm_t prereg files).
- Square results (Haiku): 18/23 valid land on-prediction, rival 2/34 overall.
  P4 highlight: N=37 prime predicted CLEAN, contradicting paper-0's own guess — confirmed.
- Rectangle transfer: rule restated q*=round(√(N/a)), p*=round(√(N·a)), never fitted to
  rectangle data; 5/9 valid on-prediction, 0/9 rival (arm_g_rect.py, STATE.md §5).
- Negative result kept: rectangle filler closed form does NOT exist (LP counterexample
  1.125 vs 1.1545085); LP as value oracle. Shows the pipeline aborts on drift.
- Table 1: cell × predicted × rival × valid × on-pred × rival-hit, both containers.

## 4. Tier ladder — three attractor families
- Haiku: truncated uniform grids, 32/45 valid (71%).
- Sonnet: perturbed/mixed-radius grid hybrids, 30/30 valid (100%), rival 6/30, one sample
  2.75 > recipe-family best 2.7485281 at N=31 (27×1/12 + 4×1/8, slack 0.00e+00 at tol=0).
- opus_alias: recursive gaskets / quarter-circle constructions, 4/30 valid (13%),
  N=31 0/10 all-overlap. ALWAYS carry alias caveat (provenance, not version claim).
- Table 2: three-attractor table (family attempted / validity / outcome per tier).
- Reading: constructive ambition rises with nominal tier, execution collapses; recipe is
  attractor, not ceiling.

## 5. Elicitation as intervention (arm T — scaled, results in)
- Pilot (N=21, 10v10) reported as pilot only; its validity/rival effects DIED at scale —
  framed as prereg working as designed (self-correction is a selling point, lead with it).
- Scaled (20/arm × N=13/21/31, prereg sha256 ab7900a8...):
  P-T1 validity NOT confirmed (direction 3/3, p=0.30). P-T2 rival not confirmed.
  P-T3 anchor concentration CONFIRMED: 46/53 (87%) vs 35/50 (70%) on-prediction, p=0.033.
  P-T4 faithfulness CONFIRMED: 38/41 (93%), and the 3 mismatches are conservative-scorer
  artifacts (fillers add coordinate rows), so 93% is a floor.
- Claim to write: method-line elicitation is a mild commitment device — it concentrates
  output onto the template anchor without changing validity. Not a neutral window.
- Implication: any process-descriptor study collecting traces by request measures a
  perturbed distribution. Names the confound for QD-descriptor work (cite QDAIF line).
- Table 3 = per-N grid above; STATE.md §9.

## 6. Faithfulness with ground truth
- Claim-vs-coordinates audit: METHOD line dims vs observed layout signature; 8/8 scoreable
  match in pilot (incl. honest value-losing hexagonal claim, 1.75).
- Contrast: 2503.08679 / 2606.13603 / 2605.29087 estimate faithfulness without ground
  truth; here coordinates ARE ground truth. Scaled-arm numbers pending (P-T4).

## 7. Related work
- Same benchmark, program space: 2605.29268 asymmetric proposal mass — corroborating,
  different modality (must-cite).
- FunSearch / AlphaEvolve line: LLM-as-proposer in evolutionary loops — our result
  characterizes the proposal distribution those loops sample from.
- Anchoring-bias lit (2505.15392, 2412.06593, 2410.15413): numeric priming; ours is
  constructive anchoring — new modality.
- CoT faithfulness line: no ground truth vs our auditable setting.
- GECCO/QD framing: [SLOT — lit-sweep agent output].

## 8. Limitations
- Single vendor (Claude tiers) — cross-vendor arm blocked on credit; disclosed.
- Zero-shot only; evolutionary loop not rerun (paper-0 showed loop ≈ best-of-N).
- Agent-runtime sampling params unpinned (full treatment → paper 2, cross-cite).
- opus_alias serving-path vs model-tier confound unseparable without pinned weights.

## 9. Reproducibility statement
- All prompts hashed pre-run, all raw outputs verbatim in repo, deterministic local
  scoring, LP verification gates. Prereg files: arm_f (header), arm_s, arm_o, arm_t.

---

## Claim → evidence map
| claim | file |
|---|---|
| closed form + rule + traps | n_sweep_forecast.py / .json |
| LP verification 83 configs | n_sweep_forecast.verify_against_lp |
| square out-of-sample | arm_f_repro.py, arm_f_candidates.jsonl |
| rectangle forecast + no-closed-form negative | rect_forecast.py / .json |
| rectangle probe | arm_g_rect.py, arm_g_candidates.jsonl |
| tier ladder | arm_f (bare/sonnet/opus rows), STATE.md §7-8b |
| trace pilot + scaled | STATE.md §3-4, arm_t_preregistration.txt, [arm T results pending] |
| faithfulness | arm_f_repro.trace_faithfulness, STATE.md §4 |

## Open slots before submission
1. Arm T scaled results (running 2026-08-01).
2. Lit-sweep integration (§7 GECCO slot + novelty-threat check).
3. Figures: trap-zone curve, three-attractor examples (one packing rendered per tier).
4. Venue pick pending lit agent's deadline scan.
