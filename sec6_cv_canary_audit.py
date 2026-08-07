"""
Section 6 item 4, audited against section 3's own released data.

Item 4 is the only element of this paper's disclosure standard we claim as new,
and the paper concedes it is the element the paper does not itself implement. It
proposes a serving-signature canary with an explicit firing condition:

    "flag an arm when its duration CV falls below one third of the neighbouring
     tier's on the same cells"

Section 3's ledgers carry per-invocation `wall_s` on every row, across weight
files pinned by SHA-256 on one fixed inference stack. So the canary CAN be run --
on a condition where the serving path is known to be constant and only the weight
file changes. That is the cleanest possible test of a false-positive mode, and it
is a test the paper owes its own proposal.

WHAT THIS SCRIPT FINDS. The canary fires. It fires on the 2-bit rung, on both
probe waves independently, at a ratio below the one-third threshold item 4 names.
And the serving path did not change: same llama.cpp build, a single Tesla P100
(per provenance.json -- the ladders ran on 2 x T4, and ladder timings are never
compared with probe timings here), same sampling parameters, same harness, only
the weight file differing.

Conditioning on echo shows why. Echo rows re-emit the parent verbatim, so they
share a token count, so they share a duration. Duration CV among echo rows is low
at EVERY rung. Duration CV among non-echo rows is high at every rung. The 2-bit
rung's aggregate CV is low because almost all of its rows are echoes -- an output
property, not a serving property.

CONSEQUENCE FOR ITEM 4. A low duration CV is not evidence of a fast or
speculative decode path until output degeneracy is excluded. Item 4 must carry
that control, and this script is the demonstration that it needs one.

Run:  python sec6_cv_canary_audit.py
"""
import json, glob, os, statistics, collections, itertools, random

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "sec3_artifacts")
RUNGS = ["q4_k_m", "q3_k_m", "q2_k"]
THIRD = 1.0 / 3.0
RNG = random.Random(20260807)


def load(pattern):
    hits = glob.glob(os.path.join(ART, pattern), recursive=True)
    if not hits:
        raise SystemExit(f"missing ledger: {pattern}")
    return [json.loads(l) for l in open(hits[0], encoding="utf-8") if l.strip()]


def cv(xs):
    return statistics.stdev(xs) / statistics.mean(xs) if len(xs) > 1 else float("nan")


def perm_cv_ratio(a, b, nperm=20000):
    """Two-sided permutation test on the CV ratio, resampling the pooled durations.
    Tests whether the dispersion difference is larger than label-shuffling produces."""
    pooled = list(a) + list(b)
    na = len(a)
    obs = cv(a) / cv(b)
    hits = 0
    for _ in range(nperm):
        RNG.shuffle(pooled)
        r = cv(pooled[:na]) / cv(pooled[na:])
        if r <= obs or r >= 1 / obs:
            hits += 1
    return (hits + 1) / (nperm + 1)


