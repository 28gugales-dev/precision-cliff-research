# Citation audit — paper 1 (TMLR), SHARD A

Date: 2026-08-28. Manuscript Rev 4.12, branch `claude/new-papers-review-pa3ona`.

Scope: the 20 `references.bib` entries whose keys sort from
`abdelnabi2025hawthorneeffectreasoningmodels` through
`kaplan2020scalinglawsneurallanguage` inclusive. Every arXiv id was fetched
live from `arxiv.org/abs/<id>` (title, authors, subject, dates, comments,
withdrawal status); non-arXiv entries were fetched from the publisher or
official source. Where the abstract was not decisive the arXiv HTML full text
was fetched and grepped (`chen2026`, `jia2026`, `cemri2026`).

Every citation site was located with `grep` over `sec_*.tex` (long variant:
`sec_intro_task`, `sec_forecast_transfer`, `sec_tiers_elicitation`,
`sec_related_repro`, `sec_appendices`; short variant: `sec_short_*`). For all
20 keys in this shard the short-variant wording is materially identical to the
long variant — no shard-A key makes a different claim in the short paper. The
one exception in phrasing only: the long variant attributes the `N > 30`
coverage gap to `\S1.1`, the short variant to `Appendix C.2`; the claim is the
same.

## 1. Summary counts

| Metric | Count |
|---|---|
| Entries in shard | 20 |
| Identifiers verified (resolve to the cited record) | 20 / 20 |
| Withdrawn | 0 |
| Unreachable / UNVERIFIED | 0 |
| CONFIRMED | 16 |
| PLAUSIBLE | 3 |
| REFUTED | 1 |

## 2. Per-entry table

