# Ecological principle blindness audit v1

Status: post-freeze synthesis audit. This document asks which established ecological principles are directly sharpened by the current deterministic routeability theory and which require additional biological dynamics.

The purpose is not to label established principles "wrong." The test is narrower:

> if a principle is expressed through a summary \(S\), can two ecological tasks share \(S\) while differing in conditional decision topology and therefore in \((C_A,C_F)\) or in the budget window \(C_A\le B<C_F\)?

If yes, \(S\) is insufficient for **routeability-sensitive** prediction unless the missing action-conditioned structure is added.

---

## 1. Audit categories

### DIRECT

The current finite theory already constructs matched systems for which the summary is held fixed while decision cost changes.

### MODIFIER

The current theory identifies a missing structural coordinate, but an evolutionary or demographic lift is needed before the established ecological outcome can be predicted.

### NOT YET REACHED

The established principle concerns a downstream object absent from the present model. Invoking routeability there would be speculative until a new model is built.

---

## 2. Information amount and fitness value

### Prior theory

Donaldson-Matasci, Bergstrom & Lachmann (2010) formalize the fitness value of environmental information.

Rivoire & Leibler (2011) derive information-fitness relations for populations in varying environments.

These theories are prior art and are not contradicted here.

### Current matched result

The quantity/topology pair holds fixed:
- the full physical cue matrix;
- cue-only joint distribution;
- target prevalence;
- target entropy \(H(T)\);
- total full-vocabulary target information
  \[
  I(T;Q_{\mathrm{all}})=H(T).
  \]

Yet the routeable mapping satisfies
\[
C_F/C_A\ge2^d/(d+1),
\]
while the matched control has
\[
C_A=C_F=2.
\]

At finite depths, registered controls can additionally match the **multiset of all pairwise target-query contingency profiles** while reducing the fixed burden sharply.

### Status

\[
\boxed{\text{DIRECT}}
\]

### What is actually shown

Total available information and pairwise information-strength summaries do not determine sequential acquisition architecture.

This does **not** imply that mutual information is irrelevant to fitness or that information-fitness theory is false.

It means that when information must be **acquired under a finite cost or time budget**, an additional coordinate is needed:

\[
\text{amount of available information}
\quad+\quad
\text{architecture of acquiring it}.
\]

### Safe claim

> Equal total target information need not imply equal ecological accessibility of that information under finite sequential acquisition constraints.

---

## 3. Specialist–generalist information-processing hypothesis

### Prior theory

Bernays & Wcislo (1994) and Bernays (2001) argue that broad resource use can impose information-processing costs, including slower or less efficient host recognition and increased exposure to ecological risk.

This is a close conceptual precursor: information-processing cost as a constraint on generalism is established.

### Current addition

The finite theory decomposes "informational complexity" more sharply.

Two consumers can have the same nominal niche breadth:
- same number of usable resources;
- same resource frequencies;
- same physical cue distribution;

yet differ in:
\[
C_A,\quad C_F,\quad g=C_F-C_A.
\]

A broad diet can therefore be:
- difficult because many distinctions remain jointly relevant; or
- cheap because early cues route encounters into branch-specific subproblems.

### Status

\[
\boxed{\text{DIRECT for processing burden}}
\]

but

\[
\boxed{\text{MODIFIER for evolved niche breadth}}.
\]

### What is directly predicted

At a fixed observation budget \(B\), nominally equally broad diets can differ in guaranteed decision feasibility.

### What is not yet directly predicted

The current model does not by itself predict the evolutionary equilibrium of diet breadth, because it lacks:
- resource profitability;
- competition;
- genetic trade-offs;
- demographic fitness consequences;
- mutation and selection dynamics.

### Safe claim

> Routeability refines the information-processing constraint on generalism by predicting when broad resource use does or does not require broad simultaneous information acquisition.

---

## 4. Environmental heterogeneity and niche breadth

### Prior theory

Kassen (2002) reviews the expectation that niche breadth often evolves to match environmental heterogeneity while emphasizing important exceptions and the role of the amount, spatial/temporal pattern, and grain of variation.

Therefore it would be inaccurate to characterize classical heterogeneity theory as using only one scalar amount.

### Current addition

The routeability theory asks a different question within environments that can already be matched on:
- state count;
- state frequencies;
- physical cue distribution;
- potentially the same spatial or temporal schedule.

It varies only the action-conditioned cue topology.

Thus two systems with comparable conventional environmental heterogeneity can differ in the information burden required for broad use.

### Status

\[
\boxed{\text{MODIFIER}}
\]

not a direct refutation.

### Missing bridge

To turn the finite decision result into a prediction for **evolved niche breadth**, one must specify how decision cost affects fitness and how niche breadth can evolve.

The hard-budget bridge gives one minimal route:
\[
C_A\le B<C_F.
\]

But a full Kassen-style evolutionary claim still requires an evolutionary model.

### Safe claim

> Environmental heterogeneity should favor broad use more readily when the relevant alternatives are routeable within the organism's sampling budget.

This is a conditional refinement, not a replacement of heterogeneity theory.

---

## 5. Diversity–stability

### Prior theory

Biodiversity–stability theory concerns population/community fluctuations, synchrony, compensatory dynamics, interaction strengths and stability metrics. Modern work shows that these relationships depend strongly on community and trophic structure rather than species richness alone.

