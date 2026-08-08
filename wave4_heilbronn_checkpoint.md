# Wave-3 Heilbronn Checkpoint

Status of the registered Heilbronn reproducibility wave (`wave3_prereg_heilbronn.md`)
as of this session. New sibling file; no source artifacts were edited.

## Runner: re-verified by dry run

`sec3_artifacts/runners/kaggle_precision_sweep_14b_heilbronn.py --dry-run` passes on
this host. Verbatim config trace:

```
[selftest] evaluator + parser + grid-zero property OK
[config] runner_version = 14b_heilbronn_wave3_v1
[config] repo           = Qwen/Qwen2.5-Coder-14B-Instruct-GGUF
[config] task           = heilbronn_triangle_n13 (N=13, C(13,3)=286)
[config] q4_k_m  qwen2.5-coder-14b-instruct-q4_k_m.gguf  lineages=8 gens=15 calls=120
[config]         seeds = [3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108]
[config] q2_k    qwen2.5-coder-14b-instruct-q2_k.gguf  lineages=25 gens=15 calls=375
[config]         seeds = [3201..3225]
[config] total registered calls = 495
[config] q8_0           = NOT RUN by design (no second GPU; spec sec 3)
[config] must-differ    = 0 per rung (wave 3 registers none)
[config] sampling       = T=0.8 top_p=0.95 max_tokens=1200 n_ctx=4096
[config] seed parent score (recomputed) = 0.009087361292500006
[config] seed parent score (constant)   = 0.009087361292500006
[config] regular grid score             = 0.0
[dry-run] OK - no model downloaded, no GPU touched.
```

Key properties confirmed from the constant: seed-parent and grid scores agree with the
preregistered values (grid scores exactly 0.0, the property that lets a default template
be distinguished from a parent echo — the reason n=13 was chosen).

## Lock status

Wave-3 prereg is still DRAFT. It is not locked and the wave has not been run. Remaining
preregistration-lock steps:

1. Resolve the paper2 author item (see `PAPER2_AND_SCOPE_PLAN.md` — "outstanding author"
   is still open).
2. Publish SHA-256 of the runner (`runner_version = 14b_heilbronn_wave3_v1`) so the
   executed runner is timestamped against the registered one.
3. Push the runner to an externally-timestamped host (Kaggle/GPU host) before sampling,
   per the wave-3 spec.
4. Then execute the 495 registered calls (25 Q2_K lineages + 8 Q4_K_M lineages).

## Environment constraint

No GPU and no GGUF/llama-cpp runtime on this host; the wave must be executed on the
Kaggle/GPU host. The dry-run here verifies configuration and scoring only.

## What the paper currently claims about this wave

`paper2_draft.md` §8 (lines 1867-1882) describes the wave as "written and not run": the
runner "is written and dry-run verified; its header holds them in the form the fresh-seed
runner held F1-F3. **It is not locked and it has not been run**, and we claim nothing from
it." This checkpoint preserves that exact claim; the dry-run above is consistent with it.

## Next actions after this checkpoint

- If the author item resolves: perform steps 1-3 of the lock, then hand the runner to the
  GPU host with the SHA-256 recorded.
- If not resolved: keep the wave unlocked; the §8 "written and not run" claim stands
  unchanged.

## Session additions (this checkpoint's sibling work)

- `arm_f_zero_shot_topup_35.py`: N=35 top-up logger, dry-run verified, prompt hash pinned
  to `3b08c56e...` (== `arm_f_prompts.json["35"]`). Flag fixed so `--run` actually runs
  (was `--sample`). Not sampled; requires `--run` + API key to spend.
- `arm_canary_contamination_audit.py`: §8 contamination-attribution screen (P1 canary
  string, P2 N=46 absent template, P3 1x3 container), dry-run verified, 3x6=18 calls when
  run. Not run; §8's contamination sentence stays "screened-by-design, run optional".
