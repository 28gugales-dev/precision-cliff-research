# POST-HOC DIAGNOSTIC - not preregistered, prompted by external review deduction 5

Generated 2026-08-04 by `diagnostics_opus_overlap.py`. Analysis only; no paper text or arm data was modified.

Source: `arm_f_candidates_v2.jsonl`. Validity predicates replicate `arm_f_repro.validate()` (primary tol 1e-6). `max_overlap` = max over pairs of (r_i+r_j-dist_ij); `max_wall` = max over circles of how far the disc exits the unit square; `max_violation` = max of the two, floored at 0. `eps_repair` = minimal eps (bisection, 200 iters) such that scaling all radii by (1-eps) with centres fixed passes 1e-6.

## opus_alias arm - every invalid sample (N=13/21/31)

| N | s | n_circles | count_ok | max_overlap | max_wall | max_violation | band | eps_repair | sum_r | sum_r_repaired |
|---|---|---|---|---|---|---|---|---|---|---|
| 13 | 1 | 13 | True | 1.703708e-02 | 0.000000e+00 | 1.703708e-02 | gross | 5.270684e-02 | 1.421572800 | 1.346646187 |
| 13 | 5 | 13 | True | 2.767567e-02 | 0.000000e+00 | 2.767567e-02 | gross | 8.386264e-02 | 1.540000000 | 1.410851536 |
| 13 | 6 | 13 | True | 6.381798e-02 | 0.000000e+00 | 6.381798e-02 | gross | 1.805017e-01 | 1.639087297 | 1.343229300 |
| 13 | 7 | 13 | True | 1.703709e-02 | 0.000000e+00 | 1.703709e-02 | gross | 5.270686e-02 | 1.510828526 | 1.431197492 |
| 13 | 8 | 13 | True | 1.035534e-01 | 0.000000e+00 | 1.035534e-01 | gross | 3.083877e-01 | 1.824422511 | 1.261793140 |
| 13 | 9 | 13 | True | 3.667760e-02 | 0.000000e+00 | 3.667760e-02 | gross | 1.092260e-01 | 1.529437313 | 1.362383016 |
| 13 | 10 | 13 | True | 3.667760e-02 | 0.000000e+00 | 3.667760e-02 | gross | 1.092260e-01 | 1.546681194 | 1.377743417 |
| 21 | 1 | 21 | True | 3.998632e-02 | 0.000000e+00 | 3.998632e-02 | gross | 2.326080e-01 | 1.991200000 | 1.528030940 |
| 21 | 3 | 21 | True | 4.665783e-02 | 0.000000e+00 | 4.665783e-02 | gross | 2.331676e-01 | 1.713500000 | 1.313967388 |
| 21 | 4 | 21 | True | 1.018327e-01 | 0.000000e+00 | 1.018327e-01 | gross | not radius-repairable | 1.666900000 | - |
| 21 | 5 | 21 | True | 1.685000e-01 | 0.000000e+00 | 1.685000e-01 | gross | not radius-repairable | 1.516500000 | - |
| 21 | 6 | 21 | True | 1.000000e-04 | 0.000000e+00 | 1.000000e-04 | intermediate | 2.937685e-04 | 1.732500000 | 1.731991046 |
| 21 | 7 | 21 | True | 3.260000e-02 | 0.000000e+00 | 3.260000e-02 | gross | 2.008564e-01 | 2.185400000 | 1.746448339 |
| 21 | 8 | 21 | True | 3.087288e-02 | 0.000000e+00 | 3.087288e-02 | gross | 2.129095e-01 | 2.121700000 | 1.669969908 |
| 21 | 9 | 21 | True | 1.027103e-02 | 0.000000e+00 | 1.027103e-02 | gross | 7.207040e-02 | 2.046800000 | 1.899286306 |
| 21 | 10 | 21 | True | 6.665581e-02 | 0.000000e+00 | 6.665581e-02 | gross | 3.692787e-01 | 2.308000000 | 1.455704724 |
| 31 | 1 | 31 | True | 2.080000e-02 | 0.000000e+00 | 2.080000e-02 | gross | 1.350584e-01 | 1.808800000 | 1.564506291 |
| 31 | 2 | 31 | True | 5.999905e-02 | 0.000000e+00 | 5.999905e-02 | gross | 3.133057e-01 | 2.141500000 | 1.470555755 |
| 31 | 3 | 31 | True | 6.000000e-02 | 0.000000e+00 | 6.000000e-02 | gross | 3.050797e-01 | 2.160000000 | 1.501027932 |
| 31 | 4 | 31 | True | 3.145258e-02 | 0.000000e+00 | 3.145258e-02 | gross | 1.509917e-01 | 2.372700000 | 2.014441893 |
| 31 | 5 | 31 | True | 6.066017e-03 | 0.000000e+00 | 6.066017e-03 | intermediate | 3.511216e-02 | 1.970451202 | 1.901264408 |
| 31 | 6 | 31 | True | 3.322275e-02 | 0.000000e+00 | 3.322275e-02 | gross | 4.921740e-01 | 2.261300000 | 1.148346831 |
| 31 | 7 | 31 | True | 1.800000e-02 | 0.000000e+00 | 1.800000e-02 | gross | 9.750271e-02 | 2.159700000 | 1.949123400 |
| 31 | 8 | 31 | True | 1.793921e-02 | 0.000000e+00 | 1.793921e-02 | gross | 9.793383e-02 | 1.840000000 | 1.659801745 |
| 31 | 9 | 31 | True | 1.424097e-02 | 0.000000e+00 | 1.424097e-02 | gross | 7.853429e-02 | 2.136900000 | 1.969080071 |
| 31 | 10 | 31 | True | 7.980000e-02 | 0.000000e+00 | 7.980000e-02 | gross | 4.249148e-01 | 2.416300000 | 1.389578362 |

