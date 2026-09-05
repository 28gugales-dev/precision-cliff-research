# Post hoc, disclosed: the 22 weak-tier arm CL programs binned stdout_parse_fail all print
# numpy 2.x scalar reprs (`np.float64(0.49...)`), which ast.literal_eval rejects. The registered
# parser is left as it is; this script applies one lenient reading (strip the `np.float64(`
# wrapper and its closing parenthesis, nothing else) to every row's stdout from the re-execution
# in evidence/cl_recount.json, then validates and scores under the registered conventions, so
# the paper can report the recovered packings beside the registered bins. Sonnet rows have no
# parse failures, so the lenient reading changes nothing there; that is checked, not assumed.
# Unseeded programs (numpy.random without a seed) were re-executed, so the recovered sums are
# from this execution, not the original run; the per-cell bins reproduced exactly.
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = Path(r"~\AppData\Local\hermes\research-corpus\precision-cliff")
sys.path.insert(0, str(CORPUS))
import arm_cl_analysis as cl  # noqa: E402

WRAP = re.compile(r"np\.float64\(([^()]*)\)")
rec = json.load(open(ROOT / "evidence" / "cl_recount.json", encoding="utf-8"))
out = {"rows": [], "weak_by_cell": {}, "sonnet_parse_fails": 0}
for x in rec["rows"]:
    if x["bin"] != "stdout_parse_fail":
        continue
    if x["tier"] == "sonnet":
        out["sonnet_parse_fails"] += 1
    s = WRAP.sub(r"\1", x["stdout"])
    packing, why = cl.parse_packing(s)
    r = dict(tier=x["tier"], n=x["n"], sample_id=x["sample_id"], seeded=x["seeded"])
    if packing is None:
        r["lenient"] = "still_unparseable"; r["why"] = why
    else:
        ok6, why6 = cl.validate(packing, x["n"], tol=1e-6)
        ok9, _ = cl.validate(packing, x["n"], tol=1e-9)
        r.update(lenient="parsed", valid_1e6=ok6, valid_1e9=ok9, why6=why6)
        if ok6:
            sm = cl.score(packing)
            r.update(sum=round(sm, 9), argmax=round(cl.ARGMAX[x["n"]], 9),
                     cleared=bool(ok9 and sm > cl.ARGMAX[x["n"]] + cl.WINDOW_9),
                     n_distinct_radii=len({round(q[2], 6) for q in packing}))
    out["rows"].append(r)

assert out["sonnet_parse_fails"] == 0
for n in (13, 21, 31):
    cell = [r for r in out["rows"] if r["tier"] == "weak" and r["n"] == n]
    valid = [r for r in cell if r.get("valid_1e6")]
    out["weak_by_cell"][str(n)] = dict(
        parse_fail=len(cell), parsed=sum(r["lenient"] == "parsed" for r in cell),
        valid_1e6=len(valid), valid_1e9=sum(1 for r in valid if r["valid_1e9"]),
        cleared=sum(1 for r in valid if r["cleared"]),
        why6=dict(Counter(r.get("why6") for r in cell if r["lenient"] == "parsed" and not r.get("valid_1e6"))),
        sums=sorted(r["sum"] for r in valid))
    print(n, out["weak_by_cell"][str(n)])
tot_v = sum(c["valid_1e6"] for c in out["weak_by_cell"].values())
tot_c = sum(c["cleared"] for c in out["weak_by_cell"].values())
out["weak_pooled"] = dict(registered_valid=11, recovered_valid=tot_v, valid_with_recovery=11 + tot_v,
                          recovered_cleared=tot_c)
print("weak pooled: registered 11 valid; lenient recovers", tot_v, "more valid,", tot_c, "clear")
(ROOT / "evidence" / "cl_lenient.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
