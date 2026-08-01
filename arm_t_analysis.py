# ============================================================================
# Arm T analysis: scaled paired trace intervention, scored against
# arm_t_preregistration.txt (P-T1..P-T4 + falsifier), nothing else.
#
# Arm definitions, matching the prereg exactly:
#   bare      = arm "bare" rows at N in {13,21,31}, ALL sample ids (old s1.. and
#               new s6+/s11+ share one verbatim prompt, so they pool)
#   trace_v2  = arm "trace" rows with sample_id >= 101 (minimal-diff prompt)
#   pilot     = arm "trace" rows with sample_id <= 100; reported, never pooled
#
# Fisher exact is computed here directly from the hypergeometric tail rather
# than importing scipy.stats, so the analysis has zero dependencies beyond the
# candidates file and the same machinery cannot drift from a library version.
# ============================================================================
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arm_f_repro as A

ROOT = Path(__file__).resolve().parent
NS = [13, 21, 31]

# Registered values, from arm_f_repro.PREDICTIONS: predicted anchor and rival.
PRED = {n: A.PREDICTIONS[n] for n in NS}
WINDOW = 2e-3


def fisher_one_sided(a, b, c, d):
    """P(X >= a) for the 2x2 table [[a,b],[c,d]] under the null, one-sided.

    Row 1 = trace_v2 (a successes, b failures), row 2 = bare. Hypergeometric:
    draw (a+b) samples from a pool of (a+c) successes in (a+b+c+d) total.
    """
    def logC(n, k):
        return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
    n1, n2, k = a + b, c + d, a + c
    total = n1 + n2
    p = 0.0
    for x in range(a, min(n1, k) + 1):
        if k - x > n2:
            continue
        p += math.exp(logC(n1, x) + logC(n2, k - x) - logC(total, k))
    return min(1.0, p)


def rows_for(arm):
    out = []
    for line in (ROOT / "arm_f_candidates.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("n") in NS and r.get("arm") == arm:
            out.append(r)
    return out


def near(v, target):
    return v is not None and abs(v - target) < WINDOW


def tally(rows, n):
    sub = [r for r in rows if r["n"] == n]
    valid = [r for r in sub if r.get("valid")]
    on_pred = [r for r in valid if near(r.get("sum_of_radii"), PRED[n]["value"])]
    rival = [r for r in valid if near(r.get("sum_of_radii"), PRED[n]["rival_argmax"])]
    return {"n_total": len(sub), "valid": len(valid),
            "on_pred": len(on_pred), "rival": len(rival)}


def main():
    bare = rows_for("bare")
    trace_all = rows_for("trace")
    trace_v2 = [r for r in trace_all if r["sample_id"] >= 101]
    pilot = [r for r in trace_all if r["sample_id"] <= 100]

    print("=== ARM T: scaled paired trace intervention ===")
    print(f"pilot (never pooled): {len(pilot)} rows, reported separately\n")

    pooled = {"t": [0, 0, 0, 0], "b": [0, 0, 0, 0]}  # total, valid, on_pred, rival
    per_n_validity_direction = []
    for n in NS:
        t, b = tally(trace_v2, n), tally(bare, n)
        for key, agg in (("t", t), ("b", b)):
            pooled[key][0] += agg["n_total"]
            pooled[key][1] += agg["valid"]
            pooled[key][2] += agg["on_pred"]
            pooled[key][3] += agg["rival"]
        per_n_validity_direction.append(
            (t["valid"] / t["n_total"] if t["n_total"] else 0.0)
            >= (b["valid"] / b["n_total"] if b["n_total"] else 0.0))
        print(f"N={n}:  trace_v2 valid {t['valid']}/{t['n_total']}  on-pred {t['on_pred']}"
              f"  rival {t['rival']}   |   bare valid {b['valid']}/{b['n_total']}"
              f"  on-pred {b['on_pred']}  rival {b['rival']}")

    tt, bt = pooled["t"], pooled["b"]
    p_valid = fisher_one_sided(tt[1], tt[0] - tt[1], bt[1], bt[0] - bt[1])
    # P-T2 / P-T3 among valid only, as registered.
    p_onpred = fisher_one_sided(tt[2], tt[1] - tt[2], bt[2], bt[1] - bt[2])
    # rival: prediction is trace LOWER, so test bare >= trace by swapping rows.
    p_rival = fisher_one_sided(bt[3], bt[1] - bt[3], tt[3], tt[1] - tt[3])

    print(f"\npooled trace_v2: valid {tt[1]}/{tt[0]}, on-pred {tt[2]}/{tt[1]}, rival {tt[3]}/{tt[1]}")
    print(f"pooled bare:     valid {bt[1]}/{bt[0]}, on-pred {bt[2]}/{bt[1]}, rival {bt[3]}/{bt[1]}")
    print(f"\nP-T1 validity:   direction-per-N {per_n_validity_direction}, pooled Fisher p = {p_valid:.4f}"
          f"  -> {'CONFIRMED' if all(per_n_validity_direction) and p_valid < 0.05 else 'NOT CONFIRMED'}")
    print(f"P-T2 rival:      one-sided Fisher (bare > trace) p = {p_rival:.4f} (directional prereg)")
    print(f"P-T3 anchor:     one-sided Fisher (trace > bare on-pred) p = {p_onpred:.4f} (directional prereg)")

    # P-T4 faithfulness on trace_v2 only.
    scoreable = matched = 0
    for r in trace_v2:
        f = r.get("faithful")
        if f in ("match", "mismatch"):
            scoreable += 1
            matched += f == "match"
    rate = matched / scoreable if scoreable else float("nan")
    print(f"P-T4 faithfulness: {matched}/{scoreable} scoreable match"
          f" ({100 * rate:.0f}%) -> {'CONFIRMED' if scoreable and rate >= 0.9 else 'NOT CONFIRMED'}")

    # Falsifier, both readings. The prereg (line: "trace_v2 validity <= bare at
    # 2+ of 3 N") is decidable by an operator glyph; the original version of this
    # script silently evaluated strict < (a tie counted as direction-held and not
    # as a falsifier cell — the same tie read favourably twice). Panel finding F8.
    # Both readings are now computed and printed; the registered text is the
    # tie-inclusive one.
    strict_down = sum(1 for d in per_n_validity_direction if not d)
    tie_or_down = 0
    for n in NS:
        t, b = tally(trace_v2, n), tally(bare, n)
        tr = t["valid"] / t["n_total"] if t["n_total"] else 0.0
        br = b["valid"] / b["n_total"] if b["n_total"] else 0.0
        tie_or_down += tr <= br
    print(f"\nFalsifier (registered, tie-inclusive <=): {tie_or_down}/3 cells"
          f" -> {'TRIGGERED' if tie_or_down >= 2 else 'not triggered'}")
    print(f"Falsifier (strict <, as originally coded): {strict_down}/3 cells"
          f" -> {'TRIGGERED' if strict_down >= 2 else 'not triggered'}")
    if tie_or_down >= 2:
        print("Registered reading TRIGGERED: pilot validity effect attributed to"
              " the bundled rewording, reported as such per prereg.")


if __name__ == "__main__":
    main()
