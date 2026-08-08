# Wave 5 preregistration — the echo primary on a DISCRETE task with no float arithmetic

**Status: DRAFT, NOT YET LOCKED.** This document becomes a registration only when its
SHA-256 is published and the runner carrying these predictions is pushed to an
externally-timestamped host *before* any row is sampled. Until then it is a design note.
Nothing in the paper may cite it as a registration.

**Runner: written and dry-run verified.** `sec3_artifacts/runners/kaggle_precision_sweep_14b_labs.py`
carries every prediction below in its header block, verbatim, in the same form the wave-3
runner carried 5.1–5.6. `python kaggle_precision_sweep_14b_labs.py --dry-run` validates the
evaluator against three hand-computed sequences, the parser (including the `bool`-is-an-`int`
trap), the seed parent against its hard-coded integer energy and merit factor, the parent's
non-degeneracy and improving-flip count, and the worst-value property of the four degenerate
templates, and the hardware-crossing plan of §3b (both rungs on both cards, plus the single-card
fallback) — without downloading a model, touching a GPU, importing `llama_cpp`, or creating a
directory. Verified on a host with no GPU and with `llama-cpp-python` **not installed**.

- runner SHA-256 `d1739f6cf38cc295bf2c0260c5a801c8f134a0e9fdc041747fff2a7b73616e7c`

**To lock, three steps remain, none of them analytic:** resolve the author field; publish this
file's SHA-256; push the runner to an externally-timestamped host before sampling a single row.
Nothing about the design is outstanding.

**Author:** *(unresolved — see the outstanding item in `PAPER2_AND_SCOPE_PLAN.md`)*
**Written:** 2026-08-08, as a sibling of `wave3_prereg_heilbronn.md`. No existing artifact was
edited to create it.

---

## 1. What this wave exists to kill

Paper 2's result is that quantizing the proposer to Q2_K makes it largely stop *departing*
from its parent inside a hill-climbing loop while every pass/fail metric stays healthy. The
evidence is circle packing (§3) and, from wave 3, Heilbronn triangle. A referee can read the
whole thing in one line:

> Two-bit quantization erodes floating-point arithmetic. Circle packing and Heilbronn triangle
> are both float-arithmetic tasks. You have measured arithmetic damage and called it a search
> pathology.

**Wave 3 does not answer this.** Heilbronn removes the *lattice attractor* — its contribution —
but it still asks for real-valued coordinates in the unit square and still scores by
floating-point geometry. It is a second continuous-coordinate task, not a second kind of task.

Wave 5 removes the premise instead of arguing with it. The output alphabet is `{+1, -1}`, the
objective is a sum of squares of integer autocorrelations, and the evaluator performs **no
floating-point arithmetic at all**: the single division that turns the integer energy into a
merit factor is the only non-integer operation in the file, and it happens after scoring is
decided. Acceptance inside the loop compares integer energies. A proposer that has lost float
precision loses nothing on this task. If the departure collapse survives here, the
float-erosion reading is refuted rather than rebutted. If it does not, §5.7 Branch B says in
advance what happens to the paper.

## 2. Task: LABS, low-autocorrelation binary sequence, n = 32

A candidate is a sequence *s* of 32 values, each +1 or −1. With

- *C<sub>k</sub>* = Σ<sub>i=1..n−k</sub> *s<sub>i</sub> s<sub>i+k</sub>* for *k* = 1..n−1
- *E* = Σ<sub>k=1..n−1</sub> *C<sub>k</sub>*²  — the **energy**, an exact integer
- *F* = *n*² / (2*E*) — the **merit factor**, higher is better

Every *C<sub>k</sub>* is a sum of products of ±1 and *E* is a sum of their squares, so both are
integers computed by integer operations. *E* ≥ 1 always, because *C<sub>n−1</sub>* = *s₁s<sub>n</sub>* = ±1
is never zero, so *F* never divides by zero and needs no guard.

Why this task and not another discrete one:

1. **It has a catastrophic default template, and four of them.** The constant sequence (all +1),
   its negation, and both alternating phases all have *C<sub>k</sub>* of magnitude *n − k*, hence
   *E* = Σ<sub>j=1..31</sub> *j*² = 31·32·63/6 = **10416 exactly** — the worst value any length-32
   sequence attains — and *F* = 1024/20832 = 0.0492. This is the exact analogue of wave 3's
   "a regular grid scores exactly 0": it is the property that separates *the proposer copies its
   parent* from *the proposer emits the default template it always emits*. Circle packing could
   not separate those, because the seeded parent **was** the template. `self_test()` asserts the
   10416 value against its closed form and aborts if it does not hold.
