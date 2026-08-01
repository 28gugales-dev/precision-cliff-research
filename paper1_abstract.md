# Paper 1 abstract (synced with revised draft 2026-08-01; supersedes kill-check draft)

Language models are increasingly placed in the proposal role of discovery loops such as
FunSearch and AlphaEvolve, on the assumption that their outputs explore a diverse solution
space. We characterize one component of that assumption: the *unconditioned* proposal — a
single zero-shot, code-free call with no parent program, no fitness feedback and no evaluator
in context. On a classic constructive-geometry benchmark, maximizing the sum of radii of N
circles in a unit square, a weak-tier proposer does not search. It emits a
grid-with-corner-fillers template and truncates it, even when a provably better construction is
one parameter away. The behavior admits a closed form: a nearest-square order k\* = round(√N)
with a value function V(k, m) identifies the *empirical modal output* at all seven tested N and
matches it to seven decimals. Per-sample agreement equals that modal frequency — 56–86% by
cell — while a round-number baseline hits 2 of 69 valid samples: the formula captures
everything short of sampling entropy. We preregistered these point predictions with prompt
hashes before sampling and tested them out of sample on two containers, a square and a
rectangle to which the rule was restated but never refitted. Across three tiers we find three
attractor families and an inversion: constructive ambition rises with nominal tier while
execution validity does not (78% → 100% → 13% at the primary 10⁻⁶ tolerance; the third arm is
an unattributable serving alias, reported with that caveat throughout). Trace elicitation is an
intervention rather than an observation: requesting a method line concentrates outputs onto the
anchor (87% vs 70% on-prediction, p = 0.03 uncorrected — failing Holm over the registered
family, carried by one of three cells), with no detectable validity change (p = 0.30,
n = 60/arm; not powered to exclude an effect of the observed size). Method lines are checkable
against emitted coordinates: 54 of 56 scoreable claims (96.4%) describe the object actually
built. Two scope conditions are load-bearing: the closed form is a weak-tier law that does not
describe the two higher tiers sampled, and it describes what an *unconditioned* call emits, not
what a loop converges to.

---

(For kill-check claim decomposition history see kill_check_2026-08-01.md.)
