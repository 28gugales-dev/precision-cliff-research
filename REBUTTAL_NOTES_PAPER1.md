# Rebuttal notes — paper 1 (anchoring), prepared against the simulated TMLR review (2026-08-27)

Internal preparation only; not part of any submission artifact. The simulated review
(opus, zero-context, TMLR two-criteria rubric) returned **leaning accept, conditional**.
Status of each requested change as of Rev 4.7 / 4.7b (tag `v4.7-fresh-eyes` + follow-up):

## Critical — all addressed in text

1. **Abstract scope (m ≤ 1, F-M1 3/3, denominator).** FIXED. Abstract now carries the
   falsifier restriction and the 8-of-11 pooled denominator alongside 7-of-7. §8's
   "sharper scope the abstract now carries" is now true.
2. **"Reduced concentration" unsupported.** FIXED. Abstract, contribution 5, §3.6 and the
   §3.6 heading all state the ranges overlap (61–67 sits inside 56–76) and that the
   reduction is directional, not separated, at these n. CI-includes-bar caveat retained.
3. **Contribution 1 post-hoc labeling.** FIXED. Contribution 1 and §3.5 both label the
   attempt-level reading as a disclosed post-hoc decomposition; classifier named (family
   filler radius); registered P-CH2 outcome (1 of 3 cells) stated in the contribution.
4. **Validity conditioning beyond CH.** ADDRESSED (disclosure route). A global scoring
   convention now states every on-prediction rate conditions on validity, names CH as the
   only arm where the attempt-level decomposition is measurable, and points at per-cell
   validity denominators for bounding. A full attempt-level re-analysis of F/GM3/V/CN is
   not possible under the registered instruments (invalid rows there lack the CH arm's
   structured attempt evidence); if a reviewer insists, offer the decomposition as a
   supplementary table computed under the CH classifier with that limitation stated.
5. **Anonymized artifact link.** ADDRESSED. §9 provenance item now states the full
   artifact accompanies the submission as anonymized supplementary material
   (`supplementary_anonymized.zip`, 520 entries, 0 identity leaks in audit).

## Minor — status and prepared responses

6. **Uniform-template null for the square arm.** DONE (Rev 4.7c). `diagnostics_template_null.py`
   (post hoc, disclosed): null = 1/3 (one branch value per k in {k*-1, k*, k*+1}); observed
   discriminating-cell rates exceed it with exact binomial tails 0.043 / 2.9e-4 / 3.4e-4 /
   6.9e-3 at N = 13/21/31/43. In §3.2 (full), Appendix D.1 (short), deviations table row.
7. **CN reconstructed rows as sensitivity, not primary.** ALREADY THE CASE — respond by
   pointing at §3.8: the eleven flagged rows are discarded from the primary analysis;
   P-CN1 reads 3 of 4 with them excluded. The review misread direction here.
8. **Demote contribution 3 / drop opus_alias leg.** DECLINED with rationale: the alias
   caveat is attached at every occurrence, the ladder is reported both with and without
   the leg (§5), and the boundary-condition framing is exactly the demotion requested.
9. **"Mode ceiling" wording + round-number baseline.** DEFERRED. Cheap wording softening
   possible on request; a construction-family baseline is new analysis. Both text-only.
10. **§1 "behaves the same way on the next sample."** FIXED — now "more often than not
    the next sample repeats the same move" (supported: per-sample on-prediction 56–86%).

## Standing evidence for the response

- Fresh-clone reproducibility: all 14 pipeline scripts, byte-identical reports (CRLF-only
  diff on two arm-M files, content identical).
- Independent ledger re-audit: ~330 numeric assertions recomputed from raw ledgers with an
  independent parser/validator; 3 findings, all fixed or glossed exactly in 4.7
  (`corrections_ledger.md` item 33).
