# Arm B bridge row (2026-09-03, round 18). NOT a new registered arm and NOT a re-registration
# of arm B: it re-runs arm B's already-registered N = 31 cell, byte-identical template and
# pipeline, on the machine that would run any larger-N extension. Purpose is instrument
# calibration only. The published arm B ran where an unscored timing probe fit 80 restarts in
# 95 s at N = 31; this machine fits 49 in 120 s (armb_timing_probe.json), so the fixed
# RESTARTS = 50 sits at the wall here. If this cell does not reproduce 15/15 valid and 15/15
# clear, no larger-N extension on this machine is interpretable and none should be registered.
#
# Writes arm_b_bridge_collect.jsonl and arm_b_bridge_report.json. The registered artifacts
# arm_b_collect.jsonl and arm_b_report.json are never opened for writing.
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import arm_cl_analysis as cl  # noqa: E402

CELL = 31
SEEDS = list(range(1, 16))
TEMPLATE = (HERE / "arm_b_baseline.py").read_text(encoding="utf-8")
TEMPLATE_SHA = hashlib.sha256(TEMPLATE.encode("utf-8")).hexdigest()
PUBLISHED = {"n_valid": 15, "n_cleared": 15, "best_sum": None}  # best filled from arm_b_report

published = json.loads((HERE / "arm_b_report.json").read_text(encoding="utf-8"))
PUBLISHED["best_sum"] = published["cells"][str(CELL)]["best_sum"]
assert published["template_sha256"] == TEMPLATE_SHA, "template drifted from the published run"

rows = [{"tier": "baseline", "n": CELL, "sample_id": s,
         "raw": TEMPLATE.replace("__N__", str(CELL)).replace("__SEED__", str(s)),
         "template_sha256": TEMPLATE_SHA} for s in SEEDS]
with open(HERE / "arm_b_bridge_collect.jsonl", "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")

print(f"bridge: N={CELL}, {len(rows)} rows, 120 s wall, template sha {TEMPLATE_SHA[:12]}", flush=True)
scored = cl.score_all(rows, timeout_s=120)
bins = Counter(s["bin"] for s in scored)
valid = [s for s in scored if s["bin"] == "valid"]
cleared = [s for s in valid if s["cleared"]]
best = max((s["sum"] for s in valid), default=None)
report = {
    "purpose": "instrument calibration for a larger-N arm B extension; not a registered arm",
    "template_sha256": TEMPLATE_SHA, "timeout_s": 120, "n": CELL, "sampled": len(rows),
    "bins": dict(bins), "n_valid": len(valid), "n_cleared": len(cleared),
    "argmax_closed_form": round(cl.ARGMAX[CELL], 9),
    "best_sum": round(best, 9) if best is not None else None,
    "published": PUBLISHED,
    "reproduces": (len(valid) == PUBLISHED["n_valid"] and len(cleared) == PUBLISHED["n_cleared"]),
    "sums": sorted(round(s["sum"], 9) for s in valid),
}
print(json.dumps({k: v for k, v in report.items() if k != "sums"}, indent=1), flush=True)
(HERE / "arm_b_bridge_report.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
print("REPRODUCES" if report["reproduces"] else "DOES NOT REPRODUCE", "-> written arm_b_bridge_report.json")
