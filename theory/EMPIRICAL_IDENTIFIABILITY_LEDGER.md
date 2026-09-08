# Empirical identifiability ledger for structural eco-evolutionary feedback

## Status

This note translates the forward/inverse theory into an ordered empirical programme.

It is deliberately **not** a claim that every quantity below is easy to estimate in a natural system. Its purpose is to prevent distinct quantities from being conflated and to show which assumptions enter at which stage.

The core closed-loop identity is

\[
\boxed{
L=(-\eta)\,\Delta s\,p^*(1-p^*)
}
\]

and, only under the continuous structural lift,

\[
\boxed{
\Delta s=\lambda\Delta g,
\qquad
\Delta g=[(C_F-C_A)_+-(C_F-C_A)_-].
}
\]

The empirical programme should therefore proceed in layers rather than infer `Delta_g` immediately from a time series.

---

## 1. Layer T: transient geometry identifies the closed-loop invariants

### Primary observation

A local time series of the evolving phenotype frequency

\[
p_t
\]

near an interior equilibrium.

Work on the logit scale

\[
x_t=\operatorname{logit}(p_t)-\operatorname{logit}(p^*).
\]

Under the local deterministic model,

\[
x_{t+2}
=(1+\phi)x_{t+1}
-[\phi+(1-\phi)L]x_t.
\]

Fitting

\[
x_{t+2}=a_1x_{t+1}+a_2x_t
\]

gives

\[
\boxed{
\phi=a_1-1,
\qquad
L=\frac{-a_2-\phi}{1-\phi}.
}
\]

Equivalent information can come from a local eigenvalue pair or from damping time plus an unaliased oscillation period.

### What this layer identifies

\[
\boxed{\phi,\;L}
\]

### What it does not identify

It does not separate

\[
\eta,\quad\Delta s,\quad\lambda,\quad\Delta g.
\]

---

## 2. Layer E: ecological feedback experiment identifies eta

The forward ecological target is

\[
q_{\rm target}(p)
=q_0+\eta(p-1/2).
\]

A manipulation or natural experiment that changes contingent-architecture frequency while measuring the subsequent high-state community occupancy identifies the slope

\[
\boxed{
\eta=\frac{d q_{\rm target}}{dp}.
}
\]

Examples of what `q` could represent depend on the natural system:

- frequency of a pollinator/visitor regime;
- occupancy of a resource or host state;
- probability of a predator regime;
- prevalence of a community configuration that changes which cue path is useful.

The model requires a clear operational definition of the two recurrent community states before `eta` is meaningful.

### What this layer identifies

\[
\boxed{\eta}
\]

### Important sign test

For the restoring feedback theory developed in the parent branch,

\[
\eta<0.
\]

An empirical positive slope is not a small quantitative discrepancy; it places the system in the non-restoring feedback regime of the model.

---

## 3. Layer P: equilibrium phenotype frequency supplies evolutionary responsiveness

Measure

\[
p^*.
\]

The local response factor is

\[
\boxed{
r=p^*(1-p^*).}
\]

This is largest at intermediate phenotype frequency and shrinks near fixation.

It is not an arbitrary nuisance parameter: the same ecological feedback and selection contrast generate weaker local frequency response near the boundaries.

---

## 4. Layer S: infer selection contrast before invoking structural cost scaling

Once `L`, `eta`, and `p*` have been independently constrained,

\[
\boxed{
\Delta s
=
\frac{L}{(-\eta)p^*(1-p^*)}.
}
\]

This step uses **no** assumption about `lambda` or the finite sensing gap.

It is therefore the first important cross-check.

### Direct fitness test

Independently estimate the state-specific log-fitness contrast between the two sensing architectures:

\[
s_-,\qquad s_+,
\]

and hence

\[
\Delta s_{\rm direct}=s_+-s_-.
\]

The feedback model predicts

\[
\boxed{
\Delta s_{\rm inverse}
=\Delta s_{\rm direct}
}
\]

within sampling/model uncertainty.

If this fails, there is no reason to proceed to structural-gap inference under the current lift.

---

## 5. Layer N: natural history constructs the finite sensing tasks

For each recurrent community state, natural history supplies the feasible information-acquisition graph.

Possible sequence:

```text
long-range detection
-> approach
-> contact
-> handling
-> reward / target discrimination
```

The finite task must state explicitly

- represented worlds/states;
- target partition;
- physically available cues/queries;
- query outcomes;
- cue costs;
- which cues become available only after earlier outcomes/actions.

Then the existing repository mathematics computes

\[
C_A^-,\;C_F^-,\;C_A^+,\;C_F^+
\]

