# Prior-art boundary for evolutionary information routing

## Purpose

This note prevents the ecological interpretation from overclaiming novelty.

The project does **not** claim to discover that animals use information, that information is costly, that cue use can be sequential or hierarchical, that learning can be adaptive, or that temporal environmental structure matters. Those are established areas of evolutionary and behavioural ecology.

The narrower question is:

> When does an outcome-contingent rule for **which cue to acquire next** outperform every fixed cue bundle, and how does that gain depend on temporal predictability?

---

## Established neighbouring literatures

### Information use in evolutionary ecology

Dall et al. (2005) framed information acquisition and use as a central object in evolutionary ecology and explicitly connected information quality to adaptive behaviour and decision theory.

What is already established:

- information can improve fitness-relevant decisions;
- information can be acquired actively or passively;
- information has ecological and evolutionary value.

What this repository adds, if the programme succeeds:

- an exact fixed-versus-contingent distinction at the level of **future cue selection**;
- structural conditions under which a cue has routing value even without direct target information.

Reference: Dall, S. R. X. et al. (2005). *Information and its use by animals in evolutionary ecology*. Trends in Ecology & Evolution. DOI: 10.1016/j.tree.2005.01.010.

### Learning and temporal environmental structure

Eliassen et al. (2009) explicitly quantified the adaptive value and efficiency of learning under spatial and temporal heterogeneity.

What is already established:

- learning value depends on environmental variation;
- information reliability and temporal change affect optimal learning;
- memory timescale can matter.

What differs here:

- the first temporal theorem does not optimize a learned estimate of one environmental variable;
- it asks whether an early context observation should determine **which later observation channel is sampled**.

Reference: Eliassen, S. et al. (2009). *Quantifying the adaptive value of learning in foraging behavior*. The American Naturalist. DOI: 10.1086/605370.

### Costs of information acquisition and cognition

Schneeberger & Taborsky (2020) emphasize that sensory and cognitive information acquisition is costly and that those costs matter for social decisions.

What is already established:

- information collection can cost time, energy, attention, risk, and cognition;
- these costs can change optimal information use.

What the minimal temporal model contributes:

\[
\Delta W=\frac{s}{4}|2\rho-1|-k,
\]

so an explicit control cost produces a threshold in temporal predictability for contingent routing.

Reference: Schneeberger, K. & Taborsky, M. (2020). *The role of sensory ecology and cognition in social decisions: Costs of acquiring information matter*. Functional Ecology. DOI: 10.1111/1365-2435.13488.

### Information Ecology

Bergman & Beehner (2023) propose Information Ecology as an integrative framework centered on what information is available to animals, how it is used, and why it is used.

This repository fits that programme only if it remains biologically explicit about

- available cue sets;
- cue order;
- cue costs;
- temporal validity;
- resulting action or fitness consequences.

Reference: Bergman, T. J. & Beehner, J. C. (2023). *Information Ecology: an integrative framework for studying animal behavior*. Trends in Ecology & Evolution. DOI: 10.1016/j.tree.2023.05.017.

### Cue hierarchies and natural history

Lund et al. (2019) document long- and short-distance cue hierarchy during `Pieris rapae` host selection.

This establishes that biologically feasible cue order can be strongly constrained by natural history and distance from the decision object.

The present theory should therefore not claim cue hierarchy as novel. Its contribution would be to ask whether an early cue's value lies partly in changing which later cue should be acquired.

Reference: Lund, M., Brainard, D. C. & Szendrei, Z. (2019). *Cue hierarchy for host plant selection in Pieris rapae*. Entomologia Experimentalis et Applicata. DOI: 10.1111/eea.12772.

---

## Current exact contribution

The current dynamic model starts from the repository's unique four-world strict adaptive-gain normal form and adds a binary context transition

\[
P(C_1=C_0)=\rho.
\]

At two-query budget,

\[
A_F^{(2)}=3/4
\]

for every fixed pair, while

\[
A_A^{(2)}=3/4+|2\rho-1|/4.
\]

Therefore

\[
G_{time}=|2\rho-1|/4.
\]

The ecological statement is deliberately narrow:

> A target-uninformative early context cue can have positive value because it predicts the identity of a later diagnostic cue; the magnitude of this value is proportional to temporal predictability in the minimal binary model.

This is not yet a general theorem for arbitrary cue likelihoods, arbitrary Markov environments, learning, or long-run population growth.

---

## Claims to avoid

Do not say:

```text
animals have not previously been modelled as information users
cue hierarchy is new
context-dependent cue weighting is new
temporal autocorrelation has not been connected to adaptation
information costs are new
negative autocorrelation has never been exploited biologically
```

The defensible novelty target is the exact structure of **contingent future cue acquisition versus fixed cue acquisition**, together with its deterministic and temporal limits.
