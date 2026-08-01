# Paper 1 — draft prose, sections 4–6

*Drafted 2026-08-01 against `paper1_anchoring_skeleton.md` §§4–6. Every quantity is
taken from `STATE.md` §§3–4, §§6–9, `arm_t_preregistration.txt`, or `arm_t_analysis.py`.
Citation placeholders are marked `[SLOT: related-work]` and carry no invented references.*

---

## 4. The tier ladder: three attractor families

The selection rule of §2 was identified on, and confirmed out of sample against, a single
proposer tier. Does it describe language models, or one model? Holding prompt, container and
scoring machinery fixed, we varied only the nominal proposer tier across the three cells that
discriminate hardest between the rule's prediction and the recipe family's own optimum —
N = 13, N = 21 and N = 31, each inside a predicted trap zone. The rule turns out to be
tier-scoped, and the tiers do not merely differ in how often they succeed: they attempt
qualitatively different constructions. We report them as three attractor families rather than
three points on an accuracy axis.

**The weak tier truncates templates.** The Haiku-tier proposer produces uniform grids of
radius 1/(2k) truncated to N circles, with corner fillers added only when the grid
underfills. Across the 45 bare invocations logged in the arm-F ledger — spanning
N ∈ {13, 17, 21, 31, 35, 37, 43} — 32 were geometrically valid (71%). At the three
discriminating cells, 12 of 16 valid samples landed on the predicted value and the
higher-scoring rival was reached twice, both times at N = 21 — the behavior the closed form
of §2 anticipates, and the baseline for the other two tiers.

**The middle tier perturbs and mixes.** The Sonnet-tier proposer was preregistered in
`arm_s_preregistration.txt`, disclosing that 5 of 20 samples at N = 13/21 had been seen
before registration and that N = 31 was fully blind. It was valid in 30 of 30 invocations
and almost never on-prediction: 0/10 at N = 13, 0/10 at N = 21, 1/10 at N = 31 — 1/30
pooled, against the Haiku tier's 12/16 at the same cells. Instead of truncating a uniform
grid it perturbs one, with enlarged edge rows, hexagonal interior rows and two or three
distinct radii in the same packing (29/30 multi-radius, against a same-metric Haiku baseline
of 13/35). It reaches the higher-scoring rival 6 times in 30, including 3/10 at N = 13 and
3/10 at N = 31, where Haiku reached it zero times in nine invocations. At N = 21 its values
lie between 2.14 and 2.25 — all above the 2.1 trap, none on the 2.2588835 rival: it escapes
the trap without finding the recipe family's optimum.

One Sonnet sample at N = 31 emitted 27 circles at r = 1/12 with 4 corner circles at r = 1/8,
summing to 2.75 — above 2.7485281, the best value the recipe family reaches at that N.

<!-- Slack verified 2026-08-01 by direct recomputation from arm_f_candidates.jsonl
(sonnet_bare, N=31, sid=2): min pairwise slack 0.000e+00, min wall slack 0.000e+00,
sum of radii 2.7499999991. Tangency-tight, zero violations at tol=0. -->

Recomputed directly from its stored coordinates, the construction is tangency-tight: minimum
pairwise slack and minimum wall slack are both exactly zero at tolerance zero, with sum of
radii 2.7499999991. It is the only sample in the study to leave the recipe family upward,
something no Haiku sample did in 101 invocations. The recipe is an attractor, not a ceiling.


**The top tier attempts recursive constructions and fails to build them.** The third arm was
invoked through the alias `opus`. We name it `opus_alias` throughout and make no claim about
which weights served it: the agent runtime accepts only the bare alias and exposes no dated
model identifier, so the alias-to-weights binding is a vendor promise rather than an
attestable fact, and this arm must not be read as a statement about any specific model
version. Two anomalies make the caveat load-bearing. Completion times ran 2.8–9 seconds
across all 30 invocations, against 75–250 s for Haiku and 150–1170 s for Sonnet, a profile
consistent with a fast-decode serving path; and the reported token count was uniform at
49,906 across the first 20 completions and stayed at ≈49.9k for the rest. Both are
consistent, not intermittent.

Under those caveats, the arm — preregistered fully blind in `arm_o_preregistration.txt`
(sha256 21171…738) — was valid in 4 of 30 invocations (13%). At every cell it attempted a
construction more ambitious than either other tier: at N = 13, four quarter-circle corners
at r = 0.25 with Apollonius-style centre, edge and corner fillers, the same family in 10/10
samples; at N = 21, mixed-radius 4×4-ish grids with corner and edge fillers; at N = 31, a
coarse 3×3 grid at r ≈ 1/6 with border strips and interior fillers, 0/10 valid, every sample
breaking tangency somewhere. The failures are geometric rather than numerical — edge strips
at r = 0.03 placed 0.138 from an r = 1/6 grid circle needing 0.197 — and twice the arm padded
to the required count with zero-radius circles, caught by the nonpositive-radius gate. Valid
samples score *below* the trap they were expected to fall into (1.26–1.41 at N = 13 against a
trap value of 1.625). Registered predictions P-O1, P-O2 and P-O4 are reported as not
evaluable: a validity collapse of this size makes a tier comparison on on-prediction rates
dishonest rather than merely noisy, and P-O3 is trivially satisfied on 4/4 valid samples. The
registered disconfirmation — regression toward the trap — did not occur; the arm fell off a
validity cliff attempting a harder family.

