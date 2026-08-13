# ============================================================================
# Precision-cliff Future Work item 8: reproducibility repair, and item 3's
# forecast put out of sample.
#
# WHY THIS EXISTS
# The paper says of itself (S4): "Arms A-D are not reproducible as run. The
# Claude proposers are undated aliases (`claude-haiku` / `claude-sonnet` in the
# jsonl) invoked through an agent runtime at default, unlogged sampling
# settings." The paper calls repairing that its highest-priority revision
# experiment.
#
# WHAT CAN AND CANNOT BE REPAIRED, stated up front so the log is not oversold.
# The original arms ran through Claude Code subagents on a Max plan, not through
# the HTTP API. That runtime exposes a model ALIAS and no sampling controls.
# So:
#   REPAIRABLE, and repaired here:
#     - prompt text pinned and SHA-256 hashed, one hash per N
#     - every raw proposer output stored verbatim, parsed or not
#     - run date recorded, and the alias -> dated-id mapping in force on that
#       date recorded alongside it
#     - scoring, validity, and recipe classification all deterministic and local
#     - registered predictions written before any proposal was sampled (below)
#   NOT REPAIRABLE through this runtime, and disclosed rather than papered over:
#     - temperature / top_p / top_k: not exposed by the agent runtime
#     - the alias->weights binding is a promise, not a hash; the alias can be
#       repointed and old runs cannot be re-executed against the old weights
#     - the subagent inherits a system prompt and user-level instruction files
#       that are not part of the task prompt and are not held fixed across time
# That third item is the substantive methodological point: an agent runtime
# cannot be made reproducible from inside itself. Any LLM-evolution study built
# on one inherits this. It is a property of the harness class, not an oversight.
#
# REGISTERED PREDICTIONS (written before any proposal was sampled; the forecast
# comes from n_sweep_forecast.py, which was fitted on N=23/26/27 only, so every
# N below is out of sample):
#   P1  N=13 traps at 1.6250000  (13/(2*4); nearest square is 16, count falls short)
#   P2  N=31 traps at 2.5833333  (31/(2*6))
#   P3  N=17 converges on 2.0517767  (4x4 grid + 1 filler)
#   P4  N=37 converges on 3.0345178  (6x6 grid + 1 filler) - prime, and predicted
#       CLEAN, which contradicts the paper's own guess that primes near 30 are
#       where no grid parameterisation is natural
#   P5  N=35 lands on 2.9166667, where truncation happens to BE the recipe
#       optimum - a trap that is indistinguishable from convergence by value
#       alone, and separable only by structure
# P1/P2 are the discriminating pair: a model that picked the BEST recipe rather
# than the nearest-square one would return 1.7761424 and 2.7485281 instead.
# ============================================================================
import ast
import hashlib
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SQRT2 = math.sqrt(2.0)
FILLER = SQRT2 - 1.0

RUN_DATE = "2026-07-30"
# Alias -> dated id in force on RUN_DATE, recorded because the runtime accepts
# only the alias. This is provenance, not a pin: nothing here prevents the alias
# being repointed later.
ALIAS_MAP = {"haiku": "claude-haiku-4-5-20251001"}
PROPOSER_ALIAS = "haiku"

# Verbatim A.5 zero-shot probe statement, with N parameterised, plus A.10's
# no-code line. The paper's loop prompt differs only by the serialized parent
# block; the zero-shot form is used because the paper's own headline result is
# that the loop reduces to best-of-N, so zero-shot sampling measures the same
# attractor at a fraction of the invocations.
PROMPT_TEMPLATE = """Pack exactly {n} non-overlapping circles inside the unit square [0,1]x[0,1] so that the sum of their radii is as large as possible.
MUST hold: exactly {n} circles; every circle fully inside the unit square [0,1]x[0,1] (x-r >= 0, x+r <= 1, same for y); no two circles overlap (distance between centers >= sum of the two radii; touching is allowed).
Do not write or execute code - construct the packing by reasoning alone.
Output ONLY the raw Python list of {n} [x, y, r] lists. No explanation, no code fences, no other text."""

