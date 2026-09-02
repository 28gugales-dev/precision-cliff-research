# Arm P-D, amendment 1: the arm is closed at 27 of 30 rows

Registered 2026-09-02, after the interim scoring and before any further sampling.

The registration (arm_pd_preregistration.txt, commit 5554cc0) planned 15 rows per condition.
Sampling stopped at 27 rows (14 D1, 13 D2) when the serving path returned HTTP 402 on the
next three requests, all recorded in arm_pd_collect.jsonl; the credit the resume rule waited
on did not arrive. The registration's own verdict logic makes the remaining three rows
irrelevant to P-PD1: D1 holds 12 valid of 14 (bar >= 8), D2 holds 0 valid of 13 (bar <= 3 for
P-PD1; D2 could reach at most 2), so no completion of the ledger can change the verdict.

Decision, fixed here: the arm is closed at 27 of 30. The three 402 rows remain in the ledger
as refusals. arm_pd_report.json is regenerated with the INTERIM mark replaced by
"closed at 27 of 30 (amendment 1)". The paper reports the arm as closed, credit-limited,
with the count 27 of 30 beside every verdict. No further P-D rows will be sampled under this
registration; a top-up would be a new arm.
