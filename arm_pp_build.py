# Arm PP (paraphrase probe) — fixed paraphrase strings and hashes.
# Registered in arm_pp_preregistration.txt BEFORE sampling.
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PP_A = (
    "Place exactly {n} circles inside the unit square [0,1]x[0,1], none of them overlapping, "
    "choosing positions and sizes so the total of all radii is as large as you can make it. "
    "Every circle must lie entirely within the square, so its center must be at least its radius "
    "away from each side (x-r >= 0, x+r <= 1, and the same for y), and the distance between any "
    "two centers must be at least the sum of their radii (touching permitted). Work this out by "
    "reasoning alone - writing or running code is not allowed. Reply with ONLY the raw Python "
    "list of {n} [x, y, r] lists: no explanation, no code fences, nothing else."
)

PP_B = (
    "Your task is a circle-packing construction. You are given the unit square [0,1]x[0,1] and "
    "must produce exactly {n} circles whose radii add up to the largest total you can achieve.\n"
    "Requirements:\n"
    "1. Exactly {n} circles.\n"
    "2. Each circle fully inside the square: x-r >= 0, x+r <= 1, y-r >= 0, y+r <= 1.\n"
    "3. No pair of circles overlaps: center distance >= sum of the two radii; contact is allowed.\n"
    "4. No code may be written or executed - the construction must come from reasoning alone.\n"
    "Your entire reply must be the raw Python list of {n} [x, y, r] lists, with no explanation, "
    "no code fences, and no other text."
)

PP_C = (
    "Maximize the sum of radii of {n} circles in the unit square [0,1]x[0,1], subject to "
    "containment (each center at least its radius from every side) and pairwise non-overlap "
    "(inter-center distance at least the sum of the corresponding radii; tangency allowed), with "
    "exactly {n} circles. Solve by reasoning alone, without writing or executing code. Output "
    "ONLY the raw Python list of {n} [x, y, r] lists - no explanation, no code fences, no other "
    "text."
)

CELLS = [13, 31]
PREDICTIONS = {13: 1.6250000, 31: 2.5833333}
RIVALS = {13: 1.7761424, 31: 2.7485281}


def main():
    out = {}
    for tag, tpl in (("A", PP_A), ("B", PP_B), ("C", PP_C)):
        for n in CELLS:
            prompt = tpl.format(n=n)
            key = f"{tag}:{n}"
            out[key] = {
                "paraphrase": tag, "n": n,
                "predicted": PREDICTIONS[n], "rival": RIVALS[n],
                "prompt": prompt,
                "sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
            }
            print(f"PP-{tag} N={n:>2} hash {out[key]['sha256'][:10]}...")
    (ROOT / "arm_pp_prompts.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("written arm_pp_prompts.json")


if __name__ == "__main__":
    main()
