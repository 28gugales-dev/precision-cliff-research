# Paper 1 — draft sections 1, 7, 8, 9

*(Drafted 2026-08-01. Citation set restricted to `kill_check_2026-08-01.md` and
`lit_sweep_2026-08-01.md`. Sections 2–6 drafted separately.)*

---

## 1. Introduction

Ask a language model to place 21 circles in a unit square so as to maximise the sum of
their radii, and it will not search. It will reach for the nearest square grid — five by
five, every circle of radius 1/(2k) — and then truncate that grid to the 21 circles it
was asked for, leaving the four freed cells empty and their area unclaimed. The four
discarded cells are not a rounding artefact; they are where the value went. A better
construction is one parameter away: drop to a four-by-four grid and add corner fillers of
radius (√2−1)/(2k), or keep the five-by-five spacing and enlarge, and the sum of radii
rises. The model does neither. It emits the truncated template, and it does so again on
the next sample, and on the sample after that.

The behaviour is regular enough to be written down. A selection rule k\* = round(√N),
combined with a value function V(k, m) over grid order k and filler count m, predicts the
exact sum of radii the model will emit — to seven decimal places, from the problem
parameters alone, before any sampling occurs. The rule also predicts where it will hurt.
When k\*² ≤ N the model extends the grid with fillers and converges toward a reasonable
construction; when k\*² > N it truncates, and value is lost. These *trap zones* —
N ∈ [13,15], [21,24], [31,35], [43,48], [57,60] — are a property of the rounding rule, not
of the packing problem, and they are visible in the output before a single token is drawn.

This matters because circle packing is not an arbitrary probe. It is the showcase
benchmark of the LLM-driven discovery literature: the task on which AlphaEvolve reported
2.635 for n = 26 and on which a succession of systems have since reported essentially the
same number — ShinkaEvolve at 2.635983283, HELIX at 2.63598308 (2603.07642), GigaEvo at
2.636 (2511.17592), AdaEvolve at 2.636 (2602.20133), with SeaEvo (2604.24372) and
ThetaEvolve (2511.23473) in the same band. Those systems place a language model in a
proposal role inside an evolutionary loop, on the working assumption that its outputs
constitute a diverse exploration of the solution space. We test that assumption on their
own home benchmark, in the simplest possible setting — a single zero-shot call, no code
execution, no loop — and find the proposal distribution to be a template lookup with a
closed-form output.

Three framing commitments deserve stating up front, because they are context for the
result rather than parts of it. First, behavioural anchoring in language models is
established territory: the literature has documented numeric priming and estimate-dragging
in scalar settings, and we inherit that vocabulary rather than extend it. What differs
here is the modality — the anchor is a *construction template*, not a number, and the
quantity dragged toward it is a geometric layout. Second, the benchmark choice is
strategic rather than novel: we deliberately run on the task the discovery-systems
literature already treats as its exemplar, so that a negative characterisation of the
proposal distribution lands where it is load-bearing. Third, preregistration is by now an
adopted standard for LLM experiments rather than a contribution
(2606.27687; 2607.07184; 2606.11217; 2607.00276); our only twist is what is locked — we
hash-lock exact-output point predictions derived from a closed form, on a held-out
container, rather than the directional or aggregate hypotheses that concurrent work such
as HindsightBench (2607.18867) freezes.

**Contributions.**

1. **A closed form that predicts exact model output.** We give a selection rule
   k\* = round(√N) and a value function V(k, m) that predict the precise sum of radii a
   model will emit for a given N, verified against a linear-programming oracle on 83
   configurations to within 1e-9, and confirmed out of sample on two containers — a
   square, and a rectangle to which the rule was restated (q\* = round(√(N/a)),
   p\* = round(√(N·a))) but never refitted. To our knowledge no prior work predicts a
   specific multi-decimal model output from problem parameters ahead of sampling.
2. **A tier inversion in constructive ambition versus execution.** Across three model
   tiers we observe three distinct attractor families and a monotone inversion:
   constructive ambition rises with nominal tier while execution validity collapses
   (71% → 100% → 13%). The most ambitious tier attempts recursive gaskets and
   quarter-circle constructions and mostly fails to produce a non-overlapping packing at
   all.
3. **Trace elicitation as an intervention, not an observation.** Asking a model to name
   its method before answering measurably concentrates its output onto the memorised
   template (87% vs 70% on-prediction, p = 0.033) while leaving validity statistically
   unchanged. Any study that collects process descriptors *by request* is therefore
   measuring a perturbed distribution, and we name the confound rather than assume it away.

**Non-claim guard.** Everything reported here is a behavioural regularity over emitted
outputs. We make no claim about mechanism inside the weights — no assertion that a
template is stored, retrieved, or represented in any particular way, and no claim that a
prompt constraint acts on internal coordinates. The closed form describes what comes out,
not what happens inside.

---

## 7. Related work

### 7.1 LLM-driven discovery systems and the saturation of circle packing

