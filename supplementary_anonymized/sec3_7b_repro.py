"""
Section 3's 7B paragraph and the four Fisher tails no other released script replays.

Until now §3 carried a boundary paragraph conceding that four of its nine Fisher
tails (p = 5.7e-10, 0.001, 0.44, 1.0) and the whole 7B paragraph had to be computed
by the reader from the vendored rows. This script closes that gap: every figure in
both is derived here from the raw ledgers, so the claim map has no "reader must
compute this themselves" row left in §3.

Run:  python sec3_7b_repro.py
"""
import json, glob, os, collections
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "sec3_artifacts")
if not os.path.isdir(ART):
    ART = os.path.join(HERE, "..", "agent-run")
RUNGS = ["fp16", "q8_0", "q4_k_m", "q3_k_m", "q2_k"]
SEED_SCORE = 0.89999


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


def wilson(k, n, z=1.96):
    if n == 0:
        return 0.0, 1.0
    p, d = k / n, 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return c - h, c + h


def key(circles):
    if not circles:
        return None
    return tuple(sorted(tuple(round(float(v), 6) for v in c) for c in circles))


print("=" * 74)
print("PART 1 -- the four Fisher tails no other script replays (14B)")
print("=" * 74)

main = load("precision_sweep_14b_v2_output/**/cand*.jsonl")
fresh = load("precision_sweep_14b_fresh_output/**/cand*fresh.jsonl")

# echo counts, recomputed here rather than imported, so this script stands alone
st = json.load(open(glob.glob(os.path.join(
    ART, "precision_sweep_14b_v2_output/**/state/q2_k_seed_42.json"),
    recursive=True)[0], encoding="utf-8"))
SEED_KEY = key(st["best_circles"])


def echo_valid(rows):
    lin = collections.defaultdict(list)
    for r in rows:
        lin[(r["quant"], r["seed"])].append(r)
    out = collections.defaultdict(lambda: [0, 0])
    improved = collections.defaultdict(lambda: [0, 0])
    for (q, s), rs in lin.items():
        rs.sort(key=lambda r: r["gen"])
        parent, best = SEED_KEY, SEED_SCORE
        improved[q][1] += 1
        moved = False
        for r in rs:
            if not r.get("valid"):
                continue
            out[q][1] += 1
            if key(r.get("circles")) == parent:
                out[q][0] += 1
            if r.get("score") is not None and r["score"] > best:
                best, parent, moved = r["score"], key(r.get("circles")), True
        improved[q][0] += moved
    return out, improved


e_main, imp_main = echo_valid(main)
e_fresh, imp_fresh = echo_valid(fresh)

up_e = sum(e_main[q][0] for q in ("q8_0", "q4_k_m", "q3_k_m"))
up_v = sum(e_main[q][1] for q in ("q8_0", "q4_k_m", "q3_k_m"))
p1 = fisher_2x2(e_main["q2_k"][0], e_main["q2_k"][1] - e_main["q2_k"][0],
                up_e, up_v - up_e)
print(f"\n  echo, Q2_K {e_main['q2_k'][0]}/{e_main['q2_k'][1]} vs upper three "
      f"{up_e}/{up_v}:  p = {p1:.2e}   (paper: 5.7e-10)")

ua = sum(imp_main[q][0] for q in ("q8_0", "q4_k_m", "q3_k_m"))
un = sum(imp_main[q][1] for q in ("q8_0", "q4_k_m", "q3_k_m"))
b = imp_main["q2_k"]
p2 = fisher_2x2(ua, un - ua, b[0], b[1] - b[0])
print(f"  seed-level improvement, original seeds, upper three pooled {ua}/{un} vs "
      f"Q2_K {b[0]}/{b[1]}:  p = {p2:.4f}   (paper: 0.001)")
print(f"      (the paired within-rung contrast Q4_K_M {imp_main['q4_k_m'][0]}/"
      f"{imp_main['q4_k_m'][1]} vs Q2_K {b[0]}/{b[1]} gives "
      f"{fisher_2x2(imp_main['q4_k_m'][0], imp_main['q4_k_m'][1]-imp_main['q4_k_m'][0], b[0], b[1]-b[0]):.4f};"
      f"\n      the paper's 0.001 is the pooled form and this script prints both so the"
      f"\n      pooling is visible rather than implied)")
print("      NOTE this is the SUPERSEDED figure. section 3 says no claim rests on it;"
      " it is\n      replayed here only because the paper prints it.")

a, b = imp_fresh["q4_k_m"], imp_fresh["q2_k"]
p3 = fisher_2x2(a[0], a[1] - a[0], b[0], b[1] - b[0])
print(f"  seed-level improvement, FRESH seeds, Q4_K_M {a[0]}/{a[1]} vs "
      f"Q2_K {b[0]}/{b[1]}:  p = {p3:.4f}   (paper: 0.44)")
