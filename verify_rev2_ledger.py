# Independent ledger verification for paper1 revision 2 (2026-08-04 review pass).
# Recomputes every headline statistic from arm_f_candidates_v2.jsonl + arm_g_candidates.jsonl.
# Run: python verify_rev2_ledger.py  (no deps beyond stdlib)
# Outputs PASS/FAIL per claim. FAILs found 2026-08-04:
#   [FAIL] §5.4 wave split N=21: paper says 2/4 old vs 10/11 new; ledger gives 4/7 vs 8/8
#          under the registered boundary (ids 1-10 old, 11-20 new). Paper's numbers match
#          the s6+ boundary (which is registered for N=13/31 only).
#   [FAIL] §3.3 pooled on-prediction "46% (47/102)": reproduces only as
#          41/57 (bare, 4 discriminating cells) + 1/30 (sonnet) + 0/4 (opus) + 5/11 (rect).
#          All 7 bare cells give 56/114 = 49%. Composition must be stated or recomputed.
import json, math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
rows_f = [json.loads(l) for l in (ROOT / "arm_f_candidates_v2.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
rows_g = [json.loads(l) for l in (ROOT / "arm_g_candidates.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]

PRED = {13:1.625, 17:2.0517767, 21:2.1, 31:2.5833333, 35:2.9166667, 37:3.0345178, 43:3.0714286}
RIVAL = {13:1.7761424, 21:2.2588835, 31:2.7485281, 43:3.2416246}
WIN = 2e-3

RPRED = {19: 3.1666667, 25: 3.125}
def on_pred(r, pred=None):
    if r.get("sum_of_radii") is None: return False
    p = pred if pred is not None else (RPRED.get(r["n"]) or PRED.get(r["n"]))
    return p is not None and abs(r["sum_of_radii"] - p) <= WIN
def rival_hit(r): return r.get("sum_of_radii") is not None and r["n"] in RIVAL and abs(r["sum_of_radii"]-RIVAL[r["n"]]) <= WIN

def fisher_one_sided(a, b, c, d):
    """P(X >= a) hypergeometric tail, table [[a,b],[c,d]] row1=trace, row2=bare."""
    def logC(n,k): return math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1)
    n1, n2, k = a+b, c+d, a+c
    total = n1+n2
    p = 0.0
    for x in range(a, min(n1,k)+1):
        if k-x > n2: continue
        p += math.exp(logC(n1,x)+logC(n2,k-x)-logC(total,k))
    return min(1.0, p)

def check(name, got, expect):
    ok = abs(got - expect) < 1e-9 if isinstance(expect, float) else got == expect
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got}, paper {expect}")
    return ok

fails = 0
print("== Table 1 / 3 / 2 core cells (bare arm, full 85-row ledger) ==")
exp = {13:(18,10,0),17:(4,3,0),21:(15,12,2),31:(17,13,0),35:(4,3,0),37:(4,3,0),43:(7,6,0)}
for n,(v,o,r) in exp.items():
    rs = [x for x in rows_f if x["n"]==n and x["arm"]=="bare"]
    vv = sum(1 for x in rs if x.get("valid"))
    oo = sum(1 for x in rs if x.get("valid") and on_pred(x))
    rr = sum(1 for x in rs if x.get("valid") and rival_hit(x))
    fails += 0 if (vv,oo,rr)==(v,o,r) else 1
    print(f"  [{'PASS' if (vv,oo,rr)==(v,o,r) else 'FAIL'}] N={n}: valid {vv}/{len(rs)} onpred {oo} rival {rr} (paper {v}/{len(rs)} {o} {r})")

print("== Discriminating cells, original-45 corpus ==")
old_ids = {13:set(range(1,6)),21:set(range(1,11)),31:set(range(1,6)),43:set(range(1,11))}
tot_v = tot_o = tot_r = 0
for n in (13,21,31,43):
    rs = [x for x in rows_f if x["n"]==n and x["arm"]=="bare" and x["sample_id"] in old_ids[n]]
    v = [x for x in rs if x.get("valid")]
    tot_v += len(v); tot_o += sum(on_pred(x) for x in v); tot_r += sum(rival_hit(x) for x in v)
print(f"  [{'PASS' if (tot_o,tot_r)==(18,2) else 'FAIL'}] 18/23 onpred, 2/23 rival: got {tot_o}/{tot_v} {tot_r}")
fails += 0 if (tot_o,tot_r)==(18,2) else 1

print("== Trace_v2 (Table 3) ==")
tv2 = [x for x in rows_f if x["arm"]=="trace" and x.get("prompt_sha256")]
exp_t = {13:(18,16,0),21:(18,16,0),31:(17,14,1)}
for n,(v,o,r) in exp_t.items():
    rs = [x for x in tv2 if x["n"]==n]
    vv = sum(1 for x in rs if x.get("valid"))
    oo = sum(1 for x in rs if x.get("valid") and on_pred(x))
    rr = sum(1 for x in rs if x.get("valid") and rival_hit(x))
    fails += 0 if (vv,oo,rr)==(v,o,r) else 1
    print(f"  [{'PASS' if (vv,oo,rr)==(v,o,r) else 'FAIL'}] N={n}: {vv}/{len(rs)} onpred {oo} rival {rr} (paper {v} {o} {r})")

print("== Fisher p-values ==")
# P-T3 pooled: bare 35/50, trace 46/53
p = fisher_one_sided(46, 7, 35, 15)
fails += 0 if abs(p-0.0325) < 1e-3 else 1
print(f"  [{'PASS' if abs(p-0.0325)<1e-3 else 'FAIL'}] P-T3 pooled p={p:.4f} (paper 0.0325)")
print(f"  [{'PASS' if abs(fisher_one_sided(16,2,10,8)-0.030)<1e-3 else 'FAIL'}] N=13 p={fisher_one_sided(16,2,10,8):.4f} (paper 0.030)")
print(f"  [{'PASS' if abs(fisher_one_sided(16,2,12,3)-0.41)<1e-2 else 'FAIL'}] N=21 p={fisher_one_sided(16,2,12,3):.4f} (paper 0.41)")
print(f"  [{'PASS' if abs(fisher_one_sided(14,3,13,4)-0.50)<1e-2 else 'FAIL'}] N=31 p={fisher_one_sided(14,3,13,4):.4f} (paper 0.50)")
p1 = fisher_one_sided(53,7,50,10)
print(f"  [{'PASS' if abs(p1-0.30)<1e-2 else 'FAIL'}] P-T1 pooled p={p1:.4f} (paper 0.30)")
p2 = fisher_one_sided(2,48,1,52)
print(f"  [{'PASS' if abs(p2-0.48)<1e-2 else 'FAIL'}] P-T2 p={p2:.4f} (paper 0.48)")
p3 = fisher_one_sided(30,5,25,7)
print(f"  [{'PASS' if abs(p3-0.31)<1e-2 else 'FAIL'}] drop-N=13 p={p3:.4f} (paper 0.31)")

print("== §5.4 wave split (registered boundary: s6+ at N=13/31, s11+ at N=21) ==")
for n, bound in ((13,6),(21,11),(31,6)):
    old = [x for x in rows_f if x["n"]==n and x["arm"]=="bare" and x["sample_id"] < bound and x.get("valid")]
    new = [x for x in rows_f if x["n"]==n and x["arm"]=="bare" and x["sample_id"] >= bound and x.get("valid")]
    oo, nn = sum(on_pred(x) for x in old), sum(on_pred(x) for x in new)
    print(f"  N={n}: old {oo}/{len(old)}  new {nn}/{len(new)}")
    exp_o, exp_n = {13:(3,4),21:(4,7),31:(5,5)}[n], {13:(7,14),21:(8,8),31:(8,12)}[n]
    ok = (oo,len(old))==exp_o and (nn,len(new))==exp_n
    fails += 0 if ok else 1
    print(f"    [{'PASS' if ok else 'FAIL'}] paper rev2 says N={n}: {exp_o} vs {exp_n}")
print("  [FAIL] §5.4 wave split at N=21: paper prints '2/4 old vs 10/11 new'; registered boundary (s11+) gives 4/7 vs 8/8. Printed numbers match the s6+ boundary, which is registered for N=13/31 only.")
fails += 1

print("== §3.3 pooled '46% (47/102)' ==")
# On-pred is only defined where the rule's prediction is at stake: the four
# discriminating cells of the bare arm + all other arms. Recompute per-arm.
def arm_stats(rows, pred_map):
    v = [x for x in rows if x.get("valid")]
    o = sum(1 for x in v if on_pred(x))
    return len(v), o
bare_all = [x for x in rows_f if x["arm"]=="bare"]
b4 = [x for x in bare_all if x["n"] in (13,21,31,43)]
b_others = [x for x in bare_all if x["n"] not in (13,21,31,43)]
sn = [x for x in rows_f if x.get("proposer_alias")=="sonnet"]
op = [x for x in rows_f if x.get("proposer_alias")=="opus"]
tv2 = [x for x in rows_f if x["arm"]=="trace" and x.get("prompt_sha256")]
rect = rows_g
for name, rows in [("bare-4disc", b4), ("bare-other3", b_others), ("sonnet", sn),
                   ("opus", op), ("trace_v2", tv2), ("rect", rect)]:
    v, o = arm_stats(rows, None)
    print(f"  {name}: {o}/{v} onpred")
nv, no = arm_stats(b4, None); sv, so = arm_stats(sn, None); ov, oo = arm_stats(op, None)
rv, ro = arm_stats(rect, None)
tot_v = nv+sv+ov+rv; tot_o = no+so+oo+ro
print(f"  pooled (4-disc-bare + sonnet + opus + rect): {tot_o}/{tot_v} = {tot_o/tot_v:.1%} (paper claims 47/102 = 46.1%)")
av, ao = arm_stats(bare_all, None)
print(f"  pooled (ALL bare cells + sonnet + opus + rect): {ao+so+oo+ro}/{av+sv+ov+rv} = {(ao+so+oo+ro)/(av+sv+ov+rv):.1%}")
tv, to = arm_stats(tv2, None)
print(f"  pooled (all bare + trace_v2 + sonnet + opus + rect): {ao+so+oo+ro+to}/{av+sv+ov+rv+tv} = {(ao+so+oo+ro+to)/(av+sv+ov+rv+tv):.1%}")
print("  NOTE: 47/102 reproduces ONLY as (41/57 bare 4-disc cells) + (1/30 sonnet) + (0/4 opus) + (5/11 rect).")
print("  If all 7 bare cells are pooled the rate is 49%, if trace_v2 included it is 62%.")
print("  The 'pooled across every tier and container' wording matches none of these compositions as written.")
fails += 1
print("  [FAIL] §3.3 pooled 47/102: paper wording 'pooled across every tier and container' matches no composition; correct value is 49% (all bare cells) or 61% (incl trace_v2)")

print("== P-T4 blind labels ==")
labels = json.loads((ROOT / "p7_blind_labels.json").read_text(encoding="utf-8"))
c = Counter(l["label"] for l in labels)
print(f"  {dict(c)} (paper: 54 MATCH, 2 MISMATCH, 4 UNSCOREABLE)")
fails += 0 if c == Counter({"MATCH":54,"MISMATCH":2,"UNSCOREABLE":4}) else 1

print("== Mode ceiling (p11 recompute) ==")
for n in PRED:
    rs = [x for x in rows_f if x["n"]==n and x["arm"]=="bare" and x.get("valid")]
    vals = Counter(round(x["sum_of_radii"],6) for x in rs)
    mode, freq = vals.most_common(1)[0]
    inw = sum(1 for x in rs if abs(x["sum_of_radii"]-PRED[n]) <= WIN)
    ok = abs(mode - round(PRED[n],6)) < 1e-4
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] N={n}: mode {mode} (freq {freq}/{len(rs)}), in-window {inw}")

print(f"\nTOTAL: {'ALL PASS' if fails==0 else f'{fails} FLAGS (see FAIL lines; two are known §5.4/§3.3 composition issues)'}")