2. **It is in the same competence class.** Constructive, value-sensitive, expressible in the same
   output format (one flat Python list), scorable in a few lines, and reachable by the same
   propose-and-accept loop. It is not a harder problem dressed as a generalisation — see §8 for
   the honest statement of where it *is* harder.
3. **The echo test loses its numerical convention.** See §2b.

**Validity** = parses as exactly 32 symbols, each exactly +1 or −1. **Viability** = parses as a
list of numbers of any length. Booleans are rejected explicitly (`bool` subclasses `int` in
Python, so `True` would otherwise read as +1). Floats are accepted only when exactly equal to
±1.0 and are then cast — a conversion, not arithmetic.

### 2b. Echo is exact equality, and this is the methodological point

**Echo** = the emitted sequence is the same list of 32 integers as the lineage's *running*
parent, evaluated before the acceptance update. Order-sensitive, because a sequence is ordered.

Waves 1–4 could not state it that cleanly. Circle packing and Heilbronn both had to
canonicalise real coordinates to 6 decimal places and compare point sets order-insensitively,
which puts a **rounding convention inside the primary metric**. Choose 5 dp and the echo rate
moves up; choose 8 dp and it moves down; the choice was defensible but it was a choice, and a
referee may say the primary is convention-dependent. On a discrete alphabet there is nothing to
round and no tolerance to pick: two sequences are the same list or they are not. **This wave's
primary carries no numerical convention at all.** That is the single largest methodological
advantage of moving to a discrete task, and it is independent of how the wave comes out.

### 2c. Seed parent

A single fixed 32-symbol sequence, published by its literals, its integer energy and its merit
factor in the runner header, identical for every lineage and every rung:

```
[-1, -1, -1, -1,  1,  1, -1,  1, -1, -1, -1,  1, -1,  1, -1,  1,
  1,  1,  1, -1,  1, -1,  1,  1, -1, -1, -1,  1, -1, -1,  1,  1]
```

*E* = **156** (exact integer), *F* = 1024/312 = 128/39 = **3.282051282051282**.

It was produced by a seeded random restart plus a truncated integer hill climb, stopped inside a
pre-set mediocrity band, then filtered for four properties that `self_test()` re-checks at
startup: not a palindrome, not skew-symmetric, longest run ≤ 4, |Σs| ≤ 4, and **at least three
single-spin flips that strictly reduce the energy**, so the reference rung is not started inside
a local optimum. The literals, not the generator, are the registered object.

**Calibration ladder** (energies; lower is better), so the mediocrity claim is checkable rather
than asserted:

| configuration | *E* | *F* |
|---|---|---|
| all +1 / all −1 / either alternating phase | 10416 | 0.0492 |
| median single uniform random draw | ~556 | ~0.92 |
| best of 4,000 seeded random draws | 160 | 3.20 |
| **this seed parent** | **156** | **3.2821** |
| best of 100,000 seeded random draws | 120 | 4.27 |
| 300-restart steepest-descent hill climb | 84 | 6.10 |
| optimum reported in the LABS literature | 64 | 8.00 |

The parent sits at ~41% of the reported optimum — the same mediocrity band wave 3 used (36%) —
with three improving single flips available and the best single flip reaching *E* = 144. **A
lineage gets 15 draws: the best of 4,000 seeded random draws (E = 160) does not reach this
parent**, so a proposer emitting arbitrary sequences will not beat it by luck. The literature
optimum is quoted for orientation only; nothing in `self_test()` and no clause of any decision
rule depends on it.

## 3. Conditions

Identical ladder, inference stack and sampling parameters to wave 3; SHA-256 recorded per weight
file.

| rung | file | lineages | generations | calls |
|---|---|---|---|---|
| Q4_K_M | `qwen2.5-coder-14b-instruct-q4_k_m.gguf` | 8 | 15 | 120 |
| Q2_K | `qwen2.5-coder-14b-instruct-q2_k.gguf` | 25 | 15 | 375 |

Sampling: T = 0.8, top_p = 0.95, max_tokens = 1200, n_ctx = 4096 — wave 3's values, unchanged.

Asymmetric by design and registered rather than discovered, for wave 3's reason: §5.3 needs
departures at the 2-bit rung, and the observed 2-bit departure rate across §3's ladders is
2–16% of calls. At 8% of 375 calls the expected departure count is 30; at the symmetric
allocation it would be 10, the count that made the earlier conditional question unanswerable.

