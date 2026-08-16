# Arm V — amendment 2 (registered before its sampling)

Registered 2026-08-12, before any invocation of the models named here.
Original registration `arm_v_preregistration.md` (git 5444f10), amendment 1
(git 52751ee). Prompts, hashes, N set, samples per cell, floor, V1/V2 rules
and scorer are unchanged.

## Added proposers — OpenRouter free tier, direct HTTP API

 9. `google/gemma-4-31b-it:free`            (Google)
10. `openai/gpt-oss-20b:free`               (OpenAI open-weights)
11. `cohere/north-mini-code:free`           (Cohere)
12. `liquid/lfm-2.5-2.6b:free`              (Liquid AI)
13. `nvidia/nemotron-3-ultra-550b-a55b:free` (NVIDIA flagship-scale)

## Why these five

Vendor families absent from every prior arm (Google at >9B, OpenAI,
Cohere, Liquid), plus one flagship-scale entry (550B-A55B) as a capability
anchor: wave 7 found 8-9B open models below the competence floor; this
amendment includes both a tiny model expected below floor (2.6B, included
deliberately as a floor control) and models large enough that a floor
failure would be informative rather than expected.

## Serving-path disclosures specific to this amendment

- Direct chat-completions API: unlike Arms A-F and the opencode arms, the
  REQUEST side is fully attested and logged per row (endpoint, model id,
  request body). The request sets max_tokens=8192 and nothing else;
  temperature/top_p are provider defaults, unattested, recorded as such.
- The response's `model` field and generation id are logged per row.
  Served quantization remains unattested (OpenRouter free variants are
  routinely served quantized) - which is the paper's point, and these rows
  inherit that caveat explicitly.
- `nemotron-3-ultra-550b-a55b` shares a family with amendment 1's
  nemotron entries; family-level counts treat all nemotron entries as one
  family (declared before results).
- Catalog note recorded pre-results: OpenRouter's catalog identifies two
  opencode aliases by vendor - laguna = Poolside, ling = inclusionAI.

## Rules

V1, V2, floor: per model, exactly as originally registered.
