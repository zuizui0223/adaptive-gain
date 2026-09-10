# Structural ceilings on eco-evolutionary transient times

## Status

This note combines three results already present in the repository:

1. finite unit-cost sensing tasks have an exact structural upper bound on `C_F-C_A` at fixed world/query/arity/adaptive-cost scope;
2. the endogenous feedback layer maps structural gap contrast to loop gain

   \[
   L=-\eta\lambda\Delta g\,p^*(1-p^*);
   \]

3. in the stable damped phase,

   \[
   \rho^2=\phi+(1-\phi)L
   \]

   determines the local damping time and oscillation period.

No new combinatorial or dynamical-systems theorem is claimed.  The repository-specific result is that the existing finite sensing bounds can now certify not only which feedback phases are impossible, but also how long any stable damped transient can persist within a declared structural scope.

---

## 1. Structural gap bound

For unit-cost tasks with

- `n` represented worlds;
- `m` declared queries;
- maximum query arity `b`;
- adaptive optimum `C_A=h`;

the parent theorem gives

\[
C_F\le \min\{m,F_b(n,h)\}.
\]

Against a gap-zero low-opportunity state,

\[
\boxed{
\Delta g\le G_{\max}
:=\min\{m,F_b(n,h)\}-h.
}
\]

With a productive-frontier edge cap `E`, replace this by

\[
\boxed{
G_{\max,E}
=\min\{m,E,F_b(n,h)\}-h.
}
\]

Because the task is unit-cost,

\[
\Delta g\in\mathbb Z_{\ge0}.
\]

That integrality is the key extra ingredient for the transient-time ceiling.

---

## 2. Gain per unit structural gap

For restoring feedback let

\[
\eta<0,
\qquad
\lambda\ge0,
\qquad
0<p^*<1.
\]

Define

\[
\boxed{
a
=(-\eta)\lambda p^*(1-p^*).}
\]

Then every integer structural contrast `g` generates

\[
\boxed{
L=ag.
}
\]

The local stability condition is

\[
0<L<1.
\]

Hence the largest stable integer gap allowed by the structural scope is

\[
\boxed{
g_{\rm stab}^{\max}
=\max\{g\in\mathbb Z:\ 1\le g\le G_{\max},\ ag<1\}.
}
\]

If this set is empty, the declared scope admits no positive restoring stable loop through this structural contrast.

The executable implementation handles the strict `L<1` boundary explicitly.

---

## 3. Entering the damped phase

The damped-oscillation boundary is

\[
L>\frac{1-\phi}{4}.
\]

Therefore the first integer structural gap that can enter the damped phase is

\[
\boxed{
g_{\rm damp}^{\min}
=\min\left\{
 g\in\mathbb Z:\
 1\le g\le G_{\max},
 \frac{1-\phi}{4}<ag<1
\right\}.
}
\]

If no such integer exists, stable damped oscillation is structurally impossible in the entire declared finite sensing scope.

This sharpens the earlier continuous upper-bound certificate because it uses the fact that structural gaps arrive in integer steps.

---

## 4. Maximum damping time

Inside the stable damped phase,

\[
\rho^2
=\phi+(1-\phi)L,
\]

so

\[
\boxed{
\tau_{\rm damp}(L,\phi)
=-\frac{1}{\log\rho}
=-\frac{2}{\log[1-(1-\phi)(1-L)]}.
}
\]

For fixed `phi`, this quantity is strictly increasing in `L` throughout the damped phase.

Therefore, if a damped phase is structurally allowed at all,

\[
\boxed{
\tau_{\rm damp}
\le
\tau_{\rm damp}
\left(
 a g_{\rm stab}^{\max},
 \phi
\right).
}
\]

This is a one-sided structural ceiling valid for every realizable task in the declared scope.

It is not an existence statement that some task attains the ceiling.

---

## 5. Maximum damped-cycle period

For a stable damped pair, let

\[
D=\phi+(1-\phi)L,
\qquad
\rho=\sqrt D.
\]

The eigenvalue angle satisfies

\[
\cos\theta
=\frac{1+\phi}{2\rho},
\]

and the local oscillation period is

