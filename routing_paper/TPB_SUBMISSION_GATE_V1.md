# Routing paper — Theoretical Population Biology submission gate v1

Date: 2026-09-13

## Target decision

**Primary current target: Theoretical Population Biology (TPB).**

This is a scope decision, not a submission claim. No manuscript has been submitted.

## Why TPB fits the present theorem

The current TPB description emphasizes theoretical aspects of population biology across evolution and genetics, with mathematical theory/models used to improve biological understanding.

The routing paper is fundamentally a population-genetic theory paper:

- it studies stationary occupancy in a finite genotype–phenotype / genotype-policy representation;
- it composes an explicit representation with established weak-mutation selection theory;
- it derives exact consequences for when the fittest gain class becomes the largest class and when it becomes a stationary majority;
- it makes representation and neutral mutation measure explicit model inputs.

Recent TPB papers continue to publish exact or strongly analytic population-genetic theory, including mutation-rate modifier theory, mutation-accumulation models and exact coalescent expressions. Empirical data are therefore not a prerequisite when the population-biological question is clear.

## Main editorial risk

The isolated combinatorics are elementary. TPB fit depends on making the **population-biological consequence of the composition** unmistakable.

The paper must not read as:

`elementary count + standard stationary law`.

It must read as:

`explicit genotype-policy representation`
`-> phenotype-class multiplicity hierarchy`
`-> distinct stationary occupancy transitions`
`-> exact limits on what can be exported across representations and mutation measures`.

## Required manuscript state before submission

### Gate A — scientific claims

- [x] mode and majority are separate estimands;
- [x] majority theorem is frozen and CI validated;
- [x] representation dependence is in the main argument;
- [x] mutation-measure dependence is in the main argument;
- [x] broad redundancy-threshold novelty is explicitly ceded to prior art;
- [x] no empirical biological representation is implied.

### Gate B — novelty

- [x] broad conceptual prior art identified;
- [x] source-level collision ledger created;
- [ ] final source-level read of the closest exact discrete/quasispecies threshold papers completed;
- [ ] bibliography checked for missing finite-class degeneracy / weak-mutation phenotype-class results.

### Gate C — manuscript coherence

- [x] Abstract v0/v1 story exists;
- [x] Introduction exists;
- [x] Model/Results contains Theorems 1–4 and scope controls;
- [x] Discussion exists;
- [x] 3-figure plan exists;
- [ ] repeated governance language removed from submission prose;
- [ ] theorem notation and terminology made globally consistent;
- [ ] one continuous submission manuscript assembled from the component drafts.

### Gate D — biological significance for TPB

The Introduction and Discussion must explicitly answer:

> What population-biological inference changes when genotype–phenotype representation is specified rather than ignored?

The intended answer is:

- individual fitness ranking does not determine aggregate phenotype occupancy;
- becoming the largest phenotype class and becoming a stationary majority are distinct;
- representation and mutation measure determine where those transitions occur;
- therefore phenotype-level selection coefficients alone are insufficient for stationary occupancy prediction.

This biological significance should appear before technical proof detail.

### Gate E — presentation

- [ ] Figure 1 generated: representation and exact layer multiplicities;
- [ ] Figure 2 generated: nested-chain certificate + mode threshold + majority threshold;
- [ ] Figure 3 generated: representation and mutation-measure scope controls;
- [ ] figure claims independently checked against frozen theorem receipts;
- [ ] final title chosen.

Preferred current title:

**Exact occupancy thresholds in finite routing representations**

### Gate F — journal-specific technical requirements

The official TPB scope page is verified. The current web-accessible Elsevier page links to the journal's Guide for Authors, but this audit did not reliably retrieve the full current journal-specific formatting instructions.

Therefore do **not** freeze guessed requirements such as:

- abstract word limit;
- number of keywords;
- whether Highlights are mandatory for TPB specifically;
- figure file formats at initial submission;
- line numbering / manuscript template requirements.

These must be checked directly in the current Guide for Authors / submission system immediately before packaging.

Generic Elsevier author resources describe Highlights, but that alone is not evidence that TPB requires them.

## Fallback journal logic

### Journal of Theoretical Biology

Plausible second target, but its current scope explicitly stresses biological significance and excludes papers that are only technical mathematics without biologically novel insight. The present theorem can fit, but desk risk is higher until the representation has stronger biological justification.

### Bulletin of Mathematical Biology

Credible mathematical-biology fallback. The concern is not lack of rigor but that the core combinatorics may be modest relative to papers centered on advanced mathematical methods.

### Evolution

Stretch target until a real biological genotype-policy representation is independently qualified.

## Current decision

`TPB_SUBMISSION_READY = FALSE`

Reason:

The mathematical/manuscript claim architecture is ready, but final submission packaging should wait for:

1. source-level collision review to close;
2. one integrated prose pass that removes internal-governance language;
3. actual generation of Figures 1–3;
4. current TPB Guide-for-Authors verification.

## Hard stop

Do not raise the journal target by adding unrelated theorems. A genuine impact upgrade would come from empirical qualification of the genotype-policy representation, not theorem accumulation.