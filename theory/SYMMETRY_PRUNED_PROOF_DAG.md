# Symmetry-pruned fixed-cover proof DAG

Status: exact finite deterministic theorem and proof-object contract for the
`adaptive-gain` target-pair-cover abstraction. It is a proof-compression result,
not a new biological claim and not a polynomial-time guarantee.

## 1. Residual fixed-cover instance

A residual fixed-cover instance is represented by

```text
I = (P, Q, c, M, B)
```

where `P` is the remaining cross-target pair-obligation set, `Q` the remaining
query identities, `c` their positive integer acquisition costs, `M` the
pair-query incidence, and `B` the remaining budget.

A query automorphism of `I` is a cost-preserving permutation of `Q` that leaves
the multiset of pair-incidence rows unchanged.

## 2. Branch-orbit theorem

Let `g` be an automorphism of residual instance `I`, and let

\[
g(q)=r.
\]

Write `I \ q` for the residual child obtained after purchasing query `q`: every
obligation separated by `q` is removed, query `q` is removed from the vocabulary,
and the budget is reduced by `c(q)`.

Then

\[
\boxed{I\setminus q \cong I\setminus r}.
\]

### Proof

Because `g` is a query automorphism:

1. `c(q)=c(r)`;
2. `g` bijects `Q\{q}` with `Q\{r}`;
3. applying `g` to every incidence row preserves the row multiset;
4. an obligation row contains `q` iff its transformed row contains `r`.

Therefore the rows removed after selecting `q` are mapped exactly to the rows
removed after selecting `r`. Restricting `g` to the surviving query vocabularies
preserves all surviving incidence and all query costs, while both children have
the same residual budget. Hence the two child pair-cover instances are
isomorphic. QED.

Notice that `g` need not fix the particular obligation chosen by a branching
heuristic. The theorem compares the complete residual children after query
selection, not the names of the parent obligation rows.

## 3. Exact orbit pruning of an infeasibility proof

Suppose a proof node chooses one uncovered obligation and its affordable
separator set is

\[
A_v\subseteq Q.
\]

Partition `A_v` by the exact query-automorphism orbits of the parent residual
instance. Let

\[
b(v)=|A_v|
\]

be the raw number of affordable branches and let

\[
o(v)=|A_v/\operatorname{Aut}(I_v)|
\]

be the number of nonempty orbit intersections.

By the branch-orbit theorem, every branch inside one orbit has an isomorphic
child decision problem. Therefore a fixed-cover **infeasibility** certificate
needs one recursive child proof per orbit, provided every skipped branch carries
an explicit isomorphism transport to that orbit representative child.

Thus

\[
\boxed{o(v)\le b(v)}
\]

and the exact local branch saving is

\[
\boxed{s(v)=b(v)-o(v)}.
\]

Across the stored proof DAG nodes,

\[
\boxed{S=\sum_v s(v)
      =\sum_v b(v)-\sum_v o(v)}.
\]

`S` is proof/search branch compression. It is **not** the scientific adaptive
gain `C_F-C_A`.

## 4. Local group-order bound

For a branch node with `b(v)>0`, define the local compression factor

\[
\rho_v=\frac{b(v)}{o(v)}.
\]

Each nonempty branch-orbit intersection has size at most
`|Aut(I_v)|`. The ratio `b(v)/o(v)` is the average size of those intersections,
so

\[
\boxed{1\le\rho_v\le |\operatorname{Aut}(I_v)|}.
\]

This bound can be loose because the affordable separator set may contain only a
small part of a large query orbit.

## 5. Explicit proof object

`adaptive_gain/symmetry_pruned_proof_dag.py` stores, for every branching node:

- the complete parent residual instance;
- an exact automorphism-group receipt;
- the complete affordable separator set;
- its partition into query-orbit intersections;
- one recursively proved representative query per orbit;
- an explicit child-to-representative-child query bijection for every skipped
  symmetric branch; and
- the usual explicit transport from the representative child to any shared
  isomorphism-DAG node.

The independent verifier reconstructs every child from the parent query,
rechecks the parent automorphism receipt, recomputes the branch-orbit partition,
and verifies every stated child transport directly. It does not accept an orbit
label or a canonical signature as proof by itself.

`adaptive_gain/proof_size_bounds.py` separately recomputes the branch counts,
automorphism-receipt count, local compression factors, and the group-order bound
from the stored proof object. This separates semantic proof verification from
execution/accounting metadata.

## 6. Registered C4 control

The reusable synthetic control `cycle_branch_symmetry_control()` has four
unit-cost queries whose cross-target separator rows are

```text
0011, 0110, 1001, 1100.
```

At fixed budget 1, the root branching obligation has two affordable separators.
The residual query automorphism group has order 8, and the two affordable queries
belong to one query orbit. Therefore

\[
b=2,\qquad o=1,\qquad s=1,\qquad \rho=2.
\]

The ordinary isomorphism-transport proof expands both branches; the
symmetry-pruned proof recursively proves only one and supplies an explicit
transport for the other.

This is a structural synthetic witness, not an empirical frequency claim.

## 7. Complete minimal-universe regression

For the complete declared minimal universe

```text
4 worlds
binary target split 2+2
3 labeled binary unit-cost queries
```

all `16^3 = 4096` tasks are compared with the exact adaptive/fixed optimizer.
The symmetry-pruned decision at `B=C_A` reports exactly the same 192 strict-gain
tasks with zero false positives and zero false negatives.

This finite regression validates the implementation over that tiny universe; it
does not establish prevalence beyond it.

## 8. Relation to the other compression layers

The proof-compression stack now separates four ideas:

1. **kernelization** removes semantically redundant pair/query obligations;
2. **exact-state DAG sharing** merges identical residual states;
3. **isomorphism transport** merges label-different but structurally identical
   residual states; and
4. **parent automorphism branch pruning** avoids recursively proving several
   sibling branches whose children are guaranteed isomorphic.

These can overlap but are not the same operation.

## 9. Current limitation

The branch pruning is exact only after an exact parent automorphism group has
been certified. The current small-task implementation obtains that group by
enumerating every stable-color-preserving query permutation up to a hard cap.
Therefore the next computational problem is to certify generators/stabilizers
without paying that full candidate-enumeration cost.

Exceeding any declared symmetry or proof-search cap remains fail-closed and is
never converted into a strict-gain or non-isomorphism claim.

## Reproduce

```bash
python -m pytest -q tests/test_symmetry_pruned_proof_dag.py
python -m pytest -q tests/test_branch_orbit_proof_size.py
```
