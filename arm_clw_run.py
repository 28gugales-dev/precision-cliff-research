# ============================================================================
# Arm CL-W collection runner. Prereg: arm_clw_preregistration.txt (2026-09-02).
# arm_ccp_run.py's runner (itself arm_cl_run.py's call shape) pointed at the
# CL-W prompt file and ledger: weak tier only, N = 13, 21, 31, n = 15 per
# cell, one worker (OpenRouter's in-flight budget; see arm_ccp_run.py),
# 402 rows retried on resume, run stops on the first 402.
# The API key comes ONLY from OPENROUTER_API_KEY; never written or printed.
# ============================================================================
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import arm_ccp_run as base  # noqa: E402

base.PROMPTS_PATH = ROOT / "arm_clw_prompts.json"
base.OUT = ROOT / "arm_clw_collect.jsonl"
_data = json.loads(base.PROMPTS_PATH.read_text(encoding="utf-8"))
base.TIERS = _data["tiers"]  # {"weak": "anthropic/claude-haiku-4.5"}
base.CCP = _data["clw"]
base.MAX_GROUP_WORKERS = 1
assert base.N_SAMPLES == 15 and base.CELLS == [13, 21, 31] and base.MAX_TOKENS == 16384 and base.TEMPERATURE == 1.0


def dry_run(prompts):
    print("dry-run: prompt hashes")
    for n in base.CELLS:
        print(f"  N={n}: {prompts[n][1]}")
    model = base.TIERS["weak"]
    print(f"\nexample request body (tier=weak, model={model}, N=13):")
    print(json.dumps(base.build_body(model, prompts[13][0]), indent=1))
    print("\n(no Authorization header printed; no HTTP call made)")


if __name__ == "__main__":
    base.dry_run = dry_run
    base.main()
