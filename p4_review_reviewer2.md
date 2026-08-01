# Review — Reviewer 2

**Submission:** *"[Circle-packing anchoring paper]" (paper1_draft.md)*
**Reviewer stance:** methods / evaluation-integrity.
**Basis:** the submitted draft, plus independent recomputation from `arm_f_candidates.jsonl`,
`arm_g_candidates.jsonl`, `arm_t_preregistration.txt`, `arm_t_analysis.py`,
`n_sweep_forecast.json`, and the three rendered figures. I did not consult author-side notes.

**Summary of stance.** The preregistration discipline, the retained negative result in §3.4, and
the decision to lead §5 with a null are all above the norm for this venue, and I want to say so
before the rest. But when I recomputed the paper's numbers from its own released ledger, several
headline figures did not reproduce, two figures reproduce only under a different denominator than
the one the abstract compares against, and the released provenance metadata contradicts two
load-bearing claims (the tier ladder and preregistration-before-sampling). The flagship
"intervention" result is one cell of three, uncorrected, and smaller than the control arm's own
between-batch drift. I detail these below.

Throughout, "the ledger" = `arm_f_candidates.jsonl` (215 rows) and `arm_g_candidates.jsonl`
(16 rows) as submitted.

---

## MAJOR

**1. [MAJOR] §2.1 vs Abstract — the paper's own scope condition severs its external-validity claim.**
The abstract closes: "Our results characterize the proposal distribution that LLM-driven discovery
systems sample from." §2.1 states that the prompt "forbids writing or executing code" and — in the
authors' own words — "Given a code channel the model delegates to an optimizer and the distribution
reflects the optimizer." Every system named in §1 and §7.1 (FunSearch, AlphaEvolve, ShinkaEvolve,
HELIX, GigaEvo, AdaEvolve) operates *through* a code channel. By the paper's own account, then, the
distribution measured here is precisely not the distribution those systems sample from; it is the
distribution obtained after removing the mechanism those systems rely on. Everything downstream is
still interesting as a study of unaided constructive reasoning, but the load-bearing bridge to the
discovery literature — the reason §1 argues the benchmark choice is "strategic" — does not hold.
*Would satisfy me:* either (a) run a code-enabled arm and show the anchoring survives it, or (b)
retitle and reframe the contribution as being about code-free constructive proposal, and delete the
claim that this characterizes what discovery loops sample from. (b) is cheap and honest; I would
accept it.

