# My assessments of the three 2026-08-04 external reviews

Reviewer of record: session agent (Fable). Each review independently checked against repo data before acting. Actions marked DONE are committed; queued items listed at bottom.

## Review 1 (workshop compact, 74/100) — verdict: ~fair for the version it graded; several deductions don't apply to the full paper

- **D1 (N=35 not a trap, −8): arithmetic CONFIRMED independently.** T(6,35) − V(5,10) = +0.0024531; general k≥6 condition verified symbolically ((k−1)/(2k) > √2−1 iff k ≥ 6). BUT full paper §2.4 already states penalty = 0 at N = 35/48/14/15 and uses N=35 as structural control — this was a compression artifact in the short versions, not a paper error. DONE: gap column + "trap names the branch" clarification added to both short versions (commit b75e0d7). Gap values triple-checked: +0.1511424 / +0.1588835 / +0.1651948 / +0.1701960.
- **D2 (baseline strawman, −7): fair.** DONE: strong 1/3 template null applied to square cells in short versions; powered cells clear it (56/80/76%).
- **D3 (n=4 cells, −6): fair, already known internally.** DONE: underpowered flag + Wilson [30%,95%] added.
- **D4 (external validity, −5): first half INDEPENDENTLY CONFIRMED by our own source audit the same day** (FunSearch reseed clones best survivor; ShinkaEvolve restart re-seeds from archive; OpenEvolve copies user seed). DONE: claim rewritten in all four artifacts (commit 3c73c23). Code-arm gap real; queued as new preregistered arm.
- **D5 (tolerance confound, −4): REFUTED by post-hoc diagnostic** (diagnostics_opus_overlap_2026-08-04.md): 24/26 opus failures gross (median max overlap 3.3×10⁻², median repair cost 15% of Σr, two samples contain radius 0.0); tolerance-scale near-misses live in the WEAK tier instead (5/7 < 2.5×10⁻⁵). Reviewer's mechanism real, wrong arm. DONE: disclosed post-hoc note in all versions (commits bf1ee23, 9141c36).
- **D6 (alias in abstract, −3): style call, deferred** — abstract flags alias inline; restructure is user's call.
- **D7 (seven decimals oversell, −2): mildly fair.** DONE: clarifier added (prediction categorical; decimals verify identification).
- **D8 (no figures, −1): fair.** DONE: fig1 (prediction vs family, gap segments) + fig2 (tier ladder) built, committed 8c440a5.
- Best unsolicited point: lead with "0/11 reached rival argmax" — negative claim needs no null. Queued for next abstract pass.

## Review 2 (full paper, Major Revision) — verdict: ~90% accurate; two factual errors

- **Error 1:** "Cross-vendor attempts (Gemma 4, Gemini) failed due to 0% parse compliance" — Gemma GM2 yes (0/140); Gemini flash-lite arm is QUOTA-throttled/incomplete, zero parse failures among collected rows, no outcome yet.
- **Error 2:** Names "Anthropic Claude: Haiku, Sonnet, Opus alias" — the paper deliberately never names vendor or version (opus_alias unattributable by design). Reviewer inference presented as paper content.
- Math verification section: matches our own checks. Weaknesses A/B/C all match what §5/§8 already self-disclose — reviewer found nothing hidden.
- **Genuinely actionable:** Figure 2 caption self-note is a real pre-submission bug (queued: regenerate at single N with sample ids). Tables 4/5 → supplementary is right for venue submission (arXiv version may keep). "Bundled prompt format and trace request" labeling: cheap wording pass, queued. "Weak-tier law" softening: queued.

## Review 3 (full paper, Strong accept w/ structural changes) — verdict: best structural read of the three; premortem items 4–6 are degraded text (word salad — "Akbar", "37/69 V prime-cell", "QD-contam socket state-merge") and were reconstructed only where recoverable

