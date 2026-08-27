# ============================================================================
# Arm CP (perturbed-container probe) — prompt builder and closed-form table.
# Registered in arm_cp_preregistration.txt BEFORE sampling.
#
# Container [3,5]x[3,5]: under x -> 2x + 3 every unit-square packing maps to a
# valid packing with radii doubled, so predictions are 2*V/2*T and the family
# structure is invariant. Prompts are template A.1 with exactly the two
# registered substitutions. SHA-256 per cell written to arm_cp_prompts.json.
# Self-check: reproduces the registration's N=13 and N=58 mapped values.
# ============================================================================
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
S2 = math.sqrt(2)
CELLS = [13, 21, 31, 58, 75]

TEMPLATE = (
    "Pack exactly {n} non-overlapping circles inside the square [3,5]x[3,5] so that the sum of their radii is as large as possible.\n"
    "MUST hold: exactly {n} circles; every circle fully inside the square [3,5]x[3,5] (x-r >= 3, x+r <= 5, same for y); "
    "no two circles overlap (distance between centers >= sum of the two radii; touching is allowed).\n"
    "Do not write or execute code - construct the packing by reasoning alone.\n"
    "Output ONLY the raw Python list of {n} [x, y, r] lists. No explanation, no code fences, no other text."
)

WRAPPER = "Do not use any tools. Your entire final message must be the answer and nothing else."


def V(k, m):
    return k / 2 + m * (S2 - 1) / (2 * k)


def T(k, n):
    return n / (2 * k)


def family(n):
    out = {}
    for k in range(1, int(math.isqrt(n)) + 3):
        if n < k * k:
            out[k] = (T(k, n), "T", None)
        elif n - k * k <= (k - 1) ** 2:
            out[k] = (V(k, n - k * k), "V", n - k * k)
    return out


def prediction(n):
    k = round(math.sqrt(n))
    if k * k <= n:
        return V(k, n - k * k), "V", k
    return T(k, n), "T", k


def rival(n):
    k = round(math.sqrt(n))
    fam = family(n)
    best_k, (best_v, br, m) = max(fam.items(), key=lambda kv: kv[1][0])
    return best_v, best_k


def main():
    # Self-check against the registration's stated mapped values.
    assert abs(2 * prediction(13)[0] - 3.2500000) < 1e-7
    assert abs(2 * prediction(58)[0] - 7.2500000) < 1e-7
    assert abs(2 * rival(13)[0] - 2 * 1.7761424) < 1e-6
    out = {}
    for n in CELLS:
        pred, branch, k = prediction(n)
        rv, rk = rival(n)
        prompt = TEMPLATE.format(n=n)
        out[str(n)] = {
            "n": n,
            "k_star": k,
            "branch": branch,
            "predicted_unit": round(pred, 7),
            "predicted_mapped": round(2 * pred, 7),
            "rival_unit": round(rv, 7),
            "rival_mapped": round(2 * rv, 7),
            "rival_k": rk,
            "discriminating": abs(pred - rv) > 2e-3,
            "prompt": prompt,
            "wrapper": WRAPPER,
            "sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        }
        print(f"N={n:>2} k*={k} {branch} pred {2*pred:.7f} rival {2*rv:.7f} "
              f"disc={out[str(n)]['discriminating']} hash {out[str(n)]['sha256'][:10]}...")
    (ROOT / "arm_cp_prompts.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("written arm_cp_prompts.json")


if __name__ == "__main__":
    main()
