# Provenance of registered witnesses

The source repositories own the scientific models. `adaptive-gain` copies no runtime code from them and imports none of them.

The finite witnesses in this repository preserve only the decision structure needed to test adaptive-versus-fixed resolution.

## MROD

Source repository: `zuizui0223/mrod`

Relevant source state inspected before extraction:

- commit `6b70671153b24b06f7d6ff4b9f798b423ae81db2`
- `causal_model/adaptive_joint_design.py`
- `causal_model/adaptive_routing_audit.py`
- `causal_model/adaptivity_budget_profile.py`
- `docs/ADAPTIVE_JOINT_DESIGN.md`
- `docs/ADAPTIVITY_BUDGET_PROFILE.md`

Abstracted pattern:

```text
context outcome 0 -> assay0 is the target-relevant continuation
context outcome 1 -> assay1 is the target-relevant continuation
```

The inactive assay's stochastic fair-coin output is represented here by explicit hidden nuisance bits, turning the witness into a deterministic finite hidden-world task without changing its routing logic.

## PAYOFF

Source repository: `zuizui0223/payoff`

Relevant source state inspected before extraction:

- commit `73df815cd24a657994c36d75e9ff14ac2c82c9ef`
- `src/adaptive_phase_design.py`
- `src/adaptivity_budget_profile.py`
- `docs/ADAPTIVE_PHASE_DESIGN.md`
- `docs/ADAPTIVITY_BUDGET_WINDOW.md`

Abstracted pattern:

```text
first intrinsic contrast -> low/high group
low group  -> interaction-distance 0.2 distinguishes phase
high group -> interaction-distance 0.1 distinguishes phase
```

The categorical outcomes in `adaptive_gain/witnesses.py` preserve only this finite separation pattern. They are not a substitute for PAYOFF's quadratic/triangular response formulas, bounded response errors, or continuous-region certification.

## BALANCE

Source repository: `zuizui0223/balance`

Relevant source state inspected before extraction:

- commit `36257a70f5c5e2e332d5f845d8690211834ea41a`
- `balance_domain/budgeted_switching_design.py`
- `balance_domain/adaptivity_budget_profile.py`
- `tests/test_adaptive_allocation_control.py`
- `docs/ADAPTIVITY_NO_GAIN_CONTROL.md`
- `docs/ADAPTIVITY_BUDGET_PROFILE.md`

Abstracted pattern:

For the declared span objective, a midpoint reset query maps both supported branch labels to the same updated span

```text
a(w,e)=min(w,w/2+e).
```

The branch location differs, but the sufficient future-value signature used by the negative control is the same.

## Interpretation rule

The three witnesses are deliberately asymmetric:

```text
MROD   -> positive routing witness
PAYOFF -> positive routing witness
BALANCE-> branch-invariant no-routing witness
```

This asymmetry is the point. The repository is not intended to erase repository-specific scientific assumptions.
