# ============================================================================
# POST-HOC DIAGNOSTIC — not preregistered. Prompted by external review 4
# (2026-08-04), deduction 8: "on-prediction" is scored as a value match within
# 2e-3; verify the *structural* claim by backing the grid order k out of each
# emitted layout and comparing with k*(N). Reads arm_f_candidates_v2.jsonl
# only; deterministic; no network.
# ============================================================================
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PRED = {13: 1.6250000, 17: 2.0517767, 21: 2.1000000, 31: 2.5833333,
        35: 2.9166667, 37: 3.0345178, 43: 3.0714286}
KSTAR = {13: 4, 17: 4, 21: 5, 31: 6, 35: 6, 37: 6, 43: 7}
WINDOW = 2e-3  # registered value-match window


def dominant_k(circles):
    """Back out the grid order from the most common radius: r_main = 1/(2k)."""
    radii = [round(c[2], 6) for c in circles]
    r_dom, _ = Counter(radii).most_common(1)[0]
    if r_dom <= 0:
        return None
    return round(1.0 / (2.0 * r_dom))


def main():
    rows = [json.loads(l) for l in
            (ROOT / "arm_f_candidates_v2.jsonl").read_text(encoding="utf-8").splitlines()
            if l.strip()]
    bare = [r for r in rows if r.get("arm") == "bare" and r.get("n") in PRED]

    print(f"square bare rows: {len(bare)}")
    print("| N | valid | on-pred (value) | k-match among on-pred | k-match among ALL valid |")
    tot_v = tot_op = tot_km_op = tot_km_v = 0
    for n in sorted(PRED):
        cell = [r for r in bare if r["n"] == n]
        valid = [r for r in cell if r.get("valid")]
        onpred = [r for r in valid if abs(r.get("sum_of_radii", 0) - PRED[n]) < WINDOW]
        km_op = [r for r in onpred if r.get("circles") and dominant_k(r["circles"]) == KSTAR[n]]
        km_v = [r for r in valid if r.get("circles") and dominant_k(r["circles"]) == KSTAR[n]]
        print(f"| {n} | {len(valid)} | {len(onpred)} | {len(km_op)}/{len(onpred)} | "
              f"{len(km_v)}/{len(valid)} |")
        tot_v += len(valid); tot_op += len(onpred)
        tot_km_op += len(km_op); tot_km_v += len(km_v)
    print(f"| pooled | {tot_v} | {tot_op} | {tot_km_op}/{tot_op} | {tot_km_v}/{tot_v} |")

    # off-prediction samples whose structure still matches k* (value miss, k hit)
    for n in sorted(PRED):
        cell = [r for r in bare if r["n"] == n and r.get("valid")]
        offp = [r for r in cell if abs(r.get("sum_of_radii", 0) - PRED[n]) >= WINDOW]
        hits = [(r.get("sample_id"), round(r.get("sum_of_radii", 0), 7))
                for r in offp if r.get("circles") and dominant_k(r["circles"]) == KSTAR[n]]
        if hits:
            print(f"off-prediction but k-matched at N={n}: {hits}")


if __name__ == "__main__":
    main()
