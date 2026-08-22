# Review: "Served Precision Is Part of the Model"

## 1. SUMMARY

The paper argues that served-weight quantization is an unattested serving-path variable that can silently collapse an LLM discovery loop's proposal variation while leaving every pass/fail metric intact. On circle packing with locally served Qwen2.5-Coder-14B GGUF ladders, the 2-bit rung produces coordinate-verified parent echoes at high rates (94% loop condition; 79%/6% on fresh seeds) while viability, validity, and final best score do not separate rungs. A forensic case study of an alias-addressed commercial arm (`opus_alias`, 4/30 valid, anomalously fast) cannot decide between serving-path degradation and genuine tier property because the runtime exposes no serving-path observable, and the alias drifted within six days, making the question permanently unaskable. Six later preregistered waves mostly return UNDERPOWERED or UNINFORMATIVE; one floor-gated secondary (gemma-4-31b, 0.0 vs 4.8 accepted steps) directionally replicates the search collapse. The paper closes with a repair protocol, an honest audit of its own instrument failures, and a claim–evidence map into a released repository.

## 2. CLAIMS-VS-EVIDENCE AUDIT

**Abstract claims:**

| Claim | Verdict | Where |
|---|---|---|
| "viability and validity flat" at degraded quantization | Partially supported | §3.4 reports non-rejection at n=50/rung, explicitly *not* equivalence (§3.1: "no equivalence test was run"); 7B viability *inverts* (§3.3). Abstract omits both caveats. |
| "at the 2-bit rung the proposer largely stops departing from its parent" | Supported descriptively | §3.4 (17/18, 19/24); but §3.5 shows the loop-condition magnitude is partly a parent-quality artifact ("the fresh-seed 79%-vs-6% figure … carr[ies] the same confound"). Abstract states the number without this discount. |
| "echo bound … held on five never-sampled seeds — 79% (19/24) against 6% (1/17)" | Traceable (§3.4, ledger replayed by `sec3_ladder_repro.py`) but **partially supports the implied conclusion**: the bound was registered against the loop design, and §3.5 concedes it "would have failed under fixed parents (52–61%)" for the upper-rung side. |
| "probe explicitly instructing the model not to copy returned coordinate-identical outputs in 5 of 5" | Fully supported | §3.4 must-differ probe; registered rule returned its pre-specified branch. This is the cleanest result in the paper. |
| "1 accepted improvement in 50 calls against 14–16 at the upper rungs" | Supported | §3.6 / Appendix C table (1/50, 15/50, 16/50, 14/50). Post-hoc statistic; does not replicate at 7B (reverses) or IQ2 (p=0.135) — disclosed in §3.6 but not in the abstract. |
| "final best score separates the rungs nowhere" | Supported as non-rejection | Six outcome-level tails, 0.119–0.937 (Appendix C). Abstract presents a null as a finding; it is explicitly underpowered ("non-rejection at five lineages per cell"). |
| "sixth model family … reproduces the search collapse under a registered floor-gated test — 0.0 accepted steps against 4.8" | Supported but thin | §8 wave 7c.2 HELD; the paper itself calls it "one directional replication, not a resolved generalization." |
| "alias drifted within six days — byte-identical prompts returning 30/30 valid against the original 4/30" | Supported | §4.1 arm B2, `arm_r_analysis.py`, Fisher 7.8e-13. Note the paper correctly flags this as pseudoreplication w.r.t. the serving-path question. |

**Introduction/contribution claims:**
- **C1**: The variation-cliff claim is carried by two registered predictions (echo bound, must-differ) plus descriptive replications. The designated primary of the fresh wave (F1) **failed**, both dispersion-probe registered verdicts are unusable (unclassified / FAILED), and the strongest control (fixed-parent) shrinks the effect from 14→94% to 33→92%. C1 as stated in the intro is carefully scoped, but the *abstract* version is not.
- **C2**: "mildly favour[s] an unattested serving path without deciding it" — honestly stated; the favouring evidence (latency) is **not checkable** (claim–evidence map row: "\S4 durations — **not checkable**"), non-interleaved arms, load confound admitted (§4). Supported as a negative/methodological result only.
- **C3**: Non-identifiability conditioned on one runtime — internally coherent, and appropriately weakened by §4.1 (the discriminator presupposed a stable referent).
- **C4**: Repair protocol "three of five repairs fully implemented" — supported by §5's own audit, which names the failures (RUN_DATE wrong for the very arm under study; sample_id collisions).

