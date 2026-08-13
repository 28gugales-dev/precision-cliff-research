# Dispersion Probe v2 — Analysis Preregistration

**Created:** 2026-07-28 07:39:00 EDT  
**Runner version:** `dispersion_probe_v2`  
**Status:** FROZEN — analysis method specified before execution; no metric may be chosen after seeing data.

---

## Directory Listing at Creation Time

```
total 12
drwxr-xr-x 1 [ANON] 197609 0 Jul 28 07:39 .
drwxr-xr-x 1 [ANON] 197609 0 Jul 28 07:39 ..
```

No output files exist. This listing confirms the preregistration was written before any v2 data.

---

## 1. Design Summary

Six frozen circle-packing parents (byte-identical to v1: same centers, same radii, same prompt template) are fed to Qwen2.5-Coder-14B-Instruct at four quantization rungs. 24 independent samples per (rung, parent). Seeds differ from v1 by a "v2" salt: `seed = sha256(rung, parent, idx, "v2")`.

Total: 4 rungs × 6 parents × 24 samples = 576 rows.

This is a **confirmatory replication** of the v1 fixed-parent dispersion probe with:
- q8_0 restored as ceiling rung
- logprobs bug fixed (retry without logprobs on exception)
- N_SAMPLES raised from 16 to 24
- Out-of-sample seeds

---

## 2. Rung Order for All Trend Tests

Decreasing precision: **q8_0 > q4_k_m > q3_k_m > q2_k**

If q8_0 cannot be loaded (2 GPUs unavailable), the substitute ceiling rung is q6_k, verified by filename existence in the Qwen/Qwen2.5-Coder-14B-Instruct-GGUF repo and sha256. If no ceiling rung loads at all, the run is FAILED and no trend tests may be reported.

---

## 3. PRIMARY Metric

**Count of distinct circle-solutions among valid rows.**

### 3.1 Canonicalisation

For each valid row (26 circles, each [x, y, r]):
1. Round x, y, r to 6 decimal places.
2. Sort the 26 triples lexicographically (by x, then y, then r).
3. Hash the sorted list with SHA256.

Two rows that produce the same hash are the same canonical solution. Sorting means a permutation of the same packing counts once.

### 3.2 Primary Test (pooled rarefaction)

Let m = minimum number of valid rows across all completed rungs.

For each rung:
- Randomly sample m valid rows without replacement.
- Count distinct canonical solutions in the sample.
- Repeat 1000 draws.
- Report mean ± sd of distinct-solution count.

### 3.3 Per-Parent JT Trend Test

For each (rung, parent) combination:
- Let m_parent = minimum number of valid rows for that parent across all rungs.
- Rarefy to m_parent rows, 2000 draws without replacement.
- Count distinct canonical solutions per draw.
- Take the mean across draws (the per-parent rarefied distinct count).

Run Jonckheere–Terpstra trend test across the four rungs (ordered q8_0 > q4_k_m > q3_k_m > q2_k) on the six per-parent rarefied counts, with a 10,000-shuffle permutation p-value.

**Tie rule:** ties contribute 0.5 to the JT statistic. Not 1.0. Not 0.0.

### 3.4 Sanity Gate

Every trend test MUST report:
- Observed JT statistic
- Permutation-null mean of JT statistic
- Permutation-null sd of JT statistic

If a permutation p comes out exactly 0.0000 or exactly 1.0000, the test is SUSPECT. Do NOT report it as a finding. Print the full null distribution (sorted permutation values, observed marked with `<<<`).

---

## 4. SECONDARY Metrics

All secondary metrics are reported descriptively. No additional hypothesis tests.

### 4.1 Distinct Radius-Vector Count

Same rarefaction as primary (pooled m, 1000 draws). Canonicalise only the sorted radius vector (26 radii rounded to 6 decimals, sorted ascending, hashed). Centers excluded.

### 4.2 Mean Score Among Valid Rows

Per rung: mean score among all valid rows with bootstrap 95% confidence interval (BCa, 10,000 resamples). Denominator = all valid rows.

### 4.3 Mean Score Among Valid Non-Echo Rows

Per rung: mean score among valid rows where `echo == false`, with bootstrap 95% CI. A row is non-echo if `coordinate_echo(sample_circles, parent_circles, tolerance=1e-3)` returns False (centers-only echo: max index-wise center displacement < 1e-3).

### 4.4 Centers-Echo Rate

Per rung: fraction of valid rows with `echo == true` (centers-only, 1e-3 tolerance). Denominator = valid rows.

### 4.5 Validity Rate

Per rung: `valid_rows / total_rows_excluding_infrastructure_errors`. Infrastructure-error rows are those where `parse_error` starts with `"gen_error:"` and `n_circles == 0`. These are removed from the denominator.

---

## 5. Decision Rule

### Terms

- **D(m)** = rarefied distinct-solution count (pooled, primary metric), per rung as mean ± sd.
- **JT** = Jonckheere–Terpstra test on per-parent rarefied distinct counts, across 4 ordered rungs.
- **Score** = mean score among valid rows, per rung.
- **UNDERPOWERED** takes precedence over all other verdicts.

### UNDERPOWERED (precedence)

Any of:
- m < 20 (fewer than 20 valid rows in any rung after rarefaction)
- Any rung has fewer than 3 parents with at least 2 valid rows
- The primary metric shows zero variance across rarefaction draws in two or more rungs

When UNDERPOWERED, report the triggering condition(s). Do not report SUPPORTED, PARTIAL, or FALSIFIED.

### SUPPORTED

D(m) declines monotonically across the precision ordering AND permutation JT p < 0.05 AND mean score among valid shows no monotone decline (JT p on per-parent mean scores > 0.10).

Interpretation: quantization damages exploration (dispersion shrinks) while exploitation (quality) holds.

### PARTIAL

D(m) declines monotonically AND permutation JT p < 0.05, BUT mean score among valid also shows monotone decline (JT p on per-parent mean scores ≤ 0.10).

Interpretation: both dispersion and quality fall; the data cannot distinguish mechanism from capability floor.

### FALSIFIED

D(m) is flat across rungs (JT p > 0.10) while validity rate falls.

Interpretation: quantization damages capability, not exploration.

---

## 6. Infrastructure Notes

- The run is on Kaggle with GPU T4 ×2.
- Kernel execution order: q2_k, q4_k_m, q8_0 (or q6_k), q3_k_m.
- `provenance.json` is written incrementally so every rung's block persists.
- Logprobs are attempted for sample 0 of each parent; if they raise, the sample is retried without logprobs. A provenance flag records whether logprobs were obtainable.
- N_SAMPLES = 24 (raised from 16). Parents and prompt template are byte-identical to v1.
- Seeds: `sha256(rung, parent, idx, "v2")` — out-of-sample from v1.

---

## 7. Amendments

None. This is the frozen preregistration. No amendments are permitted after the first output file lands in the directory.
