# Review — MLSys / Reproducibility Track

**Submission:** `paper2_draft.md` — *The Serving Stack Is Part of the Model: Precision Cliffs and the Limits of Reproducibility in Agent-Runtime LLM Studies*

**Reviewer stance:** systems / reproducibility. Every number was traced to a raw artifact or
rejected. Where I could recompute, I recomputed from `arm_f_raw.json` using the submission's
own `arm_f_repro.py` scoring functions. Recomputation commands and outputs are summarized
inline; all of it is re-runnable.

**Evidence set audited:** `precision-cliff-paper-outline.md`, `STATE.md` §8/§8b (lines 710-765),
`arm_f_repro.py` header (lines 1-90), `arm_f_raw.json` (215 rows), `p8_systems_citations.md`.

**Headline:** the §4 case study's *behavioral* arithmetic is exactly right and reproduces to the
row. The §4 *serving-signature* evidence — the paper's novel contribution — does not exist in the
released artifact, contradicts its own cited source on two of three figures, and rests on a token
counter the paper never defines and which the raw data suggests is input-side. §3 is not traceable
to any evidence in this corpus. Fix these and this is a good paper; as submitted it asserts
forensics it cannot support.

---

## Summary of verdicts on the six mandated audits

| # | Audit | Verdict |
|---|---|---|
| 1 | §3 numbers → executed-run outline sections | **Fail.** The outline contains *zero* executed-run data. It is 100% pre-execution plan. No §3 number traces to it, and the source the draft does name does not exist. See F1. |
| 2 | §4 arithmetic (24 overlap / 26 invalid / 30 rows) | **Pass, exactly.** Recomputed 4 valid, 24 `overlap`, 2 `nonpositive_radius`, per cell 7/7/10. One taxonomy caveat: F14. |
| 3 | Serving-signature provenance honesty | **Fail.** Not in any artifact; two of three figures contradict `STATE.md`; evidence class admitted in §8 for the *inference* but never for the *data*. F2-F4. |
| 4 | Impossibility argument | **Argued, but weakly** — by enumeration, not identifiability; one leg is bare assertion; contradicted by the paper's own §8. F8, F9. |
| 5 | Three `[SLOT: systems-lit]` fills | **Sound works, wrong mapping.** Slot letters in `p8` do not map 1:1 onto the draft's three markers, and the most important work is filed in the wrong section. F9, F20, and the placement table below. |
| 6 | §6 minimum disclosure standard | **Items 1-3 actionable and falsifiable; item 4 is a wishlist** and is the one item the paper does not implement. F4, F7, F17. |

**Counts:** 27 findings — 10 MAJOR, 12 MINOR, 5 NIT. Placeholder-leak count **P = 5**.

---

## MAJOR

### F1 [MAJOR] Every number in §3 is untraceable within the provided evidence, and the source it cites does not exist

`paper2_draft.md:101` declares §3 "condenses the antecedent study's quantization results." The
claim→evidence map at `paper2_draft.md:360` attributes it to *"paper-0 combined md §5.x"*. **No such
file exists in the corpus** (`ls` returns no `paper-0*`, no `*combined*`). The pointer is dangling.

The one evidence file that names the quantization study — `precision-cliff-paper-outline.md` — is a
**pre-execution plan in its entirety**, not the mixture the brief warned might be present. I checked
this three ways:

1. **Placeholders.** `precision-cliff-paper-outline.md:48` (abstract): *"We find that
   [PLACEHOLDER: the precision cliff shifts …]"*. `:262` (conclusion): *"[PLACEHOLDER — cliff
   shifted to X bits, viability rate was Y]"*.
2. **Tense and framing throughout.** `:136-142` is a table headed *"Expected Static Quality"*;
   `:186` is headed *"Expected figure structure"*; `:169-183` describes a pilot yet to be run.
3. **Chronology.** The outline's mtime is `2026-07-16 13:45`. The first executed sweep is logged at
   `STATE.md:56` (*"Update 2026-07-17 — PRECISION SWEEP COMPLETE"*) and the 14B rung at `STATE.md:81`
   (*2026-07-18*). The outline **predates every run it would have to report.**

