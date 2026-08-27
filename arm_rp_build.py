# ============================================================================
# Arm RP (direct-recall probe) — prompt builder. Registered in
# arm_rp_preregistration.txt BEFORE sampling.
#
# Six cells: three with a published sum-of-radii value carried by the paper's
# own citations (N=13 and N=30 from the vendored bound table
# n_sweep_forecast.json, transcribed from friedman_packing; N=26 from the
# S1 scoreboard cluster, AlphaEvolve 2.63586276 through GigaEvo/AdaEvolve
# 2.636 — the registered RECALL window of 2e-3 covers the whole cluster,
# anchored here at the bound-table value 2.63598) and three held-out
# (N=50, 62, 75; no published sum-of-radii value).
# The DRAFT named N=32; no cited value exists at N=32, so the registration
# substitutes N=30 (2.842 in the bound table). Documented in the
# registration.
# ============================================================================
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
S2 = math.sqrt(2)

SCOREBOARD = {
    13: {"value": 1.829, "source": "friedman_packing via n_sweep_forecast.json"},
    26: {"value": 2.63598, "source": "S1 scoreboard cluster (AlphaEvolve 2.63586276; "
                                     "ShinkaEvolve 2.6359831/2.6359777; HELIX 2.63598308; "
                                     "GigaEvo/AdaEvolve 2.636); bound-table anchor"},
    30: {"value": 2.842, "source": "friedman_packing via n_sweep_forecast.json"},
}
HELD_OUT = [50, 62, 75]

TEMPLATE = (
    "What is the best-known maximum sum of radii for {n} non-overlapping circles packed "
    "inside the unit square [0,1]x[0,1]? Answer with the number only, to at least six "
    "decimal places, and nothing else. If you do not know, answer UNKNOWN."
)

WRAPPER = "Do not use any tools. Your entire final message must be the answer and nothing else."


def V(k, m):
    return k / 2 + m * (S2 - 1) / (2 * k)


def T(k, n):
    return n / (2 * k)


def prediction(n):
    k = round(math.sqrt(n))
    if k * k <= n:
        return V(k, n - k * k)
    return T(k, n)


def main():
    # Cross-check the bound-table transcriptions.
    tbl = {r["n"]: r["published_best_known"]
           for r in json.loads((ROOT / "n_sweep_forecast.json").read_text(encoding="utf-8"))["rows"]}
    assert abs(tbl[13] - 1.829) < 1e-9 and abs(tbl[26] - 2.63598) < 1e-9 and abs(tbl[30] - 2.842) < 1e-9
    out = {}
    for n in sorted(list(SCOREBOARD) + HELD_OUT):
        prompt = TEMPLATE.format(n=n)
        out[str(n)] = {
            "n": n,
            "kind": "scoreboard" if n in SCOREBOARD else "held_out",
            "published": SCOREBOARD.get(n, {}).get("value"),
            "published_source": SCOREBOARD.get(n, {}).get("source"),
            "family_prediction": round(prediction(n), 7),
            "prompt": prompt,
            "wrapper": WRAPPER,
            "sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        }
        print(f"N={n:>2} {out[str(n)]['kind']:<10} published {out[str(n)]['published']} "
              f"family {out[str(n)]['family_prediction']} hash {out[str(n)]['sha256'][:10]}...")
    (ROOT / "arm_rp_prompts.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("written arm_rp_prompts.json")


if __name__ == "__main__":
    main()
