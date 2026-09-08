# Endogenous eco-evolutionary feedback branch

This dependent branch closes the loop left open by the parent evolutionary-timescale branch.

```text
community / natural-history state
        |
        v
exact finite sensing structure
        |
        v
structural reward contrast
        |
        v
evolution of contingent-sensing frequency
        |
        v
phenotype-dependent community occupancy
        |
        +-----------------------------+
```

Read in this order:

1. `ENDOGENOUS_COMMUNITY_FEEDBACK.md`
   - defines the minimal two-community-state feedback model;
   - gives the exact interior equilibrium and Jacobian;
   - shows moderate negative feedback stabilizes the interior state while positive feedback and excessive negative feedback destabilize it.

2. `STRUCTURAL_LOOP_GAIN_PHASE_DIAGRAM.md`
   - compresses local dynamics into

     \[
     L=-\eta\Delta s\,p^*(1-p^*);
     \]

   - proves the exact local phase boundaries

     \[
     0<L<1
     \]

     for stability and

     \[
     L>(1-\phi)/4
     \]

     for damped oscillation within the stable region;
   - maps the repository's exact structural gap contrast directly into the loop gain;
   - turns the `k`-branch and binary extremal routing families into explicit monotone / damped / overshoot phase sequences.

Executable layers:

- `adaptive_gain/endogenous_community_feedback.py`
- `adaptive_gain/feedback_loop_gain.py`
- `tests/test_endogenous_community_feedback.py`
- `tests/test_feedback_loop_gain.py`
- `validation/endogenous_community_feedback_v1.json`
- `validation/feedback_loop_gain_phase_v1.json`

The central structural identity is

\[
\boxed{
L
=-\eta\lambda\Delta g\,p^*(1-p^*)
}
\]

under the continuous structural lift, with

\[
\Delta g
=
[(C_F-C_A)_{high}-(C_F-C_A)_{low}].
\]

At the centered equilibrium `p*=1/2`,

\[
L=-\eta\lambda\Delta g/4.
\]

Thus the same exact finite-task gap that measures static adaptive advantage becomes a dynamical closed-loop gain once the evolving phenotype changes future community state occupancy.

For the `k`-branch family against a gap-zero control,

\[
L_k=-\eta\lambda(k-1)/4.
\]

For the binary family,

\[
L_d=-\frac{\eta\lambda}{4}[2^d-(d+1)].
\]

The branch therefore predicts that increasing structural adaptive advantage can drive a feedback system through

```text
stable nonoscillatory
-> stable damped oscillation
-> overshoot instability
```

without changing the sign of the ecological feedback.

Generic feedback stability, Jury analysis, and damped oscillations are prior art. The repository-specific contribution is the source and exact scaling of `Delta g` from continuation/productive-frontier sensing structure.
