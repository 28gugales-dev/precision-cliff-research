# Round 13: the tier x channel table, built from the frozen reports, never by hand.
#
# The table becomes the paper's headline, so it inherits the failure mode that cost rounds 6
# and 7: a pooled figure whose membership rule was not the one producing it. One rule per
# cell, written here and printed in the caption; the script emits the LaTeX rows, a JSON
# record, and the phrases verify_claims.py checks against the text.
#
# Clearance is section 2.4's rule throughout: valid at 1e-9 AND sum > family argmax + 1e-6,
# with the argmax recomputed in closed form (max over grid orders of T(k, N) = N/(2k) when
# N < k^2, else V(k, m) = k/2 + m(sqrt2 - 1)/(2k) with m = N - k^2 <= (k-1)^2).
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EV = ROOT / "evidence"
_UP = ROOT.parent  # bundle root, or research-corpus/ on the authoring host
CORPUS = _UP if (_UP / "arm_f_repro.py").is_file() else _UP / "precision-cliff"
BS = "\\"


def family_argmax(N):
    best = 0.0
    for k in range(2, 14):
        if N < k * k:
            best = max(best, N / (2 * k))
        else:
            m = N - k * k
            if m <= (k - 1) ** 2:
                best = max(best, k / 2 + m * (math.sqrt(2) - 1) / (2 * k))
    return best


assert abs(family_argmax(13) - 1.776142375) < 1e-9
assert abs(family_argmax(21) - 2.258883476) < 1e-9
assert abs(family_argmax(31) - 2.748528137) < 1e-9
assert abs(family_argmax(20) - 2.2071068) < 1e-7


def clears(sum_, N, valid9):
    return bool(valid9) and sum_ > family_argmax(N) + 1e-6


