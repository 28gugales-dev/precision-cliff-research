# Precision Tolerance of LLM-Guided Evolutionary Search
## Paper Outline for ISEF 2027 & GECCO 2027

---

## Target Venues

### ISEF 2027 (Regeneron International Science and Engineering Fair)
- **Format:** Science fair with poster presentation + research paper + abstract (max 250 words)
- **Category:** "Robotics and Intelligent Machines" or "Systems Software" — this project sits at the intersection of ML, evolutionary computation, and systems
- **Eligibility:** Grades 9-12; project must show <= 12 months continuous research, ending no more than 18 months before ISEF 2027
- **Rules:** 2027 International Rules for Pre-college Science Research (PDF + HTML available at societyforscience.org/isef/international-rules/)
- **AI Usage:** Society for Science has published specific AI usage guidelines — the paper must clearly distinguish between AI as a research tool (the LLM proposer under study) vs AI as a writing aid; both must be properly cited
- **Key docs needed:** Abstract (250 word max), Research Paper/Project Summary, Forms (1, 1A, 1B), Research Plan, Safety forms, Abstract with 22 categories categorization
- **Submission:** Through affiliated fair network (state/regional fair first, then ISEF); 2027 dates TBD but typically May
- **Categories PDF:** 2026 Abstract with 22 categories available; 2027 version coming soon
- **URL:** https://www.societyforscience.org/isef/

### GECCO 2027 (Genetic and Evolutionary Computation Conference)
- **Format:** ACM conference paper, typically 8-page limit (full papers), double-blind review
- **Template:** ACM SIG Proceedings template (acmart LaTeX class)
- **Track:** Most relevant: "Evolutionary Machine Learning" or "Neuroevolution" or "Real World Applications"
- **Availability:** GECCO 2027 website not yet live (2026 page is up at gecco-2026.sigevo.org); GECCO 2026 was July 13-17, 2026 in San Jose, Costa Rica. GECCO 2027 likely similar dates in mid-2027.
- **Review process:** Double-blind, typically 3+ reviewers; acceptance rate ~30-35% for full papers
- **Deadline estimate:** January/February 2027 (based on prior years)
- **Key criteria:** Novelty, significance, technical soundness, reproducibility, clarity
- **Note:** GECCO 2027 call for papers not yet published; watch https://gecco-2027.sigevo.org/ for updates

---

## Title Options

| Option | Rationale |
|--------|-----------|
| **Precision Cliff: How Weight Quantization Affects LLM-Guided Evolutionary Search** | Clear, direct. "Precision Cliff" is the brand. Prioritized. |
| Does the Loop Save the Model? Precision Tolerance of LLM-Guided Evolutionary Search | Attention-grabbing, frames the two-communities gap |
| Where the Search Loop Meets the Quantization Cliff: Precision Ablation in LLM-Guided Evolution | More literary, good for GECCO |
| Beyond Static Benchmarks: The Precision Cliff of LLM Mutation Operators in Evolutionary Search | Emphasizes the gap in the literature |
| Selection Rescues Quantization: Precision Ablation of LLM Proposers inside MAP-Elites | Niche, more technical, good for GECCO |

**Recommended primary title:** *Precision Cliff: How Weight Quantization Affects LLM-Guided Evolutionary Search*
**Recommended subtitle for GECCO:** *A Precision Ablation Study of LLM Proposers inside MAP-Elites*

---

## Abstract (Draft)

> Large language models (LLMs) are increasingly used as mutation operators inside evolutionary search loops, where they propose candidate solutions that are evaluated, selected, and inherited. Meanwhile, the quantization literature measures how weight precision (FP16 to 2-bit) degrades LLM output on static, single-shot benchmarks — but no prior work has placed that precision gradient inside a selection loop. We bridge this gap by sweeping the weight precision of a Qwen3-Coder-30B proposer (FP16, INT8, INT4, INT3, INT2) through a MAP-Elites evolutionary search on the circle packing benchmark (n=26). We measure best fitness, QD score, archive coverage, and mutation viability rate across 5 precision levels x 5 seeds x 2 budget regimes (fixed generations vs fixed compute). We find that [PLACEHOLDER: the precision cliff shifts — it moves to a lower bit-width inside the loop because selection filters malformed proposals for free, OR it moves to a higher bit-width because errors compound through inheritance]. This result has implications for deploying LLM-guided search on resource-constrained hardware, and for the design of quantized proposer models.

