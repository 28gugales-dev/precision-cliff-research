"""Evidence gate: every residual/clearance claim in paper/*.tex must (a) still be present as
the exact sentence fragment recorded in loop/r27_evidence.json and (b) agree with the ledger
field that fragment cites. Ints match exactly; floats to a relative tolerance (paper prints
are rounded); a string expected value is a substring the source file must contain.

Usage: python -X utf8 loop/evidence_gate.py            (from paper2-transfer root)
Exit 1 on any missing fragment, unreadable ledger, bad path or value mismatch.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "loop" / "r27_evidence.json"
REL_TOL = 0.05
# Inside the anonymized bundle this file sits at paper_repo/loop/, the corpus
# ledgers at the bundle root and paper-1 evidence under paper_repo/evidence/.
_UP = ROOT.parent
CORPUS = _UP if (_UP / "arm_f_repro.py").is_file() else _UP / "precision-cliff"


def resolve(rel):
    for p in ((ROOT / rel).resolve(), CORPUS / Path(rel).name,
              ROOT / "evidence" / Path(rel).name):
        if p.exists():
            return p
    return (ROOT / rel).resolve()


def walk(obj, path):
    for key in path:
        obj = obj[key]
    return obj


def main():
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    sources = {}
    for name, rel in spec["sources"].items():
        p = resolve(rel)
        if not p.exists():
            print(f"MISSING SOURCE {name}: {p}")
            return 1
        raw = p.read_text(encoding="utf-8")
        sources[name] = json.loads(raw) if p.suffix == ".json" else raw

    tex_cache = {}
    fails = []
    n_checks = 0
    for e in spec["entries"]:
        f = e["file"]
        if f not in tex_cache:
            tex_cache[f] = (ROOT / "paper" / f).read_text(encoding="utf-8")
        if e["substring"] not in tex_cache[f]:
            fails.append(f"{f}: fragment missing: {e['substring'][:70]!r}")
            continue
        for src, path, expected in e["checks"]:
            n_checks += 1
            data = sources[src]
            if isinstance(expected, str):
                if expected not in data:
                    fails.append(f"{f}: {src} lacks text {expected!r}")
                continue
            try:
                got = walk(data, path)
            except (KeyError, IndexError, TypeError) as exc:
                fails.append(f"{f}: {src}{path} unreadable ({exc!r})")
                continue
            if isinstance(expected, int) and not isinstance(expected, bool):
                ok = got == expected
            else:
                ok = abs(got - expected) <= REL_TOL * abs(expected)
            if not ok:
                fails.append(f"{f}: {src}{path} = {got!r}, paper says {expected!r}  "
                             f"<- {e['substring'][:60]!r}")

    print(f"entries {len(spec['entries'])}  checks {n_checks}  failures {len(fails)}")
    for line in fails:
        print("  " + line)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
