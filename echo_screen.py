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
    <= 30%  NORMAL  -- departing at the rate a healthy proposer does
    between AMBIGUOUS

WHAT THIS IS NOT
    A calibrated precision detector. The bounds 60/30 are the ones preregistered
    in the fresh-seed runner of section 3, where they held at 79% against 6%, and
    they are validated on one task, one model family, one scale, one quantization
    family. The rate depends on which parent you hold fixed: the fixed-parent
    control in section 3 moves the healthy baseline from 6% to 33-52% with parent
    quality alone. Read a RED verdict as "something is wrong with whatever is
    serving this proposer" -- a tripwire, not a measurement. An AMBIGUOUS verdict
    with an unmatched parent means very little.
"""
import argparse
import json
import sys
from math import comb

STRUCTURE_KEYS = ("structure", "circles", "points", "candidate")
RED, NORMAL = 0.60, 0.30


def fingerprint(struct, dp=6):
    """Order-insensitive fingerprint at dp decimals. Elements may be any fixed-arity
    numeric tuple -- [x, y, r] circles, [x, y] points, anything comparable."""
    if not struct:
        return None
    return tuple(sorted(tuple(round(float(v), dp) for v in el) for el in struct))


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
    for r in rows:
        if r.get("valid") is False:
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
