# Wave 4 model identity note (2026-08-08)

The ledger's `model_reported` field is `none_reported`: the agent runtime returned no
model identifier with any response. The `model_requested` field is the exact string
passed to the runtime's model parameter.

For parity with arm F's `proposer_dated_id_on_run_date` convention, the model IDs the
HARNESS ADVERTISED on the sampling date were:

| requested | harness-advertised ID on 2026-08-08 |
|---|---|
| haiku  | claude-haiku-4-5-20251001 |
| sonnet | claude-sonnet-5 |
| opus   | claude-opus-5 |

These are harness-advertised, NOT runtime-attested. Nothing in the response path
confirms which weights served any call (C3), and the prereg's SS2 scoping applies to
these IDs exactly as it applies to the tier names.

Uniqueness check (post-hoc, disclosed as such): all 120 valid configurations are
pairwise distinct at 6 dp within and across tiers — zero exact self-copies. Opus's
39/40 zero-score outputs are family-similar symmetric templates, not repeats of one
configuration.
