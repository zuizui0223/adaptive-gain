# Aedes compound resynthesis gate v1

## Status

Execution-logistics planning only. This document is downstream of:

- `freeze/aedes-pre-data-admission-v1`;
- `freeze/aedes-execution-planning-v1`;
- `freeze/aedes-execution-readiness-v1`;
- `freeze/aedes-assay-readiness-v1`.

It does not alter the frozen scientific task, locked Phase-1 compounds, confirmatory rules, or assay semantics.

Current compound-gate state:

`PUBLISHED_CHEMISTRY_CONTEXT_LOCATED__CORE_REVIEW_STILL_REQUIRED`

This is a real advance over supplement availability alone, but it is **not** material access and does not permit Phase 1 to start.

## Locked compounds

Phase 1 remains locked to:

1. `TDI-014188`;
2. `TDI-014186`.

No third compound is an allowed rescue after LVP outcome data are opened.

## Live supplementary-method audit closed

A one-off GitHub Actions run executed the repository's non-verbatim supplement audit against the official PMC Open Access distribution.

Execution receipt:

- workflow run: `34730165648`;
- job: `103651359191`;
- conclusion: `success`;
- official source used: PMC Open Access AWS object;
- source URL: `https://pmc-oa-opendata.s3.amazonaws.com/PMC11212260.1/13071_2024_6347_MOESM3_ESM.docx`;
- source DOCX SHA256: `abce4630ff01aaa83545a3a4690f04e3c97061acba90d2bb3ecda9256dfb33b9`;
- extracted normalized text: 57,513 characters;
- archived JSON receipt artifact: `10308124041` (`zeledon-supplement-audit-receipt`);
- artifact SHA256: `7ea3bb3338a3fbddf445a095eaecb5902e25f3a369ab1d14277e751c58587cbd`.

The live audit found both locked compound identifiers exactly once in chemistry-method context.

### `TDI-014188`

Nearby chemistry-method signals:

- `chromatography`: 2;
- `lcms`: 1;
- `mmol`: 18;
- `nmr`: 1.

### `TDI-014186`

Nearby chemistry-method signals:

- `chromatography`: 1;
- `lcms`: 2;
- `mmol`: 15;
- `nmr`: 2.

The correct interpretation is therefore:

`PUBLISHED_CHEMISTRY_CONTEXT_LOCATED__CORE_REVIEW_STILL_REQUIRED`

The repository deliberately stores counts, hashes and source identifiers rather than copying the supplementary chemistry prose.

Canonical machine-readable receipt:

`validation/AEDES_ZELEDON_SUPPLEMENT_LIVE_AUDIT_V1.json`

## Why this does not yet close resynthesis

The live receipt closes two previously open questions:

1. Supplementary Material 3 is retrievable through an official PMC distribution path.
2. Both preregistered compounds occur in genuine chemistry-method context rather than only in behavioral tables.

It does **not** establish that:

- the reaction sequence is complete enough for independent reproduction;
- all starting materials and intermediates are obtainable;
- the exact final chemical form is unambiguous;
- an institutional chemistry core judges the synthesis practical;
- a synthesized product has the correct identity;
- a synthesized product meets a prospectively declared purity threshold.

Those remain chemistry-core / physical-material gates.

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

Use if source material transfer is unavailable, impractical, or quantitatively insufficient.

Steps 1–2 below are now **closed** by the live audit:

1. [x] retrieve the published supplementary chemistry document through an official path;
2. [x] locate both locked identifiers in chemistry-method context rather than merely behavioral tables;
3. [ ] qualified chemistry core reviews the reaction sequence and determines whether each compound is reproducible;
4. [ ] identity / purity acceptance criteria are prospectively declared before mosquito testing;
5. [ ] physical synthesized material passes the declared analytical identity / purity checks.

The helper `adaptive_gain/zeledon_supplement.py` and CLI `examples/audit_zeledon_supplement.py` close only the retrieval/context layer. They do not substitute for chemistry-core review or analytical validation.

## Reproducible official retrieval routes

The helper uses two official NCBI/PMC paths in order:

1. PMC-SM-BioC relevant-supplement endpoint;
2. PMC Open Access AWS object for the published DOCX.

Locked identifiers:

- PMCID: `PMC11212260`;
- PMC version: `1`;
- supplement filename: `13071_2024_6347_MOESM3_ESM.docx`.

The successful live receipt used the AWS object. The parser extracts only DOCX WordprocessingML text and emits aggregate audit signals, not source prose.

## Chemistry-core receipt required next

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
- no claim that chemistry-context detection equals a complete synthesis protocol;
- no mosquito experiment with unverified compound identity;
- no use of the 2026 computational paper as a replacement for the primary 2024 chemistry methods;
- no inference from EC50 that `TDI-014186` should fail behaviorally; its low in-vitro potency is precisely why the in-vivo replication is informative;
- no changing dose or timing to rescue one locked compound after outcome inspection.

## Current status summary

Closed:

- locked compound identities;
- primary paper / PMCID / supplement filename;
- official machine-readable retrieval logic;
- successful live retrieval of the primary chemistry supplement;
- locked compound presence in chemistry-method context for both compounds;
- reproducible source/document hashes and execution receipt.

Still open:

- source-material transfer response;
- chemistry-core route-completeness / feasibility review;
- prospectively fixed identity/purity acceptance criteria;
- physical compound identity / purity receipt for both locked compounds.

Therefore:

`COMPOUND_MATERIAL_GATE = NOT_CLOSED`
