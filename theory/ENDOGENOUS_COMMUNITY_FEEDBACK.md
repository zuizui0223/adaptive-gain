# Endogenous community feedback closes the eco-evolutionary loop

## Status

This note is the first layer in which evolution changes the ecological transition
process that generates its own future selection.

The generic fact that negative eco-evolutionary feedback can stabilize an
interior state is not new.  The repository-specific contribution is that the
selection contrast between community states is supplied by exact finite sensing
structure through `C_A` and `C_F`.

This note is intentionally based on the evolutionary-timescale branch rather than
merged into it.  The parent branch treats community transitions as exogenous;
this dependent layer makes them phenotype-dependent.

The local phase structure implied by this model is developed separately in
`STRUCTURAL_LOOP_GAIN_PHASE_DIAGRAM.md`, where the exact structural gap contrast
is shown to enter the closed loop through the dimensionless gain

\[
L=-\eta\Delta s\,p^*(1-p^*)
=-\eta\lambda\Delta g\,p^*(1-p^*)
\]

under the continuous structural lift.

---

## 1. Two recurrent community states

Let

\[
q_t\in[0,1]
\]

be the population-level occupancy/probability of a high-opportunity community
state at generation `t`.

Let

\[
p_t\in[0,1]
\]

be the frequency of a heritable contingent sensory architecture.

The low and high community states carry state-specific structural selection
rewards

\[
s_-,\qquad s_+,
\]

which can be generated from finite sensing tasks as

\[
s_\pm
=\lambda[C_F^\pm-C_A^\pm]-\kappa.
\]

Write

\[
\Delta s=s_+-s_-.
\]

---

## 2. Evolution changes the community state it will later experience

Define the phenotype-dependent target occupancy

\[
\boxed{
q_{target}(p)
=q_0+\eta(p-1/2).
}
\]

The parameter `eta` is the eco-evolutionary feedback slope.

- `eta<0`: increasing contingent-sensing frequency reduces the future prevalence
  of the community state that favors it;
- `eta>0`: increasing contingent-sensing frequency increases the prevalence of
  the state that favors it.

Natural history decides the sign.  Examples could involve altered visitation,
predation, host use, resource depletion, competitive release, or other realized
interaction changes.

The global parameter range is restricted so

\[
0\le q_{target}(p)\le1
\quad\forall p\in[0,1].
\]

---

## 3. Community memory supplies ecological relaxation

Let

\[
0\le\phi<1
\]

be ecological memory.

The mean community update is

\[
\boxed{
q_{t+1}
=\phi q_t
+(1-\phi)q_{target}(p_t).
}
\]

Equivalently, for fixed `p`, the two-state transition matrix has stationary
high-state occupancy `q_target(p)` and nonstationary eigenvalue `phi`.

Thus

- `phi` controls how slowly ecology catches up to the current evolved phenotype;
- `eta` controls how the target ecology itself changes with phenotype frequency.

These are different mechanisms.

---

## 4. Community state selects among sensing architectures

At occupancy `q_t`, the mean log-fitness advantage of the contingent architecture
is

\[
\boxed{
s(q_t)=s_-+(s_+-s_-)q_t.}
\]

The exact haploid update is

\[
\boxed{
\operatorname{logit}(p_{t+1})
=
\operatorname{logit}(p_t)+s(q_t).
}
\]

So the current community state alters evolution, while the current evolved
frequency alters the community state it will experience later.

The update is simultaneous in the current state `(p_t,q_t)`:

```text
current state (p_t, q_t)
    |                  |
    |                  +--> q_target(p_t) --> q_{t+1}
    |
    +--> s(q_t) --> p_{t+1}

next state (p_{t+1}, q_{t+1})
```

Thus the ecological update uses `p_t`, not `p_{t+1}`.  The closed loop appears
across successive generations because the updated phenotype frequency enters the
next ecological update.

---

## 5. Interior equilibrium

Assume

\[
\Delta s=s_+-s_-\ne0.
\]

Selection vanishes when

\[
\boxed{
q^*=-\frac{s_-}{\Delta s}.
}
\]

An interior equilibrium requires

\[
0<q^*<1.
\]

The ecological fixed-point condition is

\[
q^*=q_0+\eta(p^*-1/2).
\]

If

\[
\eta\ne0,
\]

then

\[
\boxed{
p^*=\frac12+\frac{q^*-q_0}{\eta}.}
\]

An interior eco-evolutionary equilibrium exists only when

\[
0<p^*<1.
\]

For symmetric state rewards

\[
s_-=-s_+
\]

and

\[
q_0=1/2,
\]

we obtain the centered equilibrium

\[
\boxed{p^*=q^*=1/2.}
\]

---

## 6. Exact local Jacobian

Use

\[
z=\operatorname{logit}(p)
\]

so the evolutionary update is additive.

At an interior equilibrium,

\[
\frac{dp}{dz}=p^*(1-p^*).
\]

The Jacobian in coordinates `(z,q)` is

\[
\boxed{
J=
\begin{pmatrix}
1 & \Delta s\\
(1-\phi)\eta p^*(1-p^*) & \phi
\end{pmatrix}.
}
\]

Its trace is

\[
T=1+\phi,
\]

and its determinant is

\[
D
=\phi
-\Delta s(1-\phi)\eta p^*(1-p^*).
\]

---

## 7. Exact local stability condition

For the characteristic polynomial

\[
\lambda^2-T\lambda+D,
\]

the discrete-time Jury conditions are

\[
1-T+D>0,
\]

