# Routing paper — source-level collision ledger v1

Date: 2026-09-13

## Purpose

Replace broad keyword novelty claims with source-level comparisons against the closest known combinatorial, population-genetic and quasispecies results.

The target object is the complete routing composition:

`X={0,...,q}^k, g=min`

`-> D_r=(q-r+1)^k-(q-r)^k`

`-> A_s=(s+1)^k-s^k <= (2^k-1)^s`

`-> exact aggregate-mode trichotomy at T_k=2^k-1`

`-> distinct stationary-majority threshold T_k<theta_1/2<2T_k` for `q>=2`.

A source counts as a direct collision only if it contains this finite-class population-genetic structure or an algebraically equivalent theorem, not merely an isolated counting identity or the general idea that abundance, neutrality or representation changes evolutionary outcomes.

## Source 1 — Sella & Hirsh 2005

### Established object

Weak-mutation reversible mutation–selection stationary weighting / statistical-physics formulation.

### Collision

**Direct collision with the population-genetic bridge; no collision with the routing-specific composition.**

### Manuscript consequence

Treat `pi proportional to mu * fitness^(N-1)` and detailed-balance machinery as prior-art setup only.

---

## Source 2 — Riedel, Khatri, Lässig & Berg 2015

*Multiple-Line Inference of Selection on Quantitative Traits*, Genetics 201:305–322. DOI `10.1534/genetics.115.178988`.

### Established object

Sequence multiplicity / number of variants representing trait states is combined with selection in low-mutation equilibrium inference.

### Collision

**Direct collision with any broad claim that selection and state multiplicity jointly determine equilibrium.**

No source-level evidence found for the routing layer hierarchy, `2^k-1` aggregate-mode theorem or paired majority threshold.

### Manuscript consequence

Never sell “multiplicity opposes selection” or “fitness alone does not determine phenotype frequency” as new.

---

## Source 3 — Labourel, Bansept & McCandlish 2026

*Weakest link epistasis and the geometry of genetic load*, bioRxiv v2, DOI `10.64898/2025.12.08.693057`.

### Established object

Organismal fitness determined by the minimum of component fitnesses, analyzed under mutation–selection–drift / weak-mutation population genetics.

### Collision

**Direct collision with novelty claims for a `min` / weakest-link map and its generic population-genetic use.**

The inspected source does not supply the present finite routing genotype-layer multiplicities or the exact aggregate mode/majority threshold pair.

### Manuscript consequence

Frame `g=min_i x_i` as a declared finite representation, not a newly introduced epistasis class.

---

## Source 4 — Wilke 2005, Quasispecies Made Simple

PLOS Computational Biology, DOI `10.1371/journal.pcbi.0010061`.

### Established object

Quasispecies models in which inferior phenotypes represented by broader/more connected neutral networks can displace fitter phenotypes. Increasing neutral-network size can shift the error threshold. The paper explicitly discusses network breadth, replacement rates and successive thresholds.

### Dynamical regime difference

High-mutation quasispecies / mutation–selection balance, not the rare-mutation origin-fixation chain used in the routing paper.

### Collision

**Direct collision with the broad claim that genotype–phenotype redundancy or neutral-network size can shift an evolutionary threshold.**

No direct collision located with the routing-specific finite layer hierarchy or its `T_k` / `theta_1/2` formulas.

### Manuscript consequence

Do not write that this paper discovers representation-dependent evolutionary thresholds.

---

## Source 5 — Takeuchi, Poorthuis & Hogeweg 2005

*Phenotypic error threshold; additivity and epistasis in RNA evolution*, BMC Evolutionary Biology 5:9. DOI `10.1186/1471-2148-5-9`.

### Established object

Analytical phenotype-level error thresholds when genotype–phenotype redundancy / mutational neutrality is present.

### Dynamical regime difference

Phenotypic quasispecies/error-threshold setting, not reversible weak-mutation fixation.

### Collision

**Direct collision with any claim that phenotype aggregation or redundancy-dependent threshold analysis is new.**

No inspected formula matches the routing aggregate-mode or majority theorem.

### Manuscript consequence

The novelty claim must remain the exact routing-specific composition, not phenotype-level thresholding in general.

---

## Source 6 — Boolean-lattice multichain enumeration

The combinatorial literature on zeta polynomials of the Boolean lattice gives the standard fact that the number of multichains of a prescribed length is a power such as `n^k`; this appears, for example, in standard enumerative-combinatorics treatments of Boolean-lattice zeta polynomials. Equivalently, multichains can be encoded by assigning each of `k` elements the step at which it enters the chain.

### Established object

The bijection between coordinate threshold values and nested/multichain subsets of a Boolean lattice is standard combinatorics. Consequently, expressions of the form `(s+1)^k` for multichain counts and differences such as `(s+1)^k-s^k` are not candidates for pure-combinatorial priority.

### Collision

**Direct collision with any claim that the nested-subset encoding or the isolated difference-of-powers count is a new combinatorial construction.**

The current search did not locate the population-genetic composition that uses this layer count to prove the routing-specific exact aggregate-mode tie and linked majority bracket.

### Manuscript consequence

Present the nested-chain argument as a short certificate that makes the biological representation transparent, not as a new theorem about Boolean lattices.

---

# Exact-formula search status

Targeted searches were run for combinations of:

- `"2^k-1"` with genotype multiplicity, stationary mode and selection;
- `"(s+1)^k-s^k"` with genotype / fitness / weakest-link terms;
- nested nonempty subset chains and Boolean-lattice multichains;
- majority / half-mass thresholds in finite degeneracy classes;
- discrete minimum-coordinate and quasispecies phenotype-class models.

These searches recovered conceptual and component-level prior art but **did not locate an algebraically identical population-genetic routing theorem**.

This is not proof of literature-wide priority.

## Current collision classification

| Object | Current status |
|---|---|
| weak-mutation reversible stationary law | direct prior art |
| selection × multiplicity equilibrium | direct prior art |
| weakest-link / minimum fitness | direct prior art |
| redundancy / neutral-network size shifts a threshold | direct prior art |
| phenotype-level error threshold | direct prior art |
| Boolean-lattice multichain / nested-chain counting | direct combinatorial prior art |
| isolated difference-of-powers layer count | elementary / not a standalone novelty claim |
| routing use of that layer hierarchy in the declared genotype-policy map | no direct population-genetic collision located |
| all-layer reduction yielding exact `T_k` aggregate-mode transition | no direct collision located |
| exact `{q-1,q}` aggregate-mode tie | no direct collision located |
| paired `T_k < theta_1/2 < 2T_k` routing majority structure | no direct collision located |
| canonical `a=2`: `N_unique=q+2`, `N_majority=q+3` | no direct collision located |

## Verdict

**Novelty confidence remains moderate, not high.**

The broad conceptual territory and the elementary combinatorics are both crowded and must be ceded explicitly. The remaining defensible contribution is narrower: in this finite routing representation, standard combinatorial layer counts compose with weak-mutation stationary weighting in such a way that one adjacent-layer obstruction controls an exact aggregate-mode transition and a strict bracket for the stronger majority transition, with explicit representation and mutation-measure claim ceilings.

No further abstract theorem should be added to manufacture novelty. A future direct collision should trigger reframing; otherwise the current claim boundary is suitable for a theory-journal submission.