**Untraceable/soft numbers in the abstract:** none are fabricated, but "viability and validity flat," "final best score separates the rungs nowhere," and the bare "79% against 6%" are all presented without the equivalence/power/confound qualifications the body attaches to them. That gap between abstract and body is the paper's central presentation defect.

## 3. METHODOLOGICAL WEAKNESSES (ranked)

**Blocking**

1. **Abstract/body evidential asymmetry.** The abstract reports the loop-condition echo contrast (79% vs 6%), the search-step collapse (1 vs 14–16), and the outcome null as findings, while §3.5–3.6 establish that (a) the echo contrast is confounded by running-parent quality in the flattering direction, (b) the search-step statistic is post-hoc, fails its own registered primary (F1), reverses at 7B, and does not replicate on IQ2, and (c) the outcome null is unpowered non-rejection. A reader of only the abstract is materially misled relative to the paper's own analysis. Fix: rewrite the abstract around what survives everything — the must-differ 5/5, the fixed-parent radius-collapse endpoint (2/49, 5/84), the B2 drift, and the 7c.2 directional replication — with explicit qualifiers on the rest.

2. **The confirmatory layer is nearly empty, and the paper's headline rests on the surviving fragments.** Of the registered machinery: F1 refuted, dispersion wave 1 unclassified, wave 2 FAILED, scheme control inconclusive, wave 3 UNINFORMATIVE, wave 5 UNINFORMATIVE, wave 7/7b UNDERPOWERED, 7c.1/7c.3 UNDERPOWERED. What remains carrying C1 is F2 (a bound whose thresholds were set by authors who had already seen score-informed estimates of the same contrast in the destroyed first run — §3.4 admits the re-execution's console predictions were "guaranteed to hold") and the must-differ probe. Fix: state explicitly in §3.1 that F2's thresholds were chosen with knowledge of the first run's inferred rates, and downgrade "registered" framing accordingly; consider reporting F2 as a pre-registered *replication target* rather than a blind prediction.

**Major**

3. **Parent-quality confound infects most quoted echo numbers.** §3.5/Appendix B show the loop's 14%→94% is partly artifact; matched-band contrast is 33% vs 92%; the IQ2 scheme gradient is withdrawn; the ≤35% bound "would have failed under fixed parents." Yet §3.4 still presents 79%/6%, the invalid-row near-copy gradient, and the scheme ordering as if independent evidence. Fix: mark every loop-condition echo figure in §3.4 with a pointer to §3.5's discount at first use, and drop the invalid-row gradient or recompute it against matched parents.

4. **Forensic arm's only discriminating evidence is unverifiable and confounded.** Latency lives only in `STATE.md`; arms were not interleaved; load varies (five concurrency-cap rejections elsewhere); throughput is shown (§6 item 4) to be output-dependent and hardware-inverting. The paper knows all this and still titles the section around a "serving signature." Fix: demote the latency observation to anecdote in the section opening, and lead with what is checkable (validity collapse, geometric failure taxonomy, scorecard).

5. **Candidate-level Fisher tests are pseudoreplicated and yet appear throughout, including the abstract-adjacent 5.7×10⁻¹⁰.** Appendix A.4 concedes rows are nested within lineages and that "No claim in this paper rests on any of the twenty-nine." Then why print nine of them in the main text with magnitudes like 10⁻¹⁰? Fix: move all Fisher tails to an appendix table with the nesting defect printed beside each; keep at most the seed-level tests in the body.

**Minor**

6. **Arm R is uninformative by its own trigger and should be compressed.** P-R0's failure voids the H1/H2 reading; 5 invocations/cell excludes only ≥45-point effects. Currently ~1.5 pages for a null result the registration forbids interpreting.
7. **Wave-7c screen selection uses OpenRouter free-tier aliases with unattested serving paths to select models for a precision study** — the paper flags this but the circularity deserves a sentence in Limitations, not just §8.
8. **`\nocite{*}`** dumps uncited works into the bibliography; several "2026" entries are cited by inline arXiv id in Related Work ("arXiv 2605.29268", "2603.07642") rather than natbib keys — inconsistent with the stated conversion policy in the source header comment.

## 4. STATISTICAL RIGOR

