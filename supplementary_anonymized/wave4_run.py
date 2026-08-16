#!/usr/bin/env python3
"""Wave 4 dispatch harness — capability-tier control on Heilbronn n=13.

Registration: wave4_prereg_tiers_heilbronn.md
  SHA-256 7b3e67dc07788fb9439a42269540aaec4e83e83737cc6b1d41be589f99b0b3a4
  external timestamp: public Kaggle dataset ANON-KAGGLE-OWNER/wave4-prereg-tiers-heilbronn

The agent runtime is the substrate, so this script does not call any model. It is the
deterministic half of the loop: it holds the ledger, reconstructs each lineage's running
parent, emits the exact prompt for every pending call, and scores/records raw outputs the
orchestrator pastes back. The orchestrator dispatches one subagent per pending call with
the emitted prompt verbatim, tools forbidden, and records tool_uses / duration_ms /
subagent_tokens / model identifiers per row (prereg SS2, SS3).

Seed parent and evaluator are EXTRACTED from the wave-3 runner at import time, not
retyped (prereg SS3): one origin, one echo referent class.

Usage:
  python wave4_run.py pending            # print prompts for every not-yet-sampled call
  python wave4_run.py record <tier> <lineage> <gen> <raw_file> <duration_ms> <tokens> <tool_uses> <model_requested> <model_reported>
  python wave4_run.py table              # per-tier counts so far (descriptive only; no
                                         # registered verdict is computed here — that is
                                         # wave4_analysis.py's job, after all rows land)
"""
import ast, json, os, sys, re
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
RUNNER = os.path.join(HERE, "sec3_artifacts", "runners",
                      "kaggle_precision_sweep_14b_heilbronn.py")
LEDGER = os.path.join(HERE, "wave4_artifacts", "wave4_tiers.jsonl")

N = 13
N_TRIPLES = 286
COORD_DP = 6
SCORE_DP = 12
TIERS = ["haiku", "sonnet", "opus"]
LINEAGES = 8
GENERATIONS = 5

# ---- extract SEED_PARENT / SEED_PARENT_SCORE from the wave-3 runner, never retype ----
def _extract_seed():
    src = open(RUNNER, encoding="utf-8").read()
    m = re.search(r"SEED_PARENT = (\[.*?\n\])", src, re.S)
    pts = ast.literal_eval(m.group(1))  # literal list of [x, y]; literal_eval, no code exec
    m2 = re.search(r"SEED_PARENT_SCORE = ([0-9.]+)", src)
    return [tuple(p) for p in pts], float(m2.group(1))

SEED_PARENT, SEED_PARENT_SCORE = _extract_seed()

def tri_area(a, b, c):
    return abs((b[0]-a[0])*(c[1]-a[1]) - (c[0]-a[0])*(b[1]-a[1])) / 2.0

def score(points):
    return min(tri_area(*t) for t in combinations(points, 3))

assert abs(score(SEED_PARENT) - SEED_PARENT_SCORE) < 1e-12, "seed parent extraction broke"

def canon(points):
    return sorted((round(x, COORD_DP), round(y, COORD_DP)) for x, y in points)

def parse(raw):
    m = re.search(r"\[\s*\[.*\]\s*\]", raw, re.S)
    if not m:
        return None, "no list found"
    try:
        pts = json.loads(m.group(0))
    except Exception:
        try:
            pts = ast.literal_eval(m.group(0))  # literals only, no code exec
        except Exception as e:
            return None, f"parse: {e}"
    if not isinstance(pts, list):
        return None, "not a list"
    out = []
    for p in pts:
        if not (isinstance(p, (list, tuple)) and len(p) == 2):
            return None, "element not a pair"
        try:
            out.append((float(p[0]), float(p[1])))
        except Exception:
            return None, "non-numeric coordinate"
    return out, None

def validity(points):
    """(viable, valid) per wave-3 SS2. valid does NOT require positive score (5.3)."""
    if points is None:
        return False, False
    if len(points) != N:
        return True, False
    if any(not (0.0 <= x <= 1.0 and 0.0 <= y <= 1.0) for x, y in points):
        return True, False
    c = canon(points)
    if len(set(c)) != N:
        return True, False
    return True, True

