# Routing paper — source-level collision ledger v1

Date: 2026-09-13

## Purpose

Replace broad keyword novelty claims with source-level comparisons against the closest known population-genetic and quasispecies results.

The target object is the complete routing composition:

`X={0,...,q}^k, g=min`

`-> D_r=(q-r+1)^k-(q-r)^k`

`-> A_s=(s+1)^k-s^k <= (2^k-1)^s`

`-> exact aggregate-mode trichotomy at T_k=2^k-1`

`-> distinct stationary-majority threshold T_k<theta_1/2<2T_k` for `q>=2`.

A source counts as a direct collision only if it contains this finite-class structure or an algebraically equivalent theorem, not merely the general idea that abundance, neutrality or representation changes evolutionary outcomes.

## Source 1 — Sella & Hirsh 2005

### Established object

Weak-mutation reversible mutation–selection stationary weighting / statistical-physics formulation.

### Collision

**Direct collision with the population-genetic bridge; no collision with the routing combinatorics.**

### Manuscript consequence

Treat `pi proportional to mu * fitness^(N-1)` and detailed-balance machinery as prior-art setup only.

---

## Source 2 — Riedel, Khatri, Lässig & Berg 2015

*Multiple-Line Inference of Selection on Quantitative Traits*, Genetics 201:305–322. DOI `10.1534/genetics.115.178988`.

### Established object

Sequence multiplicity / number of variants representing trait states is combined with selection in low-mutation equilibrium inference.

### Collision

**Direct collision with any broad claim that selection and state multiplicity jointly determine equilibrium.**

No source-level evidence found for the routing layer count, nested-chain certificate, `2^k-1` aggregate-mode theorem or paired majority threshold.

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

No inspected formula matches `D_r`, the nested-chain all-layer bound, the exact two-layer tie at `T_k`, or the routing majority bracket.

### Manuscript consequence

The novelty claim must remain the exact routing-specific composition, not phenotype-level thresholding in general.

---

# Exact-formula search status

Targeted searches were run for combinations of:

- `"2^k-1"` with genotype multiplicity, stationary mode and selection;
- `"(s+1)^k-s^k"` with genotype / fitness / weakest-link terms;
- nested nonempty subset chains with genotype multiplicity;
- majority / half-mass thresholds in finite degeneracy classes;
- discrete minimum-coordinate and quasispecies phenotype-class models.

These searches recovered conceptual prior art but **did not locate an algebraically identical routing theorem**.

This is not proof of literature-wide priority.

## Current collision classification

| Object | Current status |
|---|---|
| weak-mutation reversible stationary law | direct prior art |
| selection × multiplicity equilibrium | direct prior art |
| weakest-link / minimum fitness | direct prior art |
| redundancy / neutral-network size shifts a threshold | direct prior art |
| phenotype-level error threshold | direct prior art |
| routing layer formula in this genotype-policy role | no direct collision located |
| nested-chain all-layer reduction to `2^k-1` | no direct collision located |
| exact `{q-1,q}` aggregate-mode tie | no direct collision located |
| paired `T_k < theta_1/2 < 2T_k` routing majority structure | no direct collision located |
| canonical `a=2`: `N_unique=q+2`, `N_majority=q+3` | no direct collision located |

## Verdict

**Novelty confidence remains moderate, not high.**

The broad conceptual territory is crowded and must be ceded explicitly. The remaining defensible contribution is narrow but coherent: the exact finite routing representation makes a particular multiplicity hierarchy solvable enough that one adjacent-layer obstruction controls both the aggregate-mode transition and a strict bracket for the stronger majority transition.

No further abstract theorem should be added to manufacture novelty. A future direct collision should trigger reframing; otherwise the current claim boundary is suitable for a theory-journal submission.