**Seeds.** A published fixed list of 33 values, none used in any prior wave. Prior lineage seeds
anywhere in this repository are 42, 123, 456, 789, 1111, 2222, 3333, 5555, 7777, 9999 (waves 1–2
and the dispersion probes) and 3101–3108 / 3201–3225 (wave 3).

| rung | seeds |
|---|---|
| Q4_K_M | 5101 5102 5103 5104 5105 5106 5107 5108 |
| Q2_K | 5201 … 5225 |

The **derived** generation-seed window is disjoint too, which matters because the runner draws
with `seed = lineage*1000 + gen`: wave 5 occupies 5,101,000–5,225,014, which does not meet wave
3's 3,101,000–3,225,014, does not meet 5555·1000 = 5,555,000, and does not meet the 880,000+*k*
must-differ window.

### 3b. Hardware is CROSSED with the rung, not nested in it

Paper 2 §6 item 4 records per-file throughput orderings that **invert across hardware on
SHA-identical weight files** (P100 against 2×T4). Kaggle serves 2×T4 at 15360 MiB each, and both
rungs fit a single card alone (Q4_K_M 8.99 GB, Q2_K 5.77 GB). A runner that pinned one rung per
card — or that let `n_gpu_layers=-1` split each rung differently — would make **GPU collinear
with rung**, reproducing inside this wave precisely the confound §6 item 4 documents.

The runner therefore alternates the card **per lineage and never per rung**: odd lineage seed →
GPU 0, even lineage seed → GPU 1, with `split_mode = LLAMA_SPLIT_MODE_NONE` and `main_gpu` set
explicitly so no layer of any model ever crosses cards.

| rung | GPU 0 | GPU 1 |
|---|---|---|
| Q4_K_M | 5101, 5103, 5105, 5107 (4 lineages) | 5102, 5104, 5106, 5108 (4) |
| Q2_K | 5201, 5203, … 5225 (13 lineages) | 5202, 5204, … 5224 (12) |

Both rungs appear on both cards. `self_test()` asserts that mapping — that each rung's device set
is exactly {0, 1}, that each card carries at least one lineage of each rung, and that the plan
partitions the seed list without loss — **before any model is downloaded**, and aborts if it does
not hold. Every ledger row carries `device_index`, `device` (the `nvidia-smi` name string) and
`gpu_crossing`; `provenance.json` carries the whole plan.

**Conditional on hardware, and declared rather than degraded.** If only one GPU is visible at
runtime the runner falls back to single-card sequential execution — wave 3's behaviour — assigns
every lineage to GPU 0, and records `gpu_crossing = "single_card_fallback"` in provenance and on
every row. In that case the crossing simply did not happen, the wave still runs, and the analysis
reports it. **The crossing is a property of the hardware the wave lands on, not a precondition of
the registration**, and no verdict in §5 or §5.7 is conditioned on it.

**Disclosure: what the crossing does and does not buy.** The registered measures are unaffected by
which card produced the tokens either way. Echo is exact sequence equality over a discrete
alphabet and the merit factor is derived from an exact integer energy; neither is a floating-point
quantity that a different card could compute differently, and neither has a tolerance a hardware
difference could push it across. **No timing-derived quantity is registered in this wave**, exactly
as in wave 3: `wall_s` is logged and reported as a descriptive only, and the throughput inversion
of §6 item 4 is therefore not a threat to any registered outcome here. The crossing is insurance
against a *sampling*-level hardware effect — a difference in kernel selection or numerics between
the two cards that shifted the token distribution — which we have no evidence for and no reason to
assume away. The analysis prints echo rate by device alongside echo rate by rung, so if such an
effect exists it is visible rather than absorbed into the rung contrast.

**Q8_0 is not run.** Both prior probe waves recorded it skipped for want of a second GPU, and
registering a condition the hardware cannot serve is what produced wave 2's FAILED verdict. Its
absence is a design decision, stated in advance.

## 4. Power

All tests are exact lineage-level permutations on the difference of means, two-sided,
enumerating every split of the pooled lineages.

| comparison | splits | smallest attainable two-sided *p* |
|---|---|---|
| 25 vs 8 (primary contrast) | 13,884,156 | 1.4e-7 |
| 8 vs 8 (any within-rung subgroup check) | 12,870 | 1.6e-4 |