A grep of the outline for §3's statistics — `7/50`, `16/50`, `87/200`, `38/200`, `2/18`, `17/18`,
`19/24`, `1/17`, `18/32`, `15/26`, `3.91`, `3.35`, `1.7e-7`, `3.4e-6`, and the strings `14B`, `echo`,
`must-differ`, `imatrix`, `IQ2` — returns **zero hits**. The outline does not mention a 14B ladder at
all; it plans a Qwen3-Coder-30B sweep with a 7B fallback (`:129`).

So: §3's numbers are not *contradicted* by the outline, they are simply unsourced in this corpus. For
a reproducibility paper this is the worst of the three possible states, because the section is
load-bearing for C1 and for the §3→§4 bridge at `paper2_draft.md:348-352`.

**Required:** either (a) cite a file that exists and is in the artifact bundle, with per-number
section anchors, or (b) demote §3 to a summary of *published* companion results with a proper
citation and drop the raw counts. A reviewer cannot check a single §3 figure today.

**Note in the authors' favour:** I could not fault §3's *internal* arithmetic. `7+6+9+7+16 = 45`
matches "45 of 250" (`:124-125`); `250 + 30 = 280` matches "280 opportunities" (`:125-126`);
`22+22+24+19 = 87` matches "87/200" (`:130`); `8/57 = 14.0%` matches "14% pooled" (`:133`);
`19/24 = 79%`, `1/17 = 5.9%`, and Fisher on those margins gives `3.4e-6` **exactly** as printed
(`:135`). The 14B-vs-7B Fisher gives `1.73e-7`, matching `1.7e-7` (`:131`). The numbers are
self-consistent; they are just unverifiable against raw data.

---

### F2 [MAJOR] The 49.9k token counts are almost certainly an input/context counter, which would vacate the paper's opening hook

`paper2_draft.md:176-179` and `:13-15`: *"Reported token counts were uniform at 49,902-49,906 across
all thirty completions: a four-token spread over thirty independent generations at three different
problem sizes."* `:28-29`: *"Nobody asked for uniform token counts and nothing in the experimental
design predicts them."* `:181-182`: *"Neither observation is explicable by the experimental design."*

The paper never says whether these are **input**, **output**, or **total** tokens. From the raw data:

- The thirty `opus_alias` completions in `arm_f_raw.json` are **215 to 1283 characters** (mean 578),
  i.e. roughly **61 to 367 output tokens**. A 49,902-token *output* is off by two orders of
  magnitude and flatly inconsistent with the stored raws.
- `arm_f_repro.py:72-75` shows the task prompt is a single template with `{n}` substituted. All three
  cells use two-digit N, so `prompt_for(13)`, `prompt_for(21)`, `prompt_for(31)` are **byte-identical
  in length — 520 characters each**.

The overwhelmingly likely reading is that ~49.9k is a **total/context counter** for a Claude Code
subagent: a large fixed system prompt plus inherited user instruction files (which §5 `:238-239`
itself flags as unlogged inherited context) plus a fixed-length task prompt. Under that reading the
observed near-uniformity is **exactly what the experimental design predicts**, and the residual
4-token spread is plausibly tokenizer-level variation between `"13"`, `"21"`, `"31"` or cache jitter —
not a serving-path signature.

This is not a hedge I am asking for. As written, one of the paper's two forensic pillars, its title
hook (`:26-31`), and an abstract claim (`:14-15`) rest on a statistic whose semantics the paper does
not state and whose most likely semantics falsify the claim.

**Required:** name the usage field verbatim (`input_tokens` / `output_tokens` / `cache_read` / sum),
report the per-invocation output-token counts separately, and if the counter is input-side, withdraw
the uniformity observation as an anomaly. If it *is* output-side, reconcile it with the 215-1283
character raws — that reconciliation would itself be a striking result and belongs in the paper.

---

### F3 [MAJOR] Latency and token figures contradict the only source cited for them

The claim map (`paper2_draft.md:362`) sources these to *"task usage blocks in session transcript,
logged STATE.md §8b."* Checking §8/§8b:

| Draft claim | Draft line | `STATE.md` says | Line |
|---|---|---|---|
| "2.8-5.9 s" for **all thirty** | `:13`, `:174` | 2.8-5.9 s for the **first twenty**; *"3-9s durations persist across all 30"* | `:714`, `:756` |
| "49,902-49,906" | `:13-14`, `:176-177` | 49,906 (a single value) across 20; *"~49.9k"* across 30 | `:716`, `:756` |
| "49,902" (range floor) | `:14`, `:177` | **appears nowhere in §8 or §8b** | — |

