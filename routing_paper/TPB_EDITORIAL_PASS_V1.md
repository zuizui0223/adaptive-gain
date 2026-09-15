# TPB editorial pass v1

This file freezes the editorial changes allowed after the scientific submission candidate. It is intentionally not a new scientific surface.

## Main editorial diagnosis

The continuous manuscript is scientifically coherent but still reads longer than necessary because the Introduction previews nearly every theorem and the Discussion restates most of them. For TPB, the paper should read as a compact population-genetic theorem paper rather than repository documentation.

## Compression rules

### Introduction

Retain four moves only:

1. stationary phenotype occupancy depends on selection plus representation/mutation measure;
2. broad multiplicity/representation effects are prior art;
3. define the finite routing question and distinguish per-genotype mode, aggregate mode, and majority;
4. state the paired threshold result and scope controls.

Compress detailed proof intuition and the full canonical example out of the Introduction; they belong in Results.

### Model and results

Keep Theorems 1–4 and their proofs. Keep the q=2,k=3 running example once, immediately after the two threshold theorems. Add Figure 1 after the multiplicity theorem, Figure 2 after the majority theorem/example, and Figure 3 after the two scope-control sections.

### Discussion

Use four paragraphs:

1. paired occupancy transitions and why mode is not majority;
2. population-size interpretation under Moran without presenting it as universal;
3. representation and neutral-measure conditionality;
4. biological qualification and the narrow modeling lesson.

Do not repeat theorem proofs or enumerate excluded side-theory modules in the main Discussion unless needed for scope.

## Citation placement

At minimum, place citations in the prose for:

- Sella & Hirsh 2005: reversible weak-mutation stationary weighting;
- Riedel et al. 2015: selection plus sequence multiplicity in low-mutation equilibrium/inference;
- Bull, Meyers & Lachmann 2005 and Takeuchi et al. 2005: quasispecies/phenotypic threshold context;
- Labourel, Bansept & McCandlish 2026: explicit weakest-link/minimum fitness prior art.

The reference list alone is insufficient.

## Figure callouts

- Figure 1: after introducing `D_r` and the q=2,k=3 profile `(19,7,1)`.
- Figure 2: after the paired mode/majority thresholds and q=2 example.
- Figure 3: after representation and mutation-measure scope controls.

## Terminology lock

Use only:

- per-genotype mode;
- aggregate-modal gain layer;
- stationary majority.

Avoid unqualified “dominant”, “takes over”, “wins”, or “threshold for adaptation”.

## Scientific content that must remain in the main paper

- exact equality structure at `theta=2^k-1`;
- distinct majority threshold and factor-two bracket;
- canonical q+2 versus q+3 population-size corollary;
- compressed-representation counterexample;
- reversible mutation-measure counterexample.

## Content that must not be reintroduced

- neutral-plateau waiting-time theory;
- mesoscopic dynamics;
- absolute mutation-rate scaling;
- Aedes or other unqualified biological anecdotes;
- broad claims that representation-dependent thresholds or selection–multiplicity tradeoffs are new.
