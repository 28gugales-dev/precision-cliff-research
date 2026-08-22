# TMLR Review: "A Closed Form for What the Model Emits: Template Anchoring in Unconditioned Zero-Shot Circle Packing"

## 1. SUMMARY

The paper claims that a weak-tier LLM, asked zero-shot to pack $N$ circles in a unit square, does not search but emits a predictable grid template: nearest-square order $k^*=\mathrm{round}(\sqrt{N})$, with value given in closed form by $V(k,m)$ or $T(k,N)$, and this prediction is the empirical modal output. Support comes from ~15 preregistered arms (~1,300 invocations total): a 7-cell square forecast (§3.2–3.3), branch-stress (§3.4), parent-conditioning and choice probes (§3.5), cross-vendor replication (§3.6), code-channel arms (§3.7), a rectangle transfer (§4), a three-tier ladder (§5), and a trace-elicitation/faithfulness study (§6). The paper is exceptional in its disclosure discipline: falsifiers that fired are reported in place (arm M, arm MU, arm T), post-hoc analyses are labeled, and a deviations table (Appendix B) itemizes every departure from registration. The headline findings are that the anchor is modal at 7/7 original square cells, dissolves under parent conditioning, survives delegation to an executed math-only program as a ceiling (0/115 above the family argmax), and is a family property bounded on both sides by the gemma pair.

## 2. CLAIMS-VS-EVIDENCE AUDIT

| # | Claim (location) | Verdict | Evidence |
|---|---|---|---|
| C1 | "that prediction is the empirical modal output at every tested $N$" (abstract) | **Does not hold as stated** | True only for the 7 original square cells (§3.2 table). Arm M, weak tier, disconfirmed the registered prediction at 3 of 3 converge cells (Table M: $N$=20/30/41, modal outputs are $(k^*{+}1)$-grid values). GM3: modal at 2/5 scoreable cells. The abstract's own next sentence ("Preregistered extensions bound the result") does not repair a flat "every tested $N$." Must be scoped to "every $N$ of the original square arm" or "7/7 square cells." |
| C2 | "fails to build it in 30 of 31 invalid attempts" (abstract) | **Partially supports; number misstated** | Table CH: 31/31 invalid rows attempt the argmax; 30 misplace fillers, 1 emits unevaluable radicals — so 31 of 31 fail to build it, 30 with misplaced fillers. "30 of 31" reads as one success. |
| C3 | "0 of 115 valid program outputs exceed the family argmax (one reaches it, exactly)" (abstract) | **Fully supports** | CC 0/37 with one exact argmax hit at $N$=13 (§3.7 table), CC2 0/41, CCS 0/37; 37+41+37=115. |
| C4 | "the anchor value remains the modal weak-tier output at all three cells in both waves" (abstract) | **Supports, with disclosed fragility** | §3.7: CC modal at 3/3 but by one-sample margins at $N$=13 and 31 (disclosed in the same section); CC2 3/3 with firm margins. |
| C5 | "The behaviour transfers across three vendors" (abstract) | **Partially supports** | Arm V: Cohere 8/12 and gpt-oss-20b 11/18, both with Wilson CIs including 50% (§3.6 table); the third "vendor" (Google) is split — gemma-26b pooled-HELD under GM3 but gemma-31b DOES-NOT-TRANSFER at 0/15. "Three vendors" is defensible only by counting GM3; the abstract should say "two vendors transfer cleanly; a third splits by model size." |
| C6 | "78% → 100% → 13% ... 64% → 90% → 13%" (Contribution 2) | **Supports but internally contradicted** | Table 2 rows match, but the paper's own Table 2 footnote says "it is the matched comparison (83% → 100% → 13%) that should be quoted across tiers" — the abstract-adjacent contribution quotes the unmatched 78%. |
| C7 | "54 of 56 scoreable claims (96.4%)" (Contribution 3) | **Fully supports** | §6.5, blind rubric frozen at commit e181d2a; CI [88%, 99%] honestly noted to straddle the 90% bar. |
| C8 | "87% vs 70%, $p=0.0325$ uncorrected ... fails multiplicity correction" (Contribution 3) | **Fully supports, honestly scoped** | §6.2, §6.4; carried by one cell, wave-confounded, reported as exploratory. |
| C9 | "the provably better in-family rival is emitted 3 times in 147" (Contribution 4) | **Supports arithmetically; pool is selected** | 2/57 + 1/53 + 0/11 + 0/10 + 0/16 = 3/147, each component traceable. But the pool excludes GM3, where the rival is the *mode* at 27/43 discriminating validities — the paper discloses this ("the counterexample that proves the statistic is a family trait") but the headline "near-deterministic strong form" is a pool constructed around the disconfirming arm. |
| C10 | "verified against a linear-programming oracle on 83 configurations to within $10^{-9}$" (Contribution 1) | **Supports** | §2.1/§1.1; rectangle oracle separately at 213 configurations (§4.1). |
| C11 | "the template is not what the model prefers but what it can reliably execute" (abstract, §3.5) | **Supports** | Arm CH decomposition (Table CH) + arm MU asymmetry (Table MU); this is the paper's best-supported mechanistic claim at the behavioral level. |
| C12 | "making anchoring a family property rather than a vendor artifact" (abstract) | **Partially supports** | Two transfer vendors at $n$=12/18 point-estimate passes + one non-transferring sibling at $n$=15, with variant/instrument confound explicitly non-attributable (§3.6, last paragraph). "Family property" is a boundary description, not an established property. |
| C13 | Untraceable number: §3.6 "the registration recorded the original family's prior for the same statistic as **0/21**" | **Untraceable** | §3.3 gives rival counts of 2/23 (original corpus) and 2/57 (full ledger). No table or section yields 0/21. Must be corrected or sourced. |
| C14 | Corpus arithmetic: §3.5 "Raw rows verbatim in arm_mu_collect.jsonl (**180 of 180** launched invocations collected)" | **Inconsistent** | Arm MU alone is 135 invocations (§3.5: "135 invocations"); 180 = MU(135) + CH(45), as §6.1 correctly states. The sentence as written attaches 180 to MU. |

