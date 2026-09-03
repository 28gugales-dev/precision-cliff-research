# ============================================================================
# Arm CL-W builder -- arm CL's registered weak-tier prompts, byte-identical
# (hashes asserted against arm_cl_prompts.json). Frozen into
# arm_clw_prompts.json so the top-up run carries its own prompt file.
# Deterministic, no network. Committed with the preregistration.
# ============================================================================
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).parent
CELLS = [13, 21, 31]

cl = json.loads((HERE / "arm_cl_prompts.json").read_text(encoding="utf-8"))


def main():
    out = {"clw": {}, "tiers": {"weak": cl["tiers"]["weak"]},
           "decoding": cl["decoding"], "execution": cl["execution"],
           "pooled_with": "arm_cl_collect.jsonl weak tier, same prompt hash, same path, same scorer"}
    assert cl["tiers"]["weak"] == "anthropic/claude-haiku-4.5"
    for n in CELLS:
        rec = cl["cl"][str(n)]
        h = hashlib.sha256(rec["prompt"].encode("utf-8")).hexdigest()
        assert h == rec["sha256"], ("CL hash", n)
        out["clw"][str(n)] = {"prompt": rec["prompt"], "sha256": h, "identical_to_cl_sha256": rec["sha256"]}
        print(f"CL-W n={n}: hash {h[:16]}... (= CL)")
    (HERE / "arm_clw_prompts.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("written arm_clw_prompts.json")


if __name__ == "__main__":
    main()
