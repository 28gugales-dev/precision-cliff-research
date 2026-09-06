#!/usr/bin/env python3
"""Transfer paper figure: arm GM3 modal sums against the anchor.

Reads arm_gm3_report.json, which arm_gm3_analysis.py regenerates from the raw
ledger (arm_gm_gm3_checkpoint.jsonl) with no arguments — chain documented in
SS9. Regenerate: python fig_gm3_anchoring.py -> fig_gm3_anchoring.png
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rep = json.load(open(os.path.join(HERE, "arm_gm3_report.json"), encoding="utf-8"))
    cells = rep["cells"]
    ns = [c["n"] for c in cells]
    pred = [c["predicted_4dp"] for c in cells]

    # Sized for its print width: the transfer paper places it at 0.44 of a
    # 6.5 in text line (2.86 in), so 1 pt here is 1 pt on the page. The title
    # lives in the caption.
    fig, ax = plt.subplots(figsize=(2.86, 2.15))
    ax.plot(ns, pred, "k--", lw=0.9, label="anchor", zorder=1)
    # Unscoreable cells sit 6 apart in N; alternate their labels above and
    # below the marker so neither collides with the neighbour's count label.
    unscoreable_seen = 0
    for c in cells:
        n = c["n"]
        if c.get("status") == "UNSCOREABLE":
            ax.plot(n, c["predicted_4dp"], "x", color="0.55", ms=6, zorder=3)
            above = unscoreable_seen % 2 == 0
            unscoreable_seen += 1
            ax.annotate(f"UNSCOREABLE\nvalid n={c['valid_n']}", (n, c["predicted_4dp"]),
                        textcoords="offset points",
                        xytext=(0, 5) if above else (0, -17),
                        va="bottom" if above else "top",
                        fontsize=5.5, ha="center", color="0.45")
            continue
        modal = c["modes_4dp"][0]
        match = c["MODE_MATCH"]
        color = "tab:green" if match else "tab:red"
        ax.plot(n, modal, "o" if match else "^", color=color, ms=5.5, zorder=3,
                mfc=color if match else "none", mew=1.2)
        top, tot = c["mode_freq"].split("/")
        ax.annotate(f"{top}/{tot}", (n, modal), textcoords="offset points",
                    xytext=(0, 5), fontsize=6.5, ha="center", color=color)
        if not match:
            ax.annotate("", xy=(n, modal), xytext=(n, c["predicted_4dp"]),
                        arrowprops=dict(arrowstyle="->", color="tab:red",
                                        lw=0.8, alpha=0.6))
    ax.plot([], [], "o", color="tab:green", ms=5.5, label="modal sum = anchor")
    ax.plot([], [], "^", color="tab:red", mfc="none", mew=1.2, ms=5.5,
            label="modal sum above anchor")
    ax.set_xlabel("N (circles)", fontsize=7, labelpad=2)
    ax.set_ylabel("modal sum of radii", fontsize=7, labelpad=2)
    ax.tick_params(labelsize=6.5, length=2.5, pad=2)
    ax.set_ylim(top=max(pred) + 0.28)
    ax.legend(fontsize=6, loc="lower right", frameon=False, handlelength=1.4)
    fig.tight_layout(pad=0.3)
    out = os.path.join(HERE, "fig_gm3_anchoring.png")
    fig.savefig(out, dpi=300)
    print("wrote", out)


if __name__ == "__main__":
    main()
