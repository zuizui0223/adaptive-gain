# Wind × independent flowering-plant richness × hoverfly larval feeding: no-go, 2026-10-20

**Status: completed original-data exploratory extension. Not a causal indirect-species interaction. Main and V5/V6 frozen manuscripts unchanged.**

## Outcome and predeclared stopping rule

The locked primary gate was >=30 independent sites, >=100 site-dates and **>=1,000 trap station records** in the cohort with within-date recorded-flowering-richness variation. The cohort has **51 sites / 128 site-dates / 622 stations** (777 captured zoophagous-larva adults and 952 other-larva adults). The >=1,000 gate fails: **PRIMARY NO-GO**, no confirmatory plant-mediated claim. Parent larval-wind analysis (86 sites / 413 days / 2,013 stations) is preserved as a distinct original observational result.

At least one independently recorded flowering herb taxon is required at **every station on each included date**. Initial full-list candidate 52 sites / 135 dates / 655 stations; 7 dates were excluded for no within-date richness contrast. These lists are 2-m near-pantrap vegetation observations, not complete available-flower/prey inventories. Median observed recorded richness is 2, range 1–13.

## Transparent below-gate descriptive model (never promoted)

Conditional two-guild site-day Poisson capture allocation (hours offset, date×larval group total conditioned, physical station/vegetation/sun/temp nuisance), testing **wind × log1p(recorded flowering taxa) × larval feeding class** after all lower-order contrasts. Wind is ordinal deployment/retrieval Beaufort mean; richness contrasts are centered within date and expressed in one pooled within-date SD (0.344855 log1p units).

| Diagnostic | sites / dates / stations | relative wind-slope ratio per +1 SD recorded richness | exploratory site-cluster 95% CI |
|---|---|---:|---|
| Full source subset (below 1,000 gate) | 51 / 128 / 622 | **1.0348** | 0.7298–1.4672 |
| Taxon matching >=95% | 46 / 94 / 458 | 1.1499 | 0.7458–1.7728 |
| Exclude extreme capture dates | 50 / 122 / 596 | 1.1309 | 0.7526–1.6995 |
| Exclude most abundant matched genus Eristalis | 48 / 109 / 529 | 1.1540 | 0.7436–1.7908 |

The registered genus sensitivity was corrected **before outcomes** from Episyrphus to source-abundance leading **Eristalis** (1,797 matched captures versus 1,372 Episyrphus). Never reinterpret wide intervals as proof of absence. Independent `statsmodels.ConditionalPoisson` estimated beta=**0.0342172**, versus production beta=**0.0341991**, absolute gap **1.82e-5**.

### Out-of-site prediction, secondary diagnostic

Use full-site-held-out fivefold conditional log-likelihood per captured specimen to compare with/without the 3-way term. **All five held-out folds worsened**: site-equal mean difference full-minus-baseline **−0.00148017** log units per captured specimen, 19/51 sites positive (37.25%). These fixed folds are not a new independent dataset and cannot override the predeclared primary gate.

## What the other-species hierarchy can and cannot say

Independent EuPollTrait annotations describe **13 hoverfly species with named larval host ants (Lasius/Formica/Myrmica), bumblebees (Bombus), or social wasps (Vespula/Vespa)**. Only **three host-annotated species** occur with exact names among quality-kept PoMS adult capture records: `Volucella bombylans` 49, `V. inanis` 2, `V. pellucens` 3, **54 captures total**. The labels describe potential host/nest natural history, NOT observed same-place host encounters, actual larval prey, or new trophic edges; this dataset cannot fit a host-specific wind mediation model.

The earlier pantrap larval-trait wind RR~1.62 remains an observed adult **lineage/feeding-class capture association**. The plant-richness moderator is **not supported or adequately powered** here, and larval diet is still near-collinear with genus (one mixed genus of 41). Do not claim that flowering plants, host ants/wasps, or aphids mediate wind-driven flower visitation.

## Reproducibility and scope

- Original UK PoMS 2017–2023 pantrap data: EIDC DOI `10.5285/5841bfae-471b-498c-af89-c30e5140d6c5`. Use original member SHA256 as locked in prior `crosslife_analysis.py`. EIDC Open Government Licence; UKCEH, PoMS, JNCC, funder/volunteer acknowledgement mandatory.
- Original independent hoverfly larval trait data: EuPollTrait (Miličić et al. 2026), DOI `10.5281/zenodo.18032357`; exact original ZIP MD5 `7a50cc03e2c5a287e663dc5d029f8026` was verified and author dataset is not relicensed by us.
- Local companion: `flower_context_moderation.py`, `cv_flower_context.py`, `test_flower_context_moderation.py`, `test_flower_context_cv.py`, results JSON, hashed 51-site conditional held-out scores, independent direct-statistics check and pre-outcome analysis contract. Complete portable overlay in linked conversation ZIP.
- **24 focused tests passed fresh**, combining seven new tests with seventeen prior source/model tests; original source checks are re-executed in analytic scripts. All 10 fivefold predictive fits converged; maximum gradient 1.72e-6. Reaggregated site-score identity max arithmetic error 3.91e-16. No repository-wide CI claim.

**Next identifying step**: synchronized species-level hoverfly flower visits, larval host or aphid density, complete choice/exposure plants and local calibrated flower-height wind, ideally random windbreak placement. Until then this remains *cross-life trait-correlated capture* with an ecological identification ceiling.
