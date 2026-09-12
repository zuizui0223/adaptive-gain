# Aedes Japan import and containment gate v1

## Status

Execution-readiness planning only. This is a regulatory/logistics gate, not legal advice and not a determination that *Aedes aegypti* can or cannot currently be imported into Japan.

The current scientific and execution freezes remain unchanged.

## Why this gate is necessary

A public stock catalog entry does **not** imply that live eggs can be shipped to and legally received by a Japanese institution.

The Ministry of the Environment's current Alien Species Act guidance distinguishes among:

- Designated Invasive Alien Species, for which import/keeping is generally prohibited without prior authorization;
- Unevaluated Alien Species, for which prior notification and review may be required;
- living organisms requiring a Certificate of Species;
- organisms outside those categories.

Depending on classification, import may require prior keeping authorization, notification, a Certificate of Species, and clearance only through designated airports.

The official guidance also states that certain regulated living organisms cannot be imported by ordinary postal service and that some review procedures may take up to six months.

This audit has **not** established the current legal classification of *Aedes aegypti* under those categories. Therefore the correct current status is:

`JAPAN_AEDES_REGULATORY_CLASSIFICATION = UNRESOLVED`

not `allowed` and not `prohibited`.

## 1. Pre-order institutional gate

Before placing any order/request for live eggs or mutant mosquitoes, obtain written confirmation from the receiving institution's biosafety / research-compliance office covering:

1. whether the institution is approved and equipped to maintain live *Aedes aegypti*;
2. what containment level and escape-prevention conditions are required locally;
3. whether an Alien Species Act authorization, notification, or species certificate applies to *Aedes aegypti* eggs/adults;
4. whether any additional infectious-disease/vector or local institutional approvals apply;
5. who is authorized to act as importer/consignee;
6. which Japanese port/airport should be used if live import is permitted.

Do not use an individual researcher as the default consignee before this institutional gate is closed.

## 2. Ministry of the Environment gate

If institutional compliance cannot give a definitive classification, contact the relevant Regional Environment Office / Ministry of the Environment Alien Species Management Office before shipment.

The question should be narrow:

> For live laboratory *Aedes aegypti* eggs/lines imported solely for contained academic research, what current category and pre-import documentation apply under the Alien Species Act?

Provide:

- scientific name to species level;
- life stage (eggs versus adults);
- quantity range;
- academic research purpose;
- containment description;
- intended receiving institution;
- intended airport/transport route.

Do not ask the foreign supplier to ship until the answer is documented.

## 3. BEI international-shipment gate

BEI Resources provides permit/compliance information on a product-by-product and destination-specific basis, and some BEI catalog items are explicitly restricted to domestic U.S. shipment.

Therefore `MRA-735 in stock` is only a stock-availability receipt, not an international-shipment receipt.

Before relying on BEI for live LVP eggs, confirm:

- whether `MRA-735` can currently be shipped to Japan;
- whether BEI can supply the export-side species certificate or other required document;
- required receiving permits/documents;
- packaging and transport mode;
- whether shipment can enter through the Japanese designated port required by the applicable classification;
- whether eggs can be shipped directly or must be routed through an approved courier/import broker.

If live `MRA-735` cannot be exported to Japan, do not automatically substitute another Liverpool line. Re-open the materials route while preserving the frozen background decision.

## 4. Source-lab line transfer gate

The Ir68a lines are expected to come from the generating lab rather than a public stock center.

A source-lab statement that a line is “available without restriction” concerns scientific material sharing, not Japanese import authorization.

Before accepting the lines, confirm:

- institutional MTA/transfer requirements;
- exporter ability to provide species identity documentation;
- shipping form (eggs preferred versus live adults);
- destination/import paperwork;
- whether parental LVP can be transferred in the same shipment.

## 5. Chemical compounds are a separate route

The NPYLR7 small molecules are not live organisms and should be handled under the receiving institution's ordinary chemical import/procurement and safety procedures rather than the live-organism gate.

This separation is useful operationally: compound access can be resolved while live-mosquito import paperwork is being reviewed.

## 6. Regulatory receipts

Record each independently:

- `INSTITUTIONAL_CONTAINMENT_APPROVAL = YES / NO / PENDING`;
- `JAPAN_AEDES_REGULATORY_CLASSIFICATION = RESOLVED / UNRESOLVED`;
- `MOE_PREIMPORT_REQUIREMENTS = DOCUMENTED / NOT_DOCUMENTED`;
- `BEI_MRA735_JAPAN_SHIPPING = CONFIRMED / NOT_CONFIRMED / NOT_AVAILABLE`;
- `IR68A_LAB_TRANSFER_TO_JAPAN = CONFIRMED / NOT_CONFIRMED / NOT_AVAILABLE`.

Phase 1 pharmacology can proceed only with an already lawful local mosquito colony or after the relevant live-organism receipts are closed.

## 7. Hard stops

- do not infer import permission from BEI `In Stock` status;
- do not infer Japanese legal classification from older ecological/invasive-species lists;
- do not ship live eggs by ordinary post unless the applicable official procedure explicitly permits the chosen route;
- do not bypass institutional biosafety/compliance by using a personal recipient;
- do not replace LVP with a more easily imported stock without revisiting the background decision prospectively;
- do not treat a regulatory delay as biological infeasibility.

## Official/public anchors

- Ministry of the Environment, Japan: Alien Species Act import-regulation guidance and import procedures.
- BEI Resources: destination/product-specific permit and compliance information; individual products may have international-shipping restrictions.
