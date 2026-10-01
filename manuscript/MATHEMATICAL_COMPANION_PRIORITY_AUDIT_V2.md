# Mathematical companion priority audit v2

Date: 2026-10-01  
Status: dedicated combinatorial/decision-theory boundary audit for the mathematical companion. This file does not modify the frozen Evolution Letters V5 submission surface.

## Executive decision

The mathematical companion should not claim novelty for:

- adaptive versus non-adaptive search as a general distinction;
- one-round/non-adaptive test cover versus multi-round/adaptive combinatorial search;
- separating systems, minimum test set/test cover, or optimal decision trees;
- generic adaptivity gaps;
- binary search / threshold-search constructions;
- bounded-outcome decision trees as a model class;
- elementary rooted-tree counting;
- generic kernelization, dominance, LP duality, or reversible-Markov spectral formulas.

The companion should instead concentrate its novelty audit on three exact results that are substantially narrower than those classical frameworks:

1. **sharp fixed-(n,m) binary unit-cost ratio in the declared target-resolution model;**
2. **exact/Pareto finite architecture required for a prescribed adaptive-fixed gap;**
3. **unbounded adaptive advantage under exact 50/50 balance of every binary query.**

No categorical priority claim is currently licensed. The correct status is **no exact predecessor located in the targeted search so far**.

---

## 1. Newly strengthened prior-art boundary: combinatorial search already unifies adaptive and non-adaptive identification

A closer literature than the earlier audit had emphasized is the general theory of combinatorial search on separating set systems / hypergraphs.

A representative source is:

- G. Wiener. 2009. *Rounds in Combinatorial Search*. Dagstuhl Seminar Proceedings 09281. DOI: 10.4230/DagSemProc.09281.6.
- G. Wiener et al. 2019. *Combinatorial search in two and more rounds*. Theoretical Computer Science 780:1-11. DOI: 10.1016/j.tcs.2019.02.004.

That literature defines, on the same separating system, worst-case:
- fully adaptive search complexity;
- one-round/non-adaptive complexity;
- intermediate k-round complexities.

The one-round problem is explicitly the Test Cover problem.

Therefore the companion must not imply that placing fixed resolving sets and adaptive decision trees into one common finite identification model is itself new. It is classical combinatorial-search structure.

This also means that threshold-path / binary-search witnesses should be presented as extremizers for the repository's **particular objective and parameterization**, not as discovery of an adaptive/non-adaptive separation phenomenon.

---

## 2. Candidate theorem A: sharp fixed-(n,m) binary unit-cost ratio

Repository theorem:

Let

\[
K=\min(m,n-1),\qquad
d=\lfloor\log_2(K+1)\rfloor.
\]

Then in the declared finite deterministic target-resolution model with binary unit-cost queries,

\[
\max \frac{C_F}{C_A}
=
\max\left(
1,
\frac{2^d-1}{d},
\frac{K}{d+1}
\right).
\]

The maximum is attained by explicit alternating-target threshold tasks.

### What is prior art

The following ingredients are classical or clearly adjacent prior art:

- binary decision trees;
- worst-case adaptive identification;
- non-adaptive separating systems / test cover;
- binary search on ordered hypotheses;
- large adaptive/non-adaptive gaps in query models;
- optimization of decision-tree depth.

### What remains potentially original

The targeted search did **not** locate an exact predecessor proving this same closed-form extremum for the ratio

\[
C_F/C_A
\]

as a function only of

\[
(n,m)
\]

under the repository's target-resolution contract, together with attainment and the observation that the answer depends on the resource cap only through

\[
K=\min(m,n-1).
\]

This is therefore a legitimate **priority-audit target** for the companion.

### Required claim wording

Use:

> In our finite deterministic target-resolution formulation, the binary unit-cost fixed-(n,m) extremal ratio has the following exact form ...

Avoid:

> We discover the adaptivity gap for decision trees.

