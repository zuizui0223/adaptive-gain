# Static information does not determine adaptive accessibility

Status: post-freeze theorem strengthening for the relational-routeability synthesis.

## Main distinction

For a deterministic finite ecological decision task, there are two mathematically different information objects.

1. **Static subset information**
   \[
   F(S)=I(T;Q_S),
   \qquad S\subseteq Q.
   \]

2. **Outcome-resolved conditional information geometry**
   generated after a realized history
   \[
   h=(q_1=a_1,\ldots,q_r=a_r).
   \]

The first completely characterizes the fixed exact-resolution cost \(C_F\).
It does **not** characterize the adaptive exact-resolution cost \(C_A\).

That separation can be proved while holding the physical cue matrix fixed and
making every available binary cue exactly 50/50 balanced.

---

## Theorem 1 — exact information characterization of fixed resolution

Let \(W\) be a finite deterministic task, let every represented world have
strictly positive probability, and let \(S\) be a fixed bundle of cues.

Then the following are equivalent:

1. \(S\) resolves the target exactly;
2. \(H(T\mid Q_S)=0\);
3. \(I(T;Q_S)=H(T)\).

Therefore

\[
\boxed{
C_F
=
\min_{S\subseteq Q}
\left\{
\sum_{q\in S}c(q):
I(T;Q_S)=H(T)
\right\}.
}
\]

### Proof

If \(S\) resolves the target, every realized cue signature is target-pure, so
\(H(T\mid Q_S)=0\).

Conversely, if \(S\) does not resolve the target, there exist two represented
worlds with different targets and the same \(Q_S\) signature. Strictly positive
world probabilities give both targets positive conditional probability in that
signature, so its conditional entropy is positive. Hence
\(H(T\mid Q_S)>0\).

The mutual-information statement follows from

\[
I(T;Q_S)=H(T)-H(T\mid Q_S).
\]

The numerical value of \(F(S)\) depends on the chosen full-support prior, but
the equality \(F(S)=H(T)\) does not: it is exactly the structural resolving
condition.

Executable implementation:

