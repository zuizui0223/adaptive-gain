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

   - proves exact local phase boundaries: stability for `0<L<1`, damped oscillation for `L>(1-phi)/4` inside that interval, and an oscillatory unit-circle boundary at `L=1`;
   - maps the repository's exact structural gap contrast directly into loop gain;
   - turns the `k`-branch and binary extremal routing families into explicit nonoscillatory / damped / unstable phase sequences.

3. `STRUCTURAL_PHASE_EXCLUSION_BOUNDS.md`
   - reuses the parent bounded-arity theorem

     \[
     C_F\le\min\{m,F_b(n,h)\}
     \]

     to bound the maximum possible loop gain in a finite sensing scope;
   - adds the productive-frontier edge cap

     \[
     C_F\le\min\{m,E,F_b(n,h)\};
     \]

   - provides rigorous one-sided certificates that damped oscillation or strong-feedback instability are structurally impossible under declared world/query/arity/frontier constraints;
   - keeps frontier-rank caps out of the certificate because the parent repository already proves positive rank caps are extremally vacuous.

4. `CRITICAL_SLOWING_OF_ECO_EVOLUTIONARY_FEEDBACK.md`
   - derives the exact damping time in the stable damped phase,

     \[
     \tau_{\rm damp}
     =-\frac{2}{\log[1-(1-\phi)(1-L)]};
     \]

   - gives the critical-slowing law

     \[
     \tau_{\rm damp}
     \sim\frac{2}{(1-\phi)(1-L)};
     \]

   - shows the unit-circle critical period scales as

     \[
     T_c\sim\frac{2\pi}{\sqrt{1-\phi}};
     \]

   - separates a slowly damped stable transient from both genuine long-run directional accumulation and recurrent zero-mean selection fluctuations.

Executable layers:

- `adaptive_gain/endogenous_community_feedback.py`
- `adaptive_gain/feedback_loop_gain.py`
- `adaptive_gain/feedback_structural_bounds.py`
- `tests/test_endogenous_community_feedback.py`
- `tests/test_feedback_loop_gain.py`
- `tests/test_feedback_structural_bounds.py`
- `validation/endogenous_community_feedback_v1.json`
- `validation/feedback_loop_gain_phase_v1.json`
- `validation/feedback_structural_bounds_v1.json`
- `validation/feedback_critical_slowing_v1.json`

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
-> oscillatory unit-circle instability
```

without changing the sign of ecological feedback.

It also predicts that dynamics can remain visible for a very long time while the equilibrium is still stable. Near the feedback boundary or long-memory limit,

```text
long transient duration
~ 1 / [(1-community memory)*(distance from loop-gain boundary)].
```

This is a third evolutionary-timescale mechanism alongside the parent branch's long-run directional trend and zero-mean recurrent fluctuation.

Conversely, inherited finite-structure bounds can rule phases out before a particular task is constructed. In the executable API, `possible=False` is the strong conclusion: the declared structural scope cannot reach that phase under the stated feedback parameters. `possible=True` means only that the upper bound does not exclude it.

Generic feedback stability, Jury analysis, damped oscillations, unit-circle crossing algebra, critical slowing, and finite-state bifurcation tools are prior art. The repository-specific contribution is the source and exact scaling of `Delta g` from continuation/productive-frontier sensing structure, plus the resulting phase boundaries, phase-exclusion certificates, and structurally parameterized transient timescale.
