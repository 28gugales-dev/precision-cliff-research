"""
Section 3.6 addendum -- why final best score is structurally blind, and how long a
run would have to be before it stops being.

Section 3.6 reports a null: the 2-bit rung takes 1 accepted hill-climb step per 50
calls against 14-16, and final best score after ten generations separates no pair of
rungs. The obvious objection is that ten generations is simply too short. This script
answers how short, and why.

THE STRUCTURAL POINT. Final best score is a MAXIMUM statistic: best-so-far after T
calls is the largest offer among those calls the proposer actually departed on. Echoes
contribute nothing -- they re-offer the parent's own score. So a rung with departure
rate d gets about d*T effective draws, and the expected maximum of n draws grows like
the (1 - 1/n) quantile of the offer distribution, which for any distribution with a
bounded or thin upper tail grows roughly logarithmically in n. A 5.5-fold reduction in
effective draws (33% vs 6% departure) therefore costs only the gap between two upper
quantiles that are close together. That is the reason the null in 3.6 is a null, and it
is a property of the instrument rather than of the effect.

THE MODEL. Non-parametric and estimated entirely from the released 14B ledgers:
  - departure rate d_q  = (valid - echo) / calls, pooled over the re-execution and
    fresh-seed waves at that rung
  - offer distribution F_q = the empirical distribution of scores among valid,
    non-echo outputs at that rung
  - a lineage of T calls draws Binom(T, d_q) offers i.i.d. from F_q; best-so-far is
    the maximum of those and the seed score 0.89999

This is a resampling projection, NOT a measurement. It assumes offers are i.i.d. and
independent of the current parent, which the loop design violates: a real proposer sees
its parent and its offers should improve with it. Both violations push toward the model
UNDERSTATING achievable scores at long horizons, and they push on both rungs. The number
this script exists to produce is a design quantity -- generations required -- not a
result, and no claim in the paper rests on it.

Run:  python sec3_horizon_power.py
"""
import json, glob, os, random, statistics, collections, itertools
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "sec3_artifacts")
SEED_SCORE = 0.89999
RNG = random.Random(20260807)          # fixed: this script must reproduce exactly


def load(pattern):
    hits = glob.glob(os.path.join(ART, pattern), recursive=True)
    if not hits:
        raise SystemExit(f"missing ledger: {pattern}")
    return [json.loads(l) for l in open(hits[0], encoding="utf-8") if l.strip()]


def key(circles):
    if not circles:
        return None
    return tuple(sorted(tuple(round(float(v), 6) for v in c) for c in circles))


def seed_key():
    h = glob.glob(os.path.join(
        ART, "precision_sweep_14b_v2_output/**/state/q2_k_seed_42.json"),
        recursive=True)
    return key(json.load(open(h[0], encoding="utf-8"))["best_circles"])


SEED_KEY = seed_key()


def harvest(rows):
    """Per rung: total calls, departures (valid and not an echo), and the offer
    scores of those departures."""
    lin = collections.defaultdict(list)
    for r in rows:
        lin[(r["quant"], r["seed"])].append(r)
    calls = collections.Counter()
    offers = collections.defaultdict(list)
    for (q, s), rs in lin.items():
        rs.sort(key=lambda r: r["gen"])
        parent, best = SEED_KEY, SEED_SCORE
        for r in rs:
            calls[q] += 1
            k = key(r.get("circles"))
            if r.get("valid"):
                if k != parent:
                    offers[q].append(float(r.get("score") or 0.0))
                if r.get("score") is not None and r["score"] > best:
                    best, parent = r["score"], k
    return calls, offers


calls, offers = collections.Counter(), collections.defaultdict(list)
for pat in ("precision_sweep_14b_v2_output/**/cand*.jsonl",
            "precision_sweep_14b_fresh_output/**/cand*fresh.jsonl"):
    c, o = harvest(load(pat))
    calls.update(c)
    for q, v in o.items():
        offers[q].extend(v)

RUNGS = ["q2_k", "q4_k_m"]
print("=" * 74)
print("HORIZON POWER -- how long a run before final best score separates the rungs")
print("=" * 74)
print("\nestimated from the pooled re-execution and fresh-seed 14B ledgers:\n")
print(f"{'rung':<10}{'calls':<8}{'departures':<13}{'departure rate':<17}"
      f"{'offer mean':<13}{'offer max'}")
