# Round 14 bookkeeping over arm CL's stored programs, no new invocations, disclosed as post hoc.
# (a) Item 4 of the round-13c outside review: the 1e-9 status of the two Sonnet-tier valid
#     programs that do not clear (the text says "not separately reported").
# (b) Item 2: what the 22 weak-tier stdout_parse_fail programs actually print. The registered
#     parser takes the outermost [...] and literal_evals it; a program that prints a packing in
#     another layout is binned as a parse failure. This script re-executes every row through the
#     registered scorer (arm_cl_analysis.py, unmodified, 120 s) and stores the raw stdout of the
#     parse failures so a lenient reading can be attempted and reported beside the registered one.
# Programs may call numpy.random unseeded, so the re-execution is checked against the frozen
# bins per cell and any drift is recorded, not hidden.
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = Path(r"~\AppData\Local\hermes\research-corpus\precision-cliff")
sys.path.insert(0, str(CORPUS))
import arm_cl_analysis as cl  # noqa: E402

rows = cl.load_rows(CORPUS / "arm_cl_collect.jsonl")
assert len(rows) == 90
frozen = json.load(open(CORPUS / "arm_cl_report.json", encoding="utf-8"))["tiers"]

out = {"rows": [], "drift": {}}
from concurrent.futures import ThreadPoolExecutor


def one(r):
    source = cl.strip_fences(r["raw"]) if r["raw"] else ""
    rec = dict(tier=r["tier"], n=r["n"], sample_id=r["sample_id"])
    if not source.strip():
        rec["bin"] = "no_program"; return rec
    ok, gate_bin = cl.ast_gate(source)
    if not ok:
        rec["bin"] = gate_bin; return rec
    err_bin, stdout = cl.run_program(source, 120)
    if err_bin:
        rec["bin"] = err_bin; rec["stdout"] = stdout[-2000:]; return rec
    packing, perr = cl.parse_packing(stdout)
    if packing is None:
        rec["bin"] = "stdout_parse_fail"; rec["why"] = perr; rec["stdout"] = stdout[:6000]
        rec["seeded"] = ("seed" in source)
        return rec
    ok6, why6 = cl.validate(packing, r["n"], tol=1e-6)
    ok9, why9 = cl.validate(packing, r["n"], tol=1e-9)
    rec.update(valid_1e6=ok6, valid_1e9=ok9, why6=why6, why9=why9, seeded=("seed" in source))
    if not ok6:
        rec["bin"] = "geom_invalid"; return rec
    s = cl.score(packing)
    rec["bin"] = "valid"; rec["sum"] = round(s, 9); rec["argmax"] = round(cl.ARGMAX[r["n"]], 9)
    rec["cleared"] = bool(ok9 and s > cl.ARGMAX[r["n"]] + cl.WINDOW_9)
    return rec


with ThreadPoolExecutor(max_workers=4) as ex:
    out["rows"] = list(ex.map(one, rows))

for tier in ("weak", "sonnet"):
    for n in (13, 21, 31):
        got = Counter(x["bin"] for x in out["rows"] if x["tier"] == tier and x["n"] == n)
        want = frozen[tier]["cells"][str(n)]["bins"]
        out["drift"][f"{tier}/{n}"] = dict(frozen=want, recount=dict(got), same=(dict(got) == want))
        print(tier, n, "same" if dict(got) == want else f"DRIFT frozen={want} recount={dict(got)}")

son_valid = [x for x in out["rows"] if x["tier"] == "sonnet" and x["bin"] == "valid"]
nc = [x for x in son_valid if not x["cleared"]]
print("sonnet valid", len(son_valid), "cleared", sum(x["cleared"] for x in son_valid), "non-clearing:", [(x["n"], x["sum"], x["valid_1e9"], x["why9"]) for x in nc])
pf = [x for x in out["rows"] if x["tier"] == "weak" and x["bin"] == "stdout_parse_fail"]
print("weak parse fails", len(pf), Counter(x["why"] for x in pf))
(ROOT / "evidence" / "cl_recount.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
