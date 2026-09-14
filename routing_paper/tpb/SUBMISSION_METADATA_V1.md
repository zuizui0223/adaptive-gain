# TPB submission metadata v1

Target journal: Theoretical Population Biology

Working title: Exact occupancy thresholds in finite routing representations

Article type: Original theoretical research article

## Keywords

Use no more than six keywords at initial submission:

1. population genetics
2. genotype–phenotype map
3. weak mutation
4. stationary distribution
5. routing representation
6. mutation–selection balance

## One-sentence editor summary

For an explicit finite genotype-policy representation, exact class multiplicities convert a standard weak-mutation stationary law into two distinct occupancy thresholds: one for becoming the largest aggregate gain class and a stronger one for carrying a stationary majority.

## Main result set

- Exact routing-layer multiplicities: `D_r=(q-r+1)^k-(q-r)^k`.
- All-layer bound: `A_s=(s+1)^k-s^k <= (2^k-1)^s`.
- Sharp aggregate-mode threshold: `theta_c=2^k-1`.
- Exact equality structure for `k>=2`: only the full and adjacent layers tie at `theta_c`.
- Unique stationary-majority threshold `theta_1/2(q,k)` with `T_k < theta_1/2 < 2T_k` for `q>=2`.
- Canonical Moran corollary for `k=q+1,a=2`: unique mode at `N=q+2`, stationary majority at `N=q+3` for `q>=2`.
- Representation and neutral-measure counterexamples delimit the result.

## Submission framing

Lead with the population-genetic consequence, not the combinatorial proof. The paper does **not** claim novelty for weakest-link fitness, reversible origin-fixation weighting, selection versus multiplicity, survival of the flattest, or representation-dependent evolutionary thresholds in general.

Preferred novelty sentence:

> For this finite routing representation, the exact multiplicity hierarchy reduces all suboptimal competitors to one adjacent obstruction, yielding linked exact thresholds for aggregate modality and stationary majority under a standard weak-mutation stationary law.

## Figures

- Figure 1: representation and exact layer multiplicities.
- Figure 2: aggregate-mode and stationary-majority transitions.
- Figure 3: representation and mutation-measure scope controls.

All three figures are generated deterministically from the theorem implementation and covered by regression tests.

## Initial-submission format

Use Elsevier's Your Paper Your Way route: a single readable manuscript PDF is sufficient for initial peer review; exact journal reference styling can be deferred. Keep the present title, abstract, sections, references, and embedded Figures 1–3 together in the review PDF.
