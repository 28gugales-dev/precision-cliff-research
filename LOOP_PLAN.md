# Paper pipeline loop plan (2026-08-01)

Orchestrator: Fable (this session). Workers: Opus agents (Max-plan subagents, NO API).
Token discipline: workers get file POINTERS not pastes; reports <300 words; one phase
per wakeup; Fable verifies by spot-read against claim-evidence maps, never full re-read.
Corpus root: C:/Users/soham/AppData/Local/hermes/research-corpus/precision-cliff/

## Phase checklist (execute top-down, check off when verified)

- [x] P1. DONE 2026-08-01. ZERO KILLS, all six claims survive; K4 narrowed to the
      combination (hash-locked + exact-output + held-out container). Full verdicts +
      new must-cite set per section: kill_check_2026-08-01.md. Gemini citations
      triaged (real set confirmed, fabrications flagged) in lit_sweep_2026-08-01.md.
      P3 (intro + related work) now UNBLOCKED — must consume kill_check must-cite set.
- [ ] P2a. Paper 1 prose §2-3 (task/recipe/forecast) — Opus writes paper1_draft_sec2-3.md
      from skeleton + STATE.md + n_sweep_forecast + arm_f/arm_g evidence. DISPATCHED
      2026-08-01 alongside loop setup.
- [ ] P2b. Paper 1 prose §4-6 (tier ladder/arm T/faithfulness) — Opus writes
      paper1_draft_sec4-6.md. DISPATCHED 2026-08-01 alongside loop setup.
- [ ] P2c. Fable verify P2a+P2b: every number cross-checked against evidence files;
      no fabricated citations; merge into paper1_draft.md.
- [ ] P3. Paper 1 prose §1 + §7-9 (intro/related/limitations/repro) — Opus, AFTER P1
      verdicts in. Then Fable verify + merge.
- [ ] P4. Peer review panel, paper 1 — 3 Opus personas in parallel:
      (a) Reviewer-2: harsh methods skeptic, hunts overclaiming;
      (b) Stats referee: prereg discipline, Fisher tests, multiple comparisons;
      (c) GECCO/EC domain reviewer: novelty vs FunSearch/QD lit, venue fit.
      Each returns numbered findings, severity-tagged.
- [ ] P5. Council pressure-test — /llm-council on paper 1 core claims + framing.
- [ ] P6. Revision pass — Opus fixes accepted findings from P4+P5; Fable arbitrates
      which findings are valid (reject persona nitpicks that contradict prereg).
- [ ] P7. Gap experiments IF reviews demand — subagent sampling only (haiku/sonnet/opus
      agents), prereg-first, no API. Kaggle only if compute-bound (unlikely; note:
      kernels need no API key for CPU experiments).
- [ ] P8. Paper 2 prose — condense paper-0 cliff data into §3 + write §1-2, 4-8.
      Opus writes, Fable verifies vs STATE.md §8-8b + arm_f_repro.py provenance.
- [ ] P9. Paper 2 review — systems/repro persona (MLSys-style reviewer) + revision.
- [ ] P10. Figures — python scripts (matplotlib, local): trap-zone curve, per-tier
      packing renders, arm-T bar chart. Scripts into corpus, PNGs alongside.
- [ ] P11. Final polish — abstract sync, venue checklist (ALIFE 2026 open now;
      TMLR window through 2026-09-30), claim-evidence map final audit. Report to user.

## Standing rules
- opus_alias caveat on every Opus-arm mention; NEVER "Opus 4.6".
- No API calls, no key usage. Subagents only.
- Never overwrite prereg files or evidence files (arm_*.jsonl, *.json raw) — read-only.
- Loop ends: all boxes checked OR user interrupt OR P1 kill verdict.
- Iteration budget: one phase per wakeup unless phases trivially small.
- CAVEMAN RULE (user order, not suggestion): all orchestrator output caveman-compressed.
  Paper prose, code, prereg text stay normal — everything else compressed.
- HEADROOM RULE (user order): use mcp__headroom__headroom_compress on bulky context
  (agent reports, review findings, transcripts) before carrying across iterations;
  headroom_retrieve when detail needed back. Check headroom_stats if unsure of budget.
- CONTEXT PRESSURE RULE (user order, ~250k trigger): /compact is CLI-only, Fable cannot
  invoke it. Substitute: every wakeup, gauge context pressure (headroom_stats; transcript
  JSONL size as proxy). Pressure high (~250k-token territory) = headroom_compress all
  carried bulk to pointers BEFORE phase work + write any unsaved state to this file so
  imminent auto-compaction loses nothing. Loop is compaction-proof by design: state
  lives here + task list + corpus files, never in conversation memory.
- Kill check = ONE-TIME gate at P1. Never re-run per iteration. Later phases reuse
  its verdicts from file.
- LOOP SELF-EDIT (user grant): Fable may reorder/add/drop phases in this file as work
  reveals needs — log every edit in iteration log with one-line reason.

## Positioning rules (from Gemini feedback triage, 2026-08-01)
- K2 (closed form), K5 (tier inversion), K6 (elicitation-as-intervention) = claimed
  contributions. K1 (anchoring concept), K3 (benchmark), K4 (prereg) = framed as
  rigorous methodology/context, NOT claimed novel. Intro + abstract phrased accordingly at P3/P11.
- Circle packing saturation as evolve-system showcase (AlphaEvolve/OpenEvolve/ShinkaEvolve)
  = strategic strength; say it: we test the assumption on their home benchmark.
- Gemini-named works (Opti-Agent-Bench, MLS-Bench, PoPE, PBRC, GlassballAI, Project
  Ariadne, Reasoning Theater, HELIX, GigaEvo, AdaEvolve) UNVERIFIED — verification agent
  running; none enter any paper without independent confirmation.
- Reject Gemini's K6 inflation ("constraint vector physically pulls coordinates") —
  mechanism claim unsupported; keep behavioral-distribution language only.

## Iteration log
- 2026-08-01 setup: loop created, P2a+P2b dispatched, kill-check running.
- 2026-08-01 Gemini feedback triaged: positioning rules above; verification agent dispatched.
- 2026-08-01 P1 closed: zero kills; kill_check_2026-08-01.md written; citations verified.
- 2026-08-01 iter1: §1+§7-9 Opus writer dispatched (P3 unblocked early — kill-check set in
  hand while §2-3/§4-6 writers still run). Next wakeup: P2c verify+merge when writers done.
- 2026-08-01 iter1b: §4-6 draft landed (2224 w). Conflict 1 (2.75 slack) RESOLVED by
  recomputation: pairwise+wall slack both 0.000e+00 at tol=0, sum 2.7499999991 — draft
  updated to assert flatly. Conflicts 2 (ladder placement) + 3 (p rounding 0.0325) accepted
  as writer resolved. Awaiting §2-3 and §1+§7-9 writers for P2c merge.