**2. [MAJOR] Abstract vs §1 "Non-claim guard" — the abstract makes exactly the claim §1 forbids.**
§1 states: "We make no claim about mechanism inside the weights — no assertion that a template is
stored, retrieved, or represented in any particular way." The abstract says models "**recall** a
single grid-with-corner-fillers template" and concludes they are "not a searcher, but a **template
memorizer**." *Recall* and *memorizer* are storage-and-retrieval claims about the weights. A
non-claim guard that the abstract violates is not a guard; it is a hedge held in reserve for
reviewers. This matters because the mechanism-free reading and the memorization reading have
different implications and different required controls (see finding 16).
*Would satisfy me:* rewrite the abstract in the vocabulary §1 commits to ("emits", "concentrates
on", "the proposal distribution is a point mass on"), or drop the guard and defend memorization
with a contamination control.

**3. [MAJOR] Abstract & §4 — the "71%" in the headline inversion does not reproduce at any tolerance.**
The abstract and Contribution 2 report "71% → 100% → 13%" and §4 states "Across the 45 bare
invocations logged in the arm-F ledger … 32 were geometrically valid (71%)." Recomputing the
pre-scaling 45-sample bare subset from the ledger, I get **35/45 valid at the 1e-6 primary
tolerance (78%)** and **29/45 at the 1e-9 tolerance (64%)**. 32 is neither. The full bare ledger is
69/85 (81%). I could not construct any subset or tolerance yielding 32/45.
Separately, the three tiers are compared on **mismatched denominators**: Haiku's 71% spans seven
values of N, while Sonnet and opus_alias span three. On the *matched* cells N ∈ {13,21,31} the
ledger gives **50/60 (83%) → 30/30 (100%) → 4/30 (13%)**. §4 acknowledges the asymmetry in one
sentence at the end and then reports the mismatched numbers in the abstract anyway. The claimed
inversion shrinks from a 29-point rise to a 17-point rise once matched. And Sonnet's "100%" is
27/30 (90%) at 1e-9, so the monotonicity of the first leg is tolerance-dependent.
*Would satisfy me:* report the matched-cell figures in the abstract, at both tolerances, and
explain the 32 or correct it.

**4. [MAJOR] §3.2 / Table 1 vs §5 / Table 3 — two data vintages, incompatible statistics for the same samples.**
§3.2 reports the bare arm at discriminating cells as "18 of 23 valid invocations landed on the
predicted construction," rival "2 in 23." That reproduces exactly — but only on the *pre-scaling*
45-sample snapshot. §5 reports the bare arm at N ∈ {13,21,31} as 35/50 on-prediction from the full
215-row ledger. These are overlapping samples of the same arm at overlapping cells, reported at
78% in one section and 70% in another. On the full ledger, §3.2's cells give **41/57 (72%)**, and
Table 1's footer figure "combined 2/34" becomes 2/68. The paper never states that Table 1 and
Table 3 are computed on different corpora.
*Would satisfy me:* regenerate every table from the final ledger, in one pass, and say so.

**5. [MAJOR] §5, P-T3 — the flagship result is one cell of three, and no multiple-comparison correction appears anywhere in the paper.**
Recomputing the pooled test I reproduce the paper exactly: 46/53 vs 35/50, one-sided Fisher
p = 0.0325. Decomposed by cell, however:

| N | trace_v2 on-pred | bare on-pred | one-sided Fisher p |
|---|---|---|---|
| 13 | 16/18 (89%) | 10/18 (56%) | 0.030 |
| 21 | 16/18 (89%) | 12/15 (80%) | 0.41 |
| 31 | 14/17 (82%) | 13/17 (76%) | 0.50 |

The pooled effect is N = 13 and nothing else. Four predictions were registered (P-T1…P-T4);
Bonferroni over those alone gives α = 0.0125, which p = 0.0325 fails. The two-sided Fisher p is
**0.0537**. The strings "Bonferroni", "multiplicity", "multiple compar", "FDR", "correction",
"confidence interval", "effect size" and "power" appear zero times in the manuscript. The paper
calls this an "intervention" and puts it in the abstract, in Contribution 3, and in §7.4 as the
differentiator against prior work.
*Would satisfy me:* report per-cell results in the body, state the sidedness in the abstract,
apply and report a correction over the registered family, and give a CI on the difference
(mine: roughly [+1, +32] points). If the claim survives only pooled and only one-sided and only
uncorrected, say "suggestive" and stop calling it an intervention.

**6. [MAJOR] §5 — batch confound: the bare arm's own drift is larger than the reported effect.**
`arm_t_preregistration.txt` specifies that the bare arm *pools* pre-existing arm-F samples with
newly collected ones ("new sample ids s6+ at N=13/31, s11+ at N=21"). Splitting the bare arm on
that boundary, with no intervention applied to either half:

| N | bare on-pred, pre-existing ids | bare on-pred, newly collected ids |
|---|---|---|
| 13 | 3/4 (75%) | 7/14 (50%) |
| 21 | 4/7 (57%) | 8/8 (100%) |
| 31 | 5/5 (100%) | 8/12 (67%) |

Swings of 25 and 43 points within a single arm, in opposite directions, dwarf the 17-point effect
attributed to the method-line request. Consequently the significance of P-T3 depends entirely on
which bare batch you compare against: trace_v2 vs **pre-existing bare only, p = 0.22**; trace_v2 vs
**newly collected bare only, p = 0.031**. Given that §8 discloses decoding parameters are unpinned,
that trace_v2 and bare were not interleaved, and that a third of the control arm predates the
preregistration, an unmodelled batch/runtime effect is a live alternative explanation for the
entire finding and is never addressed.
*Would satisfy me:* re-collect both arms interleaved within a single session, or at minimum report
the arm as a mixed model with batch as a factor and show the effect survives.

**7. [MAJOR] §5 / arm_t_preregistration.txt — trace_v2 is not the minimal diff it is claimed to be, and the residual confound is visible in the data.**
The prereg discloses that trace_v2 differs from bare by "ONE inserted METHOD line, and 'After the
METHOD line, ' prepended to the output line ('no other text' → 'no other text after the list')."
That second change strengthens the output-format instruction. In the ledger, the bare arm has
**6 parse failures** (`literal_eval_failed`, at N = 21, 31, 35, 37, 43) and the trace arm has
**zero**. Parse failures are scored as invalid and enter the validity denominator. So P-T1's
"direction held at all three cells" is at least partly a format-compliance effect from the very
rewording the authors identified as the pilot's confound and believed they had removed. The paper
diagnoses this confound in the pilot and then reproduces a weaker version of it.
*Would satisfy me:* an arm whose only difference from bare is the inserted METHOD line, with the
output-format sentence held byte-identical; and report validity separately for parse failure vs
geometric failure everywhere.

**8. [MAJOR] Abstract & §1 Contribution 3 — a null result is reported as an affirmative claim of no effect.**
Abstract: "while leaving validity unchanged." Contribution 3: "while leaving validity
statistically unchanged." §5 correctly says the opposite: the direction held at all three cells,
p = 0.30, and "we do not conclude that the pilot's validity effect was purely the bundled
rewording, only that it is not detectable at 20 per arm per cell." The observed rates are 83% vs
88%; detecting a difference that size at 80% power needs several hundred samples per arm. The body
is right and the abstract is wrong.
*Would satisfy me:* "no detectable change in validity (p = 0.30, n = 60/arm; the study is not
powered to exclude an effect of the observed size)", or an actual equivalence test.

