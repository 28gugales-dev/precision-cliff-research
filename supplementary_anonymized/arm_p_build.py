# ============================================================================
# Arm P builder — freezes the prompts and SHA-256 hashes for the pinned-
# temperature rerun. Run BEFORE sampling; the output is committed with the
# preregistration. Deterministic, no network.
#
# Byte-identity is the whole point of this arm, so every prompt that already
# carries a registered hash is ASSERTED against it rather than trusted:
#   square N = 13, 17, 31, 35, 37   -> arm_f_prompts.json
#   square N = 21                   -> the hash quoted in arm_t_preregistration.txt
#   held-out N = 50, 58, 62, 65, 75 -> arm_cn_prompts.json
#   code    N = 13, 21, 31          -> arm_cc_prompts.json
# N = 43 has never carried a registered hash; this file supplies the first one.
# ============================================================================
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
SQUARE = [13, 17, 21, 31, 35, 37, 43]
HELDOUT = [50, 58, 62, 65, 75]
CODE = [13, 21, 31]

f_prompts = json.loads((HERE / "arm_f_prompts.json").read_text(encoding="utf-8"))
cn_prompts = json.loads((HERE / "arm_cn_prompts.json").read_text(encoding="utf-8"))
cc_prompts = json.loads((HERE / "arm_cc_prompts.json").read_text(encoding="utf-8"))["cc"]
tmpl13 = f_prompts["13"]["prompt"]


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def square_prompt(n):
    # Same count substitution arm_cc_build.py uses: the registered N = 13 stem
    # with "13" replaced. The two hard-coded occurrences are the count.
    return tmpl13.replace("13", str(n))


def registered_t_hash():
    txt = (HERE / "arm_t_preregistration.txt").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"N\s*=\s*21[^0-9a-f]{0,80}?([0-9a-f]{64})", txt)
    if not m:
        m = re.search(r"([0-9a-f]{64})", txt)
    return m.group(1) if m else None


def main():
    out = {"square": {}, "heldout": {}, "code": {}, "decoding": {
        "path": "openrouter chat-completions", "model": "anthropic/claude-haiku-4.5",
        "temperature": 1.0, "top_p": "not set", "top_k": "not set", "max_tokens": 8192,
        "system_prompt": None}}

    t21 = registered_t_hash()
    for n in SQUARE:
        p = square_prompt(n)
        h = sha(p)
        if str(n) in f_prompts:
            assert p == f_prompts[str(n)]["prompt"], ("square prompt drifted from arm F", n)
            assert h == f_prompts[str(n)]["sha256"], ("square hash drifted from arm F", n)
            src = "arm_f_prompts.json"
        elif n == 21 and t21:
            assert h == t21, ("N=21 hash differs from arm_t_preregistration.txt", h, t21)
            src = "arm_t_preregistration.txt"
        else:
            src = "first registration here (N=43 never carried a hash)"
        out["square"][str(n)] = {"prompt": p, "sha256": h, "hash_source": src}
        print(f"square N={n:>2}: {h[:16]}...  [{src}]")

    for n in HELDOUT:
        rec = cn_prompts[str(n)]
        assert sha(rec["prompt"]) == rec["sha256"], ("arm CN hash mismatch", n)
        out["heldout"][str(n)] = {"prompt": rec["prompt"], "sha256": rec["sha256"],
                                  "hash_source": "arm_cn_prompts.json"}
        print(f"held-out N={n}: {rec['sha256'][:16]}...  [arm_cn_prompts.json]")

    for n in CODE:
        rec = cc_prompts[str(n)]
        assert sha(rec["prompt"]) == rec["sha256"], ("arm CC hash mismatch", n)
        out["code"][str(n)] = {"prompt": rec["prompt"], "sha256": rec["sha256"],
                               "hash_source": "arm_cc_prompts.json",
                               "kstar": rec["kstar"], "anchor_value": rec["anchor_value"],
                               "rival_value": rec["rival_value"]}
        print(f"code N={n}: {rec['sha256'][:16]}...  [arm_cc_prompts.json]")

    (HERE / "arm_p_prompts.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("written arm_p_prompts.json: 15 cells")


if __name__ == "__main__":
    main()