- \`adaptive_gain/information.py::fixed_information_minimum_cost\`

---

## Theorem 2 — the complete static subset-information function does not determine \(C_A\)

There exist two finite deterministic target-resolution tasks defined on the
**same** physical cue environment such that:

- the same 12 represented worlds are used;
- the same four binary unit-cost cues are used;
- every cue is exactly 6/6 balanced;
- the entire state-by-cue outcome matrix is identical;
- target multiplicities are identical, \((8,4)\);
- target entropy is identical;
- for **every named cue subset** \(S\subseteq\{q_0,q_1,q_2,q_3\}\),

  \[
  \boxed{
  I(T_A;Q_S)=I(T_B;Q_S)
  }
  \]

  under the uniform world prior;
- both tasks have

  \[
  C_F=4;
  \]

yet

\[
\boxed{
C_A(T_A)=4,
\qquad
C_A(T_B)=3.
}
\]

Therefore

\[
\boxed{
\{I(T;Q_S):S\subseteq Q\}
\not\Rightarrow
C_A.
}
\]

This is a finite exact separation between **static information content** and
**adaptive information accessibility**.

### Common physical cue matrix

Rows are represented worlds and columns are the four cues:

| world | q0 | q1 | q2 | q3 | T_A | T_B |
|---|---:|---:|---:|---:|---:|---:|
| w00 | 0 | 0 | 0 | 0 | 0 | 0 |
| w01 | 0 | 0 | 0 | 1 | 1 | 0 |
| w02 | 0 | 0 | 1 | 0 | 1 | 1 |
| w03 | 0 | 0 | 1 | 1 | 1 | 0 |
| w04 | 0 | 1 | 0 | 0 | 0 | 1 |
| w05 | 0 | 1 | 1 | 1 | 0 | 1 |
| w06 | 1 | 0 | 0 | 0 | 0 | 0 |
| w07 | 1 | 0 | 1 | 1 | 0 | 0 |
| w08 | 1 | 1 | 0 | 0 | 1 | 0 |
| w09 | 1 | 1 | 0 | 1 | 0 | 1 |
| w10 | 1 | 1 | 1 | 0 | 0 | 0 |
| w11 | 1 | 1 | 1 | 1 | 0 | 0 |

Each \(q_j\) contains six zeros and six ones.

### Shared static information profile

Both target maps have

\[
H(T)=H_2(1/3)=0.918295834054\ldots\text{ bits}.
\]

Their named subset-information functions are identical:

| cue subset | \(I(T;Q_S)\), bits |
|---|---:|
| \(\varnothing\) | 0 |
| \(q_0\) | 0.093284623230 |
| \(q_1\) | 0.093284623230 |
| \(q_2\) | 0 |
| \(q_3\) | 0 |
| \(q_0,q_1\) | 0.377443751082 |
| \(q_0,q_2\) | 0.229573958514 |
| \(q_1,q_2\) | 0.229573958514 |
| \(q_0,q_3\) | 0.229573958514 |
| \(q_1,q_3\) | 0.229573958514 |
| \(q_2,q_3\) | 0.044110417748 |
| any three cues | 0.584962500721 |
| all four cues | 0.918295834054 |

Thus no one-, two-, or three-cue fixed bundle contains all target information,
while the four-cue bundle does. By Theorem 1,

\[
C_F(T_A)=C_F(T_B)=4.
\]

### Exact equality certificate

The profile match is not a floating-point coincidence.

For a fixed subset \(S\), partition the 12 worlds by \(Q_S\). If one cell has
size \(n\) and target counts \(n_t\),

\[
nH(T\mid\text{cell})
=
n\log_2 n-\sum_t n_t\log_2 n_t.
\]

Factor every integer into primes. Then

\[
12H(T\mid Q_S)
\]

is an integer linear combination of \(\log_2 p\) terms. The implementation
compares this formal prime-log coefficient vector for every named subset.
All 16 vectors agree exactly between the two tasks.

Executable certificate:

- \`adaptive_gain/static_information_adaptive_separation.py\`
- \`tests/test_static_information_adaptive_separation.py\`

### Corollary 2.1 — the complete Shannon entropy vector can be identical

The same twins are stronger than an all-subset mutual-information match.

For every cue subset \(S\subseteq Q\), the physical cue matrix is common, so

\[
H_A(Q_S)=H_B(Q_S).
\]

The exact conditional-entropy certificate above gives

\[
H_A(T\mid Q_S)=H_B(T\mid Q_S)
\]

for every named subset. Therefore

\[
H_A(T,Q_S)
=
H_A(Q_S)+H_A(T\mid Q_S)
=
H_B(Q_S)+H_B(T\mid Q_S)
=
H_B(T,Q_S).
\]

Every subset of the five variables \((T,q_0,q_1,q_2,q_3)\) either contains
\(T\) and has the form \((T,Q_S)\), or is cue-only. Hence

\[
\boxed{
H_A(U)=H_B(U)
\qquad
\forall U\subseteq\{T,q_0,q_1,q_2,q_3\}.
}
\]

Thus the two tasks have the **same complete Shannon entropy vector** while

\[
C_A(T_A)=4
\neq
3=C_A(T_B).
\]

This is an operational inequivalence under exact entropic equivalence. It does
not establish that entropy vectors are generally insufficient for all decision
problems; extra-entropic operational distinctions are known elsewhere in
information theory. The present point is the exact finite acquisition
consequence in a common ecological cue environment.

Executable certificate:

- \`joint_entropy_log_fingerprint\` in
  \`adaptive_gain/static_information_adaptive_separation.py\`;
- \`test_complete_shannon_entropy_vector_matches_exactly\`.

### Corollary 2.2 — entropic equivalence supports an unbounded additive adaptive separation

The finite twin is not an isolated one-unit phenomenon.

Form the \(r\)-fold Cartesian product of either twin. A represented world is an
\(r\)-tuple of base worlds, the focal target is the \(r\)-tuple of coordinate
targets, and each declared cue belongs to exactly one coordinate. Use the
uniform product prior.

For every \(r\ge1\), the two product tasks share:

- the same \(12^r\) represented worlds;
- the same \(4r\) coordinate-local binary unit-cost cues;
- exact 50/50 balance of every cue;
- the same complete physical cue matrix;
- the same target distribution;
- the same complete Shannon entropy vector over the composite target and all
  \(4r\) cues.

The entropy-vector claim follows by factorization. If a cue subset \(S\) is
decomposed into coordinate subsets \(S_1,\ldots,S_r\), then

\[
H(Q_S)=\sum_{i=1}^r H(Q_{S_i}),
\]

and, writing the composite target as
\(\mathbf T=(T_1,\ldots,T_r)\),

\[
H(\mathbf T,Q_S)
=
\sum_{i=1}^r H(T_i,Q_{S_i}).
\]

The one-copy entropy vectors are identical, so every product entropy is
identical as well.

The exact resolution costs are additive under this product:

\[
C_F(X\otimes Y)=C_F(X)+C_F(Y),
\]

\[
C_A(X\otimes Y)=C_A(X)+C_A(Y).
\]

For \(C_F\), any fixed resolver of the product must resolve each coordinate
after the other coordinate is held fixed, while the union of coordinate-wise
optimal bundles attains the sum.

For \(C_A\), every realized history leaves a rectangular support because each
query acts on only one coordinate. The Bellman continuation value on a
rectangle is the sum of the coordinate continuation values: a query in one
coordinate changes only that coordinate's term, and the worst-child recursion
therefore preserves additivity. Induction on the remaining query set gives the
identity above.

Consequently the \(r\)-copy twins satisfy

\[
(C_A,C_F)_{A^{\otimes r}}=(4r,4r),
\]

\[
(C_A,C_F)_{B^{\otimes r}}=(3r,4r).
\]

Hence

\[
\boxed{
C_A(A^{\otimes r})-C_A(B^{\otimes r})=r\to\infty
}
\]

while the complete Shannon entropy vector remains matched.

Equivalently, with \(g=C_F-C_A\),

\[
g(A^{\otimes r})=0,
\qquad
g(B^{\otimes r})=r.
\]

At the common budget \(B_r=3r\), the \(B\)-product is adaptively resolvable but
not fixed-resolvable, whereas the \(A\)-product is not resolvable under either
access mode.

This is an **unbounded additive** separation under complete entropic
equivalence. It does not establish an unbounded multiplicative
\(C_F/C_A\) ratio under that strongest matching condition; the separate
exact-balanced routing family supplies an unbounded ratio under weaker
information matching.

Executable two-copy check:

- \`static_information_twin_product_task\`;
- \`test_two_copy_product_amplifies_adaptive_gap_under_entropic_equivalence\`.

---

### Why the adaptive costs differ

For target map \(T_A\), the optimal residual adaptive depths after each possible
first cue are:

| first cue | outcome-0 residual | outcome-1 residual | total worst-case cost |
|---|---:|---:|---:|
| q0 | 2 | 3 | 4 |
| q1 | 2 | 3 | 4 |
| q2 | 3 | 2 | 4 |
| q3 | 3 | 2 | 4 |

Every possible first observation leaves one branch requiring all three
remaining levels, so

\[
C_A(T_A)=4.
\]

For target map \(T_B\):

| first cue | outcome-0 residual | outcome-1 residual | total worst-case cost |
|---|---:|---:|---:|
| q0 | 3 | 2 | 4 |
| q1 | 2 | 3 | 4 |
| q2 | 2 | 2 | 3 |
| q3 | 2 | 2 | 3 |

Thus \(q_2\) or \(q_3\) routes both outcomes into residual tasks of depth two:

\[
C_A(T_B)=3.
\]

The difference is not how much target information any fixed subset contains.
It is how target-relevant distinctions are **distributed across the realized
outcomes** of those subsets.

---

## Theorem 3 — adaptive cost is an outcome-resolved Bellman object

For a realized history

\[
h=(q_1=a_1,\ldots,q_r=a_r),
\]

let \(W_h\) be the represented worlds consistent with that exact history.
Define \(V(h)\) as the minimum remaining worst-case cue cost.

Then

\[
V(h)=0
\quad\text{if}\quad
H(T\mid h)=0,
\]

and otherwise

\[
\boxed{
V(h)
=
\min_{q\notin h}
\left[
c(q)
+
\max_{a:P(q=a\mid h)>0}
V(h,q=a)
\right].
}
\]

Therefore

\[
C_A=V(\varnothing).
\]

Conditional mutual information,

\[
I(T;q\mid h)
=
H(T\mid h)
-
\sum_a P(a\mid h)H(T\mid h,q=a),
\]

is an **average** immediate entropy reduction. It is useful, but a single CMI
scalar does not encode the worst branch or which future cue becomes relevant
inside each child. The exact adaptive object is the full outcome-resolved
continuation geometry.

The existing MROD witness makes this visible:

\[
I(T;\text{context})=0,
\]

but

\[
I(T;\text{assay0}\mid \text{context}=0)=1,
\qquad
I(T;\text{assay1}\mid \text{context}=0)=0,
\]

while after the other context outcome,

\[
I(T;\text{assay0}\mid \text{context}=1)=0,
\qquad
I(T;\text{assay1}\mid \text{context}=1)=1.
\]

The root cue contributes no direct target information. Its value is that its
**realized result changes which later source contains the target information**.

Executable diagnostics:

- \`conditional_bundle_information_bits\`
- \`target_entropy_given_history_bits\`
- \`outcome_resolved_query_information\`

in \`adaptive_gain/information.py\`.

---

## Corrected sufficiency ladder

The previous ladder jumped too quickly from pairwise target-cue information to
the complete action-conditioned table.

The corrected hierarchy is:

### Level 1 — state/query counts

Insufficient for \(C_F\) or \(C_A\).

### Level 2 — cue marginals and cue-only distributions

Insufficient even when every cue is exactly balanced.

### Level 3 — target prevalence, \(H(T)\), and \(I(T;Q_{\rm all})\)

Insufficient.

### Level 4 — pairwise target-cue information profiles

Insufficient; the repository already has finite matched controls.

### Level 5 — the complete named static subset-information function

\[
F(S)=I(T;Q_S),\qquad \forall S\subseteq Q.
\]

This level is **sufficient for \(C_F\)** by Theorem 1.

It is **not sufficient for \(C_A\)** by Theorem 2.

### Level 6 — outcome-resolved conditional continuation geometry

Histories retain the actual result values, not only subset averages. Together
with cue costs and the admissible remaining queries, this is sufficient to
evaluate the Bellman recursion for \(C_A\).

### Level 7 — complete action-conditioned cue table

\[
(w,T(w),q_1(w),\ldots,q_m(w))
\]

plus cue costs is a direct sufficient representation of the deterministic
finite problem.

---

## Relation to PID, synergy and active feature acquisition

Williams & Beer (2010) introduced partial information decomposition to separate
unique, redundant and synergistic contributions of multiple sources to a
target. XOR is the canonical example in which individual sources contain no
target information while the pair contains complete target information.

That literature is directly relevant and must be cited. But **routeability is
not a synonym for synergy**.

A simple XOR/XNOR task can be maximally joint-only in the ordinary two-source
sense while still having

\[
C_A=C_F=2.
\]

Conversely, routeability concerns whether realized outcomes make different
future observations relevant, creating a difference between fixed provisioning
and contingent acquisition.

Theorem 2 sharpens this boundary: even the entire static Shannon
subset-information set function can be identical while adaptive cost differs.

This does **not** imply that every possible PID construction is identical for
the two twins. PID definitions may use finer distributional information than
the scalar subset-MI function, and multivariate PID itself has multiple
competing definitions. A particularly close 2026 preprint by Li, Dhali & Bouma explicitly studies when
pairwise synergy helps active feature acquisition. Their SynAFA policy combines
pairwise joint information with conditional information evaluated at realized
feature values, and their synthetic analyses include approximately
fixed-information controls. This is direct prior art for connecting synergy,
realized-value conditioning and budgeted sequential acquisition.

The present exact theorem therefore must not be positioned as the first
synergy-to-acquisition bridge. Its narrower distinction is that two deterministic
tasks on one physical cue matrix can have the same **complete Shannon entropy
vector** and still have different optimal worst-case adaptive resolution depth.

The safe claim is narrower:

> static Shannon information content, even at all subset orders, does not
> determine exact sequential accessibility.

References:
- Williams, P. L. & Beer, R. D. 2010. *Nonnegative Decomposition of
  Multivariate Information*. arXiv:1004.2515.
- Lyu, A., Clark, A. & Raviv, N. 2026. Multivariate partial information
  decomposition: constructions, inconsistencies, and alternative measures.
  *Physical Review E* 113:034102.

---

## Relation to active feature acquisition

Sequential acquisition of costly information is established prior art.

For example:
- Ma et al. (2019), EDDI, chooses additional variables using expected
  information gain under acquisition cost;
- Norcliffe et al. (2025) explicitly describe active feature acquisition as
  instance-wise sequential measurement and note conditional-mutual-information
  acquisition as an existing, often myopic, strategy.

Therefore the manuscript must **not** claim novelty for:
- sequentially choosing observations;
- conditioning information gain on observations;
- costly active feature acquisition;
- generic adaptive versus non-adaptive search.

The ecological contribution is instead the exact composition:

\[
\boxed{
\text{same physical ecological cue environment}
+
\text{same complete static subset-information profile}
+
\text{different action map}
\Rightarrow
\text{different adaptive accessibility}.
}
\]

Combined with the existing asymptotic theorem, the paper now has two
complementary results:

1. **strong matching, finite magnitude:** all static subset information can be
   matched while \(C_A\) changes;
2. **weaker information matching, unbounded magnitude:** the exact-balanced
   relational family has \(C_F/C_A\to\infty\).

Do not conflate the two. No unbounded separation under a matched complete
subset-information profile is currently claimed.

---

## One-line synthesis

\[
\boxed{
\text{Static information tells us what can be known together; routeability tells us what must be learned together.}
\]
