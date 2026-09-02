# Arm B: the optimizer alone. A fixed reference program, written by the pipeline before any
# run and never tuned on a result, that does what a reader would write first: random-restart
# SLSQP over centre and radius variables, maximising the sum of radii under containment and
# pairwise non-overlap, restarting until the wall-clock budget is spent. It is executed
# through arm CL's registered pipeline unmodified (python -I -S, the fixed driver, 120-second
# wall clock, one core, arm-F scoring, section 2.4's clearance rule), so its rows are scored
# exactly like the model-written programs it is the baseline for.
#
# Usage inside the pipeline: arm_b_run.py substitutes N and SEED below and hands the source
# to arm_cl_analysis.score_row as if it were a model completion.
import sys
import time

import numpy as np
from scipy.optimize import minimize

N = __N__
SEED = __SEED__
START_CUTOFF_S = 95.0   # no new restart after this many seconds; the 120 s wall clock is the executor's

rng = np.random.default_rng(SEED)
t0 = time.time()
iu = np.triu_indices(N, 1)


def unpack(v):
    return v[:N], v[N:2 * N], v[2 * N:]


def objective(v):
    return -np.sum(v[2 * N:])


def objective_grad(v):
    g = np.zeros_like(v)
    g[2 * N:] = -1.0
    return g


def constraints(v):
    x, y, r = unpack(v)
    dx = x[iu[0]] - x[iu[1]]
    dy = y[iu[0]] - y[iu[1]]
    rs = r[iu[0]] + r[iu[1]]
    return np.concatenate([x - r, 1 - x - r, y - r, 1 - y - r, dx * dx + dy * dy - rs * rs])


def constraints_jac(v):
    x, y, r = unpack(v)
    m = len(iu[0])
    J = np.zeros((4 * N + m, 3 * N))
    ar = np.arange(N)
    J[ar, ar] = 1.0;            J[ar, 2 * N + ar] = -1.0
    J[N + ar, ar] = -1.0;       J[N + ar, 2 * N + ar] = -1.0
    J[2 * N + ar, N + ar] = 1.0;  J[2 * N + ar, 2 * N + ar] = -1.0
    J[3 * N + ar, N + ar] = -1.0; J[3 * N + ar, 2 * N + ar] = -1.0
    i, j = iu
    rows = 4 * N + np.arange(m)
    dx = x[i] - x[j]
    dy = y[i] - y[j]
    rs = r[i] + r[j]
    J[rows, i] = 2 * dx;        J[rows, j] = -2 * dx
    J[rows, N + i] = 2 * dy;    J[rows, N + j] = -2 * dy
    J[rows, 2 * N + i] = -2 * rs; J[rows, 2 * N + j] = -2 * rs
    return J


bounds = [(0.0, 1.0)] * (2 * N) + [(0.0, 0.5)] * N
cons = [{"type": "ineq", "fun": constraints, "jac": constraints_jac}]


def repaired(v):
    """Shrink every radius by the largest constraint violation so the packing is strictly
    feasible; SLSQP satisfies constraints only to its own tolerance."""
    x, y, r = unpack(v.copy())
    viol = max(0.0, -np.min(constraints(v)))
    r = np.maximum(r - viol - 1e-12, 0.0)
    return x, y, r


best_sum, best = -1.0, None
while time.time() - t0 < START_CUTOFF_S:
    v0 = np.concatenate([rng.uniform(0.1, 0.9, N), rng.uniform(0.1, 0.9, N), rng.uniform(0.02, 0.08, N)])
    res = minimize(objective, v0, jac=objective_grad, method="SLSQP", bounds=bounds,
                   constraints=cons, options={"maxiter": 400, "ftol": 1e-12})
    x, y, r = repaired(res.x)
    if np.min(constraints(np.concatenate([x, y, r]))) < 0 or np.any(r <= 0):
        continue
    s = float(np.sum(r))
    if s > best_sum:
        best_sum, best = s, (x, y, r)

if best is None:
    sys.exit("no feasible packing found")
x, y, r = best
print("[" + ", ".join(f"[{a:.10f}, {b:.10f}, {c:.10f}]" for a, b, c in zip(x, y, r)) + "]")
