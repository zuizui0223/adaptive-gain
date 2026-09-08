# Global-label-once policy trees are a syntactic restriction, not ordinary one-use resource semantics

The standard finite adaptive model already removes a query after it is measured on a realized history. Therefore no realized run measures the same physical query twice.

A stronger restriction can nevertheless be imposed on the **written policy tree**:

> each declared query name may label at most one node anywhere in the entire counterfactual tree.

This note calls that restriction **global-label-once**.

It must not be confused with ordinary single-run resource consumption.

## 1. Pointwise containment fails

Consider four worlds

\[
a_0,b_0,a_1,b_1
\]

with targets

\[
T(a_i)=0,\qquad T(b_i)=1.
\]

There are two unit-cost queries:

```text
route = (0,0,1,1)
assay = (0,1,1,0)
```

Neither query alone resolves the target. The fixed bundle `{route, assay}` does, so

\[
C_F=2.
\]

Under the ordinary adaptive semantics, measure `route` first. Each outcome leaves one mixed pair, and `assay` resolves either pair. The same query label appears in two mutually exclusive counterfactual branches, but only one copy is executed on any realized run. Hence

\[
C_A=2.
\]

Under global-label-once syntax, that tree is forbidden because `assay` appears twice. Reversing the order has the same problem: after `assay`, resolving both mixed outcomes would require `route` in both branches.

With only two query identities there is no globally label-unique resolving tree. Thus

\[
\boxed{
C_A=C_F=2,
\qquad
C_G=\infty\;(\text{unresolved}),
}
\]

where `C_G` denotes the global-label-once adaptive optimum.

Therefore the ordinary containment

\[
C_A\le C_F
\]

must **not** be transferred to `C_G`.

The reason is conceptual: a fixed bundle is an operational set of measurements, not necessarily a globally label-unique tree syntax.

## 2. Exact small-task solver

`adaptive_gain/global_once_policy_semantics.py` implements an exact solver for small tasks.

For every world subset it enumerates globally label-unique subtree plans. A plan carries the set of query identities used anywhere in that subtree. When combining different unresolved child branches, their used-query sets must be pairwise disjoint.

This introduces counterfactual coupling absent from the ordinary Bellman recursion.

The solver is deliberately fail-closed behind query/option caps; exceeding a cap raises `GlobalOnceSearchLimitError` rather than returning an approximate feasibility judgment.

## 3. The extremal maximum is nevertheless unchanged

Now restrict attention to tasks that **are** global-label-once resolvable, with

- `n` represented worlds,
- `m` unit-cost queries,
- query arity at most `b`, and
- global-label-once optimum `C_G=h`.

A global-label-once tree has one distinct physical query at every internal node. Its internal-node count is at most the sharp bounded-arity tree quantity

\[
F_b(n,h).
\]

Flattening all node queries gives a fixed resolver, so

\[
C_F\le\min\{m,F_b(n,h)\}.
\]

Hence

\[
\frac{C_F}{C_G}
\le
\max_h\frac{\min\{m,F_b(n,h)\}}{h}
=R_b(n,m).
\]

The existing sharp bounded-arity construction assigns a different physical query to every internal node **by construction**. Therefore it is already global-label-once and attains `R_b(n,m)`.

Thus, over the subclass of globally label-unique resolvable tasks,

\[
\boxed{
R_b^{\mathrm{global\text{-}label\text{-}once}}(n,m)
=R_b(n,m).
}
\]

So there are two simultaneous facts:

```text
pointwise class containment: can fail badly
extremal maximum over feasible global-once tasks: unchanged
```

These are not contradictory.

## 4. Interpretation

The registered counterexample shows why resource semantics must be phrased operationally.

In a decision tree, repeated query labels on mutually exclusive branches mean

> whichever branch is realized, measure that physical query once there.

They do **not** mean the experiment pays for or executes multiple copies on one run.

A genuine resource constraint that limits total uses across actual time, samples, calibration cycles, destructive specimens, or inventory must be represented in the state of the realized process. Merely banning repeated labels in a counterfactual tree is a different mathematical restriction.

## 5. Scope

The result concerns finite deterministic exact target resolution and the particular global-label-once tree syntax defined above. It does not model stochastic replenishment, destructive sampling across multiple simultaneously realized subjects, shared laboratory inventory, or calibration-changing actions.

Implementation and regression:

- `adaptive_gain/global_once_policy_semantics.py`
- `tests/test_global_once_policy_semantics.py`
