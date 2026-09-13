# Higher-tier publication route v1

Status: **Evolution Letters V2 candidate materialized; Theoretical Ecology package remains an intact fallback.**

## Scientific reason to reopen routing

The paper is stronger than a generic adaptivity-gap result. In ecological state `i`, the finite sensing task has state-specific gap

```text
g_i = C_F(i) - C_A(i) >= 0.
```

Feedback depends on the ordered contrast between ecological states,

```text
Delta g = g_2 - g_1,
```

not on one `g_i` in isolation. The principal result runs backward:

```text
required local dynamical regime
-> required feedback gain
-> required between-state structural contrast
-> at least one required high-gap state
-> exact/Pareto-minimal finite sensing architecture for that state
```

For a nondecreasing sensing-to-selection map with marginal effect bounded above by `L`, and positive feedback-per-selection scale `B=-beta e`, every admissible lift obeys

```text
G <= B L Delta g.
```

Thus if an architecture class bounds every state-specific gap by `0<=g_i<=q_max`, then it also bounds `Delta g<=q_max`; whenever

```text
B L q_max <= G_osc,
```

the requested oscillatory regime is impossible for the entire class. The linear acquisition-cost model remains a microfounded constructive special case, not the sole bridge.

---

## Submission sequence

### 1. Evolution Letters — Letter

**Decision: credible high-risk first shot. Canonical candidate: `manuscript/MANUSCRIPT_EVOLUTION_LETTERS_V2.md`.**

Current official scope and format were checked on 2026-09-13 and recorded in `EVOLUTION_LETTERS_FORMAT_RECEIPT_20260913.md`. The journal explicitly welcomes theoretical evolutionary studies and new analytical or methodological frameworks with broad potential influence; a typical Letter is approximately 5,000 words.

Recent *Evolution Letters* content confirms active editorial space for mathematical work on sensing and evolutionary decision mechanisms, including Frank (2024) on anticipation of environmental trends, Han et al. (2025) on reversible plasticity, and Kuijper et al. (2026) on behavioral flexibility and limited mental resources. These are fit precedents, not priority claims.

### Required framing

Lead with one biological claim:

> **Finite sensing architecture places hard lower bounds on which eco-evolutionary feedback regimes are reachable.**

Use this hierarchy:

1. nonlinear between-state contrast no-go theorem;
2. transport from required contrast to a high-gap state and finite architecture;
3. ecological recurrence as temporal filtering of structural reward;
4. oscillation diagnostics as interpretation rather than a second flagship claim.

The cancellation-versus-restoration stasis proposition is not a coequal Letter headline.

### Main desk-reject risk

The editor may judge the result too abstract unless the finite architecture is biologically legible before the combinatorics. Figure 1 and the first two pages therefore define state-specific gaps and the between-state contrast before presenting extremal finite formulas.

### Compression rule

Continuation quotients, proof DAGs, exhaustive finite enumeration, LP certificates, most bounded-arity construction details and extended stasis algebra belong in Supplement.

---

### 2. The American Naturalist — Major Article

**Decision: strongest conceptual-fit fallback.**

The Am Nat version may retain more of the conceptual architecture: architecture-generated selection amplitude, ecological recurrence, cancellation versus restoring stasis, and what oscillatory versus monotone return can establish about feedback existence. The nonlinear no-go theorem remains the flagship result.

---

### 3. Ecology Letters — conditional challenge only

Do not route there solely because the mathematics is strong. Reconsider only if the final narrative makes the ecological principle unavoidable:

> what organisms can distinguish in each ecological state constrains the available selection contrast, while how ecological states recur determines which part of that contrast survives through time.

---

### 4. Theoretical Ecology — preserved fallback

The existing submission package remains scientifically valid and must not be dismantled. If the higher-tier route is declined, return to Theoretical Ecology without adding theorem families or changing the claim ceiling.

---

## Promotion gates

1. nonlinear no-go theorem implemented — **CLOSED**;
2. state gap versus between-state contrast separated — **CLOSED in V2 surfaces**;
3. linear lift demoted to constructive acquisition-cost special case — **CLOSED**;
4. one principal theorem dominates Letter hierarchy — **CLOSED**;
5. V2 Letter text + three-figure surface materialized — **CLOSED pending final CI/visual QA**;
6. prior-art wording remains conservative — **CLOSED**;
7. Theoretical Ecology fallback preserved — **CLOSED**.

Remaining before submission: final full CI, human visual review, author metadata/declarations, archive DOI if available, dispatch-time journal-policy recheck and all-author approval.

## Stop rule

Do **not** add additional theorem families merely to justify a higher-status journal. Repair only demonstrated semantic, validation, clarity, format or visual defects.
