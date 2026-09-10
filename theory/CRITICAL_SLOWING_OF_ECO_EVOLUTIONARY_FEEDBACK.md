# Critical slowing of stable eco-evolutionary feedback

## Status and claim boundary

This note refines the **time** interpretation of the stable damped phase in
`STRUCTURAL_LOOP_GAIN_PHASE_DIAGRAM.md`.

Critical slowing near a discrete-time stability boundary is standard dynamical-
systems theory.  The repository does not claim that asymptotic phenomenon as new.
The repository-specific link is that the distance to the boundary contains the
exact adaptive/fixed structural gap through the loop gain

\[
L=-\eta\lambda\Delta g\,p^*(1-p^*).
\]

The result matters for the motivating evolutionary-timescale question because a
system can remain locally stable while showing evolutionary and community
oscillations for many generations.  Such a long transient is mathematically
different from a genuine long-run directional evolutionary trend.

---

## 1. Exact damping rate inside the damped phase

In the stable damped phase,

\[
\frac{1-\phi}{4}<L<1,
\]

the local eigenvalues are a complex conjugate pair.  Their squared modulus is
the determinant:

\[
\rho^2
=\det J
=\phi+(1-\phi)L.
\]

Rearrange this as

\[
\boxed{
\rho^2
=1-(1-\phi)(1-L).
}
\]

Define

\[
\epsilon=(1-\phi)(1-L).
\]

Then

\[
\rho=\sqrt{1-\epsilon}.
\]

The local e-folding damping time in generations is

\[
\tau_{\rm damp}
=-\frac{1}{\log\rho}.
\]

Therefore

\[
\boxed{
\tau_{\rm damp}
=-\frac{2}{\log(1-\epsilon)}
=-\frac{2}{\log[1-(1-\phi)(1-L)]}.
}
\]

This expression is exact throughout the stable damped phase.

---

## 2. Two independent routes to long transients

For small positive `epsilon`,

\[
-\log(1-\epsilon)
\sim\epsilon.
\]

Hence

\[
\boxed{
\tau_{\rm damp}
\sim
\frac{2}{(1-\phi)(1-L)}.
}
\]

There are therefore two conceptually distinct ways to make the transient long.

### Structural-feedback criticality

\[
L\uparrow1.
\]

The feedback loop approaches its oscillatory unit-circle instability boundary.
Because

\[
L=-\eta\lambda\Delta g\,p^*(1-p^*),
\]

this can be caused by

- a larger structural adaptive-gap contrast `Delta_g`;
- stronger ecological feedback magnitude `-eta`;
- stronger fitness conversion `lambda`;
- an equilibrium closer to intermediate phenotype frequency, where
  `p*(1-p*)` is large.

### Ecological memory criticality

\[
\phi\uparrow1.
\]

The community itself relaxes slowly.  Even a loop gain well below the instability
boundary can then take many generations to damp.

The exact asymptotic shows that these two sources multiply:

\[
\boxed{
\text{slow transient factor}
\propto
\frac{1}{(1-\phi)(1-L)}.
}
\]

A structurally stiff feedback loop embedded in a persistent community is therefore
especially slow to forget a perturbation.

---

## 3. A diagnostic scaled ratio

Define

\[
Q_{\rm slow}
=
\frac{\tau_{\rm damp}(1-\phi)(1-L)}{2}.
\]

Then

\[
\boxed{
Q_{\rm slow}\to1
}
\]

as

\[
(1-\phi)(1-L)\to0^+.
\]

The executable implementation exposes this quantity directly.  It provides a
simple audit that a numerical model has entered the asymptotic critical-slowing
regime.

---

## 4. Critical oscillation period also lengthens with community memory

At the strong-feedback boundary

\[
L=1,
\]

the unit-modulus pair has angle

\[
\cos\theta_c
=\frac{1+\phi}{2}.
\]

Let

\[
\delta=1-\phi.
\]

Then

