"""Arm GM analysis v2 — scores the completed GM ledger under the registered definitions.

Registered: arm_gm_preregistration.txt (commit 37b3adb) + arm_gm_amendment1_openrouter.md
(serving-path deviation for the 85 resumed cells; dual accounting required).

Differences from arm_gm2_analysis.py, all mechanical:
- assembles from arm_gm_checkpoint.jsonl (first content row per cell wins;
  transport-error rows are excluded from denominators per the prereg
  transport-rerun clause) and writes arm_gm_v2_raw.json
- text extraction gains a `choices` branch for the OpenAI-style shape
  OpenRouter returns; the Gemini `candidates` branch is unchanged
- report carries per-row serving_path/provider and BOTH accountings:
  mixed-path (all 140) and first-party-only (the 99 Google-endpoint rows)
Scoring logic, definitions, predictions, falsifier: byte-for-byte GM2's.
"""
import json, math
from collections import Counter
from pathlib import Path
from arm_f_repro import parse_packing, validate, score

HERE = Path(__file__).parent
PRED = {13: 1.625, 17: 2.0517767, 21: 2.1, 31: 2.5833333,
        35: 2.9166667, 37: 3.0345178, 43: 3.0714286}
KSTAR = {n: round(math.sqrt(n)) for n in PRED}

# --- assembly from checkpoint (single source of truth) ---
rows_by_cell = {}
for line in (HERE / "arm_gm_checkpoint.jsonl").read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    r = json.loads(line)
    if "transport_error" in r["response"]:
        continue
    key = (r["n"], r["sample_idx"])
    if key not in rows_by_cell:          # first content row per cell wins
        rows_by_cell[key] = r
rows = sorted(rows_by_cell.values(), key=lambda r: (r["n"], r["sample_idx"]))
(HERE / "arm_gm_v2_raw.json").write_text(json.dumps(
    {"model": "gemini-2.5-flash-lite", "prereg": "arm_gm_preregistration.txt (37b3adb)",
     "amendment": "arm_gm_amendment1_openrouter.md",
     "note": "assembled from arm_gm_checkpoint.jsonl; rows without a "
             "serving_path field came through generativelanguage.googleapis.com, "
             "rows with serving_path=openrouter through openrouter.ai (provider "
             "as logged per row)",
     "rows": rows}, indent=1))


def extract_text(resp):
    if "candidates" in resp:
        # Gemini can return multi-part content: thinking parts carry
        # thought=True, the answer is the first non-thought text part.
        # (GM2's 4096-budget rows died inside the thought part; GM3's 16384
        # budget lets the answer part appear. parts[0] alone grabs thinking.)
        try:
            parts = resp["candidates"][0]["content"]["parts"]
            for p in parts:
                if not p.get("thought") and p.get("text"):
                    return p["text"]
            return ""
        except (KeyError, IndexError, TypeError):
            return ""
    if "choices" in resp:
        try:
            return resp["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError, TypeError):
            return ""
    return ""


def score_rows(row_set):
    rows_out, cells = [], {}
    for r in row_set:
        n = r["n"]
        resp = r["response"]
        text = extract_text(resp)
        circles, _ = parse_packing(text if text else None)
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
                         "serving_path": r.get("serving_path", "google-first-party"),
                         "provider": resp.get("provider"),
                         "model_version": resp.get("modelVersion") or resp.get("model"),
                         "parsed": bool(circles), "valid_1e6": valid6,
                         "valid_1e3": valid3, "sum": s, "sum_4dp": s4,
                         "on_prediction": onp, "two_radii_signature": sig,
                         "raw_text": text})
        cells.setdefault(n, []).append((valid6, s4, onp, sig))
    return rows_out, cells


def summarize(cells):
    out_cells = []
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
                         "MODE_MATCH": match, "top3": cnt.most_common(3)})
        onp_total += onp_c
        valid_total += len(vals)
        sig_yes += sig_c
        onp_n += onp_c
        out_cells.append(cell)
    summary = {
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
    return out_cells, summary


rows_out, cells_mixed = score_rows(rows)
with (HERE / "arm_gm_v2_candidates.jsonl").open("w") as f:
    for row in rows_out:
        f.write(json.dumps(row) + "\n")

cells_out, summary_mixed = summarize(cells_mixed)
first_party = [r for r in rows if "serving_path" not in r]
_, cells_fp = score_rows(first_party)
_, summary_fp = summarize(cells_fp)

report = {
    "prereg": "arm_gm_preregistration.txt (37b3adb)",
    "amendment": "arm_gm_amendment1_openrouter.md",
    "model": "gemini-2.5-flash-lite",
    "definitions": "tie-inclusive MODE-MATCH; <3 valid = UNSCOREABLE",
    "row_count": {"total": len(rows),
                  "first_party": len(first_party),
                  "openrouter": len(rows) - len(first_party)},
    "openrouter_providers": sorted({r["response"].get("provider") for r in rows
                                    if r.get("serving_path") == "openrouter"
                                    and r["response"].get("provider")}),
    "cells": cells_out,
    "summary_mixed_path": summary_mixed,
    "summary_first_party_only": summary_fp,
}
(HERE / "arm_gm_v2_report.json").write_text(json.dumps(report, indent=1))
print("rows:", report["row_count"])
print("providers:", report["openrouter_providers"])
print("\nMIXED (registered evaluation set):")
print(json.dumps(summary_mixed, indent=1))
print("\nFIRST-PARTY-ONLY (disclosure accounting):")
print(json.dumps(summary_fp, indent=1))
for c in cells_out:
    print(c["n"], c.get("status", ""), "match=" + str(c.get("MODE_MATCH")),
          "modes=" + str(c.get("modes_4dp")), f"valid={c['valid_n']}",
          f"onpred={c['on_pred']}")
