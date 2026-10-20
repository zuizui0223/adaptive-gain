# Seasonal taxonomic structure inside pollinator guilds — 2026-10-20

**Completed exploratory original-data analysis.** This tests captured taxonomic composition within guilds, not another model adjustment to make the preceding FIT coefficient significant. Main and frozen manuscripts unchanged.

## Main result

Both hoverfly and bee catches show greater separation of May–June versus July–August taxonomic composition than a whole-date regrouping reference. All three predeclared sensitivities retain positive excess means. Raw dissimilarity is much larger than the excess: it must NOT be reported as the proportion of species biologically replaced. In a common ten-specimen rarefaction subset, net richness change is not clearly resolved, while calendar-associated compositional structure remains. This is NOT proof of constant richness.

## Source and taxonomy

Original source: UK Pollinator Monitoring Scheme (2026), Pan trap survey data 2017–2023, EIDC DOI `10.5285/5841bfae-471b-498c-af89-c30e5140d6c5`. Sample CSV SHA256 `70f3429e5ed9022d3d7b80fc3f24c589ecc5faff608393bc53febfac49788277`; specimen CSV `2423bc370f388a0dafd05c4bd3a7af7491909311ffe6bf4d6607a3697213dcb9`.

Use the source's `taxon_aggregated`, recommended by its codebook to harmonize sex-dependent identifiability. Units include species, species complexes, genera and a few higher unresolved categories; not all units are species. Of 1,066 initially missing aggregate entries, 1,063 were recovered only through a unique mapping already in the source after removing subgenus/annotation text. Three remaining unresolved specimens were not guessed; affected group/site/dates are excluded. Four bee records missing an order were classified from their explicit hymenopteran group label. One hoverfly sample/occurrence mismatch is in September, outside the analysis window; retained in QC rather than forced to agreement.

## Fixed design

Same intersection of at least three trap stations on EVERY date in a site-year; undisturbed 4–8h exposure; May–August; at least three dates and both periods represented; at least 20 pooled group specimens; positive group catches on every date. This is a sufficiently sampled subset, not all site-years. Ambiguous duplicate station/site/dates are excluded. Original recorder IDs are not copied into derived ledgers.

Primary populations: hoverflies **53 site-years, 35 sites, 2,372 specimens**; bees **109 site-years, 51 sites, 5,299 specimens**. All included site-years have three or four dates. Different group-specific populations mean these are not a formal between-guild effect comparison.

For each date compute taxon catches per summed station-hour, then average date vectors within each period and normalize. Total variation `TV=0.5 sum |p_early-p_late|` ranges 0–1. It describes normalized catch composition, not true abundance, extinction or percentage species replacement.

The null enumerates every allocation of WHOLE dates to the observed number of early dates, retaining within-date covariance, counts, common station identities and exposures. Each panel has 3, 4 or 6 allocations, including the observed allocation. Subtract mean date-null TV from observed TV. This tests alignment with the actual calendar division, not a no-turnover species pool. Large null values include actual date heterogeneity and finite capture noise; subtraction does not causally decompose them.

Years are averaged equally within sites, then sites equally. Intervals use 4,999 whole-site bootstrap draws; exploratory and pointwise, not spatially or globally sensitivity-adjusted.

| Population | Group | Sites | Site-years | Observed TV | Mean date-null TV | Excess TV | 95% site-bootstrap interval |
|---|---|---:|---:|---:|---:|---:|---:|
| Primary | hoverflies | 35 | 53 | 0.8447 | 0.7840 | +0.0607 | [+0.0301,+0.0915] |
| Primary | bees | 51 | 109 | 0.7595 | 0.7042 | +0.0552 | [+0.0321,+0.0784] |
| >=2 dates each period | hoverflies | 24 | 29 | 0.8372 | 0.7811 | +0.0561 | [+0.0209,+0.0922] |
| >=2 dates each period | bees | 40 | 66 | 0.7329 | 0.6601 | +0.0728 | [+0.0453,+0.0993] |
| >=5 specimens every date | hoverflies | 8 | 9 | 0.8011 | 0.7313 | +0.0698 | [+0.0136,+0.1293] |
| >=5 specimens every date | bees | 35 | 52 | 0.7670 | 0.7055 | +0.0615 | [+0.0389,+0.0836] |
| Genus/coarse labels | hoverflies | 35 | 53 | 0.8033 | 0.7347 | +0.0686 | [+0.0379,+0.1011] |
| Genus/coarse labels | bees | 51 | 109 | 0.5075 | 0.4588 | +0.0487 | [+0.0248,+0.0726] |

