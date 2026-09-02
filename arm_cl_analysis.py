# ============================================================================
# Arm CL analysis -- executes model-written programs sandboxed (library
# imports for math/numpy/scipy permitted) and scores their stdout with
# arm-F conventions. Reads arm_cl_collect.jsonl, writes arm_cl_report.json,
# prints registered quantities and verdicts per tier. Run once.
#
# Registered taxonomy (one bin per row): no_program, blocked_import,
# forbidden_name, timeout, exec_error, stdout_parse_fail, geom_invalid, valid.
#
# Execution note (disclosed deviation from the prereg's literal wording):
# the registration says "python -I -S ... the runner passes [site-packages]
# explicitly via PYTHONPATH". Empirically, CPython's -I (isolated mode)
# ignores PYTHONPATH and every other PYTHON* environment variable by
# design (it also implies -E). "-I -S" with PYTHONPATH is therefore not
# achievable as literally written -- numpy/scipy would be unimportable and
# the arm would silently collapse to arm CC's allowlist. The registration
# also forbids "edits to model source", so the fix cannot be a sys.path
# line prepended into the extracted program text.
# Resolution used here: the model program's bytes are executed completely
# unmodified, under "python -I -S <driver> <program>", where <driver> is a
# tiny harness (not part of the scored program) that inserts the current
# interpreter's site-packages directories into sys.path and then runs the
# unmodified program file via runpy.run_path. This keeps the registered
# "-I -S" isolation (no automatic site import, no user site, no ambient
# PYTHONPATH honoured) while making numpy/scipy importable, which is the
# entire point of this arm. The interpreter, its site-packages, and the
# numpy/scipy versions resolved are recorded in the report.
# ============================================================================
import ast
import json
import math
import os
import re
import site
import subprocess
import sys
import tempfile
import textwrap
from collections import Counter
from pathlib import Path

from arm_f_repro import parse_packing, validate, score, recipe_value

HERE = Path(__file__).parent
TIERS = ["weak", "sonnet"]
CELLS = [13, 21, 31]
WINDOW_9 = 1e-6  # clearance margin over argmax, per section 2.4
TIMEOUT_S_DEFAULT = 120
FORBIDDEN = {"open", "exec", "eval", "compile", "__import__", "input",
             "breakpoint"}
ALLOWED_MODULES = {"math", "numpy", "scipy"}
FENCE_RE = re.compile(r"^\s*```[a-zA-Z0-9]*\s*\n(.*?)\n?\s*```\s*$", re.DOTALL)
EVALUABILITY_FLOOR = 5

SITE_PACKAGES = site.getsitepackages()

DRIVER_SRC = textwrap.dedent("""
    import runpy
    import sys
    for _p in %r:
        sys.path.insert(0, _p)
    runpy.run_path(sys.argv[1], run_name="__main__")
    """) % SITE_PACKAGES


def argmax_closed_form(n):
    """Family argmax recomputed in closed form, never from a literal:
    best two-radius recipe at k = floor(sqrt(n))."""
    k = math.isqrt(n)
    m = n - k * k
    return recipe_value(k, m)


ARGMAX = {n: argmax_closed_form(n) for n in CELLS}


def strip_fences(text):
    m = FENCE_RE.match(text.strip())
    return m.group(1) if m else text.strip()


