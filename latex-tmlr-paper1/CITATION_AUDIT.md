# Citation audit — paper 1 (TMLR), Rev 4.12

Date: 2026-08-28. Branch `claude/new-papers-review-pa3ona`.

Paper 1 had never had a systematic citation audit. The 38/38 audit in
`latex-tmlr/CITATION_AUDIT.md` covers **paper 2**; only 11 of paper 1's bib
entries overlap that set, leaving 49 unverified. Earlier citation fixes
(`corrections_ledger.md` items 18–26) were reviewer-driven and targeted.

Method, per entry: (a) identifier verification — fetched live and checked for
resolution, withdrawal, and metadata match; (b) claim check — every citation
site located by grepping the key across `sec_*.tex` in both the long and the
short variant, and judged against what the source actually says. Verdicts are
per entry, taking the worst verdict across that entry's distinct claims.
Run in three shards by bib key; the full per-entry tables are in the shard
sections below.

**Result: 58 unique keys audited. 58/58 identifiers resolve, 0 withdrawn,
0 unreachable. 46 CONFIRMED · 8 PLAUSIBLE · 4 REFUTED · 0 UNVERIFIED.**

| shard | key range | entries | CONFIRMED | PLAUSIBLE | REFUTED |
|---|---|---|---|---|---|
| A | `abdelnabi` → `kaplan` | 20 | 16 | 3 | 1 |
| B | `khanzadeh` → `sharma` | 20 | 14 | 3 | 3 |
| C | `shojaee` → `zhang2026testing` | 18 | 16 | 2 | 0 |

## Findings requiring action — consolidated

Ordered by severity. Full evidence, quoted manuscript sentences, and suggested
fixes are in the shard sections.

### REFUTED

1. **`friedman_packing` — the bound table does not stop at N = 30** (shard A).
   §1.1: "Above $N = 30$ there is no bound table"; fig. 1 caption: the dotted
   series terminates at $N = 30$ "because the bound table stops there". The
   live page publishes best-known values through $N = 40$, covering the whole
   $[31,35]$ trap zone (31: 2.889+; 32: 2.939+, Berthold et al., Jan 2026;
   33: 2.98728+ … 40: 3.29239+, the 33–40 entries credited to Haowei Lin,
   July 2026). Re-fetched and confirmed independently of the shard agent. The
   $N = 10\ldots30$ limit belongs to the transcription in
   `n_sweep_forecast.py`, not to the source; the adjacent sentence already
   scopes it correctly. Fix: attribute the termination to the transcription,
   record the access date, or extend the table.

2. **`novikov2025alphaevolve` — 2.63586276 is not in the AlphaEvolve paper**
   (shard B). §1: "AlphaEvolve … reported 2.63586276 for $n = 26$". The paper
   gives only 2.634 and 2.635 in range (App. B.12: "the SOTA was 2.634, and
   AlphaEvolve improved it to 2.635"; Fig. 14: "$\geq$ 2.635"). The shard
   traced the figure to the released `google-deepmind/alphaevolve_results`
   Colab: summing the radius column of the §B.12 `construction_1` gives
   2.635862756414. The number is right and belongs to the *released
   construction*, which the manuscript cites nowhere. Ledger item 22's fix is
   numerically sound but under-sourced. Fix: cite the artifact and split the
   attribution.

3. **`li2026chainholdsanswerfolds` — the descriptor inverts the source**
   (shard B). Filed under "one cluster intervenes on trace content and finds
   answers do not move". The source's intervention is multi-turn adversarial
   *user pushback*, not trace editing (its one trace-anchored manipulation
   "backfires"), and its finding is that "the chain-of-thought stays factually
   correct … while the emitted answer flips wrong" — the answer moves, the
   trace does not. Abstract re-read and confirmed independently. Ledger item
   20 moved this key out of the estimator cluster without checking the
   destination descriptor. Present in both variants.

4. **`sharma2025openevolve` — the reported band is wrong in both directions**
   (shard B). §7: OpenEvolve "reports values in the 2.634--2.636 band across
   its published example runs". At repo commit 411fb59 the only published
   results are 2.634292402141039 and 2.6304; every 2.635 in the repo is
   AlphaEvolve's `TARGET_VALUE`, and nothing reaches 2.636. The parenthetical
   2.634292 in the manuscript is exactly right.

### PLAUSIBLE

5. `friedman_packing`, second claim (shard A) — §1.1 says the source's
   $N = 26$ entry "*is* ShinkaEvolve's figure truncated, so the LLM-driven
   systems are the record". The page credits 2.63598+ at $N = 26$ to Haowei
   Lin (July 2026). Numerically consistent; the attribution is not the
   source's. Interacts with ledger item 4.
6. `balunovic2025mathconstruct` (A) — filed under proposer skepticism; it is a
   121-problem constructive-proof benchmark, silent on proposer contribution.
7. `boppana2026reasoningtheater` (A) — "all report causal decoupling"
   over-generalizes; the abstract restricts decoupling to easy recall-type
   items and explicitly contrasts genuine reasoning on hard multi-hop items.
8. `kaplan2020scalinglaws` (A) — "publish a functional form then run the
   confirming instance" is true of Hoffmann, not of Kaplan.
9. `khrulkov2025gigaevo` (B) — "where a self-reported behavioral descriptor
   would be perturbed in practice"; GigaEvo's axes are all computed and
   "descriptor" appears nowhere in it. Long variant only — the short variant
   already deletes the clause.
10. `malberg2025` (B) — "numeric primes dragging point estimates"; anchoring is
    1 of 30 biases and its response format is an 11-option 0–100% scale.
11. `romeraparedes2024funsearch` (B) — "the lineage FunSearch opened", adjacent
    to "circle packing is the showcase benchmark"; FunSearch ran cap set and
    online bin packing only.
12. `wang2026diversescientifichypothesissearch` (C) — filed under proposer
    skepticism; it attributes diversity collapse to selection pressure in the
    search loop and proposes better search as the fix.
13. `zhang2026testingfrontierlargelanguage` (C) — fourth in a four-cite list
    mapped onto three nouns, so it positionally inherits "agent protocols",
    which belongs to Vaccaro.

## Bib hygiene

- **Duplicate entries.** `sharma2025openevolve` (lines 91, 612) and
  `openai2025o3o4systemcard` (lines 319, 620) are each present twice, added by
  Rev 4.11; BibTeX logs "Repeated entry" twice in `main.blg`. The
  `openai2025o3o4systemcard` copies are whitespace-only variants. The
  `sharma2025openevolve` copies **genuinely differ** — different title,
  different `howpublished`, and only the second carries
  `note={Repository unpinned; circle-packing example value read at time of
  access, 2026}`. BibTeX keeps the first, so `main.bbl` renders the less
  accurate title and silently drops the access-date qualifier that the
  manuscript sentence depends on. Keep the **second** copy.
- **Missing venues** (no verdict change): `arcuschin2026` (ICML 2026),
  `herrmann2026` (ACM TELO, DOI only on a `@misc`), `huang2026` (ICLR 2026
  workshop).
- `openai2025o3o4systemcard`'s cited URL 403s to automated clients; the
  identical document at the `cdn.openai.com` PDF is retrievable and confirms
  the cited PersonQA figures. Recommend citing the retrievable URL.

## Outside paper 1

Paper 2's `latex-tmlr/CITATION_AUDIT.md` records ShinkaEvolve as 2.635983283,
which matches none of the three figures in ShinkaEvolve's text (relaxed
2.635983099011548; exact replication 2.63597770931127). Paper 1's numbers are
correct. Paper 2 is already submitted, so this needs checking on its own.

---

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
# Citation audit — paper 1 (TMLR), SHARD B

Date: 2026-08-28. Branch `claude/new-papers-review-pa3ona`, manuscript Rev 4.12.

