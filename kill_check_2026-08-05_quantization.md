# Kill-check panel — mixed-precision quantization thesis directions (2026-08-05)

Six proposed research directions (from an AI-generated "open gaps in mixed-precision quantization" pitch + its self-audit) adversarially reviewed. 6 independent web-searching hunters (one per direction, KILL default under uncertainty, 15+ queries each) + 1 citation-forensics auditor over every paper named in the pitch. ~140 queries total; all load-bearing arXiv IDs verified by fetching abstract pages.

## Headline: ALL SIX KILLED. Plus 1 fabricated citation and 2 spliced descriptions in the source audit.

| direction | verdict | kill shot |
|---|---|---|
| D1 Shapley/causal error cascades | KILL | IMPQ/CoopQ (2509.15455) already does Shapley + inter-layer interactions for LLM MPQ; 2607.12266 gives a certified CLOSED-FORM (non-MC) model that beats it AND shows interactions are only ~7–15% of loss variance at 4-bit — the phenomenon is a second-order residual |
| D2 data-free closed-form bit allocation | KILL | AlphaQ (2606.04980, Mahoney group) does calibration-free allocation from heavy-tailed weight spectra — the exact proposed method, by the originators of the spectral theory; NSDS (2603.17354) covers dense per-layer. OWQ shows activation outliers put a provable information ceiling on any weight-only statistic |
| D3 joint W/A/KV dynamic budget controller | KILL | MorphServe (2506.02006) already swaps weight precision + resizes KV under runtime memory pressure; "Don't Waste Bits" (2604.04722) is the learned KV-precision controller verbatim; the three-way "budget" framing is dimensionally dishonest (decode activation memory is transient/small) |
| D4 router-aware MoE via routing entropy | KILL | GeMoE (2606.26287) already uses gating entropy as information-theoretic token complexity; DynaExq (2511.15015) does runtime dynamic expert precision; 2604.06515 supplies the theory. "Routing entropy bound" reduces to a renamed top-k-margin sensitivity metric |
| D5 long-horizon degradation index | KILL | "Flat Score, Amplified Failures" (2607.27275) IS the hidden-agentic-failure claim; 2606.00206 does per-token KL along long generations; and 2606.19558 shows fidelity metrics FAIL to predict downstream quality in the near-baseline regime — the null hypothesis is favored against the proposed index |
| D6 zero-overhead bit-packing compiler | KILL | Tilus (2504.12984) + eXmY (2405.13938) + T-MAC (2407.00088) + FP6-LLM (2401.14112) jointly cover arbitrary-bit-width execution on commodity HW; "zero overhead" is incoherent in the compute-bound regime (lane-boundary crossing vs padding tradeoff) and already achieved-below-roofline in the memory-bound one |

Note the pitch's own novelty ranking was exactly backwards: it rated D5 "wide open, highest novelty" (published July 2026, plus a direct negative result against the method) and D2 "completely unrealized" (published June 2026 by the group best positioned to extend it).

## Per-direction detail

### D1 — Cooperative game theory / directional SCMs for error cascades — KILL
- SMPQ = arXiv:2508.03002 (IJCAI 2025): MC-Shapley bit-width contributions, vision NNs. REAL.
- IMPQ = arXiv:2509.15455, retitled **CoopQ** in v2 (Dec 2025), UC Irvine: Shapley layer sensitivities AND pairwise inter-layer interactions, binary quadratic opt, 2/4-bit LLMs. The thesis core, done.
- Directional propagation already exact: 2607.14630 proves the recursion e_{l+1} = A_l e_l + q_l exact for arbitrary nonlinear layers; QEP (2504.09629, NeurIPS 2025) operationalizes upstream-error compensation; BRECQ (2102.05426)/QDrop have conditioned on propagated quantized activations since 2021; cross-layer Hessian: 2306.04879 (Google); pairwise-interaction IQP: CLADO 2307.05657.
- The closed-form-instead-of-MC delta: 2607.12266 ("Saturation Makes Quantization Error Additive") — certified closed form, beats CoopQ and HAWQ on 30B–355B, shows interactions ≈ 7–15% residual at 4-bit.
- Causal branding also taken: Causal-DFQ (2309.13682, ICCV 2023); Mix-QSAM (2505.04861) has causal-MI "cross-layer synergy" by name. Asymmetric/causal Shapley machinery is off-the-shelf since NeurIPS 2020 (1910.06358, 2011.01625). On a chain DAG it degenerates toward sequential attribution = what progressive quantization already computes.
- Salvage: regime map of WHEN interactions become first-order (sub-4-bit, residual/attention couplings) + certified corrections atop 2607.12266's additive model. Analysis paper, not new axioms.

