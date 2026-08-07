## How to Run the Precision Cliff Experiment

### 0. Reproduce the paper's figures (no GPU, no downloads)

Everything section 3 and section 4 report regenerates from the artifacts vendored in
this repository. Install dependencies once (`pip install -r requirements.txt`), then
run any of these from the repository root with **no arguments**:

| script | what it reproduces |
|---|---|
| `sec3_ladder_repro.py` | 14B ladder viability, validity, echo, per-seed and must-differ counts, and five of section 3's nine Fisher tails |
| `sec3_dispersion_registered.py` | both dispersion-probe waves: registered echo measures, the post-hoc decomposition, quality forks |
| `sec3_dispersion_prereg_rule.py` | wave 1's locked decision rule (returns *unclassified*) |
| `sec3_registered_echo_test.py` | wave 1's registered primary echo JT, `score_delta` CIs, orthogonality diagnostic |
| `sec3_artifacts/dispersion_probe_v2/analyze_v2.py` | wave 2's registered analysis and its `VERDICT: FAILED` label |
| `sec4_independent_rescore.py`, `arm_f_repro.py` | section 4's validity, taxonomy, scores and prompt digests |

Section 3's raw rows live under `sec3_artifacts/`. Four Fisher tails
(*p* = 5.7e-10, 0.001, 0.44, 1.0) are **not** replayed by any script and must be
computed from those rows directly; section 3 says so where it reports them.

The sections below describe re-running the *experiment*, which needs a GPU.

### 1. Upload to Kaggle (recommended, free GPU)

1. Go to kaggle.com → Notebooks → New Notebook
2. File → Import Notebook → upload `precision-cliff-kaggle.ipynb`
3. In the notebook, set `RUN_PILOT = True` in Cell 8
4. Run all cells (Runtime → Run All)
5. Kaggle gives you a T4 x2 GPU automatically
6. First run downloads ~4.5GB GGUF model, then runs 50 generations
7. Results appear in the output + saved to /kaggle/working/

### 2. Upload to Google Colab

1. Go to colab.research.google.com → File → Upload Notebook
2. Upload `precision-cliff-kaggle.ipynb`
3. Runtime → Change runtime type → T4 GPU
4. Set `RUN_PILOT = True` in Cell 8
5. Run all

### 3. Full Sweep (after pilot succeeds)

Modify the precision list in Cell 7 to iterate over:
- FP16, Q8_0, Q4_K_M, Q3_K_M, Q2_K

Run 5 seeds per precision. Expect ~50 min per seed on T4.
Total: ~25 hours GPU time. Kaggle gives 30h/week free.

### File Locations

Only files actually in this repository are listed. Anything named in sections 1-3
above (`precision-cliff-kaggle.ipynb` and the older `*-paper.md` /
`*-future-papers.md` / `findings.md` / `overview.md` drafts) lived on the
authoring host and is **not** in the release; those sections describe how the
experiment was originally run, not a procedure a reader can follow from a clone.
Reproducing the *figures* needs none of them — see section 0.

- `paper2_draft.md` — the current manuscript, and the only one
- `paper1_draft.md` / `latex1/` — companion paper
- `latex2/` — STALE conversion of paper 2, frozen 19 revisions back; see README
- `sec3_artifacts/` — every section 3 ledger, preregistration and provenance file
- `sec3_*.py`, `sec4_independent_rescore.py`, `arm_f_repro.py` — reproduction scripts
- `requirements.txt` — dependencies for those scripts
- `STATE.md` — project status
- `paper2_drafts/` — every revision of paper 2, one file per version