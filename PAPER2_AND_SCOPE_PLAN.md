# Paper 2 work + paper 1 scope angles

Written 2026-08-07. Paper 1 v1 submits 2026-08-12.

## Governing rule

**Paper 1 v1 ships 08-12 unchanged.** It is submission-ready. Every scope-widening
arm below is v2/venue work, preregistered *after* v1 is on arXiv so the prereg
commit can cite the v1 identifier. Nothing here touches a registered claim before
submission — post-hoc widening of a preregistered claim would burn the paper's
single largest asset, and the 20 Tier A recipients are exactly the people who
check that first.

---

## Paper 2: state

Never externally reviewed. All 12 reviews went to paper 1. The paper with the
stronger finding has had zero adversarial scrutiny.

### The provenance split

| section | evidence | status |
|---|---|---|
| §4 `opus_alias` forensics | `arm_f_raw.json`, recomputable via `arm_f_repro.py` | **verifiable now** |
| §4 durations | `STATE.md` session-log ranges; per-invocation vector never captured | **unrepairable, disclosed** |
| §3 7B ladder | `handoff/kaggle/output/phase4-ad-run/phase4_ad_samples.jsonl` (868 KB) | **local, needs checking** |
| §3 dispersion probes | `precision-cliff-fixed-parent-dispersion-probe{,-v2}/probe_samples.jsonl` | **local** |
| §3 **14B ladder** | `candidates_v4.jsonl` + `provenance.json`, produced by `kaggle_precision_sweep_14b_{fresh,v2_pushed,iq2}.py` | **NOT LOCAL — Kaggle only** |

The 14B ladder is the quantitative backbone: parent-echo 14% → 94% at the 2-bit
rung, 79 vs 6% on fresh seeds, Fisher p = 0.007 / 1.7e-7 / 3.4e-6. Paper 2
currently cites these to `../precision-cliff-paper-combined.md` — a prose
document, not raw rows. Paper 1's numbers were all recomputed from raw JSONL.
Paper 2 does not yet meet the standard paper 1 set for itself, and a reviewer
will check that first.

### Ordered work

1. **Retrieve the 14B ladder from Kaggle.** Blocked: no credentials in this
   session (`~/.kaggle/kaggle.json` absent, `KAGGLE_KEY` unset), though the CLI
   is installed at `hermes-agent/venv/Scripts/kaggle.exe`. Owner or hermes must
   pull `candidates_v4.jsonl` and `provenance.json` from the sweep kernels.
   *If unrecoverable:* re-run vs. re-scope §3 is a real cost decision, owner's
   call — not one to make silently.
2. **Write the ladder equivalent of `arm_f_repro.py`.** Re-derive every §3
   headline number from raw rows. This is the single highest-value paper 2 task.
3. **First external review** via `dispatch.ps1 -Model deepseek-v4-flash` — the
   pipeline that produced review 12. Can run in parallel with 1–2, since it will
   surface issues beyond provenance.
4. **Leave §4 durations alone.** Already disclosed as the paper failing its own
   standard. A retroactive fix would be manufactured.

---

## Paper 1: scope angles, ranked

All post-v1. Ranked by structural value per unit cost.

### 1. Finish GM3 — cross-vendor arm (free, 63/140 done)

The strongest scope limitation in paper 1 is "established so far within a single
vendor lineage" (§8). GM3 is Gemma — a second vendor. Finishing it converts a
stated limitation into an answered one.

Cost: already paid, just needs to run. Two cautions:
- Two `arm_gm_run.py` processes respawned after an earlier kill (PIDs 41472,
  15564). Find the parent before killing again.
- Stale `done_pairs` snapshots across concurrent runners duplicate `(n, idx)`
  pairs. Re-run the duplicate check before scoring — this is now a paper artifact.

### 2. Pinned-endpoint strong-tier arm (highest structural value)

Replaces the `opus_alias` hole with an attested serving path. Strengthens both
papers at once: paper 1 gets a real third tier instead of an unattributable one;
paper 2 gets the positive control its forensic argument currently lacks.

### 3. Tractability mechanism test

The paper concedes an untested mechanism-free alternative, and its own CH arm
points at it ("the template is less what the model prefers than what it can
reliably build"). Review 3 flagged the resulting rejection risk.

Design direction: perturbed instances where the template arithmetic stays easy
but the template is *wrong*. The `qd-contam` programme already specifies this
shape — an instance where the memorised or default answer is no longer optimal.
Separating "prefers" from "can build" is the difference between a behavioural
regularity and a mechanism.

### 4. Third container / additional N

Cheap, incremental, lowest priority. Does not answer any stated objection.

---

## Cross-dependency the send waves create

18 of the 59 outreach drafts pitch paper 2. `[ARXIV_LINK]` resolves on 08-12 for
**paper 1 only**. Those 18 emails currently ask people to read a paper they
cannot obtain.

Three options: paper 2 also goes to arXiv (needs §3 provenance fixed and at least
one review first), or those 18 hold until it does, or they attach a draft PDF.

This gives paper 2 a real deadline tied to the send waves — it is "before wave 2",
not "when convenient".

---

## Still open, unrelated to the above

- Re-run mit, caltech-jpl, stonybrook-bu (mit's v1 archive holds O'Reilly, Tier A)
- 19 drafts missing `[ARXIV_LINK]`
- `princeton/audit.md` never written — its 6 rows skipped Phase 3 verification
- `berkeley/Garcia` `paper_title` holds the sender's paper
- **Author name still unresolved** — blocks arXiv and every one of the 59 emails
