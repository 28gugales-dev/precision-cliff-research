# ============================================================================
# Arm MU/CH scoring — preregistered in arm_mu_preregistration.txt (committed
# BEFORE sampling). Reads arm_mu_collect.jsonl (raw verbatim rows), applies
# arm-F conventions unchanged. Deterministic, no network.
# ============================================================================
import json
import math
from collections import Counter
from pathlib import Path

from arm_f_repro import parse_packing, validate, score

HERE = Path(__file__).parent
S2 = math.sqrt(2)
CELLS = [13, 21, 31]
KSTAR = {13: 4, 21: 5, 31: 6}
ANCHOR = {13: 1.6250000, 21: 2.1000000, 31: 2.5833333}
RIVAL = {13: 1.7761424, 21: 2.2588835, 31: 2.7485281}
ARGMAX_K = {13: 3, 21: 4, 31: 5}
WINDOW = 2e-3
PARENTS = json.loads((HERE / "arm_mu_prompts.json").read_text())


def dominant_k(circles):
    radii = [round(c[2], 6) for c in circles]
    r_dom, _ = Counter(radii).most_common(1)[0]
    return round(1.0 / (2.0 * r_dom)) if r_dom > 0 else None


def wilson(p, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    den = 1 + z * z / n
    c = p + z * z / (2 * n)
    hw = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - hw) / den, (c + hw) / den)


