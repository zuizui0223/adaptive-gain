# Context turnover during sensing: the critical falsification gate

Status: model stress test, not a new V6 main theorem. Builds on CONTEXT_STALENESS_COMPARATOR_GATE_V1.

## Missing mechanism

The previous A-versus-P comparison assumes A refreshes the context and then acts on a state that stays relevant during terminal acquisition. In a genuinely rapidly switching environment, the freshly acquired context can become stale *during* terminal acquisition. Ignoring this creates a systematic advantage for A.

Use a symmetric binary continuous-time Markov context with switching rate nu, and let the current-state match probability after delay t be

M(nu,t) = (1 + exp(-2*nu*t))/2.

Suppose P uses a context observed Delta before commitment and finishes after terminal time a; A observes the context after routing time r and finishes after a more units. A's sampled context is a time a old at completion, while P's is Delta+a old. This is an **end-state matching** contract: the payoff-relevant context is the state at completion. It differs from the earlier start-state contract.

Let f in [0,1] be the payoff fraction earned when the chosen terminal program does not match the completion context. With exponential opportunity survival S(t)=exp(-mu*t), the expected normalized performances are

G_A = exp(-mu*(r+a)) * [f+(1-f)*M(nu,a)]
G_P = exp(-mu*a) * [f+(1-f)*M(nu,Delta+a)].

The exact A-over-P criterion is

exp(-mu*r) * [f+(1-f)*M(nu,a)] > f+(1-f)*M(nu,Delta+a).

If nu -> infinity, both matching probabilities -> 1/2 (for a>0), and for mu*r>0 P strictly dominates A in timely performance. Thus **high-turnover reversal no longer requires mu to increase with nu**: terminal acquisition latency alone erodes the value of refreshed context. This is a distinct mechanism from the earlier coupled-hazard scenario.

At nu=0, P is again faster and wins when mu*r>0. An intermediate advantage is possible, but not guaranteed: it depends on Delta, a, r, f and mu.

### Critical negative controls

1. a=0: A observes the payoff-relevant context immediately before completion. Its fresh-information advantage need not vanish at high turnover; high-turnover reversal is not universal.
2. mu=0: if there is no time cost and Delta>0, A has no less matching probability than P, so A weakly dominates for every nu. With additive controller cost K>0, a bounded positive region may nevertheless occur.
3. Delta=0: P's context is already current at commitment. With identical terminal acquisition duration, A cannot improve end-state matching and only incurs routing delay.
4. P is allowed to refresh: then P is no longer the original frozen preindexed competitor; a new architecture-comparator definition is needed.

### Relation to the finite routing theorem

This stress test changes the target while acquisition is in progress. The original finite deterministic task assumes a fixed hidden world and deterministic query outcomes. Therefore the end-state switching model is **outside the scope** of the sharp C_A/C_F frontier. It can be used as an ecological bridge, but must not be described as a corollary of the finite theorem.

### What a real experiment must record

Randomize late context switches *during* the terminal acquisition period. Record which cue is acquired next, its timestamp, completion time, and whether the chosen action matches the context at completion. Independently vary the cue-acquisition latency a and precommitment memory lag Delta.

Predictions: if the late-switch effect disappears as a becomes large, fresh routing information is expiring; if P is allowed to refresh and matches A, a putative routing advantage is actually a comparator-choice artifact. A mere motor-response difference does not identify adaptive query routing.

No natural parameter values or population selection coefficients are inferred here. The novelty claim remains capped at V6 MAIN 1–3.
