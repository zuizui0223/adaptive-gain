# Literature positioning and novelty boundary

## Purpose

This file records the ecological/evolutionary, information-theoretic, and combinatorial literature boundary for the manuscript. It is intentionally conservative: standard results and close conceptual predecessors are cited as prior art rather than repackaged as novelty. The more detailed search history is recorded in `PRIOR_ART_AUDIT_V2.md` and `FINAL_PRIORITY_SEARCH_LOG.md`.

## 1. Rapid evolution and evolutionary time

Established theory already shows that ecological and evolutionary processes can operate on overlapping timescales, that selection can fluctuate strongly, and that rapid short-term change can coexist with long periods of bounded or weak net divergence.

Core anchors:

- Hairston et al. 2005 — rapid evolution and convergence of ecological/evolutionary time;
- Estes & Arnold 2007 — stabilizing-selection models and stasis across timescales;
- Bell 2010 — strong fluctuating selection;
- Uyeda et al. 2011 — scale-dependent evolutionary divergence;
- Messer, Ellner & Hairston 2016 — rapid short-term evolution and long-term interpretation;
- Cotto & Chevin 2020 — selection in autocorrelated environments.

### Boundary

Do not claim novelty for rapid evolution, the coexistence of short-term activity and long-term stasis, temporal cancellation, temporal autocorrelation, or evolutionary-timescale overlap.

The paper asks instead how a declared finite decision/separation structure restricts the evolutionary regimes reachable downstream.

## 2. Information use and information-processing constraints

Information acquisition and use are established topics in evolutionary ecology.

Core anchors:

- Dall et al. 2005 — information use as an evolutionary-ecological decision problem;
- Schmidt et al. 2010 — ecology of information and informed decisions;
- Dukas 2004 — limited attention / information-processing rate as an evolutionary-ecological constraint;
- Trimmer & Houston 2014 — evolutionary shaping of information-processing and decision mechanisms;
- Eliassen et al. 2016 — explicit proximate sensing/information-processing architecture embedded in evolutionary modelling;
- Wright et al. 2022 — sampling effort, memory, cue reliability, temporal autocorrelation, and plasticity.

### Boundary

Do not claim novelty for sequential cue use, sampling, state-dependent decisions, memory, learning, cue reliability, limited attention, proximate sensing architecture, or the broad idea that information constraints can limit adaptive/evolutionary response.

## 3. Fitness value of information and minimum informational requirements

The final targeted search identified a closer mathematical literature than the earlier audit had emphasized.

- Donaldson-Matasci, Bergstrom & Lachmann 2010 formalize the fitness value of environmental information and its relation to long-run growth.
- Rivoire & Leibler 2011 develop information-fitness relations for populations in varying environments.
- Moffett & Eckford 2022 use rate-distortion theory to ask explicitly for the minimal information needed to achieve a specified growth rate and the minimal information gain needed to achieve a specified average selection coefficient.
- de Boer & Hogeweg 2010 study an evolutionary information threshold for coding structure in eco-evolutionary dynamics.

### Boundary

Do not claim novelty for the fitness value of information, information-fitness bounds, minimum mutual-information requirements for target fitness or selection, or generic evolutionary information thresholds. In particular, do not use an unqualified phrase such as `the first minimum-information requirement for evolutionary dynamics`.

### Distinction used in this manuscript

The manuscript does **not** minimize Shannon information or channel rate. It minimizes a discrete finite decision/separation architecture under a declared deterministic task: represented alternatives `n`, declared cues `m`, irreducible fixed-side obligations `E`, adaptive depth, and cue outcome arity. The principal ecological composition is

`required local feedback regime`
`-> required adaptive/fixed structural gap`
`-> minimum or Pareto-minimal finite decision/separation structure (n,m,E)`.

Moffett & Eckford 2022 is therefore the closest reverse-direction mathematical precursor found, but it minimizes a different information object for a different downstream target.

## 4. Eco-evolutionary feedback and temporal recurrence

Generic reciprocal eco-evolutionary feedback is prior art (Post & Palkovacs 2009; Schoener 2011 and later literature). Temporal autocorrelation and Markov-switching environmental effects on evolution are also established; Cotto & Chevin 2020 is one relevant anchor.

### Boundary

Do not claim novelty for feedback, oscillation, environmental persistence, temporal autocorrelation, or state-dependent selection.

The candidate composition is narrower: structurally generated rewards and temporal recurrence are indexed by the same finite community-state space, which allows the discrete structural bounds and temporal persistence to enter one downstream envelope and reachability map.

## 5. Fixed information: separating systems / minimum test set / test cover

The fixed identification problem is classical. Minimum test collection, minimum test set, test cover, and separating-system literatures already study the minimum set of tests required to distinguish finite entities.

Relevant anchors include Katona 1966, Wegener 1979, Crowston et al. 2016 and related work.

### Important distinction

