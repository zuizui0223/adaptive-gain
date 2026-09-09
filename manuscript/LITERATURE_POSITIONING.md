# Literature positioning and novelty boundary

## Purpose

This file records the ecological/evolutionary literature boundary for the manuscript. It is intentionally conservative: standard results should be cited as prior art rather than repackaged as novelty.

## 1. Rapid evolution and evolutionary time

### Established

- Hairston, N. G. Jr., Ellner, S. P., Geber, M. A., Yoshida, T. & Fox, J. A. 2005. Rapid evolution and the convergence of ecological and evolutionary time. *Ecology Letters*. DOI: 10.1111/j.1461-0248.2005.00812.x.
  - Use for: ecological and evolutionary processes can operate on overlapping timescales.
  - Do not claim: recognizing ecological-timescale evolution.

- Bell, G. 2010. Fluctuating selection: the perpetual renewal of adaptation in variable environments. *Philosophical Transactions of the Royal Society B* 365:87–97. DOI: 10.1098/rstb.2009.0150.
  - Use for: strong and directionally fluctuating natural selection.
  - Do not claim: fluctuating selection can maintain rapid short-term response without indefinite directional accumulation.

- Messer, P. W., Ellner, S. P. & Hairston, N. G. Jr. 2016. Can population genetics adapt to rapid evolution? *Trends in Genetics* 32:408–418. DOI: 10.1016/j.tig.2016.04.005.
  - Use for: phenotypic evolution can be rapid and fluctuating direction can reconcile short- and long-term patterns.

- Estes, S. & Arnold, S. J. 2007. Resolving the paradox of stasis: models with stabilizing selection explain evolutionary divergence on all timescales. *The American Naturalist* 169:227–244. DOI: 10.1086/510633.
  - Use for: explicit quantitative-genetic models can reconcile short-term dynamics with long-term stasis.
  - Do not claim: stasis requires an absence of short-term evolution.

- Uyeda, J. C., Hansen, T. F., Arnold, S. J. & Pienaar, J. 2011. The million-year wait for macroevolutionary bursts. *PNAS* 108:15908–15913. DOI: 10.1073/pnas.1014503108.
  - Use for: evolutionary divergence changes character across timescales; long periods of bounded evolution can coexist with rare larger shifts.

### Manuscript boundary

The paper should not ask merely why rapid short-term evolution can coexist with long-term stasis. Its narrower question is whether finite individual information structure constrains which amplitudes, retention regimes, and feedback phases are reachable.

## 2. Information use in evolutionary ecology

### Established

- Dall, S. R. X., Giraldeau, L.-A., Olsson, O., McNamara, J. M. & Stephens, D. W. 2005. Information and its use by animals in evolutionary ecology. *Trends in Ecology & Evolution* 20:187–193. DOI: 10.1016/j.tree.2005.01.010.
  - Use for: information is an explicit evolutionary-ecological currency; animal information use can be analysed with statistical decision theory.
  - Do not claim: introducing information theory/decision theory to evolutionary ecology.

### Candidate distinction

The present framework is not primarily about how much information an animal has. It distinguishes adaptive sequential information use from a fixed one-shot information requirement and uses the gap between them as a structural quantity. The ecological claim depends on the downstream consequence of that finite structure:

`finite sensing task -> structural gap/frontier obligations -> selection or feedback gain -> reachable evolutionary timescales/phases`.

A targeted audit is still required for prior ecological work that explicitly constrains evolution by decision-tree depth, fixed-vs-adaptive test cost, test cover, or finite query arity.

## 3. Eco-evolutionary feedback

### Established

- Post, D. M. & Palkovacs, E. P. 2009. Eco-evolutionary feedbacks in community and ecosystem ecology: interactions between the ecological theatre and the evolutionary play. *Philosophical Transactions of the Royal Society B* 364:1629–1640. DOI: 10.1098/rstb.2009.0012.
  - Use for: reciprocal ecology-evolution feedbacks and organism-induced environmental change.
  - Do not claim: feedback between evolution and ecological state.

