# Stage69 | Corrected original observed guild networks joined to NHM floral TEXT and independently measured petal spectra

2026-11-17 JST. Source-authenticated SUCCESS on [GitHub Actions run 44056410895](https://github.com/zuizui0223/adaptive-gain/actions/runs/44056410895). Draft stacked on Stage68 PR #147; main remains untouched. This is **data admission and audit, not a biological effect-size result**.

## Critical original-source correction

Use original **EuPPollNet version v1.3.0**, [Zenodo DOI 10.5281/zenodo.15183272](https://doi.org/10.5281/zenodo.15183272), and editorial [correction 10.1111/geb.70054](https://doi.org/10.1111/geb.70054). Older articles/versions with 1,162,109 reported interactions contain duplicated rows and are not suitable. The pinned AUTHOR GitHub release (canonical renamed repository `joseblanuza/EuPPollNet@v1.3.0`, *not* evolving main) has compressed source Git blob SHA1 `6e639d4af81feee76eefa6804622f8b901c39feb` and **623,476** actual source rows, across **1,864** distinct study×network×year keys from **54** study IDs. The original 30 columns include actual recorded plant/pollinator accepted names, date, location, survey ID, group taxonomy and flower-count link.

Important nonindependence: original `Metadata.csv` has **80 study×year records across 54 studies**, not 80 independent studies. Matching requires the actual study/year. The corrected source contains **8** observation rows with non-UTF8 bytes, exclusively in `Pollinator_original_name`; source bytes are still SHA-verified, invalid decoded characters are separately counted, and no damaged accepted plant name is used for an invented taxon match.

## Authenticated actual new source overlaps

- Of source confident species-ranked plant names, **1,408** distinct source names; after literal-name matching to 59,369 original NHM botanical text taxa, **963** are represented.
- **809** of those 963 have original botanical source flower/petal/corolla text colour; **378** have both text colour and structural description.
- Of original 73 truly spectrophotometer-measured petal taxa from Stage67, **36** have actual EuPPollNet records, and **32** also match NHM botanical text.
- Of those 32, **28** have any original *Bombus* visitation record, and **24** occur in at least one single source study×network×year with recorded *Bombus* and a different bee/fly/Lepidoptera visitor category for that same plant.
- Original visits reduce to **18,798** qualified plant×network×year observed-presence units, **16,210** of them with literal NHM taxon label matching, **15,305** with source flower colour text, and **2,557** source units with a real petal spectral species.
- Corrected original source guild record partition: *Bombus* 79,113; other taxonomically recognised bees 457,167; nonbee Hymenoptera 4,348; Diptera 56,200; Lepidoptera 7,749; Coleoptera 18,074; other/unknown 825. These numbers are source observation records, **not census abundance, legitimate pollen transfers or standardized guild opportunities**.
- No source row had missing/unparseable site coordinates or year in the audit; observed site-network-coordinate grouping gave 1,638 keys, which is NOT the same quantity as the article's 1,214 unique sampling locations.

Source run: [44056410895](https://github.com/zuizui0223/adaptive-gain/actions/runs/44056410895), artifact **14317000061**, SHA256 `928cbdfd695b92e58b72451fbac267d19b6295eda366a7c9ad78970a05db9075`.

## Inferential grain and hard caveats

1. A record reports a taxon observed on a flower under the source protocol, not necessarily plant pollen fitness or an effective pollinator.
2. Original EuPPollNet ecological coverage is European and strongly Hymenoptera/bee-weighted. It contains no bird/hummingbird pollination data and cannot directly compare bird versus bee syndromes worldwide.
3. Plant `Plant_rank=SPECIES` must be source accepted and `Plant_unsure_id` not affirmative for strict match; genus/family rows never become species observations.
4. The recorded visitor set does not provide surveyed species-level visitor absences. Lack of a *Bombus* record in a bee-only or sparsely sampled study is **UNKNOWN opportunity**, not evidence of local absence. Different methods and study effort require explicit stratification.
5. Actual petal reflectances for 36 taxa come from a published German botanical-garden spectroscopy source, **not the EuPPollNet field plant individuals/sites**. Their cross-study same-species-name join does not establish native source range, flowering-phase co-occurrence, bee receptor-guidance function or causal optical adaptation.
6. Modalities remain distinct: UV 300–399nm **mean reflectance percentage** is not a directly measured UV bullseye; text visible colour is an organ description; published spatial UV guide states from 230 other species are a separate original source; floral scent missing is not zero.
7. Neither meteorological wind nor valid site-year climatic/environmental treatment is presently linked. Causal path SEM, pollen fitness effects and adaptation remain **NO GO**.

## Next analytical decision

Before producing any floral trait×guild regression, count how many independent study IDs and network/site blocks actually contain ≥2 *different* real spectrometer species in the **same network** and both observed guild channels under comparable sampling. Also trace matched site native ranges via official Kew/WCVP native TDWG-L3; accepted-name equality alone is insufficient. Require geographic and study holdouts, include effort-type conditioning, and use actual source-specific optical measurements when possible.

Existing and new Stage69 code:
- `research/floral_literature_macro_stage69/ingest_original_corrected_EuPPollNet_network_NHM_spectra.py`
- `research/floral_literature_macro_stage69/test_original_corrected_EuPPollNet_network.py`
- `.github/workflows/floral-stage69-corrected-euppollnet-network.yml`.

No photographs, image-derived colour, invented UV-guide absence, invented visitor guild from colour, or causal SEM.
