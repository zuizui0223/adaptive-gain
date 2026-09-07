# Global resource-transition isomorphism

The exact joint-sufficient representation `resource_continuation.py` keeps every
physical query token. This note identifies one safe quotient of those names.

## 1. Allowed quotient

Let two finite deterministic tasks have the same number of physical query
resources. A **global resource-transition isomorphism** is one cost-preserving
bijection

\[
\phi:Q_L\to Q_R
\]

used consistently at every reachable mixed state.

After replacing every left resource token `q` by `phi(q)`, the recursively defined
resource-labelled continuation roots must be identical:

```text
resource token
  -> cost
  -> set of mixed child resource-transition classes
```

The same `phi` is used in every branch. It is not chosen separately after each
outcome.

## 2. Joint-cost preservation

Because the mapping is global, any adaptive policy in the left task transports to
an adaptive policy of the same path cost in the right task. More importantly, one
fixed bundle

\[
B\subseteq Q_L
\]

transports to the single fixed bundle

\[
\phi(B)\subseteq Q_R
\]

with identical total cost and branchwise resolving behavior.

Therefore

\[
\boxed{
L\cong_{resource-transition}R
\Longrightarrow
C_A(L)=C_A(R),\quad C_F(L)=C_F(R).
}
\]

This is stronger than cost-only continuation equivalence and weaker than requiring
literal query names to match.

## 3. Exact small-state canonicalization

`canonical_resource_transition_signature()` enumerates only cost-preserving global
query permutations, transforms the already verified resource-continuation
certificate, and chooses one canonical recursive root representation.

A hard permutation cap raises
`ResourceTransitionIsomorphismLimitError`; exceeding the cap is not interpreted as
non-isomorphism.

When two canonical signatures match,
`resource_transition_isomorphism_witness()` returns an explicit left-to-right
query bijection.

`verify_resource_transition_isomorphism()` does not trust the canonical hash. It
rebuilds and independently verifies both resource-continuation certificates, then
checks the proposed global resource mapping directly on their recursive roots.

## 4. Relation to weaker overlap summaries

The current hierarchy is now

```text
resource-orbit capacity
    insufficient: explicit C_F=3 vs 2 collision

per-resource abstract role profiles
    insufficient: explicit four-query C_F=3 vs 2 collision

state-resource co-location
    repairs the complete first four-world/four-query ambiguity
    but no general sufficiency theorem yet

global resource-labelled transition isomorphism
    exact joint-safe quotient

literal resource-labelled transition system
    exact joint-sufficient representation
```

The important distinction is global consistency. A resource may play analogous
roles in several states, but a fixed bundle cares whether those roles are
implemented by the **same physical token under one global identification**.

## 5. Scope

This theorem is only for the repository's finite deterministic positive-cost
worst-path resolution model. It does not establish a quotient for noisy likelihoods,
probabilistic information utility, continuous parameter regions, calibration-
changing actions, or biological report licensing.

The next compression question is whether the global bijection can itself be
represented more compactly by a certified state-resource-action hypergraph,
stabilizer chain, or capacity-labelled orbit structure without reintroducing the
fixed-reuse collisions documented in `RESOURCE_OVERLAP_HIERARCHY.md`.
