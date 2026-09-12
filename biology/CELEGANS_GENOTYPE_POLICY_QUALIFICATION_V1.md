# C. elegans genotype-policy qualification screen v1

## Purpose

This note addresses issue #27 without extending the abstract routing/population mathematics. The question is whether an empirical sensory system can justify a biological genotype-policy bridge strongly enough to instantiate any downstream mutation/accessibility claims.

The current best candidate is **state-dependent chemoreceptor regulation in Caenorhabditis elegans**, especially the AWA olfactory-neuron systems involving `odr-10` and `str-44`.

This is a **qualification screen, not a declaration that the adaptive-gain routing model has been biologically identified**.

## Why this system is unusually close

Several experiments already establish a causal chain of the form

`external/internal context -> receptor-expression program -> sensory response -> behavioral choice`.

Examples include:

- `odr-10`: food availability and biological sex regulate receptor expression in AWA; food deprivation increases male `odr-10`, increases attraction to its ligand diacetyl, and shifts the feeding-versus-exploration decision. Insulin/TGF-beta signaling and DAF-16/FoxO provide mechanistic links.
- `str-44`: feeding state, stress and recent sensory stimuli alter expression in AWA; STR-44 detects attractive food-associated odors and changes food-seeking behavior.
- pathogen exposure can induce `str-44` in AWA, confer a pheromone response, and alter mating behavior through a ZIP-5-dependent program.

These results are much closer to a context-dependent sensory policy than systems in which receptor repertoires differ only constitutively among species.

## Issue #27 gate ledger

| Gate | Current status | Evidence / interpretation |
|---|---|---|
| G1 — declared ecological contexts | **strong** | Fed versus food-deprived animals, presence versus absence of food sensory signals, and pathogen exposure are experimentally manipulated states rather than post-hoc bins. |
| G2 — context-dependent downstream modules | **strong** | AWA chemoreceptor expression changes with feeding state, stress and pathogen context; `odr-10` and `str-44` provide direct examples. |
| G3 — heritable regulatory substrate | **strong/partial** | Genetic perturbations identify DAF-2/DAF-16, DAF-7/TGF-beta, ZIP-5 and receptor-promoter control. A putative DAF-16 element in the `odr-10` promoter has been directly mutated. However, much of the causal control is trans-regulatory and pleiotropic rather than a clean branch-local natural allele. |
| G4 — mutation locality | **partial** | Defined promoter edits and receptor loss/overexpression establish experimentally local perturbations, but the natural one-step mutation graph among complete sensory-policy states is not known. A CRISPR edit is an experimental intervention, not automatically one naturally accessible mutation step. |
| G5 — pleiotropy / coupling audit | **partial** | Cis receptor-promoter perturbations offer a promising local route, but DAF-2, DAF-16, DAF-7 and other trans regulators have broad effects. Endogenous `odr-10` work also shows promoter redundancy: mutating one DAF-16 motif need not recapitulate reporter-level effects in every biological state. This argues against assuming one branch = one independent regulatory element. |
| G6 — proposal bias / neutral mutation measure | **not qualified** | No evidence located here identifies relative mutation proposal probabilities or a neutral stationary measure over alternative sensory-policy genotypes. Stationary population occupancy therefore remains unlicensed. |
| G7 — phenotype map | **strong for receptor -> sensory/behavioral function; incomplete for adaptive-gain g** | ODR-10 is required for diacetyl responses; altered `odr-10` expression changes attraction and food-leaving/exploration. STR-44 has identified odor/pheromone functions and behavioral consequences. What is not yet measured is the adaptive-gain quantity `g=C_F-C_A` for a declared finite task. |

### Overall status

**Partial representation.**

The system clears the main causal biology gates required to take context-dependent sensory modules seriously, but it does **not** yet license the routing mutation graph, stationary occupancy, or an empirical adaptive-gain value.

## The key remaining identification problem

The strongest current evidence still establishes

`context -> receptor availability/expression -> response/behavior`,

not

`declared finite task -> C_A, C_F -> g -> genotype-policy mutation graph`.

In particular, receptor-expression plasticity by itself does not prove an adaptive decision tree or a fixed-versus-contingent cue-cost gap. A biological application must not equate "receptor induced only in one context" with "one adaptive branch" by naming convention.

## Minimal prospective bridge experiment

A decisive experiment would predeclare a small finite discrimination task before observing the adaptive-gain result.

### 1. Worlds / alternatives

Choose a small set of ecologically interpretable food/odor states for which AWA-mediated behavior is known and manipulable.

### 2. Context cue