**9. [MAJOR] §9 / ledger — released provenance metadata contradicts both the tier ladder and preregistration-before-sampling.**
Every one of the 215 rows in `arm_f_candidates.jsonl` carries
`"proposer_alias": "haiku"` and `"proposer_dated_id_on_run_date": "claude-haiku-4-5-20251001"` —
including all 30 `sonnet_bare` rows and all 30 `opus_alias` rows. The tiers are distinguished only
by the free-text `arm` string. §4 is a headline contribution and the released artifact contains no
provenance evidence that three different proposers were ever queried.
Every one of the 215 rows also carries `"run_date": "2026-07-30"` — including the 60 `trace_v2`
rows, whose preregistration (`arm_t_preregistration.txt`) is dated **2026-08-01** and opens
"Written 2026-08-01, BEFORE any arm-T proposal was sampled." Either the trace samples were
collected two days before the document that claims to precede them, or `run_date` is boilerplate
stamped uniformly across the file. In the first case §9's central claim is false; in the second
case §9's central claim is unverifiable from the artifact that is supposed to establish it. Either
way, "the hashes were recorded *before* any sampling occurred" cannot currently be checked, which
is the entire point of recording them.
*Would satisfy me:* per-row collection timestamps and per-row model identifiers, or a signed
external timestamp (OSF, OpenTimestamps, a git commit hash in a public repo) on each
preregistration file predating the first sample of the corresponding arm.

**10. [MAJOR] §4 — the opus_alias serving-path evidence exists in no released artifact.**
§4 rests the alias-provenance caveat on two "consistent, not intermittent" anomalies: completion
times of "2.8–9 seconds across all 30 invocations, against 75–250 s for Haiku and 150–1170 s for
Sonnet," and "the reported token count was uniform at 49,906 across the first 20 completions." The
ledger has no latency field and no token field; the full key set is
{arm, circles, claim_hexlike, claimed_dims, distinct_radii, exact_matches, faithful,
invalid_reason, invalid_reason_strict_1e9, method_claim, n, observed_cols, observed_rows,
parse_error, prompt_sha256, proposer_alias, proposer_dated_id_on_run_date, raw_len, raw_output,
reconstructed, run_date, sample_id, sampling_params, sampling_params_note, structure,
sum_of_radii, valid, valid_strict_1e9, value_matches}. §8 makes this confound a formal limitation
and §4 makes it "load-bearing," yet the only evidence for it is unreleased.
*Would satisfy me:* release per-invocation latency and token counts, or delete the two anomalies
and state the alias caveat as a design limitation without the empirical dressing.

