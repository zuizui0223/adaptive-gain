# Aedes confirmatory sample-size rule v1

## Purpose

Prevent sample-size tuning after treatment/genotype effects are seen.

This rule applies to the planning branch only. It does not change the frozen Aedes v1 finite task.

## Core rule

Confirmatory sample size is computed once from:

1. the preregistered primary endpoint;
2. a control/baseline response estimate obtained without opening active treatment/genotype effects;
3. a preregistered minimum practically important effect, `delta_min`;
4. a preregistered type-I error / multiplicity rule;
5. a preregistered target power;
6. a preregistered inflation for block/day clustering and expected attrition.

`delta_min` may not be estimated from an active agonist effect or an Ir68a-vs-WT effect observed in the same study.

## Phase 1 — binary host-seeking endpoint

Let

- `p0` = host-seeking probability in the LVP vehicle control;
- `delta_min > 0` = smallest reduction in host-seeking probability worth using to justify the next, more expensive integration stage;
- `p1 = p0 - delta_min`.

The confirmatory design should be powered for each of the two preselected active agonist-versus-vehicle contrasts under the frozen two-contrast familywise-error rule.

A standard two-proportion calculation may be used as the starting value, followed by inflation for day/block clustering and exclusions.

If `p1 <= 0`, the chosen `delta_min` is incompatible with the observed baseline and must be revised **before active treatment labels are opened**. The revision and reason must be committed prospectively.

### Inputs that may come from a control-only pilot

- `p0`;
- loader / miniport failure rate;
- mosquito-level attrition;
- between-day vehicle variability;
- intrablock correlation or an empirical design-effect estimate;
- feasibility of 15–25 females per replicate, consistent with established olfactometer practice.

### Inputs that may not come from the active-treatment pilot

- `delta_min`;
- expected agonist effect size;
- which of the preselected active compounds is retained because it looked strongest.

The next-generation agonist study used 15–20 females per replicate and multiple biological replicates, but those published counts are feasibility anchors rather than a substitute for a new confirmatory calculation in LVP.

## Phase 2 — B-side site-finding endpoint

The primary unit of replication is the independent assay/cage, not the individual egg.

Published Ir68a work used approximately 70 gravid females per container-seeking assay and multiple independent assays per genotype. Egg counts within one cage are therefore not to be treated as dozens or hundreds of independent biological replicates.

Sample size is based on the frozen cage-level primary endpoint and its control variance.

### Allowed control-only pilot inputs

- wild-type LVP wet-container preference / deposition distribution;
- cage-to-cage variance;
- blood-meal success and mature-gravid attrition;
- assay failure rate;
- direct-placement wild-type competence variability.

### Forbidden inputs before confirmatory n is frozen

- observed Ir68a mutant effect magnitude in the new replication experiment;
- selecting whichever of occupancy, wet-container entry, or egg deposition gives the largest genotype difference;
- increasing n because one mutant allele is initially “almost significant.”

The primary B endpoint must be committed before genotype labels are opened.

## Competence-equivalence margin

For the direct-placement oviposition competence control, an equivalence or noninferiority margin may be required.

That margin must be justified biologically and frozen before confirmatory genotype labels are opened. It may use:

- wild-type assay precision;
- an a priori statement of how large a reproductive deficit would be sufficient to explain the site-finding phenotype;
- external published competence data.

It may not be chosen to make the Ir68a mutant pass after the result is seen.

## Sequential sampling prohibition

Do not inspect the treatment/genotype effect and then add replicates until a threshold is crossed.

If a group misses the planned n because of a preregistered technical failure criterion, replacement cohorts may be run only until the originally planned analyzable n is reached.

Any extension beyond the planned analyzable n requires a new versioned confirmatory protocol and cannot be pooled silently with the first result as though it were one fixed-n test.

## Multiplicity

### Phase 1

The two preselected active agonist-versus-vehicle contrasts form one primary family. Use the frozen multiplicity procedure from `AEDES_PHASE1_2_CONFIRMATORY_DECISION_RULES_V1.md`.

### Phase 2

The two independent Ir68a allele-versus-WT contrasts form one primary causal-replication family.

Secondary sensory, locomotor, occupancy and egg-laying endpoints are supportive/control outcomes unless explicitly promoted prospectively in a new protocol version.

## Required sample-size receipt

Before confirmatory data are opened, commit a machine-readable or tabular receipt containing at least:

- protocol git SHA;
- phase;
- primary endpoint;
- `p0` or control distribution summary;
- `delta_min` or competence margin where applicable;
- alpha / multiplicity rule;
- target power;
- base calculated n;
- clustering/design-effect inflation;
- attrition inflation;
- final planned analyzable n;
- maximum number of replacement cohorts allowed under preregistered technical failure.

## Interpretation

Power is a design property, not evidence that the biological architecture is true.

A well-powered STOP or UNRESOLVED receipt is a valid endpoint and does not license redesign of the frozen v1 task.

## Literature anchors

- Zeledon et al. 2024: miniport host-seeking assays used 15–20 females per replicate and multiple independent replicates; three NPYLR7 agonists reduced live-host feeding at 1 micromolar.
- Tang et al. 2024, PNAS, DOI `10.1073/pnas.2407394121`: approximately 70 gravid females per container-seeking assay; WT LVP and two independent Ir68a alleles were evaluated across independent assay replicates, with separate direct-placement competence tests.