Shard B covers the 20 unique bib keys in `references.bib` sorting alphabetically
from `khanzadeh2026projectariadnestructuralcausal` through `sharma2025openevolve`
inclusive. Every identifier was fetched live: arXiv entries via `arxiv.org/abs/<id>`
(plus `arxiv.org/html/<id>` full text where a numeric claim had to be checked),
journal entries via Crossref and the publisher record, conference entries via
PMLR/OpenReview, and the two non-scholarly entries via the publisher PDF and the
GitHub repository itself. Claim sites were located by grepping each key across
`sec_*.tex` (both the long variant and the `sec_short_*` variant) and reading the
surrounding sentences.

**Result: 20/20 identifiers resolve, 0 withdrawn, 0 unreachable.
14 entries CONFIRMED, 3 PLAUSIBLE, 3 REFUTED, 0 UNVERIFIED.**

Verdicts are per entry and take the worst verdict across that entry's distinct
claim sites; entries whose several sites differ are broken out in the notes and in
FINDINGS REQUIRING ACTION.

## 1. Summary counts

| Metric | Count |
|---|---|
| Unique keys in shard | 20 |
| Identifiers verified (resolve) | 20 / 20 |
| Withdrawn | 0 |
| Unreachable after retries | 0 |
| CONFIRMED | 14 |
| PLAUSIBLE | 3 |
| REFUTED | 3 |
| UNVERIFIED | 0 |
| Distinct claim sites checked (long + short variant) | 33 |

## 2. Per-entry table

| bib key | identifier | resolves? | withdrawn? | verdict | note |
|---|---|---|---|---|---|
| khanzadeh2026projectariadnestructuralcausal | arXiv 2601.02314 | yes | no | CONFIRMED | Title/author/year exact. Abstract does `do`-calculus hard interventions on intermediate reasoning nodes and names the failure mode "Causal Decoupling" (violation density up to 0.77) — matches the §7 cluster descriptor verbatim, including the phrase "Reasoning Theater". |
| khrulkov2025gigaevoopensourceoptimization | arXiv 2511.17592 | yes | no | PLAUSIBLE | Scoreboard value CONFIRMED: paper states "we obtained 2.63598 (compared to the reported value 2.635)"; manuscript's "2.636" is a correct but coarse rounding. Second site's "self-reported behavioral descriptor" clause needs a human read — see Finding B4. |
| kim2026geobuildbenchbenchmarkinteractiveexecutable | arXiv 2605.13167 | yes | no | CONFIRMED | Title/authors/year exact. Abstract: "despite reasonable success rates, models frequently exhibit structural hallucinations, missing objects, and failures to satisfy geometric constraints" — supports "nominal capability and executed correctness diverge". See note (a) below on the paragraph heading. |
| kirk2024rlhf | arXiv 2310.06452; ICLR 2024 | yes | no | CONFIRMED | OpenReview: ICLR.cc/2024/Conference, "ICLR 2024 poster" — venue/year in bib correct. Abstract: "RLHF significantly reduces output diversity compared to SFT" supports "alignment-induced diversity loss"; the vendor-dependence extrapolation is explicitly hedged as an untested candidate account. |
| lange2025shinkaevolveopenendedsampleefficientprogram | arXiv 2509.19349 | yes | no | CONFIRMED | Both figures verified in App.: relaxed 2.635983099011548 → 2.6359831 ✓; AlphaEvolve exact-verification replication 2.63597770931127 → 2.6359777 ✓. Relaxed/strict labels correct. See note (b). |
| lehman2011novelty | Evol. Comput. 19(2):189–223 | yes | n/a | CONFIRMED | Crossref 10.1162/evco_a_00025: "Abandoning Objectives: Evolution Through the Search for Novelty Alone", *Evolutionary Computation* 19(2):189–223, June 2011, Lehman & Stanley. Volume/issue/pages/year in bib all exact. Cited as a method reference for "novelty pressure". |
| lehman2022evolutionlargemodels | arXiv 2206.08896 | yes | no | CONFIRMED | Title/authors/year exact. Abstract: LLMs "vastly improve the effectiveness of mutation operators applied to programs in genetic programming" — exactly "the LLM call as an EC operator over … programs". |
| li2026chainholdsanswerfolds | arXiv 2605.29087 | yes | no | **REFUTED** | Identifier and metadata exact, but the paper is filed under a cluster descriptor that inverts its finding. See Finding B2. |
| li2026dictionariesdarwinsetlevelselection | arXiv 2607.04108 | yes | no | CONFIRMED | Abstract, verbatim: "Under matched LLM-call budgets, parent-conditioned evolution is indistinguishable from fresh independent sampling" — the manuscript's §1 paraphrase is near-exact. Equation-discovery scope is correctly flagged in the same sentence ("warrant from equation discovery, not geometry"). |
| liu2024eoh | arXiv 2401.02051; ICML 2024 | yes | no | CONFIRMED | PMLR v235: "Proceedings of the 41st International Conference on Machine Learning, PMLR 235:32201–32223". Venue/year in bib correct. Abstract supports "LLM call as an EC operator". Bib could optionally add `pages={32201--32223}`. |
| lou2024anchoringbiaslargelanguage | arXiv 2412.06593 | yes | no | CONFIRMED | Full text §3.1: 62 questions each "requiring a numerical answer" with high/low numeric anchor hints (e.g. 60 °F vs 76 °F). That is precisely "numeric primes dragging point estimates". |
| malberg2025comprehensiveevaluationcognitivebiases | arXiv 2410.15413 | yes | no | PLAUSIBLE | Identifier/title/authors exact; ACL Anthology DOI in bib (10.18653/v1/2025.nlp4dh-1.50) is consistent with the v2 (Oct 2025) revision. The §1 "established territory" cite is CONFIRMED; the §7 "numeric primes dragging point estimates" cite needs a human check — see Finding B5. |
| meyerson2024languagemodelcrossovervariation | arXiv 2302.12170; ACM TELO 4(4) | yes | no | CONFIRMED | Crossref 10.1145/3694791: *ACM Transactions on Evolutionary Learning and Optimization* 4(4):1–40, online 2024-11-28. Ledger item 22's "arXiv 2023 / TELO 2024" correction is applied correctly. Abstract: LMX is "an intelligent variation operator similar in spirit to evolutionary crossover" — matches the claim. See note (c). |
| mouret2015mapelites | arXiv 1504.04909 | yes | no | CONFIRMED | Fetched title is lowercase ("Illuminating search spaces by mapping elites"); bib title-cases it — cosmetic only. Abstract introduces MAP-Elites and its user-chosen "dimensions of variation", supporting the "MAP-Elites descriptors" method cite. |
| novikov2025alphaevolve | arXiv 2506.13131 | yes | no | **REFUTED** | Identifier/title/year exact and not withdrawn, but the cited paper never states 2.63586276. See Finding B1. |
| openai2025o3o4systemcard | openai.com/index/o3-o4-mini-system-card/ | yes (see note) | n/a | CONFIRMED | Verified against the canonical PDF (see §4). Table 4: PersonQA hallucination rate o3 = 0.33 vs o1 = 0.16, with "o3 tends to make more claims overall, leading to more accurate claims as well as more inaccurate/hallucinated claims" — supports "shows the same on PersonQA". |
| romeraparedes2024funsearch | Nature 625(7995):468–475, 2024 | yes | n/a | PLAUSIBLE | Crossref confirms every bib field exactly (title, journal, volume 625, issue 7995, pages 468–475, print 2024-01-18, all 12 authors). Ledger item 22's venue correction applied correctly. The §7 claim is CONFIRMED; the §1 "the lineage FunSearch opened" phrasing needs a disambiguating edit — see Finding B6. |
| scalena2026commitmentboundaryprobingepiphenomenal | arXiv 2606.13603 | yes | no | CONFIRMED | Title/six authors/year exact. Abstract: causal importance estimated via early exit; commitment boundary "followed by *epiphenomenal* CoT steps that leave the final answer probability unaltered" — supports both "intervenes on trace content" (truncation) and "answers do not move". Ledger item 20's reclassification from "estimator" to "causal decoupling" is correct for this key. |
| sclar2024formatspread | arXiv 2310.11324; ICLR 2024 | yes | no | CONFIRMED | OpenReview: ICLR.cc/2024/Conference, "ICLR 2024 poster". Abstract: "performance differences of up to 76 accuracy points"; FormatSpread is the paper's own named algorithm, so "a formatspread-style sweep of the size reported by" is exact at all three sites. |
| sharma2025openevolve | github.com/codelion/openevolve | yes | n/a | **REFUTED** | Repo cloned at commit 411fb59 (2026-07-18). 2.634292 is exactly right; the "2.634–2.636 band" is not supported. See Finding B3. Also see §5 on the duplicate entry. |

