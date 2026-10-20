# Seasonal FIT visits with independent floral and catch context — 2026-10-20

**Completed exploratory original-data analysis.** This is a targeted follow-up of the previously observed hoverfly increase, not an independent replication, a universal law or a causal routeability test. Main and frozen manuscripts unchanged.

## Main finding

On the primary complete-case monitoring sample, the July–August minus May–June hoverfly difference remains positive after the specified adjustment for focal floral units, same-date pan-trap catch, recorded flowering-taxon richness, flower-list coverage and temperature: **+1.1731 visits per ten-minute survey**, exploratory pointwise whole-site-refit bootstrap interval **[+0.4038,+2.0620]**. Aggregate bees have **−0.1878 [−1.3488,+0.8905]**, unresolved.

The positive hoverfly mean is not uniformly precise under stricter restrictions. A <=2-fold focal-flower change restriction gives +0.6260 [−0.1671,+1.4583]; complete flower-list coverage gives +0.2552 [−0.3944,+0.8526]. Same trap-station sets retain +1.3874 [+0.5280,+2.2698]. Preserve all results; do not promote the main interval to a general mechanism.

## Population and direct observations

Original monitoring FIT: 3,053 surveys; named-target May–August eligibility: 1,861. Exact-date references with >=3 recorded flowering-plant lists and complete temperature link **1,498 FIT surveys / 89 sites / 767 site-dates**. Requiring early and late observations of the same named flower category/year gives **91 paired strata / 47 sites / 269 ten-minute surveys**. This is a selected subset of the preceding 56-site analysis, not new independent replication.

Within each site/year/flower/period average all recorded FIT counts, including zeros, then average paired strata within sites and sites equally. Primary raw hoverfly means: **1.2342 early vs 2.5456 late**; aggregate bees **1.7011 vs 2.5647** visits/10min. Twenty-two pairs have zero hoverflies in both periods and 33 have zero bees in both; all remain in the rate analysis. No zero-denominator composition exclusion is applied.

## Four fixed models, identical primary population

The outcome is a late-minus-early count-rate difference, not a prediction score or composition share. Weighted linear difference models give each site total weight one. Intercept = fitted seasonal difference at zero measured context change. All reported zero-change points lie inside the corresponding observed joint covariate-change convex hull; this does not establish causal positivity or dense support near zero.

| Model | Hoverfly difference /10min | Pointwise 95% interval | Bee difference /10min | Pointwise 95% interval |
|---|---:|---:|---:|---:|
| M0 paired difference only | +1.3114 | [+0.7134,+1.9646] | +0.8637 | [−0.4109,+2.1466] |
| M1 + focal floral-unit amount | +1.3867 | [+0.7122,+2.1158] | +0.6128 | [−0.7126,+1.9459] |
| M2 + corresponding pan-trap catch | +1.2503 | [+0.5000,+2.0385] | +0.0341 | [−1.0701,+1.2003] |
| M3 + recorded richness, coverage, temperature | +1.1731 | [+0.4038,+2.0620] | −0.1878 | [−1.3488,+0.8905] |

Covariates are changes in survey-weighted mean log1p focal floral units; log1p pan catch per station-hour; log1p mean recorded flowering-taxon richness; proportion of valid stations with a flower list; and mean trap start/end temperature divided by 5 degrees C. No predictor selection or regularization was used. Linear mean-difference modeling is a working descriptive approximation, not a normal-count model.

M0-to-M3 changes are NOT a causal explained fraction. Independently collected pan catches remain method-selective, noisy activity proxies, not true insect abundance. Conditioning on catches or flowers does not guarantee removal of confounding and may introduce bias under other causal structures. Group differences in intervals are not a formal between-guild contrast.

## All fixed restrictions: full M3

| Population | Sites | Strata | FIT surveys | Hoverfly difference /10min | Pointwise 95% interval |
|---|---:|---:|---:|---:|---:|
| Primary, >=3 flower lists/date | 47 | 91 | 269 | +1.1731 | [+0.4038,+2.0620] |
| Focal flower means change <=2-fold | 33 | 48 | 149 | +0.6260 | [−0.1671,+1.4583] |
| Every valid trap station has flower list | 20 | 30 | 92 | +0.2552 | [−0.3944,+0.8526] |
| Same trap-station set over paired dates | 42 | 72 | 208 | +1.3874 | [+0.5280,+2.2698] |

The complete-list population is rebuilt from eligible dates. Its change in recording fraction is exactly zero. The first execution correctly reported a rank-deficient full matrix; a synthetic regression test then verified a fix that omits only this structural-zero nuisance column. Its coefficient is not estimated; it contributes zero on every observation and does not change the fitted-mean model space. No nonzero covariate was removed. Initial logs and red/green regression evidence are retained in the package.