Two defects. First, the abstract and §4 state a latency range (upper bound 5.9 s) that the cited
source explicitly widens to 9 s once N=31 is added — a 52% understatement of the observed maximum,
in a paper whose argument is that the range is anomalously tight. Second, the lower bound `49,902`
is unsourced in the permitted evidence; §8b reports only `~49.9k`.

**Required:** report the actual per-invocation distributions (n=30, min/median/max, or the raw
vector) rather than a hand-carried range, and reconcile 5.9 s against `STATE.md:756`.

---

### F4 [MAJOR] The serving-signature evidence is absent from the released artifact, and §6's item 4 is the one recommendation the paper does not implement

`arm_f_raw.json` rows carry exactly four keys — verified across all 215 rows:

```
('arm', 'n', 'raw', 'sample_id')
```

No duration. No token counts. No model identifier. No timestamp. `arm_f_repro.py` contains no
timing, no usage capture, and no `opus`/`sonnet` invocation path at all (grep for `opus|sonnet|
duration|token|usage` hits only a comment at line 7).

Meanwhile `paper2_draft.md:266-267` states the four disclosure items are *"all implemented here"*,
and item 4 (`:280-285`) is *"the item the field does not currently do, and the one that caught §4."*
It is also the one item this paper does not do. A reader can recompute every validity figure but
cannot check a single latency or token number — the evidence class §4 is built on is prose in a
working log.

Compounding this: the latency comparison has **no contemporaneous control**. The paper compares
`opus_alias` at 2.8-5.9 s against tiers at 75-250 s and 150-1170 s but never states that the arms were
interleaved or run in the same window under the same concurrency. §6 item 3 (`:277-279`) discloses
that *"five invocations [were] rejected by a concurrency cap"* — so load conditions demonstrably
varied. A systems reviewer will not accept a two-orders-of-magnitude latency claim without an
interleaved or at minimum same-window control.

**Required:** ship the duration/usage vectors as a machine-readable file keyed to `arm_f_raw.json`
rows; state the invocation schedule across arms; or reclassify §4's serving signature as
session-log observation and say so in §4's body, not only in §8.

---

### F5 [MAJOR] §4 reports validity at an unstated tolerance, and the tier contrast is tolerance-dependent for exactly one arm

§3 `:151-158` makes dual-tolerance reporting a load-bearing methodological virtue: *"Both tolerances
are logged for every row, with 1e-6 primary … Choosing between them after seeing results would have
been the easiest way to fabricate the entire result table."* §4 then reports every validity figure at
a single, unnamed tolerance (`:185-186`).

Recomputed with the submission's own `validate()`:

| Arm | tol 1e-9 | tol 1e-6 (declared primary) |
|---|---|---|
| `opus_alias` | **4/30** | **4/30** |
| `sonnet_bare` | **27/30** (8/10, 10/10, 9/10) | **30/30** |

Three Sonnet rows — N=13 id 6, N=13 id 9, N=31 id 1 — fail on `overlap` at 1e-9 and pass at 1e-6. So
the headline contrast is `4/30 vs 30/30` at the loose tolerance and `4/30 vs 27/30` at the strict one.

**In the authors' favour:** the finding is entirely robust. The `opus_alias` collapse is
tolerance-invariant, and 4/30 vs 27/30 is no weaker a result than 4/30 vs 30/30. This is a *reporting*
defect, not a validity threat. But a paper that spends a paragraph explaining why post-hoc tolerance
selection would be fraud must not then print a single-tolerance table without saying which.

**Required:** report §4's validity at both tolerances, as §3 promises.

---

### F6 [MAJOR] The released harness default tolerance contradicts the paper's declared primary

`arm_f_repro.py:120`: `def validate(circles, n, tol=1e-9)`. `paper2_draft.md:155`: *"1e-6 primary."*
A reader who runs the released artifact with defaults gets different numbers from the paper — in the
Sonnet arm's case, a different headline (27/30 vs 30/30). Set the default to the declared primary,
or make the tolerance a required argument.

---

### F7 [MAJOR] The Haiku comparator (32/45) is not recomputable from the released raw file

