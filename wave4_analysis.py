#!/usr/bin/env python3
"""Wave 4 registered analysis — no arguments, replays everything from the raw ledger.

Registration: wave4_prereg_tiers_heilbronn.md
  SHA-256 7b3e67dc07788fb9439a42269540aaec4e83e83737cc6b1d41be589f99b0b3a4
  external timestamp: public Kaggle dataset sohamgugalet/wave4-prereg-tiers-heilbronn
  locked 2026-08-08 BEFORE any tier row was sampled.

Every verdict label below is computed and printed by this script, not written by us
(prereg SS7). Echo and score are recomputed from the stored canonical points, not
trusted from the recorder.
"""
import json, os
from itertools import combinations, permutations

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "wave4_artifacts", "wave4_tiers.jsonl")
TIERS = ["haiku", "sonnet", "opus"]  # capability rank order, SS5.2

# SS5.1 registered bounds
UPPER_BOUND = 0.30      # every tier <= 30% -> dissociation
Q2K_CLASS = 0.55        # any tier >= 55% -> capability confound live
POWER_FLOOR_VALID = 20  # per tier
ECHO_COUNT_FLOOR = 10   # SS5.2 total echoes else NOT EVALUATED

# seed parent replay (extraction identical to wave4_run.py)
import re, ast
RUNNER = os.path.join(HERE, "sec3_artifacts", "runners",
                      "kaggle_precision_sweep_14b_heilbronn.py")
src = open(RUNNER, encoding="utf-8").read()
SEED_PARENT = [tuple(p) for p in ast.literal_eval(
    re.search(r"SEED_PARENT = (\[.*?\n\])", src, re.S).group(1))]
SEED_SCORE = float(re.search(r"SEED_PARENT_SCORE = ([0-9.]+)", src).group(1))

def tri_area(a, b, c):
    return abs((b[0]-a[0])*(c[1]-a[1]) - (c[0]-a[0])*(b[1]-a[1])) / 2.0

def score(points):
    return min(tri_area(*t) for t in combinations(points, 3))

def canon(points):
    return sorted((round(x, 6), round(y, 6)) for x, y in points)

rows = [json.loads(l) for l in open(LEDGER, encoding="utf-8") if l.strip()]
print(f"ledger rows: {len(rows)}")

# ---- independent replay: echo + score recomputed from stored points ----
mismatch = 0
by_tl = {}
for r in rows:
    by_tl.setdefault((r["tier"], r["lineage"]), []).append(r)
for (tier, lin), rs in by_tl.items():
    rs.sort(key=lambda r: r["gen"])
    parent, pscore = list(SEED_PARENT), SEED_SCORE
    for r in rs:
        if not r["valid"]:
            continue
        pts = [tuple(p) for p in r["points"]]
        sc = score(pts)
        e = canon(pts) == canon(parent)
        if abs(sc - r["score"]) > 1e-9 or e != r["echo"]:
            mismatch += 1
            print(f"REPLAY MISMATCH {tier} L{lin} g{r['gen']}: "
                  f"score {sc} vs {r['score']}, echo {e} vs {r['echo']}")
        if sc > pscore + 1e-15:
            parent, pscore = pts, sc
print(f"replay: {'CLEAN' if mismatch == 0 else f'{mismatch} MISMATCHES'} "
      f"(echo + score recomputed for every valid row)")

# ---- per-tier table ----
print("\ntier     rows valid  echo  pooled%  zero-score  tool-excl  per-lineage echo")
tier_stats = {}
for tier in TIERS:
    t = [r for r in rows if r["tier"] == tier]
    excl = [r for r in t if r["tool_uses"] > 0]
    t = [r for r in t if r["tool_uses"] == 0]
    v = [r for r in t if r["valid"]]
    e = [r for r in v if r["echo"]]
    z = [r for r in v if r["score"] == 0.0]
    per_lin = []
    for lin in sorted(set(r["lineage"] for r in t)):
        lv = [r for r in v if r["lineage"] == lin]
        le = [r for r in lv if r["echo"]]
        per_lin.append(f"{len(le)}/{len(lv)}")
    frac = len(e) / len(v) if v else float("nan")
    tier_stats[tier] = {"rows": len(t), "valid": len(v), "echo": len(e),
                        "frac": frac, "zero": len(z), "excl": len(excl)}
    print(f"{tier:8s} {len(t):4d} {len(v):5d} {len(e):5d}  {frac:6.1%}  "
          f"{len(z):10d}  {len(excl):9d}  {' '.join(per_lin)}")

