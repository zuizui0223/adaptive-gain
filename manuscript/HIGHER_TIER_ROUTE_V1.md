# Higher-tier publication route v1

Status: **Evolution Letters candidate manuscript materialized; current Theoretical Ecology package remains an intact fallback.**

## Scientific reason to reopen routing

The current manuscript is stronger than a generic adaptivity-gap paper. Its principal result runs backward from a requested eco-evolutionary regime to the minimum finite decision/separation architecture capable of supporting that regime:

```text
required local dynamical regime
-> required feedback gain
-> required integer structural gap
-> exact/Pareto-minimal finite sensing architecture
```

The nonlinear no-go theorem removes the main routing objection that this biological conclusion depends on exact linearity of `G=a Delta g`.

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

**Decision: credible high-risk first shot. A dedicated Letter surface now exists at `manuscript/MANUSCRIPT_EVOLUTION_LETTERS_V1.md`.**

Current official scope and format were checked on 2026-09-13 and recorded in `EVOLUTION_LETTERS_FORMAT_RECEIPT_20260913.md`:

- https://academic.oup.com/evlett/pages/about
- https://academic.oup.com/evlett/pages/author-guidelines

The journal explicitly welcomes theoretical evolutionary studies and new analytical or methodological frameworks with broad potential influence. A typical Letter is approximately 5,000 words, with a 300-word abstract and optional 150-word teaser.

### Recent journal-side precedent

Recent *Evolution Letters* content shows that mathematical work on sensing, behavioral flexibility and evolutionary decision mechanisms is within the journal's active editorial space:

- Frank (2024), **A biological circuit to anticipate trend** — a compact theoretical treatment of anticipating stochastic environmental trends;
- Han et al. (2025), **The evolution of reversible plasticity in stable environments** — mathematical theory of reversible specialization;
- Kuijper et al. (2026), **Evolution of behavioral flexibility and the forming and breaking of habits** — evolutionary modelling of limited mental resources, attention and flexible information use.

These are journal-fit precedents, not priority claims. The adaptive-gain paper differs by owning a finite-architecture necessity/no-go result rather than a forward model of one sensing or learning strategy.

### Required framing

Lead with one biological claim:

> **Finite sensing architecture places hard lower bounds on which eco-evolutionary feedback regimes are reachable.**

The paper should not be presented as four coequal theorems. Use this hierarchy:

1. principal reverse reachability/no-go theorem;
2. nonlinear robustness of the sensing-to-selection bridge;
3. ecological recurrence as the temporal filter of structural reward;
4. local oscillation diagnostics as interpretation rather than a second flagship claim.

The old cancellation-versus-restoration stasis proposition should not be a main headline in the Letter version.

### Main desk-reject risk

The editor may judge the result too abstract unless the finite architecture is biologically legible before the combinatorics. The first figure and first two pages must translate represented alternatives, cue resources, adaptive branching, fixed obligations, and recurrent community states into natural-history language.

### Compression rule

Continuation quotients, proof DAGs, exhaustive finite enumeration, LP certificates, most bounded-arity construction details, and extended stasis algebra belong in Supplement. The Letter must remain about evolutionary reachability, not algorithmic machinery.

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

Current machine state:

1. nonlinear monotone-Lipschitz no-go theorem tested and merged — **CLOSED**;
2. linear lift presented as acquisition-cost special case — **CLOSED in theorem note and Letter candidate**;
3. `architecture too simple -> requested regime impossible` in title/abstract/first result — **CLOSED**;
4. one principal theorem dominates the Letter hierarchy — **CLOSED**;
5. Evolution Letters main-text candidate and three-figure plan materialized — **CLOSED pending surface CI**;
6. prior-art wording remains conservative about information-fitness bounds, decision trees and adaptivity gaps — **CLOSED**;
7. current Theoretical Ecology submission bundle remains preserved rather than overwritten — **CLOSED**.

Remaining before actual submission:

- final surface/word-limit CI;
- build the three Evolution Letters main figures from the frozen figure plan;
- final author metadata and declarations;
- permanent archive DOI if available;
- dispatch-time live journal-policy check;
- final author approval.

## Stop rule

Do **not** add additional theorem families merely to justify a higher-status journal. If the nonlinear bridge and no-go orientation do not make the existing principal theorem sufficiently broad, return to Theoretical Ecology or Am Nat rather than theorem hunting.
