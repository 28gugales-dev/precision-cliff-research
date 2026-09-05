# Arm B2 runner -- the optimizer alone at larger trap cells.
# Executes arm_b2_preregistration.txt exactly: builds the baseline "rows" (arm_b_baseline.py
# with N, SEED and the RESTARTS constant substituted, nothing else) and scores them through arm
# CL's registered pipeline unmodified (arm_cl_analysis: python -I -S, the fixed driver, one core
# per subprocess with OMP/MKL/OPENBLAS pinned to 1, arm-F parsing and scoring, validity at 1e-9
# and 1e-6 with 1e-6 primary, section 2.4's clearance rule). No model is called.
#
# Two readings, both frozen in the registration before any row was sampled:
#   primary   -- budget-matched, inside arm CL's 120 s wall: N = 57 at RESTARTS = 7,
#                N = 59 at RESTARTS = 5 (floor(0.75 * 120 / worst-seed restart cost)).
#   secondary -- restart-matched, off-pipeline: N = 57, 73, 91 at the published RESTARTS = 50
#                with the wall lifted to 3600 s. Carries no claim that arm B's rows are scored
#                like the model-written programs; the report says so in the file.
#
# Verdicts are computed from the counts by this script, never written by hand.
#
# INSTRUMENT. The registration pins the machine it was calibrated on: 22 cores, 4 concurrent
# scoring workers, numpy 2.4.6, scipy 1.17.1. This runner records what it actually ran on and
# sets instrument_matches_registration in the report. A mismatch does not silently proceed:
# the frozen restart counts were measured from that machine's worst seed, so on a smaller box
# the 120 s wall can bin rows as timeouts that the registered instrument would have scored.
# Pass --off-instrument to run anyway; the flag is recorded in the report and any such run is
# a calibration run, not the registered arm.
#
# Writes arm_b2_collect.jsonl (the substituted sources, verbatim) and arm_b2_report.json,
# the artifacts named in advance. Neither arm B's nor the bridge's artifacts are opened for
# writing. --smoke writes to arm_b2_smoke_* and
# --off-instrument to arm_b2_offinstrument_*; only a run on the registered instrument may
# claim the artifact names the registration fixed in advance.
import argparse
import hashlib
import json
import math
import os
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import arm_cl_analysis as cl  # noqa: E402
from arm_f_repro import truncated_value  # noqa: E402

TEMPLATE_SHA_REGISTERED = "298ba71c9f20614ef1d4e0008a5a6e6a6c208d61b873ce135d926e2571799f8c"
RESTARTS_LITERAL = "RESTARTS = 50"
SEEDS = list(range(1, 16))
FLOOR = 5  # five valid outputs per cell; below it the cell is UNSCOREABLE

# Frozen in the registration from the per-seed timing probes, worst seed governing.
READINGS = {
    "primary": {
        "cells": {57: 7, 59: 5},          # N -> RESTARTS
        "timeout_s": 120,
        "on_pipeline": True,
        "note": "budget-matched; arm CL's 120 s wall, RESTARTS = floor(0.75 * 120 / worst-seed "
                "restart cost) frozen in the registration",
    },
    "secondary": {
        "cells": {57: 50, 73: 50, 91: 50},
        "timeout_s": 3600,
        "on_pipeline": False,
        "note": "restart-matched; the published RESTARTS = 50 with the wall lifted to 3600 s. "
                "OFF-PIPELINE: this leaves arm CL's 120 s pipeline and can carry no claim that "
                "arm B's rows are scored like the model-written programs",
    },
}

# Registered instrument (arm_b2_preregistration.txt, INSTRUMENT).
INSTRUMENT = {"cpu_count": 22, "max_exec_workers": 4, "numpy": "2.4.6", "scipy": "1.17.1"}


def anchor(n):
    """Truncation anchor T(k*, N) = N / (2 k*), k* = ceil(sqrt(N)) -- the k the truncation
    branch uses at these cells. Recomputed in closed form, never read from a literal."""
    return truncated_value(math.ceil(math.sqrt(n)), n)