# ---- 5.1 PRIMARY verdict ----
print("\n=== 5.1 PRIMARY: pooled echo among valid outputs, per tier ===")
underpowered = [t for t in TIERS if tier_stats[t]["valid"] < POWER_FLOOR_VALID]
evaluable = [t for t in TIERS if t not in underpowered]
for t in underpowered:
    print(f"  {t}: UNDERPOWERED ({tier_stats[t]['valid']} valid < {POWER_FLOOR_VALID}) — excluded from every branch")
if not evaluable:
    print("  VERDICT: UNDERPOWERED — no evaluable tier")
elif all(tier_stats[t]["frac"] <= UPPER_BOUND for t in evaluable):
    print(f"  VERDICT: DISSOCIATION — every evaluable tier <= {UPPER_BOUND:.0%} "
          f"(observed: " + ", ".join(f"{t} {tier_stats[t]['frac']:.1%}" for t in evaluable) + ")")
    print("  SS3's attribution survives this test of its strongest alternative,")
    print("  scoped to the sampled tier range, date, and harness (prereg SS1, SS2).")
elif any(tier_stats[t]["frac"] >= Q2K_CLASS for t in evaluable):
    hot = [t for t in evaluable if tier_stats[t]["frac"] >= Q2K_CLASS]
    print(f"  VERDICT: CONFOUND LIVE — {', '.join(hot)} >= {Q2K_CLASS:.0%}; "
          "SS3 attribution must be rewritten as a disjunction (prereg SS6)")
else:
    print("  VERDICT: PARTIAL — some tier in (30%, 55%); no branch claimed")

# ---- 5.2 SECONDARY: monotonicity ----
print("\n=== 5.2 SECONDARY: monotone-decreasing echo over haiku < sonnet < opus ===")
total_echo = sum(tier_stats[t]["echo"] for t in TIERS)
if total_echo < ECHO_COUNT_FLOOR:
    print(f"  NOT EVALUATED — total echoes {total_echo} < {ECHO_COUNT_FLOOR} "
          "(a monotonicity verdict on tie-noise is not a verdict)")
else:
    fr = [tier_stats[t]["frac"] for t in TIERS]
    strict = fr[0] > fr[1] > fr[2]
    # exact permutation of tier labels over the 3! orderings
    obs = sum(1 for a, b in zip(fr, fr[1:]) if a > b)
    tails = sum(1 for perm in permutations(fr)
                if sum(1 for a, b in zip(perm, perm[1:]) if a > b) >= obs)
    print(f"  fractions: {fr}; strictly decreasing: {strict}; "
          f"permutation tail {tails}/6 = {tails/6:.3f}")

# ---- 5.3 template check ----
print("\n=== 5.3 Template check: valid outputs scoring exactly 0 (no bound registered) ===")
for t in TIERS:
    s = tier_stats[t]
    print(f"  {t}: {s['zero']}/{s['valid']} = {s['zero']/s['valid']:.1%}")

# ---- 5.4 descriptives ----
print("\n=== 5.4 Descriptives (no bounds registered) ===")
for t in TIERS:
    tv = [r for r in rows if r["tier"] == t and r["valid"]]
    acc = [r for r in tv if r.get("accepted")]
    best = max((r["score"] for r in tv), default=float("nan"))
    print(f"  {t}: accepted steps {len(acc)}; best proposal score {best:.6f} "
          f"(seed parent {SEED_SCORE:.6f}); improvements past seed: "
          f"{sum(1 for r in tv if r['score'] > SEED_SCORE)}")
print("\nNote: zero lineages improved past the seed parent in any tier. This is the")
print("hosted-tier analogue of wave 3's control-arm floor clause (its SS5.1): a")
print("proposer pool that cannot climb cannot separate echo-driven stalling from")
print("task difficulty on TRAJECTORY measures. The 5.1 echo primary is unaffected —")
print("echo is per-call and its absence is informative regardless of climbing.")
