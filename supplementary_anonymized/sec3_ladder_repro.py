"""
Recompute every headline figure in paper 2 section 3 from the raw candidate
ledgers, the way arm_f_repro.py does for section 4.

Section 3 previously cited `precision-cliff-paper-combined.md` -- a prose
document -- rather than raw rows. The ledgers were in research-corpus/agent-run/
rather than alongside the paper, which is why they read as missing. This script
closes that gap: every number below is derived from the jsonl, never copied.

Echo definition (paper section 3): a *valid* output whose emitted circle set is
identical to its lineage's running parent, order-insensitive, at the logs'
six-decimal precision.

Run:  python sec3_ladder_repro.py
"""
import json, glob, os, collections
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))

# Ladder outputs are vendored under sec3_artifacts/ so this replays in a fresh
# clone; the sibling agent-run tree is the authoring host's copy and is a fallback.
AGENT_RUN = os.path.join(HERE, "sec3_artifacts")
if not os.path.isdir(AGENT_RUN):
    AGENT_RUN = os.path.join(HERE, "..", "agent-run")

def load(pattern):
    hits = glob.glob(os.path.join(AGENT_RUN, pattern), recursive=True)
    if not hits:
        raise SystemExit(f"missing ledger: {pattern}")
    return [json.loads(l) for l in open(hits[0], encoding="utf-8") if l.strip()]

def key(circles):
    """Order-insensitive fingerprint at six decimals."""
    if not circles:
        return None
    return tuple(sorted(tuple(round(float(v), 6) for v in c) for c in circles))

def fisher_2x2(a, b, c, d):
    """Two-sided Fisher exact on [[a,b],[c,d]] by summing tables no more
    probable than the observed one."""
    n = a + b + c + d
    r1, r2, c1 = a + b, c + d, a + c
    def p(x):
        return comb(r1, x) * comb(r2, c1 - x) / comb(n, c1)
    obs = p(a)
    lo, hi = max(0, c1 - r2), min(r1, c1)
    return sum(p(x) for x in range(lo, hi + 1) if p(x) <= obs * (1 + 1e-12))

def seed_parent():
    """Every lineage starts from the same seeded valid parent: a trivial 6x5
    grid truncated to 26 circles, scoring 0.89999. Recovered from a lineage
    state file whose best_score never moved off the seed."""
    hits = glob.glob(os.path.join(AGENT_RUN,
                     "precision_sweep_14b_v2_output/**/state/q2_k_seed_42.json"),
                     recursive=True)
    st = json.load(open(hits[0], encoding="utf-8"))
    assert abs(st["best_score"] - 0.89999) < 1e-9, "state file is not the seed grid"
    return key(st["best_circles"]), st["best_score"]

SEED_KEY, SEED_SCORE = None, 0.0

def echo_by_rung(rows, label):
    """Replay each (quant, seed) lineage, tracking the running parent, and
    count valid rows whose circle set equals it."""
    out = collections.defaultdict(lambda: [0, 0])          # rung -> [echo, valid]
    per_seed = collections.defaultdict(lambda: [0, 0])
    invalid_nearcopy = collections.defaultdict(lambda: [0, 0])
    lineages = collections.defaultdict(list)
    for r in rows:
        lineages[(r["quant"], r["seed"])].append(r)
    for (q, s), rs in lineages.items():
        rs.sort(key=lambda r: r["gen"])
        # The running parent is best-so-far and advances only on STRICT
        # improvement -- the loop's own hill-climb rule. Lineages that never
        # improve keep the seeded 6x5 grid as parent for all ten generations,
        # which is exactly the q2_k case (state files end at best_score
        # 0.89999 == the seed). Advancing on >= instead lets the parent drift
        # and undercounts echo.
        parent, best = SEED_KEY, SEED_SCORE
        for r in rs:
            k = key(r.get("circles"))
            if r.get("valid"):
                out[q][1] += 1
                per_seed[(q, s)][1] += 1
                if parent is not None and k == parent:
                    out[q][0] += 1
                    per_seed[(q, s)][0] += 1
            else:
                invalid_nearcopy[q][1] += 1
                # near-copy: shares >= n-1 circles with the running parent
                if parent is not None and r.get("circles"):
                    shared = len(set(k or ()) & set(parent))
                    if shared >= max(len(parent) - 1, 1):
                        invalid_nearcopy[q][0] += 1
            if r.get("valid") and r.get("score") is not None and r["score"] > best:
                parent, best = k, r["score"]
    print(f"\n--- {label}: echo among valid, by rung ---")
    for q in sorted(out, key=lambda x: (len(x), x)):
        e, v = out[q]
        pct = f"{100*e/v:.0f}%" if v else "n/a"
        print(f"   {q:<10} echo {e}/{v}  ({pct})")
    print(f"   per-seed (echo/valid):")
    for (q, s) in sorted(per_seed):
        e, v = per_seed[(q, s)]
        print(f"     {q:<10} seed {s:<5} {e}/{v}")
    print(f"   invalid rows that are near-copies of the running parent:")
    for q in sorted(invalid_nearcopy):
        c, t = invalid_nearcopy[q]
        print(f"     {q:<10} {c}/{t}")
    return out