**11. [MAJOR] §4 — post-hoc de-registration in the one arm that disconfirmed.**
Three of four registered predictions for the top tier (P-O1, P-O2, P-O4) are declared "not
evaluable" after the fact, on the reasoning that "a validity collapse of this size makes a tier
comparison on on-prediction rates dishonest rather than merely noisy," and §4 states plainly that
"The registered disconfirmation — regression toward the trap — did not occur." Meanwhile P-T3, at
p = 0.0325 uncorrected, is promoted to the abstract. Selectively voiding registered predictions in
the arm that failed, while headlining the one that passed, converts preregistration from a
constraint into a presentation device. It may well be the right scientific call here; it is not a
call that can be made after seeing the data without recording it as a deviation.
*Would satisfy me:* a deviations table listing every registered prediction, its registered
evaluation rule, whether it was evaluated as registered, and — if not — the post-hoc reason.

**12. [MAJOR] §4 — the submission ships an unresolved contradiction from the authors' own log, and a headline number depends on how it was resolved.**
An HTML comment retained in the manuscript reads: *"CONFLICT: STATE.md §8 states the opus_alias arm
is 'excluded from the tier ladder'; §8b, written after the arm completed, tabulates it directly
against the other two tiers … Following the later entry: included in Table 2."* The abstract's
"13%" and the entire third leg of the inversion exist only because a decision to exclude the arm
was reversed after the arm's results were known. That reversal is disclosed to reviewers only via a
comment addressed to the authors themselves, referencing a document not submitted.
*Would satisfy me:* move this into the body as an explicit analysis-decision disclosure, with the
inversion reported both ways.

**13. [MAJOR] §3.2 — five invocations excluded, exclusion rule unregistered, excluded records not in the ledger, stated impact unreconcilable.**
"Five invocations were rejected by the runtime's 20-subagent concurrency cap *before reaching a
model*, and scoring them invalid would have understated validity by 17%." The exclusion is not in
any preregistration I was given; the five records do not appear in the ledger in any form (all 215
rows have `reconstructed: false` and none carry a cap-rejection marker); and I cannot reconstruct
"17%" from any plausible denominator (35/45 → 35/50 is 8 points / 10% relative). A 5-record
exclusion on a ~30-record base, decided after collection, applied to the arm that supplies the
paper's validity headline, is exactly the degree of freedom preregistration exists to close.
*Would satisfy me:* the excluded records in the ledger with an explicit `excluded_reason` field,
a preregistered or at minimum date-stamped exclusion rule, and the arithmetic behind 17%.

**14. [MAJOR] §3.1, §4 — the registered 2×10⁻³ matching window cannot resolve the distinctions the paper draws with it.**
§4's most-quoted exemplar is the Sonnet N = 31 sample summing to 2.7499999991, described as being
"above 2.7485281, the best value the recipe family reaches at that N" and as "the only sample in
the study to leave the recipe family upward." The difference is 0.00147, which is **inside** the
registered 2e-3 window. Running the paper's own scorer, that sample is counted as a rival-argmax
hit. So one sample is simultaneously (a) tallied into "It reaches the higher-scoring rival 6 times
in 30" and (b) narrated as the unique escape from the family. The honest count is 5 rival + 1
ambiguous. More generally, a window of 2e-3 sits above several of the value differences the paper
treats as qualitative distinctions, while the abstract advertises agreement "to seven decimal
places."
*Would satisfy me:* a second, tight window (say 1e-6) reported alongside, with every categorical
claim ("escaped the family", "reached the rival") made at the tight window only.

**15. [MAJOR] Abstract — "predicts the exact sum-of-radii the model will emit" is a ~46% hit rate.**
Two distinct precisions are conflated. The formula agrees with the LP oracle to 1e-9 across 83
configurations — that is arithmetic, and it is verified. The *model* agrees with the formula at
the following rates, from the ledger, at discriminating cells, excluding the trace intervention
arm: bare 41/57 (72%), Sonnet 1/30 (3%), opus_alias 0/4 (0%), rectangle 5/11 (45%) —
**47/102 = 46% overall**. Even the paper's own §4 concedes the rule is "a weak-tier law." The
abstract's "models do not search: they recall a single … template" and "predicts the exact
sum-of-radii the model will emit, to seven decimal places" describe neither the pooled rate nor the
per-tier picture the body reports.
*Would satisfy me:* the pooled 46% figure in the abstract, with the per-tier breakdown, and the
seven-decimal claim explicitly scoped to formula-vs-LP rather than formula-vs-model.

