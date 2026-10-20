# Wind and within-guild taxonomic sorting — 2026-10-20

**Status: completed exploratory original-data analysis.** This extends the same-day PoMS 12-guild wind and 66-pair co-capture screen with a NEW, finer endpoint: whether the taxonomic composition *inside* bees or hoverflies is associated with wind differences among trap stations. Not a direct biotic interaction, manipulation, or adaptive cue-routing test. Main and frozen manuscripts unchanged.

## Original sources and exact population

- UK Pollinator Monitoring Scheme pan traps, 2017–2023, EIDC DOI `10.5285/5841bfae-471b-498c-af89-c30e5140d6c5`.
- Unchanged source SHA256: sample CSV `70f3429e5ed9022d3d7b80fc3f24c589ecc5faff608393bc53febfac49788277`, specimen CSV `2423bc370f388a0dafd05c4bd3a7af7491909311ffe6bf4d6607a3697213dcb9`, flower CSV `53daa167282092b7081190de00e020b4e2635fa5e7d4fc63d3454f7c338951ba`.
- Starting QC: 5,506 unambiguous, undisturbed, 4–8h station observations, 1,139 site-dates and 92 monitoring sites with >=3 stations/date and >=0.5 variation in the *mean of deployment/retrieval Beaufort readings*. This is not calibrated or continuous wind speed in m/s.
- Source `taxon_aggregated` codes were harmonized using unique within-original-source normalized taxon matches only (1,063/1,066 otherwise missing codes recovered; remaining three **not guessed**). Species, species complexes and genus codes may coexist. Catch totals must agree with the original station/guild data. Group-specific taxonomic problems were excluded at the entire date grain.

## Test and complete finite null

For each date require >=6 captured focal guild specimens, >=2 identified aggregated taxon units, and positive catches in BOTH the minimum- and maximum-wind station groups. Measure base-2 Jensen–Shannon divergence (0–1) of the normalized taxonomic catch vectors between wind extremes. Independently enumerate **all 6–120 permutations** of wind labels over that date's 3–5 stations. Preserve every station's multivariate catch vector and condition on the same positive-extreme eligibility for both the observed value and permutation set. Exclude uninformative constant nulls.

Main quantity: observed JSD minus its exact conditional permutation mean, dates equally averaged within each site and then sites equally. Site-cluster descriptive 95% intervals from 4,999 resamplings; right-tailed 4,999 randomization simulations of independently reassigned wind labels within each date. This does NOT establish that wind labels were naturally exchangeable or that wind *caused* a taxonomic change.

| Group | Sites | Eligible dates | Raw observed JSD | Conditional permutation mean | **Excess JSD** | Exploratory site-bootstrap 95% | Conditional right-tail p |
|---|---:|---:|---:|---:|---:|---|---:|
| Hoverflies | 76 | 295 | 0.5827 | 0.5664 | **+0.0164** | [−0.0137, +0.0470] | 0.1488 |
| Bees | 72 | 364 | 0.6131 | 0.5940 | **+0.0191** | [−0.0085, +0.0470] | 0.1418 |

**Neither primary taxon-level wind alignment has a resolved positive effect.** Raw taxonomic JSD near 0.6 is *not* 60% of species replaced; sparse station catches and background heterogeneity already produce high null JSD.

### Declared sensitivity comparisons

| Group / variant | Sites / dates | Excess JSD | Site-bootstrap interval | Conditional p |
|---|---:|---:|---|---:|
| Hoverflies: >=5 specimens at both extremes | 54 / 115 | −0.0240 | [−0.0539,+0.0062] | 0.9292 |
| Bees: >=5 specimens at both extremes | 42 / 89 | −0.0238 | [−0.0553,+0.0069] | 0.9062 |
| Hoverflies: genus/coarse codes | 76 / 295 | +0.0124 | [−0.0211,+0.0465] | 0.2320 |
| Bees: genus/coarse codes | 67 / 345 | +0.0193 | [−0.0110,+0.0489] | 0.1178 |
| Hoverflies: repeated identical station sets | 66 / 215 | +0.0333 | [−0.0038,+0.0699] | 0.0304 |
| Bees: repeated identical station sets | 63 / 269 | +0.0070 | [−0.0249,+0.0363] | 0.3658 |

The single hoverfly repeat-station comparison at p=.0304 is one of eight inspected comparisons and has a site-bootstrap interval spanning zero; do NOT promote it as a robust effect or add post-hoc filters to produce one.

## Scientific synthesis and claim limits

The previous within-guild **seasonal** taxon composition signal was positive after a whole-date null (excess TV approximately 0.055–0.061), whereas this **same-day wind** species-sorting signal is weak and uncertain. Thus seasonal taxonomic composition and wind-linked guild capture reflect distinct ecological estimands. This does not prove wind has no effect in nature.

Previously, a 12-guild wind model gave a moth capture RR=0.593 per Beaufort category but that primary signal was sensitive to exceptional catch records; 66 between-guild residual co-capture wind contrasts yielded ZERO BH q<0.05, and extra nonfocal bycatch did not deliver robust site-held-out FIT predictive improvement. Adding pantrap-specimen taxonomic resolution for bees/hoverflies has not produced a transferable multi-taxon wind-interaction law.

Correlated responses can arise from shared shelter, floral microhabitats, survey time, capture detection, or phenology, **without real interactions** between parasitoid wasps, spiders, bees and hoverflies. Source pan specimens resolve bees and hoverflies; non-focal bycatch guilds lack matching specimen species identities. Testing a *real* hierarchical interaction requires species-specific flower visitors, alternative flowers concurrently available, larval hosts/prey/predator events, near-flower calibrated wind, and preferably a crossed windbreak × resource experiment.

Novelty boundary: the general finding that wind changes flower-visitor community composition is existing literature (Balfour & Ratnieks 2025, *Behavioral Ecology* 36:araf067; DOI `10.1093/beheco/araf067`). Potential novelty would be a verified *indirect* interaction network conditioned on shared wind/resources, not a generic wind correlation.

## Verification

- **7 focused tests passed on fresh run**, with strict within-date no-fake-zero and exact finite-null controls.
- **50 panel permutation distributions independently recomputed with SciPy Jensen–Shannon** rather than production log-ratio implementation: maximum absolute discrepancy `3.33e-16`.
- All eight summary effects independently reaggregated from the saved panel ledger: maximum discrepancy `1.39e-17`.
- Original pan-trap source archive was verified against published exact source member hashes. Portable reproduction companion includes EIDC original ZIP, prior audited source readers, current program, tests, source QC, full panel/exclusion ledger, results and independent audit.
- The exchangeability assumption for wind labels among physical stations is **not** guaranteed: shelter and persistent station geometry may violate it. Site-level resampling does not repair spatial or observation-process bias.
- Original sources used under the UKCEH EIDC Open Government Licence, with UK PoMS/JNCC/funder/volunteer acknowledgement in the accompanying package.

**Status:** species-level analysis has reached a NO-GO for a robust natural wind-driven indirect-interaction claim using these existing observations. Retain as a well-defined boundary and pursue independent measured biotic interaction edges rather than optimizing more post-hoc variants.
