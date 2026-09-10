# Evolutionary timescale branch

This branch connects the repository's exact finite adaptive-gain mathematics to
evolutionary timescales under recurrent community states.

Its current boundary is deliberate:

- **inside this branch:** community states generate sensing tasks and selection
  rewards; a finite stationary community process determines how those rewards
  accumulate through time;
- **not yet inside this branch:** evolved phenotype frequencies changing the
  community transition process itself.  That endogenous eco-evolutionary
  feedback belongs in the next layer.

The hierarchy is

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
structural opportunity / state-specific reward
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

---

# Read in this order

1. `INFORMATION_MEDIATED_ECO_EVOLUTIONARY_LOOP.md`
   - individual cue sequence -> behavior -> realized interaction -> community;
   - marks the natural-history links that the combinatorial theorem does not
     infer automatically.

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
   - lifts a community-state change into

     \[
     \Delta s
     =\lambda\Delta C_F
     -\lambda\Delta C_A
     -\Delta\kappa;
     \]

   - separates productive-frontier rewiring from adaptive-continuation rewiring.

4. `STRUCTURAL_SELECTION_COLLISION.md`
   - reuses the existing `resource_role_profile_collision()`;
   - same adaptive continuation and same complete per-resource role-profile
     multiset can still give `C_F=2` versus `3`;
   - therefore weaker marginal cue summaries need not determine selection on
     contingent sensing.

5. `BUDGET_GATED_EVOLUTIONARY_SELECTION.md` and
   `BUDGET_GATED_STRUCTURAL_COLLISION.md`
   - use the exact adaptive-only ecological feasibility window

     \[
     C_A\le B<C_F
     \]

     directly, without requiring a linear conversion of sensing cost into
     fitness.

6. `EVOLUTIONARY_RETENTION_SCALING.md`
   - transparent two-state zero-mean case;
   - fixed `|phi|<1` gives `O(H)` selection activity but only `O(sqrt(H))` RMS
     directional residue.

7. `DIRECTIONAL_BIAS_AND_LONG_TERM_ACCUMULATION.md`
   - adds stationary directional bias `m`;
   - any fixed `m!=0` restores `O(H)` directional accumulation;
   - derives the two-state trend-emergence crossover horizon.

8. `COMMUNITY_SPECTRAL_EVOLUTIONARY_TIMESCALE.md`
   - general finite-community result;
   - obtains the long-run reward variance rate from the Poisson equation;
   - replaces the one-number `phi` picture by reward-weighted community
     relaxation modes.

9. `STRUCTURAL_REWARD_MODE_ALIGNMENT.md`
   - builds slow-mode and fast-mode reward vectors entirely from existing exact
     repository tasks with gaps `0,1,2`;
   - holds the community transition matrix and reward variance fixed while
     changing only which community contrast carries structural adaptive gain;
   - obtains `sigma_eff^2=17/3` versus `11/9`, a ratio `51/11`.

10. `STRUCTURAL_GAP_CENTERING_AND_STASIS.md`
    - for

      \[
      s_i=\lambda[C_F(i)-C_A(i)]-\kappa,
      \]

      shows that a state-independent maintenance cost changes stationary mean
      selection but leaves centered covariance and `sigma_eff^2` unchanged;
    - critical cost

      \[
      \kappa^*=\lambda E_\pi[C_F-C_A]
      \]

      yields zero long-run directional mean while state-dependent selection
      fluctuations remain active;
    - near the threshold,

      \[
      H_\times\propto|\kappa-\kappa^*|^{-2}.
      \]

11. `PRIOR_ART_ECO_EVOLUTIONARY_TIMESCALES.md`
    - treats fluctuating selection, rapid evolution, stasis, eco-evolutionary
      feedbacks, Markov-reward theory, covariance/spectral scaling, and rate-time
      issues as prior art;
    - isolates the repository-specific structural bridge.

---

# The current general theory

## Axis 1: instantaneous structural opportunity

For a nontrivial unit-cost task,

\[
\boxed{
\Omega(X)=\frac{C_F(X)-C_A(X)}{C_A(X)}.
}
\]

This is the adaptive-only budget-window width per unit adaptive effort.  The
existing extremal theorem gives

\[
\boxed{
\Omega_b^*(n,m)=R_b(n,m)-1.
}
\]

So community and natural-history structure set a sharp upper bound on the
instantaneous opportunity for contingent sensing.

## Axis 2: state-specific structural reward

One continuous lift is

\[
\boxed{
s_i=\lambda[C_F(i)-C_A(i)]-\kappa.}
\]

The repository's existing decomposition gives

