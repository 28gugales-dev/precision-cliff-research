# ============================================================================
# Arm CC analysis — executes model-written programs sandboxed and scores their
# stdout with arm-F conventions. Reads arm_cc_collect.jsonl, writes
# arm_cc_report.json, prints the registered quantities and verdicts.
# Committed with the preregistration, before sampling. No arguments.
#
# Registered taxonomy (one bin per row): no_program, blocked_import,
# forbidden_name, timeout, exec_error, stdout_parse_fail, geom_invalid, valid.
# ============================================================================
import ast
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

from arm_f_repro import validate, score

HERE = Path(__file__).parent
CELLS = [13, 21, 31]
KSTAR = {13: 4, 21: 5, 31: 6}
ANCHOR = {13: 1.6250000, 21: 2.1000000, 31: 2.5833333}
RIVAL = {13: 1.7761424, 21: 2.2588835, 31: 2.7485281}
WINDOW = 2e-3
TIMEOUT_S = 10
FORBIDDEN = {"open", "exec", "eval", "compile", "__import__", "input",
             "breakpoint"}
FENCE_RE = re.compile(r"^\s*```[a-zA-Z0-9]*\s*\n(.*?)\n?\s*```\s*$", re.DOTALL)


def strip_fences(text):
    m = FENCE_RE.match(text.strip())
    return m.group(1) if m else text.strip()


