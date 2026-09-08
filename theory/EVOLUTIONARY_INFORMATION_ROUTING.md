# Evolutionary information routing in changing environments

## Status

This note develops an evolutionary-ecology interpretation of the deterministic `adaptive-gain` theory.

It is a **research programme**, not a claim that the evolutionary model has already been proved. The current repository proves finite deterministic fixed-versus-adaptive target-resolution results. The evolutionary layer below specifies what would have to be added.

---

## 1. The key shift

The current theory can be read in two ways.

```text
investigator interpretation:
    which measurement should the scientist acquire next?

organism interpretation:
    which cue / sensory channel should the organism sample next?
```

The second interpretation moves the theory into evolutionary and behavioural ecology.

The biological object is not "adaptation" in the population-genetic sense yet. It is an **outcome-contingent information-acquisition policy** that natural selection may favour or disfavor.

---

## 2. Four distinct timescales

A useful evolutionary treatment must separate at least four clocks.

### Information-acquisition time

\[
\tau_{\mathrm{info}}
\]

The time over which an organism samples cues in sequence.

Examples include approach, inspection, tasting, courtship assessment, host search, predator assessment, or navigation.

### Ecological-state persistence time

\[
\tau_{\mathrm{env}}
\]

The time over which the fitness-relevant ecological state remains similar enough that an earlier cue still describes the state relevant to later sensing or action.

### Phenotypic-response time

\[
\tau_{\mathrm{phen}}
\]

The time required to change behaviour, physiology, development, or another plastic phenotype after information is acquired.

### Evolutionary time

\[
\tau_{\mathrm{evo}}
\]

The time over which selection changes the sensory repertoire, cue weighting, memory, sampling behaviour, or information-routing policy.

The present deterministic repository is closest to the regime

\[
\boxed{\tau_{\mathrm{info}}\ll\tau_{\mathrm{env}}}
\]

where the hidden state is effectively frozen while the observation policy runs.

---

## 3. Time is already implicit in adaptivity

Even in the static theory, adaptivity creates an arrow of logical time:

\[
h_t
\longrightarrow q_t
\longrightarrow y_t
\longrightarrow h_{t+1}
\longrightarrow q_{t+1}.
\]

The current continuation structure is therefore a structure of **future information opportunities conditional on past information**.

The natural dynamic extension is to let the ecological state itself move:

\[
X_{t+1}\sim K(\cdot\mid X_t),
\]

and observations satisfy

\[
Y_t\sim P_{q_t}(\cdot\mid X_t).
\]

The organism chooses

\[
q_{t+1}=\pi(h_{t+1})
\]

or stops sampling and acts.

This creates a competition between two effects:

```text
routing benefit:
    an early cue makes later sensing more targeted

obsolescence cost:
    while the organism samples, the ecological state may change
```

---

## 4. Temporal persistence as a control parameter

Let ecological persistence be summarized, in the simplest Markov model, by a parameter such as

\[
\rho=P(X_{t+1}=X_t)
\]

or more generally by predictive dependence between `X_t` and `X_{t+\Delta}`.

This suggests three regimes.

### Slow environmental change

\[
\tau_{\mathrm{env}}\gg\tau_{\mathrm{info}}.
\]

Earlier cues remain valid long enough to route later sensing.

Prediction: deeper outcome-contingent sensing policies can be favoured.

### Comparable timescales

\[
\tau_{\mathrm{env}}\approx\tau_{\mathrm{info}}.
\]

Information can become stale during the sensing sequence.

Prediction: optimal policies should trade routing depth against delay and may show an optimal stopping depth.

### Fast environmental change

\[
\tau_{\mathrm{env}}\ll\tau_{\mathrm{info}}.
\]

Branch information rapidly loses relevance.

Prediction: selection may favour shallow, parallel, constitutive, or robust sensing rather than deep sequential routing.

