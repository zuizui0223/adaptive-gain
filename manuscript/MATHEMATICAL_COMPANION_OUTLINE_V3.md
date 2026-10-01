# Mathematical companion outline v3 — exact-balanced finite search

Status: revised companion architecture after the 2026-10-01 priority audit. The paper is now organized around one constrained combinatorial-search problem rather than generic adaptivity.

## Working title

**Adaptive target resolution under exactly balanced binary queries**

Alternative:

**Exact-balanced query systems: fixed separation and adaptive depth**

## Central problem

Let the represented state set have even size n. Every available query is:
- deterministic;
- binary;
- unit cost;
- globally exactly balanced, with n/2 states on each outcome.

Let:
- C_A be minimum worst-case adaptive target-resolution cost;
- C_F be minimum fixed resolving-set cost.

Question:

> How does exact global balance constrain the largest fixed burden compatible with a given adaptive depth, and can perfect balance uniformly limit the value of adaptivity?

This question sits between classical uniform separating systems and adaptive combinatorial search.

---

## Section 1 — Model and prior-art boundary

Define finite target resolution and explain that full identity search is a special case.

Connect explicitly to:
- separating systems / Test Cover;
- adaptive and k-round combinatorial search;
- uniform separating systems.

State that:
- adaptive vs non-adaptive search is classical;
- exact half-size blocks are classical;
- generic complete binary-tree geometry is classical.

The paper studies their **joint extremal geometry under exact global balance**.

---

## Section 2 — Fixed-side extremum under exact balance

### Theorem 1 — sharp balanced fixed-cost cap

For even n:

max C_F =
- 1 at n=2;
- 2 at n=4;
- n-3 for n>=6.

### Proof

Use:
1. private cross-target pair for each member of a minimum fixed resolver;
2. selected private-pair graph;
3. every selected edge is the unique edge of a query cut;
4. hence every edge is a bridge and the graph is a forest;
5. exact balance excludes one- and two-component extremizers;
6. construct the n-3 star--edge--star witness.

This should be the first true theorem of the paper.

---

## Section 3 — Equality structure and its adaptive cost

### Theorem 2 — cap saturation normal form

For n=2h>=8, if C_F=n-3, then every minimum fixed resolver B can be normalized to a private-pair forest with component sizes

{h-1, 2, h-1}

and the large components are stars.

The balanced rows of B are then forced up to world relabeling and outcome complementation.

### Theorem 3 — adaptive depth forced by saturation

If the declared vocabulary is exactly the saturated minimum resolver B, with no external balanced queries, then:

C_A >= h-1 = n/2-1,

and equality is attainable.

Interpretation:

> the most irredundant globally balanced fixed systems are not adaptively easy.

This sets up the rest of the paper: reducing adaptive depth requires extra balanced queries, but those extra queries must not lower C_F.

---

## Section 4 — Exact adaptive-depth envelopes

Define

D_h(n)=max{C_F : C_A<=h}

over exact-balanced binary unit-cost tasks.

### Theorem 4 — complete depth-three envelope

For every even n>=6:

D_3(6)=3,
D_3(8)=5,
D_3(10)=6,
D_3(n)=7 for every even n>=12.

Highlight the unique finite defect:

D_3(10)=6 < min{7,10-3}=7.

Explain the n=10 obstruction:
- complete depth-three flattening would require seven distinct internal labels;
- fixed minimality forces private-edge geometry;
- exact 5/5 balance on the non-root rows is incompatible with the required private edges.

At n=12 the full seven-query depth-three tree becomes feasible again.

### Theorem 5 — depth-four frontier

Give the closed values:

D_4(12)=8,
D_4(14)=10,
D_4(16)=12,
D_4(18)=13,
D_4(n)=15 for every even n>=20.

Use one concise proof template:
- normalize a hypothetical cap/near-cap minimum fixed resolver;
- classify identity-safe external balanced queries;
- exhaust permitted external-query subsets / mandatory pairs;
- prove depth infeasibility at the excluded endpoint.

The 20-world (4,15) construction is the visible saturation example.

### Theorem 6 — selected depth-five sharp values

Report:

D_5(16)=12,
D_5(18)=14,
D_5(22)=17.

These show that increasing adaptive depth need not improve the fixed-side extremum immediately, but can recover additional burden at larger n.

Do not attempt a complete D_5(n) theorem before submission. Record D_5(24) as an open problem.

---

## Section 5 — finite fixed-m ratio profiles

Use the exact n=4,6,8,10,12 profiles as a compact table, not as separate theorems.

Key rows:

- n=4: maximum ratio 1;
- n=6: maximum ratio 3/2;
- n=8: 1,1,3/2,3/2,5/3,5/3,...;
- n=10: 1,1,3/2,3/2,5/3,2,2,...;
- n=12: 1,1,3/2,3/2,5/3,2,7/3,7/3,...

Main message:

> exact balance imposes genuine finite-size penalties and compatibility defects, not merely a smooth rescaling of the unrestricted binary bound.

---

## Section 6 — asymptotic counterpoint

### Theorem 7 — exact balance does not uniformly bound adaptivity

Construct routing depth d tasks with every query exactly 50/50 balanced and

C_F >= 2^d,
C_A <= d+1.

Therefore

C_F/C_A >= 2^d/(d+1) -> infinity.

This is the capstone.

The finite sections establish that balance strongly constrains small finite systems; the final theorem shows that these constraints do not yield a uniform adaptivity bound as size grows.

---

## Section 7 — Discussion

Three mathematical conclusions:

1. **Uniform balance changes finite extremal geometry.**
   The fixed-side maximum drops from n-1 to n-3 and equality is structurally rigid.

2. **Fixed extremality and adaptive ease are incompatible without extra structure.**
   Star--edge--star saturation forces large adaptive depth; extra balanced queries are needed to escape it.

3. **Perfect marginal balance is not a global proxy for contingent value.**
   Despite finite restrictions, the adaptive/fixed ratio is asymptotically unbounded.

Use "branch-exclusive separation geometry" as interpretation, but keep the paper mathematical.

---

## Baseline results to move to preliminaries or supplement

- generic C_A<=C_F;
- generic C_F<=min{m,n-1,2^C_A-1};
- generic sharp fixed-(n,m) formula;
- prescribed-gap inverse formulas;
- target-relevant kernels;
- LP/certificate ladder.

They remain useful but should not compete with the balanced theorem family.

---

## Computational proof discipline

For finite exclusion theorems, every computational claim must state:
- normalized search space;
- symmetry reduction;
- exact count of cases;
- exact DP/certificate criterion;
- independent witness for the lower bound;
- scope ceiling beyond which no exhaustive claim is made.

The paper must sharply distinguish:
- analytic theorem;
- exhaustive finite theorem;
- constructive lower bound;
- open row.

---

## Figures

### Figure 1
Private-pair forest proof of the n-3 fixed cap and the star--edge--star equality case.

### Figure 2
D_3(n), D_4(n), and selected D_5(n) values against generic upper envelopes.

### Figure 3
Finite-to-asymptotic contrast:
small-n balance penalties versus the exactly-balanced unbounded-ratio family.

No ecological figure is needed.

---

## Open problems

Keep only a short final list:

1. full exact-balanced sharp fixed-(n,m) ratio for all even n;
2. general formula/structure for D_h(n);
3. characterization of finite compatibility defects;
4. extension from exact binary half-balance to bounded imbalance or multiway equal-part queries.

Do not solve these before writing the current paper.

## Stop rule

**The mathematical content is sufficient.**
Complete only:
- prior-art audit of the balanced theorem family;
- one corrected finite-profile table;
- manuscript synthesis and proof compression.
