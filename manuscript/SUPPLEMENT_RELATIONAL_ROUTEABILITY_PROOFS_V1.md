# Supplementary proofs for relational routeability v1

Status: formal proof companion for manuscript/MANUSCRIPT_RELATIONAL_ROUTEABILITY_V0_3_AMNAT.md.

## S1. Finite deterministic task

A task consists of:

- finite represented states \(W\);
- target/action map \(T:W\to\mathcal A\);
- finite cue vocabulary \(Q\);
- positive additive cue costs \(c(q)\);
- deterministic cue outcomes \(q(w)\).

A fixed resolving set \(S\subseteq Q\) must separate every pair \(x,y\in W\) such that \(T(x)\ne T(y)\).

Its minimum cost is

\[
C_F.
\]

An adaptive policy is a decision tree whose internal nodes are cues and whose outgoing edges are cue outcomes. Every leaf must be target-pure.

Its minimum worst-case root-to-leaf cost is

\[
C_A.
\]

Because any fixed resolving bundle is a feasible adaptive policy that ignores intermediate outcomes,

\[
C_A\le C_F.
\]

---

## S2. Relational routeability theorem

### Construction

Fix integer

\[
d\ge2,\qquad k=2^d.
\]

Create target-mixed branch pairs

\[
(a_i,b_i),\qquad i=0,\ldots,k-1,
\]

plus two dummy states.

The shared physical cue environment contains:

- \(d\) binary routing-bit cues;
- \(k\) branch-terminal cues.

Every cue has unit cost and is exactly globally balanced over the \(2k+2\) represented states.

The physical cue matrix is identical in both target maps below.

### Routeable target map

Assign

\[
T_R(a_i)=0,\qquad T_R(b_i)=1
\]

for every branch, and assign target 0 to both dummy states.

#### Adaptive upper bound

Read all \(d\) routing bits.

They identify branch \(i\).

Then read terminal \(t_i\).

Therefore

\[
C_A(T_R)\le d+1.
\]

#### Fixed lower bound

For pair \((a_i,b_i)\):

- every routing cue has the same outcome on both states;
- every terminal \(t_j\), \(j\ne i\), has the same outcome on both states;
- only \(t_i\) separates the pair.

Thus \(t_i\) is mandatory in every fixed resolver.

This holds for all \(i\), so

\[
C_F(T_R)\ge k=2^d.
\]

Hence

\[
\frac{C_F(T_R)}{C_A(T_R)}
\ge
\frac{2^d}{d+1}.
\]

### Matched control target map

Let \(q_0,q_1\) denote the first two routing bits.

Define

\[
T_K(w)=
\begin{cases}
0,&q_0(w)=q_1(w),\\
1,&q_0(w)\ne q_1(w).
\end{cases}
\]

The pair \((q_0,q_1)\) resolves the control target, so

\[
C_A(T_K)\le2,\qquad C_F(T_K)\le2.
\]

No single cue can resolve \(T_K\).

Every declared cue is exactly balanced and therefore has outcome classes of size

\[
k+1,\ k+1.
\]

The control target multiplicities are

\[
k+2,\ k.
\]

If one binary cue resolved the target, its two outcome classes would have to coincide with the two target classes up to outcome relabeling, which is impossible because their cardinalities differ.

Thus

\[
\boxed{
C_A(T_K)=C_F(T_K)=2.
}
\]

### Matched quantities

The two tasks have the same:

- represented states;
- physical cue matrix;
- cue identities;
- cue costs;
- cue-only probability distribution under a uniform state prior.

Because the physical cue matrix is identical, every marginal and joint distribution involving only cue variables is identical.

The two target maps have the same multiplicities

\[
(k+2,k),
\]

hence the same target entropy.

The full vocabulary resolves the target in each task, so

\[
H(T\mid Q_{\mathrm{all}})=0.
\]

Therefore

\[
I(T;Q_{\mathrm{all}})
=
H(T)
\]

for both tasks, and the total full-vocabulary target information is equal.

Combining the cost results:

\[
\boxed{
\frac{C_F(T_R)}{C_A(T_R)}
-
\frac{C_F(T_K)}{C_A(T_K)}
\ge
\frac{2^d}{d+1}-1
\to\infty.
}
\]

---

## S3. Exact common-budget corollary

Set

\[
B=d+1.
\]

For \(d\ge2\),

\[
2^d>d+1.
\]

Hence

\[
C_A(T_R)\le B<C_F(T_R).
\]

The routeable task is therefore guaranteed resolvable by contingent acquisition but not by any fixed bundle of cost at most \(B\).

For the control,

\[
C_A(T_K)=C_F(T_K)=2\le d+1=B.
\]

Thus both access modes guarantee resolution.

Define binary guaranteed-resolution indicators:

\[
S_{X,Y}
=
1
\]

if architecture \(X\) under access mode \(Y\) is guaranteed resolvable at budget \(B\), and zero otherwise.

Then

\[
(S_{R,A},S_{R,F},S_{K,A},S_{K,F})
=
(1,0,1,1),
\]

so

\[
\boxed{
(S_{R,A}-S_{R,F})
-
(S_{K,A}-S_{K,F})
=
1.
}
\]

This is a feasibility interaction, not a behavioral effect size.

---

## S4. Finite pairwise-information matched controls

The asymptotic relational construction does not preserve named target-cue pairwise association.

Two finite registered controls strengthen the matching.

For each target-cue pair, form its binary \(2\times2\) contingency table and canonicalize it under independent 0/1 relabeling of target and cue.

Compare the multiset of these canonical signatures across all cues.

### Routing depth 2

The registered control has:

- same physical cue matrix as the routeable task;
- same target multiplicities;
- same multiset of canonical target-cue contingency signatures;
- exact
  \[
  C_A=C_F=2.
  \]

### Routing depth 3

The registered control has:

- same physical cue matrix;
- same target multiplicities;
- same multiset of canonical target-cue contingency signatures;
- exact
  \[
  C_A=C_F=3.
  \]

These are finite constructive controls.

No asymptotic family preserving the named target-cue pairwise matrix is claimed.

Executable sources:

- adaptive_gain/balanced_pairwise_information_controls.py
- tests/test_balanced_pairwise_information_controls.py
- validation/balanced_pairwise_information_controls_v1.json

---

## S5. Exact-balanced ten-state stress test

Use routing depth

\[
d=2,\qquad k=4.
\]

There are:

- ten represented states;
- six binary unit-cost cues;
- every cue exactly 5/5 balanced.

### Routeable architecture

The two routing bits identify one of four branches, after which the corresponding terminal cue resolves the target.

The exact solver gives

\[
C_A=3.
\]

Each of the four terminal cues is mandatory for one target-mixed pair, and all four terminals resolve the target.

Therefore

\[
C_F=4.
\]

### Matched control

The target is equality versus inequality of the two routing bits.

Thus

\[
C_A=C_F=2.
\]

### Uniform-state contingent schedule

Use:

1. route bit 0;
2. route bit 1;
3. branch-specific terminal.

This resolves both architectures exactly, giving accuracy ceiling

\[
1.
\]

### Best fixed three-cue accuracy

Enumerate all three-cue subsets.

For each bundle, group states by observed cue pattern and classify each unresolved group by its majority target under the uniform state distribution.

The best routeable fixed three-cue bundle attains

\[
\frac45.
\]

The control has a perfect fixed three-cue bundle and therefore ceiling

\[
1.
\]

Hence the exact deterministic ceiling interaction is

\[
\boxed{
\left(1-\frac45\right)-(1-1)=\frac15.
}
\]

Executable sources:

- adaptive_gain/exact_balanced_routeability_stress_test.py
- tests/test_exact_balanced_routeability_stress_test.py
- validation/exact_balanced_routeability_stress_test_v1.json

---

## S6. Scope of computational claims

The theorem in S2 and corollary in S3 are analytic.

The finite pairwise controls in S4 and ten-state ceiling in S5 are constructive finite results checked by exact enumeration/solvers.

Focused CI covers:

- Python 3.10;
- Python 3.11;
- Python 3.12.

The dedicated workflow is:

- .github/workflows/quantity-topology-smoke.yml

The repository-wide workflow currently contains an unrelated legacy manuscript phrase assertion failure. This does not invalidate the focused mathematical checks.

---

## S7. Claim boundaries

The supplement does not establish:

- stochastic optimality under noisy cues;
- expected-loss optimality;
- empirical behavioral effect sizes;
- natural prevalence of exact-balanced cue systems;
- evolved niche breadth;
- diversity-stability consequences;
- community resilience or ecosystem-function stability.

Those claims require additional biological or stochastic models.

## Reproducibility map

Headline theorem:
- theory/RELATIONAL_ROUTEABILITY_THEOREM_SPINE_V1.md
- theory/QUANTITY_TOPOLOGY_ORTHOGONALITY.md
- adaptive_gain/balanced_quantity_topology_contrast.py
- tests/test_balanced_quantity_topology_contrast.py
- validation/balanced_quantity_topology_contrast_v1.json

Pairwise controls:
- adaptive_gain/balanced_pairwise_information_controls.py
- tests/test_balanced_pairwise_information_controls.py
- validation/balanced_pairwise_information_controls_v1.json

Ten-state stress test:
- adaptive_gain/exact_balanced_routeability_stress_test.py
- tests/test_exact_balanced_routeability_stress_test.py
- validation/exact_balanced_routeability_stress_test_v1.json