TARGET_N = [13, 17, 21, 31, 35, 37, 43]


def prompt_for(n):
    return PROMPT_TEMPLATE.format(n=n)


def prompt_hash(n):
    return hashlib.sha256(prompt_for(n).encode("utf-8")).hexdigest()


# ------------------------------------------------------------------ scoring

def parse_packing(raw):
    """Extract the outermost bracketed list, matching A.5's stated parser.

    Code fences are stripped and the outermost [...] taken before literal_eval,
    so a fenced-but-otherwise-correct output is not counted as a failure. Any
    other malformed output returns (None, reason) and is logged, never dropped.
    """
    if raw is None:
        return None, "no_output"
    text = re.sub(r"```[a-zA-Z]*", "", raw).replace("```", "")
    start, end = text.find("["), text.rfind("]")
    if start < 0 or end <= start:
        return None, "no_bracketed_list"
    try:
        val = ast.literal_eval(text[start:end + 1])
    except Exception as exc:
        return None, f"literal_eval_failed:{type(exc).__name__}"
    if not isinstance(val, (list, tuple)):
        return None, "not_a_list"
    out = []
    for row in val:
        if not isinstance(row, (list, tuple)) or len(row) != 3:
            return None, "row_not_xyr"
        try:
            out.append(tuple(float(v) for v in row))
        except (TypeError, ValueError):
            return None, "row_not_numeric"
    return out, None


def validate(circles, n, tol=1e-6):
    """Exactly n circles, all inside the unit square, none overlapping.

    The default is the DECLARED PRIMARY tolerance (1e-6), so a reader who runs
    this file with defaults reproduces the paper's headline numbers. The strict
    1e-9 gate is still computed for every row by ingest(), which passes both
    explicitly; it is a second reported column, never the default.
    """
    if len(circles) != n:
        return False, f"count_{len(circles)}_expected_{n}"
    for x, y, r in circles:
        if r <= 0:
            return False, "nonpositive_radius"
        if x - r < -tol or x + r > 1 + tol or y - r < -tol or y + r > 1 + tol:
            return False, "outside_square"
    for i in range(len(circles)):
        xi, yi, ri = circles[i]
        for j in range(i + 1, len(circles)):
            xj, yj, rj = circles[j]
            if math.hypot(xi - xj, yi - yj) < ri + rj - tol:
                return False, "overlap"
    return True, None


def score(circles):
    return sum(r for _, _, r in circles)


# ------------------------------------------------- recipe classification

def recipe_value(k, m):
    return k / 2.0 + m * FILLER / (2.0 * k)


def truncated_value(k, n):
    return n / (2.0 * k)