### opus_alias summary

- invalid samples: 26 (geometry-scored 26, parse failures 0)
- wrong circle count: 0 (none)
- tolerance-scale (max violation <1e-4): 0
- intermediate (max violation 1e-4..1e-2): 2
- gross (max violation >1e-2): 24
- max violation: min 1.000000e-04, median 3.322275e-02, max 1.685000e-01
- radius-shrink repairable at all: 24/26
- repairable at eps <= 1e-3: 1/26
- repairable at eps <= 1e-2: 1/26
- eps: min 2.937685e-04, median 1.509917e-01, max 4.921740e-01

## weak tier (haiku bare) - invalid samples, matched cells N=13/21/31

| N | s | n_circles | count_ok | max_overlap | max_wall | max_violation | band | eps_repair | sum_r | sum_r_repaired |
|---|---|---|---|---|---|---|---|---|---|---|
| 13 | 2 | 13 | True | 1.000000e-06 | 0.000000e+00 | 1.000000e-06 | tolerance-scale | 5.551115e-17 | 1.614383000 | 1.614383000 |
| 13 | 20 | 13 | True | 7.322330e-02 | 5.800000e-02 | 7.322330e-02 | gross | 4.639920e-01 | 1.625000000 | 0.871013000 |
| 21 | 4 | 21 | True | 4.400048e-06 | 0.000000e+00 | 4.400048e-06 | tolerance-scale | 1.700024e-05 | 2.100000000 | 2.099964299 |
| 21 | 7 | 21 | True | 2.330470e-05 | 0.000000e+00 | 2.330470e-05 | tolerance-scale | 1.261578e-04 | 2.259000000 | 2.258715009 |
| 21 | 10 | 21 | True | 2.461439e-05 | 0.000000e+00 | 2.461439e-05 | tolerance-scale | 1.634893e-04 | 2.044440000 | 2.044105756 |
| 21 | 12 | - | - | - | - | - | PARSE FAIL (literal_eval_failed:ValueError) | - | - | - |
| 21 | 14 | 21 | True | 1.000000e-01 | 2.500000e-02 | 1.000000e-01 | gross | 3.999960e-01 | 2.500000000 | 1.500010000 |
| 31 | 9 | - | - | - | - | - | PARSE FAIL (literal_eval_failed:ValueError) | - | - | - |
| 31 | 12 | 31 | True | 1.723342e-06 | 0.000000e+00 | 1.723342e-06 | tolerance-scale | 4.340068e-06 | 2.583323000 | 2.583311788 |
| 31 | 19 | - | - | - | - | - | PARSE FAIL (literal_eval_failed:ValueError) | - | - | - |

