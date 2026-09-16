# Mathematical Atlas v1 — finite adaptive sensing and eco-evolutionary consequences

Status: canonical map of mathematical assets for the Evolution Letters V3 expansion.

## Purpose

This Atlas prevents two opposite failures: hiding substantial mathematics behind one ecological theorem, and turning the Letter into a catalogue of unrelated results. Each theorem family is assigned one paper role:

- **MAIN** — omission would change the biological interpretation of the paper;
- **SUPPLEMENT** — proof, reduction or reproducibility machinery required to support a MAIN claim;
- **COMPANION** — mathematically substantial and reusable, but too broad for the Letter narrative;
- **ARCHIVE** — validated implementation, witness or provenance layer.

The paper-level flow is

```text
finite target-resolution geometry
-> exact adaptive/fixed cost difference
-> ecological budget or state-dependent structural contrast
-> selection
-> feedback reachability
-> temporal filtering / diagnostic limits
```

The central biological object is finite deterministic decision architecture, not Shannon or mutual information.

---

## A. Foundation: exact adaptive gain

### A1. Fixed versus adaptive exact resolution — MAIN

**Source:** `theory/ADAPTIVE_GAIN_THEOREM.md`

For any resolvable finite deterministic task with positive additive query costs,

\[
C_A\le C_F.
\]

The fixed class is contained in the adaptive class because an adaptive policy can always ignore outcomes and execute a fixed resolving bundle.

**Biological interpretation.** Contingent cue acquisition cannot require more worst-case acquisition cost than the best precommitted cue bundle for the same guaranteed decision target.

**Claim ceiling.** Class containment is exact for the declared finite task and is not an empirical frequency statement.

### A2. Exact adaptive-only budget window — MAIN

For integer ecological budget `B`, adaptive-only guaranteed resolution occurs exactly when

\[
\boxed{C_A\le B<C_F.}
\]

If `C_A<C_F`, the favorable budgets form one contiguous interval.

**Biological interpretation.** A hard deadline or resource ceiling can create a regime in which contingent sensing succeeds but every fixed resolving architecture fails. Candidate budgets include time before attack, handling deadlines, energetic ceilings, exposure risk, developmental windows and opportunity windows; the focal natural history must justify the chosen interpretation.

**Evolutionary bridge:** `theory/BUDGET_GATED_EVOLUTIONARY_SELECTION.md`.

---

## B. Target-relevant reduction and exact kernels

### B1. State-local adaptive-safe query compression — SUPPLEMENT

**Source:** `theory/ADAPTIVE_SAFE_QUERY_COMPRESSION.md`

At active represented-world state `A`, if query `q` separates a superset of active cross-target pairs separated by `r`,

\[
S_A(q)\supseteq S_A(r),
\]

and costs no more,

\[
c(q)\le c(r),
\]

then `r` is safely dominated at that Bellman state. Equality of target-mixed continuation cells is the special case.

**Biological interpretation.** Two cues that differ in raw observations need not represent distinct biological decision resources if one is target-relevantly at least as resolving at no greater cost. Decision-relevant cue diversity is therefore smaller than raw cue diversity in some natural-history descriptions.

**Claim ceiling.** Deterministic exact resolution, positive additive costs, worst-path objective only.

### B2. Same-target world twins — SUPPLEMENT

**Source:** `theory/ADAPTIVE_WORLD_TWIN_QUOTIENT.md`

Same-target represented worlds that have identical remaining cross-target separation profiles can be quotient-collapsed without changing adaptive continuation value.

**Biological interpretation.** Ecological alternatives that differ descriptively but induce identical future target-relevant discrimination requirements are the same decision state for the declared objective.

### B3. Exact adaptive two-sided Bellman kernel — SUPPLEMENT / COMPANION

**Source:** `theory/ADAPTIVE_TWO_SIDED_KERNEL.md`

World-side quotienting and query-side target-relevant refinement dominance compose exactly:

\[
\boxed{C_A^{\rm two-sided}=C_A^{\rm direct}.}
\]

**Biological interpretation.** Raw natural-history complexity can be compressed to a target-relevant decision kernel before ecological inference, provided the declared deterministic objective and costs are preserved.

**Why not MAIN.** The ecological message matters, but the kernel proof machinery would interrupt the Letter's reachability argument. V3 should mention the quotient principle briefly and keep the theorem in Supplement.

### B4. Bipartite/refinement and fixed-cover kernels — COMPANION

