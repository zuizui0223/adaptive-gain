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
bounded-arity and productive-frontier structural bounds and their constructive witness.

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

## 4. Productive-frontier edge-count exclusion

The unit-cost productive-frontier theorem gives

\[
C_F\le |\mathcal H_{\min}|,
\]

where `|H_min|` is the number of minimal productive obligations.

For binary tasks, gap two cannot occur with `C_A<=2`:

- if `C_A=1`, a depth-one productive tree uses only one internal query, so `C_F<=1`;
- if `C_A=2`, binary flattening gives `C_F<=3`, hence `C_F-C_A<=1`.

Therefore every binary gap-two task must have

\[
C_A\ge3,
\qquad
C_F\ge C_A+2\ge5.
\]

Consequently

\[
\boxed{|\mathcal H_{\min}|\ge5}
\]

is necessary to enter the canonical oscillatory regime.

Equivalently, every binary task with productive-frontier edge cap

\[
|\mathcal H_{\min}|\le4
\]

has structural gap at most one and cannot produce a non-real local eigenpair under
the declared response geometry.

This keeps the productive frontier itself on the dynamic main line: it is not merely
an internal representation of `C_F`; its minimal edge count sets a sharp structural
complexity threshold for access to the oscillatory feedback regime.

---

## 5. Constructive first joint scope

The existing sharp bounded-arity witness at

\[
(n,m,b)=(6,5,2)
\]

has

\[
\boxed{C_A=3,\qquad C_F=5,\qquad \Delta g=2.}
\]

Every one of its five declared queries has a private opposite-target pair, so its
minimal productive frontier consists of five singleton mandatory obligations:

\[
\boxed{|\mathcal H_{\min}|=5.}
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

Combining the three impossibility statements with the constructive witness gives the
canonical sharp threshold corner

\[
\boxed{
(6\text{ worlds},\ 5\text{ binary queries},\ 5\text{ minimal frontier obligations})
}
\]

for entry into stable oscillatory feedback under the declared response geometry.

In the corresponding partial order:

- every binary task with `n<=5` is excluded;
- every binary task with `m<=4` is excluded;
- every binary task with `|H_min|<=4` is excluded;
- the corner `(n,m,|H_min|)=(6,5,5)` is attained constructively.

It is not a claim that the numerical normalization

\[
\alpha=1,\phi=1/2,a=1/8
\]

is biologically universal.

---

## 6. Relation to the paper's four pillars

This threshold directly couples Pillar B and Pillar D.

### Pillar B — finite structural reachability

The finite sensing vocabulary and productive frontier place hard ceilings on attainable
structural gap.

### Pillar D — oscillation as a feedback-existence window

A non-real local eigenpair forces positive feedback within the generalized model.

The threshold therefore says:

> below a sharp binary information/frontier scope, the regime that can qualitatively
> force feedback existence is structurally unreachable.

This is stronger than saying that information structure merely changes the magnitude
of selection.  It determines whether a qualitatively different dynamical/identifiability
regime is even accessible.

---

## 7. Scope and novelty boundary

The theorem assumes:

- finite deterministic unit-cost sensing tasks;
- binary query outcomes;
- the canonical local response geometry declared above;
- linear gain lift `G=a Delta_g`;
- local deterministic dynamics.

No novelty is claimed for bounded-arity decision-tree counting, the productive-frontier
hitting-set inequality, or the standard complex-eigenvalue threshold by themselves.
The contribution is their exact composition:

\[
\boxed{
\text{finite information/frontier scope}
\to
\text{sharp structural-gap threshold}
\to
\text{first reachable oscillatory feedback regime}.
}
\]