\[
C_F-C_A
=(U-C_A)-(C_U-C_F)-(U-C_U),
\]

so the state-specific advantage can be separated into branch-exclusive
opportunity minus external shortcut discount minus internal union redundancy.

A nonlinear alternative uses the exact feasibility condition

\[
\boxed{C_A(i)\le B<C_F(i).}
\]

## Axis 3: finite community dynamics

Let community state follow a stationary finite Markov chain with transition
matrix `P`, stationary distribution `pi`, and reward vector `s`.

Long-run mean selection is

\[
\boxed{
\bar s=E_\pi[s].
}
\]

Centered reward covariance is

\[
\boxed{
\gamma(k)
=\sum_i\pi_i(s_i-\bar s)[P^k(s-\bar s)]_i.
}
\]

The exact finite-horizon cumulative variance is

\[
\boxed{
\operatorname{Var}(S_H)
=H\gamma(0)+2\sum_{k=1}^{H-1}(H-k)\gamma(k).
}
\]

## Axis 4: reward-weighted community timescale

Solve

\[
(I-P+\Pi)h=s-\bar s\mathbf1.
\]

Then

\[
\boxed{
\sigma_{\rm eff}^2
=2\langle c,h\rangle_\pi-\langle c,c\rangle_\pi.
}
\]

For zero mean selection,

\[
\boxed{
\mathcal R_H^{RMS}
\sim
\frac{\sigma_{\rm eff}}{E_\pi|s|}H^{-1/2}.
}
\]

For nonzero mean selection,

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

where `lambda_r` are ecological relaxation eigenvalues and `w_r` are structural
selection-reward projections.

Thus

\[
\boxed{
\text{community persistence}
\ne
\text{evolutionarily experienced persistence}.
}
\]

A slow ecological mode matters only if structural adaptive gain varies along
that mode.

---

# Two-state model is the one-mode special case

For

\[
P=\begin{pmatrix}1-a&a\\b&1-b\end{pmatrix},
\]

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

The earlier persistence/alternation theory is therefore retained as the
analytically transparent one-mode limit of the finite-community theory.

---

# Strongest current exact / executable results

- `payoff_routing_task()` has `(C_A,C_F)=(2,3)` and attains the exact
  `Omega*=1/2` bound for `(n,m,b)=(4,3,2)`;
- higher-order resource co-location can change `C_F` and reverse selection while
  `C_A`, adaptive continuation, and weaker per-resource role summaries stay the
  same;
- productive-frontier edge count limits maximum normalized opportunity, while a
  positive frontier-rank cap alone does not;
- finite-state Markov reward moments match exhaustive state-path enumeration;
- Poisson asymptotic variance matches independent reversible spectral
  decomposition on 500 random models with maximum absolute error `1.07e-14`;
- the same three-state community chain and equal stationary reward variance can
  yield `sigma_eff^2=17/3` or `11/9` depending only on reward-mode alignment;
- those two reward alignments can be generated from existing repository tasks,
  not arbitrary reward vectors;
- a common maintenance cost leaves `sigma_eff^2` invariant while shifting mean
  selection through zero;
- at `kappa*=lambda E_pi[C_F-C_A]`, long-run directional trend vanishes while
  state-dependent selection fluctuations remain active;
- the trend-emergence horizon diverges quadratically as `kappa` approaches that
  threshold.

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
- `adaptive_gain/structural_markov_centering.py`

Key tests include

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
- `tests/test_structural_markov_centering.py`

Validation receipts include

- `validation/evolutionary_timescale_filter_v1.json`
- `validation/evolutionary_retention_scaling_v1.json`
- `validation/directional_retention_v1.json`
- `validation/structural_selection_transition_v1.json`
- `validation/structural_opportunity_bounds_v1.json`
- `validation/budget_gated_selection_v1.json`
- `validation/budget_gated_structural_collision_v1.json`
- `validation/community_spectral_timescale_v1.json`
- `validation/structural_markov_centering_v1.json`

---

# Scope boundary and next layer

This branch remains theoretical and treats community-state dynamics as exogenous.

It does not claim new Markov-reward theory, fluctuating-selection theory,
eco-evolutionary feedback theory, or macroevolutionary rate theory.

A strong biological application still needs evidence for

```text
community state
-> feasible cue graph / finite sensing task
-> structural reward difference
-> behavior / realized interaction
-> community transition process
-> temporally varying selection.
```

The next mathematical layer should make the community transition process depend
on the evolving sensory phenotype itself.  That is where the current

```text
community -> selection -> evolution
```

construction becomes a genuine closed

```text
community -> selection -> evolution -> community
```

eco-evolutionary feedback.
