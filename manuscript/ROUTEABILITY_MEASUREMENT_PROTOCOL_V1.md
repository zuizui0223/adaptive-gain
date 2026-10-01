# Routeability measurement protocol v1

Status: post-freeze methods synthesis. This is a measurement specification for future empirical work, not a claim that routeability has already been measured in natural systems.

## Goal

Estimate the deterministic finite routeability object for a declared focal ecological decision.

The protocol is designed to recover the minimum information needed to specify:

\[
(W,T,Q,c)
\]

where:
- \(W\) = represented ecological alternatives;
- \(T\) = focal action/target;
- \(Q\) = available cue vocabulary and outcome maps;
- \(c\) = cue acquisition costs.

Once these are defined, the exact finite model determines \(C_A\), \(C_F\), decision-equivalence classes, and the adaptive-only budget window.

## 1. Declare the focal action first

Routeability is task-relative.

Before measuring cues, declare the focal decision.

Examples:
- flower accept / reject;
- host accept / reject;
- prey attack / avoid;
- mate court / reject;
- habitat enter / leave.

Do not define routeability from environmental variables alone.

The same physical environment may induce different routeability for different focal actions.

## 2. Define represented alternatives

Specify the state set \(W\).

Possible units:
- individual flowers;
- resource species;
- resource condition classes;
- partner phenotypes;
- habitat patches;
- predator contexts.

The represented state should be fine enough that target/action and cue outcomes are well-defined.

Then record the target map

\[
T:W\to\mathcal A.
\]

States with the same target may remain distinct because they can differ in future cue requirements.

## 3. Record cue identities and outcome maps

For every candidate cue \(q_j\), record:

- biological identity of the cue;
- physical measurement;
- outcome alphabet;
- outcome for every represented state;
- whether the cue is available before, during, or after other cues.

This yields the state-by-cue matrix

\[
Q=
(q_j(w)).
\]

Do not reduce immediately to:
- entropy;
- pairwise correlation;
- mutual information;
- PCA axes.

Those summaries can be reported later but do not substitute for the action-conditioned table.

## 4. Measure acquisition cost

Assign a cost \(c_j>0\) on a biologically justified scale.

Possible currencies:
- seconds of inspection;
- energetic expenditure;
- movement distance;
- predator-exposure time;
- handling opportunity lost;
- sensory acquisition latency.

If costs are not commensurable, the exact additive-cost model is not yet justified.

In that case:
- report cue order and availability;
- do not force a scalar \(C_A,C_F\) interpretation.

## 5. Record conditional acquisition paths

Observed behavior should record not only **which cues were used**, but:

- first cue;
- its outcome;
- second cue conditional on that outcome;
- subsequent cue identities and outcomes;
- stopping point;
- final action.

The minimal empirical event record is:

\[
(\text{state},\text{target},q_1,y_1,q_2,y_2,\ldots,\text{action}).
\]

A frequency table of cue use alone is insufficient because it destroys branch structure.

## 6. Compute the deterministic structural quantities

From the declared task compute:

### Adaptive optimum

\[
C_A
\]

minimum worst-case cost of a contingent policy.

### Fixed optimum

\[
C_F
\]

minimum cost of a precommitted resolving cue set.

### Routeability advantage

\[
g=C_F-C_A.
\]

### Decision-equivalence classes

Collapse states that are identical for:
- focal target;
- future cross-target separation requirements.

### Budget window

For a biological budget \(B\), test:

\[
C_A\le B<C_F.
\]

This is the exact routeability-sensitive region.

## 7. Separate structural and behavioral measurements

Do not infer \(C_A\) or \(C_F\) solely from observed animal behavior.

### Structural task

Defined by:
- state set;
- target map;
- cue outcome matrix;
- cue costs.

### Behavioral strategy

Observed:
- which cues animals actually sample;
- learning errors;
- nonoptimal choices;
- latency;
- abandonment.

An animal may fail to exploit a highly routeable environment.

Conversely, successful behavior does not by itself identify the environmental optimum.

The experiment should therefore distinguish:

\[
\text{available routeability}
\]

from

\[
\text{realized behavioral routing}.
\]

## 8. Minimum data products

### Product A — action-conditioned cue table

Rows:
- ecological state;
- target/action;
- cue outcomes.

This is the minimum deterministic structural object.

### Product B — cue cost table

Rows:
- cue identity;
- acquisition cost;
- timing/availability constraints.

### Product C — behavioral path log

Rows:
- individual;
- trial;
- state;
- ordered cue observations;
- outcomes;
- response;
- latency.

### Product D — ecological budget

Estimate:
- opportunity duration;
- exposure ceiling;
- or another biologically justified hard/effective ceiling.

These four products allow structural theory and behavioral data to be compared without conflating them.

## 9. Diagnostic summary hierarchy

Report conventional summaries, but label them correctly.

### Environment-only summaries
- richness;
- cue marginals;
- cue entropy;
- cue covariance;
- full cue-only joint distribution.

### Action summaries
- target prevalence;
- target entropy.

### Information summaries
- target-cue pairwise mutual information;
- full-vocabulary target information.

### Structural routeability summaries
- \(C_A\);
- \(C_F\);
- \(g\);
- decision-equivalence class count;
- branch-specific cue obligations.

The earlier levels cannot substitute for the final level.

## 10. Natural-system identifiability gate

A natural system is **routeability-evaluable** only if:

1. the focal action is declared;
2. represented alternatives are defined;
3. cue identities are specified;
4. cue outcomes are measured across alternatives;
5. cue acquisition costs or order constraints are defensible.

If any of these are absent, routeability should not be estimated as though it were identified.

Use status labels:

- EVALUABLE;
- PARTIALLY_EVALUABLE;
- NOT_IDENTIFIED.

Do not rescue an unevaluable system by substituting richness, entropy, or network turnover.

## 11. Noisy natural systems

The present exact protocol is a deterministic idealization.

If cue outcomes are probabilistic, record:

\[
P(Y_q\mid w)
\]

rather than one deterministic outcome.

Do **not** discretize noise away merely to use the current exact solver.

Such data belong to the future expected-loss/stochastic extension.

Until that theory is complete, deterministic routeability can be used only when:
- cue states are effectively stable at the focal scale;
- or the analysis is explicitly presented as an idealized structural approximation.

## 12. Recommended first empirical system

Use the artificial-flower experiment before attempting a natural community.

Why:
- target/action is experimentally controlled;
- physical cue matrix is known exactly;
- cue availability can be manipulated;
- budget can be imposed;
- behavioral path can be logged;
- routeable and bypass tasks can share the same cue environment.

This directly validates the measurement concept.

Natural-system applications should follow only after the causal task is shown to be behaviorally meaningful.

## One-line protocol

\[
\boxed{
\text{Measure the action-conditioned cue table first; summarize it second.}
\]
