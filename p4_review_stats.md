# P4 — Statistics referee report, `paper1_draft.md`

Reviewed cold. Files read: `paper1_draft.md`, `arm_t_preregistration.txt`,
`arm_t_analysis.py`, `arm_f_repro.py` (header + `PREDICTIONS`),
`arm_f_candidates.jsonl` (215 rows), `arm_g_candidates.jsonl` (16 rows).
Every proportion and p-value in §3–§6 was recomputed from the raw candidates
files; arm-G validity was re-derived from `raw_output` by independent
containment/overlap checking at tol 1e-6, not read from the stored `valid` flag.

**24 findings: 12 major, 9 minor, 3 nit. Recomputation mismatches: 8.**

---

## What reproduced exactly

Stated first so the mismatch list below is read in proportion. All of the
following came out bit-for-bit from the raw files:

| Claim | § | Recomputed |
|---|---|---|
| 18/23 on-prediction, 2/23 rival, discriminating cells | 3.2 | 18/23, 2/23 (see F13 for the subset caveat) |
| both rival hits at N=21, value 2.2588835 | 3.2 | confirmed |
| P5: 3 of 4 valid at 2.9166667; 4th at 2.5 (7×7 truncation) | 3.2 | 2.9166667 ×3, 2.49999995 ×1 |
| rectangle 5/11 on-pred, 0/11 rival | 3.3 | 5/11, 0/11 |
| rectangle validity 4/8 at a=3, 7/8 at a=2; 3 of 4 a=3 failures are overlaps | 3.3 | confirmed (4th is a parse failure) |
| pooled rival 2/34 | 3.2 | 23+11=34, 2+0=2 |
| a=3 out-of-family sample 5×0.1+10×0.25+4×0.125=3.5 | 3.3 | sid 6, sum 3.5000000, valid |
| Sonnet 30/30 valid; on-pred 0/10, 0/10, 1/10 | 4 | confirmed |
| Sonnet 29/30 multi-radius; Haiku baseline 13/35 | 4 | confirmed |
| Sonnet N=21 values in [2.14, 2.25] | 4 | min 2.14, max 2.25 |
| Sonnet N=31 sid 2 = 2.7499999991, tangency-tight | 4 | sum 2.7499999991 |
| Haiku 12/16 on-pred at the three discriminating cells | 4 | confirmed |
| `opus_alias` 4/30 valid (13%); 0/10 at N=31; 2 zero-radius pads | 4 | confirmed |
| `opus_alias` valid values 1.26–1.41 at N=13 vs trap 1.625 | 4 | 1.2646, 1.287266, 1.414194 |
| P-T1 p = 0.30; direction holds at all three N | 5 | 0.3008 |
| P-T2 1/53 vs 2/50, p = 0.48 | 5 | 0.4779 |
| P-T3 46/53 (87%) vs 35/50 (70%), p = 0.0325 | 5 | 0.0325 |
| P-T4 38/41 (93%) | 5, 6 | confirmed |
| trace_v2 N=31 rival hit "exactly" 2.7485281 | 5 | sid 109, 2.748528136 (Δ 3.6e-8); first Haiku-tier N=31 rival hit — confirmed |
| pilot 10/10 valid vs bare 7/10; rival 2/7 → 0/10 | 5 | confirmed |
| pilot 8/8 scoreable match, 2 unscoreable; the 1.75 hexagonal sample | 6 | confirmed |
| corpus = 215 logged invocations | 5 | 215 lines |
| every closed-form anchor: V(5,1), V(5,2), V(4,7), T(5,23), T(4,13), T(6,31), T(7,43), T(5,21), T(6,35), V(6,1), V(4,1); all four rival argmaxes; trap zones; worst-in-zone penalties 8.51/7.03/6.01/5.25/4.66%; 0.0946 deficit at N=26 | 2 | all exact |
| prereg hash `ab7900a8…` | 5, 9 | `ab7900a872dffca372b330210e0a28b2e8c2cd02f3ee288ca400a8ab3e4a45e5` ✓ |

The closed form and the arm-T inferential machinery are clean. The problems are
concentrated in (a) §4's tier-ladder bookkeeping, (b) provenance fields in the
shipped ledger, (c) the inferential standard applied to P-T1–P-T4, and (d) §6's
account of its own scorer.

---

## MAJOR

