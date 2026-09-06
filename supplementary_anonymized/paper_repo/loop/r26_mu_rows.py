"""Round 26: per-row table for the eighteen arm MU outputs above the family argmax.

Reads loop/round22e_facts.json (c_arm_mu_near_clearances) and the MU parent sums in
../precision-cliff/arm_mu_prompts.json, then writes
  paper/tab_mu_rows.tex   the supplement table (S2), generated, do not hand-edit
  loop/r26_mu_rows.json   every printed cell as a string, for numcheck.py provenance
Run from paper2-transfer root: python loop/r26_mu_rows.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FACTS = ROOT / "loop" / "round22e_facts.json"
# Working corpus sits beside the paper repo; inside the anonymized bundle the
# corpus root is one level up (bundle/paper_repo/loop/ -> bundle/).
PROMPTS = next(p for p in (ROOT.parent / "precision-cliff" / "arm_mu_prompts.json",
                           ROOT.parent / "arm_mu_prompts.json") if p.exists())
OUT_TEX = ROOT / "paper" / "tab_mu_rows.tex"
OUT_JSON = ROOT / "loop" / "r26_mu_rows.json"

PARENT_WORD = {"A_anchor": "anchor parent", "B_rival": "argmax parent"}


def sci(x, sig=3):
    """x -> (mantissa string, exponent int), e.g. 3.250846e-07 -> ('3.25', -7)."""
    s = f"{x:.{sig - 1}e}"
    mant, exp = s.split("e")
    return mant, int(exp)


def tex_sci(x):
    mant, exp = sci(x)
    return f"${mant}\\times10^{{{exp}}}$"


def main():
    facts = json.loads(FACTS.read_text(encoding="utf-8"))["c_arm_mu_near_clearances"]
    prompts = json.loads(PROMPTS.read_text(encoding="utf-8"))["mu"]
    rows = facts["rows"]
    assert len(rows) == 18 and facts["all_fail_1e9"] and facts["all_decided_by_overlap_not_containment"]

    def key(r):
        return (r["cell_N"], r["condition"], int(r["slot"][1:]))

    rows = sorted(rows, key=key)
    printed = set()
    lines = []
    n_eq_parent = 0
    for r in rows:
        parent_sum = prompts[str(r["cell_N"])][r["condition"]]["parent_score"]
        sum_s = f"{r['sum']:.7f}"
        eq = abs(r["sum"] - parent_sum) < 5e-8
        n_eq_parent += eq
        ex_m, ex_e = sci(r["excess_over_family_argmax"])
        ov_m, ov_e = sci(r["max_pairwise_overlap_magnitude"])
        assert r["excess_over_family_argmax"] > r["max_pairwise_overlap_magnitude"]
        slot = r["slot"][1:]
        printed.update({str(r["cell_N"]), slot, sum_s, ex_m, ov_m})
        note = "equals parent sum" if eq else ("above parent" if r["sum"] > parent_sum else "below parent")
        lines.append(
            f"{r['cell_N']} & {PARENT_WORD[r['condition']]} & {slot} & {sum_s} & "
            f"{tex_sci(r['excess_over_family_argmax'])} & {tex_sci(r['max_pairwise_overlap_magnitude'])} & {note} \\\\"
        )

    tex = "\n".join([
        "\\begin{center}",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{4pt}",
        "\\begin{tabular}{@{}rlrrrrl@{}}",
        "\\toprule",
        "$N$ & Parent & Slot & Recorded sum & Excess over argmax & Largest overlap & Relation to parent sum \\\\",
        "\\midrule",
        *lines,
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{center}",
        "",
    ])
    OUT_TEX.parent.mkdir(parents=True, exist_ok=True)
    OUT_TEX.write_text(tex, encoding="utf-8")

    out = {
        "source": "loop/r26_mu_rows.py over loop/round22e_facts.json c_arm_mu_near_clearances and "
                  "../precision-cliff/arm_mu_prompts.json parent_score; generates paper/tab_mu_rows.tex",
        "n_rows": len(rows),
        "n_equal_parent_sum": n_eq_parent,
        "n_not_equal_parent_sum": len(rows) - n_eq_parent,
        "excess_exceeds_largest_overlap_in_every_row": True,
        "printed": sorted(printed),
        "rows": [
            {
                "N": r["cell_N"], "parent": PARENT_WORD[r["condition"]], "slot": r["slot"],
                "sum": f"{r['sum']:.7f}",
                "excess": r["excess_over_family_argmax"],
                "largest_overlap": r["max_pairwise_overlap_magnitude"],
                "parent_sum": prompts[str(r["cell_N"])][r["condition"]]["parent_score"],
            }
            for r in rows
        ],
    }
    OUT_JSON.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"wrote {OUT_TEX.name} ({len(rows)} rows, {n_eq_parent} equal parent sum) and {OUT_JSON.name}")


if __name__ == "__main__":
    main()