The latter is false as a priority statement.

### Remaining collision risk

Moderate.

The formula may exist implicitly in older combinatorial-search or decision-tree literature under different notation. Before publication, search specifically for exact extremal relations among:
- test-cover number;
- worst-case decision-tree depth;
- number of hypotheses/items;
- number of available tests.

---

## 3. Candidate theorem B: prescribed-gap architecture and bounded-arity Pareto geometry

Repository theorem:

For binary unit-cost sensing and required integer structural gap q,

\[
h_2^*(q)=\min\{h\ge1:2^h-1-h\ge q\},
\]

and the first componentwise gap-capable corner is

\[
(n^*,m^*,E^*)
=
(h_2^*(q)+q+1,\,
 h_2^*(q)+q,\,
 h_2^*(q)+q).
\]

For maximum query arity b>2, separate minima need not be jointly attainable; the exact requirement becomes a Pareto frontier over represented worlds, query resources, and irreducible fixed-side obligations.

### What is prior art

- rooted-tree internal-node bounds;
- bounded-outdegree/multiway decision trees;
- test-cover/separating-system lower bounds;
- Pareto optimization as a general concept.

### What remains potentially original

The audit has not located a predecessor that treats a **required adaptive-minus-fixed gap q** as the inverse design target and maps it to an exact or Pareto-minimal finite structural requirement over the repository coordinates

\[
(n,m,E).
\]

The mathematical interest is the reverse extremal problem:

> how small can a finite problem be while supporting a prescribed adaptivity advantage?

rather than merely:
> how large can the advantage be for a fixed problem size?

That reverse formulation is a cleaner independent target than the downstream eco-evolutionary use.

### Required claim wording

Use:

> We solve the inverse finite-architecture problem for a prescribed adaptive-fixed gap within this model.

Avoid claiming novelty for the rooted-tree recurrence or for bounded-arity counting itself.

### Remaining collision risk

Low-to-moderate, but terminology-dependent.

A close result could appear under:
- minimum-size instance realizing a given adaptivity gap;
- extremal separating systems;
- round complexity versus test-cover number;
- decision-tree versus test-set complexity.

---

## 4. Candidate theorem C: exact global balance does not bound adaptive advantage

Repository theorem:

There exists a family of finite deterministic binary unit-cost tasks in which **every declared query is exactly 50/50 balanced over represented worlds**, yet

\[
C_F\ge 2^d,\qquad
C_A\le d+1,
\]

and hence

\[
\frac{C_F}{C_A}
\ge
\frac{2^d}{d+1}
\to\infty.
\]

### Why this is the strongest clean counterexample

Generic large adaptivity gaps are well known. The extra restriction here is the point:

- every query is binary;
- every query has unit cost;
- every query is exactly globally balanced;
- exact target resolution is still guaranteed;
- the fixed/adaptive ratio remains unbounded.

Thus marginal split balance, even when perfect for every available query, does not control contingent value.

The obstruction is branch-exclusive separation geometry, not marginal imbalance.

### Targeted search result

The search located extensive prior art on:
- adaptive versus non-adaptive property testing;
- combinatorial search and test cover;
- binary and multiway decision trees;
- group testing;
- query-balance heuristics.

It did **not** locate an exact predecessor for the statement that *every available binary test can be globally 50/50 balanced while the fixed/adaptive worst-case ratio remains unbounded* in this finite target-resolution setting.

This is the companion's **strongest current standalone novelty candidate**.

### Required claim wording

Use:

> Exact marginal balance of every binary query does not uniformly bound the adaptive advantage.

Until a deeper priority search is complete, avoid:
- first;
- first example;
- previously unknown.

### Remaining collision risk

Moderate.

Balanced-split decision-tree literature is large, and an equivalent construction may exist under different language such as:
- equipartition tests;
- balanced questions;
- twenty-questions variants;
- parallel versus sequential search.

