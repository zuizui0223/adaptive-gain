# Stage105 — Source-documented floral signal mentions vs point-sampled ERA5-model strong gust

**2026-11-20 JST. Pure exploratory, source-calibrating diagnostic. NOT a preregistered spatial effect or valid wind-selection test.** Draft on Stage104 PR #183; default main unchanged.

## Material scientific question at this step

Do simple correlations between regional strong-gust climate and floral text/size attributes persist when the *probability that botanical sources describe a flower at all* is taken into account?

The whole 125-region strict mainland original source cohort, from which 72 exploration regions were retained after eliminating 16 exploration regions whose polygons touched the fixed 37 mainland holdouts, is independent of cue outcomes. ERA5-model daily maximum gust >15 m/s over climatologically >5°C months for 1991–2020 has been genuinely acquired at source-selected representative points of the original *first 50* mainland regions. Source completeness and 30-year original 10,958 daily calendar were independently audited in Stage95C/97. This is not the original ECMWF CDS hourly 10fg area-integrated regional exposure.

Within those 50 original source representative points, only the **33** geographically contact-free exploration regions are eligible here, spanning **15** broad geographic blocks. The 37 fixed holdout floral response values and the 16 excluded contact regions are NEVER used for correlation or documented by regional output in this diagnostic. The first50 were selected alphabetically by original TDWG code, not probabilistic global sampling; the 33 are neither a random draw nor 33 independent evolutionary transitions.

## Source-authenticated response definitions

Each separate response is obtained from previously original-byte authenticated source-derived receipts with original 367 region keys, but only the original 72 exploration region rows can be materialized:

1. **Near visual source pattern report**: original NHM flower-colour textual descriptions containing documented spot/stripe words per all WCVP accepted native species, and separately per native species for which an original flower-colour field is documented. This is NOT true nectar-guide prevalence; unmentioned patterns are never verified absent.
2. **Chemical source floral fragrance**: original WFO floral-fragrance lexical positive reports per all native species with source-original flora prose, and separately the positive fraction among **positive + explicitly negative original fragrance statements**. Neither is an actual VOC emission rate, field receptor value, or unbiased fragrance prevalence. The two denominators may yield different slopes.
3. **Far-visual observed size source**: original AusTraits 7.0.0 species-level measured-source-labelled flower_diameter regional median, with independent reports of n>=3 and n>=10 source species. It comprises at most 104 globally accepted original measurement species, with repeated taxa across native regions. WFO textual size bounds are NOT silently inserted into a regional median.

For source reporting controls, independently obtain:
- Original NHM flower-colour field coverage = 1 minus missing source flower-colour field proportion, not a biological trait.
- Original WFO full description coverage = source-described native species / original accepted native species.
- Geographic latitude of original TDWG source representative point and annual-climatological 1991–2020 2m temperature at the ERA5-model source grid cell.

## Descriptive diagnostics, not tests of adaptation

Compute rank Spearman correlations between actual observed point-source strong gust and every response. Next calculate diagnostic *partial rank correlations* by residualizing ranked wind/response on ranked source colour-coverage, on ranked colour+WFO description-coverage, and on both reporting fields plus latitude and 2m temperature. These are deliberately **not causal adjustments**, because source reporting itself can depend on taxonomy, climate, documentation effort, archival source and historical region structure.

No naive IID p-values, Bayesian ecological posterior statements or formal multiple comparisons are reported. Region blocks are spatially adjacent, taxonomic source species are reused, and n<=33 or far lower for n>=10 flower-size reporting. Leave-one-broad-geoblock-out raw correlation ranges can be reported for leverage only, not precise spatial-block confidence intervals. Do not make a binary wind-driven odor-versus-visual cue ordering inference.

A correlation that looks strong before, but not after conditioning on original botanical reporting completeness, is evidence of **sensitivity to the source ascertainment process**, NOT proof that the biological effect is absent. Likewise, sign changes between "fragrance positive among all descriptions" and "positive among explicit positive/negative reports" demonstrate denominator instability, not adaptive odor loss.

## Independent source records and locked result

