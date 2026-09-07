# Adaptive gain: exact finite resolution theorem and routing certificates

Status: abstract decision-theory layer extracted from repository-specific results. The scientific models remain owned by MROD, PAYOFF, and BALANCE.

## 1. Finite deterministic task

Let

\[
\mathcal W=\{w_1,\ldots,w_n\}
\]

be a finite represented world set and let

\[
T:\mathcal W\to\mathcal T
\]

be the target.

Each query \(q\in\mathcal Q\) has:

- positive integer acquisition cost \(c(q)\);
- deterministic outcome map \(o_q:\mathcal W\to\mathcal Y_q\).

No probability distribution is required for the guaranteed-resolution theorem.

A target is resolved on \(S\subseteq\mathcal W\) when \(T\) is constant on \(S\).

## 2. Fixed bundle

A fixed bundle \(F\subseteq\mathcal Q\) resolves the target iff for every pair

\[
w_i,w_j
\quad\text{with}\quad
T(w_i)\ne T(w_j),
\]

at least one \(q\in F\) separates them:

\[
o_q(w_i)\ne o_q(w_j).
\]

Define

\[
C_F
=
\min_{F\text{ resolves}}
\sum_{q\in F}c(q).
\]

The implementation exhaustively enumerates the declared finite query vocabulary.

## 3. Adaptive tree

For current compatible set \(S\) and remaining query set \(R\), define the exact minimum worst-path resolution cost recursively:

\[
C_A(S,R)=0
\]

when \(T\) is constant on \(S\), and otherwise

\[
C_A(S,R)
=
\min_{q\in R}
\left[
c(q)+
\max_{y:o_q^{-1}(y)\cap S\ne\varnothing}
C_A(S_{q,y},R\setminus\{q\})
\right],
\]

where

\[
S_{q,y}
=
\{w\in S:o_q(w)=y\}.
\]

A query that does not split \(S\) can be omitted because it consumes positive cost without changing the compatible set.

The root value is

\[
C_A=C_A(\mathcal W,\mathcal Q).
\]

## 4. Containment theorem

**Theorem AG1.**

\[
\boxed{C_A\le C_F}
\]

whenever the task is resolvable by the declared query vocabulary.

### Proof

Take any resolving fixed bundle \(F\). Construct an adaptive policy that measures every query in \(F\) in a predeclared order and ignores intermediate outcomes when choosing the next query. Every path costs exactly

\[
\sum_{q\in F}c(q)
\]

and the final joint observation resolves the target. Therefore this policy is feasible in the adaptive class. Minimizing over adaptive policies cannot cost more than minimizing over fixed bundles. \(\square\)

This is a class-containment result, not an empirical claim.

## 5. Exact integer budget window

Let integer budget \(B\ge0\).

A guaranteed adaptive-only resolution advantage exists exactly when

\[
C_A\le B<C_F.
\]

Therefore if \(C_A<C_F<\infty\), the adaptive-only budget set is the contiguous integer interval

\[
\boxed{
\mathcal B_{\rm adapt}
=
\{C_A,C_A+1,\ldots,C_F-1\}.
}
\]

This explains the registered PAYOFF/MROD pattern:

```text
too little budget -> neither class resolves
intermediate budget -> adaptive only
enough budget -> fixed catches up
```

The theorem concerns binary guaranteed resolution. Information-valued objectives need not have a contiguous positive-gap set.

## 6. Strong root routing certificate

Fix budget \(B\) and a proposed root query \(q\).

For every reachable root outcome \(y\), let

\[
C_A^{(y)}
=
C_A(S_{q,y},\mathcal Q\setminus\{q\}).
\]

If

\[
c(q)+C_A^{(y)}\le B
\quad\forall y,
\]

and simultaneously

\[
C_F>B,
\]

then the query \(q\) gives a constructive adaptive-only resolution certificate at budget \(B\).

This is sufficient but not necessary: another root query can support an adaptive tree even if the nominated root fails.

The implementation also records the selected first continuation query in every branch. Different branch-specific next actions expose **action specialization**.

## 7. Branch-invariant no-routing theorem

The previous theorem is target-set based. A broader value problem may have a declared sufficient future-value state

\[
\sigma(s),
\]

with continuation value depending on history only through \(\sigma\).

Consider a query \(q\) at state \(s\). If every reachable outcome satisfies

\[
\boxed{
\sigma(s_{q,y})=\sigma'
\quad\forall y,
}
\]

then conditioning the **next action** on \(y\) cannot improve the continuation value at that step: every branch presents the same future decision state.

This is a conditional no-routing theorem. Its force depends entirely on the scientific validity of the declared sufficient state.

It does **not** imply:

- the query has zero direct target information;
- the query is useless for a different objective;
- adaptivity can never help elsewhere in the tree;
- the sufficient state remains valid after changing the model.

BALANCE supplies the registered negative-control structure: stay and switch change interval location but not the span-based sufficient state used by the declared minimax width objective.

## 8. Zero direct information can coexist with routing value

When probabilities are supplied, the repository separately computes target mutual information.

For a selected adaptive policy history \(H\) with root observation \(Q_1\),

\[
I(T;H)
=
I(T;Q_1)
+
\left[I(T;H)-I(T;Q_1)\right].
\]

The bracketed quantity is called **continuation target information** in this repository.

Separately, the entropy of the identity of the next selected action is

\[
H(A_2).
\]

This is **not** target information. It measures how variable the immediate continuation action is under the declared world distribution.

The registered MROD-style and PAYOFF-style finite witnesses both satisfy, under uniform represented worlds,

\[
I(T;Q_1)=0,
\]

\[
I(T;H)=1\text{ bit},
\]

\[
H(A_2)=1\text{ bit},
\]

while the best fixed two-query bundle has

\[
I(T;Q_F)=0.5\text{ bit}.
\]

Hence

\[
\boxed{
I(T;Q_1)=0
\not\Rightarrow
\text{zero decision relevance}.
}
\]

The observation can matter by changing which continuation action is appropriate.

But zero direct information plus positive joint information is not enough for adaptive gain: if the same continuation action is appropriate in every branch, the fixed and adaptive classes can coincide.

## 9. Three diagnostic ingredients

The cross-repository comparison suggests three useful diagnostics:

1. **branch-dependent future state**;
2. **action specialization** across branches;
3. **budget scarcity** preventing a fixed design from buying all branch-specific actions.

They are not asserted as a universal multiplicative formula. The exact finite solver decides whether strict gain actually occurs.

## 10. Claim boundary

This repository deliberately separates:

```text
direct target information
!= continuation target information
!= routing-action diversity
!= strict adaptive gain
!= scientific report licensing.
```

It also separates:

```text
finite represented-world resolution
!= continuous-parameter identification
!= empirical frequency in nature.
```

The results are exact conditional statements for the declared finite task.
