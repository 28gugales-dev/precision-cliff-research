# Arm V runner. Prereg: arm_v_preregistration.md (git 5444f10, committed
# before this file ever executed - the runner refuses to start unless that
# commit exists in history).
#
# 3 free-tier vendor aliases x TARGET_N x 5 samples via the opencode CLI.
# Every invocation writes one live jsonl row, failures included. Prompts are
# loaded from arm_f_prompts.json and their SHA-256 recomputed at call time;
# any mismatch aborts the whole run rather than sampling off-register.
import hashlib
import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "arm_v_candidates_raw.jsonl"
RUN_DATE = "2026-08-12"
PREREG_COMMIT = "5444f10"

MODELS = [
    "opencode/deepseek-v4-flash-free",
    "opencode/nemotron-3-ultra-free",
    "opencode/hy3-free",
]
TARGET_N = [13, 17, 31, 35, 37]
SAMPLES = 5
CALL_TIMEOUT = 300  # seconds
MAX_WORKERS = 3     # 8 parallel Bun instances exhausted the paging file;
                    # 3 is what this machine sustains (measured, not chosen)

ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]|\x1b\][^\x07]*\x07")


def load_prompts():
    d = json.loads((ROOT / "arm_f_prompts.json").read_text(encoding="utf-8"))
    prompts = {}
    for n in TARGET_N:
        p = d[str(n)]["prompt"]
        h = hashlib.sha256(p.encode("utf-8")).hexdigest()
        if h != d[str(n)]["sha256"]:
            sys.exit(f"prompt hash mismatch for N={n}; refusing to sample")
        prompts[n] = (p, h)
    return prompts


def clean(text):
    text = ANSI.sub("", text)
    lines = [l for l in text.splitlines()
             if not l.strip().startswith("> build")
             and "NativeCommandError" not in l]
    return "\n".join(lines).strip()


def call(model, prompt):
    t0 = time.time()
    try:
        r = subprocess.run(
            ["opencode.cmd", "run", "-m", model, prompt],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=CALL_TIMEOUT, cwd=str(ROOT.parent))
        return clean(r.stdout or ""), (r.stderr or "")[:2000], r.returncode, time.time() - t0
    except subprocess.TimeoutExpired:
        return "", "TIMEOUT", -1, time.time() - t0
    except FileNotFoundError:
        r = subprocess.run(
            ["opencode", "run", "-m", model, prompt],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=CALL_TIMEOUT, cwd=str(ROOT.parent), shell=True)
        return clean(r.stdout or ""), (r.stderr or "")[:2000], r.returncode, time.time() - t0


def existing_keys():
    """(model, n, sample_id) triples already in the ledger - resume support.

    Only rows that actually returned text count as done; empty/errored rows
    are retried by the resumed run, and the ledger keeps both attempts."""
    done = set()
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("raw_len", 0) > 0:
                done.add((r["proposer_alias"], r["n"], r["sample_id"]))
    return done


def worker(model, prompts, lock, done):
    short = model.split("/")[-1]
    for n in TARGET_N:
        prompt, sha = prompts[n]
        for sid in range(1, SAMPLES + 1):
            if (model, n, sid) in done:
                continue
            raw, err, rc, dur = call(model, prompt)
            row = {
                "reconstructed": False,
                "run_date": RUN_DATE,
                "prereg_commit": PREREG_COMMIT,
                "proposer_alias": model,
                "runtime": "opencode-cli-1.18.3-zen-free",
                "sampling_params": None,
                "sampling_params_note": "not exposed by the opencode runtime; see prereg",
                "n": n,
                "arm": "vendor",
                "sample_id": sid,
                "prompt_sha256": sha,
                "raw_output": raw,
                "raw_len": len(raw),
                "call_rc": rc,
                "call_error": err if (rc != 0 or not raw) else None,
                "duration_s": round(dur, 1),
            }
            with lock:
                with OUT.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(row) + "\n")
                print(f"{short:28s} N={n:>2} s{sid}  rc={rc} len={len(raw):5d} {dur:5.1f}s",
                      flush=True)


def main():
    head = subprocess.run(["git", "merge-base", "--is-ancestor", PREREG_COMMIT, "HEAD"],
                          cwd=str(ROOT), capture_output=True)
    if head.returncode != 0:
        sys.exit(f"prereg commit {PREREG_COMMIT} is not an ancestor of HEAD; refusing to sample")
    models = sys.argv[1:] or MODELS
    prompts = load_prompts()
    done = existing_keys()
    if done:
        print(f"resume: {len(done)} completed invocations skipped")
    import threading
    lock = threading.Lock()
    with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(models))) as ex:
        for m in models:
            ex.submit(worker, m, prompts, lock, done)
    print("done")


if __name__ == "__main__":
    main()
