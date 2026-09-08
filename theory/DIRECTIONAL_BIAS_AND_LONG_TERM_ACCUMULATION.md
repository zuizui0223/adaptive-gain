# Directional bias separates long-term accumulation from fluctuating stasis

## Status

The moment identities in this note are standard for stationary correlated sign
processes. The repository does not claim them as new probability theory.

Their role is to complete the evolutionary-timescale interpretation downstream
of the repository's structural selection generator.

The zero-mean result in `EVOLUTIONARY_RETENTION_SCALING.md` explains how strong
short-term activity can leave only an `O(sqrt(H))` directional residue. This note
asks the complementary question:

> what changes when selection has even a small persistent directional bias?

The answer is sharp: a nonzero mean restores `O(H)` long-term directional
accumulation.

---

## 1. Fixed-magnitude selection with biased sign

Let

\[
s_t=\delta X_t,
\qquad \delta>0,
\qquad X_t\in\{-1,+1\}.
\]

Assume a stationary sign process with

\[
E[X_t]=m,
\qquad -1\le m\le1,
\]

and geometric autocovariance

\[
\operatorname{Cov}(X_t,X_{t+k})
=(1-m^2)\phi^k.
\]

For a two-state ergodic Markov sign process, `phi` is the nontrivial temporal
eigenvalue and controls correlation decay.

The cumulative selection is

\[
S_H=\sum_{t=1}^Hs_t.
\]

---

## 2. Mean accumulation is linear whenever m is nonzero

By stationarity,

\[
\boxed{
E[S_H]=\delta mH.
}
\]

Thus any fixed directional bias

\[
m\ne0
\]

creates a linear-in-time expected displacement.

The short-term absolute activity remains

\[
A_H=\delta H.
\]

Therefore the ratio of expected signed accumulation to total activity is simply

\[
\frac{E[S_H]}{A_H}=m.
\]

The long-term directional bias is not set by the instantaneous magnitude `delta`;
`delta` scales both activity and accumulation. The key quantity is the imbalance
between how often selection points in one direction versus the other.

---

## 3. Fluctuations remain only O(sqrt(H)) for finite correlation time

Using the same partial-sum factor

\[
F_H(\phi)
=H+2\sum_{k=1}^{H-1}(H-k)\phi^k,
\]

the cumulative variance is

\[
\boxed{
\operatorname{Var}(S_H)
=\delta^2(1-m^2)F_H(\phi).
}
\]

For fixed

\[
|\phi|<1,
\]

we have

\[
F_H(\phi)=O(H),
\]

so the stochastic fluctuation scale is

\[
\sqrt{\operatorname{Var}(S_H)}=O(\sqrt H).
\]

Meanwhile the mean directional component is

\[
|E[S_H]|=\delta|m|H.
\]

Therefore every fixed nonzero `m` eventually dominates the correlated
fluctuations.

---

## 4. RMS retained fraction converges to |m|

Because

\[
E[S_H^2]
=E[S_H]^2+\operatorname{Var}(S_H),
\]

we obtain

\[
E[S_H^2]
=\delta^2
\left[
 m^2H^2+(1-m^2)F_H(\phi)
\right].
\]

Normalize the RMS directional residue by total activity `delta H`:

\[
\boxed{
\mathcal Q_H
=
\frac{\sqrt{E[S_H^2]}}{\delta H}
=
\sqrt{
 m^2+(1-m^2)\frac{F_H(\phi)}{H^2}
}.
}
\]

For every fixed

\[
-1<\phi<1,
\]

\[
\boxed{
\lim_{H\to\infty}\mathcal Q_H=|m|.
}
\]

So the asymptotic retained fraction has a simple interpretation:

> it is the absolute long-run directional bias of selection.

Temporal autocorrelation controls finite-horizon variance and the speed of
convergence, but a persistent nonzero mean controls whether directional change
accumulates linearly at all.

---

## 5. The zero-mean case is qualitatively different

If

\[
m=0,
\]

then

\[
\mathcal Q_H
=
\frac{\sqrt{F_H(\phi)}}{H}
\sim
\sqrt{\frac{1+\phi}{1-\phi}}H^{-1/2},
\]

for `|phi|<1`.

Thus

\[
\boxed{
m=0\Rightarrow\text{retained fraction vanishes},}
\]

whereas

\[
\boxed{
m\ne0\Rightarrow\text{retained fraction approaches }|m|.}
\]

This gives the minimal analytical distinction between

```text
rapid but directionally balanced evolution
    -> long-term stasis / bounded-looking trajectories

rapid evolution with persistent directional bias
    -> long-term directional accumulation
```

without changing the per-generation selection magnitude.

---

## 6. How community structure can create or erase m

The repository's structural layer provides a concrete source of state-dependent
selection.

For example, under the continuous cost-value lift,

\[
s(X)=\lambda[C_F(X)-C_A(X)]-\kappa.
\]

Under the hard-budget lift, the sign can change depending on whether

\[
B\in[C_A(X),C_F(X)).
\]

If community states occur with stationary frequencies `pi_x`, then the long-run
mean selection is

\[
\bar s=\sum_x\pi_x s(X).
\]

For a two-sign reduction with fixed magnitude `delta`, this corresponds to

\[
m=\bar s/\delta.
\]

Therefore a community transition can alter long-term evolutionary regime in two
separable ways:

1. change the **instantaneous structural opportunity** within states;
2. change the **stationary occupancy imbalance** among states that favour
   opposite selection directions.

The first controls how strongly selection can act. The second controls whether
those episodes cancel or accumulate directionally.

---

## 7. Connection to the higher-order cue collision

The registered resource-role collision gives two states with

\[
(C_A,C_F)=(2,2)
\]

and

\[
(C_A,C_F)=(2,3),
\]

while preserving adaptive continuation root type and the multiset of complete
per-resource role profiles.

At midpoint control cost, these states can generate equal-and-opposite selection.

If their long-run occupancy is exactly balanced,

\[
m=0,
\]

so long-term retained fraction vanishes for finite correlation time and cancels
exactly under deterministic alternation.

If the high-opportunity state is occupied slightly more often, then

\[
m>0,
\]

and the same system crosses into linear long-term accumulation.

Thus the distinction between short-term burst and long-term trend can depend not
only on the existence of strong structural selection states but on their
**occupancy asymmetry through time**.

---

## 8. Timescale interpretation

The combined theory now has three distinct temporal roles.

### Within an individual episode

Temporal predictability can route the next useful cue. Both positive and negative
predictability can help.

### Across ecological/community states

Community transitions change continuation structure, productive frontier, and
therefore state-specific structural opportunity and selection.

### Across evolutionary time

The long-run mean sign `m` determines whether directional change is retained
linearly, while `phi` controls finite-horizon coherence around that mean.

This yields the hierarchy

\[
\boxed{
\text{selection magnitude}
\ne
\text{selection coherence}
\ne
\text{selection directional bias}.
}
\]

All three can matter, but they answer different questions.

---

## 9. Scope boundary

This note assumes fixed-magnitude selection and geometric sign autocovariance.
It does not yet model

- state-dependent selection magnitudes beyond the sign reduction;
- nonstationary community occupancy;
- feedback from allele frequency to transition probabilities;
- drift, mutation, migration, or diploidy;
- quantitative-trait covariance dynamics;
- speciation or lineage diversification.

The purpose is to isolate the simplest analytical condition under which rapid
short-term selection changes from a reversible fluctuation into a persistent
long-term evolutionary trend.
