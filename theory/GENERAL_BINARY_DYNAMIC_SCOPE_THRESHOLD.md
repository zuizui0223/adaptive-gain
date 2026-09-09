# General binary information-scope threshold for a required dynamical gap

## Purpose

The canonical `6 worlds / 5 binary queries / 5 productive-frontier obligations`
example is only one response normalization.  The general statement is simpler.

Suppose a downstream local dynamical regime requires an integer structural gap

\[
\Delta g=C_F-C_A\ge q,
\qquad q\in\mathbb Z_{\ge1}.
\]

For binary deterministic unit-cost sensing, define

\[
\boxed{
h^*(q)=\min\{h\ge1:2^h-1-h\ge q\}.
}
\]

Then the componentwise first binary structural corner capable of gap `q` is

\[
\boxed{
C_A^*=h^*,\quad
C_F^*=h^*+q,
}
\]

and therefore

\[
\boxed{
n^*=h^*+q+1,\qquad
m^*=h^*+q,\qquad
E^*=h^*+q,
}
\]

where `n` is represented-world count, `m` is declared-query count, and
`E=|H_min|` is the number of minimal productive-frontier obligations.

The result is a composition of the repository's existing binary flattening,
world/query/frontier lower bounds, and constructive tree-to-task theorem.  No
novelty is claimed for full-binary-tree counting by itself.

---

## 1. Why the adaptive-depth threshold is exact

At adaptive cost `h`, binary flattening gives

\[
C_F\le2^h-1.
\]

Hence

\[
\Delta g=C_F-h\le2^h-1-h.
\]

Therefore any task with gap at least `q` must satisfy

\[
h\ge h^*(q).
\]

Conversely, by definition of `h^*`,

\[
h^*+q\le2^{h^*}-1.
\]

A productive binary tree of height `h^*` can therefore be chosen with exactly
`h^*+q` internal nodes.  The private-pair tree-to-task construction assigns one
physical query to each internal node, making every such query fixed-mandatory.
Thus

\[
C_F=h^*+q.
\]

The constructed adaptive tree has cost at most `h^*`.  It cannot have smaller
optimal adaptive cost.  If `C_A\le h^*-1`, binary flattening would imply

\[
C_F\le2^{h^*-1}-1.
\]

But minimality of `h^*` gives

\[
2^{h^*-1}-1-(h^*-1)<q,
\]

so

\[
2^{h^*-1}-1<h^*+q=C_F,
\]

a contradiction.  Hence

\[
\boxed{C_A=h^*}
\]

exactly.

---

## 2. World, query, and productive-frontier lower bounds

Since the target-separation problem has unit costs,

\[
C_F\le n-1,
\qquad
C_F\le m,
\qquad
C_F\le |\mathcal H_{\min}|.
\]

The first inequality is the inherited represented-world bound; the second is
trivial from declared-query count; the third is the productive-frontier
hitting-set bound.

Because any gap-`q` task has

\[
C_F\ge h^*(q)+q,
\]

it follows that

\[
\boxed{
n\ge h^*+q+1,\quad
m\ge h^*+q,\quad
|\mathcal H_{\min}|\ge h^*+q.
}
\]

The constructive binary witness attains all three simultaneously.  Thus the
corner is componentwise sharp.

---

## 3. Exact logarithmic routing overhead

Let

\[
k(q)=\left\lceil\log_2(q+1)\right\rceil.
\]

Then

\[
\boxed{h^*(q)\in\{k(q),k(q)+1\}.}
\]

The lower bound follows because `2^h-1>=q` is necessary.  For the upper bound,
`2^k>=q+1`, so

\[
2^{k+1}\ge2(q+1)\ge q+k+2
\]

for every `q>=1` because `q>=k`.  Hence `h=k+1` always satisfies
`2^h-1-h>=q`.

Therefore

\[
\boxed{
h^*(q)=\log_2 q+O(1)
}
\]

and

\[
\boxed{
n^*=q+\log_2 q+O(1),\qquad
m^*=E^*=q+\log_2 q+O(1).
}
\]

Interpretation: increasing the required structural gain mainly increases the
number of fixed-mandatory information obligations linearly.  The adaptive routing
overhead grows only logarithmically.

---

## 4. Mapping response geometry to information complexity

For the generalized local response,

\[
G=a\,\Delta g,
\qquad a>0,
\]

and the complex-eigenvalue threshold is

\[
G_{\rm osc}
=\frac{(\alpha-\phi)^2}{4(1-\phi)}.
\]

The smallest integer gap entering the oscillatory region is

\[
q_{\rm osc}
=\min\{q\in\mathbb Z_{\ge0}:aq>G_{\rm osc}\}.
\]

If the same integer gap also satisfies `a q < G_+`, stable oscillation is
available on the unit-cost integer ladder.  Substituting `q_osc` into the binary
scope theorem gives

\[
\boxed{
(\alpha,\phi,a)
\to q_{\rm osc}
\to h^*(q_{\rm osc})
\to(n^*,m^*,E^*).
}
\]

This is the general statement behind the earlier canonical `6/5/5` corollary.

---

## 5. Canonical recovery

For

\[
\alpha=1,\qquad \phi=1/2,\qquad a=1/8,
\]

we have `q_osc=2`.  Since

\[
2^2-1-2=1<2,
\qquad
2^3-1-3=4\ge2,
\]

`h^*=3`.  Therefore

\[
\boxed{(n^*,m^*,E^*)=(6,5,5)}.
\]

The existing sharp bounded-arity witness realizes exactly this corner with
`C_A=3`, `C_F=5`, and five singleton productive-frontier obligations.

---

## 6. Scope and novelty boundary

This theorem assumes finite deterministic binary unit-cost sensing and uses the
repository's existing adaptive/fixed-resolution semantics.  The dynamical lift
adds the local deterministic relation `G=a Delta_g` only after the structural
threshold has been established.

No novelty is claimed for binary tree node counting, logarithms, or the standard
complex-eigenvalue threshold.  The candidate contribution is the exact map

\[
\boxed{
\text{required dynamical gain}
\to
\text{required structural gap}
\to
\text{minimum finite information complexity}.
}
\]