def ast_gate(source):
    """Returns (ok, bin_or_None). Registered allowlist: import math only;
    forbidden names blocked anywhere."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return False, "no_program"
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] != "math":
                    return False, "blocked_import"
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] != "math":
                return False, "blocked_import"
        elif isinstance(node, ast.Name) and node.id in FORBIDDEN:
            return False, "forbidden_name"
        elif isinstance(node, ast.Attribute) and node.attr in FORBIDDEN:
            return False, "forbidden_name"
    return True, None


def run_program(source):
    """Returns (bin_or_None, stdout). Executes under python -I -S with a
    10-second timeout, per the registration."""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False,
                                     encoding="utf-8") as f:
        f.write(source)
        path = f.name
    try:
        proc = subprocess.run([sys.executable, "-I", "-S", path],
                              capture_output=True, text=True,
                              timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return "timeout", ""
    finally:
        try:
            Path(path).unlink()
        except OSError:
            pass
    if proc.returncode != 0:
        return "exec_error", proc.stdout
    return None, proc.stdout


def score_row(raw, n):
    """Full registered pipeline for one raw response. Returns a dict with
    bin plus scoring fields when valid."""
    source = strip_fences(raw)
    if not source.strip():
        return {"bin": "no_program"}
    ok, gate_bin = ast_gate(source)
    if not ok:
        return {"bin": gate_bin}
    err_bin, stdout = run_program(source)
    if err_bin:
        return {"bin": err_bin}
    try:
        packing = ast.literal_eval(strip_fences(stdout))
        packing = [[float(x), float(y), float(r)] for x, y, r in packing]
    except (ValueError, SyntaxError, TypeError):
        return {"bin": "stdout_parse_fail"}
    ok6, why6 = validate(packing, n, tol=1e-6)
    ok9, _ = validate(packing, n, tol=1e-9)
    if not ok6:
        return {"bin": "geom_invalid", "why": why6, "valid_1e9": ok9}
    s = score(packing)
    r_dom = Counter(round(r, 4) for _, _, r in packing).most_common(1)[0][0]
    k_struct = round(1 / (2 * r_dom)) if r_dom > 0 else None
    return {"bin": "valid", "sum": round(s, 7), "valid_1e9": ok9,
            "k_struct": k_struct,
            "on_anchor": abs(s - ANCHOR[n]) <= WINDOW,
            "on_argmax": abs(s - RIVAL[n]) <= WINDOW,
            "above_rival": s > RIVAL[n] + WINDOW}


def bucket(v):
    return round(v / WINDOW)


def main():
    rows = [json.loads(line) for line in
            (HERE / "arm_cc_collect.jsonl").read_text(
                encoding="utf-8").splitlines() if line.strip()]
    report = {"cells": {}, "pooled": {}}
    pooled_valid = 0
    pooled_anchor = 0
    pooled_sampled = 0
    verdict_cc1_cells = 0
    verdict_cc2_cells = 0
    for n in CELLS:
        cell_rows = [r for r in rows if r["cell"] == n]
        scored = [score_row(r["raw"], n) for r in cell_rows]
        bins = Counter(s["bin"] for s in scored)
        valid = [s for s in scored if s["bin"] == "valid"]
        pooled_sampled += len(cell_rows)
        pooled_valid += len(valid)
        pooled_anchor += sum(s["on_anchor"] for s in valid)
        cell = {"sampled": len(cell_rows), "bins": dict(bins),
                "n_valid": len(valid)}
        if valid:
            buckets = Counter(bucket(s["sum"]) for s in valid)
            top = buckets.most_common()
            modal_bucket, modal_count = top[0]
            tie = len(top) > 1 and top[1][1] == modal_count
            margin = modal_count - (top[1][1] if len(top) > 1 else 0)
            modal_val = modal_bucket * WINDOW
            cell.update({
                "modal_value_approx": round(modal_val, 4),
                "modal_count": modal_count, "modal_tie": tie,
                "modal_margin": margin,
                "anchor_rate": f"{sum(s['on_anchor'] for s in valid)}/{len(valid)}",
                "argmax_rate": f"{sum(s['on_argmax'] for s in valid)}/{len(valid)}",
                "above_rival_rate": f"{sum(s['above_rival'] for s in valid)}/{len(valid)}",
                "k_struct_dist": dict(Counter(s["k_struct"] for s in valid)),
                "sums": sorted(round(s["sum"], 7) for s in valid),
                "underpowered": len(valid) < 5,
            })
            if not tie and len(valid) >= 5:
                if abs(modal_val - ANCHOR[n]) <= WINDOW:
                    verdict_cc1_cells += 1
                elif modal_val > ANCHOR[n] + WINDOW:
                    verdict_cc2_cells += 1
        else:
            cell["underpowered"] = True
        report["cells"][str(n)] = cell
        print(f"n={n}: sampled {len(cell_rows)}, bins {dict(bins)}")
        if valid:
            print(f"  modal ~{cell['modal_value_approx']} x{cell['modal_count']}"
                  f" (tie={cell['modal_tie']}, margin={cell['modal_margin']})"
                  f" anchor {cell['anchor_rate']} argmax {cell['argmax_rate']}"
                  f" above-rival {cell['above_rival_rate']}"
                  f" k {cell['k_struct_dist']}"
                  f"{' UNDERPOWERED' if cell['underpowered'] else ''}")
    p_cc1 = verdict_cc1_cells >= 2
    p_cc2 = verdict_cc2_cells >= 2
    verdict = ("P-CC1 holds" if p_cc1 else
               "P-CC2 holds" if p_cc2 else "INCONCLUSIVE")
    report["pooled"] = {
        "sampled": pooled_sampled, "valid": pooled_valid,
        "anchor": pooled_anchor,
        "armF_baseline": "bare cells N=13/21/31: 50/60 valid, 35/50 on-prediction",
        "cc1_cells": verdict_cc1_cells, "cc2_cells": verdict_cc2_cells,
        "verdict": verdict,
    }
    (HERE / "arm_cc_report.json").write_text(json.dumps(report, indent=1),
                                             encoding="utf-8")
    print(f"pooled: valid {pooled_valid}/{pooled_sampled}, "
          f"anchor {pooled_anchor}/{pooled_valid if pooled_valid else 0}")
    print(f"VERDICT: {verdict} (CC1 cells {verdict_cc1_cells}, "
          f"CC2 cells {verdict_cc2_cells})")
    print("written arm_cc_report.json")


if __name__ == "__main__":
    main()