| bib key | identifier | resolves? | withdrawn? | verdict | note |
|---|---|---|---|---|---|
| abdelnabi2025hawthorneeffectreasoningmodels | arXiv 2505.14617 | yes | no | CONFIRMED | "The Hawthorne Effect in Reasoning Models: Evaluating and Steering Test Awareness", Abdelnabi & Salem, cs.CL, submitted 21 May 2025. Cited only in the "Related observer-effect and elicitation results" list — exactly what the paper is. |
| arcuschin2026chainofthoughtreasoningwildfaithful | arXiv 2503.08679 | yes | no | CONFIRMED | "Chain-of-Thought Reasoning In The Wild Is Not Always Faithful", v6 16 Jun 2026, comment: "Published at the 43rd International Conference on Machine Learning (ICML 2026)". Cited as the representative of the cluster that *estimates* faithfulness without observing the process — matches the method (paired "Is X bigger than Y?" questions, output-level rates up to 13%). Metadata nit: v1 is Mar 2025, bib says `year={2026}` (defensible via ICML 2026), and the ICML venue is not recorded in the entry. |
| balunovic2025mathconstructchallengingllmreasoning | arXiv 2502.10197 | yes | no | PLAUSIBLE | See Finding A-2. Identifier, title, authors, year all correct (v1 14 Feb 2025). |
| berthold2026outoftheboxglobaloptimizationpacking | arXiv 2605.04850 | yes | no | CONFIRMED | "Out-of-the-Box Global Optimization for Packing Problems", math.OC, 6 May 2026. Abstract: off-the-shelf global solvers (FICO Xpress, SCIP) "obtain numerous new incumbent solutions" on packing circles in squares, motivated explicitly by "recent LLM-driven discoveries". Independently corroborated: Friedman's page credits "Timo Berthold et al in January 2026" with the n=32 record. |
| boppana2026reasoningtheaterdisentanglingmodel | arXiv 2603.05488 | yes | no | PLAUSIBLE | See Finding A-3. |
| bradley2023qualitydiversityaifeedback | arXiv 2310.13032 | yes | no | CONFIRMED | "Quality-Diversity through AI Feedback" (QDAIF), v4 7 Dec 2023. Abstract: an EA that "applies LMs to both generate variation and evaluate the quality and diversity of candidate text" — i.e. an LM-self-reported diversity descriptor, which is precisely the QD-descriptor setting the manuscript says §6 bears on. The "most affected" ranking is the manuscript's own judgement, not a source claim. |
| carlini2021extracting | USENIX Security '21 | yes | n/a | CONFIRMED | Verified at usenix.org/conference/usenixsecurity21/presentation/carlini-extracting: title, all 12 authors and affiliations match the bib; venue "30th USENIX Security Symposium", 2021, correct. Cited as an extraction probe — abstract is a training-data extraction attack on GPT-2. |
| cemri2026adaevolveadaptivellmdriven | arXiv 2602.20133 | yes | no | CONFIRMED | "AdaEvolve: Adaptive LLM Driven Zeroth-Order Optimization", 23 Feb 2026. Full text (arXiv HTML) confirms the scoreboard entry: "reaching to a best-known score of 2.636 on the Circle Packing (N = 26)"; Table 1 best = 2.636, and the appendix gives 2.63598308 for circle packing (square) with the Gemini backbone. The manuscript's "AdaEvolve 2.636" is exact. |
| chen2026measuringgaphumanllm | arXiv 2607.01233 | yes | no | CONFIRMED | Every number in the manuscript sentence checked against the full text: 11,683 matched evaluation rows; "Only 12.1% of human opportunities are labeled as fragmentation or bridge opportunities, compared with 47.1 to 64.2% for the main LLMs"; human normalized entropy "above 0.92", model opportunity entropy "ranges from 0.550 to 0.758"; §4.4 "thinking mode moves the output distribution farther from the human reference". Minor: the source calls it thinking/reasoning mode (tested on 2 models), the manuscript calls it "chain-of-thought". |
| friedman_packing | erich-friedman.github.io/packing/cirRsqu/ | yes | n/a | REFUTED | See Findings A-1 (coverage) and A-4 (attribution). The N=26 value itself checks out: the page lists "26. Σ r = 2.63598+". |
| gideoni2026simplebaselinescompetitivecode | arXiv 2602.16805 | yes | no | CONFIRMED | "Simple Baselines are Competitive with Code Evolution", 18 Feb 2026. Abstract: "simple baselines match or exceed much more sophisticated methods in all three [domains]", one of which is "finding better mathematical bounds". Supports "recover much of the reported advantage". |
| golchin2024timetravel | ICLR 2024 (arXiv 2308.08493) | yes | no | CONFIRMED | arXiv comment: "Published at ICLR 2024 as a Spotlight paper"; OpenReview record confirms venue "ICLR 2024 spotlight" and the exact bib title. Cited as a contamination-detection probe — correct. |
| guo2024evoprompt | ICLR 2024 (arXiv 2309.08532) | yes | no | CONFIRMED | OpenReview record: title "Connecting Large Language Models with Evolutionary Algorithms Yields Powerful Prompt Optimizers", venue "ICLR 2024 poster" — bib title/venue/year all match. (The current arXiv v3 prepends "EvoPrompt:"; the bib uses the published ICLR title, which is correct.) Cited as establishing the LLM call as an EC operator over prompts — matches. |
| gurkan2026mutationvariationconvergencedynamics | arXiv 2606.05408 | yes | no | CONFIRMED | "Mutation Without Variation", 3 Jun 2026, GECCO '26 workshop. The nesting is now correct in the manuscript and matches the abstract verbatim: "in 87% of chains, over 93% of mutations revisit a previously seen structural form". Ledger item 26 is properly discharged. |
| herrmann2026indepthstudyllmcontributions | arXiv 2510.27353 | yes | no | CONFIRMED | "An In-depth Study of LLM Contributions to the Bin Packing Problem", v2 17 Jun 2026, comment: "Accepted for publication in ACM Transactions on Evolutionary Learning and Optimization" (bib's `doi=10.1145/3821574` is consistent with a TELO article). Abstract reassesses and deflates the FunSearch bin-packing discovery claim — correctly filed under proposer-contribution skepticism. Metadata nit: v1 is 31 Oct 2025; bib says `year={2026}` (defensible via the TELO version) and does not record the journal in a `journal`/`booktitle` field. |
| hoffmann2022trainingcomputeoptimallargelanguage | arXiv 2203.15556 | yes | no | CONFIRMED | "Training Compute-Optimal Large Language Models", 29 Mar 2022. Abstract: "We test this hypothesis by training a predicted compute-optimal model, Chinchilla" — exactly "publish a functional form then run the confirming instance". Also supports the §1 claim that prior work predicts *aggregate* metrics ahead of a run. |
| huang2026understandinganchoringeffectllm | arXiv 2505.15392 | yes | no | CONFIRMED | "Understanding the Anchoring Effect of LLM with Synthetic Data: Existence, Mechanism, and Potential Mitigations", v2 29 Mar 2026, "Accepted by the HCAIR workshop of ICLR 2026". Abstract treats anchoring as a general bias where "the mind relies heavily on the first information as anchors" — matches "treats anchoring as a general bias over initial information" (ledger item 24 discharged; the paper is cited by identifier and correctly characterised as *general* rather than numeric anchoring). Metadata nit: v1 is May 2025, bib says `year={2026}`. |
| jia2026hindsightbenchblackboxbehavioralaudit | arXiv 2607.18867 | yes | no | CONFIRMED | v2 10 Aug 2026. Full text supports "releases frozen preregistrations": "We release the panel, frozen preregistrations, per-model audit rows…" and "every frozen preregistration with SHA-256 hashes and freeze timestamps". Note the manuscript no longer says the *benchmark* freezes "under SHA-256" (ledger item 25) — the surviving wording is supported. The qualifier "of directional aggregate hypotheses" is a fair paraphrase: the carrier task is "macro hypothesis generation … eight structured hypothesis sketches with direction calls" and "the behavioral field is directional (bearish share)". |
| jiang2025artificialhivemindopenendedhomogeneity | arXiv 2510.22954 | yes | no | CONFIRMED | "Artificial Hivemind: The Open-Ended Homogeneity of Language Models (and Beyond)", 27 Oct 2025, NeurIPS 2025 D&B Oral. Abstract: 26K open-ended queries, intra-model repetition and inter-model homogeneity — supports "the same homogeneity across open-ended domains at survey scale". |
| kaplan2020scalinglawsneurallanguage | arXiv 2001.08361 | yes | no | PLAUSIBLE | See Finding A-5. Identifier, title, all 10 authors, year 2020 verified. |

## 3. FINDINGS REQUIRING ACTION

### A-1 (REFUTED) — `friedman_packing`: the published-bound table does **not** stop at N = 30

Manuscript, `sec_intro_task.tex` L116–124 (and `sec_short_appendix_moved.tex` L54–62):

> "Our bound table (`n_sweep_forecast.json`, transcribed from \citet{friedman_packing}) covers $N = 10\ldots30$ only … **Above $N = 30$ there is no bound table**, so both the deficit claim and the LP gate's ``never exceeds a published bound'' abort are unchecked there, covering three of five trap zones and four of our seven square cells."

and the Figure 1 caption, `sec_intro_task.tex` L127 (= `sec_short_appendix_moved.tex` L36):

> "(iii, dotted) published best-known values \citep{friedman_packing}, **terminating at $N = 30$ because the bound table stops there**."

Source, fetched 2026-08-28 from https://erich-friedman.github.io/packing/cirRsqu/ ("Circles in Squares … n circles with the largest possible sum of radii packed inside a unit square"), which now lists entries through n = 40:

> "31. Σ r = 2.889+ Found by David W. Cantrell in July 2011. **32. Σ r = 2.939+ Found by Timo Berthold et al in January 2026. 33. Σ r = 2.98728+ Found by Haowei Lin in July 2026.** … 40. Σ r = 3.29239+ Found by Haowei Lin in July 2026."

The cited source publishes best-known values for N = 31…40, i.e. it fully covers the `[31,35]` trap zone the manuscript says is unchecked. The gap is a property of the authors' own transcription (`n_sweep_forecast.json`), not of the cited source — but two sentences state it as a property of the published bounds, and the figure caption attributes the dotted curve's termination to the source ("because the bound table stops there").

**Suggested fix:** rewrite both sentences to attribute the gap to the transcription and to date it, e.g. "our transcription covers N = 10…30; the source has since been extended through N = 40 (accessed 2026-08-28), so the deficit and LP-gate checks above N = 30 are unrun in this work rather than uncheckable", and change the caption to "terminating at N = 30 because *our transcribed* bound table stops there". If the extension is easy to run, the stronger fix is to extend the table to N = 40 and close the `[31,35]` zone. Either way record the access date in the bib `note` (currently just "accessed 2026").

### A-2 (PLAUSIBLE) — `balunovic2025mathconstructchallengingllmreasoning` filed under proposer-contribution skepticism

Manuscript, `sec_related_repro.tex` L34–36 (identical in `sec_short_related_repro.tex` L36–39):

> "Converging skepticism about **what the proposer contributes** comes from ``Dictionaries, Not Darwin'' …, BehaveSim …, Strategy Diversity …, the bin-packing critiques … and **MathConstruct** \citep{balunovic2025mathconstructchallengingllmreasoning}."

Source (2502.10197 abstract): MathConstruct is "a new benchmark of 121 challenging problems sourced from various math competitions, which targets constructive proofs … State-of-the-art LLMs solve only 60% of MathConstruct problems." It is a benchmark-difficulty result about LLM mathematical reasoning; it says nothing about the contribution of an LLM *proposer* inside an evolutionary/discovery loop, which is what the other five citations in that list are about (they compare LLM-driven search against baselines or ablations). This is the ledger-18/21 failure mode in mild form — a paper recruited into an argument it does not itself make.

**What a human must check:** whether the full paper contains a search/loop-relevant result (e.g. an ablation of iterated proposal, or a discussion of construction-generation as discovery) that would justify the grouping. The abstract does not.

**Suggested fix:** either move MathConstruct out of the proposer-contribution list into a separate clause ("and, on the raw generative ceiling for constructive objects, MathConstruct \citep{...} reports SOTA LLMs solving only 60% of 121 competition construction problems" — which is directly relevant to this paper's execution-ceiling result), or drop it. The former is the better use: it corroborates §3's choice/execution dissociation.

### A-3 (PLAUSIBLE) — `boppana2026reasoningtheaterdisentanglingmodel` grouped under an unqualified "all report causal decoupling"

Manuscript, `sec_related_repro.tex` L49–52:

> "One cluster intervenes \emph{on trace content} and finds answers do not move --- Reasoning Theater \citep{boppana2026reasoningtheaterdisentanglingmodel}, Project Ariadne …, ``Beyond the Commitment Boundary'' … and ``The Chain Holds, the Answer Folds'' … **all report causal decoupling**."

Source (2603.05488 abstract) reports decoupling as *difficulty-conditional*, and explicitly draws the contrast:

> "…find task difficulty-specific differences: The model's final answer is decodable from activations far earlier in CoT than a monitor is able to say, **especially for easy recall-based MMLU questions. We contrast this with genuine reasoning in difficult multihop GPQA-Diamond questions.** Despite this, inflection points … occur almost exclusively in responses where probes show large belief shifts, **suggesting these behaviors track genuine uncertainty rather than learned 'reasoning theater.'**"

So the source supports decoupling for easy items and explicitly reports the opposite (genuine, causally engaged reasoning) for hard items. The blanket "all report causal decoupling" overstates it. There is a second, smaller mismatch: the manuscript's cluster is defined by intervening "on trace content", whereas Reasoning Theater's interventions are activation probing, early forced answering and probe-guided early exit — truncation and read-out rather than editing trace content.

**What a human must check:** whether the other three members of the cluster are cleanly "intervene on content" results, so the grouping sentence can be narrowed rather than split.

**Suggested fix:** hedge the sentence, e.g. "…all report causal decoupling, in Reasoning Theater's case for easy recall-type items specifically, with difficult multihop questions showing genuine belief movement", or move Reasoning Theater to a separate clause describing forced-answer/probe interventions.

### A-4 (PLAUSIBLE) — `friedman_packing`: the N = 26 record is attributed by the source to a person, not to ShinkaEvolve

Manuscript, `sec_intro_task.tex` L116–118:

> "…its $N = 26$ entry, 2.63598, \emph{is} ShinkaEvolve's figure truncated, **so the LLM-driven systems are the record on this problem**."

Source: the page's n = 26 line reads "Σ r = 2.63598+ **Found by Haowei Lin in July 2026**". The numeric identity with ShinkaEvolve's 2.6359831 truncated is arithmetically exact, but the cited source credits a named individual (the same person credited with n = 33…40 in July 2026), not ShinkaEvolve or any LLM-driven system. The inference "so the LLM-driven systems are the record" is not carried by the source.

**What a human must check:** whether Haowei Lin's July 2026 submission is in fact the ShinkaEvolve result (or another LLM-driven run), by checking authorship of `lange2025shinkaevolve...` / the submitter's own report.

**Suggested fix:** state the inference as an inference — "the entry's value coincides with ShinkaEvolve's figure truncated (the page credits H. Lin, July 2026), so on this problem the published record is at or below the LLM-driven systems' band" — or verify the attribution and cite it explicitly.

### A-5 (PLAUSIBLE) — `kaplan2020scalinglawsneurallanguage` credited with "then run the confirming instance"

Manuscript, `sec_related_repro.tex` L67–68 (short: L69–70):

> "Structural precedents: \citet{kaplan2020scalinglawsneurallanguage} and \citet{hoffmann2022trainingcomputeoptimallargelanguage} **publish a functional form then run the confirming instance**."

The second half is squarely true of Hoffmann ("We test this hypothesis by training a predicted compute-optimal model, Chinchilla"). Kaplan's abstract describes fitting and extrapolating power laws — "Simple equations govern … These relationships allow us to determine the optimal allocation of a fixed compute budget" — with no confirming run of a separately predicted instance. Attributing the publish-then-confirm structure jointly to both is the ledger-18-style pattern of citing a paper for a result it does not contain, though only for one clause of a shared sentence.

**What a human must check:** whether any section of Kaplan et al. (2020) presents a held-out confirmation run of a pre-registered prediction; the abstract and the paper's framing (19 pages, empirical fitting study) suggest not.

**Suggested fix:** split the clause — "\citet{kaplan2020scalinglawsneurallanguage} publishes a functional form for aggregate loss and \citet{hoffmann2022trainingcomputeoptimallargelanguage} then runs the confirming instance (Chinchilla)". This is also a *stronger* framing for the manuscript, since it makes the predict-then-confirm precedent a single clean precedent rather than two loose ones.

## 4. Non-arXiv references in this shard

| Citation | Type | How verified | Result |
|---|---|---|---|
| `carlini2021extracting` | USENIX Security '21 conference paper | Fetched https://www.usenix.org/conference/usenixsecurity21/presentation/carlini-extracting (HTTP 200) | Title, all 12 authors with affiliations, and the abstract match the bib; venue "30th USENIX Security Symposium" and year 2021 correct. |
| `golchin2024timetravel` | ICLR 2024 (bib `note={arXiv:2308.08493}`) | OpenReview API (`api2.openreview.net` search) + arXiv abs page comment field | OpenReview venue "ICLR 2024 spotlight"; arXiv comment "Published at ICLR 2024 as a Spotlight paper (notable top 5%)"; exact title match. Bib is correct; it could optionally record the spotlight status. |
| `guo2024evoprompt` | ICLR 2024 (bib `note={arXiv:2309.08532}`) | OpenReview API + arXiv abs page comment field | OpenReview venue "ICLR 2024 poster", title identical to the bib. arXiv v3 renamed the preprint "EvoPrompt: Connecting LLMs with…"; the bib correctly uses the published ICLR title. |
| `friedman_packing` | Web page (Erich Friedman, Packing Center) | Fetched https://erich-friedman.github.io/packing/cirRsqu/ (HTTP 200) | Page exists and is the right page ("Circles in Squares … largest possible sum of radii … inside a unit square"). n = 26 entry is 2.63598+. **But** the page now runs to n = 40, contradicting two manuscript sentences — see Findings A-1 and A-4. The bib `year={n.d.}` with `note={… accessed 2026}` should carry a precise access date, since the page's contents changed in January and July 2026. |

## 5. Metadata nits (no verdict change)

- `arcuschin2026…` (2503.08679): v1 Mar 2025, bib `year={2026}`; now published at ICML 2026, which the entry does not record.
- `herrmann2026…` (2510.27353): v1 Oct 2025, bib `year={2026}`; accepted to ACM TELO, recorded only as a bare `doi` on a `@misc` entry.
- `huang2026…` (2505.15392): v1 May 2025, bib `year={2026}`; ICLR 2026 HCAIR workshop not recorded.
- In all three cases the year is defensible from the published/revised version, but the entry should carry the venue so a reader can tell which version is meant.
