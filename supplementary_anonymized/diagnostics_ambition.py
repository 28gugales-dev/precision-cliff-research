# ============================================================================
# POST-HOC DIAGNOSTIC — not preregistered. Prompted by external review 7
# (2026-08-04), deduction 2: "ambition" is asserted but unmeasured. Two
# operationalizations computable from every emitted geometry (valid or not):
#   (a) distinct radius count per sample (rounded to 1e-4)
#   (b) off-lattice fraction: share of circles whose center does not sit on
#       the k-grid lattice implied by the sample's dominant radius
# Reads arm_f_candidates_v2.jsonl only; deterministic; no network.
# ============================================================================
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CELLS = {13, 21, 31}  # matched tier-ladder cells


def stats(circles):
    radii = [round(c[2], 4) for c in circles]
    distinct = len(set(radii))
    r_dom, _ = Counter(radii).most_common(1)[0]
    if r_dom <= 0:
        return distinct, None
    k = round(1.0 / (2.0 * r_dom))
    if k <= 0:
        return distinct, None
    # lattice positions for a k-grid: centers at (2i+1)/(2k)
    tol = 1e-3
    def on_lattice(v):
        return any(abs(v - (2 * i + 1) / (2 * k)) < tol for i in range(k))
    off = sum(1 for x, y, r in circles if not (on_lattice(x) and on_lattice(y)))
    return distinct, off / len(circles)


def main():
    rows = [json.loads(l) for l in
            (ROOT / "arm_f_candidates_v2.jsonl").read_text(encoding="utf-8").splitlines()
            if l.strip()]
    arms = {"bare": "weak", "sonnet_bare": "middle", "opus_alias": "top"}
    print("| tier | n w/ geometry | median distinct radii | mean distinct | median off-lattice frac |")
    for arm, tier in arms.items():
        sel = [r for r in rows if r.get("arm") == arm and r.get("n") in CELLS
               and r.get("circles")]
        ds, offs = [], []
        for r in sel:
            d, o = stats(r["circles"])
            ds.append(d)
            if o is not None:
                offs.append(o)
        ds.sort(); offs.sort()
        med = lambda v: v[len(v) // 2] if v else None
        print(f"| {tier} ({arm}) | {len(sel)} | {med(ds)} | {sum(ds)/len(ds):.2f} | "
              f"{med(offs):.2f} |")


if __name__ == "__main__":
    main()
