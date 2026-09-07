# Static generation of the minimal productive frontier

The fixed scalar-cost statistic can be built without reachable-state enumeration.

## 1. Pair-incidence route

For every pair of represented worlds with different target labels, let

\[
S_{ij}=\{q:q(i)\ne q(j)\}
\]

be the set of queries separating that pair.

The productive-frontier equivalence theorem already gives

\[
\boxed{
\min_{\subseteq}\{P_s:s\text{ reachable mixed}\}
=
\min_{\subseteq}\{S_{ij}:T_i\ne T_j\}.
}
\]

Therefore the minimal productive frontier may be generated directly from the
static world/query table:

```text
full task table
-> cross-target pair incidence
-> separator mask for each cross-target pair
-> inclusion minimization
-> minimal productive frontier
```

No Bellman state, reachable mixed state, consumed-query history, or child wiring
is needed on the fixed side.

## 2. Fixed optimum

For a minimal-frontier certificate `H_min`, a bundle `B` resolves exactly when

\[
B\cap H\ne\varnothing
\qquad\forall H\in\mathcal H_{\min}.
\]

Hence

\[
\boxed{C_F=\tau_c(\mathcal H_{\min})}.
\]

The implementation in `adaptive_gain/minimal_productive_frontier.py` stores only

- query names;
- query costs; and
- inclusion-minimal separator/productive masks.

It deliberately does **not** store all reachable productive sets, because those
are unnecessary for scalar fixed resolution once the equivalence theorem is
known.

## 3. Independent verification

`verify_minimal_productive_frontier_from_pair_incidence()` rebuilds the certificate
from target-pair incidence.  It does not call the reachable-state frontier
builder.

This keeps two independent construction routes available:

```text
state route:
  reachable mixed states -> productive sets -> inclusion minimum

static route:
  cross-target pairs -> separator sets -> inclusion minimum
```

Their equality is a theorem; agreement in regression tests is an implementation
audit rather than the source of the theorem.

## 4. Edge cases

- If the target is already identified at the root, there are no cross-target
  pairs and the minimal frontier is empty, so `C_F=0`.
- If some cross-target pair has no declared separator, the minimal frontier
  contains the empty edge.  No bundle can hit it, so `C_F=None` under the
  repository's unresolved convention.

## 5. Validation

The static and state-based minimal frontiers are compared on all

\[
16^3=4096
\]

balanced four-world / three-binary-query labeled tasks.  The tests also cover
resolved, unresolved, and tampered-certificate cases.

## 6. What remains open

Direct generation itself is closed.  The remaining algorithmic questions are
about efficiency rather than sufficiency:

- output-sensitive generation of minimal separator sets without materializing
  all cross-target pair rows;
- incremental updates when queries/worlds are added or removed;
- symmetry-aware static generation with independently checkable certificates;
- parameterized complexity in frontier size, rank, or transversal number.

## Scope

This result is limited to finite deterministic guaranteed target resolution.  It
is not a statement about noisy observations, expected information, calibration
changes, continuous compatible sets, or scientific report licensing.
