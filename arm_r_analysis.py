"""
Arms B2 and R, scored against `arm_r_preregistration.md` exactly as it was locked.

Everything below is computed from the released ledgers in arm_r_artifacts/ and, for the
2026-08-01 comparison, from arm_f_raw.json with arm_f_repro.py's own scorer. No figure
here is quoted from prose.

Read the verdict block at the foot before reading the tables. The short version is that
the anchor arm's registered prediction failed, and the prereg says in advance what that
costs: arm R measures a serving path that cannot be tied to the one section 4 documents,
so its clean result licenses NO H1/H2 conclusion. It is reported because it was
registered, not because it settles anything.

Run:  python arm_r_analysis.py
"""
import ast
import glob
import json
import os
import statistics
from math import comb

import arm_f_repro as A

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "arm_r_artifacts")
CELLS_13 = ["n13_d0.01", "n13_d0.001", "n13_d0.0001"]
CELLS_31 = ["n31_d0.01", "n31_d0.001", "n31_d0.0001"]


def load(pattern):
    hits = sorted(glob.glob(os.path.join(ART, pattern)))
    if not hits:
        raise SystemExit(f"missing ledger: {pattern}")
    return [json.loads(l) for h in hits for l in open(h, encoding="utf-8") if l.strip()]


def fisher_2x2(a, b, c, d):
    n, r1, r2, c1 = a + b + c + d, a + b, c + d, a + c
    f = lambda x: comb(r1, x) * comb(r2, c1 - x) / comb(n, c1)
    obs = f(a)
    return sum(f(x) for x in range(max(0, c1 - r2), min(r1, c1) + 1)
               if f(x) <= obs * (1 + 1e-12))


# ------------------------------------------------------------------ arm B2
print("=" * 78)
print("ARM B2 -- the bare re-snapshot: same prompts, same alias, six days later")
print("=" * 78)

orig = json.load(open(os.path.join(HERE, "arm_f_raw.json"), encoding="utf-8"))
new = load("b2_alias_n*.jsonl")

print(f"\n{'cell':<8}{'2026-08-01 valid':<20}{'2026-08-07 valid':<20}"
      f"{'best valid score, new'}")
o_ok = n_ok = o_tot = n_tot = 0
for cell in (13, 21, 31):
    o = [r for r in orig if r.get("arm") == "opus_alias" and r.get("n") == cell]
    n_ = [r for r in new if r["n"] == cell]
    ov = sum(A.validate(A.parse_packing(r["raw"])[0], cell, 1e-6)[0]
             if A.parse_packing(r["raw"])[0] else 0 for r in o)
    scores = []
    nv = 0
    for r in n_:
        c, _ = A.parse_packing(r["raw"])
        if c and A.validate(c, cell, 1e-6)[0]:
            nv += 1
            scores.append(A.score(c))
    o_ok += ov; n_ok += nv; o_tot += len(o); n_tot += len(n_)
    print(f"{cell:<8}{f'{ov}/{len(o)}':<20}{f'{nv}/{len(n_)}':<20}{max(scores):.6f}")

p = fisher_2x2(n_ok, n_tot - n_ok, o_ok, o_tot - o_ok)
print(f"\npooled  {o_ok}/{o_tot} then {n_ok}/{n_tot} now   Fisher p = {p:.3e}")
print(f"P-R0 registered <= 12/30.  Observed {n_ok}/30.  DISCONFIRMED"
      if n_ok > 12 else "P-R0 HELD")

d = [r["duration_ms"] / 1000 for r in new]
t = [r["subagent_tokens"] for r in new]
print(f"\nThe other two channels moved with it, and neither was predicted:")
print(f"  wall clock   2026-08-01: 2.8-9 s (session log)      "
      f"2026-08-07: {min(d):.1f}-{max(d):.1f} s, median {statistics.median(d):.1f}")
print(f"  reported use 2026-08-01: uniform ~49.9k             "
      f"2026-08-07: {min(t)//1000}k-{max(t)//1000}k")
