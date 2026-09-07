# Recursive continuation equivalence: an adaptive-safe quotient with a fixed-side boundary

## Answer

A cost-labelled recursive continuation quotient preserves the deterministic
minimum worst-path adaptive acquisition cost. It can identify states with
different world subsets, different query names and different immediate
separation masks. It is built from transitions before Bellman minima are
computed, and its certificate is independently checked by reconstructing every
productive query and every supported mixed child.

**The quotient does not determine fixed-bundle cost or adaptive gain.** A
four-world pair of tasks has exactly the same recursive root class, but costs
`(C_A,C_F)=(2,3)` and `(2,2)`. Thus an adaptive-safe compression must not replace
the fixed comparator.

This extends the continuation-equality and static refinement work present at
baseline commit `44c39b7b48ddd1452303b28150950339d44be732`. The five-world
`(7,28,42)` deletion-minimal classification was already present at that baseline;
it is not claimed as a new addition of this module.

## 1. Scope and definition

A task has a finite represented world set, deterministic outcomes, a target map,
and strictly positive integer query acquisition costs. Each named query may be
acquired at most once along a path. A state is `(task,A,R)`, where `A` is the
nonempty surviving world set and `R` is the remaining query vocabulary.

A state is *resolved* when every world in `A` has the same target. A query is
*productive* if it has at least two supported outcome cells in `A`. Positive-cost
constant queries may be omitted: they cannot improve the worst-path optimum.

For productive query `q`, let `M(s,q)` be the family of its target-mixed children,
each with remaining vocabulary `R minus {q}`. Pure children require no further
acquisition and are omitted from this family.

Define a recursive structural type:

```text
Type(s) = terminal                         if s is resolved
Type(s) = { (cost(q), {Type(u): u in M(s,q)}) : q productive at s }
                                              otherwise.
```

The empty set at an unresolved state is a dead-end type, NOT `terminal`.
Both sets are ordinary sets, not multisets. Duplicate child types do not change
an adversarial maximum; duplicate action types do not change a minimum. These
choices are specific to this deterministic worst-path objective.

All recursion is well founded because every transition removes a query.
`build_continuation_quotient()` interns these descriptors into one class table
for a batch of tasks. Class IDs are local to that certificate; they are not
persistent canonical IDs or cross-run hashes.

## 2. Adaptive-cost preservation theorem

Let `V(s)` be minimum guaranteed-resolution worst-path cost, using infinity for
unresolvable states. If `Type(s)=Type(t)`, then

\[
V(s)=V(t).
\]

**Proof.** Resolved states have value zero. An unresolved type with no actions
has value infinity. For each other type, use the Bellman equation

\[
V(s)=\min_q\left[c(q)+\max\left(\{V(u):u\in M(s,q)\}\cup\{0\}\right)\right].
\]

By induction on the finite continuation height, equal child types have equal
values. The set of `(cost, child-type set)` pairs is identical at equal parent
types; therefore its minimum of maxima is identical. Removing multiplicities
changes neither operation. No numeric optimum is used to define the types. QED.

The converse is false. A direct query of cost 2 and two sequential unit-cost XOR
queries both have optimum 2, but have different recursive types. This module
therefore does not claim the coarsest possible value-preserving quotient, or a
solution to arbitrary dynamic dominance between incomparable action families.

## 3. Lifting a class policy back to named experiments

`lift_continuation_policy()` finds original available queries whose cost and
child-class structure realize an optimal class action. It then follows the actual
outcome cells in that original task. At a pure leaf it recovers the actual target
from the original surviving worlds.

Thus shared future value does not authorize copying a representative's literal
query name or target label to another state. A `left` assay and a `right` assay
can realize the same one-more-measurement class without being the same assay.
Resolved `red` and resolved `None` states have equal remaining acquisition cost
zero; their reportable target values still differ.

## 4. Exact boundary: equal continuation type, different fixed cost

Use four worlds with `T=(0,0,1,1)` and three unit-cost binary queries.

| Query | Strict task | Bypass task |
|---|---|---|
| left | `(0,0,0,1)` | `(0,0,0,1)` |
| right / bypass | `(0,1,0,0)` | `(0,1,0,1)` |
| route | `(0,1,1,0)` | `(0,1,1,0)` |

Both tasks have the same recursive root descriptor. Omitting the terminal
marker, their shared class graph has only three classes:

```text
U = {(1,{})}                value 1
D = {(1,{U})}               value 2
K = {(1,{U}), (1,{D})}      value 2   <- both roots
```

The strict task's route chooses left on outcome 0 and right on outcome 1.
Its fixed comparator needs all three queries, with direct necessity witnesses:

```text
world pair (0,3): separated only by left
world pair (1,2): separated only by right
world pair (0,2): separated only by route
```