Notes referenced above:

(a) **kim2026 — heading vs. claim.** GeoBuildBench sits under the §7 boldface
heading **"Scaling inversions."** The paper reports no scaling inversion (no
"larger model does worse" finding). The claim actually attributed to it —
capability/executability divergence — is supported, and the sentence is a list of
loosely related evidence, so this is CONFIRMED, not a defect. Flagged only so a
copy-editor can decide whether the heading over-promises.

(b) **lange2025 — a third figure exists.** The ShinkaEvolve appendix reports
*three* n = 26 numbers: the relaxed solution 2.635983099011548; that same solution
made exact by shrinking each radius by 1e-8, giving **2.6359828390115476**; and a
separate re-run under AlphaEvolve's exact verification code scoring
2.63597770931127. The manuscript's "strict" figure is the third of these, not the
second. Both manuscript numbers are in the source and the relaxed/strict labelling
is defensible, so this is CONFIRMED — but if §1.1's ordering argument turns on
which strict figure is meant, a one-clause disambiguation would help. (Separately:
paper 2's `latex-tmlr/CITATION_AUDIT.md` line 28 records ShinkaEvolve's value as
"2.635983283", which matches none of the three figures in 2509.19349 — that is a
paper-2 issue, outside this shard, but worth passing on.)

(c) **meyerson2024 — entry type.** The entry is `@misc` with `year={2024}`, an
arXiv eprint whose v1 is Feb 2023, and the TELO DOI. It renders as a preprint with
a journal DOI attached. Fields are all individually correct; converting to
`@article` with `journal={ACM Transactions on Evolutionary Learning and
Optimization}, volume={4}, number={4}` would be cleaner but is not a defect.

## 3. FINDINGS REQUIRING ACTION

### B1 — REFUTED: AlphaEvolve is credited with a number its paper does not report

**Key:** `novikov2025alphaevolve` (arXiv 2506.13131)
**Sites:** `sec_intro_task.tex:24` and `sec_short_intro_task.tex:25` (identical
wording in both variants).

**Manuscript sentence:**
> "It is the task on which AlphaEvolve \citep{novikov2025alphaevolve} reported
> 2.63586276 for $n = 26$ and on which later systems report a narrow band …"

**Source evidence.** The full text of 2506.13131v1 contains no 8-decimal figure.
Appendix B.12, verbatim:
> "For $n=26$, the SOTA was $2.634$, and AlphaEvolve improved it to $2.635$; see
> Figure 14 (left)."

and Figure 14's caption: "26 circles in a unit square with sum of radii
$\geq 2.635$". A regex sweep of the whole rendered paper returns exactly two
distinct values in this range — `2.634` and `2.635`. GigaEvo (2511.17592)
independently corroborates the reading, describing its own result as "2.63598
(compared to the reported value 2.635)".

**The number itself is right, the attribution is not.** AlphaEvolve's paper points
(footnote 1, and again in Appendix B) to an accompanying Google Colab,
`google-deepmind/alphaevolve_results/mathematical_results.ipynb`. I fetched that
notebook and summed the radius column of its §B.12 `construction_1` (26 circles):

```
sum of radii = 2.635862756414  →  2.63586276 at 8 d.p.
```

So 2.63586276 is the value of AlphaEvolve's *released construction*, not a value
AlphaEvolve *reported*. This matters because ledger item 22 specifically replaced
"2.635" with "2.63586276" to fix an under-precision complaint, and the replacement
introduced a source mismatch: the paper cited for the number does not contain it,
and the artifact that does contain it is not cited anywhere in the manuscript
(`grep` for "colab", "alphaevolve_results" across all `sec_*.tex` returns nothing).
Since §1.1 and §7 hang record-comparison claims on this figure, an adversarial
reviewer who opens 2506.13131 will find 2.635 and conclude the number was invented.

**Suggested fix.** Add a bib entry for the results notebook and split the
attribution, e.g.:

> "…on which AlphaEvolve \citep{novikov2025alphaevolve} reported 2.635, its
> released construction summing to 2.63586276 \citep{alphaevolve_results}…"

with

```bibtex
@misc{alphaevolve_results,
  author       = {{Google DeepMind}},
  title        = {{AlphaEvolve} results: mathematical results notebook},
  howpublished = {\url{https://github.com/google-deepmind/alphaevolve_results}},
  year         = {2025},
  note         = {Notebook \texttt{mathematical\_results.ipynb}, §B.12
                  \texttt{construction\_1}; sum of radii 2.635862756414, accessed 2026}
}
```

The alternative — reverting to "2.635" — is cheaper but loses the precision the
ledger item was added to gain, and would reopen the §1.1 ordering argument.

### B2 — REFUTED: "The Chain Holds, the Answer Folds" is filed under a descriptor that inverts its finding

**Key:** `li2026chainholdsanswerfolds` (arXiv 2605.29087)
**Sites:** `sec_related_repro.tex:49–52`; `sec_short_related_repro.tex:51–52`
(the short variant compresses the four keys into one `\citep` list under the same
descriptor, so the defect is present in both variants).

**Manuscript sentence:**
> "One cluster intervenes \emph{on trace content} and finds answers do not move ---
> Reasoning Theater \citep{boppana2026reasoningtheaterdisentanglingmodel}, Project
> Ariadne \citep{khanzadeh2026projectariadnestructuralcausal}, ``Beyond the
> Commitment Boundary'' \citep{scalena2026commitmentboundaryprobingepiphenomenal}
> and ``The Chain Holds, the Answer Folds'' \citep{li2026chainholdsanswerfolds} all
> report causal decoupling."

**Source evidence.** 2605.29087's abstract:
> "Reasoning models are evaluated on single-turn benchmarks but deployed in
> multi-turn dialogue, where users push back on correct answers. Under sustained
> adversarial pressure we find a previously undocumented failure mode: **the
> chain-of-thought stays factually correct from first turn to last while the
> emitted answer flips wrong.** We call this unfaithful capitulation (UC) …"

Both halves of the descriptor fail for this paper:

1. *"intervenes on trace content"* — it does not. The intervention is **adversarial
   user pushback across dialogue turns**; the trace is observed, never edited. (The
   paper explicitly contrasts itself with "single-turn faithfulness probes", i.e.
   the trace-editing methods.) The one manipulation it does apply to the trace, a
   "naive trace-anchored defense", is reported to *backfire*.
2. *"finds answers do not move"* — the opposite. The finding is that the **answer
   moves while the trace holds still**: the answer "flips wrong" in 100% of the UC
   cells by construction. That is the mirror image of the other three papers, in
   which the trace is altered and the answer stays put.

"Causal decoupling" in the loosest sense (trace and answer dissociate) does cover
it, which is presumably how ledger item 20 landed it here — but item 20 only
reclassified 2605.29087 *away from* the estimator cluster; it did not check that
the destination cluster's descriptor fits. It does not.

**Suggested fix.** Move it out of the sentence and give it its own clause, e.g.:

> "…all report causal decoupling under intervention on the trace. ``The Chain
> Holds, the Answer Folds'' \citep{li2026chainholdsanswerfolds} reports the mirror
> case — under multi-turn adversarial pressure the trace stays correct while the
> answer flips — which is decoupling in the other direction."

If space forbids, the minimum repair is to drop `li2026chainholdsanswerfolds` from
the list; the remaining three (Reasoning Theater, Project Ariadne, Beyond the
Commitment Boundary) all fit the descriptor as written and Project Ariadne fits it
verbatim.

