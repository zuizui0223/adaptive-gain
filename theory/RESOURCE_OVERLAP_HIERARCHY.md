# Resource-overlap hierarchy for joint adaptive/fixed resolution

This note separates four different kinds of information that can be retained when
compressing a finite deterministic measurement problem.

The scientific model is still the same finite guaranteed-resolution contract:

- hidden worlds are finite;
- every world has a declared target label;
- every query has positive acquisition cost;
- query outcomes are deterministic in represented worlds;
- `C_A` is the minimum adaptive worst-path acquisition cost;
- `C_F` is the minimum cost of one fixed resolving query bundle.

No claim here concerns noisy measurements, natural-data prevalence, or report
licensing.

## 1. Orbit capacity is not enough

Start from the cost-only continuation quotient, which preserves `C_A` but forgets
physical query identity. A tempting repair is to add the sizes/costs of the exact
full-task query orbits.

The registered five-world pair in `orbit_capacity_collision()` defeats that idea.
Both tasks have

```text
targets = (0,0,1,1,1)
three binary unit-cost queries
same cost-only continuation root type
same exact query-orbit capacity profile
```

but their exact costs are

\[
(C_A,C_F)=(2,3)
\]

and

\[
(C_A,C_F)=(2,2).
\]

Thus

\[
\boxed{
\text{continuation type + resource-orbit capacities}
\not\Rightarrow C_F.
}
\]

The missing information is not how many resources exist in an orbit, but how the
same physical resource participates in local continuation roles across different
reachable states.

## 2. First-order per-resource role profiles are still not enough

For each physical query `q`, define its abstract role profile as the set of pairs

\[
(\text{parent continuation type},\;\text{local action type})
\]

that `q` realizes anywhere in the reachable mixed-state graph.

This remembers cross-state reuse of a resource more strongly than orbit capacity:
a query that serves several different continuation roles has all of them in one
profile.

However the four-world/four-query pair in
`resource_role_profile_collision()` has

```text
same cost-only continuation root type
same multiset of complete per-resource role profiles
```

while

\[
(C_A,C_F)=(2,2)
\]

for the bypass task and

\[
(C_A,C_F)=(2,3)
\]

for the strict task.

The representatives are

```text
T = (0,0,1,1)

no-gain:
  left   = (0,0,0,1)
  right  = (0,1,0,0)
  bypass = (0,1,0,1)
  route  = (0,1,1,0)

strict:
  left    = (0,0,0,1)
  right   = (0,1,0,0)
  route_a = (0,1,1,0)
  route_b = (0,1,1,0)
```

So even

\[
\boxed{
\text{continuation type + multiset of per-resource role sets}
\not\Rightarrow C_F.
}
\]

What the projection loses is **co-location**: it knows what roles each resource can
play somewhere, but not which role occurrences coexist in the same concrete
reachable state.

## 3. Exact finite location of the first role-profile ambiguity

For balanced four-world binary unit-cost tasks, the compact exhaustive classifier
`enumerate_balanced_resource_role_overlap_universe()` gives:

### Three queries

\[
16^3=4096
\]

labeled tasks collapse to 25 resource-role signatures, with

\[
\boxed{0\text{ ambiguous signatures}.}
\]

### Four queries

\[
16^4=65536
\]

labeled tasks collapse to 60 resource-role signatures. Exactly one signature is
ambiguous in fixed cost. It contains

\[
1536\text{ tasks with }(C_A,C_F)=(2,2)
\]

and

\[
768\text{ tasks with }(C_A,C_F)=(2,3),
\]

for a total of

\[
\boxed{2304\text{ tasks}.}
\]

Thus, at fixed four-world balanced target structure, four binary resources are the
first registered query count where first-order resource-role profiles stop being
sufficient.

This is an exact finite classification, not a prevalence statement about real
experiments.

## 4. State-resource co-location is strictly stronger

The diagnostic `state_resource_colocation_signature` retains one row for every
reachable mixed state. A row records:

- the abstract continuation type of that state;
- which physical resources are still unavailable/available;
- whether each available resource is constant or productive there; and
- the resource's local action type.

Query columns are canonicalized only under cost-preserving permutation.

The registered four-query role-profile collision has different co-location
signatures, so the stronger representation repairs that particular information
loss.

But no general sufficiency theorem is claimed for co-location alone. It still
forgets which concrete child occurrence follows each action. Two tasks could in
principle share the same row/column incidence while wiring those rows differently.

Therefore

\[
\boxed{
\text{state-resource co-location distinguishes the witness}
\neq
\text{general joint sufficiency theorem}.
}
\]

## 5. Resource-labelled transition structure is sufficient

The existing `resource_continuation.py` keeps the missing transition information:

```text
physical query token
    -> declared cost
    -> mixed child continuation classes
```

while retaining the resource token globally across branches.

That representation has already been validated to preserve both exact costs.
Therefore the current hierarchy is

\[
\boxed{
\begin{array}{c}
\text{orbit capacity}\\
\downarrow\\
\text{per-resource role profile}\\
\downarrow\\
\text{state-resource co-location}\\
\downarrow\\
\text{resource-labelled transition structure}
\end{array}
}
\]

with explicit negative controls at the first two arrows and exact joint
sufficiency at the last layer.

## 6. Interpretation

The fixed comparator is sensitive to a genuinely global question:

> Can one physical measurement resource satisfy requirements that appear in
> different possible histories?

Neither local continuation value, resource count, nor the set of roles a resource
can play somewhere answers that question completely. What matters is the
**incidence of the same physical resource with concrete branch-state obligations**.

This makes the next research problem sharper:

\[
\boxed{
\text{How much of resource-labelled transition incidence can be quotiented while
preserving all fixed cross-branch reuse?}
}
\]

A promising next object is a state-resource-action hypergraph with explicit child
transport, followed by exact automorphism/capacity quotienting. The current note
does not claim that a first-order or pairwise overlap summary is sufficient.
