#!/usr/bin/env python3
"""Wave 5 registered analysis — no arguments, replays everything from the raw ledger.

Registration: wave5_prereg_labs.md (SHA-256 a1336cfd4542634d96d7adb71d76518dd24917fd
76a311a271770548cfe45ac1), runner SHA-256 d1739f6cf38cc295bf2c0260c5a801c8f134a0e9fd
c041747fff2a7b73616e7c, pushed as a PUBLIC Kaggle kernel before any row was sampled.

Every verdict label is computed and printed here, not written by us (prereg SS7).

Everything is EXACT: the alphabet is +-1, energies are integers, acceptance is an
integer comparison, and echo is plain list equality against the running parent — the
task was chosen precisely so that no rounding convention exists for a referee to
question. Scores (merit factors) are recomputed from recomputed integer energies, so
the ledger's 12-dp `score` field is never load-bearing here.
"""
import json, os
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "wave5_output", "precision_sweep_14b_labs")
LEDGER = os.path.join(OUT, "candidates_precision_14b_labs.jsonl")
STATE_DIR = os.path.join(OUT, "state")

N = 32
SEED_ENERGY = 156

def autocorrelations(s):
    return [sum(s[i] * s[i + k] for i in range(len(s) - k))
            for k in range(1, len(s))]

def energy(s):
    return sum(c * c for c in autocorrelations(s))

def merit_factor(e):
    return (N * N) / (2 * e)

def is_template(s):
    if all(v == s[0] for v in s):
        return True
    return all(s[i] != s[i - 1] for i in range(1, len(s)))

def symmetry_orbit(s):
    orbit = set()
    for base in (tuple(s), tuple(reversed(s))):
        for neg in (1, -1):
            for mod in (0, 1):
                orbit.add(tuple(neg * base[i] * ((-1) ** (i * mod))
                                for i in range(len(s))))
    return orbit

# seed parent extracted from the pushed runner, not retyped
import re, ast
RUNNER = os.path.join(HERE, "sec3_artifacts", "runners",
                      "kaggle_precision_sweep_14b_labs.py")
src = open(RUNNER, encoding="utf-8").read()
SEED_PARENT = list(ast.literal_eval(
    re.search(r"SEED_PARENT = (\[.*?\])", src, re.S).group(1)))
assert len(SEED_PARENT) == N and energy(SEED_PARENT) == SEED_ENERGY

rows = [json.loads(l) for l in open(LEDGER, encoding="utf-8") if l.strip()]
print(f"ledger rows: {len(rows)}")

per = {}
for r in rows:
    per.setdefault((r["quant"], r["seed"]), []).append(r)

mismatch_echo = mismatch_energy = 0
lineage_stats = {}
for (quant, seed), rs in per.items():
    rs.sort(key=lambda r: r["gen"])
    parent, pe = list(SEED_PARENT), SEED_ENERGY
    accepted = echo = valid = tpl = sym = dep = dep_improve = 0
    for r in rs:
        if not r["valid"]:
            continue
        valid += 1
        seq = list(r["sequence"])
        e = energy(seq)
        if e != r["energy"]:
            mismatch_energy += 1
        is_echo = seq == parent
        if is_echo != r["echo"]:
            mismatch_echo += 1
        if is_echo:
            echo += 1
        else:
            dep += 1
            if e < pe:
                dep_improve += 1
            if tuple(seq) in symmetry_orbit(parent):
                sym += 1
        if is_template(seq):
            tpl += 1
        if e < pe:                    # exact integer acceptance, no epsilon
            parent, pe = seq, e
            accepted += 1
    st = json.load(open(os.path.join(STATE_DIR, f"{quant}_seed_{seed}.json")))
    lineage_stats[(quant, seed)] = {
        "accepted": accepted, "echo": echo, "valid": valid, "template": tpl,
        "sym_variant": sym, "departures": dep, "dep_improve": dep_improve,
        "best_energy": pe, "state_agrees": st["best_energy"] == pe}

bad = [k for k, v in lineage_stats.items() if not v["state_agrees"]]
print(f"echo replay: {'CLEAN' if mismatch_echo == 0 else f'{mismatch_echo} mismatches'}")
print(f"energy replay: {'CLEAN' if mismatch_energy == 0 else f'{mismatch_energy} mismatches'}")
print(f"state-file agreement: {len(lineage_stats)-len(bad)}/{len(lineage_stats)}"
      + (f"  DISAGREE: {bad}" if bad else ""))

def pool(quant):
    ls = [v for (q, s), v in lineage_stats.items() if q == quant]
    return {"lineages": len(ls),
            "valid": sum(l["valid"] for l in ls),
            "echo": sum(l["echo"] for l in ls),
            "template": sum(l["template"] for l in ls),
            "sym": sum(l["sym_variant"] for l in ls),
            "dep": sum(l["departures"] for l in ls),
            "dep_improve": sum(l["dep_improve"] for l in ls),
            "mean_accepted": sum(l["accepted"] for l in ls) / len(ls)}

