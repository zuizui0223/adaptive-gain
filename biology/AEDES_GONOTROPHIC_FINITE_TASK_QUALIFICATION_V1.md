# Aedes gonotrophic finite-task qualification v1

## Purpose

This note screens a second biological route for issue #27: the reproductive-state switch in female *Aedes aegypti* from host seeking before a blood meal to suppressed host seeking and oviposition-site assessment after blood feeding.

Unlike the C. elegans SRI-36 control, this system naturally points to **different environmental distinctions in different physiological branches**. It is therefore a stronger prospective candidate for a positive finite adaptive/fixed gap.

This is a qualification/prospectus only. No empirical adaptive-gain value is claimed from the published literature.

## Biological anchors

### Gonotrophic state switch

Female *Aedes aegypti* strongly seek human hosts before blood feeding. Host attraction is suppressed for days after a blood meal while eggs develop. NPY-like receptor 7 (`npylr7`) is required for normal long-term host-seeking suppression: CRISPR-Cas9 null mutants show defective behavioral suppression. Selective NPYLR7 agonists suppress human attraction and biting.

Recent work further identifies `npylr7`-expressing rectal-pad cells that respond to the ligand RYamide and amino acids and participate in post-blood-meal reproductive physiology. This strengthens the evidence that internal nutritional/reproductive state is coupled to the behavioral switch, although NPYLR7 is not a clean branch-local switch because it also affects oocyte provisioning.

### Host branch terminal channel

The IR8a ionotropic-receptor pathway is required for normal detection of acidic human-odor volatiles. CRISPR disruption of `Ir8a` eliminates attraction to lactic acid and responses to acidic odorants and reduces attraction to humans/human odor. CO2/Gr3 interacts with this pathway; host detection is therefore a multi-cue system rather than a single-receptor channel.

### Oviposition branch terminal channel

Gravid females assess oviposition sites using aquatic chemical/olfactory cues. Geosmin attracts gravid *Aedes aegypti* to oviposition sites, and the egg-laying preference is lost in `Orco` mutants, establishing an OR-pathway requirement for this cue. Other work shows gravid females discriminate larval-stage- and density-dependent aquatic VOC blends.

## Candidate q=1 finite task

The cleanest prospective task uses two physiological branches and one environmental distinction within each branch.

Declare three organism-level information sources:

- `R`: gonotrophic/reproductive state, pre-blood host-seeking versus gravid/oviposition state;
- `A`: acidic host-cue channel, operationalized prospectively by an IR8a-dependent lactic-acid/host-odor distinction under a fixed CO2 background;
- `B`: oviposition-odor channel, operationalized prospectively by an Orco-dependent geosmin or independently validated aquatic-odor distinction.

A minimal frozen laboratory task would contain:

| World | R | A | B | predeclared target |
|---|---:|---:|---:|---|
| H0 | 0 | 0 | 0 | reject/no host approach |
| H1 | 0 | 1 | 0 | host approach |
| O0 | 1 | 0 | 0 | reject/no oviposition |
| O1 | 1 | 0 | 1 | accept/oviposit |

The off-branch terminal stimulus is held at a preregistered baseline in the laboratory task rather than retrospectively coded as irrelevant.

For this exact matrix with four distinct targets:

- adaptive policy: query `R`, then `A` if `R=0` or `B` if `R=1`, so `C_A=2` under unit acquisition costs;
- fixed policy: every pair among `{R,A,B}` fails to separate at least one required target pair, so `C_F=3`;
- prospective gap: `g=1` **if and only if the biological cue and cost semantics pass admission before the matrix is opened**.

This is a predeclared testable witness, not a claim that published mosquitoes already instantiate the exact unit-cost task.

## Why this is stronger than the C. elegans SRI-36 control

The SRI-36 result changes the receptor/neuron implementation of the **same diacetyl distinction** across state. Under the natural context-by-diacetyl task, that gives no automatic extra finite cue and therefore no positive gap.

The mosquito candidate instead uses:

- a host-associated acidic odor distinction in one gonotrophic state;
- an oviposition-site odor distinction in another gonotrophic state.

Thus the two terminal queries are environmental distinctions with different ecological jobs, not merely two molecular implementations of the same cue.

## Issue #27 G1-G7 ledger

| Gate | Status | Current interpretation |
|---|---|---|
| G1 — declared ecological/internal contexts | **strong** | Pre-blood host-seeking and post-blood/gravid states are experimentally defined and behaviorally distinct. |
| G2 — context-dependent downstream modules | **strong/partial** | Host-seeking is suppressed after blood feeding and oviposition-site assessment becomes behaviorally relevant during gravidity. Published work also reports reduced peripheral sensitivity to host-associated lactic-acid cues after blood feeding. Direct proof that the exact `A` and `B` channels are selectively sampled rather than merely reweighted remains incomplete. |
| G3 — heritable regulatory substrate | **strong/partial** | CRISPR-accessible `npylr7`, `Ir8a`, `Orco`, and `Gr3` loci provide causal genetic handles. However, `npylr7` is an internal-state/reproductive regulator, while `Ir8a`/`Orco` are terminal sensory pathway genes; the full state-to-channel routing map is not one known cis-regulatory switch. |
| G4 — mutation locality | **partial** | Defined null alleles exist, but natural one-step mutational transitions among complete sensory policies are not known. Separate gene knockouts are experimental interventions, not an inferred natural mutation graph. |
| G5 — pleiotropy/coupling audit | **partial** | NPYLR7 also affects reproductive physiology/oocyte provisioning; Orco is a broad OR co-receptor; Ir8a participates in an integrated host-cue system. These cannot be treated as branch-local edits without full cross-context assays. |
| G6 — proposal bias / neutral mutation measure | **not qualified** | Relative natural proposal rates and a neutral stationary measure over sensory-policy genotypes are unavailable. Stationary population claims remain prohibited. |
| G7 — phenotype map | **strong at component level; task unmeasured** | Ir8a loss alters acidic-odor/human attraction; Orco loss abolishes the tested geosmin oviposition preference; NPYLR7 loss disrupts host-seeking suppression. The frozen four-world `C_A,C_F` matrix has not been measured as one experiment. |

