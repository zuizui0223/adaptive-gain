# Stage36 — Crall et al. original 70-session wind association reanalysis

**2026-11-15. First original-source numerical reanalysis in floral-route wind line. Existing publicly archived author observations, NOT newly sampled insects, randomized wind exposure, natural flower visitation, pollen transfer or a wind × odor factorial effect.** Stage36 is stacked after Stage35 PR #114. All prior theory, authors' original data and main remain unchanged.

## Source, provenance and correct original units

Crall et al. (2020), *Wind drives temporal variation in pollinator visitation in a fragmented tropical forest*, Biology Letters DOI 10.1098/rsbl.2020.0103. **Original DOI-cited Zenodo 3743898**. The authenticated archive contains raw source-file hashes and an author R script; only aggregate QA and effect summaries are saved in the project. The canonical original collectionMetadata.csv contains:

- **70 sessions at 9 original study sites, on 29 distinct days**;
- **409 total male orchid-bee perfume-bait arrivals**, sum of source recorded session count; **3 zero-count sessions**;
- **67 cineole and 3 methyl-salicylate sessions**. EVERY treatment uses a fragrance lure. There is NO randomized odor OFF comparison;
- raw wind speeds from **0.0206 to 0.73 m/s**, median **0.123 m/s**;
- each original bait sampling opportunity lasted **20 minutes** per original methods.

A different original beedata.csv contains 450 rows, not 450 independent wind replicates. The 409 session totals exactly reconcile with the paper's stated number of bees. The original integratedSpatialWindData.csv has 70 sessions and keep flag 1 in all these original archived records; it was not silently substituted for the same visit response.

## Independent, EXPLORATORY fixed-effect slope, with truthful units

We fitted simple source-audited log(1 + count) OLS contrasts, not the authors' R Poisson log-link mixed model. Main target is a wind speed contrast of **0.1 m/s**.

| Comparison | Original source observation level | Estimate |
|---|---|---:|
| Wind association WITHIN sites, after 9 site fixed intercepts | 70 collection sessions | **+0.21692042** log(1+count) per 0.1 m/s |
| Naively exponentiated interpretation | change in (1 + count), NOT count or fitness | **+24.2245%** per 0.1 m/s |
| Wind association BETWEEN site averages | 9 site means | **−0.15608025** log(1+count) per 0.1 m/s; site Pearson r=−0.43849 |
| Within-site, adjusting original relative turbulence | 70 sessions, two within-site regressors | **+0.23562366** wind slope per 0.1 m/s |
| Leave-one-site-out within-slope range | nine site-exclusion fits | **+0.14507123 to +0.28902624** |

The within-site sign remains positive after including turbulence and in each site deletion, but a strong *population generalization* cannot be asserted on these checks alone. Across-site slope need not have the same sign, and could be confounded by forest cover/site-level population and habitat context.

**Site-cluster bootstrap:** 4,000 resamples of the **nine original sites**, 95% percentile interval for within-site slope per 0.1 m/s is **[−0.02783832, +0.51791358]**. This interval includes ZERO and does not resolve the source site region's spatial dependence. Treat it as a limited-site uncertainty estimate, NOT a confirmatory universal ecological-effect CI.

**Site-stratified wind permutation:** 4,000 permutations of session-level wind values WITHIN sites gave a two-sided exploratory fraction **0.02574356**. This is only meaningful if winds are exchangeable within site conditional on measured design; the source collection dates/time-of-day/weather and season make this premise UNVERIFIED. Not a randomized wind treatment p-value, no causal conclusion.

The original paper's different R lme4 Poisson GLMM with collection site and date random effects, forest cover, wind and relative TKE found within-site wind z=3.45, p=0.0005. Our logged-count site fixed-effect result agrees in DIRECTION but is NOT a reproduced identical coefficient/SE, and its broad site bootstrap interval demonstrates model/unit sensitivity.

## Key ecological result and strict inference ceiling

**New source-verified descriptive evidence**: within one perfume station location, time-to-time higher wind accompanied more visiting male orchid bees, while windier locations had lower mean log(1+count) in this source-level comparison. Separating temporal wind dispersion and spatial differences therefore matters. This is consistent with a scent plume transporting odor more widely, but plume geometry or antenna detection was NOT measured on these 70 original sessions; visitation is to an ARTIFICIAL fragrance collection lure, not natural flower pollination.

No amount of original Crall refitting tests the hypothesis "scent-emitting flowers receive greater wind benefit than scentless flowers": original sessions are **ALL scented**. Nor do male orchid bee perfume visits identify physical flower-landing success, flower-pollen contact or seed set.

The previously constructed Stage34 four-cell wind×scent mathematical proof is SOURCE-FREE; Stage36 is authentic descriptive wind×odor-bait-session association in **one** study, NOT experimental validation of that four-cell interaction.

## Robustness still subject to original design limitation

The analysis code also records optional **site + date categorical fixed-effect** and **cineole-only** sensitivity when their original data identify the comparison. These contrasts are different from the source article's random-date Poisson model. If a source date pattern and site are collinear, the calculation must return a NO_GO rather than force a coefficient; record the actual pipeline receipt to determine whether sensitivity is identifiable.

The original author R script and all original source CSV rows remain external and unredistributed. Only original file hashes, aggregate summaries, model status and uncertainty are retained in project artifacts. The PR stays Draft until dedicated-source workflow and Python 3.10–3.12 whole-repo matrix are verified on its final head.

## Next independent test, not a paper conclusion yet

A within-original-study odor ON/OFF × measured wind study with original flower/patch opportunity denominators and landing successes is needed to identify a true wind×floral scent contrast; pollen deposition or seeds must be directly recorded for reproductive effect. Independent published wind/no-scent cohorts cannot be multiplied as if they were a matched stage chain. The Crall source supplies the scent-bait arrival stage only.