### D2 — Data-free closed-form bit allocator — KILL
- AlphaQ arXiv:2606.04980 (Jun 2026, Yang…Mahoney): calibration-free MoE bit allocation from HT-SR spectral alpha, beats calibration baselines. AlphaPruning (2410.10912, NeurIPS 2024) was the precedent.
- NSDS arXiv:2603.17354 (Mar 2026): calibration-free per-layer LLM allocation from weight numerical+structural sensitivity. SQuant (2202.07471, ICLR 2022): statistics-only data-free quantization is 4 years old. BAQ (2506.05664): closed-form Lagrangian allocation. RateQuant (2605.06675): reverse water-filling for LLM bit allocation.
- Killed by theory in the damaging direction: sensitivity ≈ tr(H·ΔW²), H ≈ E[XX^T] is activation-dependent; LLM.int8/SmoothQuant/OWQ (2306.02272) show fixed-channel ~100x activation outliers dominate — invisible to any weight-only statistic. So the idea is neither impossible (data-free proxies work "well enough" — already mined) nor open. Worst thesis position.
- Salvage: bounds on when/why data-free spectral statistics predict activation-Hessian sensitivity (and when outliers provably break them). Workshop-scale.

### D3 — Joint W/A/KV runtime budget controller — KILL
- MorphServe 2506.02006: runtime quantized-layer swapping + KV resizing under real-time memory pressure, in a serving stack. The claim, published.
- Controller-driven KV precision: 2604.04722. Runtime layer-wise weight precision: FlexQuant 2506.12024, DP-LLM 2508.06041. Sequence-position-driven: PMPD 2410.13461, PM-KVQ 2505.18610. Phase-aware activations: Mix-Quant 2605.20315. Switching mechanism solved by nested representations: Any-Precision LLM 2402.10517, Matryoshka 2502.06786, MoBiQuant 2602.20191, NestedFP 2506.02024. Rate-distortion angle taken: RateQuant 2605.06675, RDKV 2605.08317. Systems venue presence: Oaken ISCA 2025.
- Physics problems: decode activation memory is transient (not a budget axis); quantized KV can't be up-converted (shifts are one-directional, PM-KVQ already exploits this); "continuous" shifting is discrete kernel swaps.
- Salvage: online algorithm with regret/SLO guarantees for W-vs-KV reallocation under bursty multi-tenant load, on Matryoshka representations, in vLLM → MLSys/EuroSys systems paper, not an ML thesis.

### D4 — Router-aware MoE via routing entropy — KILL
- Router-flip phenomenon + alignment: EAC-MoE 2508.01625 (ACL), EAQuant 2506.13329, VSRAQ 2606.05688, ExpertQuant/Rank-Aware PTQ (OpenReview kPgLp47bJf). Expert-importance mixed precision: MC-MoE 2410.06270 (ICLR 2025), MC# 2510.10962, MxMoE 2505.05799, BitsMoE 2606.00079, GEMQ 2605.23078.
- The "open gap" specifically: gating entropy as MDL token-complexity → GeMoE 2606.26287. Runtime dynamic expert precision → DynaExq 2511.15015, DyMoE 2603.19172. Theory-backed allocation → 2604.06515. Rate-distortion routing → 2605.05278. Per-token precision mechanism → MoBiQuant 2602.20191.
- "Routing entropy bound" = two-line Gaussian perturbation on top-k margins; VSRAQ/rank-aware PTQ already operationalize the margin version. Per-token expert precision breaks batched GEMM uniformity (DynaExq chose per-expert granularity for exactly this reason) and saves no weight memory.
- Salvage: certified flip-probability/distortion bound + routing-robustness stress suite over the 10+ existing MoE-PTQ methods — analysis paper, 4–8 pages.