Overall status: **partial representation with a stronger prospective positive-gap task than the current C. elegans candidates**.

## Main hard stops before calling g=1 biological

### 1. `R` must be an organismal information source with declared cost

Gonotrophic state cannot be inserted as a free abstract label. The experiment must define what physiological signal makes that state available to the decision system and what a unit acquisition means. NPYLR7 is a mechanistic candidate, not automatically the query itself.

### 2. The two terminal channels must be measured in both branches

The task must assay host-cue and oviposition-cue responses in pre-blood and gravid mosquitoes. If both channels remain equally sampled in both states and only downstream motor output changes, the biological interpretation differs from contingent cue acquisition.

### 3. Off-branch baselines must be prospective

For the four-world star, the irrelevant terminal stimulus is experimentally clamped to baseline in the opposite branch. That design choice must be frozen before computing the gap and reported as part of the task domain.

### 4. Unit query costs need a biological operationalization

Counting `R`, `A`, and `B` as equal unit-cost acquisitions is not justified merely because they are three named pathways. Candidate operationalizations include standardized sampling episodes, energetic/neural activation costs, or an explicitly declared equal-cost experimental abstraction. The latter licenses a finite laboratory task but should not be oversold as physiological cost equality.

### 5. Genetic perturbations must be audited across both behavioral branches

Every `npylr7`, `Ir8a`, `Orco`, or downstream regulatory perturbation used as a policy edge must be tested for host seeking, oviposition behavior, locomotion, reproductive state and both terminal sensory responses. Broad co-receptor or endocrine perturbations should be encoded as coupled moves.

## Prospective experiment

### Freeze

Before collecting the full matrix, preregister:

1. age, mating state and blood-meal timing;
2. physiological criterion for `R=0/1`;
3. exact host-cue stimulus and CO2 background for `A`;
4. exact oviposition cue/concentration for `B`;
5. four target actions and scoring thresholds;
6. cue-acquisition cost convention;
7. off-branch baseline stimuli;
8. exclusion/failure criteria.

### Measure

For each world and genotype:

- internal-state marker / behavioral state;
- peripheral/neural response to `A`;
- peripheral/neural response to `B`;
- host-approach or blood-feeding output where appropriate;
- oviposition-site choice / egg-laying output where appropriate.

### Open once

After the matrix is frozen, compute exact `C_A` and `C_F`. Keep zero-gap, unresolved or rejected outcomes as terminal receipts; do not redesign the four worlds after seeing the result.

### Genetics only after task admission

Use genetic perturbations to determine whether the admitted positive-gap task has a defensible genotype-policy map. Do not use a successful behavioral knockout to retroactively define the queries.

## Population ceiling

Even a successful `g=1` laboratory task plus a qualified genotype-policy support graph would not identify stationary evolutionary occupancy or waiting time. Those claims remain blocked without relative mutation bias, a population process, and an absolute rate scale, exactly as shown by the downstream nonidentifiability side theory.

## Literature anchors

- Duvall L.B. et al. 2019. *Small-Molecule Agonists of Ae. aegypti Neuropeptide Y Receptor Block Mosquito Biting*. Cell 176:687-701.e5. DOI: 10.1016/j.cell.2018.12.004.
- Frank K. et al. 2026. *A signaling hub in the mosquito rectum coordinates reproductive investment after blood feeding*. Current Biology. DOI: 10.1016/j.cub.2026.02.042.
- Raji J.I. et al. 2019. *Aedes aegypti mosquitoes detect acidic volatiles found in human odor using the IR8a pathway*. Current Biology 29:1253-1262.e7. DOI: 10.1016/j.cub.2019.02.045.
- Melo N. et al. 2020. *Geosmin attracts Aedes aegypti mosquitoes to oviposition sites*. Current Biology 30:127-134.e5.
- Khan Z. et al. 2023. *Odour-mediated oviposition site selection in Aedes aegypti depends on aquatic stage and density*. Parasites & Vectors 16:264.
- Duvall L.B. 2019. *Mosquito Host-Seeking Regulation: Targets for Behavioral Control*. Trends in Parasitology 35:704-714.

## Verdict

Among candidates screened so far, the Aedes gonotrophic switch is the clearest **prospective positive-gap architecture** because different physiological branches call for different environmental distinctions.

It is not yet a qualified genotype-policy system and no natural `g=1` is claimed. Its immediate value is that the minimal q=1 star can be written down *before* data collection and falsified in one coherent experiment.