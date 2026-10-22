# Wind-dependent bee versus enemy-role visitor activity — original SA026 direct test

**2026-10-22; preregistered exploratory comparison; NO-GO for a supported wind-mediated biotic interaction.** This is a new independent endpoint from the same Andrews SA026 observations, not independent biological replication of the prior temporal-order result. Main and frozen V5/V6 are unchanged.

## Source and fixed sampling

H.J. Andrews Experimental Forest LTER, Seo et al. 2022 SA026, DOI `10.6073/pasta/eec55cbc3dbfc56428629773737ab3e5`, verified package `knb-lter-and.5216.8`. Source watch CSV **74,942 rows**, SHA1 `fcd28cf0c9623fbfbc5619136334265a65f13dc4`, MD5 `7be658632075908343c5ab72c4de9c50`; source flowering list **23,642 rows**, SHA1 `c93b5496154245b9e94dc3362297ed354db3ebb6`. Original years present 2011–2018 and 2021, no 2019–2020 sampling. Rows are not independent insects.

**1,296 eligible 15-minute watches / 19,440 verified one-minute cells / 17 meadows**, after requiring all 15 real minute records, one ST (still) or BR (breezy) wind label per watch, compatible positive/no-interaction status and strictly positive quantity when status is positive; 924 ST and 372 BR. The locked observational role definitions are **bee-visitor** and **natural-history bee-enemy-associated** pollinator-visitor role strings, NOT observed parasitism/predation or interactions between identified individuals. Count a visitor role ONCE per observed minute, even when source has several positive rows.

The preregistered paired cohort compares ST and BR within the SAME **meadow × calendar date**: **13 meadows, 92 paired dates, 578 watches** (351 ST; 227 BR). Within each meadow-day average every eligible ST watch and every BR watch independently, then calculate BR minus ST for the fraction of 15 minutes containing a confirmed role visit, then average equally across the 92 meadow-days. The two role presences can coexist within one minute. This is an observation frequency, not true abundance or detection-corrected behavior.

## Main registered endpoints

| Endpoint | Day-equal ST | Day-equal BR | BR−ST in percentage points | Full-watch label permutation p, 9,999 | Holm q across 3 | Site-cluster exploratory 95% CI, pp |
|---|---:|---:|---:|---:|---:|---|
| **Primary: (enemy BR−ST) − (bee BR−ST)** | — | — | **+4.611** | **0.0820** | **0.1884** | [+0.160,+10.371] |
| Bee visitor role | 0.304739 | 0.265924 | **−3.882** | 0.0628 | 0.1884 | [−7.721,−0.419] |
| Enemy-associated visitor role | 0.030893 | 0.038191 | **+0.730** | 0.6557 | 0.6557 | [−1.741,+4.202] |

**Interpretation:** There is a descriptive tendency for bee visits to occupy fewer observed minutes under BR, with a bigger relative gap versus enemy-labeled visitor activity. However, **the registered whole-watch within-day permutation / Holm test fails to resolve a consistent difference**. The apparent primary site-bootstrap interval excludes zero but tests a distinct resampling uncertainty and does NOT override the randomization test; exchangeability of naturally observed wind is itself questionable.

Main comparison uses **only recorded minute attendance**; no missing minute or unobserved plant is coded zero. The meadow-equal primary difference is **+12.19 pp** versus main date-equal +4.61 pp, due to uneven meadow/day representation. Leave-one-meadow-out date-equal effects are +2.81 to +5.76 pp; positive direction alone is not sufficient evidence.

## Two unchanged sensitivities

| Frozen population | Meadow / meadow-date / watch | Primary difference, pp | Two-sided permutation p | Holm q |
|---|---:|---:|---:|---:|
| Main | 13 / 92 / 578 | +4.611 | 0.0820 | 0.1884 |
| Same plot/date/watch separately recorded flower survey | **13 / 57 / 313** | **+5.353** | **0.1578** | 0.3156 |
| Years 2014–2016 only | **12 / 73 / 511** | **+2.105** | **0.2898** | 0.7704 |

Flower-survey presence is evidence a flora survey record exists, not exhaustive bloom alternatives; one linked watch has no positive `FLW` status. Neither sensitivity is significant by the predeclared three-family Holm rule. The original lagged enemy-to-bee arrival-order test (same SA026) also did not support wind moderation; it is distinct endpoint but NOT an independent dataset.

## Independently reproduced and methodological caveats

1. Raw source and flower SHA1 values were independently checked. A separate raw-row pandas reconstruction, **without importing the production QC/collapse pipeline**, found exactly 1,296 eligible watches, 92/57/73 paired day cohorts and reproduced every one of the 9 wind-role effect estimates to floating point precision. Check primary original p and effect against report. 
2. An entirely independent null implementation enumerated **all finite assignments of watch-level wind labels within each day** (2–210 assignments per paired day) and then sampled that exact conditional reference with a different random seed: primary p **0.0827**, same-plot flower p **0.1673**, 2014–2016 p **0.3021** (vs 0.0820, 0.1578, 0.2898 in production; discrepancies within expected Monte Carlo error). A separate 16-test suite (9 earlier lag-QC tests + 7 direct-role tests) passed with zero failures.
3. The primary 92 meadow-day watch contrasts have only **13 independent meadow units**. Of 86 paired days with usable start times, BR watches started on average **0.211 hours (12.7 minutes) later** than ST; of 69 paired days with valid temperatures, mean within-day BR−ST temperature was +0.032°C, with individual days differing by up to 7.5°C. Different plots and observation order may confound both wind and visitor selection. Observational label permutation cannot establish causal wind effects.
4. The response is the **fraction of observed minutes with presence of source-coded role**, not number of animals, predator attacks, relative functional fitness, cue-use behavior or a matched pair of interacting species. Historical type names such as bee-parasitic / bee-predaceous are species-group natural history, not observed activity in that watch.

## Reproducibility receipt and next identification gate

Local/released companion `andrews_wind_direct_20261022.zip`: original unchanged 2 CSVs, SHA1 receipts, source QC + earlier lag tests and source, dedicated direct-wind module + tests, independently reconstructed source/matching and exact finite daily-label permutation, full `summary.json`, hashed watch-presence ledger, full details/README. Main output JSON SHA256 **`19dc9c80e14066575ef98dfffe4aa1f6ff2fe635fde0f3050035216cc025850d`**; package SHA256 **`82e15e5c7dff19301016fdf0f1986ba3adeacd6170dd17275da9f34ff5b225f8`**. No claim that unrelated repository-wide CI is green.

**Scientific stopping rule:** no post-hoc predator taxa / windy plot groups are searched to rescue this result. To identify a genuinely hierarchical interaction, observe actual bee/enemy species-pair contact or risk exposure, concurrently blooming plants, independent wind manipulation and animal decisions (preferably followed by fitness or pollen delivery). The current result belongs to ecological observation/identification limits, not a field test of adaptive-gain routeability.

Source acknowledgement: Seo E., Jones J., Hutchinson R., Pfeiffer V. (2022), HJ Andrews Experimental Forest, USFS PNW, Oregon State University, NSF LTER, original DOI above.