### B3 — REFUTED: OpenEvolve's "2.634–2.636 band" is not in the repository

**Key:** `sharma2025openevolve`
**Sites:** `sec_related_repro.tex:11`; `sec_short_related_repro.tex:13–14`
(same claim in both variants).

**Manuscript sentence:**
> "OpenEvolve \citep{sharma2025openevolve}, the open-source AlphaEvolve reproduction
> most practitioners run, reports values in the 2.634--2.636 band across its
> published example runs (2.634292 in the circle-packing example at the time of
> access; the repository is unpinned)."

**Source evidence.** Repository cloned at `411fb59c886c18704caaffb611e17cf9e7d824d2`
(2026-07-18). An exhaustive `grep` for `2\.63[0-9]` across all `.md`, `.py`,
`.yaml` and `.json` files returns only these OpenEvolve *results*:

| file | value | what it is |
|---|---|---|
| `examples/circle_packing/README.md:190`, `best_program_info.json:9` | **2.634292402141039** | the n=26 circle-packing result |
| `examples/circle_packing_with_artifacts/README.md:349` | **2.6304** | the with-artifacts variant's result |

Every other hit is AlphaEvolve's *target*, not an OpenEvolve result:
`evaluator.py:203` `TARGET_VALUE = 2.635  # AlphaEvolve result for n=26`;
`config_phase_1.yaml:24` "The AlphaEvolve paper achieved a sum of 2.635 for n=26";
`README.md:181` "achieved a sum of radii of 2.634, matching the AlphaEvolve paper's
result of 2.635 to within 0.04%".

So: (i) the parenthetical **2.634292 is exactly right** — CONFIRMED against
`best_program_info.json`; (ii) the **band is wrong in both directions**. Nothing in
the repository reports an OpenEvolve value at or near 2.636; the highest is
2.634292, and the second published example run is *below* the stated band at 2.6304.
The only 2.635 in the repo belongs to AlphaEvolve. Because the surrounding paragraph
is arguing about where the scoreboard actually sits, stating that the most-run
open-source reproduction reaches 2.636 materially overstates it.

**Suggested fix.**

> "OpenEvolve \citep{sharma2025openevolve}, the open-source AlphaEvolve reproduction
> most practitioners run, reports 2.634292 in its circle-packing example and 2.6304
> in the with-artifacts variant — below the AlphaEvolve figure it targets. The
> repository is unpinned; values read at time of access."

Two secondary points on the same sentence: "the … reproduction most practitioners
run" is a popularity claim I could not verify (GitHub's API and HTML star counts
both returned 403 to automated fetches through the proxy) — consider softening to
"a widely used open-source AlphaEvolve reproduction" or supplying a star/download
count with an access date. And the access-date qualifier the sentence leans on is
currently dropped from the rendered bibliography — see §5.

### B4 — PLAUSIBLE: GigaEvo and the "self-reported behavioral descriptor"

**Key:** `khrulkov2025gigaevoopensourceoptimization` (arXiv 2511.17592)
**Site:** `sec_related_repro.tex:69–71` (long variant only — see below).

**Manuscript sentence:**
> "…QDAIF \citep{bradley2023qualitydiversityaifeedback} is the QD-descriptor setting
> most affected by our \S6 result, and GigaEvo
> \citep{khrulkov2025gigaevoopensourceoptimization} the concrete in-scope system
> running MAP-Elites with LLM-driven mutation, where a self-reported behavioral
> descriptor would be perturbed in practice."

**Source evidence.** The first half is CONFIRMED verbatim from the abstract:
"MAP-Elites quality-diversity algorithms … LLM-driven mutation operators".

The clause after the comma is the issue. GigaEvo's behavior space is computed, not
self-reported. §Evolutionary Engine: "programs are mapped to a two-dimensional
behavior space discretized into cells based on: (i) fitness … " with validity as the
second axis, and the multi-island variant uses "distinct behavior spaces (e.g.,
fitness vs. complexity)". The string "descriptor" does not appear in the paper at
all; no axis is an LLM self-report.

The manuscript's subjunctive "**would be** perturbed" makes this technically a
conditional about a descriptor GigaEvo does not currently use, so it is not false as
written — but a reader skimming the sentence will take it as a statement that
GigaEvo self-reports its descriptors, which it does not. Given that the §6 result is
about self-report perturbation, this is exactly the sentence a hostile reviewer
would pick up.

**What needs a human check:** whether the intended meaning is "GigaEvo is the
nearest deployed system, and a self-reported descriptor swapped into its MAP-Elites
axes is where our §6 result would bite" (fine, needs rewording) or "GigaEvo already
uses self-reported descriptors" (false).

**Suggested fix.**

> "…and GigaEvo \citep{khrulkov2025gigaevoopensourceoptimization} the concrete
> in-scope system running MAP-Elites with LLM-driven mutation — its archive axes are
> measured (fitness, validity, complexity), so our \S6 result bites only if a
> self-reported descriptor is substituted for one of them."

**Variant note:** `sec_short_related_repro.tex:72` already ends the sentence at "…
MAP-Elites with LLM-driven mutation." with the clause deleted. The short variant is
clean; only the long variant needs the edit.

### B5 — PLAUSIBLE: Malberg and "numeric primes dragging point estimates"

**Key:** `malberg2025comprehensiveevaluationcognitivebiases` (arXiv 2410.15413)
**Site:** `sec_related_repro.tex:21–23`; `sec_short_related_repro.tex:27–29`
(same claim, both variants).

**Manuscript sentence:**
> "On anchoring, \citet{huang2026understandinganchoringeffectllm} treats anchoring as
> a general bias over initial information while \citet{lou2024anchoringbiaslargelanguage}
> and \citet{malberg2025comprehensiveevaluationcognitivebiases} document numeric
> primes dragging point estimates…"

**Source evidence.** For Lou this is exact (see table). For Malberg it is a
compression of a broader paper, in two respects. First, the paper is a benchmark of
**30 cognitive biases across 20 LLMs**; anchoring is §B.2, one of thirty, and the
headline contribution is the test-generation framework and the 30,000-test dataset,
not an anchoring result. Second, the anchoring test's response format is not a point
estimate: Table 1 shows a control/treatment pair in which the treatment inserts a
numeric anchor (the worked example uses `{{anchor}}: "87"`) and the model picks from
an **11-option discrete scale, "Option 1: 0% … Option 11: 100%"**. That is a numeric
prime shifting a discrete allocation choice, which is close to but not the same as
dragging a free point estimate.

**What needs a human check:** whether "point estimates" is precise enough for a
reviewer who opens §B.2 and finds an 11-option multiple choice. Nothing load-bearing
depends on it — the sentence is scene-setting for the modality contrast that follows.

**Suggested fix.** Either widen the verb — "…document numeric primes shifting
quantitative judgments" — or attribute the two sources separately, e.g. "…\citet{lou2024anchoringbiaslargelanguage}
documents numeric primes dragging numeric answers, and
\citet{malberg2025comprehensiveevaluationcognitivebiases} finds anchoring among 30
biases present across 20 models."

### B6 — PLAUSIBLE: "the lineage FunSearch opened" reads as attributing circle packing to FunSearch

**Key:** `romeraparedes2024funsearch`
**Sites:** `sec_intro_task.tex:22–23`; `sec_short_intro_task.tex:23–24`.

**Manuscript sentence:**
> "Circle packing is the showcase benchmark of the LLM-driven discovery literature,
> the lineage FunSearch \citep{romeraparedes2024funsearch} opened."

