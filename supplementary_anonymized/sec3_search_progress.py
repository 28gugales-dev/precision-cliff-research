"""
Section 3.6 -- the outcome-side consequence of the echo result.

Every earlier section-3 measure is a property of a single call: was this output
valid, did it echo its parent. None of them says what the *loop* did. This
script computes the loop-level statistic: how many times a lineage's running
best actually advanced across its ten generations.

Three things it reports, in this order, because the third is only interpretable
after the first two:

  1. ACCEPTED IMPROVEMENTS per lineage, per rung, per ledger. A hill-climb step
     is an accepted improvement: a valid output scoring strictly above the
     lineage's running best. Tested at LINEAGE level by exact permutation --
     calls within a lineage are not exchangeable, because whether call k can
     improve depends on improvements at calls < k.

  2. THE IDENTITY. An echo cannot improve: it reproduces the parent's score
     exactly, and the rule is strict. So accepted <= (valid - echo) by
     construction, and most of the contrast in (1) is the echo contrast in
     complement. This script prints `accepted`, `valid - echo`, and the gap k
     per cell so the reader can see exactly how much is new.

  3. CONDITIONAL RATE. Among departures only (valid and not an echo), what
     fraction improved. This is the part not implied by the echo result: it asks
     whether quantization degrades the *quality* of departures or only their
     *frequency*. Reported per cell with n. At the 2-bit endpoints n is 1, 5 and
     8 -- the question is posed, not answered.

  4. FINAL BEST SCORE per lineage. The outcome metric a practitioner reports.

7B note: the 7B ledger stores no coordinates, so echo is not computable there
and rows 2 and 3 are 14B-only. Accepted improvements ARE computable, which
gives this statistic a second scale for free -- and at 7B it does not replicate.

Run:  python sec3_search_progress.py
"""
import json, glob, os, collections, itertools, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "sec3_artifacts")
if not os.path.isdir(ART):
    ART = os.path.join(HERE, "..", "agent-run")

SEED_SCORE = 0.89999          # the seeded 6x5 grid every lineage starts from


def load(pattern):
    hits = glob.glob(os.path.join(ART, pattern), recursive=True)
    if not hits:
        raise SystemExit(f"missing ledger: {pattern}")
    return [json.loads(l) for l in open(hits[0], encoding="utf-8") if l.strip()]


def key(circles):
    """Order-insensitive fingerprint at six decimals (same as sec3_ladder_repro)."""
    if not circles:
        return None
    return tuple(sorted(tuple(round(float(v), 6) for v in c) for c in circles))


def seed_key():
    hits = glob.glob(os.path.join(
        ART, "precision_sweep_14b_v2_output/**/state/q2_k_seed_42.json"),
        recursive=True)
    if not hits:
        return None
    st = json.load(open(hits[0], encoding="utf-8"))
    assert abs(st["best_score"] - SEED_SCORE) < 1e-9
    return key(st["best_circles"])


SEED_KEY = seed_key()


def replay(rows, with_echo=True):
    """Per-lineage: accepted improvements, valid count, echo count, final best."""
    lin = collections.defaultdict(list)
    for r in rows:
        lin[(r["quant"], r["seed"])].append(r)
    out = {}
    for (q, s), rs in lin.items():
        rs.sort(key=lambda r: r["gen"])
        parent, best = SEED_KEY, SEED_SCORE
        acc = valid = echo = 0
        for r in rs:
            k = key(r.get("circles")) if with_echo else None
            if r.get("valid"):
                valid += 1
                if with_echo and parent is not None and k == parent:
                    echo += 1
                if r.get("score") is not None and r["score"] > best:
                    best, parent = r["score"], k
                    acc += 1
        out[(q, s)] = dict(accepted=acc, valid=valid, echo=echo, final=best,
                           calls=len(rs))
    return out


def perm_p(group_a, group_b):
    """Exact two-sided permutation test on the difference of means, over
    lineage-level counts. Enumerates every split of the pooled lineages."""
    pooled = list(group_a) + list(group_b)
    na, n = len(group_a), len(pooled)
    obs = abs(statistics.mean(group_a) - statistics.mean(group_b))
    tot = hit = 0
    for idx in itertools.combinations(range(n), na):
        a = [pooled[i] for i in idx]
        b = [pooled[i] for i in range(n) if i not in idx]
        tot += 1
        if abs(statistics.mean(a) - statistics.mean(b)) >= obs - 1e-12:
            hit += 1
    return hit / tot, tot