def main():
    rows = [json.loads(l) for l in
            (HERE / "arm_mu_collect.jsonl").read_text(encoding="utf-8-sig").splitlines()
            if l.strip()]
    print(f"rows: {len(rows)}")
    print("tie-break convention: descriptive per-cell 'modal' lines break count-ties by "
          "first-encountered bucket (Counter insertion order over file order). CH modal "
          "detection is tie-aware and counts ties as neither prediction. Known ties on "
          "this data: A_anchor N=31 (2.594 vs 2.584, both n=2) and C_offfamily N=13 "
          "(all valid buckets n=1); the latter makes P-MU4's N=13 entry tie-sensitive - "
          "an alternative tie-break could flip it False->True, which would only "
          "strengthen the template reading; the reported False is the conservative pick. "
          "The MU decision rule and F-MU1 use anchor-rates, not modals, and are "
          "tie-free.")
    recs = []
    for r in rows:
        circles, perr = parse_packing(r["raw"].strip() if r["raw"] else None)
        rec = dict(arm=r["arm"], cell=r["cell"], condition=r.get("condition"),
                   slot=r["slot"], parse_error=perr)
        if circles is not None:
            ok6, _ = validate(circles, r["cell"], tol=1e-6)
            ok9, _ = validate(circles, r["cell"], tol=1e-9)
            s = score(circles)
            rec.update(valid6=ok6, valid9=ok9, sum=round(s, 7),
                       k_emp=dominant_k(circles),
                       on_anchor=ok6 and abs(s - ANCHOR[r["cell"]]) < WINDOW)
            if r["arm"] == "mu" and r.get("condition") == "B_rival":
                ps = PARENTS["mu"][str(r["cell"])]["B_rival"]["parent_score"]
                rec["keep_or_improve"] = ok6 and s >= ps - WINDOW
            if r["arm"] == "ch":
                kk = ARGMAX_K[r["cell"]]
                m = r["cell"] - kk * kk
                argv = kk / 2 + m * (S2 - 1) / (2 * kk)
                rec["on_argmax"] = ok6 and abs(s - argv) < WINDOW
        recs.append(rec)

    # ---- MU per condition ----
    print("\n== ARM MU ==")
    pooled = {}
    for cond in ("A_anchor", "B_rival", "C_offfamily"):
        sub = [r for r in recs if r["arm"] == "mu" and r["condition"] == cond]
        valid = [r for r in sub if r.get("valid6")]
        anc = [r for r in valid if r["on_anchor"]]
        p = len(anc) / len(valid) if valid else 0.0
        lo, hi = wilson(p, len(valid))
        pooled[cond] = dict(sampled=len(sub), valid=len(valid), anchor=len(anc),
                            rate=p, ci=(round(lo, 3), round(hi, 3)))
        extra = ""
        if cond == "B_rival":
            koi = [r for r in valid if r.get("keep_or_improve")]
            kinh = [r for r in valid if r.get("k_emp") == ARGMAX_K[r["cell"]]]
            pooled[cond]["keep_or_improve"] = len(koi)
            pooled[cond]["k_inherit"] = len(kinh)
            extra = f" keep-or-improve {len(koi)}/{len(valid)}; k-inherit {len(kinh)}/{len(valid)}"
        print(f"{cond}: valid {len(valid)}/{len(sub)}, anchor-rate {len(anc)}/{len(valid)}"
              f" = {p:.2%} CI[{lo:.2f},{hi:.2f}]{extra}")
        for n in CELLS:
            cell = [r for r in valid if r["cell"] == n]
            ca = [r for r in cell if r["on_anchor"]]
            buckets = Counter(round(r["sum"] / WINDOW) for r in cell)
            mb = buckets.most_common(1)[0] if buckets else (None, 0)
            mv = [r["sum"] for r in cell if buckets and round(r["sum"] / WINDOW) == mb[0]]
            kdist = dict(Counter(str(r.get("k_emp")) for r in cell))
            print(f"  N={n}: anchor {len(ca)}/{len(cell)}, modal "
                  f"{round(sum(mv)/len(mv),7) if mv else None} ({mb[1]}), k_emp {kdist}")

    # ---- registered decisions ----
    b = pooled.get("B_rival", {})
    if b.get("valid"):
        rate = b["rate"]
        koi_rate = b["keep_or_improve"] / b["valid"]
        if rate >= 0.50:
            verdict = "SURVIVES (anchor-rate >= 50% under B_rival)"
        elif rate <= 0.20 and koi_rate >= 0.50:
            verdict = "DISSOLVES -> F-MU1 TRIGGERED"
        else:
            verdict = (f"PARTIAL: anchor-rate {rate:.0%} CI{b['ci']}, "
                       f"keep-or-improve {koi_rate:.0%}")
        print(f"\nDECISION (registered rule): {verdict}")
        a = pooled["A_anchor"]
        print(f"P-MU1 (A anchor-rate >= 50%): {'MET' if a['rate'] >= 0.50 else 'NOT MET'} ({a['rate']:.0%})")
        print(f"P-MU2 (B anchor-rate >= 35%): {'MET' if rate >= 0.35 else 'NOT MET'} ({rate:.0%})")
        kin_rate = b["k_inherit"] / b["valid"]
        print(f"P-MU3 (B k-inheritance < 50%): {'MET' if kin_rate < 0.50 else 'NOT MET'} ({kin_rate:.0%})")

    # P-MU4: C_offfamily modal bucket structural k == k*
    c_valid = [r for r in recs if r["arm"] == "mu" and r["condition"] == "C_offfamily" and r.get("valid6")]
    mu4 = []
    for n in CELLS:
        cell = [r for r in c_valid if r["cell"] == n]
        buckets = Counter(round(r["sum"] / WINDOW) for r in cell)
        if not buckets:
            mu4.append(False)
            continue
        mb = buckets.most_common(1)[0][0]
        ks = [r.get("k_emp") for r in cell if round(r["sum"] / WINDOW) == mb]
        mu4.append(bool(ks) and Counter(ks).most_common(1)[0][0] == KSTAR[n])
    print(f"P-MU4 (C modal on k* grid, per cell): {mu4}")

    # ---- CH ----
    print("\n== ARM CH ==")
    ch1 = ch2 = 0
    for n in CELLS:
        cell = [r for r in recs if r["arm"] == "ch" and r["cell"] == n and r.get("valid6")]
        buckets = Counter(round(r["sum"] / WINDOW) for r in cell)
        anchor_b = round(ANCHOR[n] / WINDOW)
        kk = ARGMAX_K[n]
        m = n - kk * kk
        argv = kk / 2 + m * (S2 - 1) / (2 * kk)
        arg_b = round(argv / WINDOW)
        top = buckets.most_common(2)
        modal_b, modal_n = top[0] if top else (None, 0)
        tie = len(top) > 1 and top[1][1] == modal_n
        is1 = (not tie) and modal_b == anchor_b
        is2 = (not tie) and modal_b == arg_b
        ch1 += is1
        ch2 += is2
        mv = [r["sum"] for r in cell if modal_b is not None and round(r["sum"] / WINDOW) == modal_b]
        print(f"N={n}: valid {len(cell)}, modal {round(sum(mv)/len(mv),7) if mv else None} ({modal_n})"
              f"{' TIE' if tie else ''}, anchor={ANCHOR[n]}, argmax={argv:.7f}"
              f" -> {'T-anchor' if is1 else ('ARGMAX' if is2 else 'other')}")
    print(f"P-CH1 (template, modal=T(k*,N) at >=2/3): {'HOLDS' if ch1 >= 2 else 'no'} ({ch1}/3)")
    print(f"P-CH2 (tractability, modal=argmax at >=2/3): {'HOLDS' if ch2 >= 2 else 'no'} ({ch2}/3)")
    if ch1 < 2 and ch2 < 2:
        print("CH verdict: INCONCLUSIVE (registered wording)")

    (HERE / "arm_mu_scored.json").write_text(json.dumps(recs, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
