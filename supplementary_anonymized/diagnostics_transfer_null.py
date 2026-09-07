# Post hoc diagnostic (disclosed): template-shape null for the transfer paper's arm V
# and arm GM3 rows. A proposer already inside the grid-plus-filler family still picks a
# grid order. The orders in reach at a cell are k*-1, k* and k*+1, one branch value each:
# the extend value V(k, N - k^2) when k^2 <= N, the truncate value T(k, N) = N/(2k)
# otherwise. An extend value is admissible only when its fillers fit the interstices,
# N - k^2 <= (k-1)^2; at N = 17 the order-3 value needs 8 fillers where the family
# allows 4, so that cell has two admissible orders and a null rate of 1/2, not 1/3.
# The null rate is therefore per row, and a pooled tail is the exact Poisson-binomial
# upper tail over the rows' rates rather than a Binomial(n, 1/3) tail.
#
# Reads arm_v_scored.jsonl (arm V's frozen scoring) and arm_gm_gm3_checkpoint.jsonl
# (arm GM3's raw chain), scoring the latter with arm_f_repro exactly as
# arm_ceiling_gm3_v.py does. Run from the repository root with no arguments.
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from arm_f_repro import parse_packing, score, validate  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "diagnostics_transfer_null.json"
SQRT2 = math.sqrt(2.0)
WINDOW = 2e-3  # the registered value-matching window
DISCRIMINATING = {13, 21, 31}  # anchor below the family argmax by more than WINDOW
GM3_ALIAS = "gemma-4-26b"


def branch_value(k, n):
    """Admissible branch value at order k, or None when the extend branch overfills."""
    if k * k <= n:
        m = n - k * k
        if m > (k - 1) ** 2:
            return None
        return k / 2.0 + m * (SQRT2 - 1.0) / (2.0 * k)
    return n / (2.0 * k)


def anchor(n):
    k = round(math.sqrt(n))
    return branch_value(k, n)


def null_rate(n):
    """Share of admissible orders in {k*-1, k*, k*+1} whose value sits inside the window of the anchor."""
    k = round(math.sqrt(n))
    a = anchor(n)
    vals = [branch_value(j, n) for j in (k - 1, k, k + 1)]
    vals = [v for v in vals if v is not None]
    hits = sum(abs(v - a) < WINDOW for v in vals)
    return hits / len(vals), len(vals)


def poisson_binomial_upper_tail(ps, x):
    """P[X >= x] for X = sum of independent Bernoulli(p_i)."""
    dist = [1.0]
    for p in ps:
        nxt = [0.0] * (len(dist) + 1)
        for i, d in enumerate(dist):
            nxt[i] += d * (1 - p)
            nxt[i + 1] += d * p
        dist = nxt
    return sum(dist[x:])


def extract_text(resp):
    if "candidates" in resp:
        try:
            for p in resp["candidates"][0]["content"]["parts"]:
                if not p.get("thought") and p.get("text"):
                    return p["text"]
            return ""
        except (KeyError, IndexError, TypeError):
            return ""
    if "choices" in resp:
        try:
            return resp["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError, TypeError):
            return ""
    return ""


def v_rows():
    """(alias, n, sum) for every arm V row valid at 1e-6."""
    out = []
    for line in open(ROOT / "arm_v_scored.jsonl", encoding="utf-8"):
        if not line.strip():
            continue
        r = json.loads(line)
        if str(r.get("valid")) != "True":
            continue
        out.append((r["proposer_alias"], int(r["n"]), float(r["sum_of_radii"])))
    return out


def gm3_rows():
    """(n, sum) for every arm GM3 row valid at 1e-6, one per (n, sample_idx)."""
    seen = {}
    for line in open(ROOT / "arm_gm_gm3_checkpoint.jsonl", encoding="utf-8"):
        if not line.strip():
            continue
        r = json.loads(line)
        if "transport_error" in r["response"]:
            continue
        seen.setdefault((r["n"], r["sample_idx"]), r)
    out = []
    for r in seen.values():
        n = int(r["n"])
        circles, _ = parse_packing(extract_text(r["response"]) or None)
        if circles is None:
            continue
        try:
            ok = all(c is not None and len(c) == 3 and all(isinstance(v, (int, float)) for v in c)
                     for c in circles)
        except TypeError:
            ok = False
        if ok and validate(circles, n, tol=1e-6)[0]:
            out.append((n, score(circles)))
    return out


def tail_row(label, rows):
    """rows: list of (n, sum). Returns the table entry."""
    ps = [null_rate(n)[0] for n, _ in rows]
    hits = sum(abs(s - anchor(n)) < WINDOW for n, s in rows)
    entry = {"label": label, "on_prediction": hits, "valid": len(rows),
             "null_rates": sorted({round(p, 6) for p in ps}),
             "rows_at_one_half": sum(p == 0.5 for p in ps),
             "tail_admissible": poisson_binomial_upper_tail(ps, hits),
             "tail_one_third": poisson_binomial_upper_tail([1 / 3] * len(rows), hits)}
    return entry


def main():
    print("admissible orders per cell (k*-1, k*, k*+1), null rate:")
    cells = {}
    for n in (13, 17, 21, 31, 35, 37, 43):
        p, k = null_rate(n)
        cells[str(n)] = {"anchor": anchor(n), "admissible_orders": k, "null_rate": p}
        print(f"  N={n:>2} anchor {anchor(n):.7f} admissible {k} null {p:.4f}")

    table = []
    byalias = defaultdict(list)
    for alias, n, s in v_rows():
        byalias[alias].append((n, s))
    for alias in ("cohere/north-mini-code:free", "openai/gpt-oss-20b:free"):
        rows = byalias[alias]
        short = alias.split("/")[1].split(":")[0]
        table.append(tail_row(f"V {short} pooled", rows))
        table.append(tail_row(f"V {short} discriminating",
                              [(n, s) for n, s in rows if n in DISCRIMINATING]))
    g = gm3_rows()
    table.append(tail_row(f"GM3 {GM3_ALIAS} discriminating",
                          [(n, s) for n, s in g if n in DISCRIMINATING]))

    print("\nrow                                on/valid  tail(admissible)  tail(1/3)  rows at 1/2")
    for e in table:
        print(f"{e['label']:<34} {e['on_prediction']:>3}/{e['valid']:<4} "
              f"{e['tail_admissible']:>12.4g}  {e['tail_one_third']:>9.4g}  {e['rows_at_one_half']}")
    OUT.write_text(json.dumps({"window": WINDOW, "cells": cells, "table": table}, indent=1),
                   encoding="utf-8")
    print(f"\nwrote {OUT.name}. Post hoc throughout; the registered analyses are unchanged.")


if __name__ == "__main__":
    main()
