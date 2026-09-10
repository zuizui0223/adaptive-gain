# Scalar transient observability before parameter identifiability

## Status

`GENERAL_RESPONSE_IDENTIFIABILITY.md` assumes that a local scalar trajectory has
already identified the characteristic invariants

\[
(T,D).
\]

This note states the preceding observability gate.

Even in a noiseless deterministic system, one observed evolutionary coordinate
need not expose both local modes.  If only one mode is visible, the trajectory can
be arbitrarily long while the second-order invariants remain unidentified.

No novelty is claimed for second-order linear recurrence identification or Hankel
rank conditions.  The repository-specific role is to prevent a one-mode
phenotype trajectory from being overinterpreted as evidence about ecological
memory, evolutionary persistence, or structural feedback gain.

---

## 1. Four consecutive observations

A scalar coordinate of the local two-dimensional system obeys

\[
\boxed{
x_{t+2}=T x_{t+1}-D x_t.}
\]

Four consecutive observations give

\[
x_2=T x_1-Dx_0,
\]

\[
x_3=T x_2-Dx_1.
\]

Equivalently,

\[
\begin{pmatrix}
x_1 & -x_0\\
x_2 & -x_1
\end{pmatrix}
\begin{pmatrix}T\\D\end{pmatrix}
=
\begin{pmatrix}x_2\\x_3\end{pmatrix}.
\]

The determinant of this identification system is

\[
\boxed{
R=x_0x_2-x_1^2.
}
\]

If

\[
R\ne0,
\]

then

\[
\boxed{
T=\frac{x_0x_3-x_1x_2}{R}
}
\]

and

\[
\boxed{
D=\frac{x_1x_3-x_2^2}{R}.
}
\]

Thus four noiseless points are sufficient **only when the scalar observation has
rank two**.

---

## 2. Single-mode trajectories fail the gate

Suppose the observed phenotype trajectory contains only one local mode:

\[
x_t=c r^t.
\]

Then

\[
x_0x_2-x_1^2
=c^2r^2-c^2r^2
=0.
\]

So

\[
\boxed{
R=0.
}
\]

The trajectory reveals the visible eigenvalue \(r\), but not the second local
mode and therefore not the full pair \((T,D)\).

Collecting more points along the same pure mode does not repair the structural
rank deficiency.

---

## 3. Two real modes make the gate explicit

For

\[
x_t=c_1r_1^t+c_2r_2^t,
\]

direct expansion gives

\[
\boxed{
R
=c_1c_2(r_1-r_2)^2.
}
\]

Hence rank closes when

- \(c_1=0\): mode 1 is absent;
- \(c_2=0\): mode 2 is absent;
- \(r_1=r_2\): the two modes are not dynamically distinct.

This provides a simple perturbation-design interpretation:

\[
\boxed{
\text{both modes must be excited and visible.}
}
\]

---

## 4. Near-degeneracy is an empirical conditioning problem

The exact algebra uses only

\[
R\ne0.
\]

But when

\[
|R|
\]

is very small relative to the scale of the observations, the formulas for
\(T,D\) divide by a small quantity.

So there are two separate boundaries:

```text
R = 0
    exact non-observability

|R| small
    algebraically observable but numerically / statistically fragile
```

The executable helper reports a normalized visibility margin and allows a
numerical singularity threshold.  It is not a confidence interval.

---

## 5. Consequence for the evolutionary-timescale question

The generalized theory now has two successive gates.

### Gate 1 — mode observability

Can the phenotype trajectory identify

\[
(T,D)?
\]

This requires both local modes to be visible.

### Gate 2 — biological identifiability

Even if \((T,D)\) are known exactly, can they be decomposed into

\[
(\alpha,\phi,G)?
\]

In general, no.  One independent evolutionary- or ecological-persistence
measurement is still required.

Thus

\[
\boxed{
\text{long time series}
\not\Rightarrow
\text{timescale decomposition}.
}
\]

A long series can fail because it contains only one mode, or because two visible
modes still leave biological parameters confounded.

---

## 6. Experimental implication

A perturbation experiment should not merely extend the number of observed
generations.  It should attempt to excite distinct directions of the coupled
system.

For example, conceptually separate perturbations can target

- the evolutionary coordinate while minimizing immediate community displacement;
- the community coordinate while minimizing immediate evolutionary displacement.

The exact experimental realization is system-specific, but the mathematical
criterion is not:

\[
\boxed{
R=x_0x_2-x_1^2
}
\]

must be detectably nonzero before scalar-transient inversion is treated as a
second-order identification problem.

---

## 7. Independent audit

For 200,000 random two-real-mode trajectories,

\[
x_t=c_1r_1^t+c_2r_2^t,
\]

the direct Hankel determinant and the closed form

\[
c_1c_2(r_1-r_2)^2
\]

agreed with maximum absolute error

\[
5.33\times10^{-15}.
\]

Synthetic nondegenerate recurrences recover \((T,D)\) directly in the test
suite, while pure single-mode, repeated-eigenvalue, missing-mode, and
near-degenerate examples are rejected by the declared gate.

---

## 8. Claim boundary

This note does not establish statistical observability under noise, optimal
perturbation design, or state-space system identification from finite field data.

Its role is narrower:

> before interpreting a phenotype trajectory as evidence about eco-evolutionary
> timescales, verify that the observed scalar series actually carries two local
> dynamical modes.

Only after that gate is passed does the generalized biological identifiability
problem in `GENERAL_RESPONSE_IDENTIFIABILITY.md` become relevant.