def loop_prompt(best_points, best_score):
    """Byte-identical body to the wave-3 runner's loop_prompt (prereg SS2 item 5)."""
    config = json.dumps([[round(x, COORD_DP), round(y, COORD_DP)]
                         for (x, y) in best_points])
    return (
        "You are the proposal step of an evolutionary search for Heilbronn "
        "triangle configurations.\n"
        f"Current best configuration (minimum triangle area = {best_score:.9f}):\n"
        f"{config}\n\n"
        f"Produce a configuration of exactly {N} points with a LARGER minimum "
        "triangle area.\n"
        "The score of a configuration is the SMALLEST area among all "
        f"{N_TRIPLES} triangles formed by choosing 3 of the {N} points; "
        "maximise that smallest area.\n"
        f"MUST hold: exactly {N} points; every coordinate in [0,1]; no two "
        "points identical. Avoid placing any three points on a straight line "
        "— a collinear triple makes the score exactly 0.\n"
        f"Output ONLY the raw Python list of {N} [x, y] lists. No explanation, "
        "no code fences, no other text."
    )

def load_rows():
    if not os.path.exists(LEDGER):
        return []
    return [json.loads(l) for l in open(LEDGER, encoding="utf-8") if l.strip()]

def lineage_state(rows, tier, lineage):
    """Replay acceptance to get the running parent. Strict improvement, evaluator-decided."""
    parent, parent_score = [tuple(p) for p in SEED_PARENT], SEED_PARENT_SCORE
    done = set()
    for r in sorted((r for r in rows if r["tier"] == tier and r["lineage"] == lineage),
                    key=lambda r: r["gen"]):
        done.add(r["gen"])
        if r["valid"] and r["score"] > parent_score + 1e-15:
            parent = [tuple(p) for p in r["points"]]
            parent_score = r["score"]
    return parent, parent_score, done

def cmd_pending():
    rows = load_rows()
    n = 0
    for tier in TIERS:
        for lineage in range(1, LINEAGES + 1):
            parent, pscore, done = lineage_state(rows, tier, lineage)
            for gen in range(1, GENERATIONS + 1):
                if gen in done:
                    continue
                if gen > 1 and (gen - 1) not in done:
                    print(f"### {tier} L{lineage} g{gen}: BLOCKED (gen {gen-1} missing)")
                    break
                print(f"### PENDING tier={tier} lineage={lineage} gen={gen}")
                print(loop_prompt(parent, pscore))
                print("### END")
                n += 1
                break  # only the next generation per lineage is dispatchable
    print(f"# {n} dispatchable calls")

def cmd_record(tier, lineage, gen, raw_file, duration_ms, tokens, tool_uses,
               model_requested, model_reported):
    import datetime
    lineage, gen = int(lineage), int(gen)
    raw = open(raw_file, encoding="utf-8").read()
    rows = load_rows()
    if any(r["tier"] == tier and r["lineage"] == lineage and r["gen"] == gen
           for r in rows):
        sys.exit(f"duplicate: {tier} L{lineage} g{gen} already recorded")
    parent, pscore, _ = lineage_state(rows, tier, lineage)
    pts, err = parse(raw)
    viable, valid = validity(pts)
    row = {
        "arm": "wave4_tiers", "tier": tier, "lineage": lineage, "gen": gen,
        "date": datetime.date.today().isoformat(),
        "model_requested": model_requested, "model_reported": model_reported,
        "tool_uses": int(tool_uses), "duration_ms": int(duration_ms),
        "subagent_tokens": int(tokens),
        "viable": viable, "valid": valid, "parse_error": err,
        "parent_score": round(pscore, SCORE_DP),
    }
    if valid:
        c = canon(pts)
        sc = score(c)
        row["points"] = [list(p) for p in c]
        row["score"] = round(sc, SCORE_DP)
        row["score_delta"] = round(sc - SEED_PARENT_SCORE, SCORE_DP)
        row["echo"] = (c == canon(parent))
        row["accepted"] = sc > pscore + 1e-15
    else:
        row["points"] = None
        row["score"] = None
        row["echo"] = None
        row["accepted"] = False
        row["raw"] = raw[:2000]
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    with open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(row) + "\n")
    print(f"recorded {tier} L{lineage} g{gen}: valid={valid} echo={row['echo']} "
          f"score={row['score']} accepted={row['accepted']}")

def cmd_table():
    rows = load_rows()
    for tier in TIERS:
        t = [r for r in rows if r["tier"] == tier]
        v = [r for r in t if r["valid"]]
        e = [r for r in v if r["echo"]]
        z = [r for r in v if r["score"] == 0.0]
        x = [r for r in t if r["tool_uses"] > 0]
        acc = [r for r in v if r.get("accepted")]
        print(f"{tier:7s} rows={len(t):3d} valid={len(v):3d} echo={len(e):3d} "
              f"zero_score={len(z):2d} accepted={len(acc):2d} tool_excluded={len(x)}")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "pending"
    if cmd == "pending":
        cmd_pending()
    elif cmd == "record":
        cmd_record(*sys.argv[2:11])
    elif cmd == "table":
        cmd_table()
    else:
        sys.exit(f"unknown command {cmd}")