### D5 — Autoregressive Degradation Index — KILL (the "wide open" one)
- The phenomenon: 2607.27275 "Flat Score, Amplified Failures" (Jul 2026) — quantization amplifies agent failures up to 2.5x while flat scores mask it. Benchmarks exist: ACBench 2505.19433 (ICML 2025), 2505.20276 (EMNLP 2025, 4-bit drops ≤59% long-context), 2504.04823 (long-CoT).
- The measurement primitive: per-token KL quantized-vs-FP is published (2407.09141 "Accuracy is Not All You Need") and folk practice in llama.cpp/exllama since 2023; 2606.00206 already localizes divergence to high-entropy branching tokens along long generations.
- The direct negative result: 2606.19558 "Displacement Is Not Direction" — fidelity metrics collapse to non-significance in the near-baseline "silent zone" where deployment decisions live. The proposed index's null hypothesis is favored.
- Theory occupied and complicating: exposure-bias quadratic bounds 2204.01171; 2505.24187 shows accumulation is key-token-dominated, NOT uniform drift → no clean closed-form index; 2607.16237 measures quantized recursive-trajectory divergence (84.1%→0.0% Sudoku); chaotic divergence ≠ task failure (trajectories decorrelate while staying individually coherent).
- Salvage (best of the six, still not a thesis): branch-point-conditional divergence as a cheap forecaster of quantized-agent failure horizons — explicit confirm-or-rebut of the 2606.19558 silent-zone null, features from 2606.00206, validated on tau-bench-style episodes. Careful measurement paper.

### D6 — Zero-overhead virtual bit-packing compiler — KILL
- Coverage: T-MAC 2407.00088 (EuroSys'25; bit-serial LUT, any integer width, NO unpacking, linear scaling on legacy CPU SIMD); Tilus 2504.12984 (GPU VM for arbitrary 1–8-bit non-power-of-2 kernels, beats Ladder 2.61x); eXmY 2405.13938 (Google; arbitrary 3/5/6/7/9-bit types, perfect compression + byte addressability on CPU/TPU/GPU); FP6-LLM 2401.14112 (ATC'24; AOT bit-level pre-packing for x-bit on tensor cores, in DeepSpeed); FLUTE 2407.10960; FullPack 2211.06982; Marlin 2408.11743 (near-ideal 4x in memory-bound regime = overhead already hidden); Ladder OSDI'24/BitBLAS; LUT Tensor Core 2408.06003 (ISCA'25 hardware endgame); survey 2506.11728 maps the whole space.
- Coherence: "zero overhead" is regime-dependent. Memory-bound: unpacking hides under DRAM latency — no headroom left. Compute-bound: non-power-of-2 widths force cross-lane shifts (no per-lane funnel shift on commodity SIMD) or padding that surrenders the bandwidth savings — the claim is unachievable as stated. Bit-serial/LUT reformulation dissolves the premise entirely.
- Wrong genre regardless: kernels/layouts/codegen = MLSys/ATC/PPoPP engineering dominated by industrial teams. No theorem-shaped core.
- Salvage: instruction-count/density lower bounds for sub-byte decode on abstract SIMD ISAs; characterize when bit-serial LUT beats pack-shift. Workshop paper.

## Citation forensics on the source pitch/audit