def classify(circles, n, tol=2e-3, exact_tol=2e-6):
    """Name the construction by VALUE and by STRUCTURE, separately.

    Value alone cannot separate a trap from convergence at N=35, where the two
    coincide, so radii are inspected as well: the recipe uses at most two
    distinct radii, 1/(2k) and (sqrt2-1)/(2k), in a k^2 : m split.

    TWO tolerances, deliberately. Proposers emit anywhere from 4 to 17 decimal
    places, and a single tight window scores a 4-decimal rendering of the SAME
    construction as a different one - at n=31 a proposer wrote r=0.0833 and
    summed to 2.5823 against an exact 2.5833333. The loose window decides which
    construction was built; the exact window separately records whether it was
    rendered to full precision, which is what a six-decimal convergence claim
    actually rests on.
    """
    s = score(circles)
    by_value, exact = [], []
    for k in range(2, 10):
        if n >= k * k and n - k * k <= (k - 1) ** 2:
            d = abs(s - recipe_value(k, n - k * k))
            if d < tol:
                by_value.append(f"clean_k{k}_m{n - k * k}")
            if d < exact_tol:
                exact.append(f"clean_k{k}_m{n - k * k}")
        if n < k * k:
            d = abs(s - truncated_value(k, n))
            if d < tol:
                by_value.append(f"truncated_k{k}")
            if d < exact_tol:
                exact.append(f"truncated_k{k}")

    radii = sorted({round(r, 6) for _, _, r in circles})
    structure = "other"
    if len(radii) == 1:
        for k in range(2, 10):
            if abs(radii[0] - 1.0 / (2 * k)) < tol:
                structure = f"uniform_grid_k{k}"
    elif len(radii) == 2:
        for k in range(2, 10):
            big, small = 1.0 / (2 * k), FILLER / (2 * k)
            if abs(radii[1] - big) < tol and abs(radii[0] - small) < tol:
                n_big = sum(1 for _, _, r in circles if abs(r - big) < tol)
                structure = f"grid_plus_filler_k{k}_grid{n_big}_fill{n - n_big}"
    if structure == "other" and len(radii) == 1:
        # A single radius that is not 1/(2k) still tells us the shape: a p x q
        # grid or a hex layout caps every circle at the same value. Record the
        # implied cell pitch so these are distinguishable from noise.
        structure = f"uniform_r{radii[0]:.6f}_pitch{1.0 / (2 * radii[0]):.3f}"
    return {"sum_of_radii": s, "value_matches": by_value,
            "exact_matches": exact, "distinct_radii": len(radii),
            "structure": structure}


# ------------------------------------------------------------ registration

PREDICTIONS = {
    13: {"branch": "truncate", "value": 1.6250000, "rival_argmax": 1.7761424},
    21: {"branch": "truncate", "value": 2.1000000, "rival_argmax": 2.2588835},
    43: {"branch": "truncate", "value": 3.0714286, "rival_argmax": 3.2416246},
    17: {"branch": "extend", "value": 2.0517767, "rival_argmax": 2.0517767},
    31: {"branch": "truncate", "value": 2.5833333, "rival_argmax": 2.7485281},
    35: {"branch": "truncate", "value": 2.9166667, "rival_argmax": 2.9166667},
    37: {"branch": "extend", "value": 3.0345178, "rival_argmax": 3.0345178},
}


METHOD_RE = re.compile(r"METHOD:\s*(.+)")
DIMS_RE = re.compile(r"(\d+)\s*(?:x|×)\s*(\d+)")
ROWSCOLS_RE = re.compile(r"(\d+)\s*rows?\s*(?:x|×|by|and)?\s*(\d+)?\s*col", re.I)


def observed_signature(circles, tol=1e-6):
    """Coarse layout signature recovered from the coordinates alone."""
    xs = sorted({round(x, 6) for x, _, _ in circles})
    ys = sorted({round(y, 6) for _, y, _ in circles})
    per_row = sorted(sum(1 for _, y, _ in circles if abs(y - yy) < tol) for yy in ys)
    return {"cols": len(xs), "rows": len(ys), "per_row": per_row}


def trace_faithfulness(raw, circles):
    """Compare the proposer's SELF-REPORTED construction to what it actually emitted.

    This is the check the chain-of-thought faithfulness literature cannot run:
    those papers estimate faithfulness without ground truth, whereas here the
    emitted coordinates ARE the ground truth for what was built. The comparison
    is deliberately coarse - it asks only whether the row/column counts named in
    the METHOD line appear in the layout actually produced - because a stricter
    point-set match would call two correct descriptions of the same 21-circle
    layout ("5x5 minus 4 corners" and "4x5 plus 1") a disagreement.
    """
    m = METHOD_RE.search(raw or "")
    if not m:
        return {"method_claim": None, "faithful": None}
    claim = m.group(1).strip()
    sig = observed_signature(circles)
    dims = [tuple(int(g) for g in d) for d in DIMS_RE.findall(claim)]
    rc = ROWSCOLS_RE.search(claim)
    if rc and rc.group(2):
        dims.append((int(rc.group(1)), int(rc.group(2))))
    hexish = bool(re.search(r"hex|triangul|offset|stagger", claim, re.I))
    verdict = "unscored"
    if dims:
        got = {sig["rows"], sig["cols"]}
        verdict = "match" if any(a in got or b in got for a, b in dims) else "mismatch"
    elif hexish:
        verdict = "match" if len(set(sig["per_row"])) > 1 else "mismatch"
    return {"method_claim": claim, "claimed_dims": dims, "claim_hexlike": hexish,
            "observed_rows": sig["rows"], "observed_cols": sig["cols"],
            "faithful": verdict}


