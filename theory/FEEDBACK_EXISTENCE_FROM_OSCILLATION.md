# Feedback existence from oscillatory transients

## Status

This note sharpens the generalized local identifiability layer.

It does **not** identify the magnitude of eco-evolutionary feedback from a scalar transient. Instead, it asks the weaker qualitative question:

> can the observed local trajectory establish that nonzero feedback must exist at all?

For the generalized two-state response model, the answer depends sharply on whether the observed local eigenvalues are real or complex.

The generalized response domain used by the parent theory is

\[
0\le\alpha\le1,
\qquad
0\le\phi<1.
\]

The distinction between `alpha<=1` and `phi<1` matters at the neutral boundary and is kept explicit below. Because `T=alpha+phi`, at least one persistence split exists exactly when

\[
0\le T<2.
\]

---

## 1. Generalized characteristic invariants

The local Jacobian is

\[
J=
\begin{pmatrix}
\alpha & *\\
* & \phi
\end{pmatrix},
\]

with characteristic invariants

\[
T=\alpha+\phi,
\]

\[
D=\alpha\phi+(1-\phi)G.
\]

For every candidate community memory \(\phi<1\), the compatible gain is

\[
\boxed{
G(\phi)
=
\frac{D-T\phi+\phi^2}{1-\phi}.
}
\]

The numerator is exactly the characteristic polynomial evaluated at \(\phi\):

\[
\boxed{
D-T\phi+\phi^2
=\chi_J(\phi).
}
\]

This elementary identity yields a useful qualitative corollary.

---

## 2. Real nonnegative eigenvalues: stable monotone return does not identify feedback existence

Suppose the two local eigenvalues are real and satisfy

\[
0\le r_1,r_2<1.
\]

Then

\[
\chi_J(r_1)=\chi_J(r_2)=0.
\]

Choose

\[
\phi=r_1,
\qquad
\alpha=r_2.
\]

Both persistence parameters are feasible and

\[
\boxed{G=0.}
\]

Therefore

\[
\boxed{
\text{a stable monotone transient with nonnegative real modes cannot by itself establish feedback existence.}
}
\]

The same scalar transient is compatible with a no-feedback decomposition obtained by assigning the two observed roots to intrinsic evolutionary persistence and community persistence.

This is stronger than saying that feedback magnitude is not identified: under these conditions even the proposition \(G\ne0\) is not identified.

### Model-feasible neutral boundary

The parent model allows `alpha=1` but still requires `phi<1`. Therefore the no-feedback construction extends one step beyond the asymptotically stable statement. If the ordered real roots satisfy

\[
0\le r_1<1,
\qquad
0\le r_2\le1,
\]

then choosing

\[
\phi=r_1,
\qquad
\alpha=r_2
\]

is model-feasible and gives `G=0`. In particular, `r_2=1` is an allowed **neutral** boundary case. It is not asymptotically stable return, so it should not be used to broaden the stable-monotone corollary itself.

A double unit root is not feasible under this assignment because it would require `phi=1`, which is excluded.

### Scope of the real-root statement

Real transients with a negative mode are outside this particular nonnegative-persistence construction and must be treated separately.

---

## 3. Complex eigenvalues: positive feedback is forced only after model compatibility

Suppose the eigenvalues are a non-real conjugate pair. Then the discriminant is negative:

\[
T^2-4D<0.
\]

The quadratic

\[
q(\phi)=\phi^2-T\phi+D
\]

has no real root and, because its leading coefficient is positive,

\[
q(\phi)>0
\]

for every real \(\phi\). Thus for every real `phi<1`, the algebraic compatible gain is positive.

To turn that statement into a conclusion **within the generalized response model**, require at least one admissible persistence split. Since `T=alpha+phi`, this is exactly

\[
0\le T<2.
\]

Conditional on that model-compatibility requirement, every feasible community memory has positive denominator `1-phi` and therefore

\[
\boxed{
G(\phi)>0
\quad\text{for every model-feasible decomposition.}
}
\]

Hence

\[
\boxed{
\text{a model-compatible local oscillatory transient forces the existence of positive feedback.}
}
\]