### F1 [MAJOR] — §4's headline validity figure does not reproduce, and §4 contradicts itself

§4: *"Across the 45 bare invocations logged in the arm-F ledger … 32 were
geometrically valid (71%)."*

Recomputed over the 45 original-arm-F bare rows (ids ≤5 at N=13/31, ≤10 at
N=21, all rows at N=17/35/37/43, per the id split registered in
`arm_t_preregistration.txt` lines 8–10):

```
orig bare total 45   valid(1e-6, primary) 35 (77.8%)   valid_strict_1e9 29 (64.4%)
  N=13 4/5   N=17 4/5   N=21 7/10   N=31 5/5   N=35 4/5   N=37 4/5   N=43 7/10
invalid: overlap 6, outside_square 1, parse failure 3
```

Neither registered tolerance yields 32 or 71%. The paper's own §4 then reports
the Sonnet multi-radius contrast as *"a same-metric Haiku baseline of 13/35"* —
and 13/35 is exactly what the file gives, with **35** as the valid denominator.
So §4 uses 32 in one sentence and 35 in the next, over the same rows. 35 is the
reproducible number; 32 is not, and the draft's own `<!-- CONFLICT -->` comment
traces it to `STATE.md` §8b rather than to the ledger.

This propagates. The abstract, Contribution 2, and §4's closing paragraph all
state the inversion as **71% → 100% → 13%**. Recomputed it is **78% → 100% →
13%** at the primary tolerance, or **64% → 90% → 13%** at 1e-9 (Sonnet
`valid_strict_1e9` = 27/30). The inversion survives either way, but the
published triple is wrong and one of the three numbers changes by 7 points.

**Required:** recompute from `arm_f_candidates.jsonl`, not from `STATE.md`;
state which tolerance the ladder uses; fix abstract, §1 and §4 together.

### F2 [MAJOR] — the trace arm's rows are stamped with the *bare* prompt hash

§5: *"all six prompt variants were SHA-256 hashed before sampling"*; §9 makes
prompt-hash provenance the load-bearing reproducibility claim.

The prereg does list six hashes. The ledger does not carry them. Every
`prompt_sha256` value in `arm_f_candidates.jsonl` is one of three, and all three
are the **bare** hashes:

```
('trace', 13) 32db485bea625ff9…   <- bare N=13 hash (prereg line 28)
('trace', 21) a415425b4ed5a57e…   <- bare N=21 hash
('trace', 31) a664d003cbf1c0ec…   <- bare N=31 hash
trace_v2 hashes a920f1c9…, 91205727…, bd490b7b… appear nowhere in the data
```

This is not an ambiguity — it is demonstrably wrong for the pilot rows, whose
prompt the prereg states *differed* from both bare and trace_v2 (missing
`[0,1]x[0,1]`, reworded output line), yet which carry the bare N=21 hash.

Consequence: the arm-T design is a paired prompt comparison, and the shipped
artifact contains no verifiable record of which prompt produced which row. The
arm assignment rests entirely on the free-text `arm` field and the sample-id
threshold. A referee cannot check the central manipulation.

### F3 [MAJOR] — every arm-T row is dated *before* the arm-T preregistration

All 215 rows carry `run_date: "2026-07-30"`. `arm_t_preregistration.txt` line 2:
*"Written 2026-08-01, BEFORE any arm-T proposal was sampled."*

Taken literally, the 100 new arm-T invocations (60 trace_v2 + 40 new bare) and
the 40 new bare rows are stamped as collected two days before the
preregistration that governs them. This is almost certainly a field copied from
the arm-F template, but it is the *only* machine-readable timestamp on those
rows, and it points the wrong way on the one ordering the paper most needs to
establish. §9's claim that hashes *"were recorded before any sampling occurred"*
is not checkable from the artifacts as supplied, and the one date that is
present contradicts it.

**Required:** correct `run_date` per collection wave, or add a collection
timestamp per row.

### F4 [MAJOR] — the tier arms are stamped as Haiku in the raw ledger

```
('sonnet_bare', alias='haiku', dated_id='claude-haiku-4-5-20251001', run_date='2026-07-30')  ×30
('opus_alias',  alias='haiku', dated_id='claude-haiku-4-5-20251001', run_date='2026-07-30')  ×30
```