`paper2_draft.md:185-186` and `STATE.md:751` report Haiku at 32/45. `arm_f_raw.json` no longer
contains a 45-row Haiku arm at those cells. `STATE.md:767-771` (§9, 2026-08-01) records that Arm T
added **100 new invocations** into the same `bare`/`trace` arm labels and that *"All raws [are] in
arm_f_raw.json (corpus now 215 invocations)"* — the file was overwritten in place (mtime
`2026-08-01 01:14`).

Recomputing `bare` at N=13/21/31 today gives **47/60** (1e-9) or **50/60** (1e-6) across 60 rows. There
is no `batch`, `run_date`, or `wave` field, and `sample_id` values collide across batches, so the
original 45 cannot be reconstructed. The §4 headline sentence contains a denominator no reader can
reproduce from the artifact the paper ships.

**Required:** add a batch/run-date field per row and freeze arm slices, or restate the comparator
against a slice that exists in the released file.

---

### F8 [MAJOR] The impossibility argument over-claims: the two hypotheses are not observationally equivalent, and the argument is by enumeration rather than identifiability

`paper2_draft.md:209`: *"Both hypotheses predict every observation we have."* This is false as
stated. H1 (serving-path degradation) predicts the latency and token-uniformity observations —
`:180-181` says so directly (*"both are consistent with a fast-mode serving path"*). H2 (genuine tier
property of whatever weights the alias resolved to) is **silent** on both: nothing about a model
attempting harder constructions predicts 2.8-5.9 s completions or a four-token spread. To explain the
full observation set, H2 must be conjoined with *"and, separately, a fast serving path was in use but
had no behavioral effect"* — which is H1's mechanism minus its causal claim. That is a strictly more
complex hypothesis, and the likelihood asymmetry is the paper's to argue, not to flatten.

Second, the impossibility (`:209-216`) is established by listing four things that do not work — more
sampling, prompt variation, timing instrumentation, pinned weights — and concluding that *nothing*
works. Enumeration is not exhaustion. **A hostile reviewer will demand:**

1. **A formal non-identifiability statement.** Define the observable set the runtime exposes
   (response text, wall-clock, reported usage, error codes). Show H1 and H2 induce the same
   distribution over that set. Then the impossibility is a theorem, not a list. As written it is
   closer to assertion than proof, which is fatal for a paper whose stated contribution (C3, `:53`)
   *is* the impossibility.
2. **Justification for the prompt-variation dismissal.** `:211-212` — *"Prompt variation does not,
   because both act on execution rather than intent"* — is one clause of bare assertion doing the
   work of ruling out an entire experiment class. It is also wrong on its face for at least one
   design: give the alias a *fixed, known-valid* packing and ask it to verify or repair the
   tangencies. That decouples arithmetic execution from construction choice, because the model did
   not choose the construction. If the alias fails to verify tangencies it did not select, that is
   execution degradation independent of ambition — precisely the H1/H2 discriminator the paper says
   cannot exist. Either run it or explain why it fails.
3. **Engagement with output-side stack fingerprinting.** See F9.
4. **The contemporaneity control** for the latency claim (F4).

---

### F9 [MAJOR] §4's impossibility claim contradicts §8's own proposed follow-up, and ignores a work the authors themselves verified

Two internal problems, one external.

**Internal, self-contradiction.** `:213` — *"not separable by any experiment runnable from inside this
runtime."* `:344-348` — *"A second serving-signature snapshot of the same alias at a later date is the
highest-value follow-up: if the signature shifts with no alias change, §4 gains a second independent
data point."* A dated re-snapshot **is** runnable from inside the runtime, and §8 says it would be
informative. Both sentences cannot stand. Narrow `:213` to "not separable by any *single-session*
experiment" or drop the §8 proposal.

**External, and more serious.** `p8_systems_citations.md:10` lists Wimbauer et al., *Fingerprinting
Inference Systems of Large Language Models* (arXiv:2605.29979), verified by the authors, which shows
that **serving-stack differences — inference engine, attention backend, GPU type — are detectable from
output text alone.** If that holds, then fingerprinting the alias's outputs against known stack
signatures is a candidate within-runtime discriminator, and §4's impossibility is at minimum
narrowed. The submission cannot verify that citation, file it as a related-work filler under slot
"b (extra)", and simultaneously claim in `:214-216` that separation *"is not a gap in our design that
a reviewer could ask us to close."* I am asking exactly that.

