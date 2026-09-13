# Aedes wet-versus-dry oviposition replication SOP v1

## Scope

Execution-readiness SOP only. This document translates the published Ir68a-dependent wet-container / oviposition-site assay into a local replication protocol. It does not alter the frozen Aedes task, B-channel definition, Phase 2 confirmatory rules, or the scientific interpretation of a failed assay.

## Published assay anchor

The Tang et al. 2024 Ir68a study provides a directly usable Phase 2 framework:

- use mated, blood-fed females in the mature-gravid window;
- assay approximately 72 h after blood feeding;
- use approximately 70 gravid females per assay cage in the published implementation;
- present one wet container and one dry container simultaneously;
- line containers with filter paper as the oviposition substrate;
- fill the wet container to approximately 75% capacity with water;
- cover containers with mesh while leaving a central opening of approximately 5 mm to permit entry while reducing accidental contact;
- allow a 24 h choice period;
- quantify eggs deposited in / associated with the wet versus dry site;
- freeze circadian start/end timing before confirmatory data are opened.

The original paper reported a strong wild-type preference for the wet container and severe site-finding deficits in two independent Ir68a alleles. Those published effect sizes are background evidence, not acceptance thresholds for the local replication.

## Phase 2 genotypes

Required causal groups:

1. parental / matched LVP wild type;
2. `Ir68a^EYFP`;
3. `Ir68a^RFP`.

If the transferred lines arrive with a different verified parental pedigree than expected, the pedigree must be documented before confirmatory allocation. Do not substitute another Ir68a allele after data are opened.

## Primary site-finding assay

### Cohort preparation

- use age-matched females from the frozen LVP background;
- standardize mating opportunity;
- blood-feed under one frozen protocol;
- record blood-feeding success and exclude incompletely fed females using a prospectively fixed rule;
- assay at the preregistered mature-gravid post-blood time, nominally near the published 72 h anchor;
- record ovarian / egg-maturity state in a prespecified validation subset or equivalent qualification procedure;
- hold circadian phase constant across genotypes and blocks.

### Arena

For each independent replicate cage:

- place one wet and one dry oviposition container at preregistered positions;
- randomize left/right or equivalent spatial assignment of wet versus dry treatment between replicate cages;
- use identical container geometry, filter paper, mesh, and central opening;
- fill only the wet container to the frozen target volume / approximately 75% capacity;
- prevent uncontrolled standing water elsewhere in the arena;
- keep humidity, temperature and lighting within the frozen assay range.

### Endpoint

After the frozen 24 h choice window, record:

- eggs at the wet site;
- eggs at the dry site;
- total eggs recovered per replicate cage;
- mosquitoes alive / dead at endpoint;
- any protocol deviation or accidental water exposure.

Primary site-choice metric:

`wet_site_fraction = wet_site_eggs / (wet_site_eggs + dry_site_eggs)`

where denominator exclusions, if any, are frozen before genotype labels are opened.

The replicate cage, not an individual egg, is the primary independent behavioral unit unless the confirmatory analysis plan explicitly specifies a hierarchical count model.

## Mandatory direct-placement competence control

A site-finding deficit is interpretable as a B-channel phenotype only if egg-laying competence remains intact when the search problem is removed.

For each genotype, run a separate direct-placement / adjacent-to-water competence assay using mature-gravid females under matched physiological timing.

The competence assay must document that females can deposit eggs when physically placed at or immediately adjacent to a suitable wet oviposition substrate.

Record at minimum:

- proportion of females laying;
- eggs per female or per competence replicate;
- mortality / gross morbidity;
- ovarian / mature-egg status where needed to interpret failure.

If an Ir68a genotype fails both remote wet-container finding and direct-placement egg laying, the Phase 2 result is not a qualified site-information phenotype.

## Replication structure

Use both independent Ir68a alleles.

The published study used multiple independent cage replicates (wild type and each allele separately). Local confirmatory replicate count must follow `planning/AEDES_CONFIRMATORY_SAMPLE_SIZE_RULE_V1.md`, not the published n by rote.

Interpretation classes remain:

- both alleles show the preregistered site-finding deficit and competence controls pass -> candidate `GO`;
- one allele only or inconsistent blocks -> `UNRESOLVED`;
- neither allele reproduces the B phenotype under a qualified assay -> `STOP` for this v1 B implementation;
- direct-placement competence fails -> `UNRESOLVED` or `STOP` according to the frozen confirmatory rules, never `GO`.

## Apparatus qualification before genotypes

Before opening confirmatory genotype labels, run wild-type-only qualification blocks demonstrating:

1. reproducible wet-over-dry preference;
2. no persistent arena-side bias after wet/dry position randomization;
3. acceptable total egg output in the mature-gravid window;
4. acceptable mortality / escape rate;
5. stable 24 h environmental conditions;
6. successful direct-placement egg laying in the same local rearing system.

Mechanical tuning may occur during this wild-type qualification stage. Once the confirmatory apparatus is frozen, do not tune container size, mesh opening, water level, timing, humidity or lighting in response to mutant outcomes.

## Relationship to Phase 3

Phase 2 only establishes that B can be measured causally in LVP. It does not show that NPYLR7 / internal state recruits B, and it does not by itself license empirical adaptive gain.

The later routing experiment must ask whether the frozen state intervention changes relative A/B dependency while reproductive competence and circadian state remain controlled.

## Source anchor

Tang et al. 2024, PNAS, DOI 10.1073/pnas.2407394121 — Ir68a-dependent Moist Cells and wet-container seeking, including two independent alleles and the direct-placement egg-laying competence control.
