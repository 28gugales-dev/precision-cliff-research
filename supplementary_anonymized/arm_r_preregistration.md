# Arm R preregistration — the repair probe, and the bare re-snapshot it needs

**Status: LOCKED before any sampling.** Written 2026-08-07. The prompt digests below are
produced by `arm_r_build.py`, which is committed in the same commit as this file and
before any invocation of either arm. Nothing here may be edited after the first sample;
corrections go in a dated amendment block at the foot, and any amendment made after
sampling has begun says so.

This file is a registration in the sense §3 of the paper uses the word: predictions and a
decision rule fixed in advance of seeing the data. It is not a registration in the
external-timestamp sense — see *What this registration is not*, below.

---

## 1. What is being tested

§4 names one follow-up as this paper's own: hand the alias a **fixed, known-valid
packing** and ask it to find the broken tangencies. The model did not choose the
construction, so arithmetic execution is separated from constructive ambition. §4 argues
that this separates its two hypotheses and then does not run it.

- **H1, serving-path degradation.** A fast decode path erodes the arithmetic precision
  needed to close a tangency, while leaving the choice of construction intact.
- **H2, genuine tier property.** Whatever the alias resolves to really does attempt
  harder constructions and really does execute them less reliably.

On the text channel of the original arm the two are indistinguishable: both predict
ambitious families with broken tangencies. On **this** task they are not, because the task
contains no construction to be ambitious about.

---

## 2. Why a second arm is mandatory, not decorative

The original `opus_alias` rows were sampled on 2026-08-01. Arm R samples on 2026-08-07
through the same runtime, which accepts an alias only and reports nothing about which
weights served either call. **That is C3, applied to our own follow-up.** A repair score
taken alone is therefore uninterpretable: a clean result is equally consistent with
"repair is easy for the path that served 4/30" and with "the alias resolves to something
else this week."

So arm R ships with **arm B2**, a bare re-snapshot: the byte-identical N = 13, 21, 31
prompts from `arm_f_prompts.json` that produced 4/30, re-issued at 10 invocations per
cell. B2 is the anchor. It is also, separately, the dated re-snapshot §4 lists as
runnable from inside the runtime and never ran, so it discharges a stated gap either way.

**B2's own result is informative in both directions, and neither direction is a failure
of the design:**

- B2 reproduces the collapse → arm R's numbers attach to a serving path that behaves like
  the one §4 documents, and the H1/H2 reading below is available.
- B2 does **not** reproduce it → the serving signature has changed between two calls that
  the runtime describes identically. Arm R then cannot speak to the 2026-08-01 path at
  all, and we will say so in exactly those words rather than reinterpret it. That outcome
  is a direct positive instance of C3 — an unattestable serving change, caught only
  because the same prompts were kept — and it is reported as the finding, not as a null.

---

## 3. Design

**Substrate.** An exactly-tangent grid-plus-interstitial packing: a *k* × *k* grid at
*r* = 1/(2*k*) plus interstitial circles at *r* = (√2 − 1)/(2*k*) in the interior holes,
truncated to *N*. Every contact is tangent to floating-point exactness, so a perturbed
copy has no slack anywhere else and the answer key is exact rather than approximate.
This is the same grid-plus-filler family both comparator tiers produce in §4, so the
substrate is not foreign to the task.

**Injection.** The grid circle nearest the centre is **displaced** by δ along +*x*.
Displacement, not inflation: inflating a circle changes the packing's total score, which
would let a model detect the injection by comparing the total against the family's closed
form instead of by checking geometry. Every radius, and therefore the score, is untouched.

**Cells and the δ ladder.** *N* ∈ {13, 31} × δ ∈ {1e-2, 1e-3, 1e-4}, 5 invocations each
= 30 per tier. Coordinates are printed at 12 decimal places, so at every δ the violation
is present in the digits the model is shown.

| cell | overlapping pairs | min depth | max depth | prompt sha256 (first 12) |
|---|---|---|---|---|
| n13_d0.01   | 3 | 6.962e-03 | 1.000e-02 | `a2d93c76372b` |
| n13_d0.001  | 3 | 7.060e-04 | 1.000e-03 | `0da640ba8424` |
| n13_d0.0001 | 3 | 7.070e-05 | 1.000e-04 | `a9c3662d8b3e` |
| n31_d0.01   | 1 | 1.000e-02 | 1.000e-02 | `bd96b296c9ba` |
| n31_d0.001  | 1 | 1.000e-03 | 1.000e-03 | `2bccc9b86276` |
| n31_d0.0001 | 1 | 1.000e-04 | 1.000e-04 | `e5a5024eaff9` |

The two cells carry **different pair counts by construction** — at *N* = 31 the truncation
to 31 circles omits the interstitials on the displaced circle's +*x* side, so only the grid
neighbour overlaps. This is a property of the cells and not a nuisance to be pooled away:
*N* = 13 additionally tests whether a model that finds the obvious pair keeps looking.
Results are reported **per cell**, and the two are never pooled into a single rate.

**Tiers.** Arm R runs at the **alias** tier and at the **Sonnet** tier, same 30 cells
each. Without the Sonnet comparator, "the alias detects *x*%" has no scale — the task's
intrinsic difficulty at δ = 1e-4 is unknown to us. Sonnet is the comparator §4 already
uses (30/30 on the bare task) and is addressed through the same runtime.

