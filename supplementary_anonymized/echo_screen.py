"""
echo_screen.py -- the parent-echo canary of section 6, item 5.

A discovery loop can be degenerate for its entire budget while every metric it
watches reads healthy: section 3 shows viability and validity do not move, and
section 3.6 shows final best score does not separate the rungs at a ten-generation
horizon. The rate at which a proposer returns its parent unchanged does move, and
it costs nothing to compute -- if you logged the emitted structure rather than
only its score.

USE
    Hold one parent fixed. Issue 25-50 proposal calls against it at your
    production settings. Log each emitted structure verbatim. Then:

        python echo_screen.py proposals.jsonl

    Each line of proposals.jsonl is one call:
        {"valid": true, "structure": [[x, y, r], ...]}
    Optionally per row, or once via --parent:
        {"parent": [[x, y, r], ...]}

    Rows with "valid": false are counted and excluded from the rate, because an
    echo is defined among valid outputs. If your rows carry "circles" or "points"
    instead of "structure", they are picked up automatically.

VERDICT
    >= 60%  RED     -- consistent with the degenerate regime of section 3
    <= 35%  NORMAL  -- departing at the rate a healthy proposer does
    between AMBIGUOUS

    60 and 35 are the bounds preregistered in the fresh-seed runner of section 3
    (`q2_k >= 60%; q4_k_m <= 35%`), where they held at 79% against 6%.

USE A WEAK PARENT. THIS IS NOT OPTIONAL.
    Those bounds were registered for the LOOP condition. Held against a FIXED
    parent, the echo rate depends heavily on how good that parent is, and section
    3's probe measures exactly how heavily -- pooled over both waves, echo rate
    among valid outputs by parent score:

        parent   Q4_K_M        Q3_K_M        Q2_K
        0.880     7/30 (23%)    8/26 (31%)   19/21 (90%)
        0.900     8/19 (42%)    5/20 (25%)   14/16 (88%)
        1.040    21/30 (70%)   14/25 (56%)   22/24 (92%)
        1.300    16/30 (53%)   13/28 (46%)   30/30 (100%)
        1.550    23/31 (74%)   18/23 (78%)   19/19 (100%)
        1.650    15/24 (62%)   14/20 (70%)   19/23 (83%)

    Read the bottom half of that table: against a GOOD parent a perfectly healthy
    Q4_K_M proposer echoes at 62-74% and Q3_K_M at 70-78%, well past the RED line.
    The screen is only informative against a WEAK parent -- near the bottom of the
    range your loop occupies, in practice its seed configuration. There the
    separation is clean: 23-42% healthy against 88-90% degenerate.

    Against a strong parent this tool will return RED on a healthy proposer and
    the reading is worthless. It does not know your parent's quality and cannot
    warn you. That is your job.

WHAT THIS IS NOT
    A calibrated precision detector. Validated on one task, one model family, one
    scale, one quantization family. Read a RED verdict at a weak parent as
    "something is wrong with whatever is serving this proposer" -- a tripwire, not
    a measurement. Note also that even at a weak parent one healthy cell reaches
    42%, above the NORMAL line, so AMBIGUOUS does not imply degraded.
"""
import argparse
import json
import sys
from math import comb

STRUCTURE_KEYS = ("structure", "circles", "points", "candidate")
RED, NORMAL = 0.60, 0.35


def fingerprint(struct, dp=6):
    """Order-insensitive fingerprint at dp decimals. Elements may be any fixed-arity
    numeric tuple -- [x, y, r] circles, [x, y] points, anything comparable."""
    if not struct:
        return None
    try:
        return tuple(sorted(tuple(round(float(v), dp) for v in el) for el in struct))
    except (TypeError, ValueError) as e:
        raise SystemExit(
            f"a structure is not a list of numeric tuples ({e}). If your rows store "
            "the structure as a JSON *string*, decode it before passing it in.")


def pick(row):
    for k in STRUCTURE_KEYS:
        if k in row and row[k]:
            return row[k]
    return None


