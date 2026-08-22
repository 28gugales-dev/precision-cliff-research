import json, ast, math, re, collections

ROOT = r"~\AppData\Local\hermes\research-corpus\precision-cliff"
rows = json.load(open(ROOT + r"\arm_f_raw.json", encoding="utf-8"))
CELLS = (13, 21, 31)

def parse(t):
    if not t: return None
    m = re.search(r"\[\s*[\[(].*[\])]\s*\]", t, re.S)
    for cand in ([m.group(0)] if m else []) + [t.strip()]:
        try:
            v = ast.literal_eval(cand)
            if isinstance(v, list): return v
        except Exception:
            pass
    return None

def score(cs, n, tol):
    """returns (valid, reason)"""
    if not isinstance(cs, list) or len(cs) != n:
        return False, "count/parse"
    try:
        c = [[float(a), float(b), float(r)] for a, b, r in cs]
    except Exception:
        return False, "count/parse"
    if any(r <= 0 for _, _, r in c):
        return False, "nonpositive_radius"
    for x, y, r in c:
        if x - r < -tol or x + r > 1 + tol or y - r < -tol or y + r > 1 + tol:
            return False, "out_of_bounds"
    for i in range(len(c)):
        for j in range(i + 1, len(c)):
            x1, y1, r1 = c[i]; x2, y2, r2 = c[j]
            if math.hypot(x1 - x2, y1 - y2) < r1 + r2 - tol:
                return False, "overlap"
    return True, "valid"

def overlaps_ignoring_zero(cs, n, tol):
    """does it overlap once zero-radius circles are removed?"""
    try:
        c = [[float(a), float(b), float(r)] for a, b, r in cs if float(r) > 0]
    except Exception:
        return None
    for i in range(len(c)):
        for j in range(i + 1, len(c)):
            x1, y1, r1 = c[i]; x2, y2, r2 = c[j]
            if math.hypot(x1 - x2, y1 - y2) < r1 + r2 - tol:
                return True
    return False

print("=== VALIDITY BY ARM (cells 13/21/31) ===")
for arm in ("opus_alias", "sonnet_bare", "bare"):
    for tol, lab in ((1e-6, "1e-6"), (1e-9, "1e-9")):
        sub = [r for r in rows if r["arm"] == arm and r["n"] in CELLS]
        ok = sum(1 for r in sub if score(parse(r["raw"]), r["n"], tol)[0])
        per = {n: sum(1 for r in sub if r["n"] == n and score(parse(r["raw"]), r["n"], tol)[0])
               for n in CELLS}
        print(f"  {arm:<12} {lab}: {ok}/{len(sub)}   per cell {per}")

print()
print("=== opus_alias INVALID ROW ANATOMY (1e-6) ===")
sub = [r for r in rows if r["arm"] == "opus_alias"]
inval = []
for r in sub:
    cs = parse(r["raw"])
    v, why = score(cs, r["n"], 1e-6)
    if not v: inval.append((r, cs, why))
print(f"  invalid: {len(inval)}/30")
print("  first-gate reasons:", dict(collections.Counter(w for _, _, w in inval)))
ovl = sum(1 for _, cs, _ in inval if overlaps_ignoring_zero(cs, 0, 1e-6) is True)
print(f"  overlap once zero-radius removed: {ovl}/{len(inval)}  <- paper claims ALL 26 overlap")
nz = [(r["n"], r["sample_id"], sum(1 for c in cs if float(c[2]) == 0))
      for r, cs, w in inval if w == "nonpositive_radius"]
print("  rows with zero-radius circles:", nz, "<- paper: 2 rows, one has 12 of 21 radii at zero")

print()
print("=== opus_alias VALID SAMPLE SCORES ===")
for r in sub:
    cs = parse(r["raw"])
    if score(cs, r["n"], 1e-6)[0]:
        print(f"  N={r['n']} sample={r['sample_id']}  sum_r={sum(float(c[2]) for c in cs):.4f}")

print()
print("=== N=13 corner radii == 0.25 in all ten rows? ===")
cnt = 0
for r in [x for x in sub if x["n"] == 13]:
    cs = parse(r["raw"])
    if cs and sum(1 for c in cs if abs(float(c[2]) - 0.25) < 1e-9) >= 4: cnt += 1
print(f"  rows with >=4 circles of radius exactly 0.25: {cnt}/10")
