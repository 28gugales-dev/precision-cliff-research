# ============================================================================
# Arm CL builder — arm CC's registered prompts with exactly one line
# replacement: the import allowlist widens from math to math, numpy, scipy.
# Run BEFORE sampling; the output is committed with the preregistration.
# Deterministic, no network. The replacement asserts a single occurrence so
# any drift in the CC stem fails loudly instead of producing a mixed prompt.
# ============================================================================
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).parent
CELLS = [13, 21, 31]

OLD_CLAUSE = "may import only the standard-library module math"
NEW_CLAUSE = "may import only the modules math, numpy and scipy"

cc = json.loads((HERE / "arm_cc_prompts.json").read_text(encoding="utf-8"))["cc"]


def cl_prompt(n):
    stem = cc[str(n)]["prompt"]
    assert hashlib.sha256(stem.encode()).hexdigest() == cc[str(n)]["sha256"], ("CC hash", n)
    assert stem.count(OLD_CLAUSE) == 1, ("allowlist clause drifted", n)
    return stem.replace(OLD_CLAUSE, NEW_CLAUSE)


def main():
    out = {"cl": {}, "tiers": {"weak": "anthropic/claude-haiku-4.5",
                               "sonnet": "anthropic/claude-sonnet-4.5"},
           "decoding": {"path": "openrouter chat-completions", "temperature": 1.0,
                        "top_p": "not set", "top_k": "not set", "max_tokens": 16384,
                        "system_prompt": None},
           "execution": {"timeout_s": 120, "allowlist": ["math", "numpy", "scipy"]}}
    for n in CELLS:
        p = cl_prompt(n)
        rec = {"prompt": p, "sha256": hashlib.sha256(p.encode()).hexdigest(),
               "kstar": cc[str(n)]["kstar"], "anchor_value": cc[str(n)]["anchor_value"],
               "rival_value": cc[str(n)]["rival_value"],
               "derived_from_cc_sha256": cc[str(n)]["sha256"]}
        out["cl"][str(n)] = rec
        print(f"CL n={n}: hash {rec['sha256'][:16]}...  (from CC {rec['derived_from_cc_sha256'][:8]})")
    (HERE / "arm_cl_prompts.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("written arm_cl_prompts.json")


if __name__ == "__main__":
    main()
