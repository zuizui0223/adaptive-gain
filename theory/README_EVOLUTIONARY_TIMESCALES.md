# Evolutionary timescale branch

This branch asks how the repository's exact finite sensing structure can generate
rapid short-term evolution that is either retained, reversed, or averaged away
over longer time.

The current hierarchy is

```text
community / natural-history state
        |
        v
finite sensing task
        |
        +--> adaptive continuation -> C_A
        |
        +--> productive frontier  -> C_F
        |
        v
structural opportunity / state-specific selection reward
        |
        v
community-state transition process
        |
        v
reward-weighted temporal modes
        |
        v
short-term burst / reversible fluctuation / long-term trend / stasis
```

The finite-state community Markov layer is now the general temporal model.  The
previous two-state `m,phi` formulas are retained as an analytically transparent
special case.

---

## Read in this order

1. `INFORMATION_MEDIATED_ECO_EVOLUTIONARY_LOOP.md`
   - individual cue sequence -> behavior -> realized interaction -> community;
   - keeps explicit the natural-history links that the combinatorial theorem
     does not infer automatically.

2. `SHARP_STRUCTURAL_EVOLUTIONARY_OPPORTUNITY.md`
   - defines the fitness-free normalized adaptive-only opportunity

     \[
     \Omega=(C_F-C_A)/C_A=C_F/C_A-1;
     \]

   - inherits the exact fixed-`(n,m,b)` maximum

     \[
     \Omega_b^*(n,m)=R_b(n,m)-1;
     \]

   - productive-frontier edge count can cap maximum opportunity, whereas any
     positive frontier-rank cap is extremally vacuous.

3. `STRUCTURAL_SELECTION_TRANSITIONS.md`
   - lifts community-state change into

     \[
     \Delta s
     =\lambda\Delta C_F
     -\lambda\Delta C_A
     -\Delta\kappa;
     \]

   - separates productive-frontier rewiring from adaptive-continuation rewiring.

4. `STRUCTURAL_SELECTION_COLLISION.md`
   - reuses the existing `resource_role_profile_collision()`;
   - same adaptive continuation and same multiset of complete per-resource role
     profiles can still give `C_F=2` versus `3`;
   - therefore weaker marginal cue summaries need not determine selection on
     contingent sensing.

5. `BUDGET_GATED_EVOLUTIONARY_SELECTION.md` and
   `BUDGET_GATED_STRUCTURAL_COLLISION.md`
   - use the exact adaptive-only budget window

     \[
     C_A\le B<C_F
     \]

     directly, avoiding any required linear conversion from sensing cost to
     fitness.

6. `EVOLUTIONARY_RETENTION_SCALING.md`
   - symmetric zero-mean two-state result;
   - for fixed `|phi|<1`, selection activity is `O(H)` while RMS retained
     directional change is `O(sqrt(H))`;
   - hence the retained fraction is `O(H^-1/2)`.

7. `DIRECTIONAL_BIAS_AND_LONG_TERM_ACCUMULATION.md`
   - adds stationary directional bias `m`;
   - any fixed `m!=0` restores `O(H)` directional accumulation;
   - gives the two-state crossover scale for when a weak long-run trend rises
     above correlated fluctuations.

8. `COMMUNITY_SPECTRAL_EVOLUTIONARY_TIMESCALE.md`
   - general finite-community result;
   - uses the Poisson equation to obtain the effective long-run variance
     coefficient `sigma_eff^2`;
   - shows that community persistence affects evolution only through dynamical
     modes onto which structural selection actually projects;
   - therefore raw community mixing time and evolutionary selection timescale
     need not be the same.

9. `PRIOR_ART_ECO_EVOLUTIONARY_TIMESCALES.md`
   - treats fluctuating selection, rapid evolution, stasis, eco-evolutionary
     feedbacks, Markov/covariance scaling, and rate-time issues as prior art;
   - isolates the proposed repository-specific structural bridge.

---

# Four mathematically distinct controls on evolutionary timescale

## 1. Instantaneous structural opportunity

For a nontrivial unit-cost sensing task,

\[
\boxed{
\Omega(X)=\frac{C_F(X)-C_A(X)}{C_A(X)}.
}
\]

This is the adaptive-only budget-window width per unit adaptive effort.  It is
an **instantaneous amplitude generator** supplied by community and natural-history
structure before any particular fitness map is chosen.

The repository's exact extremal theorem gives

\[
\boxed{
\Omega_b^*(n,m)=R_b(n,m)-1.
}
\]

So the finite combinatorics already bound how large state-specific adaptive
opportunity can become.

## 2. State-specific selection reward

Two explicit lifts are retained.

### Continuous cost-value lift

\[
\boxed{
s(X)=\lambda[C_F(X)-C_A(X)]-\kappa.}
\]

The existing decomposition gives

\[
C_F-C_A
=(U-C_A)-(C_U-C_F)-(U-C_U),
\]

so selection can be separated into branch-exclusive opportunity minus external
shortcut discount minus internal union redundancy.

### Hard ecological budget lift

Adaptive-only deterministic success occurs exactly when

\[
\boxed{C_A(X)\le B<C_F(X).}
\]

Possible natural-history meanings of `B` include decision deadlines, energetic
ceilings, exposure time, handling-time limits, or phenological opportunity
windows.

## 3. Community temporal dynamics

Let community state follow a stationary finite Markov chain with transition
matrix `P`, stationary distribution `pi`, and state-specific selection rewards
`s_i`.

The long-run mean direction is

