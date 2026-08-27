# Researcher outreach — round 2 list + round 1 status (2026-08-21)

## Round 1 status (12 emails sent 2026-08-14)

Zero replies as of 2026-08-21, but also zero bounces — all delivered. Recipients:
Clune, Mouret, Pineau, Kang, Frantar, Rieck (lab office), Cully, Lingjiao Chen,
Evan Miller, Song Han, Kelly Marchisio, Lovish Madaan.

**Follow-up drafts for all 12 are sitting in Gmail Drafts**, threaded onto the
original emails, personalized per recipient. Recommended send date: **Aug 28–Sep 1**
(two weeks after the originals). One week of silence on cold academic email in
mid-August is normal; do not read it as a verdict.

## Round 2 — 20 new contacts (no overlap with round 1)

Email confidence: **[V]** verified/public · **[M]** medium (standard pattern or found
in commits/papers) · **[L]** low (no public email — use the noted channel).

### Quantization / compression behavior
1. **Tim Dettmers** — CMU + Ai2. QLoRA/bitsandbytes; *the* person on how low-bit
   models behave. `dettmers@cmu.edu` [M]
2. **Dan Alistarh** — ISTA. GPTQ/SparseGPT senior author. `dan.alistarh@ist.ac.at` [V]
3. **Amir Gholami** — UC Berkeley. Quantization surveys. `amirgh@berkeley.edu` [V]
4. **Sara Hooker** — Cohere Labs. "What Do Compressed Models Forget?" — the closest
   antecedent to "pass/fail metrics miss compression damage". `sarahooker@cohere.com` [M]
5. **Georgi Gerganov** — llama.cpp author — the exact runtime and K-quant formats the
   ladder uses. GitHub `@ggerganov`; `ggerganov@gmail.com` appears in commits [M]

### LLM-driven evolution / search
6. **Bernardino Romera-Paredes** — Google DeepMind, FunSearch corresponding author.
   No public email; LinkedIn or via a co-author [L]
7. **Matej Balog** — Google DeepMind, FunSearch/AlphaEvolve. [L]
8. **Robert Tjarko Lange** — Sakana AI, ShinkaEvolve + AI Scientist. Paper 1 cites
   ShinkaEvolve's N=26 record directly. `robert@sakana.ai` [V — from his site]
9. **Joel Lehman** — "Evolution through Large Models" (LLM mutation operators).
   Ex-OpenAI (old email stale); X `@joelbot3000` or personal site [L]
10. **Xinyun Chen** — Google DeepMind, OPRO ("LLMs as Optimizers"). [L]
11. **Can Gurkan** — Northwestern. "Mutation Without Variation: Convergence Dynamics
    in LLM-Driven Program Evolution" (arXiv 2606.05408) — LLM mutation converging to
    attractor templates; the nearest neighbor to Paper 2's echo result published this
    year. Likely `cangurkan@u.northwestern.edu`; GitHub `can-gurkan` [M]
    (co-authors: Forrest Stonedahl, Augustana; Uri Wilensky, Northwestern)

### Serving path / API auditing / behavior drift
12. **James Zou** — Stanford. "How is ChatGPT's behavior changing over time?"
    `jamesz@stanford.edu` [V]
13. **Matei Zaharia** — UC Berkeley. Same paper + serving infrastructure.
    `matei@berkeley.edu` [V]
14. **Horace He** — Thinking Machines. "Defeating Nondeterminism in LLM Inference" —
    serving-path variability is his exact beat. No public email; X `@cHHillee` [L]
15. **Dawn Song** — UC Berkeley. Group behind the model-substitution auditing paper
    Paper 2 cites (cai2025). `dawnsong@cs.berkeley.edu` [V]
16. **Florian Tramèr** — ETH Zürich. Auditing deployed models, ML security.
    `florian.tramer@inf.ethz.ch` [V]
17. **Nicholas Carlini** — Anthropic. Model verification/extraction; would engage
    with the attestation-gap argument. `nicholas@carlini.com` [V — personal site]

### Evaluation statistics / reproducibility
18. **Jesse Dodge** — Ai2. Reproducibility checklists and reporting standards.
    `jessed@allenai.org` [V]
19. **Percy Liang** — Stanford, HELM. `pliang@cs.stanford.edu` [V]
20. **Sanmi Koyejo** — Stanford, statistics of ML evals. `sanmi@cs.stanford.edu` [V]

## Notes for round 2 sends

- Reuse the round-1 email skeleton (junior + one-sentence hook tailored to their
  work + one concrete question + abstract link). The strongest new hooks:
  Gurkan/Lange/Romera-Paredes (their systems assume proposal variation),
  Hooker (compression damage invisible to metrics), He/Zou/Zaharia/Song
  (serving path is part of the model), Carlini/Tramèr (attestation).
- Stagger sends (4–5/day) rather than one blast; avoids spam filtering and lets
  wording improve between batches.
- [L] entries: don't guess addresses — use LinkedIn/X or route through a co-author
  with a public address.
