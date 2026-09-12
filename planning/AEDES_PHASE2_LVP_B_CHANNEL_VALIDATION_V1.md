# Aedes Phase 2 — LVP B-channel validation v1

## Purpose

Reproduce the Ir68a-dependent oviposition-site-finding phenotype in the same LVP framework chosen for Stage-A integration.

This is execution planning downstream of `freeze/aedes-pre-data-admission-v1`. It does not modify the frozen role of B and does not by itself establish state routing or empirical adaptive gain.

## Frozen B interpretation

`B` is oviposition-site information.

The primary causal handle is Ir68a-dependent Moist-Cell humidity/water-vapor sensing.

The Phase-2 question is narrow:

> Can mature-gravid LVP females use the preregistered B assay to locate a wet oviposition container, and is that site-finding phenotype specifically disrupted by Ir68a loss while egg-laying competence remains intact once the site is found?

## Published assay architecture to reproduce

Use the Tang et al. (2024) logic as the starting protocol rather than inventing a new B assay after seeing results.

Published geometry included:

- mature gravid females that had mated and blood-fed approximately 72 h earlier;
- a choice between one wet and one dry oviposition container;
- the wet container approximately 75% filled with water;
- filter paper as oviposition substrate;
- mesh over containers with an approximately 5-mm central opening to minimize incidental contact while permitting water-vapor escape and entry;
- behavioral scoring over approximately 24 h;
- group assays of roughly 70 females per assay;
- a separate direct-placement assay in which individual gravid females were placed immediately adjacent to water to test egg-laying competence independent of site finding.

These published values are replication anchors, not automatic power calculations for the new study.

## Genotype structure

Minimum:

1. LVP wild type;
2. Ir68a loss-of-function line.

Preferred if available:

- two independent Ir68a alleles/lines, matching the logic of the published EYFP and RFP disruptions;
- Ir40a loss-of-function as a pathway-specificity comparison, because published Ir40a mutants retain normal wet-container seeking while Ir68a mutants do not.

Do not replace Ir68a with a new receptor if the replication is inconvenient. A failed replication is an admissible stop result.

## Physiological-state gate

Before each assay batch, prospectively define mature-gravid eligibility.

Record or verify at least:

- successful blood feeding;
- fixed post-blood interval;
- ovarian/egg maturity criterion in a validation subset or equivalent preregistered marker;
- circadian phase;
- mating status and age window.

The frozen finite task uses a mature-gravid endpoint, not all post-blood females.

## Primary site-finding readouts

Retain at least:

- eggs deposited in wet container;
- eggs deposited in dry container;
- number/proportion of females found in or immediately associated with the wet container at assay end if measurable;
- replicate/cage identity;
- genotype;
- batch, circadian time and post-blood interval.

The strongest expected WT phenotype is selective use of the wet container.

## Mandatory competence control

Run a direct-placement egg-laying assay separately.

Place gravid females immediately adjacent to or inside a partially water-filled oviposition chamber with suitable substrate so that locating the site is no longer required.

Interpretation:

- site-finding failure + normal direct-placement egg laying supports a sensory/navigation B phenotype;
- site-finding failure + poor direct egg laying is confounded by reproductive/oviposition competence and cannot qualify B as a terminal information channel.

This control is mandatory, not optional cleanup.

## Sensory-level validation

Where technically feasible, add a direct Moist-Cell humidity-response readout in WT and Ir68a mutants.

This can strengthen the causal chain:

`Ir68a -> Moist Cell humidity response -> wet-container seeking`.

However, the behavioral site-finding phenotype plus competence control remains the critical B endpoint for the frozen task.

## Prospective outcome classes

### B0 — assay not reproduced

WT does not show a stable wet-container preference/site-finding phenotype under the preregistered conditions.

Action: stop. Do not change the B stimulus until a positive result appears.

### B1 — nonspecific reproductive defect

Ir68a mutants fail in the container assay and also fail the direct-placement egg-laying control.

Action: B is not qualified as a site-finding information channel under this implementation.

### B2 — replicated causal site-finding phenotype

WT robustly locates/uses the wet container; Ir68a mutants are impaired; direct-placement egg-laying competence is preserved.

Action: B passes the behavioral causal gate for feasibility planning.

### B3 — sensory + behavioral causal closure

B2 plus a direct Ir68a-dependent Moist-Cell humidity-response defect.

Action: strongest B-side foundation for the later integrated routing experiment.

## Cross-branch warning

Ir68a is not branch-exclusive. Published work shows Ir68a-dependent Moist Cells also contribute redundantly to blood feeding.

Therefore:

- do not encode `B=absent` in the host state;
- do not interpret any host-side Ir68a effect as a failure of the frozen architecture;
- the relevant later question is whether B is required for the frozen O target distinction and whether relative A/B dependency changes with state.

## Analysis discipline

Before the final replication:

- define the replicate unit;
- define the primary site-finding outcome;
- define exclusion criteria for failed blood feeding, failed mating or incorrect developmental stage;
- specify treatment of zero-inflated egg counts if egg number is primary;
- choose sample size from pilot variance or a preregistered power criterion rather than copying the published n mechanically.

## Hard stops

- no substitution of geosmin/Orco or another oviposition cue after an Ir68a failure within v1;
- no scoring of egg number alone without the competence control;
- no pooling of intermediate post-blood females with mature-gravid females;
- no empirical adaptive-gain claim from Phase 2;
- no interpretation of B validation as proof that NPYLR7/NPF/RYamide controls B recruitment.

## Literature anchor

Tang R et al. 2024. Functional dissection of mosquito humidity sensing reveals distinct Dry and Moist Cell contributions to blood feeding and oviposition. PNAS 121:e2407394121. DOI 10.1073/pnas.2407394121.

## Gate forward

Proceed to the integrated A/B state-dependency screen only after B2 or B3 and after Phase 1 reaches at least F2.