Dropping each primary site in turn leaves the full hoverfly point estimate positive, **+0.9453 to +1.3457**. This addresses single-site inclusion, not population selection or model assumptions.

## Independent resources and source quality

Pan-trap flowers are herbaceous plants in bloom within 2m of stations, not a whole-square inventory or the alternatives available at each FIT patch. Mean richness counts normalized recorded taxon labels only at stations with a list. No list is UNKNOWN, not zero richness. Primary dates require >=3 recorded lists; list-coverage fraction is an explicit covariate. Taxon labels can include species, genera and aggregates. Counts in different floral units are never added into a fictional common resource currency. This is adjustment for **recorded richness/coverage**, not full floral abundance, identity, nectar quality or availability.

Trap QC: undisturbed, 4–8h station exposures, 3–5 distinct stations, exact site/calendar-date match, no nearest-date interpolation. The whole ambiguous duplicate-station site/date is excluded. Eleven orphan flower occurrences are excluded. Missing temperature excludes a date before pairing. Qualified reference: 1,077 site-dates / 92 location-code labels; 319 dates lacked three flower lists and two lacked complete temperatures.

## Verification and saved state

Protocol recorded before coefficient estimation at **3358f6bc56476db7186be6d0b4dddeb84bf5d141**, with local equivalent plus a transparent post-first-run structural-zero implementation ruling.

- **14 focused tests passed.**
- All **32 model comparisons** completed, with **1,999 whole-site bootstrap full refits per comparison: 63,968 requested fits, zero failures**.
- Primary raw FIT/trap/flower join and all 91 pairs independently reconstructed without production join/grouping helpers; maximum paired-field error 8.88e-16.
- All 32 coefficient vectors independently checked using statsmodels WLS and separately assembled site weights; maximum coefficient discrepancy 7.11e-15.
- Ninety-nine independently resampled full-row bootstrap fits agree with the production per-site-moment calculation to 3.24e-14.
- Verified local runtime: Python 3.13.5, NumPy 2.3.5, pandas 2.2.3, SciPy 1.17.0, statsmodels 0.14.6.
- Original monitoring FIT CSV SHA256: 29d3deb757c053774c26ece0a7683081a4b4fe81d9497877fe1179f232182e52.
- Pan sample CSV: 70f3429e5ed9022d3d7b80fc3f24c589ecc5faff608393bc53febfac49788277; insect CSV: 2423bc370f388a0dafd05c4bd3a7af7491909311ffe6bf4d6607a3697213dcb9; flower CSV: 53daa167282092b7081190de00e020b4e2635fa5e7d4fc63d3454f7c338951ba.

Numerical fits ran locally in the conversation. Repository-wide CI is not claimed green. The delivered reproduction package contains executable code, tests, protocol, both unchanged original archives, source acknowledgement, exact source/output hashes, all comparisons, hashed-site pair/exclusion ledgers, and independent audit. This repository stores protocol and results; no original recorder IDs are copied into derived ledgers.

## Claim ceiling

The primary data support a context-adjusted residual seasonal association in hoverfly visits at persistent named flower categories under the specified descriptive model. The stricter flower-amount and list-completeness restrictions leave its magnitude uncertain. This does not establish active preference switching, unchanged resource availability, replacement of visitor guilds, pollination effectiveness, fitness, latent rewiring or adaptive cue routing. Intervals are exploratory, pointwise and not spatially or globally multiplicity-adjusted; this is a targeted follow-up of known outcomes. Do not add variants just to recover a positive result.

## Original sources and acknowledgement

UK Pollinator Monitoring Scheme (2026). Flower-Insect Timed Count data 2017–2023, EIDC DOI 10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618. Pan trap survey data 2017–2023, EIDC DOI 10.5285/5841bfae-471b-498c-af89-c30e5140d6c5.

Open Government Licence v3. **Contains data supplied by UK Centre for Ecology & Hydrology.**

The UK Pollinator Monitoring Scheme (UK PoMS) is a partnership funded jointly by the UK Centre for Ecology & Hydrology (UKCEH) and Joint Nature Conservation Committee (JNCC) (through funding from the Department for Environment, Food & Rural Affairs, Scottish Government, Welsh Government and Department of Agriculture, Environment and Rural Affairs for Northern Ireland). UKCEH's contribution is part-funded by the Natural Environment Research Council formerly as part of the UK-SCAPE programme (award NE/R016429/1) and now as part of the NC-UK programme (award NE/Y006208/1) delivering National Capability. Between 2017 and 2021, PoMS was funded by UKCEH and Defra (England), Welsh Government, Scottish Government, DAERA (Northern Ireland), and JNCC. PoMS is indebted to the many volunteers who carry out surveys and contribute data to the scheme.

Full original copyright notices and metadata are retained in the source archives and SOURCE_ACKNOWLEDGEMENT.md accompanying the delivered package.