Three of the numbered items carry a bound or a decision rule that can return a verdict (5.1, 5.3
and the branch selection in 5.7); 5.2, 5.4, 5.5 and 5.6 are descriptives with no bound and are not
counted. Bonferroni across the three is 0.05/3 = 0.0167; both floors clear it by orders of
magnitude. Rate-level bounds in §5.1 are compared against 120 and 375 calls respectively, so at
the registered 30%/50% split the binomial standard errors are ≈ 4.2 and ≈ 2.6 percentage points:
the registered 20-point gap is not within sampling noise of either bound.

## 5. Registered predictions and decision rules

Each is a closed-form bound. All of them go in the runner header verbatim, before execution.

**5.1 — PRIMARY. Echo rate.** Sequence-verified parent echo among valid outputs:
**≥ 50% at Q2_K**, **≤ 30% at Q4_K_M**. *Refuted if either bound is violated.*

This is the **same primary every wave in this paper registers**. No new primary is invented for
the discrete task; the whole point is that the *identical* measurement is transported to a task
where the referee's alternative explanation cannot apply.

*Justification for the numbers.* Wave 3 registered 55%/30% on Heilbronn, itself lowered from §3's
circle-packing bound because the Heilbronn seed parent carries no template the proposer might
emit for unrelated reasons. Wave 5 lowers the 2-bit bound a further 5 points, to 50%, for one
specific reason: **on LABS a single flipped symbol is a complete, well-formed, cheap departure.**
Departing from a Heilbronn parent means emitting 26 fresh decimal numbers; departing from a LABS
parent means copying 31 symbols and changing one, which is the sort of local edit even a heavily
degraded proposer produces. The floor on *accidental* departure is therefore higher here, and
registering 55% would be registering wave 3's number on a task whose departure economics differ.
The 4-bit ceiling is held at 30% because nothing about the discrete alphabet makes the *reference*
rung more likely to copy, and moving both bounds would make the wave uncomparable to wave 3.

**CONTROL-ARM FLOOR**, registered here for the reason wave 2 had to add one after the fact.
**If the mean number of accepted hill-climb steps per lineage at Q4_K_M is below 1.0 over the 15
generations, the wave's verdict is UNINFORMATIVE**, no branch of §5.7 is claimed, and the echo
comparison is reported as descriptive only — whatever the Q2_K figure. LABS at *n* = 32 is a
harder search than either geometric task (§8), and this floor exists so that *the reference rung
could not climb either* is never mistaken for *the rungs do not differ*. It is a floor on the
control arm, not on the treatment arm.

**5.2 — DESCRIPTIVE. Accepted hill-climb steps per lineage.** Reported per rung with its exact
permutation tail. **No bound is registered.** Wave 3's bounds (≤ 1.5 at Q2_K, ≥ 4.0 at Q4_K_M)
are deliberately **not** imported: they were calibrated on a task with an effectively continuous
score, and LABS energies move in steps of 4 (§6b), so importing them would set up a refutation
caused by task hardness and then read it as evidence about quantization. Registering no bound is
the honest option, and it is stated before execution rather than discovered after it.

**5.3 — SECONDARY. Conditional-on-departure improvement rate.** Among valid non-echo outputs,
the fraction with **strictly lower energy** than the running parent (an exact integer comparison).
**Decision rule, both branches informative:**

- Q2_K rate **≥ 0.75 × Q4_K_M rate** → quantization gates the *frequency* of departure and not
  its *quality*. This is the repairable reading, and it makes forced-departure interventions
  worth testing.
- Q2_K rate **≤ 0.50 × Q4_K_M rate** → quality degrades too; forced departure would produce worse
  proposals, not better search.
- Between → inconclusive, reported as such.
- **Power floor:** if fewer than 25 Q2_K departures are observed, the verdict is **UNDERPOWERED**
  and no branch is claimed regardless of the ratio.

**5.4 — Template check.** Fraction of valid outputs equal to one of the four degenerate templates
(all +1, all −1, both alternating phases), each with energy exactly 10416 and merit factor 0.0492.
Reported per rung with **no bound**. It has no prediction attached because we have no basis for
one; it exists to detect the failure mode this task was chosen to expose, and reporting it
unpredicted is honest about that. It is the direct analogue of wave 3's zero-area clause.

