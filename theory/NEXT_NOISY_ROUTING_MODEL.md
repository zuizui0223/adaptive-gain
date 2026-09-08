# Noisy temporal routing: first symmetric case closed

The symmetric binary-noise extension that was staged here is now closed exactly.

Let

\[
P(C_1=C_0)=\rho,
\qquad
P(R=C_0)=a,
\qquad
P(Y_q=q(T,C_1))=b,
\]

with `a,b in [1/2,1]`, where the route signal and specialist observations pass through independent binary symmetric channels.

Then every two-query fixed pair has

\[
\boxed{
A_F^{(2)}
=
\frac12+\frac{2b-1}{4},
}
\]

and the optimal contingent policy has exact gain

\[
\boxed{
G_{noisy}
=
\frac{|2\rho-1|(2a-1)(2b-1)}{4}.
}
\]

Thus the previously conjectured product structure is exact in this symmetric construction.

See:

```text
theory/NOISY_TEMPORAL_ROUTING_FACTORIZATION.md
adaptive_gain/noisy_temporal_routing.py
tests/test_noisy_temporal_routing.py
```

## What is now genuinely next

The next unresolved layer is no longer `does noise destroy the temporal theorem?` It is the boundary of the factorization under more realistic observation laws.

Priority questions:

1. asymmetric false-positive / false-negative rates;
2. unequal reliabilities for the two specialist channels;
3. correlated routing and specialist errors;
4. nonuniform target and context priors;
5. more than one context transition before action;
6. moving fitness-relevant target `T_t` rather than fixed `T`;
7. explicit sensing-time costs and mortality / missed-opportunity risk;
8. heritable investment trade-offs in `a`, `b`, memory, and switching machinery.

The most biologically useful next theorem would identify which of these perturbations preserve a multiplicative or monotone complementarity among temporal predictability, early-cue quality, and downstream-cue quality.