and therefore

\[
\boxed{
\Delta g
=[(C_F-C_A)_+-(C_F-C_A)_-].
}
\]

This is where natural history enters the structural part of the model. It is not inferred from the evolutionary time series.

---

## 6. Layer lambda: calibrate the continuous fitness conversion only after Delta_s and Delta_g exist independently

If the continuous lift is appropriate,

\[
\Delta s=\lambda\Delta g.
\]

Therefore an independently reconstructed structural gap gives

\[
\boxed{
\lambda
=\frac{\Delta s}{\Delta g}.
}
\]

This ordering is important:

```text
bad order:
    assume lambda
    -> infer Delta_g from L
    -> declare structural support

preferred order:
    infer L from dynamics
    + measure eta and p*
    -> infer Delta_s
    -> test Delta_s with direct fitness
    + construct finite task from natural history
    -> compute Delta_g
    -> calibrate/test lambda
```

If one common `lambda` is claimed across multiple state contrasts or systems, the inferred values should agree. Large unexplained variation falsifies the simple common-scaling lift even if each finite task is individually valid.

---

## 7. Alternative hard-budget route avoids lambda

The repository also has a nonlinear hard-budget lift.

For ecological sensing budget/deadline

\[
B,
\]

adaptive-only deterministic resolution occurs exactly when

\[
\boxed{
C_A\le B<C_F.
}
\]

Natural-history candidates for `B` include

- time before a host/prey/partner leaves;
- exposure time before predation risk becomes prohibitive;
- energy available for inspection;
- handling-time ceiling;
- short phenological opportunity window.

If the biological system is fundamentally deadline-gated, this route may be preferable to estimating a universal linear `lambda`.

---

## 8. Structural falsification after factorization

If `lambda` has been independently calibrated, or a structural `Delta_g` has been proposed directly from natural history, the exact finite theory supplies hard checks.

For unit-cost tasks,

\[
\Delta g\in\mathbb Z.
\]

At fixed structural scope,

\[
\boxed{
\Delta g
\le
\min\{m,F_b(n,h)\}-h
}
\]

or, with productive-frontier edge cap `E`,

\[
\boxed{
\Delta g
\le
\min\{m,E,F_b(n,h)\}-h.
}
\]

An inverse-required gap above this ceiling rejects the entire declared sensing scope as the source of the observed loop gain.

A gap below the ceiling is only compatible; it is not an existence proof.

---

## 9. Minimum data packages and what each can establish

### Package A: phenotype time series only

Observations:

- local `p_t` trajectory.

Can identify under the deterministic local model:

\[
\phi,\;L.
\]

Cannot identify biological factorization of `L`.

### Package B: phenotype time series + community response

Add:

- `q_target(p)` slope `eta`;
- equilibrium `p*`.

Can additionally infer:

\[
\Delta s.
\]

This already gives a test against direct fitness measurements.

### Package C: Package B + fitness

Add:

- direct estimates of `s_-` and `s_+`.

Can test the closed-loop factorization before invoking sensing combinatorics.

### Package D: Package C + natural-history sensing graph

Add:

- state-specific finite tasks;
- exact `C_A,C_F` calculations.

Can test:

\[
\Delta s=\lambda\Delta g
\]

or the hard-budget alternative.

This is the first package that directly links observed evolutionary dynamics to the repository's structural sensing theory.

---

## 10. Conditioning warning

The inverse is algebraically identifiable but becomes poorly conditioned at high community memory.

For phenotype-AR(2) coefficient errors

\[
\hat a_1=a_1+\epsilon_1,
\qquad
\hat a_2=a_2+\epsilon_2,
\]

the exact error is

\[
\hat L-L
=-\frac{(1-L)\epsilon_1+\epsilon_2}
{1-\phi-\epsilon_1}.
\]

Thus high `phi` creates a tradeoff:

```text
high community memory
    -> longer and more visible forward transients
    -> worse conditioning of loop-gain inversion
```

Any empirical implementation should therefore report uncertainty propagation rather than only point estimates of `L`.

---

## 11. Claim boundary

This ledger does not provide a statistical estimator for noisy ecological data.

It specifies the deterministic identification logic and the order in which independent evidence should enter.

The proposed empirical logic is deliberately falsification-oriented:

1. recover only the invariants justified by the time series;
2. independently estimate ecological and fitness factors;
3. compare rather than reuse the same data to define both sides of an identity;
4. construct finite sensing tasks from natural history;
5. apply exact structural ceilings as rejection tests.

That sequence is intended to prevent a flexible structural narrative from being fitted post hoc to any observed evolutionary trajectory.
