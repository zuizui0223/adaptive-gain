# Higher-tier publication route v1

Status: **promotion lane for review; current Theoretical Ecology package remains an intact fallback.**

## Scientific reason to reopen routing

The current manuscript is stronger than a generic adaptivity-gap paper. Its principal result runs backward from a requested eco-evolutionary regime to the minimum finite decision/separation architecture capable of supporting that regime:

```text
required local dynamical regime
-> required feedback gain
-> required integer structural gap
-> exact/Pareto-minimal finite sensing architecture
```

The new nonlinear no-go theorem removes the main routing objection that this biological conclusion depends on exact linearity of `G=a Delta g`.

For a nondecreasing sensing-to-selection map with marginal effect bounded above by `L`, and positive feedback-per-selection scale `B=-beta e`, every admissible lift obeys

```text
G <= B L Delta_g.
```

Therefore

```text
B L q_max <= G_osc
-> the requested oscillatory regime is impossible
   for every lift in the declared monotone-Lipschitz class.
```

The linear acquisition-cost model remains a microfounded special case, not the sole bridge.

---

## Submission sequence

### 1. Evolution Letters — Letter

**Decision: credible high-risk first shot after the nonlinear bridge is integrated into the main manuscript.**

Current official scope checked 2026-09-13:

- https://academic.oup.com/evlett/pages/about
- https://academic.oup.com/evlett/pages/author-guidelines

The journal explicitly welcomes theoretical evolutionary studies and new analytical or methodological frameworks with broad potential influence. A typical Letter is approximately 5,000 words.

### Required framing

Lead with one biological claim:

> **Finite sensing architecture places hard lower bounds on which eco-evolutionary feedback regimes are reachable.**

The paper should not be presented as four coequal theorems. Use this hierarchy:

1. principal reverse reachability/no-go theorem;
2. nonlinear robustness of the sensing-to-selection bridge;
3. ecological recurrence as the temporal filter of structural reward;
4. oscillation/stasis results as diagnostics and interpretation.

### Main desk-reject risk

The editor may judge the result too abstract unless the finite architecture is biologically legible before the combinatorics. The first figure and first two pages must translate represented alternatives, cue resources, adaptive branching, fixed obligations, and recurrent community states into natural-history language.

### Compression rule

Continuation quotients, proof DAGs, exhaustive finite enumeration, LP certificates, and most bounded-arity construction details belong in Supplement. The Letter must remain about evolutionary reachability, not algorithmic machinery.

---

### 2. The American Naturalist — Major Article

**Decision: strongest conceptual-fit fallback and potentially the best home if Evolution Letters judges the manuscript too theory-heavy for a concise Letter.**

Current official scope checked 2026-09-13:

- https://www.journals.uchicago.edu/journals/an/about
- https://www.journals.uchicago.edu/journals/an/instruct
- https://www.journals.uchicago.edu/journals/an/editorial

The journal explicitly prioritizes conceptual unification, sophisticated methodology and innovative theoretical synthesis across ecology and evolution.

### Required framing

The Am Nat version may retain more of the conceptual architecture than the Evolution Letters version, especially the distinction between:

- architecture-generated selection amplitude;
- ecological recurrence of the same state-indexed rewards;
- cancellation versus restoring stasis;
- what oscillatory versus monotone return can establish about feedback existence.

The no-go theorem should still remain the flagship result.

---

### 3. Ecology Letters — conditional challenge only

**Decision: do not route there solely because the mathematics is strong.**

Current scope checked 2026-09-13:

- https://onlinelibrary.wiley.com/page/journal/14610248/homepage/productinformation.html

Ecology Letters prioritizes highly novel, broad ecological advances. The current theory has an ecological component because community-state recurrence and reward-mode alignment are load-bearing, but the strongest immediate identity remains evolutionary theory.

Reconsider an Ecology Letters challenge only if the final paper makes the joint principle unavoidable:

> what organisms can distinguish constrains structural selection amplitude, while how ecological states recur determines which part of that structural reward survives through time.

A second model or empirical example is not required by declaration, but the ecological recurrence side must be visibly indispensable rather than decorative.

---

### 4. Theoretical Ecology — preserved fallback

The current submission package remains scientifically valid and should not be dismantled. If the higher-tier route is declined, the manuscript can return to Theoretical Ecology without adding more theorem families or changing the claim ceiling.

---

## Promotion gates before first higher-tier submission

All must be true:

1. nonlinear monotone-Lipschitz no-go theorem is tested and integrated;
2. linear lift is presented as a biological acquisition-cost special case, not an unexplained equality;
3. `architecture too simple -> requested regime impossible` appears in title/abstract/first main result;
4. one principal theorem dominates the manuscript hierarchy;
5. main text is reduced to an evolution-first narrative with mathematical machinery moved to Supplement;
6. prior-art wording remains conservative about information-fitness bounds, decision trees and adaptivity gaps;
7. current Theoretical Ecology submission bundle remains archived as fallback rather than overwritten.

## Stop rule

Do **not** add additional theorem families merely to justify a higher-status journal. If the nonlinear bridge and no-go orientation do not make the existing principal theorem sufficiently broad, return to Theoretical Ecology or Am Nat rather than theorem hunting.
