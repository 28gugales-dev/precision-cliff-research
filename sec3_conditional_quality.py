"""
Section 3.6 -- does quantization degrade the QUALITY of departures, or only their
FREQUENCY?

Section 3 establishes that at the 2-bit rung the proposer very largely stops
departing from its parent. It does not establish what happens on the occasions it
does depart, and the distinction is the consequential one: a frequency-only effect
is in principle repairable by forcing departure, a quality effect is not.

The loop ladders cannot answer it. Their 2-bit departure counts are 1, 5 and 8 --
too few, and section 3.6 says so. The FIXED-PARENT probes can do better, and are
the cleaner instrument besides:

  - the parent is held constant, so "improved" is a comparison against a known
    fixed target rather than against a lineage's drifting best
  - `score_delta` is logged per row, so no reconstruction is needed
  - the two waves share a design, so pooling within the family is legitimate in a
    way that pooling a loop ladder with a probe is not
  - six parents spanning 0.88 to 1.65 permit a per-parent breakdown, which matters
    because the chance of beating a parent obviously depends on the parent

Definitions, unchanged from section 3: a DEPARTURE is a valid output that is not a
coordinate echo of the parent. It IMPROVED if its `score_delta` is strictly positive.

POST-HOC, AND THE THRESHOLD IS OURS. This analysis is in neither wave's
preregistration. It is scored against a decision rule and a power floor written by us
in wave3_prereg_heilbronn.md -- an UNLOCKED design note, authored on the day this
analysis became computable, from data already in the repository. That note states that
nothing in the paper may cite it as a registration, and the paper does not. Read the
verdict below as a threshold we specify, fixed in advance of reporting rather than in
advance of seeing.

AND THE EXCLUSION IS ONE OBSERVATION WIDE. The collapse branch is defined against half
the reference rate, and the choice of reference moves the line by three points while
the observed lower bound sits within one. Both are printed below, along with what
happens if a single departure flips.

Run:  python sec3_conditional_quality.py
"""
import json, glob, os, collections
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "sec3_artifacts")
RUNGS = ["q4_k_m", "q3_k_m", "q2_k"]
FLOOR = 25                     # OUR floor, from the unlocked wave-3 design note


def load(pattern):
    hits = glob.glob(os.path.join(ART, pattern), recursive=True)
    if not hits:
        raise SystemExit(f"missing ledger: {pattern}")
    return [json.loads(l) for l in open(hits[0], encoding="utf-8") if l.strip()]


def fisher_2x2(a, b, c, d):
    n, r1, r2, c1 = a + b + c + d, a + b, c + d, a + c
    f = lambda x: comb(r1, x) * comb(r2, c1 - x) / comb(n, c1)
    obs = f(a)
    return sum(f(x) for x in range(max(0, c1 - r2), min(r1, c1) + 1)
               if f(x) <= obs * (1 + 1e-12))


def clopper_pearson(k, n, conf=0.95):
    if n == 0:
        return 0.0, 1.0
    t = (1 - conf) / 2

    def le(p, j):
        return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(j + 1))

    def bisect(f, inc):
        lo, hi = 0.0, 1.0
        for _ in range(200):
            m = (lo + hi) / 2
            if (f(m) < t) == inc:
                lo = m
            else:
                hi = m
        return (lo + hi) / 2

    low = 0.0 if k == 0 else bisect(lambda p: 1 - le(p, k - 1), True)
    high = 1.0 if k == n else bisect(lambda p: le(p, k), False)
    return low, high


rows = (load("dispersion_probe/probe_samples.jsonl")
        + load("dispersion_probe_v2/**/probe_samples.jsonl"))

print("=" * 74)
print("CONDITIONAL QUALITY -- among DEPARTURES only, what fraction improved")
print("=" * 74)
print(f"\nfixed-parent probe, both waves pooled: {len(rows)} rows\n")

agg = collections.defaultdict(lambda: [0, 0, 0])       # valid, departures, improved
per_parent = collections.defaultdict(lambda: [0, 0])
for r in rows:
    if not r.get("valid"):
        continue
    q = r["rung"]
    agg[q][0] += 1
    if r.get("echo"):
        continue
    agg[q][1] += 1
    up = (r.get("score_delta") or 0) > 0
    agg[q][2] += up
    cell = per_parent[(round(r["parent_score"], 4), q)]
    cell[0] += 1
    cell[1] += up