Hence `C_A=2` and `C_F=3`, without using exhaustive fixed optimization for this
lower bound. In the bypass task, `(bypass,route)` is a fixed resolver of cost 2;
no single query resolves the target. Hence `C_A=C_F=2`.

Why the difference disappears under the quotient: the strict task has two named
actions of the `(1,{D})` type, while the bypass task has two named actions of the
`(1,{U})` type. Action multiplicity and global reuse of physical query identities
matter for a bundle, but not for the local Bellman minimum.

The executable witness is `continuation_fixed_cost_collision()`. Across these
two tasks, 16 reachable mixed states become 3 nonterminal continuation classes.
The local policies are replay-tested with their original outcomes and names.

## 5. Verification contract

`verify_continuation_quotient()` independently reconstructs outcome cells using
an equality-based partition routine rather than the builder's partition helper.
It checks every productive action, every supported mixed child, each child
membership, exact acquisition costs, topological class references, descriptor
uniqueness, root identities, and state reachability. No adaptive/fixed optimizer,
canonicalizer, or hash-table verdict is used as a proof oracle.

Missing actions are rejected even if the omitted action would not change the
current scalar optimum. Missing states, fake terminal claims, wrong costs,
self-referential class edges, duplicate memberships and incomplete certificates
are also rejected. The state cap raises `ContinuationQuotientLimitError`; it does
not return an apparently complete partial equivalence.

This verifier certifies the stated finite structural quotient, not the truth of
the scientific observation model or the exhaustive coverage of nature by the
represented worlds.

## 6. Exhaustive and seeded regression

The checked-in result is `validation/continuation_bisimulation.json`.
The original direct Bellman implementation is byte-verified against baseline
blob SHA `93e91ef08097e91cb9003823601bc5d706452ba7` in the local audit snapshot.
It is a separate solver from the new structural builder.

| Declared universe (3 queries) | Tasks | Reachable mixed states | Nonterminal classes | Adaptive-cost mismatches |
|---|---:|---:|---:|---:|
| 4 worlds, 2+2 targets, labelled binary maps | 4,096 | 20,992 | 12 | 0 |
| 5 worlds, 2+3 targets, labelled binary maps | 32,768 | 238,880 | 43 | 0 |
| 4 worlds, 2+2 targets, all deterministic partitions | 3,375 | 13,275 | 16 | 0 |
| 4 worlds, 2+1+1 targets, all deterministic partitions | 3,375 | 15,075 | 17 | 0 |

Total: **43,614 declared finite tasks**, including unresolved tasks. The
multiway scopes use the 15 restricted-growth representatives of all partitions
of four worlds; their counts must not be compared as prevalence estimates with
labelled binary-map counts. Counts of states sum over task-indexed residual
states; classes share structural types across the entire batch. They are not
state counts for one biological dataset or one unusually large task.

There are also 250 seeded weighted/multiway/multitarget tasks, each compared with
a world/query/outcome relabelling, with optimal policy replay. Unit tests include
input validation, exact cost recalibration rejection, structural tampering, and
proof that builder/verifier do not invoke optimum oracles.

These are semantic compression counts, NOT an end-to-end runtime speedup. The
current constructor still visits the full reachable mixed-state graph. The
remaining query-count bound is inherited from `FiniteTask` (at most 20).

## 7. What remains open

The larger representation question is now two-sided:

```text
fixed-only obligation kernel:     preserve C_F; can lose adaptive geometry
adaptive continuation quotient:   preserve C_A; can lose fixed query reuse
full identity-indexed incidence:  retain the information needed by both
```

Useful next targets are a smaller JOINT sufficient representation that retains
cross-branch query identity, on-demand discovery of continuation equivalence
without constructing the full graph, and simulations that certify dominance
between unequal recursive types. Arbitrary cost recalibration, expected cost,
probability-weighted information, and continuous uncertainty require separate
contracts. No biological empirical claim is made here.

## 8. Relation to established state abstraction

Bisimulation and value-preserving state aggregation are established methods,
not inventions of this repository. Dean and Givan (1997), *Model Minimization in
Markov Decision Processes*, develops model minimization by stochastic
bisimulation; Givan, Dean and Greig (2003), *Equivalence notions and model
minimization in Markov decision processes*, develops related equivalence and
aggregation theory. This implementation uses a finite deterministic minimax
AND/OR continuation structure, not their stochastic transition criterion.
The repository-specific additions are its target-mixed, cost-labelled contract,
independent certificate and policy lifting, exhaustive audit, and the explicit
fixed-comparator counterexample.

Primary sources:
- https://s.aaai.org/Library/AAAI/1997/aaai97-017.php
- https://doi.org/10.1016/S0004-3702(02)00376-4

## Reproduce

```bash
python -m pip install -e . pytest
python -m pytest tests/test_continuation_bisimulation.py -q
PYTHONPATH=. python examples/audit_continuation_bisimulation.py --exhaustive \
  --output validation/continuation_bisimulation.json
```