| item | verdict | actual ID | note |
|---|---|---|---|
| AlphaAMR | **FABRICATED** | none | No paper, repo, or preprint exists; only stock-ticker noise. Classic hallucination. |
| EAQuant | MISDESCRIBED (spliced) | 2506.13329 | Real, but uses KL-style router-distribution alignment; the "hinge losses" attributed to it belong to ExpertQuant. Mechanisms swapped between the two. |
| ExpertQuant | REAL, desc. slightly off | OpenReview kPgLp47bJf ("Router Choice Matters") | Rank-aware Jaccard + gap hinge loss; the "logit alignment" the audit credits it with is actually EAQuant's approach, which ExpertQuant criticizes. |
| ZeroQuant-HERO | REAL, context suspect | 2310.17723 | W8A8 HW-aware PTQ (2023), not a "recent sub-component precision-scaling" paper; attached to the same suspect context as fabricated AlphaAMR. |
| IMPQ | REAL (renamed) | 2509.15455 | Now titled CoopQ on arXiv (v2). |
| SMPQ | REAL (gloss) | 2508.03002 | "SMPQ" is the method name; paper title differs; vision NNs, not LLMs. |
| DeepGEMM | REAL, wrong category | github.com/deepseek-ai/DeepGEMM | DeepSeek's is FP8/byte-width, not sub-byte bit-packing (a separate 2304.09049 "DeepGEMM" is LUT CPU — ambiguous reference). |
| Mix-GEMM | REAL, wrong category | IEEE HPCA 2023 (10071076) | HW-SW co-designed RISC-V accelerator, not a GPU software library; miscategorized alongside BitBLAS. |
| SMPQ, CoQuant, KVmix, EAC-MoE, FWSVD, HAWQ/V3, AWQ, LUT-GEMM, BitBLAS, Blackwell 4/6-bit UMMA | REAL, match | see per-direction sections | Blackwell claim verified via Colfax/CUTLASS docs (nuance: f8f6f4 mode pads sub-byte operands to 1 byte in SMEM; packed sub-byte needs block-scaled paths). |

## "Does it scream AI-generated?" — assessment of the source pitch

Yes, on five independent tells:
1. **One fabricated citation (AlphaAMR)** and one mechanism-splice (EAQuant↔ExpertQuant hinge loss) — the same failure classes we caught in the Gemini triage on paper 1 (fabricated Opti-Agent-Bench; Gideoni real-person/wrong-paper splice).
2. **Confidence inversely correlated with truth**: the two directions declared most open ("completely unrealized", "wide open, highest novelty") were both published in June–July 2026 — the pitch's knowledge is ~12 months stale and it presented staleness as novelty.
3. **Template gap-construction**: every direction is "combine [trendy formalism] with [trendy subfield]" (Shapley+quantization, SCM+quantization, entropy+MoE, chaos+agents) — the formalism is decorative; hunters found each reduces to an existing sensitivity metric renamed.
4. **Grandiose unfalsifiable framing**: "NP-hard 6^80 combinatorial explosion", "completely changing the landscape", "elegant analytical framework" — hype phrasing with no mechanism.
5. **No negative-result awareness**: the pitch never checks whether its proposed metrics could fail; 2606.19558 (a direct null against D5's core mechanism) is exactly what a real literature pass surfaces first.

## Net recommendation

Do not build a thesis on any of the six as pitched. If the student wants this subfield anyway, the two least-dead salvage seams, both analysis-paper-scale:
- **D5 salvage**: branch-point-conditional divergence as failure-horizon forecaster, framed against the 2606.19558 null (measurement/negative-result paper; cheapest to run; single-node feasible).
- **D1 salvage**: regime map of when cross-layer interactions become first-order (sub-4-bit), with certified corrections atop the additive model of 2607.12266.
Everything else: occupied (D2, D3, D4) or wrong genre for academic math (D3, D6).

No changes to paper 1 / paper 2 scope; this panel was a branch-off evaluation only.
