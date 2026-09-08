# Inverse diagnostics: from evolutionary transients back to sensing structure

## Status

This note reverses the local deterministic feedback theory developed in the
parent endogenous-feedback branch.

The algebraic inversion of a two-dimensional linear map, AR(2) recurrence, or
complex eigenvalue pair is standard.  No novelty is claimed for those tools.

The repository-specific question is instead:

> can an observed eco-evolutionary transient be mapped back to the exact finite
> sensing structure strongly enough to test or falsify a proposed adaptive-gain
> mechanism?

The answer has two layers.

1. Local transient geometry identifies the **community-memory parameter** `phi`
   and the **closed structural loop gain** `L`.
2. Recovering the exact structural gap `Delta_g` from `L` requires independent
   information about ecological feedback strength, fitness scaling, and
   equilibrium evolutionary responsiveness.

This creates a sharp identifiability boundary and makes natural-history data part
of the inverse problem rather than merely biological decoration.

---

## 1. Forward local invariants

The parent feedback model has local Jacobian

\[
J=
\begin{pmatrix}
1 & \Delta s\\
(1-\phi)\eta p^*(1-p^*) & \phi
\end{pmatrix}.
\]

Define

\[
L=-\eta\Delta s\,p^*(1-p^*).
\]

Then the two local invariants are

\[
\boxed{
T=\operatorname{tr}J=1+\phi
}
\]

and

\[
\boxed{
D=\det J=\phi+(1-\phi)L.
}
\]

Therefore every local observable that identifies the trace and determinant also
identifies `phi` and `L`:

\[
\boxed{
\phi=T-1,
\qquad
L=\frac{D-\phi}{1-\phi}.
}
\]

The current endogenous-feedback model assumes

\[
0\le\phi<1.
\]

The inverse diagnostic retains that scope rather than silently extending the
biological interpretation to negative ecological memory.

---

## 2. Inversion from local eigenvalues

Let the local eigenvalues be

\[
\lambda_1,\lambda_2.
\]

Then

\[
T=\lambda_1+\lambda_2,
\qquad
D=\lambda_1\lambda_2.
\]

Hence

\[
\boxed{
\phi
=\lambda_1+\lambda_2-1
}
\]

and

\[
\boxed{
L
=\frac{\lambda_1\lambda_2-\phi}{1-\phi}.
}
\]

This route is useful when the local two-dimensional map has been estimated
explicitly.

It does not require the system to be in the stable damped phase; the trace and
determinant inversion is algebraic wherever the stated parameterization is
nondegenerate.

---

## 3. Inversion from damping time and oscillation period

Inside the stable damped phase, write the conjugate pair as

\[
\rho e^{\pm i\theta}.
\]

If the observed local e-folding damping time is

\[
\tau
\]

and the oscillation period is

\[
P,
\]

then

\[
\boxed{
\rho=e^{-1/\tau}
}
\]

and

\[
\boxed{
\theta=\frac{2\pi}{P}.
}
\]

Since

\[
T=2\rho\cos\theta
\]

and

\[
D=\rho^2,
\]

we obtain

\[
\boxed{
\phi
=2e^{-1/\tau}\cos(2\pi/P)-1
}
\]

and

\[
\boxed{
L
=\frac{e^{-2/\tau}-\phi}{1-\phi}.
}
\]

Thus an observed damped transient can separate

```text
community memory phi
from
closed-loop gain L.
```

This is important because the forward theory shows that long transient duration
can arise from either source.

---

## 4. Phenotype-only AR(2) inversion

Direct community-state observation is not mathematically necessary for the local
inverse.

Let

\[
x_t
\]

be the deviation of phenotype logit from its interior equilibrium:

\[
x_t
=\operatorname{logit}(p_t)-\operatorname{logit}(p^*).
\]

Every component of a two-dimensional linear system obeys its characteristic
second-order recurrence.  Therefore

\[
\boxed{
x_{t+2}
=(1+\phi)x_{t+1}
-[\phi+(1-\phi)L]x_t.
}
\]

Suppose a local phenotype-only time series supports the deterministic recurrence

