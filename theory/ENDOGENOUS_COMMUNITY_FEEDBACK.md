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

## 4. Community state feeds selection back to evolution

Mean selection at occupancy `q_t` is

\[
\boxed{
\bar s_t
=s_-+\Delta s\,q_t.
}
\]

Exact haploid viability selection gives

\[
\boxed{
\operatorname{logit}(p_{t+1})
=\operatorname{logit}(p_t)+\bar s_t.
}
\]

The loop is now closed:

```text
p_t
 -> realized interactions / community target
 -> q_{t+1}
 -> state-dependent structural selection
 -> p_{t+1}
 -> ...
```

---

## 5. Interior equilibrium

An interior evolutionary equilibrium requires zero mean selection:

\[
0=s_-+\Delta s\,q^*.
\]

Therefore

\[
\boxed{
q^*=-\frac{s_-}{\Delta s}.
}
\]

The ecological equilibrium condition is

\[
q^*=q_0+\eta(p^*-1/2).
\]

Hence, for `eta!=0`,

\[
\boxed{
p^*
=\frac12+\frac{q^*-q_0}{\eta}.}
\]

An interior closed-loop equilibrium exists when both `p*` and `q*` lie strictly
inside `[0,1]`.

For the repository-native gap-0/gap-1 pair with

\[
\lambda=1,
\qquad
\kappa=1/2,
\]

we have

\[
s_-=-1/2,
\qquad
s_+=1/2,
\]

so

\[
q^*=1/2.
\]

With `q_0=1/2`, any nonzero feedback slope gives

\[
p^*=1/2.
\]

---

## 6. Exact Jacobian

Use coordinates

\[
z=\operatorname{logit}(p),
\qquad q.
\]

At an interior equilibrium,

\[
\frac{dp}{dz}=p^*(1-p^*).
\]

The exact Jacobian is

\[
\boxed{
J=
\begin{pmatrix}
1 & \Delta s\\
(1-\phi)\eta p^*(1-p^*) & \phi
\end{pmatrix}.
}
\]

Its trace and determinant are

\[
\boxed{T=1+\phi,}
\]

\[
\boxed{
D=\phi
-\Delta s(1-\phi)\eta p^*(1-p^*).
}
\]

The eigenvalues are

\[
\boxed{
r_\pm
=\frac{1+\phi
\pm\sqrt{(1-\phi)^2
+4\Delta s(1-\phi)\eta p^*(1-p^*)}}{2}.
}
\]

This separates ecological memory from feedback sign and strength.

---

## 7. Exact local stability criterion

For a two-dimensional discrete map, the Jury conditions are

\[
1-T+D>0,
\]

\[
1+T+D>0,
\]

\[
1-D>0.
\]

For

\[
\Delta s>0,
\qquad
0\le\phi<1,
\]

and an interior equilibrium, these reduce to

\[
\boxed{
-\frac{1}{\Delta s\,p^*(1-p^*)}
<\eta<0.
}
\]

Therefore:

### Positive feedback

\[
\eta>0
\]

makes the interior equilibrium unstable.

A phenotype that creates more of the community state that favors itself produces
self-reinforcement rather than stabilizing balance.

### Moderate negative feedback

\[
-\frac{1}{\Delta s p^*(1-p^*)}
<\eta<0
\]

stabilizes the interior equilibrium.

The phenotype erodes the ecological condition that favors it, producing a
restoring loop.

### Excessively strong negative feedback

\[
\eta
<-rac{1}{\Delta s p^*(1-p^*)}
\]

is locally unstable in discrete time because the restoring response overshoots.

Thus negative feedback is not automatically stable at arbitrary gain.

---

## 8. Community memory changes transient time, not the stability interval

A notable cancellation occurs in the Jury inequalities.

For the interior structural contrast considered above, the stability interval for
`eta` is independent of `phi` as long as

\[
0\le\phi<1.
\]

But the eigenvalues still depend on `phi`.

Therefore community memory affects

- damping time;
- whether convergence is monotone or oscillatory;
- transient burst duration;

without moving the interior equilibrium or the basic sign boundary between
negative and positive feedback.

For the repo-native gap-0/gap-1 example with

\[
p^*=q^*=1/2,
\quad
\eta=-1,
\]

raising `phi` from `0.2` to `0.8` leaves the equilibrium and stability class
unchanged but increases the dominant eigenvalue modulus, producing much slower
damped convergence.

---

## 9. Existing structural tasks generate the feedback contrast

No arbitrary reward pair is required.

### Low-opportunity state

`routing_bypass_control()` gives

\[
(C_A,C_F)=(2,2),
\]

hence structural gap zero.

### High-opportunity state

`payoff_routing_task()` gives

\[
(C_A,C_F)=(2,3),
\]

hence structural gap one.

At

\[
\lambda=1,
\qquad
\kappa=1/2,
\]

these become exactly

\[
(s_-,s_+)=(-1/2,+1/2).
\]

So the closed-loop equilibrium and stability results are built on existing
repository witnesses.

A larger contrast can be obtained from

`extremal_routing_task(3)` with `(C_A,C_F)=(2,4)`, which makes the upper state
structural gap two.  The executable tests use this to demonstrate that sufficiently
strong negative feedback can cross the discrete-time overshoot boundary.

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
- ecological memory producing damped transients.

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
