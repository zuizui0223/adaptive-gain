# UK PoMS Stage 3b–d — wind-dependent pollinator guild composition (2026-10-26)

**Exploratory, post-hoc original-data result.** Three stages (conditional guild composition, held-out survey-mode and matched controls, clock/recorder/flower-cover controls) were executed after the Stage 3 total-visit-rate analysis. These are **NOT** preregistered confirmation, manipulated wind experiments, true simultaneously available flower choice sets, competition or routeability measurements. All published source content SHA-256 digests remain checked and frozen V5/V6 manuscripts remain untouched.

## Original source and completion receipts

UK Pollinator Monitoring Scheme (2026), *Flower-Insect Timed Count data 2017–2023*, NERC EDS EIDC, https://doi.org/10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618. Original CSVs:
- structured 1km FIT (3,053 surveys): SHA-256 `29d3deb757c053774c26ece0a7683081a4b4fe81d9497877fe1179f232182e52`;
- public FIT (13,457 surveys): SHA-256 `bcd2ef780d3208a5a4aba5c191178900ccef705e5b569dc0160b27d00652dc3c`.

All 16,510 original sample IDs are unique; insect-group sum equals the reported total in 16,510/16,510 surveyed rows; zero-total-insect surveys are genuine published FIT sample rows (774 public, 271 structured), **not imputed absent survey dates**. The provider's dynamically generated ZIP wrapper is not hashed as if byte-stable; original uncompressed CSV bytes are hashed independently.

Execution:
- Stage 3b + group binomial tests: https://github.com/zuizui0223/adaptive-gain/actions/runs/40266755014 (20 tests, original source and group analyses green).
- Stage 3c transfer/influence/matched stress tests: https://github.com/zuizui0223/adaptive-gain/actions/runs/40282533307 (25 tests; source, models and result receipts green).
- Stage 3d clock/recorder/flower-cover stress tests: https://github.com/zuizui0223/adaptive-gain/actions/runs/40283435697 (34 tests; all original-source + sensitivity steps green).

All count and guild analyses use the same 10-minute **single selected flower/quadrat** unit of observation. The pair-specific composition denominator conditions on >=1 visitor from the selected pair in that FIT sample, and therefore does **not** constitute a zero-inclusive binary link-occupancy or choice-set test. The Stage 3 total-visit-rate analysis retains genuine zero observations separately.

## Finding 1: overall observed insect visits decline with stronger reported wind

Stage 3 primary adjusted Poisson count model (prespecified before the first Stage 3 fit):
- structured 1km FIT n=3,037, strong wind vs calm/occasional leaf movement IRR **0.764 [95% site-cluster CI 0.624, 0.935]**;
- public FIT n=13,257, IRR **0.837 [0.750, 0.933]**.

Models adjust log1p floral-unit count, floral-unit and target categories, season (4df smooth), sunshine and year, structured site fixed effects, or public country/habitat effects. Counts are overdispersed (Pearson ratios 9.22/16.49); exploratory negative-binomial fixed-alpha 1/2 sensitivity preserves strong-wind IRR directions and site-robust interval signs. Wind is an observer-recorded leaf-movement category, *not* anemometer velocity or wind direction.

## Finding 2: conditional bumblebee / other-fly composition differs under strong wind

Stage 3b compares a **pair of insect group counts from the exact same FIT survey** via a site-clustered binomial model. All available flowers outside the selected target are unknown, and grouped insect detections do not identify individual visitors. The pair is conditioned on >=1 of its component groups being observed. The three comparator choices were fixed *before seeing Stage 3b outputs*, but after inspecting Stage 3 outcomes, and Holm correction applies to exactly these three exploratory strong-wind tests.

| 1km pair (bumblebees relative to...) | Pair-positive surveys | Strong-wind adjusted OR [95% site CI] | Holm p across 3 pairs |
|---|---:|---:|---:|
| **other_flies** | 2,335 | **1.973 [1.401, 2.779]** | **0.000300** |
| hoverflies | 1,889 | 1.460 [0.982, 2.171] | 0.123 |
| butterflies_moths | 1,035 | 1.798 [0.659, 4.905] | 0.252 |

These are relative odds within already counted visits to selected flowers, **not** increases in absolute bumblebee visit rate; a lower observed other-fly rate is sufficient to increase the ratio. The pair binomial model remains overdispersed (Pearson/df ~2.15–2.79), with cluster robust SE used to account for site dependence. Guild labels are broad and classification errors may vary with wind or observers.

