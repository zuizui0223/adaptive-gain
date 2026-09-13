# Focused novelty audit v0

Date: 2026-09-13

## Scope

This audit is intentionally narrow. It does not ask whether selection, genotype multiplicity, weakest-link epistasis, neutral networks, or reversible mutation-selection balance are novel. They are not.

It asks whether the current search located a direct prior result matching the **composition** of the three candidate-new objects in the routing paper:

1. finite weakest-branch routing layer multiplicity
   `D_r=(q-r+1)^k-(q-r)^k`;
2. the all-layer reduction
   `A_s=(s+1)^k-s^k <= (2^k-1)^s`, with strictness for `k>=2,s>=2`;
3. the resulting exact aggregate-layer trichotomy at
   `theta_c=2^k-1`.

Absence from this targeted search is not proof of literature-wide priority.

## Strong prior-art collisions that narrow the claim

### 1. Reversible stationary weighting is established

Sella & Hirsh (2005) and subsequent weak-mutation work provide the mutation-selection stationary weighting underlying the bridge

`pi(x) proportional to mu(x) fitness(x)^(N-1)`

in the relevant origin-fixation setting.

**Consequence:** do not claim the stationary law, detailed balance, fixation-ratio identity, or neutral-measure factor as new.

### 2. Selection versus sequence multiplicity is explicitly established

Riedel, Khatri, Lässig & Berg (2015), *Multiple-Line Inference of Selection on Quantitative Traits* (Genetics 201:305–322; doi:10.1534/genetics.115.178988), define a locus-specific multiplicity parameter from the relative number of sequence variants representing alternative states. Their low-mutation equilibrium combines selection and multiplicity in the same stationary statistic, citing Iwasa, Berg et al., and Sella & Hirsh.

This is especially important prior art because it makes the abundance/selection competition explicit at equilibrium rather than merely invoking neutral networks qualitatively.

**Consequence:** the routing paper must not claim that it newly shows “multiplicity can oppose selection”, “sequence abundance shifts equilibrium”, or “fitness alone does not determine stationary phenotype frequency.”

### 3. Weakest-link `min` fitness is explicit recent prior art

Labourel, Bansept & McCandlish, *Weakest link epistasis and the geometry of genetic load*, bioRxiv version 2 posted January 27, 2026 (doi:10.64898/2025.12.08.693057), define organismal fitness by the minimum of trait-specific fitness components and analyze direct population-genetic consequences, including the expansion of neutral/masked mutational effects.

**Consequence:** do not claim the `min` map, weakest-link epistasis, masking, or its population-genetic use as new.

### 4. Robustness / survival-of-the-flattest is established

Wilke et al. and the broader neutral-network/error-threshold literature establish that a lower-fitness but more mutationally robust or numerous region can dominate evolutionary outcomes.

**Consequence:** “selection must overcome degeneracy” is interpretation, not novelty.

## Exact-object searches run

Targeted web searches included combinations of:

- `(s+1)^k - s^k` with genotype, fitness, minimum, weakest link;
- `2^k-1` with stationary mode, genotype multiplicity, selection;
- nested subsets with genotype multiplicity, selection, weakest link;
- branch-product routing genotype with minimum fitness.

The searches recovered the prior-art classes above, especially weakest-link epistasis and general selection–multiplicity stationary theory, but did not locate a direct source stating the routing-paper composition:

`finite branch-product min representation`

`-> exact gain-layer counts`

`-> nested-chain all-layer bound`

`-> exact aggregate-mode threshold 2^k-1`

`-> exact two-layer tie at equality`.

Again, this is a targeted negative search result, not proof that no such theorem exists.

## What is potentially new versus merely elementary

The formula

`(s+1)^k-s^k`

is an elementary count and should not be sold as a newly discovered combinatorial identity.

Likewise, the inequality

`A_s<=(2^k-1)^s`

has a short elementary injection/counting proof. Its isolated mathematical difficulty is not the novelty claim.

The strongest candidate contribution is the **exact composition**:

1. a declared finite routing genotype-policy representation generates this specific layer hierarchy;
2. the adjacent layer controls every lower layer;
3. standard selection weighting therefore yields a necessary-and-sufficient aggregate-layer transition with an exact equality structure;
4. representation and neutral-measure counterexamples delimit precisely when that transition can and cannot be exported.

This should be described as a finite representation result, not as a deep new theorem in pure combinatorics or a new population-genetic law.

## Current novelty confidence

### High confidence that these are prior art

- weak-mutation reversible stationary weighting;
- selection plus multiplicity in equilibrium distributions;
- weakest-link/minimum fitness maps;
- robustness/abundance opposing fitness;
- representation dependence and mutation bias in general.

### Moderate confidence as candidate-new composition

- the routing-specific exact layer hierarchy plus adjacent-obstruction reduction;
- the `theta_c=2^k-1` necessary-and-sufficient aggregate gain-layer threshold for this representation;
- the exact `{q-1,q}` equality tie combined with the representation/mutation-measure claim ceiling.

The confidence is **moderate**, not high, until mathematical and population-genetic literature searches are expanded beyond keyword/web retrieval.

## Manuscript consequence

The Abstract and Introduction should use formulations such as:

> For this finite routing representation, we derive...

> The routing-specific layer hierarchy yields...

> Combining the exact multiplicities with the standard origin-fixation stationary law gives...

Avoid:

> We introduce a new selection–multiplicity principle...

> We discover a new form of weakest-link epistasis...

> We show for the first time that suboptimal genotype abundance can overwhelm selection...

## Next novelty gate

Before submission, perform one dedicated scholarly pass over:

1. mathematical inequalities for forward differences of powers and nested multichains;
2. discrete order-statistic / minimum-coordinate occupancy models;
3. mutation-selection models with phenotype degeneracy classes and exact modal thresholds;
4. quasispecies / neutral-network threshold results that might produce algebraically identical finite-class transitions.

A direct collision with the exact threshold composition should trigger reframing before any journal selection or priority wording is frozen.