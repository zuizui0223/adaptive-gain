# Local routing-mutation accessibility inside a fixed sensing task

Status: side theory. This note is **not** part of the frozen Theoretical Ecology submission. It develops a direct small-jump analogue inside adaptive-gain's own heritable sensory-policy space without borrowing PAYOFF topology semantics.

## 1. Why this bridge is cleaner than forcing PAYOFF topology into sensing

The current source audit found no licensed map from PAYOFF's developmental/genetic/structural coupling edges to organismal cues or routing rules. Writing `one released edge = one cue` would therefore be post hoc.

adaptive-gain itself already contains a heritable contingent sensory architecture in the endogenous eco-evolutionary model. The finite sensing task can therefore be held fixed while only the **policy wiring** changes locally.

This gives a direct version of the earlier small-jump question:

> A structurally efficient contingent policy exists. Can a heritable routing architecture reach it through small local wiring changes, and how many changes are required before worst-case sensing cost improves?

The result below answers that question exactly for the repository's `k`-branch extremal routing family under one deliberately narrow mutation syntax.

## 2. Fixed ecological task

Fix `k>=2` and use `extremal_routing_task(k)`.

The task has

```text
2k represented worlds,
1 k-ary router,
k binary branch-terminal queries.
```

Its exact optima are

```text
C_A=2,
C_F=k+1,
g*=C_F-C_A=k-1.
```

After the router identifies branch `i`, only the pair `(a_i,b_i)` remains. Terminal `q_i` separates that pair. Every other terminal `q_j`, `j!=i`, is constant on `(a_i,b_i)` and is therefore target-irrelevant inside branch `i`.

The ecological worlds and cue vocabulary are fixed throughout this note. Only the branch-conditioned acquisition program evolves.

## 3. Heritable routing architecture state

Represent one routing architecture by branch program lengths

```text
ell=(ell_1,...,ell_k),
1<=ell_i<=k.
```

In branch `i`:

- the required separator `q_i` is retained as the final acquisition;
- `ell_i-1` other terminal occurrences are acquired before it;
- those earlier terminals are target-irrelevant within the already identified branch.

The full zero-saving routing program is

```text
ell_full=(k,...,k).
```

It uses the router and then all `k` terminals on every realized branch, so its worst-path acquisition cost is `k+1`, equal to the fixed optimum.

The fully pruned contingent optimum is

```text
ell_opt=(1,...,1),
```

which measures only the branch-specific separator after the router and has worst-path cost 2.

For any state `ell`,

```text
C(ell)=1+max_i ell_i,
```

and define its **realized structural gain** relative to the fixed task cost by

```text
g(ell)=C_F-C(ell)=k-max_i ell_i.
```

Thus

```text
0<=g(ell)<=k-1=g*.
```

This policy-specific `g(ell)` is an extension of the submitted task-level gap. The frozen manuscript uses the optimal task gap `g*=C_F-C_A`; it does not contain this mutation model.

## 4. Declared small routing mutation

One local mutation removes exactly one target-irrelevant terminal occurrence from exactly one branch:

```text
ell_i -> ell_i-1
```

when `ell_i>1`.

The required separator `q_i` is never removed, so every allowed mutant remains target-resolving. The mutation does not:

- invent a new sensor;
- change the ecological world set;
- change query outcomes;
- relabel queries;
- reorder the required separator;
- rewire several branches simultaneously.

This is therefore a deletion-only local wiring model, not a universal mutation model for decision trees.

## Theorem LRM1 — exact local-mutation distance to realized structural gain

Let `r` be an integer with

```text
0<=r<=k-1.
```

Starting from

```text
ell_full=(k,...,k),
```

the minimum number of allowed local pruning mutations required to reach any architecture with

```text
g(ell)>=r
```

is exactly

```text
boxed:  k r.
```

### Proof

The condition

```text
g(ell)>=r
```

is equivalent to

```text
max_i ell_i<=k-r.
```

Hence every one of the `k` branches must be shortened from length `k` to at most `k-r`. Each branch therefore requires at least `r` local deletions. Because one mutation changes only one branch, every valid path needs at least `k r` mutations.

The bound is attained by pruning exactly `r` irrelevant occurrences from each branch. The resulting state has

```text
ell_i=k-r
```

for every `i`, so

```text
g(ell)=r.
```

QED.

## Corollary LRM1.1 — a mandatory neutral prefix before the first worst-case gain

For `r=1`, Theorem LRM1 gives a minimum of `k` local mutations.