\[
\cos\theta_c
=1-\frac{\delta}{2}.
\]

For small `delta`,

\[
\theta_c\sim\sqrt{\delta}.
\]

Thus the critical period obeys

\[
\boxed{
T_c
\sim
\frac{2\pi}{\sqrt{1-\phi}}.
}
\]

So increasing community memory has two different temporal effects near the
instability boundary:

- damping becomes slower as `(1-phi)^{-1}` for fixed distance `1-L`;
- the oscillation period itself becomes longer as `(1-phi)^{-1/2}` at `L=1`.

Long ecological memory therefore creates both long-lived and long-period
transients.

---

## 5. Distinguishing three kinds of long evolutionary time

The parent evolutionary-timescale branch and the endogenous feedback branch now
separate three mechanisms that can all look like "evolution continuing for a
long time" in a finite record.

### Long-run directional accumulation

The parent Markov-reward theory has

\[
\bar s\ne0.
\]

Then

\[
E[S_H]=H\bar s
\]

and directional evolution is genuinely `O(H)`.

### Directionally balanced fluctuation

The parent branch can have

\[
\bar s=0
\]

while state-specific selection remains strong.  The RMS directional residue is
only `O(sqrt(H))`, and the retained fraction decays as `H^{-1/2}`.

### Critical slowing around a stable endogenous equilibrium

The current branch can have a **stable** interior equilibrium but

\[
\tau_{\rm damp}\gg1.
\]

The system then shows a long transient that eventually disappears.

These are not interchangeable explanations:

```text
long-term trend
    nonzero stationary mean selection

long fluctuating history
    zero mean but recurrent state-dependent selection

long stable transient
    loop gain / community memory near a local stability boundary
```

A natural system observed for only a few tens of generations could confuse the
three unless both the temporal trajectory and the underlying feedback structure
are measured.

---

## 6. Structural interpretation

Under the continuous lift,

\[
L=-\eta\lambda\Delta g\,p^*(1-p^*).
\]

Therefore the exact damping denominator is

\[
1-L
=
1+\eta\lambda\Delta g\,p^*(1-p^*).
\]

For negative feedback, increasing the finite-task structural contrast

\[
\Delta g
\]

can push the system closer to critical slowing even before it crosses the
instability boundary.

This creates a more nuanced interpretation of large adaptive gain:

> a larger static contingent-sensing advantage can make the closed ecological
> feedback not only stronger, but also slower to settle.

The parent bounded-arity / frontier bounds then constrain how close a declared
finite sensing scope can come to this critical region.

---

## 7. Independent numerical audit

The executable formulas were independently checked using direct eigenvalues.

For 200,000 random points in the stable damped region:

- maximum absolute error between direct eigenvalue modulus and
  `sqrt(phi+(1-phi)L)` was `1.11e-16`;
- maximum relative error between damping time from direct eigenvalues and the
  exact closed form was `4.15e-10`.

For 100,000 points satisfying

\[
\epsilon=(1-\phi)(1-L)\le10^{-3},
\]

the maximum deviation of

\[
\tau_{\rm damp}\epsilon/2
\]

from one was `5.01e-4`.

For 100,000 long-memory boundary points with

\[
10^{-6}\le1-\phi\le10^{-2},
\]

the maximum relative error of

\[
T_c\approx2\pi/\sqrt{1-\phi}
\]

was `4.18e-4`.

---

## 8. Scope boundary

This note concerns local linearized behavior around the interior equilibrium of
the minimal deterministic two-community-state feedback model.

It does not establish

- global persistence of nonlinear oscillations beyond the local boundary;
- stochastic early-warning indicators;
- demographic critical slowing;
- mutation, migration, drift, or multiple evolving species;
- an empirical critical transition in any natural system.

The biological use is instead a precise timescale distinction: if natural history
can estimate structural gap contrast, ecological feedback slope, community
memory, and equilibrium phenotype frequency, the model predicts whether observed
long dynamics are compatible with a slowly damped stable loop.