Use a predeclared upstream state signal such as food-presence history or pathogen state only if it is experimentally shown to alter which downstream chemoreceptor module is available or behaviorally used.

### 3. Terminal cues

Use receptor-ligand channels with known causal function, e.g. ODR-10/diacetyl and a separately validated AWA receptor-ligand channel.

### 4. Measure the finite task directly

For each genotype/regulatory state, determine the smallest context-contingent cue program that guarantees the target action (`C_A`) and the smallest fixed cue repertoire that guarantees the same distinctions (`C_F`). Do not infer either cost from receptor-expression counts alone.

### 5. Regulatory perturbation ladder

Construct a small set of endogenous cis-regulatory edits that alter one receptor/context dependency at a time where possible. Measure receptor expression, ligand response and behavior in **all declared contexts** to quantify coupling/pleiotropy.

### 6. Only then define the genotype-policy graph

An edge is licensed only when a specified heritable edit is both biologically plausible and experimentally shown to map one policy state to another. If trans-regulatory edits alter several contexts simultaneously, encode them as coupled moves.

### 7. Stop before population occupancy unless mutation bias is measured

Even a successful G1-G5/G7 bridge licenses at most structural capability and an experimentally declared accessibility graph. Issue #31/PR #33 shows that stationary phase occupancy additionally requires mutation bias / neutral measure, and waiting time additionally requires an absolute proposal-rate scale and population process.

## Candidate comparison

### African cichlid opsin expression

Cichlids are a strong secondary candidate. Environmental light is ecologically explicit, opsin palettes alter visual sensitivity, genetic crosses map cis- and trans-regulatory loci, and a 691-bp promoter deletion is associated with SWS1 expression. However, the present evidence is better for evolved/plastic sensory tuning than for a sequential context-routing architecture. Multiple trans-eQTL also make branch independence doubtful.

### Drosophila host-odor specialization

`Drosophila sechellia` provides exceptionally strong receptor/circuit/behavior genetics: host specialization has been linked to receptor tuning, promoter/regulatory changes and circuit changes. It is excellent for genotype-to-sensory-phenotype causality, but most of the evidence concerns constitutive evolutionary specialization rather than within-organism context-dependent module routing. It is therefore a weaker first match to issue #27 than C. elegans AWA state dependence.

## Literature anchors

- Ryan et al. 2014. *Sex, age, and hunger regulate behavioral prioritization through dynamic modulation of chemoreceptor expression*. Current Biology. DOI: 10.1016/j.cub.2014.09.032.
- Wexler et al. 2020. *C. elegans males integrate food signals and biological sex to modulate state-dependent chemosensation and behavioral prioritization*. Current Biology. PMID: 32531276.
- McLachlan et al. 2022. *Diverse states and stimuli tune olfactory receptor expression levels to modulate food-seeking behavior*. eLife 11:e79557.
- Wu et al. 2023. *Pathogenic bacteria modulate pheromone response to promote mating*. Nature. PMID: 36599989.
- Gruner et al. 2014. *Feeding state, insulin and NPR-1 modulate chemoreceptor gene expression via integration of sensory and circuit inputs*. PLoS Genetics 10:e1004707.
- Gruner et al. 2016. *Cell-autonomous and non-cell-autonomous regulation of a feeding state-dependent chemoreceptor gene via MEF-2 and bHLH transcription factors*. PLoS Genetics / related record PMID: 27487365.
- Sengupta et al. 1996. *odr-10 encodes a seven transmembrane domain olfactory receptor required for responses to the odorant diacetyl*. Cell 84:899-909.
- O'Quin et al. 2012. *Evolution of cichlid vision via trans-regulatory divergence*. BMC Evolutionary Biology / PMC3575402.
- Nandamuri et al. 2018. *Multiple trans QTL and one cis-regulatory deletion are associated with differential expression of cone opsins in African cichlids*. BMC Genomics 19:945.
- Auer et al. 2020. *Olfactory receptor and circuit evolution promote host specialization*. Nature 579:402-408. DOI: 10.1038/s41586-020-2073-7.

## Claim boundary

Do not use this screen to claim that C. elegans already realizes the exact adaptive-gain extremal architecture. The useful conclusion is narrower:

> C. elegans AWA state-dependent chemosensation is currently a plausible empirical system for prospectively testing the genotype-policy bridge because ecological/internal context, sensory-module expression, receptor function and behavior are causally linked. The finite decision task, adaptive/fixed costs, branch-local mutation graph and mutation proposal measure remain to be established.

Until those measurements exist, keep the Theoretical Ecology flagship unchanged and keep downstream population claims gated.