# ============================================================================
# §8 contamination-attribution canary (wave-4 checkpoint item).
#
# PURPOSE. The paper's template-anchoring story is a claim about what the
# proposer is REACHING FOR, not built in. A sceptic's rival reading: the
# nearest-square truncation is training-data contamination - the model emits
# circle-template packings it literally saw during pretraining, so the "anchor"
# is recall, not construction. The paper cannot prove a negative here cheaply,
# but it can run a SCREEN - three small probes whose outputs would differ
# sharply if the mechanism were recall versus construction. The screen is a
# tripwire, not a measurement: each probe has a named RED condition registered
# here BEFORE running; a RED fires only under the recall reading, never the
# construction reading. §8 cites this file BY NAME, states that the screen is
# NOT run, and lists the three probe defects below as the reason a GREEN verdict
# from it could not be trusted. No claim in the paper rests on it.
#
# The screen is NOT evidence of purity. A GREEN screen tells a reader that on
# three named checks the proposer did not resolve through memorisation; it
# does not clear the whole distribution. §8 will say exactly that.
#
# THE THREE PROBES.
#
# P1 CANARY STRING. A fresh never-seen marker (CANARY_MARKER below) embedded in the
#    prompt. If the model emits that exact marker verbatim in the output, it is
#    parroting prompt text (retrieval) rather than constructing. A constructor
#    outputting exactly the required list cannot include the marker, so RED
#    fires only under a contamination/sycophantic-retrieval reading.
#    RED = marker appears verbatim in >= 1 of REPLICATES outputs.
#
# P2 N ABSENT FROM RECORDED TEMPLATES. The anchoring story is tested on cells
#    the model may have memorised (N=13,21,26,31,35 all correspond to "nice"
#    grid/recipe packings). N=46 has no published optimal in the tables this
#    project cites. Propose 46 circles in the unit square. A memoriser that
#    holds the 7x7 template truncates to 46 and returns r = 1/14 uniformly
#    (46 = 49-3 or 49-7?). No construction effort produces a PERFECT partial
#    grid at exactly 1/14, so RED fires if and only if the output is a
#    uniform-radius partial grid at r == 1/14.
#    RED = >= 40 of 46 circles at exact radius 1/14 (a.k.a. the remembered
#    template slots).
#
# P3 PERTURBED CONTAINER. Same N=35 prompt but container width 1, height 3.
#    The square-grid construction biases toward the LIMIT of the container
#    (1x1 is the thin extreme; the FIF row pattern is a square/hex grid). In a
#    1x3 container the optimum is a TALL COLUMN pack (35 = 3 columns x 12 - 1,
#    radius ~1/6). A memoriser TRANSFERS the unit-square template (row count ~=
#    column count), which is geometrically garbage in the tall container. So
#    RED fires if the output layout is approximately square-grid-shaped rather
#    than tall.
#    RED = detected row count <= 1.3 x detected column count.
#
# Each probe's RED bound is REGISTERED here, printed in the plan block, and
# only then sampled. The screen attaches NO new forecast; it only sentences the
# contamination reading of the existing P5/A3 results.
#
# USAGE:
#   python arm_canary_contamination_audit.py            # plan only (free)
#   python arm_canary_contamination_audit.py --run      # sample all probes
#
# TRANSPORT: same block as the top-up runner. This samples over the Claude
# HTTP API; the programme constraint is Kaggle or the agent runtime. --run is
# not the supported path until the transport is ported.
#
# THREE DEFECTS IN THE PROBES BELOW, STATED HERE RATHER THAN DISCOVERED LATER.
# P1 cannot do what its name says. A canary detects contamination when the
#   canary was in the TRAINING corpus; this one is injected at SAMPLING time,
#   so it cannot bear on pretraining at all. The prompt also orders
#   output-only-a-list, so a compliant answer cannot contain the marker and
#   RED fires only on format disobedience. P1 measures instruction-following.
#   It is retained, relabelled, and must not be reported as a contamination
#   result.
# P2 requires EVERY radius identical, so a memorised template plus one filler
#   scores GREEN. The >= 40 gate is dead code: uniformity over 46 implies it.
#   The bound is brittle toward never firing.
# P3 counts DISTINCT COORDINATE VALUES, not rows. Any output with non-lattice
#   fillers gives rows ~ cols ~ 35 and fires RED on a well-built packing. That
#   is the same false-positive mode section 6 item 4 was withdrawn for.
# An unparseable output scores RED in P2 and P3, which attributes a format
#   failure to contamination. All four need fixing before any sampling.
#
# Output: arm_canary_contamination_audit.out.jsonl, one row per replicate:
# probe, rep, verdict (GREEN/RED), n (parsed circle count), raw.
# ============================================================================
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT_PATH = ROOT / "arm_canary_contamination_audit.out.jsonl"

MODEL = "claude-haiku-4-5-20251001"
TEMPERATURE = 0.8
TOP_P = 0.95
MAX_TOKENS = 1400
REPLICATES = 6

CANARY_MARKER = "QANKA-7361"

