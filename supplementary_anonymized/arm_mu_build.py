# ============================================================================
# Arm MU/CH builder — constructs parent packings and prompts, validates every
# parent with the arm-F validator, writes arm_mu_prompts.json with SHA-256
# hashes. Run BEFORE sampling; the output file is committed with the
# preregistration. Deterministic, no network.
# ============================================================================
import hashlib
import json
import math
from pathlib import Path

from arm_f_repro import validate, score

HERE = Path(__file__).parent
S2 = math.sqrt(2)
CELLS = [13, 21, 31]
KSTAR = {13: 4, 21: 5, 31: 6}
ANCHOR = {13: 1.6250000, 21: 2.1000000, 31: 2.5833333}
RIVAL = {13: 1.7761424, 21: 2.2588835, 31: 2.7485281}
RIVAL_KM = {13: (3, 4), 21: (4, 5), 31: (5, 6)}


def grid_t(k, n):
    r = 1 / (2 * k)
    cells = [(x, y) for y in range(k) for x in range(k)][:n]
    return [[round((2 * x + 1) * r, 7), round((2 * y + 1) * r, 7), round(r, 7)] for x, y in cells]


def grid_v(k, m):
    """k x k grid + m corner-vertex fillers (interior vertices, row-major)."""
    r = 1 / (2 * k)
    rf = (S2 - 1) / (2 * k)
    out = [[round((2 * x + 1) * r, 7), round((2 * y + 1) * r, 7), round(r, 7)]
           for y in range(k) for x in range(k)]
    verts = [((x + 1) / k, (y + 1) / k) for y in range(k - 1) for x in range(k - 1)]
    for vx, vy in verts[:m]:
        out.append([round(vx, 7), round(vy, 7), round(rf, 7)])
    return out


def diagonal_chain(n):
    """Off-family parent: n equal circles spaced along the main diagonal.
    One radius, off-lattice centers, score well below the family best."""
    r = 0.9 * S2 / (2 * (n + 1))
    d = r  # wall margin (>= r suffices since centers stay r from each wall)
    lo, hi = r, 1 - r
    out = []
    for i in range(n):
        t = i / (n - 1)
        c = lo + t * (hi - lo)
        out.append([round(c, 7), round(c, 7), round(r, 7)])
    return out


BARE = (HERE / "arm_f_prompts.json")
tmpl13 = json.loads(BARE.read_text())["13"]["prompt"]


def bare_prompt(n):
    return tmpl13.replace("13", str(n))


def mu_prompt(n, parent, parent_score):
    coords = json.dumps(parent)
    return (bare_prompt(n)
            + f"\nHere is an existing packing of {n} circles scoring {parent_score:.7f} (sum of radii):\n"
            + coords
            + "\nPropose a modification of this packing that increases the sum of radii. "
            + "Output ONLY the raw Python list of the modified packing, nothing else.")


def ch_prompt(n):
    k = KSTAR[n]
    lines = []
    for kk in range(2, 8):
        m = n - kk * kk
        if 0 <= m <= (kk - 1) ** 2:
            v = kk / 2 + m * (S2 - 1) / (2 * kk)
            lines.append(f"k={kk}: grid of k x k circles radius 1/(2k) plus {m} corner fillers radius (sqrt(2)-1)/(2k), total sum = {v:.7f}")
        elif n < kk * kk:
            v = n / (2 * kk)
            lines.append(f"k={kk}: k x k grid truncated to {n} circles, radius 1/(2k), total sum = {v:.7f}")
    return (bare_prompt(n)
            + "\nYou may use this known family of constructions (choose whichever k gives the largest sum, or any better packing):\n"
            + "\n".join(lines))


def main():
    out = {"mu": {}, "ch": {}}
    for n in CELLS:
        k = KSTAR[n]
        pa = grid_t(k, n)
        kb, mb = RIVAL_KM[n]
        pb = grid_v(kb, mb)
        pc = diagonal_chain(n)
        parents = {"A_anchor": pa, "B_rival": pb, "C_offfamily": pc}
        cellrec = {}
        for tag, p in parents.items():
            ok, why = validate(p, n, tol=1e-6)
            s = score(p)
            assert ok, (n, tag, why)
            if tag == "B_rival":
                assert abs(s - RIVAL[n]) < 2e-3, (n, s)
            if tag == "A_anchor":
                assert abs(s - ANCHOR[n]) < 2e-3, (n, s)
            prompt = mu_prompt(n, p, s)
            cellrec[tag] = {
                "parent": p, "parent_score": round(s, 7),
                "prompt": prompt,
                "sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            }
            print(f"MU n={n} {tag}: parent valid, score {s:.7f}, hash {cellrec[tag]['sha256'][:16]}…")
        out["mu"][str(n)] = cellrec
        cp = ch_prompt(n)
        out["ch"][str(n)] = {"prompt": cp,
                             "sha256": hashlib.sha256(cp.encode()).hexdigest()}
        print(f"CH n={n}: hash {out['ch'][str(n)]['sha256'][:16]}…")
    (HERE / "arm_mu_prompts.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("written arm_mu_prompts.json")


if __name__ == "__main__":
    main()
