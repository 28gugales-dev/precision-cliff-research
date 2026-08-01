# Kill-check results (2026-08-01, workflow wf_9a46b89d-1b0: 6 hunters + 4 verifiers, ~90 queries)

## Headline: ZERO KILLS. All six claims survive. K4 narrowed as expected.

| claim | verdict | damage |
|---|---|---|
| K1 template anchoring in constructive geometry | SURVIVES clean | none — 10 neighbors all corroborate other modalities; no template-family identification anywhere |
| K2 closed-form exact output prediction | SURVIVES clean | none — zero collision; nearest priors predict categories/accuracy via probes, never exact multi-decimal values from problem parameters |
| K3 behavioral characterization on circle packing | SURVIVES | none — benchmark used ONLY for scores by evolve systems; nobody characterized WHAT constructions emerge |
| K4 hash-locked prereg of exact outputs | SURVIVES NARROWED | claim only the combination: hash-locked + exact-output + held-out container. Prereg-of-LLM-experiments alone predates us |
| K5 tier inversion ambition/validity | SURVIVES | cite-and-differentiate Zhou et al. Nature 2024 (QA domain analog) |
| K6 elicitation concentrates onto anchor | SURVIVES clean | none — 15+ queries across observer-effect/self-explanation/reactivity lits; effect unreported |

## Verified threats (4 checked, 0 kills)
- Zhou et al., "Larger and more instructable LLMs become less reliable" (Nature 2024) — corroborate-cite. QA-domain attempt-more/err-more; our constructive-regime inversion is the new instantiation.
- HindsightBench (2607.18867, concurrent 2026-07-21) — scoop-partial on K4. SHA-256-frozen prereg of DIRECTIONAL aggregate hypotheses; we hash-lock exact closed-form point predictions. Cite as concurrent.
- Predicting LLM Safety Before Release (2607.07184) — scoop-partial on K4. OSF-prereg of prevalence RATES; not exact outputs, no hash, no held-out container.
- Thomas, Gligoric & Shah "Preregistering for the Next LLM" (2606.27687) — corroborate-cite. Preregisters recipe not predictions.

## New must-cite set by section
§4 tier ladder: Zhou et al. Nature 2024; o3/o4-mini system card (PersonQA more-claims/more-hallucinations); Illusion of Thinking (2506.06941); GeoBuildBench (2605.13167).
§5 elicitation: Hawthorne Effect in Reasoning Models (2505.14617, test-awareness steering); The Price of Format (2505.18949, format-induced diversity collapse — closest cousin, differentiate: format constraint vs method-descriptor request); Verbalized Sampling (2510.01171, mode collapse); Latent Memory Anchor (2506.17630).
§6 faithfulness + K6 disambiguation (MANDATORY paragraph): Reasoning Theater (2603.05488, VERIFIED real — answer decodable from activations before trace completes); Project Ariadne (2601.02314, VERIFIED real — hard interventions ON trace content leave answers unchanged; metric = "Ariadne Score"/"Causal Sensitivity", NOT "Causal Faithfulness Score"). Our result: request FOR trace changes output distribution. Different intervention point; complementary.
§3/§9 prereg positioning: HindsightBench (2607.18867), 2607.07184, 2606.27687, Preregistration for AI-agent experiments (2606.11217), physics-literacy prereg (2607.00276). Framing: prereg = adopted standard, our addition = exact-output closed-form point predictions.
§7 saturation table (all VERIFIED real): AlphaEvolve 2.635 (n=26), ShinkaEvolve 2.635983283, HELIX 2.63598308 (2603.07642), GigaEvo 2.636 (2511.17592), AdaEvolve 2.636 (2602.20133), SeaEvo (2604.24372), ThetaEvolve (2511.23473). Simple-baselines critique: Gideoni/Risi/Gal (2602.16805). Classical-solvers critique: Berthold et al. (2605.04850) — NOT Gideoni, Gemini spliced two papers.
§7 diversity/search skepticism: What Makes an LLM a Good Optimizer (2604.19440); Dictionaries Not Darwin (2607.04108); EvoDiverse (2606.10587); bin-packing critiques (2510.27353, 2501.11411); Evolutionary-search importance (2407.10873); MathConstruct (2502.10197); BehaveSim (2603.02787); Strategy Diversity (2605.09292).

## Gemini triage final
- Real + as-described: Reasoning Theater, Ariadne (one metric name wrong), HELIX, GigaEvo, AdaEvolve, ShinkaEvolve, SeaEvo, MLS-Bench (2605.08678, gloss inflated), all n=26 scores (OpenEvolve 2.634 unconfirmed as OpenEvolve's own).
- Fabricated/spliced: Opti-Agent-Bench (no results — "template anchoring" term UNCLAIMED); PoPE-as-prereg; GlassballAI-as-audit; PBRC role; inference-scheduling no-closed-form quote; Gideoni framing (real person, wrong paper).

## Consequence for abstract
No claim retracted. Rewrite emphasis per positioning rules: contributions = K2 (anchor), K5, K6; armor = K1 lineage, K3 saturation, K4 prereg-with-a-twist (exact-output hash-locking = the twist worth one sentence, not a contribution bullet).
