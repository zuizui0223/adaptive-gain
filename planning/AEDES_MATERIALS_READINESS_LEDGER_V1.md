# Aedes materials readiness ledger v1

## Status

Execution-readiness planning only. This file is downstream of the immutable planning freeze at `freeze/aedes-execution-planning-v1` and does not modify the frozen scientific task or confirmatory decision rules.

## Executive conclusion

The main physical bottleneck is **not** wild-type LVP access or the Ir68a phenotype itself. Public/source-lab access paths exist for most mosquito assets. The largest immediate bottleneck is the NPYLR7 small-molecule intervention, because the active TDI compounds are not currently represented by an obvious public stock/catalog path in the material audit and were synthesized within the TDI medicinal-chemistry program.

The practical acquisition order should therefore be:

1. secure/confirm LVP baseline access;
2. request the Ir68a causal lines directly from the generating lab;
3. request or arrange synthesis of two preselected active NPYLR7 agonists;
4. only after Phase 1-3 justify it, obtain or recreate same-background Ir8a genetics.

## 1. LVP baseline mosquito stock — public path exists

### BEI LVP-IB12

BEI Resources currently lists `Aedes aegypti LVP-IB12` as `MRA-735` (eggs) in its mosquito catalog. Public catalog evidence also lists an LVP-IB12 frozen kit (`MRA-735K`) and bulk frozen material (`MRA-735B`).

Interpretation:

- obtaining a public Liverpool/LVP baseline is not the principal blocker;
- before treating MRA-735 as equivalent to the exact parental LVP stock used in the Ir68a study, verify pedigree/parental identity with the Ir68a generating lab;
- do not silently equate `Black Eye Liverpool` (`NR-48921`) with LVP-IB12 for the confirmatory causal experiment.

### Black Eye Liverpool

BEI also currently lists `NR-48921`, Black Eye Liverpool eggs, as in stock. This is a useful additional Liverpool resource but is not prospectively substituted for the frozen LVP-first plan without a new background decision.

## 2. Ir68a B-side causal lines — direct lab request path exists

Tang et al. 2024 generated independent `Ir68a` knock-in alleles (RFP and EYFP) in the LVP framework and used both in the wet-container/site-finding assay.

Crucially, the paper states:

> all unique/stable reagents generated in the study are available from the lead contact without restriction.

Therefore the preferred route is **request the published Ir68a lines**, not recreate them before Phase 2.

Requested minimum package:

- `Ir68a^EYFP` line;
- `Ir68a^RFP` line;
- parental LVP stock/pedigree information;
- current rearing notes relevant to the published site-seeking assay;
- if available, the reporter/helper line needed for Moist-Cell imaging.

Phase 2 should use both independent Ir68a alleles under the already frozen replication rule.

## 3. Moist-Cell imaging assets — partial public path, source-lab route remains simplest

BEI currently lists a Liverpool-derived `PUb-GCaMP6s` strain (`NR-51480`) as in stock. This confirms that public calcium-reporter mosquito resources exist.

However, the frozen Phase 2 plan should not silently replace the reporter configuration used in the Ir68a study with `PUb-GCaMP6s` merely because it is catalogued.

Preferred order:

1. reproduce the behavioral B phenotype first;
2. obtain the exact reporter/helper configuration from the Ir68a generating lab if sensory imaging is required;
3. use a public alternative reporter only as a prospectively documented method substitution with a validation bridge.

## 4. Ir8a A-side genetics — causal lines exist, but public-stock route is not yet closed

Published Orlando-background Ir8a causal lines include independent `Ir8a^attP` and `Ir8a^DsRed` alleles, and later mosquito genetic-tool work continues to use/request IR8a strains and plasmids.

Current literature also reports that strains and plasmids are available upon request, and a modern IR8a plasmid sequence is deposited in GenBank (`pBB-AaIR8a`, accession `PQ671724`).

No dedicated current BEI listing for the exact Ir8a mutant pair surfaced in this audit.

Therefore the execution plan remains correct:

- do **not** make Ir8a acquisition a Phase 1 blocker;
- after a positive routing screen, request the existing Orlando Ir8a lines and decide whether to backcross/recreate them in LVP;
- if line transfer is infeasible, use the published molecular constructs / target information to recreate the allele only after Stage B is justified.

## 5. NPYLR7 active agonists — current primary materials bottleneck

The confirmatory Phase 1 design requires two independent active compounds.

Published active compounds at 1 micromolar include:

- `TDI-014184`;
- `TDI-014186`;
- `TDI-014188`.

