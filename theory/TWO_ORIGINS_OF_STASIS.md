# Two origins of stasis: cancellation versus restoration

## Claim boundary

This note does **not** claim that fluctuating selection can generate stasis, nor that stable feedback equilibria are novel. Both are standard ideas.

The purpose is narrower: the eco-evolutionary synthesis in this repository contains two mechanisms that can both produce little long-run net change, and they must not be collapsed into one category.

The exact local distinction is

\[
\boxed{
\text{cancellation stasis: neutral one-cycle map}
\qquad\neq\qquad
\text{restoring stasis: attractive fixed-point map}.
}
\]

---

## 1. Cancellation stasis

Use the additive weak-selection coordinate already used by the evolutionary-timescale filter,

\[
z_{t+1}=z_t+E\beta_t,
\]

with evolvability `E >= 0`.

For a periodic selection cycle of length `P`,

\[
(\beta_0,\ldots,\beta_{P-1}),
\]

the one-cycle map is

\[
F_P(z)
=
z+E\sum_{t=0}^{P-1}\beta_t.
\]

If

\[
\sum_{t=0}^{P-1}\beta_t=0,
\]

then

\[
\boxed{F_P(z)=z\quad\text{for every }z.}
\]

Therefore the one-cycle derivative is exactly

\[
\boxed{F_P'(z)=1.}
\]

A perturbation `delta z` is not repaired. After any number of complete cycles it remains `delta z`.

Yet within-cycle evolutionary activity can be large:

\[
A_P=E\sum_t|\beta_t|.
\]

For example, the family

\[
(M,-M)
\]

has

\[
A_2=2EM
\]

with zero retained net change for arbitrarily large `M`.

Thus cancellation stasis is

\[
\boxed{
\text{large movement + zero period drift + neutral perturbation retention}.
}
\]

This exact identity statement is stronger than merely saying that the long-run average selection is zero.

---

## 2. Restoring stasis

Now consider the endogenous eco-evolutionary feedback model near an interior fixed point. Let `J` be the local Jacobian.

If every eigenvalue lies strictly inside the unit disk,

\[
\rho(J)=\max_i|\lambda_i|<1,
\]

then the fixed point is locally asymptotically attractive:

\[
\boxed{
\|\delta y_t\|\to0
}
\]

for sufficiently small perturbations.

Hence restoring stasis is not cancellation of externally imposed signed increments. The state itself generates a return tendency.

Two local subtypes remain useful:

- **monotone restoring candidate**: stable non-negative real eigenvalues;
- **oscillatory restoring stasis**: a stable non-real conjugate eigenpair.

The latter is especially important because, in the generalized response model, a complex local eigenpair also eliminates every zero-feedback decomposition; see `FEEDBACK_EXISTENCE_FROM_OSCILLATION.md`.

---

## 3. Same net change, different period maps

The two mechanisms may both satisfy

\[
\text{long-run net change}\approx0,
\]

but they are dynamically inequivalent.

### Cancellation

\[
F_P=\mathrm{Id},
\qquad
\text{period multiplier}=1.
\]

Perturbations survive.

### Restoration

\[
\rho(J)<1.
\]

Perturbations decay.

Therefore

\[
\boxed{
\text{zero net change does not define a unique stasis mechanism.}
}
\]

The distinction is neutral versus attractive dynamics, not merely low versus high evolutionary rate.

---

## 4. Relation to the four-pillar paper structure

This theorem sharpens Pillar C of `MAIN_ECO_EVOLUTIONARY_CLAIM.md`.

The four main lines remain:

1. structural selection amplitude and temporal recurrence are generated on the same ecological state space;
2. finite sensing extremal bounds cap attainable structural selection and reachable dynamical phases;
3. cancellation stasis and restoring stasis are distinct because their return maps have different stability structure;
4. oscillatory local dynamics create a qualitative feedback-existence window.

The present note concerns only item 3.

---

## 5. Scope

The cancellation theorem uses the additive weak-selection coordinate

\[
z_{t+1}=z_t+E\beta_t.
\]

It is **not** claimed for arbitrary nonlinear evolutionary maps.

The restoring theorem is local: it classifies behavior from the Jacobian around an interior fixed point. It does not establish global convergence, global bifurcation structure, mutation-selection balance, or stochastic persistence.

No novelty is claimed for identity period maps, Floquet multipliers, spectral-radius stability, or contraction theory. The candidate contribution is their explicit separation inside the same information-structured eco-evolutionary framework.