def report(rows, label, with_echo=True, endpoint=None, comparators=()):
    st = replay(rows, with_echo)
    quants = sorted({q for q, _ in st})
    print(f"\n{'='*74}\n{label}\n{'='*74}")
    print(f"{'rung':<11}{'accepted / lineage':<26}{'total':<9}"
          f"{'valid':<8}{'echo':<7}{'final best / lineage'}")
    per_rung = {}
    for q in quants:
        cells = [st[(qq, s)] for qq, s in sorted(st) if qq == q]
        acc = [c["accepted"] for c in cells]
        per_rung[q] = acc
        calls = sum(c["calls"] for c in cells)
        v = sum(c["valid"] for c in cells)
        e = sum(c["echo"] for c in cells)
        fin = [round(c["final"], 4) for c in cells]
        print(f"{q:<11}{str(acc):<26}{f'{sum(acc)}/{calls}':<9}"
              f"{f'{v}':<8}{(str(e) if with_echo else '-'):<7}{fin}")

    if with_echo:
        print(f"\n  identity check -- an echo cannot improve, so accepted <= valid - echo:")
        print(f"  {'rung':<11}{'accepted':<11}{'valid - echo':<15}{'gap k'}")
        for q in quants:
            cells = [st[(qq, s)] for qq, s in sorted(st) if qq == q]
            a = sum(c["accepted"] for c in cells)
            d = sum(c["valid"] - c["echo"] for c in cells)
            print(f"  {q:<11}{a:<11}{d:<15}{d - a}")
        print(f"\n  conditional on departing (valid and not an echo), fraction that improved:")
        for q in quants:
            cells = [st[(qq, s)] for qq, s in sorted(st) if qq == q]
            a = sum(c["accepted"] for c in cells)
            d = sum(c["valid"] - c["echo"] for c in cells)
            rate = f"{a}/{d}" + (f" ({100*a/d:.0f}%)" if d else "")
            flag = "   <- n too small to read" if d < 10 else ""
            print(f"    {q:<11}{rate}{flag}")

    if endpoint and comparators:
        print(f"\n  lineage-level exact permutation on accepted improvements:")
        for c in comparators:
            if c == "POOLED":
                other = [x for q in quants if q != endpoint for x in per_rung[q]]
                cl = "pooled other rungs"
            else:
                other, cl = per_rung[c], c
            p, tot = perm_p(per_rung[endpoint], other)
            print(f"    {endpoint} {per_rung[endpoint]} vs {cl} {other}"
                  f"  ->  p = {p:.4f}  ({tot} splits enumerated)")
        print(f"\n  same test on FINAL BEST SCORE (the outcome metric):")
        fin_r = {q: [st[(qq, s)]["final"] for qq, s in sorted(st) if qq == q]
                 for q in quants}
        for c in comparators:
            if c == "POOLED":
                other = [x for q in quants if q != endpoint for x in fin_r[q]]
                cl = "pooled other rungs"
            else:
                other, cl = fin_r[c], c
            p, _ = perm_p(fin_r[endpoint], other)
            print(f"    {endpoint} mean {statistics.mean(fin_r[endpoint]):.4f} vs "
                  f"{cl} mean {statistics.mean(other):.4f}  ->  p = {p:.4f}")
    return st


print("=" * 74)
print("PAPER 2 SECTION 3.6 -- loop-level search progress, from raw ledgers")
print("=" * 74)
print("\nPOST-HOC. This statistic was not preregistered on any wave. It is\n"
      "reported as a consequence of the registered echo result, not as an\n"
      "independent test, and the identity block below shows how much of it is\n"
      "the echo contrast restated.")

report(load("precision_sweep_14b_v2_output/**/cand*.jsonl"),
       "14B re-execution ladder (the registered ladder)",
       endpoint="q2_k", comparators=("POOLED", "q4_k_m"))

report(load("precision_sweep_14b_fresh_output/**/cand*fresh.jsonl"),
       "14B fresh seeds (five never-sampled seeds)",
       endpoint="q2_k", comparators=("q4_k_m",))

report(load("precision_sweep_14b_iq2_output/**/cand*iq2.jsonl"),
       "14B IQ2 control (scheme vs bit-width)",
       endpoint="q2_k_imx", comparators=("iq2_m",))

report(load("precision_sweep/candidates_precision.jsonl"),
       "7B ladder -- SECOND SCALE. No coordinates stored, so echo is not "
       "computable\n     here; accepted improvements are.",
       with_echo=False, endpoint="q2_k", comparators=("POOLED", "q4_k_m"))

print(f"\n{'='*74}\nWHAT TO READ OFF THE ABOVE\n{'='*74}")
print("""  14B: the 2-bit rung takes 1 hill-climb step in 50 calls where the upper
       three take 14-16 each. Replicates on never-sampled seeds (3 vs 14) and
       on the independently produced imatrix Q2_K (6 vs 16).
  identity: most of that gap is the echo result in complement. The gap k is
       small and positive in every cell -- the residual is rows that departed
       from the parent and still failed to beat it.
  conditional: at every 2-bit endpoint the departure count is under 10, so
       whether quantization degrades departure QUALITY as well as FREQUENCY is
       posed and not answered by these data.
  outcome: final best score after ten generations does not separate the rungs.
       A metric a practitioner would report is blind to a collapse in search
       activity of more than an order of magnitude.
  7B:  does not replicate -- the 2-bit rung takes the MOST steps of five rungs.
       Validity at 7B is 4-12 of 50 at every rung, so no rung is searching
       much; the statistic has little room to separate. Consistent with the
       viability inversion section 3 already reports at this scale.""")
