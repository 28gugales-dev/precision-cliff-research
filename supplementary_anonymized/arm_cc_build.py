# ============================================================================
# Arm CC builder — constructs the code-channel prompts for N = 13, 21, 31,
# writes arm_cc_prompts.json with SHA-256 hashes. Run BEFORE sampling; the
# output file is committed with the preregistration. Deterministic, no network.
#
# Prompt surgery: the arm-F bare stem is count-substituted FIRST ("13" -> n),
# then two exact line-swaps convert the code-free contract into a
# program-emission contract. Each swap asserts exactly one occurrence so any
# stem drift fails loudly instead of producing a mixed prompt.
# ============================================================================
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).parent
CELLS = [13, 21, 31]
KSTAR = {13: 4, 21: 5, 31: 6}
ANCHOR = {13: 1.6250000, 21: 2.1000000, 31: 2.5833333}
RIVAL = {13: 1.7761424, 21: 2.2588835, 31: 2.7485281}

CODEFREE_LINE = ("Do not write or execute code - construct the packing by "
                 "reasoning alone.")
OUTPUT_LINE_T = ("Output ONLY the raw Python list of {n} [x, y, r] lists. "
                 "No explanation, no code fences, no other text.")

CONTRACT_LINE_T = ("Write a Python program that constructs the packing. The "
                   "program may import only the standard-library module math "
                   "(no other imports, no file, network or subprocess "
                   "access). When run it must print exactly one line to "
                   "stdout: the raw Python list of {n} [x, y, r] lists.")
NEW_OUTPUT_LINE = ("Output ONLY the Python program source. No explanation, "
                   "no other text.")

tmpl13 = json.loads((HERE / "arm_f_prompts.json").read_text())["13"]["prompt"]


def cc_prompt(n):
    stem = tmpl13.replace("13", str(n))  # count substitution first
    assert stem.count(CODEFREE_LINE) == 1, ("code-free line drifted", n)
    stem = stem.replace(CODEFREE_LINE, CONTRACT_LINE_T.format(n=n))
    out_line = OUTPUT_LINE_T.format(n=n)
    assert stem.count(out_line) == 1, ("output line drifted", n)
    stem = stem.replace(out_line, NEW_OUTPUT_LINE)
    return stem


def main():
    out = {"cc": {}}
    for n in CELLS:
        p = cc_prompt(n)
        rec = {
            "prompt": p,
            "sha256": hashlib.sha256(p.encode()).hexdigest(),
            "kstar": KSTAR[n],
            "anchor_value": ANCHOR[n],
            "rival_value": RIVAL[n],
        }
        out["cc"][str(n)] = rec
        print(f"CC n={n}: hash {rec['sha256'][:16]}...")
    (HERE / "arm_cc_prompts.json").write_text(json.dumps(out, indent=1),
                                              encoding="utf-8")
    print("written arm_cc_prompts.json")


if __name__ == "__main__":
    main()
