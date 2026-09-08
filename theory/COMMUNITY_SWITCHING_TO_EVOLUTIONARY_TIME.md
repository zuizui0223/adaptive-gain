# From community switching to evolutionary time

## Status

This note closes the simplest explicit map from ecological/community-state dynamics
to the evolutionary timescale quantities used by this branch.

The Markov-chain algebra is standard. The repository-specific role is to connect
it downstream of community-dependent structural sensing states that generate
opposite selection on contingent versus fixed sensory architectures.

---

## 1. Two community states with opposite selection

Let

```text
X_- : community/sensing state favouring the fixed architecture
X_+ : community/sensing state favouring the contingent architecture
```

with equal-magnitude selection coefficients

\[
-s
\qquad\text{and}\qquad
+s.
\]

The structural collision already registered in the repository provides an exact
minimal example of such a pair under either the continuous cost-value lift or the
hard-budget lift.

Let the community switch according to

\[
a=P(X_{t+1}=X_+\mid X_t=X_-)
\]

and

\[
b=P(X_{t+1}=X_-\mid X_t=X_+).
\]

Assume

\[
a+b>0
\]

so there is a unique stationary occupancy over the two states.

---

## 2. Stationary occupancy determines long-run directional bias

The stationary probability of the positive-selection state is

\[
\boxed{
\pi_+=\frac{a}{a+b}.
}
\]

Similarly,

\[
\pi_-=\frac{b}{a+b}.
\]

Writing the selection sign as

\[
X_t\in\{-1,+1\},
\]

the stationary mean sign is

\[
\boxed{
m=E[X_t]=\pi_+-\pi_-=rac{a-b}{a+b}.}
\]

Therefore the asymptotic retained fraction in the fixed-magnitude sign model is

\[
\boxed{
|m|=rac{|a-b|}{a+b}.
}
\]

This has a direct ecological interpretation:

> long-run directional evolutionary bias is determined by the occupancy imbalance
> between community states favouring opposite sensory architectures.

If

\[
a=b,
\]

then stationary occupancy is balanced and

\[
m=0.
\]

Strong state-specific selection can persist indefinitely without producing a
linear long-term directional trend.

---

## 3. Total switching rate determines temporal coherence

The nontrivial eigenvalue of the two-state transition matrix is

\[
\boxed{
\phi=1-a-b.
}
\]

This is also the lag-one correlation parameter of the centered sign process.

Thus

```text
small a+b  -> phi near +1 -> long residence times / persistent runs
large a+b  -> lower phi   -> faster switching
```

When

\[
a+b>1,
\]

the correlation becomes negative: state switching is more likely than remaining
in the current state.

The same two transition probabilities therefore determine two distinct
long-timescale quantities:

\[
\boxed{
\text{occupancy asymmetry } a-b
\to
m,
}
\]

while

\[
\boxed{
\text{total switching } a+b
\to
\phi.
}
\]

This separation is useful because `m` controls asymptotic directional retention,
whereas `phi` controls finite-horizon coherence around that long-run mean.

---

## 4. Direct community formula for trend-emergence time

The directional-trend crossover in `(m,phi)` coordinates is

\[
H_\times
\approx
\frac{1-m^2}{m^2}
\frac{1+\phi}{1-\phi}.
\]

Substituting

\[
m=\frac{a-b}{a+b},
\qquad
\phi=1-a-b
\]

gives

\[
\boxed{
H_\times
\approx
\frac{4ab(2-a-b)}{(a-b)^2(a+b)}.
}
\]

This is the minimal direct map from community switching to evolutionary trend
emergence time.

If

\[
a=b,
\]

then the denominator vanishes because the long-run directional bias is zero:

\[
\boxed{H_\times=\infty.}
\]

There is no persistent directional trend to emerge.

---

## 5. Occupancy and residence time have different effects

A particularly useful comparison keeps the stationary occupancy fixed while
changing residence time.

Multiply both transition probabilities by a common positive factor `c` while
remaining within `[0,1]`:

