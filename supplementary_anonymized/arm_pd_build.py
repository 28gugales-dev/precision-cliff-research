# ============================================================================
# Arm P-D builder -- arm P's N = 13 square prompt (== arm F's, hash 32db485b...),
# byte-identical, frozen with the two condition specs into arm_pd_prompts.json.
# Deterministic, no network. Committed with the preregistration.
# ============================================================================
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).parent
p = json.loads((HERE / "arm_p_prompts.json").read_text(encoding="utf-8"))
rec = p["square"]["13"]
h = hashlib.sha256(rec["prompt"].encode("utf-8")).hexdigest()
assert h == rec["sha256"] == "32db485bea625ff9f39f4723ebf1a01f337559a9e2cf567fb486928f71f7f8df", h
out = {
    "prompt": rec["prompt"], "sha256": h, "n": 13, "anchor_value": 1.625, "rival_value": 1.7761424, "kstar": 4,
    "model": "anthropic/claude-haiku-4.5",
    "decoding": {"path": "openrouter chat-completions", "temperature": 1.0, "top_p": "not set", "top_k": "not set", "max_tokens": 8192},
    "conditions": {
        "D1": {"reasoning": {"enabled": True}, "system_prompt": None,
               "note": "extended thinking on at OpenRouter's default effort for the vendor; no system prompt"},
        "D2": {"reasoning": None, "system_prompt": "You are a careful assistant. Think before you answer.",
               "note": "thinking off; one-line system prompt"},
    },
    "n_per_condition": 15,
}
(HERE / "arm_pd_prompts.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print("P-D prompt hash", h[:16], "(= arm P square 13 = arm F); written arm_pd_prompts.json")