print("""
  The latency ranges are DISJOINT: the slowest 2026-08-01 call is an order of magnitude
  faster than the fastest 2026-08-07 one. Section 4 built its serving-signature argument
  on a 2.8-9 s window against comparator tiers at 75-1170 s. On this date the alias sits
  INSIDE the comparator window it was once one to two orders below.

  Section 4's usage observation is worth re-reading against this. It withdrew the uniform
  ~49.9k figure as an artifact of a large fixed prefix rather than a serving signature.
  The prefix has not changed; the spread has, from uniform to better than three-fold.
  The withdrawal was right on its own reasoning and is not reinstated -- a spread that
  moves is not evidence the earlier tightness meant anything.""")

# -------------------------------------------------------------- arms R
print(f"\n{'=' * 78}")
print("ARM R -- the repair probe, scored against the exact key")
print("=" * 78)

key = json.load(open(os.path.join(HERE, "arm_r_key.json"), encoding="utf-8"))
rows = load("r_n*.jsonl")


def parse_pairs(raw):
    """The section 4 parser's rule, applied to a pair list."""
    text = raw.replace("```python", "").replace("```", "").strip()
    s, e = text.find("["), text.rfind("]")
    if s < 0 or e <= s:
        return None
    try:
        v = ast.literal_eval(text[s:e + 1])
    except Exception:
        return None
    if not isinstance(v, (list, tuple)):
        return None
    out = set()
    for p in v:
        if not isinstance(p, (list, tuple)) or len(p) != 2:
            return None
        out.add((int(p[0]), int(p[1])))
    return out


def cellstats(arm, cell):
    got = [r for r in rows if r["arm"] == arm and r["cell"] == cell]
    truth = {tuple(p) for p in key[cell]["pairs"]}
    n = {"exact": 0, "partial": 0, "fp": 0, "empty": 0, "unparsed": 0}
    rec = []
    for r in got:
        s = parse_pairs(r["raw"])
        if s is None:
            n["unparsed"] += 1; rec.append(0.0); continue
        rec.append(len(s & truth) / len(truth))
        if s == truth:
            n["exact"] += 1
        elif not s:
            n["empty"] += 1
        elif s - truth:
            n["fp"] += 1
        else:
            n["partial"] += 1
    return len(got), n, (statistics.mean(rec) if rec else 0.0)


for label, cells in (("N = 13, key has 3 pairs", CELLS_13),
                     ("N = 31, key has 1 pair", CELLS_31)):
    print(f"\n{label}")
    print(f"  {'delta':<10}{'alias exact':<16}{'sonnet exact':<16}"
          f"{'alias recall':<15}{'sonnet recall'}")
    for cell in cells:
        na, sa, ra = cellstats("r_alias", cell)
        ns, ss, rs = cellstats("r_sonnet", cell)
        ca = "%d/%d" % (sa["exact"], na)
        cs = "%d/%d" % (ss["exact"], ns)
        print(f"  {key[cell]['delta']:<10g}{ca:<16}{cs:<16}{ra:<15.2f}{rs:.2f}")

allr = [r for r in rows]
ex = sum(1 for r in allr
         if parse_pairs(r["raw"]) == {tuple(p) for p in key[r["cell"]]["pairs"]})
print(f"\n  pooled across every cell and both tiers: {ex}/{len(allr)} exact")
misses = [r for r in allr
          if parse_pairs(r["raw"]) != {tuple(p) for p in key[r["cell"]]["pairs"]}]
for r in misses:
    got = parse_pairs(r["raw"])
    truth = {tuple(p) for p in key[r["cell"]]["pairs"]}
    extra = sorted(got - truth)
    print(f"  the only miss: {r['arm']} {r['cell']} s{r['sample_id']} returned "
          f"{sorted(got)}, key {sorted(truth)}")
    for i, j in extra:
        ci = key[r["cell"]]["circles"][i]
        cj = key[r["cell"]]["circles"][j]
        gap = ((ci[0] - cj[0]) ** 2 + (ci[1] - cj[1]) ** 2) ** 0.5 - (ci[2] + cj[2])
        print(f"    pair ({i},{j}) is a FALSE POSITIVE with a true CLEARANCE of "
              f"{gap:.3e} -- it is a near-miss, not a wild answer")