## 3. METHODOLOGICAL WEAKNESSES (ranked)

**Blocking**

- **B1. GM3's registered pooled bar produces a misleading "HELD" verdict.** The pooled ≥30% bar passes at 57.5%, but 35 of 46 hits sit in the two non-discriminating cells where prediction = family argmax (any family member hits by construction); the discriminating-cell rate is 11/43 = 25.6%, *below* the bar (§3.6). The registered verdict rule was misdesigned, and Table CV still prints "pooled **HELD**" as the verdict. Fix: relabel the verdict in Table CV as "pooled bar met; discriminating-cell bar failed" and strip "HELD" from every downstream summary (§5, §8).
- **B2. Contamination is unprobed while the fitted cells are the published ones.** The rule was fitted on $N$=23/26/27 (§3.3) — $N$=26 is the canonical, almost certainly in-training cell — and no canary, held-out-$N$, or lexical-perturbation test was run (§8 admits this). Every "out-of-sample" square cell could be lexically contaminated. Fix: run the bare prompt on 3–5 $N$ values with no published packing history (e.g., $N$=52, 55, 59) before this claim is treated as a law rather than a description of trained-on cells.

**Major**

- **M1. Arm V verdicts are point-estimate passes at $n$=12 and $n$=18 with CIs including the bar** (§3.6 table, disclosed). "TRANSFERS" as a registered verdict label overstates. Fix: label "point-estimate pass, CI includes bar" in the table, and pool the two transferring vendors (19/30, CI ~[47%, 79%]) as the arm-level statistic.
- **M2. opus_alias arm: three of four registered predictions de-registered post hoc in the only arm that disconfirmed** (§5, Appendix B). The disclosure is exemplary, but the ladder's third rung rests on 4 valid samples from an unattestable alias with anomalies (latency, uniform token counts) that exist only in an unreleased transcript. Fix: either release the session transcript or cut the latency/token paragraph; demote the 13% validity figure to "descriptive, $n$=30, alias unattested."
- **M3. The gemma pair's "boundary runs both ways" interpretation is confounded by design** (§3.6, admitted: "model variant and instrument quality change together"). 26b was measured first-party at 7×20; 31b free-tier at 5×5 through a rate-starved alias. Fix: one arm running both gemma sizes under the GM3 instrument would make this claim attributable; until then, soften "bounded in both directions by a fourth family" in the abstract to "bracketed, with the split not attributable to model size vs. instrument."
- **M4. No cross-arm multiplicity accounting, and the "stopping rule" is post hoc.** §9 states no correction across arms; CC2/CCS were registered *after* CC's results (disclosed), and the revision "closed" before arms that were then run. The garden-of-forking-paths protection is registration-per-arm plus exhaustive reporting — acceptable, but the paper should state the implied per-arm false-positive budget explicitly (15 arms × directional tests at nominal α).

**Minor**

