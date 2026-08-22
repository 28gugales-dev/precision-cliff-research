# Smoke test for arm_cn_analysis.score_cell: replay arm M's N=57 ledger rows
# through the CN scorer with N=57's registered spec and require the arm M
# registered outcome (P-M4: modal = T(8,57) = 3.5625000, 6 on-prediction, 0 rival).
import json
from pathlib import Path

from arm_cn_analysis import score_cell
from arm_cn_build import cell_table

ROOT = Path(__file__).resolve().parent
rows = [json.loads(l) for l in (ROOT / "arm_m_collect.jsonl").read_text(encoding="utf-8-sig").splitlines() if l.strip()]
rows57 = [r for r in rows if int(r["cell"]) == 57]
spec = cell_table(57)
assert spec["discriminating"] and abs(spec["argmax"] - 3.7366935) < 1e-6
r = score_cell(57, spec, rows57)
print({k: r[k] for k in ("sampled", "valid6", "on_pred", "modal_value", "modal_count", "margin", "hit", "rival", "k_star_structure")})
assert r["sampled"] == 15 and r["on_pred"] == 6 and r["rival"] == 0, r
assert r["hit"] is True and abs(r["modal_value"] - 3.5625) < 2e-3, r
print("SMOKE OK: CN scorer reproduces arm M P-M4 at N=57")
