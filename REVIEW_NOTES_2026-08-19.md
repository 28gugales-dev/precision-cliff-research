# Review notes — both papers, post-CC/CC2/CCS + tightening pass (2026-08-19, re-confirmed 2026-08-21)

**STATUS UPDATE 2026-08-22 (after main's rev 4.5 merge):** main's ox-alpha QA +
revisions 4–4.5 independently fixed Paper 1 defects 2 (argmax miscounts removed
from abstract and §3.7), 6 (named-but-not-run list), 8 ("clean, well-powered"),
and 9 ("external review" framing). The remaining verified defects were fixed on
this branch in the same merge commit: Paper 1 defect 1 (CC table above-anchor
cell 1 → 2), Paper 2 defects 1–3 and 5 (§8 exclusion contradiction, sixth-family
antecedent, A.3 table pointer, §SS2, fig:family-echo now referenced). Still open:
defect 3/12 — `ANONYMIZATION_REPORT.md` + `main.log` inside both submission
folders (excluded from all zips, but must never be uploaded as folders), and
Paper 1 defect 11 only (paper1_draft.md not updated for CC/CC2/CCS/CN — twelve
vs fifteen arms; archival md, does not gate submission). Rev 4.5 itself fixed
defect 10 (Appendix B has the CC2 tool-use deviation row) and the pooled argmax
sentence; defects 4, 5 and 7 were fixed on this branch post-merge (descriptive
pool label, §2.1 quote aligned, abstract-scope sentence re-pointed).

Two-agent editorial review of the current drafts; every finding below was re-verified
against the frozen data files / tex sources before being recorded. Nothing here
undermines a headline result — but Paper 1 has two sentences its own frozen reports
contradict, and both submission folders contain de-anonymizing files.

## Paper 1 (template anchoring) — NOT submission-ready until fixed

### Must fix (contradicted by the arms' own frozen reports)

1. **"Exactly one exceeds the anchor" is false — it's two.**
   `latex-tmlr-paper1/sec_forecast_transfer.tex` §3.7 and its table.
   `arm_cc_report.json` cell N=13 sums contain **1.6614054 and 1.7761424**, both above
   the 1.625 anchor (+2e-3 window). The table cell "1 — the family argmax, exactly"
   should be "2 — one the family argmax, exactly", and "the lost mass sits entirely
   below the anchor" should be "almost entirely below".

2. **"Exactly one reaches the family argmax" is false — one per arm, three total.**
   Abstract (`main.tex` ~line 94: "(one reaches it, exactly)") and §3.7
   (`sec_forecast_transfer.tex` ~line 563: "exactly one reaches it").
   Frozen argmax rates: CC 1/12, CC2 1/11, CCS 1/13. So **2 of 78** weak-tier outputs
   reach it (both exactly), **3 of 115** overall. The "0 exceed it" halves are correct.
   Suggested: abstract "(three reach it, none pass it)"; §3.7 "exactly one per wave
   reaches it, both exactly".

3. **De-anonymizing files inside `latex-tmlr-paper1/`:**
   `main.log` carries `C:\Users\soham\...` on ~89 lines; `ANONYMIZATION_REPORT.md`
   quotes the real name and email. tex/bib/pdf are clean; the prepared zips exclude
   them — but any folder upload or re-zip leaks. Move both out (same for
   `latex-tmlr/ANONYMIZATION_REPORT.md`, which has the email + Kaggle handle).

### Stale-reference cluster (from the tightening + CC integration rounds)

4. "Pooled over both weak-tier waves… 0 of 78" and the 0/115 pool lack the
   "labelled descriptive" tag the CC2 preregistration requires for pooled figures.
5. §3.7 quotes §2.1 as saying "a code channel routes around the anchor" — §2.1
   actually says "routes the task to an executed optimizer"; the quoted sentence
   exists only in the preregistration.
6. `sec_related_repro.tex` "Analyses named but not run" list names four analyses the
   paper now runs (arm MU, arm CH, N=57, empirical-k back-out). Prune to the genuinely
   un-run items (library-enabled probe, faithfulness split, interleaved arm-T
   re-collection, P5 at n=20).
7. Two sentences claim the abstract carries content the condensed abstract dropped:
   "the sharper scope the abstract now carries" (m≥4) and "correcting the… figures in
   the abstract and Contribution 2". Re-point to §1/Contribution 2.
8. Contribution 3 again says "a clean, well-powered finding (§6.5)" — §6.5 itself
   states the CI's lower bound sits below the registered 90% threshold and the audit
   is confounded with the elicitation arm. Restore "reported in §6.5 with its limits".
   (This regressed once already; watch it in future merges.)
9. "External review / council review" framing survives in ~4 spots
   (`sec_forecast_transfer.tex`, `sec_tiers_elicitation.tex`) after the rename to
   "internal adversarial checks".
10. Appendix B deviations table stops before the five newest arms — no rows for
    MU/CH/CC/CC2/CCS, including the disclosed CC2 tool-use deviation (N=13 slot 2)
    that §9 promises is "tabled in Appendix B".
11. `paper1_draft.md` was never updated for CC/CC2/CCS: "twelve arms / 468
    invocations" vs the tex's fifteen / 603; md §2.1 still says "we ran no
    code-enabled arm". Either port §3.7 into the md or drop `main.tex`'s
    "1:1 translation of paper1_draft.md" claim and re-date the revision note.

## Paper 2 (served precision) — submission-ready after three small fixes

1. **§8 contradicts the withdrawn §3.6 exclusion.** `sec_forensic_repair.tex` still
   says the exclusion "holds by 0.8 points… the thinnest load-bearing thing in the
   paper", but the tightening pass withdrew it — §3.6 and the evidence map now state
   the departure-quality question open. Rewrite as a nominal margin + "§3.6 reports
   the question as open"; soften Appendix C's "excluding… by 3.8, 2.4 and 0.8 points"
   to "would nominally exclude".
2. **"A sixth model family" dangles in the condensed abstract** — the five-families
   sentence was cut. Add "after five others fell below registered competence floors"
   (or say "a further family").
3. **Appendix A.3 points to a table "in §3"** that lives in Appendix B (§3 has no
   tables). Same misdirection in Appendix A's opening line.
4. Minor: Figure 1 (`fig:family-echo`) is never `\ref`'d — add a reference at the
   wave-7c sentence in §8; evidence-map "§SS2" should read "§2".
5. `latex-tmlr/ANONYMIZATION_REPORT.md` + `CITATION_AUDIT.md` — move out of the
   submission folder before any packaging (see Paper 1 item 3).

## What passed (verified, no action)

- All condensed-abstract numbers in Paper 2 match the body; "final best score
  separates the rungs nowhere" retained, so Appendix C's back-reference resolves.
- All six new §7 bib entries resolve in `references.bib`/`main.bbl`; no duplicate
  bibitems from `\nocite{*}`.
- Both PDFs build with 0 errors, 0 undefined references/citations.
- No identity strings in any `.tex/.bib/.bbl/.pdf`; the prepared upload zips
  (`overleaf_paper1.zip`, `overleaf_paper2_v3.zip`, `latex-tmlr-openreview.zip`)
  exclude the flagged files and are safe as built.
- Arm CC/CC2/CCS headline verdicts (code channel does not escape the family;
  ceiling replicates on fresh draws and survives the Sonnet tier) are supported by
  the frozen reports — only the "exactly one" garnish sentences are wrong.
