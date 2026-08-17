# ============================================================================
# Arm G provenance ledger. Reads arm_g_candidates.jsonl (already reconstructed
# with rect_forecast validators) and emits arm_g_ledger_with_hashes.jsonl with
# the provenance columns the square arm carries in arm_f_prompts.json.
#
# Honest columns only. The rect prompt text was never pinned on disk anywhere
# (no arm_g_prompts.json analogue exists; the template lives only inside the
# agent handoff that generated arm_g_rect.py). Therefore prompt_sha256 is
# recorded as "unrecoverable" rather than invented by hashing a guessed
# reconstruction. Everything else is filled from the source ledger.
# ============================================================================
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "arm_g_candidates.jsonl"
OUT = ROOT / "arm_g_ledger_with_hashes.jsonl"

HEADER = {
    "ledger": "arm_g_rect",
    "rule": "registered in arm_g_rect.py header before any proposal was sampled",
    "cells": {
        "(19, 3.0)": {"predicted": 3.1666667, "pred_shape": "8x3 truncate",
                      "rival": 3.5749194, "rival_shape": "7x2 extend"},
        "(25, 2.0)": {"predicted": 3.1250000, "pred_shape": "7x4 truncate",
                      "rival": 3.4832492, "rival_shape": "6x3 extend"},
    },
    "prompt_status": "prompt text not recoverable from released artifacts; "
                     "no pinned prompt file exists for the rectangle arm",
}


def row_digest(r):
    seed = json.dumps(r, sort_keys=True)
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()


def main():
    rows = [json.loads(line) for line in SRC.open(encoding="utf-8") if line.strip()]

    out = []
    for r in rows:
        ledger = {
            "n": r["n"],
            "a": r["a"],
            "sample_id": r["sample_id"],
            "valid": r["valid"],
            "parse_error": r.get("parse_error"),
            "invalid_reason": r.get("invalid_reason"),
            "sum_of_radii": r.get("sum_of_radii"),
            "layout": (None if not r["valid"] else
                       {"cols": r["cols"], "rows": r["rows"],
                        "distinct_radii": r["distinct_radii"],
                        "max_radius": r["max_radius"]}),
            "prompt_sha256": "unrecoverable",
            "proposer": "unattested",
            "row_digest_sha256": row_digest(r),
        }
        out.append(ledger)

    with OUT.open("w", encoding="utf-8") as fh:
        fh.write(json.dumps(HEADER) + "\n")
        for r in out:
            fh.write(json.dumps(r) + "\n")

    print(f"{len(out)} arm_g rows written to {OUT.name} (header + rows)")
    for (n, a) in sorted({(r["n"], r["a"]) for r in out}):
        sub = [r for r in out if r["n"] == n and round(r["a"], 6) == a]
        valid = [r for r in sub if r["valid"]]
        print(f"N={n} a={a}: {len(sub)} rows, {len(valid)} valid, "
              f"prompt_sha256={sub[0]['prompt_sha256']}")


if __name__ == "__main__":
    main()