All sources use their immutable artifact SHA from genuinely successful original Actions:
- Stage95C original 25 ERA5-model point daily gust climatologies ZIP SHA256 7c98421306466b589b1f80ec97d4ca32ba58e73ba7807f0c2330a7f082fe6b67
- Stage97 next25 original daily point climatologies SHA256 5e5ee1c325cc85abfb3cfb98a85d9b3faecacd116db9d917eaebdd3a0c453d79
- Stage98B 72 contact-free original mainland source train SHA256 8026b800672cad2afd97e2fe416349cc3aca8f650e78ae8c001dd31de104c8b7
- Stage96 real WFO prose and NHM source three-cue counts SHA256 99aaf623ac3a7f948c5d0cdad9a8ce8668c2131ee07af6fb5d02d81c573c3149
- Stage91 original NHM marking and flower-colour source coverage SHA256 f1197a050d110d1e3626ab01f3c5d49626ac32fd0588d41ce3a162b44d921cdf
- Stage92 original AusTraits7 measured source median regional trait SHA256 01d76457aa8423b7964b5fccdfea597f5c158a805c138fd8597e7efd1733a05f

Actual exploratory slopes and source sensitivity counts must come from the original Actions logs, not from an invented globally complete or confirmed model. Regardless of signs, the scientifically valid next work is to compute the same 1991–2020 daily gust fraction over TRUE mainland regions using CDS daily statistics 1-hourly-derived 10fg at 0.25° gridded resolution, land-mask and area weights, which is independent of the external Open-Meteo one-point proxy and the botanical archive.

Code: research/floral_macro_stage105/source_50point_wind_vs_flora_report_bias.py, tests; workflow floral-stage105-33-source-mainland-wind-cue-docbias.yml.


## Actual original-source screening RESULT — 2026-11-20

Original [Actions #44679591129](https://github.com/zuizui0223/adaptive-gain/actions/runs/44679591129) **SUCCESS**. Seven source-free tests passed and all SIX independently source-gated original derived GitHub Actions ZIP SHA256 digests passed. Derived artifact ID **14603498026**, ZIP SHA256 **0d7cc6609c9ee3b85e24aafbbfd5dec307119506c4a4d5f79a579c21ed6c1534**.

Exactly **33** of 50 original ERA5-model one-point climate source regions lie in the frozen contact-free 72-region exploration scope (15 coarse geo-blocks). Neither the 37 original holdout cue outcomes nor 16 region source-contact exclusions entered the correlations. This is an alphabetic original TDWG-source first50 subsample, NOT 33 spatially or phylogenetically independent ecological experiments.

| Original regional source metric | n source regions | Raw Spearman rho with 30y 15m/s gust exceedance | Partial rank correlation after four source/geography controls |
|---|---:|---:|---:|
| NHM floral pattern word-positive / original native species | 33 | **+0.679** | **+0.082** |
| NHM floral pattern word-positive / source flower-colour-documented species | 33 | +0.637 | +0.146 |
| WFO floral fragrance-positive source mentions / full source descriptions | 33 | **+0.677** | **+0.344** |
| WFO fragrance-positive / explicit positive plus explicit negative source mentions | 29 | **-0.512** | **-0.116** |
| AusTraits original source labelled flower_diameter median (>=3 source species per region) | 30 | -0.199 | -0.325 |
| AusTraits size median with >=10 source species | **9** (4 blocks) | -0.184 | **NOT ESTIMABLE** |

The four partial rank control fields are NHM original flower-colour documentation fraction, WFO full-flora description coverage, latitude and source ERA5 1991-2020 temperature. Source NHM flower-colour *documentation coverage itself* correlated with the point-gust fraction at rho **+0.776**, and source WFO original full-flora descriptions at rho **+0.774**. The apparent original wind-to-floral-pattern text gradient is **highly sensitive to reporting/ascertainment bias**, not a demonstrated adaptive phenotype gradient. The WFO scent association changes SIGN when selecting explicit positive-vs-negative documents instead of positive mentions among all descriptions; the two source variables are not comparable measures of true fragrance prevalence.

The Stage105 estimates are descriptive geographical-source correlations, NO conventional IID p-values, no valid common ecological outcome denominator across the three senses, no independent phylogenetic trait evolution, no externally certified 100-km holdout distance, and no original CDS 0.25-degree area-aggregated 10fg wind. A source species repeatedly occurring in regional native lists is not repeated observed selection. Do not promote this screening to a confirmatory strong-wind-driven bee choice or sensory cue order theory.

Next formal source task: use Copernicus CDS derived ERA5 daily-statistics on single levels, daily max of 10m wind gust since previous post processing from hourly original source (1-hourly), plus daily mean 2m temperature for original mainland region grid cells. Aggregate across mainland land-weighted cell areas for the frozen 1991–2020 baseline, never silently replace original ERA5 post-processing gust with one-point Open-Meteo or mean wind. Official CDS dataset name: derived-era5-single-levels-daily-statistics. Region source documentation/canopy/taxonomy controls remain necessary after that data task.
