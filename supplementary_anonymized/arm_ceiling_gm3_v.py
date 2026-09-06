"""Per-arm best valid sum vs family argmax for arms GM3 and V.
Run from precision-cliff root. Uses arm_f_repro scoring (same as the frozen reports)."""
import json, math, sys
from collections import defaultdict
sys.path.insert(0, ".")
from arm_f_repro import parse_packing, validate, score

R2 = math.sqrt(2.0) - 1.0


def family_argmax(N):
    """Closed form, identical to arm_mu_ceiling.py: k-grid of radius 1/(2k) plus up to
    (k-1)^2 fillers of radius (sqrt2-1)/(2k); truncated grid N/(2k) when k^2 > N."""
    best = 0.0
    for k in range(1, N + 1):
        if k * k > N:
            v = N / (2.0 * k)
        else:
            m = min(N - k * k, (k - 1) ** 2)
            v = k / 2.0 + m * R2 / (2.0 * k)
        best = max(best, v)
    return best


ARGMAX = {n: family_argmax(n) for n in (13, 17, 21, 31, 35, 37, 43)}
for n in sorted(ARGMAX):
    print(f"argmax N={n}: {ARGMAX[n]:.10f}")


def extract_text(resp):
    if "candidates" in resp:
        try:
            for p in resp["candidates"][0]["content"]["parts"]:
                if not p.get("thought") and p.get("text"):
                    return p["text"]
            return ""
        except (KeyError, IndexError, TypeError):
            return ""
    if "choices" in resp:
        try:
            return resp["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError, TypeError):
            return ""
    return ""


def report(name, per_cell):
    print("==", name)
    tot6 = tot9 = clr6 = clr9 = 0
    for n in sorted(per_cell):
        v6 = [s for s, ok9 in per_cell[n]]
        v9 = [s for s, ok9 in per_cell[n] if ok9]
        tot6 += len(v6); tot9 += len(v9)
        c6 = sum(1 for s in v6 if s - ARGMAX[n] > 1e-6)
        c9 = sum(1 for s in v9 if s - ARGMAX[n] > 1e-9)
        clr6 += c6; clr9 += c9
        b6 = max(v6) if v6 else None
        print(f"  N={n:2d} valid6={len(v6):2d} valid9={len(v9):2d} best={b6} "
              f"argmax={ARGMAX[n]:.7f} gap={(b6 - ARGMAX[n]) if b6 is not None else None} "
              f"clear6={c6} clear9={c9}")
    print(f"  TOTAL valid6={tot6} valid9={tot9} clear6={clr6} clear9={clr9}")


# ---- GM3 ----
rows_by = {}
for line in open("arm_gm_gm3_checkpoint.jsonl", encoding="utf-8"):
    if not line.strip():
        continue
    r = json.loads(line)
    if "transport_error" in r["response"]:
        continue
    key = (r["n"], r["sample_idx"])
    rows_by.setdefault(key, r)
gm = defaultdict(list)
for r in rows_by.values():
    n = int(r["n"])
    circles, _ = parse_packing(extract_text(r["response"]) or None)
    if circles is None:
        continue
    try:
        ok = all(c is not None and len(c) == 3 and all(isinstance(v, (int, float)) for v in c)
                 for c in circles)
    except TypeError:
        ok = False
    if not ok:
        continue
    if validate(circles, n, tol=1e-6)[0]:
        gm[n].append((score(circles), validate(circles, n, tol=1e-9)[0]))
report("GM3", gm)

# ---- V ----
byalias = defaultdict(lambda: defaultdict(list))
for line in open("arm_v_scored.jsonl", encoding="utf-8"):
    if not line.strip():
        continue
    r = json.loads(line)
    if str(r.get("valid")) != "True":
        continue
    n = int(r["n"])
    s = float(r["sum_of_radii"])
    ok9 = str(r.get("valid_strict_1e9")) == "True"
    byalias[r["proposer_alias"]][n].append((s, ok9))
allv = defaultdict(list)
for a, pc in byalias.items():
    report("V " + a, pc)
    for n, lst in pc.items():
        allv[n].extend(lst)
report("V ALL ALIASES", allv)
