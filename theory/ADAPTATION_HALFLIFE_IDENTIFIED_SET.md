# The OU adaptation half-life is not a mechanistically identified point under the causal gauge

## Result

In the one-way moving-optimum OU model used by evoTS, the fitted pull rate \(\alpha\) is interpreted as the rate at which the observed trait adapts toward the moving optimum. The corresponding adaptation half-life is

\[
H_{\rm OU}=\frac{\log 2}{\alpha}.
\]

The exact reciprocal observation-law congruence instead permits, for any \(0<q<1\),

\[
a=q\alpha,\qquad d=(1-q)\alpha,
\]

where \(a\) is the direct response of the observed trait to the latent state and \(d\) is the reciprocal response of the latent state to the observed trait. The complete observed trait law and hence the likelihood are unchanged after the corresponding hidden-state and innovation transformation.

If the latent state were experimentally held fixed, the direct trait relaxation half-life in that congruent realization would be

\[
\boxed{
H_{\rm direct}(q)
=\frac{\log 2}{a}
=\frac{H_{\rm OU}}{q}.
}
\]

Therefore

\[
\boxed{
H_{\rm direct}\in(H_{\rm OU},\infty)
}
\]

within the reciprocal family. Including the one-way boundary \(q=1\) gives the closed lower endpoint

\[
\boxed{
H_{\rm direct}\in[H_{\rm OU},\infty).
}
\]

Thus the conventional one-way OU fit supplies the **minimum** direct-response half-life inside this broader observation-equivalent class; it supplies no finite upper bound on the mechanistic response time unless the hidden causal/noise structure is constrained independently.

## Published fossil-series implication

Voje, Saito-Kato & Spanbauer (2024) report a point estimate of about **12 years** for the time required for the ancestral trait state of *Cyclostephanos andinus* to evolve halfway toward the continually moving optimum, and interpret the fitted dynamics as rapid trait adaptation to a rapidly and randomly moving optimum.

Under the exact congruent family, the same trait likelihood permits

\[
q=1/2\Rightarrow H_{\rm direct}=24\text{ years},
\]

\[
q=0.1\Rightarrow H_{\rm direct}=120\text{ years},
\]

\[
q=0.01\Rightarrow H_{\rm direct}=1200\text{ years},
\]

and arbitrarily larger direct-response half-lives as \(q\to0^+\).

This does **not** mean the published 12-year estimate is numerically wrong inside the declared one-way OUBM model. It means its interpretation as a uniquely data-supported *mechanistic rate of trait adaptation* is conditional on the one-way/no-common-shock model restrictions. The scalar fossil series identifies the apparent relaxation scale of the fitted observation model, not the decomposition of that scale into direct trait response versus reciprocal latent response.

## Why this is a better practice-level target

A generic statement that hidden OU parameters are non-identifiable is already close to prior work in state-space and structural-identifiability theory. The half-life consequence is biologically operational:

- a quantity routinely reported as an evolutionary speed can vary without bound across exactly observation-equivalent mechanisms;
- the likelihood, AIC comparison and model adequacy checks on the observed trait remain unchanged;
- the ambiguity is broken only by assumptions or measurements involving the latent process or its innovation covariance.

This is therefore a candidate bridge from structural non-identifiability to a concrete published inferential practice.

## Claim boundary

Do not state that OU half-life is never estimable. Within a fully declared one-way OU model, \(\alpha\) and \(\log2/\alpha\) may be statistically estimable. The result concerns **mechanistic transport across a broader partially observed model class**: the numerical half-life cannot be promoted from a model parameter to a uniquely identified biological response time without an independently justified causal/noise structure.
