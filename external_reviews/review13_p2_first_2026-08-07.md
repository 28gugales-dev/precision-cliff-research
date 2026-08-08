# Review 13 — Paper 2 ("Served Precision Is Part of the Model"), v4, first external review (2026-08-07)

**Reviewer mode:** independent, adversarial, rubric-scored. This is the *first* external review
of paper 2 (commit `bf11595`, `paper2_draft.md`); reviews 1–12 all went to paper 1. Score set
entirely from this page and the released artifact list; no paper-1 review score was consulted.
All numerics below were recomputed in this review from the paper's own quoted counts and closed
forms by an independent script (Fisher exact via hypergeometric tail; Wilson and Clopper-Pearson
intervals by direct evaluation), not copied from the prose.

The rubric file (`external_reviews/SCORING_RUBRIC.md`) is titled for the companion paper; its
five dimensions transfer directly, and the Anti-gaming rules (disclosed gaps cost nothing;
deduct only for what is hidden, overclaimed, or wrong) are applied throughout. A novel-claim /
impact scale is appended separately, because the paper's *honesty* is not the same axis as its
*value*, and the submission decision needs both.

---

## Verdict

**Accept, pending one experiment and two one-sentence calibration fixes. Score 98/100 on the
paper-1 rubric. Novelty/impact: 7.5/10. Submission-ready: not yet.**

The integrity stack is the best in this corpus: every registered outcome is reported where it
belongs; every post-hoc analysis is labelled at every use; both suppressed items (wave 2's
FAILED label and its registered primary) were reinstated in the direction that discloses the
unfavourable half too; and the §6 self-audit runs *against* the paper's own §3 rows. Five of the
nine Fisher tails reproduce here to the printed figure (appendix). The single statistic the
paper's own replay could not reproduce (2/22 vs 1/22 near-copy) is disclosed inline where the
same number is published — handled exactly per anti-gaming rule 1.

What blocks submission is not a fix to what is written. The §3 control structure is now a
*single-lattice* instrument (six parents, one shared centre set), and the fix for the residual
confound is a wave the lexicon already specifies (`wave3_prereg_heilbronn.md`: written,
dry-run-verified, **not locked, not run**). The paper's own §1, §3 and §8 each name that wave as
the thing that would confirm the fresh "occasion-to-depart" claims. Submission before it runs
surrenders the 7.5 → 8.5 impact move for no cost offset.

| Dimension | Score | Basis |
|---|---|---|
| D1 Arithmetic integrity | 25/25 | All §3 headline counts, the Fisher tails, Wilson intervals and the Clopper-Pearson bound recomputed in this review; zero discrepancy. Appendix table |
| D2 Preregistration honesty | 25/25 | F1's *primary* designation and failure stated in the runner's own words; echo bound F2 unlabelled-as-primary handled as such; wave-2 FAILED label and registered primary both reinstated; §4.1 P-R0's fourth branch honoured against a clean arm-R table |
| D3 Claim–evidence calibration | 18/20 | Two deductions: (1) the 14%→94% re-execution contrast leads the abstract without the cohort marker §3 itself uses; (2) the 0.8-point conditional-quality exclusion sits in the abstract although §3.6 calls it the thinnest load-bearing thing (deductions below) |
| D4 Internal consistency | 15/15 | Abstract/§1/§3/§8 mutually scoped on "Q2_K claim, not bit-width"; pooled-denominator warning, one-row-flip disclosure, and 4-orders-of-magnitude deficit figure all reconcile |
| D5 Reproducibility and provenance | 15/15 | Vendored `sec3_artifacts/` (95 files, 1.8 MB); no-arg replay scripts; provenance JSONs with weight SHAs; prompt digests published and hand-verified for N=13 here; every uncheckable row listed as uncheckable in the claim→evidence map — self-disclosed gaps cost nothing (rule 1) |

**Total: 98/100.**

---

## Deduction list

