# Context staleness: an ecological comparator gate for contingent sensing

**Status:** support / falsification design on PR #67. This is a declared
toy process with illustrative parameters; **not** MAIN 4, not an empirical
test of selection, and not a replacement for the finite sharp frontier.

## Why this comparator matters

The finite theorem compares contingent acquisition A with a universal fixed
query bundle U, so a strict structural gap C_A < C_F is an advantage over U.
Biological evolution can instead compare A with a *context-preindexed
repertoire* P. P possesses alternative terminal programs and selects one from
a context already known before focal commitment. Such a competitor can avoid
the runtime router. Thus A < U does not establish that A > P.

A general account must say **when context information becomes available**
relative to action commitment. This note makes old information potentially
stale, then asks when refreshing the present context is worth its delay.

## Minimal process and exact comparison

Assume:

- The environmental context has two states, switching symmetrically with
  continuous-time Markov rate \(\nu\); the last context observation was
  \(\Delta\) time units before commitment. It is available to P at no
  additional focal runtime cost.
- P commits to one terminal program using the remembered context and takes
  acquisition time \(a\). If context has changed, it earns fraction
  \(f\in[0,1]\) of the timely payoff; it cannot refresh or self-correct.
- A refreshes the *current* context in time \(r\), then acquires the
  context-appropriate terminal information in time \(a\).
- An opportunity survives through time \(t\) with probability
  \(S(t)=e^{-\mu t}\), independent of context switching conditional on the
  parameters. Correct timely completion is worth \(v\ge0\).
- Per-decision acquisition time and constitutive architecture cost remain
  separate. A and P are physically feasible comparator classes only if their
  declared cue and program access is biologically possible.

The context-memory mismatch probability and normalized expected timely
performances are exactly

\[
q(\nu,\Delta)=\frac{1-e^{-2\nu\Delta}}{2},
\qquad
G_A=e^{-\mu(r+a)},\qquad
G_P=[1-q(1-f)]e^{-\mu a}.
\]

The necessary and sufficient condition for strictly larger timely performance
of A over P with equal maintenance costs is

\[
\boxed{q(1-f)>1-e^{-\mu r}.}\tag{CS1}
\]

For additive controller debit \(K\ge0\) in expected performance-reward units,
the strict threshold becomes

\[
\boxed{
q>\frac{1-e^{-\mu r}+K e^{\mu a}/v}{1-f}
}\quad (v>0,\;f<1).\tag{CS2}
\]

The symmetric Markov model has \(q<1/2\) at finite turnover and positive lag,
so even a threshold below one need not be ecologically attainable.

Alternatively, with baseline \(w_0>0\) and *log* maintenance costs
\(\kappa_A,\kappa_P\), the exact selection coefficient is

\[
\boxed{
s_{A:P}=\log\frac{w_0+vG_A}{w_0+vG_P}
-(\kappa_A-\kappa_P).
}\tag{CS3}
\]

Do not substitute a reward-unit K directly for a log-fitness kappa.

## A conditional, nonmonotone volatility prediction

As a mechanistic ecological **scenario**, suppose the same environmental
process drives both context turnover and opportunity loss:

\[
\mu=\alpha\nu,\quad\alpha>0.
\]

Then the additive net advantage of A over P is

\[
\boxed{
\Phi(\nu)=v e^{-\alpha\nu a}
\left[\frac{1-f}{2}(1-e^{-2\nu\Delta})
-(1-e^{-\alpha\nu r})\right]-K.
}\tag{CS4}
\]

With \(K>0\), both limits are negative:
\(\lim_{\nu\to0}\Phi(\nu)=\lim_{\nu\to\infty}\Phi(\nu)=-K\).
At low turnover the old context is accurate; at extremely high turnover
even refreshed decisions seldom finish before opportunity loss.

There is an exact no-positive-performance criterion for this narrow model:

\[
\boxed{(1-f)\Delta\le\alpha r
\ \Longleftrightarrow\
G_A(\nu)\le G_P(\nu)\ \text{for all}\ \nu\ge0.}\tag{CS5}
\]

Proof: let \(x=2\nu\Delta\) and \(c=(1-f)/2\le1\).
The condition gives \(\alpha r\nu\ge cx\).
The increasing concave function \(1-e^{-x}\), vanishing at zero, satisfies
\(1-e^{-\alpha r\nu}\ge1-e^{-cx}\ge c(1-e^{-x})\).
Conversely the derivative of \(G_A-G_P\) at \(\nu=0\) is
\((1-f)\Delta-\alpha r\); if positive, sufficiently small positive turnover
favors A *before* controller cost.

When the latter difference is positive and \(0<K<\max_\nu
v(G_A-G_P)\), a **bounded range of turnover rates** can favor refreshing.
This is not the unconditional assertion that variability favors plasticity.

### Reproducible scenario, not an ecological parameter estimate

Dimensionless parameters:
\(\Delta=2,\alpha=0.3,r=a=1,f=0.1,v=1,K=0.05\).

| \(\nu\) | \(\Phi(\nu)\) |
|---:|---:|
| 0.0 | -0.050000 |
| 0.1 | +0.065290 |
| 0.5 | +0.165011 |
| 1.0 | +0.085256 |
| 2.0 | -0.050735 |

Numerical positive window: \(0.03675<\nu<1.53861\); peak near
\(\nu=0.417\), \(\Phi=0.16842\). These are deterministic model outputs.

**Required negative control:** if \(\mu\) stays constant while \(\nu\)
rises, q increases but deadline pressure does not. The high-turnover
reversal then disappears. Environmental change must alter both context
validity and opportunity duration to produce this mechanism.

## How a biological test could reject the routing interpretation

Independently manipulate (1) context information arriving before versus
after commitment, including a randomized late context switch, (2) opportunity
window duration, and (3) specificity of terminal programs across contexts.
Measure whether later **information acquisition choices**, not only
motor responses, differ, alongside individual completion CDFs and achieved
payoff within the window.

A rise in flight speed, attraction, or sensory gain is insufficient to
distinguish routed sensing from a preindexed or fixed stimulus-response
repertoire. No switch in the *next acquired cue* after a late context
manipulation would falsify the key routing interpretation.

Potential assay-design reference: Kato-Namba et al. (2025),
[context-dependent cross-modal integration in mosquito flight](https://doi.org/10.1038/s41598-025-13427-z),
with [public data/code](https://doi.org/10.60178/cbs.20250721-001).
This study reports cross-modal modulation, **not** direct A-versus-P
fitness evidence. The Chandel et al. (2024) IR timecourse and
Uehara et al. (2026) individual first-probe profiles retain their
limited, distinct roles in the V6 manuscript.

Prior art is substantial: environmental predictability and plasticity
(e.g. [Reed et al. 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2982227/))
and delayed phenotype/sensing responses
([Moffett et al. 2020](https://doi.org/10.1103/PhysRevE.102.052403))
already address related ideas. Here the purpose is to force an explicit
comparator and an experimentally falsifiable **ecological timing gate**,
not to claim a new universal theorem of plasticity.

## Scope relative to PAYOFF and V6

The pairwise expected performance benefit \(R_{A:P}=v(G_A-G_P)\)
and pairwise controller cost \(K_{A:P}\) can be transferred into PAYOFF's
architecture-selection logic, provided both use the same comparator and
fitness currency. Neither is interchangeable with the original
universal-fixed structural gap \(C_F-C_A\).

V6 MAIN 1--3 remain unchanged; no extra novelty result is promoted.

Executable model:
[adaptive_gain/context_staleness.py](../adaptive_gain/context_staleness.py);
[tests/test_context_staleness.py](../tests/test_context_staleness.py).
