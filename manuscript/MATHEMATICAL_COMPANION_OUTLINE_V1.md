# Mathematical companion outline v1 — exact finite adaptive resolution

Status: companion-paper architecture for mathematical results that are substantial but would dilute the single biological headline of the Evolution Letters V3 manuscript. No new theorem family is introduced here.

## Working title

**Exact reductions and extremal gaps in finite adaptive target resolution**

Alternative biological-facing title:

**The geometry of contingent information acquisition in finite decision problems**

## Paper-level question

For finite deterministic target-resolution problems with positive additive query costs and worst-path optimization:

> Which parts of the represented world/query structure can be removed exactly, and which finite structures generate the largest gap between adaptive and fixed acquisition?

The paper should connect **exact representation reduction** to **extremal adaptive advantage**. These are two sides of the same question: what structure is genuinely necessary for contingent information acquisition to outperform a fixed resolving bundle?

## Main theorem sequence

### Theorem 1 — Exact adaptive/fixed containment and budget interval

Use `theory/ADAPTIVE_GAIN_THEOREM.md` as the foundation:

\[
C_A\le C_F.
\]

When `C_A<C_F`, the exact adaptive-only integer-budget set is

\[
\{C_A,\ldots,C_F-1\}.
\]

This is foundational rather than the main novelty claim.

### Theorem 2 — Query-side target-relevant refinement dominance

Use `theory/ADAPTIVE_SAFE_QUERY_COMPRESSION.md`.

At Bellman state `A`, if

\[
S_A(q)\supseteq S_A(r)
\]

and

\[
c(q)\le c(r),
\]

then `r` is safely removable without changing the exact adaptive optimum.

This strictly generalizes continuation equality and identifies the state-local nondominated query frontier.

### Theorem 3 — World-side target-relevant quotient

Use `theory/ADAPTIVE_WORLD_TWIN_QUOTIENT.md`.

Same-target worlds with identical remaining cross-target separation profiles can be quotient-collapsed without changing Bellman continuation value.

### Theorem 4 — Exact two-sided Bellman kernel

Use `theory/ADAPTIVE_TWO_SIDED_KERNEL.md`.

Recursive composition of world-side quotienting and query-side refinement dominance preserves the direct optimum:

\[
\boxed{C_A^{\rm two-sided}=C_A^{\rm direct}.}
\]

This is the natural central reduction theorem.

### Theorem 5 — Fixed-side weighted-cover kernel and certificate layer

Integrate the existing fixed-cover dominance/kernel and certificate machinery. The adaptive and fixed optimizers share the full identity-indexed target-pair incidence representation but admit different safe reductions downstream.

The central representation diagram is

```text
full world/outcome model
-> identity-indexed cross-target incidence
-> adaptive Bellman kernel     -> C_A
-> fixed weighted-cover kernel -> C_F.
```

This is a stronger unifying presentation than treating solver optimizations separately.

### Theorem 6 — Sharp binary gap threshold

Use the exact binary family:

\[
h_2^*(q)=\min\{h\ge1:2^h-1-h\ge q\},
\]

with first componentwise corner

\[
(n^*,m^*,E^*)=(h_2^*+q+1,h_2^*+q,h_2^*+q).
\]

Include the logarithmic routing overhead result

\[
h_2^*(q)=\log_2q+O(1).
\]

The point is not merely the formula: it identifies the smallest finite problem geometry capable of a prescribed adaptive/fixed gap.

### Theorem 7 — Bounded-arity Pareto extremals

Use `ARITY_GAP_PARETO` and related bounded-arity extremal results.

For `b>2`, exact joint complexity is generally a Pareto frontier over represented worlds, queries and productive-frontier obligations. The paper should distinguish componentwise minima from jointly attainable structures.

### Theorem 8 — Exact global balance does not bound adaptive advantage

Use `BALANCED_BINARY_UNBOUNDED_ADAPTIVE_GAIN.md`:

\[
\frac{C_F}{C_A}\ge\frac{2^d}{d+1}\to\infty
\]

even when every query is deterministic, binary, unit cost and exactly 50/50 balanced over represented worlds.

This is the clean extremal counterexample showing that low-order marginal query statistics do not control contingent value.

## Finite-profile and certificate results

The many balanced-binary finite-scope modules should not become one theorem each. Use them as a **validated extremal ladder**:

- depth-three cap results;
- depth-four sharp boundaries;
- fixed-cost caps;
- eight-/ten-/twelve-/sixteen-/eighteen-/twenty-/twenty-two-world profiles;
- saturation-depth calculations;
- constructive extremal families.

Their paper role is to show how the closed forms emerged, where finite sharpness is known, and where only constructive upper/lower bounds remain. A compact table can record `(n,m,depth)` versus certified `C_A`, `C_F`, gap/ratio, and proof type.

Do not advertise a finite-profile result as general if it is only exhaustive within its registered scope.

## Compression and symmetry results

Collect the following as representation theory around the exact kernels:

- adaptive-safe query compression;
- same-target world twins;
- bipartite color refinement;
- automorphism/symmetry reductions;
- two-sided adaptive kernel;
- fixed-side cover kernel;
- bypass-channel minimality where it establishes necessity of structural ingredients.

The story is: exact finite decision problems possess a target-relevant quotient structure that is richer than naive marginal information but smaller than the raw world/outcome description.

## Negative controls

Retain examples showing that individual ingredients are not enough:

- zero direct target information can coexist with routing value;
- positive joint target information need not imply adaptive gain if continuation action is branch invariant;
- global balance does not bound the gain;
- a bypass can erase strict gain even when routing structure exists;
- budget scarcity is necessary for an adaptive-only success interval at a fixed budget.

These controls are important because they separate four notions:

```text
direct target information
!= continuation target information
!= routing-action diversity
!= strict adaptive gain.
```

## Computational validation architecture

The companion should make the repository's proof discipline a feature rather than an appendix:

1. theorem statement;
2. constructive or combinatorial proof;
3. executable exact solver;
4. exhaustive small-universe validation where feasible;
5. witness/certificate receipt;
6. explicit cap beyond which the code does not pretend exhaustive proof.

The existing test suite and certificate ladder already implement most of this architecture.

## What stays out

Do not import the full eco-evolutionary dynamics from the Evolution Letters manuscript. The companion may use one short motivating paragraph and point back to the biological application, but its mathematical claim should stand independently.

Also exclude unless separately proved:

- noisy likelihood observations;
- expected-loss objectives;
- randomized policies;
- continuous query costs without an appropriate extension;
- calibration-changing actions;
- Bayesian experiment comparison;
- empirical prevalence claims.

## Relationship to Evolution Letters V3

The two papers should own different claims.

**Evolution Letters V3 owns:**

```text
finite architecture
-> ecological budget/selection exposure
-> structural contrast
-> feedback reachability
-> temporal filtering.
```

**Mathematical companion owns:**

```text
raw finite decision problem
-> exact target-relevant kernels
-> exact C_A and C_F geometry
-> sharp/Pareto gap extremals
-> counterexamples to naive structural summaries.
```

Cross-citation is legitimate because the companion supplies the reusable mathematical engine while the Letter supplies the evolutionary composition.

## Current readiness

Substantial theorem and implementation material already exists. The missing work is synthesis rather than theorem hunting:

- choose one canonical notation across all theorem notes;
- consolidate fixed-side kernel/certificate statements into one section;
- build a finite-profile summary table from existing validated receipts;
- perform a dedicated prior-art audit in decision-tree/adaptive query/separating-system/kernelization literature;
- write the companion manuscript around the theorem sequence above.

Stop rule: **do not invent another theorem family merely to make the companion look larger.** Use the mathematics already present and identify any genuine prior-art collision before claiming novelty.