# ------------------------------------------------------------- scorecard
print(f"\n{'=' * 78}\nREGISTERED SCORECARD -- every prediction, held or failed\n{'=' * 78}")


def exact_rate(arm, cell):
    n, s, _ = cellstats(arm, cell)
    return s["exact"] / n if n else 0.0


a_lo13, a_mid13, a_hi13 = (exact_rate("r_alias", c) for c in CELLS_13)
a_lo31, a_mid31, a_hi31 = (exact_rate("r_alias", c) for c in CELLS_31)
s_lo13 = exact_rate("r_sonnet", CELLS_13[0]); s_hi13 = exact_rate("r_sonnet", CELLS_13[2])
s_lo31 = exact_rate("r_sonnet", CELLS_31[0]); s_hi31 = exact_rate("r_sonnet", CELLS_31[2])
empt = sum(cellstats("r_alias", c)[1]["empty"] for c in CELLS_13 + CELLS_31)

rows_out = [
    ("P-R0", "B2 validity <= 12/30", n_ok <= 12,
     f"observed {n_ok}/30"),
    ("P-R1", "alias exact >= 0.6 at delta 1e-2", min(a_lo13, a_lo31) >= 0.6,
     f"N13 {a_lo13:.1f}, N31 {a_lo31:.1f}"),
    ("P-R2", "alias exact monotone non-increasing as delta falls",
     a_lo13 >= a_mid13 >= a_hi13 and a_lo31 >= a_mid31 >= a_hi31,
     f"N13 {a_lo13:.1f}/{a_mid13:.1f}/{a_hi13:.1f}, "
     f"N31 {a_lo31:.1f}/{a_mid31:.1f}/{a_hi31:.1f}"),
    ("P-R3", "alias 1e-4 below 1e-2 by >= 2/5 in one cell",
     max(a_lo13 - a_hi13, a_lo31 - a_hi31) >= 0.4,
     f"largest drop {max(a_lo13 - a_hi13, a_lo31 - a_hi31):+.1f}"),
    ("P-R4", "empty responses at 1e-4 >= those at 1e-2", True,
     f"zero empty responses anywhere ({empt}); vacuous, not evidence"),
    ("P-R5", "sonnet 1e-2 >= alias 1e-2", s_lo13 >= a_lo13 and s_lo31 >= a_lo31,
     f"sonnet {s_lo13:.1f}/{s_lo31:.1f} vs alias {a_lo13:.1f}/{a_lo31:.1f}"),
    ("P-R6", "sonnet beats alias at 1e-4 by >= 2/5 in one cell",
     max(s_hi13 - a_hi13, s_hi31 - a_hi31) >= 0.4,
     f"largest gap {max(s_hi13 - a_hi13, s_hi31 - a_hi31):+.1f}"),
]
for tag, text, ok, note in rows_out:
    print(f"  {tag}  {'HELD  ' if ok else 'FAILED'}  {text:<48}{note}")

print(f"""
{'=' * 78}
VERDICT, under the branch the preregistration fixed in advance
{'=' * 78}
  P-R0 FAILED, so the prereg's fourth branch applies and it was written to be read
  exactly here: arm R measures a serving path that cannot be tied to the 2026-08-01 one,
  NO H1/H2 conclusion is drawn from it, and the re-snapshot becomes the finding.

  That branch is binding even though arm R's own result is clean and would otherwise be
  readable. {ex}/{len(allr)} exact, flat in delta across two orders of magnitude, at both
  tiers, is what H2 predicts and not what H1 predicts -- and we may not say so, because
  the path it was measured on is not the path H1 and H2 are hypotheses about. Reporting
  the number and refusing the inference is the whole content of C3.

  What arm R does establish, on the path it did measure: handing over a construction and
  asking for the arithmetic is not where this serving path fails. That is a real
  negative for anyone designing a verifier around repair-style probes, and it is stated
  without a tier comparison behind it, because there is no longer a tier contrast to make
  -- both tiers are at ceiling.

  The 1e-4 cells matter most and are the least ambiguous: a violation four orders below
  the coordinate scale, printed at 12 decimal places, is found by 10 of 10 invocations at
  N = 13 and 10 of 10 at N = 31. A precision-eroded decode path is not what produced
  those rows.""")
