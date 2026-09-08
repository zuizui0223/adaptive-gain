# Evolutionary information routing in changing environments

## Status

This note interprets the deterministic `adaptive-gain` theory as a theory of outcome-contingent information acquisition by organisms and records the evolutionary-ecology programme around it.

A first dynamic theorem is now closed in `TEMPORAL_ROUTING_THRESHOLD.md`. The important correction relative to the initial sketch is that **temporal predictability, not persistence alone, controls routing value** in the minimal model.

---

## 1. From investigator measurement to organism sensing

The same formal object has two interpretations.

```text
investigator:
    which measurement should be acquired next?

organism:
    which cue, location, sensory modality, or inspection behaviour should be sampled next?
```

The evolutionary object is therefore not adaptation in the population-genetic sense by definition. It is a heritable or condition-dependent information-acquisition policy on which natural selection may act.

The central question becomes

> **When should an organism condition future information acquisition on information already obtained?**

---

## 2. Four clocks

A useful evolutionary treatment must distinguish at least four timescales.

\[
\tau_{info}
\]

is the time over which cues are sampled in sequence.

\[
\tau_{env}
\]

is the characteristic time over which the ecological context governing cue usefulness changes.

\[
\tau_{phen}
\]

is the response time for behaviour, physiology, development, or another phenotype.

\[
\tau_{evo}
\]

is the evolutionary time over which cue weighting, memory, sensory repertoires, and routing policies change.

The original deterministic repository is closest to a frozen-state limit in which the information-acquisition episode is short relative to relevant state change.

---

## 3. Adaptivity already creates an arrow of time

Even before the ecological state moves, the adaptive policy has logical time:

\[
h_t
\to q_t
\to y_t
\to h_{t+1}
\to q_{t+1}.
\]

The continuation structure therefore describes **future information opportunities conditional on past information**.

A dynamic ecological extension lets context move:

\[
X_{t+1}\sim K(\cdot\mid X_t),
\qquad
Y_t\sim P_{q_t}(\cdot\mid X_t).
\]

The organism chooses a later cue from its history or stops sensing and acts.

This creates a competition among

```text
routing benefit:
    early information makes later sensing more targeted

obsolescence:
    early information can become stale

predictable transformation:
    early information may remain useful after a systematic reversal or other transition
```

The third term is essential. Rapid change need not destroy routing if the change itself is predictable.

---

## 4. First exact temporal theorem

The unique four-world strict-gain normal form can be written as

\[
(T,C)\in\{0,1\}^2,
\]

where `T` is a target and `C` determines which specialist query is diagnostic.

Let

\[
P(C_1=C_0)=\rho.
\]

At budget two, every fixed pair has Bayes target accuracy

\[
\boxed{A_F^{(2)}=3/4.}
\]

The optimal contingent policy has

\[
\boxed{
A_A^{(2)}
=
3/4+|2\rho-1|/4.
}
\]

Therefore

\[
\boxed{
G_{time}=|2\rho-1|/4.
}
\]

Consequences:

- `rho > 1/2`: follow the same branch because context tends to persist;
- `rho < 1/2`: route to the opposite branch because context tends to alternate;
- `rho = 1/2`: routing value vanishes exactly.

The relevant ecological quantity is thus **predictability of future cue usefulness from current context**.

See `theory/TEMPORAL_ROUTING_THRESHOLD.md` and `adaptive_gain/temporal_routing.py`.

---

## 5. Routing cues versus target-predictive cues

The deterministic core and its temporal extension motivate a useful distinction.

### Target-predictive cue

A cue directly changes belief about the final fitness-relevant target.

### Routing cue

A cue changes which later cue, sensory modality, location, or inspection behaviour should be sampled.

A routing cue can satisfy

\[
I(T;Y_q)=0
\]

while still changing the optimal continuation policy.

This does **not** mean cue hierarchies or context-dependent sensing are newly discovered. Those are established biological phenomena. The proposed contribution is narrower: an exact fixed-versus-contingent theory showing when the routing role itself generates value.

---

## 6. Evolutionary objective

Let an organism eventually choose an action `a` with fitness contribution

\[
w(a,X_\tau),
\]

and let sensing carry energetic, temporal, predation, attention, or opportunity costs.

A within-episode objective is

\[
J(\pi)
=
E\left[
 w(a_\pi,X_\tau)
 -\sum_{t<\tau}c(q_t)
 -d(\tau)
\right].
\]

Define the value of contingent sensing as

\[
\Delta_{route}
=
\max_{\pi\in\Pi_A}J(\pi)
-
\max_{F\in\Pi_F}J(F).
\]

In the first temporal model, if one unit of classification accuracy is worth `s` fitness units and maintaining contingent control costs `k`,