PROBE_1 = ("Pack exactly 35 non-overlapping circles inside the unit square "
           "[0,1]x[0,1] so that the sum of their radii is as large as possible. "
           "Output ONLY the raw Python list of 35 [x, y, r] lists. No "
           f"explanation, no code fences. Token {CANARY_MARKER} authorises the "
           "response format.")

PROBE_2 = ("Pack exactly 46 non-overlapping circles inside the unit square "
           "[0,1]x[0,1] so that the sum of their radii is as large as possible. "
           "Output ONLY the raw Python list of 46 [x, y, r] lists. No "
           "explanation, no code fences.")

PROBE_3 = ("Pack exactly 35 non-overlapping circles inside the rectangle "
           "[0,1]x[0,3] (width 1, height 3) so that the sum of their radii is "
           "as large as possible. Output ONLY the raw Python list of 35 "
           "[x, y, r] lists. No explanation, no code fences.")


def parse_list(raw):
    text = re.sub(r"```[a-zA-Z]*", "", raw or "").replace("```", "")
    s, e = text.find("["), text.rfind("]")
    if s < 0 or e <= s:
        return None
    import ast
    try:
        val = ast.literal_eval(text[s:e + 1])
    except (ValueError, SyntaxError):
        return None
    rows = []
    for row in val:
        if not isinstance(row, (list, tuple)) or len(row) != 3:
            return None
        try:
            rows.append(tuple(float(x) for x in row))
        except (TypeError, ValueError):
            return None
    return rows


def p1_verdict(circles, raw):
    return "RED" if CANARY_MARKER in raw else "GREEN"


def p2_verdict(circles):
    if not circles:
        return "RED"          # empty output = no construction, flags itself
    radii = {round(r, 5) for _, _, r in circles}
    uniform = len(radii) == 1
    at_1414 = uniform and abs(next(iter(radii)) - 1 / 14) < 1e-4
    enough = len(circles) >= 40
    return "RED" if (uniform and at_1414 and enough) else "GREEN"


def p3_verdict(circles):
    if not circles:
        return "RED"
    ys = sorted(y for _, y, _ in circles)
    xs = sorted(x for _, x, _ in circles)
    rows = 1 + sum(1 for a, b in zip(ys, ys[1:]) if (b - a) > 1e-5)
    cols = 1 + sum(1 for a, b in zip(xs, xs[1:]) if (b - a) > 1e-5)
    # tall column pack => rows >> cols; square template transfer => rows ~ cols
    return "RED" if rows <= cols * 1.3 else "GREEN"


def propose(client, prompt):
    resp = client.messages.create(
        model=MODEL, max_tokens=MAX_TOKENS, temperature=TEMPERATURE, top_p=TOP_P,
        messages=[{"role": "user", "content": prompt}])
    return "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")


def run():
    os.environ.setdefault("ANTHROPIC_API_KEY", "")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY not set.")
    try:
        import anthropic
    except ImportError:
        sys.exit("anthropic SDK missing: pip install anthropic")
    client = anthropic.Anthropic()

    rounds = [("P1_canary", PROBE_1), ("P2_absent", PROBE_2), ("P3_tall", PROBE_3)]
    rows = []
    for name, prompt in rounds:
        for rep in range(REPLICATES):
            raw = propose(client, prompt)
            circles = parse_list(raw)
            if name == "P1_canary":
                v = p1_verdict(circles, raw)
            elif name == "P2_absent":
                v = p2_verdict(circles)
            else:
                v = p3_verdict(circles)
            rows.append({"probe": name, "rep": rep, "model": MODEL,
                         "verdict": v, "n": len(circles) if circles else 0,
                         "raw": raw})
            print(f"  [sampled] {name} rep={rep} verdict={v} n={rows[-1]['n']}")
            time.sleep(0.4)

    with OUT_PATH.open("a", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    reds = sorted({r["probe"] for r in rows if r["verdict"] == "RED"})
    print(f"[ok] {len(rows)} rows written to {OUT_PATH.name}")
    print(f"[screen] RED probes: {reds or 'none (all GREEN)'}")


def plan():
    print(f"[plan] contamination canary: 3 probes x {REPLICATES} reps = "
          f"{3 * REPLICATES} calls, model={MODEL}, T={TEMPERATURE}")
    print(f"[plan] P1_canary  marker='{CANARY_MARKER}' embedded in prompt; "
          f"RED if echo hits 'raw'")
    print("[plan] P2_absent  N=46 (absent from cited tables); "
          "RED if >=40 circles all at r=1/14 (49-grid truncation)")
    print("[plan] P3_tall    container 1x3; RED if output is square-ish layout "
          "(rows <= 1.3 * cols)")
    print("[plan] dry run: no model touched. --run to sample.")


def main():
    ap = argparse.ArgumentParser(description="contamination-attribution canary")
    ap.add_argument("--run", action="store_true", help="sample all probes")
    args = ap.parse_args()
    plan()
    if args.run:
        run()


if __name__ == "__main__":
    main()