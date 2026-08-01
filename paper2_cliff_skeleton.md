# Paper 2 skeleton — Precision Cliff + Irreproducibility

Working title: **"The Serving Stack Is Part of the Model: Precision Cliffs and the
Limits of Reproducibility in Agent-Runtime LLM Studies"**

Audience: systems / reproducibility (MLSys, repro workshops at NeurIPS/ICLR).
Target length: 8-9 pages. Leans on paper 1 for WHY the task is precision-sensitive
(one paragraph cross-cite, not a section).

---

## 1. Introduction
- Hook: same alias, same prompt, days apart — different attractor family, different
  validity rate, uniform token counts nobody asked for. The weights behind an alias
  are a promise, not a hash.
- Contributions:
  C1 precision cliff: quantization / serving precision measurably moves outputs on a
     value-sensitive constructive task (paper-0 core data).
  C2 forensic case study: opus_alias arm — behavioral + serving-signature evidence of
     an unattested serving path, undetectable from inside the runtime.
  C3 impossibility argument: an agent runtime cannot be made reproducible from inside
     itself; formal list of what is and is not repairable.
  C4 repair protocol: the maximal reproducibility an agent-runtime study CAN achieve
     (hashes, verbatim raws, dated alias maps, preregistration) — implemented, shipped.

## 2. Background and task
- One paragraph on the packing benchmark + why value depends on precision
  (cross-cite paper 1: anchored constructions sit at exact rational/algebraic values;
  perturbation of the anchor is detectable at 1e-6).
- Serving-stack variables: quantization, fast-mode paths, alias rebinding, sampling
  defaults, system-prompt inheritance.

## 3. The precision cliff (paper-0 data, condensed)
- Quantization sweep results [SLOT: condense §5.x of combined paper].
- Dual-tolerance scoring (1e-9 strict / 1e-6 primary) as the instrument that sees it.

## 4. Forensic case study: the opus_alias arm
- Setup: 30 invocations via agent runtime, alias "opus", user intent "Opus 4.6" —
  runtime accepts alias only. Request unsatisfiable AND undetectably so.
- Serving signature: completions 2.8-5.9s (vs 75-250s Haiku, 150-1170s Sonnet on same
  harness), reported tokens uniform 49,902-49,906 across all 30. Fast-mode serving
  offered on Opus 5/4.8/4.7 at run date; 4.6 absent from offering.
- Behavioral signature: attractor family shift (recursive gaskets, quarter-circle
  constructions), validity 4/30 vs Haiku 32/45 vs Sonnet 30/30.
- Two hypotheses, unseparable without pinned weights: serving-path degradation vs
  genuine tier property. THE POINT: no experiment runnable from inside the runtime
  separates them. That is the finding.

## 5. What is repairable and what is not
- Repairable (implemented in arm_f_repro.py): prompt SHA-256 pre-run; verbatim raw
  storage; run dates + alias→dated-id maps; deterministic local scoring; preregistered
  predictions with falsifiers.
- Not repairable from inside: temperature/top_p/top_k unexposed; alias→weights binding
  unattestable; system-prompt + user-config inheritance unheld across time.
- Table: repairability matrix (item × repairable? × mechanism × residual risk).

## 6. Implications
- Every LLM-evolution / best-of-N study run through an agent harness inherits this;
  affected class includes FunSearch-style loops run on managed runtimes.
- Minimum disclosure standard proposal: (a) alias+date+dated-id map, (b) prompt hashes,
  (c) raw outputs, (d) serving-signature stats (latency, token counts) as anomaly canary.
  Cheap, non-proprietary, catches cases like §4.
- What vendors could expose to close the gap: weights digest, sampling-param echo,
  serving-path flag. Each one line.

## 7. Related work
- Reproducibility-in-ML line; quantization-effects literature; eval-variance studies.
  [SLOT: lit-sweep agent output, systems side.]
- 2605.29268 (same benchmark, program space) for benchmark lineage.

## 8. Limitations
- Single vendor, single runtime observed; serving-signature evidence circumstantial by
  construction (that is the thesis, but say it plainly).
- opus_alias n=30; anomaly uniform across all 30 but one batch window.

---

## Claim → evidence map
| claim | source |
|---|---|
| cliff data | paper-0 combined md §5.x [condense] |
| opus_alias forensics | arm_f_raw.json opus rows, STATE.md §8-8b |
| durations/token uniformity | task usage blocks in session transcript, logged STATE.md §8b |
| repair protocol | arm_f_repro.py header + prereg files |
| alias-map provenance | ALIAS_MAP + RUN_DATE in arm_f_repro.py |

## Open slots before submission
1. Condense paper-0 quantization sections into §3 (writing task, no new data).
2. Lit-sweep systems-side citations.
3. Optional strengthener: second serving-signature snapshot of opus_alias at a later
   date — if signature shifts with no alias change, §4 gains a second data point.
