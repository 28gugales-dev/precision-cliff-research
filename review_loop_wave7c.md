# Review-loop prompt pack — post-wave-7c integration pass

Run AFTER wave-7c results are integrated into both papers. Pattern per
feedback_skill_research-paper-ops.md: 5 parallel sonnet reviewers with exact
paths + no-re-run ground rule, one batch fix, then 1 opus area-chair pass
with fixed rubric that recounts numbers itself. Do not re-run all reviewers
per iteration — area-chair-only regrade.

Ground rules baked into every reviewer prompt:
- Read files fresh; papers: paper1_draft.md, paper2_short.md (paper2_draft.md
  is archival long form — flag inconsistency only if paper2_short cites it).
- LaTeX mirror: latex-tmlr/*.tex must agree with paper2_short.md.
- Recompute from ledgers via the no-argument scripts; NEVER re-run sampling.
- Stale exclusions: latex1/, latex2/, superseded/, paper-explorer/,
  section-dir fragments of paper 1.
- Report findings as file:line + claim + evidence + suggested fix. <300 words
  each finding, no praise.

## Reviewer 1 — validity-recompute
Re-run: arm_gm3_analysis.py, wave7c_analysis.py, fig4_family_echo.py,
sec3_ladder_repro.py (paper 2's existing replay). Diff every number they
print against every occurrence of those numbers in both papers, both
abstracts, the LaTeX fragments, and figure captions. Any figure/caption/text
number not derivable from a script output = finding.

## Reviewer 2 — method-vs-code
For each new section (paper 1 §3.6, §8 vendor-scope, §9 multiplicity +
GM/GM3 provenance entries; paper 2 wave-7c paragraph, screen disclosure,
evidence-map rows): check the described procedure against the actual
scripts (arm_gm3_analysis.py, screen_s_run.py, screen_s_doc.md,
wave7c_make_runner.py, kaggle_wave7c_*.py, wave7c_analysis.py). Any
divergence between prose and code = finding. Verify the prereg SHA chain:
screen doc committed before screen rows; 7c prereg locked before kernel
push; runners carry b1fc9ee9… in headers.

## Reviewer 3 — integrity-provenance (the six attack lenses)
Attack exactly these; verdict per lens — defended / exposed:
1. GM3 pooled-win emphasis vs 2/5 mode-match miss (is the miss stated
   where the win is stated?)
2. GM3 serving-path split 99/41 (is the amendment + dual accounting
   visible everywhere the 57.5% appears?)
3. Paid-gemma re-screen ("re-rolled until pass" reading — is 12/13
   free-tier delivered-validity + registered-rule-before-sampling stated
   wherever the 43/50 appears?)
4. gpt-oss MXFP4 confound (qualifier inline with every gpt-oss claim, not
   footnoted elsewhere?)
5. Screen-vs-ladder validity gap 27/50 -> 5/50 (treated as finding via the
   registered SS6 branch, or spun?)
6. Multiplicity (does the SS9 statement cover the new arms; does any text
   imply corrected significance?)

## Reviewer 4 — cross-consistency
Both papers + LaTeX + figures + preregs as one corpus. Check: family names
and sizes consistent (gemma-4-26b vs gemma-4-31b never conflated); echo
definitions identical wording; wave-7c verdict identical in abstract,
section, evidence map, LaTeX; figure 2/3/4 numbering in paper 1 sequential
with no dangling references; screen numbers in prereg == screen numbers in
papers; arm counts in paper 1 SS9 match arms actually listed.

## Reviewer 5 — claims-scope / novelty
Every sentence added since v56 (git diff v56..HEAD on the two paper files):
does any claim outrun its evidence by even a word? Specifically hunt:
"cross-vendor" without "pooled-level" qualifier; "replicates" for anything
that is not a fresh draw; "confirms" where the registered bar was not met;
any statement about nemotron-super beyond advanced-not-run; any implication
the screen measures competence rather than selects candidates.

## Area chair (opus, after batch fix)
Fixed rubric: (a) recount 10 randomly chosen numbers from scripts yourself;
(b) verify every reviewer finding marked FIXED actually changed in the file;
(c) grade each of the six attack lenses defended/exposed; (d) venue-calibrated
verdict: would this survive a TMLR AC's "claims and evidence" test — yes/no
per paper, with the single weakest sentence quoted. No prose rewrites —
findings only.
