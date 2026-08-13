"""Runs the dispersion probe's registered decision rule (analysis_prereg.md + Amendment 1).

Requires: numpy, rapidfuzz, scipy  ->  pip install -r requirements.txt

NOTE ON THE SPREAD STATISTIC. The preregistration names its quantity by the
generating kernel's field, `mean_pairwise_ned`. That kernel is not in this corpus,
and the one surviving logged value (provenance.json,
text_dispersion_mean_pairwise_ned = -0.3558 for q3_k_m) is negative, so it is not a
normalized edit distance in the usual sense and its definition is unrecoverable.
The definition below -- Levenshtein over raw_text divided by the longer length,
averaged over unordered within-cell pairs -- is a substitution of ours, not a replay
of the registered one. Section 3 discloses this.
"""
import json, itertools, math, os, sys
import numpy as np
from rapidfuzz.distance import Levenshtein
from scipy.stats import spearmanr
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    HERE, "sec3_artifacts", "dispersion_probe", "probe_samples.jsonl")
if not os.path.exists(PATH):
    PATH = os.path.join(HERE, "..", "agent-run", "dispersion_probe", "probe_samples.jsonl")
rows = [json.loads(l) for l in open(PATH, encoding='utf-8')]
RUNGS = ['q4_k_m', 'q3_k_m', 'q2_k']          # decreasing precision; q8_0 absent
rng = np.random.default_rng(20260806)

valid = [r for r in rows if r['valid']]
print("total rows", len(rows), "| valid", len(valid),
      "| rungs present", sorted(set(r['rung'] for r in rows)))
for R in RUNGS:
    print(f"  {R}: n={sum(1 for r in rows if r['rung']==R)} valid={sum(1 for r in valid if r['rung']==R)}")

# ---------- sanity: circle counts + parent recovery from echo rows ----------
bad = [r for r in valid if not r['circles'] or len(r['circles']) != 26]
print("valid rows without exactly 26 circles:", len(bad))

parents = {}
for pid in sorted(set(r['parent_id'] for r in rows)):
    ech = [r for r in rows if r['parent_id'] == pid and r.get('echo') and r['circles']]
    arrs = np.array([[c[:2] for c in r['circles']] for r in ech])
    disc = float(np.abs(arrs - arrs[0]).max())
    parents[pid] = arrs[0]                      # centres only
    print(f"  parent {pid}: {len(ech)} echo rows, max index-wise centre discrepancy {disc:.2e}")

# ---------- 1. PRIMARY SPREAD TEST: mean pairwise NED per (rung,parent) ----------
def ned(a, b):
    return Levenshtein.distance(a, b) / max(len(a), len(b))

cell_ned, dropped = {}, {R: 0 for R in RUNGS}
for R in RUNGS:
    for pid in parents:
        txts = [r['raw_text'] for r in valid if r['rung'] == R and r['parent_id'] == pid]
        if len(txts) < 2:
            dropped[R] += 1
            continue
        cell_ned[(R, pid)] = float(np.mean([ned(a, b) for a, b in itertools.combinations(txts, 2)]))

groups_ned = [[cell_ned[(R, p)] for p in parents if (R, p) in cell_ned] for R in RUNGS]
print("\n=== 1. PRIMARY SPREAD (mean pairwise NED, valid only) ===")
for R, g in zip(RUNGS, groups_ned):
    print(f"  {R}: cells={len(g)} dropped={dropped[R]} mean={np.mean(g):.4f} sd={np.std(g,ddof=1):.4f} "
          f"vals={[round(v,4) for v in sorted(g)]}")

def jt(groups):
    """Jonckheere-Terpstra, increasing alternative; ties get 0.5. Small JT = decline."""
    s = 0.0
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            for x in groups[i]:
                for y in groups[j]:
                    s += 1.0 if y > x else (0.5 if y == x else 0.0)
    return s

def perm_p_jt(groups, nperm=10000):
    obs = jt(groups)
    pool = np.array([v for g in groups for v in g]); sizes = [len(g) for g in groups]
    cnt = 0
    for _ in range(nperm):
        pm = rng.permutation(pool); k = 0; gs = []
        for s in sizes:
            gs.append(pm[k:k+s]); k += s
        if jt(gs) <= obs: cnt += 1
    return obs, (cnt + 1) / (nperm + 1)

jt_ned, p_ned = perm_p_jt(groups_ned)
print(f"  JT statistic = {jt_ned:.1f}  (max possible {sum(len(groups_ned[i])*len(groups_ned[j]) for i in range(3) for j in range(i+1,3))})")
print(f"  permutation p (decline, 10,000 shuffles) = {p_ned:.4f}")

# ---------- 2. RAREFACTION on orthogonal descriptor ----------
def d1_of(cs):
    P = np.array([c[:2] for c in cs])
    D = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=-1)
    iu = np.triu_indices(len(P), 1)
    return float(D[iu].mean())

