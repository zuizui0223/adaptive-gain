# Aedes locked-compound outreach addendum v1

## Purpose

Supersede **only the NPYLR7 compound-request subsection** of the frozen `planning/AEDES_MATERIAL_REQUEST_OUTREACH_PACKET_V1.md`.

The older readiness packet was frozen before the second Phase-1 agonist was selected and therefore still says `TDI-014184` or `TDI-014186`. That wording is no longer valid for new outreach.

All non-compound portions of the frozen outreach packet remain unchanged.

## Locked pair

Every new compound request must name exactly:

1. `TDI-014188`
2. `TDI-014186`

`TDI-014184` is literature context only and is **not** an allowed alternative within Phase-1 v1.

## Preferred contact order

1. Laura B. Duvall — `lbd2126@columbia.edu`
2. Sanders Tri-Institutional Therapeutics Discovery Institute — `info@tritdi.org`
3. Mayako Michino / TDI medicinal chemistry — `mmichino@tritdi.org`

Do not send a broad request for any active NPYLR7 compound.

## Updated request goal

Close, for each locked compound independently, either:

- `SOURCE_TRANSFER_CONFIRMED`, or
- a concrete source-lab / TDI path to chemistry-core resynthesis support.

Published Supplementary Material 3 has now been live-audited and both locked identifiers are confirmed in chemistry-method context. Therefore a reply saying physical material is unavailable does **not** end the route; ask whether the source team can clarify any ambiguity a local chemistry core encounters in the published method.

## Information to request for physical transfer

For **both `TDI-014188` and `TDI-014186`**, request:

- research-use amount available;
- compound identity and final chemical form;
- lot / batch identifier;
- measured purity and analytical method;
- solvent and stock concentration used in the mosquito experiments;
- storage / stability guidance;
- compatibility with the published 1 micromolar non-nutritive feeding formulation;
- institutional transfer / shipping requirements;
- whether the same physical batches were used for the published Miniport and biting assays, if known.

## Information to request if direct transfer is unavailable

The primary chemistry supplement has already been retrieved from PMC Open Access and audited by hash. A local chemistry core will review the published sequence.

Ask whether the source team can provide, if needed:

- confirmation of final salt/free-base form;
- clarification of any unpublished precursor naming or internal intermediate;
- expected LCMS / NMR identity checkpoints;
- expected purity range for the biological experiments;
- practical storage / stock-preparation advice;
- contact with the TDI chemist most appropriate for a method clarification.

Do **not** request a different agonist as a backup.

## Current source receipt to mention if useful

The repository has already verified the primary Supplementary Material 3:

- PMCID `PMC11212260`;
- file `13071_2024_6347_MOESM3_ESM.docx`;
- source SHA256 `abce4630ff01aaa83545a3a4690f04e3c97061acba90d2bb3ecda9256dfb33b9`;
- both locked compound IDs found in chemistry-method context.

This makes the request narrower: physical material is preferred, but published resynthesis is a credible second route rather than an unspecified fallback.

## Updated email draft

**Subject:** Request for TDI-014188 and TDI-014186 for a preregistered *Aedes aegypti* replication

Dear Dr. Duvall,

I am preparing a preregistered replication and extension of the nutrient-independent NPYLR7 host-seeking suppression result in *Aedes aegypti*. The study is deliberately staged: the pharmacological state perturbation must first replicate in a Liverpool/LVP background before any downstream genetic integration is attempted.

The two Phase-1 agonists have been fixed in advance as **TDI-014188 and TDI-014186**. Would it be possible to obtain small research-use aliquots of these two compounds? I would also be very grateful for batch/purity information, the solvent and stock concentration used for mosquito feeding, storage guidance, and any handling detail needed to reproduce the published 1 micromolar non-nutritive feeding assay.

The confirmatory rule is fixed prospectively: both compounds must reproduce the preregistered host-suppression direction, and failure of one compound will not trigger post-hoc screening of another agonist.

We have also retrieved the primary 2024 Supplementary Material 3 through PMC Open Access and confirmed that both locked compounds occur in chemistry-method context. If direct compound transfer is not possible, would you or the TDI medicinal-chemistry team be willing to clarify any ambiguity that an institutional chemistry core encounters while evaluating the published routes for resynthesis, particularly final chemical form, analytical identity checkpoints, and storage/stock preparation?

Thank you very much for considering this request.

Best regards,
Ruiqi Zhang

## Receipt rule

Any response must be classified per compound as one of:

- `AVAILABLE_DIRECT_TRANSFER`;
- `AVAILABLE_WITH_MTA_OR_INSTITUTIONAL_PROCESS`;
- `RESYNTHESIS_SUPPORT_AVAILABLE`;
- `RESYNTHESIS_WITHOUT_SOURCE_SUPPORT`;
- `UNAVAILABLE`;
- `NO_RESPONSE_YET`.

`NO_RESPONSE_YET` must never be promoted to `UNAVAILABLE`.

## Hard stop

Do not use the obsolete phrase `TDI-014184 or TDI-014186` in any new outreach. The locked v1 pair is `TDI-014188 + TDI-014186`.