def ast_gate(source):
    """Returns (ok, bin_or_None). Registered allowlist: math, numpy, scipy
    (including submodule / from-imports); forbidden names blocked anywhere."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return False, "no_program"
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] not in ALLOWED_MODULES:
                    return False, "blocked_import"
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] not in ALLOWED_MODULES:
                return False, "blocked_import"
        elif isinstance(node, ast.Name) and node.id in FORBIDDEN:
            return False, "forbidden_name"
        elif isinstance(node, ast.Attribute) and node.attr in FORBIDDEN:
            return False, "forbidden_name"
    return True, None


def run_program(source, timeout_s):
    """Returns (bin_or_None, stdout). Executes the UNMODIFIED source under
    python -I -S <driver> <program>, one CPU core, per the registration."""
    with tempfile.NamedTemporaryFile("w", suffix="_model.py", delete=False,
                                     encoding="utf-8") as f:
        f.write(source)
        model_path = f.name
    with tempfile.NamedTemporaryFile("w", suffix="_driver.py", delete=False,
                                     encoding="utf-8") as f:
        f.write(DRIVER_SRC)
        driver_path = f.name
    env = dict(os.environ)
    env["OMP_NUM_THREADS"] = "1"
    env["MKL_NUM_THREADS"] = "1"
    env["OPENBLAS_NUM_THREADS"] = "1"
    try:
        proc = subprocess.run(
            [sys.executable, "-I", "-S", driver_path, model_path],
            capture_output=True, text=True, timeout=timeout_s, env=env)
    except subprocess.TimeoutExpired:
        return "timeout", ""
    finally:
        for p in (model_path, driver_path):
            try:
                Path(p).unlink()
            except OSError:
                pass
    if proc.returncode != 0:
        return "exec_error", proc.stdout
    return None, proc.stdout


def uses_scipy_optimize(source):
    """Descriptive only, not scored: does the source reference
    scipy.optimize (any attribute)?"""
    patterns = [
        r"import\s+scipy\.optimize",
        r"from\s+scipy\.optimize\s+import",
        r"from\s+scipy\s+import[^\n]*\boptimize\b",
        r"scipy\s*\.\s*optimize\b",
    ]
    return any(re.search(p, source) for p in patterns)


def score_row(raw, n, timeout_s=TIMEOUT_S_DEFAULT):
    """Full registered pipeline for one raw response. Returns a dict with
    bin plus scoring fields when valid."""
    source = strip_fences(raw) if raw else ""
    if not source.strip():
        return {"bin": "no_program"}
    ok, gate_bin = ast_gate(source)
    if not ok:
        return {"bin": gate_bin}
    err_bin, stdout = run_program(source, timeout_s)
    if err_bin:
        return {"bin": err_bin}
    packing, parse_err = parse_packing(stdout)
    if packing is None:
        return {"bin": "stdout_parse_fail", "why": parse_err}
    ok6, why6 = validate(packing, n, tol=1e-6)
    ok9, why9 = validate(packing, n, tol=1e-9)
    if not ok6:
        return {"bin": "geom_invalid", "why": why6, "valid_1e9": ok9}
    s = score(packing)
    argmax = ARGMAX[n]
    radii = sorted({round(r, 6) for _, _, r in packing})
    r_dom = Counter(round(r, 6) for _, _, r in packing).most_common(1)[0][0]
    k_struct = round(1 / (2 * r_dom)) if r_dom > 0 else None
    cleared = bool(ok9 and s > argmax + WINDOW_9)
    return {
        "bin": "valid",
        "sum": round(s, 9),
        "valid_1e6": ok6,
        "valid_1e9": ok9,
        "argmax": round(argmax, 9),
        "cleared": cleared,
        "uses_scipy_optimize": uses_scipy_optimize(source),
        "n_distinct_radii": len(radii),
        "k_struct": k_struct,
    }


def load_rows(path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    # resume-by-skip semantics: keep the latest usable row per key
    latest = {}
    for r in rows:
        key = (r["tier"], r["n"], r["sample_id"])
        if r.get("raw_len", 0) > 0 or r.get("call_error"):
            latest[key] = r
    return list(latest.values())


def versions():
    import numpy
    import scipy
    return numpy.__version__, scipy.__version__


MAX_EXEC_WORKERS = 4  # mirrors the collection runner's worker cap; each
                      # subprocess is pinned to one core (OMP/MKL/OPENBLAS=1)
                      # so 4 concurrent executions fit a 4+ core machine.


def score_all(rows, timeout_s, max_workers=MAX_EXEC_WORKERS):
    """Scores every row's program, up to max_workers concurrent subprocess
    executions (threads; subprocess.run releases the GIL while waiting).
    Returns {row_index: scored_dict} in the same order as rows."""
    from concurrent.futures import ThreadPoolExecutor
    results = [None] * len(rows)

    def task(i, r):
        results[i] = score_row(r["raw"], r["n"], timeout_s=timeout_s)

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = [ex.submit(task, i, r) for i, r in enumerate(rows)]
        for f in futs:
            f.result()
    return results


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeout", type=float, default=TIMEOUT_S_DEFAULT,
                    help="wall-clock timeout per program, seconds "
                         "(registered default 120; smoke test overrides)")
    ap.add_argument("--collect", default=str(HERE / "arm_cl_collect.jsonl"),
                    help="path to the collection jsonl (default: registered "
                         "arm_cl_collect.jsonl)")
    ap.add_argument("--report-out", default=str(HERE / "arm_cl_report.json"))
    args = ap.parse_args()

    np_v, sp_v = versions()
    print(f"numpy {np_v}, scipy {sp_v} (recorded once, child processes use "
          f"the same site-packages via the driver)")
    rows = load_rows(Path(args.collect))
    print(f"scoring {len(rows)} rows, up to {MAX_EXEC_WORKERS} concurrent "
          f"executions, {args.timeout}s timeout each")
    scored_all = score_all(rows, timeout_s=args.timeout)
    scored_by_key = {(r["tier"], r["n"], r["sample_id"]): s
                     for r, s in zip(rows, scored_all)}

    report = {"numpy_version": np_v, "scipy_version": sp_v, "tiers": {}}
    for tier in TIERS:
        tier_rows = [r for r in rows if r["tier"] == tier]
        tier_report = {"cells": {}}
        cleared_cells = 0
        pooled_valid = 0
        pooled_cleared = 0
        pooled_sampled = 0
        for n in CELLS:
            cell_rows = [r for r in tier_rows if r["n"] == n]
            scored = [scored_by_key[(r["tier"], r["n"], r["sample_id"])] for r in cell_rows]
            bins = Counter(s["bin"] for s in scored)
            valid = [s for s in scored if s["bin"] == "valid"]
            cleared = [s for s in valid if s["cleared"]]
            pooled_sampled += len(cell_rows)
            pooled_valid += len(valid)
            pooled_cleared += len(cleared)
            underpowered = len(valid) < EVALUABILITY_FLOOR
            cell = {
                "sampled": len(cell_rows),
                "bins": dict(bins),
                "n_valid": len(valid),
                "n_cleared": len(cleared),
                "argmax_closed_form": round(ARGMAX[n], 9),
                "underpowered": underpowered,
            }
            if valid:
                cell["uses_scipy_optimize_rate"] = (
                    f"{sum(s['uses_scipy_optimize'] for s in valid)}/{len(valid)}")
                cell["n_distinct_radii_dist"] = dict(
                    Counter(s["n_distinct_radii"] for s in valid))
                cell["k_struct_dist"] = dict(Counter(s["k_struct"] for s in valid))
                cell["cleared_sums"] = sorted(round(s["sum"], 9) for s in cleared)
            if not underpowered and cleared:
                cleared_cells += 1
            tier_report["cells"][str(n)] = cell
            print(f"[{tier}] n={n}: sampled {len(cell_rows)}, bins {dict(bins)}, "
                  f"valid {len(valid)}, cleared {len(cleared)}"
                  f"{' UNSCOREABLE' if underpowered else ''}")

        pooled_rate = (pooled_cleared / pooled_valid) if pooled_valid else 0.0
        if pooled_valid == 0:
            verdict = "UNSCOREABLE (no valid outputs)"
        elif pooled_cleared == 0:
            verdict = "P-CL1 holds (ceiling survives libraries)"
        elif pooled_rate >= 0.20:
            verdict = "P-CL2 holds (>=20% of valid outputs clear)"
        else:
            verdict = f"dead zone (cleared, rarely: {pooled_cleared}/{pooled_valid})"
        falsifier_fcl1 = cleared_cells >= 2
        tier_report["pooled"] = {
            "sampled": pooled_sampled, "valid": pooled_valid,
            "cleared": pooled_cleared,
            "cleared_rate": round(pooled_rate, 4),
            "cleared_cells": cleared_cells,
            "verdict": verdict,
            "falsifier_F_CL1": falsifier_fcl1,
        }
        report["tiers"][tier] = tier_report
        print(f"[{tier}] POOLED: valid {pooled_valid}/{pooled_sampled}, "
              f"cleared {pooled_cleared}/{pooled_valid if pooled_valid else 0} "
              f"({pooled_rate:.1%})")
        print(f"[{tier}] VERDICT: {verdict}")
        print(f"[{tier}] F-CL1 (cleared at >=2/3 cells): "
              f"{'FIRES' if falsifier_fcl1 else 'does not fire'} "
              f"({cleared_cells}/3 cells cleared)")

    Path(args.report_out).write_text(json.dumps(report, indent=1),
                                     encoding="utf-8")
    print(f"written {args.report_out}")


if __name__ == "__main__":
    main()
