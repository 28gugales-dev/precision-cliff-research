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

## Queue state after this wave

DONE (committed): short-version fixes for D1/D2/D3/D5/D7/D8, loop-audit claim correction (all versions), tolerance diagnostic + disclosure, figures.
QUEUED (prose, cheap): weak-tier-law softening; bundled-intervention labeling; "0/11 rival" abstract lead; §5.4 rename; Fig 1 caption internal-note removal.
QUEUED (new preregistered arms, need swarm run): N=57; rectangle n=20 hashed; N=35/37 top-ups; code arm.
QUEUED (venue-time restructure): section reorder; Tables 4/5 → supplement; §5-6 compression in full paper.
BLOCKED (user): open-weights arm (Kaggle login or OpenRouter key); author name for arXiv.
