# Evolutionary timescale branch

This branch asks how the repository's finite sensing structure can generate rapid short-term evolution that is either retained or cancelled over longer time.

Read in this order:

1. `INFORMATION_MEDIATED_ECO_EVOLUTIONARY_LOOP.md`
   - individual cue sequence -> interaction -> community -> structural selection -> evolution;
   - reuses continuation, productive frontier, gain decomposition, and extremal families.

2. `SHARP_STRUCTURAL_EVOLUTIONARY_OPPORTUNITY.md`
   - defines the fitness-free normalized adaptive-only opportunity

     \[
     \Omega=(C_F-C_A)/C_A=C_F/C_A-1;
     \]

   - inherits the repository's exact fixed-`(n,m,b)` maximum as `Omega*=R_b(n,m)-1`;
   - productive-frontier edge count can cap the maximum opportunity, whereas any positive frontier-rank cap is extremally vacuous;
   - identifies the **within-state amplitude generator**.

3. `EVOLUTIONARY_RETENTION_SCALING.md`
   - for symmetric zero-mean selection with lag-one correlation `phi`, short-term activity grows as `H` while RMS retained directional change grows as `sqrt(H)` for fixed `|phi|<1`;
   - hence

     \[
     \mathcal R_H^{RMS}\sim\sqrt{\frac{1+\phi}{1-\phi}}H^{-1/2};
     \]

   - identifies the **across-generation temporal retention filter**.

4. `DIRECTIONAL_BIAS_AND_LONG_TERM_ACCUMULATION.md`
   - lets the selection sign have stationary mean `m`;
   - gives

     \[
     E[S_H]=\delta mH,
     \qquad
     \operatorname{Var}(S_H)=\delta^2(1-m^2)F_H(\phi);
     \]

   - proves the RMS retained fraction tends to `|m|` for fixed `|phi|<1`;
   - distinguishes rapid-but-balanced evolution (`m=0`) from persistent long-term trend (`m!=0`).

5. `BUDGET_GATED_EVOLUTIONARY_SELECTION.md`
   - uses the exact repository window `C_A <= B < C_F` directly as an adaptive-only ecological success window;
   - provides a nonlinear threshold-fitness alternative to the linear cost-to-fitness map.

6. `STRUCTURAL_SELECTION_COLLISION.md`
   - reuses the existing `resource_role_profile_collision()`;
   - same adaptive continuation and same per-resource role-profile multiset can still give `C_F=2` versus `3`;
   - under midpoint control cost this reverses selection on contingent sensing.

7. `BUDGET_GATED_STRUCTURAL_COLLISION.md`
   - combines that same higher-order collision with the exact adaptive-only budget window;
   - at `B=2`, the `(2,2)` state lets both architectures resolve while the `(2,3)` state lets only the contingent architecture resolve.

8. `STRUCTURAL_SELECTION_TRANSITIONS.md`
   - decomposes a community-state change as

     \[
     \Delta s=\lambda\Delta C_F-\lambda\Delta C_A-\Delta\kappa;
     \]

   - separates fixed/productive-frontier rewiring from adaptive-continuation rewiring.

9. `PRIOR_ART_ECO_EVOLUTIONARY_TIMESCALES.md`
   - fluctuating selection, eco-evolutionary feedback, rapid evolution, stasis, individual-information-to-community effects, partial-sum covariance scaling, and rate-time issues are treated as prior art;
   - isolates the proposed repository-specific structural bridge.

Executable layers:

