# Aedes assay build bill of materials v1

## Scope

Execution-readiness checklist for physically building the Phase 1 and Phase 2 assay systems defined in PR #51.

This is not a purchasing authorization, supplier recommendation, or claim that any item is currently available locally. Equivalent components are acceptable if they preserve the frozen assay geometry and performance specifications.

## A. Phase 1 Miniport — minimum build set

### Starting canisters and attraction modules

- clear acrylic or equivalent inert material for starting canisters near the published ~6 in x 3 in x 3 in geometry;
- fine mosquito-proof mesh for ventilation faces;
- sliding / removable gate that can be opened without disturbing the canister;
- attraction trap / host-cue chamber compatible with the published Miniport geometry;
- identical duplicated modules sufficient to run the four parallel positions used in the screening design;
- connectors / gaskets that prevent uncontrolled leaks while allowing defined airflow.

### CO2 delivery

- laboratory CO2 source approved for the receiving facility;
- two-stage regulator or equivalent stable pressure control;
- flow-control device capable of delivering the frozen target of 30 mL/min per active Miniport line at 5% CO2;
- tubing and manifolds with identical path lengths where practical;
- independent verification of delivered flow before each qualification block;
- safe exhaust / room ventilation appropriate for the local insectary.

A simple rotameter can be used for qualification if its accuracy at the target low flow is documented; a calibrated mass-flow controller is preferable when available.

### Human odor source

- standardized clean nylon stockings from one frozen material/type;
- sealed odor-storage bags;
- -20 C freezer access;
- handling gloves / forceps to minimize uncontrolled odor transfer;
- written donor-use / institutional procedure if required locally.

The confirmatory study should freeze donor, wear duration, storage duration and reuse policy before treatment outcomes are opened.

### Timing / environmental control

- stopwatch or automated gate timing;
- temperature and relative-humidity logger;
- fixed lighting / circadian test window;
- four-position randomization map;
- labels that permit scorer blinding where feasible.

### Recording

At minimum:
- replicate ID;
- treatment code;
- starting eligible females;
- females entering attraction trap;
- deaths / escapes;
- position number;
- block / date / clock time;
- environmental readings;
- meal/intake qualification receipt.

Video recording is recommended where feasible so attraction counts can be independently audited.

## B. General-performance locomotor control — minimum build set

- visually uniform, mosquito-proof observation chamber(s);
- camera capable of stable video or infrared capture;
- fixed camera mount;
- uniform illumination that permits normal flight while avoiding strong directional visual cues;
- temperature / humidity logging;
- analysis workflow capable of producing the preregistered distance-travelled and active-time metrics.

The local implementation may use FlyBox, custom video tracking or an equivalent system. The same hardware/software pipeline must be used for saline and both locked agonists.

## C. Phase 2 wet-versus-dry arena — minimum build set

### Arena / cage

- mosquito-proof cage sized to accommodate the frozen cohort without crowding artifacts;
- two identical oviposition containers per cage;
- identical filter-paper substrates;
- mesh covers for each container;
- reproducible central entry opening near the published ~5 mm anchor;
- calibrated volume marker for the wet container, nominally ~75% full;
- position labels enabling randomized wet/dry left-right assignment.

### Environmental controls

- stable temperature / RH;
- fixed circadian start time;
- light regime matching the qualified mature-gravid assay window;
- no uncontrolled standing water elsewhere in the cage.

### Egg counting

- stereomicroscope or validated imaging/counting workflow;
- sample containers / labels preserving cage identity;
- independent recount rule for ambiguous/high-density samples.

### Direct-placement competence control

- matched wet oviposition substrate;
- small transfer / holding enclosure allowing mature-gravid females to be placed immediately adjacent to the substrate;
- assay geometry that removes the long-range site-search requirement without physically forcing egg deposition;
- egg counting and female survival records.

## D. Shared insectary / safety requirements

Before any live experiment:

- documented facility authorization for live *Aedes aegypti*;
- escape-proof primary and secondary containment;
- aspirator / transfer tools dedicated to mosquito work;
- freezer or approved kill method for waste / escaped-specimen response;
- written escape incident procedure;
- training documentation for all handlers;
- approved blood-feeding source / procedure where Phase 2 requires blood-fed females.

These institutional items are independent of the public scientific SOP and remain part of issue #49.

## E. Build qualification sequence

Do not order or expose locked agonists before the behavioral apparatus itself is qualified.

### Miniport
1. assemble four positions;
2. verify leak-free equivalent airflow;
3. calibrate CO2 flow;
4. run saline / untreated LVP only;
5. quantify position bias and between-block stability;
6. freeze apparatus specification;
7. only then open confirmatory drug allocation.

### Locomotor control
1. validate tracking on vehicle LVP females;
2. quantify missing-track / camera-error rate;
3. freeze activity metrics and impairment margin from control data only;
4. only then record treatment groups.

### Wet/dry assay
1. assemble identical wet/dry containers;
2. run parental LVP only;
3. verify stable wet preference and acceptable total egg output;
4. validate direct-placement competence;
5. freeze geometry / timing;
6. only then open Ir68a genotype comparison.

## F. Readiness classes

- `DESIGN_ONLY`: SOP exists but hardware is not assembled.
- `BUILT_NOT_QUALIFIED`: hardware exists but vehicle / wild-type qualification is incomplete.
- `QUALIFIED_FOR_CONFIRMATORY_USE`: all preregistered vehicle / wild-type qualification gates pass.
- `FAILED_QUALIFICATION`: apparatus cannot achieve the frozen baseline after prospectively allowed mechanical troubleshooting.

Only `QUALIFIED_FOR_CONFIRMATORY_USE` permits locked compounds or mutant genotypes to enter confirmatory analysis.

## Hard stops

- do not change geometry after treatment/genotype outcomes are opened;
- do not increase CO2 or odor strength to rescue a weak drug effect;
- do not alter water level/opening size to rescue an Ir68a effect;
- do not call a protocol-defined assay physically ready;
- do not use consumer availability as a substitute for institutional safety approval.
