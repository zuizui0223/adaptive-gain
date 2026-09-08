# Feedback inverse-diagnostics branch

This dependent branch reverses the local forward theory from the endogenous
community-feedback branch.

```text
observed local evolutionary transient
        |
        +--> eigenvalue pair
        |
        +--> damping time + period
        |
        +--> phenotype-logit AR(2)
        |
        v
community memory phi + loop gain L
        |
        +--> independent eta, lambda, p*
        |
        v
inferred structural gap Delta_g
        |
        v
unit-cost integrality + bounded-arity/frontier compatibility
        |
        v
structural mechanism retained or falsified
```

Read `INVERSE_FEEDBACK_DIAGNOSTICS.md` for the full derivation and claim boundary.

Executable layer:

- `adaptive_gain/feedback_inverse_diagnostics.py`
- `tests/test_feedback_inverse_diagnostics.py`
- `tests/test_feedback_inverse_ar2.py`
- `validation/feedback_inverse_diagnostics_v1.json`

The local forward invariants are

\[
T=1+\phi,
\qquad
D=\phi+(1-\phi)L.
\]

Hence local eigenvalues identify

\[
\boxed{
\phi=T-1,
\qquad
L=\frac{D-\phi}{1-\phi}.
}
\]

Inside the stable damped phase,

\[
\rho=e^{-1/\tau},
\qquad
\theta=2\pi/P,
\]

so

\[
\boxed{
\phi=2\rho\cos\theta-1,
\qquad
L=\frac{\rho^2-\phi}{1-\phi}.
}
\]

Direct community-state observation is not required for the local algebra.  If
phenotype-logit deviations satisfy

\[
x_{t+2}=a_1x_{t+1}+a_2x_t,
\]

then

\[
\boxed{
\phi=a_1-1,
\qquad
L=\frac{-a_2-\phi}{1-\phi}.
}
\]

The crucial identifiability boundary is

\[
\boxed{
L=(-\eta)\lambda\Delta g\,p^*(1-p^*).
}
\]

Time-series geometry identifies `L`; it does not identify its biological factors
separately.  Recovering the exact structural gap therefore requires independent
natural-history / ecological / fitness information for `eta`, `lambda`, and
`p*`.

Once those are supplied,

\[
\boxed{
\Delta g
=\frac{L}{(-\eta)\lambda p^*(1-p^*)}.
}
\]

The unit-cost finite theory then makes two falsifiable predictions:

1. `Delta_g` should lie near a non-negative integer, within a tolerance justified
   by estimation uncertainty;
2. it must not exceed the inherited bounded-arity / productive-frontier gap
   ceiling for the declared sensing scope.

Thus this branch is not a claim that every observed oscillation proves adaptive
sensing structure.  Its purpose is the opposite: to expose what the transient
actually identifies and to make the proposed structural mechanism rejectable.

Independent algebraic audits use 200,000 random models for each inversion route.
The maximum round-trip errors are at machine precision (`~1e-14` for `L` and
`~1e-16` for `phi`).  These are algebraic validation checks, not noisy empirical
identifiability experiments.
