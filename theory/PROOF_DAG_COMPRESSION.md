# Shared-state DAG compression of integer fixed-cover proofs

Status: exact finite deterministic proof engineering for `adaptive-gain`. It compresses an already verified bounded fixed-cover infeasibility proof; it does not weaken the fixed comparator or alter source scientific models.

## 1. Residual-state Markov property

The bounded fixed-cover continuation problem depends only on

```text
(U, A, B)
```

where

- `U` is the set of still-uncovered cross-target pairs;
- `A` is the set of still-available query identities;
- `B` is the remaining acquisition budget.

How that residual state was reached is irrelevant to future fixed-cover feasibility.

Therefore if two different branch histories reach exactly the same residual state,

\[
(U_1,A_1,B_1)=(U_2,A_2,B_2),
\]

their continuation infeasibility subproof is identical in logical content.

This is a state-equivalence statement, not a probabilistic Markov assumption.

## 2. Tree-to-DAG quotient theorem

Start from an independently verified recursive infeasibility proof tree produced by `fixed_budget_cover_decision()`.

Associate each proof occurrence with the exact residual state reconstructed from its parent transitions. Define an equivalence relation

\[
n_1\sim n_2
\iff
(U_{n_1},A_{n_1},B_{n_1})=(U_{n_2},A_{n_2},B_{n_2}).
\]

Merge equivalent nodes and redirect incoming proof branches to one shared representative.

Because every outgoing fixed-cover decision from a node is determined by the same residual state, this quotient preserves infeasibility exactly.

Thus a recursive proof tree can be represented as a directed acyclic graph of unique residual states.

Implementation: `adaptive_gain/proof_dag.py`.

## 3. Why the quotient is acyclic

Every proof branch selects one previously available query with strictly positive cost. Hence along an edge,

```text
available query count decreases by one
remaining budget strictly decreases.
```

A valid transition therefore cannot return to the same residual state or create a directed cycle.

The verifier nevertheless rejects inconsistent or cyclic references rather than relying only on this argument.

## 4. Independent DAG verifier

`verify_cover_proof_dag()` reconstructs the cross-target pair system from the declared task and checks, for every reachable DAG node:

- the node ID is associated with one and only one residual state;
- the stated uncovered pair is actually uncovered;
- the listed affordable separators are exactly all currently available separators within budget;
- every separator has the corresponding child edge;
- each child ID is reached with the exact updated `(U,A,B)` state;
- shared child IDs are accepted only when all incoming histories imply the same residual state;
- infeasible leaves have no affordable separator;
- all declared DAG nodes are reachable from the root.

The verifier also mathematically re-expands the DAG and checks the declared expanded-tree node count and compression fields.

A tampered child reference is rejected by regression tests.

## 5. Exact compression metrics

For one DAG node set, define

```text
N_tree = number of node occurrences after recursive tree expansion
N_DAG  = number of unique residual-state nodes
S      = N_tree - N_DAG
R      = N_tree / N_DAG.
```

Always

\[
N_{DAG}\le N_{tree},
\]

with equality exactly when no residual infeasibility state is reached by more than one proof history.

These are proof-representation metrics, not adaptive-gain effect sizes.

## 6. Registered reconvergence witness

A seeded synthetic eight-world / eight-query task has

```text
C_A = 3
C_F = 4.
```

At fixed budget `B=3`, the verified integer infeasibility search has 14 unique residual states but its recursive tree contains 19 node occurrences.

DAG quotienting gives

```text
N_tree = 19
N_DAG  = 14
shared-state savings = 5
compression ratio = 19/14 = 1.357142857...
```

The task is a proof-compression witness only; the numerical ratio is not asserted to be typical or maximal.

## 7. Relation to kernelization

DAG compression and residual kernelization act on different redundancies.

### Kernelization

Transforms a residual state to an equivalent smaller state by deleting inactive/dominated queries and propagating forced queries **before branching**.

### DAG compression

Keeps the residual decision structure unchanged but merges **different histories** that arrive at the same state.

Thus they can be composed:

```text
history
 -> exact residual kernel
 -> canonical state
 -> shared DAG node.
```

The current repository exports the two mechanisms separately so their guarantees and compression effects remain auditable.

## 8. Scope boundary

State-DAG memoization is standard dynamic-programming/proof-sharing structure; no novelty is claimed for DAG compression itself. The repository contribution is the explicit, independently checkable proof object tied to the adaptive-versus-fixed target-resolution comparison.

DAG compression does not change worst-case computational complexity. A problem with exponentially many distinct residual states can still require an exponentially large DAG.

The next question is whether kernelization plus symmetry quotienting can identify larger classes of residual states that are equivalent up to relabeling rather than exactly equal.

## Reproduce

```bash
python -m pytest -q tests/test_proof_dag.py
```
