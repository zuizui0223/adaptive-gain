# Aedes chemistry-core review packet v1

## Purpose

Provide a minimal, auditable handoff to an institutional medicinal/synthetic chemistry core for the two locked Phase-1 NPYLR7 agonists without copying the published supplementary chemistry prose into this repository.

This packet does not change the frozen Aedes task, compounds, dose, timing, assay, or confirmatory rules.

## Locked compounds

Review **both** independently:

1. `TDI-014188`
2. `TDI-014186`

No substitute compound is in scope.

## Primary source identity

Use the primary 2024 chemistry supplement, not a later computational reconstruction.

- article: Zeledon et al. 2024, *Parasites & Vectors*, DOI `10.1186/s13071-024-06347-w`;
- PMCID: `PMC11212260`;
- supplement: `13071_2024_6347_MOESM3_ESM.docx`;
- audited source SHA256: `abce4630ff01aaa83545a3a4690f04e3c97061acba90d2bb3ecda9256dfb33b9`;
- canonical validation receipt: `validation/AEDES_ZELEDON_SUPPLEMENT_LIVE_AUDIT_V1.json`.

The repository audit has already established that both locked identifiers occur in genuine chemistry-method context and that NMR/LCMS-related analytical information is present nearby. It has **not** judged the reaction sequence chemically sufficient.

## Core review question

For each locked compound, answer:

> Does the primary Supplementary Material 3 contain a sufficiently complete, unambiguous and practically executable route for an independent institutional chemistry core to produce analytically verified material suitable for the preregistered mosquito experiment?

Do not answer this from scaffold similarity or from the 2026 computational follow-up.

## Required extraction — one record per compound

Record facts without pasting long source passages.

### A. Route completeness

- compound identifier;
- source section / page or searchable heading;
- number of synthetic transformations needed from commercially available or clearly identified starting material;
- whether each intermediate used in the final sequence is itself either commercially obtainable or described sufficiently in the supplement;
- whether quantities / stoichiometry are sufficient to reproduce each critical step;
- whether temperature, time, solvent and work-up are sufficiently specified for each critical step;
- whether chromatographic or other purification method is sufficiently specified;
- whether any critical step depends on an unnamed proprietary reagent, unpublished precursor, or inaccessible internal procedure.

Classify:
- `ROUTE_COMPLETE`;
- `ROUTE_INCOMPLETE`;
- `ROUTE_AMBIGUOUS`.

### B. Starting-material accessibility

For every required starting material or precursor, classify:
- `COMMERCIAL_OR_ROUTINELY_AVAILABLE`;
- `SUPPLEMENT_DESCRIBED_PRECURSOR`;
- `CUSTOM_BUT_FEASIBLE`;
- `ACCESS_UNRESOLVED`.

A single unresolved essential precursor keeps resynthesis feasibility unresolved.

### C. Final chemical identity

Record:
- final chemical form specified or inferred from the primary method (free base, salt, etc.);
- molecular formula / expected mass if explicitly supported by the source;
- analytical modalities reported for the final compound (for example NMR and LCMS);
- whether the source evidence is sufficient to define an independent identity check.

Do not use biological activity as an identity assay.

### D. Prospective acceptance plan

Before synthesis is ordered or mosquito data are generated, the chemistry core should propose:
- identity test(s);
- purity method;
- minimum purity acceptance threshold appropriate for the intended biological use;
- residual-solvent / salt-form considerations if relevant;
- storage form and conditions;
- recommended preparation of the stock solution compatible with the frozen mosquito-feeding protocol.

The purity threshold must be declared **before** seeing mosquito treatment outcomes.

### E. Practical synthesis risk

Classify:
- `LOW` — routine chemistry, expected to be straightforward;
- `MODERATE` — feasible but with nontrivial step, purification or precursor burden;
- `HIGH` — technically demanding / specialized / uncertain yield or handling;
- `NOT_FEASIBLE` — core cannot execute the primary route as documented.

Also note any safety, controlled-reagent or specialized-equipment constraints.

## Compound-level terminal verdict

Each compound must receive exactly one:

- `RESYNTHESIS_FEASIBLE_PENDING_PHYSICAL_VALIDATION`;
- `RESYNTHESIS_UNRESOLVED`;
- `RESYNTHESIS_NOT_FEASIBLE`.

A feasible paper route still does not equal usable material. `RESYNTHESIS_FEASIBLE_PENDING_PHYSICAL_VALIDATION` only unlocks procurement/synthesis.

## Physical-material closure after synthesis

For each synthesized batch record:
- batch identifier;
- synthesis date / core;
- analytical identity result;
- measured purity;
- declared purity threshold;
- pass/fail;
- storage condition;
- stock-preparation record;
- amount released for pilot / confirmatory work.

Only a passing batch may be assigned:

`RESYNTHESIS_ANALYTICALLY_VALIDATED`.

## Phase-1 compound gate

Both locked compounds must independently be one of:

- `SOURCE_TRANSFER_CONFIRMED`, or
- `RESYNTHESIS_ANALYTICALLY_VALIDATED`.

Anything weaker leaves:

`COMPOUND_MATERIAL_GATE = NOT_CLOSED`.

## Hard stops

- no substitution of another agonist because one route is inconvenient;
- no purity threshold chosen after behavioral outcomes are visible;
- no biological potency used to rescue failed chemical identity;
- no mixing source-transferred and resynthesized batches without recording provenance independently;
- no assumption that one compound's feasible synthesis proves the other's route;
- no long verbatim reproduction of Supplementary Material 3 in the repository.
