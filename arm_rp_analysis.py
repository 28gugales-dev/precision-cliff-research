# Arm RP scorer. Classifies each response: RECALLS (within 2e-3 of the
# published value for that N), FAMILY (within 2e-3 of V(k*,m)/T(k*,N)),
# UNKNOWN (the literal token), or UNPARSEABLE. No geometry, so validity does
# not apply. Registered rules of arm_rp_preregistration.txt; committed
# before sampling.
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
COLLECT = ROOT / "arm_rp_collect.jsonl"
PROMPTS = json.loads((ROOT / "arm_rp_prompts.json").read_text(encoding="utf-8"))
WINDOW = 2e-3
NUM = re.compile(r"-?\d+(?:\.\d+)?")


def classify(text, meta):
    t = (text or "").strip()
    if not t:
        return "UNPARSEABLE", None
    if "unknown" in t.lower():
        return "UNKNOWN", None
    nums = NUM.findall(t)
    if len(nums) != 1:
        return "UNPARSEABLE", None
    v = float(nums[0])
    if meta["published"] is not None and abs(v - meta["published"]) < WINDOW:
        return "RECALLS", v
    if abs(v - meta["family_prediction"]) < WINDOW:
        return "FAMILY", v
    return "OTHER", v


def main():
    rows = [json.loads(l) for l in COLLECT.read_text(encoding="utf-8").splitlines() if l.strip()]
    report = {"cells": {}, "pooled": {}}
    recalls_sb = family_sb = n_sb = 0
    family_ho = n_ho = 0
    for key, meta in PROMPTS.items():
        n = meta["n"]
        sub = [r for r in rows if r["n"] == n and not r.get("runtime_rejection")]
        rej = [r for r in rows if r["n"] == n and r.get("runtime_rejection")]
        counts = {"RECALLS": 0, "FAMILY": 0, "UNKNOWN": 0, "UNPARSEABLE": 0, "OTHER": 0}
        values = []
        for r in sub:
            cls, v = classify(r.get("raw_output"), meta)
            counts[cls] += 1
            if v is not None:
                values.append(round(v, 7))
        if meta["kind"] == "scoreboard":
            recalls_sb += counts["RECALLS"]
            family_sb += counts["FAMILY"]
            n_sb += len(sub)
        else:
            family_ho += counts["FAMILY"]
            n_ho += len(sub)
        report["cells"][key] = {"n": n, "kind": meta["kind"], "scored": len(sub),
                                "runtime_rejections": len(rej), **counts,
                                "distinct_values": sorted(set(values))}
        print(f"N={n:>2} {meta['kind']:<10} {counts}  values {sorted(set(values))[:6]}")
    fam_rate_sb = family_sb / n_sb if n_sb else 0.0
    fam_rate_ho = family_ho / n_ho if n_ho else 0.0
    asym = (fam_rate_sb - fam_rate_ho) * 100
    p_rp1 = recalls_sb <= 2 and asym <= 20
    p_rp2 = recalls_sb >= 10
    verdict = ("P-RP2 (F-RP1 TRIGGERED)" if p_rp2 else
               "P-RP1" if p_rp1 else "PARTIAL")
    report["pooled"] = {
        "recalls_scoreboard": recalls_sb, "scoreboard_n": n_sb,
        "family_rate_scoreboard": round(fam_rate_sb, 4),
        "family_rate_held_out": round(fam_rate_ho, 4),
        "asymmetry_pp": round(asym, 1), "verdict": verdict,
    }
    (ROOT / "arm_rp_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nRECALLS at scoreboard cells: {recalls_sb}/{n_sb}; FAMILY sb {fam_rate_sb:.0%} "
          f"vs held-out {fam_rate_ho:.0%} (asymmetry {asym:+.1f} pp)")
    print(f"VERDICT: {verdict}")
    print("report frozen in arm_rp_report.json")


if __name__ == "__main__":
    main()
