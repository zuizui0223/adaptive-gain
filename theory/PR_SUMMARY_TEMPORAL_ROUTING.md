# Review summary: temporal evolutionary information routing

This branch reframes the deterministic fixed-versus-adaptive measurement theory as a candidate theory of contingent cue acquisition by organisms and closes two exact dynamic layers.

## 1. Temporal routing with perfect cues

Starting from the unique four-world strict-gain normal form, represent worlds as `(T,C)` where `T` is the fitness-relevant target and `C` determines which specialist cue is diagnostic. Let

\[
P(C_1=C_0)=\rho.
\]

At a two-query budget, every fixed pair has Bayes accuracy

\[
A_F^{(2)}=3/4,
\]

while the optimal contingent policy has

\[
A_A^{(2)}=3/4+|2\rho-1|/4.
\]

Hence

\[
G_{time}=|2\rho-1|/4.
\]

The key ecological correction is that **temporal predictability, not persistence alone, creates routing value**. Positive autocorrelation favours same-branch continuation; negative autocorrelation favours branch reversal; temporal independence removes the gain exactly.

## 2. Symmetric noisy cues

Let the early route cue have reliability

\[
P(R=C_0)=a,
\]

and let each specialist bit pass through an independent binary symmetric channel of reliability `b`, with `a,b>=1/2`.

Then every fixed pair has

\[
A_F^{(2)}
=
1/2+(2b-1)/4,
\]

and the exact contingent gain factorizes as

\[
\boxed{
G_{noisy}
=
\frac{|2\rho-1|(2a-1)(2b-1)}{4}.
}
\]

Thus temporal predictability, usable routing information, and usable downstream specialist information form a multiplicative gate.

With fitness value `v` per unit accuracy and routing-control cost `k`,

\[
\Delta W
=
vG_{noisy}-k.
\]

The positive cross-partial between `a` and `b` gives a first within-episode mechanism for complementary selection on early and downstream sensory precision, conditional on temporal predictability.

## Added evidence

- exact temporal implementation: `adaptive_gain/temporal_routing.py`
- exact noisy implementation: `adaptive_gain/noisy_temporal_routing.py`
- focused regressions: `tests/test_temporal_routing.py`, `tests/test_noisy_temporal_routing.py`
- temporal theorem: `theory/TEMPORAL_ROUTING_THRESHOLD.md`
- noisy theorem: `theory/NOISY_TEMPORAL_ROUTING_FACTORIZATION.md`
- scientific receipts: `validation/temporal_routing_threshold_v1.json`, `validation/noisy_temporal_routing_factorization_v1.json`
- prior-art boundary: `theory/PRIOR_ART_EVOLUTIONARY_ROUTING.md`
- evolutionary/natural-history framing: `theory/EVOLUTIONARY_INFORMATION_ROUTING.md`

The perfect-cue temporal regression passed 18/18 focused tests in an independent local reconstruction. The noisy closed forms were independently checked by direct latent-state enumeration on 756 parameter triples (3,780 formula comparisons; maximum absolute error `2.22e-16`). A branch-wide local clone was blocked by DNS in the execution environment; repository CI is the intended full-suite check.