**Sources include:**
- `theory/BIPARTITE_COLOR_REFINEMENT.md`
- fixed weighted-cover/kernel and certificate modules under `adaptive_gain/`

These results formalize representation reduction and proof certificates for fixed and adaptive optimization. They are reusable decision-theory contributions but are not separate EL headline claims.

---

## C. Sharp finite extremal geometry

### C1. General binary structural threshold — MAIN

**Source:** `theory/GENERAL_BINARY_DYNAMIC_SCOPE_THRESHOLD.md`

For integer required structural gap `q>=1`, define

\[
h_2^*(q)=\min\{h\ge1:2^h-1-h\ge q\}.
\]

The first componentwise binary unit-cost corner capable of gap `q` is

\[
\boxed{
(n^*,m^*,E^*)
=(h_2^*+q+1,\;h_2^*+q,\;h_2^*+q).
}
\]

It is componentwise sharp. Moreover,

\[
h_2^*(q)=\log_2 q+O(1),
\]

so adaptive routing depth grows logarithmically while fixed-mandatory structural burden grows essentially linearly in the required gap.

**Biological interpretation.** Increasingly demanding state-dependent advantage requires disproportionately more branch-exclusive/fixed-mandatory cue structure even when contingent routing remains shallow.

### C2. Bounded-arity Pareto frontier — MAIN

**Sources:**
- `theory/ARITY_GAP_PARETO.md`
- `theory/DYNAMIC_ARITY_PARETO.md`

For maximum cue arity `b>=2`, separate minima for represented worlds, cue resources and productive obligations need not be attained by one task. The exact requirement is generally a Pareto frontier `P_b(q)`.

Canonical example for `q=3,b=4`:

\[
(7,6,6),\qquad(8,5,5)
\]

are both nondominated.

**Biological interpretation.** Richer cue outcomes can trade cue/resource burden against the number of ecological alternatives that must be represented; there is no universal one-dimensional notion of sensory complexity.

### C3. Exactly-balanced binary queries do not bound adaptive gain — MAIN

**Source:** `theory/BALANCED_BINARY_UNBOUNDED_ADAPTIVE_GAIN.md`

There exists a family with finite represented worlds, deterministic binary unit-cost queries, and every query exactly 50/50 balanced, yet

\[
\boxed{
\frac{C_F}{C_A}
\ge
\frac{2^d}{d+1}
\to\infty.
}
\]

**Biological interpretation.** Global marginal cue balance is not the structural quantity controlling adaptive value. Large gain can arise entirely from branch-exclusive resource geometry: adaptive sensing first discovers which branch matters and pays only for that branch-specific terminal cue, whereas fixed sensing must carry every branch-specific obligation.

**Claim ceiling.** Existence lower bound only; not the sharp maximum at fixed `(n,m)` under balancedness.

### C4. Balanced binary fixed-scope/sharp finite profiles — SUPPLEMENT / ARCHIVE

**Sources include:** balanced-binary depth, cap, small-scope and finite-profile theorem/implementation families.

These establish exact finite witnesses, caps and boundaries that support the general constructions. They remain proof support unless a reviewer requests a fixed-scope statement.

---

## D. Evolutionary lifts

### D1. Monotone-Lipschitz nonlinear no-go theorem — MAIN / principal reachability result

**Sources:**
- `theory/NONLINEAR_LIFT_NO_GO_V2.md`
- `adaptive_gain/nonlinear_feedback_reachability.py`
- `validation/nonlinear_lipschitz_no_go_v2.json`

For state-specific gaps `g_i>=0`, ordered contrast `Delta g=g_2-g_1>=0`, and a nondecreasing sensing-to-selection lift satisfying

\[
0\le f(g_2)-f(g_1)\le L\Delta g,
\]

feedback obeys

\[
0\le G\le BL\Delta g.
\]

If complex local return requires `G>G_osc`, then

\[
\boxed{
\Delta g>\frac{G_{\rm osc}}{BL}
}
\]

is necessary. Consequently, any architecture class with

\[
BL\Delta g_{\max}\le G_{\rm osc}
\]

is structurally excluded from the requested oscillatory regime for every lift in the declared class.

**Claim ceiling.** Crossing the bound does not guarantee oscillation.

### D2. Hard-budget evolutionary selection — MAIN

**Source:** `theory/BUDGET_GATED_EVOLUTIONARY_SELECTION.md`

