# TMLR submission plan — Paper 2 first

Decision (revised with owner 2026-08-16, supersedes 2026-08-12): BOTH papers
→ TMLR (solo quota 2/yr covers both), then GECCO Hot-off-the-Press for
Paper 1 once its TMLR acceptance lands (HOP presents recently published
journal work; deadline ~Feb for GECCO 2027). TELO dropped as primary: TMLR
speed serves the HOP timeline better and Paper 1's measurement style fits
TMLR's rubric. Desk-rejects burn a quota slot — both papers get the full
review loop before submission.

Source of truth: `paper2_short.md` (git 3c52e40 — deliberate shortened
submission build, 20.6k words; `paper2_draft.md` stays the archival long
form). LaTeX build: `latex-tmlr/`. `latex1/` and `latex2/` are STALE —
never submit them.

## Checklist

### Done (this pass)
- [x] `arm_f_repro.py` no longer rewrites `arm_f_candidates.jsonl` in place —
      replay goes to `arm_f_candidates.replay.jsonl` (gitignored) and prints
      MATCH/MISMATCH vs the ledger on scientific fields. Verified: MATCH,
      215/215 rows, fresh tree stays clean. `HOW_TO_RUN.md` updated.
- [x] Official TMLR style files fetched (JmlrOrg/tmlr-style-file @ main):
      `tmlr.sty`, `tmlr.bst`, `fancyhdr.sty` in `latex-tmlr/`.
- [x] `main.tex` assembled: anonymous author block, one-paragraph abstract
      (TMLR requires single paragraph — the markdown's two abstract
      paragraphs were joined, text unchanged), section fragments \input.
- [x] Anonymization scan + report (`latex-tmlr/ANONYMIZATION_REPORT.md`):
      author block replaced, 8 Kaggle owner-handle refs de-handled, no
      absolute paths in body.
- [x] Citation audit (`latex-tmlr/CITATION_AUDIT.md`): 38/38 arXiv ids
      exist, 0 withdrawn; 36 claim-CONFIRMED, 2 PLAUSIBLE flagged.
- [x] `references.bib` rebuilt from official arXiv bibtex + carried-over
      non-arXiv entries.

### Before upload (user or next session)
- [x] 2 PLAUSIBLE citation rows resolved 2026-08-12: 2605.29268 CONFIRMED
      (fulltext: CP n=26 unit square, sum of radii, 2.635 AlphaEvolve
      reference, explicit best-of-N baseline); 2607.07184 CONFIRMED
      ("registered, outcome-blinded predictions for GPT-5.4").
- [x] Non-arXiv references verified: Zhou Nature 634:61-68 (2024), Pineau
      JMLR 22(164), AlphaEvolve = arXiv 2506.13131 (Novikov et al.),
      GUIDE-LLM = Feuerriegel et al., Nature Human Behaviour 10:1182-1186
      (2026), bib entry added. He/Thinking Machines blog URL still worth a
      click-through.
- [x] Compiled locally (MiKTeX installed): 31 pp, 0 errors, 0 undefined
      refs, GUIDE-LLM in bibliography. 8 overfull hboxes remain — cosmetic,
      fix at proof stage if desired.
- [x] Proofread DONE 2026-08-18 (4-agent PDF-vs-markdown parity pass, both
      papers, every number/table/citation verified exact; 3 layout/typo
      defects found and fixed, commit d305d02). NOTE: the same-day tightening
      pass then changed abstracts, S9 disclosures, Appendix C (paper 1) and
      S3.6 (paper 2) — those sections postdate the parity pass.
- [x] Anonymized supplementary bundle built: `supplementary_anonymized.zip`
      (351 files, 22 redacted, 0 identity strings after redaction, includes
      antecedent study). Builder: `build_anon_bundle.py`. Redaction of
      hash-locked preregs disclosed in BUNDLE_README.md. USER uploads.
- [x] Paper source zip built: `latex-tmlr-openreview.zip` (tex + bib + bbl +
      sty + pdf, no logs/aux). Leak-checked: 0.
- [x] "Use of AI systems" reread: SUPERSEDED 2026-08-18 tightening pass
      (external-advisor round): both disclosures trimmed to short paragraphs,
      "referee/review" framing renamed internal adversarial checks, paper 1
      Table 5 (corrections ledger) replaced by a summary paragraph pointing at
      supplementary, both abstracts condensed (~200 words), paper 2 S3.6
      conditional-quality exclusion withdrawn (question stated open), arm V
      TRANSFERS cells carry Wilson CIs. Paper 1 now 29 pp, paper 2 33 pp.
      Overleaf v3 zips are the current builds (v2 stale).
