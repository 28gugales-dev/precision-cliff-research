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
