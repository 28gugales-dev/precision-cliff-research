## How to Run the Precision Cliff Experiment

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

- `research-corpus/precision-cliff-kaggle.ipynb` — the notebook
- `research-corpus/precision-cliff-paper.md` — paper draft
- `research-corpus/precision-cliff-future-papers.md` — future directions
- `research-corpus/precision-cliff/paper-outline.md` — outline
- `research-corpus/precision-cliff/STATE.md` — project status
- `research-corpus/precision-cliff/findings.md` — findings log
- `research-corpus/precision-cliff/overview.md` — full spec