- Schoener, T. W. 2011. The newest synthesis: understanding the interplay of evolutionary and ecological dynamics. *Science* 331:426–429. DOI: 10.1126/science.1193954.
  - Use for: ecological and evolutionary dynamics can be reciprocally coupled on overlapping timescales.
  - Do not claim: eco-evolutionary feedback as a novel concept.

### Candidate distinction

The manuscript does not claim novelty for feedback or oscillation in a two-dimensional feedback system. The candidate result is upstream structural reachability: a required feedback regime imposes a minimum or Pareto-minimal finite information structure.

## 4. Temporal autocorrelation and fluctuating environments

### Established

Temporal autocorrelation in environments and selection can alter evolutionary dynamics. This literature must be cited wherever `P`, `r_max`, or temporal filtering is introduced.

Starter reference:

- Cotto, O. & Chevin, L.-M. 2020. Fluctuations in lifetime selection in an autocorrelated environment. *Theoretical Population Biology* 134:119–128. DOI: 10.1016/j.tpb.2020.03.002.

### Candidate distinction

The manuscript does not claim that autocorrelation matters. The structural-temporal theorem combines a finite structural reward ceiling with temporal persistence in one sharp downstream bound, and reward-mode alignment determines which community timescales matter.

## 5. Dynamical-systems results

### Treat as standard mathematics

Do not claim novelty for:

- eigenvalue classification of a two-dimensional local map;
- Jury/Schur stability conditions;
- complex eigenvalues implying damped oscillatory return;
- characteristic-polynomial algebra;
- spectral formulas for reversible Markov chains;
- Popoviciu-type variance bounds;
- Floquet/period-map distinction between neutral and attractive dynamics.

### Candidate composition

The manuscript's use of these results is biological/compositional:

1. finite information structure bounds attainable feedback gain;
2. attainable gain determines which local phases can be reached;
3. complex local modes exclude every zero-feedback decomposition inside the declared generalized model;
4. therefore the finite sensing extremal theory can exclude or permit a regime that has a qualitative mechanistic interpretation.

## 6. Combinatorial prior art

The fixed side overlaps minimum test set / test cover; the adaptive side overlaps optimal decision trees and adaptive query complexity. The bounded-arity extremal formulas must be checked against the exact test-cover / decision-tree literature before submission.

Do not claim novelty for a known extremal formula merely because it is re-derived in repository notation. The ecological contribution can instead be:

`known or independently proved combinatorial extremal result -> exact ecological reachability bound`.

This is a legitimate use of prior mathematics if attribution is explicit.

## 7. Target-journal fit

### Theoretical Ecology

The journal explicitly welcomes theoretical approaches across ecology, including evolutionary ecology and work relying heavily on careful mathematical arguments, provided the questions are ecological and the paper is readable by a broad ecological audience.

Fit requirements for this manuscript:

- lead with the ecological question, not the query-complexity machinery;
- keep four headline theorems only;
- translate `world`, `query`, `arity`, and `productive frontier` into biological meaning before formal definitions;
- move continuation quotients, proof DAGs, exhaustive enumeration, and solver details to Supplement;
- use at least one running natural-history example to make finite sensing states concrete, without turning the paper into an empirical validation paper.

### More ambitious alternative

*The American Naturalist* becomes plausible only if the biological synthesis is made broader and the information-structure result is shown to change how evolutionary stasis/feedback should be conceptualized, not merely to provide mathematical bounds. The current theory is closer to *Theoretical Ecology* in presentation and scope.

## 8. Immediate literature audit still required

Before submission, search specifically for:

1. sequential sampling / sequential decision making in animal behaviour;
2. adaptive information acquisition and cue ordering;
3. ecological applications of decision trees, test cover, or query complexity;
4. bounded cue repertoires and limits to adaptive plasticity/decision making;
5. Markov-switching environments linked to evolutionary selection rewards;
6. information constraints in eco-evolutionary feedback or niche construction;
7. exact prior art for bounded-arity minimum-test-set extremal formulas and adaptivity gaps.

No final novelty claim should be written until these searches are complete.