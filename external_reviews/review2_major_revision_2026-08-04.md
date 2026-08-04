# External review 2 — full paper, "Major Revision"

Received 2026-08-04 (user-supplied, external model). Target: full paper (rev2).

---

**Recommendation:** Major Revision
**Primary Field:** Empirical Evaluation of Language Models / Evolutionary Computation & LLM-Driven Search

## 1. Executive Summary

Paper investigates the unconditioned proposal distribution p(coordinates | task description) of LLMs on zero-shot circle packing. Closed form (k*(N) = round(√N), V(k,m), T(k,N)) identifies empirical modal output to seven decimals across seven N. Notable for methodological rigor (preregistration, deterministic local scoring, transparent error accounting in Table 5). Held back by methodological confounds, missing mechanistic controls, vendor lock-in, and excessive meta-commentary.

## 2. Mathematical & Empirical Verification

- V(k,m) = k/2 + m(√2−1)/(2k) exact; T(k,N) = N/(2k) correct; trap-zone bounds [k²−k+1, k²−1] correct. T(5,24) = 2.4000000 vs V(4,8) = 2.4142136, 0.59% deficit — verified. Table 5 items 2–4 accurate.
- Mode-ceiling claim (§3.3) mathematically sound; mode captured 7/7.
- P-T3: p = 0.0325 fails Holm (0.0167, m=3); paper correctly refuses confirmation.

## 3. Major Strengths

1. Exact output point predictions (vs aggregate scaling laws).
2. Clear scope isolation: p(coords|prompt) vs in-loop p(program|parents,fitness).
3. Exemplary disclosure ledger (Table 5, 32 items).

## 4. Critical Weaknesses

A. **Vendor lock-in & scope inflation.** Single vendor family; cross-vendor attempts failed (NOTE: see assessment — partially inaccurate). "Weak-tier law" overgeneralizes from single lineage.

B. **Bundled intervention confound.** trace_v2 = METHOD line + output-format rewording. Validity gain driven entirely by format compliance (0 vs 3 parse failures). Fails to isolate trace elicitation.

C. **Missing mechanistic controls.** (1) Arithmetic tractability vs template lookup untested. (2) 1-parent mutation arm unrun — in-loop claim speculative.

## 5. Structural Recommendations

1. Relocate audit meta-history (Table 4, Table 5, versioning notes) to supplementary; >25% of body is process log.
2. Fix or replace Figure 2 — caption contains self-admitted draft note ("should be regenerated"). Regenerate at single N with sample ids and overlap highlighting.
3. Rebalance §5 — condense; focus on the negative result.

## 6. Checklist for Revision 3

| Priority | Section | Action |
|---|---|---|
| High | §1, §4, §8 | Soften "weak-tier law" to single-vendor scope until open-weight models parse |
| High | Fig. 2 | Regenerate at constant N across tiers; remove draft caption notes |
| High | §9, App. | Move Tables 4 & 5 to supplementary |
| Medium | §5.1, §5.3 | Label trace_v2 "bundled prompt format and trace request" throughout |
| Medium | §8 | Frame arithmetic tractability as open alternative; emphasize 1-parent control |