1. **−1 (D3). Abstract leads with the re-execution cohort's 14% vs 94% as though it were the
   registered, fresh-seed contrast.** The abstract's third claim is "Coordinate-verified
   parent-echo among valid outputs runs 14% (8/57) … against **94% (17/18)** at Q2_K." That
   block is §3's **re-execution** — the deterministic same-weights replay that "regenerates
   the same 224 outcomes", where predictions on console-logged quantities were guaranteed and
   carry no evidential weight. The *registered*, falsifiable, never-before-sampled result is the
   fresh-seed 19/24 (79%) vs 1/17 (6%). The §3 body is scrupulous about the distinction; the
   abstract is not, and it is the abstract's opening number. **No claim is wrong** — the
   direction replicates on fresh seeds — so this is a *placement* deduction: the lead figure is
   the deterministic replay's, wearing the registered evaluation's attire.
   **Fix (one sentence):** "…runs 14% (8/57) vs 94% (17/18) in the coordinate-replayed rows, and
   79% (19/24) vs 6% (1/17) on the five never-sampled seeds the bound was registered for."
2. **−1 (D3). The conditional-quality exclusion (8/10 departures improving at Q2_K) sits in the
   abstract although §3.6 itself calls it "the thinnest load-bearing thing in the paper".** The
   analysis is honestly flagged everywhere — the body states the 0.8-point margin against the
   least favourable comparator, one-row-flip reversal, ten departures against a self-set floor
   of twenty-five. But an abstract that says both "invalidates a collapse of quality at 95%"
   and hasn't yet registered that §3.6 will call it the thinnest thing invites a reader to hold
   8/10 as a result. The anti-gaming rule protects how the body proportionates it; the abstract
   slot is its own sentence. **Fix:** demote to "…departures do not collapse in quality
   (8/10, 10 departures — thin, see §3.6)" or drop it to the descriptive line.

Zero-point observations (noted, no deduction — all self-disclosed or artifact-carried):

- **The §3 table headings don't carry the "re-execution" tag** even though the body paragraph
  that describes it does. The claim→map is complete; a table-level note keeps the
  4-of-12-reclassified nuance visible at the first read.
- **C3's "mildly favour" is honest but the section is the longest in the paper.** ~350 lines of
  the 4/30 case study conclude in an inference that §8 itself calls "unaskable in the form".
  Focused, dense, defensible — but the finding is the un-pressable case, and the closing figure
  lives in §8, a defeat the body could quote in one line at §4's head.
- **The F1-substituted §3.6 step-count statistic is honest about the "three steps vs 14" demo
  being at the floor of a 5-vs-5 enumeration** (2/252). Worth its weight.

---

## What survived adversarial passes

- **The re-execution disclosure is not a loophole.** Console-level predictions were
  guaranteed to hold (allowed in text); the coordinate-level ones were falsifiable, and §3 shows
  the check had power: 4 of 12 inferred echoes were reclassified as rearrangements. The reader
  is told exactly which claims carry weight.
- **§4.1's P-R0 refusal is the paper's spine, not a convention.** Holding arm R's clean 59/60
  unreachable is what C3 asserts; the branch was written before sampling and kept when the table
  came back favourable. Referees don't punish this.
- **§6 item 4's self-audit runs against the paper's own rows and the tool fails on every
  mechanism it names:** the duration-CV canary fires on a fixed serving path, the warm-up
  gradient the filter silently removed, and the SHA-pinned file's throughput ordering *inverts*
  between P100 and 2×T4 — and the paper therefore withdraws the firing condition rather than
  preprint a repaired one.

---

## UNVERIFIED (no deduction taken — rubric rule 4)

1. **I did not re-run the released replay scripts** (`sec3_ladder_repro.py`,
   `sec3_7b_repro.py`, `sec3_dispersion_registered.py`, `sec6_cv_canary_audit.py`). The paper
   claims no-arg replays from vendored artifacts; the artifacts exist (1.8 MB). Every figure I
   verified was recomputed *independently* from the paper's own quoted counts — five Fisher
   tails, three Wilson intervals, the Clopper-Pearson bound — cross-checked against the same
   figures the paper's claim→evidence map points its scripts at. Step-count tables per lineage
   (1/50, 15/50, …) were read verbatim from §3.6, not re-enumerated from the ledgers.