---

## Section Structure

### 1. Introduction (~1 page / 1.5 pages for ISEF)

**Hook:** Static benchmarks tell us one story about quantization. The search loop may tell a different one.

**The two-communities gap:**
- Quantization community: sweeps precision on static code/reasoning benchmarks, measures one-shot pass@k. Has never put the model inside a selection loop.
- Evolutionary computation community: varies model identity, size, ensemble composition, routing. Has never varied weight precision of a fixed model.
- Nobody has looked at the intersection.

**Central question:** Does the MAP-Elites loop rescue or compound quantization damage?
- Selection filters malformed offspring for free (rescue hypothesis — cliff shifts lower)
- Errors compound through inheritance and lineage (compound hypothesis — cliff shifts higher or stays same)
- Both are publishable outcomes.

**Key claims under test:**
1. The effective precision cliff inside an evolutionary loop sits at a different bit-width than the static cliff.
2. At matched compute budget, a lower-precision proposer may produce a higher QD score (more mutations per dollar, more archive niches filled).

**Contribution statement:**
- First systematic precision ablation of an LLM proposer inside an evolutionary search loop
- First measurement of mutation viability rate as a mediator of precision degradation
- Two-budget-regime comparison (fixed generations vs fixed compute)
- Empirical evidence for the relationship between quantized model deployment and search performance

**Roadmap:** Brief overview of paper structure.

### 2. Related Work (~1 page)

**2.1 LLM-Guided Evolutionary Search**
- ELM (2206.08896): established the LLM-as-mutation-operator MAP-Elites paradigm
- In-context QD (2404.15794): ablated prompt design and parameter count, not precision
- AlphaEvolve (2506.13131), OpenEvolve, ShinkaEvolve: established the circle packing n=26 benchmark

**2.2 Precision as a Fixed Deployment Detail**
- CALM (2505.12285): INT4 Qwen2.5-7B proposer, single 24GB GPU. INT4 is a fixed memory constraint, never ablated. Only precision sentence acknowledges the model card says quantization reduces accuracy.
- Squeeze Evolve (2604.07725): Near-SOTA circle packing (2.635896) with GPT-OSS models (natively ~4.25-bit MXFP4). Zero precision content. The MXFP4 nature is external knowledge from the OpenAI model card, not from the paper.
- ThetaEvolve (2511.23473): Varies proposer size and family (1.5B vs 8B, ProRL vs DeepSeek-R1). Not precision.
- X-evolve (2508.07932), LEVI (2605.09764): Ablate model capacity, routing, family. Not precision.
- DEI (2605.27130): Varies model identity and ensemble composition. Not precision.

**2.3 Near-Collisions (Must Cite and Differentiate)**
- arXiv 2605.09781: "Parameter-Efficient Neuroevolution for Diverse LLM Generation" — runs a 4-bit proposer inside a QD loop, but precision is a fixed deployment detail, no sweep. **Highest re-check priority.**
- arXiv 2606.27205: "Smaller Models, Unexpected Costs" — same IV (precision swept to 2-bit), on candidate generation. Single-shot pass@10, no selection loop.
- arXiv 2602.03120: "Quantized Evolution Strategies" — keyword collision. Evolution optimizes the quantized weights; the LLM is the optimizee, not the proposer. Differentiate explicitly.
- arXiv 2602.13595: "The Quantization Trap" — iteration-amplified quantization damage in reasoning chains. Nearest conceptual relative. Chains are not selection loops, but the error-compounding framing is directly relevant.

**2.4 Static Quantization Benchmarks**
- Llama-3-8B KLD: q4_K_M 0.028, ~2.7 bpw 0.326 (cliff onset), ~2.06 bpw 0.812 (PPL 6.38 -> 8.60 -> 14.09)
- Static cliff for modern dense models sits between 2 and 3 bits
- This anchors our Figure 4 overlay

