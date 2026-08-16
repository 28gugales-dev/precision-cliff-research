#!/usr/bin/env python3
"""Figure 4 (companion paper): parent-echo rate by rung across model families.

Replays every family's raw candidate ledger with the wave-7 lineage logic
(echo = 6 dp order-insensitive coordinate equality against the RUNNING parent,
validity recomputed from coordinates, acceptance on strict score improvement).
No convenience fields are read. Families whose valid-row count sits below the
wave power floor (20 per rung) are drawn hollow with n annotated — their
points are descriptive, not evidential, matching the papers' text.

Regenerate: python fig4_family_echo.py  (no arguments) -> fig4_family_echo.png
Skips any family whose ledger is absent (wave 7c gemma lands later).
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
N = 26
EPS = 1e-6

FAMILIES = [
    # label, ledger path, note, power floor (per that family's own registration:
    # the Qwen fresh wave's registered echo bound was evaluated on the rows it
    # drew — 24/17 valid — with no 20-valid floor; waves 7/7b/7c register 20)
    ("Qwen2.5-Coder-14B\n(fresh seeds)",
     "sec3_artifacts/precision_sweep_14b_fresh_output/precision_sweep_14b_fresh/candidates_precision_14b_fresh.jsonl", "", 0),
    ("Llama-3.1-8B",
     "wave7_output/wave7_llama31_8b/candidates_wave7_llama31_8b.jsonl", "", 20),
    ("Gemma-2-9B",
     "wave7_output/wave7_gemma2_9b/candidates_wave7_gemma2_9b.jsonl", "", 20),
    ("Phi-4-14B",
     "wave7b_output/wave7b_phi4_14b/candidates_wave7b_phi4_14b.jsonl", "", 20),
    ("Mistral-Small-24B",
     "wave7b_output/wave7b_mistral24b/candidates_wave7b_mistral24b.jsonl", "", 20),
    ("GPT-OSS-20B",
     "wave7c_output/wave7c_gpt_oss_20b/candidates_wave7c_gpt_oss_20b.jsonl", "MXFP4-native parent", 20),
    ("Gemma-4-31B",
     "wave7c_output/wave7c_gemma4_31b/candidates_wave7c_gemma4_31b.jsonl", "", 20),
]
RUNGS = ["q4_k_m", "q2_k"]


def canon(circles):
    return sorted((round(x, 6), round(y, 6), round(r, 6)) for (x, y, r) in circles)


def valid_score(circles):
    if circles is None or len(circles) != N or any(r <= 0 for (_, _, r) in circles):
        return False, 0.0
    if not all(x - r >= -EPS and x + r <= 1 + EPS and y - r >= -EPS and y + r <= 1 + EPS
               for (x, y, r) in circles):
        return False, 0.0
    for i in range(N):
        xi, yi, ri = circles[i]
        for j in range(i + 1, N):
            xj, yj, rj = circles[j]
            if math.hypot(xi - xj, yi - yj) + EPS < ri + rj:
                return False, 0.0
    return True, sum(r for (_, _, r) in circles)


def baseline():
    r = round(0.9 / N, 6)
    pts = []
    for row in range(5):
        for col in range(6):
            if len(pts) >= N:
                break
            pts.append((round((col + 0.5) / 6.0, 6), round((row + 0.5) / 5.0, 6), r))
    return pts


BASE = baseline()
_, BASE_SCORE = valid_score(BASE)


def replay(path):
    rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    per = {}
    for r in rows:
        per.setdefault((r["quant"], r["seed"]), []).append(r)
    out = {q: {"valid": 0, "echo": 0} for q in RUNGS}
    for (quant, seed), rs in per.items():
        if quant not in out:
            continue
        rs.sort(key=lambda r: r["gen"])
        parent, pscore = list(BASE), BASE_SCORE
        for r in rs:
            circles = None if r.get("circles") is None else [tuple(c) for c in r["circles"]]
            ok, sc = valid_score(circles)
            if not ok:
                continue
            out[quant]["valid"] += 1
            if canon(circles) == canon(parent):
                out[quant]["echo"] += 1
            if sc > pscore:
                parent, pscore = circles, sc
    return out


def wilson(k, n, z=1.96):
    if n == 0:
        return 0.0, 0.0, 0.0
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    data = []
    for label, rel, note, floor in FAMILIES:
        p = os.path.join(HERE, rel)
        if not os.path.exists(p):
            print(f"skip (no ledger yet): {label.splitlines()[0]}")
            continue
        data.append((label, replay(p), note, floor))

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    xpos = {q: i for i, q in enumerate(RUNGS)}
    colors = plt.cm.tab10.colors
    for i, (label, res, note, floor) in enumerate(data):
        xs, ys, lo, hi, powered = [], [], [], [], []
        for q in RUNGS:
            v, e = res[q]["valid"], res[q]["echo"]
            pr, l, h = wilson(e, v)
            xs.append(xpos[q] + (i - len(data) / 2) * 0.06)
            ys.append(pr * 100)
            lo.append((pr - l) * 100)
            hi.append((h - pr) * 100)
            powered.append(v >= floor and v > 0)
        c = colors[i % 10]
        for j in range(2):
            face = c if powered[j] else "white"
            ax.errorbar(xs[j], ys[j], yerr=[[lo[j]], [hi[j]]], fmt="o",
                        mfc=face, mec=c, ecolor=c, capsize=3, ms=7,
                        label=label.replace("\n", " ") if j == 0 else None)
            v = res[RUNGS[j]]["valid"]
            if not powered[j]:
                ax.annotate(f"n={v}", (xs[j], ys[j]), textcoords="offset points",
                            xytext=(0, 9), fontsize=6.5, ha="center", color=c)
        ax.plot(xs, ys, "-", color=c, alpha=0.35, lw=1)
    ax.set_xticks(list(xpos.values()))
    ax.set_xticklabels(["Q4_K_M", "Q2_K"])
    ax.set_ylabel("parent-echo rate among valid outputs (%)")
    ax.set_xlabel("served quantization rung")
    ax.set_ylim(-4, 104)
    ax.legend(fontsize=7, loc="center left", framealpha=0.9)
    ax.set_title("Echo rate by rung across families (hollow = below that wave's power floor)",
                 fontsize=9)
    fig.tight_layout()
    out = os.path.join(HERE, "fig4_family_echo.png")
    fig.savefig(out, dpi=200)
    print("wrote", out)
    for label, res, note, floor in data:
        print(label.replace("\n", " "), {q: (res[q]["echo"], res[q]["valid"]) for q in RUNGS}, note)


if __name__ == "__main__":
    main()
