# Paper 1 abstract (draft for kill-check hunt, 2026-08-01)

Large language models are increasingly used as proposal generators in scientific-discovery
loops such as FunSearch and AlphaEvolve, on the assumption that their outputs explore a
diverse solution space. We show that on a classic constructive-geometry benchmark —
maximizing the sum of radii of N circles packed in a unit square — this assumption fails in
a strikingly predictable way. Across hundreds of zero-shot invocations, models do not
search: they recall a single grid-with-corner-fillers template and truncate it, even when a
provably better construction is one parameter away. The behavior is regular enough to admit
a closed form: a selection rule k* = round(√N) together with a value function V(k,m)
predicts the exact sum-of-radii the model will emit, to seven decimal places, including
"trap zones" of N where the rule provably costs value. We preregistered these predictions
with cryptographic prompt hashes before sampling and confirmed them out of sample in two
containers (square and rectangle), the latter with a rule restated but never refitted.
Across three model tiers we find three attractor families with a consistent inversion:
constructive ambition rises with tier while execution validity collapses (71% → 100% → 13%).
Finally, we show trace elicitation is an intervention, not an observation: asking the model
to name its method before answering concentrates outputs onto the template anchor (87% vs
70% on-prediction, p = 0.033) while leaving validity unchanged, and the emitted method
lines are verifiable against output coordinates (93% faithful). Our results characterize
the proposal distribution that LLM-driven discovery systems sample from: not a searcher,
but a template memorizer whose outputs a formula can anticipate.

## Kill-check claim decomposition (hunt targets)

K1. LLM template anchoring in constructive geometry / packing tasks (core novelty)
K2. Closed-form prediction of exact LLM output values (any domain)
K3. Behavioral analysis of LLMs on circle-packing benchmark specifically
K4. Preregistered, hash-locked, out-of-sample prediction of LLM behavior
K5. Tier inversion: bigger model, more ambitious construction, lower validity
K6. Method-line/trace elicitation shifts output distribution toward memorized anchor
    (DANGER ZONE: CoT-changes-answers literature is large; kill requires the narrow
    claim — minimal method-naming request concentrates onto memorized template —
    not merely "prompting for reasoning changes accuracy")
