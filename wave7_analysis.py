#!/usr/bin/env python3
"""Wave 7 registered analysis — no arguments, replays everything from the raw ledgers.

Registration: wave7_prereg_families.md, SHA-256
44244005bf272916e5950f6aeec79011eb6c17382c39b7df6a0873e03c956c59, pushed as public
Kaggle dataset sohamgugalet/wave7-prereg-families before any sampling.

Every verdict label is computed and printed here, not written by us (prereg SS7).
Per family, independently — NO POOLING, per the registration. A family whose output
directory is absent is reported PENDING and skipped; the script is safe to run
before both kernels have returned.

Echo and scores are recomputed from the stored coordinate lists, not read from the
ledger's convenience fields. Stored coordinates are 6 dp (the ledger convention);
the echo definition is itself 6 dp order-insensitive set equality, so the primary
carries no extra rounding. Acceptance is replayed with strict > on recomputed sums
and cross-checked against every kernel state file; any disagreement prints loudly
(wave 3's phantom-step lesson).
"""
import json, os
from math import comb, hypot

HERE = os.path.dirname(os.path.abspath(__file__))
N = 26
EPS = 1e-6
COORD_DP = 6

FAMILIES = {
    "llama31_8b": os.path.join(HERE, "wave7_output", "wave7_llama31_8b"),
    "gemma2_9b":  os.path.join(HERE, "wave7_output", "wave7_gemma2_9b"),
}

def canon(circles):
    return sorted((round(x, COORD_DP), round(y, COORD_DP), round(r, COORD_DP))
                  for (x, y, r) in circles)

def valid_score(circles):
    """Re-derive validity and score from coordinates (mirrors the runner)."""
    if circles is None or len(circles) != N or any(r <= 0 for (_, _, r) in circles):
        return False, 0.0
    inside = all(x - r >= -EPS and x + r <= 1 + EPS and
                 y - r >= -EPS and y + r <= 1 + EPS for (x, y, r) in circles)
    if not inside:
        return False, 0.0
    for i in range(N):
        xi, yi, ri = circles[i]
        for j in range(i + 1, N):
            xj, yj, rj = circles[j]
            if hypot(xi - xj, yi - yj) + EPS < ri + rj:
                return False, 0.0
    return True, sum(r for (_, _, r) in circles)

def baseline_packing():
    r = round(0.9 / N, 6)
    pts = []
    for row in range(5):
        for col in range(6):
            if len(pts) >= N:
                break
            pts.append((round((col + 0.5) / 6.0, 6), round((row + 0.5) / 5.0, 6), r))
    return pts

BASE = baseline_packing()
BASE_OK, BASE_SCORE = valid_score(BASE)
assert BASE_OK and abs(BASE_SCORE - 0.89999) < 1e-4

def fisher_two_sided(a, b, c, d):
    n = a + b + c + d; r1 = a + b; c1 = a + c
    def p(x): return comb(r1, x) * comb(n - r1, c1 - x) / comb(n, c1)
    p0 = p(a)
    return sum(p(x) for x in range(max(0, c1 - (n - r1)), min(r1, c1) + 1)
               if p(x) <= p0 + 1e-12)

