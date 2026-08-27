# GM3 resume runbook — finish the Gemma weak-tier arm

State as of 2026-08-16: `arm_gm_gm3_checkpoint.jsonl` holds **99/140 content
rows, 0 transport-error rows, 0 duplicates** (verified). Complete cells:
N=13/17/21/31 (20/20 each). Remaining: N=35 (1 call), N=37 (20), N=43 (20)
— **41 calls**. The run stalled on daily free-tier quota, not on an error
(runner sets `quota_dead` and exits; checkpoint resume is built in).

Prereg: `arm_gm3_preregistration.txt` (registered 2026-08-03, before
sampling). Design = GM2 (prereg 3019aab) with `maxOutputTokens` 16384.

## Resume command

Put your Google AI Studio API key in a file OUTSIDE the repo (never commit
it), then from the repo root:

```bash
GM_MAXTOK=16384 GM_TIMEOUT=900 \
  python3 arm_gm_run.py /path/to/google_api_key.txt gemma-4-26b-a4b-it gm3
```

- `gm3` (argv[3]) selects the existing checkpoint
  `arm_gm_gm3_checkpoint.jsonl`; the runner prints
  `resuming: 99 content rows kept, 0 transport-error rows requeued` and
  only issues the 41 missing (n, sample_idx) cells.
- `GM_MAXTOK=16384` is the single registered design change vs GM2 — do not
  omit it, or truncation reproduces GM2's 0/140-parseable outcome.
- `GM_TIMEOUT=900`: generation at this budget ran past the 120 s and 420 s
  defaults during the disclosed 2026-08-03 false starts.
- Single worker + 3.2 s spacing is deliberate (free-tier RPM cap). 41 calls
  at this budget ≈ 1–3 h wall clock. If the daily quota dies again, just
  re-run the same command after reset; content rows are never re-called.

On completion the runner prints `COMPLETE: 140 rows, 0 transport errors`
and assembles `arm_gm_gm3_raw.json` from the checkpoint.

## Analysis (registered definitions)

GM2's analysis expected the raw file under the prereg's name, so mirror
that convention, then run a GM3 copy of the analysis:

```bash
cp arm_gm_gm3_raw.json arm_gm3_raw.json
sed 's/gm2/gm3/g' arm_gm2_analysis.py > arm_gm3_analysis.py
python3 arm_gm3_analysis.py   # writes arm_gm3_candidates.jsonl, arm_gm3_report.json
```

(The sed produces a faithful copy because the analysis differs from GM2
only in filenames; eyeball the diff before running.)

Registered outcomes to report, whichever branch obtains:
- **P-GM3.1** MODE-MATCH ≥ 5 scoreable cells (needs ≥ 5 scoreable)
- **P-GM3.2** pooled on-prediction ≥ 30%
- **P-GM3.3** two-radii signature in ≥ half of on-prediction samples
- **FALSIFIER** MODE-MATCH fails in ≥ 4 scoreable cells
- **< 5 scoreable cells** → per the prereg's added note: Gemma weak-tier
  anchoring is reported "unanswerable under this protocol (two attempts,
  both disclosed)"; **no third budget increase** is permitted.

Whatever the branch, Paper 1's cross-vendor section gets its answer and the
paper is submittable.