Classical `bounded test size` limits the number of items contained in a separating subset. The repository's query arity `b` instead limits the number of possible outcomes of one query. These restrictions must not be cited as equivalent.

## 6. Adaptive information: optimal and multiway decision trees

Adaptive identification by decision trees is classical. Hyafil & Rivest 1976 and Chakaravarthy et al. 2009 provide direct binary/multiway anchors; broader adaptive-search and decision-tree literatures cover related complexity and adaptivity questions.

### Boundary

Do not claim novelty for adaptive sequencing, decision-tree depth, binary or multiway queries, bounded outcome arity as a modelling idea, adaptive outperforming fixed acquisition, or generic adaptivity gaps.

The manuscript treats this machinery as imported or independently re-derived structure.

## 7. Bounded-arity extremal formulas are not a novelty claim

The repository recurrence `F_b(n,h)` is an elementary rooted-tree extremal count under leaf, depth, and out-degree constraints, combined with separating-test witness constructions. An exact published formula in identical notation is not required for the manuscript's contribution.

No novelty claim should depend on the priority of `F_b`, its endpoint formulas, private-pair constructions, or the sharp adaptive/fixed ratios. They are supporting combinatorial machinery.

## 8. Productive frontier

`Productive frontier` is repository terminology for the irreducible separation obligations retained by the declared fixed-cost problem. No exact published synonym has been established, but this is not used as a priority claim.

In the ecological paper, productive frontier appears only where its edge count has downstream weight: a cap on irreducible obligations caps fixed information burden, structural gap, and therefore reachable feedback gain. Rank alone does not provide the same bound.

## 9. Dynamical-systems mathematics

Treat the following as standard mathematics:

- Jury/Schur stability;
- eigenvalue classification;
- complex eigenvalues and damped oscillation;
- characteristic-polynomial algebra;
- reversible Markov spectral formulas;
- variance range bounds;
- neutral versus attractive return maps.

The paper's contribution is not any of these ingredients separately.

## 10. Submission-safe novelty statement

Use wording close to:

> Existing theory already connects environmental information to fitness and even derives minimal mutual-information requirements for target growth or selection, while evolutionary ecology treats information-processing constraints and sensing architectures as evolving mechanisms. Test theory and computer science separately characterize separating systems, adaptive and multiway decision trees, and adaptivity gaps; fluctuating-selection and eco-evolutionary theory already cover temporal recurrence and feedback. We do not claim novelty for those components. Our contribution is a narrower discrete ecological composition: a declared finite deterministic decision/separation architecture bounds structurally generated selection, recurrence of the same community states filters those rewards through time, and a required local feedback regime implies a minimum or Pareto-minimal structural requirement over represented alternatives, declared cues, and irreducible obligations.

Avoid `first`, `first-ever`, `no previous theory`, or analogous priority language.

## 11. Status of the priority audit

The targeted pre-submission search was completed on 2026-09-10. The most important additional mathematical precursor is Moffett & Eckford (2022), because it already reverses the usual information-to-fitness direction and derives minimum mutual-information requirements for target growth and selection. Donaldson-Matasci et al. (2010) and Rivoire & Leibler (2011) anchor the broader fitness-value-of-information literature; de Boer & Hogeweg (2010) anchors evolutionary information-threshold work. Trimmer & Houston (2014) and Eliassen et al. (2016) remain close architecture-level precursors.

The search did not identify an exact predecessor with the full discrete chain

`finite deterministic decision/separation structure`
`-> adaptive/fixed structural gap`
`-> state-indexed selection or feedback gain`
`-> required local feedback phase`
`-> minimum/Pareto-minimal (n,m,E) structure`,

nor one composing that structural object with the reversible reward-mode envelope used here.

This is not proof of priority. It supports a narrow structural distinction and conservative wording, not a categorical novelty claim.

See:

- `manuscript/PRIOR_ART_AUDIT_V2.md`;
- `manuscript/FINAL_PRIORITY_SEARCH_LOG.md`;
- `manuscript/NOVELTY_PARAGRAPH_V1.md`.

## 12. Target-journal fit

### Theoretical Ecology

The manuscript should:

- lead with the ecological reachability question rather than query-complexity machinery;
- make the principal reachability theorem visually and rhetorically dominant;
- name its object precisely as a finite decision/separation structure rather than generic `information` when making novelty comparisons;
- retain the structural-temporal envelope and feedback-existence result as supporting/diagnostic theorems, and the stasis distinction as a mechanistic proposition rather than a coequal theorem headline;
- translate `world`, `query`, `arity`, and `productive frontier` into ecological meanings before formal definitions;
- move continuation quotients, proof DAGs, exhaustive enumeration, and solver details to Supplement;
- use natural-history motivation only to make the finite-state model biologically intelligible, not to turn the paper into an observation-design or empirical-methods paper.

### More ambitious alternative

The American Naturalist would require a broader biological synthesis showing that the theory changes how stasis and eco-evolutionary feedback should be conceptualized. The current manuscript remains better matched to Theoretical Ecology.
