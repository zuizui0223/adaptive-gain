# Payoff-relevant information lifetime: a falsifiable extension

Status: supporting ecological model, not V6 MAIN 4 and not a corollary of static deterministic C_A/C_F.

## Distinguish state turnover from decision failure

A two-state Markov environment switches at rate nu. A context observation is t old at action completion. Let a mismatched action retain fraction f of the timely reward (0 <= f <= 1). Then

M(nu,t) = (1+exp(-2 nu t))/2
Q(nu,t,f) = f+(1-f)M(nu,t)
           = (1+f)/2+(1-f)exp(-2 nu t)/2.

Q is **payoff-relevant validity**, not the probability that the environment never changed. Multiple switches can restore the same state. This distinction matters for data interpretation.

For 0 <= f < 1, define the normalized recoverable information premium over an uninformed random binary action:

D(nu,t,f) = Q(nu,t,f) - (1+f)/2
          = (1-f)exp(-2 nu t)/2.

Its relative retention is D(nu,t,f)/D(nu,0,f)=exp(-2 nu t), so the half-life of the information premium is

t_half = ln(2)/(2 nu).

This half-life does **not** imply that the probability of successful action falls to one-half; Q approaches (1+f)/2. At f=1 there is no information premium and the half-life is not behaviorally identifiable.

For A (refresh taking r, followed by terminal acquisition a) and P (old context Delta before commitment, followed by terminal acquisition a), under exponential opportunity survival with hazard mu:

G_A = exp(-mu(r+a)) Q(nu,a,f)
G_P = exp(-mu a) Q(nu,Delta+a,f).

A has a performance advantage exactly when exp(-mu r)Q(nu,a,f)>Q(nu,Delta+a,f). A separate maintenance-cost term is required for selection. The payoff-relevant context is defined at completion, not at the beginning of the trial.

## Falsification and identification

A time-lag experiment can estimate the decay of the *incremental value* of the cue, provided the experiment also measures the uninformed baseline. Observing raw success alone does not identify nu or f because non-contextual success and motivation can vary. Randomize context-switch time and action latency separately, measure the realized context at completion, and compare matched versus mismatched actions.

The Markov half-life is not universal: asymmetric switching, continuous states, state-dependent reward, and learning can change the decay law. Fit a nonparametric lag-response curve first; only then compare the exponential model against alternatives.

A direct counterexample to naive volatility predictions is f=1: state turnover can be arbitrarily rapid but context information has zero marginal payoff. Another is Delta=0: the preindexed program is already fresh, so the additional router cannot improve match probability under the declared process.

## Link to PAYOFF

Use R_A:P = v(G_A-G_P) in the same units as a *pairwise* architecture cost K_A:P. This quantity is not C_F-C_A. To obtain selection coefficients instead, use a declared baseline fitness and log-maintenance costs.

## Model provenance

All statements above are analytic consequences of the declared symmetric binary Markov and exponential opportunity assumptions, not estimated ecological parameters. The static finite routing theorem remains unchanged.