**2.5 The Gap (Synthesis)**
- Systems closest to our setting never touch our variable
- Nobody has placed proposer weight precision inside a selection loop and measured what the loop does to the cliff

### 3. Background (~0.5 page)

**3.1 Static Quantization Cliff**
- Brief explanation of weight quantization (FP16 -> INT8 -> INT4 -> INT3 -> INT2)
- PPL/KLD per level from the literature
- Single-shot benchmark behavior

**3.2 MAP-Elites and LLM-Guided Search**
- MAP-Elites algorithm: archive of (behavior descriptor, fitness) pairs, mutation selects from a cell, evaluates, inserts if better
- LLM as mutation operator: prompt + context -> diff/candidate -> evaluate -> archive
- Circle packing benchmark (n=26): maximize sum of radii, standard field benchmark

### 4. Method (~1.5 pages)

**4.1 Experimental Design**
- **Independent variable:** Weight precision of the proposer model (5 levels)
- **Dependent variables:** Best fitness, QD score, archive coverage, mutation viability rate
- **Mediator:** Mutation viability rate (link between precision and search outcome)

**4.2 Fixed Configuration**
- Model: Qwen3-Coder-30B (MoE, A3B architecture) — or Qwen2.5-Coder-7B fallback if hardware forces it
- Quantization method: llama.cpp K-quants (single family, never mixed)
- Benchmark: Circle packing n=26, maximize sum of radii
- Archive: MAP-Elites with fine-grained behavior descriptors
- Temperature, prompt template, population size, island topology, generation count all fixed

**4.3 Precision Levels (Swept)**
| Level | Label | Bits per Weight | Expected Static Quality |
|-------|-------|-----------------|------------------------|
| FP16 | Baseline | 16 | Full precision |
| INT8 | Q8_0 | 8 | Near-lossless |
| INT4 | Q4_K_M | ~4.5 | Mild degradation |
| INT3 | Q3_K_M | ~3.5 | Cliff onset (static) |
| INT2 | Q2_K | ~2.5 | Severe degradation (static) |

**4.4 Budget Regimes (Reported Separately)**
1. **Fixed generations:** Same number of candidate evaluations per condition. Answers: is a quantized proposer worse per attempt?
2. **Fixed compute:** Same wall-clock GPU seconds (or token budget) per condition. Lower precision gets more attempts. Answers: does cheap search beat expensive search per dollar?

**4.5 Metrics (All Logged Per Condition Per Seed)**
- Best fitness found
- QD score (sum of fitness across filled cells)
- Archive coverage (niches filled)
- Mutation viability rate: fraction of proposals that (a) parse, (b) apply as a diff, (c) execute without error
- Tokens generated, wall clock, GPU seconds
- Fitness vs budget curves for both regimes

**4.6 Integrity Checks**
- Quantization integrity: assert loaded model's bits-per-weight and file hash match intended config
- Cost accounting: wall clock, GPU seconds, and token counts measured, not estimated
- Metrics: QD score, coverage, and viability rate each get a unit test with hand-constructed archives
- Hardware fingerprinting: every run log records GPU name, driver, engine version, engine build flags

**4.7 Statistical Design**
- 5 precision levels x 5 seeds x 2 budget regimes = 50 runs minimum
- Report mean, std, and best per condition
- Statistical tests (see Section 7)

### 5. Experiments (~1 page)

**5.1 Pilot / Smoke Test (Phase 1)**
- Single configuration (INT4, 50 generations, 1 seed) on sweep hardware
- Verify best score above 2.5 (sanity check against SOTA ~2.635)
- Budget estimate for full sweep

**5.2 Main Sweep (Phase 3)**
- Full 5x5x2 design
- All conditions on ONE machine, ONE engine, ONE quant family
- Each condition logged to jsonl

**5.3 Static Viability Pre-check**
- Before the sweep: N one-shot generations per precision level
- Count parse/exec rate per level
- If Q2_K viability is exactly zero, add intermediate level (Q2_K_L or IQ3_XXS) for resolution

### 6. Results (~1.5 pages)

**Expected figure structure (4 core figures):**

