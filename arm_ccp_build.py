# ============================================================================
# Arm CCP builder -- arm CC's registered prompts, byte-identical, no edits.
# The build exists so the run has a frozen prompt file of its own with the
# CC hashes asserted at build time and again before every invocation.
# Deterministic, no network. Committed with the preregistration.
# ============================================================================
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).parent
CELLS = [13, 21, 31]

cc = json.loads((HERE / "arm_cc_prompts.json").read_text(encoding="utf-8"))["cc"]


def main():
    out = {"ccp": {}, "tiers": {"sonnet": "anthropic/claude-sonnet-4.5"},
           "decoding": {"path": "openrouter chat-completions", "temperature": 1.0,
                        "top_p": "not set", "top_k": "not set", "max_tokens": 16384,
                        "system_prompt": None},
           "execution": {"timeout_s": 120, "allowlist": ["math"]}}
    for n in CELLS:
        p = cc[str(n)]["prompt"]
        h = hashlib.sha256(p.encode("utf-8")).hexdigest()
        assert h == cc[str(n)]["sha256"], ("CC hash", n)
        out["ccp"][str(n)] = {"prompt": p, "sha256": h, "kstar": cc[str(n)]["kstar"],
                              "anchor_value": cc[str(n)]["anchor_value"],
                              "rival_value": cc[str(n)]["rival_value"],
                              "identical_to_cc_sha256": cc[str(n)]["sha256"]}
        print(f"CCP n={n}: hash {h[:16]}... (= CC)")
    (HERE / "arm_ccp_prompts.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("written arm_ccp_prompts.json")


if __name__ == "__main__":
    main()