def instrument():
    np_v, sp_v = cl.versions()
    got = {"cpu_count": os.cpu_count(), "max_exec_workers": cl.MAX_EXEC_WORKERS,
           "numpy": np_v, "scipy": sp_v}
    return got, got == INSTRUMENT


def build_rows(reading, seeds, template, template_sha):
    rows = []
    for n, restarts in READINGS[reading]["cells"].items():
        src_n = (template.replace("__N__", str(n))
                         .replace(RESTARTS_LITERAL, f"RESTARTS = {restarts}"))
        for seed in seeds:
            rows.append({"tier": "baseline", "reading": reading, "n": n, "sample_id": seed,
                         "restarts": restarts, "raw": src_n.replace("__SEED__", str(seed)),
                         "template_sha256": template_sha})
    return rows


def score_cell(reading, n, cell_rows, timeout_s):
    """Scores one cell through arm CL's pipeline, timing it."""
    restarts = READINGS[reading]["cells"][n]
    print(f"[{reading}] n={n}: {len(cell_rows)} rows, RESTARTS = {restarts}, "
          f"{timeout_s} s wall, {cl.MAX_EXEC_WORKERS} concurrent", flush=True)
    t0 = time.perf_counter()
    scored = cl.score_all(cell_rows, timeout_s=timeout_s)
    wall = round(time.perf_counter() - t0, 3)
    bins = Counter(s["bin"] for s in scored)
    valid = [s for s in scored if s["bin"] == "valid"]
    cleared = [s for s in valid if s["cleared"]]
    best = max((s["sum"] for s in valid), default=None)
    a = anchor(n)
    cell = {
        "restarts": restarts, "timeout_s": timeout_s, "wall_clock_s": wall,
        "sampled": len(cell_rows), "bins": dict(bins),
        "n_valid_1e6": len(valid),
        "n_valid_1e9": sum(1 for s in valid if s["valid_1e9"]),
        "n_cleared": len(cleared),
        "clear_rate": (len(cleared) / len(valid)) if valid else None,
        "underpowered": len(valid) < FLOOR,
        "argmax_closed_form": round(cl.ARGMAX[n], 9),
        "anchor_T_kstar_N": round(a, 9),
        "best_sum": round(best, 9) if best is not None else None,
        "best_exceeds_anchor": (best is not None and best > a),
        "sums": sorted(round(s["sum"], 9) for s in valid),
        "cleared_sums": sorted(round(s["sum"], 9) for s in cleared),
        "k_struct_dist": dict(Counter(s["k_struct"] for s in valid)),
    }
    print(f"[{reading}] n={n}: bins {dict(bins)}, valid {cell['n_valid_1e6']} "
          f"(1e-9: {cell['n_valid_1e9']}), cleared {cell['n_cleared']}, best {cell['best_sum']}, "
          f"argmax {cell['argmax_closed_form']}, anchor {cell['anchor_T_kstar_N']}"
          f"{'  UNSCOREABLE (below the five-valid floor)' if cell['underpowered'] else ''}"
          f"  [{wall} s]", flush=True)
    return cell


def pooled(reading, cells):
    valid = sum(c["n_valid_1e6"] for c in cells.values())
    cleared = sum(c["n_cleared"] for c in cells.values())
    at20 = sum(1 for c in cells.values()
               if not c["underpowered"] and c["clear_rate"] is not None
               and c["clear_rate"] >= 0.20)
    any_clear = sum(1 for c in cells.values()
                    if not c["underpowered"] and c["n_cleared"] > 0)
    over_anchor = sum(1 for c in cells.values() if c["best_exceeds_anchor"])
    return {"sampled": sum(c["sampled"] for c in cells.values()), "valid": valid,
            "cleared": cleared, "cells_registered": len(READINGS[reading]["cells"]),
            "cells_scored": len(cells), "cells_at_20pct": at20,
            "cells_with_any_clearance": any_clear, "cells_best_over_anchor": over_anchor}