def binom_interval(k, n, conf=0.95):
    """Exact Clopper-Pearson interval by bisection on the binomial tail. No scipy:
    this script must run wherever a practitioner's loop runs."""
    if n == 0:
        return (0.0, 1.0)
    target = (1 - conf) / 2

    def le(p, j):                              # P(X <= j)
        return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(j + 1))

    def bisect(f, increasing):
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if (f(mid) < target) == increasing:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    # lower bound: P(X >= k) = alpha/2, increasing in p
    low = 0.0 if k == 0 else bisect(lambda p: 1 - le(p, k - 1), True)
    # upper bound: P(X <= k) = alpha/2, decreasing in p
    high = 1.0 if k == n else bisect(lambda p: le(p, k), False)
    return low, high


def screen(rows, parent=None, dp=6):
    pf = fingerprint(parent, dp) if parent else None
    valid = echo = invalid = no_struct = 0
    seen_parents = set()
    for r in rows:
        if "valid" not in r:
            raise SystemExit(
                "a row has no 'valid' key. This tool will not guess: a row whose "
                "validity is unknown could be an invalid row counted as valid, "
                "which silently deflates the echo rate and can turn RED into "
                "AMBIGUOUS. Add the key to every row.")
        v = r["valid"]
        if isinstance(v, str):
            raise SystemExit(f"'valid' is the string {v!r}. Use a JSON boolean or 0/1.")
        if not v:
            invalid += 1
            continue
        s = pick(r)
        if s is None:
            no_struct += 1
            continue
        if pf is None:
            p = r.get("parent")
            if not p:
                raise SystemExit(
                    "no parent: pass --parent parent.json, or give each row a "
                    "'parent' field. The screen is defined against a FIXED parent -- "
                    "running it against a moving parent measures something else.")
            pf_row = fingerprint(p, dp)
        else:
            pf_row = pf
        seen_parents.add(pf_row)
        if len(seen_parents) > 1:
            raise SystemExit(
                "the parent is not constant across rows. The screen is defined "
                "against a FIXED parent; run against a moving parent and the "
                "number means something else entirely (see section 3).")
        valid += 1
        if fingerprint(s, dp) == pf_row:
            echo += 1
    return dict(valid=valid, echo=echo, invalid=invalid, no_struct=no_struct)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ledger", help="JSONL, one proposal call per line")
    ap.add_argument("--parent", help="JSON file holding the fixed parent structure")
    ap.add_argument("--dp", type=int, default=6,
                    help="decimals at which structures are compared (default 6)")
    a = ap.parse_args()

    rows = [json.loads(l) for l in open(a.ledger, encoding="utf-8") if l.strip()]
    parent = json.load(open(a.parent, encoding="utf-8")) if a.parent else None
    if isinstance(parent, dict):
        parent = pick(parent)

    r = screen(rows, parent, a.dp)
    n, k = r["valid"], r["echo"]
    if n == 0:
        print("no valid rows -- the screen is undefined. Check the ledger.")
        sys.exit(2)
    rate = k / n
    lo, hi = binom_interval(k, n)

    verdict = ("RED" if rate >= RED else "NORMAL" if rate <= NORMAL else "AMBIGUOUS")
    print(f"calls read            {len(rows)}")
    print(f"valid                 {n}   (invalid {r['invalid']}, unparsed {r['no_struct']})")
    print(f"parent echoes         {k}")
    print(f"echo rate             {100*rate:.1f}%   95% CI [{100*lo:.1f}%, {100*hi:.1f}%]")
    print(f"verdict               {verdict}")
    if n < 20:
        print("\nWARNING: fewer than 20 valid rows. The interval above is wide enough "
              "to span both thresholds at most rates; issue more calls before acting.")
    if verdict == "RED":
        print("\nAt or above 60%. In section 3's data this regime coincided with a loop "
              "taking 1 accepted hill-climb step in 50 calls while viability, validity "
              "and final best score all read normal. Check what is serving this "
              "proposer before trusting the run. This is a tripwire, not a measurement "
              "of served precision -- see the header.")
    elif verdict == "AMBIGUOUS":
        print("\nBetween the bounds. Note that the healthy baseline moves with parent "
              "quality (6% to 52% across section 3's conditions), so a middling rate "
              "against an unmatched parent is close to uninformative. Re-run against a "
              "parent of known quality, or use the five-call must-differ variant.")


if __name__ == "__main__":
    main()
