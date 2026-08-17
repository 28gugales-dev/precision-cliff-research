# TMLR submission plan — Paper 2 first

Decision (from venue analysis, 2026-08-12): Paper 2 → TMLR now; Paper 1 →
hold for GM3 cross-vendor completion, then ACM TELO (quota-free). TMLR solo
quota is 2 submissions per calendar year and desk-rejects burn a slot, so
Paper 1 does not go to TMLR unless Paper 2's review round argues for it.

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
- [x] Anonymized supplementary bundle built: `supplementary_anonymized.zip`
      (351 files, 22 redacted, 0 identity strings after redaction, includes
      antecedent study). Builder: `build_anon_bundle.py`. Redaction of
      hash-locked preregs disclosed in BUNDLE_README.md. USER uploads.
- [x] Paper source zip built: `latex-tmlr-openreview.zip` (tex + bib + bbl +
      sty + pdf, no logs/aux). Leak-checked: 0.
- [x] "Use of AI systems" reread: already a single tight disclosure
      paragraph, ordering-checkability stated, no claimed review process.
      Verdict: keep as-is, no trim.
- [x] Claims-cleanup pass (2026-08-17, agent, mirrored in `paper2_short.md`,
      `paper2_draft.md`, and all four tex fragments): fixed the stale
      "abstract's 0.12–0.94 range" cross-references (the short abstract no
      longer contains the range — reattributed to Appendix C), corrected the
      stale §7 description of §6 item 4 (it is serving-signature disclosure,
      not decode-path attestation), renamed Appendix C's "pricing exercise"
      to horizon-power, scoped the abstract's step-collapse to 14B, softened
      five overclaiming sentences to the paper's own hedged register (intro
      serving-path attribution, §6 "every study" opener, timing "ruled out",
      "any study inherits this", must-differ "not reachable by instruction"),
      added the wave-6 numbering disclosure, the 7B/14B VRAM scope sentence
      in §8, and 1.79998-style consistency. Rebuild: 32 pp, 0 errors, same
      2 overfulls; `latex-tmlr-openreview.zip` rebuilt, leak check clean.
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

## Paper 1 (parked)
- Claims-cleanup pass done 2026-08-17 (agent): §9 stopping rule rewritten
  (it falsely listed arms MU/CH/M/k-back-out as not run), GM+GM2+GM3+V
  preregs and ledgers added to §9's registration/artifact bullets, corpus
  468 reconciled (cross-vendor arms ledgered separately), abstract +
  Contribution 2 now quote the matched 83%→100%→13% triple per Table 2's
  own note, Contribution 3's "clean, well-powered" replaced with §6.5's
  actual CI and confound, Fig 1 caption fixed (N=10…60, fifth penalty
  4.66%), byline revision note de-internalized, arm V disclosed in §8
  (270 rows, 5 valid, repairs registered, not yet resumed), and four
  overclaims softened. USER should proof the diff.
- STILL MISSING for TELO (deliberate, do at conversion time): References
  section (~50 inline arXiv IDs need bibliography), Conclusion section,
  CCS concepts/keywords, artifact-availability URL/DOI.
- Arm V: resume per amendment 3 or report as transport-failed; 5/270 valid
  supports no analysis either way. GM3: 41 calls left (GM3_RESUME.md).
- Wait for GM3 arm; fold result in (preregistered, both branches reportable).
- Target ACM TELO (rolling, no quota). GECCO 2027 (abstract ~late Jan) is
  the fallback; page limit would force cutting appendices.
- No TMLR conversion built for Paper 1 on purpose.
