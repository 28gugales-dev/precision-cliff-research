# Wave 7c prep sheet — NOT a preregistration

Working notes only, written 2026-08-16 while screen S (screen_s_doc.md) was
still queued. The wave-7c prereg proper is written AFTER the screen tally,
names only the advancing family/families, and is locked (SHA-256 as public
Kaggle dataset) before any sampling — same mechanism as waves 7/7b. Nothing
in this file constrains anything; it exists so the prereg can be assembled
in minutes.

## Ladder-ready configs (Q2_K/Q4_K_M presence verified via HfApi 2026-08-16)

| family | REPO | PRECISIONS files | fits Kaggle T4x2 |
|---|---|---|---|
| gemma-4-31b-it | `mradermacher/gemma-4-31B-it-GGUF` | `gemma-4-31B-it.Q2_K.gguf`, `gemma-4-31B-it.Q4_K_M.gguf` | yes (~12/19 GB) |
| nemotron-3-nano-30b-a3b | `bartowski/nvidia_Nemotron-3-Nano-30B-A3B-GGUF` | `nvidia_Nemotron-3-Nano-30B-A3B-Q2_K.gguf`, `nvidia_Nemotron-3-Nano-30B-A3B-Q4_K_M.gguf` | yes |
| gpt-oss-20b | `unsloth/gpt-oss-20b-GGUF` | `gpt-oss-20b-Q2_K.gguf`, `gpt-oss-20b-Q4_K_M.gguf` | yes |
| north-mini-code-1.0 | `bartowski/North-Mini-Code-1.0-GGUF` | `North-Mini-Code-1.0-Q2_K.gguf`, `North-Mini-Code-1.0-Q4_K_M.gguf` | yes |
| nemotron-3-super-120b-a12b | `bartowski/nvidia_Nemotron-3-Super-120B-A12B-GGUF` | (rung files unverified) | NO — rented A100-80GB only |

Caveat to disclose if gpt-oss-20b advances: its native release is MXFP4;
Q2_K/Q4_K_M are community conversions, so the "parent" full-precision
reference differs in kind from the dense-model waves. Prereg must name this.

## Seeds

Prior fresh-seed blocks: 71xx (wave5?), 72xx, 73xx (phi4), 74xx (mistral24b),
plus [2222,3333,5555,7777,9999] and the original [42,123,456,789,1111].
Next blocks, grep-verified unused in any runner as of this commit:
first advancing family `[7501..7505]`, second `[7601..7605]`.

## Procedure at screen-tally time

1. Fill winner(s) into the wave-7c prereg (template: wave7b_prereg_families_14b.md
   structure — predictions 7b.1/7b.2/7b.3 verbatim, per family, no pooling,
   same power floor >= 20 valid rows/rung, same disconfirmation branches).
2. Runner: copy `kaggle_wave7b_phi4_14b.py`, substitute REPO / PRECISIONS /
   SEEDS / labels; protocol byte-identical (5 seeds x 10 gens + 10
   must-differ per rung, temperature 0.8, top_p 0.95, MAX_TOKENS 1200,
   N=26, EPS=1e-6).
3. Push prereg as public Kaggle dataset; record SHA-256 in kernel header.
4. Push kernel(s) public, launch on T4x2. ~1.5-2 h wall per family.
5. `wave7c_analysis.py` = wave7b_analysis.py with paths/family names swapped.
