# Sharp binary structural threshold for entering oscillatory feedback

## Purpose

This note connects the finite sensing extremal theory directly to the qualitative
feedback-existence window of the generalized eco-evolutionary response.

The local generalized response has complex eigenvalues when

\[
G>G_{\rm osc}
=
\frac{(\alpha-\phi)^2}{4(1-\phi)}.
\]

Under a linear restoring structural lift,

\[
G=a\,\Delta g,
\qquad
\Delta g=C_F-C_A\in\mathbb Z_{\ge0},
\]

where

\[
a=(-\beta e)\lambda>0.
\]

Therefore the smallest structural gap capable of entering the oscillatory region is

\[
\boxed{
\Delta g_{\rm osc,min}
=
\left\lfloor\frac{G_{\rm osc}}{a}\right\rfloor+1.
}
\]

Stable oscillation additionally requires

\[
a\Delta g<G_+,
\qquad
G_+=\frac{1-\alpha\phi}{1-\phi}.
\]

No novelty is claimed for this integer rounding or for the complex-eigenvalue
threshold.  The repository-specific result is the exact composition with the
bounded-arity structural gap theorem and its constructive witness.

---

## 1. Canonical response geometry

Use the normalized local geometry

\[
\alpha=1,
\qquad
\phi=\frac12,
\qquad
 a=\frac18.
\]

Then

\[
G_{\rm osc}
=
\frac{(1-1/2)^2}{4(1-1/2)}
=
\frac18,
\]

and

\[
G_+=1.
\]

Hence

\[
\boxed{
\Delta g_{\rm osc,min}=2,
\qquad
\Delta g_{\rm stable,max}=7.
}
\]

A gap-one task reaches exactly the real/complex boundary,

\[
G=\frac18=G_{\rm osc},
\]

but does not produce a non-real eigenpair.  Gap two gives

\[
G=\frac14,
\]

which is strictly oscillatory and still strictly stable.

---

## 2. Binary world-count exclusion

For binary unit-cost sensing,

\[
C_F
\le
F_2(n,h)
\]

at adaptive cost `h`.  Therefore

\[
\Delta g
\le
F_2(n,h)-h.
\]

Taking the maximum over positive adaptive depths gives

\[
\begin{array}{c|ccccc}
n & 2 & 3 & 4 & 5 & 6\\
\hline
\max_h(F_2(n,h)-h) & 0 & 0 & 1 & 1 & 2.
\end{array}
\]

Thus every binary task with at most five represented worlds satisfies

\[
\boxed{\Delta g\le1.}
\]

Under the canonical response geometry it therefore cannot enter the oscillatory
feedback phase.

Six represented worlds are the first world count for which the inherited binary
structural ceiling reaches the required gap two.

---

## 3. Binary query-count exclusion

The declared query count also limits fixed cost:

\[
C_F\le m.
\]

For binary routing, maximizing

\[
\min\{m,F_2(n,h)\}-h
\]

over adaptive depth and over a world budget large enough to saturate all relevant
binary trees gives

\[
\begin{array}{c|ccccc}
m & 1 & 2 & 3 & 4 & 5\\
\hline
\Delta g_{\max} & 0 & 0 & 1 & 1 & 2.
\end{array}
\]

Hence every binary task with at most four declared queries satisfies

\[
\boxed{\Delta g\le1}
\]

regardless of world count.

Five queries are the first query budget that can support the required gap two.

---

## 4. Constructive first joint scope

The existing sharp bounded-arity witness at

\[
(n,m,b)=(6,5,2)
\]

has

\[
\boxed{C_A=3,\qquad C_F=5,\qquad \Delta g=2.}
\]

Therefore

\[
G=\frac18\times2=\frac14.
\]

Since

\[
\frac18<G=\frac14<1,
\]

this task lies in the stable oscillatory region.

Combining the two impossibility statements with the constructive witness gives the
canonical sharp threshold:

\[
\boxed{
(6\text{ worlds},5\text{ binary queries})
}
\]

is the first joint binary finite-sensing scope that can enter stable oscillatory
feedback under the declared response geometry.

This is a statement about the joint world/query partial order:

- every binary task with `n<=5` is excluded;
- every binary task with `m<=4` is excluded;
- the corner `(n,m)=(6,5)` is attained constructively.

It is not a claim that the numerical normalization

\[
\alpha=1,\phi=1/2,a=1/8
\]

is biologically universal.

---

## 5. Relation to the paper's four pillars

This threshold directly couples Pillar B and Pillar D.

### Pillar B — finite structural reachability

The finite sensing vocabulary places a hard ceiling on attainable structural gap.

### Pillar D — oscillation as a feedback-existence window

A non-real local eigenpair forces positive feedback within the generalized model.

The threshold therefore says:

> below a sharp binary information scope, the regime that can qualitatively force
> feedback existence is structurally unreachable.

This is stronger than saying that information structure merely changes the magnitude
of selection.  It determines whether a qualitatively different dynamical/identifiability
regime is even accessible.

---

## 6. Scope and novelty boundary

The theorem assumes:

- finite deterministic unit-cost sensing tasks;
- binary query outcomes;
- the canonical local response geometry declared above;
- linear gain lift `G=a Delta_g`;
- local deterministic dynamics.

No novelty is claimed for bounded-arity decision-tree counting by itself, nor for the
standard complex-eigenvalue threshold.  The contribution is their exact composition:

\[
\boxed{
\text{finite information scope}
\to
\text{sharp structural-gap threshold}
\to
\text{first reachable oscillatory feedback regime}.
}
\]