**Figure 1: Static Cliff vs Loop Cliff**
- X-axis: Precision level (FP16, Q8_0, Q4_K_M, Q3_K_M, Q2_K), left to right decreasing precision
- Y-axis (left): Best fitness (normalized to FP16 baseline)
- Y-axis (right): Static benchmark score (KLD or PPL, from literature)
- Two curves: one from the loop (our data), one from static benchmarks (literature)
- Error bars: std across seeds
- **Key comparison:** Where does each curve drop? If the loop cliff is to the right of the static cliff, the loop rescues. If to the left, the loop compounds.

**Figure 2: Fitness vs Precision at Fixed Generations**
- X-axis: Precision level
- Y-axis: Best fitness (absolute, not normalized)
- Bar chart with error bars (std across 5 seeds)
- Overlay: SOTA line (2.635862 from AlphaEvolve) for reference
- Panels: (a) 50 generations, (b) 200 generations, (c) 500 generations

**Figure 3: QD Score and Archive Coverage vs Precision**
- X-axis: Precision level
- Y-axis (left): QD score (sum of fitness across filled cells)
- Y-axis (right): Archive coverage (niches filled / total niches)
- Two overlaid line plots, different colors, with std bands
- Answers: does lower precision explore more (higher QD score) or less?

**Figure 4: Mutation Viability Rate vs Precision**
- X-axis: Precision level
- Y-axis: Viability rate (fraction of proposals that parse, apply, execute)
- Bar chart with error bars
- Overlay: static benchmark cliff from literature (KLD or PPL)
- **Key mediator check:** If viability drops monotonically with precision, the loop's rescue is limited. If viability stays high until INT2, the loop can absorb most quantization damage.

**Supplementary figures (for appendix or extended version):**
- Figure 5: Fixed compute budget comparison (fitness vs GPU seconds, one curve per precision)
- Figure 6: Lineage depth vs viability (do errors compound across generations?)
- Figure 7: Archive heatmaps at each precision level (selected seeds)
- Figure 8: Scale compensation (30B INT4 vs 7B FP16 at matched memory, if run)

### 7. Statistical Analysis (~0.5 page)

**Required tests to show conditions separate:**

