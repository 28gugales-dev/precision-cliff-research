# ============================================================================
# Paper 1 figures. Deterministic: reads only n_sweep_forecast.json and
# arm_f_candidates.jsonl, writes fig1_trapzones.png, fig2_packings.png,
# fig3_armT.png at 150 dpi. No network, no randomness.
# ============================================================================
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

ROOT = Path(__file__).resolve().parent
DPI = 150

# Okabe-Ito colorblind-safe palette
C_PRED = "#0072B2"   # blue: selection-rule prediction
C_BEST = "#009E73"   # green: recipe-family best
C_PUB = "#999999"    # grey: published best known
C_TRAP = "#E69F00"   # orange: trap shading
C_BAD = "#D55E00"    # vermillion: violations


def fig1():
    d = json.loads((ROOT / "n_sweep_forecast.json").read_text(encoding="utf-8"))
    rows = d["rows"]
    n = [r["n"] for r in rows]
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    for z in d["trap_zones"]:
        ax.axvspan(z["n_from"] - 0.5, z["n_to"] + 0.5, color=C_TRAP, alpha=0.18,
                   label="trap zone" if z is d["trap_zones"][0] else None)
    ax.plot(n, [r["published_best_known"] for r in rows], color=C_PUB, lw=1.0,
            ls=":", label="published best known")
    ax.plot(n, [r["recipe_best"] for r in rows], color=C_BEST, lw=1.2,
            ls="--", label="recipe-family best")
    ax.plot(n, [r["predicted"] for r in rows], color=C_PRED, lw=1.6,
            label=r"predicted: $k^*=\mathrm{round}(\sqrt{N})$")
    ax.set_xlabel("N (circles)")
    ax.set_ylabel("sum of radii")
    ax.set_xlim(min(n), max(n))
    ax.legend(loc="upper left", fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(ROOT / "fig1_trapzones.png", dpi=DPI)
    plt.close(fig)


def load_candidates():
    out = []
    for line in (ROOT / "arm_f_candidates.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            out.append(json.loads(line))
    return out


def draw_packing(ax, circles, title, mark_overlaps=False):
    ax.add_patch(Rectangle((0, 0), 1, 1, fill=False, lw=1.2, color="black"))
    bad = set()
    if mark_overlaps:
        for i in range(len(circles)):
            xi, yi, ri = circles[i]
            if min(xi - ri, yi - ri, 1 - xi - ri, 1 - yi - ri) < -1e-9:
                bad.add(i)
            for j in range(i + 1, len(circles)):
                xj, yj, rj = circles[j]
                if ((xi - xj) ** 2 + (yi - yj) ** 2) ** 0.5 - ri - rj < -1e-9:
                    bad.add(i); bad.add(j)
    for i, (x, y, r) in enumerate(circles):
        col = C_BAD if i in bad else C_PRED
        ax.add_patch(Circle((x, y), r, fill=False, lw=1.0, color=col))
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(title, fontsize=8)


def fig2():
    rows = load_candidates()

    def pick(pred):
        for r in rows:
            if pred(r) and r.get("circles"):
                return r
        return None

    haiku = pick(lambda r: r["arm"] == "bare" and r["n"] == 21 and r.get("valid")
                 and abs(r.get("sum_of_radii", 0) - 2.1) < 2e-3)
    sonnet = pick(lambda r: r["arm"] == "sonnet_bare" and r["n"] == 31 and r.get("valid")
                  and abs(r.get("sum_of_radii", 0) - 2.75) < 1e-3)
    opus = pick(lambda r: "opus" in r["arm"] and not r.get("valid"))

    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.6))
    panels = [
        (haiku, "Haiku: uniform r=1/10 truncation, N=21\n(on-prediction, 2.1000000)", False),
        (sonnet, "Sonnet: mixed-radius escape\n(2.7499999991, tangency-tight)", False),
        (opus, "opus_alias: ambitious attempt\n(overlaps in red, invalid)", True),
    ]
    for ax, (row, title, mark) in zip(axes, panels):
        if row is None:
            ax.text(0.5, 0.5, "sample not found", ha="center")
            ax.set_axis_off()
            continue
        draw_packing(ax, row["circles"], title, mark_overlaps=mark)
    fig.tight_layout()
    fig.savefig(ROOT / "fig2_packings.png", dpi=DPI)
    plt.close(fig)
    return {k: (v["arm"], v["sample_id"]) if v else None
            for k, v in {"haiku": haiku, "sonnet": sonnet, "opus": opus}.items()}


def fig3():
    # Registered outcomes, STATE.md §9 / arm_t_analysis.py output.
    labels = ["on-prediction\n(among valid)", "validity"]
    bare = [35 / 50, 50 / 60]      # 70% anchor; bare validity pooled 50/60
    trace = [46 / 53, 53 / 60]     # 87% anchor; trace_v2 validity pooled 53/60
    x = range(len(labels))
    w = 0.34
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    ax.bar([i - w / 2 for i in x], bare, w, color=C_PUB, label="bare")
    ax.bar([i + w / 2 for i in x], trace, w, color=C_PRED, label="trace_v2")
    for i, (b, t) in enumerate(zip(bare, trace)):
        ax.text(i - w / 2, b + 0.01, f"{b:.0%}", ha="center", fontsize=8)
        ax.text(i + w / 2, t + 0.01, f"{t:.0%}", ha="center", fontsize=8)
    ax.set_xticks(list(x)); ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylim(0, 1.18)
    ax.set_ylabel("proportion")
    ax.annotate("p = 0.0325", xy=(0, max(bare[0], trace[0]) + 0.07),
                ha="center", fontsize=8)
    ax.annotate("n.s. (p = 0.30)", xy=(1, max(bare[1], trace[1]) + 0.07),
                ha="center", fontsize=8)
    ax.legend(frameon=False, fontsize=8, loc="upper center", ncol=2)
    fig.tight_layout()
    fig.savefig(ROOT / "fig3_armT.png", dpi=DPI)
    plt.close(fig)


if __name__ == "__main__":
    fig1()
    picked = fig2()
    fig3()
    print("figures written; fig2 exemplars:", picked)