def ingest(samples, out_name="arm_f_candidates.replay.jsonl"):
    """samples: list of {n, sample_id, raw}. Writes one jsonl row per invocation.

    Every invocation produces a row, including unparsed ones. Nothing is dropped
    on the floor - a silently discarded failure is how validity rates get
    inflated.
    """
    rows = []
    for s in samples:
        n, raw = s["n"], s.get("raw")
        circles, parse_err = parse_packing(raw)
        row = {
            "reconstructed": False,
            "run_date": RUN_DATE,
            "proposer_alias": PROPOSER_ALIAS,
            "proposer_dated_id_on_run_date": ALIAS_MAP[PROPOSER_ALIAS],
            "sampling_params": None,
            "sampling_params_note": "not exposed by the agent runtime; see header",
            "n": n,
            "arm": s.get("arm", "bare"),
            "sample_id": s["sample_id"],
            "prompt_sha256": prompt_hash(n),
            "raw_output": raw,
            "raw_len": len(raw) if raw else 0,
            "parse_error": parse_err,
            "valid": False,
            "invalid_reason": None,
        }
        if circles is not None:
            # TWO tolerances, both reported, neither chosen after seeing results.
            # Proposers print 6-8 decimals; a tangency written at 8 decimals
            # misses by ~5e-9, so a 1e-9 gate rejects correct constructions for
            # rounding alone. 1e-6 is the primary because it sits far below the
            # ~1e-2 spacing between rival constructions and far above decimal
            # noise, so it cannot manufacture or destroy a prediction hit.
            strict_ok, strict_why = validate(circles, n, tol=1e-9)
            ok, why = validate(circles, n, tol=1e-6)
            row["valid"] = ok
            row["invalid_reason"] = why
            row["valid_strict_1e9"] = strict_ok
            row["invalid_reason_strict_1e9"] = strict_why
            row["circles"] = circles
            if ok:
                row.update(classify(circles, n))
                row.update(trace_faithfulness(raw, circles))
        rows.append(row)

    path = ROOT / out_name
    with path.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    return rows, path


