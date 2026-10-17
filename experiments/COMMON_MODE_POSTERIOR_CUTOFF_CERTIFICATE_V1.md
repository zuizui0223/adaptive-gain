# Exact posterior-odds cutoff across the entire error-correlation interval

**Status:** finite benchmark-specific supplementary lemma to PR #68. This strengthens the tabulated cutoff checks in `JOINT_READOUT_CORRELATION_AUDIT_V1.md`; it is not a general theorem about sensory coding, an empirical bee finding, or MAIN 4.

## Statement and boundary

Keep topology A of the existing five-world example: targets `(0,1,1,0,0)`, cue vectors root `(0,0,1,1,0)`, left `(0,1,0,0,0)`, right `(0,0,0,1,0)`, prior `(1/3,1/6,1/6,1/6,1/6)`, at most **two** unit-cost queries, per-query flip probability `epsilon=1/10`, reward `v>0`, wrong-choice penalty `L>=0`, and free abstention.

Mix independently flipped error vectors (weight `1-rho`) with a completely shared flip vector (weight `rho`); each cue has the same 10% marginal error for every rho. Let `R_star(rho)` be the maximum posterior odds in favor of any target after any affordable fixed cue subset and observed outcome pattern, including no cue.

The **exact** cutoff is

\[
\boxed{R_{\star}(\rho)=\frac{14+\rho}{1-\rho}\quad(0\le\rho<1),\qquad R_\star(1)=\infty.}
\]

For `rho<1`, both the optimally adaptive and optimally precommitted **gross** expected payoff are zero exactly when `L/v >= R_star(rho)`. A zero-profit action can tie abstention at equality. At `rho=1` some observed cue pairs classify the target without residual error, so at any finite `L` both policy classes can obtain positive gross payoff.

This is a **shared positivity/no-action boundary**, not an equality of the two optimal payoffs or of their conditional acquisition premiums.

## Complete rational certificate

There are exactly 19 distinct affordable subset/outcome histories: one empty history, six one-query histories, and twelve two-query histories. Considering both target choices gives 38 posterior-odds inequalities.

For each history `h` and proposed target `y`, let the unconditional good and wrong masses under independent noise be `G_I,B_I`, and under shared noise be `G_S,B_S`. All four are exact rational numbers. Under the mixture,

\[
G_h(\rho)=(1-\rho)G_I+\rho G_S,\qquad B_h(\rho)=(1-\rho)B_I+\rho B_S.
\]

The desired upper bound is equivalent to

\[
P_h(\rho)=(14+\rho)B_h(\rho)-(1-\rho)G_h(\rho)\ge0.
\]

Each `P_h` is quadratic. The independent Fraction audit computes the three degree-two Bernstein coefficients, `b0=P(0)`, `b2=P(1)`, `b1=2P(1/2)-(b0+b2)/2`, and checks **all three coefficients are nonnegative for each of the 38 histories**. Thus every inequality holds for the entire continuous interval `0<=rho<=1`, not merely for selected grid points.

Equality holds identically for one feasible history: acquire root and left, observe `(0,0)`, and consider target 0. Its good and wrong unconditional masses are

\[
G_h(\rho)=\frac{21}{50}+\frac{3\rho}{100},\qquad
B_h(\rho)=\frac{3(1-\rho)}{100}.
\]

Consequently `G_h/B_h=(14+rho)/(1-rho)` for every `rho<1`; at `rho=1` this history has positive good mass but zero wrong mass. This attains the upper bound and proves sharpness.

Executable exact certificate: `tests/test_joint_bitflip_closed_form_cutoff.py` (13 passing cases). Its likelihood masses are constructed directly from the full latent-world × joint-error table, independently of the dynamic-programming solver.

## Ecological implications and no-go separation

For example, if the wrong-action penalty is `L=20v`, the zero-reward region is exactly

\[
\boxed{0\le\rho\le\frac{2}{7}.}
\]

For `rho>2/7`, at least one observed history supports positive expected reward from acting, even though every individual cue still has exactly 10% error. **This does not imply conditional cue acquisition has a positive premium:** at `rho=0.30,L=20v`, both adaptive and fixed-subset policies gain the same positive gross reward.

The exact formula also exhibits a singular support boundary: as `rho` tends to 1 from below, the all-abstention cutoff diverges, but at every strictly subunit `rho` it remains finite. The result depends on the specified two-query task, *joint-error mixture*, known prior, and free-abstention reward map. The correlated-encoding and Bayesian-abstention phenomena themselves are prior art.
