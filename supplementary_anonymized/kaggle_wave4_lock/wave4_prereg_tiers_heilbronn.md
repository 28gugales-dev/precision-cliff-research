# Wave 4 preregistration — capability-tier control on the Heilbronn task

**Status: DRAFT, NOT YET LOCKED.** This document becomes a registration when its SHA-256
is published and pushed to an externally-timestamped host *before* any tier row is
sampled. Until then it is a design note.

**Written:** 2026-08-08, against paper 2 at commit `8417bfb` (v42), while wave 3
(`wave3_prereg_heilbronn.md`) is executing on Kaggle and before any of its rows have been
read.

**Author:** *(unresolved — same outstanding item as wave 3; this wave inherits wave 3's
caveat verbatim: citable as a timestamped registration, not as a complete lock.)*

---

## 1. What this wave exists to test

Every ladder result in §3 varies precision while holding the model fixed. A critic can
still say: *echo is what any sufficiently weak proposer does; you have shown a weak-model
artifact, not a precision artifact.* No experiment in either paper varies capability while
holding the precision axis out of the design. This wave does.

Three hosted capability tiers — `haiku`, `sonnet`, `opus` — run the identical Heilbronn
n=13 lineage protocol wave 3 is running on the GGUF ladder. The tiers form a capability
ladder with **no quantization axis under our control**. If echo tracks capability, the
weakest tier should echo at rates resembling Q2_K. If echo is precision-specific, no tier
should — *over the capability range these tiers span*, which is the only range the wave
can speak to.

Both outcomes bind:

- **Weak tier echoes like Q2_K** → the capability confound is live; §3's attribution must
  be rewritten as a disjunction (precision *or* capability gates departure), and this
  document commits to that rewrite before the outcome is known.
- **No tier echoes like Q2_K** → echo dissociates from capability over the sampled range.
  That bounds the confound; it does not eliminate it below the range, and the paper must
  say "over the tiers sampled", not "capability is excluded".

## 2. What the tiers are, and what they are not

Tiers are requested by **explicit model parameter** on the agent runtime — not by alias.
This is the distinction §4 turns on: an alias's referent drifted within six days (§4.1);
a pinned model parameter names a tier family, which is weaker than naming weights but
stronger than an alias. Each row records the exact model string requested and any model
identifier the runtime reports back. The following remain unattested, and every claim in
this wave is scoped by them:

1. **Served precision is unattested** (C3). We cannot verify what precision any tier is
   served at. The wave tests the *capability axis as the runtime exposes it*, not
   "full-precision models" — the paper must not describe the tiers as full-precision
   comparators.
2. **Sampling parameters are unattested.** The GPU ladder runs T=0.8, top_p=0.95. The
   agent runtime exposes no temperature control. Tier rows and GGUF rows are compared on
   echo — a discrete, parameter-robust measure — never on any statistic that presumes
   matched sampling.
3. **One serving path per tier.** Rows within a tier share whatever infrastructure served
   that tier that day: pseudoreplication for any serving-level question, exactly as arm R
   disclosed. Lineage-level tests remain valid for between-tier behavioural comparison;
   nothing here supports inference about serving infrastructure.
4. **Date-bound.** §4.1 showed same-alias behaviour moving within six days. Every row
   carries its date; claims are about the tiers as served on the sampled date(s).
5. **Harness context differs from the GPU ladder.** Subagent invocations carry a system
   prompt and tool harness the GGUF calls do not. The prompt body (task, parent, output
   format) is byte-identical to wave 3's; the wrapper is not, and cross-substrate
   comparisons are behavioural, not mechanistic.

**Tool policy, registered because the harness is the instrument.** GGUF calls are pure
text completion; a subagent with tool access could run an optimizer and return a
genuinely optimized configuration, measuring the harness rather than the proposal
distribution. Rule, matching the arm B2 / arm R protocol whose ledgers carry `tool_uses`
per row: the dispatch prompt forbids tool use and demands a direct answer; `tool_uses` is
recorded per row; **any row with `tool_uses` > 0 is excluded from every registered
outcome and reported separately with its count.**

## 3. Protocol

Identical to wave 3 wherever the substrate permits, by construction:

- **Task:** Heilbronn triangle, n=13, unit square. Score = minimum triangle area over 286
  triples. Same evaluator code as wave 3's runner.
- **Seed parent:** the SAME fixed 13-point configuration wave 3's runner hard-codes
  (`SEED_PARENT`, score 0.009087361292500006), extracted from
  `sec3_artifacts/runners/kaggle_precision_sweep_14b_heilbronn.py` programmatically — not
  retyped — so the two waves share one origin and one echo referent class.
- **Lineage loop:** hill-climb, strict improvement, running parent shown in the prompt,
  acceptance decided by the evaluator, never by the model.
- **Validity / viability / echo:** wave 3 §2's definitions verbatim. Echo = emitted point
  set equals the lineage's running parent, order-insensitive, at 6 dp.
- **Logging:** wave 3 §6b's conventions verbatim — scores at 12 dp, coordinates
  canonicalised to 6 dp before scoring, `echo` against the running parent, `score_delta`
  against the fixed seed. Each row additionally carries `tier` (requested model string),
  any runtime-reported model identifier, `tool_uses`, `duration_ms`, `subagent_tokens`,
  and `date`.

## 4. Allocation

| tier | lineages | generations | calls |
|---|---|---|---|
| haiku | 8 | 5 | 40 |
| sonnet | 8 | 5 | 40 |
| opus | 8 | 5 | 40 |

