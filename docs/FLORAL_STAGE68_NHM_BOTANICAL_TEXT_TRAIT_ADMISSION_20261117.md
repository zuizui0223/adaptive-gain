# Stage68 | Original botanical-description floral traits, strictly textual

2026-11-17 JST. Draft stacked on Stage67 PR #146. Main is unchanged. This is source auditing, not a new ecological coefficient.

## Original data and why it matters

[Natural History Museum plant-traits](https://github.com/NaturalHistoryMuseum/plant-traits) releases CC-BY NLP-extracted text descriptions from BHL, eFloras and Ecoflora. Its source README reports 59,369 plant species and 888,328 trait entries. **Use only output/raw/ocr-traits; do not read the photo-derived cv-traits dataset.** The source is absent from the frozen Stage67 26-source registry, and is separate from the 880 previously accepted optical/flower-age evidence species.

## Independently observed Ecoflora pilot

Git blob SHA-1: dbdc6b4469583743b8b35e26912d21d05b550f32; 524,901 raw bytes; 84 source columns; 1,989 distinct literal taxon labels, no duplicate taxon label.

- At least one recorded flower/petal/corolla colour text field: **1,141**.
- At least one recorded flower shape/symmetry/orientation/tube min/max length: **304**.
- Both text-colour and structure categories: **249**.
- Source text rows with pollination descriptor: **1**; reward: **7**.

These are NLP description records, not directly measured UV spatial sectors, nectar-guide presence, pollinator visits, or trait function. Multi-state phrases are retained per original organ; they are not converted into synthetic flowers. A blank is UNKNOWN, never a biological negative.

## Full original source source-authentic ingestion

The Stage68 GitHub Action downloads two original text CSVs from NHM. Git-object content SHA-1 is checked byte-for-byte; combined original is pinned to e1cfd2d5c518c2061ec91d1a9e8b64fc7ca69389. An original 59k-scale file is processed and both source-coverage receipts and compact taxon-level text traits are saved as Action artifacts. The README's stated 59,369 species has now been independently reproduced from the source file under SHA authentication (see final verified results below). Tests guard organ separation, CSV quoting, missing trait states, duplicate labels, and source digest integrity. No individual photographic pixels are consumed.

## Independently source-verified full results and crosswalk (2026-11-17)

**All Stage68 source checks passed in GitHub Actions run [44051561567](https://github.com/zuizui0223/adaptive-gain/actions/runs/44051561567)**. Six text-only extraction tests plus four literal species-name crosswalk tests passed, and the original Ecoflora and full 17,279,412-byte NHM combined CSV both passed Git blob identity checks. The separate, authenticated Stage67 73-species spectroscopy artifact was retrieved via GitHub CLI with the extracted original CSV SHA256 pinned; the earlier direct urllib artifact redirect gave HTTP 401 and was superseded. The final data join passed all fixed source-identity and exact count assertions.

- 59,369 literal botanical taxon labels, with no repeated literal labels;
- **31,773** taxon labels with nonempty flower/petal/corolla text colour;
- **13,508** with nonempty flower shape/symmetry/orientation/tube-length text;
- **11,105** with both colour and structural text fields;
- in the original **73** measured-petal-spectra names (70 strict GBIF species): **55** exact literal names occur in the NHM combined text corpus, all 55 strictly accepted on the spectroscopy side;
- of those 55, **49** have any flower colour text, **25** any structural text, and **25** both; **7** of the 55 have prior Stage67 817 optical-evidence atlas membership;
- original 73 source reflectance values remain real petal spectrometer measurements; a mean spectrum does **not** resolve the presence/absence of spatial UV guides.

The crosswalk joins **original named taxa only**. It does not validate shared native population/site, same biological individual, original taxon concept reconciliation between WFO and GBIF, pollinator guild, wind, scent, pollen deposition or plant fitness. Consequently no true global optical signal–guild slope, causal SEM or pollinator-dependent selection result has been established. The 880 Stage67 independent optical species cannot be augmented by summing the 59,369 text labels.

Action artifact: stage68-NHM-original-botanical-TEXT-59k-traits-no-photo-no-UV (artifact ID 14313209081; SHA256 efa944763aa5971f7642f063295436119c9cafae204325922e9979f3214d1d85). It includes both text-coverage receipts, compact 59k source traits, exact 73-name crosswalk and join receipt.

## Next required source admission gates

1. Verify Action run and inspect actual all-corpus totals; distinguish literal taxon labels, independently measured species, and duplicated records.
2. Strictly match the original Stage67 880 optical species accepted keys using WFO and GBIF, without genus-level imputation. **Not yet measured; do not add 1,989 or 59,369 to 880.**
3. Attach separately sourced native region, site and measured plant-visitor interactions for bee/Bombus, butterfly, fly and bird guilds. Visitation is not proof of successful pollen transfer. Plant colour cannot define its own guild predictor.
4. Co-locate climate, UV-B/light, source site/year and wind exposure. If no source-site/time alignment exists, no mediation SEM or wind×scent×visual interaction is identified.
5. Compare genuinely observed signal modalities in multiple source-independent regions, with genus/phylogeny and geographic holdout. Report selection/missingness and confidence intervals. No new global receiver-specific coefficient yet.

## Scientific limit and novelty

Mean reported human colour × bee richness is not automatically original: multi-site floral spectra/pollinator diversity gradients and published island colour/bee visitation precede Stage68. The target is receiver-specific ecological sorting among distinct genuine optical/scent/reward-state information modalities, if original matching data can identify it. NHM textual records may help denominators and floral architecture controls; they do not on their own support causal pollinator selection, UV nectar-guide presence or field use.

Original source: https://github.com/NaturalHistoryMuseum/plant-traits
DOI metadata: https://data.nhm.ac.uk/dataset/angiosperm-functional-traits-extracted-from-botanical-descriptions
Original data license: CC-BY. Preserve source attribution.
