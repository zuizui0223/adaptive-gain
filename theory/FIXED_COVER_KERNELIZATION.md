# Exact two-sided residual kernelization for fixed target-pair cover

Status: finite deterministic bounded-cost theory for `adaptive-gain`. The reductions preserve the exact fixed-cover feasibility question; they are not heuristic approximations and do not alter the source scientific models.

## 1. Residual state

A residual fixed-cover decision is

```text
(U, A, B)
```

where `U` is the set of still-uncovered cross-target world-pair obligations, `A` the still-available query identities, and `B` the remaining integer acquisition budget.

The question is whether some subset of `A` of total cost at most `B` covers every pair in `U`.

Before any genuine branching, the implementation now applies **four** exact reductions to a fixed point.

## 2. Inactive / unaffordable query deletion

A query `q` may be removed if

\[
c(q)>B
\]

or if it separates no pair in `U`.

Such a query cannot occur in any feasible residual completion or contributes no remaining coverage. Deletion preserves feasibility exactly.

## 3. Pair-obligation dominance

For an uncovered pair `p`, let

\[
Sep_A(p)=\{q\in A:q\text{ separates }p\}.
\]

Suppose two uncovered obligations satisfy

\[
Sep_A(p_{hard})\subseteq Sep_A(p_{easy}).
\]

Any fixed completion that covers `p_hard` must choose at least one query in `Sep_A(p_hard)`, and every such query also lies in `Sep_A(p_easy)`. Therefore covering the harder pair automatically covers the easier pair.

Hence `p_easy` is redundant and can be deleted from `U`.

Equal separator signatures retain the lower declared pair index only to make the kernel deterministic.

This is the constraint-side dual of query dominance below.

## 4. Forced-query propagation

If some remaining pair has exactly one available separator `q`, every feasible completion must buy `q`. Therefore

```text
select q
B <- B - cost(q)
U <- U minus all pairs covered by q
A <- A minus {q}
```

is feasibility-equivalent to the original residual state.

If any remaining pair has no separator, the residual state is immediately infeasible.

## 5. Query dominance

For current obligations `U`, define

\[
R_q=S_q\cap U,
\]

where `S_q` is the full pair cover of query `q`.

If available queries `q,r` satisfy

\[
R_q\subseteq R_r,
\qquad
c(r)\le c(q),
\]

then `q` can be removed. Any completion using `q` can replace it by `r` or delete `q` when `r` is already present, weakly improving coverage without increasing cost.

Equal cover and cost keep the lower query index deterministically.

## 6. Two-sided fixed point

The reductions interact and are repeated:

```text
remove inactive / unaffordable queries
-> remove dominated pair obligations
-> propagate forced queries
-> remove dominated queries
-> repeat
```

At a nonterminal fixed point:

- every remaining pair has at least two available separators;
- no remaining pair-separator signature contains another remaining signature;
- every remaining query covers at least one remaining obligation and is affordable;
- no remaining query has a residual cover contained in another weakly cheaper query's cover.

Thus the residual incidence matrix has been simplified on **both rows and columns** before branching. For unit query costs, both sides are literal inclusion antichains after duplicate tie-breaking; with unequal costs, the query side uses cover inclusion jointly with cost dominance.

Implementation: `adaptive_gain/cover_kernel.py`.

## 7. Exactness theorem

Write `F(U,A,B)` for existence of a fixed completion within residual budget. Each reduction maps the state to a smaller state `(U',A',B')`, plus forced selections where applicable, such that

\[
\boxed{F(U,A,B)\iff F(U',A',B')}.
\]

Therefore exact branching after the fixed point returns the same bounded fixed-cover decision as the unkernelized integer proof.

The hard `max_states` cap remains fail-closed: exceeding it raises `CoverKernelLimitError`, never an infeasibility conclusion.

## 8. Sperner bound on pair obligations

After pair-obligation dominance, the distinct nonempty separator signatures are an antichain of subsets of the remaining `m` query identities.

By Sperner's theorem,

\[
\boxed{
|U_K|
\le
{m\choose\lfloor m/2\rfloor}
}
\]

for the number of distinct minimal pair-obligation signatures in such a residual kernel.

`adaptive_gain/kernel_bounds.py` independently checks this combinatorial receipt. The bound is on distinct separator signatures; multiple world pairs with the same signature are one logical cover obligation after dominance.

The bound does **not** make the overall problem polynomial in the original input: the middle binomial coefficient is exponential in `m`.

## 9. Minimal strict-gain form saturates the bound

The unique minimal strict-gain normal form has three queries. Its four raw cross-target pairs reduce to separator signatures

\[
\{001,010,100\}.
\]

Hence

\[
|U_K|=3={3\choose1},
\]

so the pair-obligation Sperner bound is exactly tight at the smallest strict-gain example.

This gives a combinatorial reading of the normal form: every one of the three queries owns a minimal singleton obligation, while the fourth raw pair separated by all three queries is dominance-redundant.

## 10. Complete minimal-universe validation

Across all

\[
16^3=4096
\]

labeled 4-world / 3-binary-query tasks with target split 2+2:

- the exact adaptive/fixed strict-gain classification has 192 positive tasks;
- the kernelized decision at `B=C_A` returns the same 192 positives;
- false positives = 0;
- false negatives = 0;
- the pair-antichain receipt satisfies the Sperner bound in every task.

These are complete finite regression results, not empirical frequencies.

## 11. Compression witness

A seeded eight-world / eight-query strict-gain control has

```text
C_A=3
C_F=4.
```

The unkernelized bounded proof visits 13 search states at `B=3`. The two-sided kernel closes infeasibility in one kernel call with no genuine branch state:

```text
dominated pair removals               = 12
forced query selections               = 3
dominated query removals               = 3
inactive/unaffordable query removals   = 2
canonical branch states                = 0.
```

The example demonstrates possible compression, not a universal ratio.

## 12. Relation to proof DAG compression

Kernelization and proof sharing remove different redundancies:

- **kernelization** replaces one residual state by a smaller equivalent state;
- **proof DAG quotienting** merges different histories that reach the same residual state.

The repository now implements both. `proof_dag.py` exports shared-state DAG certificates from independently verified recursive integer proofs and verifies every residual-state reference separately.

A registered DAG witness has 19 recursively expanded node occurrences but 14 unique residual states, so five subproof occurrences are shared.

The next structural compression problem is to identify states equivalent **up to relabeling/isomorphism**, not only bit-identical states.

## 13. Scope boundary

Dominance reduction, forced selection, Sperner's theorem, memoization and proof DAGs are established combinatorial ideas. The contribution here is their explicit, fail-closed integration into the adaptive-versus-fixed target-resolution bridge and the exact finite validation suite.

None of these reductions claims polynomial worst-case complexity, nor do they establish how often the synthetic structures occur in natural systems.

## Reproduce

```bash
python -m pytest -q tests/test_cover_kernel.py
python -m pytest -q tests/test_kernel_bounds.py
python -m pytest -q tests/test_proof_dag.py
```
