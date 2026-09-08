# Evolutionary timescale branch

This branch asks how the repository's finite sensing structure can generate rapid short-term evolution that is either retained or cancelled over longer time.

Read in this order:

1. `INFORMATION_MEDIATED_ECO_EVOLUTIONARY_LOOP.md`
   - individual cue sequence -> interaction -> community -> structural selection -> evolution;
   - reuses continuation, productive frontier, gain decomposition, and extremal families;
   - exact alternating-community witness for rapid reversible evolution plus long-term stasis.

2. `PRIOR_ART_ECO_EVOLUTIONARY_TIMESCALES.md`
   - fluctuating selection, eco-evolutionary feedback, rapid evolution, stasis, and rate-time issues are treated as prior art;
   - isolates the proposed repository-specific structural bridge.

Executable layers:

- `adaptive_gain/structural_eco_evolution.py`
- `adaptive_gain/evolutionary_timescale_filter.py`
- `tests/test_structural_eco_evolution.py`
- `tests/test_evolutionary_timescale_filter.py`
- `validation/evolutionary_timescale_filter_v1.json`

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
