# Template Anchoring & the Precision Cliff

Two companion papers on what an LLM proposal is actually made of — the template
the model emits, and the served precision behind it — plus every ledger, script
and preregistration behind both. Same benchmark throughout (circle packing,
scored by an exact local evaluator, no LLM judge), so every source of variance
sits on the model side of the interface.

**Interactive atlas of both papers:** https://soham-research.vercel.app —
every arm, wave, control and claim as a navigable graph.

## The papers

### Paper 1 — A Closed Form for What the Model Emits
**[paper1_draft.pdf](paper1_draft.pdf)** · source `paper1_draft.md`

Asked to place N circles in a unit square zero-shot, a weak-tier model does not
search — it emits a k×k grid template whose order is predictable in closed form
from N alone. The predicted mode matched the empirical mode at all 7 tested N,
with point predictions and prompt hashes registered before sampling. Across
tiers, constructive ambition rises while execution validity collapses
(78% → 100% → 13% valid). Two registered falsifiers triggered; both reported.

### Paper 2 — Served Precision Is Part of the Model
**[paper2_short.pdf](paper2_short.pdf)** · source `paper2_short.md` · *under review at TMLR* · extended version: [paper2_draft.pdf](paper2_draft.pdf)

Quantizing a proposer's weights can leave every metric a discovery loop watches
unchanged while collapsing the variation the loop depends on. Headline numbers,
all registered before the runs that tested them:

- 2-bit proposer parent-echoes **79% (19/24)** coordinate-verified vs **6% (1/17)**
  at q4_k_m — bound released before the run, held on never-sampled seeds
- must-differ probe: **5/5** coordinate-identical copies under an explicit
  instruction not to copy
- loop cost: **1 accepted hill-climb step in 50 calls** at 2-bit vs 14–16 at
  upper rungs, while final best score separates the rungs nowhere

Second half: what this means for studies addressing models by alias — a
forensic case study that became untestable within six days, and a repair
protocol audited against itself.

## Reproduce

Every figure traces to a released script over a raw ledger row. §3 artifacts
are vendored under `sec3_artifacts/` (95 files); the released scripts default
to the in-repo copies, so both of these run in a fresh clone with no arguments:

```bash
python sec3_dispersion_registered.py
python arm_f_repro.py
```

`arm_f_repro.py` replays all 215 paper-1 invocations and diffs its output
against the checked-in ledger field-by-field (MATCH 215/215). Full replay map:
`HOW_TO_RUN.md`. Dependencies: `requirements.txt`.

## Preregistration

Every preregistration commit is a git ancestor of the sampling it governs —
the ordering is checkable in this repository's history, not asserted. Several
registrations were additionally pushed as public Kaggle datasets before
sampling (SHA-256 in the files). Registered outcomes that failed are reported
under their registered labels alongside the ones that held.

## AI-use disclosure

Both papers study language-model behaviour and were written with
language-model assistance; harnesses, scoring scripts and prose were
model-drafted under the author's direction, with the full reasoning disclosed
in each paper (§9 / Use of AI systems). The human author is solely responsible
for the content.

## Layout

| where | what |
|---|---|
| `paper1_draft.md`, `paper2_short.md` | canonical manuscripts |
| `latex-tmlr/` | paper 2 TMLR submission build (compiles clean, pdflatex) |
| `arm_*`, `wave*`, `sec3_*` | per-arm runners, ledgers, preregistrations, analyses |
| `external_reviews/` | LLM referee reports + assessment log (disclosed) |
| `echo_screen.py` | standalone parent-echo canary for practitioners, no dependencies |
| `STATE.md` | full working log, every session, unedited |

Contact: 28gugales@gmail.com
