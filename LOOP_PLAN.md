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
- REVERTIBILITY (user order): corpus is now a git repo (revert point 84e4db0,
  2026-08-01). Commit after every iteration's file changes, one-line message.
  Revert anything: git checkout / git revert. Never force-push (no remote anyway),
  never delete evidence files.
- WORKER MODEL RULE (user order): subagents = Opus at MEDIUM effort where effort is
  settable (Workflow agent() opts.effort='medium'); Agent tool lacks effort param —
  model:'opus' only, never model:'fable' for workers. Fable = orchestrator only.
  Cheap mechanical lookups may use sonnet/haiku.
- RESOURCE: user has NotebookLM in Chrome + notebooklm MCP — usable for source-grounded
  Q&A on uploaded corpora if a phase needs it (e.g. checking venue guidelines, related-work
  digestion). Optional, not required.

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

## Per-phase resource map (user order: name optimal tools per step, token-lean)
| phase | workers | tools/skills/MCPs | token notes |
|---|---|---|---|
| P2c verify+merge | none (Fable) | Bash python recompute, Grep spot-checks | never full-file re-read; grep numbers only |
| P4 review panel | 3x Agent opus | plain persona prompts; findings to files | reviewers write findings to corpus files, return 1-line counts |
| P5 council | Fable invokes | Skill: llm-council | feed abstract + claim map only, not full drafts |
| P6 revision | 1x Agent opus | headroom_compress findings first | worker gets finding list + file pointers |
| P7 gap experiments | Agent haiku/sonnet samplers | arm_f_repro.py protocol, collect_raw.py regexes | prereg first; label-exact dispatch (HOW_TO_RUN.md) |
| P8 paper 2 prose | 1x Agent opus | paper2 skeleton + STATE §8-8b + precision-cliff-paper-outline.md | pointer-based, no pastes |
| P9 paper 2 review | 1x Agent opus | MLSys persona | same file-based findings |
| P10 figures | Fable local | Bash python matplotlib; Read on PNGs to verify | no browser, no screenshots |
| P11 polish | Fable + 1 opus | WebFetch venue pages (ALIFE/TMLR); NotebookLM optional | fetch format rules once, cache in file |
| backup (every iter) | Fable | PowerShell robocopy to OneDrive; git commit | free, zero context cost |
| backup (milestones) | Agent sonnet | Drive MCP create_file to folder 1duA4rzycj1Ad2pGKA6XOT5VQt7WGWtqG | delegate = bytes stay out of orchestrator context |
| any code search | Fable | Grep/Glob direct | corpus tiny + known layout; graphify skipped deliberately |

## Skill/plugin bindings per phase (explicit, user order)
| phase | Claude skills / plugins to invoke | why |
|---|---|---|
| ALL | caveman (full) — orchestrator output; brain skill verifying-before-done before checking any box | style rule + done-gate |
| P2c merge | grounding-claims-in-evidence (rigid) — every number recomputed or grep-verified before assert | prevents draft drift |
| P4 panel | validating-with-fresh-eyes — personas get NO access to our justifications, only draft + evidence files | uncontaminated review |
| P5 council | llm-council skill (installed) | user-designated pressure-test tool |
| P6 revision | intercepting-rationalizations (rigid) — when tempted to reject a finding because fixing is work | arbitration honesty |
| P7 experiments | planning-before-building + premortem-thinking BEFORE prereg write; root-cause-investigation on anomalies; pr-review-toolkit:silent-failure-hunter on new analysis code | prereg discipline |
| P8-P9 paper 2 | grounding-claims-in-evidence again; calibrating-confidence on serving-signature claims | forensic sections risk overclaim |
| P10 figures | ponytail-review on figure scripts (complexity cut); verifying-before-done on rendered PNGs (Read them) | scripts stay minimal |
| P11 polish | communicating-outcomes for final user report; humanizer (antigravity) OPTIONAL on abstract readability — never on technical sections | report quality |
| NOT used (deliberate) | graphify (corpus tiny), gstack-review/qa (built for app code diffs, not paper corpus; revisit only if P7 spawns real experiment code), taste-skill/gsap/frontend (no UI), context7 (no library APIs in play; matplotlib basic) | listed so future iterations don't re-litigate |

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
- 2026-08-01 iter1c: §1+§7-9 landed (~2400 w, 40 citations, positioning executed). Merge
  fixes queued for P2c: restore FunSearch (Romera-Paredes et al., Nature 2023) to §1/§7.1;
  restore skeleton anchoring-bias trio (2505.15392, 2412.06593, 2410.15413) + faithfulness
  trio (2503.08679, 2606.13603, 2605.29087) — real citations from earlier sweep, writer
  excluded them only by authoritative-file rule. Consider BehaveSim + Strategy Diversity adds.
  Drive backup rerun on haiku after sonnet safeguard false-positive; OneDrive mirror done (90 files).
