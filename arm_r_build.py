"""
Arm R -- the repair probe section 4 names as this paper's follow-up, and the bare
re-snapshot that has to run alongside it.

WHY BOTH ARMS. Section 4 proposes handing the alias a fixed, known-valid packing and
asking it to find the broken tangencies. The model did not choose the construction, so
arithmetic execution is decoupled from constructive ambition, and that is the H1/H2
discriminator. But the arm cannot be run alone. The original `opus_alias` rows were
sampled on 2026-08-01; anything sampled now goes through the same alias, and the runtime
reports nothing about which weights served either call. Section 4's own C3 says that
gap is unattestable. So a repair result on its own has no anchor: a clean repair score
would be equally consistent with "repair is easy" and with "the alias resolves to
something else today". The bare re-snapshot -- the SAME byte-identical prompts that
produced 4/30 -- is what makes the repair number interpretable, and it is also the
dated re-snapshot section 4 lists as runnable-from-inside-the-runtime and never ran.

THE SUBSTRATE. Both repair cells use an exactly-tangent grid-plus-interstitial packing:
a k x k grid at r = 1/(2k) plus interstitial circles at r = (sqrt(2)-1)/(2k) dropped into
the interior holes. Every contact in that family is tangent to floating-point exactness,
so a packing perturbed by delta has NO other slack anywhere -- the injected violation is
the only violation, and the answer key is exact rather than approximate. That family is
also the one both comparator tiers actually produce (section 4), so the substrate is not
foreign to the task.

THE LADDER. Each cell is probed at delta = 1e-2, 1e-3, 1e-4. This is the part that
discriminates. H1 (a decode path that erodes arithmetic precision while leaving
construction choice intact) predicts detection degrades as delta shrinks, because
resolving a 1e-4 overlap is an arithmetic act and resolving a 1e-2 one is nearly a visual
one. H2 (a genuine tier property: harder constructions attempted, less reliably executed)
predicts NOTHING about a task with no construction in it -- the model is handed the
packing -- so H2's natural prediction is flat, high detection at every delta. A monotone
decline is evidence for H1 that the text channel cannot supply.

Run:  python arm_r_build.py            # writes arm_r_prompts.json + arm_r_key.json
"""
import hashlib
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT2 = math.sqrt(2.0)

CELLS = {13: 3, 31: 5}          # N -> grid side k
DELTAS = [1e-2, 1e-3, 1e-4]
REPS = 5


def base_packing(n, k):
    """k x k grid at r = 1/(2k), interstitials at (sqrt(2)-1)/(2k), first n total.

    Contacts are tangent by construction: grid neighbours are 1/k apart with radii
    summing to 1/k, and an interstitial sits at the hole centre a distance
    (sqrt(2)/2)/k from each of its four grid neighbours, which equals
    1/(2k) + (sqrt(2)-1)/(2k). Both hold exactly in exact arithmetic, so the only
    departure from tangency in what follows is the one this file injects.
    """
    r = 1.0 / (2 * k)
    circles = [(( 2 * i + 1) * r, (2 * j + 1) * r, r)
               for j in range(k) for i in range(k)]
    rf = (ROOT2 - 1.0) / (2 * k)
    holes = [((i + 1) / k, (j + 1) / k, rf)
             for j in range(k - 1) for i in range(k - 1)]
    out = (circles + holes)[:n]
    if len(out) != n:
        raise SystemExit(f"cell N={n} with k={k} yields only {len(out)} circles")
    return out


def perturb(circles, k, delta):
    """Slide the grid circle nearest the centre a distance delta toward +x.

    Displacement, not inflation: inflating a circle changes its radius and therefore
    the packing's SCORE, which would let a model detect the injection by comparing the
    total against the family's closed form instead of by checking geometry. Sliding
    leaves every radius, and so the score, untouched.
    """
    idx = (k // 2) * k + (k // 2)
    x, y, r = circles[idx]
    out = list(circles)
    out[idx] = (x + delta, y, r)
    return out, idx


# Tangency is exact in exact arithmetic and off by ~5e-17 in double precision, so a
# zero-tolerance pair test reports every contact in the base packing as an overlap. The
# answer key uses 1e-9, five orders below the smallest injected delta (1e-4) and eight
# above the representation residue, so no choice inside that window changes any key.
KEY_TOL = 1e-9


def overlapping_pairs(circles, tol=KEY_TOL):
    pairs = []
    for i in range(len(circles)):
        xi, yi, ri = circles[i]
        for j in range(i + 1, len(circles)):
            xj, yj, rj = circles[j]
            gap = math.hypot(xi - xj, yi - yj) - (ri + rj)
            if gap < -tol:
                pairs.append((i, j, -gap))
    return pairs


PROMPT = (
    "Below is a list of {n} circles in the unit square [0,1]x[0,1], given as "
    "[x, y, r] and indexed 0 to {last} in the order shown.\n"
    "Exactly one circle has been moved slightly from a valid packing, so one or more "
    "pairs of circles now OVERLAP (distance between centers strictly less than the sum "
    "of the two radii).\n"
    "Find every overlapping pair.\n"
    "Do not write or execute code - work it out by reasoning alone.\n"
    "Output ONLY a raw Python list of [i, j] index pairs, i < j, one pair per "
    "overlapping pair, sorted. If you find no overlapping pair, output [].\n"
    "No explanation, no code fences, no other text.\n\n"
    "{packing}"
)


def fmt(circles):
    return "[" + ", ".join(f"[{x:.12f}, {y:.12f}, {r:.12f}]" for x, y, r in circles) + "]"


def main():
    prompts, key = {}, {}
    for n, k in CELLS.items():
        base = base_packing(n, k)
        base_bad = overlapping_pairs(base)
        if base_bad:
            raise SystemExit(f"base packing for N={n} is not valid: {base_bad}")
        for d in DELTAS:
            circles, moved = perturb(base, k, d)
            pairs = overlapping_pairs(circles)
            if not pairs:
                raise SystemExit(f"N={n} delta={d} injected no overlap at all")
            tag = f"n{n}_d{d:g}"
            text = PROMPT.format(n=n, last=n - 1, packing=fmt(circles))
            prompts[tag] = {
                "n": n, "delta": d, "reps": REPS, "prompt": text,
                "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            }
            key[tag] = {
                "n": n, "delta": d, "moved_index": moved,
                "pairs": [[i, j] for i, j, _ in pairs],
                "depths": [round(v, 12) for _, _, v in pairs],
                "min_depth": round(min(v for _, _, v in pairs), 12),
                "max_depth": round(max(v for _, _, v in pairs), 12),
                "circles": [[round(c, 12) for c in row] for row in circles],
            }

    for path, obj in (("arm_r_prompts.json", prompts), ("arm_r_key.json", key)):
        with open(os.path.join(HERE, path), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(obj, fh, indent=2)
            fh.write("\n")

    print(f"{'cell':<14}{'pairs':<8}{'min depth':<16}{'max depth':<16}sha256[:12]")
    for tag, kv in key.items():
        print(f"{tag:<14}{len(kv['pairs']):<8}{kv['min_depth']:<16.3e}"
              f"{kv['max_depth']:<16.3e}{prompts[tag]['sha256'][:12]}")
    print(f"\n{sum(p['reps'] for p in prompts.values())} repair invocations per tier"
          f" ({len(prompts)} cells x {REPS} reps).")


if __name__ == "__main__":
    main()
