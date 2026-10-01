# Mathematical companion outline v2 — extremal geometry of adaptive target resolution

Status: revised companion architecture after the 2026-10-01 priority audit. This outline narrows the paper to three mathematical headline results. It does not modify the frozen Evolution Letters V5 submission surface.

## Working title

**Extremal gaps in finite adaptive target resolution**

Alternative:

**Exact extremal geometry of adaptive and fixed finite identification**

## Central question

For a finite deterministic target-resolution problem with positive additive query costs,

> how large can the advantage of adaptive query selection be, what is the smallest finite architecture that can support a prescribed advantage, and which simple summaries fail to control that advantage?

The paper compares:
- \(C_A\): minimum worst-case adaptive query cost;
- \(C_F\): minimum fixed resolving-set cost.

The general distinction between adaptive and non-adaptive search is prior art. The paper is about the exact extremal geometry of this declared target-resolution formulation.

---

## Part I. Common finite model

### 1. Target resolution rather than full identification

Define worlds, target labels, deterministic query outcomes, positive additive query costs, and guaranteed worst-case target resolution.

Emphasize that worlds with the same target need not be mutually distinguished.

### 2. Adaptive and fixed costs

Define \(C_A\) by Bellman recursion and \(C_F\) by the fixed cross-target separation cover.

Record

\[
C_A\le C_F
\]

as foundation, not headline novelty.

### 3. Exact target-relevant reduction

Present the two-sided adaptive kernel compactly:
- same-target world quotient;
- query refinement dominance;
- recursive preservation of \(C_A\).

Present the fixed side as a cross-target pair-cover problem with standard dominance/certificate machinery.

Purpose: expose the reduced structural object on which the extremal results act.

---

## Part II. Headline theorem 1 — sharp fixed-(n,m) binary extremum

Assume deterministic binary unit-cost queries.

Let

\[
K=\min(m,n-1),\qquad
d=\lfloor\log_2(K+1)\rfloor.
\]

Then

\[
\boxed{
\max \frac{C_F}{C_A}
=
\max\left(
1,
\frac{2^d-1}{d},
\frac{K}{d+1}
\right)
}
\]

over the declared finite target-resolution class.

### Proof architecture

1. Flatten an optimal adaptive tree:
   \[
   C_F\le\min\{m,n-1,2^{C_A}-1\}.
   \]
2. Optimize
   \[
   \min\{K,2^h-1\}/h
   \]
   over integer depth \(h\).
3. Show only the two depths straddling saturation can be optimal.
4. Attain both candidate branches using alternating-target threshold paths.

### Corollaries

- exact first scope above ratio \(3/2\);
- dependence only on \(K=\min(m,n-1)\);
- extra worlds beyond \(m+1\), or extra queries beyond \(n-1\), cannot improve the extremal ratio.

### Claim boundary

Binary search and threshold queries are classical. The candidate contribution is the exact fixed-\((n,m)\) extremal formula and attainment within this target-resolution objective.

---

## Part III. Headline theorem 2 — inverse architecture for a prescribed gap

Let the required additive gap be

\[
q=C_F-C_A\ge1.
\]

### Binary unit-cost corner

Define

\[
h_2^*(q)
=
\min\{h\ge1:2^h-1-h\ge q\}.
\]

Then the first componentwise gap-capable architecture is

\[
\boxed{
(n^*,m^*,E^*)
=
(h_2^*(q)+q+1,,
 h_2^*(q)+q,,
 h_2^*(q)+q)
}
\]

with

\[
h_2^*(q)=\log_2 q+O(1).
\]

Interpretation:

> routing depth grows only logarithmically while the fixed-side mandatory burden grows essentially linearly with the requested gap.

### Bounded arity

For maximum outcome arity \(b\ge2\),

\[
h_b^*(q)
=
\min\left\{
h\ge1:
\frac{b^h-1}{b-1}-h\ge q
\right\}.
\]

