# Structural transient-time ceilings under generalized evolutionary response

## Status

This note generalizes the parent endogenous-feedback transient ceiling from the haploid-logit response to the local scalar response of `GENERAL_EVOLUTIONARY_RESPONSE.md`.

The ingredients are all already established:

1. unit-cost finite sensing gives an integer structural-gap ceiling;
2. structural gap maps linearly to generalized gain under the continuous lift;
3. the generalized stable damped phase is bounded by `G_osc` and `G_+`;
4. local damping time increases with gain while damped-cycle period decreases with gain.

The resulting integer envelope is a composition of existing results, not a new generic optimization theorem.

---

## 1. Integer structural gain ladder

For restoring feedback

\[
e<0,
\]

define gain per structural-gap unit

\[
\boxed{
a_g=(-\beta e)\lambda>0.}
\]

For unit-cost sensing,

\[
\Delta g\in\mathbb Z_{\ge0}.
\]

Hence structurally generated generalized gains lie on the discrete ladder

\[
\boxed{G=a_g\Delta g.}
\]

The inherited finite sensing theorem supplies

\[
0\le\Delta g\le G_{gap}^{max}.
\]

---

## 2. Generalized damped interval

For

\[
0\le\alpha\le1,
\qquad
0\le\phi<1,
\]

define

\[
G_{osc}
=\frac{(\alpha-\phi)^2}{4(1-\phi)},
\]

\[
G_+
=\frac{1-\alpha\phi}{1-\phi}.
\]

Stable damped dynamics require

\[
\boxed{G_{osc}<G<G_+.}
\]

Therefore the smallest integer gap that can enter the damped phase is

\[
\boxed{
 g_{damp}^{min}
 =\min\{g\in\mathbb Z_{\ge1}:g\le G_{gap}^{max},\;G_{osc}<a_g g<G_+\}.
}
\]

The largest structurally allowed stable integer gap is

\[
\boxed{
 g_{stab}^{max}
 =\max\{g\in\mathbb Z_{\ge1}:g\le G_{gap}^{max},\;a_g g<G_+\}.
}
\]

If the first set is empty, stable damped oscillation is structurally impossible.

---

## 3. Damping-time ceiling

For stable damped generalized gain `G`,

\[
D=\alpha\phi+(1-\phi)G
\]

and

\[
\rho=\sqrt D.
\]

The exact e-folding damping time is

\[
\boxed{
\tau(G)
=-\frac{1}{\log\sqrt{\alpha\phi+(1-\phi)G}}.
}
\]

For fixed `alpha,phi`, this increases monotonically with `G` inside the stable damped phase.

Therefore

\[
\boxed{
\tau
\le
\tau(a_g g_{stab}^{max}).
}
\]

This is a universal one-sided ceiling over every realizable task inside the declared finite sensing scope.

---

## 4. Period ceiling

Inside the stable damped phase,

\[
\cos\theta
=\frac{\alpha+\phi}
{2\sqrt{\alpha\phi+(1-\phi)G}}.
\]

Thus

\[
\boxed{
T(G)
=\frac{2\pi}
{\arccos\left[(\alpha+\phi)/(2\sqrt{\alpha\phi+(1-\phi)G})\right]}.
}
\]

For the stated nonnegative `alpha,phi` domain, period is nonincreasing as `G` rises through the damped region.

Hence the longest damped cycle allowed by the integer structural ladder occurs at the first damped gap:

\[
\boxed{
T\le T(a_g g_{damp}^{min}).
}
\]

---

## 5. Exact recovery of the parent ceiling

Set

\[
\alpha=1,
\qquad
\beta=1,
\qquad
e=\eta p^*(1-p^*).
\]

Then

\[
G=L,
\quad
G_{osc}=(1-\phi)/4,
\quad
G_+=1.
\]

The integer envelope becomes exactly the parent PR #3 structural transient ceiling.

For

\[
(n,m,b,h)=(12,12,2,3),
\]

with gap ceiling four and gain per gap `0.125` at `phi=0.5`, we recover

\[
g_{damp}^{min}=2,
\qquad
g_{stab}^{max}=4,
\]

\[
\tau_{max}\approx6.95211899,
\]

\[
T_{max}\approx19.52812581.
\]

---

## 6. Same structural scope, changed time envelope

Now keep the same finite sensing scope and gain per gap but change only

\[
\alpha=0.8,
\qquad
\phi=0.5.
\]

Then

\[
G_{osc}=0.045,
\qquad
G_+=1.2.
\]

Because the first positive structural gain is

\[
a_g\cdot1=0.125>0.045,
\]

we obtain

\[
g_{damp}^{min}=1,
\qquad
g_{stab}^{max}=4.
\]

The class-wide ceilings become

\[
\boxed{
\tau_{max}\approx4.64270965\ \text{generations}
}
\]

and

\[
\boxed{
T_{max}\approx21.04927235\ \text{generations}.
}
\]

Thus changing evolutionary persistence while holding the sensing scope fixed can shorten the maximum damping time yet lengthen the maximum allowed period because it moves both the oscillation threshold and the local eigenvalue geometry.

---

## 7. Minimal four-world scope

For

\[
(n,m,b,h)=(4,3,2,2),
\]

we have

\[
G_{gap}^{max}=1.
\]

At `a_g=0.125`, `phi=0.5`:

### Parent `alpha=1`

\[
G_{osc}=0.125.
\]

The only positive structural gain lies exactly at the nonoscillatory boundary, so no damped transient exists.

### Generalized `alpha=0.7`

\[
G_{osc}=0.02.
\]

The same structural gap now lies inside the damped region. Because only gap one is available, it is simultaneously the first damped and largest stable gap.

This gives approximately

\[
\tau\le2.25856231
\]

generations and

\[
T\le17.22412046
\]

generations.

The same natural-history sensing scope therefore changes from "damped dynamics impossible" to "damped dynamics possible but tightly time-bounded" after changing only the local evolutionary response.

---

## 8. Frontier-edge cap

As before, a productive-frontier edge cap can collapse the structural gap ceiling.

At

\[
(n,m,b,h)=(12,12,2,3),
\qquad
E=3,
\]

we obtain

\[
G_{gap,E}^{max}=0.
\]

Then no positive structurally generated generalized gain exists, and the entire damped transient layer is excluded regardless of `alpha,phi,beta,lambda,e` within the stated restoring model.

---

## 9. Biological interpretation

The duration of an eco-evolutionary transient is not determined by "evolutionary rate" alone.

It is constrained by three layers:

```text
finite sensing structure
    -> which integer structural gaps are possible

response conversion beta, lambda, e
    -> how far each structural gap moves generalized gain G

persistence geometry alpha, phi
    -> where oscillation/stability boundaries lie and how slowly eigenmodes decay
```

A natural-history observation such as a fixed number of feasible cue stages can therefore provide a real upper bound on transient duration only after the evolutionary and ecological response coefficients are specified.

This also shows why structural and temporal explanations should not be collapsed. The same sensing architecture can generate different transient durations in organisms with different heritable response dynamics.

---

## 10. Validation and claim boundary

The integer envelope implementation is checked against direct enumeration of allowable integer gaps. A separate 200,000-model random audit found zero mismatches for the largest stable and smallest damped gap rules.

As throughout this branch, a finite time ceiling is a one-sided universal bound. It does not assert that a task attaining the ceiling exists.

The result remains local, deterministic, unit-cost, scalar, and tied to restoring ecological feedback under the continuous structural lift.
