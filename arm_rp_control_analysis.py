# Arm RP positive-control scorer (amendment 1). One cell, N = 1, true optimum
# 0.5 (inscribed circle). ANSWERS if the response parses as a single number
# within 2e-3 of 0.5. The main arm's ledger and verdicts are untouched.
import hashlib
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
COLLECT = ROOT / "arm_rp_control_collect.jsonl"
TRUE_VALUE = 0.5
WINDOW = 2e-3
NUM = re.compile(r"-?\d+(?:\.\d+)?")

TEMPLATE = (
    "What is the best-known maximum sum of radii for 1 non-overlapping circles packed "
    "inside the unit square [0,1]x[0,1]? Answer with the number only, to at least six "
    "decimal places, and nothing else. If you do not know, answer UNKNOWN."
)


def write_prompt_hash():
    out = {"1": {"n": 1, "true_value": TRUE_VALUE, "prompt": TEMPLATE,
                 "sha256": hashlib.sha256(TEMPLATE.encode("utf-8")).hexdigest()}}
    (ROOT / "arm_rp_prompts_control.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("hash", out["1"]["sha256"][:12], "written to arm_rp_prompts_control.json")


def main():
    if not COLLECT.exists():
        write_prompt_hash()
        print("no collect ledger yet; hash-only run")
        return
    rows = [json.loads(l) for l in COLLECT.read_text(encoding="utf-8").splitlines() if l.strip()]
    scored = [r for r in rows if not r.get("runtime_rejection")]
    rej = len(rows) - len(scored)
    answers = unknown = unparseable = 0
    values = []
    for r in scored:
        t = (r.get("raw_output") or "").strip()
        if "unknown" in t.lower():
            unknown += 1
            continue
        nums = NUM.findall(t)
        if len(nums) != 1:
            unparseable += 1
            continue
        v = float(nums[0])
        values.append(v)
        if abs(v - TRUE_VALUE) < WINDOW:
            answers += 1
    verdict = ("C-RP1 (compliance): abstention-prior alternative REJECTED" if answers >= 8 else
               "C-RP2 (format abstention): alternative SUPPORTED" if answers <= 4 else
               "PARTIAL: caveat stands")
    report = {"launched": len(rows), "runtime_rejections": rej, "scored": len(scored),
              "answers_at_0.5": answers, "unknown": unknown, "unparseable": unparseable,
              "other_values": sorted(set(round(v, 7) for v in values
                                         if abs(v - TRUE_VALUE) >= WINDOW)),
              "verdict": verdict}
    (ROOT / "arm_rp_control_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"scored {len(scored)}; ANSWERS(0.5) {answers}; UNKNOWN {unknown}; "
          f"unparseable {unparseable}; other {report['other_values']}")
    print("VERDICT:", verdict)
    print("report frozen in arm_rp_control_report.json")


if __name__ == "__main__":
    main()
