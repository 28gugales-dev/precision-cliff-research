# ============================================================================
# Arm CC smoke test — pushes four dummy responses through the full registered
# executor path BEFORE any sampling. Each must land in its registered bin.
# Run and committed with the preregistration.
# ============================================================================
from arm_cc_analysis import score_row

VALID_PROG = """```python
import math
r = 1 / 8
rows = []
for y in range(4):
    for x in range(4):
        rows.append([round((2 * x + 1) * r, 7), round((2 * y + 1) * r, 7), r])
print(rows[:13])
```"""

BLOCKED = "import numpy as np\nprint(np.zeros(3).tolist())"
TIMEOUT = "while True:\n    pass"
GARBAGE = "print('hello world, no list here')"

cases = [
    ("valid grid program", VALID_PROG, "valid"),
    ("scipy/numpy import", BLOCKED, "blocked_import"),
    ("infinite loop", TIMEOUT, "timeout"),
    ("garbage stdout", GARBAGE, "stdout_parse_fail"),
]

ok = True
for name, raw, expected in cases:
    got = score_row(raw, 13)
    status = "PASS" if got["bin"] == expected else "FAIL"
    if status == "FAIL":
        ok = False
    print(f"{status}: {name} -> {got['bin']} (expected {expected})"
          + (f" sum={got.get('sum')}" if got["bin"] == "valid" else ""))
assert ok, "smoke test failed"
print("smoke test: 4/4 bins correct")