These are hypotheses to prove in a dynamic extension, not consequences already established by the deterministic theorem.

---

## 5. Routing cues versus target-predictive cues

Much evolutionary theory of phenotypic plasticity values a cue by how reliably it predicts the environment of selection.

The deterministic `adaptive-gain` witnesses expose a different possibility.

An early observation may have little or even zero direct information about the final target while still being essential because it determines which later observation is useful.

This motivates a distinction between:

### target-predictive cue

A cue directly changes the organism's belief about the fitness-relevant target.

### routing cue

A cue primarily changes **which subsequent cue, sensory modality, location, or behaviour should be sampled**.

Symbolically, a routing cue may satisfy

\[
I(T;Y_q)\approx0
\]

while

\[
\pi^*(h,Y_q)\ne\pi^*(h).
\]

Its value lies in changing the continuation policy rather than directly predicting `T`.

This should not be advertised as a newly discovered biological phenomenon without a dedicated literature audit: context-dependent cue hierarchies and sequential multimodal sensing are already documented. The potential contribution is an exact **fixed-versus-contingent structural theory** of such routing value.

---

## 6. Evolutionary objective

To move from behavioural routing to evolutionary adaptation, assign fitness consequences to information acquisition and action.

Let an organism eventually choose action or phenotype `a`, with fitness contribution

\[
w(a,X_t),
\]

and let cue acquisition have costs in time, energy, exposure, or opportunity:

\[
c(q)>0.
\]

A simple within-episode objective is

\[
J(\pi)
=
\mathbb E\left[
 w(a_\pi,X_{\tau})
 -\sum_{t<\tau}c(q_t)
 -d(\tau)
\right],
\]

where `tau` is the stopping time and `d(tau)` is an optional delay cost.

For repeated episodes or population growth, a more explicitly evolutionary objective may use long-run growth or expected lifetime reproductive success.

Define the evolutionary value of contingent sensing as

\[
\Delta_{\mathrm{route}}
=
\max_{\pi\in\Pi_{\mathrm{adaptive}}}J(\pi)
-
\max_{F\in\Pi_{\mathrm{fixed}}}J(F).
\]

The current deterministic `C_F-C_A` becomes a zero-error, static-state, resolution-cost boundary case rather than a separate unrelated theory.

---

## 7. Evolutionary predictions suggested by the framework

The dynamic theory should test the following predictions.

### P1. Environmental persistence should favour deeper cue routing

When state persistence is high relative to cue-acquisition time, early branch information remains useful long enough to justify specialized later sensing.

### P2. Volatile environments should favour shallower or parallel sensing

When states change rapidly, sequential specialization can lose value because early routing information becomes stale.

### P3. Large cue-cost asymmetry should favour cheap routers followed by expensive specialists

If one cue cheaply identifies which expensive sensory channel is worth using, contingent acquisition can strongly outperform constitutive acquisition of all channels.

### P4. A cue can be evolutionarily important despite weak marginal correlation with the final fitness target

Selection can maintain a cue because it changes the value of future cues.

This predicts a failure mode for empirical analyses that rank cue importance only by marginal cue-target association.

### P5. Memory should evolve jointly with routing depth and environmental autocorrelation

Memory preserves branch information, but retaining old information can become harmful when environmental states turn over quickly.

### P6. Organisms may evolve behaviour that changes the order in which cues become available

If cue order affects information value, natural selection can act not only on sensory sensitivity but also on approach, inspection, search, movement, or handling behaviours that reorder information acquisition.

### P7. Signalers and receivers can coevolve around routing cues

A signal or cue that controls a receiver's next information-acquisition step can alter later inspection effort even without directly identifying quality. This suggests a possible connection to deception, sensory exploitation, mate assessment, host finding, and plant-pollinator interactions.

---

## 8. Natural history is part of the theory, not merely an illustration

Natural history determines the feasible observation policy.

For an organism, cues are not arbitrary labels in a mathematical table. Natural history determines:

```text
which cue is available at long range
which appears only after approach or contact
which cue acquisition consumes time or energy
which cue exposes the organism to predation or competition
which cues can be sampled simultaneously
which cues disappear after an action
which cues themselves alter the interaction partner or environment
how long the ecological state persists
```

Mathematically, natural history specifies a state- and time-dependent action set

\[
Q(h_t,X_t,t)
\]

and sometimes action-dependent ecological transitions.

Thus natural history supplies the **feasible cue graph** on which the adaptive-information theory runs.

This gives the theory a concrete empirical interface: document the actual cue sequence first, then ask whether the observed sequence has routing structure.

---

## 9. Natural-history systems where the idea is plausible

These are example classes, not empirical claims about any particular species.

### Host finding and oviposition

Long-distance habitat or plant cues can be encountered before short-distance chemical, nutritional, predator, or contact cues. Sequential cue hierarchies are already documented in host-selection behaviour.

### Foraging

Animals may first identify a promising patch class, then deploy more costly local assessment, handling, or prey-discrimination behaviours.

### Mate assessment

Long-range signals can determine whether an individual approaches and which close-range visual, acoustic, chemical, or behavioural information is then acquired.

### Predator assessment

A coarse alarm or habitat-risk cue can route attention toward predator-specific confirmation channels before escape or refuge choice.

### Navigation

Global and local cues can have context- and experience-dependent hierarchical roles.

### Plant-pollinator interactions

Pollinators encounter floral information through a temporally and spatially structured sequence from detection and approach to landing, handling, reward assessment, and memory. Selection on floral traits can therefore act partly through effects on the pollinator's future information-acquisition trajectory, not only through instantaneous attraction.

---

## 10. Relation to established evolutionary ecology

This project must explicitly connect to, rather than rediscover, existing information-use theory.

Representative starting points include:

- Dall, S. R. X., Giraldeau, L.-A., Olsson, O., McNamara, J. M. & Stephens, D. W. (2005). *Information and its use by animals in evolutionary ecology*. Trends in Ecology & Evolution. DOI: 10.1016/j.tree.2005.01.010.
- Chevin, L.-M. & Lande, R. (2015). *Evolution of environmental cues for phenotypic plasticity*. Evolution. DOI: 10.1111/evo.12755.
- Eliassen, S., Jørgensen, C., Mangel, M. & Giske, J. (2009). *Quantifying the adaptive value of learning in foraging behavior*. The American Naturalist. DOI: 10.1086/605370.
- Schneeberger, K. & Taborsky, M. (2020). *The role of sensory ecology and cognition in social decisions: Costs of acquiring information matter*. Functional Ecology. DOI: 10.1111/1365-2435.13488.
- Nieh, J. C. et al. (2023). *Information Ecology: an integrative framework for studying animal behavior*. Trends in Ecology & Evolution. DOI: 10.1016/j.tree.2023.05.017.
- Lund, M. et al. (2019). *Cue hierarchy for host plant selection in Pieris rapae*. Entomologia Experimentalis et Applicata. DOI: 10.1111/eea.12772.

The literature already establishes that information has fitness value, costs, temporal structure, cue hierarchies, and context dependence.

The proposed contribution is therefore narrower:

\[
\boxed{
\text{When does conditional cue routing itself create value beyond a fixed cue repertoire?}
}
\]

and

\[
\boxed{
\text{How does that value depend on the relative timescales of sensing and environmental change?}
}
\]

---

## 11. Stronger theoretical-ecology framing

A possible conceptual centre is no longer merely

> When is adaptive measurement cheaper than fixed measurement?

but

> **When should an organism condition future information acquisition on information already obtained, and how does environmental time structure determine the evolutionary value of that routing?**

This framing connects the exact deterministic theory to behavioural ecology, sensory ecology, phenotypic plasticity, learning, and natural history without pretending those literatures are absent.