- Architecture diagnosis (A 60% / B 25% / C 15%, C currently ~40% of text) — agrees with review 2's rebalance point; correct. §5-6 compression queued for venue version; workshop versions already implement it.
- Mode-ceiling-first ordering: correct and cheap; queued for venue restructure.
- Trap zones as named section + full-sweep shaded figure: good; Figure 1 already planned covers most of it.
- **Highest-value concrete asks, all runnable as NEW preregistered arms (allowed under stopping rule):**
  1. **N=57 cell** (k=8, fifth branch-rule test) — ~20 haiku invocations via Max-plan swarm. Cheapest big win.
  2. **Rectangle defense cell at n≥20 with hashed prompt** — fixes weakest-provenance arm.
  3. **N=35/37 top-ups to n≈15–20** — fixes review 1's D3 and P5's n=4.
  4. **Code-emitting arm at N=13/21/31** — addresses programs-vs-coordinates modality gap (review 1 D4, review 2 C2).
  5. Open-weights rerun of P-O1/O2/O4 — needs Kaggle GPU (GM4 idea) or OpenRouter key; blocked on user.
- opus_alias cut-vs-keep: recommend KEEP (properly caveated, reported both ways per prereg discipline; cutting after inclusion would itself be a post-hoc move requiring disclosure).

## Cross-review consensus (three independent reviewers agree)

1. Structure buries the best result — mode ceiling forward, §5-6 shrink, Tables 4/5 to appendix.
2. Fig 2 placeholder caption must be fixed pre-submission.
3. Underpowered cells need top-ups or louder flags.
4. Single-vendor scope needs either softer wording or a completed cross-vendor arm (GM/GM3 in flight).

## Review 4 (hermes/deepseek-v4-pro, restructured full paper, 72/100 Major revision) — verdict: high-quality, 7 of 8 deductions actioned same day

- D1 (abstract rectangle overclaim, −8): fair. DONE — abstract now carries "partial support, 5/11, not separable from uniform-template null" in md+tex+compact.
- D2 (wave confound missing from abstract, −5): fair. DONE — clause added.
- D3 (appendix ordering, −4): fair. DONE — appendices swapped, Table 4 (deviations) now Appendix B, Table 5 (corrections) Appendix C; all refs re-pointed (md+tex).
- D4 ("precisely" + precision drop, −3): arithmetic CONFIRMED (0.0945586). DONE — full value given, "precisely" dropped.
- D5 (monotonicity ambiguity, −2): fair. DONE — "rises monotonically … rises then collapses".
- D6 (opus_alias anomalies unreproducible, −2): fair. DONE — marked "anecdotal context from an unreleased session transcript". Transcript release remains user's call.
- D7 (penalty coverage footnote, −1): PARTIALLY WRONG — worst-in-zone penalties are family-internal arithmetic, exact at every N; only the published-bound comparison stops at N=30. DONE — caption now states the distinction explicitly.
- D8 (structural k-match, −1): fair and valuable. DONE — post-hoc `diagnostics_kmatch.py` (disclosed): 50/50 on-prediction samples k\*-structured, 64/69 (93%) of all valid samples on the k\* grid. Strengthens the template claim; added as table column in §3.2.

## Review 5 (hermes/deepseek-v4-flash, compact 3-pager, 80/100) — verdict: mixed; 2 of 8 deductions rest on reviewer errors

