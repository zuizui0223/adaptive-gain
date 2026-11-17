# Stage72 | Original same-community floral scent×visitation records, source-access limits for regional optical comparison

**2026-11-17 JST, Draft on top of Stage71 PR #150. Main untouched.** This is an original-public-source evidence audit and real-data reconstruction, not a new across-region visual-cue effect or causal evolution inference.

## 1. Why this stage: correct the Stage71 measurement mismatch

Stage71's 452 conservative / 625 repaired-map outcome-blind EuPPollNet networks associate **botanical-garden species-average UV reflectance** with real field observed bee events. The positive null-local UV score in the conservative subset (+0.8468) disappears in repaired geography (-0.0179); original source study composition matters. That is not evidence for local UV colour selection. We now require field source timing/site/pollinator context and original optical vs VOC observation grain, not more post-hoc splits of the same measured-garden proxy.

## 2. Source-authenticated original Kantsa 2018 data: actual downloaded and computed

**Study:** Kantsa et al., *Disentangling the role of floral sensory stimuli in pollination networks*, Nature Communications 9:1041, DOI [10.1038/s41467-018-03448-w](https://doi.org/10.1038/s41467-018-03448-w); original 2018 Figshare article DOI [10.6084/m9.figshare.5663455.v2](https://doi.org/10.6084/m9.figshare.5663455.v2). Published ecological study region: ONE Lesvos scrubland ecosystem. Original 2017 Kantsa *Nature Ecology & Evolution* study used the same plant community, so those two papers are **not two independent study regions**.

Original source files now downloaded with **exact Figshare file-ID, byte size, source supplied MD5 and independently computed SHA256**:

- `Kantsa_etal_Supp_Data1.xlsx` (source file ID 10377684, **33,745 bytes**, SHA256 `41d0c650cd9c1e02597aacf0631491615cd5214fa34a1eb18ae51a37c369b7b7`): actual field plant–insect visitation matrix.
- `Kantsa_2018_Supp_Data2.xlsx` (file ID 10389468, **90,627 bytes**, SHA256 `72a5ae89b85ac3216071560b5db36585efbba0af9ea0bef5b99c73268de557ea`): species-specific emitted VOC components with original mean emission rate **ng/g/h**.

Original public Excel source, independently reconstructed from OOXML matrix coordinates and all numeric cells, NOT taken from article title counts alone:

| Distinct original source unit | Original computed |
|---|---:|
| Source plant column names | **41** |
| Source insect visitor row names | **168** |
| Plant×visitor numeric cells, complete | **6,888** |
| Cells with positive visitation links | **403** |
| Sum of all original numeric visitation events | **7,954** |
| Published paper states visitation events | **7,955** |
| Difference (source − manuscript) | **−1** |
| Source separate botanical VOC taxon sheets | **41** |
| Positive compound-species mean-emission entries, across sheets | **955** |
| Exact literal plant name overlap across both original Excel files | **40** |

The original Figshare matrix carries exactly 41×168 integer cells, and all 403 positive links agree with the article; the single-event count discrepancy (7,954 versus published 7,955) must be retained, not silently repaired by adding a visitor. It can be due to author source versioning or a publication transcription difference; **the cause is unresolved**.

**Taxon provenance:** The original network labels `Cistus salvifolius` while the VOC worksheet labels `Cistus salviifolius`. The two are a spelling-reconciliation candidate, not a verified common source taxon under strict literal matching. Do not auto-join based on genus or assumed synonym. Thus **40** original source taxa are exactly linked, **one network name** and **one VOC sheet label** are conservatively unresolved. A source row that is not matched is UNKNOWN scent, not biologically scentless.

**Scientific ceiling:** The original 2018 source workbooks support same-study scent×visitation and source-network structure, but do not themselves supply source-original wavelength-resolved 2017 floral reflectance, spatial UV nectar-guide positive/negative, source meteorological wind, pollen-transfer effectiveness or plant seed fitness. The separate 2017 color study contains published optical results; the original underlying numeric optical source must be authenticated before claiming a new re-computed *optical×VOC×visits* model. Source compound measurements are not independent plant evolutionary replicates, and 955 is NOT the number of plant species. The 2018 authors already formally studied flower colour and scent in visitor networks with phenology, abundance and phylogeny; generic multimodal association is established prior art, not a new novelty claim.

**Exact CI:** Original source [Actions 44079692947](https://github.com/zuizui0223/adaptive-gain/actions/runs/44079692947) SUCCESS independently validates complete 41×168 matrix, 403 links, 7,954 raw events, 41 VOC species sheets and exact 40-species original literal join. Original source provenance [Actions 44079235439](https://github.com/zuizui0223/adaptive-gain/actions/runs/44079235439) SUCCESS verifies source Figshare file metadata and raw SHA.

## 3. Scope-expanded source candidates: no unverified raw data promoted

| Independent candidate geography | Source and original scope | Authenticated during Stage72 |
|---|---|---|
| **Lesvos, Greece** | Kantsa 2017/2018, one natural community, 41 plants, field visits and VOC; original numeric optical colour stored separately | Original 2018 visit and VOC Excel fetched and joined; original 2017 optical data NOT yet recovered |
| **California, USA** | Albor et al. 2022, DOI 10.1111/1365-2435.14142, 39 naturally co-flowering source plants with field measured 340–700nm spectra and pollinator sharing | Original Dryad DOI 10.5061/dryad.2ngf1vhrb dataset metadata and version identified, but **no source XLSX bytes downloaded/analyzed** |
| **Thousand Island Lake, China** | Xie et al. 2025 DOI 10.1016/j.biocon.2025.111322, 41 islands + 16 mainland sites, 98 reported original spectrum-coded plants, 2023–2024 bee visits | Original Dryad DOI 10.5061/dryad.612jm64gq metadata and version identified, **no original ZIP/XLSX bytes downloaded/analyzed**; 57 source sites are NOT 57 geographically independent regions |
| **Japan and New Zealand alpine** | Ishii et al. 2018 DOI 10.1093/aob/mcy188, 106 reported native Japanese and 96 NZ plants, field spectra 300–700nm and order-level bee/fly visitor data, 1 JP and 3 NZ sites | The published manuscript verifies these counts and the author source supp file labels `aob-18614-s02.xlsx`, `aob-18614-s03.xlsx`; but original bytes **NOT authenticated** via PMC OA, Europe PMC supplementary ZIP or public article-bin URLs in this execution; anti-bot HTML200 must NEVER be counted as XLSX |

Note the last study has no observed pollinator visits at Mount Hutt; missing is UNKNOWN. Its 106+96 reported plant species and 5,900 JP / 3,594 NZ visitation events remain **published background**, not numbers re-extracted in this project. Neither the Greek nor the Japanese/NZ paper is a new independent published result.

## 4. Source-access validity correction

A Nature `...MOESM4_ESM.xlsx` URL responded **HTTP 200 with only 3,038 bytes of non-XLSX content**. It is *not original data*. The Stage72 acquisition audit was hardened to reject HTTP200 non-OOXML and count source-original content files by UNIQUE SHA256, not by HTTP success or duplicate publisher/Figshare file aliases. Figshare author original files remain the validated 2 unique XLSX sources. This source-integrity correction is enforced by tests and provenance receipts.

The Ishii source's PMC OA package returned 404, Europe PMC supplementary URL content was not a valid archive, PMC article-bin returned non-XLSX content and Europe PMC article-bin returned HTTP403. **This is an access result, not evidence the published underlying data do not exist.** Stop retrying identical endpoints; use a new genuinely sourced archive or lawful author institution access instead.

## 5. Positive ecological interpretation and actual ceiling

The achieved original measured-data result is **same-community VOC source variation × plant-specific visitor-network counts** for 40 directly name-matched plant species, plus one name collision requiring independent taxon reconciliation. This is useful as a validated calibration/secondary source for a prospective multi-region database. It does NOT establish novel chemical/visual signal sorting or fitness, because prior work already did the core joint analysis, original optical raw data have not yet been independently recovered here, and we have just one source community.

The revised macro research question is **how receiver availability and environmental noise alter which independently measured floral information modality predicts observed interaction channels across independent ecosystems**, while preserving plant source optical organs and receiver sensitivity. This requires multiple truly independent natural populations/regions and proper timing, sampling and detection. Sensory modality is not a scalar "complexity" score. Source mean UV reflectance is distinct from measured spatial nectar guide, and article colour class is not a true bee sensory contrast. WCVP native region is not same-population phenotype provenance. Atmospheric wind speed must not be replaced with source `wind pollination` flags or scent emission units.

**NO global association beta, p-value, phylogenetic conditional null test or mediation SEM is claimed for Stage72.** The valid next step is source-authenticated same-population optical data for additional regions, not an optimization that extracts an apparently positive result from one published community or a blocked dataset.

## 6. Reproduction

- `research/floral_original_field_stage72/audit_original_field_spectra_visits_sources.py`: source article/DOI/Dryad/Figshare availability and original XLSX structure receipts, corrected for HTTP200 fake documents and duplicate original bytes.
- `research/floral_original_field_stage72/replay_original_kantsa2018_network_voc.py`: authentic source Figshare 2018 XLSX workbook and source compound sheet audit.
- `research/floral_original_field_stage72/reconstruct_original_kantsa2018_41x168_VOC_crosswalk.py`: 41×168 original raw numeric matrix, complete 403 links, 7,954 events, and 40 exact species VOC join.
- `research/floral_original_field_stage72/audit_original_ishii2018_japan_nz_alpine.py`: OA original supplementary access route audit, no source-inferred non-existence.
- `.github/workflows/floral-stage72-real-original-field-multimodal.yml`: source-locked all above plus source-free mock guards, and derived source-only artifact, no original third-party binary redistribution.

Stage72 current final run and artifact digest must be read from latest GitHub Actions; earlier successful [source baseline 44080372577](https://github.com/zuizui0223/adaptive-gain/actions/runs/44080372577) verified real 2018 data and limited alpine access.