def d2_of(cs, pid):
    P = np.array([c[:2] for c in cs])
    return float(np.linalg.norm(P - parents[pid], axis=1).mean())

d1 = np.array([d1_of(r['circles']) for r in valid])
d2 = np.array([d2_of(r['circles'], r['parent_id']) for r in valid])
sc = np.array([r['score'] for r in valid])
rung_lab = np.array([r['rung'] for r in valid])

qs = np.linspace(0, 1, 9)
e1, e2 = np.quantile(d1, qs), np.quantile(d2, qs)
b1, b2 = np.clip(np.digitize(d1, e1[1:-1]), 0, 7), np.clip(np.digitize(d2, e2[1:-1]), 0, 7)
cells = b1 * 8 + b2
print("\n=== 2. RAREFACTION (d1 x d2, 8x8 pooled quantile bins) ===")
print("  d1 edges:", np.round(e1, 5).tolist())
print("  d2 edges:", np.round(e2, 6).tolist())
print(f"  distinct d1 bins occupied={len(set(b1.tolist()))}  d2 bins occupied={len(set(b2.tolist()))}  "
      f"(d2 edge collapse: {9-len(set(np.round(e2,12).tolist()))} duplicate edges; "
      f"{int((d2<1e-9).sum())}/{len(d2)} rows have d2~0)")

m = min((rung_lab == R).sum() for R in RUNGS)
print(f"  m (min valid count across rungs) = {m}")

def emp_rarefy(idx, m, B=1000):
    c = cells[idx]
    return np.array([len(np.unique(rng.choice(c, m, replace=False))) for _ in range(B)])

def exp_unique(c, m):
    """analytic E[# unique cells in a size-m subsample without replacement]"""
    n = len(c); _, k = np.unique(c, return_counts=True)
    return float(sum(1 - (comb(n - nc, m) / comb(n, m) if n - nc >= m else 0.0) for nc in k))

obs_means = {}
for R in RUNGS:
    idx = np.where(rung_lab == R)[0]
    v = emp_rarefy(idx, m)
    obs_means[R] = v.mean()
    print(f"  {R}: n_valid={len(idx)} unique cells (rarefied to m={m}) mean={v.mean():.3f} sd={v.std(ddof=1):.3f} "
          f"| raw occupied={len(set(cells[idx].tolist()))} | analytic E={exp_unique(cells[idx], m):.3f}")

# permutation trend test on analytic E[unique] with contrast (+1, 0, -1)
def contrast(labels):
    return exp_unique(cells[labels == RUNGS[0]], m) - exp_unique(cells[labels == RUNGS[2]], m)
T_obs = contrast(rung_lab)
cnt = 0
for _ in range(10000):
    if contrast(rng.permutation(rung_lab)) >= T_obs: cnt += 1
p_rare = (cnt + 1) / 10001
print(f"  trend contrast T = E[q4_k_m] - E[q2_k] = {T_obs:+.3f}; permutation p (decline) = {p_rare:.4f}")

# orthogonality
for name, arr in (('d1', d1), ('d2', d2)):
    rho, p = spearmanr(arr, sc)
    print(f"  ORTHOGONALITY {name} vs score: rho={rho:+.4f} p={p:.3g} -> {'CONFOUNDED' if abs(rho)>0.5 else 'ok'}")

# ---------- 3. POWER FLOOR ----------
print("\n=== 3. POWER FLOOR ===")
print(f"  m = {m} ({'OK' if m>=8 else 'BELOW 8'});  parents with defined NED per rung: "
      + ", ".join(f"{R}={len(g)}" for R, g in zip(RUNGS, groups_ned)))
underpowered = m < 8 or any(len(g) < 3 for g in groups_ned)
print(f"  UNDERPOWERED = {underpowered}")

# ---------- 4. QUALITY / DECISION ----------
print("\n=== 4. QUALITY (score among valid) ===")
score_groups = [sc[rung_lab == R].tolist() for R in RUNGS]
for R, g in zip(RUNGS, score_groups):
    print(f"  {R}: n={len(g)} mean score={np.mean(g):.5f} sd={np.std(g,ddof=1):.5f}")
jt_sc, p_sc = perm_p_jt(score_groups)
print(f"  score JT = {jt_sc:.1f}; permutation p (decline) = {p_sc:.4f}")

print("\n=== VERDICT INPUTS ===")
print(f"  NED decline p={p_ned:.4f} ({'sig' if p_ned<0.05 else 'ns'}) | rarefaction p={p_rare:.4f} "
      f"({'sig' if p_rare<0.05 else 'ns'}) | score JT p={p_sc:.4f} ({'no decline' if p_sc>0.10 else 'declines'})")
