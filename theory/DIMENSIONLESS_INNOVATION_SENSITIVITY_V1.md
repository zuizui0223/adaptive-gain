# Dimensionless correlation sensitivity within the exact evoTS OUBM congruence gauge

## Mathematical result
Under the reciprocal two-state realization, with `q=a/alpha` and source
trait/optimum process variance rates `v_x>0` and `v_o>0`, the innovation
covariance is

```
Q11 = v_x
Q12 = -(1-q)*v_x/q
Q22 = ((1-q)^2 * v_x + v_o)/q^2.
```

The instantaneous innovation correlation is

`rho(q)=-(1-q)/sqrt((1-q)^2+v_o/v_x)`.

If **independent biological information** supports `|rho|<=rho_max<1`, then

`1-q <= rho_max*sqrt(v_o/[v_x(1-rho_max^2)]) = delta_max`.

If `delta_max<1`, the sharp family-specific half-life bound is

`H_OU <= H_direct <= H_OU/(1-delta_max)`.

If `delta_max>=1`, the correlation cap supplies **no finite upper bound** on
`H_direct` in this family. In particular the critical correlation is

`rho_critical = sqrt(v_x/(v_x+v_o))`.

This is a dimensionless counterpart of the earlier absolute `|Q12|<=C`
sensitivity bound, which is scale-dependent on the hidden state's physical units.

## Biological and inferential restrictions
- This is a *partial-identification/sensitivity* analysis, not a fitted estimate.
- The bound applies to the exact **two-state moving-optimum** reciprocal gauge,
  not arbitrary multivariate, phylogenetic, or nonlinear models.
- A physical interpretation of `rho` requires external definition of what the
  hidden Y variable actually measures. Since `Y=(Theta-(1-q)X)/q` mixes a
  latent optimum and observed trait, an unanchored correlation cap is as much a
  modelling restriction as the earlier absolute covariance cap.
- Do not apply the formula naively to `v_o=0` fixed-optimum boundary: for
  `q<1` and positive trait noise, the constructed fixed-OU reciprocal gauge
  has **perfectly anticorrelated innovations** (|rho|=1). A stipulated
  non-perfect innovation correlation would exclude that witness.
- The conventional OU observation-law relaxation rate and its half-life remain
  valid *conditional on the fitted stochastic model*. The bound concerns the
  direct response coefficient's biological attribution.

## Empirical use
Report both `H_OU` and either a biologically justified hidden covariance
bound (`C`) or innovation correlation cap (`rho_max`), with clear state
definitions. If neither can be justified, use the unbounded identified set
rather than asserting a uniquely identified direct selection response time.
