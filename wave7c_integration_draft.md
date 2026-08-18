# Wave-7c integration staging — paper 2 text, two branches

NOT paper text yet. Numbers marked ⟨…⟩ fill from wave7c_analysis.py output
when the gemma kernel lands. gpt-oss numbers are final (analysis run
2026-08-16, replay clean). Whichever branch fires, the paragraph goes after
the wave-7b paragraph (paper2_short.md line ~251), one evidence-map row per
family, abstract sentence updated, LaTeX mirrored.

## Shared opening (both branches)

Wave 7c (`wave7c_prereg_screened_families.md`, SHA-256 `b1fc9ee9…`, public
Kaggle dataset before sampling) changed the selection procedure, not the
test: candidates were chosen by a disclosed 50-call competence screen through
an OpenRouter alias (screen_s_doc.md, committed before screen sampling;
selection record in the prereg, screen numbers are gating decisions and
appear nowhere as evidence). Two families advanced to the pinned-GGUF ladder
— gemma-4-31B-it (43/50 screen-valid) and gpt-oss-20B (27/50, its MXFP4-
native parent disclosed at lock as a rung qualifier) — with
nemotron-3-super-120B advanced-not-run (hardware) and two families not
selected, one of them (north-mini-code) on 49/50 reasoning-censored empties,
the amendment-3 failure mode reproduced cross-vendor.

## gpt-oss result (final, both branches)

The gpt-oss arm returned UNDERPOWERED at both rungs — 5 valid rows in 100
loop calls at Q4_K_M against a 20-valid floor, 0 at Q2_K — after passing the
screen at 27/50 through the API path. Two descriptives, unclaimable: all
five valid Q4_K_M rows are coordinate-exact parent echoes (echo at the
CONTRAST rung — no prior family echoes there while producing nothing at
Q2_K), and its single valid must-differ probe echoed despite the prohibition
(1 probe, floor is 5). The screen-to-ladder validity collapse (27/50 served
full-precision → 5/50 at local Q4_K_M) is consistent with the MXFP4
qualifier registered at lock: K-quant rungs of an MXFP4-native release may
measure conversion damage rather than bit-width sensitivity, which is why
the family's rungs carry that label in every mention.

## Branch A — gemma evaluable (≥20 valid both rungs)

Gemma-4-31B is the first non-Qwen family to clear the competence floor at
both rungs: ⟨valid_q4⟩ and ⟨valid_q2⟩ valid rows. The registered primary
7c.1: echo(Q2_K) ⟨e2⟩% − echo(Q4_K_M) ⟨e4⟩% = ⟨gap⟩pp → ⟨HELD/REFUTED/
INCONCLUSIVE⟩. [If HELD: the echo cliff is no longer a Qwen-family
observation — a second lineage, selected by a disclosed screen rather than
by outcome, reproduces the Q2_K echo signature under SHA-pinned weights.]
[If REFUTED: with one family evaluable and refuted, the disconfirmation
clause (all-advanced-refuted) ⟨fires/does not fire⟩; family-dependence is
the reading and the abstract's scope sentence says so.] 7c.2 (floor-gated):
⟨…⟩. 7c.3 must-differ: ⟨…⟩. Abstract sentence replaces "two tasks plus four
non-Qwen families sit below their own registered competence floors, leaving
family generality unresolved" with: "…five non-Qwen families sat below their
registered competence floors until a screened sixth cleared it; on that
family the echo contrast ⟨verdict clause⟩."

## Branch B — gemma underpowered (<20 valid at either rung)

The registered SS6 branch fires: screen passage at an unattested serving
precision (43/50, four providers logging fp-serving) does not predict
local-ladder competence at Q2_K/Q4_K_M — on two families out of two, with
the same instrument that found 12/13 validity on free-tier-delivered calls.
That mismatch is itself the wave's finding, and it is a serving-path result:
the quantity the screen measures (format competence under whatever precision
the alias serves) and the quantity the ladder measures (competence under
pinned 2- and 4-bit weights) come apart in exactly the direction SS3's cliff
predicts. Family generality is stated unresolved after three waves and six
non-Qwen families, no fourth attempt on this task; the abstract keeps its
unresolved clause with the count updated.

## Evidence-map rows (fill numbers)

| §8 wave 7c gemma4_31b: ⟨verdicts⟩ | `wave7c_output/wave7c_gemma4_31b/` ledger (100 rows), replayed by `wave7c_analysis.py`, no arguments. Registration `wave7c_prereg_screened_families.md` SHA `b1fc9ee9…`, public Kaggle dataset + public kernel pushed before sampling |
| §8 wave 7c gpt_oss_20b: UNDERPOWERED both rungs (5 valid Q4_K_M — all parent echoes — 0 Q2_K); MXFP4-conversion qualifier registered at lock | `wave7c_output/wave7c_gpt_oss_20b/` ledger (100 rows), same replay/registration chain |

## Also queued at integration (both branches)

- Paper 2 §6: one paragraph, three live exhibits from the screen ledger —
  provider churn (4 upstreams in one 50-call run through one unchanged
  alias), cross-vendor reasoning-budget censoring (north-mini 49/50,
  nemotron rows finish=length), free-tier serving starvation (gemma :free,
  single upstream, 37/50 transport holes) — each as corroboration of the
  repair protocol's per-row provider/finish_reason logging items.
- fig4_family_echo.py regenerate (gemma auto-joins); insert as paper 2
  figure with caption noting per-wave floors.
- Paper 1 §8 scope touch + abstract count only if Branch A HELD.
- LaTeX: sec_forensic_repair.tex (wave-7c + §6 paragraphs),
  sec_evidence_map.tex (rows), main.tex abstract; recompile; verify via
  registered-number grep.