- **m1.** Arm T's falsifier tie-handling: registered prose vs. analysis code disagreed; both readings reported (§6.3) — good, but the remedy (executable registrations) should be adopted for any future arm and stated as a recommendation.
- **m2.** $N$=43 bare prompt hash never registered (§9, Appendix A.4) — one of seven headline cells has no pre-sampling prompt lock.
- **m3.** Rectangle ledger has no hashes, dates, or proposer fields (§4.1, §9) — the transfer arm has the weakest provenance.
- **m4.** Sampling parameters unpinned throughout (§8) — all "modal" claims are regime-relative; already scoped, keep it that way in the abstract.
- **m5.** Library-assisted code channel (numpy/scipy) — the channel deployed loops actually permit — unmeasured (§2.1, §3.7). The code-channel conclusion "the ceiling is a property of the math-only channel" is carefully scoped, but the abstract's "Delegating construction to an executed program does not escape it" drops the "math-only" qualifier. Restore it.

## 4. STATISTICAL RIGOR

- **Sample sizes**: per-cell valid $n$ ranges 2–20. The mode-identity claim at $N$=17/35/37 rests on $n$=4 valid each (§3.2 table); the paper says so for P5 but not for 17/37 in the table itself. Add per-cell CIs or a footnote.
- **CIs**: given for arm MU, arm V, rectangle, faithfulness — good. Missing for the §3.2 modal frequencies and the CC/CC2/CCS anchor rates.
- **Multiplicity**: within-arm Holm applied where registered (§6.4); across arms explicitly none (§9). The pooled "3/147" and "0/115" are descriptive pools over separately registered arms — labeled as such, acceptable, but see C9's selection issue.
- **Gameable verdict rules**: (i) GM3 pooled bar (B1); (ii) GM3's cell-level bar of 5/5 scoreable cells with falsifier at ≥4 failures creates a 2–3-miss dead zone where neither fires — exactly what happened; (iii) arm V's ≥50% point-estimate bar at tiny $n$; (iv) CH's valid-conditioned metric (survivorship, disclosed and decomposed — handled well); (v) opus de-registration (M2). The paper flags each; the fix is to stop printing the registered verdict labels ("HELD", "TRANSFERS") without their decompositions attached.
- **Power**: arm MU registered a power analysis (0.83) — the only arm that did. Arm T's P-T1 needed "several hundred samples per arm" (§6.2) and was run at 60/arm; the paper correctly reports this as a failure to detect. Arm V at 5 samples/cell is exploratory in all but label.
- **Preregistration logic**: genuinely strong — commits precede sampling, falsifiers pre-stated with consequences, deviations tabled. The residual risks are the tie-convention layer (§6.3), the unregistered $N$=43 hash, and the post-hoc "not evaluable" move (M2).

## 5. INTERNAL CONSISTENCY

1. **"0/21" (§3.6)** — untraceable; contradicts 2/23 and 2/57 (§3.3). Blocking-level numeric error.
2. **"180 of 180" attached to arm MU (§3.5)** vs. 135 invocations; 180 is MU+CH (§6.1).
3. **78% vs. 83% ladder headline** — Contribution 2 and §5's opening quote the unmatched figure; Table 2's footnote mandates the matched one.
4. **Abstract "every tested $N$"** vs. Table M (3 disconfirmations) and GM3 (3 cell-level misses).
5. **Abstract "30 of 31"** vs. Table CH's 31/31 attempting, 30 misplaced + 1 unevaluable.
6. **Build notes vs. body**: the header comment says "S3.6+S3.7 merged into one S3.6 ... all S3.7 cross-refs now S3.6," but the body retains a separate §3.7 with §3.7 cross-references working. The note is stale; more importantly, none of this revision machinery belongs in a submission.
7. **Figure 1 caption** lists four worst-in-zone penalties; §1.1 lists five (omits 4.66% at $N$=57).
8. **GM2 "118/140 parseable" (§8) vs. GM3 table's 80 valid** — parseable ≠ valid; a one-line reconciliation would prevent misreading.
9. Terminology is otherwise disciplined ("recipe family"/"template"/"anchor" defined in §2.2 and used consistently; the notation table in §2.4 works).

## 6. WRITING AND STRUCTURE

