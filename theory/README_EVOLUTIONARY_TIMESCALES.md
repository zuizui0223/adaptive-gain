# Evolutionary timescale branch

This branch asks how the repository's finite sensing structure can generate rapid short-term evolution that is either retained or cancelled over longer time.

Read in this order:

1. `INFORMATION_MEDIATED_ECO_EVOLUTIONARY_LOOP.md`
   - individual cue sequence -> interaction -> community -> structural selection -> evolution;
   - reuses continuation, productive frontier, gain decomposition, and extremal families;
   - exact alternating-community witness for rapid reversible evolution plus long-term stasis.

2. `STRUCTURAL_SELECTION_COLLISION.md`
   - reuses the existing `resource_role_profile_collision()`;
   - same adaptive continuation and same per-resource role-profile multiset can still give `C_F=2` versus `3`;
   - under midpoint control cost this reverses selection on contingent sensing.

3. `STRUCTURAL_SELECTION_TRANSITIONS.md`
   - decomposes a community-state change as

     \[
     \Delta s=\lambda\Delta C_F-\lambda\Delta C_A-\Delta\kappa;
     \]

   - separates fixed/productive-frontier rewiring from adaptive-continuation rewiring;
   - the registered collision isolates a pure frontier-side selection change with `Delta C_A=0`.

4. `PRIOR_ART_ECO_EVOLUTIONARY_TIMESCALES.md`
   - fluctuating selection, eco-evolutionary feedback, rapid evolution, stasis, and rate-time issues are treated as prior art;
   - isolates the proposed repository-specific structural bridge.

Executable layers:

- `adaptive_gain/structural_eco_evolution.py`
- `adaptive_gain/structural_selection_transition.py`
- `adaptive_gain/evolutionary_timescale_filter.py`
- `tests/test_structural_eco_evolution.py`
- `tests/test_structural_selection_collisions.py`
- `tests/test_structural_selection_transition.py`
- `tests/test_structural_collision_timescale.py`
- `tests/test_evolutionary_timescale_filter.py`
- `validation/evolutionary_timescale_filter_v1.json`
- `validation/structural_selection_transition_v1.json`

Core distinction:

\[
\text{short-term activity}=\sum_t|s_t|,
\qquad
\text{long-term retained change}=\left|\sum_t s_t\right|.
\]

The structural selection coefficient in the minimal cost-fitness model is

\[
s(X)=\lambda[C_F(X)-C_A(X)]-\kappa,
\]

with `C_A` determined by adaptive continuation structure and `C_F` by the productive frontier.

The branch therefore distinguishes two questions:

```text
within one community state:
    why is contingent sensing favoured?
    -> existing U / C_A / C_F / C_U decomposition

between community states:
    why did selection change?
    -> Delta C_F frontier channel
       - Delta C_A continuation channel
       - Delta kappa control channel
```

The strongest current exact witness combines both levels: higher-order resource co-location changes `C_F` while leaving adaptive continuation and marginal per-resource role profiles unchanged, producing reversible short-term evolution but zero retained change under alternating community states.