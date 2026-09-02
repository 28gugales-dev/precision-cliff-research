# ============================================================================
# Arm P-D analysis -- arm P's registered direct-emission scorer
# (arm_p_analysis.score_direct_row, imported unmodified: arm-F parse,
# validity at 1e-6 primary and 1e-9 logged, sum, structure, dominant k)
# applied per condition. Registered quantities per condition: valid counts,
# on-prediction (|sum - 1.625| < 2e-3), rival (|sum - 1.7761424| < 2e-3),
# modal valid value, k_emp distribution. Predictions P-PD1/P-PD2/P-PD3 and
# the anchor secondary S-PD1 evaluated as registered. Writes arm_pd_report.json.
# ============================================================================
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import arm_p_analysis as pa  # noqa: E402

SPEC = json.loads((HERE / "arm_pd_prompts.json").read_text(encoding="utf-8"))
ANCHOR, RIVAL, WINDOW, N = SPEC["anchor_value"], SPEC["rival_value"], pa.WINDOW, SPEC["n"]
HI, LO = 8, 3  # registered: >= 8 of 15 valid vs <= 3 of 15


def main():
    rows = [r for r in pa.load_rows(HERE / "arm_pd_collect.jsonl") if r.get("raw_len", 0) > 0]
    latest = {}
    for r in rows:
        latest[(r["condition"], r["sample_id"])] = r
    rows = list(latest.values())
    report = {"conditions": {}, "rows": []}
    for cond in ("D1", "D2"):
        cr = [r for r in rows if r["condition"] == cond]
        sc = []
        for r in cr:
            s = pa.score_direct_row(r["raw"], N)
            s.update(sample_id=r["sample_id"], reasoning_len=r.get("reasoning_len"))
            sc.append(s)
            report["rows"].append(dict(condition=cond, **s))
        valid = [s for s in sc if s["valid6"]]
        on_pred = [s for s in valid if abs(s["sum"] - ANCHOR) < WINDOW]
        rival = [s for s in valid if abs(s["sum"] - RIVAL) < WINDOW]
        buckets = Counter(round(s["sum"] / WINDOW) for s in valid)
        modal = buckets.most_common(2)
        modal_value = None
        if modal and (len(modal) == 1 or modal[0][1] > modal[1][1]):
            modal_value = round(modal[0][0] * WINDOW, 4)
        report["conditions"][cond] = {
            "sampled": len(cr), "valid_1e6": len(valid), "valid_1e9": sum(s["valid9"] for s in sc),
            "parse_fail": sum(1 for s in sc if s["parse_error"]),
            "invalid_why": dict(Counter(s.get("why6") for s in sc if not s["valid6"] and not s["parse_error"])),
            "on_prediction": len(on_pred), "rival": len(rival), "modal_valid_value": modal_value,
            "k_emp": dict(Counter(s.get("k_emp") for s in valid)),
            "structures": dict(Counter(s.get("structure") for s in valid)),
            "sums": sorted(round(s["sum"], 7) for s in valid),
            "median_reasoning_len": sorted(s["reasoning_len"] or 0 for s in sc)[len(sc) // 2] if sc else None,
        }
        c = report["conditions"][cond]
        print(f"{cond}: sampled {c['sampled']}, valid {c['valid_1e6']} (1e-9 {c['valid_1e9']}), parse fail {c['parse_fail']}, "
              f"on-pred {c['on_prediction']}, rival {c['rival']}, modal {c['modal_valid_value']}, k {c['k_emp']}")
    d1, d2 = report["conditions"]["D1"], report["conditions"]["D2"]
    full = d1["sampled"] == 15 and d2["sampled"] == 15
    if d1["valid_1e6"] >= HI and d2["valid_1e6"] <= LO:
        verdict = "P-PD1 holds: the reasoning budget is the cause"
    elif d2["valid_1e6"] >= HI and d1["valid_1e6"] <= LO:
        verdict = "P-PD2 holds: the system prompt / context is the cause"
    else:
        verdict = "P-PD3: cause not located by these two manipulations"
    s_pd1 = {}
    for cond, c in (("D1", d1), ("D2", d2)):
        if c["valid_1e6"] >= HI:
            s_pd1[cond] = {"modal_is_anchor": c["modal_valid_value"] is not None and abs(c["modal_valid_value"] - ANCHOR) < WINDOW,
                           "on_prediction": f"{c['on_prediction']}/{c['valid_1e6']}"}
    report["verdict"] = verdict + ("" if full else " (INTERIM: sampling incomplete)")
    report["S-PD1"] = s_pd1 or "no condition reached 8 valid"
    print("VERDICT:", report["verdict"], "| S-PD1:", report["S-PD1"])
    (HERE / "arm_pd_report.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print("written arm_pd_report.json")


if __name__ == "__main__":
    main()