print("      This is the outcome of F1, the fresh wave's DESIGNATED PRIMARY, and it"
      " is\n      the value against which F1 is scored REFUTED (it forecast <= 2/5).")

print("\n" + "=" * 74)
print("PART 2 -- the 7B paragraph, in full")
print("=" * 74)

rows = load("precision_sweep/candidates_precision.jsonl")
probes = load("precision_sweep/probes_precision.jsonl")
print(f"\n7B ledger: {len(rows)} candidate rows, {len(probes)} probe rows")

vi = {q: sum(1 for r in rows if r["quant"] == q and r.get("viable")) for q in RUNGS}
n = {q: sum(1 for r in rows if r["quant"] == q) for q in RUNGS}
print(f"\n{'rung':<9}{'viable':<12}{'Wilson 95%':<22}{'valid'}")
for q in RUNGS:
    lo, hi = wilson(vi[q], n[q])
    va = sum(1 for r in rows if r["quant"] == q and r.get("valid"))
    print(f"{q:<9}{f'{vi[q]}/{n[q]}':<12}[{lo:.3f}, {hi:.3f}]{'':<6}{va}/{n[q]}")

print(f"\n  paper: viability 7/50, 6/50, 9/50, 7/50 across FP16..Q3_K_M, "
      f"Q2_K inverting at 16/50")
print(f"  FP16 {vi['fp16']}/50 vs Q3_K_M {vi['q3_k_m']}/50:  "
      f"p = {fisher_2x2(vi['fp16'], 50-vi['fp16'], vi['q3_k_m'], 50-vi['q3_k_m']):.4f}"
      f"   (paper: 1.0)  <- the fourth un-replayed tail")
up = sum(vi[q] for q in RUNGS if q != "q2_k")
print(f"  Q2_K {vi['q2_k']}/50 vs pooled upper four {up}/200:  "
      f"p = {fisher_2x2(vi['q2_k'], 50-vi['q2_k'], up, 200-up):.4f}   (paper: 0.007)")
print(f"  Q2_K {vi['q2_k']}/50 vs FP16 alone {vi['fp16']}/50:  "
      f"p = {fisher_2x2(vi['q2_k'], 50-vi['q2_k'], vi['fp16'], 50-vi['fp16']):.4f}"
      f"   (paper: 0.056, n.s.)")

print("\n  the format lottery -- viability at 7B reduces to count accuracy:")
cnt = collections.Counter(r["n_circles"] for r in rows)
print(f"    proposals with exactly 26 circles: {cnt[26]}/{len(rows)}   (paper: 45)")
print(f"    proposals with 24 or 25:           {cnt[24]+cnt[25]}/{len(rows)}"
      f"   (paper: 153)")
print(f"\n    {'rung':<9}{'modal count':<16}{'range observed'}")
for q in RUNGS:
    c = collections.Counter(r["n_circles"] for r in rows if r["quant"] == q)
    m, k = c.most_common(1)[0]
    print(f"    {q:<9}{f'{m} (x{k})':<16}{min(c)}-{max(c)}")
print("      Paper's claim is that the mode runs one or two SHORT of the target 26 from"
      "\n      FP16 through Q3_K_M and that Q2_K's distribution is broader and happens to"
      "\n      centre on 26. The modes above bear that out. The ranges do not line up as"
      "\n      neatly: Q4_K_M and Q3_K_M each carry a single 45-circle outlier, so 'broader'"
      "\n      is true of where the mass sits, not of the extreme. Printed so a reader sees"
      "\n      both.")

sub = [r for r in rows if r["n_circles"] in (24, 25)]
print(f"\n    truncation ruled out: max completion_tokens among the {len(sub)} rows with"
      f"\n    24-25 circles is {max(r['completion_tokens'] for r in sub)} against a 1200"
      f" cap   (paper: 687)")
print(f"    (max over ALL 7B rows is {max(r['completion_tokens'] for r in rows)}; the"
      f" paper's\n     figure is scoped to the 24-25 subset, which is the subset the"
      f" argument needs)")

print(f"\n    valid probes: {sum(1 for p in probes if p.get('valid'))}/{len(probes)}"
      f"   (paper: 0/30)")
print(f"    best score in the entire 7B sweep: {max(r['score'] for r in rows):.5f}"
      f"   (paper: 1.800)")
best = max(r["score"] for r in rows)
print(f"    against the canonical anchored value 2.5414: {100*(1-best/2.5414):.0f}% below"
      f"   (paper: 29%)")
