# Aedes Phase 1–2 confirmatory decision rules v1

## Purpose

Predeclare go / no-go / unresolved classifications for the two feasibility stages that precede the frozen state-routing test.

This planning note does not change the immutable v1 finite-task semantics at `freeze/aedes-pre-data-admission-v1` (`b5949da`). It only determines whether the experimental components are reliable enough to justify moving to the expensive integrated causal test.

The design principle is deliberately conservative: a single positive perturbation, a single successful allele, or a nominal p-value is not enough to advance the program.

## General separation of pilot and confirmatory work

### Pilot work

Pilot runs may be used only to establish:

- assay failure / exclusion rates;
- practical cohort size and throughput;
- plate/cage/day blocking factors;
- stimulus delivery stability;
- baseline response range;
- a biologically defensible equivalence margin for general-performance controls if one is needed.

Pilot data do **not** count as confirmatory evidence for the routing hypothesis.

The confirmatory analysis plan, endpoint definition, multiplicity rule, exclusion criteria and any equivalence margin must be frozen after pilot work and before confirmatory treatment/genotype labels are opened.

### Confirmatory work

Use independent cohorts, randomized treatment allocation where applicable, blinded scoring where technically possible, and day/block identifiers retained in the analysis table.

Report effect estimates and confidence intervals, not p-values alone.

## Phase 1 — transfer NPYLR7 pharmacology into LVP

### Fixed intervention logic

Use:

1. saline / matched vehicle control;
2. active NPYLR7 agonist A;
3. structurally independent active NPYLR7 agonist B;
4. inactive / non-behaviourally-active comparator when practical.

The preferred active pair should be selected before the confirmatory run from compounds already reported to suppress host seeking / biting at 1 micromolar. Current anchors include TDI-014188 and either TDI-014184 or TDI-014186.

Do not screen additional compounds after seeing the LVP result merely to obtain two positives.

### Primary endpoint

One preregistered host-seeking / host-approach endpoint measured under the same time point and delivery logic for all groups.

The published next-generation agonist work identifies multiple compounds that reduce blood-feeding at 1 micromolar, but published effect magnitude is **not** used as the acceptance threshold because the background and apparatus may differ.

### General-performance controls

At minimum include a readout capable of detecting broad impairment, such as locomotor/activity output or a simple non-host-directed behavioural response.

A treatment that suppresses both host seeking and general performance to a similar degree is not qualified as a portable state perturbation.

### Confirmatory statistical rule

For each of the two preselected active agonists estimate the contrast versus vehicle for the primary host-seeking endpoint with a confidence interval. Control the two predeclared primary agonist contrasts as one family (for example Holm control at familywise alpha 0.05).

Classify:

#### P1-GO — replicated portable state perturbation

All of the following hold:

- both independent active agonists show host-seeking suppression relative to vehicle in the preregistered direction;
- both primary contrasts pass the frozen multiplicity rule;
- the inactive comparator, if used, does not reproduce the same host-suppression pattern;
- no general-performance endpoint shows a deficit large enough to explain the host-seeking effect under the frozen impairment/equivalence rule.

This licenses Phase 3 state-routing screening in LVP. It does **not** license empirical adaptive gain or the claim that NPYLR7 is the complete R variable.

#### P1-UNRESOLVED — pharmacology not clean enough

Examples:

- only one of the two active agonists replicates;
- both act, but a general-performance deficit can plausibly explain the result;
- treatment uptake/exposure is too inconsistent for interpretation;
- an inactive comparator produces the same behavioural suppression.

One preregistered technical repeat is allowed only if the failure was caused by an assay-quality criterion declared before outcome inspection. Compound hunting is not allowed.

#### P1-STOP — no transfer to LVP

Neither preselected active agonist produces the preregistered host-seeking suppression under a technically valid run.

Stop the LVP-first pharmacological integration route rather than adding new agonists post hoc.

## Phase 2 — validate the Ir68a B-side site-information phenotype

### Published anchor

