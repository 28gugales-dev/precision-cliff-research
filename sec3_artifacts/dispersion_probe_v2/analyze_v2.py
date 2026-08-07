#!/usr/bin/env python
"""Dispersion probe v2 analysis — exactly as preregistered in analysis_prereg_v2.md.
Reads probe_samples.jsonl from the output directory, computes all metrics,
runs trend tests, and reports the verdict."""

import hashlib
import json
import math
import os
import random
import sys
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Config — point at the output directory containing probe_samples.jsonl
# ---------------------------------------------------------------------------
# Defaults to the rows vendored beside this script, so a clone reproduces the
# registered v2 verdict with `python analyze_v2.py` and no arguments.
OUTPUT_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
CAND_LOG = OUTPUT_DIR / "probe_samples.jsonl"
PROVENANCE = OUTPUT_DIR / "provenance.json"

# Precision ordering for trend tests (decreasing precision)
RUNG_ORDER = ["q8_0", "q4_k_m", "q3_k_m", "q2_k"]
# If q8_0 was substituted with q6_k, the order becomes:
# q6_k > q4_k_m > q3_k_m > q2_k

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_rows(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def load_provenance(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Canonicalisation (prereg §3.1)
# ---------------------------------------------------------------------------

def canonicalise(circles):
    """Round x,y,r to 6 decimals, sort 26 triples lexicographically, hash.
    Returns hex digest or None if circles is None."""
    if circles is None:
        return None
    # Round to 6 decimals
    rounded = [(round(x, 6), round(y, 6), round(r, 6)) for (x, y, r) in circles]
    # Sort lexicographically
    sorted_triples = sorted(rounded)
    # Hash
    packed = json.dumps(sorted_triples, separators=(",", ":"))
    return hashlib.sha256(packed.encode()).hexdigest()


def canonicalise_radii(circles):
    """Canonicalise only the sorted radius vector (§4.1)."""
    if circles is None:
        return None
    radii = sorted(round(r, 6) for (_, _, r) in circles)
    packed = json.dumps(radii, separators=(",", ":"))
    return hashlib.sha256(packed.encode()).hexdigest()


# ---------------------------------------------------------------------------
# Infrastructure-error detection
# ---------------------------------------------------------------------------

def is_infra_error(row):
    """Rows where parse_error starts with 'gen_error:' and n_circles == 0."""
    pe = row.get("parse_error")
    return pe is not None and pe.startswith("gen_error:") and row.get("n_circles", 0) == 0


# ---------------------------------------------------------------------------
# Centers-only echo check (same as v1: max index-wise center displacement < 1e-3)
# ---------------------------------------------------------------------------

def centers_echo(sample_circles, parent_circles, tolerance=1e-3):
    """Check if sample centers match parent centers within tolerance.
    Uses the echo field from the row (precomputed), but we recompute for safety."""
    if sample_circles is None or parent_circles is None:
        return False
    if len(sample_circles) != len(parent_circles):
        return False
    s_sorted = sorted(sample_circles)
    p_sorted = sorted(parent_circles)
    for (sx, sy, _), (px, py, _) in zip(s_sorted, p_sorted):
        if abs(sx - px) > tolerance or abs(sy - py) > tolerance:
            return False
    return True


# ---------------------------------------------------------------------------
# Rarefaction
# ---------------------------------------------------------------------------

def rarefy_distinct(hashes, m, n_draws, seed=42):
    """Rarefy to m samples, count distinct hashes, repeat n_draws times.
    Returns list of distinct-counts."""
    rng = random.Random(seed)
    hashes_list = list(hashes)
    results = []
    for _ in range(n_draws):
        sample = rng.sample(hashes_list, m)
        results.append(len(set(sample)))
    return results


# ---------------------------------------------------------------------------
# Bootstrap CI
# ---------------------------------------------------------------------------

def bootstrap_ci(values, n_resamples=10000, seed=42):
    """Bootstrap 95% CI (percentile) of the mean."""
    rng = random.Random(seed)
    n = len(values)
    means = []
    for _ in range(n_resamples):
        sample = [rng.choice(values) for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    lo = means[int(0.025 * n_resamples)]
    hi = means[int(0.975 * n_resamples)]
    return lo, hi


# ---------------------------------------------------------------------------
# Jonckheere-Terpstra permutation test
# ---------------------------------------------------------------------------
# Tie rule: ties contribute 0.5 (§3.4 of preregistration)

def jt_statistic(groups, ordered_groups):
    """Compute Jonckheere-Terpstra statistic with tie=0.5 rule.
    groups: dict[label] -> list of values
    ordered_groups: list of labels in hypothesized order (decreasing)
    """
    labels = ordered_groups
    k = len(labels)
    T = 0.0
    for i in range(k):
        for j in range(i + 1, k):
            for vi in groups[labels[i]]:
                for vj in groups[labels[j]]:
                    if vi > vj:
                        T += 1.0
                    elif vi == vj:
                        T += 0.5
                    # else vi < vj: contribute 0
    return T


def jt_permutation_test(groups, ordered_groups, n_shuffles=10000, seed=42):
    """JT permutation test with observed statistic, null mean, null sd, and p-value.
    Returns dict with observed, null_mean, null_sd, p, null_distribution."""
    rng = random.Random(seed)
    observed = jt_statistic(groups, ordered_groups)
    k = len(ordered_groups)
    
    # Collect all values with group labels
    all_items = []
    for label in ordered_groups:
        for v in groups[label]:
            all_items.append((v, label))
    
    null_stats = []
    for _ in range(n_shuffles):
        # Shuffle group assignments
        rng.shuffle(all_items)
        shuffled_groups = {label: [] for label in ordered_groups}
        idx = 0
        for label in ordered_groups:
            n = len(groups[label])
            for v, _ in all_items[idx:idx + n]:
                shuffled_groups[label].append(v)
            idx += n
        null_stats.append(jt_statistic(shuffled_groups, ordered_groups))
    
    null_mean = sum(null_stats) / len(null_stats)
    null_var = sum((s - null_mean) ** 2 for s in null_stats) / len(null_stats)
    null_sd = math.sqrt(null_var)
    
    # Permutation p (one-sided: T >= observed)
    extreme = sum(1 for s in null_stats if s >= observed)
    p = extreme / len(null_stats)
    
    return {
        "observed": observed,
        "null_mean": null_mean,
        "null_sd": null_sd,
        "p": p,
        "n_shuffles": n_shuffles,
        "null_distribution_sorted": sorted(null_stats),
    }


# ---------------------------------------------------------------------------
# Decision rule (§5)
# ---------------------------------------------------------------------------

def decide_verdict(m, per_rung_distinct, jt_result, score_jt_p, per_rung_validity, 
                   distinct_variance_by_rung, parent_counts,
                   run_label="CONFIRMATORY", label_note=""):
    """Apply decision rule from preregistration §5 (+ addendum R1-R7, 2026-07-28)."""
    reasons = []

    # 2026-07-28 (director): addendum R2/R5 gate. Ceiling rung absent, or
    # fewer than three rungs landed -> no trend test reportable regardless
    # of the numbers. Placed before the §5 gates because it is a
    # design-validity condition, not a power condition.
    if run_label == "FAILED":
        return "FAILED", [label_note, "descriptives above are EXPLORATORY only"]

    # UNDERPOWERED checks (precedence)
    if m < 20:
        return "UNDERPOWERED", [f"m = {m} < 20"]
    
    # Check parents: at least 3 parents with >= 2 valid rows per rung
    for rung, pcounts in parent_counts.items():
        n_good_parents = sum(1 for c in pcounts.values() if c >= 2)
        if n_good_parents < 3:
            return "UNDERPOWERED", [f"rung {rung}: only {n_good_parents} parents with >=2 valid rows (need >=3)"]
    
    # Zero variance in rarefaction draws in >=2 rungs
    zero_var_rungs = []
    for rung in per_rung_distinct:
        if max(per_rung_distinct[rung]) - min(per_rung_distinct[rung]) < 0.5:  # effectively zero
            zero_var_rungs.append(rung)
    if len(zero_var_rungs) >= 2:
        # 2026-07-28 (director): diagnostic only, verdict unchanged (defect 21).
        # Zero rarefaction variance has two causes: collapse (few distinct
        # solutions, mean << m) and saturation (every draw all-distinct,
        # mean == m). Prereg §5 treats both as dead instrument. Print which.
        diag = []
        for rung in zero_var_rungs:
            mu = sum(per_rung_distinct[rung]) / len(per_rung_distinct[rung])
            diag.append(f"{rung}={mu:.2f}/{m} " +
                        ("SATURATED" if mu >= m - 0.5 else "COLLAPSED"))
        return "UNDERPOWERED", [
            f"zero variance in rarefaction draws in {len(zero_var_rungs)} rungs: {zero_var_rungs}",
            "cause: " + ", ".join(diag)]
    
    # Sanity gate check on JT
    if jt_result["p"] == 0.0 or jt_result["p"] == 1.0:
        return "SUSPECT", [f"JT p = {jt_result['p']:.4f} exactly — suspect test"]
    
    # Extract mean distinct counts per rung
    means = {}
    for rung in RUNG_ORDER:
        if rung in per_rung_distinct:
            means[rung] = sum(per_rung_distinct[rung]) / len(per_rung_distinct[rung])
    
    # Check monotonic decline: D(q8_0) >= D(q4_k_m) >= D(q3_k_m) >= D(q2_k)
    present_rungs = [r for r in RUNG_ORDER if r in means]
    monotonic = True
    for i in range(len(present_rungs) - 1):
        if means[present_rungs[i]] < means[present_rungs[i + 1]]:
            monotonic = False
            break
    
    # SUPPORTED / PARTIAL / FALSIFIED
    distinct_significant = jt_result["p"] < 0.05
    score_flat = score_jt_p > 0.10
    
    if monotonic and distinct_significant and score_flat:
        return "SUPPORTED", [f"D(m) monotonic decline, JT p={jt_result['p']:.4f}, score JT p={score_jt_p:.4f}"]
    elif monotonic and distinct_significant and not score_flat:
        return "PARTIAL", [f"D(m) monotonic decline, JT p={jt_result['p']:.4f}, but score JT p={score_jt_p:.4f} (both fall)"]
    elif not distinct_significant:
        # Check if validity falls
        return "FALSIFIED", [f"D(m) flat, JT p={jt_result['p']:.4f}"]
    else:
        return "INCONCLUSIVE", [f"no decision rule matched"]


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("DISPERSION PROBE v2 — PREREGISTERED ANALYSIS")
    print("=" * 60)
    
    # Load data
    if not CAND_LOG.exists():
        print(f"ERROR: {CAND_LOG} not found")
        sys.exit(1)
    
    rows = load_rows(CAND_LOG)
    print(f"\nLoaded {len(rows)} rows from {CAND_LOG}")
    print(f"File size: {CAND_LOG.stat().st_size:,} bytes")
    
    prov = {}
    if PROVENANCE.exists():
        prov = load_provenance(PROVENANCE)
        print(f"Provenance: {PROVENANCE.stat().st_size:,} bytes")
        # Check ceiling substitution
        if "ceiling_substitution" in prov.get("conditions", {}):
            cs = prov["conditions"]["ceiling_substitution"]
            print(f"\nCeiling rung: q8_0 -> {cs.get('substitute', '???')} "
                  f"(q8_0 error: {cs.get('q8_0_error', '?')})")
            # Adjust rung order
            global RUNG_ORDER
            RUNG_ORDER = [cs.get("substitute", "q8_0") if r == "q8_0" else r for r in RUNG_ORDER]
            print(f"Adjusted rung order: {' > '.join(RUNG_ORDER)}")
    
    # Partition rows
    rung_rows = defaultdict(list)
    for r in rows:
        rung_rows[r["rung"]].append(r)

    # -----------------------------------------------------------------
    # 2026-07-28 (director): implement analysis_prereg_v2_addendum.md
    # rules R1-R5/R7 (landed-rung gate). Analyser predates the addendum
    # (defect 20); without this block a truncated run is silently
    # analysed over whatever rungs happen to be present, with no
    # CONFIRMATORY-DEGRADED label and no ceiling requirement. Written
    # blind, before any real v2 data existed. No metric, threshold,
    # draw count, or tie rule is changed by this block.
    # R6 note: when both R2/R5 FAILED and the UNDERPOWERED gates could
    # fire, FAILED is returned. Both are non-positive verdicts; FAILED
    # is the stronger statement (no trend test reportable at all).
    # -----------------------------------------------------------------
    CEILING = RUNG_ORDER[0]
    prov_rungs = prov.get("rungs") or sorted(rung_rows.keys())
    landed, not_landed = [], {}
    for rung in RUNG_ORDER:
        pcounts = defaultdict(int)
        for r in rung_rows.get(rung, []):
            if r["valid"]:
                pcounts[r["parent_id"]] += 1
        n_good = sum(1 for c in pcounts.values() if c >= 2)
        if rung in prov_rungs and n_good >= 3:
            landed.append(rung)
        else:
            not_landed[rung] = (rung in prov_rungs, n_good)

    print("\n" + "=" * 60)
    print("ADDENDUM R1: RUNG LANDING")
    print("=" * 60)
    for rung in RUNG_ORDER:
        if rung in landed:
            print(f"  {rung}: LANDED")
        else:
            in_prov, n_good = not_landed[rung]
            print(f"  {rung}: NOT LANDED (in provenance: {in_prov}, "
                  f"parents with >=2 valid rows: {n_good}, need >=3)")

    missing = [r for r in RUNG_ORDER if r not in landed]
    if CEILING not in landed:
        RUN_LABEL = "FAILED"
        LABEL_NOTE = (f"addendum R2: ceiling rung {CEILING} did not land; "
                      f"no trend test reportable")
    elif not missing:
        RUN_LABEL = "CONFIRMATORY"
        LABEL_NOTE = "addendum R3: all rungs landed; analysed exactly per prereg"
    elif len(landed) == 3 and "q2_k" in landed:
        RUN_LABEL = "CONFIRMATORY-DEGRADED"
        LABEL_NOTE = (f"addendum R4: three rungs landed ({' > '.join(landed)}); "
                      f"MISSING RUNG: {', '.join(missing)}")
    else:
        RUN_LABEL = "FAILED"
        LABEL_NOTE = (f"addendum R5: only {len(landed)} rung(s) landed "
                      f"({', '.join(landed) or 'none'}); trend test FAILED, "
                      f"all figures below are EXPLORATORY")
    print(f"\nRUN LABEL: {RUN_LABEL}")
    print(f"  {LABEL_NOTE}")

    RUNG_ORDER = [r for r in RUNG_ORDER if r in landed]
    if len(RUNG_ORDER) < 2:
        print("\nVERDICT: FAILED")
        print(f"  {LABEL_NOTE}")
        print("\n[done]")
        return

    print(f"\nRung counts:")
    for rung in RUNG_ORDER:
        if rung in rung_rows:
            n = len(rung_rows[rung])
            valid_n = sum(1 for r in rung_rows[rung] if r["valid"])
            infra_n = sum(1 for r in rung_rows[rung] if is_infra_error(r))
            print(f"  {rung}: {n} total, {valid_n} valid, {infra_n} infra-error")
    
    # Compute per-rung metrics
    print("\n" + "=" * 60)
    print("METRICS PER RUNG")
    print("=" * 60)
    
    per_rung_valid_canonical = {}  # rung -> list of canonical hashes (valid only)
    per_rung_valid_radii_canonical = {}
    per_rung_scores_valid = {}
    per_rung_scores_non_echo = {}
    per_rung_centers_echo = {}  # fraction
    parent_valid_counts = defaultdict(lambda: defaultdict(int))  # rung -> parent -> count
    per_rung_parent_rows = defaultdict(lambda: defaultdict(list))  # rung -> parent -> valid rows
    
    for rung in RUNG_ORDER:
        if rung not in rung_rows:
            continue
        rr = rung_rows[rung]
        
        # Filter valid rows
        valid_rows = [r for r in rr if r["valid"]]
        non_infra_rows = [r for r in rr if not is_infra_error(r)]
        valid_non_echo = [r for r in valid_rows if not r.get("echo", False)]
        
        # Denominator: exclude infrastructure errors (§4.5)
        denom = len(non_infra_rows)
        valid_n = len(valid_rows)
        validity_rate = valid_n / max(denom, 1)
        
        # Canonical hashes for valid rows
        valid_hashes = [canonicalise(r["circles"]) for r in valid_rows]
        valid_hashes = [h for h in valid_hashes if h is not None]
        per_rung_valid_canonical[rung] = valid_hashes
        
        valid_radii_hashes = [canonicalise_radii(r["circles"]) for r in valid_rows]
        valid_radii_hashes = [h for h in valid_radii_hashes if h is not None]
        per_rung_valid_radii_canonical[rung] = valid_radii_hashes
        
        # Scores
        scores = [r["score"] for r in valid_rows]
        per_rung_scores_valid[rung] = scores
        
        scores_ne = [r["score"] for r in valid_non_echo]
        per_rung_scores_non_echo[rung] = scores_ne
        
        # Centers-echo rate
        echo_n = sum(1 for r in valid_rows if r.get("echo", False))
        per_rung_centers_echo[rung] = echo_n / max(valid_n, 1)
        
        # Parent breakdown
        for r in valid_rows:
            pid = r["parent_id"]
            parent_valid_counts[rung][pid] += 1
            per_rung_parent_rows[rung][pid].append(r)
        
        print(f"\n{rung}:")
        print(f"  Total rows: {len(rr)}")
        print(f"  Infra-error rows: {len(rr) - denom}")
        print(f"  Valid rows: {valid_n}")
        print(f"  Validity rate (excl infra): {validity_rate:.4f}")
        print(f"  Raw distinct solutions: {len(set(valid_hashes))}")
        print(f"  Raw distinct radius-vectors: {len(set(valid_radii_hashes))}")
        if scores:
            print(f"  Mean score (valid): {sum(scores)/len(scores):.6f}")
        if scores_ne:
            print(f"  Mean score (valid non-echo): {sum(scores_ne)/len(scores_ne):.6f}")
        print(f"  Centers-echo rate: {per_rung_centers_echo[rung]:.4f}")
        print(f"  Parents with >=2 valid: {sum(1 for c in parent_valid_counts[rung].values() if c >= 2)}")
    
    # =====================================================================
    # PRIMARY TEST (§3.2–3.3): Rarefaction + JT
    # =====================================================================
    print("\n" + "=" * 60)
    print("PRIMARY TEST: RAREFIED DISTINCT-SOLUTION COUNT")
    print("=" * 60)
    
    # Determine m = minimum valid count across rungs
    valid_counts = {rung: len(per_rung_valid_canonical.get(rung, [])) for rung in RUNG_ORDER if rung in per_rung_valid_canonical}
    m = min(valid_counts.values()) if valid_counts else 0
    print(f"\nRarefaction depth m = {m}")
    
    # Pooled rarefaction
    per_rung_pooled = {}
    for rung in RUNG_ORDER:
        if rung not in per_rung_valid_canonical:
            continue
        hashes = per_rung_valid_canonical[rung]
        if len(hashes) < m:
            continue
        draws = rarefy_distinct(hashes, m, 1000)
        per_rung_pooled[rung] = draws
        mean_d = sum(draws) / len(draws)
        var_d = sum((d - mean_d) ** 2 for d in draws) / len(draws)
        sd_d = math.sqrt(var_d)
        print(f"  {rung}: {mean_d:.2f} ± {sd_d:.2f} (raw distinct: {len(set(hashes))})")
    
    # Per-parent rarefaction + JT
    print(f"\nPer-parent rarefied distinct counts (2000 draws):")
    per_parent_counts = defaultdict(dict)  # rung -> parent -> mean rarefied count
    
    for rung in RUNG_ORDER:
        if rung not in per_rung_parent_rows:
            continue
        for pid in sorted(per_rung_parent_rows[rung].keys()):
            prow = per_rung_parent_rows[rung][pid]
            phashes = [canonicalise(r["circles"]) for r in prow]
            phashes = [h for h in phashes if h is not None]
            m_parent = min(
                len([r for r in per_rung_parent_rows[r2].get(pid, []) if r["valid"]])
                for r2 in RUNG_ORDER if r2 in per_rung_parent_rows
            )
            if m_parent >= 2 and len(phashes) >= m_parent:
                draws = rarefy_distinct(phashes, m_parent, 2000)
                mean_p = sum(draws) / len(draws)
                per_parent_counts[rung][pid] = mean_p
                print(f"  {rung:8s} {pid:15s}: {mean_p:.3f} (raw {len(phashes)} rows, rarefied to {m_parent})")
            else:
                per_parent_counts[rung][pid] = None
                print(f"  {rung:8s} {pid:15s}: SKIP (m_parent={m_parent} < 2 or {len(phashes)} < {m_parent})")
    
    # JT test on per-parent rarefied counts
    # Use only parents that have counts in all rungs
    all_parents = sorted(set().union(*(set(d.keys()) for d in per_parent_counts.values())))
    complete_parents = []
    for pid in all_parents:
        if all(pid in per_parent_counts[rung] and per_parent_counts[rung][pid] is not None for rung in RUNG_ORDER if rung in per_parent_counts):
            complete_parents.append(pid)
    
    print(f"\nComplete parents for JT: {complete_parents}")
    
    if len(complete_parents) >= 3:
        jt_groups = {rung: [per_parent_counts[rung][pid] for pid in complete_parents] for rung in RUNG_ORDER if rung in per_parent_counts}
        present_rungs = [r for r in RUNG_ORDER if r in jt_groups]
        
        jt_result = jt_permutation_test(jt_groups, present_rungs, 10000)
        
        print(f"\nJT Trend Test (n={len(complete_parents)} parents):")
        print(f"  Observed JT = {jt_result['observed']:.2f}")
        print(f"  Null mean    = {jt_result['null_mean']:.2f}")
        print(f"  Null sd      = {jt_result['null_sd']:.2f}")
        print(f"  Permutation p = {jt_result['p']:.4f}")
        
        # Sanity gate
        if jt_result['p'] == 0.0 or jt_result['p'] == 1.0:
            print(f"\n  *** SUSPECT: p = {jt_result['p']:.4f} exactly — printing null distribution:")
            null_sorted = jt_result['null_distribution_sorted']
            for i, s in enumerate(null_sorted):
                marker = " <<< OBSERVED" if s == jt_result['observed'] else ""
                print(f"    {i+1:5d}: {s:.2f}{marker}")
        
        # Also run JT on per-parent mean scores
        score_groups = {}
        for rung in present_rungs:
            score_groups[rung] = []
            for pid in complete_parents:
                prow = per_rung_parent_rows[rung][pid]
                scores = [r["score"] for r in prow if r["valid"]]
                if scores:
                    score_groups[rung].append(sum(scores) / len(scores))
                else:
                    score_groups[rung].append(0.0)
        
        score_jt = jt_permutation_test(score_groups, present_rungs, 10000)
        print(f"\n  Score JT test:")
        print(f"    Observed JT = {score_jt['observed']:.2f}")
        print(f"    Permutation p = {score_jt['p']:.4f}")
    else:
        print(f"\n  JT test SKIPPED: only {len(complete_parents)} complete parents (need >=3)")
        jt_result = {"observed": 0, "null_mean": 0, "null_sd": 1, "p": 1.0}
        score_jt = {"observed": 0, "null_mean": 0, "null_sd": 1, "p": 1.0}
    
    # =====================================================================
    # SECONDARY METRICS
    # =====================================================================
    print("\n" + "=" * 60)
    print("SECONDARY METRICS")
    print("=" * 60)
    
    # Distinct radius-vector count (rarefied)
    print(f"\nDistinct radius-vector count (rarefied to m={m}, 1000 draws):")
    for rung in RUNG_ORDER:
        if rung not in per_rung_valid_radii_canonical:
            continue
        rhashes = per_rung_valid_radii_canonical[rung]
        if len(rhashes) >= m:
            rdraws = rarefy_distinct(rhashes, m, 1000)
            mean_r = sum(rdraws) / len(rdraws)
            var_r = sum((d - mean_r) ** 2 for d in rdraws) / len(rdraws)
            print(f"  {rung}: {mean_r:.2f} ± {math.sqrt(var_r):.2f}")
    
    # Mean score with bootstrap CI
    print(f"\nMean score among valid (bootstrap 95% CI):")
    for rung in RUNG_ORDER:
        if rung not in per_rung_scores_valid:
            continue
        scores = per_rung_scores_valid[rung]
        if len(scores) >= 2:
            lo, hi = bootstrap_ci(scores)
            mean_s = sum(scores) / len(scores)
            print(f"  {rung}: {mean_s:.4f} [{lo:.4f}, {hi:.4f}]")
    
    # Mean score among non-echo valid
    print(f"\nMean score among valid non-echo (bootstrap 95% CI):")
    for rung in RUNG_ORDER:
        if rung not in per_rung_scores_non_echo:
            continue
        scores = per_rung_scores_non_echo[rung]
        if len(scores) >= 2:
            lo, hi = bootstrap_ci(scores)
            mean_s = sum(scores) / len(scores)
            print(f"  {rung}: {mean_s:.4f} [{lo:.4f}, {hi:.4f}]  (n={len(scores)})")
        else:
            print(f"  {rung}: insufficient non-echo rows (n={len(scores)})")
    
    # =====================================================================
    # VERDICT
    # =====================================================================
    print("\n" + "=" * 60)
    print("VERDICT")
    print("=" * 60)
    
    verdict, reasons = decide_verdict(
        m=m,
        per_rung_distinct=per_rung_pooled,
        jt_result=jt_result,
        score_jt_p=score_jt["p"],
        per_rung_validity={rung: sum(1 for r in rung_rows[rung] if r["valid"]) / max(sum(1 for r in rung_rows[rung] if not is_infra_error(r)), 1) for rung in RUNG_ORDER if rung in rung_rows},
        distinct_variance_by_rung={rung: max(draws) - min(draws) if draws else 0 for rung, draws in per_rung_pooled.items()},
        parent_counts={rung: dict(parent_valid_counts[rung]) for rung in RUNG_ORDER if rung in parent_valid_counts},
        run_label=RUN_LABEL,
        label_note=LABEL_NOTE,
    )

    # 2026-07-28 (director): addendum R4 — every statement out of a
    # three-rung run must name the missing rung.
    if RUN_LABEL == "CONFIRMATORY-DEGRADED":
        verdict = f"{verdict} [CONFIRMATORY-DEGRADED]"
        reasons = list(reasons) + [LABEL_NOTE]

    print(f"\nVERDICT: {verdict}")
    for reason in reasons:
        print(f"  {reason}")
    
    print("\n[done]")


if __name__ == "__main__":
    main()
