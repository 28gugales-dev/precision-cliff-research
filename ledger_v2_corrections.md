# Ledger v2 — provenance corrections to `arm_f_candidates.jsonl`

Produced 2026-08-01 in response to referee findings **F2**, **F3**, **F4** in
`p4_review_stats.md`.

- **Input (immutable evidence, never modified):** `arm_f_candidates.jsonl`
  — sha256 `02ecabcdd07f55193844873ed05c67b54bda26b7d158978b9658d358ae2cf235`,
  215 rows, mtime 2026-08-01 01:14:34.
- **Output:** `arm_f_candidates_v2.jsonl`
  — sha256 `9f845f78e02da977f5fcedae5cf1778f9d300dc5ebeb784d15ce2ed01a1c00c0`,
  215 rows, same row order.
- **Scope:** metadata only. No scored quantity, geometry, raw output, arm label
  or sample id was touched. Every corrected field carries a sibling `*_v1`
  field holding the original value, so v2 is self-documenting against v1.

Fields added by this revision: `prompt_sha256_v1`, `prompt_sha256_note`,
`run_date_v1`, `proposer_alias_v1`, `proposer_dated_id_on_run_date_v1`,
`proposer_dated_id_on_run_date_note`, `metadata_revision` (= `"v2"`),
`metadata_revision_wave`.

---

## Rule 1 — `prompt_sha256` (addresses F2)

