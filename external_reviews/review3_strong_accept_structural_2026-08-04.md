# External review 3 — full paper, "Strong accept with structural changes"

Received 2026-08-04 (user-supplied, external model). Target: full paper (rev2). NOTE: later sections (premortem items 4–6) contain degraded/incoherent text — see assessment file.

---

**Overall: Strong accept with structural changes.** Core finding real, well-measured, unusually honest. Empirics = strong suit; structure = weak suit — it buries the ladder.

## 1. The paper's real architecture

Three papers inside one document:

| Layer | Content | Deserved weight |
|---|---|---|
| A: closed form (§2-3) | behavioral law, prereg point predictions, mode ceiling, out-of-sample transfer | 60% |
| B: tier ladder (§4) | three attractor families; opus_alias caveat bomb | 25% |
| C: elicitation (§5-6) | trace intervention + faithfulness; knows it's weak | 15% |

Problem: narrated A→B→C but C occupies ~40% of text with a result failing multiplicity, carried by one cell, wave-confounded. Reader finishes §5-6 thinking "fragile" and retroactively discounts §3. Fix: shrink §5-6 / move to appendix; don't end on weakest material.

## 2. §3.3 mode ceiling = the paper's title slide

Strongest single exhibit; belongs right after intro, not buried. Figure 1 first, then mode-ceiling table, then narrative.

## 3. Under-sold assets

- **Trap zones**: catchy term, usable facts ("don't benchmark at N=21"). Make a section header + full N-sweep shaded figure.
- **Round-number baseline (2/69 = 3%)**: nearly the most devastating evidence, currently one clause. Make explicit side-by-side table.
- **"k* is a definition" honesty**: creates thinness problem — only 4 independent branch-rule tests (k = 4,5,6,7). State explicitly; N=57 (k=8) is the missing fifth. Run it if constraints allow.

## 4. Structure moves

- Reproducibility-posture box after §3.1 (4 lines: which hashes exist, which don't) instead of §9 burial.
- §2.4 premature cross-ref to §7 — replace with 2-sentence inline summary.
- §5.3 falsifier paragraph: rewrite framing so it's legible without knowing the project's internal review history.
- Table 5 → supplement. End the paper on §8 (limitations-forward), not the stopping rule.

## 5. Substance below the bar

- **opus_alias arm**: either cut entirely (Haiku+Sonnet already shows the qualitative shift) or keep as properly caveated pointer. Best forward move: rerun P-O1/O2/O4 on open-weight tier (weights known) — converts caveat into separated finding.
- **P-T3**: rename §5.4 block to "Limits of P-T3"; wave confound possibly severe — one-cell + wave = potentially inflated peak.
- **Rectangle transfer**: 5/11, CI [21%,72%], no-hash no-timestamp ledger = replicability weakest link. Run second rectangle cell at n = 40+ with hashed prompt — converts "partial support" into confirmation or clean negative.

## 6. Proposed section order

1. Introduction + Trap Zones (merged) · 2. Task and Recipe Family · 3. Preregistered Forecast → Mode Ceiling · 4. Rectangle Transfer · 5. Tier Ladder · 6. Elicitation (short, explicitly secondary) · 7. Related Work · 8. Corrections table (from §9) · 9. Reproducibility (200-word provenance list, not filedump).

## 7. Premortem (items 1–3 coherent; 4–6 degraded in original)

1. "No one asked for a weak-tier law" rejection — pre-empt via §7 + framing as groundwork for the mutation-arm experiment.
2. Method-line confound — already disclosed via bundling note; keep visible.
3. N=57 unsampled while k=8 zone appears in abstract/§1/§2.4/Fig 1 — reviewer will notice. Sample it or scope the figure. Also: Fig 1 caption contains internal revision note — remove before publication.
4–6. [Original text degraded/incoherent — retained points where recoverable: run N=35/37 top-ups to n≈10–20; P5 "consistent with" at n=4 needs ~20 samples for the separability claim.]

## Summary — do these if nothing else

1. Reorder: mode-ceiling table first.
2. §5-6 down to ~15% of paper.
3. Sample N=57.
4. Rectangle defense cell at n=20+ with proper hashing.
5. Table 5 to appendix.