**5.5 — Symmetry-variant rate, no analogue in prior waves.** Negation, reversal and (−1)^i
modulation each leave *E* exactly unchanged, so every sequence sits in an orbit of at most 8
score-tied variants (`self_test()` asserts the parent's orbit has exactly 8 members, all at
*E* = 156). Fraction of valid **non-echo** outputs lying in the running parent's orbit: reported
per rung with **no bound**. A degraded proposer that emits the negated parent has *departed* by
the registered definition of echo and has not *searched*; this metric makes that visible instead
of burying it inside the departure count. The echo test itself stays plain equality, as
registered — the orbit is a descriptive, not a redefinition.

**5.6 — Outcome.** Final best merit factor per lineage, permutation-tested at lineage level.
**No bound is registered**, for wave 3's reason and one more, stated in §6b.

**5.7 — THREE-BRANCH OUTCOME RULE.** Exactly one branch is claimed, chosen by the arithmetic
below and by nothing else. Write **echo2** for the Q2_K echo rate among valid outputs and
**echo4** for the Q4_K_M rate.

> **BRANCH A — GENERALISES.**
> Control floor met **and** echo2 ≥ 50% **and** echo4 ≤ 30%.
> The departure collapse is not an artefact of floating-point arithmetic: it appears on a task
> whose output alphabet and objective are both integer. The paper's scope sentence widens from
> "constructive geometric search" to "constructive search", and the float-erosion reading of §3
> is reported as **refuted** rather than argued against.

> **BRANCH B — NARROWS. This branch is real, and it is the one that costs us.**
> Control floor met **and** echo4 ≤ 35% **and** echo2 < 50% **and** (echo2 − echo4) < 15
> percentage points.
> The reference rung climbed, the 2-bit rung did not collapse into copying, and the two rungs are
> not separated. Then the collapse is a property of **continuous-coordinate** tasks, the
> float-arithmetic reading of §3 stands unrefuted, and **the paper's claim is narrowed in text**:
> §3.6 and the abstract are rewritten to say the effect is observed on continuous-coordinate
> constructive search and is **absent** on a discrete combinatorial task of the same competence
> class, with the referee's alternative explanation reported as live. We commit to that rewrite
> here so that the commitment predates the outcome.
> The `echo4 ≤ 35%` conjunct is not decoration: without it, a pattern like echo2 = 45%,
> echo4 = 40% would trigger Branch B, and that pattern says *everything copies on this task*, not
> *discreteness kills the effect*. Such a pattern routes to Branch C.

> **BRANCH C — INCONCLUSIVE.**
> Everything else. This includes every case where the control floor is not met, every case where
> echo4 exceeds 35%, and every mixed pattern (for example a clear 20-point gap sitting entirely
> below the 50% bound). No scope change is made in either direction and the wave is reported as
> inconclusive with its numbers.

**Branch B is not a formality.** 7B already *inverts* on circle packing, so the effect is known
not to be universal across the axes already tested; a discrete task is a further axis and there
is no strong prior that it survives. This wave is designed so that the outcome which narrows the
paper is as cheap to report as the one that widens it.

## 6. Disconfirmation

**Branch B is the disconfirmation clause, and it is stated as a rewrite rather than a softening.**
If it fires, the sentence "quantizing the proposer to two bits largely stops it departing from
its parent" acquires the qualifier "on continuous-coordinate constructive tasks" everywhere it
appears in paper 2, including the abstract, and the referee's float-arithmetic alternative is
reported in the paper as live and unrefuted rather than dismissed in a limitations paragraph.

If 5.1 holds at Q2_K but 5.3 returns the quality-collapse branch, the *repairable* reading of the
effect fails on a discrete task even though the effect itself generalises. That is reported as its
own result and is not folded into Branch A.

If 5.1 holds at Q2_K while 5.4 shows a high template rate at Q2_K, the two are in tension —
echo and template emission are mutually exclusive per row — and the pair is reported together
rather than the more favourable one alone.

## 6b. Score granularity, and the defect this wave re-inherits

Flipping a single spin changes each *C<sub>k</sub>* by exactly 0 or ±2, so every *ΔC<sub>k</sub>*²
is a multiple of 4 and **every energy difference is a multiple of 4**. The LABS score support is
therefore **lumpy** in precisely the way circle packing's was (0.900 / 1.040 / 1.300 / 1.625), and
the defect wave 3 was built to remove — that `accepted ≤ valid − echo` leaves a near-zero residual
because most departures tie or worsen — comes back here in full.

We state this before execution rather than being caught with it afterwards. **Waves 3 and 5 are
complements, not a series:** wave 3 buys a fine-grained, tie-free score and keeps floating-point
geometry; wave 5 buys integer discreteness and gives the fine grain back. Neither task is the
one that would settle both questions at once, and no such task has been identified. Any claim
that survives both is stronger than either wave alone; a claim surviving only one must say which.