\[
\boxed{
\Delta W
=
\frac{s}{4}|2\rho-1|-k.
}
\]

Thus routing is selected when

\[
\boxed{|2\rho-1|>4k/s.}
\]

This turns temporal predictability into an explicit evolutionary threshold.

---

## 7. Predictions

### P1. Marginally weak cues can be strongly selected

A cue can have little or no direct association with the final target while being maintained because it predicts which later cue will be useful.

### P2. The sign of temporal autocorrelation can reverse cue order

Positive autocorrelation favours same-branch continuation; negative autocorrelation can favour deliberate branch reversal.

### P3. Unpredictability, not change alone, erodes routing value

A rapidly oscillating but predictable environment can support contingent sensing. A slowly changing but locally unpredictable environment need not.

### P4. Memory and routing should coevolve

Memory is useful insofar as stored branch information predicts future cue usefulness. Its optimal duration should therefore depend on the temporal correlation structure relevant to the next sensing step.

### P5. Selection can act on information order

Approach, inspection, movement, handling, and attention can change which cues become available first. Natural selection can therefore act on the order of information acquisition, not only sensory sensitivity or cue weighting.

### P6. Signalers may affect receiver routing

Signals may alter which later features a receiver inspects even when they do not directly reveal final quality. This creates possible links to mate assessment, sensory exploitation, host finding, deception, and mutualistic signalling.

---

## 8. Natural history specifies the feasible cue graph

Natural history is not a decorative example after the mathematics. It constrains the policy space.

It determines

```text
which cues exist at long range
which require approach or contact
which cues can be sampled simultaneously
which cues take time or energy
which cues increase predation or competition risk
which cues disappear after an action
which interactions change after inspection
how quickly the relevant context changes
```

Mathematically, this defines a history- and state-dependent feasible set of observations.

Empirically, the workflow should therefore begin with a natural-history map of the actual cue sequence and only then ask whether it contains routing structure.

---

## 9. Plausible natural-history systems

These are candidate system classes, not claims that they instantiate the exact theorem.

### Host finding and oviposition

Long-distance habitat or plant cues precede short-distance chemical, nutritional, predator, and contact cues. `Pieris rapae` host choice provides an empirical example of sequential long- and short-distance cue hierarchy.

### Foraging

A coarse patch cue can determine whether an animal invests in more costly local assessment or prey discrimination.

### Mate assessment

Long-range signals can determine approach and thereby which close-range visual, acoustic, chemical, or behavioural information becomes available.

### Predator assessment

A coarse risk cue can route attention toward predator-specific confirmation before escape or refuge choice.

### Navigation

Global and local orientation cues can be used in context- and experience-dependent orders.

### Plant-pollinator interactions

Pollinators encounter floral information through detection, approach, landing, handling, reward assessment, and memory. Floral traits may therefore affect later information acquisition as well as immediate attraction.

---

## 10. Literature boundary

The project must connect explicitly to established information-use and sensory-ecology theory.

Representative anchors:

- Dall, S. R. X., Giraldeau, L.-A., Olsson, O., McNamara, J. M. & Stephens, D. W. (2005). *Information and its use by animals in evolutionary ecology*. Trends in Ecology & Evolution. DOI: 10.1016/j.tree.2005.01.010.
- Eliassen, S., Jørgensen, C., Mangel, M. & Giske, J. (2009). *Quantifying the adaptive value of learning in foraging behavior*. The American Naturalist. DOI: 10.1086/605370.
- Schneeberger, K. & Taborsky, M. (2020). *The role of sensory ecology and cognition in social decisions: Costs of acquiring information matter*. Functional Ecology. DOI: 10.1111/1365-2435.13488.
- Bergman, T. J. & Beehner, J. C. (2023). *Information Ecology: an integrative framework for studying animal behavior*. Trends in Ecology & Evolution. DOI: 10.1016/j.tree.2023.05.017.
- Lund, M., Brainard, D. C. & Szendrei, Z. (2019). *Cue hierarchy for host plant selection in Pieris rapae*. Entomologia Experimentalis et Applicata. DOI: 10.1111/eea.12772.

These literatures already establish information value, information costs, cue hierarchy, attention, learning, and temporal environmental effects.

The proposed theoretical niche is

\[
\boxed{
\text{fixed cue bundles versus outcome-contingent cue routing, with exact structural and temporal gain.}
}
\]

---

## 11. Journal-level framing

For a theoretical-ecology paper, the conceptual centre should be

> **When should organisms use present information to choose what information to acquire next?**

The deterministic `C_A<C_F` theorem supplies the structural boundary. The temporal theorem supplies the first evolutionary consequence. A next-stage model should add noisy cues, arbitrary transition kernels, and explicit fitness actions without losing the distinction between direct target information and continuation-routing information.