**Required:** move Wimbauer to §5 and argue explicitly why output-text fingerprinting does or does not
separate H1 from H2 here (sample size, absence of reference signatures for the vendor's stacks, and
the fact that the arm's outputs are ~578 characters are all plausible reasons — make them).

---

### F10 [MAJOR] Placeholder and editorial-scaffolding leak (P = 5), and one leak is load-bearing

Five markers survive into the submission:

| Line | Marker |
|---|---|
| `:110-111` | `<!-- CONFLICT: outline names Qwen3-Coder-30B with a 7B "fallback" … -->` |
| `:113-116` | `<!-- CONFLICT: outline's precision table gives Q3_K_M "~3.5" and Q2_K "~2.5" bpw … -->` |
| `:300` | `[SLOT: systems-lit]` |
| `:304` | `[SLOT: systems-lit]` |
| `:306` | `[SLOT: systems-lit]` |

Two separate problems.

**(a) The CONFLICT comments adjudicate against a plan as if it were rival evidence.** Both compare
executed measurements to `precision-cliff-paper-outline.md`'s *expected* values (`:136-142`, headed
"Expected Static Quality"). Per F1 that table is a pre-execution guess with no measurements behind
it. There is nothing to reconcile; the correct action is deletion, not adjudication. Leaving the
comments in advertises to a reviewer that the authors treated an unexecuted plan as a data source.

**(b) The second leak carries the only bits-per-weight numbers in the paper.** `:113-116` is where
"3.91" and "3.35" bpw appear — and **nowhere in §3's body does a single measured bpw figure appear.**
Yet §3's central mechanism claim at `:147-149` is that the cliff is *"scheme-mediated, tracking
quantization quality rather than nominal bit width, and graded rather than binary."* That claim is
unsupportable without the measured bpw of each rung in the text. Promote the measured file bpw into
the §3 ladder description (`:105-108`), then delete the comment.

---

## MINOR

### F11 [MINOR] §3 uses two different "/200" denominators for the same 7B ladder, disclosing neither
`:118-120` quotes fp16 7/50, q8_0 6/50, q4_k_m 9/50, q3_k_m 7/50 — which sum to **29**. `:130-131`
then states *"87/200 versus 38/200, Fisher p = 1.7e-7."* I confirmed 38 = q8_0 + q4_k_m + q3_k_m +
q2_k (6+9+7+16), i.e. the rung-matched subset against the 14B ladder's four rungs, and that this
margin reproduces `1.73e-7` exactly. The choice is correct and defensible — but the reader who sums
the four numbers printed twelve lines earlier gets 29, not 38. One clause fixes it: *"rung-matched to
the 14B ladder, i.e. excluding fp16 and including q2_k."*

### F12 [MINOR] The `p = 0.007` comparator is unstated, and the comparison the sentence invites is not significant
`:121-122`: *"The 2-bit rung inverted, at 16/50, a post-hoc effect (p = 0.007 uncorrected)."* The
sentence names fp16 two clauses earlier, so a reader tests 16/50 vs 7/50 → **two-sided Fisher
p = 0.056**, not significant. `p = 0.007` reproduces only against the pooled upper four rungs:
16/50 vs 29/200 → **p = 0.00682**. State the comparator. Note also that this pooling (29/200) is a
*different* rung membership from the 38/200 used nine lines later (F11) — two unlabelled "/200"s for
one ladder in one section.

### F13 [MINOR] `p = 0.44` for the failed improvement-count prediction does not reproduce under any stated test
`:136`: *"a companion prediction about improvement counts failed at the same rung (3/5 seeds improved,
p = 0.44)."* No test is named. Binomial 3/5 against p=0.5 gives two-sided 1.0 and one-sided 0.5;
Fisher against plausible comparators does not land on 0.44 either. Name the test and its comparator.
The paper is right to foreground the failed prediction (`:136-137`) — do not let an unreproducible
p-value undermine the one place it reports a miss.