**16. [MAJOR] Throughout — contamination and the arithmetic-tractability alternative are never tested.**
"Contamina*" appears once in the entire manuscript, in §4, as the concessive clause "the canonical,
plausibly contaminated cell N = 26." No contamination probe is run: no canary-string test, no
comparison against N values absent from the literature, no perturbed-container test that preserves
difficulty while destroying lexical overlap with training text. Meanwhile a second, simpler
explanation goes unaddressed: under an explicit "do not write or execute code — construct the
packing by reasoning alone" constraint, a k×k grid at r = 1/(2k) is the only construction whose
coordinates a model can emit from mental arithmetic without error accumulation, and k = round(√N)
is the arithmetically nearest such grid. That predicts every observation in §2–§3 without any
appeal to memorization, and it predicts the tier inversion in §4 too (the more capable tier
attempts constructions whose coordinates it cannot compute by hand, and overlaps — which is
precisely the reported failure mode: 24 overlap + 2 nonpositive_radius out of 26 opus_alias
failures). The paper's title claim and the abstract's "memorizer" both require ruling this out.
*Would satisfy me:* the cheap decisive experiment — hand the model the recipe family explicitly
(state V(k,m), state the admissible k) and ask it to *choose* k. If it picks argmax, the
memorization reading dies and the tractability reading stands. This is one arm and it is the
single most valuable addition the paper could make.

**17. [MAJOR] §3.3 — the rectangle transfer is described as confirmation at a 45% hit rate, with 6 of 11 valid samples uncharacterized.**
"5 of 11 valid proposals landed on the predicted value and 0 of 11 reached the rival" reproduces
exactly. But the paper draws from it "Nearest-template anchoring is not an artifact of the
one-parameter square case," and the abstract escalates to "confirmed them out of sample in two
containers." The majority of valid rectangle samples — 6 of 11 — landed on **neither** the
prediction nor the rival (values 3.45, 3.5 at N = 19/a = 3; 2.5, 2.5, 3.0, 3.151875 at
N = 25/a = 2). Only one of the six is discussed. A rule that fires on 45% of out-of-sample
proposals and whose misses are unmodelled is not confirmed; it is partially supported. Note also
that two of the "hits" are 3.1666666667 and 3.16666673 — the latter agreeing to six decimals, not
seven. Sample sizes here are 4 and 7 valid.
*Would satisfy me:* characterize all 11, drop "confirmed" for something calibrated, and either
raise n substantially or present §3.3 as a pilot.

**18. [MAJOR] §9 / arm_g ledger — the rectangle arm has no recorded provenance at all.**
§9 states without qualification: "Every prompt was hashed with SHA-256 and the hashes were recorded
*before* any sampling occurred." `arm_g_candidates.jsonl` contains no `prompt_sha256`, no
`run_date`, no proposer alias, and no sampling-params field — its full key set is
{a, circles, cols, distinct_radii, invalid_reason, max_radius, n, parse_error, raw_output,
reconstructed, rows, sample_id, sum_of_radii, valid}. The rectangle transfer is the paper's
strongest claim to genuine out-of-sample confirmation, and it is the arm with the least provenance.
*Would satisfy me:* the rectangle prompts and their hashes, with the same fields as arm F.

---

## MINOR

**19. [MINOR] §2.4 — "hits exactly zero at the top of each zone" is false, and ~18% of "trap" N carry no penalty.**
Computing the gap across every trap zone in the swept range: it is zero at N = 14, 15, 35, 48 (and
63, outside the sweep) but **0.589% at N = 24**, the top of the k = 5 zone. So the stated general
rule fails at one of the four zones fully inside the sweep. More consequentially, N = 14 and N = 15
sit inside the [13,15] "trap zone" with a gap of exactly zero — meaning 4 of the 22 trap-zone N in
range cost nothing, while the abstract describes trap zones as "N where the rule provably costs
value."
*Would satisfy me:* correct the sentence, and define trap zones by penalty rather than by branch,
or state explicitly that the branch label and the penalty are not coextensive.

