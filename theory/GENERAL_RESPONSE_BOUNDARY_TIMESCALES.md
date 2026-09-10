# Two critical-slowing boundaries in the generalized evolutionary response

## Status

`GENERAL_EVOLUTIONARY_RESPONSE.md` gives the exact local stability interval

\[
G_-<G<G_+,
\]

with

\[
G_- = \alpha-1,
\qquad
G_+ = \frac{1-\alpha\phi}{1-\phi}.
\]

The upper boundary `G_+` is the oscillatory unit-circle boundary already discussed in the parent feedback theory. The generalized model reveals a second, lower boundary that matters whenever the evolutionary update has intrinsic damping.

The eigenvalue asymptotics below are standard local dynamical-systems results. The repository-specific use is to show how the structurally generated gain can create long evolutionary transients near **either** edge of the admissible feedback interval.

---

## 1. Lower boundary

At

\[
G=G_-=\alpha-1,
\]

the characteristic polynomial has roots

\[
\boxed{
\lambda_1=1,
\qquad
\lambda_2=\alpha+\phi-1.
}
\]

For

\[
0\le\alpha\le1,
\qquad
0\le\phi<1,
\]

the second root remains inside the unit circle while the first root reaches `+1`.

Thus the lower boundary is a nonoscillatory loss of restoring stability.

---

## 2. Exact dominant eigenvalue just inside the stable region

Write

\[
G=G_-+\delta,
\qquad
\delta>0.
\]

In the stable nonoscillatory region, the discriminant becomes

\[
\Delta_J
=(2-\alpha-\phi)^2
-4(1-\phi)\delta.
\]

The dominant real eigenvalue is

\[
\boxed{
\lambda_+
=\frac{
\alpha+\phi
+\sqrt{(2-\alpha-\phi)^2-4(1-\phi)\delta}
}{2}.
}
\]

The exact local damping time is

\[
\boxed{
\tau_{lower}
=-\frac{1}{\log\lambda_+}.
}
\]

---

## 3. Lower-boundary critical slowing

For small `delta`, expand the square root. Then

\[
1-\lambda_+
\sim
\frac{(1-\phi)\delta}{2-\alpha-\phi}.
\]

Therefore

\[
\boxed{
\tau_{lower}
\sim
\frac{2-\alpha-\phi}
{(1-\phi)(G-G_-)}.
}
\]

So a system can show a very long nonoscillatory transient because the restoring loop is only barely stronger than the lower stability threshold.

This mechanism is distinct from the upper-boundary critical slowing associated with strong feedback.

---

## 4. Recovery of the parent haploid result

For the parent model

\[
\alpha=1.
\]

Then

\[
G_-=0
\]

and

\[
2-\alpha-\phi=1-\phi.
\]

Hence

\[
\boxed{
\tau_{lower}
\sim\frac{1}{G}.
}
\]

To leading order, the weak-restoring-feedback timescale is independent of community memory in that special case.

This is separate from the parent branch's upper critical slowing

\[
\tau_{upper}
\sim
\frac{2}{(1-\phi)(1-L)}.
\]

The parent haploid model therefore already contains two conceptually different long-transient limits:

```text
L -> 0+
    weak restoring feedback
    -> slow nonoscillatory return

L -> 1-
    strong feedback near oscillatory instability
    -> slow damped oscillation
```

The generalized response makes the lower boundary visible at `G_-=alpha-1`, which can be negative when `alpha<1`.

---

## 5. Three kinds of feedback-mediated long transient

Combining the parent and generalized layers gives three local transient mechanisms.

### Weak-restoring criticality

\[
G\downarrow G_-.
\]

The dominant real mode approaches `+1`.

### Strong-feedback criticality

\[
G\uparrow G_+.
\]

A conjugate pair approaches the unit circle.

### Long community memory

\[
\phi\uparrow1.
\]

The ecological state itself relaxes slowly and can amplify upper-boundary critical slowing.

These should not be collapsed into one generic statement that "evolution is slow." They correspond to different local mechanisms and different transient geometry.

---

## 6. Structural interpretation

Under the continuous structural lift,

\[
G=-\beta\lambda\Delta g\,e.
\]

Thus increasing the exact finite sensing contrast can move a system away from the lower boundary, through the interior stable region, toward the upper oscillatory boundary.

For fixed `alpha, beta, lambda, e, phi`, the structural gap can therefore affect not only the direction and magnitude of selection but **which critical timescale the coupled system is close to**.

This sharpens the meaning of structural adaptive gain:

> too little effective structural feedback can produce a long weakly restoring transient; intermediate gain gives faster stabilization; sufficiently large gain can create damped oscillation and eventually upper-boundary instability.

---

## 7. Independent numerical audit

For 100,000 random generalized-response models, the lower-boundary asymptotic was audited in the regime

\[
\chi
=\frac{4(1-\phi)(G-G_-)}{(2-\alpha-\phi)^2}
\le10^{-3}.
\]

The maximum absolute deviation of

\[
\tau_{exact}/\tau_{asymptotic}
\]

from one was approximately

\[
4.87\times10^{-4}.
\]

This is a deterministic algebraic validation, not an empirical stochastic claim.

---

## 8. Scope

The result is local, deterministic, and scalar. It does not establish statistical early-warning signals, global nonlinear bifurcations, or empirical critical transitions.

Its role is narrower: after generalizing the evolutionary response, the stable interval has two mathematically distinct boundaries, and both can generate long evolutionary transients for different reasons.
