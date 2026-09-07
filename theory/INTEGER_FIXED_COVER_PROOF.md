# Integer fixed-cover proof trees

Status: exact finite deterministic certificate for `adaptive-gain`. It proves the bounded-cost fixed-cover decision problem needed for strict adaptive gain; it does not replace the source scientific models.

## 1. Why the LP gap matters

The fixed target-resolution problem is a weighted cover of cross-target world pairs. Private-pair, integral-packing, and fractional LP-dual certificates all give lower bounds on the fixed optimum `C_F`, but the repository contains a five-world strict-gain control with

```text
C_A = 2
fractional lower bound = 2
C_F = 3.
```

Thus the fractional relaxation cannot prove the real strict gain.

For strict gain, however, we do not need the exact value of `C_F`. We only need to decide whether a fixed resolver exists with cost at most the already-computed adaptive optimum `C_A`.

## 2. Bounded-cost decision problem

Given integer budget `B`, ask

```text
Does any fixed query bundle of total cost <= B separate every cross-target pair?
```

If the answer is no at `B=C_A`, then

\[
C_F>C_A,
\]

which is already a complete strict-adaptive-gain certificate.

## 3. Exact branching proof

At any partial fixed bundle, choose one cross-target pair that is still uncovered. Every completing resolver must contain at least one remaining query that separates that pair.

Therefore branch over **all** affordable remaining separators of that pair.

For each branch:

1. pay that query's integer cost;
2. remove every cross-target pair it separates;
3. remove that query from the remaining vocabulary;
4. recurse on the residual budget.

A node is infeasible when its chosen uncovered pair has no remaining separator whose cost fits the residual budget. A parent is infeasible when every affordable separator branch is infeasible.

This is exhaustive over feasible completions because every fixed resolver must cover the chosen pair somehow. It is not subset enumeration: the search branches only on separators of a currently uncovered obligation and memoizes residual states.

## 4. Independently checkable proof tree

`fixed_budget_cover_decision()` emits either:

- a concrete fixed resolving bundle within the budget; or
- an infeasibility proof tree.

`verify_fixed_budget_decision_certificate()` independently reconstructs the cross-target pair system from the task and checks that:

- the node's selected pair is still uncovered;
- the listed affordable separators are exactly all remaining affordable separators for that pair;
- every one of those separators has a corresponding child branch;
- child budgets, available-query sets, and uncovered-pair sets are updated correctly;
- infeasible leaves truly have no affordable separator.

The verifier does not trust the searcher's memoization state or heuristic choice. A tampered proof fails regression tests.

## 5. Integrality-gap witness

For the registered five-world LP-gap control,

```text
C_A = 2
LP lower bound = 2
C_F = 3.
```

Private-pair, integral-packing, and fractional-packing layers are incomplete. The integer proof tree at budget 2 certifies

```text
no fixed resolver of cost <= 2
```

and therefore

\[
\boxed{C_F\ge3>C_A=2}.
\]

No global fixed optimum needs to be computed for that strict-gain conclusion.

## 6. No-gain control

For the routing-bypass control, the same bounded-cost decision at `B=C_A=2` returns a constructive fixed bundle of cost 2. The integer certificate therefore correctly refuses a strict-gain claim.

## 7. Certificate ladder

The current hierarchy is

```text
private-pair necessity
  -> integral pair packing
  -> fractional pair-cover dual
  -> exact integer budget-infeasibility proof
  -> exact fixed optimum, only when its numerical value is needed
```

The first three are lower-bound relaxations. The fourth is an exact yes/no proof for the one budget relevant to strict gain. The fifth solves the stronger optimization problem.

The integer proof can still be exponential in the worst case. `max_states` is a hard resource cap; hitting it raises `IntegerCoverProofLimitError` and is never reported as infeasibility.

## 8. Claim boundary

This is a standard exact branching principle for an integer covering decision problem specialized to cross-target pair cover. The contribution of this repository is the verified connection to adaptive-tree cost comparison and the explicit proof object, not a claim of a new general integer-programming algorithm.

## Reproduce

```bash
python -m pytest -q tests/test_integer_cover_proof.py
python examples/audit_certificate_ladder.py
```