| Test | Purpose | What It Shows |
|------|---------|---------------|
| **One-way ANOVA** (or Kruskal-Wallis if non-normal) | Are there significant differences in best fitness across precision levels? | Whether precision matters at all |
| **Post-hoc Tukey HSD** | Which specific pairs (e.g., FP16 vs INT4, INT4 vs INT3) differ significantly? | Where the cliff is |
| **Effect size (Cohen's d or η²)** | How large is the precision effect in practical terms? | Not just statistical significance but practical magnitude |
| **Regression: fitness ~ precision + seed + viability** | Does viability rate mediate the precision-fitness relationship? | The mediator claim |
| **Shapiro-Wilk test** | Are the residuals normally distributed? | Assumption check for ANOVA |
| **Levene's test** | Are variances equal across groups? | Assumption check for ANOVA |
| **Fixed-generations vs fixed-compute comparison** | Do the two regimes produce different precision rankings? | The two-budget-regime claim |

**Reporting:**
- Mean, std, min, max per condition
- Effect sizes with confidence intervals
- If conditions do not separate at 5 seeds, add seeds before concluding "no effect"
- Report null results explicitly (precision may not matter between INT8 and FP16, for example)

### 8. Discussion (~0.5 page)

**Interpretation of results:**
- Where is the precision cliff in the loop vs the static cliff?
- Does the loop rescue or compound?
- What does the viability rate tell us about the mechanism?

**Implications:**
- For deploying LLM-guided search on resource-constrained hardware (edge devices, mobile, inference at scale)
- For the design of quantized proposer models (which parts of the model need precision, which can be compressed)
- For the two-communities gap (quantization and evolutionary computation researchers should talk to each other)

**Scalability:**
- Results at 30B (or 7B) — would they hold at 70B? At 1B?
- Different quantization methods (GPTQ, AWQ, bitsandbytes) — would results replicate?

### 9. Conclusion (~0.25 page)

- Restate the gap: nobody has varied precision inside a selection loop
- Restate the finding: [PLACEHOLDER — cliff shifted to X bits, viability rate was Y]
- Broader significance: the loop is not a neutral observer of the precision cliff — it reshapes it
- Future work: mixed-precision ensembles, adaptive precision routing, precision-aware archive design

### 10. Limitations and Future Work (~0.25 page)

- Single model family (Qwen3-Coder) — may not generalize to other architectures
- Single quantization method (K-quants) — other methods (GPTQ, AWQ, bitsandbytes) may differ
- Single benchmark (circle packing) — may not generalize to other optimization tasks
- Single QD algorithm (MAP-Elites) — may not generalize to other selection schemes
- The sweep runs on rented GPU hardware — cost limits the number of seeds and generations
- Re-run the contrarian literature hunt before submission (field velocity — the intersection is empty as of July 2026 but may fill)

---

## Required Figures Summary

| Figure | Content | Type | Purpose |
|--------|---------|------|---------|
| 1 | Static cliff vs loop cliff (overlay) | Line plot with error bands | Key comparison — primary contribution |
| 2 | Best fitness vs precision, fixed gens | Bar chart + error bars | Per-budget-regime result |
| 3 | QD score + coverage vs precision | Dual-axis line plot | Diversity/exploration effect |
| 4 | Mutation viability rate vs precision | Bar chart + overlay | Mediator mechanism |
| 5 | Fixed compute comparison | Multi-line plot | Second budget regime |
| 6 | Lineage depth vs viability | Scatter/line plot | Error compounding check |
| 7 | Archive heatmaps by precision | Heatmap grid | Qualitative view |
| 8 | Scale compensation (optional) | Bar chart | Memory-equivalent comparison |

---

## Required Statistical Tests Summary

| Test | Purpose |
|------|---------|
| One-way ANOVA / Kruskal-Wallis | Does precision significantly affect fitness? |
| Post-hoc Tukey HSD | Which precision levels differ? |
| Effect size (Cohen's d / η²) | How large is the effect? |
| Mediation analysis (fitness ~ precision + viability) | Is viability the mechanism? |
| Normality check (Shapiro-Wilk) | ANOVA assumption |
| Homogeneity of variance (Levene's) | ANOVA assumption |
| Paired comparison across budget regimes | Do regimes rank conditions differently? |

---

## Timeline (Recommended)

| Phase | What | Deliverable | Deadline |
|-------|------|-------------|----------|
| Pilot | Phase 1 pilot on sweep hardware | Gate 1 pass (best score > 2.5) | Q3 2026 |
| Sweep | Full 5x5x2 sweep | Raw jsonl data | Q4 2026 |
| Analysis | Figures 1-4, statistical tests | Statistical report | Q1 2027 |
| ISEF paper | Write project paper, abstract, forms | ISEF submission packet | Per affiliated fair timeline (typically Jan-Mar 2027) |
| GECCO paper | Write 8-page ACM paper | GECCO submission | Per CFP (typically Jan-Feb 2027) |
| Re-check | Re-run prior-art hunt | Updated grounding.md | Before GECCO submission |

---

## Notes for the Student

- **ISEF is a science fair, not a conference.** The paper format is more flexible — you write a research paper (10-20 pages) describing your project, prepare a poster board, and give a 5-10 minute oral presentation to judges. The 22 categories include "Robotics and Intelligent Machines" and "Systems Software" as the most relevant fits.
- **GECCO is a conference.** The paper is an 8-page ACM-format paper with double-blind review. The acceptance rate is ~30-35%. GECCO 2027 deadlines are not yet published — watch sigevo.org.
- **The AI usage rules at ISEF are strict.** You used Claude/AI agent as an assistant, which is allowed under the 2027 ISEF rules, but you must clearly document and cite all AI usage. The Society for Science has published specific AI guidelines.
- **Re-run the prior-art hunt before submitting.** The space is active and the gap may close. The project's grounding.md recommends quarterly re-checks.
- **The two-communities gap framing is your strongest argument.** Make it prominent in the Introduction and Related Work.
- **Both positive and null results are publishable.** If precision doesn't matter inside the loop, that's a finding. If the cliff shifts, that's a finding. The mechanism (viability rate) is the mediator either way.