### F14 [MINOR] The "24 of 26" failure taxonomy implies a disjointness that is an artifact of gate ordering
`:187-190`: *"24 of 26 invalid rows overlap … and two rows padded to the requested count with
zero-radius circles."* The arithmetic is exactly right (recomputed: 24 `overlap`, 2
`nonpositive_radius`, 7/7/10 per cell), but `arm_f_repro.py` checks `nonpositive_radius` at line 126
**before** `overlap` at line 133, so the two padded rows are labelled by whichever gate fires first.
I checked: **both padded rows also overlap** once the zero-radius circles are removed. The honest
statement is *"all 26 invalid rows overlap; 2 of them additionally pad the count with zero-radius
circles."* Related: one of the two rows (N=21, id 5) has **12 of 21** radii at zero. That is not
"padding to the requested count," it is a mostly-degenerate output, and calling it padding overstates
how coherent the failure was.

### F15 [MINOR] §3 never states the problem size of the quantization ladder, which the §3→§4 bridge needs
§3 gives no N for the 7B/14B sweeps. `:143-144` mentions *"26 of 27 circles unchanged"* — the only
hint, and an ambiguous one. §8 `:348-352` explicitly rests the paper's central inference on §3
transferring to §4's cells (N=13/21/31). A reader cannot assess that transfer without knowing whether
§3 measured the same task instance class. State N (or the N-set) in `:105-108`.

### F16 [MINOR] The "17%" validity-inflation figure in §6 item 3 is untraceable
`:277-279`: *"five invocations rejected by a concurrency cap before reaching a model would have
understated validity by 17% had they been counted as proposer failures."* Neither the arm nor the
denominator nor the sense of "understated by" is given. The Haiku reading (32/45 = 71.1% → 32/50 =
64.0%) gives 7.1 pp absolute / 10.0% relative. The Sonnet reading (30/30 → 30/35) gives 14.3 pp /
16.7%. Neither is naturally "17%." Since 45 = 50 − 5, the five rejects appear to be Haiku's — which is
the reading that does *not* produce 17%. State arm, denominator, and definition.

### F17 [MINOR] §6 item 4 has no statistic, no threshold, and no decision rule — it is a wishlist as written
`:280-285` asks for *"per-invocation wall-clock duration and reported token counts, logged and reported
as distributions."* It then offers only eyeballing: *"visible in a histogram … visible in a sorted
list."* An "anomaly canary" needs a firing condition. Give one — e.g. report coefficient of variation
and IQR per arm per cell, flag when a tier's duration CV falls below some multiple of the neighbouring
tier's, or when reported-token spread is under k tokens over n invocations. Falsifiable as stated:
no. Compare with items 1-3, which are concrete, checkable, and genuinely good. Also: no such histogram
or sorted list appears in this paper (F4), so item 4 is currently advocacy rather than demonstration.

### F18 [MINOR] Disclosure item 1 is not implemented for the arm the paper is about
`:226-228` and `:269-272` present `RUN_DATE` + `ALIAS_MAP` as implemented provenance. In
`arm_f_repro.py`: `RUN_DATE = "2026-07-30"` (line 60), `ALIAS_MAP = {"haiku": "claude-haiku-4-5-
20251001"}` (line 64), `PROPOSER_ALIAS = "haiku"` (line 65). **There is no `opus` entry, no `sonnet`
entry, and no opus invocation path in the file.** Further, `arm_o_preregistration.txt` is dated
2026-07-31 and the N=31 cell ran later still (`STATE.md:745`), so the single hardcoded `RUN_DATE` is
not even the opus arm's run date. The paper's headline provenance repair is unimplemented in exactly
the place it matters. Either extend `ALIAS_MAP` and make `RUN_DATE` per-arm, or state plainly in §5
that the map covers the Haiku arm only.

### F19 [MINOR] Disclosure item 2 is implemented as code but not as disclosure
`arm_f_repro.py:84-85` defines `prompt_hash(n)`, but **no digest appears anywhere in the paper**, and
`arm_f_prompts.json` is not referenced from the draft. Item 2 (`:273-276`) says the hash closes the
largest silent degree of freedom "at zero cost" — it only does so if the digest is published. Print
the per-N SHA-256 digests in §5 or an appendix table.

### F20 [MINOR] The `p8` slot letters do not map onto the draft's three markers, and two proposed fills are the wrong *kind* of work
`p8_systems_citations.md` tags five distinct works as slot "c" (GPTQ `:11`, AWQ `:12`, Marchisio
`:13`, Madaan `:14`, Miller `:15`), but the draft has **two** distinct markers after slot (a)/(b) —
`:304` for quantization effects and `:306` for evaluation variance. The mapping must be made explicit.

