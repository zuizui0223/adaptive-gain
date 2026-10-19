# First original-data macro run: temporal partitioning of observed partner use

2026-10-19 exploratory analysis plan, recorded before inspecting its numerical results. This is separate from the frozen V5/V6 theoretical papers and PR68 animal-experiment scaffolding. It implements one observational branch of RESEARCH_PROTOCOL_2026_10_18, not a direct routeability test.

## Source and complete-data policy
Fetch the complete OIK-07303_database.csv, not OIK-07303_results.csv, from Schwarz et al.'s 30-source compilation (Dryad doi:10.5061/dryad.qz612jmbp, Zenodo record 4744654). Require the repository's published raw MD5 7a70c3e2356611b0871c163a2f9aed4a. Retain full original bytes and SHA256, references workbook, README and aggregation script. Cite original contributing studies using the supplied references table. No new organismal data are invented.

Count every raw row; do not deduplicate repeated positive records without observation IDs. Sum freq as recorded interaction multiplicity, not as number of independent insects or hours of effort. Tabulate all 30 source IDs and inclusion/exclusion reasons. Restrict primary temporal tests to observations explicitly labeled sgrain=day with valid positive integral frequency, date and taxon identifiers. No positive-only table can supply a zero-survey denominator.

Use compiled study x sSite x calendar-year x higher (visitor taxon) as a panel. Species/morphospecies codes remain local to their source; a panel is NOT an individual bee. Compilers pooled some nearby original sites and shifted dates by +182 days in Chacoff2018, Kaiser-Bunbury2017 and Vazquez2003. Compiled years are season containers, not true calendar years for climate matching. Do not attach actual-day weather or interpret a sampling date as an animal decision deadline.

## Quantity
For each panel, construct the full count matrix of date x plant. Pooled effective partner diversity is exp[H(plant)]; within-date effective partner diversity is exp[sum_d p(d) H(plant|d)]. Their ratio is exp[I(plant;date)]. The ratio is at least 1 by entropy algebra, so observing ratio>1 alone is NOT a novel or sufficient ecological result.

## Conditional randomization
Compare observed I against 199 label permutations preserving the total number of records for each date AND total visits to each plant within that visitor panel. This is a fixed-margin finite-sampling benchmark, not a free random network. Secondary nulls shuffle only within 7-,14-,28-day calendar blocks, preserving plant totals within each block and date totals. They retain broad observed seasonal turnover at those resolutions, but do NOT directly measure or correct floral abundance, actual phenology, observation effort or detectability.

Primary eligibility fixed before results: >=40 recorded visits, >=4 recorded dates and >=3 recorded plant partners. Retain exclusion tables for EVERY daily panel. Keep all source studies in the source inventory even if no panel qualifies. Display group-level permutation tail rates descriptively; visitor panels within study/site/year are not independent experimental replicates. Equal-source summaries, not event-pool significance, are the first macro comparison. Shared-origin source datasets must be audited before treating source labels as independent meta-analysis units.

## Interpretation boundary and competing explanations
Positive excess segregation beyond fixed margins means the observed partner composition is more time-organized than the chosen conditional exchangeability null. It may reflect plant or visitor phenology, resource availability, temporal habitat sampling, floral observation allocation, colony/individual turnover, or behavior. Positive 14-day-block excess is not proof that phenology or effort is controlled. This file does not infer C_A, C_F, perceived cues, profitable resource labels, latent network rewiring or adaptive fitness.

The ecological bridge is a narrower question: is broad observed season-long resource use concentrated in temporally narrower partner subsets? A positive answer challenges treating seasonal pooled degree as simultaneous choice burden, but does not prove the adaptive-gain mechanism. Independent resource and sensory data remain required for that hypothesis.

## Outputs
quality_profile.json, source_inventory.csv, eligibility_all_panels.csv, visitor_site_season_results.csv, study_results.csv, summary.json and unmodified source files. Numerical unit tests are executed before data analysis. A completed Actions run, source checksum and printed ANALYSIS_COMPLETE marker are required before describing all-source computations as completed.
