# From feedback geometry to a bounded-arity information Pareto frontier

## Statement

The generalized local response determines a strict complex-eigenvalue threshold

\[
G_{\rm osc}
=
\frac{(\alpha-\phi)^2}{4(1-\phi)}
\]

and an upper stability boundary

\[
G_+=\frac{1-\alpha\phi}{1-\phi}.
\]

Under a linear structural lift

\[
G=a\,\Delta g,
\qquad a>0,
\]

the smallest integer structural gap entering the oscillatory region is

\[
q_{\rm osc}
=
\min\{q\in\mathbb Z_{\ge0}:aq>G_{\rm osc}\},
\]

while stable oscillation is available only if some integer gap also satisfies

\[
aq<G_+.
\]

For a declared maximum query arity `b>=2`, let

\[
\mathcal P_b(q)
\]

denote the exact structural Pareto frontier from `ARITY_GAP_PARETO.md`.

Then the first finite-information scopes capable of stable oscillatory feedback are

\[
\boxed{
(\alpha,\phi,a,b)
\longrightarrow
q_{\rm osc}
\longrightarrow
\mathcal P_b(q_{\rm osc}),
}
\]

provided the integer gap ladder contains a stable gap.  If the first oscillatory integer gap already lies at or above the upper stability boundary, the Pareto set is empty.

---

## Binary special case

For `b=2`, the structural Pareto frontier collapses to the unique componentwise first corner

\[
(n^*,m^*,E^*)
=
(h_2^*+q+1,\ h_2^*+q,\ h_2^*+q).
\]

Hence the previous binary formula is exactly the `b=2` specialization of the general Pareto statement.

At

\[
\alpha=1,
\qquad
\phi=1/2,
\qquad
a=1/8,
\]

one has `q_osc=2` and therefore

\[
\mathcal P_2(2)=\{(6,5,5)\}.
\]

---

## Higher arity can change the kind of minimum

For the same dynamic geometry but ternary queries,

\[
\mathcal P_3(2)=\{(6,4,4)\}.
\]

The minimum world count remains six, while one query/frontier obligation is saved.

For a response geometry whose first oscillatory integer gap is `q=3`, quaternary sensing yields

\[
\boxed{
\mathcal P_4(3)
=
\{(8,5,5),\ (7,6,6)\}.
}
\]

The first point minimizes query/frontier burden; the second minimizes represented-world burden.  Neither dominates the other.

Thus bounded arity changes not merely the numerical value of a minimum but sometimes the **mathematical type of the reachability constraint**:

```text
binary
    -> one componentwise minimum

higher arity
    -> potentially multiple nondominated information structures
```

---

## Biological interpretation within the declared abstraction

The result should not be read as a literal count of sensory organs or species.  Within the finite structural abstraction:

- represented worlds quantify the number of distinct ecological states that must coexist in the resolving problem;
- declared queries quantify available information channels;
- productive-frontier edges quantify fixed-mandatory information obligations;
- query arity quantifies how many distinct outcomes one information channel can return.

A required eco-evolutionary gain therefore constrains these dimensions differently. Richer single cues can reduce the number of channels or mandatory obligations, but they cannot generally reduce the minimum number of represented ecological states required to support the same adaptive/fixed gap.

---

## Scope and novelty boundary

The theorem assumes finite deterministic unit-cost sensing, a hard query-arity cap, linear structural-to-feedback gain, and the local generalized response model.

No novelty is claimed for bounded-arity tree counting, Pareto optimization, or complex-eigenvalue thresholds individually.  The repository-specific contribution is the exact composition

\[
\boxed{
\text{dynamical phase requirement}
\to
\text{integer adaptive/fixed gap}
\to
\text{bounded-arity information Pareto frontier}.
}
\]