This is also why 5.2 registers no bound and 5.6 registers none: the accepted-step count is the
statistic most damaged by tie-heavy support, and it is exactly the statistic whose wave-3 bounds
it would have been convenient to reuse.

Two further logging conventions the runner fixes and this registration adopts. Energies are
logged as **integers** and merit factors at 12 decimals; `valid` does **not** require a good
score, because 5.4 counts valid outputs that are worst-case templates; and `echo` is computed
against the lineage's *running* parent as shown in the prompt, evaluated before the acceptance
update, while `score_delta` and `energy_delta` are always measured against the *fixed seed*
parent — two different references, deliberately, because 5.1 is about copying and 5.2 is about
progress from a common origin.

## 7. Analysis, fixed in advance

Computed by a script released with the wave, no arguments, from the raw ledger only: per-lineage
accepted-step vectors, echo counts and rates, departure counts, conditional improvement rates,
the template fraction, the symmetry-variant fraction, final best per lineage, **echo rate broken
out by device index alongside echo rate by rung** (§3b), and every exact permutation tail with its
split count printed beside it. **Every registered outcome is reported
with its verdict label — held, refuted, inconclusive, underpowered or uninformative — including
outcomes unfavourable to the paper's claim, and the labels are printed by the script rather than
written by us.** The branch selected in 5.7 is printed by the script from the registered
arithmetic. Two prior waves in this paper returned unusable verdicts and both are reported; that
is the standard this one inherits.

**Contamination guard.** LABS at small *n* is a standard optimization benchmark with published
optimal sequences, so a proposer could in principle *recall* a good *n* = 32 sequence rather than
search for one. Any emitted sequence with *E* ≤ 64 is flagged in the analysis and audited against
the repository's existing canary procedure (`arm_canary_contamination_audit.py`) before any
improvement claim built on it is reported. This does not affect 5.1, which measures copying of
the *parent* and is unaffected by recall.

## 8. What this wave does *not* answer

A third task at one scale in one vendor's 14B model is not generality. The cross-vendor question —
whether the collapse appears in a non-Qwen lineage at all — remains untouched, and 7B's
non-replication means scale-dependence is still live.

### 8b. The four objections to LABS, stated in full and not softened

These are the ways LABS is a **worse** choice than it first appears. They are recorded here, before
execution, because a limitation discovered after an unfavourable result reads as an excuse.

1. **It re-inherits the exact defect wave 3 was built to remove.** A single spin flip changes each
   *C<sub>k</sub>* by 0 or ±2, so every ΔE is a multiple of 4. The score support is lumpy — the
   circle-packing 0.900 / 1.040 / 1.300 problem, back in full. `accepted ≤ valid − echo` will again
   leave a near-zero residual, and departures will frequently tie or worsen rather than separate.
   **Waves 3 and 5 are complements, not a series**: wave 3 buys a fine-grained, tie-free score and
   keeps floating-point geometry; wave 5 buys integer discreteness and gives the fine grain back.
   Neither task settles both questions, and no task that does has been identified. A claim
   surviving both waves is stronger than either alone; a claim surviving one must say which.
2. **The control arm may not climb.** LABS at *n* = 32 has a "golf course" landscape: broad flat
   regions with isolated deep minima. Steepest descent from a random start reaches only *E* ≈ 84
   against a reported optimum of 64. A 14B proposer over 15 generations may fail to climb at all,
   in which case §5.1's floor fires and the wave returns UNINFORMATIVE having spent 495 generations
   and settled nothing.
3. **The discrete framing invites its own alternative reading.** A referee may say that echo on a
   32-symbol list measures long structured-output fidelity rather than search behaviour. 5.4 and
   5.5 are the instruments that speak to it — a proposer that has lost output fidelity should drift
   toward the low-entropy templates or the score-tied symmetry variants, not toward exact
   32-symbol reproduction of its parent — but neither carries a registered bound, so the reading is
   **addressed and not closed**.
4. **Memorization risk.** LABS at small *n* is a standard optimization benchmark with published
   optimal sequences, so a proposer could *recall* a good *n* = 32 sequence rather than search for
   one. Any emitted sequence with *E* ≤ 64 is flagged and audited under §7's contamination guard
   before any improvement claim built on it is reported. This does not touch 5.1, which measures
   copying of the *parent*.

This wave answers "one discrete task" and nothing else, and the paper must not be edited to imply
otherwise.
