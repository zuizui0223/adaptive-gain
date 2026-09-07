# Extremal depth-two routing family

This note gives an explicit infinite family in the repository's finite deterministic guaranteed-target-resolution contract.

All query costs are one. Query outcome alphabets may be finite and need not be binary.

## 1. Construction

Fix an integer `k >= 2`.

Create `2k` represented worlds

\[
a_1,\ldots,a_k,\qquad b_1,\ldots,b_k,
\]

with

\[
T(a_i)=0,\qquad T(b_i)=1.
\]

Use `k+1` unit-cost queries.

### Router

The router has `k` outcomes and satisfies

\[
r(a_i)=r(b_i)=i.
\]

Thus every router outcome leaves exactly one target-mixed pair

\[
\{a_i,b_i\}.
\]

### Terminal queries

There is one binary terminal query `q_i` for every branch.

Choose the orientations

- `q_1(b_1)=1` and zero everywhere else;
- for `i>=2`, `q_i(a_i)=1` and zero everywhere else.

Each pair `(a_i,b_i)` is separated by `q_i` and by no other terminal query.

The implementation is `adaptive_gain/extremal_routing.py`.

## 2. Exact adaptive cost

Measure the router first. Outcome `i` leaves only `(a_i,b_i)`, so `q_i` resolves that branch.

Hence

\[
C_A\le2.
\]

No single query resolves the target: the router leaves every pair `(a_i,b_i)` mixed, while every terminal query is constant on many cross-target pairs. Therefore

\[
\boxed{C_A=2}.
\]

## 3. Exact fixed cost

For every `i`, pair `(a_i,b_i)` is separated only by terminal `q_i`. Thus every fixed resolving bundle must contain all `k` terminal queries.

The router is also mandatory. Pair `(a_1,b_2)` has the same outcome under every terminal query but different router outcomes. Hence every fixed resolver must also contain the router.

Therefore all `k+1` queries are globally mandatory and the complete vocabulary resolves:

\[
\boxed{C_F=k+1}.
\]

The productive-frontier formulation gives the same proof. Its inclusion-minimal hyperedges are exactly the singleton sets

\[
\{r\},\{q_1\},\ldots,\{q_k\}.
\]

A fixed resolver is a hitting set of this frontier, so it must buy every query.

## 4. Unbounded adaptive advantage

Consequently

\[
\boxed{C_F-C_A=k-1}
\]

and

\[
\boxed{\frac{C_F}{C_A}=\frac{k+1}{2}}.
\]

As `k` grows, both the additive advantage and the fixed/adaptive cost ratio are unbounded.

Thus the previously registered `3/2` ratio in the four-world minimal normal form is not a universal upper bound. It is only the first member (`k=2`) of this family.

The statement is structural. It does not say that large routing gains are common in empirical experiments.

## 5. A sharp world-count bound for depth two

Consider any unit-cost finite deterministic task with `n` represented worlds and

\[
C_A=2.
\]

Take an optimal adaptive policy. Its root query has some target-pure children and some target-mixed children. Every mixed child contains at least two represented worlds of different targets, so the number of mixed children is at most

\[
\lfloor n/2\rfloor.
\]

Each mixed child is resolvable by one second query. Flatten the root plus one second query for each mixed child. This is a valid fixed bundle with at most

\[
1+\lfloor n/2\rfloor
\]

distinct unit-cost queries. Therefore

\[
\boxed{C_F\le1+\lfloor n/2\rfloor\qquad(C_A=2).}
\]

Equivalently,

\[
\boxed{
\frac{C_F}{C_A}
\le
\frac{1+\lfloor n/2\rfloor}{2}
\qquad(C_A=2).
}
\]

For `n=2k`, the constructed family has `C_F=k+1`, so it saturates this bound exactly.

## 6. First possible ratio above 3/2

The `k=3` member has

```text
6 worlds
4 queries
C_A = 2
C_F = 4
C_F/C_A = 2
```

and is minimal in two senses under unit query costs.

### At least four queries are necessary

With at most three declared unit-cost queries,

\[
C_F\le3.
\]

If `C_A=1`, then the resolving query is itself a fixed resolver, so `C_F=1`. Otherwise `C_A>=2`, giving

\[
C_F/C_A\le3/2.
\]

Hence ratio strictly above `3/2` requires at least four queries.

### At least six worlds are necessary

Suppose `n<=5`.

- If `C_A=1`, then `C_F=1`.
- If `C_A=2`, the depth-two bound gives `C_F<=1+floor(5/2)=3`, hence ratio at most `3/2`.
- If `C_A>=3`, flatten an optimal productive decision tree. A tree on `n` represented worlds has at most `n` nonempty leaves and therefore at most `n-1` internal nodes. Its union is a fixed resolver using at most `n-1<=4` distinct unit-cost queries. Thus
  \[
  C_F/C_A\le4/3.
  \]

Therefore no task with at most five represented worlds can have ratio above `3/2`.

The six-world, four-query `k=3` construction attains both lower bounds simultaneously.

## 7. Connection to the existing normal form

For `k=2`, the construction has four worlds, three binary queries and

\[
(C_A,C_F)=(2,3).
\]

Its canonical separator signature is exactly the repository's unique minimal strict-gain signature

\[
\boxed{(3,5,9)}.
\]

So the old minimal normal form is the first member of the extremal routing family rather than an isolated exception.

## 8. Claim boundary

The theorem assumes:

- finitely many represented worlds;
- deterministic query outcomes;
- guaranteed exact target resolution;
- positive unit acquisition costs for the stated extremal/minimality formulas.

The unbounded family uses a router whose outcome arity grows with `k`. It does not by itself prove the same quantitative ratio for a globally binary-query vocabulary. No empirical prevalence or biological report claim follows from the construction.
