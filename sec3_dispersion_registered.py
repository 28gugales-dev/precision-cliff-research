"""
Report the fixed-parent dispersion probe against its OWN preregistration, and
against its registered v2 replication -- rather than reporting only the legacy
echo measure.

Registered measures (agent-run/dispersion_probe/analysis_prereg.md, Amendment 1):
  - centers-only echo: max index-wise center displacement < 1e-3, radii ignored
  - graded companion (the registration's PRIMARY echo measure): median
    per-circle center displacement per sample
  - legacy 1e-5 three-field coordinate_echo, retained by the registration
    explicitly so "the comparison against the 14B score-inferred echo rate
    remains possible" -- this is the `echo` field and the one the paper quotes

v2 (analysis_prereg_v2.md + addendum) is a confirmatory replication on
out-of-sample salted seeds. Its rows live under the Kaggle output tree.

Run:  python sec3_dispersion_registered.py
"""
import json, glob, os, statistics, collections

HERE = os.path.dirname(os.path.abspath(__file__))
V1 = os.path.join(HERE, "..", "agent-run", "dispersion_probe", "probe_samples.jsonl")
V2 = os.path.join(HERE, "..", "..", "handoff", "kaggle", "output",
                  "precision-cliff-fixed-parent-dispersion-probe-v2", "**",
                  "probe_samples.jsonl")
RUNGS = ["q4_k_m", "q3_k_m", "q2_k"]

def load(p):
    hits = glob.glob(p, recursive=True)
    if not hits:
        return None
    return [json.loads(l) for l in open(hits[0], encoding="utf-8") if l.strip()]

def parents_of(rows):
    """Map parent_id -> the circle set every sample at that parent was shown.
    The probe holds the parent fixed, so any echo row recovers it exactly."""
    out = {}
    for r in rows:
        pid = r.get("parent_id")
        if pid not in out and r.get("echo") and r.get("circles"):
            out[pid] = [[float(c[0]), float(c[1])] for c in r["circles"]]
    return out

def centers_metrics(r, parent):
    """(max displacement, median displacement) index-wise, radii ignored."""
    cs = r.get("circles")
    if not cs or not parent or len(cs) != len(parent):
        return None, None
    d = [((float(a[0]) - b[0]) ** 2 + (float(a[1]) - b[1]) ** 2) ** 0.5
         for a, b in zip(cs, parent)]
    return max(d), statistics.median(d)

def report(rows, label):
    print(f"\n{'='*66}\n{label}: {len(rows)} rows\n{'='*66}")
    pmap = parents_of(rows)
    print(f"parents recovered from echo rows: {len(pmap)}")

    legacy = collections.defaultdict(lambda: [0, 0])
    centers = collections.defaultdict(lambda: [0, 0])
    graded = collections.defaultdict(list)
    bins = collections.defaultdict(set)
    scores = collections.defaultdict(list)

    for r in rows:
        if not r.get("valid"):
            continue
        q = r["rung"]
        legacy[q][1] += 1
        if r.get("echo"):
            legacy[q][0] += 1
        scores[q].append(r.get("score") or 0.0)
        bb = r.get("behaviour_bin")
        bins[q].add(tuple(bb) if isinstance(bb, list) else bb)
        mx, md = centers_metrics(r, pmap.get(r.get("parent_id")))
        if mx is not None:
            centers[q][1] += 1
            if mx < 1e-3:
                centers[q][0] += 1
            graded[q].append(md)

    print(f"\n{'rung':<10}{'legacy echo (1e-5)':<22}{'centers echo (<1e-3)':<24}"
          f"{'median ctr displ':<20}{'uniq bins':<11}{'mean score'}")
    for q in RUNGS:
        if not legacy[q][1]:
            continue
        le, lv = legacy[q]
        ce, cv = centers[q]
        g = statistics.median(graded[q]) if graded[q] else float("nan")
        ms = statistics.mean(scores[q]) if scores[q] else float("nan")
        print(f"{q:<10}{f'{le}/{lv} ({100*le/lv:.0f}%)':<22}"
              f"{f'{ce}/{cv} ({100*ce/cv:.0f}%)' if cv else 'n/a':<24}"
              f"{g:<20.6f}{len(bins[q]):<11}{ms:.4f}")

    # The decomposition that locates the cliff: among valid rows, split by
    # whether centres were copied and, if so, whether radii were varied.
    # "centres copied + radii varied" is the proposer's entire realised search.
    print(f"\n{'rung':<10}{'centres+radii varied':<24}{'centres+radii copied':<24}"
          f"{'centres varied'}")
    for q in RUNGS:
        cc = cr = cv2 = 0
        for r in rows:
            if not r.get("valid") or r["rung"] != q:
                continue
            mx, _ = centers_metrics(r, pmap.get(r.get("parent_id")))
            if mx is None:
                continue
            if mx < 1e-3:
                if r.get("echo"):
                    cr += 1
                else:
                    cc += 1
            else:
                cv2 += 1
        t = cc + cr + cv2
        if t:
            print(f"{q:<10}{f'{cc}/{t} ({100*cc/t:.0f}%)':<24}"
                  f"{f'{cr}/{t} ({100*cr/t:.0f}%)':<24}{cv2}/{t}")

    # Registered quality fork: mean score must be FLAT for the mechanism claim.
    print("\nregistered quality fork (mean score among valid must not decline"
          " monotonically):")
    ms = [statistics.mean(scores[q]) for q in RUNGS if scores[q]]
    mono = all(ms[i] > ms[i + 1] for i in range(len(ms) - 1))
    print(f"   means in rung order {RUNGS}: "
          f"{[round(x,4) for x in ms]}  -> monotone decline: {mono}")

    # Rarefaction-matched unique behaviour cells at matched n.
    m = min(len(scores[q]) for q in RUNGS if scores[q])
    print(f"\nrarefaction depth m = {m} (min valid rows across rungs)")
    if m < 8:
        print("   registered power floor: m < 8 -> verdict UNDERPOWERED,"
              " no directional claim")
    return {q: (legacy[q][0], legacy[q][1]) for q in RUNGS}

v1 = load(V1)
a = report(v1, "v1 fixed-parent dispersion probe")

v2 = load(V2)
if v2 is None:
    print("\nv2 replication ledger not found")
else:
    b = report(v2, "v2 confirmatory replication (out-of-sample salted seeds)")
    print(f"\n{'='*66}\nREPLICATION: legacy echo, v1 vs v2\n{'='*66}")
    for q in RUNGS:
        e1, v1n = a[q]
        e2, v2n = b[q]
        p1 = f"{100*e1/v1n:.0f}%" if v1n else "n/a"
        p2 = f"{100*e2/v2n:.0f}%" if v2n else "n/a"
        print(f"   {q:<10} v1 {e1}/{v1n} ({p1})   v2 {e2}/{v2n} ({p2})")
