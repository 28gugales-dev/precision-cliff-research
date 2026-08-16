# ============================================================================
# P5 zero-shot top-up: N=35 -> 20 candidates.
#
# WHY THIS EXISTS. The zero-shot arm's P5 cell (N=35) currently holds 5 rows in
# arm_f_candidates.jsonl (sample_ids 1-5). The plan target for that cell is 20.
# The forecast (arm_f_repro.py header, P5) is that N=35 lands on 2.9166667,
# where truncation coincides with the recipe optimum - separable from
# convergence only by structure. Small per-cell N leaves that structural
# distribution too thin to read, so the cell is topped up to n=20. This is a
# zero-shot extension of the SAME pinned prompt: no new forecast is attached,
# the P5 story is unchanged, and any claim about N=35 still rests on the whole
# cell of 20.
#
# Prompt: taken verbatim from arm_f_prompts.json["35"] so the prompt_sha256
# recorded per new row EQUALS the pinned 3b08c56e... (asserted below, not
# assumed). Sampling goes through the Claude HTTP API, which exposes
# temperature/top_p - recorded per row, unlike the agent-runtime rows in the
# original arm (which were UNLOGGED and say so). Both are stated in the ledger
# rather than mixed.
#
# NOT validated against the forecast: value matches are scored after sampling
# by arm_f_repro.py; this file only collects and stores raw outputs.
#
# USAGE:
#   python arm_f_zero_shot_topup_35.py            # see plan, spend nothing
#   python arm_f_zero_shot_topup_35.py --run      # sample NEW_SAMPLES rows
#
# TRANSPORT, AND WHY --run IS BLOCKED. This file samples over the Claude HTTP
# API. The programme constraint for this study is Kaggle or the agent runtime,
# never a metered API, so --run is not the supported path and is kept only so
# the plan block stays checkable. Port the transport before running.
#
# COMPARABILITY WARNING THE PLAN BLOCK CANNOT ENFORCE. The 5 existing N=35
# rows came through the agent runtime with sampling parameters UNLOGGED. Rows
# added here carry T/top_p/dated-id. Two conditions, not one cell of 20;
# pooling them is the defect section 4 names in the trace arm. Keep the two
# cohorts separable in the ledger whatever runs.
# ============================================================================
import hashlib
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

NEW_SAMPLES = 15            # 5 existing + 15 = 20 rows at N=35
PROMPT_KEY = "35"           # arm_f_prompts.json key
PINNED_HASH = "3b08c56e587df8700a5db0be38bbca680eb8d1ea1ad138eb0768fead69a6b22c"
SAMPLE_ID_START = 6         # existing N=35 ids are 1..5
MODEL = "claude-haiku-4-5-20251001"   # alias->dated-id binding recorded per run

PROMPTS_FILE = ROOT / "arm_f_prompts.json"
OUT_RAW = ROOT / "arm_f_raw_topup_35.json"
OUT_LEDGER = ROOT / "arm_f_candidates_topup_35.jsonl"

TEMPERATURE = 0.8
TOP_P = 0.95
MAX_TOKENS = 1600


def load_pinned_prompt():
    payload = json.loads(PROMPTS_FILE.read_text(encoding="utf-8"))
    entry = payload[PROMPT_KEY]
    h = hashlib.sha256(entry["prompt"].encode("utf-8")).hexdigest()
    if h != PINNED_HASH or h != entry["sha256"]:
        sys.exit(f"PROMPT MISMATCH: computed {h}, pinned {PINNED_HASH}, "
                 f"file says {entry['sha256']}. Aborting - never sample on a "
                 f"prompt that does not hash to the registered value.")
    return entry["prompt"], h


def plan(prompt, h):
    print(f"[plan] N=35 top-up: {NEW_SAMPLES} new raw rows, "
          f"sample_ids {SAMPLE_ID_START}..{SAMPLE_ID_START + NEW_SAMPLES - 1}")
    print(f"[plan] prompt_sha256 = {PINNED_HASH} (pinned, verified) "
          f"[computed {h}]")
    print(f"[plan] model = {MODEL}, T={TEMPERATURE}, top_p={TOP_P}, "
          f"max_tokens={MAX_TOKENS}")
    print(f"[plan] output raw  -> {OUT_RAW.name}")
    print(f"[plan] output ledger -> {OUT_LEDGER.name} (analysed the same way "
          f"as arm_f_candidates.jsonl)")
    print("[plan] dry-run cap only; re-run with --run to sample.")


def sample_one(client, prompt, sid):
    resp = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
    return {
        "n": 35,
        "sample_id": sid,
        "arm": "topup_35",
        "model": MODEL,
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "max_tokens": MAX_TOKENS,
        "raw": text,
        "stop_reason": resp.stop_reason,
        # resp.usage is a pydantic model, not a mapping: dict() raises
        # TypeError. model_dump() is the supported accessor.
        "usage": resp.usage.model_dump() if resp.usage else None,
        "prompt_sha256": PINNED_HASH,
    }


def run():
    os.environ.setdefault("ANTHROPIC_API_KEY", "")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY not set.")
    try:
        import anthropic
    except ImportError:
        sys.exit("anthropic SDK missing: pip install anthropic")
    prompt, h = load_pinned_prompt()
    plan(prompt, h)

    existing = json.loads(OUT_RAW.read_text(encoding="utf-8")) \
        if OUT_RAW.exists() else []
    used = {r["sample_id"] for r in existing if r.get("n") == 35}
    sid = SAMPLE_ID_START
    while sid in used:
        sid += 1

    client = anthropic.Anthropic()
    new_rows = []
    for i in range(NEW_SAMPLES):
        while sid in used:
            sid += 1
        row = sample_one(client, prompt, sid)
        new_rows.append(row)
        used.add(sid)
        sid += 1
        print(f"  [sampled] sid={row['sample_id']} "
              f"len(raw)={len(row['raw'])} stop={row['stop_reason']}")
        time.sleep(0.5)

    out = existing + new_rows
    OUT_RAW.write_text(json.dumps(out, indent=2), encoding="utf-8")

    with OUT_LEDGER.open("w", encoding="utf-8") as fh:
        for r in new_rows:
            fh.write(json.dumps({"n": r["n"], "sample_id": r["sample_id"],
                                 "arm": r["arm"], "model": r["model"],
                                 "temperature": r.get("temperature"),
                                 "top_p": r.get("top_p"),
                                 "prompt_sha256": r["prompt_sha256"],
                                 "raw_output": r["raw"]}) + "\n")

    print(f"\n[ok] {len(out)} rows total in {OUT_RAW.name}; "
          f"{len(new_rows)} new ledger rows written to {OUT_LEDGER.name}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--run":
        run()
    else:
        prompt, h = load_pinned_prompt()
        plan(prompt, h)


if __name__ == "__main__":
    main()