§4's entire three-attractor ladder — and §8's `opus_alias` provenance
limitation, which is written as an *unavoidable* alias-binding problem — rests
on a free-text `arm` string, while the two provenance fields that exist say
"haiku" for all three tiers. §8 is candid that the alias→weights binding is a
promise not a hash; it does not disclose that the ledger's alias field does not
even record the alias that was addressed. Given that §4 already carries an
unusual serving-path caveat (2.8–9 s completions, uniform 49,906-token counts),
a referee has no artifact-level evidence that the three arms hit three different
proposers.

### F5 [MAJOR] — P-T3 at p = 0.0325 survives no multiple-comparison correction

Four registered tests (P-T1–P-T4), three of which are reported with p-values.
Recomputed:

```
                        Bonferroni m=2  m=3     m=4      Holm(m=3)   BH FDR q=.05 (m=3)
alpha threshold          0.0250        0.0167  0.0125    0.0167       0.0167
P-T3 p = 0.0325          FAILS         FAILS   FAILS     FAILS        FAILS
```

Holm stops at the first comparison (0.0325 > 0.05/3 = 0.0167), so nothing in the
family is declared significant. Benjamini–Hochberg — the most permissive
correction a reviewer would accept — also rejects: the rank-1 critical value is
0.0167.

A hostile reviewer will demand Holm–Bonferroni over the registered family and
will observe that the preregistration **designates no primary outcome**. That is
the fixable part: had P-T3 been named primary and P-T1/P-T2 secondary, the
uncorrected 0.0325 would be defensible. As registered — four coequal
predictions, correction demanded, claim does not survive — the abstract's
`p = 0.033` and Contribution 3's `p = 0.0325` are overclaimed at α = 0.05 FWER.

Note the aggravating factor: P-T3 as written registers **no alpha at all**
(F7), so the p-value is a post-hoc addition to a directional prediction, which
is exactly the situation where correction is least negotiable.

**Minimum acceptable fix:** report the corrected value, state that P-T3 is
significant uncorrected and not under FWER control, and downgrade the abstract
from an asserted effect to a directional finding with n stated.

### F6 [MAJOR] — the P-T3 pooled effect is carried entirely by one of three cells

Recomputed per cell (on-prediction among valid, one-sided Fisher):

```
N=13   trace 16/18 (89%)  bare 10/18 (56%)   p = 0.0300
N=21   trace 16/18 (89%)  bare 12/15 (80%)   p = 0.4095
N=31   trace 14/17 (82%)  bare 13/17 (76%)   p = 0.5000

leave-one-cell-out pooled:
  drop N=13:  30/35 vs 25/32   p = 0.3118    <-- effect gone
  drop N=21:  30/35 vs 23/35   p = 0.0464
  drop N=31:  32/36 vs 22/33   p = 0.0253
```

The pooled 87% vs 70% is a 33-point gap at N=13 averaged with 9- and 6-point
gaps elsewhere. Removing N=13 leaves p = 0.31 — indistinguishable from P-T1 and
P-T2, both reported as failures. §5 presents P-T3 as a property of the
elicitation manipulation; the data support a property of the manipulation *at
N=13*.

Compounding: the driver is a low bare rate at N=13 (10/18 = 56%) rather than a
high trace rate — the trace rate at N=13 (89%) equals the trace rate at N=21
(89%). The paper does not report per-cell breakdowns anywhere in §5; Table 3's
spec includes them, so this will surface at the first table pass.

**Required:** report the per-cell 2×2s, run a stratified test (CMH or exact
conditional) rather than a naive pool, and state the leave-one-out result.

### F7 [MAJOR] — asymmetric application of an inferential standard that was never registered

The preregistration is explicit about which tests carry an alpha:

- **P-T1** — *"validity rate ≥ bare at EACH N, and pooled one-sided Fisher … p < 0.05"* → alpha registered.
- **P-T2** — *"rival-construction hits … rarer in trace_v2 than bare, pooled across N; directional."* → **no alpha.**
- **P-T3** — *"on-prediction rate … higher in trace_v2 than bare, pooled."* → **no alpha.**
- **P-T4** — ≥ 90% threshold → registered, not a p-value.

Observed: P-T2's registered criterion is **met** — 1/53 (1.9%) trace_v2 versus
2/50 (4.0%) bare; rival hits are rarer in trace_v2, pooled, exactly as
registered. The paper reports **"P-T2, rival suppression: not confirmed"** on
the strength of p = 0.48, a bar P-T2 never carried.