def report(rows, label, rung_key):
    rows = [r for r in rows if r.get("wall_s") and r.get("valid")]
    print(f"\n{'='*76}\n{label}: {len(rows)} valid rows with a duration\n{'='*76}")
    by = {q: [r for r in rows if r[rung_key] == q] for q in RUNGS}
    by = {q: v for q, v in by.items() if len(v) > 1}
    if not by:
        return None

    print(f"{'rung':<10}{'n':<6}{'median wall_s':<16}{'duration CV':<15}"
          f"{'median tokens':<16}{'distinct token counts'}")
    cvs = {}
    for q in RUNGS:
        if q not in by:
            continue
        w = [r["wall_s"] for r in by[q]]
        t = [r["completion_tokens"] for r in by[q]]
        cvs[q] = cv(w)
        print(f"{q:<10}{len(w):<6}{statistics.median(w):<16.2f}{cv(w):<15.4f}"
              f"{statistics.median(t):<16.0f}{len(set(t))}")

    ref = "q4_k_m"
    if ref in cvs:
        print(f"\nitem 4's firing condition -- CV below one third of the neighbouring"
              f" tier's ({ref} = {cvs[ref]:.4f}, threshold {THIRD*cvs[ref]:.4f}):")
        for q in RUNGS:
            if q == ref or q not in cvs:
                continue
            fires = cvs[q] < THIRD * cvs[ref]
            print(f"   {q:<10}CV {cvs[q]:.4f}   ratio {cvs[q]/cvs[ref]:.3f}   "
                  f"-> {'FIRES' if fires else 'does not fire'}")
        a = [r["wall_s"] for r in by["q2_k"]]
        b = [r["wall_s"] for r in by[ref]]
        print(f"   permutation on the CV ratio, q2_k vs {ref}: "
              f"p = {perm_cv_ratio(a, b):.4f}")

    print(f"\nsame rows split by whether the output ECHOES its parent:")
    print(f"{'rung':<10}{'echo n':<9}{'echo CV':<12}{'echo tok-uniq':<16}"
          f"{'non-echo n':<13}{'non-echo CV':<14}{'non-echo tok-uniq'}")
    for q in RUNGS:
        if q not in by:
            continue
        e = [r for r in by[q] if r.get("echo")]
        n = [r for r in by[q] if not r.get("echo")]
        ec = cv([r["wall_s"] for r in e]) if len(e) > 1 else float("nan")
        nc = cv([r["wall_s"] for r in n]) if len(n) > 1 else float("nan")
        print(f"{q:<10}{len(e):<9}{ec:<12.4f}{len(set(r['completion_tokens'] for r in e)):<16}"
              f"{len(n):<13}{nc:<14.4f}{len(set(r['completion_tokens'] for r in n))}")
    return cvs


print("=" * 76)
print("AUDIT OF SECTION 6 ITEM 4 -- does the duration-CV canary have a")
print("false-positive mode, on a condition where the serving path is FIXED?")
print("=" * 76)
print("""
Setup. Every row below comes from a run in which the inference stack was constant
-- same llama.cpp build, a single Tesla P100, same sampling parameters, same
harness -- and only the SHA-256-pinned weight file changed. Whatever the canary
reports here, it is not reporting a serving-path change, because there was none.

One confound is NOT excluded and is stated rather than buried: the probe loads one
weight file at a time and runs that rung to completion, so rungs are sequential
within a session, not interleaved. Slow drift over a session would present as a
between-rung difference.""")

report(load("dispersion_probe/probe_samples.jsonl"),
       "fixed-parent dispersion probe, wave 1", "rung")
report(load("dispersion_probe_v2/**/probe_samples.jsonl"),
       "fixed-parent dispersion probe, wave 2 (independent seeds)", "rung")

print(f"\n{'='*76}\nAN ATTEMPTED REPAIR, AND WHY IT FAILS AS AN ATTESTATION TOOL\n{'='*76}")
print("""  If duration dispersion is confounded by output identity, the obvious repair is
  to remove the confound: throughput over NON-ECHO valid rows only. It looks
  excellent on one wave and then fails three ways. Everything below is computed
  here, not quoted.""")

def nonecho(pat):
    return [r for r in load(pat)
            if r.get("valid") and r.get("wall_s") and not r.get("echo")]

print("\n  (a) per-wave non-echo throughput, with RANGES and not only medians:")
print(f"    {'wave':<7}{'rung':<10}{'n':<5}{'median tok/s':<15}{'observed range'}")
for _lab, _pat in (("w1", "dispersion_probe/probe_samples.jsonl"),
                   ("w2", "dispersion_probe_v2/**/probe_samples.jsonl")):
    for _q in RUNGS:
        _s = sorted(r["completion_tokens"] / r["wall_s"]
                    for r in nonecho(_pat) if r["rung"] == _q)
        if len(_s) < 2:
            print(f"    {_lab:<7}{_q:<10}{len(_s):<5}(too few)")
            continue
        print(f"    {_lab:<7}{_q:<10}{len(_s):<5}{statistics.median(_s):<15.2f}"
              f"[{min(_s):.3f}, {max(_s):.3f}]")