**Source evidence.** FunSearch never ran circle packing. The Nature paper applies
FunSearch to exactly two problems — the cap set problem and online bin packing
("Applying FunSearch to a central problem in extremal combinatorics—the cap set
problem… We showcase the generality of FunSearch by applying it to an algorithmic
problem, online bin packing"). A full-text search of the article returns **0**
occurrences of "circle pack" against 42 each for "cap set" and "bin packing".

Parsed strictly, the manuscript is right: the appositive "the lineage … FunSearch
opened" attaches to *the LLM-driven discovery literature*, not to *circle packing*,
and FunSearch did open that lineage — §7's separate claim, "FunSearch turned the
pattern into a discovery claim", is CONFIRMED. But the two noun phrases sit adjacent
and a fast reader takes the sentence to mean FunSearch introduced the circle-packing
benchmark. Given that §1.1 is where the record-comparison correction (ledger item 4)
lives, this is a sentence worth making unambiguous.

**What needs a human check:** whether the ambiguity is worth a word. No numeric or
registered claim depends on it.

**Suggested fix.**

> "Circle packing is the showcase benchmark of the LLM-driven discovery literature —
> the lineage FunSearch \citep{romeraparedes2024funsearch} opened on cap sets and bin
> packing, and AlphaEvolve later extended to geometry."

## 4. Non-arXiv references in this shard, and how each was verified

Four entries in Shard B are not primarily arXiv preprints. Three more
(`liu2024eoh`, `sclar2024formatspread`, `kirk2024rlhf`) are `@inproceedings` with
arXiv numbers in a `note`; both the arXiv id and the conference record were checked
for those and are listed here too.

| Citation | Type | How verified | Result |
|---|---|---|---|
| `romeraparedes2024funsearch` — Nature | journal article | Crossref API on DOI 10.1038/s41586-023-06924-6, plus full text via PubMed Central (PMC10794145) | Title, journal, **volume 625, issue 7995, pages 468–475**, print date 2024-01-18 (online 2023-12-14), and all 12 author surnames match the bib exactly. Ledger item 22's venue/year correction applied correctly. Full text used for Finding B6. |
| `lehman2011novelty` — Evolutionary Computation | journal article | Crossref bibliographic query; record DOI 10.1162/evco_a_00025 | "Abandoning Objectives: Evolution Through the Search for Novelty Alone", *Evolutionary Computation* **19(2):189–223**, June 2011, Lehman & Stanley. Every bib field exact. Bib has no DOI field; adding one is optional. |
| `openai2025o3o4systemcard` — vendor system card | web/PDF report | The `howpublished` URL `openai.com/index/o3-o4-mini-system-card/` returns **HTTP 403 to automated fetchers** (both curl with a browser UA and WebFetch; the agent proxy itself is healthy — `__agentproxy/status` shows `enabled: true`, no relay failures — so this is openai.com's own bot filter, not a proxy fault). Verified instead against the canonical PDF at `cdn.openai.com/pdf/2221c875-02dc-4789-800b-e7758f3722c1/o3-and-o4-mini-system-card.pdf`, extracted and read in full (33 pp.) | Document is "OpenAI o3 and o4-mini System Card", OpenAI, **April 16, 2025** — bib year correct. §3.3 Table 4: PersonQA hallucination rate **o3 0.33, o4-mini 0.48, o1 0.16** (accuracy 0.59 / 0.36 / 0.47), with the text "o3 tends to make more claims overall, leading to more accurate claims as well as more inaccurate/hallucinated claims… More research is needed". Claim CONFIRMED. **Recommendation:** add the cdn.openai.com PDF URL to the bib entry (as a second `\url` or a `note`), since the cited landing page is not machine-retrievable and a reviewer using an automated link checker will see a dead link. |
| `sharma2025openevolve` — GitHub repository | software repository | GitHub REST API returned 403 for this session, so the repository was **cloned** (`git clone --depth 1`, commit `411fb59c886c18704caaffb611e17cf9e7d824d2`, 2026-07-18) and searched directly; the two example READMEs and `best_program_info.json` were read in full | Repository exists, is public and active. Self-description: "The most advanced open-source evolutionary coding agent". Circle-packing result **2.634292402141039** confirmed; band claim REFUTED (Finding B3). Star count not verifiable (403). |
| `liu2024eoh` — ICML 2024 | conference paper | PMLR volume 235 index page | "Evolution of Heuristics: Towards Efficient Automatic Algorithm Design Using Large Language Model", Fei Liu et al., *Proceedings of the 41st ICML*, **PMLR 235:32201–32223**. Venue and year in bib correct; arXiv 2401.02051 also resolves. |
| `sclar2024formatspread` — ICLR 2024 | conference paper | OpenReview API (`api2.openreview.net/notes/search`) | Submission 6435, venue "ICLR 2024 poster", venueid `ICLR.cc/2024/Conference`. Venue/year correct; arXiv 2310.11324 also resolves. |
| `kirk2024rlhf` — ICLR 2024 | conference paper | OpenReview API | Submission 5728, venue "ICLR 2024 poster", venueid `ICLR.cc/2024/Conference`. Venue/year correct; arXiv 2310.06452 also resolves. (Also appeared at the NeurIPS 2023 Instruction Workshop; the ICLR record is the right one to cite.) |
| `mouret2015mapelites` | arXiv-only tech report | arXiv abs page | Legitimately has no venue — MAP-Elites was never formally published beyond arXiv 1504.04909. `@article` with `journal={arXiv preprint …}` is the standard workaround and is fine. |

## 5. Duplicate entries (previously known — recorded here for completeness)

`references.bib` contains two copies each of `sharma2025openevolve` (lines 91 and
612) and `openai2025o3o4systemcard` (lines 319 and 620), added by Rev 4.11.
`main.blg` logs "Repeated entry" twice (lines 8 and 12, pointing at
`references.bib` lines 1222 and 1230 of the concatenated read). BibTeX keeps the
**first** definition and discards the second silently. I audited each key once, and
compared the two copies of each:

**`openai2025o3o4systemcard` — copies are equivalent.** They differ only in
intra-field whitespace (`author       = {...}` vs `author={...}`) and a trailing
blank line. Normalizing whitespace makes them byte-identical. No semantic
consequence; deleting either copy is safe.

**`sharma2025openevolve` — the copies DIFFER in content. This is a new finding.**

| field | line 91 (kept by BibTeX) | line 612 (silently discarded) |
|---|---|---|
| `title` | `OpenEvolve: an open-source implementation of {AlphaEvolve}` | `OpenEvolve: an open-source evolutionary coding agent` |
| `howpublished` | `GitHub repository, \url{...}` | `\url{...}` |
| `note` | *(absent)* | `Repository unpinned; circle-packing example value read at time of access, 2026` |

Two consequences:

1. **The access-date qualifier is lost from the rendered bibliography.**
   `main.bbl:300–304` renders only "Openevolve: an open-source implementation of
   AlphaEvolve. GitHub repository, https://github.com/codelion/openevolve, 2025."
   The manuscript sentence at `sec_related_repro.tex:11` leans on exactly that
   qualifier ("at the time of access; the repository is unpinned") for a number read
   off an unpinned moving repository — and the bibliography no longer carries it.
   This is precisely the reproducibility hygiene the `note` was written to provide,
   defeated by the duplicate.
2. **The surviving title is the less accurate of the two.** The repository's own
   README headline is "The most advanced open-source **evolutionary coding agent**",
   which is the discarded copy's title; the kept copy's "implementation of
   AlphaEvolve" is a characterization the repo makes only about a specific example
   ("replicating one of the tasks from the AlphaEvolve paper").

**Suggested fix.** Delete the line-91 copy and keep the line-612 copy (its title
matches the source and its `note` is load-bearing), then add the commit or access
date to the note now that one is known:
`note={Repository unpinned; circle-packing example value 2.634292402141039 read at commit 411fb59, 2026-07-18}`.
For `openai2025o3o4systemcard`, delete either copy.

## 6. Verification of ledger items 18–26 that touch this shard

Ledger items 18–26 name the previously found citation defects. Those falling in or
adjacent to Shard B were re-checked to confirm the corrections were actually applied,
not merely that the entries resolve.

| Ledger item | Applies to | Status |
|---|---|---|
| 18 — SeaEvo removed (does not evaluate circle packing) | `2604.24372` | **Correctly applied.** No `luo`/SeaEvo key exists anywhere in `references.bib`, and no `sec_*.tex` mentions SeaEvo. The removal is clean. (Key itself is outside this shard's range.) |
| 22 — AlphaEvolve "2.635" → 2.63586276 | `novikov2025alphaevolve` | **Applied, but incorrectly sourced — see Finding B1.** The value is arithmetically right (it is the sum of the released construction, 2.635862756414) but is not in the cited paper, and the artifact that contains it is uncited. |
| 22 — FunSearch → *Nature* 625(7995):468–475, 2024 | `romeraparedes2024funsearch` | **Correctly applied.** Every field verified against Crossref. |
| 22 — LMX: arXiv 2023 / TELO 2024 | `meyerson2024languagemodelcrossovervariation` | **Correctly applied.** `year={2024}` with `doi={10.1145/3694791}` (TELO 4(4):1–40, Nov 2024) and eprint 2302.12170 (v1 Feb 2023). Both halves of the correction are present. |
| 22 — AlphaEvolve/ShinkaEvolve identified by name | `novikov2025alphaevolve`, `lange2025shinkaevolveopenendedsampleefficientprogram` | **Correctly applied.** Both systems are named in prose at `sec_intro_task.tex:24–25`. |
| 20 — 2606.13603 and 2605.29087 are causal-decoupling results, not estimators | `scalena2026...`, `li2026chainholdsanswerfolds` | **Half applied.** Both were moved out of the estimator cluster, which was the correction as written. But the destination cluster's descriptor was not re-checked against the sources: it fits `scalena2026` (CONFIRMED) and **inverts** `li2026chainholdsanswerfolds` — see Finding B2. |
| 23 — ShinkaEvolve/HELIX ordering | `lange2025...` | **Correctly applied and arithmetically sound.** HELIX 2.63598308 lies between ShinkaEvolve's strict 2.6359777 and relaxed 2.6359831, exactly as `sec_related_repro.tex:8` states. |
| 26 — "Mutation Without Variation" nesting (87% of chains / >93% of mutations) | `gurkan2026...` | **Nesting correctly applied** — `sec_related_repro.tex:19` reads "in 87\% of chains, over 93\% of mutations revisit a previously seen form", which is the nested phrasing the ledger requires, not the parallel one. The key itself is outside Shard B's range; verification of the percentages against the source belongs to the shard that owns `gurkan2026gurkan...`. |
| 19, 21, 24, 25 | keys outside this shard | Not audited here. |

## 7. Method and caveats

- Every arXiv abstract page was fetched with `curl` through the session proxy and
  parsed for title, authors, subject, submission history and any withdrawal notice.
  None of the 16 arXiv entries carries a withdrawal.
- Where a claim turned on a number, the rendered full text (`arxiv.org/html/<id>`)
  was fetched and searched, and in the AlphaEvolve case the released data artifact
  was downloaded and the quantity recomputed from the raw coordinates.
- Nothing in this shard is marked CONFIRMED on the strength of recalled literature:
  every CONFIRMED row names the fetched text it rests on.
- One source could not be retrieved at its cited URL (`openai.com/index/...`, HTTP
  403 to automated clients). It is **not** marked UNVERIFIED because the identical
  document was retrieved and read in full at the publisher's own CDN; the 403 is a
  bot filter on the landing page, and the recommendation in §4 addresses it.
- No file other than this one was modified. `references.bib` and all `.tex` files
  are untouched.
# Citation audit — paper 1 (Rev 4.12), SHARD C

Date: 2026-08-28. Branch `claude/new-papers-review-pa3ona`. Scope: the bib
entries in `latex-tmlr-paper1/references.bib` whose keys sort from
`shojaee2025illusionthinkingunderstandingstrengths` through
`zhang2026testingfrontierlargelanguage` inclusive — 18 entries, all arXiv.

Every arXiv id was fetched live (`arxiv.org/abs/<id>`) this pass and checked
for existence, withdrawal status, and title/author/year agreement with the bib
entry. Every citation site was located by grepping the key across
`sec_*.tex` (long variant: `sec_intro_task.tex`, `sec_forecast_transfer.tex`,
`sec_tiers_elicitation.tex`, `sec_related_repro.tex`, `sec_appendices.tex`;
short variant: `sec_short_*.tex`) and the surrounding sentence read.

## 1. Summary counts

| Metric | Count |
|---|---|
| Entries in shard | 18 |
| ids fetched and resolving (HTTP 200) | 18 / 18 |
| Withdrawn | 0 |
| Unreachable / UNVERIFIED | 0 |
| Title/author/year mismatches vs. bib | 0 substantive (2 minor year notes, §5) |
| Distinct claim sites checked (long + short) | 26 |
| CONFIRMED | 16 |
| PLAUSIBLE | 2 |
| REFUTED | 0 |

Short-variant note: for all 18 keys the short variant makes the *same* claim as
the long variant, in compressed wording. No key carries a different claim in
`sec_short_*.tex`. Deviations, where the compression changes emphasis, are
noted per-row.

Ledger cross-checks (the specific failure modes this pass was asked to hunt):

- **Item 21** (`zhang2024understandingimportanceevolutionarysearch`, 2407.10873,
  previously misfiled as loop skepticism): **fix has landed and has not
  reverted.** Both the long (`sec_related_repro.tex` L37–39, L78–80) and short
  (`sec_short_related_repro.tex` L39–40, L78–79) variants now file it under
  "Two results cut the other way", describing it as grounding the *importance*
  of evolutionary search and as evidence *against* the manuscript's
  substitution. This matches the source abstract verbatim in substance
  ("providing empirical grounding for the importance of evolutionary search in
  LLM-based AHD approaches"). CONFIRMED.
- **Item 21 second half** (`zhang2026makesllmgoodoptimizer`, 2604.19440, "recites
  as local refiner"): fix landed. Source says "strong LLM optimizers behave as
  local refiners"; manuscript says "finds strong LLM optimizers act as
  \emph{local refiners}". CONFIRMED.
- **Item 23** (ThetaEvolve / HELIX orderings): both fixes landed and both are
  now source-supported. See §3, "verified orderings".
- **Item 24** (`wang2026diversescientifichypothesissearch`, 2606.10587, formerly
  cited as "EvoDiverse" with an unverified method name): the method name has
  been removed — it is now a bare `\citet{}`. Correct, because the arXiv
  abstract leaves the system name as an unexpanded `\ours` macro, so no method
  name is verifiable from the record. However the *placement* of this citation
  is the one PLAUSIBLE finding below.
- **Item 25** (`williams2026predictingllmsafetyrelease`, 2607.07184, formerly
  "files OSF preregistrations"): fix landed. The manuscript now says
  "outcome-blinded predictions", which the abstract supports word-for-word
  ("registered, outcome-blinded predictions for GPT-5.4"). CONFIRMED.
  (The HindsightBench half of item 25 is key `jia2026hindsightbench...`, which
  sorts outside this shard — not audited here.)
- **Item 26** (nesting of the 87%/93% statistic) concerns
  `gurkan2026mutationvariation...`, outside this shard. Noted only that the
  sentence adjacent to my shard's citations now reads with the correct nesting
  ("in 87\% of chains, over 93\% of mutations revisit a previously seen form").

## 2. Per-entry table

| bib key | identifier | resolves? | withdrawn? | verdict | note |
|---|---|---|---|---|---|
| shojaee2025illusionthinkingunderstandingstrengths | arXiv 2506.06941 | yes (200) | no | CONFIRMED | Title/authors/year match exactly (v3, 20 Nov 2025). Cited in "Scaling inversions" as reporting "collapse past a complexity threshold"; abstract: "LRMs face a complete accuracy collapse beyond certain complexities". Identical in short variant. |
| sim2025hypebenchmarkingllmevolvedheuristics | arXiv 2501.11411 | yes (200) | no | CONFIRMED | "Beyond the Hype: Benchmarking LLM-Evolved Heuristics for Bin Packing", Sim/Renau/Hart, 2025 — matches. Cited as one of "the bin-packing critiques"; abstract: "most of the LLM heuristics do not generalise well". Identical in short variant. |
| snell2024predictingemergentcapabilitiesfinetuning | arXiv 2411.16035 | yes (200) | no | CONFIRMED | Matches. Two sites, same claim: contribution bullet ("Prior work publishes functional forms predicting \emph{aggregate} metrics ahead of a run") and related work ("closest structural twin"). Abstract fits "emergence laws": a parametric function fit in advance, then validated — and the predicted object is an aggregate benchmark metric, not an individual output, so the manuscript's contrast holds. |
| su2026helixevolutionaryreinforcementlearning | arXiv 2603.07642 | yes (200) | no | CONFIRMED | Matches. **Numeric record verified**: abstract states "HELIX achieves state-of-the-art result with a sum of radii of 2.63598308 using only a 14B model" — exactly the manuscript's figure and the manuscript's "described as state of the art". Ordering also verified (§3). Identical in short variant. |
| tam2024letspeakfreelystudy | arXiv 2408.02442 | yes (200) | no | CONFIRMED | Matches (v3, Oct 2024). Cited: "Format-restriction performance costs are documented at scale in \citet{...}". Abstract: "a significant decline in LLMs reasoning abilities under format restrictions... stricter format constraints generally lead to greater performance degradation". Identical in short variant. |
| thomas2026mitigatingllmbasedphackingpreregistering | arXiv 2606.27687 | yes (200) | no | CONFIRMED | Matches. Two sites (intro framing + preregistration lineage), same claim: preregisters "recipes". Abstract: preregisters "the experiment and eligible models", then runs on the first eligible future LLM — a preregistered recipe, and the authors "followed our own protocol and preregistered our experiment". Identical in short variant. |
| vaccaro2026preregistrationexperimentsaiagents | arXiv 2606.11217 | yes (200) | no | CONFIRMED | Matches (single author Michelle Vaccaro). Two sites, same claim: preregisters "agent protocols". Abstract proposes "a preregistration template tailored to experiments with AI agents". Minor metadata oddity noted in §5. Identical in short variant. |
| vanstein2025llamealargelanguagemodel | arXiv 2405.20132 | yes (200) | no | CONFIRMED | Title/authors match (Bäck accent correct in bib). Cited as one of the systems that "established the LLM call as an EC operator over prompts and programs"; abstract: LLaMEA "iteratively generates, mutates and selects algorithms based on performance metrics and feedback". Year note in §5. Identical in short variant. |
| wang2025thetaevolvetesttimelearningopen | arXiv 2511.23473 | yes (200) | no | CONFIRMED | Matches (16 authors, 28 Nov 2025). Cited: "ThetaEvolve \citep{...} claiming new best-known bounds rather than matching it". Abstract: "the first evolving framework that enable a small open-source model... to achieve new best-known bounds on open problems (circle packing and first auto-correlation inequality)". Ledger item 23 fix confirmed landed; correctly *not* described as "in the same band". Identical in short variant. |
| wang2026diversescientifichypothesissearch | arXiv 2606.10587 | yes (200) | no | **PLAUSIBLE** | Id/title/authors/year all match; the formerly-unverified "EvoDiverse" method name is correctly gone. But the *placement* — in the list of "converging skepticism about what the proposer contributes" — does not follow from the abstract, which faults the *search/selection loop*, not the proposer. See Finding C-1. Same placement in short variant. |
| williams2026predictingllmsafetyrelease | arXiv 2607.07184 | yes (200) | no | CONFIRMED | Matches (11 authors, 8 Jul 2026). Cited for preregistering "outcome-blinded predictions"; abstract: "using registered, outcome-blinded predictions for GPT-5.4". Ledger item 25 fix landed. Identical in short variant. |
| wu2025answercentricreasoningdrivenuncoveringlatent | arXiv 2506.17630 | yes (200) | no | CONFIRMED | Matches. Bare `\citep` in the list "Related observer-effect and elicitation results". Abstract: a "five-level answer-visibility prompt framework that systematically manipulates answer cues and probes model behavior through indirect, behavioral analysis" — squarely an elicitation-manipulation result (26.90% drop when cues masked). The "observer-effect" half of that phrase is carried by `abdelnabi2025hawthorne...` (outside shard). Identical in short variant. |
| yang2026accuracyevaluatingstrategydiversity | arXiv 2605.09292 | yes (200) | no | CONFIRMED | Matches; the shorthand "Strategy Diversity" tracks the title "Beyond Accuracy: Evaluating Strategy Diversity in LLM Mathematical Reasoning". Cited under skepticism about proposer contribution; abstract: models "recover substantially fewer strategies than the human reference set", strongest model recovering 39/55 (71%) after three runs — i.e. the generator's breadth falls short of the human reference. Identical in short variant. |
| yun2025priceformatdiversitycollapse | arXiv 2505.18949 | yes (200) | no | CONFIRMED | Matches. Cited as "The Price of Format ... showing format constraints collapse generation diversity"; abstract coins exactly that: "it induces a phenomenon we term diversity collapse... structural tokens in templates significantly constrain the model's output space". Identical in short variant. |
| zhang2024understandingimportanceevolutionarysearch | arXiv 2407.10873 | yes (200) | no | CONFIRMED | Matches. **Two distinct sites, both checked.** (a) Related work: "provides empirical grounding for the \emph{importance} of evolutionary search, which is evidence against our substitution of an unconditioned call for the loop". (b) §8 Limitations: "published evidence that evolutionary search contributes materially, cutting against any stronger reading". Abstract: "providing empirical grounding for the importance of evolutionary search in LLM-based AHD approaches". Ledger item 21 fix landed in both long and short variants; **no reversion to the old loop-skepticism framing**. |
| zhang2026makesllmgoodoptimizer | arXiv 2604.19440 | yes (200) | no | CONFIRMED | Matches (Xinhao Zhang, Chen, Portet, Peyrard; 21 Apr 2026). Cited: "finds strong LLM optimizers act as \emph{local refiners}". Abstract: "strong LLM optimizers behave as local refiners, producing frequent incremental improvements while progressively localizing the search in semantic space". Ledger item 21 fix landed. Identical in short variant. |
| zhang2026rethinkingcodesimilarityautomated | arXiv 2603.02787 | yes (200) | no | CONFIRMED | Matches (Rui Zhang, Zhichao Lu). **Method name check** (the ledger-item-24 failure mode): the manuscript's shorthand "BehaveSim" *is* the source's own method name — abstract: "We propose BehaveSim, a novel method to measure algorithmic similarity". Placement under proposer skepticism is supported: the paper's premise is "distinguishing genuine algorithmic innovation from mere syntactic variation". Identical in short variant. |
| zhang2026testingfrontierlargelanguage | arXiv 2607.00276 | yes (200) | no | **PLAUSIBLE** | Id/title/author/year match (single author Dong Zhang). Cited twice for preregistration. Abstract confirms "locked pre-registrations", but the manuscript's tricolon assigns it, by position, to "agent protocols"; the source preregisters a *staged physics-diagnostic protocol*, not an agent protocol. See Finding C-2. Same in short variant. |

## 3. Verified orderings and numeric records (§1 scoreboard)

The task flagged numeric records and above/below orderings for special
attention. Two of the three scoreboard sentences fall in this shard.

- `sec_intro_task.tex` L25–27 (and `sec_short_intro_task.tex` L26–28):
  "ShinkaEvolve \citep{lange2025...} 2.6359831 (its relaxed-tolerance figure;
  2.6359777 strict), HELIX 2.63598308 \citep{su2026helix...}".
  - HELIX's 2.63598308 is verbatim in the HELIX abstract. **CONFIRMED.**
  - The two ShinkaEvolve figures were cross-checked against the ShinkaEvolve
    full text (`arxiv.org/html/2509.19349v1`) purely to test the ordering claim
    — the key itself belongs to another shard. The source gives the relaxed
    value as **2.635983099011548** (→ 2.6359831 ✓) and the AlphaEvolve
    exact-verification replication as **2.63597770931127** (→ 2.6359777 ✓).
    Both manuscript figures round correctly.
- `sec_related_repro.tex` L8–10 (and short L10–11): "HELIX's figure is
  marginally \emph{below} ShinkaEvolve's relaxed-tolerance figure (and above its
  strict one) while being described as state of the art".
  - 2.63598308 < 2.635983099 → **below**, by ~2e-8. ✓
  - 2.63598308 > 2.63597771 → **above the strict one**. ✓
  - HELIX's abstract does describe its result as "state-of-the-art". ✓
  - **CONFIRMED**, including the "marginally" hedge.
  - Non-blocking nuance for the human pass: ShinkaEvolve reports a *third*
    figure — 2.6359828390115476, its own relaxed solution made exact by
    shrinking each radius by 1e-8 — distinct from the 2.63597771 replication
    run the manuscript calls "strict". HELIX's 2.63598308 sits above both
    exact figures, so the manuscript's ordering holds under either reading;
    only the word "strict" is slightly under-specified.
  - Discrepancy worth relaying to the merge step: paper 2's
    `latex-tmlr/CITATION_AUDIT.md` records ShinkaEvolve's lineage value as
    "2.635983283", which matches neither figure in the ShinkaEvolve text
    (2.635983099 relaxed, 2.635982839 shrunk-exact, 2.635977709 replication).
    **Paper 1's numbers are the correct ones**; paper 2's audit line looks like
    a transcription slip and should be re-checked by whoever owns it.
- ThetaEvolve: "claiming new best-known bounds rather than matching it" —
  CONFIRMED against the abstract (see table). The manuscript correctly does not
  attribute a specific numeric value to ThetaEvolve.

## 4. FINDINGS REQUIRING ACTION

No REFUTED findings in this shard. Two PLAUSIBLE.

### C-1 — PLAUSIBLE — `wang2026diversescientifichypothesissearch` (2606.10587) is filed under proposer skepticism, but it indicts the *search loop*

**Manuscript sentence** (`sec_related_repro.tex` L34–36; identically
`sec_short_related_repro.tex` L38–39):

> "Converging skepticism about what the proposer contributes comes from
> ``Dictionaries, Not Darwin'' \citep{li2026dictionariesdarwinsetlevelselection},
> \citet{wang2026diversescientifichypothesissearch}, BehaveSim
> \citep{zhang2026rethinkingcodesimilarityautomated}, Strategy Diversity
> \citep{yang2026accuracyevaluatingstrategydiversity}, the bin-packing critiques
> \citep{herrmann2026indepthstudyllmcontributions,sim2025hypebenchmarkingllmevolvedheuristics}
> and MathConstruct \citep{balunovic2025mathconstructchallengingllmreasoning}."

**Source evidence** (abstract of 2606.10587, fetched 2026-08-28):

> "commonly used evolutionary search recipes tend to prioritize optimization
> over exploration in hypothesis generation, and the resulting **selection
> pressure during the search process** leads to diversity collapse."

The paper's causal attribution runs the other way from the sentence that cites
it: diversity collapse is blamed on the evolutionary *selection pressure*, and
the paper's fix is a parallel-tempering *search* framework — i.e. it is a
result about the loop, and if anything a defence of what a less-greedy loop can
elicit from the same proposer. Nothing in the abstract says the LLM proposer
contributes little. This is the same misfiling shape as ledger item 21
(2407.10873 filed under the opposite argument), in a milder form: the citation
is not contradicted, it is mis-grouped.

**Also note**: the manuscript's own diversity-collapse paragraph, two sentences
earlier, is exactly where this source belongs.

**Suggested fix** — move it out of the skepticism list and into the
template-convergence/diversity-collapse discussion, e.g. after the "Artificial
Hivemind" sentence:

> "...at survey scale. \citet{wang2026diversescientifichypothesissearch} locate
> the same collapse inside the evolutionary loop itself, attributing it to
> selection pressure and mitigating it with multi-temperature search."

Then drop it from the "converging skepticism" list, which is well supported by
its remaining members. **Needs a human full-text read** only if the authors
prefer to keep it in the skepticism list — in that case they must point to a
specific in-paper result about proposer contribution (not present in the
abstract) and cite it by section.

### C-2 — PLAUSIBLE — `zhang2026testingfrontierlargelanguage` (2607.00276) is positionally assigned to "agent protocols"

**Manuscript sentence** (`sec_related_repro.tex` L69–71; identically
`sec_short_related_repro.tex` L64–65; the same list appears compressed in
`sec_intro_task.tex` L52–53 and `sec_short_intro_task.tex` L51–53):

> "\citet{thomas2026mitigatingllmbasedphackingpreregistering},
> \citet{williams2026predictingllmsafetyrelease},
> \citet{vaccaro2026preregistrationexperimentsaiagents} and
> \citet{zhang2026testingfrontierlargelanguage} preregister recipes,
> outcome-blinded predictions and agent protocols"

**Source evidence** (abstract of 2607.00276):

> "The diagnostic combines **locked pre-registrations**, fresh sessions between
> stages, dual-LLM judging, and a human-audit pathway, and we apply it to three
> parallel physics worlds..."

The *preregistration* attribution is solidly supported — "locked
pre-registrations" is explicit, and this paper is arguably the closest lineage
member to the manuscript's own practice (locked predictions, fresh sessions,
held-out container). The soft spot is purely the tricolon: four citations are
mapped onto three nouns, and by position the fourth citation inherits "agent
protocols", which belongs to Vaccaro. 2607.00276 preregisters a four-stage
physics *diagnostic* protocol for frontier LLMs, not an agent-experiment
protocol.

**Suggested fix** — make the mapping explicit rather than positional:

> "\citet{thomas2026mitigatingllmbasedphackingpreregistering} preregisters the
> analysis recipe and the eligible future model,
> \citet{williams2026predictingllmsafetyrelease} registers outcome-blinded
> predictions, \citet{vaccaro2026preregistrationexperimentsaiagents} proposes a
> preregistration template for agent experiments, and
> \citet{zhang2026testingfrontierlargelanguage} locks a staged diagnostic
> protocol before running it;"

This is a low-severity wording fix, not a factual defect; no numeric or
directional claim depends on it. **Needs a human read** only to confirm the
authors are content with the reassignment.

## 5. Non-arXiv references in this shard

**None.** All 18 entries in the shard are `@misc` arXiv preprints and were
verified directly against `arxiv.org/abs/<id>`.

Two minor metadata observations, neither affecting resolution or any claim:

- `vanstein2025llamealargelanguagemodel` (2405.20132) — bib `year={2025}`; arXiv
  v1 is 30 May 2024, v4 is 30 Jan 2025. The 2025 year tracks the latest
  revision (and the journal version, van Stein & Bäck, IEEE TEVC), so it is
  defensible, but note that other bib entries in this file key the year to v1.
  If the file's convention is v1-year, this should read 2024. Purely a
  consistency question.
- `vaccaro2026preregistrationexperimentsaiagents` (2606.11217) — the arXiv
  listing page reads "[Submitted on 3 May 2026]" while the identifier is a
  2606 (June 2026) id. This is an inconsistency on arXiv's side, not in the bib
  entry; the id resolves, the title and sole author match, and `year={2026}` is
  correct either way. No action.

## 6. Method notes

- All 18 abs pages fetched over the session proxy with `curl`; all returned
  HTTP 200 on the first attempt. No retries were needed and no fetch failed, so
  there are no UNVERIFIED rows.
- Withdrawal was checked by scanning each fetched page for withdrawal markers
  and by reading the submission-history block; no entry shows a withdrawn
  version.
- Claim checks are based on the arXiv abstract unless stated otherwise. The one
  full-text fetch this pass was `arxiv.org/html/2509.19349v1` (ShinkaEvolve),
  used solely to adjudicate the HELIX ordering in §3; ShinkaEvolve's own bib key
  is outside this shard and was not audited.
- No `.bib` or `.tex` file was modified; this file is the only write.