\[
\boxed{
x_{t+2}=a_1x_{t+1}+a_2x_t.}
\]

Then

\[
T=a_1,
\qquad
D=-a_2.
\]

Hence

\[
\boxed{
\phi=a_1-1
}
\]

and

\[
\boxed{
L
=\frac{-a_2-\phi}{1-\phi}.
}
\]

So, under the local deterministic model and provided the relevant mode is visible
in the phenotype trajectory,

\[
\boxed{
\text{phenotype time series alone can identify }(\phi,L).
}
\]

This does **not** mean that the structural mechanism is identified from phenotype
alone.  It identifies only the two closed-loop invariants.

In real data, estimating an AR(2) relation robustly would require observation
noise, process noise, sampling interval, transient localization, and model-checking
that are outside the present deterministic theorem.

---

## 5. The central identifiability boundary

Under the continuous structural lift,

\[
\Delta s=\lambda\Delta g
\]

and therefore

\[
\boxed{
L
=(-\eta)\lambda\Delta g\,p^*(1-p^*).
}
\]

The transient identifies the product `L`, not its factors.

Therefore

\[
\boxed{
\text{local time series}
\not\Rightarrow
\Delta g\text{ by itself}.
}
\]

To recover the structural gap, one must independently know or estimate

- ecological feedback slope `eta`;
- fitness conversion `lambda`;
- equilibrium phenotype frequency `p*`.

Then

\[
\boxed{
\Delta g
=\frac{L}
{(-\eta)\lambda p^*(1-p^*)}.
}
\]

This is where natural history and direct ecological measurements become
mathematically indispensable.

For example:

- `eta` requires measuring how phenotype frequency changes the future prevalence
  of the relevant community state;
- `lambda` requires a fitness calibration for the structural sensing advantage;
- `p*` is observable from the evolving population.

The exact sensing theory alone cannot supply these quantities.

---

## 6. Unit-cost integrality becomes a diagnostic

In the unit-cost deterministic theory,

\[
C_A,C_F\in\mathbb Z
\]

and therefore

\[
\boxed{
\Delta g\in\mathbb Z.
}
\]

An inferred structural contrast far from every nonnegative integer is therefore
incompatible with the exact unit-cost structural lift, subject to estimation
uncertainty.

The executable diagnostic records

- inferred real-valued `Delta_g`;
- nearest integer;
- distance to that integer;
- compatibility with a user-declared tolerance.

This is not intended as a naive statistical test.  The tolerance must reflect the
uncertainty of the fitted dynamical and ecological parameters.  The theoretical
point is that the structural model generates a discrete prediction once its
continuous nuisance factors are calibrated.

---

## 7. Finite sensing bounds provide a falsification test

The parent bounded-arity theorem gives, for a unit-cost high-state task with

\[
C_A=h,
\]

\[
C_F\le\min\{m,F_b(n,h)\}.
\]

Therefore, against a gap-zero comparison state,

\[
\boxed{
\Delta g
\le
\min\{m,F_b(n,h)\}-h.
}
\]

With a productive-frontier edge cap `E`,

\[
\boxed{
\Delta g
\le
\min\{m,E,F_b(n,h)\}-h.
}
\]

Consequently, if the dynamically inferred and independently factorized gap exceeds
this upper bound, then

\[
\boxed{
\text{the declared finite sensing scope is falsified as the source of the observed loop gain.}
}
\]

This is stronger than saying that one hand-built task fits poorly.  The inherited
bound excludes the entire declared structural class.

A compatibility result in the opposite direction is only one-sided: an inferred
gap below the upper bound is not proof that an appropriate task exists.

---

## 8. Repo-native round trip

Use the existing gap-zero / gap-one pair

- `routing_bypass_control()`;
- `payoff_routing_task()`.

With

\[
\lambda=1,
\qquad
\eta=-\frac12,
\qquad
p^*=\frac12,
\]

we have

\[
\Delta g=1
\]

and therefore

\[
L=\frac18.
\]

Take

\[
\phi=0.8.
\]

The forward damped transient has approximately

\[
\tau_{\rm damp}=10.3965\ \text{generations}
\]

and

