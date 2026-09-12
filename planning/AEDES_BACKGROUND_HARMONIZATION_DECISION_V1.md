# Aedes background harmonization decision v1

## Status

Execution planning only. This document is downstream of `freeze/aedes-pre-data-admission-v1` and cannot alter the frozen scientific semantics.

## Decision

Use a **two-stage background strategy** rather than rebuilding all causal lines before any state-routing signal is known.

### Stage A — screen in LVP first

Start from the LVP background used for the Ir68a Moist-Cell/oviposition-site work.

Rationale:

1. the B-side phenotype is the more specialized and expensive endpoint to recreate;
2. NPYLR7 manipulation can be pharmacological and is therefore portable in principle across backgrounds;
3. acidic-host-cue behavior can be measured in wild-type LVP before an Ir8a line is rebuilt;
4. if state manipulation fails to shift the relative A/B phenotype in LVP, recreating multiple mutant lines would have produced little information.

This stage is a **screening/feasibility layer**, not a full causal admission of A.

### Stage B — harmonize genetics only after a positive routing signal

If Stage A shows the preregistered state-dependent A/B shift, then create a common causal background by either:

- introducing/recreating an Ir8a null allele in LVP; or
- moving the Ir68a causal perturbation into an Orlando-compatible background.

Choose between those routes based on line availability, transformation capacity, linked markers and backcross burden at that time. Do not choose a route merely because it yields the desired finite-task result.

## Why not begin in Orlando?

Orlando already supports the published NPYLR7 pharmacology and Ir8a host-cue work, but the decisive B-side causal line is published in LVP. The B assay also includes an unusually useful competence control: Ir68a mutants fail to locate the wet container but lay eggs normally when placed directly at water.

Losing that causal B anchor at the first stage would make the main unresolved edge harder to interpret.

## Stage A minimal cohort matrix

The first screening experiment should use one common LVP background and avoid combining published effect sizes across strains.

### Endpoint H — previtellogenic

At minimum:

- LVP + vehicle;
- LVP + active NPYLR7 agonist A;
- LVP + active NPYLR7 agonist B;
- inactive/nonspecific comparator where practical.

Use two preselected active agonists because one-compound-only effects are classified as unresolved pharmacology rather than a portable state manipulation.

Readouts:

- A sensory/behavioral response under a frozen acidic-cue + CO2 condition;
- B Moist-Cell/humidity sensory response or a non-oviposition humidity-orientation readout that does not require egg-laying competence;
- locomotion/arousal and meal/intake controls.

Do **not** infer an Ir8a causal effect in LVP from the Orlando mutant literature alone. At this stage A is a validated stimulus dimension, not yet a same-background genetic causal perturbation.

### Endpoint O — mature gravid

At minimum:

- LVP wild type;
- two independent Ir68a mutant alleles where available;
- state-intervention and vehicle groups if the pharmacological manipulation remains effective in this physiological window.

Readouts:

- wet-versus-dry container seeking;
- direct-placement egg-laying competence;
- A acidic-cue response under the frozen host-cue assay;
- egg maturity and circadian phase.

## State-intervention validation gate

Before using any NPYLR7 agonist as `R` evidence in LVP, establish all of the following in that background:

1. replicated host-seeking suppression with two preselected active agonists under the frozen multiplicity rule;
2. no gross locomotor impairment;
3. no trivial meal/intake artifact;
4. preferably receptor-specificity evidence, such as loss/reduction of the drug effect in a matched NPYLR7 perturbation or an equivalent specificity test.

Published Orlando specificity is not automatically portable to LVP.

If neither preselected active agonist transfers under a technically valid confirmatory run, stop the LVP-first route rather than hunting new compounds.

## B-channel validation gate

Before using Ir68a as the causal B handle, require:

1. same-direction site-finding deficits for two independent Ir68a alleles under the frozen multiplicity rule;
2. direct-placement egg-laying competence passing the prospectively frozen control margin;
3. no gross locomotor/viability failure sufficient to explain the phenotype;
4. mature-gravid timing meeting the frozen endpoint-domain criteria.

A single positive allele is `UNRESOLVED`, not `GO`.

## A/B shift gate

The screening question is not whether the agonist suppresses host seeking. That is already biologically plausible.

The question is whether the intervention changes the **relative use/dependency** of the frozen terminal information sources.

Classify outcomes prospectively:

### S0 — no routing signal

`A` dependency decreases or host seeking is suppressed, but `B` sensory/dependency measures do not increase in the predicted direction.

Interpretation: state manipulation is insufficient for the integrated H-to-O router. This is a high-value negative result.

### S1 — sensory reweighting only

A/B sensory responses shift, but target-level dependency does not.

Interpretation: state-dependent sensory modulation, not yet biological adaptive-gain routing.

### S2 — candidate routing signal

State manipulation changes relative A/B target dependency in the predicted direction while locomotor, reproductive and competence controls remain intact.

Interpretation: proceed to Stage B genetic harmonization. Do not yet claim full empirical adaptive gain.

## Single-R rejection rule

Published biology suggests that host suppression and mature-gravid site seeking may depend on partially distinct state controllers.

If NPYLR7/NPF controls A while egg maturity / circadian `cycle` independently controls B and no shared organism-level state representation mediates the relative dependency switch, reject the single-query `R` architecture.

Do not repair v1 by redefining R as an arbitrary composite after seeing the data. Any multi-state-query alternative is a new prospectively declared v2 with new exact costs.

## Genetic harmonization gate after S2

Only after S2 should resources be spent on a common-background causal stack.

The minimum strong stack would contain:

- a qualified state perturbation in the chosen common background;
- an Ir8a causal perturbation for A;
- an Ir68a causal perturbation for B;
- wild-type controls;
- cross-branch phenotyping of every perturbation;
- rescue or independent alleles where needed to exclude background/off-target explanations.

At that point the empirical claim gate can evaluate terminal-channel causality and state-routing causality on one coherent biological system.

## Confirmatory discipline

Before Stage B genetic harmonization:

- Phase 1 and Phase 2 must each return machine-readable `GO` receipts;
- receipts follow `AEDES_PHASE_RECEIPT_SCHEMA_V1.json`;
- fixed-n confirmatory planning follows `AEDES_CONFIRMATORY_SAMPLE_SIZE_RULE_V1.md`;
- one-compound-only or one-allele-only evidence cannot unlock the next stage.

## What this decision deliberately avoids

- concatenating Orlando, LVP and UGAL effect sizes into one synthetic finite-task matrix;
- backcrossing/recreating multiple lines before seeing any A/B routing signal;
- treating pharmacological host suppression as proof of B recruitment;
- treating the LVP acidic-cue response as an Ir8a causal result before same-background genetics exists;
- replacing failed A/B channels post hoc;
- adding replicates sequentially until a threshold is crossed.

## Information-value ranking

1. validate two-agonist NPYLR7 pharmacology in LVP;
2. validate the Ir68a B channel with independent alleles plus competence control;
3. measure whether state manipulation changes A/B relative response/dependency;
4. only then invest in same-background A genetics;
5. only after same-background causal closure revisit genotype-policy mutation structure.

This ordering maximizes the chance that each expensive genetic step answers a question not already falsified by cheaper experiments.