## Finding 3: selected contrast survives exploratory stress tests

A **single selected bumblebees/other_flies contrast** was carried forward after Stage 3b. The following are transparently post-hoc tests, not fresh independently preregistered discoveries.

| Analysis | OR strong vs calm, bumblebee/other-fly composition | Scope |
|---|---:|---|
| Original structured 1km survey adjusted model | 1.973 [1.401, 2.779] | 2,335 pair-positive surveys, 95 sites |
| Public FIT mode transfer | **1.513 [1.186, 1.930]** | 9,895 pair-positive surveys, 2,579 recorded 1km squares |
| Drop entire top-1%-pair-count surveys | **1.916 [1.345, 2.730]** | 23 original surveys removed (116 bumble and 930 other-fly visits), 2,312 pair-positive remaining |
| Site×year×target matched strata CMH | **1.659 [naive 1.034, 2.662]** | 41 strata from 32 sites, 107 pair-positive surveys; **only descriptive OR** |
| Structured FIT + observed clock/recorder confidence/flower cover | **1.956 [1.361, 2.812]** | 2,335 pair-positive, 95 sites |
| Public FIT + observed clock/recorder confidence/flower cover | **1.540 [1.222, 1.942]** | 9,894 pair-positive, 2,579 grid squares |

Strict matched-strata result uses a continuity correction for sparse 2×2 tables. Its naive confidence interval and p-value rely on visit-level independence that is not satisfied by insects repeatedly counted within surveys/sites; **do not use them for site-clustered significance inference**. The OR direction and sensitivity scope are the diagnostic, not a new independent p-value.

With added observed clock, recorder experience category and target flower cover:
- 1km FIT: all 3,037 model-eligible surveys have recognizable count_start_time; adjusted strong-wind OR 1.956 [1.361,2.812], site-cluster p=0.000290.
- public FIT: 13,256/13,257 model-eligible surveys have recognizable count_start_time; adjusted OR 1.540 [1.222,1.942], cluster p=0.000257.

Both modes use fixed clock bins <10, 10–12, 12–14, 14–16 and >=16, preserve missing observer expertise as a declared category, and keep site and floral controls. Adding these covariates does not remove the conditional guild-composition association in this original source.

## Nontrivial ecological interpretation and strict boundary

**Supported observational hierarchy:**

`wind class ↔ lower overall detected flower visitation`

and simultaneously

`wind class ↔ altered relative guild composition (bumblebees : other_flies)`.

The two estimands cannot be conflated: total visit-rate depression and within-survey guild-composition shifts are different levels of ecological filtering. Evidence from the same monitored programme and two survey modes, plus the explicit stress checks, makes the statistical association a **supported candidate environmental-guild filter**.

**Not established:** wind causation (wind is not randomized), wind direction, individual flight or cue-selection sequences, equal availability of all flower alternatives, individual within-species niches, interspecific competition/displacement, indirect trophic cascades, adaptive-gain structure `C_A,C_F`, fitness or evolutionary selection. Recorder expertise is self-reported and may not perfectly capture identification error; flower availability outside the focal quadrat is unobserved. The public and structured FIT modes are **not independent ecological monitoring programmes**, and all Stage 3b–d tests were exploratory after prior data inspection. Multiple comparison families beyond the original three pairs remain unadjusted across successive analysis stages.

## Next substantive verification (separate question)

To move from an **environmental relative-detection filter** to competition or information-routeability, collect simultaneous alternative flowering resources and marked individuals; manipulate wind or effective sensory cues while preserving available flower abundances, track individual decision sequences and nectar payoff, and separately measure interspecific encounter effects. A new data set with recorder/target-flower exposure and zero visits can externally test the time/flower-filter hypothesis independently of PoMS.

No routeability or novel ecological selection headline is promoted to frozen V5/V6 theory papers from these data alone.

## Attribution

UK PoMS is jointly funded by UKCEH and JNCC through Defra, Scottish Government, Welsh Government and DAERA for Northern Ireland; the UKCEH contribution is part-funded by NERC (NE/R016429/1 and NE/Y006208/1). Thanks to the volunteers and staff who collected the surveys. Data are Open Government Licence.
