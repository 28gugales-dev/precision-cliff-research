#!/usr/bin/env python3
"""Paper 1 figure: arm GM3 modal sums against the registered prediction.

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

    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    ax.plot(ns, pred, "k--", lw=1.2, label="registered prediction V(k*, m) / T(k*, N)", zorder=1)
    for c in cells:
        n = c["n"]
        if c.get("status") == "UNSCOREABLE":
            ax.plot(n, c["predicted_4dp"], "x", color="0.55", ms=9, zorder=3)
            ax.annotate(f"UNSCOREABLE\n(valid n={c['valid_n']})", (n, c["predicted_4dp"]),
                        textcoords="offset points", xytext=(0, -26),
                        fontsize=6.5, ha="center", color="0.45")
            continue
        modal = c["modes_4dp"][0]
        match = c["MODE_MATCH"]
        color = "tab:green" if match else "tab:red"
        ax.plot(n, modal, "o" if match else "^", color=color, ms=8, zorder=3,
                mfc=color if match else "none", mew=1.6)
        top, tot = c["mode_freq"].split("/")
        ax.annotate(f"{top}/{tot}", (n, modal), textcoords="offset points",
                    xytext=(0, 8), fontsize=7, ha="center", color=color)
        if not match:
            ax.annotate("", xy=(n, modal), xytext=(n, c["predicted_4dp"]),
                        arrowprops=dict(arrowstyle="->", color="tab:red",
                                        lw=1.0, alpha=0.6))
    ax.plot([], [], "o", color="tab:green", label="modal sum = prediction (MODE-MATCH)")
    ax.plot([], [], "^", color="tab:red", mfc="none", mew=1.6,
            label="modal sum above prediction (miss, upward)")
    ax.set_xlabel("N (circles)")
    ax.set_ylabel("sum of radii (modal value among valid samples)")
    ax.set_title("Arm GM3: second-vendor modal sums vs. the registered prediction",
                 fontsize=9)
    ax.legend(fontsize=7, loc="lower right")
    fig.tight_layout()
    out = os.path.join(HERE, "fig_gm3_anchoring.png")
    fig.savefig(out, dpi=200)
    print("wrote", out)


if __name__ == "__main__":
    main()
