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
- [ ] Proof the rendered PDF against `paper2_short.pdf` section by section —
      conversion was agent-assisted; registered numbers + table-row parity
      already machine-checked, human read still recommended.
- [x] Anonymized supplementary bundle built: `supplementary_anonymized.zip`
      (351 files, 22 redacted, 0 identity strings after redaction, includes
      antecedent study). Builder: `build_anon_bundle.py`. Redaction of
      hash-locked preregs disclosed in BUNDLE_README.md. USER uploads.
- [x] Paper source zip built: `latex-tmlr-openreview.zip` (tex + bib + bbl +
      sty + pdf, no logs/aux). Leak-checked: 0.
- [x] "Use of AI systems" reread: already a single tight disclosure
      paragraph, ordering-checkability stated, no claimed review process.
      Verdict: keep as-is, no trim.
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
  (5 defects) fixed. `latex-tmlr-paper1/` compiles clean, **28 pp**,
  fidelity-audited against the markdown (5/5 fragments PASS).
- **Supplementary**: `build_anon_bundle.py` regenerated
  `supplementary_anonymized.zip` (6.2 MB, 0 identity leaks post-scan) now
  covering wave-7c, screen S, the full arm surface (F→V, GM chain) and all
  figure scripts. Upload per §Before-upload steps (user action).
- Remaining user actions: OpenRouter key rotation; optional DigitalOcean
  redemption for the registered-but-not-run 120B condition
  (`wave7c_addendum1_120b.md` stays advanced-not-run if never redeemed —
  reportable either way).
