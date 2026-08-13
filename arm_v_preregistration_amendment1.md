# Arm V — amendment 1 (registered before its sampling)

Registered 2026-08-12, after the original three-model run began but BEFORE
any invocation of the models named here. Original registration:
`arm_v_preregistration.md` (git 5444f10). Nothing in the original is
changed: same prompts and hashes, same N set, same 5 samples per (model, N),
same floor, same V1/V2 rules and thresholds, same scorer.

## Added proposers (opencode zen free tier, run date 2026-08-12)

4. `opencode/laguna-s-2.1-free`
5. `opencode/ling-3.0-tiny-free`
6. `opencode/mimo-v2.5-free`
7. `opencode/nemotron-3.5-lightning-free`
8. `opencode/big-pickle`

## Disclosures specific to this amendment

- `big-pickle` is a deliberately unattributed stealth alias: the vendor
  itself is unattested, not merely the serving path. It is included for
  exactly that reason - it is the limiting case of the paper's alias
  argument - and any result from it is reported as "vendor unknown".
- `nemotron-3.5-lightning-free` shares a vendor family with the original
  run's `nemotron-3-ultra-free`; for family-level counts these two are one
  family, disclosed here before results exist.
- Model-name aliases on this tier carry no version pin; the dated ledger
  row is the only address each invocation has (the paper's §4 point,
  restated for this tier).
- OpenRouter free tier was requested but is unavailable in this
  environment (no API key); if added later it requires amendment 2 before
  sampling.

## Rules

V1, V2, and the competence floor apply to each added model exactly as
written in the original registration, evaluated per model.
