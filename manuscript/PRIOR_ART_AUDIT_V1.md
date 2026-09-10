# Prior-art audit v1

## Purpose

This audit narrows the manuscript novelty boundary. It is intentionally conservative. The manuscript should not claim novelty for animal information use, sequential/adaptive decision making, eco-evolutionary feedback, fluctuating selection, minimum test cover, optimal decision trees, or generic adaptivity gaps.

## A. Evolutionary ecology of information

### Established prior art

- Dall, S. R. X., Giraldeau, L.-A., Olsson, O., McNamara, J. M. & Stephens, D. W. 2005. Information and its use by animals in evolutionary ecology. Trends in Ecology & Evolution 20:187–193. DOI: 10.1016/j.tree.2005.01.010.
  - Already frames information acquisition/use as an evolutionary-ecological decision problem and explicitly advocates statistical decision theory.
  - Therefore do not claim novelty for bringing information, utility, or decision theory into evolutionary ecology.

- Schmidt, K. A., Dall, S. R. X. & van Gils, J. A. 2010. The ecology of information: an overview on the ecological significance of making informed decisions. Oikos 119.
  - Treats information acquisition, decision making, and ecological consequences as an integrated ecological topic.
  - Therefore do not claim novelty for connecting informed decisions to population/community/ecosystem consequences.

- Movement and foraging literatures already treat repeated information acquisition, state/context dependence, and feedback between movement and information acquisition.
  - Therefore sequential cue use, repeated sampling, and state-dependent cue integration are background rather than headline contributions.

### Remaining candidate distinction

The manuscript does not ask whether organisms use information adaptively. It asks whether a finite information structure places exact ceilings on the evolutionary amplitudes, temporal fluctuation strength, and feedback phases that are reachable downstream.

The candidate contribution is therefore a reachability map:

`finite sensing structure -> structural gap / productive obligations -> selection or feedback gain -> reachable evolutionary timescale or local phase`.

## B. Eco-evolutionary feedback and evolutionary time

### Established prior art

- Hairston et al. 2005: ecological and evolutionary dynamics can operate on overlapping timescales.
- Estes & Arnold 2007: stabilizing-selection models reconcile short-term dynamics with long-term stasis.
- Bell 2010: fluctuating selection can be strong and directionally variable.
- Uyeda et al. 2011: evolutionary divergence changes character across temporal scales.
- Messer, Ellner & Hairston 2016: rapid short-term change does not imply comparable long-term accumulation.
- Post & Palkovacs 2009 and Schoener 2011: reciprocal eco-evolutionary feedback is established.

### Consequence for claims

Do not headline:

- rapid short-term evolution with long-term stasis;
- temporal cancellation of selection;
- ecological-timescale evolution;
- generic eco-evolutionary feedback;
- oscillations or Jury/Schur stability conditions.

The manuscript instead uses these established dynamics as downstream regimes whose reachability is constrained by upstream finite information structure.

## C. Fixed information side: minimum test set / test cover

### Established prior art

The fixed identification problem overlaps the minimum test collection / minimum test set / minimum test cover literature: choose the smallest subset of tests whose outcome vectors distinguish all entities. This problem is well established and has a substantial approximation, parameterized-complexity, and operations-research literature.

Relevant anchors include:

- Halldórsson, Halldórsson & Ravi (2001), as cited in later minimum-test-collection literature.
- Crowston et al. 2012/2013, Parameterized Study of the Test Cover Problem.
- later stochastic test-collection work explicitly treating minimum test set/test cover as established prior art.

### Consequence for claims

Do not claim novelty for:

- defining the fixed separating-test problem;
- the pair-separation / hitting-set formulation itself;
- hardness or approximation behavior of generic test cover;
- using a minimum test collection to distinguish finite states.

The fixed side is an imported or independently re-derived combinatorial ingredient.

## D. Adaptive information side: optimal decision trees

### Established prior art

Adaptive identification by a decision tree is classical. Hyafil & Rivest (1976) established NP-completeness of constructing optimal binary decision trees. Later work develops approximation algorithms and adaptive search formulations; Gupta, Nagarajan & Ravi and Adler & Heeringa are useful anchors.

Moshkov and collaborators provide a broad test-theory / information-system framework for decision trees, tests, rules, and complexity, including depth and time-space classifications.

### Consequence for claims

Do not claim novelty for:

- adaptive test sequencing;
- decision-tree depth as an information-acquisition cost;
- the existence of an adaptivity advantage;
- generic adaptivity gaps;
- standard binary-tree counting or decision-tree complexity facts.

The manuscript may use exact or independently proved bounded-arity extremal formulas, but attribution must be explicit wherever an equivalent result is known.

## E. Adaptivity gap boundary

The computer-science literature already compares adaptive and non-adaptive strategies and uses the term adaptivity gap. Therefore the statement `adaptive can outperform fixed` is prior art.

The ecological contribution begins only after the static gap is treated as an upstream structural coordinate and composed with evolutionary dynamics. The manuscript-level novelty candidate is:

> A required evolutionary dynamical regime implies a required structural gap, which in turn implies a minimum or Pareto-minimal finite information structure.

For bounded query arity, this gives a downstream ecological interpretation to known/independently proved extremal combinatorics without claiming the combinatorial theorem itself as new.

## F. Strongest defensible novelty paragraph

The manuscript should use a paragraph close to the following:

> Evolutionary ecology already treats information acquisition as an adaptive decision problem, while computer science and test theory separately characterize the costs of fixed separating test sets and adaptive decision trees. Likewise, fluctuating selection and eco-evolutionary feedback already explain how rapid short-term change can fail to accumulate or can be dynamically restored. Our contribution lies in composing these previously separate levels. We show that finite information structure places exact ceilings on structurally generated selection, that those ceilings combine with community persistence to bound long-run evolutionary fluctuation, and that a required feedback regime implies a minimum or Pareto-minimal information structure. Thus the combinatorial structure of individual information use restricts which evolutionary timescales and local feedback phases are reachable; neither generic information use, adaptivity, nor feedback itself is claimed as novel.

## G. Remaining audit before submission

Still verify carefully before final novelty language:

1. exact equivalence, if any, between the repository bounded-arity extremal formulas and published test-theory results;
2. whether the productive-frontier edge lower bound has an established equivalent under another name;
3. ecological theory that explicitly bounds evolutionary response using a finite cue repertoire or finite decision-tree depth;
4. models in which selection reward and environmental/community recurrence are generated on the same finite state space and jointly bounded rather than independently parameterized.

Until those four checks are complete, novelty should be stated as a candidate synthesis/reachability result, not as a first-ever theorem claim.