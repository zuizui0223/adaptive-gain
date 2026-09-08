# General evolutionary-response branch

This dependent branch removes the parent feedback model's specific haploid-logit evolutionary update and keeps only local response derivatives.

```text
finite sensing structure
    -> exact structural gap Delta_g
    -> selection contrast Delta_s=lambda*Delta_g
    -> local evolutionary responsiveness beta
    -> ecological effect slope e
    -> generalized loop gain G=-beta*Delta_s*e
    -> local eco-evolutionary phase
```

Read `GENERAL_EVOLUTIONARY_RESPONSE.md` for the derivation.

Executable layer:

- `adaptive_gain/general_evolutionary_response.py`
- `tests/test_general_evolutionary_response.py`
- `validation/general_evolutionary_response_v1.json`

The generic local map is

\[
x_{t+1}=F(x_t,s(q_t)),
\qquad
q_{t+1}=\phi q_t+(1-\phi)Q(x_t).
\]

At equilibrium define

\[
\alpha=\partial_xF,
\qquad
\beta=\partial_sF,
\qquad
e=Q'(x^*).
\]

Then

\[
\boxed{
J=\begin{pmatrix}
\alpha & \beta\Delta s\\
(1-\phi)e & \phi
\end{pmatrix}
}
\]

and

\[
\boxed{G=-\beta\Delta s\,e.}
\]

For

\[
0\le\alpha\le1,
\qquad
0\le\phi<1,
\]

local stability is exactly

\[
\boxed{
\alpha-1
<G<
\frac{1-\alpha\phi}{1-\phi}.
}
\]

The damped-oscillation threshold is

\[
\boxed{
G>
\frac{(\alpha-\phi)^2}{4(1-\phi)}.
}
\]

The parent haploid-logit model is the exact special case

\[
\alpha=1,
\qquad
\beta=1,
\qquad
e=\eta p^*(1-p^*),
\]

which gives

\[
G=L,
\qquad
0<L<1,
\qquad
L>(1-\phi)/4
\]

for damped oscillation.

The important qualitative change is that when

\[
\alpha<1,
\]

weak reinforcing feedback can remain stable:

\[
\boxed{
\alpha-1<G<0.
}
\]

Intrinsic evolutionary damping can therefore buffer positive ecological feedback. The parent conclusion that any positive feedback destabilizes the interior state is specific to `alpha=1`.

Under the continuous structural lift,

\[
\boxed{
G=-\beta\lambda\Delta g\,e.
}
\]

so the original continuation/productive-frontier mathematics still supplies the upstream selection contrast. The generalized response layer changes only the conversion from structural selection to local evolutionary dynamics.

At the upper stability boundary

\[
G_+=\frac{1-\alpha\phi}{1-\phi},
\]

the conjugate pair reaches the unit circle with

\[
\cos\theta_c=(\alpha+\phi)/2.
\]

Near that boundary,

\[
\boxed{
\tau_{damp}
\sim
\frac{2}{(1-\phi)(G_+-G)}.
}
\]

Thus the parent critical-slowing result also survives after removing the specific haploid update.

Prior-art boundary: local linearization, 2x2 Jury stability, and generic response coefficients are standard. The repository-specific contribution is the structural sensing gap entering the generalized eco-evolutionary gain, and the exact identification of which parent conclusions survive or change when the evolutionary update is generalized.