Placing a language model in the proposal role of an evolutionary loop has an established
lineage in the evolutionary-computation community: Language Model Crossover (Meyerson et
al., ACM TELO 2023) framed the LLM call as an EC operator, ELM (2206.08896) paired LLM
mutation with MAP-Elites, EvoPrompt realised GA and DE operators through model calls, and
LLaMEA (2405.20132) carried the pattern into algorithm design. Circle packing became the
public scoreboard of this line. AlphaEvolve's 2.635 at n = 26 was followed by
ShinkaEvolve's 2.635983283, HELIX's 2.63598308 (2603.07642), GigaEvo's 2.636 (2511.17592),
AdaEvolve's 2.636 (2602.20133), and further entries from SeaEvo (2604.24372) and
ThetaEvolve (2511.23473). The spread across systems is smaller than the systems'
architectural differences, which is itself informative: the benchmark is saturated at the
reporting precision these papers use.

Two critiques of that scoreboard bear directly on our framing. Gideoni, Risi and Gal
(2602.16805) show that simple baselines recover much of the reported advantage, and
Berthold et al. (2605.04850) show that classical solvers do so as well — the two critiques
are independent and are frequently conflated, so we note the attribution explicitly. Both
ask whether the *system* is adding what its headline number implies. We ask a prior
question: what does the LLM component actually propose when queried directly? Our answer —
a truncated grid template whose value a formula anticipates — supplies a mechanism-free
account of why saturation looks the way it does, and of what the loop's selection pressure
is filtering.

### 7.2 Template convergence and diversity collapse

The closest cousin to our result is "Mutation Without Variation" (2606.05408), which finds
that iterated LLM program mutation collapses onto previously seen structural templates —
87% of chains and 93% of mutations revisit prior form. That is the same bias family in a
different regime: mutation loops rather than single calls, program space rather than
geometry, and no closed form or preregistration. It corroborates rather than scoops.
Nearer still in benchmark terms, 2605.29268 reports asymmetric proposal mass on this same
task in program space — corroborating evidence in a different modality, which is why our
zero-shot, no-code setting is worth reporting separately: the anchoring is not an artefact
of the code-generation channel.

A broader skeptical literature converges on the same worry from several directions.
"What Makes an LLM a Good Optimizer" (2604.19440) and "Dictionaries Not Darwin"
(2607.04108) question whether the model contributes search or retrieval; EvoDiverse
(2606.10587) measures diversity directly; the bin-packing critiques (2510.27353;
2501.11411) show reported gains on a second combinatorial showcase to be fragile; and
2407.10873 isolates how much of the performance is attributable to evolutionary search
rather than the proposer. MathConstruct (2502.10197) makes the complementary point in the
constructive-mathematics setting, where a model must *build* an object rather than select
an answer. Our contribution to this cluster is specificity: not that diversity is low, but
that the concentration point is identifiable in advance and its value computable.

### 7.3 Scaling inversions

The tier inversion we report has precedent outside constructive geometry. Zhou et al.
(*Nature*, 2024) show that larger and more instructable models become less reliable —
attempting more and erring more in a QA regime — and the o3/o4-mini system card documents
the same shape on PersonQA, where more claims accompany more hallucinations. "The Illusion
of Thinking" (2506.06941) reports capability collapse past a complexity threshold, and
GeoBuildBench (2605.13167) finds geometric construction to be a regime where nominal
capability and executed correctness diverge. Our contribution is the constructive
instantiation: the inversion is not merely accuracy versus attempt rate but *attractor
family* versus executability — the more capable tier reaches for recursive gaskets and
quarter-circle constructions and then fails to produce a valid layout, while the middle
tier produces perturbed grid hybrids that always validate.

### 7.4 Trace faithfulness, and what our elicitation result is not

**Disambiguation.** A substantial recent literature intervenes *on trace content* and
finds that answers do not move. Reasoning Theater (2603.05488) shows the answer is
decodable from activations before the trace completes; Project Ariadne (2601.02314)
applies hard interventions to trace content and finds answers largely unchanged, quantified
by the Ariadne Score, a measure of Causal Sensitivity. The shared conclusion is causal
decoupling: the trace is not the computation. Our result operates at a different
intervention point. We do not edit the trace; we vary whether one is *requested*, and we
find that the request itself shifts the output distribution toward the memorised template
(87% vs 70% on-prediction, p = 0.033). That is measurement reactivity, not causal
faithfulness, and the two findings are complementary: the decoupling literature says the
trace does not drive the answer, while our result says that asking for a trace nonetheless
changes what is answered. Both must hold for a process-descriptor study to be interpreted
correctly, and neither substitutes for the other.

