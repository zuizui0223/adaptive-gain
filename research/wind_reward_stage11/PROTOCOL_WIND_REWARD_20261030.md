# Stage11 wind x floral reward — fixed pre-outcome observational analysis

2026-10-30. Original source integrity inspected, NO Stage11 association fit yet. This is an exploratory secondary analysis of a published study, not externally preregistered confirmatory evidence. Harris et al.'s seasonal energetic patterns and null simple wind association are prior findings, not ours.

## Source and sample
Dryad 10.5061/dryad.9kd51c608, version 456836. Original forensic counts: forage 1227 rows/123 survey IDs; nectar 137 rows/123 survey IDs; weather 127 readings/122 survey IDs; insect survey 123 rows. All six original file SHA256 digests verified against provider metadata. The article reports 1217/122, so do NOT force raw observations to that total. Determine primary sample by explicit keys and source validity, not the response or p-value.

Collapse forage rows to equal-weight means per original survey. Nectar columns site and weather/forage columns site differ semantically: nectar.site is local patch location, forage.site is city. Match survey and exact native parsed date; validate plant and local location. Multiple original nectar/weather readings averaged within survey BEFORE joining. Drop a survey without weather, without nectar, with unresolved metadata contradiction, or with any missing original tube volume/length/number of flowers/nectar length (documented mean-imputed ivy sample). Never fill missing raw nectar measurements using already-filled published derived volume/concentration. Keep all native rows and exclusions in QA. Source unit is survey; weather uncertainty grouped by city x date. No assumption of persistent animal identity.

Reward: use the original author's formula from Harris_2026_FE_energetics.R, applied to survey mean volume in microlitres and mean Brix: gravity=1+Brix/(258.6-(Brix/258.2)*227.1); E=(volume/1000)*(Brix/100)*gravity*16480 J/flower. E is sampled potential nectar energy, NOT observed ingestion, animal fitness, or independently validated profit. Do not multiply by visit rate for the primary predictor. Do not use original 1.24 discrimination uplift for this predictor.

## One primary estimand
Observed response y=log(1 + mean flowers probed per 60-second observation). A flower is counted only when probed in the source. This is not calculated energetic profit; the response is not algebraically generated from reward.

For each original plant species, center wind and log(1+E) using its survey means. Define w=Beaufort minus plant mean and r=[log(1+E) minus plant mean]/pooled within-plant SD. The primary effect is the coefficient of w*r. Wind is an ordinal Beaufort score, NOT m/s. Model is unweighted survey-level OLS:
y ~ plant intercepts + city intercept + w + r + w*r + temperature + blue_sky/100 + sin(2*pi*DOY/365.25) + cos(2*pi*DOY/365.25) + log(1+flower_density).

No data-driven variable selection or interactions beyond w*r. Temperature remains in native Celsius; density in flowers per square metre. Report primary coefficient, city-date clustered CR1 standard error, two-sided t p-value and 95% t interval (df=number of city-date clusters-1). Report conditional wind slopes at r=-1,0,+1 using the same covariance. Exponentials describe 1+mean probing rate, NOT an exact visit-count rate ratio. Do not infer buffering unless the actual wind slopes support that interpretation.

Feasibility gates: >=80 retained original surveys, >=30 city-date clusters, both cities, >=40 residual degrees of freedom, finite nonzero within-plant reward SD, full-rank design. If a gate fails, record NO_GO rather than dropping controls or changing response. The same data cannot identify a causal wind effect, causal nectar compensation, internal sensory order, or interspecific competition.

Supporting descriptive check (not another discovery): apply the same covariate formula separately to each city, omitting the invariant city intercept and retaining the already defined within-plant variables; require full rank and >=15 residual degrees of freedom; otherwise report not estimable. All city estimates reported, no selected positive city. No new formal p-value family is promoted.

Stop after the first source-valid execution regardless of sign or significance. Do not alter eligibility, response, energy formula, weather scale, centering, controls or clusters to rescue a result. Any source parsing/metadata repair must be diagnosed and documented separately before a new biological fit. Frozen Stage9b, Stage10 and V5/V6 remain untouched.