- `adaptive_gain/structural_eco_evolution.py`
- `adaptive_gain/structural_selection_transition.py`
- `adaptive_gain/structural_opportunity_bounds.py`
- `adaptive_gain/budget_gated_selection.py`
- `adaptive_gain/evolutionary_timescale_filter.py`
- `adaptive_gain/directional_retention.py`
- `tests/test_structural_eco_evolution.py`
- `tests/test_structural_selection_collisions.py`
- `tests/test_structural_selection_transition.py`
- `tests/test_structural_collision_timescale.py`
- `tests/test_structural_opportunity_bounds.py`
- `tests/test_budget_gated_selection.py`
- `tests/test_budget_gated_structural_collision.py`
- `tests/test_evolutionary_timescale_filter.py`
- `tests/test_evolutionary_retention_scaling.py`
- `tests/test_directional_retention.py`
- `validation/evolutionary_timescale_filter_v1.json`
- `validation/evolutionary_retention_scaling_v1.json`
- `validation/directional_retention_v1.json`
- `validation/structural_selection_transition_v1.json`
- `validation/structural_opportunity_bounds_v1.json`
- `validation/budget_gated_selection_v1.json`
- `validation/budget_gated_structural_collision_v1.json`

## Three mathematically distinct controls on evolutionary timescale

### 1. Instantaneous structural opportunity

\[
\boxed{
\Omega(X)=\frac{C_F(X)-C_A(X)}{C_A(X)}
}
\]

is the adaptive-only budget-window width per unit adaptive effort. Its exact worst-case value is

\[
\boxed{
\Omega^*_b(n,m)=R_b(n,m)-1.
}
\]

This is the **short-term amplitude generator**: community and natural-history structure determine how much opportunity exists for contingent sensing before any fitness map is chosen.

### 2. Temporal coherence

For a zero-mean sign process `s_t=delta X_t` with `Corr(X_t,X_{t+k})=phi^k`,

\[
A_H=\delta H,
\]

but, for fixed `|phi|<1`,

\[
R_H^{RMS}=O(\sqrt H),
\]

and

\[
\boxed{
\mathcal R_H^{RMS}\sim\sqrt{\frac{1+\phi}{1-\phi}}H^{-1/2}.
}
\]

Time does not weaken instantaneous selection here. It averages away directionally incoherent selection.

### 3. Long-run directional bias

If the selection sign has stationary mean `m`, then

\[
\boxed{
E[S_H]=\delta mH
}
\]

and

\[
\boxed{
\frac{\sqrt{E[S_H^2]}}{\delta H}
\to |m|
}
\]

for fixed `|phi|<1`.

Thus

```text
m = 0     -> rapid activity can leave only sublinear long-term residue
m != 0    -> directional change accumulates linearly in the long run
```

The branch therefore separates

\[
\boxed{
\text{selection magnitude}
\ne
\text{selection coherence}
\ne
\text{selection directional bias}.
}
\]

These three quantities answer different biological questions.

## Two explicit fitness lifts

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

This model does not require a linear fitness value per unit sensing cost.

## Questions now separated

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
    how coherent is selection direction?
    -> phi / retention scaling

across long evolutionary time:
    does one direction win on average?
    -> m / directional-bias accumulation
```

## Strongest current exact results

- `payoff_routing_task()` has `(C_A,C_F)=(2,3)` and exactly attains the sharp normalized opportunity `Omega*=1/2` for `(n,m,b)=(4,3,2)`;
- the registered higher-order resource collision changes `C_F` from 2 to 3 while keeping `C_A=2`, adaptive continuation root type, and the multiset of per-resource role profiles fixed;
- under either the continuous cost-value lift or the hard-budget lift, that structural difference can reverse selection;
- under exactly balanced alternating states, allele frequency moves each generation but returns after each two-generation cycle;
- productive-frontier edge count limits maximum normalized opportunity, while a positive frontier-rank cap alone does not;
- for fixed `|phi|<1` and zero mean, selection activity is `O(H)` while RMS retained directional change is `O(sqrt(H))`;
- any fixed nonzero long-run directional bias `m` restores `O(H)` directional accumulation, with asymptotic RMS retained fraction `|m|`.

The organizing picture is

```text
community / natural-history structure
        |
        v
instantaneous structural opportunity Omega
        |
        v
state-dependent selection magnitude and sign
        |
        v
temporal coherence phi
        |
        v
long-run directional bias m
        |
        v
short-term burst, reversible fluctuation, long-term trend, or stasis
```

The branch remains theoretical: natural history must still supply the mappings from ecological state to feasible cue graph, from target resolution to action and realized interaction, and from those interactions back to community state.