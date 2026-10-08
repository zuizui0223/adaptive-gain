# A finite sensitivity envelope from bounds on hidden common shocks

## Why this matters

The exact causal gauge shows that a trait-only moving-optimum OU likelihood cannot distinguish a one-way adaptive-tracking model from reciprocal latent feedback if shared process innovations are allowed. The no-common-shock assumption \(Q_{12}=0\) collapses the ambiguity, but treating that binary assumption as the only option would make the result less useful empirically.

A weaker external bound on common shocks already yields a finite identified set for the mechanistic adaptation half-life.

## Exact bound

In the reciprocal congruence family,

\[
a=q\alpha,\qquad d=(1-q)\alpha,\qquad 0<q\le1,
\]

and the transformed innovation covariance is

\[
Q_{12}=-\frac{d}{a}v_x
=-\frac{1-q}{q}v_x,
\]

where \(v_x>0\) is the observed-trait process variance in the source OUBM representation.

Suppose independent biological information supports

\[
|Q_{12}|\le C,
\qquad C\ge0.
\]

Then

\[
\frac{1-q}{q}v_x\le C
\]

implies

\[
\boxed{
q\ge\frac{v_x}{v_x+C}.
}
\]

Since

\[
H_{\rm direct}=\frac{H_{\rm OU}}q,
\]

we obtain

\[
\boxed{
H_{\rm OU}
\le H_{\rm direct}
\le H_{\rm OU}\left(1+\frac{C}{v_x}\right).
}
\]

This envelope is exact for the declared reciprocal gauge.

## Assumption-sensitivity interpretation

Write

\[
c=\frac{C}{v_x}.
\]

Then the entire sensitivity analysis is the dimensionless rule

\[
\boxed{
\frac{H_{\rm direct}^{\max}}{H_{\rm OU}}=1+c.
}
\]

Examples:

- \(c=0\): no common shock; the usual one-way half-life is recovered exactly;
- \(c=0.5\): direct half-life can be up to 1.5 times the reported OU half-life;
- \(c=1\): up to 2 times;
- \(c=9\): up to 10 times;
- no finite bound on \(C\): no finite upper bound on direct half-life.

For a reported 12-year OUBM half-life, the same scale becomes 12 years at \(c=0\), at most 24 years at \(c=1\), at most 120 years at \(c=9\), and unbounded if latent common shocks are left unconstrained.

## Methodological replacement

This suggests a constructive reporting standard rather than a blanket prohibition on mechanistic OU interpretation:

1. report the conventional model-conditional half-life \(H_{\rm OU}\);
2. state the assumed restriction on hidden innovation covariance;
3. when possible, justify an external bound \(C\) from environmental measurements, replicate series, experimental perturbations, or domain knowledge;
4. report the resulting mechanistic half-life interval instead of silently equating \(H_{\rm OU}\) with a uniquely identified adaptation speed.

The result turns a structural-identifiability objection into an assumption-sensitivity analysis with an explicit biological scale.

## Claim boundary

The bound applies to the exact two-state reciprocal gauge constructed for the evoTS moving-optimum OU observation law. It should not be advertised as a universal bound for arbitrary nonlinear, higher-dimensional, or phylogenetic OU systems without a separate proof.