- **Strip all revision history from the manuscript body**: "(Revision 3, 2026-08-17.)" after `\maketitle`; "revision 1's abstract claimed" (§3.2); "Two external reviews of this revision observed" (§3.4); "pressed by the council review of this revision" (§3.5); "Citation errors in revision 1 are corrected here" (§7); "corrections relative to the reviewed draft" (§9); all of Appendix C. This is correspondence with reviewers, not paper text. It currently makes the paper read as an internal lab log and will confuse every fresh reader.
- **§6.5**: the nine verbatim excluded-claim examples belong in an appendix; the section is otherwise the right length.
- **§9** is a 1,000-word bullet list mixing registration, provenance corrections, AI-use disclosure, internal QA, and the stopping rule. Split into a Reproducibility statement, a Deviations pointer (Appendix B already exists), and an AI-use paragraph.
- **§3.6 is overloaded**: two instruments, four tables' worth of content, and the gemma-pair discussion in one subsection. Split GM3 and arm V.
- **§1's second paragraph** (the discovery-systems scoreboard with five decimal-figure citations) is scoreboard trivia; compress to two sentences and move figures to §7.
- **The arms-index table (§3 opening)** is excellent — keep, and add a column for corpus size per arm.
- **"the companion paper's protocol" (§3.6, arm V)** — an unresolvable cross-reference to an unseen document. Either summarize the protocol inline or cite it as a released artifact.
- Readers get lost at §3.6's GM3 decomposition ("The registered metric pools all cells, and the pass rides on that") — this is the single most important caveat in the paper and is buried mid-paragraph; promote it to the subsection's first verdict sentence.

## 7. MISSING BASELINES / RELATED WORK

- **Classical circle-packing literature**: the paper compares against an LLM-systems scoreboard and a private bound table, but never engages the classical sum-of-radii packing literature (equal-circle packing optima, Packomania-style compendia, constructive bounds). A classical-solver baseline (even a packaged NLP/SLP solver at these $N$) would contextualize both the recipe family's deficit and the Sonnet escape at 2.75.
- **Simple-baseline proposers**: the paper cites Gideoni et al. and Berthold et al. on baselines matching LLM discovery claims but runs none. A trivial baseline — "emit round(√N) grid" written in 5 lines — reproduces the anchor by construction; the paper's actual contribution is that the *model* matches it, which should be stated against that baseline explicitly.
- **Contamination-detection methodology** (canary literature, held-out-$N$ design) is unengaged despite B2.
- **Sampling-diversity / mode-collapse in RLHF'd models** beyond the cited Verbalized Sampling and Artificial Hivemind — e.g., the self-consistency and decoding-temperature literature — bears directly on the "modal output" framing under unpinned parameters.
- **Library-assisted code channel** (numpy/scipy) is the missing experimental baseline, acknowledged (§2.1, §3.7) but material to the loop-relevance claim.

## 8. TOP 10 CONCRETE EDITS (priority order)

1. Rescope the abstract's "at every tested $N$" to "at all seven $N$ of the original square arm" and add "math-only" before "executed program."
2. Correct the abstract's "30 of 31" to "all 31 invalid attempts fail to build it (30 by misplaced fillers)."
3. Source or correct the "0/21" figure in §3.6.
4. Fix "180 of 180" in §3.5 to "135 of 135 (arm MU); 180 with arm CH."
5. In Table CV, replace GM3's verdict "pooled HELD" with "pooled bar met; discriminating-cell rate 25.6% below bar," and propagate to §5 and §8.
6. Replace Contribution 2's "78% → 100% → 13%" with the matched-cell "83% → 100% → 13%" per Table 2's own footnote.
7. Delete all revision-history sentences (§3.2, §3.4, §3.5, §7, Appendix C) and the "(Revision 3...)" line.
8. Add per-cell Wilson CIs (or an $n$ footnote) to the §3.2 modal-frequency table and the §3.7 CC/CC2/CCS tables.
9. Release or remove the opus_alias latency/token-count paragraph in §5.
10. Add a contamination paragraph to §8 committing to (or reporting) canary/held-out-$N$ tests, and add a URL/DOI for the released ledgers and scripts in §9.

## 9. RECOMMENDATION: **Major revision**

This is a genuinely interesting paper that would find TMLR readers: a closed-form, preregistered point prediction of an individual LLM output value, tested with exact evaluation, honest falsifiers, and a deviations table most venues never see. The core findings — mode-ceiling anchoring in the weak tier, dissolution under parent conditioning, the choice/execution decomposition from arms CH and MU, and the code-channel ceiling — are well supported and well scoped. It is not acceptable in its current form for four reasons. First, the abstract overclaims relative to the paper's own tables ("every tested $N$," "30 of 31," unqualified "executed program"), which is disqualifying at TMLR where claims must match evidence exactly. Second, two registered verdict labels are misleading as printed: GM3's "HELD" passes only on non-discriminating cells its own §3.2 convention excludes elsewhere, and arm V's "TRANSFERS" rests on point estimates whose CIs include the bar. Third, the contamination confound is unprobed while the fitted cells are the literature's canonical ones, leaving open that the "law" is partly a description of trained-on instances. Fourth, the manuscript carries its revision history, reviewer correspondence, and build notes in the body, which no fresh reader should have to parse. None of these requires new science except the contamination check and ideally a same-instrument gemma pair; all are implementable in one revision cycle. I would expect to accept a revision that makes edits 1–10 and reports the held-out-$N$ probe.