- Arms CP and RP have now been RUN (Rev 4.8): CP confirms the anchor survives a container
  the training text never phrased ([3,5]^2, modal 4/5); RP eliminates the simplest recall
  mechanism (87/87 UNKNOWN, 0/44 recalls). Strongest available answer to any contamination
  weakness a reviewer raises.

## Second-round simulated review (Rev 4.8b -> 4.8c, 2026-08-27)

Verdict: **leaning accept** (up from leaning-accept-conditional). Criticals 1-4 verified
RESOLVED with quotes; #5 (artifact statement) PARTIAL -> fixed in 4.8c with a standalone
Artifact-availability bullet addressing the public-remote anonymity question. New-material
findings all folded in 4.8c: abstract "erases every lexical handle" softened (N survives as
the retrieval key -- caveat now in S3.9/D.9); RP positive-control caveat added (uniform
UNKNOWN also consistent with an abstention prior; beyond-registration caveat, labeled);
F-RP1 stated in text; S9 registration/stopping bullets carry CP/RP; contribution 5 flags
the looser offset-frame strong form. Reviewer's stated path to plain accept was exactly
these four text edits -- all made.


## Prepared response: regime relevance (expected as the strongest objection)

**The objection.** "You characterize unconditioned zero-shot calls. FunSearch and AlphaEvolve
condition on parent programs and fitness feedback from the first step. Arm MU's falsifier
fired -- the anchor dissolves under conditioning. So the paper measures a regime the cited
systems do not run in, and concedes the effect disappears in the one they do."

**Do not contest the scope.** It is in the abstract, in S5, in the contributions, and the arm
that establishes it is ours, reported as a triggered falsifier. Any reply that softens this
forfeits the disclosure credit the whole paper rests on. Concede in the first sentence.

**Four moves.**

1. *The contribution is an instrument, not a claim about loop internals.* The closed form
   gives a computable prior-mode for the task: the value the model emits when nothing
   conditions it. Its use is diagnostic -- when a discovery system reports a value at a cell
   where V(k*, m) or T(k*, N) equals that value, the report is not by itself evidence of
   search, because the unconditioned prior already concentrates there. That inference holds
   regardless of which regime the loop runs in; it constrains how a *result* may be read,
   not how a loop works. The objection does not touch it.

2. *The dissolution is a finding about where loop diversity originates.* If the anchor were
   regime-invariant, conditioning would be doing little. F-MU1 firing says the opposite:
   variation in these loops is produced by the parent/archive mechanism, not by the
   proposer's intrinsic exploration. For a loop designer that is actionable -- it locates the
   diversity budget in the scaffold, and yields a falsifiable prediction: weakening
   conditioning (small archives, single-island runs, low-diversity parents) should collapse
   proposals back toward the family.

3. *The ceiling is not an artifact of the unconditioned text channel.* Arms CC, CC2 and CCS
   delegate construction to an executed math-only program -- the channel closest to what
   discovery systems actually generate -- across two tiers and a fresh-draw replication:
   0 of 115 valid program outputs exceed the family argmax. At these cells the program
   channel does not clear the family on its own.

4. *Scope is what makes a floor usable.* A floor that applied everywhere would say nothing
   about when to apply it. We report where it holds (unconditioned, weak tier, this
   container, under paraphrase and an offset frame -- arms CP/PP) and where it stops (parent
   conditioning, higher tiers, rectangles -- arms MU, S/O, S4.2). The boundary is measured,
   not asserted.

**What we do not claim, stated plainly.** We have not shown anchoring persists inside a
running loop and do not claim it. The experiment that would settle it: seed a FunSearch-style
loop, log every proposal from generation 0 through k, score each against V(k*, m)/T(k*, N) as
a function of generation and archive size. Offer to add this as specified future work in S8,
and to soften any sentence the reviewer reads as a claim about deployed loops.

**Optional concession if pressed.** Reframe from the discovery-loop framing toward "the
unconditioned proposal distribution and its use as an evaluation floor," keeping
FunSearch/AlphaEvolve as motivation rather than object of study. Costs nothing scientific.
