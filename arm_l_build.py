# Arm L (iterated loop probe) — template hashes and cell table.
# Registered in arm_l_preregistration.txt BEFORE sampling. Both templates are
# reused verbatim: generation 0 is bare A.1, generations 1..5 are arm MU's
# registered mutation template.
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
S2 = math.sqrt(2)

BARE = (
    "Pack exactly {n} non-overlapping circles inside the unit square [0,1]x[0,1] so that the sum of their radii is as large as possible.\n"
    "MUST hold: exactly {n} circles; every circle fully inside the unit square [0,1]x[0,1] (x-r >= 0, x+r <= 1, same for y); "
    "no two circles overlap (distance between centers >= sum of the two radii; touching is allowed).\n"
    "Do not write or execute code - construct the packing by reasoning alone.\n"
    "Output ONLY the raw Python list of {n} [x, y, r] lists. No explanation, no code fences, no other text."
)

# Arm MU's mutation tail, verbatim.
MUTATE_TAIL = (
    "\nHere is an existing packing of {n} circles scoring {score} (sum of radii):\n{parent}\n"
    "Propose a modification of this packing that increases the sum of radii. "
    "Output ONLY the raw Python list of the modified packing, nothing else."
)

WRAPPER = "Do not use any tools. Your entire final message must be the answer and nothing else."

CELLS = {13: {"k_star": 4, "predicted": 1.6250000, "family_argmax": 1.7761424},
         31: {"k_star": 6, "predicted": 2.5833333, "family_argmax": 2.7485281}}
REGIMES = {"greedy": 1, "diverse": 5}
POP = 5
GENERATIONS = 5  # plus generation 0


def lineages():
    return [f"{n}-{r}" for n in sorted(CELLS) for r in REGIMES]


def main():
    out = {"cells": {}, "templates": {}, "regimes": REGIMES, "pop": POP,
           "generations": GENERATIONS, "lineages": lineages(), "wrapper": WRAPPER}
    for n, meta in CELLS.items():
        bare = BARE.format(n=n)
        out["cells"][str(n)] = dict(meta, n=n, gen0_prompt=bare,
                                    gen0_sha256=hashlib.sha256(bare.encode("utf-8")).hexdigest())
        print(f"N={n:>2} gen0 hash {out['cells'][str(n)]['gen0_sha256'][:10]}... "
              f"pred {meta['predicted']} argmax {meta['family_argmax']}")
    tail = MUTATE_TAIL
    out["templates"]["mutation_tail"] = tail
    out["templates"]["mutation_tail_sha256"] = hashlib.sha256(tail.encode("utf-8")).hexdigest()
    print(f"mutation tail hash {out['templates']['mutation_tail_sha256'][:10]}...")
    (ROOT / "arm_l_prompts.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("written arm_l_prompts.json; lineages:", ", ".join(lineages()))


if __name__ == "__main__":
    main()