The 2024 study reports that compound synthesis was coordinated through the Sanders Tri-Institutional Therapeutics Discovery Institute (TDI) medicinal-chemistry program.

A current public commercial/catalog supplier for these TDI compounds did not surface in the materials search.

Implication:

**Do not order mosquitoes before confirming a compound path.**

Preferred acquisition sequence:

1. contact the study corresponding/medicinal-chemistry team to request two active compounds or transfer-ready aliquots;
2. if direct transfer is unavailable, ask whether synthetic routes / intermediates / analytical specifications can be shared;
3. only then commission resynthesis through an institutional medicinal-chemistry/core facility;
4. retain the preselected two-compound rule — do not screen a larger analog library and select whichever pair works best in LVP.

For Phase 1, the preferred pair remains two compounds with independent published in-vivo activity. `TDI-014188` is the strongest first anchor because it combined high in-vitro potency with strong in-vivo suppression; the second compound must be frozen before any LVP outcome is opened.

## 6. Assay hardware — no major proprietary blocker identified

### Host-seeking

The miniport olfactometer used in the NPYLR7 work is a custom behavioral apparatus rather than a proprietary platform. The published methods and figures provide enough architecture to reproduce the assay, but a build/validation run should precede confirmatory treatment testing.

### Wet-container seeking

The Ir68a B assay is likewise a custom container-seeking behavioral setup. Its critical biological validation is not the hardware itself but:

- mature-gravid timing;
- fixed circadian window;
- wet-versus-dry geometry;
- prevention of trivial direct contact;
- direct-placement egg-laying competence control.

Thus hardware is secondary to biological standardization.

## 7. Resource-risk classification

| Asset | Current path | Risk | Phase consequence |
|---|---|---|---|
| LVP baseline | BEI MRA-735 public catalog | low | not a blocker |
| Black Eye Liverpool | BEI NR-48921 public catalog | low | auxiliary only |
| Ir68a EYFP/RFP | lead-lab request, stated unrestricted | medium | Phase 2 blocker if unavailable |
| exact Moist-Cell reporter stack | source-lab request / alternative reporter possible | medium | imaging only; behavior can proceed first |
| Ir8a alleles | source-lab request; recreation path exists | medium | defer until Stage B |
| NPYLR7 agonist #1 | author/TDI request or resynthesis | high | Phase 1 blocker |
| NPYLR7 agonist #2 | author/TDI request or resynthesis | high | Phase 1 blocker |
| miniport assay | custom build | medium-low | validate before confirmatory run |
| wet-container assay | custom build | low | replicate published geometry |

## 8. Immediate action order

Before any biological experiment starts, obtain four yes/no receipts:

1. `LVP_ACCESS = yes/no`;
2. `IR68A_TWO_ALLELES_ACCESS = yes/no`;
3. `NPYLR7_AGONIST_1_ACCESS = yes/no`;
4. `NPYLR7_AGONIST_2_ACCESS = yes/no`.

The highest-information first administrative action is to resolve the two agonist receipts, because every other current asset has a clearer public or source-lab acquisition path.

## 9. Hard stops

- do not substitute another mosquito background because one stock ships faster;
- do not replace the two preselected NPYLR7 agonists after seeing one fail in LVP;
- do not replace Ir68a with another humidity receptor if the published line request fails;
- do not treat public Liverpool reporters as equivalent to the published Ir68a reporter stack without validation;
- do not recreate Ir8a genetics before the cheaper routing screen justifies Stage B;
- do not concatenate published effects from different backgrounds into one empirical finite-task receipt.

## Public/source references used for readiness audit

- BEI Resources mosquito catalog: LVP-IB12 `MRA-735`, Black Eye Liverpool `NR-48921`, and Liverpool-derived `PUb-GCaMP6s` `NR-51480`.
- Tang et al. 2024, PNAS, DOI `10.1073/pnas.2407394121`: Ir68a RFP/EYFP alleles; unique/stable reagents available from lead contact without restriction.
- Raji et al. 2019, Current Biology, DOI `10.1016/j.cub.2019.02.045`: independent Orlando Ir8a alleles.
- Shankar et al. / later Aedes olfactory-tool work: IR8a strains/plasmids available upon request; `pBB-AaIR8a` GenBank `PQ671724`.
- Zeledon et al. 2024, Parasites & Vectors, DOI `10.1186/s13071-024-06347-w`: active TDI NPYLR7 agonists and TDI-coordinated compound synthesis.