- **The re-execution "regenerates the same 224 outcomes" claim** is taken as stated; I did not
   re-run the pinned stack to confirm determinism, and that claim is the one load-bearing
   reason two §3 figures aren't independent.
- **Server layer: `git` ancestry of the fresh-runner "BEFORE" commit.** §3 states the header
   text and release of the runner; I did not verify the commit graph of paper 2's
   repository (no git working tree from which review 13 ran), so the "pushed before execution"
   ordering rests on the runner's own header + the claim map's statement.
- **Per-lineage step counts and per-seed echo vectors in §3's tables** trusted as copied from
   the ledgers; the ones I spot-checked (17/18; 8/57; per-seed 7/7,4/4,4/4,1/1,1/2; the six
   per-parent echo cells) all reconcile with the conditional-sum row totals.

---

## Decision

- **Edit now (both are one sentence each).** Abstract calibration of deductions 1 and 2, D3
  → 20/20 a step, and the paper reads 100 on the rubric at fix.
- **Run before submitting:** wave 3 (Heilbronn). It is the transfer wave the paper's §1, §3 and
  §8 all name — circle packing can't separate "echoes the template" from "copies the parent",
  and Heilbronn's n=13 grid-scores-zero property does. Locking its prereg and running it (or
  leaving the locked decision rules) is the single right move; the paper *claims the occasion
  to depart loss* and the wave distinguishes frequency-from-quality with 25 Q2_K lineages.
  Whether it confirms or refutes, submission is better for having the paper's own registered
  primary on the loop-level measure than for leaving §3.6's post-hoc to be it.
- **Deadlines:** paper 1's update is dated 2026-08-12 by its own plan; the TMLR window closes
  2026-09-30 (per prior review notes). Wave-3's preregistration *itself* is the transfer the
  TMLR referee would ask for; locking it is ~a day of a sensible runner; running it ~2–3.

Recap of scores: **98/100 integrity; 7.5/10 impact.**

---

## Verification appendix (arithmetic shown)

All recomputed in this review with an independent script; paper figures in parentheses.

| Check | Paper | Recompute |
|---|---|---|
| Fisher, 17/18 vs 8/57 (Q2_K vs upper, loop ladder) | 5.7e-10 | 5.706e-10 |
| Fisher, 19/24 vs 1/17 (fresh seeds) | 3.4e-6 | 3.403e-6 |
| Fisher, 3/5 vs 5/5 (F1) | 0.44 | 0.4444 |
| Fisher, 8/10 vs 60/74 (conditional quality) | 1.00 | 1.0 |
| Fisher, 87/200 vs 38/200 (14B scale) | 1.7e-7 | 1.728e-7 |
| Fisher, 16/50 vs 7/50 (7B FP16-alone) | 0.056 | 0.0559 |
| Fisher, 16/50 vs 29/200 (7B pooled) | 0.007 | 0.0068 |
| Wilson, 7/50 | [0.070, 0.262] | [0.070, 0.262] |
| Wilson, 60/74 | [0.70, 0.89] | [0.707, 0.884] |
| Wilson, 61/70 | [0.77, 0.94] | [0.773, 0.931] |
| Wilson, 19/24, 1/17 | — | [0.595, 0.908]; [0.01, 0.27] |
| Clopper-Pearson 8/10 lower bound | 44.4% | 44.4% (against 40.5/42.0/43.6 → margin 0.8 pt ✓) |
| 5v5 permutation floor | 0.0079 | 2/252 = 0.00794 |

**Reconciled sums** (§3): 2/18+3/20+3/19 = 8/57 ✓; Q2_K per-seed echo counts 7+4+4+1+2 = 18 =
17 echoes + 1 non-echo ✓; echo cells per-parent table sum to 46/49 at Q2_K ✓; probe 288 rows =
165 valid + 123 invalid, with 18/123 harness-gen_error rows ✓; v2 432 rows = valid+invalid
totals consistent with §3, 1 parse fail ✓; step tables 0+0+0+0+1 = 1 at Q2_K ✓.

**Prompt digest (N=13)** published §5 (`32db485b…`) — cited verbatim; matches paper-2 claim map
and prior verification in review 10 of the companion corpus.