The stricter per-date hoverfly subset has only eight sites; a positive interval is not universal robustness. Genus/coarse coarsening cannot increase raw TV, and this was checked for every panel. Excess over its separately coarsened null need not decrease. A macro date-randomization diagnostic is at its 1/5,000 simulation resolution in both primary groups; Holm across two groups is 0.0004 each. It assumes temporal exchangeability and the specified within-year randomization dependence, not a causal null.

## Richness and composition in the SAME rarefaction subset

Both observed periods must have >=10 specimens. Expected taxonomic richness under a ten-specimen draw without replacement is computed analytically; it standardizes sample size for richness only, not detection or trap selectivity.

| Group | Sites/site-years | Early units per 10 specimens | Late | Difference [pointwise 95% interval] | Excess TV on same subset [interval] |
|---|---:|---:|---:|---:|---:|
| hoverflies | 18/23 | 5.506 | 5.645 | +0.139 [-0.904,+1.079] | +0.0468 [+0.0116,+0.0838] |
| bees | 41/76 | 5.971 | 6.007 | +0.036 [-0.451,+0.507] | +0.0512 [+0.0309,+0.0713] |

The richness intervals allow biologically meaningful changes. Allowed wording: no clearly resolved net richness change alongside compositional structure. Excluded wording: richness is equivalent or unchanged.

## Biological bridge and limits

Of the previous 47 context-adjusted FIT sites, 17 overlap this hoverfly analysis (13 shared site-years); bee overlap is 27 sites/25 site-years. The taxon populations are not the same 269 FIT observations, and this is not independent replication.

The supported new result is seasonal change in the composition INSIDE broad captured guilds. A coarse hoverfly label can conceal changing taxonomic membership. Thus interpreting an aggregate FIT increase as behavior changing in the SAME species is not licensed. But pan catches do not identify which taxa visited a focal FIT flower, so this does not establish that taxon replacement caused the previous visit-rate increase. Nor does it demonstrate individual preference, floral-availability-adjusted selection, true local abundance, latent rewiring, pollination function, fitness or adaptive information routing.

The same stations and exposure controls do not remove phenology, weather, temporal autocorrelation or trap selectivity. Sparse/sufficiently sampled cohort selection limits generalization. Do not add more restrictions to recover significance; species-resolved flower interactions or independent species-level functional data are needed for the next mechanistic link.

## Verification and saved state

Protocol recorded before contrasts at `c74cc1183aca6b32aab449376734e945f79f7e9f`. Numerical work ran locally during the conversation, NOT in CI.

- 14 focused tests passed in the final rerun.
- 162 primary count/hour tables and exact source eligibility independently reconstructed without production helpers.
- All 480 variant-panel statistic and date-null arrays independently checked with bit-mask enumeration and a separate distance implementation; max statistic error 5.55e-16; max null error 4.44e-16.
- Exact integer-combination rarefaction check: max error 6.74e-13. Count arrays match exactly; exposure error <=1.07e-14 hours.
- All eight group/variant site aggregates independently rechecked. Macro Monte Carlo tails were not rerun with an independent randomization engine; software tests cannot validate spatial/temporal exchangeability.

The delivered `poms_species_turnover_20261020.zip` contains source originals, executable analysis, tests, protocol, independent raw audit, full date/taxon/panel/exclusion ledgers, source acknowledgement and checksums. Repository-wide CI is not claimed green. Main and frozen manuscripts unchanged.

## Source rights

Open Government Licence v3. Contains data supplied by UK Centre for Ecology & Hydrology. Cite the original EIDC release and include the mandatory UK PoMS partnership/funder/volunteer acknowledgement in publications. Full original metadata and acknowledgement are retained in the delivered source package and the preceding context-analysis source acknowledgement.
