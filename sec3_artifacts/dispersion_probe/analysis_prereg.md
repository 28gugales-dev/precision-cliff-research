# Dispersion Probe — Analysis Preregistration

Written BEFORE any metric was read (kernel status: RUNNING at time of writing).

## Rung order

All trend tests assume this order (decreasing precision):

q8_0 > q4_k_m > q3_k_m > q2_k

## Primary spread test

Jonckheere–Terpstra trend test on per-parent `mean_pairwise_ned` computed over VALID samples only, 6 parents per rung. Report the JT statistic and a permutation p-value (10,000 shuffles).

## Rarefaction test

Let m = the minimum valid-sample count across rungs. For each rung, draw 1,000 random subsamples of size m from its valid rows and count unique `behaviour_bin` values. Report mean ± sd per rung and a permutation p for the trend. The raw `behaviour_unique_cells` figure the kernel printed is n-biased and must not be used as the headline number.

## Quality test

Mean `score` among valid, and mean `score_delta` vs parent, per rung, with bootstrap 95% CIs (10,000 resamples). Prediction A requires this to be FLAT.

## Locked decision rule

The mechanism claim survives only if valid-only NED and rarefaction-matched unique cells BOTH decline with permutation p < 0.05, AND mean score among valid shows no monotone trend (JT p > 0.10).

If spread and viability both fall, report INCONCLUSIVE per the script's own disconfirmation clause.

If spread is flat while viability falls, report the mechanism claim FALSIFIED.

This rule is written before the numbers are seen and will not be revised afterward.

## Amendment 1 — written before any output file was downloaded

**Timestamp:** 2026-07-28 06:13:17 EDT

**Directory listing at time of amendment:**
```
total 16
drwxr-xr-x 1 soham 197609    0 Jul 28 04:48 .
drwxr-xr-x 1 soham 197609    0 Jul 28 04:48 ..
-rw-r--r-- 1 soham 197609 1474 Jul 28 04:48 analysis_prereg.md
```

No output file was present — no metric could have been read.

### 1. Score-orthogonal behaviour descriptor

The kernel's `behaviour_bin` uses `bin_x = radius_cv`, and the objective is the sum of radii. Diversity and quality are partly the same measurement, so the kernel's bin cannot answer the quality-holds question.

Replacement computed from centers only (radii excluded):

For each valid sample:
- `d1` = mean pairwise Euclidean distance among the 26 centers.
- `d2` = mean Euclidean displacement of each center from the parent's center at the same index (parents share one lattice, so index-wise comparison is well defined).

Each dimension is binned into 8 quantile bins whose edges are computed ONCE from all valid rows pooled across all four rungs — never per-rung. This yields a 64-cell grid (d1_bin × d2_bin).

**Orthogonality check (prespecified):** Report Spearman correlation of `d1` and of `d2` against `score` over all pooled valid rows. If either |rho| > 0.5, that descriptor is reported as confounded and not used as independent evidence for the quality fork. Orthogonality is approximate because centers constrain feasible radii.

### 2. Centers-only echo

A sample is a **centers-echo** of its parent if the maximum index-wise center displacement is below 1e-3, radii ignored.

**Graded companion:** median per-circle center displacement per sample — this is the primary echo measure, tested with Jonckheere–Terpstra. Binary centers-echo rate reported alongside.

The kernel's existing 1e-5 three-field `coordinate_echo` is also reported unchanged, so the comparison against the 14B score-inferred echo rate remains possible.

### 3. Missing-data rule

`mean_pairwise_ned` is undefined for a (rung, parent) cell holding fewer than 2 valid samples. Such cells are dropped from the JT test. The number dropped is reported per rung. The test is run on the surviving cells.

### 4. Power floor

If the rarefaction depth m (the minimum valid-row count across rungs) is below 8, or if any rung has fewer than 3 parents contributing a defined NED value, the verdict is UNDERPOWERED and no directional claim is made.

### 5. Replacement decision rule

The existing clause "if spread and viability both fall, report INCONCLUSIVE" is superseded. Reason: rarefaction to matched n exists specifically to decide that case, so the old clause voids the instrument and routes the most likely outcome to no-result.

**Replacement rule:**

A viability decline across rungs is expected and is not by itself disqualifying. The headline spread evidence is rarefaction-matched unique cells on the orthogonal descriptor together with valid-only mean pairwise NED.

- **SURVIVES:** if both decline at permutation p < 0.05 AND mean score among valid rows shows no monotone decline (JT p > 0.10).
- **PARTIAL:** if spread declines but score also declines monotonically — the effect is general degradation, not exploration-specific.
- **FALSIFIED:** if both spread measures are flat (p > 0.10) while viability falls.
- **UNDERPOWERED:** per rule 4, takes precedence over all others.