**20. [MINOR] Figure 1 as rendered does not match its own caption, and the record comparison covers only N = 10–30.**
The caption instructs: label each band "with its worst-in-zone percentage (8.51%, 7.03%, 6.01%,
5.25%)" and "Mark N = 35 and N = 48, where the gap closes to zero." The rendered `fig1_trapzones.png`
has neither the percentage labels nor the marks. Separately, `n_sweep_forecast.json` carries
`published_best_known` for exactly 21 rows, N = 10…30, which is why the dotted curve terminates
mid-plot. §2.4's "The family is also never competitive with the record" and §9's gate that "aborts
… on any predicted value exceeding a published lower bound" are therefore unchecked for N = 31–60 —
which contains three of the five trap zones and four of the seven square test cells (31, 35, 37, 43).
*Would satisfy me:* regenerate the figure to its caption; scope the record claim to N ≤ 30 or
extend the bound table.

**21. [MINOR] §7.1 — the record claim is contradicted by the paper's own evidence file.**
§7.1: "the published best-known lower bounds that §2.1 scores against sit above all of them." The
bound stored for N = 26 in `n_sweep_forecast.json` is **2.63598**, which is below ShinkaEvolve's
2.635983283 and HELIX's 2.63598308 as cited three sentences earlier. Probably a truncation in the
bound table, but as written the sentence is false against the submitted artifact, and the same
table is what the abort gate checks against.

**22. [MINOR] Figure 2 — exemplars are cherry-picked, unlabelled, and not matched on N.**
The three panels compare Haiku at N = 21, Sonnet at N = 31, and opus_alias at what appears to be
N = 13. The figure is the visual argument for "three attractor families," and it varies tier and
cell simultaneously. No sample identifiers are given, so no panel can be traced to a ledger row.
The opus_alias panel renders every circle in the overlap colour, which reads as "all circles
overlap" rather than "this packing contains overlaps."
*Would satisfy me:* one N, three tiers, sample ids in the caption, and overlap highlighting
restricted to the offending pairs.

**23. [MINOR] §4 — three further counts do not reconcile with the ledger.**
(a) "29/30 multi-radius, against a same-metric Haiku baseline of 13/35" — the ledger gives Haiku
bare multi-radius 24/69 across all valid samples, or 15/50 at the matched cells; 13/35 is neither.
(b) "something no Haiku sample did in 101 invocations" — the ledger contains 155 Haiku-arm rows
(85 bare + 70 trace). (c) "two bare samples emitted fraction literals … and failed the §A.5 parser"
(§5, echoed in §3.2) — the ledger records 6 bare parse failures. Individually small; collectively
they reinforce finding 4, that the prose was written against an earlier corpus.

