# Focused novelty audit v0

Date: 2026-09-13

## Scope

This audit is intentionally narrow. It does not ask whether selection, genotype multiplicity, weakest-link epistasis, neutral networks, reversible mutation-selection balance, representation-dependent thresholds, or phenotype-level error thresholds are novel. They are not.

It asks whether the current search located a direct prior result matching the **composition** of the candidate-new objects in the routing paper:

1. finite weakest-branch routing layer multiplicity
   `D_r=(q-r+1)^k-(q-r)^k`;
2. the all-layer reduction
   `A_s=(s+1)^k-s^k <= (2^k-1)^s`, with strictness for `k>=2,s>=2`;
3. the resulting exact aggregate-layer trichotomy at
   `theta_c=2^k-1`;
4. the paired stationary-majority result
   `T_k < theta_1/2(q,k) < 2T_k` for `q>=2`, including the canonical `a=2` separation `N_unique_mode=q+2` versus `N_majority=q+3`.

Absence from this targeted search is not proof of literature-wide priority.

## Strong prior-art collisions that narrow the claim

### 1. Reversible stationary weighting is established

Sella & Hirsh (2005) and subsequent weak-mutation work provide the mutation-selection stationary weighting underlying

`pi(x) proportional to mu(x) fitness(x)^(N-1)`

in the relevant origin-fixation setting.

**Consequence:** do not claim the stationary law, detailed balance, fixation-ratio identity, or neutral-measure factor as new.

### 2. Selection versus sequence multiplicity is explicitly established

Riedel, Khatri, Lässig & Berg (2015), *Multiple-Line Inference of Selection on Quantitative Traits* (Genetics 201:305–322; doi:10.1534/genetics.115.178988), define a locus-specific multiplicity parameter from the relative number of sequence variants representing alternative states. Their low-mutation equilibrium combines selection and multiplicity in the same stationary statistic, citing Iwasa, Berg et al., and Sella & Hirsh.

**Consequence:** the routing paper must not claim that it newly shows “multiplicity can oppose selection”, “sequence abundance shifts equilibrium”, or “fitness alone does not determine stationary phenotype frequency.”

### 3. Weakest-link `min` fitness is explicit recent prior art

Labourel, Bansept & McCandlish, *Weakest link epistasis and the geometry of genetic load*, bioRxiv version 2 posted January 27, 2026 (doi:10.64898/2025.12.08.693057), define organismal fitness by the minimum of trait-specific fitness components and analyze mutation-selection-drift consequences.

**Consequence:** do not claim the `min` map, weakest-link epistasis, masking, or its population-genetic use as new.

### 4. Robustness / survival-of-the-flattest is established

Wilke et al. and broader neutral-network/error-threshold literature establish that a lower-fitness but more mutationally robust or numerous region can dominate evolutionary outcomes.

**Consequence:** “selection must overcome degeneracy” is interpretation, not novelty.

### 5. Genotype–phenotype redundancy can move evolutionary thresholds

Quasispecies literature explicitly treats error thresholds as dependent on neutral-network breadth and genotype-to-phenotype redundancy. Wilke's *Quasispecies Made Simple* describes error thresholds shifting as lower-fitness neutral networks broaden, and phenotype-level error-threshold work coarse-grains many genotypes into a phenotype before analyzing its persistence. Reviews of viral evolution likewise distinguish sequence-level from phenotype-level thresholds and note that degeneracy of the genotype–phenotype map changes the threshold.

This literature is dynamically different from the present weak-mutation origin-fixation model, but it closes another broad novelty route.

**Consequence:** do not claim that this paper newly shows “representation changes an evolutionary threshold” or “phenotypic redundancy can preserve or displace a fitter state.” The candidate contribution must remain the exact finite routing-specific threshold composition.

## Exact-object searches run

Targeted searches included combinations of:

- `(s+1)^k - s^k` with genotype, fitness, minimum, weakest link;
- `2^k-1` with stationary mode, genotype multiplicity, selection;
- nested subsets with genotype multiplicity, selection, weakest link;
- branch-product routing genotype with minimum fitness;
- majority / half-mass thresholds for finite phenotype-degeneracy classes;
- quasispecies and neutral-network thresholds with exact finite class multiplicities;
- phenotype-level error thresholds and genotype–phenotype redundancy;
- forward differences of powers and nested multichains.

