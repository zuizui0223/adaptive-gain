# Evolutionary timescale branch

This branch asks how the repository's finite sensing structure can generate rapid short-term evolution that is either retained or cancelled over longer time.

Read in this order:

1. `INFORMATION_MEDIATED_ECO_EVOLUTIONARY_LOOP.md`
   - individual cue sequence -> interaction -> community -> structural selection -> evolution;
   - reuses continuation, productive frontier, gain decomposition, and extremal families;
   - exact alternating-community witness for rapid reversible evolution plus long-term stasis.

2. `SHARP_STRUCTURAL_EVOLUTIONARY_OPPORTUNITY.md`
   - defines the fitness-free normalized adaptive-only opportunity

     \[
     \Omega=(C_F-C_A)/C_A=C_F/C_A-1;
     \]

   - inherits the repository's exact fixed-`(n,m,b)` maximum as `Omega*=R_b(n,m)-1`;
   - productive-frontier edge count can cap the maximum opportunity, whereas any positive frontier-rank cap is extremally vacuous;
   - identifies the **within-state amplitude generator**.

3. `EVOLUTIONARY_RETENTION_SCALING.md`
   - promotes the existing partial-sum implementation into the explicit long-timescale theorem;
   - for symmetric zero-mean selection with lag-one correlation `phi`, short-term activity grows as `H` while RMS retained directional change grows as `sqrt(H)` for fixed `|phi|<1`;
   - hence the retained fraction obeys

     \[
     \mathcal R_H^{RMS}\sim\sqrt{\frac{1+\phi}{1-\phi}}H^{-1/2};
     \]

   - identifies the **across-generation temporal retention filter**.

4. `BUDGET_GATED_EVOLUTIONARY_SELECTION.md`
   - uses the exact repository window `C_A <= B < C_F` directly as an adaptive-only ecological success window;
   - provides a nonlinear threshold-fitness alternative to the linear cost-to-fitness map.

5. `STRUCTURAL_SELECTION_COLLISION.md`
   - reuses the existing `resource_role_profile_collision()`;
   - same adaptive continuation and same per-resource role-profile multiset can still give `C_F=2` versus `3`;
   - under midpoint control cost this reverses selection on contingent sensing.

6. `BUDGET_GATED_STRUCTURAL_COLLISION.md`
   - combines that same higher-order collision with the exact adaptive-only budget window;
   - at `B=2`, the `(2,2)` state lets both architectures resolve while the `(2,3)` state lets only the contingent architecture resolve;
   - selection reverses under the shared threshold-fitness model without assigning a linear fitness value to each unit of sensing cost.

7. `STRUCTURAL_SELECTION_TRANSITIONS.md`
   - decomposes a community-state change as

     \[
     \Delta s=\lambda\Delta C_F-\lambda\Delta C_A-\Delta\kappa;
     \]

   - separates fixed/productive-frontier rewiring from adaptive-continuation rewiring;
   - the registered collision isolates a pure frontier-side selection change with `Delta C_A=0`.

8. `PRIOR_ART_ECO_EVOLUTIONARY_TIMESCALES.md`
   - fluctuating selection, eco-evolutionary feedback, rapid evolution, stasis, individual-information-to-community effects, partial-sum covariance scaling, and rate-time issues are treated as prior art;
   - isolates the proposed repository-specific structural bridge.

Executable layers:

- `adaptive_gain/structural_eco_evolution.py`
- `adaptive_gain/structural_selection_transition.py`
- `adaptive_gain/structural_opportunity_bounds.py`
- `adaptive_gain/budget_gated_selection.py`
- `adaptive_gain/evolutionary_timescale_filter.py`
- `tests/test_structural_eco_evolution.py`
- `tests/test_structural_selection_collisions.py`
- `tests/test_structural_selection_transition.py`
- `tests/test_structural_collision_timescale.py`
- `tests/test_structural_opportunity_bounds.py`
- `tests/test_budget_gated_selection.py`
- `tests/test_budget_gated_structural_collision.py`
- `tests/test_evolutionary_timescale_filter.py`
- `tests/test_evolutionary_retention_scaling.py`
- `validation/evolutionary_timescale_filter_v1.json`
- `validation/evolutionary_retention_scaling_v1.json`
- `validation/structural_selection_transition_v1.json`
- `validation/structural_opportunity_bounds_v1.json`
- `validation/budget_gated_selection_v1.json`
- `validation/budget_gated_structural_collision_v1.json`

## The two-axis timescale theory

