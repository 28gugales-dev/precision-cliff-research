"""Runs the two registered v1 dispersion-probe analyses that earlier drafts left unreported.

Section 2 of analysis_prereg.md's Amendment 1 designates median per-circle centre
displacement "the primary echo measure, tested with Jonckheere-Terpstra". Earlier
drafts printed the medians as a descriptive and never ran that test. The quality
test's second registered half -- mean score_delta vs parent with bootstrap CIs --
was likewise unreported. Both are computed here, along with the prespecified
orthogonality diagnostic's p-values.

The result is unfavourable and degenerate, and section 3 reports it as such.

Requires: numpy, scipy  ->  pip install -r requirements.txt
Run:  python sec3_registered_echo_test.py
"""
import json, math, os, sys, statistics, itertools
import numpy as np
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    HERE, "sec3_artifacts", "dispersion_probe", "probe_samples.jsonl")
if not os.path.exists(PATH):
    PATH = os.path.join(HERE, "..", "agent-run", "dispersion_probe", "probe_samples.jsonl")

RUNGS = ["q4_k_m", "q3_k_m", "q2_k"]      # decreasing precision; q8_0 never ran
SHUFFLES = 10_000
rng = np.random.default_rng(20260807)

rows = [json.loads(l) for l in open(PATH, encoding="utf-8")]

# The probe holds each parent fixed, so any echo row recovers that parent's circles.
parents = {}
for r in rows:
    if r.get("echo") and r["parent_id"] not in parents:
        parents[r["parent_id"]] = r["circles"]

valid = [r for r in rows if r["valid"]]


def median_displacement(r):
    """Median per-circle centre displacement from the parent, index-wise."""
    p, c = parents[r["parent_id"]], r["circles"]
    n = min(len(p), len(c))
    if n == 0:
        return None
    return statistics.median(math.dist(p[i][:2], c[i][:2]) for i in range(n))


def jonckheere(groups):
    """JT statistic over ordered groups, 0.5 credit for ties (prereg tie rule)."""
    total = 0.0
    for a, b in itertools.combinations(range(len(groups)), 2):
        for x in groups[a]:
            for y in groups[b]:
                total += 1.0 if x > y else (0.5 if x == y else 0.0)
    return total


print("=" * 66)
print("REGISTERED PRIMARY ECHO MEASURE (Amendment 1 section 2)")
print("=" * 66)

per_rung = {g: [] for g in RUNGS}
for r in valid:
    d = median_displacement(r)
    if d is not None:
        per_rung[r["rung"]].append(d)

for g in RUNGS:
    v = per_rung[g]
    zeros = sum(1 for x in v if x == 0.0)
    print(f"  {g:9s} n={len(v):3d}  median={statistics.median(v):.6f}  "
          f"mean={sum(v)/len(v):.6f}  exact-zero={zeros}/{len(v)}")

groups = [per_rung[g] for g in RUNGS]
observed = jonckheere(groups)
pooled = [x for g in RUNGS for x in per_rung[g]]
sizes = [len(per_rung[g]) for g in RUNGS]

null = np.empty(SHUFFLES)
for i in range(SHUFFLES):
    shuffled = list(pooled)
    rng.shuffle(shuffled)
    cut, parts = 0, []
    for s in sizes:
        parts.append(shuffled[cut:cut + s])
        cut += s
    null[i] = jonckheere(parts)

p = (np.sum(null >= observed) + 1) / (SHUFFLES + 1)
print(f"\n  JT = {observed:.1f}  null mean {null.mean():.2f} (sd {null.std():.2f})"
      f"  permutation p = {p:.4f}")

total_zero = sum(1 for x in pooled if x == 0.0)
print(f"  DEGENERACY: {total_zero}/{len(pooled)} valid rows have displacement exactly 0,")
print("  so the test is very nearly all ties and the p-value is saturation, not flatness.")

print()
print("=" * 66)
print("REGISTERED QUALITY TEST, SECOND HALF: mean score_delta vs parent")
print("=" * 66)
for g in RUNGS:
    v = np.array([r["score_delta"] for r in valid
                  if r["rung"] == g and r.get("score_delta") is not None])
    boot = np.array([rng.choice(v, len(v), replace=True).mean() for _ in range(SHUFFLES)])
    lo, hi = np.percentile(boot, [2.5, 97.5])
    print(f"  {g:9s} n={len(v):3d}  mean={v.mean():+.6f}  95% CI [{lo:+.6f}, {hi:+.6f}]")

print()
print("=" * 66)
print("PRESPECIFIED ORTHOGONALITY DIAGNOSTIC (with p-values)")
print("=" * 66)
d1, d2, scores = [], [], []
for r in valid:
    pts = [(x, y) for x, y, _ in r["circles"]]
    if len(pts) < 2:
        continue
    pairs = list(itertools.combinations(pts, 2))
    d1.append(sum(math.dist(a, b) for a, b in pairs) / len(pairs))
    d2.append(median_displacement(r))
    scores.append(r["score"])

for name, series in (("spread descriptor  ", d1), ("displacement descr.", d2)):
    rho, pv = spearmanr(series, scores)
    verdict = "confounded" if abs(rho) > 0.5 else "passes registered |rho| <= 0.5"
    print(f"  {name} rho={rho:+.4f}  p={pv:.4f}  n={len(series)}  -> {verdict}")
print("  Passing the registered threshold is not independence: both are nominally non-zero.")
