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
    -> lower / upper feedback timescale
    -> structurally permitted transient-time envelope
```

Read in this order:

1. `GENERAL_EVOLUTIONARY_RESPONSE.md`
   - derives the generalized local Jacobian;
   - gives exact stability and oscillation thresholds;
   - recovers the parent haploid-logit model as an exact special case;
   - shows intrinsic evolutionary damping can stabilize a finite amount of reinforcing ecological feedback.

2. `GENERAL_RESPONSE_BOUNDARY_TIMESCALES.md`
   - separates the two stability boundaries;
   - lower `G_-=alpha-1`: real eigenvalue approaches `+1`, producing slow nonoscillatory return;
   - upper `G_+=(1-alpha*phi)/(1-phi)`: conjugate pair approaches the unit circle, producing slow damped oscillation;
   - derives distinct critical-slowing laws near both boundaries.

3. `GENERAL_RESPONSE_STRUCTURAL_PHASE_BOUNDS.md`
   - reuses the existing bounded-arity / productive-frontier gap ceiling;
   - maps it into a generalized gain ceiling

     \[
     G_{max}=(-\beta e)\lambda\,\Delta g_{max}
     \]

     for restoring `e<0`;
   - certifies damped oscillation impossible when `G_max<=G_osc`;
   - certifies upper instability impossible when `G_max<G_+`;
   - shows the same finite sensing scope can exclude a phase under one evolutionary response and fail to exclude it under another.

4. `GENERAL_RESPONSE_TRANSIENT_CEILINGS.md`
   - uses unit-cost structural-gap integrality;
   - identifies the first integer gap entering the generalized damped region and the largest integer gap remaining below `G_+`;
   - converts those envelopes into class-wide upper bounds on stable damping time and oscillation period;
   - recovers the parent transient ceiling exactly at `alpha=1`;
   - shows the same sensing scope can have different time ceilings after changing only evolutionary persistence.

Executable layers:

- `adaptive_gain/general_evolutionary_response.py`
- `adaptive_gain/general_response_boundary_timescales.py`
- `adaptive_gain/general_response_structural_bounds.py`
- `adaptive_gain/general_response_transient_bounds.py`
- `tests/test_general_evolutionary_response.py`
- `tests/test_general_response_boundary_timescales.py`
- `tests/test_general_response_structural_bounds.py`
- `tests/test_general_response_transient_bounds.py`
- `validation/general_evolutionary_response_v1.json`
- `validation/general_response_boundary_timescales_v1.json`
- `validation/general_response_structural_bounds_v1.json`
- `validation/general_response_transient_ceiling_v1.json`

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
G_-:=\alpha-1
<G<
G_+:=\frac{1-\alpha\phi}{1-\phi}.
}
\]

The damped-oscillation threshold is

\[
\boxed{
G>
G_{osc}:=
\frac{(\alpha-\phi)^2}{4(1-\phi)}.
}
\]

Thus

```text
G_- < G <= G_osc
    stable nonoscillatory return

G_osc < G < G_+
    stable damped oscillation
```

The parent haploid-logit model is the exact special case

\[
\alpha=1,
\quad
\beta=1,
\quad
e=\eta p^*(1-p^*),
\]

which gives

\[
G=L,
\quad G_-=0,
\quad G_+=1,
\quad G_{osc}=(1-\phi)/4.
\]

When

\[
\alpha<1,
\]

weak reinforcing feedback can remain stable:

\[
\boxed{\alpha-1<G<0.}
\]

So the parent conclusion that any positive ecological feedback destabilizes the interior state is specific to `alpha=1`.

Under the continuous structural lift,

\[
\boxed{G=-\beta\lambda\Delta g\,e.}
\]

The original continuation/productive-frontier mathematics therefore remains upstream; the generalized response changes how structural selection is converted into dynamics.

## Two distinct critical-slowing limits

### Lower weak-restoring boundary

\[
\boxed{
\tau_{lower}
\sim
\frac{2-\alpha-\phi}
{(1-\phi)(G-G_-)}.
}
\]

For `alpha=1`,

\[
\boxed{\tau_{lower}\sim1/G.}
\]

### Upper strong-feedback boundary

\[
\boxed{
\tau_{upper}
\sim
\frac{2}{(1-\phi)(G_+-G)}.
}
\]

Long-lived evolutionary transients can therefore arise for opposite reasons:

```text
too little effective restoring gain
    -> slow nonoscillatory relaxation near G_-

large gain near the upper feedback boundary
    -> slow damped oscillation near G_+
```

## Structural scope no longer determines phase or timescale by itself

For the minimal four-world scope `(n,m,b,h)=(4,3,2,2)`, the inherited gap ceiling is one. With generalized gain per gap `0.125` and `phi=0.5`, the gain ceiling is `0.125`.

For `alpha=1`, `G_osc=0.125`, so the whole scope is certified nonoscillatory.

For `alpha=0.7`, `G_osc=0.02`, so the same scope admits a damped integer gap. Because gap one is the only positive structural step, the resulting class-wide bounds are approximately

\[
\tau_{damp}\le2.25856
\]

and

\[
T\le17.22412
\]

generations.

For the larger `(12,12,2,3)` scope with gap ceiling four and gain/gap `0.125` at `phi=0.5`:

- parent `alpha=1`: first damped gap 2, max stable gap 4, `tau<=6.95212`, `T<=19.52813`;
- generalized `alpha=0.8`: first damped gap 1, max stable gap 4, `tau<=4.64271`, `T<=21.04927`.

Therefore

\[
\boxed{
\text{finite sensing structure constrains the gain ladder, while response geometry sets both phase and transient-time boundaries.}
}
\]

Independent validation includes 200,000 random phase checks with zero stability/oscillation mismatches, 100,000 upper-boundary critical-slowing checks, 100,000 lower-boundary checks, 200,000 integer-envelope checks with zero gap-envelope mismatches, parent special-case recovery tests, and direct structural-bound examples.

Prior-art boundary: local linearization, 2x2 Jury stability, generic response coefficients, critical slowing, integer-envelope optimization, and composition of upper bounds are standard. The repository-specific contribution is the exact finite sensing gap entering generalized eco-evolutionary gain and the resulting structural phase/time-exclusion logic.
