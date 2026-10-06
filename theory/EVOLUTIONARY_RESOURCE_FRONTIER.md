# Natural-history-dependent evolutionary resource frontier

Status: theorem extension on branch \`theory/opportunity-fitness-process-v1\`.

This note inverts the sharp value envelope.

The forward theorem asks:

> given finite information resources, how much biological value can adaptivity
> generate?

The inverse theorem asks:

> given the constitutive cost of adaptive control, how much information
> structure is minimally required before adaptivity can be favored?

This gives the earlier structural-gap thresholds a direct biological
microfoundation.

## 1. Setup

Let

\[
U(c)
\]

be any finite nonincreasing biological value of guaranteed completion at cost
\(c\).

Let

\[
K\ge0
\]

be the additive constitutive architecture cost of contingent control relative
to the declared universal fixed comparator.

For a task with completion costs \((C_A,C_F)\), net architecture value is

\[
\Phi
=
U(C_A)-U(C_F)-K.
\]

Fix adaptive depth

\[
h=C_A.
\]

## 2. Required fixed burden at depth h

Define

\[
\boxed{
J_K(h)
=
\min
\left\{
j\in\mathbb Z_{\ge h}:
U(h)-U(j)>K
\right\},
}
\]

with

\[
J_K(h)=\infty
\]

if no such finite \(j\) exists.

\(J_K(h)\) is the minimum fixed completion cost that makes adaptive completion
at depth \(h\) worth its architecture cost.

Because \(U\) is nonincreasing,

\[
\boxed{
U(h)-U(j)>K
\iff
j\ge J_K(h)
}
\]

whenever \(J_K(h)<\infty\).

So the biology supplies a **depth-specific required fixed burden**.

## 3. Theorem RF1 — exact selection criterion inside a finite structural scope

For world count \(n\), query count \(m\), and maximum query arity \(b\), define

\[
I_h
=
\min\{m,F_b(n,h)\}.
\]

The sharp structural frontier gives the exact best fixed burden attainable at
adaptive depth \(h\):

\[
(C_A,C_F)=(h,I_h).
\]

Therefore positive architecture value exists at depth \(h\) if and only if

\[
\boxed{
I_h\ge J_K(h).
}
\]

Consequently positive adaptive architecture value exists somewhere in the
entire finite scope if and only if

\[
\boxed{
\exists h:
\min\{m,F_b(n,h)\}
\ge
J_K(h).
}
\]

This is equivalent to the forward condition

\[
K<K_{\rm crit},
\]

but it exposes the required structural resources rather than the maximum
payable architecture cost.

## 4. Two independent resource requirements

At one declared depth \(h\), the condition

\[
I_h\ge J_K(h)
\]

requires both

\[
\boxed{
m\ge J_K(h)
}
\]

and

\[
\boxed{
F_b(n,h)\ge J_K(h).
}
\]

Thus natural history creates a joint resource requirement:

- enough distinct query resources to make the fixed comparator sufficiently
  expensive; and
- enough represented-world/tree geometry to make that burden structurally
  realizable at depth \(h\).

This separates "more sensors" from "enough state structure for those sensors to
become branch-exclusive."

## 5. Exact binary resource corner

For binary queries,

\[
F_2(n,h)
=
\min(n-1,2^h-1).
\]

Let

\[
j_h=J_K(h)<\infty.
\]

A positive-value binary witness at depth \(h\) exists if and only if

\[
\boxed{
j_h\le 2^h-1.
}
\]

When this holds, the componentwise minimum world/query counts are

\[
\boxed{
n_h^*=j_h+1,
\qquad
m_h^*=j_h.
}
\]

The exact witness has

\[
(C_A,C_F)=(h,j_h).
\]

The overall binary evolutionary resource frontier is the nondominated set of

\[
\boxed{
(j_h+1,j_h)
}
\]

across feasible adaptive depths.

Unlike the old gap threshold, different depths can require different
\(j_h-h\).

## 6. Linear completion value recovers the old integer gap theorem

Take

\[
U(c)=-\lambda c,
\qquad
\lambda>0.
\]

Then

\[
U(h)-U(j)
=
\lambda(j-h).
\]

Positive architecture value requires

\[
\lambda(j-h)>K.
\]

Define

\[
\boxed{
q_K
=
\left\lfloor\frac{K}{\lambda}\right\rfloor+1.
}
\]

Then

\[
\boxed{
J_K(h)=h+q_K.
}
\]

The required gap is independent of absolute depth.

The binary resource corner becomes

\[
\boxed{
n_h^*=h+q_K+1,
\qquad
m_h^*=h+q_K,
}
\]

provided

\[
h+q_K\le2^h-1.
\]

Minimizing over \(h\) recovers the repository's earlier exact binary structural
corner for a required integer gap \(q\).

Thus the old \(q\)-threshold theorem is the constant-marginal-value special
case of RF1.

## 7. Exponential opportunity value makes the required gap depth dependent

Take

\[
U(c)=v e^{-\mu c},
\qquad
v>0,
\quad
\mu>0.
\]

At adaptive depth \(h\),

\[
U(h)-U(j)
=
v e^{-\mu h}
\left[
1-e^{-\mu(j-h)}
\right].
\]

A necessary condition for any finite fixed burden to pay architecture cost is

\[
\boxed{
K<v e^{-\mu h}.
}
\]

If this fails, then

\[
\boxed{
J_K(h)=\infty.
}
\]

So sufficiently deep adaptive routes are evolutionarily impossible regardless
of how expensive fixed resolution becomes.

When

\[
K<v e^{-\mu h},
\]

define

\[
r_h
=
\frac{K e^{\mu h}}{v}
\in[0,1).
\]

The minimum required additive structural gap

\[
q_h=J_K(h)-h
\]

is

\[
\boxed{
q_h
=
\left\lfloor
-\frac{1}{\mu}
\log(1-r_h)
\right\rfloor
+1.
}
\]

Therefore

\[
\boxed{
J_K(h)
=
h+
\left\lfloor
-\frac{1}{\mu}
\log
\left(
1-\frac{K e^{\mu h}}{v}
\right)
\right\rfloor
+1.
}
\]

Unlike the linear model, the required gap increases with absolute adaptive
depth.

Natural history therefore penalizes "late savings": saving ten queries after an
already-long route can be less useful than saving a few queries early.

## 8. Corollary RF1.1 — exact maximum viable adaptive depth under exponential opportunity loss

A finite required fixed burden exists only if

\[
K<v e^{-\mu h}.
\]

Equivalently,

\[
h
<
\frac{1}{\mu}
\log\frac{v}{K}.
\]

For \(0<K<v\), the largest integer adaptive depth that can possibly repay the
architecture cost is

\[
\boxed{
h_{\max}^{\rm viable}
=
\left\lceil
\frac{1}{\mu}
\log\frac{v}{K}
\right\rceil
-1.
}
\]

This ceiling is independent of how many fixed query resources are available.

No amount of branch-exclusive fixed burden can rescue an adaptive route that
finishes after the biological value of timely completion has fallen below its
constitutive control cost.

## 9. Corollary RF1.2 — natural history turns one structural threshold into a Pareto set

Under a linear lift, one integer gap

\[
q_K
\]

summarizes the evolutionary requirement.

Under nonlinear time value, each adaptive depth has its own

\[
J_K(h).
\]

Therefore the minimum evolutionary architecture is generally not one scalar
complexity threshold.

It is a resource Pareto frontier over:

- adaptive depth;
- represented worlds;
- query resources;
- query arity.

This is the inverse form of the result that natural history re-ranks the exact
structural frontier.

## 10. Relation to PAYOFF

The forward interface is

\[
R_{\max}
=
\max_h[U(h)-U(I_h)].
\]

PAYOFF asks whether

\[
R-K>0.
\]

The inverse interface developed here asks what structural resources are needed
to make that inequality possible.

Thus:

\[
\boxed{
\text{natural history + architecture cost}
\to
J_K(h)
\to
\text{minimum finite information architecture}.
}
\]

This is the cleanest reverse bridge from fitness back to sensing structure.

## 11. Prior-art boundary

Inverse resource requirements are algebraically equivalent to the forward sharp
envelope, so they are not a separate independent novelty family.

Their biological role is interpretive and predictive:

- recover the old exact structural-gap theorem from a linear fitness model;
- show why nonlinear natural history makes required structural complexity
  depth dependent;
- give a direct minimum-world/query requirement for a declared architecture
  cost.

Do not claim novelty for integer inversion of a monotone utility function by
itself.