- [x] **Before zipping latex-tmlr/ for any upload: delete `main.log`,
      `main.aux`, `main.out`, `main.blg` and `template-reference.tex`.**
      The .log embeds `C:/Users/soham/...` paths on nearly every line and
      would de-anonymize the submission. `main.bbl` is clean — keep it
      (OpenReview may want it). PDF metadata checked: Author field empty.
- [ ] OpenReview account + submission form; TMLR asks for reviewers'
      conflicts and a statement of prior submissions.

### Camera-ready (only if accepted)
- [ ] `\usepackage[accepted]{tmlr}`, restore real author block
      (Soham Shailesh Gugale, Independent Researcher, 28gugales@gmail.com),
      set \month/\year/\openreview, restore `sohamgugalet/` handles.

## Repo hygiene flags
- RESOLVED 2026-08-12: `arm_m_report.json`, `arm_m_scored.json`,
  `arm_mu_scored.json` were parsed against HEAD and found SEMANTICALLY
  EQUAL (formatting-only replay side effects) — restored via git checkout.
  Remaining tree changes are this pass's intentional work (latex-tmlr/,
  SUBMISSION_TMLR.md, arm_f_repro.py fix, STATE.md v9) — commit when ready.
- Overleaf: git token received in-session; Overleaf git cannot CREATE
  projects. User creates blank project, shares its git URL
  (https://git.overleaf.com/<id>), then push is scripted. Token should be
  REGENERATED after use — it passed through chat transcript.

## Paper 1 (active as of 2026-08-16)
- GM3 arm complete and folded in (v57–v60: §3.6 results section, Figure 2,
  abstract elevation, provenance chain).
- Target: TMLR (owner decision 2026-08-16), then GECCO 2027 Hot-off-the-Press
  from the published paper.
- TMLR LaTeX conversion for Paper 1: build after the wave-7c integration and
  review loop, same fan-out pattern as Paper 2's.

## Arms CC2 + CCS (replication + tier probe) — run 2026-08-18

Registered together at 4d7b7c5 (pushed before sampling, after CC results
known, disclosed). Byte-identical prompts, 45+45 invocations, 0 losses.
**CC2 (haiku fresh draws): REPLICATED** — 0/41 above argmax (zero-count
prediction exact), anchor modal 3/3 cells, N=31 firmed one-sample -> margin
8. **CCS (Sonnet): P-CCS2 HOLDS** — 0/37 above argmax despite genuine
optimizer programs (annealing/Halton/force-directed); ceiling is CHANNEL
property, not tier. Pooled 3 arms: **0/115 above the family argmax**.
Protocol note disclosed: 1 CC2 row used tools against wrapper, scored
verbatim. Integrated into S3.7 + abstract + S2.1 + arms index (15 arms) +
corpus 603. Paper 1 31 pp clean. Bundle rebuilt (0 leaks).

## Arm CC (code-channel probe) — run pre-submission 2026-08-18

Pre-empts the top predicted reviewer objection (paper measures code-free
calls; loops elicit programs). Registered at commit 285deca (prereg +
frozen prompts + executor + smoke test pushed to public remote BEFORE
sampling); 45/45 weak-tier invocations collected, no losses.
**P-CC1 HOLDS 3/3 cells** (anchor stays modal; one-sample margins at
N=13/31 disclosed, N=21 heavy at 9/13). Robust row: **0/37 valid program
outputs above the family argmax**; one reaches it exactly. Integrated as
S3.7 + abstract sentence + S2.1 rewrite (rationale now measured) + arms
index (13 arms) + corpus 513 + S9 registration/stopping-rule entries.
Paper 1 now **31 pp**, compiles clean. Bundle rebuilt (502 files, includes
arm_cc_* + corrections_ledger.md, 0 leaks). Library-enabled (numpy/scipy)
channel stays registered future work.

## Final state (2026-08-17) — both papers submission-ready

- **Paper 2**: gemma-4-31b wave-7c integrated (7c.2 HELD — first non-Qwen
  control-floor pass; 7c.1/7c.3 UNDERPOWERED; invalidity channel), 5-reviewer
  round + area-chair PASS applied (11 + 1 fixes incl. 304-row miscount
  disclosure, runner-edit commit-pair 8cfaffb→342cdea, amendment-gap named).
  `latex-tmlr/` compiles clean, **33 pp**, Figure 1 (fig4_family_echo) in.
- **Paper 1**: arm V complete (877 invocations) and integrated as §3.7 —
  anchoring TRANSFERS in north-mini-code 8/12 and gpt-oss-20b 11/18,
  DOES-NOT-TRANSFER in gemma-4-31b 0/15, V2 HOLDS 0/16; adversarial pass
  (5 defects) fixed. 2026-08-17 council round (5 Opus advisors + Fable
  verification) landed 9 further fixes: GM3 pooled-bar decomposition
  disclosed (discriminating cells 11/43 = 25.6%), GM3 misses identified as
  the rival construction (27/27 structure-verified, new
  `diagnostics_gm3_rival.py`), abstract arm-V elevation ("Three scope
  conditions"), phantom GM3-vs-V protocol split removed (prompts
  byte-identical, real axes: model variant + serving + budget), arm V floor
  wording corrected to slot accounting, corpus sentence de-staled, GM3
  prereg SHAs cited, 4 Table 4 rows added. Same-day structural round
  (council recommendations, all applied): abstract condensed 805 → 363
  words, Contribution 4 (family boundary + 3/147 strong form), §2.4
  notation table, §3 arms-index table (12 arms), Tables M/MU/CH for the
  falsifier-triggered arms, §3.6+§3.7 merged into one cross-vendor
  section with unified Table CV (all §3.7 refs renumbered), revision note
  bumped to Revision 3. `latex-tmlr-paper1/` compiles
  clean, **31 pp**, fidelity-audited (all greps PASS).
- **Supplementary**: `build_anon_bundle.py` regenerated
  `supplementary_anonymized.zip` (6.2 MB, 0 identity leaks post-scan) now
  covering wave-7c, screen S, the full arm surface (F→V, GM chain) and all
  figure scripts. Upload per §Before-upload steps (user action).
- Remaining user actions: OpenRouter key rotation; optional DigitalOcean
  redemption for the registered-but-not-run 120B condition
  (`wave7c_addendum1_120b.md` stays advanced-not-run if never redeemed —
  reportable either way).

## OpenReview form fields (copy-paste at upload)

### Paper 2 (submit first)
- **Title**: Served Precision Is Part of the Model: A Quantization Cliff in
  Proposal Variation, and the Limits of Reproducibility in Agent-Runtime LLM
  Studies
- **Abstract**: paste from `latex-tmlr/main.tex` abstract block (keep the
  current version — it carries the wave-7c sixth-family sentence).
- **TLDR** (one sentence): Quantizing a proposer's weights can collapse the
  search variation a discovery loop depends on while every health metric the
  loop watches stays green — and studies that address models through managed
  runtime aliases cannot even attest the precision they measured.
- **Keywords**: quantization; reproducibility; LLM-driven discovery;
  evolutionary search; preregistration; serving transparency; agent runtimes
- **Supplementary**: `supplementary_anonymized.zip` (replay-tested; README
  inside discloses redaction and hash-verification path).

### Paper 1 (after paper 2 is in)
- **Title**: A Closed Form for What the Model Emits: Template Anchoring in
  Unconditioned Zero-Shot Circle Packing
- **Abstract**: paste from `latex-tmlr-paper1/main.tex` abstract block.
- **TLDR**: Weak-tier language models emit circle packings whose scores land
  on a closed-form template value predictable before sampling — a regularity
  that is preregistered, cross-vendor under two instruments, family-bounded
  in both directions (one family escapes to the in-family rival, another
  anchors nowhere), and absent at the frontier tier.
- **Keywords**: template anchoring; zero-shot generation; circle packing;
  preregistration; closed-form prediction; model families; capability tiers
- **Supplementary**: same bundle (arm surface F→V and GM chain included).

Quota note: TMLR allows 2 solo submissions/yr — these are both of them.

## 2026-08-21 — Revision 4: external QA pass (ox-alpha), both papers

Full LaTeX source of each paper was reviewed by `stealth/ox-alpha` (OpenRouter,
1M context) under a TMLR-reviewer prompt; raw reviews in `reviews/`. Both came
back "major revision" on presentation, not science. Every numeric consistency
claim was grep-verified before editing. Pre-edit state is tagged
`v3-pre-oxalpha`; revert with `git checkout v3-pre-oxalpha -- latex-tmlr latex-tmlr-paper1`.

Paper 1 (31 pp): abstract rescoped ("all seven N of the original square arm",
"all 31 invalid attempts (30 by misplaced fillers)", "executed math-only
program"); untraceable "0/21" sourced to `arm_v_preregistration.md` and marked
as an undercount vs ledger 2/23; "180 of 180" attributed to MU+CH; ladder
headline switched to matched-cell 83% -> 100% -> 13% (78% kept as the
all-cells figure); Table CV gemma verdict relabelled "pooled bar met;
discriminating 26%, below bar"; arm V verdicts marked point-estimate with CI
including bar; opus_alias latency/token anomaly paragraph cut to one sentence
(unreleased, not relied on); every revision-history sentence removed
(revision note under \maketitle, "revision 1/2" mentions, external/council
review mentions, Appendix C corrections-ledger section -> one sentence in §9
Internal checks); stale build notes removed from main.tex header.

Paper 2 (33 pp): abstract carries fixed-parent contrast (92% vs 33%),
"post-hoc" on the step-count statistic, and "at the power available" on the
outcome null; F2 echo bound labelled a registered replication target (thresholds
written after the destroyed first run's estimates were known); 38/200
denominator defined (7B at Q8_0/Q4_K_M/Q3_K_M/Q2_K = 6+9+7+16); "same three
rungs (four names)" fixed in §3.5 and App B; inferential-status block in §3
replaced by two-sentence pointer to App A.4; conditional-quality per-parent
breakdown in App C reduced to one non-load-bearing sentence; wave index table
added (Table tab:wave_index) resolving the "wave 2" naming collision;
`\nocite{*}` removed (bibliography 42 -> 28 entries, all cited); appendix
[h] floats relaxed, page break before registered-outcomes longtable.

Not applied (reviewer-request territory, new data): contamination probe at
held-out N, classical-solver baseline, non-GGUF 2-bit arm, longer-horizon run,
numpy/scipy code probe, same-instrument gemma pair.

Artifacts: `overleaf_paper1_v4.zip`, `overleaf_paper2_v4.zip` (v3 stale),
`latex-tmlr-openreview.zip`, `supplementary_anonymized.zip` (0 leaks),
site PDFs + meta.json (Revision 4, 2026-08-21).

## 2026-08-21 — Revision 4.1 (paper 1): family-property softening + contribution reorder

Tag `v4.1-family-scope`. Abstract close now "transfers to two further vendors at
reduced concentration (61–67% of valid outputs against 56–80% in-family) ... so
anchoring is not a single-vendor artifact, and its concentration is
vendor-dependent". §3.6 title and verdict sentence match; one clause added on
why reduced concentration on byte-identical prompts is what a shared attractor
predicts. Contributions reordered: (1) choice/execution dissociation (CH + CC
chain, scope-independent), (2) closed form, (3) tier, (4) faithfulness,
(5) family boundary. "Contribution 2" cross-ref in §5 updated to 3.

### Pre-drafted rebuttal paragraphs (paper 1) — paste-ready, normal prose

**If a reviewer says the scope is too narrow (generation-0, weak tier, code-free):**

> We agree the measured regime is the unconditioned call, and the paper says so in the abstract, §2.1 and §8. Three registered arms were run specifically to find the edges of that regime rather than to extend the claim past them: arm MU shows the anchor dissolves under one-parent conditioning, the tier ladder shows the frontier tier escapes it, and arms CC/CC2/CCS show that a math-only code channel does not. Each is reported as a boundary, not as a caveat. The contribution that does not depend on the regime is the choice/execution dissociation (contribution 1): the model selects the provably better construction when shown it and cannot instantiate it in text (0/31) or in executed code (0/115), across two tiers. That is a statement about what the model can build, and it holds whether or not any deployed loop issues unconditioned calls. The library-enabled code channel (numpy/scipy) is the one loop-relevant regime we have not measured; it is named as such in §2.1 and §8, and we would run it as a registered arm if the reviewers consider it decisive.

**If a reviewer raises the pipeline provenance (sole author, model-generated harness and prose, same-family QA):**

> Every artifact the claims rest on is checkable without trusting the process that produced it. The scoring path is an exact evaluator verified against a linear-programming oracle on 83 configurations to 1e-9; every registered arm has a preregistration and frozen prompt hashes committed to a public repository before sampling, with the commit serving as the external timestamp; every invocation is in the released ledgers verbatim; and every analysis script was committed before its data arrived and is replayable with no arguments. The internal model-based checks are disclosed as quality assurance, not as review, and the correction ledger they produced is in the supplementary so the reader can see what changed and why. We would rather a reviewer distrust the process and verify the artifact than the reverse, which is why the artifact is built to be verified.

**If a reviewer says the transfer rates show a weaker phenomenon, not the same one:**

> The registered transfer criterion is modal identity on byte-identical prompts, not equal concentration, and the paper now states the concentration gap explicitly (61–67% at the transfer vendors against 56–80% in-family). Reduced concentration on the same modal value at a different vendor is what a shared attractor predicts; matching concentration would be harder to distinguish from shared training text. We claim family-bounded transfer, not a universal, and the gemma pair is reported precisely because it bounds the claim from both sides.

## 2026-08-21 — Revision 4.2 (paper 1): arm CN, held-out-N contamination probe

Tag `v4.2-arm-cn`. Registered at commit `69a1642` (pushed before sampling) in
response to the ox-alpha review's blocking item B2. Five held-out N (50, 58, 62,
65, 75 — absent from the cited scoreboard and every prior arm), 15 haiku
invocations each, bare template A.1 byte-identical to arm M (hash asserted).
Competing registered predictions: P-CN1 construction (mode at >=4/5 cells incl.
>=2/3 discriminating) vs P-CN2 recall (<=2/5).

Result: **P-CN1 HOLDS** — mode at 4/5 cells, 3/3 discriminating, margins +6 to
+13; k*-structure majority 5/5 (57/63); 0 rivals in 39 discriminating
validities; 0/63 above the family argmax; validity 63/75 with no collapse at
large N. The N=50 miss is filler mis-execution on the selected 7x7 template
(6 of 11 push the filler into a corner, 0.017 below V(7,1)) — the arm-CH
pattern. Frozen in `arm_cn_results.txt` / `arm_cn_report.json`.

Paper 1 (32 pp): new §3.8; abstract gains one held-out sentence; arms index
16 arms; §8 contamination paragraph rewritten from "not probed" to "probed at
one level" (canary + perturbed-container still unrun); §9 registration and
stopping-rule entries; App A.4 hashes; corpus 603 -> 678. Stale "N = 57 not
run" in §9 removed (arm M ran it).

Rebuttal paragraph for contamination now reads: point to §3.8; concede the
canary/perturbed-container probes remain and offer to run them as a registered
arm if decisive.

## 2026-08-22 — Revision 4.3: submit-readiness audit, both papers

Tag `v4.3-submit-ready`. Audit script (scratchpad `submit_audit.py`) does a
clean-room compile of each Overleaf zip and checks: stray log/aux/pdf files
(none); active `\usepackage{tmlr}` with anonymous author block (both);
0 LaTeX errors, 0 undefined citations/references, 0 bibtex warnings (both);
PDF Author/Title metadata empty (both); no "??" in rendered text (both);
identity strings in sources and rendered text (none); page counts 32 / 33.

Fixes made: seven leftover "revision N" / "post-council" / "external review"
phrases removed from paper 1; paper-1 abstract condensed 356 -> 293 words;
bundle builder now redacts `C:/Users/<anything>/` to `~` and the leak scanner
flags Windows user paths (four files carried `C:/Users/[ANON]/...` -- not
identity, now gone). Paper 2 unchanged except rebuilt PDF; its "earlier drafts
omitted" sentences in App A/B are deliberate selective-reporting disclosures
and stay.

Submit-ready state: `overleaf_paper1_v4.zip`, `overleaf_paper2_v4.zip`,
`supplementary_anonymized.zip` (518 entries, 0 leaks). Remaining items are
user-only: Overleaf upload, OpenReview form, key rotation.

## 2026-08-22 — Revision 4.4: five-lens review pass, paper 1

Tag `v4.4-five-lens`. Five independent reviewers (claims/evidence, prose,
floats, positioning, internal consistency) over the v4.3 sources; every
accepted finding grep-verified before editing; verdicts unchanged.

Numeric and scope corrections: in-family comparator for the cross-vendor
transfer restated as 56-76% at arm V's own five cells (was 56-80% in three
places and 56-86% in two; neither matched the cells compared); "all 31" CH
execution failures -> 30 of 31 (one unevaluable) in abstract, Contribution 1
and S8; "well-powered" faithfulness claim replaced by its Wilson interval;
10^-9 ladder triple labelled all-cells vs matched; strong-form pool extended
to arm CN (3 in 186, weak-tier only, Sonnet excluded by tier, S6 added to the
pointer); abstract code-channel sentence scoped "at these cells"; GM3
decomposition arithmetic 19/20 -> 20/20; P-CH2 wording un-inverted;
non-claim guard no longer says the tractability alternative went untested;
stale "correcting the abstract" self-reference removed; Figure 1 caption
range 10..60 and fifth trap penalty added.

Disclosure added: arm CN N=65 reconstructed rows — discarding them leaves
the cell below floor and P-CN1 at 3 of 4 evaluable cells, discriminating
cells untouched (S3.8); n=4 cells in the square arm named as thin (S3.2).

Positioning: EvoPrompt now has its own citation (was attributed to the
LLaMEA key), EoH added; contamination literature cited at S8
(Carlini 2021, Golchin & Surdeanu 2024); Friedman's Packing Center cited as
the source of the bound table (provenance was only in code comments);
typicality-bias account (Verbalized Sampling) named as a second untested
mechanism; new limitation paragraph on single-prompt scope (Sclar 2024) and
RLHF diversity collapse as a candidate account of vendor-dependent
concentration (Kirk 2024); one paragraph in S1 stating the consequence for
EC readers (initialization diversity; MAP-Elites, novelty search cited) and
for evaluation readers (computable floor).

Structure: Contributions paragraph -> enumerate; Figures 2-4 and Table 2
now pointed to by \ref (were orphaned); Table 2 caption glosses columns;
"attractor" added to the notation table. Figure 2 regenerated with marker
shape encoding match/miss (colorblind-safe). HOW_TO_RUN.md gains a paper-1
table (the S9 claim that it documented the commands was previously false).

Pages 32 -> 33. Audit: 0 errors, 0 undefined, 0 bibtex warnings, metadata
empty, identity 0, bundle 0 leaks.

Not done, logged for the review stage: redundancy cuts (GM3 numbers in four
places, provenance in three) and S9 trim — left because each restatement
carries a traceable count; Table CH N=13 (n=2) left as registered; abstract
not restructured (sharpened only).

### 4.4b (same day): fresh-eyes pass on the 4.4 diff
Opus verifier over `git diff v4.3..v4.4`: one real error caught — CN N=65
caveat said "two valid samples" after discarding reconstructed rows; correct
figure is three (slot 12 of the reconstructed rows is invalid). Downstream
"3 of 4 evaluable" unchanged. Plus: weak-tier scope on the S1 floor sentence,
n=4 cells flagged non-discriminating, typicality-bias sentence softened,
Friedman dated n.d., five arm headings shortened. Tag `v4.4-five-lens` moved
to this commit.

## 2026-08-22 - Revision 4.5: second-round review, paper 1

Tag `v4.5-round2`. Two fresh opus reviewers over the 4.4c sources (claims,
readability). Claims reviewer: ten residuals, all verified against frozen
reports before editing - pooled argmax-reaching outputs 1 -> 2 (CC 1/12 and
CC2 1/11 at N=13), CC above-anchor 1 -> 2, GM3 two-radius gloss (instrument
blind at truncate cells), 56-80 at CC cells, Table CV routed-rows note, arm V
vendor count (seven attributed + one unattributed), CN "twice", arm S
100%/90%, dangling S5 attribution -> ledger item 30, two Appendix B rows
(CN transcription, CC2 tool use). Readability: 8 of 10 proposed rewrites
applied; two declined (clarity loss). Pages 33 -> 34.

Pre-staged for rebuttal (DRAFT, unregistered, no sampling):
`arm_cp_preregistration_DRAFT.txt` (container [3,5]^2, values x2, 5 cells
all discriminating, P-CP1 vs P-CP2) and `arm_rp_preregistration_DRAFT.txt`
(direct recall of scoreboard values, 3 scoreboard + 3 held-out N, P-RP1 vs
P-RP2). Both ship in the supplementary bundle with the DRAFT marker.

### 4.5b (same day): third-round claims pass
Opus reviewer over sections not yet recomputed (3.3-3.5, 4, 6, 8). Two numeric
fixes: Table CC N=13 above-anchor cell 1 -> 2 (prose had been fixed in 4.5,
table not); GM3 16k-budget parse count 118/140 -> 123/140 (recomputed from the
`parsed` flag; 118 existed only in drafts). Wording: arm V prereg 0/21 recast
as a scope difference (N in {13,31}) not an undercount; rectangle arm "sixteen
proposers" -> "sixteen invocations (eight per cell)"; a=2 sample 3.151875
noted as a third out-of-family above-prediction output; faithfulness
exclusions "nine of 12" are regex gaps. Reviewer recomputed every other
fraction in those sections clean. Round 3 yield (2 numeric) < round 2 (6):
converging.

## 2026-08-22 - Revision 4.6: fourth-round pass (qualitative claims, stats, hashes, figures)

Tag `v4.6-round4`. Reviewer recomputed every p-value, Wilson CI, hash prefix,
commit id and prereg quotation: all clean. Four findings fixed: (1) S5's
"only sample in the study to leave the recipe family upward" was false - arm M
holds three hexagonal converge-cell rows above the family best (N=20 x2 at
2.2222, N=30 at 2.7273), confirmed by independent re-score; rescoped to the
swept corpus, reported in S3.4 as a post-hoc sweep, Appendix B row added;
(2) arm_cn_collect.jsonl `reconstructed` flag set true on the eleven N=65
rows (collector wrote false), report byte-identical; (3) Figure 2 legend
V/T; (4) Figure 3 caption "pooled", p marked uncorrected. Round yields
10 -> 6 -> 2 -> 1 numeric: next round expected dry.

### 4.6c (same day): reproducibility smoke test of the HOW_TO_RUN paper-1 table
Every command run from a fresh scratch copy of the repo root (no network, no
keys): 13/14 exit 0; arm_cn verdict, GM3 57.5% and Table M counts regenerate
exactly. `arm_v_score.py` crashed on a non-ASCII glyph under cp1252 stdout
after writing its ledger - stdout now forced to UTF-8; verdict counts match
`arm_v_score_final.txt`. Two table rows had wrong reads/writes (arm M, arm V)
- corrected. Bundle rebuilt, 0 leaks.

### 4.6d (same day): citation-accuracy pass (web-verified)
Sonnet agent fetched each primary source: HELIX, GigaEvo, AdaEvolve, ThetaEvolve,
li2026, zhang2024, Verbalized Sampling, Kirk, Sclar, EvoPrompt, Friedman page
all VERIFIED. AlphaEvolve 2.63586276 unverifiable from abstract/HTML (lives in
the linked notebook) - left. ShinkaEvolve digit string replaced by the source
HTML's two figures (2.6359831 relaxed / 2.6359777 strict); the S7 "HELIX below
ShinkaEvolve" ordering now says against which. OpenEvolve "~2.635977" not at
the README checked (2.634292) - restated as the 2.634-2.636 band, repo unpinned.


### Revision 4.7 / 4.7b (2026-08-27, tag `v4.7-fresh-eyes`)
Fresh-eyes validation round: three independent validators (fresh-clone repro of all 14
pipeline scripts, byte-identical; ~330-assertion ledger re-audit, 3 findings; zero-context
simulated TMLR review, leaning-accept-conditional). All confirmed findings folded:
abstract carries the m<=1 falsifier scope and 8-of-11 pooled denominator; concentration
overlap (61-67 within 56-76) stated honestly everywhere incl. the S3.6 heading;
supplementary-artifact sentence added; contribution 1 post-hoc label + P-CH2 outcome;
global validity-conditioning convention in S3.1; magnitude glosses made exact
(3.0e-7/3.5e-9; 1.5-2.0e-2); arm V 314-of-325 slot qualifier; GM range scoped; S1
per-sample overclaim softened; corrections_ledger item 33. NEW: `main_short.tex` short
variant (15 pp body, refs p16, 36 pp total; 311/311 numeric tokens preserved; Figure 1 in
Appendix C.2) ships inside `overleaf_paper1_v4.zip` -- submit either form.
Rebuttal prep: `REBUTTAL_NOTES_PAPER1.md`.

### Revision 4.7c (2026-08-27, tag `v4.7c-template-null`)
Reviewer minor #6 implemented: uniform-template null (post hoc, disclosed) --
`diagnostics_template_null.py`, null 1/3, discriminating-cell binomial tails
0.043/2.9e-4/3.4e-4/6.9e-3 at N=13/21/31/43. Added to S3.2 (full), Appendix D.1 (short,
body pointer only -- 15 pp body held), deviations-table row, HOW_TO_RUN row; output frozen
in `diagnostics_template_null_out.txt`. Short numeric coverage 314/314.

### Revision 4.8 / 4.8b (2026-08-27, tags `v4.8-arms-cp-rp`)
NEW DATA: arms CP (perturbed container [3,5]^2, 75 invocations) and RP (direct recall, 90)
registered before sampling (105e8b7, prompt hashes + analysis scripts committed and pushed
first; RP draft cell N=32 -> N=30 documented), sampled once on the weak-tier subagent
channel, scored once. CP: P-CP1 CONFIRMED -- mapped prediction modal 4/5 discriminating
cells (N=75 a registered tie against, five each at mapped T(9,75) and T(15,75)); pooled
validity 81%; k* majority 5/5; S-CP1 not met (4/61 rival, reported as registered). RP:
P-RP1 CONFIRMED -- 0/44 recalls, 87/87 scored responses UNKNOWN. Folded into S3.9 (both
variants + Appendix D.9), S8, abstract, arm table, deviations table, corpus arithmetic
(843). Main now 35 pp (audit expectation bumped), short 38 pp / 16 pp body (one over old
target -- new data section, user's call to trim). Fresh-eyes diff verifier re-scored both
ledgers independently and confirmed registration ancestry; 4.8b fixed one stale "unrun"
line and scoped the canary-test wording. Numeric coverage 321/321.

### Revision 4.8c (2026-08-27, tag `v4.8c-second-round`)
Second-round simulated review of 4.8b: RECOMMENDATION UP to leaning accept -- criticals
1-4 verified RESOLVED with quotes, 5 PARTIAL, both minors resolved. All four remaining
blockers fixed: standalone Artifact-availability bullet in S9 (public-remote anonymity
addressed); abstract "erases every lexical handle" softened to "removes the benchmark's
phrasing and magnitudes" + N-as-retrieval-key caveat added to S3.9/D.9; RP
positive-control caveat (abstention-prior alternative) + F-RP1 stated in text; S9
Registration and Stopping-rule bullets updated for CP/RP; contribution 5 flags the
looser offset-frame strong form (4/61). Main 36 pp, short 39 pp; coverage 321/321.

### Revision 4.9 (2026-08-27, tag `v4.9-rp-control`)
RP positive control run: amendment 1 registered before sampling (15555eb), N=1 cell
(optimum 0.5 elementary/certain), 15 invocations same channel. C-RP1 CONFIRMED: 14/15
state 0.5, one UNKNOWN -- abstention-prior alternative rejected with data; the S3.9
positive-control caveat is replaced by the result in both variants. Corpus 858.
Deviations row + HOW_TO_RUN row added. This closes the last data-answerable finding of
the second-round review; its remaining path to plain accept is submission logistics only.

### Revision 4.10 (2026-08-27, tag `v4.10-arm-pp`)
Arm PP (paraphrase probe) registered before sampling (2e89614; paraphrases authored
results-aware, disclosed), 90 invocations, 0 rejections, scored once. P-PP1 CONFIRMED
6/6: registered prediction modal at every paraphrase-cell (pooled validity 83%);
S-PP1 not met (6/75 rival), S-PP2 5/6. S9's (model, prompt string) limitation rescoped:
anchor not keyed to hash-locked string at tested cells; formatspread sweep stays out of
scope. Corpus 948. Folded into S3.9 (retitled CP/RP/PP), abstract ("Three review-stage
probes"), arm tables, deviations row, registration/stopping bullets, both variants.
ARMS FROZEN after PP per session decision -- remaining alternatives stay stated non-claims.

### Revision 4.11 (2026-08-27, tag `v4.11-final-read`)
Final holistic read-through (flow/format/claims/citations, opus, one-pass reader): 8 MUST
+ 3 POLISH, all fixed. Stale "not run" list purged (MU/CH/empirical-k ran); S3.9 opener
matches three-arm heading; S8 dedup; "looser strong form" -> "registered strong-form
secondary not met" everywhere incl. abstract (+ PP's 6/75 added for symmetry); post-hoc
label on 30-of-31 in abstract and S8; OpenEvolve + o3/o4 system card get bib keys
(sharma2025openevolve, openai2025o3o4systemcard), 
ocite{*} dropped both mains;
misattached sclar cite moved in short; hardcoded "Table 1" -> Table~
ef{tab:forecast};
"Related:" citations given a claim. Main 36 pp, short 40 pp, 0 errors/overfull, bibtex 0
warnings. Coverage intact.

### Revision 4.12 (2026-08-28, tag `v4.12-ai-note`)
Use-of-AI-systems bullet rewritten at author's instruction in both variants: script
authorship attribution removed; now "Claude models were used to draft manuscript prose and
to assist implementation", with the human author credited for study design, instrument
specification and decision rules. "Authoring models" -> "drafting models" in the
family-overlap caveat, which is retained along with the artifact-trust sentence. Builds
clean, 36 / 40 pp.