\[
P=46.4554\ \text{generations}.
\]

The inverse formulas recover

\[
\hat\phi=0.8,
\qquad
\hat L=0.125.
\]

Using the independently supplied

\[
(-\eta)\lambda p^*(1-p^*)=0.125
\]

then gives

\[
\boxed{
\hat{\Delta g}=1.
}
\]

The minimal structural scope

\[
(n,m,b,h)=(4,3,2,2)
\]

has inherited gap upper bound one, so the reconstructed mechanism sits exactly on
that structural boundary.

---

## 9. Structural rejection examples

An inferred

\[
\Delta g=4
\]

is incompatible with the minimal

\[
(4,3,2,h=2)
\]

scope because its gap upper bound is one.

The same inferred gap is not ruled out by

\[
(12,12,2,h=3),
\]

whose inherited upper bound is four.

Likewise, an otherwise acceptable inferred gap can become structurally impossible
when a productive-frontier edge cap is added.

For example, at

\[
(12,12,2,h=3,E=3),
\]

the structural gap upper bound is zero.

Thus the inverse pipeline can distinguish

```text
transient compatible with a broad sensing scope
from
transient impossible under a stronger obligation constraint.
```

---

## 10. Independent numerical audits

Three independent forward/inverse audits were run.

### Damping-period inversion

Across 200,000 random stable damped points,

\[
(L,\phi)
\to
(\tau,P)
\to
(\hat L,\hat\phi),
\]

with maximum errors

- `|L-L_hat| <= 2.55e-14`;
- `|phi-phi_hat| <= 3.33e-16`.

### Eigenvalue inversion

Across 200,000 random points in the declared feedback parameter domain, direct
local eigenvalues were inverted back to the model invariants with maximum errors

- `|L-L_hat| <= 2.83e-14`;
- `|phi-phi_hat| <= 3.30e-16`.

### Phenotype AR(2) inversion

Across 200,000 random points,

\[
(L,\phi)
\to
(a_1,a_2)
\to
(\hat L,\hat\phi),
\]

with maximum errors

- `|L-L_hat| <= 1.92e-14`;
- `|phi-phi_hat| <= 1.11e-16`.

These are algebraic consistency checks, not empirical identifiability simulations
with noise.

---

## 11. Empirical workflow suggested by the theory

A natural-system application could proceed in layers.

### A. Identify a local transient

Observe phenotype frequency across enough generations to determine whether the
trajectory is approximately local to an interior state.

### B. Estimate dynamical invariants

Use either

- a joint phenotype/community local linearization;
- damping time and oscillation period;
- phenotype-logit AR(2) coefficients

to estimate `phi` and `L`.

### C. Independently estimate the nonstructural factors

Measure

- community response to phenotype frequency -> `eta`;
- fitness conversion of sensing burden -> `lambda`;
- equilibrium phenotype frequency -> `p*`.

### D. Infer structural gap

Compute

\[
\hat{\Delta g}
=\frac{\hat L}
{(-\hat\eta)\hat\lambda\hat p^*(1-\hat p^*)}.
\]

### E. Confront the finite sensing theory

Check

- unit-cost integrality, when appropriate;
- bounded-arity gap ceiling;
- productive-frontier edge ceiling;
- natural-history feasibility of the implied cue graph.

The outcome can be a rejection.  That is a feature: the inverse layer is intended
to expose structural incompatibility rather than force every transient into the
adaptive-gain explanation.

---

## 12. Claim boundary

The exact result is a local deterministic identifiability statement for the
specified feedback model.

It does **not** establish

- statistically consistent AR(2) estimation under process or observation noise;
- causal identification of `eta` or `lambda` from phenotype trajectories;
- global nonlinear parameter identification;
- uniqueness of ecological mechanisms sharing the same local `phi,L`;
- empirical support for the feedback model in a natural system.

The strongest current statement is therefore:

\[
\boxed{
\text{local transient geometry identifies }(\phi,L),
\text{ while natural-history/fitness measurements are required to factor }L\text{ into structural mechanism.}
}
\]

That boundary is useful because it says exactly what time-series data can recover
on their own and exactly where biological information must enter.
