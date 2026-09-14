# Routing paper submission gate v1

Date: 2026-09-14

## Candidate identity

**Working title:** Exact occupancy thresholds in finite routing representations

**Primary target:** Theoretical Population Biology

**Paper center:** one explicit finite branch-product routing representation generates exact genotype multiplicities; a nested-chain bound reduces competition with all lower gain layers to the adjacent obstruction; standard weak-mutation stationary weighting then yields two distinct occupancy transitions—aggregate modality and stationary majority—with explicit representation and mutation-measure claim ceilings.

## Closed gates

### Mathematics

- exact layer count `D_r=(q-r+1)^k-(q-r)^k`;
- global bound `A_s<=(2^k-1)^s`;
- exact aggregate-mode trichotomy at `T_k=2^k-1`;
- exact equality structure: only full and adjacent layers tie for `k>=2`;
- unique half-mass threshold;
- strict bracket `T_k<theta_1/2(q,k)<2T_k` for `q>=2`;
- canonical Moran `a=2`, `k=q+1` consequence: `N_unique_mode=q+2`, `N_majority=q+3` for `q>=2`.

### Claim boundary

- weakest-link/minimum fitness is treated as prior art;
- reversible weak-mutation stationary weighting is treated as prior art;
- generic selection-versus-multiplicity and genotype-phenotype redundancy effects are treated as prior art;
- representation dependence and mutation bias are not claimed as generic discoveries;
- branch-product and reversible-neutral-measure counterexamples remain in the main argument.

### Novelty collision review

`NOVELTY_AUDIT_V1.md` performs the source-level pass on the closest prior-art classes. No algebraically identical routing-specific mode-plus-majority theorem was located. Status: **PASS WITH CONDITIONAL WORDING**.

### Figures

Three deterministic SVG figures are generated from the theorem implementation:

1. routing representation and exact layer multiplicities;
2. adjacent-obstruction bound, aggregate-mode threshold, majority threshold and canonical population-size gap;
3. representation and neutral-measure scope controls.

`tests/test_routing_paper_figures.py` regenerates the figures in a temporary directory and checks pinned theorem semantics.

### Reproducibility provenance

The older integrated v0 manuscript ref was not self-contained with respect to the stationary-majority implementation. The repaired theorem+manuscript base is:

`freeze/routing-paper-integrated-v1-self-contained`

at

`90f9d29f685a2a2cd9507e11df49751bfc289c43`.

Figure work is based only on that repaired tree.

## Remaining submission work

These are editorial/bibliographic tasks, not theorem-development gates:

1. convert the working reference list into journal-ready bibliography with complete volume/pages/DOIs;
2. ensure every literature-boundary statement has an explicit citation in the final formatted manuscript;
3. convert Markdown notation and figures into the chosen journal submission format;
4. perform one final prose compression pass so the paper reads as a compact theoretical-population-biology article rather than repository documentation;
5. write cover letter after the manuscript source is frozen.

## Do not reopen without a concrete trigger

Do not add neutral waiting-time, mesoscopic, absolute-rate, downstream-process, or additional routing theorems to this paper unless a reviewer or direct prior-art collision specifically requires them.

The next scientific upgrade path is empirical qualification of a biological genotype-policy representation, not theorem accumulation.

## Freeze rule

A submission-candidate freeze may be created when the current figure+novelty-audit head passes the repository's full Python 3.10/3.11/3.12 CI matrix. The freeze should point to the exact tested commit and should not be advanced in place.