**Total: 90 invocations** — 30 B2 (alias), 30 R (alias), 30 R (Sonnet).

---

## 4. Scoring, fixed here

A response is **parsed** if it yields a list of `[i, j]` integer pairs (code fences
stripped, outermost bracketed list taken — the §4 parser's rule). Anything else is
`unparsed` and counts as a miss, never dropped.

Per response, against the exact key:

- **exact** — the returned set equals the key set.
- **partial** — non-empty, a subset of the key, not equal.
- **false-positive-bearing** — contains at least one pair not in the key.
- **empty** — returned `[]`, i.e. asserted the packing is valid.

**Primary measure: `exact` rate, per cell, per tier.** Designated primary here, in
advance, and reported as primary whatever it does. (§3 records what happens when a
paper leans on a secondary after its primary fails; this file is written to not repeat it.)

Secondary, reported always: partial rate, false-positive rate, empty rate, and mean
recall over key pairs.

---

## 5. Predictions

Registered before sampling.

**On B2 (bare re-snapshot, alias tier):**

- **P-R0.** B2 validity at 1e-6, pooled over 30, is **≤ 12/30**. The original was 4/30; a
  band rather than a point because the claim under test is "the collapse is still there",
  not a rate reproduction. *Disconfirmed by ≥ 13/30* — which would be a serving-signature
  change and is reported as such.

**On arm R, alias tier:**

- **P-R1.** Exact rate at δ = 1e-2 is **≥ 0.6** (≥ 3/5 per cell). The violation is 1% of
  the unit square and the packing is handed over; a tier that fails even here is failing
  something other than precision.
- **P-R2.** Exact rate is **monotone non-increasing in decreasing δ** within each cell.
  This is H1's signature. Under H2 the task has no construction to be ambitious about, so
  H2 predicts no δ dependence.
- **P-R3.** Exact rate at δ = 1e-4 is **strictly below** the rate at δ = 1e-2, in at least
  one of the two cells, by ≥ 2/5.
- **P-R4.** The **empty** response — asserting validity — is at least as common at
  δ = 1e-4 as at δ = 1e-2. A precision-limited reader stops seeing the violation; it does
  not start seeing a different one.

**On arm R, Sonnet tier:**

- **P-R5.** Sonnet's exact rate at δ = 1e-2 is ≥ the alias's at δ = 1e-2.
- **P-R6.** Sonnet's δ = 1e-4 exact rate exceeds the alias's δ = 1e-4 exact rate by
  ≥ 2/5 in at least one cell.

---

## 6. The decision rule, and what each branch licenses

Fixed here, and deliberately narrow.

- **H1-favouring.** P-R0 holds *and* P-R2 holds *and* P-R3 holds. Licensed statement:
  *on a task with no constructive ambition in it, the alias tier's accuracy falls with the
  arithmetic precision the task demands, which H2 does not predict and H1 does.* Not
  licensed: any claim about which weights served the call. C3 is untouched by either
  branch, and this file does not get to move it.
- **H2-favouring.** P-R0 holds *and* the alias's exact rate is flat in δ *and* at least
  matches Sonnet's. Licensed: *execution on a handed-over construction is intact, so the
  bare-task collapse is not general arithmetic degradation.* That is a real result against
  the paper's own preferred reading, and it is reported in the abstract if it occurs.
- **Neither.** Reported as neither, with the cells printed.
- **P-R0 fails.** Arm R is reported as measuring a serving path we cannot tie to the
  2026-08-01 one, no H1/H2 conclusion is drawn from it, and the re-snapshot result becomes
  the finding. **In this branch the paper's §4 hypothesis pair remains unseparated, and we
  say so.**

**Disconfirmation clause.** If arm R produces a result that undercuts a claim currently in
the paper, the claim comes out. §4's "the observations mildly favour H1" is in scope: an
H2-favouring branch weakens it and the sentence is rewritten, not annotated.

---

## 7. What this registration is not

Same clause as `wave3_prereg_heilbronn.md`, and for the same reason. This file is
committed to a **local** git repository before sampling. Local commit timestamps are
writable by the person who wrote them. Nothing here is externally timestamped, no author
is named, and **the paper may not describe this as a preregistration in the archival
sense** — the honest description is *a decision rule and a prediction set fixed in advance
of seeing the data, in a repository we control*. That is worth something and it is not
worth what an external timestamp is worth. Wherever the paper cites this file it says
which of the two it means.

**Known limitations, stated now rather than after.**

1. **Five per cell.** The finest distinction 5 invocations can draw is 1/5 = 20 points, and
   a two-sided exact test on 5 vs 5 bottoms out at 2/252 = 0.0079. P-R3 and P-R6 are set
   at 2/5 because anything finer is not resolvable at this size. This arm is a
   discriminator, not an estimator.
2. **One substrate family.** A single packing family at two *N*. A δ-dependence found
   here is a δ-dependence on grid-plus-interstitial packings.
3. **One displacement direction.** +*x* only. Direction is not varied.
4. **No contemporaneous interleaving of the two tiers** is guaranteed; they are sampled in
   whatever order the runtime schedules them. §4's own no-contemporaneous-control caveat
   applies to any timing observation made here, and no timing claim is registered.
5. **The alias is an alias in both arms.** Nothing in this design attests a serving path,
   and the design does not claim to. It is precisely because it cannot that arm B2 exists.
