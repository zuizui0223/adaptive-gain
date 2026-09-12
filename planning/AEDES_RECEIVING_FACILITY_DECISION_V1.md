# Aedes receiving-facility decision v1

## Status

Operational planning only. This document is downstream of `freeze/aedes-execution-readiness-v1` and cannot alter the frozen scientific task, comparator, background rules, or confirmatory criteria.

## Executive conclusion

No single Japanese institution is yet proven to dominate every requirement. The facilities identified from public evidence have different strengths:

- **RIKEN BDR** — strongest scientific/behavioral fit to the frozen host-seeking ↔ reproductive-state question;
- **Jikei Medical Entomology** — strongest demonstrated live/genetically modified *Aedes aegypti* infrastructure and best domestic line-manipulation host candidate;
- **Obihiro Vector Biology** — strongest exact Liverpool pedigree/material route, especially MRA-735/LVP-IB12;
- **Nagasaki University Tropical Medicine** — explicit live-Aedes maintenance and strong insectary backup, but less direct match to the frozen H↔O mechanism.

The receiving institution should be chosen by a prospective decision rule, not convenience after material responses arrive.

## 1. Required capabilities for an integrated Phase 1–3 site

A primary receiving/phenotyping site should be able to satisfy, or credibly add, all of the following:

1. lawful contained rearing of live *Aedes aegypti*;
2. acceptance of external eggs/lines under institutional procedures;
3. maintenance of the exact frozen comparator background;
4. non-nutritive feeding / NPYLR7 pharmacology;
5. host-seeking behavioral assay;
6. mature-gravid wet-versus-dry/site-seeking assay;
7. direct-placement egg-laying competence assay;
8. ability to phenotype genetically modified Ir68a lines;
9. sufficient environmental control for circadian/gravid assays;
10. institutional willingness to preserve preregistered GO/UNRESOLVED/STOP rules.

Genome editing is desirable but **not required at the primary site** if published mutant lines can be transferred and maintained there.

## 2. RIKEN BDR

### Public strengths

- current active *Aedes aegypti* colony;
- direct research focus on host-seeking, blood feeding, egg maturation, endocrine state and gonotrophic behavioral transitions;
- automated heat-seeking / behavioral-monitoring expertise;
- artificial feeding and reproductive physiology workflows;
- Liverpool-derived current colony.

### Open gates

- current Liverpool pedigree is not established as LVP-IB12;
- willingness/approval to receive external genetically modified Ir68a lines is unknown;
- exact wet-versus-dry Ir68a-style assay is not publicly documented;
- genome-editing capacity is not the primary demonstrated strength.

### Selection rule

Choose RIKEN as the **primary integrated phenotyping site** if it confirms:

- external GM-Aedes line receipt is institutionally possible;
- exact LVP comparator can be introduced/maintained;
- the frozen host-seeking and gravid-site assays can both be implemented.

If those three conditions are met, RIKEN has the strongest scientific alignment with the causal-routing question.

## 3. Jikei Medical Entomology

### Public strengths

- dedicated medical-entomology/vector platform;
- published secure *Aedes aegypti* rearing;
- Japanese Society of Tropical Medicine explicitly documents genetically modified *Aedes aegypti* maintained in Kanuka laboratory;
- coauthorship on the 2023 Aedes DIPA-CRISPR experiment;
- strong blood-feeding and mosquito physiology experience.

### Open gates

- exact LVP background currently maintained is unresolved;
- exact wet-versus-dry Ir68a-style behavior assay is not yet documented;
- current precise tagged-HDR capacity for Ir68a is unconfirmed.

### Selection rule

Choose Jikei as the **primary integrated site** if RIKEN cannot receive/maintain the frozen GM background, and Jikei confirms:

- receipt of exact LVP/Ir68a materials;
- feasibility of both host-seeking and mature-gravid site-seeking assays;
- willingness to maintain the fixed comparator and confirmatory rules.

Jikei is currently the strongest domestic **GM-Aedes handling/editing-host** candidate.

## 4. Obihiro Vector Biology

### Public strengths

- current Aedes-vector research;
- explicit historical separation of LVP-OB and BEI MRA-735/LVP-IB12;
- strongest domestic chance of recovering the exact IB12 baseline without new international baseline import.

### Open gates

- current availability of the 2024 MRA-735/IB12 colony is unknown;
- frozen host-seeking ↔ gravid-routing behavioral platform is not established publicly;
- GM Ir68a handling/behavior integration is not yet established.

### Selection rule

Use Obihiro primarily as the **baseline/pedigree/material source** unless it independently confirms that the full frozen behavioral program can be hosted.

Do not choose Obihiro as primary simply because the exact baseline is physically nearby.

## 5. Nagasaki University Institute of Tropical Medicine

### Public strengths

- official public evidence of laboratory *Aedes aegypti* maintenance;
- established tropical-medicine/vector infrastructure.

### Open gates

- exact Liverpool pedigree;
- frozen H↔O behavior assays;
- GM-line receipt/editing capability for this project.

### Selection rule

Keep Nagasaki as a **backup receiving/insectary candidate** if RIKEN/Jikei routes fail institutionally.

Do not broaden to it merely to avoid resolving the better-matched routes.

## 6. Preferred distributed architecture if no single site covers everything

A distributed collaboration is acceptable only if the biological comparison remains coherent.

Preferred split:

- **Obihiro**: exact IB12 baseline supply/pedigree;
- **Jikei**: GM-Aedes receipt/editing/reconstruction fallback;
- **RIKEN**: final common-background behavioral phenotyping if it can receive and maintain the lines.

The confirmatory A/B comparison itself should not be split across institutions/backgrounds unless the assay is explicitly bridged and preregistered. Published effects from different facilities cannot be concatenated into the empirical finite-task matrix.

## 7. Facility decision receipt

Record for each candidate:

- `LIVE_AEDES_APPROVED = YES/NO/UNKNOWN`;
- `EXTERNAL_GM_LINE_RECEIPT = YES/NO/UNKNOWN`;
- `EXACT_IB12_AVAILABLE = YES/NO/UNKNOWN`;
- `HOST_SEEKING_ASSAY = YES/NO/ADAPTABLE/UNKNOWN`;
- `GRAVID_SITE_ASSAY = YES/NO/ADAPTABLE/UNKNOWN`;
- `PRECISE_EDITING = YES/NO/PARTIAL/UNKNOWN`;
- `WILLING_TO_PRESERVE_FROZEN_DESIGN = YES/NO/UNKNOWN`.

Primary-site selection requires all essential Phase 1–3 fields to be `YES` or prospectively validated `ADAPTABLE`.

## 8. Decision order after outreach

1. Resolve Obihiro IB12 material availability.
2. Resolve Garrity exact Ir68a parental pedigree/material route.
3. Ask RIKEN whether it can receive/maintain the exact GM comparator and run both endpoint assays.
4. Ask Jikei the same plus precise-editing fallback capability.
5. Select one primary confirmatory phenotyping site **before** live material is moved.
6. Use other institutions only for clearly separated supply/editing/support roles.

## 9. Hard stops

- do not choose a facility solely because it is geographically convenient;
- do not substitute its resident Liverpool colony for the exact comparator without pedigree closure;
- do not split treatment/control phenotyping across institutions without a preregistered bridge;
- do not let editing capability override behavioral/comparator requirements;
- do not treat willingness to collaborate as evidence for the biological hypothesis.
