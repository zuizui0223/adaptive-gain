# Minimal-transversal characterization of internal and external bypass

This note refines the productive-frontier scalar decomposition into an exact
structural statement about inclusion-minimal hitting sets.

Let `H` be the inclusion-minimal productive frontier on the physical query
vocabulary `Q`, with positive query costs `c`.  Let `Tr(H)` denote the family of
inclusion-minimal transversals (minimal hitting sets) of `H`.

For one selected optimal adaptive policy, let `S subseteq Q` be the union of all
query identities used anywhere in that policy tree and let `c(S)=U`.

## Fixed optima from minimal transversals

Every hitting set contains an inclusion-minimal hitting subset.  Because all
query costs are positive, removing a resource strictly lowers cost.  Therefore

\[
\boxed{
C_F = \min_{T\in\operatorname{Tr}(H)} c(T).
}
\]

The same argument restricted to the selected policy union gives

\[
\boxed{
C_U = \min_{\substack{T\in\operatorname{Tr}(H)\\T\subseteq S}} c(T).
}
\]

The selected policy union itself hits every productive-frontier edge because
flattening an adaptive resolving policy is a valid fixed resolving bundle.

## Exact three-way decomposition

Hence

\[
\boxed{
U-C_A
=
(C_F-C_A)
+
(C_U-C_F)
+
(U-C_U).
}
\]

The three nonnegative terms retain their previous meanings:

- `C_F-C_A`: realized adaptive gain;
- `C_U-C_F`: external shortcut discount;
- `U-C_U`: internal union redundancy.

No cross-target pair identity or fixed-side child wiring is needed once the
productive frontier is known.

## Internal redundancy: exact private-edge criterion

Because `S` is already a hitting set and costs are positive,

\[
U-C_U=0
\iff
S\in\operatorname{Tr}(H).
\]

A hitting set is inclusion-minimal iff every one of its resources has a private
edge relative to that set.  Therefore

\[
\boxed{
U-C_U=0
\iff
\forall q\in S\;\exists E\in H:\ E\cap S=\{q\}.
}
\]

Thus the frontier-private-edge test is not merely sufficient: it is necessary
and sufficient for zero internal redundancy of the selected policy union.

## External shortcut: exact outside-transversal criterion

By the restricted-transversal formula,

\[
C_U-C_F>0
\]

iff there exists a minimal transversal using at least one query outside `S` whose
cost is strictly below every transversal contained in `S`.  Equivalently,

\[
\boxed{
C_U-C_F>0
\iff
\exists T\in\operatorname{Tr}(H):
T\not\subseteq S,
\quad c(T)<C_U.
}
\]

Such a `T` is an explicit external-shortcut witness.

## Executable certificate

`adaptive_gain/frontier_transversals.py` performs exact small-state transversal
enumeration behind a hard subset cap.  It returns:

- all inclusion-minimal frontier transversals;
- globally cheapest transversals;
- cheapest transversals contained in the selected adaptive union;
- the internal private-edge certificate; and
- explicit cheaper outside-transversal witnesses when external discount is
  positive.

The verifier re-enumerates the bounded subset family rather than trusting a
stored hash or generator claim.

The complete balanced four-world / three-binary-query universe (`4096` tasks) is
checked against the existing productive-frontier scalar decomposition, and the
registered internal/external/partial bypass controls are checked separately.

## Claim boundary

The theorem concerns the repository's finite deterministic guaranteed-target-
resolution setting with positive query costs.  Exact transversal enumeration is
not claimed scalable.  The structural equivalences do not extend automatically
to noisy likelihoods, expected utility, calibration-changing actions, or report
licensing.
