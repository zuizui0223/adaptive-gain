# Literature positioning and novelty boundary

## Purpose

This file records the ecological/evolutionary and combinatorial literature boundary for the manuscript. It is intentionally conservative: standard results are cited as prior art rather than repackaged as novelty. The more detailed search history is recorded in `PRIOR_ART_AUDIT_V2.md` and `FINAL_PRIORITY_SEARCH_LOG.md`.

## 1. Rapid evolution and evolutionary time

Established theory already shows that ecological and evolutionary processes can operate on overlapping timescales, that selection can fluctuate strongly, and that rapid short-term change can coexist with long periods of bounded or weak net divergence.

Core anchors:

- Hairston et al. 2005 — rapid evolution and convergence of ecological/evolutionary time;
- Estes & Arnold 2007 — stabilizing-selection models and stasis across timescales;
- Bell 2010 — strong fluctuating selection;
- Uyeda et al. 2011 — scale-dependent evolutionary divergence;
- Messer, Ellner & Hairston 2016 — rapid short-term evolution and long-term interpretation.

### Boundary

Do not claim novelty for rapid evolution, the coexistence of short-term activity and long-term stasis, temporal cancellation, or evolutionary-timescale overlap.

The paper asks instead whether finite individual information structure constrains which evolutionary amplitudes, retention regimes, and feedback phases are reachable.

## 2. Information use and information-processing constraints

Information acquisition and use are established topics in evolutionary ecology.

Core anchors:

- Dall et al. 2005 — information use as an evolutionary-ecological decision problem;
- Schmidt et al. 2010 — ecology of information and informed decisions;
- Dukas 2004 — limited attention / information-processing rate as an evolutionary-ecological constraint;
- Wright 2022 — sampling effort, memory, cue reliability, temporal autocorrelation, and plasticity.

### Boundary

Do not claim novelty for sequential cue use, sampling, state-dependent decisions, memory, learning, cue reliability, limited attention, or the broad idea that information constraints can limit adaptive/evolutionary response.

The candidate distinction is the exact downstream composition

`finite discrete sensing complexity -> structural ceiling -> evolutionary reachability ceiling`.

## 3. Eco-evolutionary feedback and temporal recurrence

Generic reciprocal eco-evolutionary feedback is prior art (Post & Palkovacs 2009; Schoener 2011 and later literature). Temporal autocorrelation and Markov-switching environmental effects on evolution are also established; Cotto & Chevin 2020 is one relevant anchor.

### Boundary

Do not claim novelty for feedback, oscillation, environmental persistence, temporal autocorrelation, or state-dependent selection.

The candidate composition is narrower: structurally generated rewards and temporal recurrence are indexed by the same finite community-state space, which allows finite information bounds and temporal persistence to enter one exact downstream ceiling.

## 4. Fixed information: separating systems / minimum test set / test cover

The fixed identification problem is classical. Minimum test collection, minimum test set, test cover, and separating-system literatures already study the minimum set of tests required to distinguish finite entities.

Relevant anchors include Halldórsson et al., Katona 1966, Wegener 1979, and Crowston et al. 2016.

### Important distinction

Classical `bounded test size` limits the number of items contained in a separating subset. The repository's query arity `b` instead limits the number of possible outcomes of one query. These restrictions must not be cited as equivalent.

## 5. Adaptive information: optimal and multiway decision trees

Adaptive identification by decision trees is classical. Hyafil & Rivest 1976, Adler & Heeringa, Gupta/Nagarajan/Ravi, Chakaravarthy et al. 2009, Moshkov and others cover binary/multiway decision trees, adaptive search, and complexity. Adaptivity gaps are likewise established terminology.

### Boundary

Do not claim novelty for adaptive sequencing, decision-tree depth, binary or multiway queries, bounded outcome arity as a modelling idea, adaptive outperforming fixed acquisition, or generic adaptivity gaps.

The manuscript treats this machinery as imported or independently re-derived structure.

## 6. Bounded-arity extremal formulas are not a novelty claim

The repository recurrence `F_b(n,h)` is an elementary rooted-tree extremal count under leaf, depth, and out-degree constraints, combined with separating-test witness constructions. An exact published formula in identical notation is not required for the manuscript's contribution.

No novelty claim should depend on the priority of `F_b`, its endpoint formulas, private-pair constructions, or the sharp adaptive/fixed ratios. They are supporting combinatorial machinery.

## 7. Productive frontier

`Productive frontier` is repository terminology for the irreducible separation obligations retained by the declared fixed-cost problem. No exact published synonym has been established, but this is not used as a priority claim.

In the ecological paper, productive frontier appears only where its edge count has downstream weight: a cap on irreducible obligations caps fixed information burden, structural gap, and therefore reachable feedback gain. Rank alone does not provide the same bound.

## 8. Dynamical-systems mathematics

Treat the following as standard mathematics:

- Jury/Schur stability;
- eigenvalue classification;
- complex eigenvalues and damped oscillation;
- characteristic-polynomial algebra;
- reversible Markov spectral formulas;
- variance range bounds;
- neutral versus attractive return maps.

The paper's contribution is not any of these ingredients separately.

## 9. Submission-safe novelty statement

Use wording close to:

> Evolutionary ecology already treats information acquisition, sampling, memory, and information-processing limits as factors shaping adaptive decisions and evolutionary responses. Test theory and computer science separately characterize separating systems, adaptive and multiway decision trees, and adaptivity gaps, while fluctuating-selection and eco-evolutionary theory already explain temporal cancellation and restoring feedback. We do not claim novelty for these components or for the bounded-arity tree extremal formulas used internally. Our contribution is their exact ecological composition: finite sensing complexity bounds structurally generated selection, recurrence of the same community states filters those rewards through time, and required dynamical regimes imply minimum or Pareto-minimal finite information structures. Thus declared finite information structure restricts which evolutionary fluctuations and local feedback phases are reachable within the model class.

Avoid `first`, `first-ever`, `no previous theory`, or analogous priority language.

## 10. Status of the priority audit

The broad prior-art audit is complete enough to draft the manuscript conservatively.

Targeted searches found many neighboring theories — cognitive constraints, costly sampling, plasticity, cue integration, fluctuating environments, and eco-evolutionary feedback — but did not identify a direct predecessor with the full exact chain

`finite decision/separation complexity`
`-> exact structural selection / feedback ceiling`
`-> recurrence of the same state-indexed rewards`
`-> sharp long-run fluctuation ceiling or minimum/Pareto-minimal information complexity for a feedback phase`.

This search result is not proof of priority. One final pre-submission database search should still be performed, but no unresolved mathematical-priority question needs to block manuscript drafting.

See:

- `manuscript/PRIOR_ART_AUDIT_V2.md`
- `manuscript/FINAL_PRIORITY_SEARCH_LOG.md`
- `manuscript/NOVELTY_PARAGRAPH_V1.md`

## 11. Target-journal fit

### Theoretical Ecology

The manuscript should:

- lead with the ecological reachability question rather than query-complexity machinery;
- keep four headline theorems only;
- translate `world`, `query`, `arity`, and `productive frontier` into ecological meanings before formal definitions;
- move continuation quotients, proof DAGs, exhaustive enumeration, and solver details to Supplement;
- use natural-history motivation only to make the finite-state model biologically intelligible, not to turn the paper into an observation-design or empirical-methods paper.

### More ambitious alternative

The American Naturalist would require a broader biological synthesis showing that the theory changes how stasis and eco-evolutionary feedback should be conceptualized. The current manuscript remains better matched to Theoretical Ecology.
