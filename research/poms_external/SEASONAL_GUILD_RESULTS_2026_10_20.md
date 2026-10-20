# Persistent flowers and seasonal visitor guilds — 2026-10-20

**Completed exploratory original-data analysis.** No universal routing, causal preference, latent rewiring or fitness claim. This is a different estimand from the previous predictive-transfer comparison, not extra tuning to make monitoring transfer positive. Frozen manuscripts/main unchanged.

## Main advance

Compare May–June versus July–August within site × year × named flower category. Reuse the checksum-locked original FIT archive and retain performed-survey zero counts. Independently recover the official PoMS pan-trap archive, containing **7,050 trap samples, 24,175 bee/hoverfly occurrence rows and 12,858 flowering-plant occurrence rows**. These are record counts, not independent experiments, species counts or unique insects.

Original pan-trap DOI: `10.5285/5841bfae-471b-498c-af89-c30e5140d6c5`. Its flower observations cover herbaceous plants in bloom within 2m of each station. They are neither an exhaustive 1km-square floral inventory nor the known choice set around each FIT patch. Pan-trap catches are method-selective activity/catch proxies, not unbiased true local insect abundance.

Source-recovery workflow: https://github.com/zuizui0223/adaptive-gain/actions/runs/39372582407
Artifact 12242062482; independently checked artifact SHA256 `8134f38a74e5c283a7cceb393b1cbb2d2b2a25d10c22243942bc6c62524b66e7`.

**The numerical analyses ran locally on recovered originals, not in the download workflow.**

## 1. Same-category paired FIT analysis

The monitoring sample contains **119 paired site-year-flower strata / 56 sites / 358 ten-minute surveys**. Public FIT contains **175 strata / 130 grid cells / 775 surveys**, after removing public records in the full original monitoring grid set. Only May–August, positive recorded floral-unit counts and a consistent floral-unit definition within each stratum are included. Unspecified Other plants are excluded rather than pooled into a fictional species.

A site is a 1km square/grid, NOT an identical flower patch or individual plant. Some named categories pool multiple species/genera. Use the wording **same named flower category in the same square/year**, not identical plant species or individuals.

Strata are averaged equally within sites, then sites equally. Count rates include zero observations. Compositional proportions are undefined when the whole season's total is zero; 12 paired strata in each design are excluded from composition only, not from count rates. Composition uses 55 monitoring sites and 123 public grids.

### Observed count rates, not prediction improvements

| Dataset/group | May–June records /10min | July–August records /10min | Paired difference /10min | Exploratory simultaneous 95% interval across ten guilds |
|---|---:|---:|---:|---:|
| Monitoring: hoverflies | 1.5235 | 2.8407 | +1.3172 | [+0.0791, +2.5553] |
| Public: butterflies/moths | 0.1651 | 0.4126 | +0.2475 | [+0.0084, +0.4866] |

All ten groups and both rate/composition endpoints are retained, along with five predeclared comparison restrictions per dataset (200 numeric rows), not just the two above. Intervals resample sites 4,999 times; simultaneous intervals use a max-standardized-deviation bootstrap within each dataset/endpoint. They do not correct all exploratory comparisons jointly, spatial dependence or observational confounding.

Monitoring hoverfly point estimates remain positive in all declared restrictions, but precision is not uniformly robust. Limiting mean flower-amount change to at most twofold leaves 40 sites and +0.7706/10min, with simultaneous interval [-0.2823, +1.8234]. Requiring >=2 surveys in each season leaves 15 sites and +0.3206/10min, also unresolved. The same-entering-user and same-habitat restrictions retain positive resolved main-family intervals. An entering-user ID does not guarantee the same observer.

**No individual guild's mean compositional-share change has a clearly nonzero ten-coordinate simultaneous interval in either dataset.** An increase in one guild's visit rate and uniform replacement of one guild by another are distinct propositions.

## 2. Independent pan traps and nearby measured flowers

Trap QC retains 6,773 undisturbed, unambiguous station rows with valid 4–8h exposure. A duplicate station/date is represented by two source rows: the entire ambiguous site/date is excluded, not arbitrarily deduplicated. Eleven flower occurrence rows from nine 2017 IDs lack a parent sample; they are explicitly excluded from linkage. Qualified reference dates need >=3 distinct stations. There are 96 distinct eligible pan-trap location-code labels despite metadata referring to up to 95 squares; no speculative merger was made. The FIT linkage uses 93 compatible codes.

**1,800 of 1,861 eligible named-target monitoring FIT surveys** match qualified traps on exactly the same site and calendar date. No nearest-date interpolation is used. This gives 1,471 site-plant-date records. The FIT flower category is positively recorded in a nearby trap plot in **701/1,471 (47.7%)** records. Non-recording does NOT mean floral absence: limited plot coverage, spatial separation, herbaceous-only inventory and conservative taxonomic matching matter.

### Paired two-method comparison