- **Sample sizes**: 50 loop candidates/rung (5 seeds × 10), 24–30 probes; dispersion probes 288/432 rows; forensic arm n=30 single batch window; arm R 5/cell; waves 3/5 495 calls; family waves 100/arm. The paper is candid that almost nothing is powered for equivalence, and that five lineages/rung floor any lineage-level permutation tail at 0.0079 — above its own Bonferroni threshold of 0.0042 (Appendix A.4). No CI is reported for the headline echo contrasts (only counts); Wilson intervals appear only for 7B viability.
- **Multiplicity**: 29 p-values in four families, no correction, all disclaimed. Honest, but the disclaimers mean the inferential apparatus is decorative; the paper runs on registered bounds and descriptives. Say this once, prominently, instead of distributing the confession across §3.1, §3.6, and Appendix A.4.
- **Gaming surface**: (i) F2 vs F1 primary designation — disclosed, but the abstract's reliance on F2 alone is a soft garden-of-forking-paths; (ii) the conditional-quality analysis uses a self-set floor of 25 departures written "in an unlocked note, the day the analysis became computable," exclusion holding by 0.8 points and reversing if one row flips — the paper calls this "the thinnest load-bearing thing in the paper," correctly; it should not appear in the main text at all; (iii) the dispersion-probe NED statistic is a substituted definition on a reconstructed quantity (Appendix A.2) — the p=0.030 should be labelled unavailable-by-default; (iv) the seed-crossed, unstratified permutation design (Appendix A.4) is argued conservative, which is plausible but asserted rather than proven — cite or derive the monotonicity claim.
- **Preregistration logic**: generally strong (hash-locked, externally timestamped via public Kaggle pushes), with commendable disclosure of defects (wave 7 priors-section misquote; 304-vs-322 row miscount; unamended gemma-4 retry runner edit). The residual weakness is that several "registrations" are runner-header comments authored by the same party minutes before execution, with thresholds informed by prior partial data (see Blocking #2).

## 5. INTERNAL CONSISTENCY

- **"Three rungs" listing four**: §3.5 "it runs the same Qwen2.5-Coder-14B at the same three rungs (Q8\_0, Q4\_K\_M, Q3\_K\_M, Q2\_K …)" — lists four names for three rungs. Replicated verbatim in Appendix B's Design paragraph. Fix wording.
- **The 38/200 denominator** (§3.4 scale contrast) is said to be "rung-matched, distinct from the 29/200 used above" but its composition is never specified (which 7B rungs?). Define it.
- **Wave numbering collision**: "wave 2" denotes the dispersion probe's second wave in §3.5/Appendix B, while §8's generality programme numbers waves 3,4,5,7,7b,7c — a reader tracking "wave 2" across sections will stumble. Add a wave index table.
- **Echo denominators**: §3.4 gives 17/18 at Q2_K (re-execution) and the map confirms; consistent with 8/57 pooled. Fresh-wave per-seed vectors sum correctly (19/24). 7B pooled 29/200 = 7+6+9+7 ✓. 14B viability sums 87/200 ✓.
- **Abstract "14–16"** matches §3.6 (15, 16, 14 — note 14 is Q8_0, so "14–16 at the upper rungs" is accurate but the range's endpoints come from different rungs than a reader will assume).
- **IQ2_M near-copy 2/22 vs replay 1/22** — disclosed; fine.
- **Terminology drift**: "echo" is used for at least four distinct measures (loop coordinate-verified, centres-only, legacy 1e-5 all-fields, radius decomposition column) with different rates (92–98% vs 52–61% vs 94%). Table 2 in Appendix B helps, but the main text switches senses without flags, e.g., §3.5's "92–98\% at every rung" vs §3.4's "94\% at Q2\_K."
- **Fig. 1 (`fig4_family_echo`)** caption says "each family judged against its own registration's power floor" but plots below-floor bars anyway; the caption then says those bars "cannot speak to either." Cut the below-floor bars.

## 6. WRITING AND STRUCTURE

- **Cut**: the conditional-quality paragraphs in §3.6 and Appendix C (self-admitted thinnest material); the second throughput-withdrawal narrative in §6 item 4 (keep the three mechanisms, cut the wave-by-wave ranges); roughly half of §8 — waves 5, 7, 7b can compress to one table row each since all return UNINFORMATIVE/UNDERPOWERED; the Broader Impact's third paragraph overlaps Limitations almost verbatim.
- **Move**: the "Inferential status of every p-value" block (§3.1) belongs entirely in Appendix A.4 with a two-sentence pointer; the item-4 canary self-audit (§6) is a paper-length digestation inside a list item — promote to its own subsection or an appendix.
- **Where readers get lost**: §3.1 is a 1,500-word meta-summary of a section the reader hasn't read yet, referencing forward to §3.4, §3.5, §3.6, §6, §8 simultaneously; the Introduction's C1 paragraph is similarly a compressed abstract-of-the-paper containing every caveat at once. Restructure: short contributions list, caveats at point of use.
- The companion/antecedent dependency ("protocol §3.4, results §5.9" of an external markdown file) makes §3 partially unverifiable without a second document; state which antecedent figures are load-bearing and vendor those too.
- Sentence-level: §4's "weaker than absent, and it matters at this size" is opaque on first read; §8's wave-7c paragraph is a single ~600-word block mixing five topics (screen, provider churn, gpt-oss, gemma-4, amendment discipline) — split.

## 7. MISSING BASELINES / RELATED WORK

- **Quantization methods**: no GPTQ/AWQ/bitsandbytes run (acknowledged as a caveat in §7); at minimum, one non-GGUF method at 2-bit-class would test whether the cliff is K-quant-specific — especially given the IQ2 result already points away from bit-width.
- **A full-precision 14B rung** is missing for hardware reasons; a CPU/offload FP16 arm, even at reduced n, would anchor the top of the ladder.
- **Longer-horizon run**: registered as a prediction, never run (Appendix C); a reviewer will ask why a 100-generation run on one rung pair wasn't executed given the entire outcome-null hinges on horizon.
- **Contamination screen**: specified, not run (Limitations); given the anchoring story leans on exactly the N most likely in training corpora, this is the obvious referee request.
- **Related work**: the fingerprinting/attestation coverage is strong; missing are (a) quantization-robustness work on *agentic/tool-use* benchmarks beyond Mix-Quant, (b) model-routing literature (multi-provider routers, e.g., RouteLLM-style systems) directly relevant to the four-providers-one-alias observation in wave 7c, and (c) the spec-decoding fidelity literature (draft-model distribution divergence), which is the most direct prior art for H1's mechanism.

## 8. TOP 10 CONCRETE EDITS

1. Rewrite the abstract so every quantitative claim carries its §3.5/§3.6 qualifier (confound, failed primary, non-rejection) in-line.
2. State in §3.1 that F2's thresholds were authored with knowledge of the first run's score-informed estimates, and relabel F2 accordingly everywhere.
3. Delete the conditional-quality analysis from §3.6 and Appendix C main flow; leave one sentence pointing to a locked-note disclosure.
4. Move the entire "Inferential status of every p-value" block to Appendix A.4 and replace with two sentences.
5. Fix the "same three rungs (four names)" contradiction in §3.5 and Appendix B.
6. Define the composition of the 38/200 denominator in §3.4.
7. Demote the `opus_alias` latency observation in §4's opening to a clearly-labelled unverifiable working-log anecdote, leading instead with the recomputable validity collapse.
8. Compress §8 waves 5/7/7b into a summary table with one verdict line each; expand only 7c.
9. Remove below-floor bars from Fig. 1 and add a wave-index table resolving the "wave 2" numbering collision.
10. Replace `\nocite{*}` with explicit keys and convert the inline arXiv-id citations in §7 to natbib entries.

## 9. RECOMMENDATION: **Major revision**

This is an unusually honest paper with a genuinely interesting thesis, exemplary artifact discipline (the claim–evidence map with explicit "not checkable" rows is the best I have seen), and real findings — the must-differ 5/5, the fixed-parent 2-bit endpoint, the B2 drift, and the 7c.2 directional replication would each survive scrutiny. But the manuscript currently buries its defensible core under a confirmatory apparatus that largely returned unusable verdicts, quotes confounded and post-hoc statistics in the abstract without their own body-text discounts, and spends pages on analyses it itself withdraws. TMLR readers would find the topic valuable; the current version asks them to trust framing that the paper's own appendices contradict. The revision needed is substantial but tractable — it is primarily compression, re-scoping of claims, and abstract repair, not new data collection, though I would strongly urge the cheap additions (one non-GGUF 2-bit method; a contamination probe) before acceptance.