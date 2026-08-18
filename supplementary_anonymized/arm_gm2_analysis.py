"""Arm GM analysis — scores arm_gm2_raw.json under the registered definitions.

Registered in arm_gm_preregistration.txt (commit 37b3adb):
- valid = arm_f_repro.validate at 1e-6 (ladder also reported)
- cell mode = most frequent 4dp sum among valid; MODE-MATCH tie-inclusive
- cell < 3 valid -> UNSCOREABLE
- P-GM1: MODE-MATCH >= 5 of scoreable cells (>= 5 scoreable required)
- P-GM2: pooled on-prediction (|sum - pred| <= 0.002) >= 30% of valid
- P-GM3: >= half of on-prediction samples have exactly two distinct radii
  (1/(2k) and (sqrt2-1)/(2k), each within 1e-3)
- FALSIFIER: MODE-MATCH fails in >= 4 scoreable cells (tie-inclusive)
"""
import json, math
from collections import Counter
from pathlib import Path
from arm_f_repro import parse_packing, validate, score

HERE = Path(__file__).parent
PRED = {13: 1.625, 17: 2.0517767, 21: 2.1, 31: 2.5833333,
        35: 2.9166667, 37: 3.0345178, 43: 3.0714286}
KSTAR = {n: round(math.sqrt(n)) for n in PRED}

raw = json.loads((HERE / "arm_gm2_raw.json").read_text())
rows_out = []
cells = {}
for r in raw["rows"]:
    n = r["n"]
    resp = r["response"]
    text = ""
    if "candidates" in resp:
        try:
            text = resp["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            text = ""
    circles, parse_reason = parse_packing(text if text else None)
    # guard malformed parses (e.g. rows containing None / wrong arity):
    # treat as unparsed, same standard as every other arm
    if circles is not None:
        try:
            ok_shape = all(c is not None and len(c) == 3
                           and all(isinstance(v, (int, float)) for v in c)
                           for c in circles)
        except TypeError:
            ok_shape = False
        if not ok_shape:
            circles = None
    valid6 = circles is not None and validate(circles, n, tol=1e-6)[0]
    valid3 = circles is not None and validate(circles, n, tol=1e-3)[0]
    s = score(circles) if circles else None
    s4 = round(s, 4) if s is not None else None
    onp = s is not None and valid6 and abs(s - PRED[n]) <= 0.002
    # structural signature: exactly two distinct radii = grid + filler
    sig = False
    if onp:
        k = KSTAR[n]
        rg, rf = 1 / (2 * k), (math.sqrt(2) - 1) / (2 * k)
        radii = sorted({round(c[2], 6) for c in circles})
        groups = []
        for rad in radii:
            for g in groups:
                if abs(g - rad) <= 1e-3:
                    break
            else:
                groups.append(rad)
        sig = (len(groups) == 2
               and any(abs(g - rg) <= 1e-3 for g in groups)
               and any(abs(g - rf) <= 1e-3 for g in groups))
    rows_out.append({"n": n, "sample_idx": r["sample_idx"],
                     "prompt_sha256": r["prompt_sha256"], "ts": r["ts"],
                     "transport_error": resp.get("transport_error"),
                     "model_version": resp.get("modelVersion"),
                     "response_id": resp.get("responseId"),
                     "parsed": bool(circles), "valid_1e6": valid6,
                     "valid_1e3": valid3, "sum": s, "sum_4dp": s4,
                     "on_prediction": onp, "two_radii_signature": sig,
                     "raw_text": text})
    cells.setdefault(n, []).append((valid6, s4, onp, sig))

with (HERE / "arm_gm2_candidates.jsonl").open("w") as f:
    for row in rows_out:
        f.write(json.dumps(row) + "\n")

report = {"prereg_commit": "3019aab", "model": raw["model"], "cells": [],
          "definitions": "tie-inclusive MODE-MATCH; <3 valid = UNSCOREABLE"}
matches, scoreable, onp_total, valid_total, sig_yes, onp_n = 0, 0, 0, 0, 0, 0
for n in sorted(PRED):
    vals = [s4 for (v, s4, _, _) in cells.get(n, []) if v and s4 is not None]
    onp_c = sum(1 for (v, _, o, _) in cells.get(n, []) if o)
    sig_c = sum(1 for (v, _, o, g) in cells.get(n, []) if o and g)
    pred4 = round(PRED[n], 4)
    cell = {"n": n, "predicted_4dp": pred4, "valid_n": len(vals),
            "on_pred": onp_c, "sig_two_radii": sig_c}
    if len(vals) < 3:
        cell["status"] = "UNSCOREABLE"
    else:
        scoreable += 1
        cnt = Counter(vals)
        top = max(cnt.values())
        modes = sorted([v for v, c in cnt.items() if c == top])
        match = pred4 in modes
        matches += match
        cell.update({"modes_4dp": modes, "mode_freq": f"{top}/{len(vals)}",
                     "MODE_MATCH": match,
                     "top3": cnt.most_common(3)})
    onp_total += onp_c
    valid_total += len(vals)
    sig_yes += sig_c
    onp_n += onp_c
    report["cells"].append(cell)

report["summary"] = {
    "scoreable_cells": scoreable, "mode_matches": matches,
    "P_GM1_mode_match_ge5": (scoreable >= 5) and (matches >= 5),
    "P_GM1_underpowered": scoreable < 5,
    "pooled_valid": valid_total, "pooled_on_pred": onp_total,
    "P_GM2_rate": round(onp_total / valid_total, 4) if valid_total else None,
    "P_GM2_ge_30pct": valid_total > 0 and onp_total / valid_total >= 0.30,
    "P_GM3_sig_frac": f"{sig_yes}/{onp_n}",
    "P_GM3_ge_half": onp_n > 0 and sig_yes >= onp_n / 2,
    "FALSIFIER_triggered": scoreable >= 5 and (scoreable - matches) >= 4,
}
(HERE / "arm_gm2_report.json").write_text(json.dumps(report, indent=1))
print(json.dumps(report["summary"], indent=1))
for c in report["cells"]:
    print(c["n"], c.get("status", ""), "match=" + str(c.get("MODE_MATCH")),
          "modes=" + str(c.get("modes_4dp")), f"valid={c['valid_n']}",
          f"onpred={c['on_pred']}")