[TABLE 2: three-attractor ladder. Columns: `tier` (haiku / sonnet / opus_alias — footnote
the alias-provenance caveat on the third row) | `cells` | `n invocations` | `attempted
construction family` | `valid / n (%)` | `on-prediction` | `rival-argmax hits` |
`characteristic failure mode`. Sources: `STATE.md` §§6–8b, `arm_f_candidates.jsonl`,
`arm_s_preregistration.txt`, `arm_o_preregistration.txt`.]

<!-- CONFLICT: STATE.md §8 states the opus_alias arm is "excluded from the tier ladder";
§8b, written after the arm completed, tabulates it directly against the other two tiers
("valid 4/30 (13%) vs Haiku 32/45 (71%) vs Sonnet 30/30 (100%)"). Following the later
entry: included in Table 2, with the caveat carried in the row label. -->

Two asymmetries carry through to §8: the Haiku denominator spans seven values of N against
three for the other tiers, and the serving-path and model-tier readings of the third arm are
inseparable without a pinned-weights run the runtime does not permit.

The ladder shows one inversion. Constructive ambition rises monotonically with nominal tier —
truncated template, perturbed hybrid, recursive gasket — while execution validity does not:
71%, then 100%, then a collapse to 13%. At the canonical, plausibly contaminated cell N = 26
all tiers converge on the same 2.5414 attractor; they diverge only at withheld trap cells.
The nearest-square rule of §2 is therefore a weak-tier law, and the tier contrast is a second
observation rather than a caveat on the first: the 2.5414 attractor is tier-shared, the
truncation trap tier-specific.

---

## 5. Elicitation as intervention

The cleanest result in this section is a negative one, and we lead with it because the
design was built to produce exactly this outcome if the pilot had been noise.

A ten-versus-ten pilot at N = 21 compared the bare prompt against a variant asking the
proposer to name its construction on a leading `METHOD:` line. It showed two effects, both
against the naive expectation that a label is free: validity rose from 7/10 to 10/10, and
the higher-scoring rival construction disappeared entirely, from 2 of 7 valid bare samples
to 0 of 10 trace samples. Taken at face value, that pair would have supported a strong
claim — that asking for a method statement makes a proposer both more reliable and more
conservative.

We did not take it at face value. Before any scaled sample was drawn we registered four
predictions and an explicit falsifier in `arm_t_preregistration.txt` (sha256 ab7900a8…),
together with a disclosure that the pilot's trace prompt had drifted from the bare template
beyond the method line itself: it omitted the `[0,1]x[0,1]` tokens and reworded the
output-format line, so the pilot's intervention was method-line-plus-rewording, bundled.
The scaled trace prompt, `trace_v2`, is a minimal diff against the bare template — one
inserted `METHOD:` line and three words prepended to the output line. Pilot samples are
never pooled with `trace_v2`, and the pilot is reported as a pilot.

At scale the pilot's two headline effects died.

The scaled arm ran 100 new invocations, bringing both arms to 20 samples per cell at
N ∈ {13, 21, 31}; all six prompt variants were SHA-256 hashed before sampling and the raw
completions stored verbatim, taking the corpus to 215 logged invocations. Scoring used
`arm_f_repro.py` unchanged with the registered 2 × 10⁻³ value window, and the Fisher exact
test is computed directly from the hypergeometric tail in `arm_t_analysis.py` rather than
imported, so the analysis cannot drift with a library version.

**P-T1, validity: not confirmed.** The direction held at all three cells — trace_v2 at least
as valid as bare at 13, 21 and 31 — but the pooled one-sided Fisher test gives p = 0.30. The
registered falsifier (trace_v2 validity at or below bare at two or more cells) was not
triggered, so we do not conclude that the pilot's validity effect was purely the bundled
rewording, only that it is not detectable at 20 per arm per cell.

**P-T2, rival suppression: not confirmed.** Rival hits were 1 of 53 valid trace_v2 samples
against 2 of 50 valid bare samples, p = 0.48: the pilot's apparent suppression was an
artifact of how rare the rival is in *both* arms at this sample size. One trace_v2 sample at
N = 31 hit the rival value 2.7485281 exactly — the first Haiku-tier rival hit at N = 31 in
any arm of the study.

