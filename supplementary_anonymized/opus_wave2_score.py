# Opus-alias replication wave 2 (post-hoc, NOT preregistered).
# Collected 2026-08-10 via Claude Code agent runtime, model alias "opus",
# same bare prompts as arm O (prompt SHAs verified against arm_f ledger).
# Scores opus_wave2_raw.json with the paper's parser/validator
# (copied verbatim from arm_f_repro.py) and writes opus_wave2_ledger.jsonl.
import ast
import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PROMPT_TEMPLATE = (
    "Pack exactly {n} non-overlapping circles inside the unit square [0,1]x[0,1] "
    "so that the sum of their radii is as large as possible.\n"
    "MUST hold: exactly {n} circles; every circle fully inside the unit square "
    "[0,1]x[0,1] (x-r >= 0, x+r <= 1, same for y); no two circles overlap "
    "(distance between centers >= sum of the two radii; touching is allowed).\n"
    "Do not write or execute code - construct the packing by reasoning alone.\n"
    "Output ONLY the raw Python list of {n} [x, y, r] lists. No explanation, "
    "no code fences, no other text."
)


def parse_packing(raw):
    if raw is None:
        return None, "no_output"
    text = re.sub(r"```[a-zA-Z]*", "", raw).replace("```", "")
    start, end = text.find("["), text.rfind("]")
    if start < 0 or end <= start:
        return None, "no_bracketed_list"
    try:
        val = ast.literal_eval(text[start:end + 1])
    except Exception as exc:
        return None, f"literal_eval_failed:{type(exc).__name__}"
    if not isinstance(val, (list, tuple)):
        return None, "not_a_list"
    out = []
    for row in val:
        if not isinstance(row, (list, tuple)) or len(row) != 3:
            return None, "row_not_xyr"
        try:
            out.append(tuple(float(v) for v in row))
        except (TypeError, ValueError):
            return None, "row_not_numeric"
    return out, None


def validate(circles, n, tol=1e-6):
    if len(circles) != n:
        return False, f"count_{len(circles)}_expected_{n}"
    for x, y, r in circles:
        if r <= 0:
            return False, "nonpositive_radius"
        if x - r < -tol or x + r > 1 + tol or y - r < -tol or y + r > 1 + tol:
            return False, "outside_square"
    for i in range(len(circles)):
        xi, yi, ri = circles[i]
        for j in range(i + 1, len(circles)):
            xj, yj, rj = circles[j]
            if math.hypot(xi - xj, yi - yj) < ri + rj - tol:
                return False, "overlap"
    return True, None


def main():
    raw = json.loads((ROOT / "opus_wave2_raw.json").read_text(encoding="utf-8"))
    rows = []
    for rec in raw["samples"]:
        n = rec["n"]
        circles, perr = parse_packing(rec["raw_output"])
        row = {
            "arm": "opus_alias_wave2",
            "n": n,
            "sample_id": rec["sample_id"],
            "run_date": raw["run_date"],
            "prompt_sha256": hashlib.sha256(
                PROMPT_TEMPLATE.format(n=n).encode("utf-8")).hexdigest(),
            "raw_output": rec["raw_output"],
            "raw_len": len(rec["raw_output"] or ""),
            "parse_error": perr,
            "circles": circles,
        }
        if circles is None:
            row.update(valid=False, valid_strict_1e9=False,
                       invalid_reason=perr, invalid_reason_strict_1e9=perr,
                       sum_of_radii=None)
        else:
            v6, why6 = validate(circles, n, tol=1e-6)
            v9, why9 = validate(circles, n, tol=1e-9)
            row.update(valid=v6, valid_strict_1e9=v9,
                       invalid_reason=why6, invalid_reason_strict_1e9=why9,
                       sum_of_radii=sum(r for _, _, r in circles))
        rows.append(row)

    with (ROOT / "opus_wave2_ledger.jsonl").open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")

    for n in (13, 21, 31):
        cell = [r for r in rows if r["n"] == n]
        v6 = sum(r["valid"] for r in cell)
        v9 = sum(r["valid_strict_1e9"] for r in cell)
        scores = sorted(r["sum_of_radii"] for r in cell if r["valid"])
        print(f"N={n}: {v6}/{len(cell)} valid @1e-6, {v9}/{len(cell)} @1e-9, "
              f"valid scores {['%.4f' % s for s in scores]}")
        for r in cell:
            if not r["valid"]:
                print(f"  {r['sample_id']}: {r['invalid_reason']}")
    tot6 = sum(r["valid"] for r in rows)
    tot9 = sum(r["valid_strict_1e9"] for r in rows)
    print(f"POOLED: {tot6}/{len(rows)} @1e-6 ({100*tot6//len(rows)}%), "
          f"{tot9}/{len(rows)} @1e-9. Wave 1 was 4/30 (13%) both tolerances.")


if __name__ == "__main__":
    main()
