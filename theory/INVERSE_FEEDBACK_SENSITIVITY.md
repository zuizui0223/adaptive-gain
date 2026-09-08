# Sensitivity of the feedback inverse near long community memory

## Status

The companion note `INVERSE_FEEDBACK_DIAGNOSTICS.md` proves an algebraic local
inverse from phenotype AR(2) coefficients, eigenvalues, or damped-transient
geometry to the closed-loop invariants `(phi,L)`.

Algebraic identifiability is not the same as empirical recoverability.

This note gives an exact deterministic perturbation identity for the phenotype-
only AR(2) inverse and shows that the reconstruction of loop gain becomes
ill-conditioned as community memory approaches one.

The perturbation algebra is elementary and is not claimed as new mathematics.
Its role is to expose a measurement-design limitation of the repository's inverse
feedback interpretation.

---

## 1. Phenotype AR(2) coefficients

Near the interior equilibrium, phenotype-logit deviations obey

\[
x_{t+2}=a_1x_{t+1}+a_2x_t,
\]

with

\[
\boxed{
a_1=1+\phi
}
\]

and

\[
\boxed{
a_2=-[\phi+(1-\phi)L].
}
\]

The exact inverse is

\[
\phi=a_1-1
\]

and

\[
L
=\frac{-a_2-\phi}{1-\phi}.
\]

---

## 2. Exact coefficient-perturbation identity

Suppose fitted coefficients differ from the exact local coefficients by

\[
\hat a_1=a_1+\epsilon_1,
\qquad
\hat a_2=a_2+\epsilon_2.
\]

Then immediately

\[
\boxed{
\hat\phi-\phi=\epsilon_1.
}
\]

For loop gain,

\[
\hat L
=\frac{-(a_2+\epsilon_2)-(\phi+\epsilon_1)}
{1-\phi-\epsilon_1}.
\]

Using

\[
-a_2-\phi=(1-\phi)L,
\]

we get the exact finite-perturbation identity

\[
\boxed{
\hat L-L
=-\frac{(1-L)\epsilon_1+\epsilon_2}
{1-\phi-\epsilon_1}.
}
\]

This is not a first-order approximation.

---

## 3. Deterministic worst-case error bound

If

\[
|\epsilon_1|\le E_1,
\qquad
|\epsilon_2|\le E_2,
\]

with

\[
E_1<1-\phi,
\]

then

\[
1-\phi-\epsilon_1
\ge
1-\phi-E_1>0.
\]

Therefore

\[
\boxed{
|\hat L-L|
\le
\frac{|1-L|E_1+E_2}
{1-\phi-E_1}.
}
\]

And, exactly,

\[
\boxed{
|\hat\phi-\phi|\le E_1.
}
\]

This is a deterministic coefficient-error envelope, not a statistical
confidence interval.

---

## 4. Local inverse Jacobian

Differentiating the inverse with respect to the fitted AR(2) coefficients gives

\[
\boxed{
\frac{\partial\phi}{\partial a_1}=1,
\qquad
\frac{\partial\phi}{\partial a_2}=0
}
\]

and

\[
\boxed{
\frac{\partial L}{\partial a_1}
=-\frac{1-L}{1-\phi},
\qquad
\frac{\partial L}{\partial a_2}
=-\frac{1}{1-\phi}.
}
\]

Hence the loop-gain inverse carries an explicit amplification factor

\[
\boxed{
(1-\phi)^{-1}.
}
\]

---

## 5. Long memory is dynamically informative but statistically difficult

The parent feedback theory showed that increasing community memory can produce

- longer damping time;
- longer oscillation period near the unit-circle boundary;
- more visible multi-generation transients.

But the inverse sensitivity gives the complementary statement:

\[
\boxed{
\phi\uparrow1
\quad\Rightarrow\quad
\text{loop-gain inversion becomes increasingly ill-conditioned.}
}
\]

So the same biological condition that makes the transient long and visually
prominent also amplifies coefficient-estimation error when reconstructing `L`.

This creates a real empirical tradeoff:

```text
high community memory
    -> stronger/longer temporal signal
    -> but poorer numerical conditioning of structural inversion.
```

That tradeoff is invisible if one discusses only forward critical slowing or only
algebraic identifiability.

---

## 6. Propagation to the structural gap

If the nonstructural scale

\[
A=(-\eta)\lambda p^*(1-p^*)
\]

is treated as independently known, then

\[
\Delta g=\frac{L}{A}.
\]

Therefore a loop-gain error envelope `E_L` gives

\[
\boxed{
E_{\Delta g}=\frac{E_L}{A}.
}
\]

This matters for the unit-cost integer diagnostic.

It is not enough to compare a point estimate of `Delta_g` with the nearest integer.
The uncertainty interval must be narrow enough to distinguish neighboring integer
structural gaps.

For example, an inferred gap near one with uncertainty larger than roughly one
half cannot meaningfully distinguish gap one from gap zero or two.

The present module propagates only uncertainty in the local AR(2) coefficients
while treating `eta`, `lambda`, and `p*` as fixed.  Their uncertainty would add
further error and remains outside the current deterministic bound.

---

## 7. Singular boundary

If the coefficient uncertainty allows

\[
\hat a_1\ge2,
\]

then

\[
\hat\phi\ge1.
\]

The current feedback parameterization no longer has a finite inverse denominator.

Thus a sufficient condition for the deterministic error envelope is

\[
\boxed{
E_1<1-\phi.
}
\]

If that condition fails, the local coefficient uncertainty itself crosses the
long-memory singular boundary and a finite model-specific bound on `L` cannot be
claimed from this formula.

---

## 8. Independent audit

Across 200,000 random models with

- `0 <= phi < 0.98`;
- `-0.5 <= L <= 1.5`;
- lag-one coefficient error envelope below `0.4(1-phi)`;
- independent lag-two error envelope;

random perturbations were compared with the exact deterministic error bound.

Results:

- bound violations: `0`;
- maximum observed ratio `|L_hat-L| / bound`: `0.9993340639582554`.

The near-one maximum is expected because the analytic bound can be approached by
aligned corner perturbations.

---

## 9. Empirical claim boundary

The result does **not** solve statistical inference for noisy ecological time
series.

It does not address

- errors-in-variables bias in AR coefficient fitting;
- finite sample bias;
- observation noise on phenotype frequencies;
- demographic/process stochasticity;
- irregular sampling;
- model misspecification or nonlocal trajectories.

Its role is narrower:

\[
\boxed{
\text{even under the correct local model, the inverse has a quantifiable conditioning limit set by community memory.}
}
\]

That limit should be carried into any future empirical estimator rather than
assuming that algebraic invertibility guarantees practical recoverability.