**P-T3, anchor concentration: confirmed.** Among valid samples, 46 of 53 trace_v2
invocations (87%) landed on the registered nearest-square prediction, against 35 of 50
(70%) in the bare arm; one-sided Fisher p = 0.0325.

<!-- CONFLICT: skeleton §5 and paper1_abstract.md both give p = 0.033; STATE.md §9 gives
p = 0.0325. Same test, same table — this is rounding, not disagreement. Evidence-file
value used here; the abstract's rounded form is consistent. -->

**P-T4, faithfulness: confirmed.** 38 of 41 scoreable method claims matched the emitted
layout (93%), against a registered threshold of 90%. Section 6 treats this result on its
own terms.

[TABLE 3: paired trace grid. Columns: `N` | `arm` (bare / trace_v2) | `n invocations` |
`valid` | `on-prediction` | `rival-argmax`, with pooled totals and the P-T1/P-T2/P-T3
Fisher p-values as table notes; the pilot reported in a separate, clearly-labelled block
that is never summed into the totals. Source: `STATE.md` §9, regenerated by
`arm_t_analysis.py`.]

The claim we draw is narrower than the pilot's and, we think, more interesting. A minimal
method-naming request does not make the proposer better at geometry and does not measurably
change which rare constructions it reaches. What it does is concentrate the output
distribution onto the template anchor, making the model more likely to emit the very
construction the closed form of §2 predicts. Eliciting a trace is a mild commitment device:
a request for a nameable method selects for nameable constructions, and the nearest-square
truncated grid is the most nameable object in this space.

Two implications follow. Trace-on and trace-off samples must never be pooled, here or in any
study mixing prompts that differ by a reasoning-elicitation line. And any work collecting
process descriptors *by asking for them* — including descriptor-driven quality-diversity
pipelines, where a behavioural descriptor is often obtained by requesting a self-report — is
measuring a perturbed distribution, perturbed in a direction that specifically favours the
memorized template [SLOT: related-work — QDAIF / quality-diversity descriptor line]. We name
this confound because our own pipeline was going to rely on it; it is now measured rather
than assumed, and the measurement says the window is not neutral glass.

One bookkeeping note from the same harvest: two bare samples emitted fraction literals
(`1/12`) and failed the §A.5 parser, logged rather than dropped.

---

## 6. Faithfulness with ground truth

The trace arm creates an unusual auditing opportunity. When a proposer writes
`METHOD: 5x5 grid plus 2 corner fillers` and then emits 27 coordinate triples, claim and
artifact sit in the same completion, and the artifact is fully determined: the radii and
centres say exactly how many rows, how many columns and how many distinct radii were
actually built. The method line is checkable against ground truth rather than against a
plausibility judgement. Our check is deliberately coarse:
`arm_f_repro.trace_faithfulness()` extracts the numeric dimensions named in the method
line — row and column counts, grid order, filler counts — and asks whether the emitted
layout signature contains them, recording claims with no numeric content as unscoreable
rather than scoring them generously.

In the pilot, 8 of 8 scoreable traces matched, 2 unscoreable for lack of numeric dimensions.
The most informative match cost the proposer value: a sample claiming `Triangular hexagonal
packing with 6+5+4+3+2+1 rows` emitted exactly that — 21 circles at r = 1/12, summing to
1.75, below both the 2.1 trap and the 2.2588835 rival. The model described what it built,
including when what it built was bad.

At scale the result holds: 38 of 41 scoreable method claims match the emitted layout, 93%,
clearing the registered 90% threshold. The three mismatches are all the same case, and the
case runs against us in a useful direction. Each is a claim of the form "4×4 grid + 5 gap
circles", where the fillers add coordinate rows that the coarse row/column signature reads as
a violation of the stated grid dimensions. The scorer penalises a claim that is, in fact,
accurate. The conservative scorer therefore undercounts matches, and 93% should be read as a
floor on faithfulness in this setting rather than a point estimate.

This is the check that the chain-of-thought faithfulness literature cannot run. That line of
work must estimate whether a stated reasoning process corresponds to the process that produced
the answer without ever observing the latter, and its methods are consequently indirect —
counterfactual perturbation, hint-insertion, consistency probing
[SLOT: related-work — CoT faithfulness line, incl. 2503.08679, 2606.13603, 2605.29087].
In constructive geometry the emitted coordinates *are* the ground truth for what was built.
Faithfulness becomes a measurement rather than an inference, and on this task, at this tier,
under this elicitation, the traces pass.

We claim no more than the setting supports. The check is coarse and can only falsify claims
carrying explicit numeric dimensions; it verifies that the description matches the artifact,
not that it matches whatever internal process produced the artifact — the non-claim guard of
§1 applies in full. The audit covers one proposer tier and one elicitation prompt, and §5 has
just shown that the prompt itself shifts the distribution being described. What survives is
narrow and load-bearing: in a domain where claims are checkable, the method lines this model
emits are, to at least 93%, true of the object it produced.