### Current routeability model

The deterministic finite target-resolution theory contains no:
- species abundances;
- population growth rates;
- Jacobian/community matrix;
- synchrony process;
- resilience or resistance metric;
- ecosystem-function variance.

Therefore the theory cannot presently establish that two communities with the same diversity but different decision topology differ in ecological stability.

The earlier reversible Markov reward results concern temporal filtering of **state-specific selection rewards**, not community stability in the biodiversity–stability sense.

### Status

\[
\boxed{\text{NOT YET REACHED}}
\]

### Future bridge

A valid extension would require routeability to alter:
1. behaviorally accessible links or interaction strengths;
2. a community dynamical model;
3. a declared stability quantity.

Only then can one ask whether decision topology shifts diversity–stability relationships.

### Safe current use

None in the V5 headline.

At most:

> routeability supplies a candidate behavioral mechanism that could alter realized interaction structure, with downstream stability consequences left for future theory.

---

## 6. Network interaction complexity

This sits between the previous categories.

The finite theory can directly distinguish:
- compatibility-permitted links;
- links that can be behaviorally resolved under a finite observation budget.

But it cannot yet predict equilibrium network topology or community dynamics.

### Status

\[
\boxed{\text{DIRECT for accessibility}}
\]

and

\[
\boxed{\text{NOT YET REACHED for network stability/dynamics}}.
\]

### Safe claim

> Equal potential interaction richness need not imply equal behaviorally accessible interaction richness.

---

## 7. Nonidentifiability as a general methodological bridge

Two distinct nonidentifiability results now coexist in the program.

### Observation-state nonidentifiability

In binary interaction turnover, detection and latent ecological state can generate the same observed transition table. This blocks causal interpretation of observed gain/loss as true rewiring.

### Decision-topology insufficiency

In the quantity/topology constructions, the same cue-side environmental distribution and strong information summaries can coexist with different action-conditioned acquisition architecture.

These are not the same theorem.

The shared methodological rule is:

> **an ecological summary supports a mechanistic claim only when the latent structure required by that claim is identifiable from the summary or independently measured.**

This is a more general contribution than either case alone.

---

## 8. Ranking of the four candidate integrations

| Candidate principle | Current status | What current theory adds | New model needed? |
| --- | --- | --- | --- |
| Information amount / fitness value | DIRECT structural distinction | amount vs acquisition architecture | fitness consequences for full quantitative synthesis |
| Specialist–generalist information cost | DIRECT burden, MODIFIER evolution | niche breadth does not determine processing burden | evolutionary dynamics for evolved breadth |
| Heterogeneity–niche breadth | MODIFIER | routeability as conditional structural modifier | yes, for evolutionary outcome |
| Diversity–stability | NOT YET REACHED | only a candidate behavioral upstream mechanism | yes, community dynamics + stability metric |

This ranking should control manuscript emphasis.

---

## 9. Recommended V5 positioning

Lead with the first three levels only:

1. conventional heterogeneity summaries do not determine effective decision complexity;
2. information amount does not determine acquisition architecture;
3. the ecological consequence appears when the natural-history budget intersects
   \[
   C_A\le B<C_F.
   \]

Use specialist/generalist and niche breadth as ecological interpretations.

Do **not** make diversity–stability a major V5 consequence.

---

## 10. Next-paper boundary

The next theory paper should target the gap between DIRECT structural results and quantitative ecology.

A suitable stochastic expected-loss model would allow:

\[
J(\pi)
=
\mathbb E[C_\pi]
+
\lambda\mathbb E[L(A,T)].
\]

Then ask whether:
- matched information amount still permits different optimal acquisition architecture;
- routeability modifies evolved niche breadth;
- imperfect cues preserve a nonzero adaptive/fixed risk gap.

Community stability should remain a separate downstream extension unless interaction dynamics are explicitly added.

## References anchoring the audit

- Bernays, E. A. & Wcislo, W. T. 1994. Sensory capabilities, information processing, and resource specialization. *Quarterly Review of Biology* 69:187–204. DOI: 10.1086/418539.
- Bernays, E. A. 2001. Neural limitations in phytophagous insects: implications for diet breadth and evolution of host affiliation. *Annual Review of Entomology* 46:703–727. DOI: 10.1146/annurev.ento.46.1.703.
- Donaldson-Matasci, M. C., Bergstrom, C. T. & Lachmann, M. 2010. The fitness value of information. *Oikos* 119:219–230. DOI: 10.1111/j.1600-0706.2009.17781.x.
- Rivoire, O. & Leibler, S. 2011. The Value of Information for Populations in Varying Environments. *Journal of Statistical Physics* 142:1124–1166. DOI: 10.1007/s10955-011-0166-2.
- Kassen, R. 2002. The experimental evolution of specialists, generalists, and the maintenance of diversity. *Journal of Evolutionary Biology* 15:173–190. DOI: 10.1046/j.1420-9101.2002.00377.x.

## Stop rule

Do not enlarge V5 by claiming diversity–stability consequences.

The strongest current integration is:

\[
\boxed{
\text{heterogeneity/information amount}
+
\text{conditional decision topology}
+
\text{ecological budget}
\to
\text{effective decision feasibility}.
}
\]
