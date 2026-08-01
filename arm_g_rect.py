# ============================================================================
# Arm G: the rectangle probe. Turns rect_forecast.py from a prediction into a test.
#
# Registered before any proposal was sampled, taken verbatim from
# rect_forecast.py's two sharpest discriminating cells:
#
#   N=19, a=3  predict 3.1666667 as an 8x3 grid TRUNCATED to 19
#              rival   3.5749194 as a 7x2 grid EXTENDED with 5 fillers   (11.4%)
#   N=25, a=2  predict 3.1250000 as a 7x4 grid TRUNCATED to 25
#              rival   3.4832492 as a 6x3 grid EXTENDED with 7 fillers   (10.3%)
#
# The rival is the better construction in both cells. If the nearest-template
# anchoring found in the unit square is a general property rather than an
# artefact of the 1-parameter square case, proposers should land on the
# PREDICTED value and not on the rival - in a container they have never been
# tested in, under a rule that was never fitted to rectangle data.
# ============================================================================
import ast
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rect_forecast as R

ROOT = Path(__file__).resolve().parent
LABEL_RE = re.compile(r'<summary>Agent "R(\d+)a(\d+) s(\d+)" finished</summary>')
RESULT_RE = re.compile(r"<result>(.*?)</result>", re.S)

CELLS = {
    (19, 3.0): {"predicted": 3.1666667, "pred_shape": "8x3 truncate",
                "rival": 3.5749194, "rival_shape": "7x2 extend"},
    (25, 2.0): {"predicted": 3.1250000, "pred_shape": "7x4 truncate",
                "rival": 3.4832492, "rival_shape": "6x3 extend"},
}


def parse_packing(raw):
    if raw is None:
        return None, "no_output"
    text = re.sub(r"```[a-zA-Z]*", "", raw).replace("```", "")
    s, e = text.find("["), text.rfind("]")
    if s < 0 or e <= s:
        return None, "no_bracketed_list"
    try:
        val = ast.literal_eval(text[s:e + 1])
    except Exception as exc:
        return None, f"literal_eval_failed:{type(exc).__name__}"
    out = []
    for row in val:
        if not isinstance(row, (list, tuple)) or len(row) != 3:
            return None, "row_not_xyr"
        try:
            out.append(tuple(float(v) for v in row))
        except (TypeError, ValueError):
            return None, "row_not_numeric"
    return out, None


def validate(circles, n, a, tol=1e-6):
    if len(circles) != n:
        return False, f"count_{len(circles)}_expected_{n}"
    for x, y, r in circles:
        if r <= 0:
            return False, "nonpositive_radius"
        if x - r < -tol or x + r > 1 + tol or y - r < -tol or y + r > a + tol:
            return False, "outside_rectangle"
    for i in range(len(circles)):
        xi, yi, ri = circles[i]
        for j in range(i + 1, len(circles)):
            xj, yj, rj = circles[j]
            if math.hypot(xi - xj, yi - yj) < ri + rj - tol:
                return False, "overlap"
    return True, None


def layout(circles, tol=1e-6):
    xs = sorted({round(x, 6) for x, _, _ in circles})
    ys = sorted({round(y, 6) for _, y, _ in circles})
    radii = sorted({round(r, 6) for _, _, r in circles})
    return {"cols": len(xs), "rows": len(ys), "distinct_radii": len(radii),
            "max_radius": radii[-1]}


def iter_text(obj):
    """Yield every string inside a transcript record, whatever its shape.

    Walking the decoded structure rather than json.dumps'ing it matters: the
    dumped form escapes the quotes in <summary>Agent "R19a3 s4"</summary> to \\",
    so the label regex silently matches nothing and the harvest reports zero
    invocations while the data is sitting right there.
    """
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from iter_text(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from iter_text(v)


def collect(transcripts):
    seen, out = set(), []
    for t in transcripts:
        with Path(t).open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                for blob in iter_text(rec):
                    if "<task-notification>" not in blob:
                        continue
                    m, res = LABEL_RE.search(blob), RESULT_RE.search(blob)
                    if not m or not res:
                        continue
                    n, a, sid = int(m.group(1)), float(m.group(2)), int(m.group(3))
                    if (n, a) not in CELLS or (n, a, sid) in seen:
                        continue
                    seen.add((n, a, sid))
                    out.append({"n": n, "a": a, "sample_id": sid,
                                "raw": res.group(1).strip()})
    return out


def main():
    samples = collect(sys.argv[1:])
    rows = []
    for s in samples:
        n, a = s["n"], s["a"]
        circles, err = parse_packing(s["raw"])
        row = {"reconstructed": False, "n": n, "a": a, "sample_id": s["sample_id"],
               "raw_output": s["raw"], "parse_error": err, "valid": False}
        if circles is not None:
            ok, why = validate(circles, n, a)
            row["valid"], row["invalid_reason"] = ok, why
            row["circles"] = circles
            if ok:
                row["sum_of_radii"] = sum(r for _, _, r in circles)
                row.update(layout(circles))
        rows.append(row)

    with (ROOT / "arm_g_candidates.jsonl").open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")

    print(f"{len(rows)} rectangle invocations, all rows written\n")
    for (n, a), c in CELLS.items():
        sub = [r for r in rows if r["n"] == n and r["a"] == a]
        if not sub:
            continue
        valid = [r for r in sub if r["valid"]]
        hit = [r for r in valid if abs(r["sum_of_radii"] - c["predicted"]) < 2e-3]
        riv = [r for r in valid if abs(r["sum_of_radii"] - c["rival"]) < 2e-3]
        best = max((r["sum_of_radii"] for r in valid), default=None)
        bad = {}
        for r in sub:
            if not r["valid"]:
                k = r["parse_error"] or r.get("invalid_reason")
                bad[k] = bad.get(k, 0) + 1
        print(f"N={n} a={a}:  predict {c['predicted']:.7f} ({c['pred_shape']})"
              f"   rival {c['rival']:.7f} ({c['rival_shape']})")
        print(f"   valid {len(valid)}/{len(sub)}   on-prediction {len(hit)}"
              f"   rival {len(riv)}   best observed "
              f"{best if best is None else round(best, 7)}"
              + (f"   failures {bad}" if bad else ""))
        shapes = {}
        for r in valid:
            k = f"{r['rows']}x{r['cols']}_r{r['distinct_radii']}"
            shapes[k] = shapes.get(k, 0) + 1
        print(f"   layouts (rows x cols, distinct radii): {shapes}\n")


if __name__ == "__main__":
    main()
