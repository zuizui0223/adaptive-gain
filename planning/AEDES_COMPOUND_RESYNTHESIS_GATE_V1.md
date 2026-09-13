# Aedes compound resynthesis gate v1

## Status

Execution-logistics planning only. This document is downstream of:

- `freeze/aedes-pre-data-admission-v1`;
- `freeze/aedes-execution-planning-v1`;
- `freeze/aedes-execution-readiness-v1`;
- `freeze/aedes-assay-readiness-v1`.

It does not alter the frozen scientific task, locked Phase-1 compounds, confirmatory rules, or assay semantics.

## Locked compounds

Phase 1 remains locked to:

1. `TDI-014188`;
2. `TDI-014186`.

No third compound is an allowed rescue after LVP outcome data are opened.

## Why this gate exists

The current highest-risk material is access to the two NPYLR7 agonists. Public evidence establishes that:

- Zeledon et al. 2024 synthesized 128 analogs and states that individual synthetic reaction details are provided in Supplementary Material 3;
- Supplementary Material 3 is the published DOCX `13071_2024_6347_MOESM3_ESM.docx`;
- the paper is in the PMC Open Access collection (`PMC11212260`);
- NCBI provides an official PMC-SM-BioC API that converts Open Access supplementary documents into machine-readable text;
- the locked compounds were selected because `TDI-014188` and `TDI-014186` produced the two largest Miniport effects in the 2024 study.

The existence of a published supplement is not itself proof that an institutional chemistry core can reproduce either compound. The exact compound sections and analytical information must first be located and reviewed.

## Two admissible access routes

### Route A — source material transfer

Preferred when possible.

Close this route only after documentation of:

- identity: `TDI-014188` and `TDI-014186`;
- amount available for pilot plus confirmatory work;
- purity / lot information;
- solvent and stock concentration;
- storage conditions;
- feeding formulation compatibility;
- institutional transfer / shipping requirements.

A verbal statement that the compounds exist is not a closed material receipt.

### Route B — institutional resynthesis

Use only if source material transfer is unavailable, impractical, or quantitatively insufficient.

Close this route only after all of the following:

1. the published supplementary chemistry text for **both** locked compounds is retrieved;
2. both compound identifiers are located in chemistry-method context, not merely in behavioral tables;
3. a qualified chemistry core reviews the reaction sequence and determines that the compounds are reproducible;
4. identity / purity acceptance criteria are prospectively declared before mosquito testing;
5. the synthesized material passes the declared analytical identity / purity checks.

The repository helper `adaptive_gain/zeledon_supplement.py` and CLI `examples/audit_zeledon_supplement.py` are designed only to close steps 1–2 reproducibly. They do not substitute for chemistry-core review or analytical validation.

## Canonical machine-readable retrieval route

The official NCBI PMC-SM-BioC API documents retrieval by PMCID and supplementary filename.

For this study the locked source identifiers are:

- PMCID: `PMC11212260`;
- supplement filename: `13071_2024_6347_MOESM3_ESM.docx`.

The helper constructs the canonical endpoint:

`https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/supplmat_relevant.cgi/bioc_xml/PMC11212260/13071_2024_6347_MOESM3_ESM.docx`

This is preferable to scraping publisher HTML because it uses the official PMC Open Access supplementary-material text-mining service.

## Repository audit states

The helper may return only these interpretation classes:

- `PUBLISHED_CHEMISTRY_CONTEXT_LOCATED__CORE_REVIEW_STILL_REQUIRED`;
- `COMPOUNDS_LOCATED__CHEMISTRY_CONTEXT_NOT_YET_QUALIFIED`;
- `SUPPLEMENT_RETRIEVED__LOCKED_COMPOUNDS_NOT_BOTH_LOCATED`.

Retrieval failure is an operational failure and must remain distinct from all three scientific/material states.

## Chemistry-core receipt required after retrieval

For each compound separately record:

- source section / supplement version;
- reaction sequence judged complete: yes / no;
- starting materials obtainable: yes / no / unresolved;
- critical reagents / conditions;
- expected final form (free base / salt, if specified);
- expected molecular identity evidence;
- expected purity evidence;
- expected or reported yield where relevant;
- synthesis risk / special handling;
- core verdict: `RESYNTHESIS_FEASIBLE`, `UNRESOLVED`, or `NOT_FEASIBLE`.

Do not copy long source passages into the repository; store source identifiers, audit hashes, and chemistry-core interpretation.

## Phase-1 material start rule

The compound side of Phase 1 is ready only if **both locked compounds** independently satisfy either:

- `SOURCE_TRANSFER_CONFIRMED`, or
- `RESYNTHESIS_ANALYTICALLY_VALIDATED`.

Mixed routes are allowed (for example, one transferred and one resynthesized) provided identity and handling are documented for both.

## Hard stops

- no substitution of `TDI-014184` or another agonist after LVP outcomes are opened;
- no claim that a supplement mention equals a valid synthesis protocol;
- no mosquito experiment with unverified compound identity;
- no use of the 2026 computational paper as a replacement for the primary 2024 chemistry methods;
- no inference from EC50 that `TDI-014186` should fail behaviorally; its low in-vitro potency is precisely why the in-vivo replication is informative;
- no changing dose or timing to rescue one locked compound after outcome inspection.

## Current status

`COMPOUND_GATE = NOT_CLOSED`

What is closed:

- compound identities are locked;
- primary paper / PMCID / supplement filename are fixed;
- publisher supplement exists;
- official NCBI machine-readable retrieval route is defined;
- retrieval/audit code is implemented and offline-tested.

What remains:

- obtain a successful live supplement audit receipt;
- source-transfer response and/or chemistry-core review;
- physical material identity / purity receipt for both locked compounds.