\[
1+T+D>0,
\]

\[
1-D>0.
\]

Assume

\[
\Delta s>0,
\qquad
0\le\phi<1.
\]

Substitution gives

\[
1-T+D
=-(1-\phi)\Delta s\eta p^*(1-p^*).
\]

Hence positive feedback

\[
\eta>0
\]

immediately violates the restoring condition.

For negative feedback, the remaining upper stability bound is

\[
1-D>0
\]

which gives

\[
\boxed{
-\frac{1}{\Delta s\,p^*(1-p^*)}
<\eta<0.
}
\]

Thus

```text
eta > 0
    positive feedback
    -> interior equilibrium locally unstable

-1/[Delta_s p*(1-p*)] < eta < 0
    moderate negative feedback
    -> interior equilibrium locally stable

eta = -1/[Delta_s p*(1-p*)]
    -> L=1 oscillatory unit-circle boundary

eta < -1/[Delta_s p*(1-p*)]
    stronger negative feedback
    -> oscillatory instability
```

The stability interval does **not** depend on `phi` as long as

\[
0\le\phi<1.
\]

Community memory changes transient damping, oscillation period, and the route to
the boundary, but not the local negative-feedback stability interval itself.

---

## 8. Repository-native minimal witness

Use the existing tasks

- `routing_bypass_control()` with

  \[
  C_A=C_F=2;
  \]

- `payoff_routing_task()` with

  \[
  C_A=2,
  \qquad
  C_F=3.
  \]

Under

\[
\lambda=1,
\qquad
\kappa=0.5,
\]

we get

\[
s_-=-0.5,
\qquad
s_+=+0.5.
\]

Therefore

\[
q^*=0.5.
\]

With

\[
q_0=0.5,
\]

the interior equilibrium is

\[
p^*=q^*=0.5.
\]

For

\[
\eta=-1,
\]

we have

\[
-4<\eta<0,
\]

so the equilibrium is locally stable.

The executable simulation converges back to the centered state from displaced
initial conditions.

For

\[
\eta=+0.5,
\]

the same structural reward contrast creates positive feedback and the interior
state is unstable.

Thus the sign of the ecological feedback, not the existence of structural
adaptive gain itself, decides whether the closed loop restores or amplifies a
perturbation.

---

## 9. Stronger structural contrast narrows the stabilizing feedback range

The stability interval is

\[
-\frac{1}{\Delta s\,p^*(1-p^*)}
<\eta<0.
\]

For fixed equilibrium frequency, larger

\[
\Delta s
\]

makes the lower bound less negative.

So increasing the structural selection contrast makes the closed system more
sensitive to feedback instability.

Under the continuous structural lift,

\[
\Delta s
=\lambda
\left(
[(C_F-C_A)_+]
-[(C_F-C_A)_-]
\right).
\]

The repository's extremal adaptive-gain families can therefore be interpreted as
families that amplify eco-evolutionary feedback sensitivity.

For example, comparing a gap-zero control with the `k`-branch family gives

\[
\Delta s=\lambda(k-1).
\]

At

\[
p^*=1/2,
\]

stability requires

\[
\boxed{
-\frac{4}{\lambda(k-1)}<\eta<0.
}
\]

As `k` grows, the stable negative-feedback interval shrinks toward zero.

The complete transient and oscillatory-instability phase diagram is developed in
`STRUCTURAL_LOOP_GAIN_PHASE_DIAGRAM.md`.

---

## 10. Natural-history interpretation

The sign of `eta` is an empirical natural-history question.

Examples of possible negative feedback:

- a sensory architecture improves exploitation of one resource state and thereby
  depletes that state;
- improved predator detection changes habitat use in a way that reduces future
  exposure to the predator regime that selected for it;
- pollinator behavior changes plant reproduction and gradually reduces the flower
  phenotype/community configuration that favored that behavior.

Examples of possible positive feedback:

- preferential visitation increases reproduction of the plant state that most
  rewards that same sensory strategy;
- habitat choice reinforces the biotic state that makes the chosen cue pathway
  valuable.

The mathematics does not decide which mechanism is real.  It identifies the
qualitative evolutionary consequences once natural history supplies the feedback
sign and magnitude.

---

## 11. Relation to short-term burst versus long-term evolution

The parent branch showed that exogenous community switching can produce

- large instantaneous structural opportunity;
- strong state-specific selection;
- little long-term directional accumulation when rewards balance.

The present feedback layer adds a new mechanism for that balance:

\[
\boxed{
\text{evolution can change ecology so that its own mean selection is driven back toward zero.}
}
\]

Under moderate negative feedback, the long-run balanced state is dynamically
attracting rather than externally imposed.

This makes long-term stasis or stable polymorphism compatible with strong
short-term evolutionary movement without assuming that the external environment
happens to alternate symmetrically forever.

---

## 12. Prior-art boundary

The following are not claimed as new:

- negative eco-evolutionary feedback stabilizing coexistence or polymorphism;
- positive feedback generating runaway or threshold behavior;
- Jacobian/Jury stability analysis of two-dimensional maps;
- ecological memory producing damped transients;
- unit-circle instability algebra for discrete two-dimensional maps.

The repository-specific contribution is the upstream source of the selection
contrast:

```text
community state
-> exact finite sensing task
-> (C_A,C_F)
-> structural reward contrast
-> endogenous eco-evolutionary feedback.
```

This layer is still a minimal deterministic mean-field model.  It does not yet
include demographic stochasticity, multiple species' evolving traits, mutation,
migration, or stochastic observation likelihoods.