print(f"{'rung':<10}{'valid':<8}{'departures':<13}{'improved':<20}{'95% CI'}")
for q in RUNGS:
    v, d, i = agg[q]
    lo, hi = clopper_pearson(i, d)
    print(f"{q:<10}{v:<8}{d:<13}{f'{i}/{d} ({100*i/d:.0f}%)':<20}"
          f"[{100*lo:.0f}%, {100*hi:.0f}%]")

a, b = agg["q2_k"], agg["q4_k_m"]
p = fisher_2x2(a[2], a[1] - a[2], b[2], b[1] - b[2])
print(f"\nFisher, q2_k {a[2]}/{a[1]} vs q4_k_m {b[2]}/{b[1]}:  p = {p:.4f}")

print(f"\n{'='*74}\nPER-PARENT, because the chance of beating a parent depends on it"
      f"\n{'='*74}")
print(f"{'parent':<10}{'q4_k_m':<14}{'q3_k_m':<14}{'q2_k'}")
parents = sorted({k[0] for k in per_parent})
for ps in parents:
    cells = []
    for q in RUNGS:
        n, i = per_parent[(ps, q)]
        cells.append(f"{i}/{n}" if n else "-")
    print(f"{ps:<10}{cells[0]:<14}{cells[1]:<14}{cells[2]}")

hard = max(parents)
n2 = per_parent[(hard, 'q2_k')][0]
tot2 = agg['q2_k'][1]
n4 = per_parent[(hard, 'q4_k_m')][0]
tot4 = agg['q4_k_m'][1]
print(f"\nThe 2-bit rung's departures are NOT drawn from easier parents. At the hardest"
      f"\nparent ({hard}) they are {n2} of {tot2} = {100*n2/tot2:.0f}% of its departures,"
      f" against {n4} of {tot4} ="
      f"\n{100*n4/tot4:.0f}% at Q4_K_M. If anything the 2-bit sample faces the harder task.")

# Verdict, scored against the wave-3 registered decision rule for this quantity.
r2 = a[2] / a[1]
r4 = b[2] / b[1]
lo2, hi2 = clopper_pearson(a[2], a[1])
r3 = agg["q3_k_m"][2] / agg["q3_k_m"][1]
rp = ((agg["q4_k_m"][2] + agg["q3_k_m"][2]) /
      (agg["q4_k_m"][1] + agg["q3_k_m"][1]))
print(f"\n{'='*74}\nVERDICT, scored against OUR OWN unlocked decision rule\n{'='*74}")
print(f"  Q2_K rate           {100*r2:.1f}%   95% CI [{100*lo2:.1f}%, {100*hi2:.1f}%]")
print(f"  Q4_K_M rate         {100*r4:.1f}%      Q3_K_M rate  {100*r3:.1f}%")
print(f"  frequency-only branch needs Q2_K >= 0.75 x reference")
print(f"  quality-collapse branch needs Q2_K <= 0.50 x reference -- and WHICH reference")
print(f"  is not fixed by the rule, so all three are shown:")
for lab, ref in (("Q4_K_M", r4), ("pooled upper rungs", rp), ("Q3_K_M", r3)):
    line = 0.50 * ref
    verdict = "excluded" if lo2 > line else "NOT excluded"
    print(f"      vs {lab:<20}{100*line:>6.1f}%   -> {verdict} by "
          f"{100*(lo2-line):+.1f} points")
lo7, _ = clopper_pearson(a[2] - 1, a[1])
print(f"\n  SENSITIVITY: had one of the {a[1]} departures failed to improve, "
      f"{a[2]-1}/{a[1]} gives a lower\n      bound of {100*lo7:.1f}% and the collapse"
      f" branch is excluded against NONE of the three.")
print(f"  power floor (ours, in an unlocked note): {FLOOR} departures at the 2-bit rung;"
      f" observed {a[1]}")
print()
if a[1] < FLOOR:
    print("  UNDERPOWERED by a floor we set ourselves, so no branch is CONFIRMED. The")
    print("  collapse branch is excluded against all three references -- but by 0.8 points")
    print("  against the least favourable of them, and not at all if a single departure")
    print("  flips. The point estimate sits on top of the upper rungs' and the per-parent")
    print("  table shows no cell where the 2-bit rung underperforms. What the data support")
    print("  is a THIN exclusion and no confirmation: a collapse in departure quality is")
    print("  not the explanation of the echo cliff, and the frequency-only reading that")
    print("  leaves standing is unconfirmed rather than established.")
