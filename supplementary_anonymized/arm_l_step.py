# Arm L stepper. Given a lineage, reads the ledger so far, rebuilds the archive
# under the registered rule, and emits the next generation's five prompts to
# arm_l_next_<lineage>.json. Deterministic: parent for slot i is
# archive[i mod len(archive)]. Committed with arm_l_preregistration.txt before
# sampling.
#
#   python arm_l_step.py 13-greedy
#
# Prints "DONE" when the lineage has completed generation 5.
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arm_f_repro as A
import arm_l_build as B

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
CFG = json.loads((ROOT / "arm_l_prompts.json").read_text(encoding="utf-8"))


def ledger(lineage):
    """One ledger per lineage: the four lineages run concurrently and must not
    share an append target."""
    return ROOT / f"arm_l_collect_{lineage}.jsonl"


def rows_for(lineage):
    path = ledger(lineage)
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("lineage") == lineage:
            out.append(r)
    return out


def score_row(r, n):
    """Return (sum_of_radii, circles) for a valid row, else (None, None)."""
    if r.get("runtime_rejection"):
        return None, None
    circles, err = A.parse_packing(r.get("raw_output"))
    if circles is None or len(circles) != n:
        return None, None
    ok, why = A.validate(circles, n, tol=1e-6)
    if not ok:
        return None, None
    return sum(c[2] for c in circles), circles


def build_archive(rows, n, size):
    """Top `size` valid proposals by score, one per distinct 2e-3 bucket, best first."""
    scored = []
    for r in rows:
        s, circles = score_row(r, n)
        if s is not None:
            scored.append((s, circles))
    scored.sort(key=lambda t: -t[0])
    archive, seen = [], set()
    for s, circles in scored:
        b = round(s / 2e-3)
        if b in seen:
            continue
        seen.add(b)
        archive.append((s, circles))
        if len(archive) >= size:
            break
    return archive


def fmt_packing(circles):
    return "[" + ", ".join("[" + ", ".join(repr(v) for v in c) + "]" for c in circles) + "]"


def main():
    lineage = sys.argv[1]
    n_str, regime = lineage.split("-")
    n = int(n_str)
    size = CFG["regimes"][regime]
    pop = CFG["pop"]
    gens = CFG["generations"]
    cell = CFG["cells"][n_str]

    rows = rows_for(lineage)
    done_gens = {r["generation"] for r in rows}
    nxt = 0
    while nxt in done_gens:
        nxt += 1
    if nxt > gens:
        print("DONE")
        (ROOT / f"arm_l_next_{lineage}.json").write_text(
            json.dumps({"lineage": lineage, "done": True}, indent=2), encoding="utf-8")
        return

    if nxt == 0:
        prompts = [{"slot": i, "parent_score": None, "prompt": cell["gen0_prompt"]}
                   for i in range(1, pop + 1)]
    else:
        archive = build_archive(rows, n, size)
        if not archive:
            # Registered: no valid proposals yet -> repeat the unconditioned prompt,
            # recorded rather than repaired.
            prompts = [{"slot": i, "parent_score": None, "prompt": cell["gen0_prompt"]}
                       for i in range(1, pop + 1)]
        else:
            tail = CFG["templates"]["mutation_tail"]
            prompts = []
            for i in range(1, pop + 1):
                s, circles = archive[(i - 1) % len(archive)]
                p = cell["gen0_prompt"] + tail.format(
                    n=n, score=f"{s:.7f}", parent=fmt_packing(circles))
                prompts.append({"slot": i, "parent_score": round(s, 7), "prompt": p})

    payload = {"lineage": lineage, "n": n, "regime": regime, "generation": nxt,
               "done": False, "archive_size": size, "prompts": prompts,
               "wrapper": CFG["wrapper"]}
    (ROOT / f"arm_l_next_{lineage}.json").write_text(json.dumps(payload, indent=2),
                                                     encoding="utf-8")
    print(f"lineage {lineage} generation {nxt}: {len(prompts)} prompts written to "
          f"arm_l_next_{lineage}.json"
          + ("" if nxt == 0 else
             f" (parents at {[p['parent_score'] for p in prompts]})"))


if __name__ == "__main__":
    main()