def compute_verdicts(report):
    """Every verdict comes from the counts. A reading whose registered cells are not all
    scored yet is marked INCOMPLETE and claims nothing: the registered denominator is the
    registered cell count, never the number of cells that happen to be on disk."""
    verdicts = {}
    readings = report["readings"]
    partial = {r: readings[r]["pooled"]["cells_scored"] < readings[r]["pooled"]["cells_registered"]
               for r in readings}
    mark = lambda r, t: (f"INCOMPLETE ({readings[r]['pooled']['cells_scored']} of "
                         f"{readings[r]['pooled']['cells_registered']} cells scored) -- " + t
                         if partial[r] else t)
    if "primary" in readings:
        p = readings["primary"]["pooled"]
        n_cells = p["cells_registered"]
        scoreable = sum(1 for c in readings["primary"]["cells"].values()
                        if not c["underpowered"])
        if scoreable == 0:
            v = (f"UNSCOREABLE (0 of {n_cells} primary cells reach the five-valid floor; "
                 f"a cell under the floor claims nothing on its own)")
        elif p["cells_at_20pct"] >= n_cells:
            v = (f"P-B2-1 holds (clears >= 20% of valid outputs at {n_cells} of {n_cells} "
                 f"primary cells): arm B's verdict map carries to the larger trap cells")
        else:
            v = (f"P-B2-2 holds (clears at {p['cells_at_20pct']} of {n_cells} primary cells, "
                 f"below {n_cells} of {n_cells}): contribution 1 is scoped in the paper to the "
                 f"cells where it was measured, and the scoping sentence is written whether or "
                 f"not the secondary reading rescues the arm")
        verdicts["primary"] = mark("primary", v)
    if "secondary" in readings:
        s = readings["secondary"]["pooled"]
        n_cells = s["cells_registered"]
        verdicts["S-B2-1"] = mark("secondary", (
            f"{'HOLDS' if s['cells_with_any_clearance'] >= 2 else 'does not hold'} "
            f"(clearance at {s['cells_with_any_clearance']} of {n_cells} cells at 50 "
            f"restarts; at >= 20%: {s['cells_at_20pct']} of {n_cells})"))
        verdicts["S-B2-2"] = mark("secondary", (
            f"{'HOLDS' if s['cells_best_over_anchor'] >= n_cells else 'does not hold'} "
            f"(best sum exceeds the anchor T(k*, N) at {s['cells_best_over_anchor']} of "
            f"{n_cells} cells)"))
    if len(readings) == 2:
        p, s = readings["primary"]["pooled"], readings["secondary"]["pooled"]
        fired = p["cleared"] == 0 and s["cleared"] == 0 and (p["valid"] + s["valid"]) > 0
        t = (f"{'TRIGGERED' if fired else 'not triggered'} (primary cleared {p['cleared']} of "
             f"{p['valid']} valid, secondary cleared {s['cleared']} of {s['valid']}). "
             + ("The generalization fails outright and the paper says so in contribution 1 and "
                "the abstract, not only in limitations." if fired else
                "The falsifier fires only when both readings clear nothing."))
        verdicts["F-B2"] = ("INCOMPLETE -- " + t if any(partial.values()) else t)
    return verdicts


