# Harvest verbatim proposer outputs from the session transcript.
#
# The agent runtime's per-task .output files are empty for subagents, so the
# durable verbatim record of each invocation's return value is the session
# transcript itself: every completed subagent appears there as a
# <task-notification> block carrying <summary>Agent "N13 s3" finished</summary>
# and <result>...</result>.
#
# Taking the label from <summary> and the payload from <result> means the
# REQUESTED n and the DELIVERED circle count are recorded independently, so a
# proposer that returns the wrong number of circles is caught as a count failure
# instead of being silently relabelled by its own output length.
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arm_f_repro as A

TRANSCRIPTS = [Path(p) for p in sys.argv[1:]]

RESULT_RE = re.compile(r"<result>(.*?)</result>", re.S)
SUMMARY_RE = re.compile(r'<summary>Agent "N(\d+) s(\d+)" finished</summary>')
# Paired trace-on arm. Labelled separately so the two arms are never pooled -
# asking for a method line is an intervention, not an observation, and the whole
# point of running both is to measure whether it moves the outcome distribution.
TRACE_RE = re.compile(r'<summary>Agent "N(\d+) trace t(\d+)" finished</summary>')
# Sonnet arm: same bare prompt, different proposer tier. Kept separate because
# pooling across models would blur the single-model limitation this arm exists
# to address.
SONNET_RE = re.compile(r'<summary>Agent "S(\d+) s(\d+)" finished</summary>')
# Opus-ALIAS arm. Named opus_alias, not a version number, deliberately: the
# runtime accepts only the alias, the user asked for 4.6 specifically, and the
# 3-6 second completion times (vs 75-250s Haiku, 150-1170s Sonnet) plus uniform
# token counts suggest a fast-mode serving path whose exact weights we cannot
# attest. Scored, but every downstream claim must carry this caveat.
OPUS_RE = re.compile(r'<summary>Agent "O(\d+) s(\d+)" finished</summary>')


def iter_text(obj):
    """Yield every string in a transcript record's content, whatever its shape."""
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from iter_text(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from iter_text(v)


def main():
    seen = set()
    samples = []
    for transcript in TRANSCRIPTS:
      with transcript.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            for blob in iter_text(rec):
                if "<task-notification>" not in blob:
                    continue
                res = RESULT_RE.search(blob)
                if not res:
                    continue
                lab, arm = SUMMARY_RE.search(blob), "bare"
                if not lab:
                    lab, arm = TRACE_RE.search(blob), "trace"
                if not lab:
                    lab, arm = SONNET_RE.search(blob), "sonnet_bare"
                if not lab:
                    lab, arm = OPUS_RE.search(blob), "opus_alias"
                if not lab:
                    continue
                n, sid = int(lab.group(1)), int(lab.group(2))
                if n not in A.TARGET_N:
                    continue
                key = (arm, n, sid)
                if key in seen:
                    continue          # a task-id can notify more than once
                seen.add(key)
                samples.append({"n": n, "sample_id": sid, "arm": arm,
                                "raw": res.group(1).strip()})

    samples.sort(key=lambda r: (r["arm"], r["n"], r["sample_id"]))
    out = Path(A.ROOT) / "arm_f_raw.json"
    out.write_text(json.dumps(samples, indent=1), encoding="utf-8")
    per_n = {}
    for s in samples:
        k = f"{s['arm']}:{s['n']}"
        per_n[k] = per_n.get(k, 0) + 1
    print(f"harvested {len(samples)} invocations  per-N {per_n}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