print("""
  Wave 2's three bands are disjoint. WAVE 1'S ARE NOT: Q4_K_M spans
  [16.455, 18.188] and entirely CONTAINS Q2_K's [16.703, 16.753]. Reporting wave 1
  by its median alone -- which an earlier draft of this paper did -- hides that.
  Pooled across waves the bands overlap. Disjointness is a wave-2 property, not a
  property of the released data.""")

print("\n  (b) the cold-start effect, and what it silently filtered:")
print(f"    {'wave':<7}{'rung':<10}{'cold n':<9}{'cold med':<11}{'warm n':<9}"
      f"{'warm med':<11}{'ratio'}")
for _lab, _pat in (("w1", "dispersion_probe/probe_samples.jsonl"),
                   ("w2", "dispersion_probe_v2/**/probe_samples.jsonl")):
    _rows = [r for r in load(_pat) if r.get("wall_s") and r.get("completion_tokens")]
    _seen, _c, _w = set(), collections.defaultdict(list), collections.defaultdict(list)
    for r in _rows:
        k = (r["rung"], r.get("parent_id"))
        (_c if k not in _seen else _w)[r["rung"]].append(
            r["completion_tokens"] / r["wall_s"])
        _seen.add(k)
    for _q in RUNGS:
        if not _c[_q] or not _w[_q]:
            continue
        cm, wm = statistics.median(_c[_q]), statistics.median(_w[_q])
        print(f"    {_lab:<7}{_q:<10}{len(_c[_q]):<9}{cm:<11.2f}{len(_w[_q]):<9}"
              f"{wm:<11.2f}{cm/wm:.3f}")
print("""
  The FIRST invocation against each parent runs at about 92 percent of that rung's
  steady-state throughput, uniformly across all twelve rung-by-wave cells --
  consistent with prefill or cache warm-up, and far too small to be model load
  bleeding into wall_s. On wave 2 every cold row happens to be an echo or invalid,
  so the echo filter removed them by accident and the non-echo set is silently a
  WARM set. Wave 1's cold Q4_K_M row leaked through at 16.455 tok/s, and it is
  precisely the row that destroys wave-1 disjointness. A verifier's fresh probe is
  always a cold invocation, so a verifier reads the 92 percent band, not the
  published one.""")

print("\n  (c) the same weight file on different hardware -- and the order INVERTS:")
lad = [r for r in load("precision_sweep_14b_v2_output/**/cand*.jsonl")
       if r.get("wall_s") and r.get("completion_tokens")]
prb = [r for r in load("dispersion_probe_v2/**/probe_samples.jsonl")
       if r.get("valid") and r.get("wall_s")]
print(f"    {'weight file':<12}{'P100 probe med':<18}{'2 x T4 ladder med'}")
for _q in ("q4_k_m", "q2_k"):
    a = [r["completion_tokens"] / r["wall_s"] for r in prb if r["rung"] == _q]
    b = [r["completion_tokens"] / r["wall_s"] for r in lad if r["quant"] == _q]
    print(f"    {_q:<12}{statistics.median(a):<18.2f}{statistics.median(b):.2f}")
print("""
  Identical SHA-256-pinned files. On the P100 probe Q4_K_M is FASTER than Q2_K;
  on the 2 x T4 ladder Q2_K is faster than Q4_K_M. Not a shifted scale -- the
  ORDER inverts. A per-file throughput band is not portable across hardware, and
  attestation is exactly the case where the verifier does not control hardware.""")

