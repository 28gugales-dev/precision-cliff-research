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
- [x] Proof of rendered PDF vs `paper2_short.md`, prose-parity pass
      (2026-08-16, agent): all 124 prose paragraphs shingle-checked against
      the rendered text. 112 matched verbatim; 12 flagged and each resolved
      as a deliberate transformation with content verified present —
      inline citations rendered via natbib \citet (4), unicode math
      normalisation (2), SHA/ellipsis line-rendering (3), and scientific
      notation re-typeset (`7.8e-13` → $7.8\times10^{-13}$, `1.6e-4` →
      $1.6\times10^{-4}$) (2), plus one long-digest wrap. No dropped or
      altered content found. Human skim still worthwhile but no longer
      load-bearing.
- [x] §7 related-work paragraph added (2026-08-16, mirrored in
      `paper2_short.md`, `paper2_draft.md`, `sec_forensic_repair.tex`):
      situates parent-echo against diversity metrics (distinct-n, Self-BLEU,
      Vendi) and QD search (novelty search, MAP-Elites, FunSearch islands) —
      pre-empts the "diversity metrics already exist" reviewer objection.
      Six bib entries appended (official arXiv bibtex); build re-verified
      clean (32 pp, 0 errors, same 2 pre-existing 3.5pt overfulls);
      `latex-tmlr-openreview.zip` rebuilt, leak check 0. USER should proof
      the paragraph's wording.
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
- [x] "Use of AI systems" reread: already a single tight disclosure
      paragraph. SUPERSEDED 2026-08-18 tightening pass
      (external-advisor round): both disclosures trimmed to short paragraphs,
      "referee/review" framing renamed internal adversarial checks, paper 1
      Table 5 (corrections ledger) replaced by a summary paragraph pointing at
      supplementary, both abstracts condensed (~200 words), paper 2 S3.6
      conditional-quality exclusion withdrawn (question stated open), arm V
      TRANSFERS cells carry Wilson CIs. Paper 1 now 29 pp, paper 2 33 pp.
      Overleaf v3 zips are the current builds (v2 stale).
- [x] Claims-cleanup pass (2026-08-17, agent, mirrored in `paper2_short.md`,
      `paper2_draft.md`, and all four tex fragments): fixed the stale
      "abstract's 0.12–0.94 range" cross-references (reattributed to
      Appendix C — now doubly needed since the tightened abstract dropped the
      range), corrected the stale §7 description of §6 item 4, renamed
      Appendix C's "pricing exercise" to horizon-power, softened five
      overclaiming sentences, added the wave-6 numbering disclosure and the
      7B/14B VRAM scope sentence in §8. Md keeps the long abstracts (main's
      tightening was tex-only); tex carries the condensed ones. Paper 2 tex
      rebuilt post-merge with the §7 diversity paragraph + 6 bib entries on
      top of the tightened tree; `overleaf_paper2_v3.zip` and
      `latex-tmlr-openreview.zip` rebuilt, leak-checked.
      USER should proof the reworded sentences (git diff shows them all).
- [ ] **Before zipping latex-tmlr/ for any upload: delete `main.log`,
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
- Claims-cleanup fixes re-applied post-merge (2026-08-18, agent), the five
  rev-3 still carried: matched 83%→100%→13% triple in abstract +
  Contribution 2 (per Table 2's own note), Contribution 3's "clean,
  well-powered" replaced with §6.5's CI + confound, §1 actionability
  scoped by arm MU, "never competitive" scoped to the bound table,
  antecedent-anchor claim labeled motivation-only, Fig 1 caption fixed
  (N=10…60, fifth penalty 4.66%) — mirrored in `latex-tmlr-paper1/`.
  Paper 2's cleanup + §7 paragraph merged with main's wave-7c/proofread
  state (abstract now carries both the sixth-family result and the 14B
  scoping; wave-6 numbering note adapted to "six later waves").
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