For \(b>2\), separate minima need not be jointly attainable. The exact inverse requirement is therefore a Pareto frontier over finite architecture coordinates.

Use \(q=3,b=4\) as the canonical visible example:

\[
(7,6,6),\qquad(8,5,5)
\]

are nondominated.

### Claim boundary

Do not claim novelty for rooted-tree counting or generic Pareto optimization. The candidate contribution is the exact inverse problem: minimum/Pareto-minimal finite architecture supporting a prescribed adaptive-fixed gap.

---

## Part IV. Headline theorem 3 — perfect global balance does not control adaptive value

Construct a family indexed by routing depth \(d\) such that:

- every query is binary;
- every query has unit cost;
- every query is exactly 50/50 balanced over represented worlds;
- exact target resolution is guaranteed;
- yet
  \[
  C_F\ge2^d,
  \qquad
  C_A\le d+1.
  \]

Hence

\[
\boxed{
\frac{C_F}{C_A}
\ge
\frac{2^d}{d+1}
\to\infty.
}
\]

### Main conceptual consequence

Marginal split balance is not the structural quantity controlling adaptive value.

Perfectly balanced tests can still hide branch-exclusive separation obligations that a fixed resolver must provision simultaneously while an adaptive policy pays only for the realized branch.

### Why this belongs last

The first two theorems characterize the extremal geometry. This theorem then destroys a natural low-order summary that might appear to explain it.

---

## Part V. Exact finite profiles as verification, not headline theorems

Compress the existing finite-scope results into one table with columns:

- worlds \(n\);
- queries \(m\);
- arity;
- certified \(C_A\);
- certified \(C_F\);
- ratio;
- gap;
- proof type: closed form / exhaustive exact solver / certificate / construction only.

Use the table to show:
- agreement with the closed-form theorems;
- finite transition points;
- where balanced-subclass sharpness is known;
- where only constructive bounds are currently claimed.

Do not promote each profile to a named theorem.

---

## Part VI. Exact reductions and certificates

One compact section only.

### Adaptive side
- same-target world quotient;
- query refinement dominance;
- two-sided Bellman kernel.

### Fixed side
- cross-target pair cover;
- private-pair certificates;
- integral packing;
- fractional dual lower bounds;
- exact integer cover where needed.

The paper should emphasize proof discipline rather than software novelty:

\[
\text{theorem}
\to
\text{construction/proof}
\to
\text{exact solver}
\to
\text{small-scope exhaustive validation}
\to
\text{certificate receipt}.
\]

---

## Part VII. Discussion

Three take-home mathematical statements:

1. **instance size alone does not determine adaptive advantage; exact finite geometry does;**
2. **a prescribed adaptivity gap has an inverse minimum-architecture problem;**
3. **perfect marginal balance does not control contingent value.**

The unifying object is branch-exclusive separation geometry after target-relevant reduction.

Avoid importing the full eco-evolutionary dynamics. One paragraph may explain that the mathematics was motivated by ecological decision architecture, but the companion should stand without the biological lift.

---

## Prior-art boundary

The manuscript must explicitly cite combinatorial-search work in which adaptive, non-adaptive, and limited-round identification are already defined on the same separating system.

At minimum include:
- classical separating systems / Test Cover;
- Aigner-style combinatorial search;
- Wiener 2009 on rounds in combinatorial search;
- Wiener et al. 2019 on two and more rounds;
- multiway decision-tree literature;
- modern adaptive Test Cover where relevant.

The dedicated status file is:

`manuscript/MATHEMATICAL_COMPANION_PRIORITY_AUDIT_V2.md`.

No categorical priority wording until that audit is closed.

---

## Exclusions

Do not add:
- noisy observations;
- expected-loss variants;
- randomized policies;
- stochastic Boolean-function evaluation;
- Bayesian design;
- eco-evolutionary dynamics;
- another theorem family.

Those are separate research programs.

## Stop rule

**Resolve the priority of the three headline theorems, build the finite-profile table, and write. Do not search for a fourth mathematical headline.**
