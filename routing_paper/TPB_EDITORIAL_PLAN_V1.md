# TPB editorial plan v1

This plan starts from the validated submission-candidate freeze and changes **presentation, not theorem content**.

## Main editorial problem

`MANUSCRIPT_V0.md` is scientifically coherent but still reads partly like a theorem dossier: the Introduction previews most formulas before the Model/Results sections derive them, and several scope warnings are repeated. The TPB version should be shorter and more population-genetic in its first-page logic.

## Compression rules

### Abstract

Target roughly 180–220 words.

Keep:
- established selection–multiplicity tension;
- declared finite representation;
- exact aggregate-mode threshold;
- distinct majority threshold;
- Moran population-size corollary;
- conditionality on representation/mutation measure.

Remove proof-detail language such as the nested-subset construction.

### Introduction

Use four conceptual paragraphs rather than reproducing the Results:

1. stationary occupancy depends on selection plus representation/neutral measure;
2. broad prior art: multiplicity, quasispecies/neutral networks, weakest-link fitness;
3. unresolved finite question: exact largest-class versus majority transitions in the declared routing representation;
4. contributions and scope controls, with Figure 1 callout.

Move detailed formulas for `D_r`, `A_s`, and the majority root to Results.

### Model

Keep the population-genetic bridge concise. Explicitly state that Moran fixation weighting is prior art and define `theta=a^(N-1)` once.

### Results

Retain four theorem statements, but shorten elementary proofs in the main manuscript where possible. The central narrative is:

- exact multiplicities (Fig. 1);
- global bound;
- mode threshold;
- majority threshold and canonical `q+2`/`q+3` separation (Fig. 2);
- representation and mutation-measure controls (Fig. 3).

### Discussion

Avoid repeating every theorem. Organize around three interpretations:

1. per-genotype fitness versus aggregate occupancy are different objects;
2. mode and majority are distinct population-level transitions;
3. exact thresholds require an explicit representation and neutral measure.

End with the modeling lesson and biological qualification requirement.

## Citation completion

Before upload, convert conceptual mentions into explicit in-text citations. At minimum:

- Sella & Hirsh (2005) for reversible weak-mutation/statistical-physics stationary weighting;
- Riedel et al. (2015) for selection plus sequence multiplicity;
- Bull, Meyers & Lachmann (2005) and Takeuchi et al. (2005) for quasispecies/phenotype-level threshold context;
- Labourel, Bansept & McCandlish (2026) for weakest-link epistasis.

Do not add a large literature review merely to make the bibliography longer.

## Figure callouts

Insert explicit callouts in the final prose:

- Fig. 1 immediately after defining the routing layer hierarchy;
- Fig. 2 at the transition from aggregate mode to stationary majority;
- Fig. 3 in the representation/mutation-measure scope-control section.

## Hard scope boundary

The TPB version must not absorb neutral-plateau times, mesoscopic dynamics, absolute mutation-rate scaling, Aedes qualification work, or other side-theory modules. Those answer different questions.

## Completion criterion

The editorial branch is ready when a reader can understand the population-genetic question and both occupancy transitions without knowing the repository history, while every numerical figure statement remains generated from the frozen theorem implementation.