def viability_validity(rows, label):
    print(f"\n--- {label}: viability / validity by rung ---")
    by = collections.defaultdict(lambda: [0, 0, 0])
    for r in rows:
        b = by[r["quant"]]
        b[0] += 1
        b[1] += 1 if r.get("viable") else 0
        b[2] += 1 if r.get("valid") else 0
    for q in by:
        t, vi, va = by[q]
        print(f"   {q:<10} viable {vi}/{t}   valid {va}/{t}")
    return by

print("=" * 68)
print("PAPER 2 SECTION 3 -- recomputed from raw ledgers")
print("=" * 68)

SEED_KEY, SEED_SCORE = seed_parent()
print(f"\nseed parent: {len(SEED_KEY)} circles, score {SEED_SCORE}")

main = load("precision_sweep_14b_v2_output/**/cand*.jsonl")
print(f"\n14B re-execution ledger: {len(main)} rows")
viability_validity(main, "14B re-execution")
m = echo_by_rung(main, "14B re-execution")

fresh = load("precision_sweep_14b_fresh_output/**/cand*fresh.jsonl")
print(f"\n14B fresh-seed ledger: {len(fresh)} rows")
f = echo_by_rung(fresh, "14B fresh seeds")

iq2 = load("precision_sweep_14b_iq2_output/**/cand*iq2.jsonl")
print(f"\n14B IQ2 control ledger: {len(iq2)} rows")
i = echo_by_rung(iq2, "14B IQ2 control")

for name, pat in (("must-differ (official)", "precision_sweep_14b_fresh_output/**/mustdiffer_14b.jsonl"),
                  ("must-differ (IQ2)", "precision_sweep_14b_iq2_output/**/mustdiffer_14b_iq2.jsonl")):
    try:
        md = load(pat)
    except SystemExit:
        print(f"\n{name}: ledger not found"); continue
    # The must-differ probe holds the parent FIXED at the seeded grid, so echo
    # is a direct comparison against SEED_KEY. There is no echo flag in this
    # ledger -- it must be computed from coordinates.
    print(f"\n--- {name}: {len(md)} rows ---")
    by = collections.defaultdict(lambda: [0, 0])
    for r in md:
        if r.get("valid"):
            by[r["quant"]][1] += 1
            if key(r.get("circles")) == SEED_KEY:
                by[r["quant"]][0] += 1
    for q in by:
        e, v = by[q]
        print(f"   {q:<12} coordinate-identical to fixed parent: {e}/{v} valid")
    assert all(abs(r.get("parent_score", 0) - SEED_SCORE) < 1e-9 for r in md), \
        "must-differ parent is not the seed grid"

print("\n" + "=" * 68)
print("PAPER CLAIMS TO CHECK AGAINST THE ABOVE")
print("=" * 68)
print("""  viability 14B:  22/50, 22/50, 24/50, 19/50  (q8_0/q4_k_m/q3_k_m/q2_k)
  validity  14B:  18/50, 20/50, 19/50, 18/50
  echo re-exec :  2/18, 3/20, 3/19 upper three = 8/57 (14%)  vs  17/18 (94%) q2_k
  per-seed q2_k:  7/7, 4/4, 4/4, 1/1, 1/2
  fresh seeds  :  19/24 (79%) q2_k  vs  1/17 (6%) q4_k_m,  Fisher p = 3.4e-6
  must-differ  :  5/5 q2_k,  1/5 q4_k_m
  IQ2 control  :  24/32 (75%) imatrix q2_k  vs  12/28 (43%) iq2_m,  p = 0.017
  invalid near-copy: 0/33 fresh q4_k_m, 2/22 iq2_m, 5/18 imatrix q2_k,
                     15/26 fresh q2_k, 18/32 re-exec q2_k""")
print(f"\n  Fisher check 19/24 vs 1/17: p = {fisher_2x2(19, 5, 1, 16):.2e}  (paper: 3.4e-6)")
print(f"  Fisher check 24/32 vs 12/28: p = {fisher_2x2(24, 8, 12, 16):.4f}  (paper: 0.017)")
print(f"  Fisher check 87/200 vs 38/200: p = {fisher_2x2(87, 113, 38, 162):.2e}  (paper: 1.7e-7)")
print(f"  Fisher check 16/50 vs 29/200: p = {fisher_2x2(16, 34, 29, 171):.4f}  (paper: 0.007)")
print(f"  Fisher check 16/50 vs 7/50:   p = {fisher_2x2(16, 34, 7, 43):.4f}  (paper: 0.056 n.s.)")