The 2024 Ir68a study used approximately 70 gravid females per container-seeking assay, compared wet and dry containers, and reported strong defects for two independent Ir68a mutant alleles while direct-placement egg laying remained intact. Wild-type LVP was tested in 10 container-seeking assays; the two Ir68a alleles were tested in 6 assays each. Direct-placement competence was assessed in individual females.

These published sample sizes are feasibility anchors, not mandatory replication sample sizes. Confirmatory size should be chosen from pilot variance / attrition before genotype labels are opened.

### Primary B endpoint

Use one frozen site-finding endpoint before opening confirmatory data, for example:

- wet-container entry / occupancy; or
- egg deposition in the wet-container seeking assay.

Do not switch the primary endpoint after observing genotype effects.

### Causal replication requirement

Use wild type plus two independent Ir68a loss-of-function alleles where available.

The B-side phenotype is considered replicated only if both independent alleles show the same-direction site-finding deficit relative to wild type under the frozen multiplicity rule.

### Mandatory competence control

Run a direct-placement oviposition assay in which gravid females are placed immediately adjacent to an acceptable wet substrate.

Before confirmatory genotype labels are opened, freeze a biologically acceptable competence margin using pilot/assay-precision information. The purpose is not to prove exact equality; it is to exclude a reproductive or egg-laying deficit large enough to explain the site-finding phenotype.

### Classification

#### P2-GO — B qualified as a site-information channel

All of the following hold:

- both independent Ir68a alleles show the preregistered site-finding deficit relative to wild type;
- direct-placement oviposition for both alleles passes the frozen competence rule;
- gross locomotor/viability failure does not explain the seeking deficit;
- the mature-gravid timing window satisfies the frozen endpoint-domain criteria.

This licenses use of Ir68a-dependent Moist Cell input as the primary B causal handle in Phase 3.

#### P2-UNRESOLVED

Examples:

- only one allele replicates;
- site-finding is impaired but direct-placement competence is also materially impaired;
- the two alleles disagree in direction;
- mature-gravid timing or blood-meal success is too heterogeneous for interpretation.

Do not replace Ir68a with another receptor simply to preserve the v1 architecture.

#### P2-STOP

Under a technically valid confirmatory run, neither independent Ir68a allele reproduces the frozen site-finding phenotype in the chosen colony/assay framework.

Stop B-side qualification for this implementation.

## Phase 1 × Phase 2 routing to the next stage

| Phase 1 | Phase 2 | Next action |
|---|---|---|
| GO | GO | Proceed to Phase 3 crossed state × terminal-dependency experiment |
| GO | UNRESOLVED | Repair only the preregistered B technical ambiguity; no integrated claim |
| UNRESOLVED | GO | Resolve state-perturbation specificity before Phase 3 |
| UNRESOLVED | UNRESOLVED | Stop integration; evidence base is too ambiguous |
| STOP | any | Stop LVP-first NPYLR7 route |
| any | STOP | Stop v1 B implementation |

No cell in this table licenses redesign of the frozen four worlds, target ontology, comparator semantics or endpoint domain.

## Analysis discipline

The confirmatory result should produce one machine-readable receipt per phase containing:

- frozen protocol version / git SHA;
- colony/background;
- treatment or genotype identifiers;
- cohort/block identifiers;
- exclusions and reasons;
- primary effect estimate and interval;
- multiplicity-adjusted decision;
- impairment/competence-control result;
- terminal class: `GO`, `UNRESOLVED`, or `STOP`.

Only `GO` receipts may unlock the next phase.

## Literature anchors

- Zeledon et al. 2024, next-generation NPYLR7 agonists: three compounds reduced live-host blood feeding at 1 micromolar; TDI-014184, TDI-014186 and TDI-014188 provide independent active candidates.
- Tang et al. 2024, PNAS, DOI `10.1073/pnas.2407394121`: two independent Ir68a mutant alleles are strongly defective in water-container seeking, while direct-placement egg-laying competence is preserved.

## Hard stop

These criteria are component-qualification gates only. They do not reopen the frozen Aedes v1 scientific surface and do not license an empirical adaptive-gain claim by themselves.
