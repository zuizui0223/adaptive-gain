# Stage76 | Original continental flower-colour × bee network: WCVP native-location filtering and study confounding

**Status (2026-11-18 JST):** Verified actual source [Stage76 WCVP macro Actions 44193987591](https://github.com/zuizui0223/adaptive-gain/actions/runs/44193987591) **SUCCESS**, source output artifact **14377103968** SHA256 `a67b0a5a27f6504f8a94d6a350589e4708025388dc64e0edff03d3622fddc552`. Draft stacked on Stage75 PR #154. This is a continued **macroecological** project, not another single-species mechanistic case study. `main` unmodified.

## Genuine original public-source chain

1. Original [Natural History Museum botanical TEXT](https://github.com/NaturalHistoryMuseum/plant-traits) combined 59,369 plant taxon labels, 31,773 with flower colour prose, source Git blob pinned by Stage68 (DO NOT photo-impute traits); 233 species in Stage75 independently reported a lexically single colour-family among 963 exactly source-matched accepted EuPPollNet species.
2. Original author-corrected [EuPPollNet v1.3.0](https://github.com/joseblanuza/EuPPollNet/tree/v1.3.0), original 623,476 observed plant-visitor records, 1,864 study×network×year units, 54 original studies, 23 countries. Derived source plant×network table has **18,798 units and 1,408 source accepted species names**; original source `Stage75` hue networks selected **before** opening bee guild recording.
3. Original official Kew [WCVP distribution ZIP](https://sftp.kew.org/pub/data-repositories/WCVP/wcvp.zip), SHA256 `d32ea2b3a85e489b14e83bcc9eae7274532e1d113753f7be290d4b2dfde573fa`: strict `taxon_rank=species`, `taxon_status=Accepted`, unambiguous accepted species name → original source TDWG-L3 `area_code_l3` with source binary introduced=0, extinct=0 and doubtful=0. Ambiguous/missing flags are UNKNOWN.
4. Original TDWG WGSRPD [Level3 geospatial polygons](https://github.com/tdwg/wgsrpd/blob/master/geojson/level3.geojson), Git blob SHA1 `91104e5159e31f88154833a51d3b0d1c9271083f`. Primary source retains **350 valid polygons**, excludes **19 historically invalid**; secondary sensitivity uses `shapely.make_valid` for the 19, separately labelled. No nearest-country lookup or arbitrary site location is substituted. Source field networks with multiple coordinates or near a 0.02° source polygon boundary are conservatively excluded.
5. Corrected original source visitor guilds from recognized species-ranked bees, Bombus vs other bee families, already reconstructed and independently source SHA-verified by Stages69, 71 and 75. These are **recorded guilds, not modelled receiver environmental suitability**. An unrecorded bee does not prove absence.

**Do NOT conflate** regional-native compatibility with proof an observed individual was native, or DoPI/GloBI/GBIF remote geographic co-occurrence with field visitation.

## Macro sample-size verification from real source

| Source universe | Original counts |
|---|---:|
| Real source plant names with accepted taxon in corrected field visits | **1,408** |
| Strict WCVP accepted species name matches | **1,367/1,408** |
| Exact original NHM species name overlaps | **963** |
| Plant species with some original NHM colour text | **809** |
| Original study×network×year units | **1,864** |
| Source plant×network/year units | **18,798** |
| Plant×network units regionally native-compatible and safely inside original valid polygons | **11,578** |
| Same under *historically invalid geometry repair* sensitivity | **15,024** |

The 11,578/15,024 are **plant×network rows**, NOT distinct plant species, pollen transfer services or newly measured traits. The original geometry-only primary leaves **5,333** source plant×network units with unresolved exact TDWG L3; repaired geometry reduces this to **1,029**, without proving field accuracy. Original primary further has **749** WCVP explicit introduced-area statuses, **284** WCVP source-area not recorded (UNKNOWN), **426** species not exact accepted, and **428** near the old polygon boundary. These categories are mutually exclusive at that source plant×network level. The repaired geographic sensitivity changes source study inclusion, not plant fitness.

## Direct source native-specific flower hue × actual bee visitation macro result

We preserve **Stage75's prespecified original hue comparison** before inspecting recorded guild composition. Every source species must be explicitly described as one hue family in author botanical text. Multiple reported hues and absent visual colour text are UNKNOWN/excluded for this narrow contrast; text `spot` positive is NOT direct spatial UV nectar guide, and absence of the word does NOT mean motif absent. There is no source field phenotype measurement of the same individual.

| Original source cohort | Networks with both documented hue states before inspecting bee records | Strict bee informative networks | Distinct informative study IDs | Local null-score / information ratio (NOT fitted logit beta) | Descriptive 2,000-study-bootstrap interval |
|---|---:|---:|---:|---:|---|
| Baseline Stage75 yellow vs white | 345 | 84 | 21 | +0.0763 | [−0.731, +1.316] |
| **Stage76 primary WCVP compatible** yellow vs white | **199** | **38** | **13** | **+0.1506** | **[−1.263, +1.157]** |
| Source repaired TDWG geometry WCVP compatible yellow vs white | **286** | **65** | **18** | **+0.7278** | **[−0.406, +1.679]** |
| Baseline Stage75 yellow vs purple | 65 | 25 | 13 | −1.3703 | [−3.245, −0.341] |
| **Stage76 primary WCVP compatible** yellow vs purple | **33** | **11** | **7** | **−1.2010** | **[−4.530, +0.644]** |
| Source repaired TDWG geometry WCVP compatible yellow vs purple | **47** | **19** | **9** | **−1.3927** | **[−3.797, −0.170]** |

The null-score/information ratio is a **first-order linear approximation at a zero coefficient** in a network-stratified binomial score for source visit composition. **It is NOT a fitted maximum-likelihood logit coefficient, source validated odds ratio, confirmatory CI or p-value**. The bootstrap is a non-phylogenetic descriptive study-block resampling interval. Source study populations and species identity are repeated. Colour is taxon-constant, so plant species fixed effects would absorb source colour slopes.

### Evidence and falsification

- Yellow vs white has no robust source-supported positive or negative relationship. Conservative source native vs repaired geographic sensitivity changes the size and score of included studies. Its descriptive intervals all include zero.
- Yellow vs purple remains negative in point direction after original native-source area matching. **But only 11 networks / 7 original independent study IDs** contain useful strict bee records in the conservatively verified native comparison. The primary study-block bootstrap range **crosses zero**. Do **not** claim a stable evolutionary purple preference or pollinator-driven floral adaptation. The repaired-geometry sensitivity is negative but depends on repair admitting additional original study locations and still lacks validated phylogenetic independence.
- WCVP is site-*region* compatible, not evidence each flowering plant was an original native individual. Missing area is an unresolved provenance class, not introduced or zero flora.
- Seven European bioregions were present at the full original source scope, but the two source comparative hue frames have far less independently replicated coverage. Original wind/UV intensity/site fragrance and ecological receiver availability probability are not in the original EuPPollNet site data.
- The previously archived *Bombus* global hypervolume source lock in `zuizui0223/island` recorded 169 discovered/142 scored species, 8,265 historical islands with an original artifact that **expired 2026-10-10**. Its source data are **NOT silently imported** into Stage76. A fresh, hash-pinned receiver opportunity surface that distinguishes suitable vs observed vs true absence remains necessary for the future planned climate-confounding SEM.

## Additional global-origin evidence in the user's existing island/fd research

The independent original, verified [island source Actions 44102655957](https://github.com/zuizui0223/island/actions/runs/44102655957) (different study branch and purpose) aligns **4,505 GIFT botanical island flora rosters** with original public **DoPI v2 676,900 European positive visitor records**, from **518 source publications** and **3,203 accepted botanical island-roster plant names overlapping DoPI**. This does NOT measure 4,505 independent island-local pollinator networks: DoPI is an external European visitor source. Source original colour, shape, nectar-guide/morphological motifs across 27 floral templates have 107 positive within-publication documented guild comparisons but do not establish true absent guilds. Its 76 equal-genus descriptive panels, 11 genus-conditioned source coaccess panels and **zero** genus-fixed effort-conditioned guild richness panels are useful **positive-only controls**, not claims of global adaptive guild replacement. Dataset and study independence against EuPPollNet/GloBI must be checked before any joint source inference.

**Stage76B** uses the original DoPI 2026 file as an independently auditable cross-provider *positive recorded guild* evidence panel for the 233 text-colour species; it is source version/byte pinned, distinguishes pollination-evidence grades 1/2/3 from nonpollinating 4, and will never reinterpret absence of a reported guild as a biological zero. This source is primarily European and not an actual site-native island guild survey.

## Actual executed work

- `research/floral_macro_stage76/official_native_WCVP_Stage75_macro_field_guilds.py`: reuse original source-authenticated Kew native distribution, historical TDWG exact coordinates and corrected EuPPollNet real visiting bees; source data site-state and pre-outcome WCVP native hue cohort; observation-only composition score.
- `research/floral_macro_stage76/test_official_native_WCVP_Stage75_macro_field_guilds.py`: nine adversarial mock-only tests for WCVP missingness, ambiguous site, border exclusion, outcome-blind cohort, introduced-area exclusion, guild identity.
- `research/floral_macro_stage76/original_DoPI2026_external_study_hue_guild_macro.py` and corresponding tests: original positive DoPI study, original pollination evidence tiers, per-study documented guild portfolios and same-genus panel; **no raw source species/study DOI identifiers uploaded**, no p-value.
- `.github/workflows/floral-stage76-original-WCVP-native-macro.yml`: full archived 59k/963 source pipeline, official WCVP zip and original TDWG polygons, all source SHA checks, independently verified source result artifact.
- `.github/workflows/floral-stage76b-DOPI-original-external-source-macro.yml`: external source-only DoPI v2 Zenodo source checksum 384,896,230 bytes, 676,900 source-positive records, original 233 NHM positive lexical hues, source publication and pollination-evidence grade scopes.

**Verified WCVP CI:** [44193987591](https://github.com/zuizui0223/adaptive-gain/actions/runs/44193987591) SUCCESS; artifact ID **14377103968**, SHA256 `a67b0a5a27f6504f8a94d6a350589e4708025388dc64e0edff03d3622fddc552`.

**Scientific next goal:** obtain a CURRENT original source-locked Bombus niche/availability surface (distinct from original GBIF field detections and no-effort nondetection), align to genuine plant native distribution locations and climate/wind/scent source covariates. Test prospective interaction of receiver accessibility × source floral information with original study/context/covariate controls and independent clade support. The existing source output is a *continental macro observational constraint*, not causal global flower-colour adaptation.