Endpoint: bee share among **bees + hoverflies only**, not all visitors. FIT bees combine bumblebees, honeybees and solitary bees. Daily FIT mean counts per 10min and pan catches per station-hour are computed before equally averaging dates within seasons. The same trap date is never counted as an independent replicate for every FIT row.

Requiring persistent flowers, exact-date matching and nonzero two-group denominators in both methods/seasons leaves **61 strata / 37 sites / 167 FIT surveys**. Fifty-three otherwise paired strata have an undefined zero bee+hoverfly total and are excluded from this conditional composition endpoint; this is a selected subset, not the full 56-site rate population.

| Method in the same paired population | Early bee share | Late bee share | Change in percentage points |
|---|---:|---:|---:|
| FIT visits | 47.18% | 36.30% | -10.87 |
| Pan-trap catches | 63.66% | 51.90% | -11.76 |

Difference of changes: **+0.89 percentage points**, exploratory pointwise 95% site-bootstrap interval **[-15.96, +17.97]**; the simultaneous three-endpoint interval is [-19.23, +21.01]. This is NOT evidence of equality/equivalence, nor an estimate of the fraction of visitation change caused by the background insect community.

The primary pan decline is not precisely resolved under every declared restriction (identical station sets, all five stations, limited flower-amount change, and positive target-flower recording in both seasons). Do not promote its main interval's borderline exclusion of zero into a robust general law.

A **post-result exploratory sitewise correspondence check** gives Pearson r=0.0871, bootstrap interval [-0.2419, +0.4575], and Spearman rho=0.2786. Changes share a sign in 21 sites, have opposite signs in 11, and at least one is zero in five. **Similar grand means do not show that local pan-trap changes explain local flower-visit changes.** Additive share contrasts also do not remove sampling-method selectivity or identify preference.

## 3. Ecological interpretation

The positive descriptive result is group-specific within-season variation in observed visits at persistent flower categories, exemplified by monitoring hoverflies and public butterfly/moth counts. A common directional shift of visitor composition across all groups is not established.

The major data advance is direct linkage of **independently collected insect catches and independently surveyed nearby flowering plants** to flower visits. These quantities can now be kept separate from the visitation response. They have been recovered and linked, but an adequately validated floral-availability-adjusted causal or behavioral mechanism has NOT been estimated. The data do not measure every available floral alternative, individual insect decisions, sensory acquisition sequences, pollination effectiveness or fitness.

## Verification and files

- **15 focused tests passed** in the final local rerun.
- Forty primary effects were independently recomputed directly from original FIT bytes without production grouping helpers.
- All 200 variant estimates were independently reaggregated from paired ledgers. Joined-method effect arithmetic was checked from saved paired rows, not a second full raw trap-join implementation.
- Maximum discrepancy: 1.7763568394002505e-15.
- Reproduction package: `poms_seasonal_composition_20261020.zip`, 1,801,687 bytes, SHA256 `984d981812a881e9d7b397ab31697232e603ad00daf035159b6bbb90c017406a`.
- The package contains both unchanged original archives, executable code, tests, pre-result protocol/addendum, all-group CSV, paired/exclusion ledgers, exact-source hashes, independent checks and full source acknowledgement. Full executable numerical analysis is in the delivered package; this repository update stores the source-recovery workflow and result summary. Repository-wide CI is not claimed green.

## Source attribution

UK Pollinator Monitoring Scheme (2026). Flower-Insect Timed Count data from the UK Pollinator Monitoring Scheme, 2017–2023. NERC EDS Environmental Information Data Centre. DOI `10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618`.

UK Pollinator Monitoring Scheme (2026). Pan trap survey data from the UK Pollinator Monitoring Scheme, 2017–2023. NERC EDS Environmental Information Data Centre. DOI `10.5285/5841bfae-471b-498c-af89-c30e5140d6c5`.

Open Government Licence v3. **Contains data supplied by UK Centre for Ecology & Hydrology.**

The UK Pollinator Monitoring Scheme (UK PoMS) is a partnership funded jointly by the UK Centre for Ecology & Hydrology (UKCEH) and Joint Nature Conservation Committee (JNCC) (through funding from the Department for Environment, Food & Rural Affairs, Scottish Government, Welsh Government and Department of Agriculture, Environment and Rural Affairs for Northern Ireland). UKCEH's contribution is part-funded by the Natural Environment Research Council formerly as part of the UK-SCAPE programme (award NE/R016429/1) and now as part of the NC-UK programme (award NE/Y006208/1) delivering National Capability. Between 2017 and 2021, PoMS was funded by UKCEH and Defra (England), Welsh Government, Scottish Government, DAERA (Northern Ireland), and JNCC. PoMS is indebted to the many volunteers who carry out surveys and contribute data to the scheme.

© UK Centre for Ecology & Hydrology, Bumblebee Conservation Trust, Butterfly Conservation, British Trust for Ornithology, Hymettus, Natural History Museum, University of Reading, University of Leeds, Department for Environment, Food & Rural Affairs, Welsh Government, Scottish Government, Department of Agriculture, Environment and Rural Affairs, Joint Nature Conservation Committee.