The searches recovered the prior-art classes above but did not locate a direct source stating the routing-paper composition:

`finite branch-product min representation`

`-> exact gain-layer counts`

`-> nested-chain all-layer bound`

`-> exact aggregate-mode threshold 2^k-1`

`-> exact two-layer tie at equality`

`-> distinct unique stationary-majority threshold inside (T_k,2T_k)`.

This remains a targeted negative search result, not proof that no such theorem exists.

## What is potentially new versus merely elementary

The formula

`(s+1)^k-s^k`

is an elementary count and should not be sold as a newly discovered combinatorial identity.

Likewise, the inequality

`A_s<=(2^k-1)^s`

has a short elementary counting proof, and the existence of a half-mass threshold for a monotone finite partition function is not novel by itself.

The strongest candidate contribution is the **exact composition**:

1. a declared finite routing genotype-policy representation generates this specific layer hierarchy;
2. the adjacent layer controls every lower layer;
3. standard weak-mutation selection weighting therefore yields a necessary-and-sufficient aggregate-mode transition with an exact equality structure;
4. the same global bound places the stronger stationary-majority transition in the strict factor-two window `T_k<theta_1/2<2T_k` for `q>=2`;
5. in the canonical `a=2` family these become two adjacent but distinct population-size thresholds, `q+2` and `q+3`;
6. representation and neutral-measure counterexamples delimit precisely when these transitions can and cannot be exported.

This should be described as a finite representation result, not as a deep new theorem in pure combinatorics or a new population-genetic law.

## Why the majority addition improves the novelty position

The majority theorem does **not** create novelty by making the algebra harder. Its value is conceptual completeness. A reviewer cannot dismiss `2^k-1` as a conveniently chosen mode statistic, because the manuscript now asks two separate occupancy questions and derives a second, stronger threshold from the same routing-specific hierarchy.

The paired result is more informative than either alone:

- `T_k` marks when the optimum becomes the largest aggregate class;
- `theta_1/2` marks when it carries most stationary probability;
- the exact interval between them is controlled by the same finite architecture.

The canonical `a=2` one-step population-size gap is a useful corollary, but should not be sold independently from the structural theorem.

## Current novelty confidence

### High confidence that these are prior art

- weak-mutation reversible stationary weighting;
- selection plus multiplicity in equilibrium distributions;
- weakest-link/minimum fitness maps;
- robustness/abundance opposing fitness;
- representation dependence and mutation bias in general;
- genotype–phenotype redundancy shifting evolutionary/error thresholds;
- generic notions of modal versus majority occupancy.

### Moderate confidence as candidate-new composition

- the routing-specific exact layer hierarchy plus adjacent-obstruction reduction;
- the `theta_c=2^k-1` necessary-and-sufficient aggregate gain-layer threshold for this representation;
- the exact `{q-1,q}` equality tie;
- the linked majority bracket `T_k<theta_1/2<2T_k` and canonical mode/majority population-size separation;
- the combination of those results with explicit representation and mutation-measure claim ceilings.

The confidence remains **moderate**, not high. The deeper search materially strengthened the prior-art boundary but still did not expose an algebraically identical theorem.

## Manuscript consequence

The Abstract and Introduction should use formulations such as:

> For this finite routing representation, we derive...

> The routing-specific layer hierarchy yields two distinct stationary occupancy transitions...

> Combining the exact multiplicities with the standard origin-fixation stationary law gives...

Avoid:

> We introduce a new selection–multiplicity principle...

> We discover a new form of weakest-link epistasis...

> We show for the first time that suboptimal genotype abundance can overwhelm selection...

> We show for the first time that genotype–phenotype redundancy changes an evolutionary threshold...

> `2^k-1` is the threshold for majority occupancy...

## Next novelty gate

Before submission, the only remaining literature task is a source-level check of the most relevant discrete/quasispecies papers uncovered here, looking specifically for an algebraically identical finite-class theorem rather than another conceptual analogue.

A direct collision with the exact threshold composition should trigger reframing before priority wording is frozen.