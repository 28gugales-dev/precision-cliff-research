"""
Section 3.6 addendum -- why final best score is structurally blind.

CAUTION, READ FIRST. An earlier draft used this script's power table to state that
section 3.6's design had "roughly 17% power". That claim is WITHDRAWN. Power is
power against a specific alternative; the only alternative this model supplies is
its own projection, which comes out backwards and rests on six Q2_K offers. What
survives here is the structural argument below and the design guidance at the end
-- not a number.

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
this script exists to produce is a structural argument about the dependent variable
-- not a result and not a power figure, and no claim in the paper rests on it.

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


def perm_p_mc(a, b, nperm=2000):
    """Monte-Carlo permutation with the (hits+1)/(nperm+1) correction. The power
    sweep runs thousands of these, so exact enumeration is not affordable here;
    the correction keeps the estimate conservative rather than anti-conservative."""
    pooled = list(a) + list(b)
    na = len(a)
    obs = abs(statistics.mean(a) - statistics.mean(b))
    hits = 0
    for _ in range(nperm):
        RNG.shuffle(pooled)
        if abs(statistics.mean(pooled[:na]) - statistics.mean(pooled[na:])) >= obs - 1e-12:
            hits += 1
    return (hits + 1) / (nperm + 1)


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

print()
print("READ THE SIGN. The projected gap is NEGATIVE at every horizon: under this model")
print("the 2-bit rung ends AHEAD, and the margin widens with the budget. That is not a")
print("prediction we believe and it is not one the paper makes. It follows from the")
print("estimation asymmetry noted above -- Q2_K's offer distribution is six observations")
print("with mean 1.226 and max 1.625, Q4_K_M's is thirty-three with mean 0.962 and max")
print("1.300, so a single jackpot offer sets the ceiling the max statistic converges to.")
print("Conditional on departing at all, the 2-bit rung's observed offers are not worse.")
print("That is the same open question section 3.6 poses and declines to answer, seen")
print("here through a resampling model too thin to answer it either.")
print()
print("So the directional projection is discarded -- and with it any power figure")
print("derived from it, because power is power against a SPECIFIC alternative and this")
print("model supplies only the one just disowned. The table below is printed for")
print("completeness and is NOT a power statement about the design section 3.6 reports.")
print("See the closing block for what does survive.")

BAR = "=" * 74
print()
print(BAR)
print("POWER: fraction of simulated experiments returning p < 0.05")
print(BAR)
print("lineage-level permutation on final best score, two-sided, 2000 shuffles per")
print("test with the (hits+1)/(nperm+1) correction; 200 simulated experiments per cell")
print()
print(f"{'gens/lineage':<15}{'5 vs 5':<12}{'8 vs 8':<12}{'12 vs 12':<12}{'20 vs 20'}")
for T in (10, 50, 100, 200, 400, 800):
    row = []
    for L_ in (5, 8, 12, 20):
        reps, hits = 200, 0
        for _ in range(reps):
            a = simulate("q2_k", T, reps=L_)
            b = simulate("q4_k_m", T, reps=L_)
            if perm_p_mc(a, b) < 0.05:
                hits += 1
        row.append(f"{100*hits/reps:.0f}%")
    print(f"{T:<15}{row[0]:<12}{row[1]:<12}{row[2]:<12}{row[3]}")

print()
print("Read the first row for the design section 3.6 actually reports: ten generations,")
print("five lineages per rung. That is the power its outcome-level null was observed at.")


print(f"\n{'='*74}\nWHAT THIS SAYS ABOUT THE WAVE THAT WOULD SETTLE IT\n{'='*74}")
print("""  READ THIS BEFORE QUOTING ANY NUMBER ABOVE.

  An earlier draft of section 3.6 quoted the top-left power cell, 17 percent, as
  the power of the design the paper reports. That was wrong and the paper has
  withdrawn it. Power is power against a SPECIFIC alternative, and the only
  alternative this model supplies is its own projection -- the one printed above
  as unusable, resting on six Q2_K offers of which the maximum appears twice and
  one entry is the seed score itself. Six observations cannot carry a direction
  and cannot carry an effect size either.

  The power column also does not behave like power at T = 10: the rejection rate
  FALLS as lineages are added, 17 / 8 / 5 / 4 percent for 5 / 8 / 12 / 20. That is
  the coarse permutation tail at five-versus-five doing the work, not an effect.
  Read that row as a warning about the instrument.

  And "widen rather than lengthen" does not follow from this table either. Cost
  equalised, lengthening wins: 5 lineages x 100 generations is 500 calls for 84
  percent, 12 x 50 is 600 calls for 82.

  WHAT SURVIVES is structural and independent of every estimate here. Best-so-far
  is a MAXIMUM, so it is insensitive to the draw count by construction -- more
  draws move it by the distance between two upper quantiles of the same offer
  distribution, not by anything proportional to the draw ratio. A wave that wants
  to demonstrate harm should not use final best score as its dependent variable.
  It should measure time-to-threshold, area under the best-so-far curve, or the
  accepted-step count itself, which is what section 3.6 measures and what the
  wave-3 registration adopts as its primary.

  No claim in the paper rests on any number above.""")