If `T<0` or `T>=2`, the observed transient is outside the declared persistence domain. The correct conclusion is then **model incompatibility**, not feedback existence. This avoids treating a universal statement over an empty feasible-decomposition set as biological evidence.

The magnitude of \(G\) remains unidentified unless one persistence parameter is measured independently, but its sign/existence is no longer free once compatibility is established.

---

## 4. Exact gain infimum over the unit memory interval

The public executable helper also reports

\[
\inf_{0\le\phi<1}G(\phi).
\]

This helper optimizes over the unit community-memory interval itself and does not additionally constrain the implied `alpha=T-phi`. It therefore should not silently inherit the Schur-stable or model-compatibility assumptions of the main corollary. Let

\[
R=1-T+D,
\qquad
x=1-\phi.
\]

Then `0<x<=1` and

\[
G
=\frac{R}{x}+(T-2)+x.
\]

Therefore

\[
\boxed{
\inf_{0\le\phi<1}G(\phi)
=
\begin{cases}
-\infty,&R<0,\\
T-2,&R=0,\\
T-2+2\sqrt R,&0<R\le1,\\
D,&R>1.
\end{cases}
}
\]

The `R=0` value is an infimum approached as `phi->1-`; it is not attained because `phi=1` is excluded. For `R>1`, the infimum is attained at `phi=0`. For `0<R<=1`, it is attained at the stationary point `phi=1-sqrt(R)`.

This piecewise result matters for software correctness even though the main model-compatible oscillatory corollary uses a regime in which `R>0` and the gain infimum is positive.

---

## 5. Interpretation for stasis versus oscillation

This creates an asymmetry between two superficially similar long-lived regimes.

### Monotone return / stasis-like trajectory

If the local eigenvalues are real, nonnegative, and asymptotically stable, a zero-feedback decomposition remains available.

Therefore monotone return cannot distinguish among, for example,

- intrinsic evolutionary persistence;
- community persistence;
- nonzero coupled feedback.

### Oscillatory return

A model-compatible complex eigenpair cannot be generated by the same diagonal no-feedback decomposition with real persistence parameters.

Therefore oscillation is not merely a nuisance pattern. Within this model class it is a qualitative identification window:

\[
\boxed{
\text{oscillation identifies feedback existence even when feedback magnitude remains unidentified.}
}
\]

This does **not** mean that all biological oscillations imply this specific sensing mechanism. It means that, conditional on the generalized two-state local response model and its persistence domain, oscillatory local dynamics rule out the zero-feedback member of the compatible decomposition family.

---

## 6. Relation to the main timescale question

The broader theory distinguishes two sources of stasis-like behavior:

1. **exogenous temporal cancellation** — recurrent selection has large short-term activity but near-zero long-run directional mean, so retained change grows much more slowly than cumulative activity;
2. **endogenous restoring feedback** — the coupled eco-evolutionary system returns toward an interior equilibrium.

The present corollary adds an identification asymmetry:

- monotone endogenous return can be observationally indistinguishable from a no-feedback decomposition;
- model-compatible damped oscillatory return cannot.

This result is diagnostic support for the paper's principal reachability theorem, not a competing principal theorem.

---

## 7. Prior-art boundary

No novelty is claimed for

- the characteristic polynomial identity;
- the fact that a real-root quadratic vanishes at its eigenvalues;
- the positivity of a monic quadratic with negative discriminant;
- elementary one-variable minimization of the compatible-gain expression;
- generic interpretations of complex eigenvalues as damped oscillation.

The repository-specific contribution is the consequence these elementary facts have for the exact eco-evolutionary decomposition

\[
D=\alpha\phi+(1-\phi)G
\]

that sits downstream of the finite sensing-gap theory.

---

## 8. Claim boundary

This note does not claim

- that oscillation uniquely identifies the microscopic sensing architecture;
- that all real ecological/evolutionary systems are two-dimensional;
- that every observed `(T,D)` lies inside the declared persistence domain;
- that process noise cannot generate apparent oscillation;
- global nonlinear feedback identification;
- finite-sample statistical tests for complex versus real local eigenstructure.

It is an exact local deterministic corollary inside the generalized response model, conditional on model compatibility before mechanistic inference.