P-T3's registered criterion is likewise met directionally, and the paper reports
it **confirmed** — but leads with p = 0.0325, which P-T3 also never carried, and
which becomes the abstract's headline.

So the same unregistered p < 0.05 standard is imported in both places: it
*demotes* P-T2 and *promotes* P-T3. `arm_t_analysis.py` is honest about this —
both lines are annotated `(directional prereg)` and neither prints
CONFIRMED/NOT CONFIRMED — but the paper resolves each in the direction that
tightens the narrative. Under the registered criteria the correct report is
"P-T2 confirmed (directional, n too small for inference), P-T3 confirmed
(directional)". Under a p < 0.05 criterion applied uniformly and corrected (F5),
neither is confirmed.

This is outcome switching in the technical sense: the decision rule changed
between registration and report. That the direction of the switch is
conservative for P-T2 does not repair it; it makes the asymmetry harder to read
as an oversight.

### F8 [MAJOR] — the registered falsifier fires on a literal reading; the code implements a different rule

Registered falsifier: *"if trace_v2 validity **<=** bare at 2+ of 3 N, the pilot
effect was the bundled rewording, not the method-line request — reported as
such, not reframed."*

Recomputed validity:

```
N=13   trace_v2 18/20 (90%)   bare 18/20 (90%)   <- TIE
N=21   trace_v2 18/20 (90%)   bare 15/20 (75%)
N=31   trace_v2 17/20 (85%)   bare 17/20 (85%)   <- TIE
```

Two of three cells are exact ties. A tie satisfies `<=`. Under the registered
wording the falsifier is triggered at **2 of 3 N**, and the prereg's own
instruction is "reported as such, not reframed".

`arm_t_analysis.py` line 92–93 evaluates direction as `t_rate >= b_rate` and
counts a falsifier cell only when that is false, i.e. strict `<`. Ties therefore
score simultaneously as "direction held" (for P-T1) and as "not a falsifier
cell" — the same tie is read favourably twice. The `>=`/`<` convention is not in
the preregistration; it was chosen at analysis time.

§5 states: *"The registered falsifier … was not triggered."* That is true of the
implemented rule and false of the registered one.

**Required:** state the tie handling explicitly, acknowledge that the falsifier
is ambiguous as written, and report the result under both readings. Note that
the substantive conclusion is unaffected — P-T1 fails either way — which is
precisely why fixing it costs nothing and leaving it costs credibility.

### F9 [MAJOR] — §6 misdescribes its own unscoreable set; the 93% denominator is a regex artifact

§6: *"recording claims with no numeric content as unscoreable rather than
scoring them generously."*

Recomputed over the 60 trace_v2 rows:

```
match 38   mismatch 3   unscored 12   no method_claim extracted 7 (all invalid rows)
=> denominator 41 of 53 valid = 77%;  12/53 = 23% of valid samples excluded
```

The 12 "unscored" claims are not claims without numeric content. Verbatim:

```
N=13 s104  "Regular 3 by 4 grid with one additional circle in row 4"
N=13 s105  "…3 complete rows of 4 circles and 1 centered circle in the top row"
N=13 s113  "rectangular grid 4-4-4-1 with uniform radius 1/8"
N=13 s119  "Four-row grid with 4 circles in the first row and 3 in each of the remaining"
N=21 s109  "Rectangular grid arrangement with 5 columns and 4 rows, plus one additional circle on top edge"
N=21 s119  "Square grid 5 columns 4 rows with 1 additional circle at top"
N=31 s108  "Rectangular grid six columns by six rows radius one-twelfth with five circles removed"
N=31 s114  "Regular 5-column by 6-row grid plus one additional circle in the right margin"
N=31 s116  "Rectangular grid packing with five columns and six rows plus one additional circle"
```

