# Item 5 of the round-13 outside review: the clearance rule requires validity at 1e-9, but the
# pooled 0-of-290 denominator counts CC, CC2, CCS, CN and L at the primary 1e-6. Every ledger
# holds what is needed to state the 1e-9 count too: CN's frozen report carries valid9 per cell,
# arm L's carries valid_1e9 per generation, and the three code arms store every program
# verbatim, so they are re-executed here through the registered scorer (arm_cc_analysis.py,
# unchanged, 10-second timeout) and counted at both tolerances. This is bookkeeping over rows
# already in the study, adds no invocations, and is disclosed as post hoc. Deterministic by
# construction: the registered AST gate blocks `random`, and the programs run under python -I.
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = Path(r"~\AppData\Local\hermes\research-corpus\precision-cliff")
sys.path.insert(0, str(CORPUS))
import arm_cc_analysis as cc  # noqa: E402  (registered scorer, imported unmodified)

out = {}


def family_argmax(N):
    import math
    best = 0.0
    for k in range(2, 14):
        if N < k * k:
            best = max(best, N / (2 * k))
        else:
            m = N - k * k
            if m <= (k - 1) ** 2:
                best = max(best, k / 2 + m * (math.sqrt(2) - 1) / (2 * k))
    return best


ARGMAX = {n: family_argmax(n) for n in (13, 21, 31)}

# ---- code arms: re-execute and count
for arm, ledger in [("CC", "arm_cc_collect.jsonl"), ("CC2", "arm_cc2_collect.jsonl"), ("CCS", "arm_ccs_collect.jsonl")]:
    rows = [json.loads(l) for l in open(CORPUS / ledger, encoding="utf-8-sig") if l.strip()]
    v6 = v9 = 0
    above9 = 0
    for r in rows:
        n = int(r["cell"]) if "cell" in r else int(r["n"])
        res = cc.score_row(r["raw"], n)
        if res.get("bin") == "valid":
            v6 += 1
            if res.get("valid_1e9"):
                v9 += 1
                if res["sum"] > ARGMAX[n] + 1e-6:
                    above9 += 1
    out[arm] = dict(rows=len(rows), valid_1e6=v6, valid_1e9=v9, clear_1e9=above9)
    print(f"{arm}: {len(rows)} rows, valid 1e-6 {v6}, valid 1e-9 {v9}, clear {above9}")

# the frozen reports are the reference for the 1e-6 counts; the recount must reproduce them
frozen = {"CC": 37, "CC2": 41, "CCS": 37}
for arm, n6 in frozen.items():
    assert out[arm]["valid_1e6"] == n6, (arm, out[arm]["valid_1e6"], n6)

# ---- CN: per-cell counts are in the frozen report
cn = json.load(open(ROOT / "evidence" / "arm_cn_report.json", encoding="utf-8-sig"))["cells"]
out["CN"] = dict(valid_1e6=sum(c["valid6"] for c in cn.values()), valid_1e9=sum(c["valid9"] for c in cn.values()))
assert out["CN"]["valid_1e6"] == 63
print("CN:", out["CN"])

# ---- L: conditioned generations 1..5 of each lineage
lr = json.load(open(ROOT / "evidence" / "arm_l_report.json", encoding="utf-8-sig"))["lineages"]
v6 = v9 = 0
for name, L in lr.items():
    gens = L["generations"]
    gens = gens if isinstance(gens, list) else [gens[k] for k in sorted(gens, key=int)]
    for g in gens[1:]:
        v6 += g["valid_1e6"]
        v9 += g["valid_1e9"]
out["L"] = dict(valid_1e6=v6, valid_1e9=v9)
assert v6 == 49, v6
print("L:", out["L"])

# ---- MU is already counted at 1e-9 in the pool (63)
out["MU"] = dict(valid_1e6=88, valid_1e9=63)
pool6 = out["CC"]["valid_1e6"] + out["CC2"]["valid_1e6"] + out["CCS"]["valid_1e6"] + out["CN"]["valid_1e6"] + out["L"]["valid_1e6"] + out["MU"]["valid_1e9"]
pool9 = sum(out[a]["valid_1e9"] for a in ["CC", "CC2", "CCS", "CN", "L", "MU"])
out["pool"] = dict(as_reported=pool6, all_at_1e9=pool9)
assert pool6 == 290, pool6
print("pool: as reported", pool6, "| all six arms at 1e-9", pool9)
(ROOT / "evidence" / "valid_1e9_counts.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
