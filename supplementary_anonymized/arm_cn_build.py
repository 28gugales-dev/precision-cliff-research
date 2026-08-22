# ============================================================================
# Arm CN (contamination / held-out-N probe) — prompt builder and closed-form
# table. Registered in arm_cn_preregistration.txt BEFORE sampling.
#
# Bare template A.1 verbatim (byte-identical to arm F / arm M instances apart
# from the substituted N), SHA-256 per cell, and the registered predictions:
#   k* = round(sqrt(N))
#   V(k, m) = k/2 + m (sqrt2 - 1) / (2k)      for N = k^2 + m, 0 <= m <= (k-1)^2
#   T(k, N) = N / (2k)                        for N < k^2
# Family argmax = max over every k whose member is defined at N. A cell is
# "discriminating" when the registered prediction is not the family argmax.
# Self-check: reproduces arm M's registered values at N = 20 and N = 57.
# ============================================================================
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
S2 = math.sqrt(2)
CELLS = [50, 58, 62, 65, 75]

TEMPLATE = (
    "Pack exactly {n} non-overlapping circles inside the unit square [0,1]x[0,1] so that the sum of their radii is as large as possible.\n"
    "MUST hold: exactly {n} circles; every circle fully inside the unit square [0,1]x[0,1] (x-r >= 0, x+r <= 1, same for y); "
    "no two circles overlap (distance between centers >= sum of the two radii; touching is allowed).\n"
    "Do not write or execute code - construct the packing by reasoning alone.\n"
    "Output ONLY the raw Python list of {n} [x, y, r] lists. No explanation, no code fences, no other text."
)


def V(k, m):
    return k / 2 + m * (S2 - 1) / (2 * k)


def T(k, n):
    return n / (2 * k)


def family(n):
    """Every family member defined at N: {k: (value, branch, m)}."""
    out = {}
    for k in range(1, int(math.isqrt(n)) + 3):
        if n < k * k:
            out[k] = (T(k, n), "T", None)
        elif n - k * k <= (k - 1) ** 2:
            out[k] = (V(k, n - k * k), "V", n - k * k)
    return out


def cell_table(n):
    ks = round(math.sqrt(n))
    fam = family(n)
    assert ks in fam, (n, ks, fam)
    pred, branch, m = fam[ks]
    k_arg = max(fam, key=lambda k: fam[k][0])
    argmax = fam[k_arg][0]
    return dict(N=n, kstar=ks, branch=branch, m=m, prediction=round(pred, 7),
                argmax_k=k_arg, argmax=round(argmax, 7),
                discriminating=abs(argmax - pred) > 1e-9,
                family={str(k): round(v[0], 7) for k, v in fam.items()})


if __name__ == "__main__":
    # self-check against arm M registration
    assert abs(cell_table(20)["prediction"] - 2.2071068) < 1e-6
    assert abs(cell_table(57)["prediction"] - 3.5625000) < 1e-6
    assert abs(cell_table(57)["argmax"] - 3.7366935) < 1e-6
    # self-check against the original square arm (N=13 anchor 1.6250000, rival 1.7761424)
    assert abs(cell_table(13)["prediction"] - 1.6250000) < 1e-6
    assert abs(cell_table(13)["argmax"] - 1.7761424) < 1e-6
    prompts = {}
    for n in CELLS:
        p = TEMPLATE.format(n=n)
        prompts[str(n)] = {"prompt": p, "sha256": hashlib.sha256(p.encode("utf-8")).hexdigest(),
                           **cell_table(n)}
    # arm M N=20 prompt hash must reproduce from the same template (byte-identity check)
    m20 = hashlib.sha256(TEMPLATE.format(n=20).encode("utf-8")).hexdigest()
    assert m20 == "7fb87eb5aa2d7a157339b282a7bc8cf89ef8165919eaf50a9ce1bab3c4de9729", m20
    (ROOT / "arm_cn_prompts.json").write_text(json.dumps(prompts, indent=2), encoding="utf-8")
    for n, v in prompts.items():
        print(f"N={n} k*={v['kstar']} {v['branch']} m={v['m']} pred={v['prediction']} "
              f"argmax={v['argmax']} (k={v['argmax_k']}) discriminating={v['discriminating']} sha={v['sha256'][:16]}")