### weak tier (haiku bare) summary

- invalid samples: 10 (geometry-scored 7, parse failures 3)
- wrong circle count: 0 (none)
- tolerance-scale (max violation <1e-4): 5
- intermediate (max violation 1e-4..1e-2): 0
- gross (max violation >1e-2): 2
- max violation: min 1.000000e-06, median 2.330470e-05, max 1.000000e-01
- radius-shrink repairable at all: 7/7
- repairable at eps <= 1e-3: 5/7
- repairable at eps <= 1e-2: 5/7
- eps: min 5.551115e-17, median 1.261578e-04, max 4.639920e-01

## Structure of the opus invalid samples

Bears directly on the reviewer's 'ambitious gasket' hypothesis: a tangency-driven near-miss should show many distinct radii and a violation at rounding scale. Column `not radius-repairable` means even eps=0.5 (halving every radius) still fails 1e-6, i.e. two centres are close enough that no uniform shrink separates them.

| N | s | distinct_radii | min_radius | max_violation | eps_repair |
|---|---|---|---|---|---|
| 13 | 1 | 4 | 0.021446600 | 1.703708e-02 | 5.270684e-02 |
| 13 | 5 | 4 | 0.030000000 | 2.767567e-02 | 8.386264e-02 |
| 13 | 6 | 3 | 0.030330086 | 6.381798e-02 | 1.805017e-01 |
| 13 | 7 | 4 | 0.028595479 | 1.703709e-02 | 5.270686e-02 |
| 13 | 8 | 4 | 0.068542495 | 1.035534e-01 | 3.083877e-01 |
| 13 | 9 | 3 | 0.025126281 | 3.667760e-02 | 1.092260e-01 |
| 13 | 10 | 3 | 0.029437252 | 3.667760e-02 | 1.092260e-01 |
| 21 | 1 | 3 | 0.020000000 | 3.998632e-02 | 2.326080e-01 |
| 21 | 3 | 3 | 0.017700000 | 4.665783e-02 | 2.331676e-01 |
| 21 | 4 | 4 | 0.000000000 | 1.018327e-01 | n/a (>0.5) |
| 21 | 5 | 2 | 0.000000000 | 1.685000e-01 | n/a (>0.5) |
| 21 | 6 | 3 | 0.022500000 | 1.000000e-04 | 2.937685e-04 |
| 21 | 7 | 4 | 0.021500000 | 3.260000e-02 | 2.008564e-01 |
| 21 | 8 | 6 | 0.016600000 | 3.087288e-02 | 2.129095e-01 |
| 21 | 9 | 2 | 0.021200000 | 1.027103e-02 | 7.207040e-02 |
| 21 | 10 | 3 | 0.020000000 | 6.665581e-02 | 3.692787e-01 |
| 31 | 1 | 7 | 0.010400000 | 2.080000e-02 | 1.350584e-01 |
| 31 | 2 | 3 | 0.030000000 | 5.999905e-02 | 3.133057e-01 |
| 31 | 3 | 2 | 0.030000000 | 6.000000e-02 | 3.050797e-01 |
| 31 | 4 | 3 | 0.020200000 | 3.145258e-02 | 1.509917e-01 |
| 31 | 5 | 4 | 0.006066017 | 6.066017e-03 | 3.511216e-02 |
| 31 | 6 | 3 | 0.032600000 | 3.322275e-02 | 4.921740e-01 |
| 31 | 7 | 3 | 0.017900000 | 1.800000e-02 | 9.750271e-02 |
| 31 | 8 | 4 | 0.008000000 | 1.793921e-02 | 9.793383e-02 |
| 31 | 9 | 3 | 0.014100000 | 1.424097e-02 | 7.853429e-02 |
| 31 | 10 | 3 | 0.039900000 | 7.980000e-02 | 4.249148e-01 |

## Verdict inputs

- opus tolerance-scale fraction: 0/26
- weak-tier tolerance-scale fraction: 5/7
