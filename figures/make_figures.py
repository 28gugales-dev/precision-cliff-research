#!/usr/bin/env python3
"""Paper 2 figures. Every number here is replay-verified by a released no-argument
script (named in each annotation); this file only draws, it computes nothing.
Run with no arguments; writes PDF + PNG beside itself."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))

C_Q2 = "#b2182b"    # 2-bit rung
C_Q4 = "#2166ac"    # reference rung
C_TIER = "#8c8c8c"  # hosted tiers

# ---- Figure 1: echo among valid outputs, Q2_K vs Q4_K_M, across tasks --------
# (task, q2 echo, q2 n, q4 echo, q4 n, replay script)
TASKS = [
    ("circle packing\n(registered seeds)", 17, 18, 3, 20, "sec3_ladder_repro.py"),
    ("circle packing\n(fresh seeds)",      19, 24, 1, 17, "sec3_search_progress.py"),
    ("Heilbronn n=13\n(wave 3)",         186, 295, 53, 113, "wave3_analysis.py"),
    ("LABS n=32\n(wave 5, floor fired)",  10, 233, 12, 60, "wave5_analysis.py"),
]

fig, ax = plt.subplots(figsize=(7.2, 3.4))
x = range(len(TASKS))
w = 0.36
for i, (name, a2, n2, a4, n4, script) in enumerate(TASKS):
    r2, r4 = 100 * a2 / n2, 100 * a4 / n4
    ax.bar(i - w / 2, r2, w, color=C_Q2, zorder=3)
    ax.bar(i + w / 2, r4, w, color=C_Q4, zorder=3)
    ax.text(i - w / 2, r2 + 1.5, f"{a2}/{n2}", ha="center", fontsize=7.5)
    ax.text(i + w / 2, r4 + 1.5, f"{a4}/{n4}", ha="center", fontsize=7.5)
ax.set_xticks(list(x))
ax.set_xticklabels([t[0] for t in TASKS], fontsize=8)
ax.set_ylabel("parent echo among valid outputs (%)")
ax.set_ylim(0, 105)
ax.grid(axis="y", lw=0.4, alpha=0.4, zorder=0)
ax.bar(0, 0, color=C_Q2, label="Q2_K (2-bit)")
ax.bar(0, 0, color=C_Q4, label="Q4_K_M (reference)")
ax.legend(frameon=False, fontsize=8, loc="upper right")
ax.set_title("Echo transfers as a rung contrast, not as absolute bands", fontsize=10)
ax.text(0.01, -0.30,
        "Qwen2.5-Coder-14B GGUF ladder. Counts printed by the released replay scripts. "
        "LABS reverses under a fired control floor (descriptive only, wave5_analysis.py).",
        transform=ax.transAxes, fontsize=6.8, color="0.35")
fig.tight_layout()
for ext in ("pdf", "png"):
    fig.savefig(os.path.join(HERE, f"fig_echo_transfer.{ext}"), dpi=220,
                bbox_inches="tight")
plt.close(fig)

# ---- Figure 2: same task, same parent, same stall — two failure modes --------
# Heilbronn n=13, zero improvements everywhere. Echo vs template rates.
# GGUF: wave3_analysis.py; tiers: wave4_analysis.py.
GROUPS = [
    ("Q2_K",   186 / 295, 45 / 295,  "295"),
    ("Q4_K_M",  53 / 113, 27 / 113,  "113"),
    ("haiku",    0 / 40,  21 / 40,   "40"),
    ("sonnet",   0 / 40,  11 / 40,   "40"),
    ("opus",     0 / 40,  39 / 40,   "40"),
]
fig, ax = plt.subplots(figsize=(7.2, 3.4))
x = range(len(GROUPS))
w = 0.36
for i, (name, echo, tpl, n) in enumerate(GROUPS):
    ce = C_Q2 if name == "Q2_K" else (C_Q4 if name == "Q4_K_M" else C_TIER)
    ax.bar(i - w / 2, 100 * echo, w, color=ce, zorder=3)
    ax.bar(i + w / 2, 100 * tpl, w, color=ce, alpha=0.45, hatch="//", zorder=3)
ax.set_xticks(list(x))
ax.set_xticklabels([f"{g[0]}\n(n={g[3]})" for g in GROUPS], fontsize=9)
ax.set_ylabel("rate among valid outputs (%)")
ax.set_ylim(0, 105)
ax.grid(axis="y", lw=0.4, alpha=0.4, zorder=0)
solid = plt.Rectangle((0, 0), 1, 1, color="0.3")
hatched = plt.Rectangle((0, 0), 1, 1, color="0.3", alpha=0.45, hatch="//")
ax.legend([solid, hatched],
          ["parent echo (copying)", "zero-score template emission"],
          frameon=False, fontsize=8, loc="upper left")
ax.set_title("Heilbronn n=13, identical seed parent, zero improvements anywhere:\n"
             "quantized rungs copy, hosted tiers emit templates", fontsize=10)
ax.text(0.01, -0.34,
        "GGUF rungs: wave3_analysis.py (495 rows). Hosted tiers: wave4_analysis.py "
        "(120 rows, 0/120 echo, DISSOCIATION). Tier precision unattested (C3).",
        transform=ax.transAxes, fontsize=6.8, color="0.35")
fig.tight_layout()
for ext in ("pdf", "png"):
    fig.savefig(os.path.join(HERE, f"fig_two_failure_modes.{ext}"), dpi=220,
                bbox_inches="tight")
plt.close(fig)
print("figures written")