\[
(a,b)\mapsto(ca,cb).
\]

Then

\[
\frac{ca-cb}{ca+cb}
=
\frac{a-b}{a+b},
\]

so

\[
m\text{ is unchanged}.
\]

But

\[
\phi'=1-c(a+b)
\]

changes.

For smaller `c`, switching is slower and `phi` is more positive. The system spends
longer uninterrupted runs in each community state while preserving the same
long-run occupancy imbalance.

The crossover horizon increases because correlated short-term bursts create a
larger fluctuation scale around the same weak long-run bias.

Thus two ecological systems can have

```text
the same fraction of evolutionary time in each community state
```

but different

```text
time required for the long-term evolutionary trend to become visible.
```

The difference is residence-time structure, not stationary occupancy.

---

## 6. Connection to short-term rapid evolution

Suppose each state generates large selection magnitude `s` because its sensing
structure strongly favours one architecture.

Then short studies can observe rapid evolution in whichever direction corresponds
to the current state.

The long-term trajectory depends on two additional quantities:

1. **occupancy imbalance**

   \[
   |m|=|a-b|/(a+b),
   \]

   which determines whether one direction wins asymptotically;

2. **residence-time coherence**

   \[
   \phi=1-a-b,
   \]

   which determines how noisy and burst-like the approach to that asymptotic
   trend is.

Therefore

\[
\boxed{
\text{rapid evolution in a short window}
\not\Rightarrow
\text{rapid emergence of a long-term trend}.
}
\]

A system can have large state-specific selection yet require hundreds or thousands
of generations before a small occupancy imbalance becomes distinguishable from
reversible community-driven bursts.

---

## 7. Natural-history meaning

The transition rates `a` and `b` need not refer to abstract environmental states.
They can summarize switches between community configurations that change the
organism's feasible cue graph or productive obligations.

Examples might include transitions between states dominated by

- alternative pollinator guilds;
- alternative host communities;
- predator-rich versus predator-poor interaction contexts;
- seasonal or successional community configurations;
- alternative competitive neighborhoods.

Natural history is needed to justify both

- why the two community states generate different finite sensing structures, and
- what ecological processes determine their switching/residence rates.

The mathematics then supplies a transparent chain

\[
\boxed{
\text{community switching }(a,b)
\to
(m,\phi)
\to
H_\times
\to
\text{evolutionary observation timescale}.
}
\]

---

## 8. Relation to the repository's structural objects

The two-state Markov layer should not hide the upstream mechanism.

For each state

\[
X_-\quad\text{and}\quad X_+,
\]

the repository still requires explicit finite tasks

\[
\mathcal T(X_-),\qquad\mathcal T(X_+).
\]

Their structural differences can be decomposed as

\[
\Delta(C_F-C_A)
=
\Delta C_F-\Delta C_A,
\]

or, inside a state, through the `U/C_A/C_F/C_U` decomposition.

The community transition matrix answers **how often and how persistently** those
selection-generating structures are encountered. It does not replace the
continuation/productive-frontier mechanism.

Thus the full hierarchy is

```text
natural-history cue constraints
        -> finite sensing tasks
        -> continuation / productive frontier
        -> structural opportunity and selection sign
        -> community-state transition matrix
        -> occupancy bias m and coherence phi
        -> trend-emergence horizon H_x
        -> long-term evolutionary pattern
```

---

## 9. Scope boundary

This is a two-state stationary Markov closure with equal-magnitude opposite
selection. It does not yet cover

- more than two community states;
- unequal selection magnitudes among states;
- nonstationary transition matrices;
- endogenous transition rates changed by the evolving phenotype;
- explicit population-density feedbacks;
- mutation, migration, drift, or diploidy;
- lineage diversification or speciation.

The next mathematically meaningful generalization is a finite-state Markov reward
process in which each community state carries a structural selection value derived
from its own `(C_A,C_F)` pair and the long-term accumulation is controlled by the
stationary distribution and spectral structure of the community transition
matrix.
