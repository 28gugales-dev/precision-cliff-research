# Citation audit — paper2_short.md (TMLR submission)

Date: 2026-08-12. Every arXiv id cited in the manuscript was fetched live
(`arxiv.org/abs/<id>`) and checked for existence, withdrawal status, and
whether the fetched title/topic supports the claim attributed to it in the
manuscript's prose (§7 unless noted).

**Result: 38/38 ids exist, 0 withdrawn, 0 unreachable. 36/38 claim-match
CONFIRMED; 2 PLAUSIBLE (title consistent, specific claim needs a human
read of the abstract before submission).**

| arXiv id | First author | Title (fetched) | Exists | Claim match |
|---|---|---|---|---|
| 2003.12206 | Pineau | Improving Reproducibility in ML Research (NeurIPS 2019 program) | yes | CONFIRMED — cited as canonical reproducibility anchor |
| 2210.17323 | Frantar | GPTQ: Accurate Post-Training Quantization | yes | CONFIRMED — method reference |
| 2306.00978 | Lin | AWQ: Activation-aware Weight Quantization | yes | CONFIRMED — method reference |
| 2307.09009 | Chen | How is ChatGPT's behavior changing over time? | yes | CONFIRMED — behavioral change behind stable identifier |
| 2406.10229 | Madaan | Quantifying Variance in Evaluation Benchmarks | yes | CONFIRMED — seed variance, 280 models/13 benchmarks |
| 2407.03211 | Marchisio | How Does Quantization Affect Multilingual LLMs? | yes | CONFIRMED — automatic metrics understate harm |
| 2411.00640 | Miller | Adding Error Bars to Evals | yes | CONFIRMED — power/uncertainty machinery |
| 2501.03035 | Li | Quantization Meets Reasoning (exploration) | yes | CONFIRMED — reasoning fragile under compression |
| 2504.04715 | Cai | Are You Getting What You Pay For? Auditing Model Substitution | yes | CONFIRMED — TEE conclusion as cited |
| 2505.11574 | Li | Quantization Meets Reasoning (mitigation) | yes | CONFIRMED — companion of 2501.03035 |
| 2506.09501 | Yuan | Numerical Sources of Nondeterminism in LLM Inference | yes | CONFIRMED — batch/hardware nondeterminism, ~9% swings |
| 2506.12044 | Chang | Why Do Some Inputs Break Low-Bit Quantization? | yes | CONFIRMED — residual-stream explanation |
| 2506.23706 | Schnabl | Attestable Audits: Verifiable AI Safety Benchmarks (TEEs) | yes | CONFIRMED — enclave benchmarks |
| 2508.15503 | Baltes | Guidelines for Empirical LLM Studies in SE | yes | CONFIRMED — reporting-guideline citation (§6/§7 hazard list) |
| 2509.19349 | Lange | ShinkaEvolve | yes | CONFIRMED — two-tier novelty rejection sampling; 2.635983283 lineage value |
| 2511.17592 | Khrulkov | GigaEvo | yes | CONFIRMED — 2.636 lineage entry |
| 2511.23473 | Wang | ThetaEvolve: Test-time Learning on Open Problems | yes | CONFIRMED — cited as unverified report, correctly hedged |
| 2512.00651 | Siddiq | LLMs for SE: A Reproducibility Crisis | yes | CONFIRMED — reproducibility-crisis citation |
| 2601.01954 | Korn | Reporting LLM Prompting in Automated SE | yes | CONFIRMED — prompt-reporting guideline |
| 2601.10657 | Yan | PACEvolve | yes | CONFIRMED — context pollution / mode collapse / collaboration failure list |
| 2601.14277 | Kurt | Which Quantization Should I Use? (llama.cpp on Llama-3.1-8B) | yes | CONFIRMED — same ladder, same wave-7 model, one-shot |
| 2601.14888 | Lv | What Makes Low-Bit QAT Work for Reasoning LLMs? | yes | CONFIRMED |
| 2602.20133 | Cemri | AdaEvolve | yes | CONFIRMED — 2.636 lineage entry |
| 2603.07642 | Su | Helix: Evolutionary RL for Open-Ended Scientific Problem Solving | yes | CONFIRMED — 2.63598308 lineage entry |
| 2603.19022 | Leshin | Behavioral Fingerprints for LLM Endpoint Stability and Identity | yes | CONFIRMED — Stability Monitor, detects quantization change; detect-vs-attest distinction is the manuscript's own |
| 2604.19884 | Zhou | From Signal Degradation to Computation Collapse | yes | CONFIRMED — two 2-bit failure modes, exactly as characterized |
| 2604.24372 | Luo | SeaEvo: Strategy Space Evolution | yes | CONFIRMED — cited as unverified report, correctly hedged |
| 2605.20315 | Lu | Mix-Quant: Quantized Prefilling, Precise Decoding for Agentic LLMs | yes | CONFIRMED — decode-phase sensitivity |
| 2605.29268 | Xing | Compute Allocation in Evolutionary Search: Depth-Breadth to Bandits | yes | CONFIRMED (upgraded 2026-08-12, fulltext read) — studies CP n=26 in unit square maximizing sum of radii, fitness normalized to AlphaEvolve's 2.635, explicit best-of-N baseline (T=1 allocation) |
| 2605.29979 | Wimbauer | Fingerprinting Inference Systems of LLMs | yes | CONFIRMED — output-text fingerprinting, engaged in §5 |
| 2606.11217 | Vaccaro | Preregistration for Experiments with AI Agents | yes | CONFIRMED — registration-standard list |
| 2606.21090 | Lin | Self-Improvement Can Self-Regress (rise-and-collapse) | yes | CONFIRMED — nearest loop-degradation precedent |
| 2606.27687 | Thomas | Mitigating LLM-based p-Hacking by Preregistering | yes | CONFIRMED — registration-standard list |
| 2607.07184 | Williams | Predicting LLM Safety Before Release by Simulating Deployment | yes | CONFIRMED (upgraded 2026-08-12, abstract read) — uses "registered, outcome-blinded predictions for GPT-5.4"; belongs in the registration-standards list |
| 2607.08734 | Rababah | The Illusion of Equivalency (quantization) | yes | CONFIRMED — correctness agreement; divergence under stable accuracy/perplexity |
| 2607.10252 | Bruckner | One Token Is Enough (single-token fingerprinting) | yes | CONFIRMED — ~hundred single-token queries, identity not quantization |
| 2607.18867 | Jia | HindsightBench | yes | CONFIRMED — concurrent, registration list |
| 2607.20860 | Zhang | IRIS: Auditing Model Substitution and Routing Dilution in LLM Gateways | yes | CONFIRMED — routing-dilution extension |

## Non-arXiv citations (not machine-checked this pass)

| Citation | Where | Status |
|---|---|---|
| Pineau et al., JMLR 22(164), 2021 | §7 | journal version of 2003.12206 — consistent |
| He et al., Thinking Machines Lab, 2025 (batch-invariance) | §7 | verify blog/report URL before submission |
| Zhou et al., Nature, 2024 (larger models err more) | §7 | verify exact Nature reference |
| AlphaEvolve (2.635) | §7 | verify source (DeepMind report/paper) |
| GUIDE-LLM | claim-evidence map hazard list | RESOLVED (2026-08-12): Feuerriegel et al., "A reporting checklist for large language models in behavioural science", Nature Human Behaviour 10:1182–1186 (2026), nature.com/articles/s41562-026-02492-7 — bib entry added |

## Notes

- One metadata nit from the fetch pass: AWQ (2306.00978) reported year 2026 by
  the fetcher — that is the latest-revision date; the paper is 2023 (MLSys
  2024). Bib entry uses the official arXiv bibtex.
- The two PLAUSIBLE rows are existence-confirmed; only the fine-grained claim
  wording needs a human pass. Neither is load-bearing for any registered
  outcome.