Define exact resolution indicators

\[
S_A(X,B)=1\{C_A(X)\le B\},
\qquad
S_F(X,B)=1\{C_F(X)\le B\}.
\]

With baseline fitness `w_0>0`, resolution benefit `v>=0` and contingent-control maintenance cost `kappa>=0`,

\[
W_A=e^{-\kappa}[w_0+vS_A],
\qquad
W_F=w_0+vS_F,
\]

and

\[
s_B=\log(W_A/W_F).
\]

Selection favoring contingent architecture is concentrated in the exact adaptive-only window `C_A<=B<C_F`, provided the benefit exceeds maintenance cost.

**Biological interpretation.** State-dependent selection can arise through crossing a hard ecological deadline/resource ceiling even when there is no linear conversion from each saved cue to fitness.

**Why it matters to V3.** This is an independent biological bridge from the same finite mathematics and protects the paper from depending solely on a continuous cost-to-selection lift.

### D3. Budget-gated structural collision and related threshold notes — SUPPLEMENT / COMPANION

**Source:** `theory/BUDGET_GATED_STRUCTURAL_COLLISION.md` and associated modules.

These refine the geometry of thresholded success/selection. Use only where they clarify the exact budget-window mechanism; do not create a second headline.

---

## E. Temporal filtering and dynamical interpretation

### E1. Structural-spectral joint envelope — MAIN supporting result

**Sources:**
- `theory/STRUCTURAL_SPECTRAL_JOINT_BOUND.md`
- `theory/STRUCTURAL_REWARD_MODE_ALIGNMENT.md`

For a finite ergodic reversible ecological chain,

\[
\sigma_{\rm eff}^2
=
\sum_r w_r\frac{1+r_r}{1-r_r}.
\]

In the linear acquisition-cost special case with `0<=g_i<=g_max`,

\[
\sigma_{\rm eff}^2
\le
\frac{(\lambda g_{\max})^2}{4}
\frac{1+r_{\max}}{1-r_{\max}}.
\]

**Biological interpretation.** Environmental persistence amplifies only the component of structurally generated selection that loads onto the slow ecological mode. Persistence alone does not imply strong evolutionary memory.

**Claim ceiling.** Sharp extremal ceiling, not a generic realized-variance predictor.

### E2. Feedback-existence diagnostic — MAIN boundary result

**Sources:**
- `theory/FEEDBACK_EXISTENCE_FROM_OSCILLATION.md`
- `theory/GENERAL_RESPONSE_IDENTIFIABILITY.md`

Within the declared persistence domain, a compatible complex eigenpair excludes all zero-feedback decompositions, while feedback magnitude and persistence components remain unidentified.

**Biological interpretation.** Oscillatory return can diagnose that feedback exists within the model without identifying how much of it is caused by sensing architecture.

### E3. Stasis and transient observability notes — COMPANION / ARCHIVE

Two-origins-of-stasis, scalar transient observability, critical-slowing and related diagnostic material remain useful conceptual extensions but are not needed for the V3 core claim.

---

## F. What V3 should say as one theory

The mathematical results are not five independent novelty claims. Their integrated ecological interpretation is:

1. A finite task has an exact adaptive and fixed resolution cost.
2. Exact target-relevant quotienting identifies which raw natural-history distinctions matter to that decision problem.
3. Sharp extremal theory bounds how large the adaptive advantage can be for a declared architecture and shows that simple marginal cue statistics can be deeply misleading.
4. Ecological state changes can alter either the structural gap or the position of a fixed budget relative to `[C_A,C_F)`, creating state-dependent selection by two different biological routes.
5. The available structural contrast bounds which local eco-evolutionary feedback regimes are reachable.
6. Ecological recurrence then filters the generated selection through time.

Compressed as a causal architecture:

```text
natural-history alternatives + cue repertoire
-> target-relevant decision kernel
-> (C_A, C_F)
-> {structural contrast, adaptive-only budget window}
-> state-dependent selection
-> feedback reachability
-> temporal expression
```

This is the mathematical backbone of the V3 paper.

---

## G. Explicit exclusions

The Atlas does not license extensions to noisy Bayesian observations, expected-loss optimization, variable likelihood quality, continuous sensing time, unequal unmodeled physiological costs, finite-population genetics, migration, mutation, demographic stochasticity, multivariate genetics or global nonlinear bifurcation theory. Those require separate assumptions or theorems.