def save(report, path):
    """Rewrites the report after every cell, so a killed run keeps the cells it finished."""
    for reading, block in report["readings"].items():
        block["pooled"] = pooled(reading, block["cells"])
    report["verdicts"] = compute_verdicts(report)
    path.write_text(json.dumps(report, indent=1), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reading", choices=["primary", "secondary", "both"], default="both")
    ap.add_argument("--off-instrument", action="store_true",
                    help="run although the machine is not the one the registration pins; "
                         "recorded in the report, and such a run is calibration, not the arm")
    ap.add_argument("--smoke", action="store_true",
                    help="mechanical check only: 2 seeds, 60 s wall, arm_b2_smoke_* outputs; "
                         "never a registered run")
    ap.add_argument("--resume", action="store_true",
                    help="keep the cells an earlier run already scored into the same report "
                         "file and score only the ones missing; the secondary reading runs "
                         "for hours, so a killed run should not cost them")
    args = ap.parse_args()

    template = (HERE / "arm_b_baseline.py").read_text(encoding="utf-8")
    template_sha = hashlib.sha256(template.encode("utf-8")).hexdigest()
    assert template_sha == TEMPLATE_SHA_REGISTERED, (
        f"arm_b_baseline.py drifted from the registered template "
        f"({template_sha} != {TEMPLATE_SHA_REGISTERED}); a needed edit voids the arm")
    assert template.count(RESTARTS_LITERAL) == 1, "the RESTARTS constant is not substitutable"

    got, matches = instrument()
    print(f"instrument: {got}", flush=True)
    if not matches:
        print(f"INSTRUMENT MISMATCH -- registration pins {INSTRUMENT}", flush=True)
        if not (args.off_instrument or args.smoke):
            print("refusing to sample: the frozen restart counts were measured on the "
                  "registered machine's worst seed, so this box can bin rows as timeouts that "
                  "the registered instrument would have scored. Re-run there, or pass "
                  "--off-instrument to produce a calibration run that is not the arm.")
            return 2

    # arm CL registered the three cells 13/21/31; these cells are new, so their family argmax
    # is added by the same closed form the pipeline already uses. No pipeline code is edited.
    for n in set(READINGS["primary"]["cells"]) | set(READINGS["secondary"]["cells"]):
        cl.ARGMAX.setdefault(n, cl.argmax_closed_form(n))

    seeds = SEEDS[:2] if args.smoke else SEEDS
    readings = ["primary", "secondary"] if args.reading == "both" else [args.reading]
    # Only a run on the registered instrument may claim the artifact names the
    # registration fixed in advance; anything else writes beside them.
    prefix = "arm_b2" if (matches and not args.smoke) else (
        "arm_b2_smoke" if args.smoke else "arm_b2_offinstrument")
    report_path = HERE / f"{prefix}_report.json"

    rows = []
    for reading in readings:
        rows += build_rows(reading, seeds, template, template_sha)
    with open(HERE / f"{prefix}_collect.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print(f"template sha256 {template_sha[:12]}; {len(rows)} rows -> {prefix}_collect.jsonl",
          flush=True)

    report = {"arm": "B2", "registration": "arm_b2_preregistration.txt",
              "template_sha256": template_sha, "seeds": seeds,
              "floor_valid_per_cell": FLOOR, "instrument": got,
              "instrument_registered": INSTRUMENT,
              "instrument_matches_registration": matches,
              "off_instrument_run": bool(args.off_instrument and not matches),
              "smoke": bool(args.smoke), "readings": {}}
    if args.resume and report_path.exists():
        prior = json.loads(report_path.read_text(encoding="utf-8"))
        assert prior.get("template_sha256") == template_sha, "resuming across a template change"
        assert prior.get("seeds") == seeds, "resuming across a seed change"
        report["readings"] = prior.get("readings", {})
        done = {r: sorted(b["cells"]) for r, b in report["readings"].items()}
        print(f"resuming; already scored: {done}", flush=True)
        save(report, report_path)  # recompute the carried pooled counts and verdicts now

    for reading in readings:
        spec = READINGS[reading]
        timeout_s = 60 if args.smoke else spec["timeout_s"]
        block = report["readings"].setdefault(
            reading, {"note": spec["note"], "on_pipeline": spec["on_pipeline"],
                      "timeout_s": timeout_s, "cells": {}, "pooled": {}})
        for n in spec["cells"]:
            if str(n) in block["cells"]:
                print(f"[{reading}] n={n}: already scored, kept", flush=True)
                continue
            cell_rows = [r for r in rows if r["reading"] == reading and r["n"] == n]
            block["cells"][str(n)] = score_cell(reading, n, cell_rows, timeout_s)
            save(report, report_path)   # after every cell, so a kill costs one cell at most
        print(f"[{reading}] POOLED: {block['pooled']}", flush=True)

    save(report, report_path)
    for k, v in report["verdicts"].items():
        print(f"VERDICT {k}: {v}", flush=True)
    print(f"written {report_path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