This theorem merits the deepest dedicated literature search of the three.

---

## 5. Results that should remain supporting rather than mathematical headlines

### Exact containment

\[
C_A\le C_F
\]

is immediate class containment.

### Hard-budget interval

\[
C_A\le B<C_F
\]

is an exact and useful biological corollary, but not a deep mathematical theorem.

### Target-relevant quotient/kernel

The exact Bellman-preserving reduction is useful and may be publishable as part of the framework, but dominance/quotient reductions are too close to established dynamic-programming and decision-tree reduction ideas to carry the paper's priority claim without a separate audit.

Its strongest role is structural:
- remove raw distinctions that are irrelevant to the declared target;
- expose the reduced geometry on which the extremal theorems act.

### Nonlinear eco-evolutionary no-go

The monotone-Lipschitz composition is valuable for the ecological paper because it removes dependence on an exact linear lift. Mathematically, however, the core step is composition of a Lipschitz upper bound with a downstream threshold. It should not anchor the mathematical companion.

### Spectral recurrence results

Reversible Markov reward decompositions, Popoviciu bounds, and spectral amplification factors are standard. Their composition with repository-native structural rewards is useful biologically but is not the mathematical companion's strongest independent contribution.

---

## 6. Revised companion theorem spine

The companion should be shorter and more mathematical than the current eight-theorem outline.

### Part I — Model and exact reduction

1. finite target-resolution model;
2. adaptive cost C_A and fixed cost C_F;
3. exact target-relevant world/query kernel;
4. fixed-side pair-cover representation.

These establish the common object but are not advertised as the primary novelty.

### Part II — Exact extremal geometry

**Theorem 1. Sharp fixed-(n,m) binary unit-cost ratio.**

\[
\max C_F/C_A
=
\max\left(1,(2^d-1)/d,K/(d+1)\right).
\]

**Theorem 2. Inverse prescribed-gap architecture.**

Exact binary corner and bounded-arity Pareto frontier for a required gap q.

**Theorem 3. Balanced-query counterexample.**

Exact 50/50 balance of every binary query does not bound the ratio.

### Part III — finite profiles and certificates

Use exhaustive small-scope results only as:
- verification;
- finite sharpness maps;
- examples of where general formulas change regime.

Do not create one theorem per finite profile.

### Part IV — implications

One short section:
- marginal balance is not enough;
- raw instance size is not enough;
- target-relevant branch/resource geometry is the controlling object.

No eco-evolutionary dynamics are needed for the mathematical claim.

---

## 7. Priority-search checklist still required

Before any mathematical submission:

- [ ] search classical books/monographs on combinatorial search for extremal relations between c(H) and c_na(H);
- [ ] search Aigner-style combinatorial search literature for exact ratios conditional on number of items/tests;
- [ ] search older decision-tree surveys and Moret/Shapiro minimum-test-set work for the fixed-(n,m) formula;
- [ ] search balanced-question / equipartition / twenty-questions literature for the 50/50 theorem;
- [ ] search multi-round Test Cover for inverse prescribed-gap/minimum-instance results;
- [ ] search multiway decision-tree literature for an equivalent Pareto statement;
- [ ] after those searches, record either an exact collision or a conservative no-collision result.

Non-discovery is not a proof of novelty.

---

## 8. Current verdict

The mathematics is strong enough to justify a separate companion **if** the three highlighted results survive the dedicated priority search.

Current confidence ranking:

1. **exactly-balanced binary unbounded advantage** — strongest conceptual standalone result;
2. **sharp fixed-(n,m) binary ratio** — strongest closed-form extremal result;
3. **prescribed-gap exact/Pareto architecture** — strongest inverse-design result.

The remaining mathematics is valuable infrastructure or ecological composition, not equal-priority mathematical novelty.

Stop rule:

> Do not add a fourth theorem family. Resolve priority for these three, then write the companion around them.