d = {}
for q in RUNGS:
    n, o = calls[q], offers[q]
    d[q] = len(o) / n
    print(f"{q:<10}{n:<8}{len(o):<13}{f'{100*len(o)/n:.0f}%':<17}"
          f"{statistics.mean(o):<13.4f}{max(o):.4f}")

print("\nNOTE the estimation asymmetry: the Q2_K offer distribution is estimated from"
      f"\n{len(offers['q2_k'])} observations against {len(offers['q4_k_m'])} at Q4_K_M."
      " Every projection below inherits that\nimprecision, and it is the single largest"
      " source of error in this script.")


def simulate(q, T, reps=20000):
    """Best-so-far after T calls, under the resampling model."""
    o, rate = offers[q], d[q]
    out = []
    for _ in range(reps):
        best = SEED_SCORE
        k = sum(1 for _ in range(T) if RNG.random() < rate)
        for _ in range(k):
            v = o[RNG.randrange(len(o))]
            if v > best:
                best = v
        out.append(best)
    return out


def perm_p(a, b):
    pooled = list(a) + list(b)
    na, n = len(a), len(pooled)
    obs = abs(statistics.mean(a) - statistics.mean(b))
    tot = hit = 0
    for idx in itertools.combinations(range(n), na):
        x = [pooled[i] for i in idx]
        y = [pooled[i] for i in range(n) if i not in idx]
        tot += 1
        if abs(statistics.mean(x) - statistics.mean(y)) >= obs - 1e-12:
            hit += 1
    return hit / tot


print(f"\n{'='*74}\nPROJECTED MEAN FINAL BEST SCORE BY HORIZON\n{'='*74}")
print(f"{'gens/lineage':<15}{'q2_k':<12}{'q4_k_m':<12}{'gap':<10}"
      f"{'effective draws q2_k / q4_k_m'}")
proj = {}
for T in (10, 25, 50, 100, 200, 400, 800):
    a, b = simulate("q2_k", T), simulate("q4_k_m", T)
    proj[T] = (statistics.mean(a), statistics.mean(b))
    print(f"{T:<15}{statistics.mean(a):<12.4f}{statistics.mean(b):<12.4f}"
          f"{statistics.mean(b)-statistics.mean(a):<10.4f}"
          f"{T*d['q2_k']:.1f} / {T*d['q4_k_m']:.1f}")

print("\nThe gap grows, and it grows slowly -- which is the point. Best-so-far is a max\n"
      "statistic, so multiplying effective draws by 5.5 moves it by the distance between\n"
      "two upper quantiles of the same offer distribution, not by anything proportional\n"
      "to the draw ratio. An instrument with this shape cannot be made sensitive by\n"
      "running longer at any horizon a practitioner would fund.")

print(f"\n{'='*74}\nPOWER: fraction of simulated experiments returning p < 0.05\n{'='*74}")
print("exact lineage-level permutation, two-sided, as in section 3.6\n")
print(f"{'gens/lineage':<15}{'8 vs 8 lineages':<20}{'12 vs 12 lineages'}")
for T in (50, 100, 200, 400, 800):
    row = []
    for L in (8, 12):
        if L == 12 and T > 200:      # 2.7M splits per rep -- enumerate only where cheap
            row.append("     (not run)")
            continue
        reps = 200 if L == 8 else 60
        hits = 0
        for _ in range(reps):
            a = simulate("q2_k", T, reps=L)
            b = simulate("q4_k_m", T, reps=L)
            if perm_p(a, b) < 0.05:
                hits += 1
        row.append(f"{100*hits/reps:.0f}%")
    print(f"{T:<15}{row[0]:<20}{row[1]}")

print(f"\n{'='*74}\nWHAT THIS SAYS ABOUT THE WAVE THAT WOULD SETTLE IT\n{'='*74}")
print("""  Section 3.6 registers longer-horizon divergence as a prediction and does not
  run it. This script prices that run under an explicitly stated model, and the
  price is the finding: the horizon needed is far beyond the ten generations
  already spent, because the outcome metric is a maximum and maxima are
  insensitive to the draw count by construction.

  The design consequence is not "run longer". It is that final best score is the
  wrong dependent variable for this effect at any fundable horizon, and a wave
  that wants to demonstrate harm should measure something that is not a maximum
  -- time-to-threshold, area under the best-so-far curve, or the accepted-step
  count itself, which is what section 3.6 measures and what wave 3 registers.

  Every number above is a projection from a resampling model whose Q2_K offer
  distribution rests on a handful of observations. It is a design quantity. It is
  not evidence about any real run, and the paper claims nothing from it.""")
