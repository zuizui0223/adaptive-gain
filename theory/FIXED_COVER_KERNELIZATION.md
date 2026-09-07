# Exact residual kernelization for fixed target-pair cover

Status: finite deterministic bounded-cost theory for `adaptive-gain`. The reductions preserve the exact fixed-cover feasibility question; they are not heuristic approximations and do not alter the source scientific models.

## 1. Residual state

For a fixed acquisition budget decision, a residual state is

```text
(U, A, B)
```

where

- `U` is the set of still-uncovered cross-target world pairs;
- `A` is the set of not-yet-selected query identities;
- `B` is the remaining integer acquisition budget.

The question is whether some subset of `A` with total cost at most `B` covers every pair in `U`.

The existing integer proof tree branches on an uncovered pair and then on every affordable query that can cover that pair. Before that branching, three exact reductions can be applied to a fixed point.

## 2. Inactive / unaffordable query deletion

A query `q` can be removed when either

```text
cost(q) > B
```

or

```text
S_q intersection U = empty,
```

where `S_q` is the set of cross-target pairs separated by `q`.

The first condition means `q` cannot belong to any completion within the residual budget. The second means it contributes no coverage to any remaining obligation.

Therefore deleting such a query preserves bounded feasibility exactly.

## 3. Forced-query propagation

Suppose an uncovered pair `p` has exactly one remaining separator `q` after unaffordable queries have been removed.

Then every feasible fixed completion must include `q`. Hence the residual decision is equivalent to

```text
select q,
B <- B - cost(q),
U <- U minus S_q,
A <- A minus {q}.
```

No branching is required. This is the target-pair-cover analogue of unit propagation: one uncovered obligation has a unique available way to be satisfied.

If an uncovered pair has no remaining separator, the residual state is immediately infeasible.

## 4. Query dominance

For the current uncovered set `U`, define the residual cover of query `q` as

\[
R_q=S_q\cap U.
\]

If two available queries satisfy

\[
R_q\subseteq R_r
\]

and

\[
c(r)\le c(q),
\]

then `q` is dominated by `r` and may be deleted.

### Proof

Take any feasible completion containing `q`.

- If it already contains `r`, deleting `q` cannot uncover any pair that `r` does not also cover and weakly lowers cost.
- If it does not contain `r`, replace `q` by `r`. Coverage weakly increases and total cost does not increase.

Thus every completion using `q` has an equally cheap or cheaper completion not using `q`. Deleting `q` preserves existence of a completion within budget `B`.

For equal residual cover and equal cost, the implementation retains the lower declared query index so the kernel is deterministic.

## 5. Kernel fixed point

The three rules interact:

```text
remove inactive/unaffordable queries
-> detect / propagate forced queries
-> remove dominated queries
-> repeat
```

Dominance can create a unique remaining separator; forced selection can make other queries inactive; therefore reductions are iterated to a fixed point before genuine branching.

The resulting canonical residual state is then memoized. Histories that reduce to the same residual state share one continuation computation.

Implementation: `adaptive_gain/cover_kernel.py`.

## 6. Exactness statement

Let

```text
F(U,A,B)
```

mean that a fixed completion of cost at most `B` exists for residual pair set `U` using queries in `A`. Each reduction above maps a state `(U,A,B)` to a reduced state `(U',A',B')`, plus any forced query selections, such that

\[
\boxed{F(U,A,B)\iff F(U',A',B')}.
\]

Therefore an exact branching solver applied only after kernelization returns the same yes/no bounded fixed-cover decision as the unkernelized integer proof search.

The implementation still has a hard `max_states` cap. Exceeding it raises `CoverKernelLimitError`; it is never converted into an infeasibility claim.

## 7. Complete minimal-universe validation

For the entire balanced minimal universe

```text
4 worlds
binary target split 2+2
3 labeled binary unit-cost queries
```

all `16^3 = 4096` tasks are checked against the exact adaptive/fixed cost classification.

The kernelized decision at budget `B=C_A` reports strict gain for exactly the same 192 tasks and has

```text
false positive = 0
false negative = 0.
```

This validates the implementation over the complete deliberately tiny universe; it is not an empirical prevalence result.

## 8. Compression witness

A seeded eight-world / eight-query synthetic strict-gain control has

```text
C_A = 3
C_F = 4.
```

At fixed budget `B=3`, the existing unkernelized proof search visits 13 residual search states.

The kernelized solver closes the same infeasibility decision in one kernel call with no genuine branch state:

```text
forced query selections              = 3
dominated query removals              = 3
inactive/unaffordable query removals  = 2
canonical branch states               = 0.
```

Thus the reduction is not merely cosmetic on that witness: the fixed-side impossibility becomes propagation-only after safe residual simplification.

This single witness is not a universal compression ratio.

## 9. Relation to proof DAG compression

Kernelization and DAG sharing are different operations.

- **Kernelization** changes a residual state to an equivalent smaller state before branching.
- **DAG sharing** merges different branch histories that reach the same canonical residual state.

The current kernelized decision engine memoizes canonical states internally, but does not yet export the shared computation as a standalone proof DAG. The independently checkable recursive integer proof tree remains the authoritative proof object.

The next proof-engineering problem is to export canonical residual states once, reference them by node ID, and verify the resulting DAG without expanding shared subproofs.

## 10. Scope boundary

These reductions are standard covering-problem simplifications specialized to the repository's cross-target pair cover. The contribution here is their exact integration with adaptive-gain comparison, fail-closed implementation, complete minimal-universe regression, and explicit separation from the scientific source models.

They do not imply polynomial-time fixed-cover resolution: after kernelization the remaining integer cover decision can still require exponential branching in the worst case.

## Reproduce

```bash
python -m pytest -q tests/test_cover_kernel.py
```
