# TPB submission metadata v1

Target: **Theoretical Population Biology**

Scientific source freeze: `freeze/routing-paper-submission-candidate-v1` at `68caf51d4ec908f54dca6bd773b491769239a252`.

## Proposed title

**Exact occupancy thresholds in finite routing representations**

The title deliberately says `representations`, not `biological routing systems`, because the theorem is conditional on the declared branch-product genotype-policy map.

## Keywords

Use at most six:

1. population genetics
2. genotype–phenotype map
3. mutation–selection balance
4. stationary distribution
5. weakest-link epistasis
6. genotype multiplicity

## Article identity

Compact theory paper in weak-mutation population genetics. The central result is not a new fixation process, weakest-link principle, or generic selection–multiplicity tradeoff. It is the exact composition

`finite routing representation -> exact layer multiplicities -> adjacent-layer obstruction -> aggregate-mode threshold -> stationary-majority threshold`,

with explicit representation and neutral-measure scope controls.

## Editorial emphasis

The opening page should establish, in this order:

1. phenotype-level fitness ranking does not determine aggregate stationary occupancy;
2. this broad principle is prior art;
3. the finite routing representation generates an exactly solvable multiplicity hierarchy;
4. the hierarchy separates becoming the largest aggregate class from becoming a stationary majority;
5. the result is conditional on representation and mutation measure.

Do not lead with the combinatorial proof or describe `2^k-1` as a universal biological threshold.

## Initial-submission format

TPB currently participates in Elsevier's Your Paper Your Way workflow. Initial submission can therefore prioritize a readable single manuscript rather than journal-specific reference styling. Keep the source repository auditable, but the submitted manuscript must not contain repository/PR/freeze language.

## Figures

Main text:

- Figure 1 — routing representation and exact layer multiplicities.
- Figure 2 — aggregate-mode and stationary-majority transitions; this is the central figure.
- Figure 3 — representation and neutral-measure scope controls.

The deterministic SVG generator and regression test remain part of the reproducibility surface. Convert figure format only if the submission system requires it; do not redraw numerical content manually.

## Required declarations before upload

Confirm at submission time:

- author list and affiliations;
- corresponding author;
- funding statement;
- competing-interests declaration;
- data/code availability statement;
- AI/tool-use disclosure if required by the journal's then-current policy;
- preprint status if applicable.

These are intentionally not guessed in the repository.

## Scientific hard stop

Do not add another abstract theorem before initial TPB submission unless a concrete reviewer/prior-art collision requires it. Remaining work is editorial compression, citation placement, figure callouts, and submission packaging.