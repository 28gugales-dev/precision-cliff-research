# Arm B, amendment 1: fixed restart count (the registered contract forbids `time` and `sys`)

Registered 2026-09-02, after the first scored run and before the second.

The first run of arm_b_baseline.py (version 1, sha256 af73c017...) was binned blocked_import
at all 45 rows by arm CL's registered AST gate: the allowlist is math, numpy and scipy, and
version 1 imported `time` (to bound restarts by wall clock) and `sys` (for the exit path). The
model-written programs the baseline is compared to never imported either; every Sonnet
program used a fixed restart count. The run is kept verbatim as
arm_b_v1_blocked_collect.jsonl / arm_b_v1_blocked_report.json / arm_b_v1_blocked_run.log and
counts as a registration defect of the baseline's author, not of the pipeline.

Change, fixed here: version 2 replaces the wall-clock cutoff with RESTARTS = 50 fixed restarts
at every cell and prints an empty list when no restart is feasible. The count comes from one
unscored timing run at N = 31, seed 999, under the version-1 program outside the gate: 80
feasible restarts in 95 s on one core, so 50 leaves a margin inside the 120 s wall clock at the
largest cell. Nothing else changes: same optimizer, same initialisation, same repair, same
seeds, same cells, same predictions P-B1 / P-B2 and secondary S-B1, same scoring pipeline.
The runner asserts the version-2 hash.
