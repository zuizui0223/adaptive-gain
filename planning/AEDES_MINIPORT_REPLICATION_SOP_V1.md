# Aedes Miniport replication SOP v1

## Scope

Execution-readiness SOP only. This document does not change the frozen scientific task or Phase 1 decision rules. It translates the published Miniport host-seeking assay into a reproducible local implementation checklist.

## Published assay anchor

The 2024 NPYLR7 study and the original 2019 assay describe the following canonical elements:

- starting canister: approximately 6 in x 3 in x 3 in acrylic, mesh-screened for airflow;
- group size: 10-20 females per canister (original implementation commonly 15-20);
- mosquitoes loaded 24 h after meal and acclimated overnight;
- two water-soaked cotton balls supplied during overnight acclimation to limit desiccation;
- behavioral test at 48 h after meal;
- four attraction positions used in parallel, with canisters randomly assigned to positions;
- 5 min pre-trial acclimation after connection;
- 5% CO2 delivered at 30 mL/min;
- 30 s CO2 pre-activation before the sliding door opens;
- human odor source: nylon stocking worn by one experimenter for 8-10 h in the 2024 implementation, frozen in a sealed plastic bag at -20 C until use;
- attraction endpoint: mosquito enters the attraction trap after access to host cues;
- treatment comparison should be matched to saline controls within experimental blocks.

The original 2019 Miniport paper used a 10 min host-seeking period. If the 2024 construction/source protocol specifies a different trial duration for the exact apparatus, the duration must be frozen before confirmatory data are opened. Do not tune duration after observing treatment effects.

## Phase 1 treatment groups

Locked compounds:

1. saline vehicle;
2. TDI-014188;
3. TDI-014186.

Both agonists are administered at the preregistered published concentration and timing once material/formulation details are verified from the source-lab/TDI route.

No replacement agonist is permitted after LVP outcome data are opened.

## Randomization and blocking

For every behavioral block:

- randomize treatment canisters across Miniport positions 1-4;
- balance position exposure across treatment groups across blocks;
- keep odor-source preparation constant within a confirmatory batch;
- blind scoring to treatment where technically feasible;
- treat replicate canister, not individual mosquito, as the primary independent behavioral unit unless the final preregistered analysis explicitly uses a hierarchical model.

## Required controls

### Meal/intake control

Record:
- proportion feeding to repletion;
- post-feeding mass or equivalent intake proxy;
- exclusion rule for incompletely fed females before behavior.

The published NPYLR7 work explicitly measured feeding and body weight to exclude palatability/intake artifacts.

### Mortality control

Record cage mortality before behavioral testing. A treatment showing substantial mortality or severe morbidity cannot be interpreted as selective host-seeking suppression.

### General-performance control

Use a preregistered non-host locomotor/activity assay independent of the Miniport endpoint. A treatment that suppresses host seeking but produces comparable global activity impairment does not satisfy the Phase 1 specificity gate.

## Primary endpoint

For each replicate canister:

`host_seeking_fraction = n_entered_attraction_trap / n_eligible_at_trial_start`

Do not replace the denominator post hoc after seeing treatment effects except for exclusions frozen in the protocol before unblinding.

## Confirmatory classification

Use `planning/AEDES_PHASE1_2_CONFIRMATORY_DECISION_RULES_V1.md` and the machine-readable phase receipt.

- `GO`: both TDI-014188 and TDI-014186 reproduce the preregistered host-suppression direction versus saline and general-performance/intake controls pass;
- `UNRESOLVED`: one compound only, inconsistent independent blocks, or specificity/general-performance ambiguity;
- `STOP`: both preselected compounds fail under an otherwise qualified assay, or the assay itself cannot reproduce a stable saline host-seeking baseline.

Do not add compounds or alter host cues after outcome data are opened.

## Build/validation gate before compounds

Before any confirmatory compound experiment, the local Miniport must pass a vehicle-only qualification run showing:

1. stable host-seeking toward CO2 + human odor;
2. no persistent position bias beyond the preregistered tolerance;
3. acceptable between-block repeatability;
4. no excessive desiccation/mortality;
5. reproducible scorer/recording workflow.

Pilot qualification may tune mechanical factors such as seals, airflow balance and lighting, but once the confirmatory apparatus specification is frozen, no treatment-informed mechanical tuning is permitted.

## Source anchors

- Duvall et al. 2019, Cell, Miniport construction and host-seeking assay.
- Zeledon et al. 2024, Parasites & Vectors, 1 micromolar NPYLR7 agonist screening, 48 h post-meal Miniport assay.
- VosshallLab/Miniport-Construction public design repository referenced by both papers.
