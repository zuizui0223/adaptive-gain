# Exact co-location repair in the first resource-role ambiguous scope

This note records a **scope-specific exhaustive result**. It does not claim that
state-resource co-location is a generally sufficient representation.

## Scope

```text
4 hidden worlds
T = (0,0,1,1)
4 binary unit-cost queries
all 16^4 = 65,536 labeled query systems
```

For each task, first build the weaker signature

```text
cost-only continuation root class
+
multiset of complete per-resource abstract role profiles
```

where one resource profile records every

```text
(parent continuation class, local action type)
```

that the physical query realizes anywhere in the reachable mixed-state graph.

## First classification

Across all 65,536 tasks there are exactly 60 such resource-role signatures.
Exactly one signature is ambiguous in fixed cost. It contains

\[
1536\text{ tasks with }(C_A,C_F)=(2,2)
\]

and

\[
768\text{ tasks with }(C_A,C_F)=(2,3).
\]

Thus the ambiguous class contains

\[
\boxed{2304\text{ tasks}.}
\]

The executable representatives are provided by
`resource_role_profile_collision()`.

## State-resource co-location refinement

Now retain one row for every reachable mixed state. Each row records

- its continuation class;
- which physical resources are unavailable;
- which available resources are constant;
- which are productive; and
- the local child-class action type of every productive resource.

Columns are canonicalized under all cost-preserving query permutations.

Inside the 2,304-task ambiguous resource-role class, this stronger signature has
exactly two values:

```text
co-location class A -> all 1,536 tasks have (C_A,C_F)=(2,2)
co-location class B -> all   768 tasks have (C_A,C_F)=(2,3)
```

Therefore

\[
\boxed{
\text{co-location ambiguous signatures}=0
}
\]

inside the complete first resource-role ambiguous scope.

Equivalently, in this finite universe,

\[
\boxed{
\text{state-resource co-location repairs the entire first-order role-profile ambiguity.}
}
\]

This is checked by
`enumerate_balanced_four_query_colocation_repair()` and the corresponding CI
regression.

## What this does not establish

The result does **not** prove

\[
\text{state-resource co-location}\Longrightarrow(C_A,C_F)
\]

for arbitrary finite deterministic tasks.

Co-location still forgets explicit child-occurrence wiring. The generally verified
joint-sufficient layer remains the resource-labelled transition quotient in
`resource_continuation.py`.

A seeded search over larger five-world/four-query tasks found no co-location
counterexample, but that negative search is not used as a theorem or completeness
claim.

The next exact question is whether two tasks can share the complete co-location
matrix while differing only in how productive state-resource incidences are wired
to concrete child occurrences, and whether such rewiring can change `C_F`.