The branch now separates two orthogonal quantities.

### Axis 1: within-state structural opportunity

\[
\boxed{
\Omega(X)=\frac{C_F(X)-C_A(X)}{C_A(X)}
}
\]

is the adaptive-only budget-window width per unit adaptive effort. Its exact worst-case value at fixed world count, cue count, and query arity is inherited from the repository's sharp ratio theorem:

\[
\boxed{
\Omega^*_b(n,m)=R_b(n,m)-1.
}
\]

This is the **short-term amplitude generator**: it quantifies how much structural room a community state can create for contingent sensing before any particular fitness map is chosen.

### Axis 2: across-generation temporal retention

For a realized selection path,

\[
A_H=\sum_t|s_t|,
\qquad
R_H=\left|\sum_t s_t\right|,
\qquad
\mathcal R_H=R_H/A_H.
\]

For the stationary symmetric sign process `s_t=delta X_t` with `Corr(X_t,X_{t+k})=phi^k`,

\[
A_H=\delta H
\]

but, for fixed `|phi|<1`,

\[
R_H^{RMS}=\delta\sqrt{F_H(\phi)}=O(\sqrt H),
\]

so

\[
\boxed{
\mathcal R_H^{RMS}\sim\sqrt{\frac{1+\phi}{1-\phi}}H^{-1/2}.
}
\]

This is the **long-term retention filter**: selection can remain strong every generation while the fraction retained as directional long-term change vanishes.

The singular endpoints clarify the role of time:

```text
phi = 1   -> perfect persistence, retention fraction = 1
phi = 0   -> independent direction, retention fraction = H^(-1/2)
phi = -1  -> perfect alternation, exact cancellation on even horizons
```

Thus time does not necessarily weaken instantaneous selection. It can instead average away directionally incoherent evolutionary activity.

## Two explicit fitness lifts

The theory keeps two alternatives rather than pretending that one map is universal.

### Continuous cost-value lift

\[
s(X)=\lambda[C_F(X)-C_A(X)]-\kappa,
\]

with `C_A` determined by adaptive continuation structure and `C_F` by the productive frontier.

### Hard ecological budget lift

For a sensing deadline/resource ceiling `B`, exact deterministic resolution success differs only when

\[
\boxed{C_A(X)\le B<C_F(X).}
\]

This model does not require a linear fitness value per unit sensing cost: contingent sensing gets a resolution benefit only when it crosses the ecological feasibility threshold.

## Structural questions now separated

```text
within one community state:
    how much adaptive-only opportunity is structurally possible?
    -> Omega=(C_F-C_A)/C_A
    -> sharp bounded-arity / frontier-edge / frontier-rank theorems

within one realized state:
    why is contingent sensing favoured here?
    -> existing U / C_A / C_F / C_U decomposition
    -> or whether B lies in [C_A,C_F)

between community states:
    why did selection change?
    -> Delta C_F frontier channel
       - Delta C_A continuation channel
       - Delta kappa control channel

across generations:
    why does rapid evolution accumulate or disappear?
    -> signed temporal coherence / retention scaling
```

## Strongest current exact results

- the registered `payoff_routing_task()` has `(C_A,C_F)=(2,3)` and exactly attains the sharp normalized opportunity `Omega*=1/2` for its `(n,m,b)=(4,3,2)` scope;
- the registered higher-order resource collision changes `C_F` from 2 to 3 while keeping `C_A=2`, adaptive continuation root type, and the multiset of per-resource role profiles fixed;
- under the continuous cost-value model, that structural change can reverse selection;
- under the hard-budget model at `B=2`, the same structural change moves the population into an adaptive-only resolution window and also reverses selection;
- under alternating community states, either lift yields nonzero short-term allele-frequency movement but zero retained change after each two-generation cycle at the corresponding midpoint maintenance cost;
- productive-frontier edge count limits the maximum normalized opportunity, while a positive cap on frontier rank alone does not;
- for every fixed `|phi|<1`, stationary zero-mean selection can remain active at `O(H)` while RMS retained directional change is only `O(sqrt(H))`, so the retained fraction vanishes as `H^-1/2`.

The organizing picture is now

```text
community / natural-history structure
        |
        v
instantaneous structural opportunity Omega
        |
        v
state-dependent selection amplitude and sign
        |
        v
temporal retention filter
        |
        v
short-term burst, long-term accumulation, or long-term stasis
```

The burst-versus-stasis conclusion is not tied to one arbitrary linear conversion of sensing cost into fitness.