\[
\boxed{
T(L,\phi)
=\frac{2\pi}{
\arccos\left[(1+\phi)/(2\sqrt{\phi+(1-\phi)L})\right]
}.
}
\]

Within the stable damped phase, `T` decreases monotonically with `L`.

Therefore the longest damped cycle permitted by the integer structural envelope occurs at the first damped integer gap:

\[
\boxed{
T
\le
T\left(
 a g_{\rm damp}^{\min},
 \phi
\right).
}
\]

Again this is a universal ceiling over the declared structural scope, not an existence theorem.

---

## 6. Repo-native examples

### Minimal four-world scope

For

\[
(n,m,b,h)=(4,3,2,2),
\]

the parent theorem gives

\[
G_{\max}=1.
\]

Take

\[
\eta=-\frac12,
\qquad
\lambda=1,
\qquad
p^*=\frac12,
\qquad
\phi=\frac12.
\]

Then

\[
a=\frac18
\]

and the damped threshold is also

\[
\frac{1-\phi}{4}=\frac18.
\]

The only positive integer gap gives `L=1/8`, exactly the nonoscillatory boundary. Therefore

\[
\boxed{
\text{no stable damped transient is possible in this entire scope.}
}
\]

The existing `payoff_routing_task()` attains the structural gap bound itself.

### Medium binary scope

For

\[
(n,m,b,h)=(12,12,2,3),
\]

the inherited bound gives

\[
G_{\max}=4.
\]

With the same feedback parameters,

\[
g_{\rm damp}^{\min}=2,
\qquad
L_{\rm damp}^{\min}=\frac14,
\]

and

\[
g_{\rm stab}^{\max}=4,
\qquad
L_{\rm stab}^{\max}=\frac12.
\]

Hence every stable damped transient in this structural scope obeys approximately

\[
\boxed{
\tau_{\rm damp}\le 6.9521\ \text{generations}
}
\]

and

\[
\boxed{
T\le 19.5281\ \text{generations}.
}
\]

So the finite sensing scope bounds not only whether oscillation can occur, but how persistent and how long-period it can be.

### Frontier-edge cap

At the same `n,m,b,h`, imposing

\[
E=3
\]

gives

\[
G_{\max,E}=0.
\]

Thus no restoring structural loop, damped phase, or associated transient time is available through this gap mechanism.

---

## 7. Relation to critical slowing

Without a finite structural ceiling, the damped time diverges as

\[
L\uparrow1
\]

or

\[
\phi\uparrow1.
\]

Near the boundary,

\[
\tau_{\rm damp}
\sim
\frac{2}{(1-\phi)(1-L)}.
\]

The present result shows when finite sensing structure prevents the loop from approaching `L=1` closely enough to realize arbitrary critical slowing.

Thus two layers jointly determine long transient time:

```text
community memory phi
        x
structurally attainable stable loop gain L
```

The parent combinatorics constrain the second factor.

---

## 8. Biological interpretation

The result separates three statements that should not be conflated.

### Long-run directional trend

Generated by nonzero long-run mean selection in the parent timescale theory.

### Balanced recurrent fluctuation

Strong selection can persist while signed accumulation cancels through time.

### Long stable transient

Even with a stable equilibrium and no permanent directional trend, a system near the feedback boundary can take many generations to damp out.

Finite sensing structure can place an upper bound on the third phenomenon.

Therefore a long observed evolutionary trajectory need not imply ongoing directional adaptation.  It may instead be a slowly decaying eco-evolutionary transient, and the feasible duration of that transient can sometimes be constrained from the organism's finite information-acquisition structure.

---

## 9. Claim boundary

The following ingredients are standard and are not claimed as new:

- damping-time and oscillation-period formulas for a complex conjugate eigenvalue pair;
- monotonicity of damping with eigenvalue modulus;
- integer-envelope optimization;
- critical slowing near a unit-circle boundary.

The repository-specific contribution is the chain

```text
finite sensing constraints
-> exact structural gap ceiling
-> integer stable/damped gap envelope
-> loop-gain envelope
-> universal transient-time ceiling.
```

The result remains local, deterministic, unit-cost, and tied to the stated two-community-state feedback lift.
