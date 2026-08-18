# ============================================================================
# GM parse-path POSITIVE CONTROL (post-hoc diagnostic, disclosed; prompted by
# council review 2026-08-05). Question: can the GM scoring path (a) accept a
# well-formed packing as VALID, and (b) record each malformed-response class
# as a parse/validity failure rather than crashing or silently dropping?
# If (a) fails, the 0/140 GM2 outcome is uninterpretable (harness bug).
# Deterministic, no network. Run: python diagnostics_gm_parse_control.py
# ============================================================================
import json
import math
from pathlib import Path

from arm_f_repro import parse_packing, validate, score

HERE = Path(__file__).parent
S2 = math.sqrt(2)


def grid_t(k, n):
    """Well-formed T(k,n): k x k lattice truncated to n cells, r = 1/(2k)."""
    r = 1 / (2 * k)
    cells = [(x, y) for y in range(k) for x in range(k)][:n]
    return [[(2 * x + 1) * r, (2 * y + 1) * r, r] for x, y in cells]


CASES = [
    ("valid_T413", json.dumps(grid_t(4, 13)), 13, "VALID"),
    ("valid_fenced", "```python\n" + json.dumps(grid_t(4, 13)) + "\n```", 13, "VALID"),
    ("prose_only", "I think a grid works best. Let me reason step by step...", 13, "PARSE_FAIL"),
    ("truncated_list", json.dumps(grid_t(4, 13))[:-25], 13, "PARSE_FAIL"),
    ("empty_text", "", 13, "PARSE_FAIL"),
    ("wrong_count", json.dumps(grid_t(4, 12)), 13, "INVALID_GEOM"),
    ("overlap", json.dumps([[0.5, 0.5, 0.3], [0.6, 0.5, 0.3]] + grid_t(4, 13)[:11]), 13, "INVALID_GEOM"),
]


def classify(text, n):
    circles, reason = parse_packing(text if text else None)
    if circles is None:
        return "PARSE_FAIL", None
    ok, why = validate(circles, n, tol=1e-6)
    return ("VALID" if ok else "INVALID_GEOM"), score(circles)


def main():
    print("| case | expected | observed | sum |")
    fails = 0
    for name, text, n, expected in CASES:
        try:
            obs, s = classify(text, n)
        except Exception as e:  # a crash IS a control failure
            obs, s = f"CRASH:{type(e).__name__}", None
        ok = obs == expected
        fails += 0 if ok else 1
        print(f"| {name} | {expected} | {obs} | {s} | {'ok' if ok else '** FAIL **'}")

    # Real GM2 rows: confirm the registered failure signature (finishReason)
    raw = json.loads((HERE / "arm_gm2_raw.json").read_text())
    from collections import Counter
    fr = Counter()
    empty_text = 0
    for r in raw["rows"]:
        resp = r["response"]
        cand = (resp.get("candidates") or [{}])[0]
        fr[cand.get("finishReason", "NONE")] += 1
        try:
            t = cand["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            t = ""
        if not t.strip():
            empty_text += 1
    print(f"GM2 finishReason distribution: {dict(fr)}; empty-text rows: {empty_text}/{len(raw['rows'])}")
    print(f"CONTROL {'PASSED' if fails == 0 else 'FAILED'} ({len(CASES)-fails}/{len(CASES)} cases)")


if __name__ == "__main__":
    main()
