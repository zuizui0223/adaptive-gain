# Structural gap centering: rapid selection with long-term stasis

## Status

This note derives a simple but useful consequence of combining the repository's
exact structural gap with the finite-community Markov timescale layer.

The algebra of subtracting a constant reward is elementary.  The repository-
specific content is that the state-dependent raw reward is supplied by the exact
adaptive/fixed sensing gap

\[
g_i=C_F(i)-C_A(i).
\]

---

## 1. Structural reward with a constitutive maintenance cost

Let community state `i` carry the exact structural gap

\[
g_i=C_F(i)-C_A(i)\ge0.
\]

Under the continuous cost-value lift,

\[
\boxed{
s_i=\lambda g_i-\kappa,}
\]

where

- `lambda>=0` converts structural sensing advantage into log-fitness units;
- `kappa>=0` is a state-independent constitutive cost of maintaining contingent
  sensory control.

Let the stationary community distribution be `pi`.

Define

\[
\bar g=\sum_i\pi_i g_i.
\]

Then stationary mean selection is

\[
\boxed{
\bar s=\lambda\bar g-\kappa.
}
\]

---

## 2. Critical maintenance cost

Selection is directionally centered exactly when

\[
\bar s=0.
\]

Therefore

\[
\boxed{
\kappa^*=\lambda\bar g
=\lambda E_\pi[C_F-C_A].
}
\]

This is the constitutive-cost threshold separating

```text
kappa < kappa*  -> contingent architecture has positive long-run mean selection
kappa = kappa*  -> long-run directional mean is zero
kappa > kappa*  -> fixed architecture has positive long-run mean selection
```

The threshold depends on stationary occupancy of structurally different
community states, not only on any one state in isolation.

---

## 3. Maintenance cost does not change fluctuation geometry

Center the reward:

\[
s_i-\bar s
=
\lambda g_i-\kappa-(\lambda\bar g-\kappa).
\]

Hence

\[
\boxed{
s_i-\bar s=\lambda(g_i-\bar g).}
\]

The common maintenance cost cancels exactly.

Therefore every centered covariance satisfies

\[
\boxed{
\gamma_s(k)=\lambda^2\gamma_g(k),
}
\]

and the Poisson long-run variance rate obeys

\[
\boxed{
\sigma_{\rm eff}^2(s)
=\lambda^2\sigma_{\rm eff}^2(g),
}
\]

independently of `kappa`.

So a state-independent constitutive cost can change the long-run evolutionary
direction without changing the temporal structure of short-term selection
fluctuations.

---

## 4. Exact mechanism for rapid evolution plus long-term stasis

At

\[
\kappa=\kappa^*,
\]

we have

\[
\bar s=0,
\]

but if the structural gap differs among community states,

\[
\sigma_{\rm eff}^2(s)>0
\]

can remain strictly positive.

Thus

\[
\boxed{
\text{long-run directional trend}=0
}
\]

while

\[
\boxed{
\text{state-dependent selection fluctuations remain active}.
}
\]

This is the general finite-community version of the earlier alternating
`+s,-s` witness.

The stasis does not arise because selection becomes weak.  It arises because the
constitutive cost centers the occupancy-weighted structural benefit while
community switching continues to expose the lineage to different structural
selection states.

---

## 5. Trend-emergence time diverges near the threshold

The general community crossover scale is

\[
H_\times
\approx
\frac{\sigma_{\rm eff}^2(s)}{\bar s^2}.
\]

Using the identities above,

\[
\boxed{
H_\times
\approx
\frac{\lambda^2\sigma_{\rm eff}^2(g)}
{(\lambda\bar g-\kappa)^2}.
}
\]

Since

\[
\kappa^*=\lambda\bar g,
\]

this becomes

\[
\boxed{
H_\times
\approx
\frac{\lambda^2\sigma_{\rm eff}^2(g)}
{(\kappa-\kappa^*)^2}.
}
\]

Therefore

\[
\boxed{
H_\times\propto|\kappa-\kappa^*|^{-2}.
}
\]

A system can have a genuine directional bias and still look fluctuation-
dominated for a very long time when maintenance cost lies close to the critical
value.

---

## 6. Repository-native three-state witness

Use existing tasks with exact gaps

```text
routing_bypass_control()   -> g=0
payoff_routing_task()      -> g=1
extremal_routing_task(3)   -> g=2
```

and the common stationary distribution

\[
\pi=(1/3,1/3,1/3).
\]

Then

\[
\bar g=1.
\]

For `lambda=1`,

\[
\boxed{
\kappa^*=1.
}
\]

The reward vector at the threshold is

\[
\boxed{
s=(-1,0,1).
}
\]

Its stationary mean is exactly zero, but its state-to-state variation is
nonzero and the registered community transition matrix gives positive
asymptotic fluctuation variance.

Moving to

\[
\kappa=1\pm\varepsilon
\]

changes the stationary mean to

\[
\bar s=\mp\varepsilon
\]

without changing `sigma_eff^2` at all.

Consequently halving `|epsilon|` multiplies the asymptotic trend-emergence
horizon by exactly four.

---

## 7. Biological interpretation

The same community can support large state-specific benefits of contingent
sensing while the architecture remains approximately neutral in the long run if
its constitutive maintenance cost nearly matches the occupancy-weighted average
benefit.

This separates two questions that are often conflated:

```text
How much selection happens from generation to generation?
    -> structural heterogeneity + community switching

Which architecture wins over long time?
    -> occupancy-weighted mean benefit - constitutive cost
```

A lineage can therefore show rapid repeated evolutionary response without a
clear long-term direction even in a perfectly stationary community regime.

---

## 8. Relation to natural history

The threshold becomes biologically interpretable only when the ingredients are
measured.

Natural history must identify

- which recurrent community states create different feasible cue tasks;
- their state-specific `C_A` and `C_F` analogues or empirically calibrated noisy
  counterparts;
- the long-run occupancy of those states;
- the constitutive cost of maintaining contingent sensory machinery.

The theory predicts that changing state occupancy can move the critical cost
threshold even if the cue machinery itself does not change.

---

## 9. Prior-art boundary

No novelty is claimed for constant reward shifts, covariance centering, or the
quadratic divergence of a signal-to-noise crossover near a zero mean.

The repository-specific contribution is the exact source of the state-dependent
raw benefit:

\[
g_i=C_F(i)-C_A(i),
\]

including its existing continuation/frontier decomposition and sharp finite
bounds.