Separately, `:304` claims *"the quantization-effects literature measures degradation on static
single-shot benchmarks."* GPTQ and AWQ are **method** papers, not measurement studies; only Marchisio
et al. (arXiv:2407.03211) actually fits that sentence, and it fits very well (the automatic-metrics-
understate-harm result at `p8:13` directly reinforces §3's "invisible to viability and validity
metrics" claim at `:46-47`). Also unflagged: §3 sweeps **llama.cpp K-quants** (`:105`), a different
family from GPTQ/AWQ, and the outline's own limitations (`:269`) list GPTQ/AWQ/bitsandbytes as
untested. Citing GPTQ/AWQ as the backdrop for a K-quant sweep without noting the family gap invites a
reviewer objection.

### F21 [MINOR] C3 is stated unconditionally on n = 1 runtime
`:53-55` states flatly that *"an agent runtime cannot be made reproducible from inside itself"* and
calls the residue a property of *"the harness class"* (`:216`). `:332` concedes *"We observed a single
vendor and a single agent runtime."* Condition C3 in the contributions list, or the reviewer does it
for you.

### F22 [MINOR] `arm_f_raw.json` has no unique row key
`sample_id` collides across arms and batches: `trace` at N=21 spans ids 1-120 across 30 rows while
`bare` at N=21 uses 1-20. Combined with F7 (no batch field), the released artifact cannot be sliced
back into the arms the paper reports. For a paper whose §5 table lists "Raw outputs — Yes — verbatim
storage" with "no inference risk," the storage schema is the weak link.

---

## NIT

### F23 [NIT] The N=31 geometric example does not match the raw to three decimals
`:188-189`: *"edge strips at r = 0.03 sitting 0.138 from a grid circle of radius 1/6 that requires
0.197."* Recomputed on the matching row (N=31, id 3, radii {0.03, 0.1667}): the minimum centre
distance between an r=0.03 strip and an r=1/6 grid circle is **0.1367**, which rounds to 0.137. The
required 0.197 checks out (1/6 + 0.03 = 0.19667). The qualitative point is untouched, but a paper
that stakes its instrument on 1e-6 tolerances should not carry a 0.001 discrepancy in its one worked
example. (The figure is inherited verbatim from `STATE.md:748`.)

### F24 [NIT] The example is presented as a cell-level characterization but is one row
`:188` reads as though "edge strips at r = 0.03" describes N=31 generally. Only 2 of 10 N=31 rows have
an r=0.03 radius; the other eight use varied filler radii (0.0104-0.0521). Label it as an example row.

### F25 [NIT] "The four valid samples score below the trap" flattens very different margins
Recomputed: N=13 valids score 1.2646 / 1.2873 / 1.4142 against a trap of 1.625 (13-22% below); the
N=21 valid scores 2.07 against a trap of 2.1 (**1.4%** below). One clause noting the heterogeneity
costs nothing and preempts a reviewer who checks.

### F26 [NIT] Citation ordering in slot (b)
`p8:8` (He et al.) is a company blog post; `p8:9` (Yuan et al., arXiv:2506.09501, NeurIPS 2025) is the
peer-reviewed result. For an MLSys venue, lead with Yuan et al. and cite He et al. as the practitioner
companion — the reverse of the file's ordering.

### F27 [NIT] "Quarter-circle corners" is a misnomer
`:190-191` describes the N=13 family as *"quarter-circle corners."* The raws show four ordinary
circles of r = 0.25 at the corners, not quarter-disc sectors. Inherited from `STATE.md:728`. Also,
*"10/10 the same family"* (`:191`) is asserted without the classifier output that establishes family
membership — `arm_f_repro.py:152-202` has a `classify()` that produces exactly this; report it.

---

## Recommended `[SLOT: systems-lit]` placement

All nine works in `p8_systems_citations.md` are real, correctly described, and appropriate to this
paper. The problem is mapping, not quality. Proposed fills:

| Draft line | Sentence's claim | Fill |
|---|---|---|
| `:300` (clause 1) | reported results depend on undocumented implementation/environment detail | **Pineau et al.**, JMLR 22(164) 2021 / arXiv:2003.12206 (`p8:7`). Exact fit; the canonical anchor for this line. |
| `:300` (clause 2) | numerical nondeterminism / batch-invariance; fixed model, fixed hardware, non-identical output | **Yuan et al.**, arXiv:2506.09501 (`p8:9`) as primary — peer-reviewed, quantifies up to 9% accuracy swing from batch size / GPU count. **He et al.** (`p8:8`) as the practitioner companion; "batch-invariance" is literally their framing. |
| `:304` | quantization-effects literature measures degradation on static single-shot benchmarks | **Marchisio et al.**, arXiv:2407.03211 (`p8:13`) as the substantive fit — and it strengthens §3, since its finding that automatic metrics understate harm is §3's own thesis in a different domain. **GPTQ** (`p8:11`) and **AWQ** (`p8:12`) as method citations only, with an explicit note that §3 swept llama.cpp K-quants, a different family. |
| `:306` | evaluation-variance studies quantify seed and prompt sensitivity | **Madaan et al.**, arXiv:2406.10229 (`p8:14`) + **Miller**, arXiv:2411.00640 (`p8:15`). Both fit cleanly and both support §5's "cannot be averaged out by more seeds" point — Miller in particular gives the statistical machinery for saying when a delta clears noise. |

**Do not** use `:300`/`:304`/`:306` for **Wimbauer et al.**, arXiv:2605.29979 (`p8:10`, currently
tagged "b (extra)"). It is the single most consequential work in the file for this submission and it
belongs in **§5**, engaged as a threat to the impossibility claim — see F9. Filing it as related-work
padding while §4 asserts that no within-runtime experiment can separate the hypotheses is the kind of
thing a reviewer notices and does not forgive.

One structural note: `:300` carries two distinct claims (reproducibility-in-ML; numerical
nondeterminism) under one marker. Split the sentence so each citation attaches to the claim it
supports.

---

## Verdict on §6 as a standard

Items 1-3 are **actionable and falsifiable**: a reader can check whether an alias map exists, whether
a prompt digest was published, and whether failure rows are present in the raw file. They cost
nothing, require no vendor cooperation, and the paper is right that item 3 is where validity rates
silently inflate. Item 4 is the novel one and is currently a **wishlist**: no statistic, no threshold,
no decision rule (F17), and not implemented in this paper's own artifact (F4). It is also the item the
whole paper exists to motivate, so it is worth the extra half-page.

The "What vendors could expose" paragraph (`:288-291`) is the strongest passage in the submission —
three concrete single-field asks, each traceable to a specific failure in §4/§5. Keep it exactly as is.

---

## Recommendation

**MAJOR REVISION.**

The paper has a real result and an unusually honest posture — it reports a failed prediction over a
passing one (`:136-137`), marks three of four registered predictions NOT EVALUABLE rather than
scoring them (`:197-198`), and states its circumstantiality plainly (`:337-342`). The §4 behavioral
arithmetic reproduces to the row; the pre-registration SHA-256 verifies against
`arm_o_preregistration.txt` (full digest `211718c6b58d627f17e34aa73ad6142b89c7f39048e5e19a8cc864d63c281738`,
matching the paper's truncated `21171…738` — though publish the full digest, an 8-character
abbreviation is not an identifier). None of that is in question.

What blocks acceptance is that a reproducibility paper is failing its own audit in four places, and
the specific claim it is built on may not survive one definition:

1. **F2** — define the token counter. If it is input/total, the uniformity anomaly is predicted by the
   design and must be withdrawn; the paper survives on the latency and behavioral evidence, but §1's
   hook and one abstract claim must be rewritten. **This is the gate. Resolve it first, because the
   answer determines how much of §4 remains.**
2. **F1** — cite a source for §3 that exists, or demote §3.
3. **F4 / F7 / F18 / F19** — ship the serving-signature data, add a batch key so the reported arms can
   be sliced out of `arm_f_raw.json`, extend `ALIAS_MAP` past `haiku`, publish the prompt digests.
4. **F8 / F9** — recast the impossibility as a non-identifiability argument over a stated observable
   set, drop or defend the prompt-variation dismissal, resolve the `:213` / `:344-348` contradiction,
   and engage Wimbauer et al. head-on.
5. **F5 / F6 / F10** — report §4 at both tolerances, align the harness default with the declared
   primary, and remove all five scaffolding markers (promoting the bpw numbers into §3's body first).

None of these require new experiments except the optional repair-probe suggested in F8, and the
serving-signature re-log implied by F4. If F2 resolves in the authors' favour, this is a paper the
track should want.
