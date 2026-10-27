# Stage 3g — surrounding Pan flowering-family composition versus wind/guild association

**Date:** 2026-10-28. **Exploratory/post-hoc:** the earlier positive bumblebee versus other-fly wind association was observed in Stage 3b–f. This protocol is committed *before* inspecting Stage 3g empirical family covariate model results. It is not a confirmatory preregistration or evidence of other-species causal effects.

## Hypothesis
**Richness and community composition are different ecological quantities.** Stage 3f found the wind-associated shift in relative recorded bumblebee-to-other-fly visitation persists after controlling **how many** distinct flowering plant labels were recorded near Pan stations. Stage 3g asks whether controlling **which botanical families were represented** in those measured Pan station flower inventories changes the association.

### Source and strictly comparable grain
Re-use exactly the verified original UK PoMS data:
- 2017–2023 Pan station original CSV SHA256 `70f3429e5ed9022d3d7b80fc3f24c589ecc5faff608393bc53febfac49788277`.
- 2017–2023 Pan flower occurrence original CSV SHA256 `53daa167282092b7081190de00e020b4e2635fa5e7d4fc63d3454f7c338951ba`.
- Structured 1km FIT original CSV SHA256 `29d3deb757c053774c26ece0a7683081a4b4fe81d9497877fe1179f232182e52`.

Stage 3f strict `location_code × x1km_square × date` join, **all five unique Pan stations**, at least one named original Pan flower taxon, Stage 3d eligibility, and **bumblebees + other_flies > 0** are unchanged. Baseline population is the same **2,210 original 10-minute focal-flower FIT censuses at 95 1km sites**. No FIT row multiplication. Eleven Pan flower occurrences without a source parent station remain quarantined. No imputed zeros or unobserved alternative flower choice sets.

## Family composition covariates, chosen without FIT outcome
For every source Pan sample: link flowering occurrence `sample_id` to Pan station `sample_id`; attach native Pan `family` and source taxon version key. Deduplicate **one taxon identity per exact Pan site-day**, even when found at multiple Pan stations. Preserve `unknown` family as an explicit denominator class; do not guess a taxon-to-family assignment. If a single original Pan taxon identity has conflicting recorded family labels, record the conflicts and **fail close** instead of arbitrarily choosing a family.

Choose exactly **three** botanical families by the number of **unique Pan site-days in the 1km source** where at least one of their taxa was recorded, in decreasing order, with lexicographic tie-break. Choose from the *complete Pan source with all five Pan stations and at least one recorded taxon*, not from FIT outcomes or model p-values. Family candidates must have >=50 distinct Pan site-days. No threshold tuning and no substituting another family if a gate fails; log the source top families and coverage.

At each site-day, define `Pan family fraction` = (# distinct Pan flower taxa with that original family label) / (# distinct Pan flower taxa with any original family label, including source-unknown). Thus all three fractions lie in [0,1]; other botanical families form the unmodeled reference mass. **Never sum original `total_floral_units` across heterogeneous flower-unit definitions.** Source Pan occurrence taxon identity is not an FIT animal's perceived alternative plant.

## Primary model and gates
On exactly the same 2,210 prior matched FIT surveys, compare:

1. **Stage 3f baseline:** grouped-binomial `[bumblebees,other_flies]` on original 10-min pair-positive FIT visits, with wind categories, corrected FIT target flower, log1p focal floral units and floral-unit type, year, 4-df day-of-year spline, sunshine, source clock bins, recorder classification, flower cover, **site fixed effects**, log1p Pan recorded floral richness and site-clustered sandwich covariance.
2. **Pan community composition model:** add the three Pan-family fractions *only*, retaining all prior covariates and the same survey records. Primary inferential quantity: one **joint 3-df Wald test** of the three fractions; report strong-wind (vs calm) OR and 95% cluster CI before/after on the exact same FIT records. Log family fractions, within-site variation, model rank, source site-year representation, Pearson overdispersion, and nonfinite nuisance coefficient uncertainty separately.

Family admission gates: >=50 Pan site-days and >=10 distinct original Pan 1km sites for each chosen family, >=10 1km FIT sites showing within-site fractional variation for each selected family, and all 2,210 FIT census links to five-station Pan contexts identified. Need full design rank and finite *wind + family* targeted covariance/intervals; otherwise report NO_GO. Do **not** swap family variables or replace the model after inspecting outcome.

**No family-by-wind interactions in this stage.** No selecting one botanical family as an explanatory mechanism based on nominal p-values. The 3-df test is a descriptive association across a family selected with no FIT outcomes, not biological interaction/causal mediation.

## Predictive firewall
In-sample incremental fit cannot establish generality. Do not claim improved forecasting or general ecological interactions without **site-year-blocked held-out validation**, with complete train/test separation for fitting feature weights. Any positive Stage 3g in-sample signal is exploratory and requires externally validated taxonomic and floral availability data before promotion.

## Interpretation boundary
Pan stations measure flowering plants within 2 m of separate pan traps, not alternative flowers at the FIT focal quadrat. Family proportions can be affected by year, site, plant richness, monitoring protocol, completeness and taxon-ID consistency; site FE does not repair nonlocal exposure. FIT records counted insects at one observer-chosen floral target, not individual foraging sequences. **No wind-caused interspecific competition, nectar handling, flower-direction mechanism, rewiring, decision `C_A/C_F` or fitness inference** follows from this stage. Source data remain in CI runtime only; upload only hashes, aggregate site-day/diagnostics and model results. V5/V6 manuscripts unchanged.