def wilson_upper(x, n, z=1.96):
    p = x / n
    return (p + z * z / (2 * n) + z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / (1 + z * z / n)


def jsonl(p):
    # utf-8-sig: one ledger carries a BOM
    return [json.loads(l) for l in open(p, encoding="utf-8-sig") if l.strip()]


cells = {}

# ---- direct emission, agent runtime: arm F bare ledger at the four discriminating square cells,
# and the Sonnet-tier arm at its three. Rows are scored from stored sums and 1e-9 validity.
rows = jsonl(CORPUS / "arm_f_candidates_v2.jsonl")
bare = [r for r in rows if r["arm"] == "bare" and r["n"] in (13, 21, 31, 43)]
bare_valid = [r for r in bare if r["valid"]]
assert len(bare_valid) == 57, len(bare_valid)
bare_clear = sum(clears(r["sum_of_radii"], r["n"], r["valid_strict_1e9"]) for r in bare_valid)
cells["weak/direct/runtime"] = dict(valid=57, clear=bare_clear, cells="13, 21, 31, 43",
                                     rule="arm F full ledger, four discriminating square cells")
son = [r for r in rows if r["arm"] == "sonnet_bare"]
son_valid = [r for r in son if r["valid"]]
assert len(son_valid) == 30, len(son_valid)
son_clear = [r for r in son_valid if clears(r["sum_of_radii"], r["n"], r["valid_strict_1e9"])]
assert len(son_clear) == 1 and son_clear[0]["n"] == 31, [(r["n"], r["sum_of_radii"]) for r in son_clear]
cells["sonnet/direct/runtime"] = dict(valid=30, clear=1, cells="13, 21, 31", rule="arm S, all rows")

# arm M's extend cell N = 20: the two out-of-family escapes, weak tier, direct, runtime
# the collect ledger is raw text; the scored rows (sum, validity at both tolerances) are frozen
# per cell in arm_m_scored.json
m20 = json.load(open(CORPUS / "arm_m_scored.json", encoding="utf-8-sig"))["20"]["detail"]
m20_valid = [r for r in m20 if r["valid6"] and r["sum"] is not None]
m20_clear = sum(clears(r["sum"], 20, r["valid9"]) for r in m20_valid)
assert (len(m20_valid), m20_clear) == (15, 2), (len(m20_valid), m20_clear)
cells["weak/direct/runtime/N20"] = dict(valid=15, clear=2, cells="20", rule="arm M extend cell, out-of-family hexagonal rows")

# ---- direct emission, pinned path: arm P, seven square cells
p = json.load(open(EV / "arm_p_report.json", encoding="utf-8"))
sq_valid = sum(c["valid_1e6"] for c in p["square"].values())
sq_n = sum(c["sampled"] for c in p["square"].values())
assert (sq_valid, sq_n) == (0, 105)
cells["weak/direct/pinned"] = dict(valid=0, sampled=105, clear=0, cells="13, 17, 21, 31, 35, 37, 43", rule="arm P square cells; no valid output, unscoreable")

# ---- math-only code, agent runtime: CC + CC2 (weak), CCS (Sonnet)
cc = json.load(open(EV / "arm_cc_report.json", encoding="utf-8"))
cc2 = json.load(open(CORPUS / "arm_cc2_report.json", encoding="utf-8"))
ccs = json.load(open(CORPUS / "arm_ccs_report.json", encoding="utf-8"))


def above(rep):
    return sum(int(c["above_rival_rate"].split("/")[0]) for c in rep["cells"].values())


def argmax_hits(rep):
    return sum(int(c["argmax_rate"].split("/")[0]) for c in rep["cells"].values())


w_valid = cc["pooled"]["valid"] + cc2["pooled"]["valid"]
assert w_valid == 78 and above(cc) + above(cc2) == 0
cells["weak/math/runtime"] = dict(valid=78, clear=0, cells="13, 21, 31", argmax_reached=argmax_hits(cc) + argmax_hits(cc2),
                                   rule="arms CC and CC2 pooled, math-only programs")
assert ccs["pooled"]["valid"] == 37 and ccs["pooled"]["above_rival"] == 0
cells["sonnet/math/runtime"] = dict(valid=37, clear=0, cells="13, 21, 31", rule="arm CCS, math-only programs")

# ---- math-only code, pinned path, Sonnet tier: arm CCP (round 14, the isolating arm)
ccp = json.load(open(EV / "arm_ccp_report.json", encoding="utf-8"))
assert (ccp["pooled"]["valid"], ccp["pooled"]["cleared"], ccp["pooled"]["falsifier_F_CCP1"]) == (35, 0, False)
ccp_best = {n: max(c["sums"]) for n, c in ccp["cells"].items()}
assert all(ccp_best[n] < c["argmax_closed_form"] for n, c in ccp["cells"].items())
cells["sonnet/math/pinned"] = dict(valid=35, clear=0, cells="13, 21, 31", best=ccp_best,
                                    rule="arm CCP, arm CC's prompt on arm CL's path and 120 s budget, math only")

# ---- math-only code, pinned path: arm P code cells (the CC prompt on the pinned path)
pc_valid = sum(c["n_valid"] for c in p["code"].values())
pc_clear = sum(c["cleared"] for c in p["code"].values())
assert (pc_valid, pc_clear) == (12, 0)
pc_scoreable = {n: c["n_valid"] for n, c in p["code"].items() if c["evaluable"]}
assert pc_scoreable == {"21": 6}, pc_scoreable
cells["weak/math/pinned"] = dict(valid=12, clear=0, cells="13, 21, 31", scoreable_valid=6, scoreable_clear=0,
                                  wilson_upper_scoreable=round(100 * wilson_upper(0, 6), 1),
                                  rule="arm P code cells, CC prompt on the pinned path; 0 of 12 pooled, 0 of 6 at the one cell above the five-valid floor")

# ---- library code, pinned path: arm CL both tiers
cl = json.load(open(EV / "arm_cl_report.json", encoding="utf-8"))
wk, sn = cl["tiers"]["weak"]["pooled"], cl["tiers"]["sonnet"]["pooled"]
assert (wk["valid"], wk["cleared"]) == (11, 0) and (sn["valid"], sn["cleared"], sn["cleared_cells"]) == (25, 23, 3)
wk_cells = cl["tiers"]["weak"]["cells"]
scoreable = {n: c["n_valid"] for n, c in wk_cells.items() if not c["underpowered"]}
assert scoreable == {"31": 6}, scoreable
cells["weak/scipy/pinned"] = dict(valid=11, clear=0, cells="13, 21, 31", wilson_upper=round(100 * wilson_upper(0, 11), 1),
                                   scoreable_valid=6, scoreable_clear=0, wilson_upper_scoreable=round(100 * wilson_upper(0, 6), 1),
                                   rule="arm CL weak tier; 0 of 11 pooled, 0 of 6 at the one cell above the five-valid floor")
# round 14, post hoc: the lenient reparse of the 22 stdout failures (loop/cl_lenient_reparse.py)
lenient = json.load(open(EV / "cl_lenient.json", encoding="utf-8"))["weak_pooled"]
assert (lenient["recovered_valid"], lenient["recovered_cleared"], lenient["valid_with_recovery"]) == (9, 1, 20)
cells["weak/scipy/pinned"]["lenient_valid"] = lenient["valid_with_recovery"]
cells["weak/scipy/pinned"]["lenient_clear"] = lenient["recovered_cleared"]
# round 14: arm CL-W, the registered top-up, pooled with arm CL's weak tier under its pre-stated rule
clw = json.load(open(EV / "arm_clw_report.json", encoding="utf-8"))["pooled"]
assert (clw["sampled"], clw["valid"], clw["cleared"], clw["lenient_valid"], clw["lenient_cleared"]) == (90, 19, 0, 41, 4)
assert abs(clw["wilson_upper_95"] - wilson_upper(0, 19)) < 1e-3 and clw["falsifier_F_CLW1"] is False
cells["weak/scipy/pinned"].update(pooled_valid=19, pooled_clear=0, pooled_wilson_upper=round(100 * clw["wilson_upper_95"], 1),
                                  pooled_lenient_valid=41, pooled_lenient_clear=4)
# excess over the argmax among the 23 clearing programs, so the margin is reported as a distribution
sn_cells = cl["tiers"]["sonnet"]["cells"]
excess = sorted((s - c["argmax_closed_form"]) / c["argmax_closed_form"] * 100
                for c in sn_cells.values() for s in c["cleared_sums"])
assert len(excess) == 23
cells["sonnet/scipy/pinned"] = dict(valid=25, clear=23, cells="13, 21, 31", clear_cells=3, rule="arm CL Sonnet tier",
                                     excess_min=round(excess[0], 2), excess_median=round(excess[11], 2), excess_max=round(excess[-1], 2))

# ---- round 15b: arm B, the optimizer alone -- a fixed reference program through arm CL's pipeline
b = json.load(open(EV / "arm_b_report.json", encoding="utf-8"))
b_valid, b_clear = b["pooled"]["valid"], b["pooled"]["cleared"]
b_cells_at_20 = b["pooled"]["cells_at_20pct"]
b_best = {n: c["best_sum"] for n, c in b["cells"].items()}
b_beats_sonnet = b["pooled"]["S_B1_cells_where_baseline_best_exceeds_sonnet_best"]
cells["none/scipy/local"] = dict(valid=b_valid, clear=b_clear, cells="13, 21, 31", clear_cells_at_20=b_cells_at_20,
                                  best=b_best, beats_sonnet_best_at=b_beats_sonnet,
                                  rule="arm B, fixed random-restart SLSQP reference program, no model, arm CL's pipeline")

(EV / "channel_table.json").write_text(json.dumps(cells, indent=2), encoding="utf-8")

# ---- LaTeX
c = cells
wu = c["weak/scipy/pinned"]["wilson_upper"]
rows_tex = [
    ("weak", "direct emission", "agent runtime", "13, 21, 31, 43", f"{c['weak/direct/runtime']['clear']} of 57", "trap cells; at the extend cell $N = 20$ (arm M) 2 of 15 clear, both out-of-family"),
    ("weak", "direct emission", "pinned API", "7 square cells", "0 valid of 105", "unscoreable (arm P)"),
    ("Sonnet", "direct emission", "agent runtime", "13, 21, 31", "1 of 30", "one out-of-family packing at $N = 31$; 27 of 30 valid at $10^{-9}$, the clearance among them (arm S)"),
    ("weak", "math-only program", "agent runtime", "13, 21, 31", "0 of 78", f"reaches the argmax exactly {c['weak/math/runtime']['argmax_reached']} times, never passes it (CC, CC2)"),
    ("weak", "math-only program", "pinned API", "13, 21, 31", "0 of 12", "two cells under the five-valid floor; 0 of 6 at the scoreable cell (arm P code cells)"),
    ("Sonnet", "math-only program", "agent runtime", "13, 21, 31", "0 of 37", "annealing and multi-restart search, still 0 (CCS)"),
    ("Sonnet", "math-only program", "pinned API", "13, 21, 31", "0 of 35", f"the library row's path and 120 s budget without the libraries; best per cell {ccp_best['13']}, {ccp_best['21']}, {ccp_best['31']:.3f}, none at the argmax (CCP)"),
    ("weak", "numpy/scipy program", "pinned API", "13, 21, 31", f"0 of 11; 0 of {c['weak/scipy/pinned']['pooled_valid']} pooled", f"arm CL, then pooled with its registered top-up CL-W (90 invocations; the $N = 21$ cell stays under the five-valid floor): Wilson upper bound {c['weak/scipy/pinned']['pooled_wilson_upper']}\\%, under the 20\\% bar; a post-hoc reparse of the \\texttt{{numpy}}-scalar stdouts reads {c['weak/scipy/pinned']['pooled_lenient_clear']} of {c['weak/scipy/pinned']['pooled_lenient_valid']} (CL, CL-W)"),
    ("Sonnet", "numpy/scipy program", "pinned API", "13, 21, 31", BS + "textbf{23 of 25}", f"3 of 3 cells; excess over the argmax {c['sonnet/scipy/pinned']['excess_min']}--{c['sonnet/scipy/pinned']['excess_max']}\\%, median {c['sonnet/scipy/pinned']['excess_median']}\\% (CL)"),
    ("none", "numpy/scipy program, fixed", "local, 120 s", "13, 21, 31",
     (BS + "textbf{" if b_cells_at_20 >= 2 else "") + f"{b_clear} of {b_valid}" + ("}" if b_cells_at_20 >= 2 else ""),
     f"a fixed random-restart SLSQP reference program, no model, through the library row's pipeline; {b_cells_at_20} of 3 cells at the 20\\% bar; "
     + (f"best per cell exceeds the Sonnet best at {len(b_beats_sonnet)} of 3 cells" if b_beats_sonnet else "best per cell below the Sonnet best at every cell") + " (arm B)"),
]
lines = [
    "% GENERATED by loop/build_channel_table.py from the frozen reports; do not edit by hand.",
    BS + "begin{table}[t]", BS + "centering", BS + "small", BS + "setlength{" + BS + "tabcolsep}{3pt}",
    BS + "begin{tabular}{@{}lllp{0.11" + BS + "linewidth}p{0.13" + BS + "linewidth}p{0.29" + BS + "linewidth}@{}}",
    BS + "toprule",
    "Tier & Channel & Instrument & Cells & Clear & Note " + BS + BS,
    BS + "midrule",
]
for tier, ch, inst, cl_, clear, note in rows_tex:
    lines.append(f"{tier} & {ch} & {inst} & {cl_} & {clear} & {note} " + BS + BS)
lines += [
    BS + "bottomrule", BS + "end{tabular}",
    BS + "caption{" + BS + "textbf{Who clears the family argmax.} Each row is one arm or one registered pair of arms, "
    "scored under " + BS + "S" + BS + "ref{sec:notation}'s clearance rule: valid at $10^{-9}$ and above the family "
    "argmax by more than $10^{-6}$, the argmax recomputed in closed form. ``Clear'' counts valid outputs. "
    "Instrument names the serving path, which arm P shows is not interchangeable: the same weak-tier prompt yields "
    "35 of 45 valid packings (78" + BS + "%) through the agent runtime and 0 of 105 through the pinned API. Rows are not "
    "pooled across instruments.}",
    BS + "label{tab:channel}", BS + "end{table}",
]
(ROOT / "paper").mkdir(exist_ok=True)
(ROOT / "paper" / "tab_channel.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("tab_channel.tex written;", len(rows_tex), "rows")
for k, v in cells.items():
    print(f"  {k:28} valid {v.get('valid'):>3}  clear {v['clear']:>2}")