After at most `k-1` deletions, at least one branch is still unedited and retains length `k`. Therefore

```text
max_i ell_i=k
```

and

```text
g(ell)=0.
```

So the first `k-1` local routing edits are necessarily neutral with respect to the worst-path structural reward. A large adaptive opportunity can therefore exist in the task while no one-step or short-prefix fitness gradient exposes that opportunity under this mutation syntax.

This is a combinatorial plateau result, not a claim that real sensory evolution is neutral for exactly `k-1` mutations.

## Corollary LRM1.2 — full adaptive optimum requires `k(k-1)` local prunings

The task optimum has

```text
g*=k-1.
```

Substituting `r=k-1` into LRM1 gives

```text
minimum local mutations = k(k-1).
```

Thus the static statement

```text
an adaptive policy of cost 2 exists
```

and the evolutionary-accessibility statement

```text
that policy can be reached quickly by local routing edits
```

are different.

## 5. Canonical q=2 connection to the submitted reachability theorem

For the generalized local dynamical example used in the manuscript, the first stable oscillatory structural requirement is

```text
q=2.
```

At maximum cue arity `b=3`, the exact structural Pareto theorem contains

```text
(worlds,queries,frontier_edges,depth)
=(6,4,4,2).
```

The `k=3` extremal star-routing task attains exactly those coordinates:

```text
2k=6 worlds,
k+1=4 queries,
C_A=2,
C_F=4,
g*=2.
```

So static structural reachability says that this fixed sensing task is sufficient for the required gap.

The local mutation result then adds a different statement. Starting from the zero-saving full branch program

```text
ell=(3,3,3),
```

reaching realized gain 2 requires

```text
3*2=6
```

single-branch pruning mutations.

Moreover:

```text
minimum edits to gain 1 = 3,
minimum edits to gain 2 = 6.
```

Thus the exact minimum task can already exist while the efficient heritable routing program remains several local wiring changes away.

## 6. Relation to small-jump, HK, and mesoscopic ideas

This result creates a direct bridge to the **small-jump accessibility** idea without claiming that it is adaptive-dynamics novelty.

The analogy is now exact at the level of logical structure:

```text
static adaptive optimum exists
!=
locally efficient routing architecture is immediately reachable.
```

Hegselmann-Krause/bounded interaction and PAYOFF's mesoscopic distribution layer remain separate population-level mechanisms. They are not needed for LRM1.

A future population model could place mutation, drift, and selection on this finite routing-architecture graph. That would be a new extension and would need its own claim audit.

## 7. Optional downstream feedback composition

If a future model declares that the eco-evolutionary feedback lift depends on **realized policy gain**

```text
G(ell)=a Delta g(ell)
```

rather than directly on the task optimum `g*`, then a local dynamical regime requiring integer gain `q` inherits the mutation-distance condition

```text
minimum local pruning mutations >= k q
```

whenever `q<=k-1`.

If

```text
q>k-1,
```

then the fixed task itself is structurally incapable of supporting the required regime, independently of mutation accessibility.

This gives a two-stage gate inside one state space:

```text
q<=g* ?
    no  -> structural task exclusion
    yes -> local policy accessibility requires at least k q deletions from ell_full.
```

This composition is **not** part of the frozen manuscript. The current submitted theorem uses the optimal structural gap and does not model local mutation among policy trees.

## 8. Novelty boundary

Do not claim novelty for:

- small-step mutation as an evolutionary idea;
- local search on decision trees;
- neutral plateaus in combinatorial landscapes;
- edit distance between policies;
- generic existence-versus-accessibility distinctions.

The side result that is exact here is narrower:

> In the declared `k`-branch sensing family, under one-branch-at-a-time pruning of target-irrelevant acquisitions, the shortest path from a zero-saving routing program to realized structural gain `r` is exactly `k r`, while the first `k-1` local edits cannot improve worst-case sensing cost.

Whether that exact composition is publishably novel requires a dedicated prior-art search in evolutionary computation, decision-tree pruning, and genotype-to-policy mutation models before any companion-paper claim.

## 9. Executable audit

Implementation:

```text
adaptive_gain/local_routing_mutation.py
```

Tests:

```text
tests/test_local_routing_mutation.py
```

The test suite independently checks the `k r` formula by exhaustive BFS for small `k`, verifies the mandatory neutral prefix, and confirms that the canonical `q=2,k=3` witness lies on the exact arity-3 Pareto frontier.