print("\n  (d) throughput is length-dependent; seconds-per-token is the stable form:")
_rows = nonecho("dispersion_probe_v2/**/probe_samples.jsonl")
for _q in RUNGS:
    xs = [(r["completion_tokens"], r["completion_tokens"] / r["wall_s"])
          for r in _rows if r["rung"] == _q]
    if len(xs) < 3:
        continue
    mx = statistics.mean([x for x, _ in xs]); my = statistics.mean([y for _, y in xs])
    num = sum((x - mx) * (y - my) for x, y in xs)
    den = (sum((x - mx) ** 2 for x, _ in xs) * sum((y - my) ** 2 for _, y in xs)) ** 0.5
    spt = sorted(r["wall_s"] / r["completion_tokens"] for r in _rows if r["rung"] == _q)
    print(f"    {_q:<10}corr(tokens, tok/s) = {num/den:+.3f}   "
          f"s/token range [{min(spt):.5f}, {max(spt):.5f}]")
print("""
  Within a rung, longer completions run slower per token, correlation about -0.9.
  The tok/s bands hold only inside the observed token window. Inverting to seconds
  per token removes the dependence and gives tighter bands, so s/token is the form
  to report -- though it fixes none of (a), (b) or (c).""")

print("\n  (e) throughput does not order by bit-width, on EITHER ladder"
      " (computed here, not quoted):")
for _lab, _pat, _rungs in (
        ("14B ladder, 2 x T4", "precision_sweep_14b_v2_output/**/cand*.jsonl",
         ["q8_0", "q4_k_m", "q3_k_m", "q2_k"]),
        ("7B ladder, 2 x T4", "precision_sweep/candidates_precision.jsonl",
         ["fp16", "q8_0", "q4_k_m", "q3_k_m", "q2_k"])):
    _r = [x for x in load(_pat) if x.get("wall_s") and x.get("completion_tokens")]
    cells = [(q, statistics.median([x["completion_tokens"] / x["wall_s"]
                                    for x in _r if x["quant"] == q])) for q in _rungs]
    print(f"    {_lab:<22}" + "  ".join(f"{q} {v:.2f}" for q, v in cells))
print("""
  On the 14B ladder Q8_0 -- the highest-precision rung run -- is the SLOWEST of
  four. On the 7B ladder FP16 is slower than every quantized rung, and Q3_K_M
  sits below Q4_K_M at both scales.""")


print(f"\n{'='*76}\nWHAT THIS MEANS FOR ITEM 4\n{'='*76}")
print("""  The canary FIRES on the 2-bit rung, on both waves independently, at a ratio
  below the one-third threshold item 4 names -- and the serving path was fixed by
  construction. So item 4 as published has a false-positive mode.

  The mechanism is visible in the echo split. An echo re-emits its parent
  verbatim, so it lands on the same token count, so it takes very nearly the same
  time. Duration CV among echo rows is low at EVERY rung, 0.011 to 0.022. Duration
  CV among non-echo rows is high at EVERY rung, 0.029 to 0.082. The 2-bit rung's
  aggregate CV is low because almost all of its rows are echoes -- 46 of 49 on
  wave 1, 77 of 84 on wave 2. That is a property of the OUTPUT, not of the path
  that served it.

  Item 4 therefore needs a control it does not currently carry: report duration
  dispersion CONDITIONED on output identity, or exclude repeated outputs before
  computing CV. Without it, a degenerate proposer looks exactly like a fast
  serving path on the one statistic the standard asks a reader to watch.

  This does not overturn section 4, whose serving-signature evidence is an
  absolute latency gap of one to two orders of magnitude rather than a dispersion
  ratio, and whose arm was not echoing -- its failure mode was invalid geometry,
  4 of 30 valid. But it is a competing explanation section 4 never named for the
  class of evidence it relies on, and section 6 now names it.

  The non-monotonicity above is a second caution for section 4, of a different
  kind. Section 4 reads an unusually FAST arm as evidence of a cheaper or
  speculative serving path. Within these ladders speed does not order by precision
  at all: the highest-precision rung is the slowest at both scales. The magnitudes
  are not comparable -- section 4's gap is one to two orders and these are tens of
  percent -- so this does not contradict the reading. It does show that "faster"
  and "lower precision" are not the same axis even on a fixed stack, which is a
  step section 4's inference passes through without stating.""")