q4, q2 = pool("q4_k_m"), pool("q2_k")
for name, p in (("q4_k_m", q4), ("q2_k", q2)):
    print(f"\n{name}: lineages {p['lineages']}, valid {p['valid']}, "
          f"echo {p['echo']}/{p['valid']} = {p['echo']/p['valid']:.1%}, "
          f"template {p['template']}/{p['valid']}, "
          f"symmetry-variant {p['sym']}/{p['dep']} of departures, "
          f"departures improving {p['dep_improve']}/{p['dep']}, "
          f"mean accepted {p['mean_accepted']:.3f}")

print("\n=== CONTROL-ARM FLOOR (SS5.1): mean accepted at Q4_K_M >= 1.0 required ===")
floor_met = q4["mean_accepted"] >= 1.0
if not floor_met:
    print(f"  TRIGGERED — mean accepted {q4['mean_accepted']:.3f} < 1.0.")
    print("  Registered consequence: verdict UNINFORMATIVE, no branch of 5.7 claimed,")
    print("  echo comparison reported as DESCRIPTIVE ONLY, whatever the Q2_K figure.")
else:
    print(f"  met ({q4['mean_accepted']:.3f})")

e2, e4 = q2["echo"] / q2["valid"], q4["echo"] / q4["valid"]
print("\n=== 5.1 PRIMARY echo (>=50% Q2_K, <=30% Q4_K_M) ===")
print(f"  observed Q2_K {q2['echo']}/{q2['valid']} = {e2:.1%}, "
      f"Q4_K_M {q4['echo']}/{q4['valid']} = {e4:.1%}"
      f" -> {'DESCRIPTIVE ONLY (floor)' if not floor_met else 'evaluable'}")
if not floor_met:
    print("  descriptive note, unclaimable: the rates REVERSE — the 2-bit rung echoes")
    print("  LESS than the reference rung on this task. No branch interprets this.")

print("\n=== 5.2 DESCRIPTIVE accepted steps (no bound registered) ===")
print(f"  Q2_K {q2['mean_accepted']:.3f}, Q4_K_M {q4['mean_accepted']:.3f}; "
      "permutation tail degenerate (all lineage values 0)"
      if q2["mean_accepted"] == q4["mean_accepted"] == 0 else
      f"  Q2_K {q2['mean_accepted']:.3f}, Q4_K_M {q4['mean_accepted']:.3f}")

print("\n=== 5.3 SECONDARY conditional-on-departure improvement ===")
print(f"  Q2_K departures {q2['dep']} (improving {q2['dep_improve']}), "
      f"Q4_K_M departures {q4['dep']} (improving {q4['dep_improve']})")
print(f"  -> {'UNINFORMATIVE (control floor)' if not floor_met else ('UNDERPOWERED' if q2['dep'] < 25 else 'evaluable')}")

print("\n=== 5.4 Template check (no bound) ===")
print(f"  Q2_K {q2['template']}/{q2['valid']} = {q2['template']/q2['valid']:.1%}; "
      f"Q4_K_M {q4['template']}/{q4['valid']} = {q4['template']/q4['valid']:.1%}")

print("\n=== 5.5 Symmetry-variant rate among departures (no bound) ===")
print(f"  Q2_K {q2['sym']}/{q2['dep']}; Q4_K_M {q4['sym']}/{q4['dep']}")

print("\n=== 5.6 Outcome (final best per lineage, no bound) ===")
bests = sorted(set(v["best_energy"] for v in lineage_stats.values()))
if bests == [SEED_ENERGY]:
    print(f"  every lineage in both rungs finished at the seed energy {SEED_ENERGY};")
    print("  permutation test degenerate (all values identical), reported as such")
else:
    print(f"  distinct final best energies: {bests}")

print("\n=== 5.7 THREE-BRANCH RULE ===")
if not floor_met:
    print("  Control floor not met -> BRANCH C (INCONCLUSIVE) by the registered rule:")
    print("  'This includes every case where the control floor is not met.' No scope")
    print("  change in either direction; the wave is reported with its numbers.")
else:
    a = e2 >= 0.50 and e4 <= 0.30
    b = e4 <= 0.35 and e2 < 0.50 and (e2 - e4) < 0.15
    print(f"  BRANCH {'A - GENERALISES' if a else ('B - NARROWS' if b else 'C - INCONCLUSIVE')}")

# descriptive Fisher on the reversed echo contrast, unregistered
def fisher_two_sided(a, b, c, d):
    n = a + b + c + d; r1 = a + b; c1 = a + c
    def p(x): return comb(r1, x) * comb(n - r1, c1 - x) / comb(n, c1)
    p0 = p(a)
    return sum(p(x) for x in range(max(0, c1 - (n - r1)), min(r1, c1) + 1)
               if p(x) <= p0 + 1e-12)
fp = fisher_two_sided(q2["echo"], q2["valid"] - q2["echo"],
                      q4["echo"], q4["valid"] - q4["echo"])
print(f"\ndescriptive Fisher (unregistered), Q2_K vs Q4_K_M echo: p = {fp:.2e}")

prov = json.load(open(os.path.join(OUT, "provenance.json")))
print(f"gpu_crossing: {prov.get('gpu_crossing')} (single P100 — the registered "
      "hardware crossing did not run; recorded per row and in provenance)")
