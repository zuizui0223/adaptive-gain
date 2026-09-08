# Review summary: temporal evolutionary information routing

This branch reframes the deterministic fixed-versus-adaptive measurement theory as a candidate theory of contingent cue acquisition by organisms and closes the first exact dynamic result.

## Exact result

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

With an extra routing-control cost `k` and fitness value `s` per unit target accuracy,

\[
\Delta W=\frac{s}{4}|2\rho-1|-k,
\]

so contingent sensing is favoured iff

\[
|2\rho-1|>4k/s.
\]

## Added evidence

- exact enumeration implementation: `adaptive_gain/temporal_routing.py`
- focused regression: `tests/test_temporal_routing.py`
- theorem note: `theory/TEMPORAL_ROUTING_THRESHOLD.md`
- scientific receipt: `validation/temporal_routing_threshold_v1.json`
- prior-art boundary: `theory/PRIOR_ART_EVOLUTIONARY_ROUTING.md`
- evolutionary/natural-history framing: `theory/EVOLUTIONARY_INFORMATION_ROUTING.md`

The focused temporal regression passed 18/18 tests in an independent local reconstruction. The full repository suite has not been rerun in that reconstruction environment; repository CI should provide the branch-wide check.
