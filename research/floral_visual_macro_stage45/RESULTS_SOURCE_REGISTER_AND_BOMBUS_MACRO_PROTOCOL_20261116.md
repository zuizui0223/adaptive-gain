# Stage45 — source-verified floral visual-trait atlas and geographic Bombus hypothesis

**2026-11-16 JST. This is a new visual-signal macro research programme, not the wind biomechanics result.** Original source files and their authentication are in scripts and dedicated GitHub Actions receipts. No floral visual-information by Bombus geographic coefficient has been fitted.

## A. Measured UV trait seed (Tunes et al. 2021; doi:10.3389/fpls.2021.618028)
Source PDF Data Sheet 2, SHA256 d11b41a36d85d1b70c8d3d47c04f3e03e7d8f5f58ebaaa331a737e56ed4c2820. The authentic original table contains 80 taxon rows: A uniform UV-absorbing 47; R uniform UV-reflecting 7; BE bullseye 7; CM corolla markings 4; CR contrasting reproductive structures 15. **26/80 measured UV-patterned, 54 uniform**. The article prose R6/CM5 is inconsistent with the source PDF Table S2 R7/CM4; never recode source individuals to match the article summary. 73 source rows look like binomial names and seven are genus/uncertain. Visible non-UV patterns marked present in 51 source rows. Source pollinator guild labels are literature/syndrome information, NOT direct Bombus visits. The 80 original taxa are geographically concentrated in the Brazilian savanna, not a representative global flora. Authentic source CI 43834312835 SUCCESS.

## B. Large floristic source (NHM 2026; doi:10.5519/p3dm31kc)
Original official NaturalHistoryMuseum/plant-traits commit 4843c22bb2fc91018d9828dcddebf067c83b1097, original Git blob SHA1 e1cfd2d5c518c2061ec91d1a9e8b64fc7ca69389, source file 17,279,412 bytes, SHA256 7548836b788ad5c9a3a6eaf382c05646ac2b0be73d889092228a3fba9dea5e0b. The NHM portal direct CSV was 403 and CKAN deep search window exceeded 10,000 (409); the official immutable Git file was verified instead.

59,369 source taxon rows have: 32,183 with at least one flower/petal/corolla/labellum colour entry; 1,887 with shape/symmetry/architecture/lipped corolla; 1,398 with both; 353 with text matching potential flower marking terms. **None of those 353 are verified UV nectar-guide species**: they are original colour-description review candidates. No dedicated guide status exists in the large trait source. Do not recode missing visual signals as absent. Full source CI 43835564375 SUCCESS; derived registry artifact 14209573962, SHA256 3b01e535c6936cccd50a4d857a1536d8e1f4ac05f19782d2e03873c7d94c86d1.

## C. Taxonomic interoperability
Only 21/80 measured UV taxa exactly match an NHM binomial text label; 52 source taxa do not match and seven have no unambiguous binomial. This is not proof of taxonomic nonidentity; independent WFO/GBIF synonym processing is necessary. Dedicated source join CI 43835216727 SUCCESS.

GBIF accepted species-level matching confirms 71/80 original UV taxon rows at exact high confidence, with positive coordinate-qualified GBIF occurrence index counts for all 71. Two additional candidates lack exact high-confidence identification and seven names are unresolved. Observations are NOT predicted plant ranges. Dedicated GBIF CI 43835572885 SUCCESS; artifact 14209319688, SHA256 0dd14b3264938a121ac287a6b0592aaaf29f68d9bb52d67c414414c67b6e641a.

The GBIF Bombus genus taxon key is 1340278; index count of 4,749,717 coordinate-qualified occurrences is NOT a count of independent Bombus individuals, species richness, native populations or predicted suitability.

## D. Falsifiable ecological macro hypothesis

Main question: Is the global or regional occurrence of physically measured floral visual spatial guides associated with the predicted availability of pollinator guilds able to detect/use those signals, **after** climatic, spatial, lineage and observation-process controls?

This differs from the trivial correlation between visually conspicuous flower colours and bee occurrence density. Two distinct optical outcomes are required: (i) visible colour display/contrast, and (ii) flower-part-specific UV/spectral guide architecture. Static guide position information and flower age/reward information are separate, and plant reproductive success is not deducible from either.

Freeze model grain as plant species × equal-area grid cell × documented time/source, with independent pollinator species × same grid cell. Bombus predictor should be species-level *modelled environmental suitability/native-range-restricted predicted richness with uncertainty*, NOT raw GBIF observation counts. Include alternative bees, moths, flies, butterflies and vertebrate pollinators where measurable; Bombus is not a globally sufficient proxy.

Essential controls: climate (temperature, moisture, light), habitat, plant phylogeny, guild native/introduced status, plant and pollinator sampling effort, region/biogeographic source pool and overlapping time. Analyse regional heterogeneity and compare spatial-block/region-held-out validation, not one shuffled pooled p-value. Missing plant or Bombus records must never be treated as confirmed biological absence.

Source candidates for actual modeled pollinator distribution:
- Global bee bioregion models and species SDM data, 3,370 modeled bee species: Zenodo 10.5281/zenodo.20525239 (2026 PNAS). Inspect file manifest, species resolution, grid, period, quality before reusing.
- European Bombus species ecological niche models and source observations, De Tandt et al. 2026: Zenodo 10.5281/zenodo.21620753, GitHub BastienDT/counterclim_bombus. These can be external validation but do not share geography with Brazilian UV seed.
- Independent comparative visual spectra: FReD (Arnold et al. 2010) and additional regional UV-petal contrast collections. A single whole-flower reflectance spectrum is NOT proof of a nectar guide.

## Publication/inference ceiling
The **positive outcome established at Stage45 is source acquisition and coverage** (80 measured UV taxa, 59,369 original NHM taxon rows, 71 GBIF-mapped UV taxa), NOT a biological UV–Bombus association. Before running a global model we must expand measured UV guide categories beyond the Brazilian savanna and obtain actual native/species-specific predicted guild exposure on matching grid cells. No new adaptations, visitation, pollen, seed, or plant fitness effects are claimed.

Repository Stage45 is intentionally independent from Stages37–44 wind work. Keep it Draft, audit source licenses, and do not modify main until cross-source provenance is accepted.
