# Arm V scorer. Reuses arm_f_repro.py's parse/validate/classify verbatim -
# no new instrument, no new tolerance. Applies the registered rules of
# arm_v_preregistration.md (git 5444f10) and prints per-model verdicts.
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arm_f_repro as A

# Failure-mode strings carry non-ASCII glyphs; a cp1252 console (Windows default)
# otherwise raises UnicodeEncodeError after the ledger has already been written.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "arm_v_candidates_raw.jsonl"
OUT = ROOT / "arm_v_scored.jsonl"

FLOOR = 10          # valid rows (of 25) a model needs before any claim
V1_THRESHOLD = 0.5  # anchoring-transfer branch point
V2_THRESHOLD = 0.1  # rival-argmax ceiling, discriminating Ns only
DISCRIMINATING = {13, 31}


def main():
    rows = [json.loads(l) for l in RAW.read_text(encoding="utf-8").splitlines() if l.strip()]
    scored = []
    for r in rows:
        circles, parse_err = A.parse_packing(r.get("raw_output"))
        row = dict(r)
        row["parse_error"] = parse_err
        row["valid"] = False
        row["invalid_reason"] = None
        if circles is not None:
            strict_ok, strict_why = A.validate(circles, r["n"], tol=1e-9)
            ok, why = A.validate(circles, r["n"], tol=1e-6)
            row["valid"] = ok
            row["invalid_reason"] = why
            row["valid_strict_1e9"] = strict_ok
            row["circles"] = circles
            if ok:
                row.update(A.classify(circles, r["n"]))
        scored.append(row)

    with OUT.open("w", encoding="utf-8") as fh:
        for r in scored:
            fh.write(json.dumps(r) + "\n")

    models = sorted({r["proposer_alias"] for r in scored})
    print(f"{len(scored)} invocations scored; ledger {OUT.name}\n")
    for m in models:
        sub = [r for r in scored if r["proposer_alias"] == m]
        valid = [r for r in sub if r["valid"]]
        print(f"=== {m}  ({len(valid)}/{len(sub)} valid at 1e-6) ===")
        floor_ok = len(valid) >= FLOOR
        if not floor_ok:
            print(f"  BELOW-FLOOR (<{FLOOR} valid): no anchoring claim either direction\n")
        on_pred = rival_hits = disc_valid = 0
        for r in valid:
            pred = A.PREDICTIONS[r["n"]]
            hit = abs(r["sum_of_radii"] - pred["value"]) < 2e-3
            on_pred += hit
            if r["n"] in DISCRIMINATING:
                disc_valid += 1
                if (abs(r["sum_of_radii"] - pred["rival_argmax"]) < 2e-3
                        and abs(pred["rival_argmax"] - pred["value"]) > 1e-9):
                    rival_hits += 1
        for n in A.TARGET_N if hasattr(A, "TARGET_N") else sorted({r["n"] for r in sub}):
            nn = [r for r in sub if r["n"] == n]
            nv = [r for r in nn if r["valid"]]
            if not nn:
                continue
            pred = A.PREDICTIONS[n]
            hits = sum(abs(r["sum_of_radii"] - pred["value"]) < 2e-3 for r in nv)
            best = max((r["sum_of_radii"] for r in nv), default=None)
            fails = {}
            for r in nn:
                if not r["valid"]:
                    k = r["call_error"] or r["parse_error"] or r["invalid_reason"]
                    fails[str(k)[:40]] = fails.get(str(k)[:40], 0) + 1
            print(f"  N={n:>2} valid {len(nv)}/{len(nn)}  on-pred {hits}"
                  f"  best {None if best is None else round(best, 7)}"
                  + (f"  fails {fails}" if fails else ""))
        if floor_ok and valid:
            rate = on_pred / len(valid)
            v1 = "TRANSFERS" if rate >= V1_THRESHOLD else "DOES-NOT-TRANSFER"
            print(f"  V1 anchoring: {on_pred}/{len(valid)} = {rate:.0%} -> {v1}")
            if disc_valid:
                rr = rival_hits / disc_valid
                v2 = "HOLDS" if rr <= V2_THRESHOLD else "FAILS"
                print(f"  V2 rival-argmax (N in {sorted(DISCRIMINATING)}):"
                      f" {rival_hits}/{disc_valid} = {rr:.0%} -> {v2}")
            else:
                print("  V2: no valid rows on discriminating Ns -> UNSCORABLE")
        print()


if __name__ == "__main__":
    main()
