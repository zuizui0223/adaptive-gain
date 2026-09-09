# Literature positioning and novelty boundary

## Purpose

This file records the ecological/evolutionary and combinatorial literature boundary for the manuscript. It is intentionally conservative: standard results should be cited as prior art rather than repackaged as novelty.

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

## 2. Information use and sequential decision making in evolutionary ecology

### Established

- Dall, S. R. X., Giraldeau, L.-A., Olsson, O., McNamara, J. M. & Stephens, D. W. 2005. Information and its use by animals in evolutionary ecology. *Trends in Ecology & Evolution* 20:187–193. DOI: 10.1016/j.tree.2005.01.010.
  - Use for: information is an explicit evolutionary-ecological currency; animal information use can be analysed with statistical decision theory.
  - Do not claim: introducing information/decision theory to evolutionary ecology.

- Schmidt, K. A., Dall, S. R. X. & van Gils, J. A. 2010. The ecology of information: an overview on the ecological significance of making informed decisions. *Oikos*.
  - Use for: acquisition, processing, decision making, and ecological consequences are already treated as one ecological topic.
  - Do not claim: first connection between information use and population/community/ecosystem consequences.

- Movement and foraging literatures already treat repeated information acquisition, context/state dependence, and feedback between action and subsequent information acquisition.
  - Do not claim: sequential cue use, repeated sampling, or cue ordering as the paper-level novelty.

### Candidate distinction

The present framework is not primarily about how much information an animal has or whether it samples sequentially. It distinguishes a finite adaptive identification cost from the corresponding fixed separating-test requirement and then uses the resulting structural constraints downstream.

The ecological claim is:

`finite sensing task -> structural gap/frontier obligations -> selection or feedback gain -> reachable evolutionary timescales/phases`.

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

## 5. Fixed information side: minimum test set / test cover

### Established

The fixed identification problem is a standard minimum test collection / minimum test set / test cover problem: choose a smallest subset of tests whose signatures distinguish every item.

Relevant anchors:

- Halldórsson, Halldórsson & Ravi (2001), cited throughout later minimum-test-collection literature.
- Crowston, Gutin, Jones, Saurabh & Yeo. 2012/2013. Parameterized Study of the Test Cover Problem.
- later stochastic test-collection literature explicitly describes minimum test collection/test set/test cover as well studied.

### Do not claim

- novelty for the pair-separation formulation;
- novelty for minimum separating-test collections;
- generic test-cover hardness/approximation behavior;
- novelty for using test signatures to distinguish finite states.

The fixed side should be presented as imported/independently re-derived combinatorial machinery.

## 6. Adaptive information side: optimal decision trees and adaptivity gaps

### Established

Adaptive identification by decision trees is classical.

- Hyafil, L. & Rivest, R. L. 1976. Constructing optimal binary decision trees is NP-complete. *Information Processing Letters* 5:15–17.
- Adler, M. & Heeringa, B. 2012. Approximating optimal binary decision trees. *Algorithmica* 62:1112–1121.
- Gupta, Nagarajan & Ravi: approximation algorithms for optimal decision trees and adaptive search problems.
- Moshkov and collaborators: extensive test-theory / information-system treatment of tests, decision trees, rules, and complexity.

The computer-science literature also explicitly uses the term `adaptivity gap` for comparisons between adaptive and non-adaptive strategies.

### Do not claim

- novelty for adaptive test sequencing;
- novelty for decision-tree depth as an information-acquisition cost;
- novelty for adaptive outperforming non-adaptive;
- generic adaptivity gaps;
- generic binary-tree counting or decision-tree complexity.

### Candidate ecological use

The ecological contribution begins after the static gap is treated as an upstream structural coordinate and composed with evolutionary dynamics:

`required dynamical regime -> required structural gap -> minimum/Pareto-minimal finite information structure`.

## 7. Dynamical-systems results

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
4. finite sensing extremal theory can therefore exclude or permit a regime with a qualitative mechanistic interpretation.

## 8. Strongest defensible novelty statement

Use wording close to:

> Evolutionary ecology already treats information acquisition as an adaptive decision problem, while computer science and test theory separately characterize the costs of fixed separating test sets and adaptive decision trees. Fluctuating selection and eco-evolutionary feedback likewise already explain how rapid short-term change can fail to accumulate or can be dynamically restored. Our contribution lies in composing these previously separate levels. We show that finite information structure places exact ceilings on structurally generated selection, that those ceilings combine with community persistence to bound long-run evolutionary fluctuation, and that a required feedback regime implies a minimum or Pareto-minimal finite information structure. Thus the combinatorial structure of individual information use restricts which evolutionary timescales and local feedback phases are reachable.

Do not replace `our contribution lies in composing` with `for the first time` until the remaining audit supports it.

## 9. Target-journal fit

### Theoretical Ecology

Fit requirements for this manuscript:

- lead with the ecological reachability question, not query-complexity machinery;
- keep four headline theorems only;
- translate `world`, `query`, `arity`, and `productive frontier` into biological meaning before formal definitions;
- move continuation quotients, proof DAGs, exhaustive enumeration, and solver details to Supplement;
- use at least one running natural-history example to make finite sensing states concrete without turning the paper into an empirical validation paper.

### More ambitious alternative

*The American Naturalist* becomes plausible only if the biological synthesis is shown to change how evolutionary stasis/feedback should be conceptualized, not merely to provide mathematical bounds. The current theory is closer to *Theoretical Ecology* in presentation and scope.

## 10. Remaining audit before submission

The broad boundary is now established. The remaining checks are narrow:

1. exact equivalence, if any, between the repository bounded-arity extremal formulas and published test-theory results;
2. whether the productive-frontier edge lower bound has an established equivalent under another name;
3. ecological/evolutionary theory that maps finite cue repertoire or decision-tree complexity to a ceiling on evolutionary response;
4. models in which selection reward and environmental/community recurrence are generated on the same finite state space and jointly bounded rather than independently parameterized.

Until those four checks are complete, novelty should be stated as a conservative synthesis/reachability contribution rather than a first-ever theorem claim.