**24. [MINOR] §2.3 — "Zero free parameters" understates a discrete model-selection step, and 3 binary anchors do not identify much.**
Four candidate rules were scored against three anchors and one survived 3/3 (`floor` 2/3,
`argmax` 2/3, `ceil` 1/3). Under a null where each candidate matches each anchor with probability
½, the chance that *some* candidate among four goes 3/3 is roughly 40%. The paper's own
`n_sweep_forecast.json` carries the honest caveat ("the rule is the unique survivor of four
candidates, not an independently confirmed law") and §2.3 restates it well — but "Zero free
parameters" in the same block is misleading, since selecting among four candidates on three points
*is* fitting one discrete parameter. Relatedly, §2.2 lists five reproduced anchors including
V(5,0) = 2.500 (N = 25), while §2.3/§3.2 and the JSON both say the rule was fitted on N = 23/26/27
only; N = 25 is used as evidence but not counted as fitted-on.

**25. [MINOR] §6 — all failures reclassified as scorer error, no symmetric audit of the successes, and the CI contains the registered threshold.**
"The three mismatches are all the same case … The scorer penalizes a claim that is, in fact,
accurate. The conservative scorer therefore undercounts matches, and 93% should be read as a
floor." Every one of the three failures is manually reclassified as a scorer artifact; none of the
38 matches is audited for the converse error (a vague claim that the coarse signature accepted).
Reclassifying only the misses guarantees a floor. Additionally, 12 of the 53 valid trace_v2 samples
produced claims with no numeric content and were dropped as unscoreable — 23% of the arm, and
plausibly the vaguest claims, i.e. exactly the ones a faithfulness metric should penalise. Finally
38/41 = 92.7% with a Wilson 95% CI of roughly [80%, 97%]: the registered 90% threshold lies inside
the interval, so "clearing the registered threshold" is a coin-flip at this n.
*Would satisfy me:* blind manual adjudication of all 53, with the unscoreable class reported as a
third outcome rather than dropped; and a CI on the rate.

**26. [MINOR] §6 opening overclaims relative to §6's own closing paragraph.**
"This is the check that the chain-of-thought faithfulness literature cannot run." The final
paragraph then concedes the check "verifies that the description matches the artifact, not that it
matches whatever internal process produced the artifact." Those are different objects: the CoT
literature asks whether the stated process caused the answer; this asks whether a stated *dimension*
matches an emitted *artifact*. For a model already emitting grids, "5x5 grid" matching a 5×5 grid
is close to a self-consistency check. The closing paragraph is the correct one; the opening and the
abstract's "verifiable against output coordinates (93% faithful)" both read as more than that.

**27. [MINOR] Missing materials: no tables, no figures in-text, no appendix.**
Tables 1–3 and Figures 1–3 appear only as bracketed generation instructions. "Appendix A.5" is
cited twice — for the verbatim prompt (§2.1) and the parser (§5) — and no appendix is included. The
verbatim prompt is the single most important artifact in a paper whose thesis is that a specific
prompt produces a specific distribution; a reviewer should not have to reconstruct it from a
preregistration file for a different arm.

**28. [MINOR] Citation hygiene.** Roughly 35 references are given as bare arXiv numerals with no
author, title, or venue (e.g. "2603.07642", "2607.18867", "2606.05408"). Several are load-bearing
— 2605.29268 is used in §7.2 to argue the anchoring is not a code-channel artifact, and
2607.18867 is the concurrent-work comparison in §1. These cannot be checked at review time.

**29. [MINOR] Author-side comments retained in the submission.** Four HTML comments survive in the
draft (`<!-- NOTE (not a conflict) … -->`, `<!-- VERIFIED 2026-08-01 recount … -->`, two
`<!-- CONFLICT … -->`), plus a sourcing block citing `STATE.md §§v8–v9`. They reference an internal
log not submitted. Two of them (findings 12 and the p = 0.033/0.0325 discrepancy) disclose real
analysis decisions that belong in the body, not in comments.

---

## NIT

**30. [NIT] Abstract, "Across hundreds of zero-shot invocations."** The corpus is 215 + 16 = 231
invocations across all arms, tiers and containers. Technically plural; reads as more.

**31. [NIT] p = 0.033 vs p = 0.0325.** The abstract rounds, §1 and §5 do not. The authors noticed
(there is a comment saying so) and fixed the body but not the abstract.

**32. [NIT] "The recipe is an attractor, not a ceiling."** This exact sentence closes both §3.3 and
§4, in both cases generalising from a single sample. Pick one.

**33. [NIT] §2.4's k = 8 zone.** The text gives [57,60], the formula gives [57,63], and the
reconciliation ("clipped by the sweep bound") lives only in an HTML comment. The comment itself
suggests putting it in the caption; do that.

---

## Recommendation

**Reject.**

The paper is unusually disciplined in places I normally have to fight for — a registered falsifier,
a retained negative result in §3.4, a null led with rather than buried — and I would like to see it
succeed, but three of its findings cannot be repaired by revision: a headline validity figure that
reproduces at no tolerance from the submitted ledger (finding 3), provenance metadata that records
every one of the 215 invocations as the same model on a date preceding one arm's own
preregistration (finding 9), and a flagship "intervention" that is one cell of three, uncorrected,
two-sided-nonsignificant, and smaller than the control arm's undiscussed between-batch drift
(findings 5–6). Each requires re-collection rather than rewriting, and the untested
arithmetic-tractability alternative (finding 16) means even clean data may not support the
memorization framing the abstract asserts.