The closest cousin is "The Price of Format" (2505.18949), which shows that imposing an
output format collapses generation diversity. The differentiator is what is imposed: a
format constraint restricts the *shape* of the answer, whereas our manipulation adds a
one-line request to name a method and leaves the answer format untouched — yet still
concentrates the output. Related reactivity results include the Hawthorne effect in
reasoning models (2505.14617), where test-awareness steers behaviour; Verbalized Sampling
(2510.01171), which treats mode collapse as addressable at the prompt level; and Latent
Memory Anchor (2506.17630). Our setting adds something these lack: the emitted method line
is auditable against the emitted coordinates, so faithfulness is checkable against ground
truth rather than estimated.

### 7.5 Preregistration lineage

Preregistration of LLM experiments is an established and growing practice. Thomas, Gligoric
and Shah (2606.27687) preregister the experimental recipe; "Predicting LLM Safety Before
Release" (2607.07184) files OSF preregistrations of prevalence rates; 2606.11217 adapts the
protocol to AI-agent experiments; and 2607.00276 applies it in a physics-literacy study.
Concurrently, HindsightBench (2607.18867, 2026-07-21) freezes directional aggregate
hypotheses under SHA-256. We adopt this standard rather than claim it. What we add is the
object being locked: exact closed-form point predictions of specific output values, hashed
together with the prompts, and then tested on a container the rule was never fitted to.
The structural precedents for this move come from outside the prereg literature — Kaplan et
al. (2001.08361) and Chinchilla (2203.15556) publish a functional form and then run the
confirming instance, and "Predicting Emergent Capabilities by Finetuning" (2411.16035) is
the closest structural twin: a timestamped preregistered threshold tested on deliberately
excluded models. Related in spirit, MatLLMSearch (2502.20933) reports crowding in an
LLM-driven materials search, and QDAIF (2310.13032) is the QD-descriptor setting most
directly affected by our §5 reactivity finding.

---

## 8. Limitations

**Single vendor.** All model tiers sampled here come from one provider. A cross-vendor arm
was scoped and is blocked on credit rather than on design; we disclose this rather than
generalise past it. The closed form is stated over problem parameters, not over any
vendor's architecture, so it is testable elsewhere — but it has not yet been tested
elsewhere, and the tier-inversion result in particular should be read as a within-family
observation until it is.

**Zero-shot only.** We characterise the single-call proposal distribution and do not rerun
an evolutionary loop. This is a deliberate scope choice — paper 0 found the loop to perform
comparably to best-of-N on this task, so the single-call distribution is the object of
interest — but it means our claims describe what the loop *samples from*, not what the loop
converges to. Selection pressure over many generations may escape the attractor in ways a
single call cannot show.

**Sampling parameters unpinned.** The agent runtime used for collection does not expose
pinned decoding parameters, so temperature and related settings are not fixed across
invocations. Every effect we report is a distributional claim over the observed sampling
regime, not over a specified one. This limitation is the direct subject of the companion
paper (paper 2), which treats runtime nondeterminism as its object; we cross-cite rather
than re-litigate it here.

**opus_alias serving-path confound.** The highest tier is referred to throughout as
`opus_alias` and never by a version number. The label denotes the serving alias we
addressed, not an identified model version: without pinned weights we cannot separate a
model-tier effect from a serving-path effect, and the 13% validity figure is a property of
what that alias returned during our collection window. Any reading of the tier inversion as
a statement about a specific released model would exceed the provenance we have.

---

## 9. Reproducibility statement

Every prompt was hashed with SHA-256 and the hashes were recorded *before* any sampling
occurred, together with the predicted values they were to be tested against. The
preregistration files are in the repository and named: `arm_f_repro.py` (header, predictions
P1–P5, square arm), `arm_s_preregistration.txt` (Sonnet tier), `arm_o_preregistration.txt`
(opus_alias tier), and `arm_t_preregistration.txt` (elicitation arm, prereg hash
`ab7900a8…`). The rectangle transfer was registered before collection and never refitted to
rectangle data (`rect_forecast.py`, `arm_g_rect.py`).

All raw model outputs are stored verbatim, unedited, in the repository
(`arm_f_raw.json`, `arm_f_candidates.jsonl`, `arm_g_candidates.jsonl`), so that any scoring
decision can be re-derived from the original text rather than trusted. Scoring is
deterministic and local: candidate layouts are parsed into coordinates and radii, overlap
and containment are checked at fixed tolerance, and the sum of radii is computed without
model involvement at any stage.

Value claims are gated on an independent linear-programming oracle rather than on the
closed form being tested. The forecast pipeline (`n_sweep_forecast.py`, with
`verify_against_lp`) checks 83 recipe-family configurations against LP-computed values to
within 1e-9, and the same oracle is what produced the negative result we report in §3: the
rectangle filler closed form does not exist, with an LP counterexample at 1.125 against
1.1545085. We keep that negative in the paper because it demonstrates the gate working —
the pipeline aborts on drift rather than fitting through it.

Analysis scripts (`arm_t_analysis.py`), the forecast artefacts (`n_sweep_forecast.json`,
`rect_forecast.json`), and a running experimental log (`STATE.md`) are included so that
each table in this paper can be regenerated from the raw outputs by a single command
documented in `HOW_TO_RUN.md`.