120 calls total, symmetric, because the primary is echo (per-call) rather than accepted
steps (per-lineage-trajectory): five generations is thin for trajectory statistics and
adequate for echo counts, and the registration below binds echo and leaves trajectory
measures descriptive. Eight lineages rather than wave 3's larger allocation is a token
budget decision made and registered before sampling; the 5.1 power floor below is set
against this allocation.

## 5. Registered predictions and decision rules

**5.1 — PRIMARY. Echo among valid outputs, per tier.** Estimator: the **pooled per-tier
fraction** — echo rows over valid rows across all 40 calls of the tier — the same form as
wave 3's 5.4. Calls within a lineage are dependent (each conditions on the running
parent), so the pooled fraction is pseudoreplicated at lineage level; per-lineage echo
fractions are reported alongside as an unregistered robustness descriptive, and the
dependence is disclosed wherever the pooled figure is cited.

Bound, under the paper's precision-specific reading: **every tier ≤ 30%** — inherited
from wave 3's 5.4 Q4_K_M bound, the registered non-collapsed-class figure *on this task*
(§3's circle-packing registration used 35%; the task-matched bound is the right
inheritance and the stricter of the two, which is the conservative direction for the
dissociation branch).

**Prior state of this question, computed before lock (wave 3 §5.3's standard).** The
corpus contains hosted-tier loop ledgers from the companion paper's swarm arms, on circle
packing, 2026-07: `agent-run/candidates_v2.jsonl` (unit_sonnet 50 rows, rect_haiku 50),
`candidates_v3.jsonl` (prog_haiku 50), `candidates_v4.jsonl` (n_generality haiku 100,
n=23, coordinates stored), plus one-shot arms (arm F 215 rows; arm B2 30 — no parent in
prompt, echo undefined there). The one arm whose ledger stores coordinates supports a
true coordinate-echo computation: reconstructing each lineage's running parent from
stored configurations and the strict-improvement rule gives **haiku coordinate echo
7/41 = 17%** among valid rows (echo evaluable only after a lineage's first acceptance;
the seed parent's coordinates are not in that ledger). The v2 arms store no coordinates;
their score-tie-with-parent fractions (sonnet 29/50, haiku 33/46) are **upper bounds
only** — §3's own coordinate check reclassified 4 of 12 score-inferred echoes as
rearrangements, and packing's lumpy score support makes ties uninformative. The
computable prior therefore sits at 17% for the weakest tier on a different task —
consistent with, and not the source of, the 30% bound, which is inherited from the
task-matched wave 3 registration.

**DECISION RULE, all branches written before sampling:**

- All three tiers ≤ 30% → dissociation over the sampled range. §3's attribution survives
  this test of its strongest alternative, with §1's range scoping attached.
- Any tier ≥ 55% (wave 3's Q2_K-class bound) → the capability confound is live. §3's
  attribution is rewritten as a disjunction, per §1.
- Any tier in (30%, 55%) → partial; reported as such, no branch claimed, and the paper
  gains a caveat rather than a result.
- **Power floor:** a tier with fewer than 20 valid outputs is labelled UNDERPOWERED and
  excluded from every branch. 40 calls per tier makes this unlikely (arm B2's single
  tier produced 30/30 valid on the harder packing task) but wave 2 taught us to write
  the clause before needing it.

**5.2 — SECONDARY. Monotonicity over the unambiguous ordering.** Capability rank
haiku < sonnet < opus is taken from the vendor's own tier naming and positioning; no
finer ordering is assumed. Under the precision reading, echo should NOT decrease strictly
monotonically with rank. A strict monotone decreasing gradient is evidence *for* the
capability confound even if no tier crosses 55%. Exact permutation on tier rank, reported
with its tail. **Count floor:** if total echoes across the three tiers number fewer than
10, this check is labelled NOT EVALUATED — a monotonicity verdict on tie-noise is not a
verdict.

**5.3 — Template check.** Fraction of valid outputs scoring exactly 0, per tier,
reported with no bound — wave 3 §5.5's clause, same rationale.

**5.4 — Descriptives, no bounds.** Accepted steps per lineage, conditional-on-departure
improvement rate, final best score per lineage — all reported per tier with exact tails
where a test is defined, none registered, because no prior tier data on this task exists
and inventing bounds would manufacture registrations. Wave 3's 5.6 states the same
principle.

## 6. Disconfirmation

If 5.1's confound branch fires (any tier ≥ 55%), the paper's §3 attribution sentence is
rewritten as a disjunction and §8 gains the capability-confound entry as a *finding*
rather than a limitation. We commit to that rewrite here so the commitment predates the
outcome. If the dissociation branch holds, the result enters §6 as a bound on the
capability alternative over the sampled tier range — with every scope limit in §2
attached, and without the word "excluded".

## 7. Analysis, fixed in advance

A no-argument script released with the wave replays every count from the raw ledger:
validity, echo (pooled and per-lineage), tool-use exclusions, zero-score fraction,
per-tier tables, the 5.2 permutation, and every verdict label — held, refuted, partial,
underpowered, not-evaluated — printed by the script, not written by us. Same standard as
wave 3 §7.

## 8. What this wave does not answer

Hosted tiers are not a precision ladder, and nothing here measures precision. The wave
tests one alternative explanation for §3's echo result, on one task, on one date, through
one harness, over one vendor's tier range. It cannot attribute any tier's behaviour to
any serving property (C3), and it says nothing about the GGUF ladder beyond supplying its
comparator.