def report(rows):
    print(f"run_date={RUN_DATE}  proposer={PROPOSER_ALIAS} "
          f"({ALIAS_MAP[PROPOSER_ALIAS]} on that date)  sampling=UNLOGGED (runtime)")
    print(f"{len(rows)} invocations, all rows written including failures\n")
    arms = sorted({r["arm"] for r in rows})
    for arm in arms:
      print(f"--- arm: {arm} ---")
      for n in TARGET_N:
        sub = [r for r in rows if r["n"] == n and r["arm"] == arm]
        if not sub:
            continue
        valid = [r for r in sub if r["valid"]]
        pred = PREDICTIONS[n]
        hits = [r for r in valid if abs(r["sum_of_radii"] - pred["value"]) < 2e-3]
        exact = [r for r in valid if abs(r["sum_of_radii"] - pred["value"]) < 2e-6]
        rival = [r for r in valid
                 if abs(r["sum_of_radii"] - pred["rival_argmax"]) < 2e-3
                 and abs(pred["rival_argmax"] - pred["value"]) > 1e-9]
        best = max((r["sum_of_radii"] for r in valid), default=None)
        strict = [r for r in sub if r.get("valid_strict_1e9")]
        bad = {}
        for r in sub:
            if not r["valid"]:
                k = r["parse_error"] or r["invalid_reason"]
                bad[k] = bad.get(k, 0) + 1
        print(f"N={n:>3}  predicted {pred['branch']:<8} {pred['value']:.7f}"
              f"   valid {len(valid)}/{len(sub)}"
              f"  (at 1e-9: {len(strict)}/{len(sub)})"
              + (f"   failures {bad}" if bad else ""))
        print(f"        on-prediction {len(hits)}/{max(len(valid),1)}"
              f"  (of which exact to 2e-6: {len(exact)})"
              f"   rival-argmax({pred['rival_argmax']:.7f}) {len(rival)}"
              f"   best observed {best if best is None else round(best, 7)}")
        struct = {}
        for r in valid:
            struct[r["structure"]] = struct.get(r["structure"], 0) + 1
        if struct:
            print(f"        structures: {struct}")
        print()


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "prompts":
        payload = {str(n): {"prompt": prompt_for(n), "sha256": prompt_hash(n)}
                   for n in TARGET_N}
        (ROOT / "arm_f_prompts.json").write_text(json.dumps(payload, indent=2))
        for n in TARGET_N:
            print(f"N={n}  sha256={prompt_hash(n)}")
        print(f"\nwrote {ROOT / 'arm_f_prompts.json'}")
        return
    src = ROOT / "arm_f_raw.json"
    if not src.exists():
        sys.exit(f"no {src}; collect proposer outputs into it first "
                 f"(list of {{n, sample_id, raw}})")
    samples = json.loads(src.read_text(encoding="utf-8"))
    rows, path = ingest(samples)
    report(rows)
    print(f"wrote {path}")
    compare_to_ledger(rows)


# Fields whose values must agree row-for-row between a replay and the
# checked-in ledger for the replay to count as a reproduction. Volatile
# fields (raw float rendering, key order, later-added annotations) are
# deliberately excluded: a MISMATCH here means the science moved, not the
# formatting.
COMPARE_FIELDS = ("valid", "valid_strict_1e9", "parse_error",
                  "invalid_reason", "sum_of_radii", "structure")


def compare_to_ledger(rows, ledger_name="arm_f_candidates.jsonl"):
    """Diff the replay against the checked-in ledger without touching it.

    The replay writes only to *.replay.jsonl; the canonical ledger is
    read-only here, so running this script never dirties a fresh clone.
    """
    ledger_path = ROOT / ledger_name
    if not ledger_path.exists():
        print(f"\nno checked-in ledger at {ledger_path}; comparison skipped")
        return
    ledger = {}
    with ledger_path.open(encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                r = json.loads(line)
                ledger[(r["arm"], r["n"], r["sample_id"])] = r
    replay = {(r["arm"], r["n"], r["sample_id"]): r for r in rows}
    missing = sorted(set(ledger) - set(replay))
    extra = sorted(set(replay) - set(ledger))
    diffs = []
    for key in sorted(set(ledger) & set(replay)):
        a, b = ledger[key], replay[key]
        for f in COMPARE_FIELDS:
            va, vb = a.get(f), b.get(f)
            if isinstance(va, float) and isinstance(vb, float):
                if abs(va - vb) > 1e-9:
                    diffs.append((key, f, va, vb))
            elif va != vb:
                diffs.append((key, f, va, vb))
    print(f"\n--- ledger comparison ({ledger_name}) ---")
    if not (missing or extra or diffs):
        print(f"MATCH: {len(replay)} rows agree with the checked-in ledger "
              f"on {', '.join(COMPARE_FIELDS)}")
        return
    print("MISMATCH:")
    for key in missing:
        print(f"  row {key} in ledger but not in replay")
    for key in extra:
        print(f"  row {key} in replay but not in ledger")
    for key, f, va, vb in diffs[:40]:
        print(f"  row {key} field {f!r}: ledger={va!r} replay={vb!r}")
    if len(diffs) > 40:
        print(f"  ... and {len(diffs) - 40} more field differences")


if __name__ == "__main__":
    main()
