# Next extension: noisy temporal routing

The exact temporal theorem currently assumes a perfectly observed routing context and deterministic specialist queries conditional on context.

The next model should introduce

\[
P(R=C_0)=a>1/2
\]

for routing reliability and

\[
P(S_C=T\mid \text{specialist matches current context})=b>1/2
\]

for specialist reliability, while retaining an uninformative or branch-specific nuisance law for a mismatched specialist.

The first target is a closed-form analogue of

\[
G_{time}=|2\rho-1|/4
\]

that separates three effects:

```text
temporal predictability
x routing-cue reliability
x specialist-cue reliability
```

and then adds an explicit control cost.

A useful conjectural factorization to test is that, under a symmetric binary-noise construction preserving the minimal normal-form semantics, routing gain scales monotonically with

\[
|2\rho-1|(2a-1)(2b-1).
\]

This is a conjecture, not yet a repository theorem. The exact mismatched-specialist likelihood must be chosen so that the deterministic limit recovers the existing four-world strict-gain core rather than a different two-query problem.