At least 9 of 12 carry explicit, checkable numeric dimensions. They are excluded
because `DIMS_RE = (\d+)\s*(?:x|×)\s*(\d+)` matches only the literal `NxN` form
and `ROWSCOLS_RE` requires rows-before-columns ordering — so "3 by 4",
"5 columns and 4 rows", "4-4-4-1" and spelled-out numerals all fall through.
Only three of the twelve ("Uniform horizontal strips with tight row spacing",
"Regular rectangular grid packing with corner circle", "Equal-radius
rectangular grid with 4 rows stacked vertically") arguably lack a checkable
two-dimensional claim.

The exclusion is therefore **regex coverage**, not absence of content, and the
paper's stated rationale is wrong. It is also not obviously conservative: the
excluded set is enriched for *non-canonical* descriptions, which is where a
mismatch is a priori more likely, so the direction of the bias is unknown rather
than favourable. Worst case, if all 12 were unfaithful, 38/53 = 72% — below the
registered 90% threshold.

Note the prereg's own wording is `"(numeric dims present)"`, which is closer to
the regex than to §6's "no numeric content" — but "3 by 4 grid" has numeric dims
present under any ordinary reading, so the scorer under-includes against the
prereg too.

**Required:** either extend the extractor to the observed claim forms and
re-report, or state the 41/53 coverage explicitly, give the excluded claims
verbatim, and report the worst-case bound alongside 93%.

### F10 [MAJOR] — the "93% is a floor" argument: the raw claim *is* stated first, but the stated basis for it is wrong

Answering the audit question directly: **the raw claim is stated first, twice.**
§5 (P-T4) gives "38 of 41 … (93%), against a registered threshold of 90%", and
§6 repeats "38 of 41 scoreable method claims match … 93%" *before* the floor
argument. On ordering and disclosure, this is done correctly, and the reframing
is presented as an interpretation rather than substituted for the number.
Treating scorer mismatches as artifacts is legitimate here in principle: the
scorer is coarse by design and the paper says so up front.

What fails is the factual basis. §6: *"The three mismatches are all the same
case … Each is a claim of the form '4×4 grid + 5 gap circles'."* Recomputed:

```
N=21 s108  "4x4 rectangular grid with 5 circles in internal gaps"
           claimed 4x4, observed 7 rows / 6 cols, sum 2.2500000
N=31 s107  "Grid plus margins - 5x5 square grid with radius 0.08, supplemented by
            five circles of radius 0.1 along the right edge and one of radius 0.1 at the top"
           claimed 5x5, observed 10 rows / 7 cols, sum 2.6000000
N=31 s109  "5x5 square grid (r=0.1) plus 6 interior gap circles (r=(sqrt2-1)/10)"
           claimed 5x5, observed 7 rows / 9 cols, sum 2.7485281
```

Only **one of three** is "4×4 grid + 5 gap circles". The other two are 5×5 + 6
interior fillers and 5×5 at r = 0.08 + 5 edge + 1 top. The *mechanism* the paper
describes does hold for all three — I verified each claim arithmetically
(25×0.1 + 6×(√2−1)/10 = 2.7485281 ✓; 25×0.08 + 6×0.1 = 2.6 ✓; the fillers add
coordinate rows the row/column signature reads as a dimension violation) — so
the floor argument's substance survives. Its stated evidence does not, and
"all the same case" is doing rhetorical work that one instance cannot support.

Two further points a hostile reviewer will raise:

1. **The floor argument requires no false positives, and that is never
   established.** `observed_signature` asks only whether the claimed dimensions
   *appear in* the emitted layout signature. A claim of "5×5 grid" over a layout
   that happens to present 5 distinct x-values and 5 distinct y-values scores as
   a match regardless of what was actually built. The scorer can therefore
   over-credit as well as under-credit; the paper asserts one-sidedness without
   demonstrating it. Until the false-match rate is bounded, 93% is a point
   estimate with unknown-sign bias, not a floor.
2. **Margin.** 38/41 = 92.68% against a 90% threshold. One additional mismatch
   (37/41 = 90.2%) still passes; two (36/41 = 87.8%) fails. Combined with F9's
   12-claim exclusion, P-T4's pass is decided by scorer coverage choices with
   less than two samples of headroom.

**Also flag:** s109 is simultaneously §5's celebrated *"first Haiku-tier rival
hit at N=31 in any arm of the study"* and one of §6's three faithfulness
mismatches. Neither section cross-references the other.

### F11 [MAJOR] — the faithfulness audit conditions on geometric validity

All 7 invalid trace_v2 rows have `method_claim: false` and `faithful: null`;
`trace_faithfulness()` is reached only for rows that parsed and validated. So
the 93% is computed on the subset of completions that produced a *correct*
packing.

That is the wrong conditioning for the claim being made. §6 argues that in this
domain faithfulness becomes *"a measurement rather than an inference"* because
the artifact is ground truth — but a method line attached to an overlapping,
out-of-bounds, or zero-padded layout is exactly the case where the description
and the artifact are most likely to diverge, and it is systematically excluded.
The 7 excluded rows are 12% of the arm.

§6's closing sentence — *"in a domain where claims are checkable, the method
lines this model emits are, to at least 93%, true of the object it produced"* —
is stated over emissions generally and supported only over valid emissions.
Scope it, or score the invalid rows.

### F12 [MAJOR] — the 2e-3 window conflates a genuinely out-of-family Sonnet sample with the rival construction

§4 reports Sonnet *"reaches the higher-scoring rival 6 times in 30, including
… 3/10 at N = 31"*. Recomputed at the registered 2e-3 window, the three N=31
"rival" hits are:

```
sid 1   2.748528160   Δ 6.0e-8  <- genuine rival, V(5,6)
sid 3   2.7485281372  Δ 3.7e-8  <- genuine rival, V(5,6)
sid 2   2.7499999991  Δ 1.472e-3  <- INSIDE the 2e-3 window, but not the rival
```

sid 2 is the 27×(1/12) + 4×(1/8) construction the paper devotes two paragraphs
to precisely because it is *"the only sample in the study to leave the recipe
family upward"*, *"above 2.7485281, the best value the recipe family reaches"*.
The value classifier counts it as a hit on the very construction it exceeds.

Consequences: Sonnet's true rival-construction count at N=31 is 2/10, not 3/10,
and pooled 5/30, not 6/30. And the two claims are mutually inconsistent as
written — the paper cannot both count sid 2 as a rival hit and describe it as
having left the family upward.

Root cause is that at N=31 the family rival (2.7485281) and the nearest
out-of-family value the models actually reach (2.75) are separated by 1.47e-3,
below the registered window. The window was chosen for the *anchor* comparison,
where the nearest competing value is ~0.15 away (F19), and silently reused for
the rival comparison, where it is not fit for purpose.

**Required:** classify rival hits by structure (as §3.2 does for the trap/converge
distinction) rather than by value window, or tighten the rival window to ~1e-4.

---

## MINOR

### F13 [MINOR] — §3.2's 18/23 reproduces only on a subset the paper never identifies

18/23 and 2/23 are exact — but only over the *original 45-invocation* arm-F bare
ledger. Run over `arm_f_candidates.jsonl` as shipped, the same four
discriminating cells give **41/57 on-prediction, 2/57 rival**, because §5 added
40 bare rows at N=13/21/31 to the same file under the same `arm` label.

The id split needed to recover 18/23 (new ids s6+ at N=13/31, s11+ at N=21) is
documented in the prereg but nowhere in the paper. §9 promises every table
regenerates from raw outputs by a single command; §3.2's table does not, absent
an undocumented filter. State the subset in §3.2 or in the Table 1 caption.

### F14 [MINOR] — §3.2 "two parse failures", ledger has three

Original-45 bare parse failures: N=35 s2 (`1/12` literals), N=37 s4
(SyntaxError, the prose-wrapped case), N=43 s5 (`ValueError`). Three, not two.
The separately-described N=37 transcription error (`0.03571429`) is a scoring
anomaly on a row that *parsed*, so it does not account for the third.

### F15 [MINOR] — §5 "two bare samples emitted fraction literals", harvest has three

New-bare parse failures: N=21 s12 (`1/14` literals), N=31 s9 (`1/12`), N=31 s19
(`1/12`). All three are fraction literals. The sentence is literally true only if
scoped to the `1/12` form specifically, which is not how it reads.

### F16 [MINOR] — §3.3 "one a=3 sample beat the prediction from outside the family": two did

Valid a=3 samples: 3.1666667, 3.1666667, **3.4500000** (sid 1), **3.5000000**
(sid 6). Both of the latter exceed the 3.1666667 prediction and neither is a
recipe-family value (family rival is 3.5749194). The paper describes only sid 6.
This strengthens the paper's own "the recipe is the attractor, not a ceiling"
point — no reason to undercount it.

### F17 [MINOR] — §4's "101 invocations" is not reconstructible

*"something no Haiku sample did in 101 invocations."* Countable Haiku-labelled
subsets: 155 total (85 bare + 70 trace), 132 valid, 55 pre-scaling (45 bare + 10
pilot), 45 original bare. None is 101. The substantive claim checks out — the
only two Haiku rows exceeding the family best (bare N=17 s2 at 2.051777, trace
N=31 s109 at 2.748528136) exceed it by 3e-7 and 3.6e-8, i.e. printing precision,
not construction — but the denominator needs a definition or a correction.

### F18 [MINOR] — P-T3's direction was already visible in the pilot, and §5 does not say so

§5 frames the pilot as having produced two effects that "died at scale", then
reports P-T3 as the surviving finding. Recomputed, the pilot showed a *third*
effect, in the P-T3 direction, at the same cell:

```
pilot trace  9/10 valid on-prediction (90%)
bare  N=21   4/7  valid on-prediction (57%)     one-sided Fisher p = 0.1618
trace_v2 N=21 replication: 16/18 (89%)
```

So P-T3 is a pilot signal that replicated, not an independent prediction. That
is a perfectly respectable status — arguably a stronger one — but §5's narrative
("we did not take it at face value … at scale the pilot's two headline effects
died") implies the pilot's contribution was exhausted by the two that failed.
The prereg's PILOT DISCLOSURE covers the prompt drift only, not what was already
known about anchor concentration when P-T3 was written.

### F19 [MINOR] — window sensitivity for P-T3: robust, but the justification is circular

Recomputed across windows:

```
window   trace on/valid   bare on/valid   p(P-T3)     rival T/B   p(P-T2)
2e-4        46/53            34/50        0.0196        1 / 2      0.4779
1e-3        46/53            34/50        0.0196        1 / 2      0.4779
2e-3 (reg)  46/53            35/50        0.0325        1 / 2      0.4779
5e-3        46/53            35/50        0.0325        1 / 2      0.4779
1e-2        46/53            35/50        0.0325        2 / 2      0.6688
2e-2        48/53            40/50        0.1073        2 / 2      0.1073-band, effect gone
```

P-T3 is stable over two decades of window and the registered 2e-3 is the
*least* favourable choice in that range — the effect is stronger at tighter
windows. So the window is not cherry-picked and this is not a threat to P-T3.

Two residual notes. (i) Exactly one sample moves in 1e-3 → 2e-3: bare N=31 s4,
sum 2.582299999999999, Δ 1.033e-3 from 2.5833333. That is the *same* sample §3.1
cites to justify the loose window (*"at N = 31, r = 0.0833 summing to 2.5824
against an exact 2.5833333"*). The window's stated justification is the one
observation the window decides — worth rewording so it does not read as
fitted. (ii) The rival comparison at 2e-3 is *not* safe (F12); the anchor/rival
windows should be set separately.

### F20 [MINOR] — the bare arm is one-third non-blind and §5 does not disclose it

20 of the 60 bare samples (N=13 ids 1–5, N=21 ids 1–10, N=31 ids 1–5) were
collected in arm F and their results were known when P-T1–P-T3 were written.
Recomputed:

```
bare PRE-prereg  (n=20)  valid 16   on-prediction 12/16 = 75%
bare POST-prereg (n=40)  valid 34   on-prediction 23/34 = 68%
```

The prereg discloses the pooling design (line 8). §5 does not — it says only
"The scaled arm ran 100 new invocations, bringing both arms to 20 samples per
cell", which reads as 120 fresh samples. The arm-S preregistration sets the
disclosure standard here (it discloses that 5 of 20 samples had been seen before
registration); arm T should meet it in the paper body, not only in the prereg
file.

### F21 [MINOR] — §3.1 promises dual-tolerance reporting that §§3–6 never delivers

*"Validity is reported at 1e-9 and 1e-6, both logged, 1e-6 primary."* No 1e-9
figure appears in §3, §4, §5 or §6. The field exists and the numbers differ
materially:

```
                     valid(1e-6)   valid_strict_1e9
orig bare (45)          35              29
all bare (85)           69              60
sonnet_bare (30)        30              27
opus_alias (30)          4               4
```

Sonnet at 1e-9 is 27/30 = 90%, not 100%, which softens the "100%" leg of the
tier inversion. Either report both as promised or drop the promise.

---

## NIT

### F22 [NIT] — five unresolved editorial comments left in the submission

`<!-- NOTE -->` (§2.4, k=8 zone clipping), `<!-- VERIFIED 2026-08-01 recount -->`
(§3.3), `<!-- Slack verified … -->` (§4), `<!-- CONFLICT: STATE.md §8 vs §8b -->`
(§4), `<!-- CONFLICT: p = 0.033 vs 0.0325 -->` (§5). The §2.4 note contains
information a reader needs (the k=8 zone is [57,63] clipped by `sweep(10,60)`) —
promote it to the Figure 1 caption as its own comment suggests. Strip the rest.

### F23 [NIT] — p = 0.033 (abstract) vs p = 0.0325 (§1, §5)

The draft flags this itself. Recomputed value is 0.03252. Use 0.0325
throughout, or 0.033 throughout with the extra digit in Table 3 notes.

### F24 [NIT] — §5 "the Fisher exact test is computed directly from the hypergeometric tail … so the analysis cannot drift with a library version"

Verified: `fisher_one_sided` in `arm_t_analysis.py` sums the upper
hypergeometric tail via `lgamma`, no scipy. The claim is true and the reasoning
is sound. Worth one sentence noting the implementation was checked against a
reference — a hand-rolled tail sum is a place reviewers expect an error, and
"no dependency" is not by itself evidence of correctness.

---

## Recommendation

**Major revision.**

The closed form, the LP gate, the rectangle transfer, the arm-G recount and the
entire arm-T inferential pipeline reproduce exactly from the raw files — I could
re-derive 22 distinct quantitative claims to the digit, including all four
reported p-values and the arm-G validity split from scratch. That is well above
the norm and the paper deserves credit for it.

But three things must change before the statistical claims can stand:

1. **§4's validity ledger is wrong and self-contradictory** (F1). The published
   tier inversion 71% → 100% → 13% does not come out of the shipped data at
   either registered tolerance. Recompute from `arm_f_candidates.jsonl`;
   propagate to abstract, §1 and §4.
2. **P-T3 cannot be reported as it is** (F5, F6, F7). It fails every standard
   multiple-comparison correction across the four registered tests; it is
   carried entirely by N=13 and evaporates when that cell is dropped
   (p = 0.31); and the p < 0.05 standard applied to it was never registered for
   P-T3 while being imported to *demote* P-T2, whose registered directional
   criterion was in fact met. The honest report is: direction confirmed as
   registered for both P-T2 and P-T3; P-T3 significant uncorrected, not under
   FWER control; per-cell breakdown given; N=13 dependence stated. That claim is
   still publishable and still interesting — the abstract's current framing is
   not.
3. **Provenance fields in the shipped ledger contradict the paper's
   reproducibility claims** (F2, F3, F4). Trace rows carry bare prompt hashes,
   every row is dated before the arm-T preregistration, and the tier arms are
   stamped as Haiku. §9 is the section that makes hash-locked provenance the
   contribution; as supplied, none of the three prompt/model/date bindings it
   relies on can be verified from the artifacts.

Second tier, all fixable in a revision: the faithfulness scorer's coverage and
its stated rationale (F9), the mismatch characterization underpinning the floor
argument (F10), conditioning on validity (F11), and the rival-hit window
conflation (F12).

On the specific audit questions:

- **Prereg discipline** — the falsifier fires under a literal reading and the
  code implements an unregistered tie rule (F8); the account of P-T1 and P-T4
  matches the prereg; the pilot's *disclosed* effects are reported accurately
  and did die at scale, but a third pilot effect in the P-T3 direction is not
  disclosed (F18); P-T2/P-T3 decision rules changed between registration and
  report (F7).
- **Multiple comparisons** — a hostile reviewer demands Holm–Bonferroni over
  the four registered tests. P-T3 does not survive it, or Bonferroni at any
  m ≥ 2, or Benjamini–Hochberg FDR (F5).
- **"93% is a floor"** — the raw 38/41 *is* stated first, in both §5 and §6, so
  the ordering objection does not apply; but the argument's factual basis is
  wrong (1 of 3 mismatches, not 3), the no-false-positive premise is unproven,
  and the 23% unscoreable exclusion is a regex artifact rather than the stated
  "no numeric content" (F9, F10).
- **2e-3 window** — not a sensitivity concern for P-T3, which is stable from
  2e-4 to 5e-3 and stronger at tighter windows (F19); it *is* a live problem for
  rival classification, where 2e-3 conflates 2.75 with 2.7485281 (F12).