def analyse_family(fam, out_dir):
    ledger = os.path.join(out_dir, f"candidates_wave7_{fam}.jsonl")
    md_log = os.path.join(out_dir, f"mustdiffer_wave7_{fam}.jsonl")
    state_dir = os.path.join(out_dir, "state")
    if not os.path.exists(ledger):
        print(f"\n##### {fam}: PENDING — no ledger at {ledger}")
        return
    rows = [json.loads(l) for l in open(ledger, encoding="utf-8") if l.strip()]
    print(f"\n##### {fam}: {len(rows)} ledger rows")

    per = {}
    for r in rows:
        per.setdefault((r["quant"], r["seed"]), []).append(r)
    mismatch_valid = 0
    lineage = {}
    for (quant, seed), rs in per.items():
        rs.sort(key=lambda r: r["gen"])
        parent, pscore = list(BASE), BASE_SCORE
        accepted = echo = valid = 0
        for r in rs:
            circles = (None if r["circles"] is None
                       else [tuple(c) for c in r["circles"]])
            ok, sc = valid_score(circles)
            if ok != r["valid"]:
                mismatch_valid += 1
            if not ok:
                continue
            valid += 1
            if canon(circles) == canon(parent):
                echo += 1
            if sc > pscore:
                parent, pscore = circles, sc
                accepted += 1
        sp = os.path.join(state_dir, f"{quant}_seed_{seed}.json")
        agrees = None
        if os.path.exists(sp):
            st = json.load(open(sp))
            agrees = abs(st["best_score"] - pscore) < 1e-9
        lineage[(quant, seed)] = {"accepted": accepted, "echo": echo,
                                  "valid": valid, "best": pscore,
                                  "improved": pscore > BASE_SCORE + 1e-12,
                                  "state_agrees": agrees}
    bad = [k for k, v in lineage.items() if v["state_agrees"] is False]
    print(f"validity replay: {'CLEAN' if mismatch_valid == 0 else f'{mismatch_valid} MISMATCHES'}")
    known = [v for v in lineage.values() if v["state_agrees"] is not None]
    print(f"state-file agreement: {sum(1 for v in known if v['state_agrees'])}/{len(known)}"
          + (f"  DISAGREE: {bad}" if bad else ""))

    def pool(quant):
        ls = [v for (q, s), v in lineage.items() if q == quant]
        return {"lineages": len(ls),
                "valid": sum(l["valid"] for l in ls),
                "echo": sum(l["echo"] for l in ls),
                "mean_accepted": (sum(l["accepted"] for l in ls) / len(ls)
                                  if ls else 0.0),
                "improved": sum(1 for l in ls if l["improved"]),
                "bests": sorted(round(l["best"], 6) for l in ls)}
    q4, q2 = pool("q4_k_m"), pool("q2_k")
    for name, p in (("q4_k_m", q4), ("q2_k", q2)):
        er = p["echo"] / p["valid"] if p["valid"] else float("nan")
        print(f"{name}: lineages {p['lineages']}, valid {p['valid']}, "
              f"echo {p['echo']}/{p['valid']} = {er:.1%}, "
              f"mean accepted {p['mean_accepted']:.3f}, "
              f"seeds improved {p['improved']}/{p['lineages']}, "
              f"bests {p['bests']}")

    print(f"=== 7.1 PRIMARY echo contrast ({fam}) — NOT floor-gated ===")
    if q2["valid"] < 20 or q4["valid"] < 20:
        print(f"  UNDERPOWERED — valid rows q2_k {q2['valid']}, q4_k_m {q4['valid']} "
              "(floor: 20 at either rung). No branch claimed.")
    else:
        e2, e4 = q2["echo"] / q2["valid"], q4["echo"] / q4["valid"]
        gap = (e2 - e4) * 100
        if gap >= 15 and e2 >= 0.30:
            label = "HELD"
        elif gap <= 5:
            label = "REFUTED"
        else:
            label = "INCONCLUSIVE"
        print(f"  echo q2_k {e2:.1%}, q4_k_m {e4:.1%}, gap {gap:.1f}pp -> {label}")
        print(f"  descriptive Fisher (unregistered): p = "
              f"{fisher_two_sided(q2['echo'], q2['valid']-q2['echo'], q4['echo'], q4['valid']-q4['echo']):.2e}")

    print(f"=== 7.2 SECONDARY search progress ({fam}) — floor-gated ===")
    if q4["mean_accepted"] < 1.0:
        print(f"  CONTROL FLOOR TRIGGERED — q4_k_m mean accepted "
              f"{q4['mean_accepted']:.3f} < 1.0. 7.2 UNINFORMATIVE for {fam}; "
              "7.1 expressly unaffected.")
    else:
        ratio = (q2["mean_accepted"] / q4["mean_accepted"])
        label = ("HELD" if ratio <= 0.5 else
                 "REFUTED" if q2["mean_accepted"] >= q4["mean_accepted"]
                 else "INCONCLUSIVE")
        print(f"  q2_k {q2['mean_accepted']:.3f} vs q4_k_m {q4['mean_accepted']:.3f} "
              f"(ratio {ratio:.2f}) -> {label}")

    print(f"=== 7.3 Must-differ probe ({fam}), q2_k ===")
    if not os.path.exists(md_log):
        print("  no probe log present")
    else:
        md = [json.loads(l) for l in open(md_log, encoding="utf-8") if l.strip()]
        for quant in ("q2_k", "q4_k_m"):
            qm = [r for r in md if r["quant"] == quant]
            vv = [r for r in qm if r["valid"]]
            ech = sum(1 for r in vv
                      if canon([tuple(c) for c in r["circles"]]) == canon(BASE))
            tag = ""
            if quant == "q2_k":
                if len(vv) < 5:
                    tag = " -> UNDERPOWERED (<5 valid probes)"
                else:
                    rate = ech / len(vv)
                    tag = (" -> instruction-INSENSITIVE (degraded novelty)"
                           if rate >= 0.5 else
                           " -> instruction-SENSITIVE" if rate <= 0.2
                           else " -> inconclusive")
            print(f"  {quant}: probes {len(qm)}, valid {len(vv)}, "
                  f"echo-under-differ {ech}/{len(vv)}{tag}")

for fam, out_dir in FAMILIES.items():
    analyse_family(fam, out_dir)

print("\nDisconfirmation clause (prereg SS6): fires only if 7.1 is REFUTED in BOTH")
print("families with both evaluable; split outcome reports FAMILY-DEPENDENT verbatim.")