- D1 (100 vs 120 invocations, −6): REFUTED — 100 new = 40 bare + 60 trace; 20 of 60 analyzed bare rows are pre-existing arm-F samples (disclosed in full paper §6.1). Reviewer assumed all 120 analyzed rows were new. DONE anyway — compact now carries the decomposition inline.
- D2 (46% unreproducible, −4): half-valid — full paper gives 47/102; compact had dropped the fraction. DONE — "(47/102 valid samples)" restored.
- D3 (N=15/N=24 also lose value, −3): HALF-REFUTED — N=15 has NO reachable family alternative (filler cap (k−1)² = 4 < m = 6; reviewer's V(3,6) is outside the family). N=24 loss 0.0142136 is real and was already in the full paper. DONE — wording now "largest losses … with a small residual at N = 24 (0.014, i.e. 0.59%)" in compact + 4-page.
- D4 ("rules out" too strong, −2): fair. DONE — "finds no evidence … in this sample" in all four artifacts.
- D5 (rectangle formulas cut, −2): fair. DONE — q\*/p\* formulas restored.
- D6 (primality lists cut, −1): fair. DONE — both prime lists restored inline (membership re-verified).
- D7 (no figure, −1): fair. DONE — figure pointer paragraph added (docx build already embeds fig1/fig2).
- D8 (rival suppression cut, −1): fair. DONE — P-T2 1/53-vs-2/50 clause restored.

## Queue state after this wave

DONE (committed): short-version fixes for D1/D2/D3/D5/D7/D8, loop-audit claim correction (all versions), tolerance diagnostic + disclosure, figures.
QUEUED (prose, cheap): weak-tier-law softening; bundled-intervention labeling; "0/11 rival" abstract lead; §5.4 rename; Fig 1 caption internal-note removal.
QUEUED (new preregistered arms, need swarm run): N=57; rectangle n=20 hashed; N=35/37 top-ups; code arm.
QUEUED (venue-time restructure): section reorder; Tables 4/5 → supplement; §5-6 compression in full paper.
BLOCKED (user): open-weights arm (Kaggle login or OpenRouter key); author name for arXiv.

## Review 8 (hermes/deepseek-v4-pro, arm M delta + full paper, 90/100 submission-ready YES) — verdict: clean verify pass; 1 wording fix actioned

- Independently re-ran arm_m_analysis.py: all validity counts (15/15, 14/15, 7/12, 10/15), modal values (2.0, 2.5, 2.9285714, 3.5625), on-pred (1/0/0/6), rival 0/10, filler 35/36 — all confirmed against paper §3.4. Modal arithmetic shown and correct.
- Falsifier honesty: F-M1 3/3 TRIGGERED per registered wording; tie convention unexercised; no wiggle room found. F-M2 not triggered, correct.
- "Sharpening, not a rescue" framing judged legitimate — scope narrowing, negative result at equal prominence, no post-hoc salvage.
- Review 7 D1 declared RESOLVED; estimated review-7 revised score 78–82. D2 partial (post-hoc metrics disclosed), D3 essentially adopted, D4 caveat load-bearing.
- Only fix requested: abstract "truncates the (k*+1) grid" imprecise for N=20/30 (exact-fill rectangles, not truncations). DONE — s/truncates/moves to/ in paper1_draft.md, main.tex, compact3_draft.md.
- Minor note accepted without action: prereg vocabulary didn't anticipate the (k*+1)-grid-shift outcome; paper already reports it as observation, not prediction.
- Top remaining action per reviewer: one-parent mutation arm (120 invocations, conditioning test). QUEUED as next preregistered arm.

Score trajectory: 72 (r4) -> 88 (r6) -> 90 (r8). Compact: 80 (r5) -> 93 (r6-flash). User-side compact review: 71 (r7) -> est 78-82 post arm M.

## Review 9 (user-run, rubric-based, 85/100 accept-with-fixes) — verdict: best review yet; every checkable deduction CONFIRMED against ledger, all fixes applied

- D1 −2 (N=31 modal freq full-paper 12/17 vs compact 13/17): CONFIRMED — p11_mode_baseline.json says 12/17 with on_pred 13; compact was wrong. DONE — compact table fixed to 12/17; both formats now carry bucketing-convention clause on "7 of 7".
- D1 −2 (47/102 "every tier and container"): CONFIRMED — decomposition 41/57 + 1/30 + 0/4 + 5/11 excludes non-discriminating cells (9/12). DONE — wording rescoped + decomposition printed inline (md+tex+compact).
- D4 −3 (N=21 wave split 2/4 vs 10/11 impossible): CONFIRMED against ledger — true split 4/7 old vs 8/8 new; pooled new-wave 23/34 (68%), paper's 25/37 also wrong. DONE — corrected with in-text correction note (md+tex). Conclusion unchanged (drift argument holds, 68% figure coincidentally identical).
- D4 −3 (155/231 stale post arm M): fair. DONE — 155 scoped as pre-arm-M with disclosure arm M rows not swept; corpus restated 231 at rev-2 close, 288 with arm M (md+tex).
- D4 −1 (§3.4 "pre-registered rejection rule" vs §9 "not preregistered"): apparent contradiction, both true (arm M registered its own rule). DONE — clause disambiguated (md+tex).
- D2 −3 (Table 4 missing arm M rows): fair. DONE — six rows added: P-M1–M3 disconfirmed, P-M4 confirmed, F-M1 triggered 3/3, F-M2 not triggered, rejection rule (md+tex).
- §9 lists missing arm M artifacts: DONE — arm_m_preregistration.txt + arm_m_prompts.json in registration bullet, arm_m_collect.jsonl + arm_m_analysis.py in artifacts bullet (md+tex).
- Reviewer's key UNVERIFIED (F-M1 registered wording): resolved by review 8, which checked it against arm_m_preregistration.txt and found no wiggle room.
- Reviewer's projected post-fix score: 92–93.

## Review 10 (user-run Gemini, stale rev3 doc, 88/100) — verdict: NO-ACTION; score untrustworthy

- Its only shown recomputation is misattributed: calls V(3,4) = 1.7761424 the "empirical modal sum" at N=13 — that is the RIVAL the model never reaches (0 hits); modal is T(4,13) = 1.6250000.
- Invents model versions (Claude 3 Haiku / 3.5 Sonnet / Opus) the paper deliberately never names — review 2's error repeated.
- Violates our own rubric while citing it: deducts for self-disclosed tabled items (D2 −3 opus ladder inclusion, D5 −2 cap exclusions) and for the paper's own §6.4 fragility analysis (D4 −3) — rubric rule 1 says disclosed gaps cost nothing. ~8 of its 12 deducted points invalid. No per-deduction arithmetic, no UNVERIFIED list, no ledger evidence.
- Scored stale rev3 snapshot, predates review-9 fixes.
- Kept: nothing requiring change (its format-vs-geometry ask already implemented in §6.2). Venue facts plausible; strategy noted: AI-for-Science workshop (compact) then TMLR (full).
- Full record: review10_gemini_88of100_2026-08-05.md; review 9 verbatim at review9_rubric_85of100_2026-08-05.md.

## Council session 2026-08-05 (5 advisors + 5 peer reviewers + chairman) — actions taken

1. GM parse-path positive control (chairman's #1): FOUND REAL BUG — parse_packing() 2-tuple mishandled in arm_gm_analysis.py + arm_gm2_analysis.py (successful parse would misclassify as parse failure; invalid could score truthy-valid). Fixed both; GM2 rescored under corrected scorer: outcome UNCHANGED (0/140; 139 literal_eval SyntaxError + 1 no_bracketed_list; 140/140 finishReason=MAX_TOKENS). Control now 7/7 (diagnostics_gm_parse_control.py). Commit 07bdf64.
2. Arm MU (mutation, 135 inv) + arm CH (tractability choice probe, 45 inv) preregistered BEFORE sampling with council's required elements: MDE/power (0.83 at 70%->44%), numeric survive/dissolve thresholds (50%/20%) with non-overlapping Wilson regions, PARTIAL band with fixed sentence, tie-inclusive conventions, post-hoc-motivation + LLM-authorship provenance declaration, hard submission date 2026-08-12. Commit 2b7d202. Sampling wave 1 (18 B_rival haiku invocations) launched after commit.
3. Dual-submission check: TMLR editorial policy allows arXiv + non-archival workshop overlap; bars parallel archival only. Verify "non-archival" on chosen workshop page at pick time.
4. Chairman's tractability-confound point addressed by arm CH (the section-8 separating experiment, now registered).
5. Still user-blocked: author name/affiliation (gates arXiv v1), naive-human read-back gate, transcript release decision.
6. Not tunnel-visioned: flash-lite arm GM relaunched post-quota-reset (background); GM3 gemma running from 24/140 checkpoint.

## Arm MU/CH final outcomes (2026-08-05, 180/180 collected, zero runtime deaths)

- B_rival: anchor 0/26 valid (CI [0.00,0.13]), keep-or-improve 26/26, k-inheritance 26/26 -> registered DISSOLVES verdict, F-MU1 TRIGGERED. Title/abstract scoped to unconditioned calls per registered wording; section 3.5 added to all three paper versions.
- A_anchor: 25% (7/28) stay on own anchor; P-MU1 not met.
- C_offfamily: 58.8% (20/34) snap back to k* template from bad off-family parent; P-MU4 per-cell 2/3 (N=21, N=31; not N=13).
- CH registered verdict: P-CH1 holds 2/3 cells (valid-conditioned modal = T(k*,N) at N=13 and N=31 despite argmax printed in prompt). DISCLOSED survivorship artifact: all 31 invalid CH rows attempt the stated argmax (every one carries the family filler radius); 30/31 overlap from misplaced fillers (container corners instead of grid interstices), 1 parse (radical literals). Attempt-level reading: choice follows score table, execution fails off-template. Paper reports decomposition, not a winner: tractability wrong about selection, right about instantiation.
- Artifacts: arm_mu_collect.jsonl (180 rows verbatim), arm_mu_analysis.py (committed before sampling done), arm_mu_results.txt (frozen output), integrity check: 12 condition-cells all 15/15, no duplicate slots.
- Paper integration commit: section 3.5 + abstract + title word "Unconditioned" + section 8 two "not run" paragraphs closed + section 9 registration/artifact lists + corpus 288->468, mirrored md/tex/compact.

## Review 12 (deepseek-v4-flash via hermes dispatch, rev4+MU, 2026-08-05) - 98/100, Accept minor, submission-ready YES

Dispatched through handoff\dispatch.ps1 -Model deepseek-v4-flash (telegram messages_send lands in user DM, NOT hermes task queue - dispatch.ps1 is the working path; opencode-go flash 403 region-lock did not bite through this path). Reviewer recomputed every section 3.5 number from raw ledgers with its own scripts; zero discrepancies; git ancestry of prereg commit verified; Fisher/Wilson stats all matched.

My verification of its critiques (all checked against raw rows before acting):
- Deduction 1 (-1, CH N=31 4:3 margin unstated in prose): CONFIRMED (buckets 2.584 n=4 vs 2.748 n=3). FIXED: "(4 of 7 valid) against 2.7485281 (3 of 7) - a one-sample margin" in md+tex.
- Zero-point tie note: CONFIRMED (A31 2.594/2.584 both n=2; C13 all n=1). FIXED: tie-convention header added to arm_mu_analysis.py, arm_mu_results.txt regenerated, verdicts byte-equal.
- Optional abstract clause: APPLIED in md+tex+compact ("unconditioned calls only in the in-family-parent regime").
- REVIEWER ERROR caught in its zero-point note: claimed P-MU4 verdict tie-invariant. FALSE for N=13 - all-singleton buckets make the modal pick arbitrary; alternative tie-break flips False->True (3/3). Direction favors the paper (current False is conservative pick), so no claim change; disclosed in the new results header instead.

Score ledger: r8 90 -> r9 85 (fixes applied) -> r12 98 (post-MU/CH). Reviewer says 99 after deduction-1 fix (now applied).

## LaTeX structural verification, 2026-08-06 (opus)

main.tex (1369 lines, 101 KB) has NEVER been compiled - no TeX engine on the authoring machine (pdflatex/xelatex/lualatex/tectonic/latexmk all absent). Added latex1/texlint.py as a compile proxy. Result: structurally clean.

Checked: environment balance, brace balance, inline-math $ parity, undefined/duplicate labels, cite-vs-bibliography wiring, tabular/longtable column-count consistency, non-ASCII. Non-ASCII count is 0 (safest state for pdflatex). All four initial hits were lint bugs, not manuscript bugs, and each was confirmed by hand before being taught as an exception:
- "uncited bibliography" - FALSE. \nocite{*} present at main.tex:1277 with a documented rationale (manuscript cites inline by venue to stay 1:1 with the source markdown). Nearly "fixed" a non-bug here; checked the file first.
- "tabular 0/2 cols" x4 - FALSE. Regex stopped at the first } inside the user column type L{19mm}; replaced with a brace matcher.
- "caption row has 1 cell" x2 - FALSE. \caption* as the first longtable row spans all columns.

REMAINING RISK (needs user): the manuscript is still unverified against a real TeX run. texlint cannot see missing packages, overfull hboxes, or float placement. Installing a TeX engine requires a download, which is user-gated. Recommend compiling once on Overleaf/arXiv before the 2026-08-12 submission.

Note: 6 \label commands, 0 \ref - tables/figures are numbered by hand (\setcounter{table}{N} + \caption*) and referenced by name in prose. Consistent with the inline-citation choice; labels are inert. Not a defect, but hand-numbering can desync if a float is added.
