# Summary sufficiency ladder for ecological routeability

Status: post-freeze synthesis. This note organizes the existing counterexamples by how much quantitative information is matched before conditional decision topology becomes identifiable.

The question is:

> how rich must an ecological summary be before it determines the finite routeability problem?

The answer in the current deterministic model is hierarchical.

---

## Level 0 — raw ecological counts

Matched:
- number of represented states;
- number of query/cue resources;
- unit costs.

Not sufficient.

Routeable and control tasks can have the same \(n\) and \(m\) but different \((C_A,C_F)\).

---

## Level 1 — all one-cue marginals

Matched:
- Level 0;
- every query outcome frequency.

The exact-balanced family goes further: every binary query is exactly 50/50.

Not sufficient.

\[
\frac{C_F}{C_A}
\]

can still diverge.

---

## Level 2 — the complete cue-only joint distribution

Matched:
- Level 1;
- the entire physical query-outcome matrix;
- therefore every cue-only marginal and every cue-only joint distribution of every order.

The quantity-matched routeable/control pair uses the **same physical cue matrix**.

Not sufficient.

The action map changes while the cue environment is literally unchanged.

---

## Level 3 — target amount

Matched:
- Level 2;
- target multiplicities;
- target entropy under the uniform world prior.

Not sufficient.

For routing depth \(d\), both tasks have target multiplicities

\[
(2^d+2,\ 2^d).
\]

Yet the matched control has

\[
C_A=C_F=2,
\]

while the routeable task satisfies

\[
C_F\ge2^d,\qquad C_A\le d+1.
\]

---

## Level 4 — total available target information

Matched:
- Level 3;
- full-vocabulary target information.

Because the full query vocabulary resolves the target in both tasks,

\[
I(T;Q_{\mathrm{all}})=H(T)
\]

is identical.

Still not sufficient.

Thus:

\[
\boxed{
\text{total information available}
\neq
\text{architecture required to acquire it}.
}
\]

The asymptotic separation remains unbounded.

---

## Level 5 — pairwise target-cue information-strength profile

At registered finite scopes, matched:
- Level 2;
- target multiplicities;
- the multiset of canonical target-query \(2\times2\) contingency profiles.

This implies the same multiset of pairwise target-cue information strengths up to binary relabeling.

### Depth 2

Matched control:

\[
C_A=C_F=2.
\]

### Depth 3

Matched control:

\[
C_A=C_F=3.
\]

The routeable tasks on the same physical cue matrices retain substantially larger fixed burden.

Therefore even pairwise target-cue information-strength summaries can fail to identify decision topology.

Claim ceiling:

- this is a finite registered result;
- the pairwise match is a multiset match, not cue-name-by-cue-name identity;
- no asymptotic Level-5 family is currently claimed.

---

## Level 6 — complete action-conditioned cue table

Observed:
- represented state identity;
- target/action \(T(w)\);
- every cue outcome \(q_j(w)\);
- cue costs.

In the deterministic finite model this is sufficient to define the optimization problem.

Then \(C_A\) and \(C_F\) can in principle be computed exactly.

Thus the theory does **not** say topology is fundamentally unobservable.

It says:

> summaries below the complete action-conditioned structure can remain insufficient even when they are quantitatively very rich.

---

## Identification ladder

\[
\begin{array}{rcl}
\text{counts} &\not\Rightarrow& \text{routeability}\\
\text{marginals} &\not\Rightarrow& \text{routeability}\\
\text{full cue-only distribution} &\not\Rightarrow& \text{routeability}\\
\text{target entropy} &\not\Rightarrow& \text{routeability}\\
I(T;Q_{\rm all}) &\not\Rightarrow& \text{routeability}\\
\text{pairwise target-cue profile} &\not\Rightarrow& \text{routeability}\quad\text{(finite witnesses)}\\
\text{complete action-conditioned cue table} &\Rightarrow& \text{deterministic routeability problem specified.}
\end{array}
\]

---

## Ecological consequence

This ladder changes the measurement question.

Instead of asking only:

- how many species?
- how variable is the environment?
- how informative is each cue?
- how much total information is available?

a routeability test must eventually recover:

- what action each state requires;
- which alternatives remain confusable after each observation;
- which cue becomes relevant on each branch;
- the cost/timing of acquiring that cue.

The missing coordinate is not "more information" in the same scalar sense.

It is **action-conditioned conditional structure**.

---

## Relation to nonidentifiability

The ladder supplies a constructive form of nonidentifiability.

At Levels 0–4, there are matched tasks with the same summary but different routeability.

At Level 5, finite matched controls show the same phenomenon for pairwise target-cue information-strength profiles.

Only when the complete deterministic action-conditioned table is available is the present routeability object identified by construction.

This yields a reusable methodological rule:

> before interpreting an ecological summary mechanistically, determine whether the latent structure required by the mechanism is identifiable from that summary.

---

## Experimental implication

The hierarchy suggests escalating controls.

### Minimal direct experiment

Match:
- physical cue support;
- cue frequencies;
- pairwise information signatures;
- cue-only joint distribution.

### Exact-balanced stress test

Match:
- full physical cue matrix;
- target prevalence;
- target entropy;
- total full-vocabulary target information.

### Strong finite pairwise stress test

Additionally match:
- pairwise target-cue information-strength profile.

The experiment need not begin at the strongest level. The ladder clarifies what each design rules out.

---

## Current claim boundary

The current deterministic theory supports a **summary-insufficiency hierarchy**, not a universal theorem that all scalar ecological metrics fail.

A statistic computed from the complete action-conditioned table can of course encode routeability.

The novel point is that several natural and unusually strong quantitative summaries still do not.

## One-line result

\[
\boxed{
\text{More complete measurement of amount does not become measurement of conditional structure until the action-conditioned mapping itself is observed.}
}
\]
