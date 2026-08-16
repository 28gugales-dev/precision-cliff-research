# TMLR submission build — Paper 2

Anonymized double-blind submission of `../paper2_short.md` in the official
TMLR stylefile. **Edit `../paper2_short.md`, never `body.tex`** — the tex
body is generated.

## Build

```bash
python3 preprocess.py      # paper2_short.md -> body.md (anonymize, headings, unicode)
pandoc body.md -f gfm -t latex --wrap=none --no-highlight -o body.tex
python3 fix_tables.py      # wrap longtables, breakable paths, \appendix, unnumber AI-use
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

Last verified build: 33 pages, 0 LaTeX errors, 0 overfull boxes, 0 BibTeX
warnings, 47 bibliography entries.

## What differs from paper2_short.md

- Author block removed; tmlr.sty (submission mode) prints "Anonymous
  authors". PDF metadata carries no author.
- Kaggle handle replaced with `REDACTED` (9 sites); an anonymization notice
  after the abstract explains it and the restore-on-camera-ready plan.
- One content addition, mirrored back into `paper2_short.md` and
  `paper2_draft.md`: the §7 paragraph on diversity-measurement traditions
  (distinct-n, Self-BLEU, Vendi; novelty search, MAP-Elites, FunSearch's
  island model).

## Before submitting (manual checklist)

- [ ] Re-read the AI-use statement against TMLR's current LLM policy.
- [ ] Decide the anonymized-artifact route (e.g. anonymous.4open.science
      mirror of this repo) and update the anonymization notice to point
      at it. Kernel *slugs* are still searchable on Kaggle; the notice
      covers this, but a reviewer determined to deanonymize could.
- [ ] Bibliography stubs (`alphaevolve`, `arxiv2605.29268`, HindsightBench
      etc.) reflect the manuscript's own cite-by-identifier convention;
      TMLR reviewers may ask for full entries — upgrade if asked.
- [ ] `\def\month{09}` in main.tex — set to the actual submission month.
- [ ] Switch `\usepackage{tmlr}` to `[accepted]` only after acceptance.
