# Productive-frontier form of the adaptive/fixed decomposition

The fixed comparator no longer needs world-pair identities or child wiring.  Let

\[
\mathcal H=\{P_s:s\text{ is a reachable mixed state}\}
\]

be the productive-query hypergraph, reduced to its inclusion-minimal edges.  A
fixed bundle resolves exactly when it hits every edge, so with query-cost function
`c`,

\[
\boxed{C_F=\tau_c(\mathcal H)}
\]

where `tau_c` is minimum weighted hitting-set cost.

Now take one selected optimal adaptive policy and let `S` be the set of distinct
query resources appearing anywhere in that tree.  Its flattened union is a fixed
resolver.  Define

\[
C_U=\tau_c(\mathcal H; B\subseteq S),
\]

the cheapest hitting set constrained to resources used somewhere by that selected
adaptive tree.

Then

\[
C_A\le C_F\le C_U\le c(S)
\]

and the existing three-way identity becomes

\[
\boxed{
c(S)-C_A
=
[\tau_c(\mathcal H)-C_A]
+
[\tau_c(\mathcal H;S)-\tau_c(\mathcal H)]
+
[c(S)-\tau_c(\mathcal H;S)].
}
\]

Interpretation:

- `c(S)-C_A`: branch-exclusive overhead;
- `tau_c(H)-C_A`: realized adaptive gain;
- `tau_c(H;S)-tau_c(H)`: external shortcut discount;
- `c(S)-tau_c(H;S)`: internal union redundancy.

So the gain/bypass decomposition itself is a statement about one adaptive policy
union plus one fixed-side productive-frontier hypergraph.  Cross-target pair
identities, fixed-side state histories, and child wiring are not needed once
`H` is known.

## Executable audit

`adaptive_gain/frontier_decomposition.py` recomputes all four quantities from the
productive frontier and compares them against the original direct decomposition.
Regression coverage includes:

- the partial internal-bypass strict-gain control;
- the partial external-bypass strict-gain control;
- the complete-bypass no-gain control; and
- all `16^3 = 4096` balanced four-world / three-binary-query labeled tasks.

The comparison is exact: disagreement raises instead of silently returning two
competing decompositions.

## Scope boundary

This theorem concerns the finite deterministic guaranteed-resolution cost layer.
It does not imply that the productive frontier preserves adaptive policy labels,
child outcome semantics, stochastic information values, calibration dynamics, or
scientific report licensing.  It is sufficient for the fixed hitting-set terms in
the cost decomposition, not for reconstructing the adaptive tree itself.
