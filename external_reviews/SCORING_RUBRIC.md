# Scoring Rubric — Template Anchoring Paper (for AI reviewers)

You are scoring a preregistered LLM-evaluation paper. Score 0–100. You must show arithmetic for every numerical check you perform. Do not award or deduct points for claims you did not verify.

## Inputs you must read

- Full paper: `paper1_draft.md` (or the Google Doc mirror)
- Data ledgers: `arm_f_candidates_v2.jsonl`, `arm_g_candidates.jsonl`, `arm_m_collect.jsonl`
- Scoring code: `arm_f_repro.py`, `arm_m_analysis.py`, `arm_t_analysis.py`
- Preregistrations: `arm_f_repro.py` header, `arm_s/o/t/m_preregistration.txt`
- Prior reviews (context only, do not anchor on their scores): `external_reviews/`

## Dimension 1 — Arithmetic integrity (25 points)

Recompute, from raw data and closed forms, at least:
- V(k, m) = k/2 + m(√2−1)/(2k) and T(k, N) = N/(2k) at every cell the paper quotes (e.g. V(4,4) = 2.2071068, T(8,57) = 3.5625000).
- Validity counts, on-prediction counts, modal values per cell against the ledgers.
- At least one p-value (Fisher exact) from raw counts.

Scoring: start at 25. −5 per material discrepancy the paper does not itself disclose. −2 per rounding/presentation inconsistency (same quantity, two values, no explanation). A discrepancy the paper discloses in its corrections ledger costs nothing.

## Dimension 2 — Preregistration honesty (25 points)

- Was every registered prediction reported, including failures? (P-T1 failed; P-M1–M3 disconfirmed; P-O1/2/4 de-registered — the paper must not hide these.)
- Are falsifiers evaluated per their REGISTERED wording, tie conventions included? Check §6.3 (tie-inclusive `<=` vs code's strict `<`) and arm M's F-M1/F-M2 against `arm_m_preregistration.txt`.
- Are post-hoc analyses labeled post-hoc everywhere they appear (kmatch, ambition, tolerance diagnostics, wave stratification)?
- Are deviations tabled (Table 4) rather than narrated away?

Scoring: start at 25. −8 for any registered outcome reported only in its favorable reading. −5 for a post-hoc analysis presented with confirmatory weight. −3 for a deviation absent from Table 4.

## Dimension 3 — Claim–evidence calibration (20 points)

For each headline claim, ask: does the stated scope match the data?
- Mode-ceiling claim: scoped to weak tier, single vendor, unpinned decoding? 
- Filler branch: restricted to m ≤ 1 after arm M? Abstract, §1.1, §2.3, §3.4, §8 mutually consistent on this scope?
- Rectangle: reported as partial support (5/11, null not cleanly separated), negative result (0/11 rival) leading?
- Trace/concentration: reported as fragile (fails Holm, one-cell-driven, wave-confounded), never as demonstrated effect?
- `opus_alias`: never attributed to a named model version anywhere?

Scoring: start at 20. −5 per overclaim (scope stated wider than evidence). −3 per underclaim (evidence stronger than stated — miscalibration cuts both ways). −5 if any negative result is buried below equal-prominence threshold relative to its paired confirmation.

## Dimension 4 — Internal consistency (15 points)

Sweep for the same number appearing twice with different values, cross-references pointing at wrong sections, table totals not matching prose, figure captions contradicting body text.

Scoring: start at 15. −3 per genuine contradiction. −1 per harmless imprecision the body corrects nearby.

## Dimension 5 — Reproducibility and provenance (15 points)

- Can every table regenerate from released artifacts by a documented command?
- Are raw outputs verbatim (not reconstructed)? Are exclusions counted and disclosed (concurrency-cap rejections, runtime deaths)?
- Are hash-coverage gaps, unpinned parameters, and alias provenance self-disclosed rather than discovered by you?

Scoring: start at 15. −5 per provenance gap the paper does not itself disclose. Self-disclosed gaps cost nothing — this paper's identity is self-correction; punish concealment, not honesty.

## Anti-gaming rules (binding on you, the reviewer)

1. Do not deduct for limitations the paper already discloses and correctly scopes. Deduct only for what is hidden, overclaimed, or wrong.
2. Do not reward caveat volume. A caveat that changes no claim is noise; flag caveat-saturation as a writing issue (max −2 total), not a rigor issue.
3. Anchor on the data, not on prior reviews' scores. State your score before reading any prior review's verdict if both are in context.
4. If you cannot verify a claim (missing artifact, cannot run code), say UNVERIFIED — do not guess a deduction.
5. Every deduction line must name: section, claim quoted, your recomputation or evidence, points.

## Output format

```
## Dimension scores
D1 arithmetic: X/25 — [itemized deductions with arithmetic]
D2 preregistration: X/25 — [...]
D3 calibration: X/20 — [...]
D4 consistency: X/15 — [...]
D5 reproducibility: X/15 — [...]

## Total: X/100
## Verdict: submission-ready yes/no
## Top remaining action: [single highest-value experiment or fix]
## UNVERIFIED items: [list]
```

Band guide: 90+ submission-ready, minor polish only. 80–89 accept with fixes. 65–79 major revision. <65 reject-and-resubmit.