\[
\boxed{
\bar s=\sum_i\pi_i s_i.
}
\]

Centered reward covariance is

\[
\boxed{
\gamma(k)
=\sum_i\pi_i(s_i-\bar s)
[P^k(s-\bar s)]_i.
}
\]

Thus the ecological transition process controls the temporal ordering of
state-specific selection rewards.

## 4. Reward-weighted temporal modes

Solve the Poisson equation

\[
(I-P+\Pi)h=s-\bar s\mathbf1.
\]

The effective long-run variance rate is

\[
\boxed{
\sigma_{\rm eff}^2
=2\langle c,h\rangle_\pi-\langle c,c\rangle_\pi.
}
\]

For zero mean selection, expected absolute activity is `H E_pi|s|` while RMS
retained directional change is asymptotically `sqrt(H) sigma_eff`, so

\[
\boxed{
\mathcal R_H^{RMS}
\sim
\frac{\sigma_{\rm eff}}{E_\pi|s|}H^{-1/2}.
}
\]

For nonzero mean selection, the directional mean rises above correlated
fluctuations near

\[
\boxed{
H_\times\approx\frac{\sigma_{\rm eff}^2}{\bar s^2}.
}
\]

For a reversible chain,

\[
\boxed{
\sigma_{\rm eff}^2
=\sum_r w_r\frac{1+\lambda_r}{1-\lambda_r},
}
\]

where `lambda_r` are community relaxation eigenvalues and `w_r` are the centered
selection-reward projections onto those modes.

This yields the key distinction

\[
\boxed{
\text{community persistence}
\ne
\text{evolutionarily experienced persistence}.
}
\]

A slow ecological mode matters only when the structural reward changes along
that mode.

---

# Two-state model as a special case

For

\[
P=\begin{pmatrix}1-a&a\\b&1-b\end{pmatrix},
\]

we have

\[
\boxed{
m=\frac{a-b}{a+b}},
\qquad
\boxed{
\phi=1-a-b.
}
\]

Then

\[
\sigma_{\rm eff}^2
=\delta^2(1-m^2)\frac{1+\phi}{1-\phi},
\]

and

\[
H_\times
\approx
\frac{1-m^2}{m^2}\frac{1+\phi}{1-\phi}.
\]

So the earlier `m,phi` theory is the one-mode finite-community case, not a
separate model family.

---

# Strongest current exact / executable results

- `payoff_routing_task()` has `(C_A,C_F)=(2,3)` and attains the exact
  `Omega*=1/2` bound for `(n,m,b)=(4,3,2)`;
- the registered higher-order resource collision changes `C_F` from 2 to 3
  while keeping `C_A=2`, adaptive continuation root type, and the multiset of
  per-resource role profiles fixed;
- under either the continuous cost-value lift or the hard-budget lift, that
  structural difference can reverse selection;
- productive-frontier edge count limits maximum normalized opportunity, while a
  positive frontier-rank cap alone does not;
- finite-state Markov covariance formulas match exhaustive community-state path
  enumeration;
- the Poisson long-run variance matches an independent reversible-chain spectral
  decomposition on 500 random models to maximum absolute error
  `1.07e-14`;
- one registered three-state chain has the same transition matrix and equal
  stationary reward variance for two reward vectors, yet slow-mode alignment
  gives `sigma_eff^2=17/3` while fast-mode alignment gives `11/9`;
- therefore the same ecological dynamics can generate very different
  evolutionary timescales solely through reward geometry.

---

# Executable layers

- `adaptive_gain/structural_eco_evolution.py`
- `adaptive_gain/structural_selection_transition.py`
- `adaptive_gain/structural_opportunity_bounds.py`
- `adaptive_gain/budget_gated_selection.py`
- `adaptive_gain/evolutionary_timescale_filter.py`
- `adaptive_gain/directional_retention.py`
- `adaptive_gain/community_markov_selection.py`
- `adaptive_gain/community_spectral_timescale.py`

Key tests:

- `tests/test_structural_eco_evolution.py`
- `tests/test_structural_selection_collisions.py`
- `tests/test_structural_selection_transition.py`
- `tests/test_structural_opportunity_bounds.py`
- `tests/test_budget_gated_selection.py`
- `tests/test_budget_gated_structural_collision.py`
- `tests/test_evolutionary_timescale_filter.py`
- `tests/test_directional_retention.py`
- `tests/test_community_markov_selection.py`
- `tests/test_community_spectral_timescale.py`

Validation receipts include

- `validation/evolutionary_timescale_filter_v1.json`
- `validation/evolutionary_retention_scaling_v1.json`
- `validation/directional_retention_v1.json`
- `validation/structural_selection_transition_v1.json`
- `validation/structural_opportunity_bounds_v1.json`
- `validation/budget_gated_selection_v1.json`
- `validation/budget_gated_structural_collision_v1.json`
- `validation/community_spectral_timescale_v1.json`

---

# Scope boundary

The branch remains theoretical.

It does not claim new Markov-reward theory, fluctuating-selection theory,
eco-evolutionary feedback theory, or macroevolutionary rate theory.  It also does
not yet claim that a natural system realizes the full chain.

A strong biological application still needs evidence for

```text
community state
-> feasible cue graph / finite sensing task
-> structural reward difference
-> behavior / realized interaction
-> community transition process
-> temporally varying selection.
```

Natural history is therefore not decoration at the end of the model.  It is what
identifies both the structural sensing map and the ecological transition process
that feed the mathematics.
