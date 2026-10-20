# Independent-context adjustment of paired seasonal FIT rates — 2026-10-20

Exploratory follow-up: previous PoMS outcomes are already known. This is not preregistered or independent confirmation. Do not tune a predictor set to obtain a favorable seasonal coefficient or interpret coefficient changes as a causal mediated fraction. Frozen manuscripts and main remain unchanged.

## Question and inputs
Within the same monitoring square/year/named flower category, what late-minus-early visit-rate difference remains after accounting for measured focal flowers, independently collected insect catches, and nearby recorded flowering plants? Compare May–June with July–August, 2017–2023, monitoring FIT only. Primary outcome: hoverflies, selected because of the preceding result. Prespecified comparator: aggregate bees (bumblebees+honeybees+solitary bees). Retain performed-survey zero counts; exclude unspecified Other flowers and inconsistent floral-unit definitions.

Use original FIT DOI 10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618 and pan-trap DOI 10.5285/5841bfae-471b-498c-af89-c30e5140d6c5. Verify all member SHA256 values against the preceding reproduction package. Exact site/calendar-date matching only. Traps must be undisturbed, exposed for 4–8h, with >=3 unique stations; exclude the full ambiguous duplicate-station site/date. Orphan flower records are excluded.

## Independently measured floral context
Flower records cover herbaceous plants in bloom within 2m of stations, not a square-wide inventory or FIT-patch choice set. A station without a list is unknown, NOT zero floral richness. Primary dates require at least three valid stations with recorded flower lists. Use the mean distinct normalized taxon-label richness among those stations and separately the fraction of valid stations with a list. Do not add counts measured in different floral units into a fictitious common quantity. Missing temperature excludes a date before pairing.

## Estimand and four fixed models
Pair strata with at least one eligible survey in each period. Outcome = late mean recorded visits/10min minus early mean recorded visits/10min. Within-site strata receive equal weights, with every site having total weight one. Covariates use the same survey weighting as the outcome. Reuse of a trap date for different flowers is clustered at whole-site level.

Fit weighted linear mean-difference models on identical complete-case strata:
- M0: intercept only, reproducing the equal-site paired difference.
- M1: M0 plus change in mean log1p focal floral-unit count.
- M2: M1 plus change in mean log1p corresponding pan catch per station-hour.
- M3: M2 plus change in mean log1p recorded flowering-taxon richness, change in recorded-station fraction, and change in mean trap start/end temperature divided by five degrees C.

The intercept is an adjusted seasonal difference at zero change in measured context. Check whether zero is in the joint covariate-change convex hull. This is descriptive adjustment, not a normal-count generative model or a causal effect. Catch rates are method-selective noisy activity proxies, not unbiased abundance. Temperature and recorded richness do not remove weather, detection, flower-quality or resource-composition confounding.

## Fixed uncertainty and sensitivity rules
Use 1,999 whole-site bootstrap resamples with full refitting, preserving all paired strata of selected sites and equal total site weights. Report percentile intervals and singular-fit rates. Do not promote an interval if >5% of refits fail. These intervals are exploratory and pointwise, not spatially or globally multiplicity-adjusted.

Report the same four models under: primary population; <=2-fold mean focal-flower change; all valid stations having flower lists (rebuild pairs after restricting dates); and identical station sets over paired dates. Report all results regardless of sign. Full-model leave-one-site-out influence check. Independently reproduce primary M0 from original FIT rows and verify coefficients with a separate weighted least-squares implementation. No additional model hunt after these runs.

Deliver exact source receipts, exclusions, hashed-site paired ledgers, all 32 model comparisons, code/tests, raw and adjusted differences, and qualified biological conclusions. No causal preference, sensory routeability, fitness or latent rewiring claim.