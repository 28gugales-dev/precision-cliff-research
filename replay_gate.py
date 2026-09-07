"""Replay gate: every script the shipped bundle documents must run from the bundle.

Usage: python -X utf8 replay_gate.py <extracted_artifact_dir> [--timeout 900]

Collects every `*.py` named in HOW_TO_RUN.md and BUNDLE_README.md inside the
artifact directory, plus every script under paper_repo/loop/, and runs each one
with no arguments from the artifact root (paper_repo scripts from their own
directory). Writes replay_gate.json beside this file and exits 1 if any named
script is missing or exits non-zero.
"""
import json
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAMED = re.compile(r"`([A-Za-z0-9_./]+\.py)`")
# Scripts that need a live serving path or a GPU; the bundle documents them as
# how the data was collected, not as replays.
SKIP = re.compile(r"_run\.py$|_build\.py$|_smoketest\.py$|arm_b_baseline\.py$|arm_b_bridge_run\.py$"
                  r"|arm_l_step\.py$|arm_g_rect\.py$")


def main():
    root = Path(sys.argv[1]).resolve()
    timeout = 900
    if "--timeout" in sys.argv:
        timeout = int(sys.argv[sys.argv.index("--timeout") + 1])
    names = []
    for doc in ("HOW_TO_RUN.md", "BUNDLE_README.md"):
        text = (root / doc).read_text(encoding="utf-8", errors="replace")
        for m in NAMED.finditer(text):
            n = m.group(1)
            if n not in names:
                names.append(n)
    for p in sorted((root / "paper_repo" / "loop").glob("*.py")):
        rel = "paper_repo/loop/" + p.name
        if rel not in names:
            names.append(rel)

    results = []
    for n in names:
        path = root / n
        entry = {"script": n}
        if not path.is_file():
            entry["status"] = "MISSING"
            results.append(entry)
            print(f"MISSING  {n}")
            continue
        if SKIP.search(n):
            entry["status"] = "SKIP_LIVE"
            results.append(entry)
            print(f"SKIP     {n} (needs a serving path)")
            continue
        cwd = path.parent if n.startswith("paper_repo/") else root
        t0 = time.time()
        try:
            proc = subprocess.run([sys.executable, "-X", "utf8", str(path)], cwd=str(cwd),
                                  capture_output=True, text=True, timeout=timeout,
                                  encoding="utf-8", errors="replace")
            entry["exit"] = proc.returncode
            entry["status"] = "OK" if proc.returncode == 0 else "FAIL"
            tail = (proc.stderr or proc.stdout).strip().splitlines()
            entry["tail"] = tail[-3:]
        except subprocess.TimeoutExpired:
            entry["status"] = "TIMEOUT"
            entry["exit"] = None
        entry["seconds"] = round(time.time() - t0, 1)
        results.append(entry)
        print(f"{entry['status']:8} {n} ({entry['seconds']}s)")
        if entry["status"] == "FAIL":
            for line in entry.get("tail", []):
                print(f"         | {line}")

    bad = [r for r in results if r["status"] in ("MISSING", "FAIL", "TIMEOUT")]
    out = HERE / "replay_gate.json"
    out.write_text(json.dumps({"root": str(root), "results": results,
                               "failures": len(bad)}, indent=1), encoding="utf-8")
    print(f"\n{len(results)} scripts named, {len(bad)} failures -> {out}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
