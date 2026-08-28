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
