# Arm V — amendment 3 (mechanical repair, registered before resumption)

Registered 2026-08-12, after the first OpenRouter attempt and before any
resumed sampling. No rule, threshold, prompt, model set or scorer changes.

## What broke, mechanically

1. Three reasoning-style models (gpt-oss-20b, nemotron-3-ultra-550b,
   north-mini-code) returned HTTP 200 with `finish_reason: length`,
   completion tokens consumed, and EMPTY message content: the 8192-token
   ceiling was exhausted by hidden reasoning before any answer tokens.
   16 such rows exist in the ledger and stay there.
2. 52 rows failed HTTP 429 (upstream free-tier provider limits) under
   3-second spacing with parallel workers.
3. On the opencode side, 8 parallel Bun processes exhausted the local
   paging file ("The paging file is too small", "cannot execute the
   specified program"); those failure rows also stay in the ledger.

## Repairs (all mechanical, none behavioral)

- max_tokens raised 8192 -> 24576. This is the ONLY request parameter the
  runner sets; it was an arbitrary mechanical bound, and at 8192 it
  censored three models' outputs entirely rather than sampling them.
  Rows produced under each ceiling are distinguishable by their logged
  `request_params`.
- In-call retry with backoff on transport errors (45 s on 429, 10 s
  otherwise, max 4 attempts); attempts count logged per row.
- Per-call spacing 3 s -> 6 s.
- opencode worker cap 8 -> 3 (machine memory limit, measured).

## Accounting rule for the censored rows

Empty rows from the 8192 era are excluded from validity DENOMINATORS for
the three affected models (they were never complete samples); the resumed
run re-draws those cells. The ledger keeps every original row, so both
accountings (with and without the censored rows) are computable by any
reader. All other empty rows (429s, local exec failures) are likewise
transport failures, not model outputs, and follow the same rule -
consistent with Arm F's treatment of runtime-rejected dispatches.
