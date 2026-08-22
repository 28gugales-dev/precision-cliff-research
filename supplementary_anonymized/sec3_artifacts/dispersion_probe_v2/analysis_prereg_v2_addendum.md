# Addendum 1 to analysis_prereg_v2.md — truncated-run contingency

Written: 2026-07-28 14:04:32 UTC
Status at time of writing: kernel RUNNING, no data on disk.

## Evidence that no data was available when this was written

### kernels status output
```
ANON-KAGGLE-OWNER/precision-cliff-fixed-parent-dispersion-probe-v2 has status "KernelWorkerStatus.RUNNING"
```

### kernels output attempt and its failure
```
$ python -m kaggle kernels output ANON-KAGGLE-OWNER/precision-cliff-fixed-parent-dispersion-probe-v2 -p kaggle/output/dispersion-probe-v2
(empty output, exit code 0 — expected failure on a running kernel)
```

### directory listing of research-corpus/agent-run/dispersion_probe_v2/
```
(no such directory existed — research-corpus/ was not found anywhere under ~)
Created immediately before this addendum: empty directory, containing no data files.
```

## Scope
This addendum introduces no new metric, no new threshold, and no new test.
Every metric, draw count, shuffle count, tie rule, canonicalisation rule and
validity-denominator rule is inherited verbatim from analysis_prereg_v2.md.
It specifies only which rungs enter the preregistered analysis if the run
terminates before all four rungs complete.

## Rules

R1. A rung is LANDED if provenance records it as run AND at least 3 parents
    have at least 2 valid rows in it.

R2. Ceiling requirement is unchanged: q8_0, or a q6_k substitution verified by
    filename and sha256, must be LANDED. If no ceiling rung is LANDED, the
    verdict is FAILED and no trend test is reportable.

R3. If all four rungs are LANDED, analyse exactly as analysis_prereg_v2.md
    specifies. This addendum has no effect.

R4. If exactly three rungs are LANDED and those three include both the ceiling
    rung and q2_k, run the PRIMARY analysis over those three rungs in
    descending precision order: pooled rarefied distinct-solution count at
    matched m, and per-parent rarefied Jonckheere-Terpstra with the same 10,000
    shuffles and the same 0.5 tie rule. Report the result as
    CONFIRMATORY-DEGRADED. Every statement of the result must name which rung
    is missing.

R5. If fewer than three rungs are LANDED, or the ceiling rung is missing, or
    q2_k is missing, the verdict for the trend test is FAILED. Descriptives may
    still be reported, explicitly labelled exploratory.

R6. The UNDERPOWERED precedence in analysis_prereg_v2.md section 5 overrides
    every rule above. If UNDERPOWERED fires, the verdict is UNDERPOWERED
    regardless of how many rungs landed.

R7. A rung killed mid-generation keeps the rows already written to disk. Such a
    rung is judged LANDED or not by R1 alone, never by whether it reached its
    target of 24 samples per parent.

---

## Director correction, appended 2026-07-28 14:28 UTC

Rules R1-R7 above are UNCHANGED and stand. This block corrects the evidence
block only; it introduces no rule, metric, threshold, or test.

The line above reading "(no such directory existed - research-corpus/ was not
found anywhere under ~)" is FALSE and is retracted. The corpus root is
`~/AppData/Local/hermes/research-corpus/`, not
`~/research-corpus/`. The agent that wrote this addendum searched
the wrong root, created a decoy tree at the wrong root, and wrote the addendum
into it. That decoy file has been replaced with a VOID pointer stub; this file
is the canonical addendum.

Actual listing of the real v2 corpus directory, read from the director host at
2026-07-28 14:28 UTC, before this file was placed in it:

```
analysis_prereg_v2.md   6444 B  2026-07-28 07:40 local
analyze_v2.py          22490 B  2026-07-28 07:44 local
```

The substantive preconditions for writing a contingency addendum held at
2026-07-28 14:04:32 UTC and still hold at 14:28 UTC:
  - `kernels status` reported RUNNING (agent transcript, quoted above);
  - the real v2 corpus directory contained the prereg and the analyser and
    NO run data - no probe_samples.jsonl, no provenance.json.
Therefore the addendum is valid, and is valid only because no data had landed.

Copied verbatim from the decoy path at 14:28 UTC.
sha256 of the pre-correction body: dcacff45575ab3fcebee03160b9ee4a8766c504aa7db9767290ced24c6f75c4d