**Sources.** `arm_t_preregistration.txt` lines 20–33 (trace_v2 template + six
registered hashes); `arm_f_prompts.json` (bare templates/hashes for
N=13/17/31/35/37); `STATE.md` §6 ("Same bare prompt, proposer = sonnet") and
`arm_o_preregistration.txt` line 5 ("bare prompt identical to Haiku/Sonnet
arms").

**Independent verification performed before rewriting anything.** The bare and
trace_v2 templates were re-hashed locally from the verbatim text in the two
source files. All ten hashes reproduce exactly — including the N=21 and N=43
bare hashes, which appear in no prompts file and were confirmed by
reconstructing the bare template at those N:

| N | bare sha256 (recomputed) | matches |
|---|---|---|
| 13 | `32db485bea62…` | prompts file + prereg |
| 17 | `8437df753f98…` | prompts file |
| 21 | `a415425b4ed5…` | prereg line 30 |
| 31 | `a664d003cbf1…` | prompts file + prereg |
| 35 | `3b08c56e587d…` | prompts file |
| 37 | `2c0a88191cb2…` | prompts file |
| 43 | `1208e7d2a004…` | **ledger only — registered nowhere** (see Caveats) |
| 13 | trace_v2 `a920f1c9e1b9…` | prereg line 29 |
| 21 | trace_v2 `9120572793cd…` | prereg line 31 |
| 31 | trace_v2 `bd490b7b02cb…` | prereg line 33 |

| Change | Rows | Detail |
|---|---:|---|
| `prompt_sha256` → per-N **trace_v2** hash | **60** | `arm=trace`, `sample_id` 101–120 at N=13/21/31 (20 each). Was the bare hash for that N. `prompt_sha256_v1` preserves it. |
| `prompt_sha256` → `null` + note | **10** | `arm=trace`, `sample_id` 1–10 at N=21 — the pilot. |
| unchanged | **145** | 85 `bare` + 30 `sonnet_bare` + 30 `opus_alias`. |

**Pilot rows.** Neither `arm_t_preregistration.txt` nor `STATE.md` records a
hash for the pilot prompt. The prereg (lines 12–18) states only that the pilot's
base wording drifted from the bare template (missing `[0,1]x[0,1]` tokens,
reworded output line) and that pilot samples are never pooled with trace_v2. A
repo-wide grep for a pilot/trace prompt constant or hash returns nothing.
Per the rule, those ten rows therefore get:

```json
"prompt_sha256": null,
"prompt_sha256_v1": "a415425b4ed5a57ea9b6f09c2328508f12370e1624734e1c5ed32913741795a9",
"prompt_sha256_note": "pilot prompt not registered; verbatim prompt recovered in prereg disclosure"
```

Stamping them with the bare N=21 hash — as v1 did — asserted something the
prereg explicitly contradicts. `null` is the honest value.

**Bare / sonnet / opus rows kept their bare hashes because the sources say so,
not by assumption:** `arm_o_preregistration.txt` states the Opus arm used the
bare prompt "identical to Haiku/Sonnet arms", and `STATE.md` §6 states the
Sonnet arm used the "Same bare prompt". Both were verified by reading, not
inferred from the stamped value.

---

## Rule 2 — `run_date` (addresses F3)

v1 stamped all 215 rows `2026-07-30`. Waves derived from `STATE.md` section
headers and their contents:

| Wave key | STATE.md source | run_date | Rows | Composition |
|---|---|---|---:|---|
| `W1_armF_original` | `## v8 (2026-07-30, cont.)` — "25 fresh Haiku proposers, 5 each at N = 13, 17, 31, 35, 37" | **2026-07-30** (unchanged) | 25 | `bare` N=17/35/37 s1–5; `bare` N=13/31 s1–5 |
| `W2_v9_deepening` | `## v9 (2026-07-31)` §1 + §3; double-check pass "arm_f 55 rows (bare 45 + trace 10)" | **2026-07-31** | 30 | `bare` N=21 s1–10, `bare` N=43 s1–10, `trace` pilot N=21 s1–10 |
| `W3_sonnet_arm` | `## v9 landscape check (2026-07-31, Fable seat)` §6, §7 | **2026-07-31** | 30 | `sonnet_bare` N=13/21/31 |
| `W4_opus_alias_arm` | same 2026-07-31 header, §8, §8b; corroborated by `arm_o_preregistration.txt` line 1 ("2026-07-31") | **2026-07-31** | 30 | `opus_alias` N=13/21/31 |
| `W5_armT_scaled` | `### 9. ARM T SCALED (2026-08-01)` — "100 new invocations: bare to 20/N, trace_v2 20/N at N=13/21/31" | **2026-08-01** | 100 | `bare` N=13 s6–20, N=21 s11–20, N=31 s6–20 (40); `trace` s101–120 at N=13/21/31 (60) |

**Arithmetic that pins the wave boundaries** (not guesswork): v8 collected
5 per N at five cells = 25 bare rows. The v9 double-check pass tallies the
ledger from disk at 55 rows = 45 bare + 10 trace, so v9 added exactly 20 bare
(N=21 ×10, N=43 ×10, the two cells v8 never sampled) plus the 10-sample trace
pilot. §9 states the arm-T wave added 100 invocations, and 215 − 55 − 30
(Sonnet) − 30 (Opus) = 100. Every row is accounted for; no cell is split
ambiguously.

| Change | Rows |
|---|---:|
| `run_date` `2026-07-30` → `2026-07-31` (+ `run_date_v1`) | **90** |
| `run_date` `2026-07-30` → `2026-08-01` (+ `run_date_v1`) | **100** |
| unchanged (`2026-07-30`, correct as stamped) | **25** |
| `run_date_note = "wave date not recorded"` | **0** — every wave was derivable |

The arm-T rows now post-date `arm_t_preregistration.txt` (written 2026-08-01,
"BEFORE any arm-T proposal was sampled"), which is the ordering F3 required.

---

## Rule 3 — `proposer_alias` / `proposer_dated_id_on_run_date` (addresses F4)

| Change | Rows |
|---|---:|
| `proposer_alias` `haiku` → `sonnet` (+ `_v1`) | **30** (`sonnet_bare`) |
| `proposer_alias` `haiku` → `opus` (+ `_v1`) | **30** (`opus_alias`) |
| `proposer_dated_id_on_run_date` `claude-haiku-4-5-20251001` → `null` (+ `_v1` + note) | **60** (both tier arms) |
| alias / dated id unchanged | **155** (85 `bare` + 70 `trace`) |

Note applied to all 60 tier-arm rows:

```json
"proposer_dated_id_on_run_date_note": "alias-addressed dispatch; backing dated id not attestable from runtime"
```

This records what was actually addressed (an alias) and declines to assert a
binding the runtime never exposed — the paper's own §8 position, now enforced in
the artifact rather than only in prose. `STATE.md` §8 is explicit: *the agent
runtime accepts only the alias "opus" — no dated ids*, and
`arm_o_preregistration.txt` line 3 calls the alias→weights binding "a promise
not a hash". The Sonnet arm is the same dispatch mechanism; `arm_s_preregistration.txt`
records no dated id either.

**Haiku rows verified, not assumed.** `arm_t_preregistration.txt` line 3:
*"Proposer alias: haiku (claude-haiku-4-5-20251001 in force on this date)"*, and
`STATE.md` v8 records "the alias->dated-id mapping in force on that date". The
`bare` and `trace` stamps are therefore correct as written and were left alone.
The same alias-binding caveat applies to them in principle; it is disclosed in
the paper text and was not injected here, since these rows do carry a recorded
dated-id mapping and the tier rows do not.

---

## Sanity check (verbatim output)

```
  [PASS] row count v2 == 215  -- got 215
  [PASS] row count v2 == v1  -- v1=215 v2=215
  [PASS] per-arm counts match v1  -- bare=85 opus_alias=30 sonnet_bare=30 trace=70
  [PASS] per-(arm,N) counts match v1  -- 16 cells
  [PASS] row order / identity (arm,n,sample_id) preserved
  [PASS] sum_of_radii byte-identical to v1  -- 166 rows carry field, 0 mismatch
  [PASS] circles byte-identical to v1  -- 209 rows carry field, 0 mismatch
  [PASS] valid byte-identical to v1  -- 215 rows carry field, 0 mismatch
  [PASS] no non-metadata field changed  -- {}
  [PASS] every changed field has a faithful *_v1 sibling  -- {}
  [INFO] sha256 v1 = 02ecabcdd07f55193844873ed05c67b54bda26b7d158978b9658d358ae2cf235
  [INFO] sha256 v2 = 9f845f78e02da977f5fcedae5cf1778f9d300dc5ebeb784d15ce2ed01a1c00c0
  [INFO] v1 mtime = 2026-08-01 01:14:34 (unmodified; opened read-only)

  RESULT: ALL CHECKS PASS
```

`sum_of_radii` is present on 166 of 215 rows and `circles` on 209 — the
remainder are parse/harvest failures that legitimately carry neither. The check
compares field *presence* as well as value, so a silently dropped field would
have failed.

### Post-correction distribution

```
      5  bare        N=13 2026-07-30  haiku  claude-haiku-4-5-20251001    32db485bea62
     15  bare        N=13 2026-08-01  haiku  claude-haiku-4-5-20251001    32db485bea62
      5  bare        N=17 2026-07-30  haiku  claude-haiku-4-5-20251001    8437df753f98
     10  bare        N=21 2026-07-31  haiku  claude-haiku-4-5-20251001    a415425b4ed5
     10  bare        N=21 2026-08-01  haiku  claude-haiku-4-5-20251001    a415425b4ed5
      5  bare        N=31 2026-07-30  haiku  claude-haiku-4-5-20251001    a664d003cbf1
     15  bare        N=31 2026-08-01  haiku  claude-haiku-4-5-20251001    a664d003cbf1
      5  bare        N=35 2026-07-30  haiku  claude-haiku-4-5-20251001    3b08c56e587d
      5  bare        N=37 2026-07-30  haiku  claude-haiku-4-5-20251001    2c0a88191cb2
     10  bare        N=43 2026-07-31  haiku  claude-haiku-4-5-20251001    1208e7d2a004
     10  opus_alias  N=13 2026-07-31  opus   None                         32db485bea62
     10  opus_alias  N=21 2026-07-31  opus   None                         a415425b4ed5
     10  opus_alias  N=31 2026-07-31  opus   None                         a664d003cbf1
     10  sonnet_bare N=13 2026-07-31  sonnet None                         32db485bea62
     10  sonnet_bare N=21 2026-07-31  sonnet None                         a415425b4ed5
     10  sonnet_bare N=31 2026-07-31  sonnet None                         a664d003cbf1
     20  trace       N=13 2026-08-01  haiku  claude-haiku-4-5-20251001    a920f1c9e1b9
     10  trace       N=21 2026-07-31  haiku  claude-haiku-4-5-20251001    null
     20  trace       N=21 2026-08-01  haiku  claude-haiku-4-5-20251001    9120572793cd
     20  trace       N=31 2026-08-01  haiku  claude-haiku-4-5-20251001    bd490b7b02cb
```

All six registered prompt hashes now appear in the artifact, each on the arm
that generated it. The paired arm-T comparison is machine-checkable from
`prompt_sha256` alone; it no longer rests on the free-text `arm` field plus a
sample-id threshold.

---

## Caveats and limits

1. **`run_date` has day granularity only.** No per-row collection timestamp
   exists anywhere in the corpus (`arm_f_raw.json` stores `n`, `sample_id`,
   `arm`, `raw` and nothing else). F3's alternative remedy — "add a collection
   timestamp per row" — is therefore not satisfiable retroactively, and was not
   faked. Waves W3/W4 in particular are placed by their `STATE.md` section
   header (2026-07-31); the Opus arm's prereg file was written at 23:37 local on
   that date, so a portion of that arm may have executed after local midnight.
   The section header is taken as authoritative per the correction rules; the
   date is recorded, the hour is not knowable.
2. **The N=43 bare hash `1208e7d2a004…` is registered in no prereg or prompts
   file.** It was left unchanged (it is a bare row, and the value recomputes
   correctly from the bare template at N=43), but it is the one prompt hash in
   the corpus with no pre-sampling registration record. Worth disclosing
   alongside F2 rather than leaving for a referee to find.
3. **The pilot's verbatim prompt text is described but not stored.** The prereg
   characterises the drift; it does not reproduce the string. `null` plus the
   note is the strongest claim the evidence supports — a hash cannot be
   reconstructed from a prose description of a diff.
4. **`v2` corrects provenance, not analysis.** Every scored quantity is
   byte-identical to v1. No finding in `p4_review_stats.md` other than F2/F3/F4
   is addressed here, and no reported statistic changes as a result of this
   revision.
5. **Commit provenance.** `arm_f_candidates_v2.jsonl` was written at 04:05 and
   swept into commit `7567268` ("Blind faithfulness rescore", 04:06:11) by a
   concurrent session working the same checkout — the commit message does not
   describe this file. The committed blob is byte-identical to the file this
   ledger documents (sha256 `9f845f78…`). `arm_f_candidates.jsonl` was not
   modified by this work and remains at `02ecabcd…` in both the worktree and
   `HEAD`.
