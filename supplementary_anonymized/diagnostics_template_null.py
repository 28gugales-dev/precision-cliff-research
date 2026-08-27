# Post-hoc diagnostic (disclosed): uniform-template null for the square
# discriminating cells. A proposer choosing uniformly among the plausible
# template shapes -- one branch value per grid order k in {k*-1, k*, k*+1} --
# lands on-prediction 1/3 of the time. This script counts, per discriminating
# cell of the bare weak-tier square arm, valid rows (1e-6) matching the
# registered prediction within the registered 2e-3 window, and reports the
# exact binomial upper tail against p0 = 1/3. Reuses arm_f_repro.py's
# parse/validate verbatim; no new instrument, no new tolerance.
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arm_f_repro as A

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "arm_f_candidates_v2.jsonl"

SQRT2 = math.sqrt(2.0)


def V(k, m):
    return k / 2.0 + m * (SQRT2 - 1.0) / (2.0 * k)


def T(k, n):
    return n / (2.0 * k)


def branch_value(k, n):
    # The family's branch rule at order k: extend with fillers when k^2 <= n,
    # truncate when k^2 > n.
    if k * k <= n:
        return V(k, n - k * k)
    return T(k, n)


def binom_upper_tail(n, x, p):
    return sum(math.comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(x, n + 1))


def main():
    rows = [json.loads(l) for l in LEDGER.read_text(encoding="utf-8").splitlines() if l.strip()]
    bare = [r for r in rows if r.get("arm") == "bare"]
    ns = sorted({r["n"] for r in bare})
    print(f"{len(bare)} bare rows across N = {ns}")
    print("null: uniform choice over one branch value per order k in {k*-1, k*, k*+1} -> p0 = 1/3\n")
    p0 = 1.0 / 3.0
    for n in ns:
        kstar = round(math.sqrt(n))
        pred = branch_value(kstar, n)
        cands = sorted({round(branch_value(k, n), 7) for k in (kstar - 1, kstar, kstar + 1)})
        argmax = max(branch_value(k, n) for k in (kstar - 1, kstar, kstar + 1))
        # Discriminating in the paper's operational sense: prediction and family
        # argmax must be separable by the registered 2e-3 value-matching window
        # (N = 17's 5e-4 gap is not; see S5 on the window's limits).
        discriminating = abs(pred - argmax) > 2e-3
        sub = [r for r in bare if r["n"] == n]
        valid = []
        for r in sub:
            circles, err = A.parse_packing(r.get("raw_output"))
            if circles is None:
                continue
            ok, why = A.validate(circles, n, tol=1e-6)
            if ok:
                valid.append(sum(c[2] for c in circles))
        hits = sum(abs(s - pred) < 2e-3 for s in valid)
        tail = binom_upper_tail(len(valid), hits, p0) if valid else float("nan")
        tag = "DISCRIMINATING" if discriminating else "non-discriminating (pred = family argmax)"
        print(f"N={n:>2} k*={kstar} pred {pred:.7f} candidates {cands} [{tag}]")
        print(f"      on-pred {hits}/{len(valid)} valid; exact binomial upper tail vs 1/3: "
              f"{tail:.3g}" if valid else "      no valid rows")
    print("\nPost hoc throughout; the registered analyses are unchanged.")


if __name__ == "__main__":
    main()
