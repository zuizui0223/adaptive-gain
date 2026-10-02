# Supplementary proofs for relational routeability v1

Status: formal proof companion for manuscript/MANUSCRIPT_RELATIONAL_ROUTEABILITY_V0_4_INFORMATION_ACCESS.md.

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

## S6. Static information exactly characterizes fixed resolution

Give every represented state strictly positive probability.

For any fixed cue bundle \(S\),

\[
S\text{ resolves }T
\iff
H(T\mid Q_S)=0
\iff
I(T;Q_S)=H(T).
\]

Therefore

\[
\boxed{
C_F=
\min_{S\subseteq Q}
\left\{
c(S):I(T;Q_S)=H(T)
\right\}.
}
\]

The equivalence is structural rather than prior-dependent: under any
full-support prior, a nonresolving bundle leaves at least one observed cue
signature containing two different targets with positive conditional mass.

Executable source:

- adaptive_gain/information.py::fixed_information_minimum_cost

---

## S7. Complete Shannon entropic equivalence does not determine adaptive cost

Use the common 12-state, four-cue physical environment encoded in
\`adaptive_gain/static_information_adaptive_separation.py\`.

Every cue is exactly 6/6 balanced. Two target maps \(T_A,T_B\) have identical
target multiplicities \((8,4)\).

For every named cue subset \(S\),

\[
I(T_A;Q_S)=I(T_B;Q_S).
\]

Because the cue-only distribution is physically identical,

\[
H_A(Q_S)=H_B(Q_S),
\]

and the exact conditional-entropy fingerprints also match. Hence for every
subset \(U\) of the five variables \((T,q_0,q_1,q_2,q_3)\),

\[
\boxed{
H_A(U)=H_B(U).
}
\]

Nevertheless exact optimization gives

\[
(C_A,C_F)_A=(4,4),
\qquad
(C_A,C_F)_B=(3,4).
\]

The entropy equalities are certified without floating point by expressing
\(12H(T\mid Q_S)\) and the relevant joint entropies as integer combinations of
\(\log_2 p\) over prime \(p\).

### Direct-product amplification

Take \(r\) independent coordinate copies. Queries act only within one
coordinate and the composite target is the tuple of coordinate targets.

Entropy is additive across coordinates, so complete Shannon entropic
equivalence is preserved.

Fixed and adaptive exact-resolution costs are additive:

\[
C_F(X\otimes Y)=C_F(X)+C_F(Y),
\]

\[
C_A(X\otimes Y)=C_A(X)+C_A(Y).
\]

For \(C_F\), each coordinate must remain resolved after all other coordinates
are held fixed.

For \(C_A\), every query preserves rectangular support across coordinates.
Induction in the Bellman recursion therefore gives a continuation value equal
to the sum of coordinate continuation values.

Thus

\[
(C_A,C_F)_{A^{\otimes r}}=(4r,4r),
\]

\[
(C_A,C_F)_{B^{\otimes r}}=(3r,4r),
\]

and

\[
\boxed{
C_A(A^{\otimes r})-C_A(B^{\otimes r})=r\to\infty.
}
\]

This is an unbounded **additive** separation under complete Shannon
entropy-vector matching. The exact-balanced family in S2 supplies an unbounded
**multiplicative** \(C_F/C_A\) ratio under weaker information matching.

Executable sources:

- adaptive_gain/static_information_adaptive_separation.py
- tests/test_static_information_adaptive_separation.py
- validation/static_information_adaptive_separation_v1.json

---

## S8. Outcome-resolved Bellman object for adaptive accessibility

For a realized history

\[
h=(q_1=a_1,\ldots,q_r=a_r),
\]

let \(V(h)\) be the minimum remaining worst-case cost.

If the history is target-pure,

\[
V(h)=0.
\]

Otherwise

\[
\boxed{
V(h)=
\min_{q\notin h}
\left[
c(q)+
\max_{a:P(q=a\mid h)>0}
V(h,q=a)
\right].
}
\]

Thus \(C_A=V(\varnothing)\).

Conditional mutual information \(I(T;q\mid h)\) is an average immediate
entropy reduction. It does not, by itself, retain the worst child history or
which future cue becomes useful in each realized child. This is why a complete
static entropy vector can fail to identify exact adaptive cost.

---

## S9. Nonlinear accessibility-to-feedback no-go theorem

For ecological state \(i\), define the state-specific routeability gap

\[
g_i=C_F(i)-C_A(i)\ge0.
\]

For an ordered pair of states define

\[
\Delta g=g_2-g_1\ge0.
\]

Let the local selection contribution be

\[
s_i=f(g_i)-\kappa,
\]

where \(f\) is nondecreasing and \(L\)-Lipschitz over the relevant domain.
Then

\[
0\le\Delta s\le L\Delta g.
\]

Let

\[
B=-\beta e>0
\]

be the local feedback-per-selection scale. The loop gain obeys

\[
\boxed{G\le BL\Delta g.}
\]

For the generalized local Jacobian

\[
J=
\begin{pmatrix}
\alpha & \beta\Delta s\\
(1-\phi)e & \phi
\end{pmatrix},
\]

the discriminant is

\[
\Delta_J
=
(\alpha-\phi)^2-4(1-\phi)G.
\]

Hence complex eigenvalues require

\[
G>
G_{\rm osc}
=
\frac{(\alpha-\phi)^2}{4(1-\phi)}.
\]

Combining the two inequalities gives the necessary condition

\[
\boxed{
\Delta g>
\frac{G_{\rm osc}}{BL}.
}
\]

If a declared architecture class has

\[
0\le g_i\le q_{\max}
\]

for every state and

\[
BLq_{\max}\le G_{\rm osc},
\]

then stable oscillatory feedback is unreachable for the entire class.

Crossing the contrast threshold is not sufficient for oscillation. The result
is local to the declared eco-evolutionary response model and does not estimate
\(B,L,\alpha,\phi\) empirically.

Executable sources:

- adaptive_gain/nonlinear_feedback_reachability.py
- tests/test_nonlinear_feedback_reachability.py
- validation/nonlinear_lipschitz_no_go_v2.json

---

## S10. Prospective direct Bombus experiments

### S10.1 Minimal four-state causal design

Use four physical cue vectors and three cue channels.

Routeable and matched-control groups share the physical cue environment but
differ in the focal target/action map.

Manipulate a hard acquisition budget

\[
B=1,2,3.
\]

The discriminating qualitative prediction is

\[
\Delta_{B=1}=0,
\qquad
\Delta_{B=2}>0,
\qquad
\Delta_{B=3}=0.
\]

Thus the routeability effect is predicted only in the intermediate budget
window rather than as a generic main effect.

### S10.2 Exact-balanced ten-state stress test

Use the S5 ten-state, six-cue environment with every cue exactly 5/5 balanced.

The exact costs are

\[
(C_A,C_F)_R=(3,4),
\qquad
(C_A,C_F)_K=(2,2).
\]

At common budget \(B=3\), the routed contingent schedule resolves both tasks
exactly. The best fixed three-cue ceiling is \(4/5\) in the routeable task and
1 in the control, giving deterministic ceiling interaction

\[
\boxed{
(1-4/5)-(1-1)=1/5.
}
\]

The value \(1/5\) is a task ceiling, not an assumed behavioral effect size.

Canonical design files:

- manuscript/ROUTEABILITY_EXPERIMENT_DESIGN_V1.md
- manuscript/EXACT_BALANCED_ROUTEABILITY_STRESS_TEST_DESIGN_V1.md

---

## S11. Additional theory retained outside the main narrative

The integrated paper uses one theorem spine. Several valid results are retained
as supporting or supplementary theory rather than competing headlines.

### S11.1 Temporal recurrence and spectral filtering

Community recurrence determines which structurally generated reward modes
persist through time. The formal spectral treatment is retained in:

- theory/COMMUNITY_SPECTRAL_EVOLUTIONARY_TIMESCALE.md
- theory/STRUCTURAL_SPECTRAL_JOINT_BOUND.md
- adaptive_gain/community_spectral_timescale.py
- adaptive_gain/structural_spectral_joint_bounds.py

These results support temporal interpretation but are not required for the
static-information non-identification theorem.

### S11.2 Identifiability limits

Local transient geometry generally identifies characteristic invariants rather
than a unique decomposition into evolutionary persistence, ecological memory
and loop gain.

Canonical files:

- theory/GENERAL_RESPONSE_IDENTIFIABILITY.md
- adaptive_gain/general_response_identifiability.py
- validation/general_response_identifiability_v1.json

These results remain supporting diagnostics rather than a main-paper headline.

### S11.3 Exact-balanced extremal geometry

The mathematical companion results remain useful as finite geometry behind the
routeability coordinate. In particular:

- for even \(n\ge6\), exact 50/50 balance gives the sharp fixed-cost cap
  \[
  C_F\le n-3;
  \]
- cap saturation has a rigid star--edge--star private-pair geometry;
- the depth-constrained envelopes \(D_h(n)\) have finite compatibility defects;
- despite those finite restrictions, exact balance does not uniformly bound
  the adaptive/fixed ratio.

Canonical files include:

- theory/EXACT_BALANCED_BINARY_FIXED_COST_CAP.md
- theory/EXACT_BALANCED_BINARY_CAP_SATURATION_DEPTH.md
- theory/EXACT_BALANCED_BINARY_DEPTH_THREE_CAP.md
- theory/EXACT_BALANCED_BINARY_DEPTH_FOUR_SHARP.md
- theory/EXACT_BALANCED_BINARY_DEPTH_FIVE_FRONTIER.md

These details belong in the Supplement/math appendix, not in the ecological
headline.

---

## S12. Scope of computational claims

The relational theorem, fixed-information characterization, direct-product
amplification and nonlinear no-go are analytic.

Finite matched controls and exact-balanced stress tests are constructive
finite results checked by exact solvers/enumeration.

Repository CI covers Python 3.10, 3.11 and 3.12. The current integrated branch
also contains dedicated machine-readable receipts for the entropy-vector,
nonlinear no-go and public Bombus bridge calculations.

---

## S13. Claim boundaries

The integrated supplement does not establish:

- stochastic optimality under noisy cues;
- expected-loss optimality;
- an unbounded multiplicative \(C_F/C_A\) ratio under complete Shannon
  entropy-vector matching;
- a one-dataset empirical measurement of the exact relational theorem;
- evolved niche breadth without an explicit evolutionary lift;
- diversity-stability, community resilience or ecosystem-function stability.

Those require additional biological or stochastic models.

---

## Reproducibility map

Strong static-information theorem:
- theory/STATIC_INFORMATION_ADAPTIVE_ACCESS_THEOREM.md
- adaptive_gain/static_information_adaptive_separation.py
- tests/test_static_information_adaptive_separation.py
- validation/static_information_adaptive_separation_v1.json

Relational asymptotic theorem:
- theory/RELATIONAL_ROUTEABILITY_THEOREM_SPINE_V1.md
- theory/QUANTITY_TOPOLOGY_ORTHOGONALITY.md
- adaptive_gain/balanced_quantity_topology_contrast.py
- tests/test_balanced_quantity_topology_contrast.py
- validation/balanced_quantity_topology_contrast_v1.json

Nonlinear no-go:
- theory/NONLINEAR_LIFT_NO_GO_V2.md
- adaptive_gain/nonlinear_feedback_reachability.py
- tests/test_nonlinear_feedback_reachability.py
- validation/nonlinear_lipschitz_no_go_v2.json

Pairwise controls:
- adaptive_gain/balanced_pairwise_information_controls.py
- tests/test_balanced_pairwise_information_controls.py
- validation/balanced_pairwise_information_controls_v1.json

Ten-state stress test:
- adaptive_gain/exact_balanced_routeability_stress_test.py
- tests/test_exact_balanced_routeability_stress_test.py
- validation/exact_balanced_routeability_stress_test_v1.json

Bombus empirical bridge:
- adaptive_gain/bumblebee_public_bridge.py
- tests/test_bumblebee_public_bridge.py
- validation/bombus_public_data_component_receipt_v1.json
- validation/bombus_empirical_convergence_panel_v1.json
