# Within-guild seasonal taxonomic turnover — 2026-10-20

Prospective analysis contract within an already exploratory PoMS research programme. This is a NEW endpoint, not another adjustment aimed at recovering a positive FIT coefficient. Main and frozen manuscripts unchanged.

## Question
Does the composition INSIDE hoverfly and bee pan-trap groups differ between May–June and July–August beyond rearrangement of whole sampling dates? The previous FIT data identify broad guilds, not the visiting species, and cannot establish that captured taxa visited the focal flower.

## Original sources and taxonomy
Use checksum-locked original PoMS 2017–2023 pan sample and specimen CSVs from DOI 10.5285/5841bfae-471b-498c-af89-c30e5140d6c5, retained with the preceding reproduction package. Primary taxon field is the supplied `taxon_aggregated`, whose codebook explicitly harmonizes sex-dependent identifiability. It includes species complexes and genus-level units; do not call every unit a species.

A missing aggregate may be filled only by a unique mapping found in other source rows after removing parenthesized subgenera and `[Genus inferred]` from the original name. No guessed taxonomic assignments. Unresolved group/site/dates and sample-vs-occurrence count mismatches are excluded and inventoried. Classify bees using supplied Hymenoptera group labels, including the four records lacking an order label. Retain source originals unchanged and omit original recorder identifiers from derived outputs.

## Fixed population
May–August; undisturbed stations; 4–8 hours; exclude entire ambiguous duplicate station/site/date sets. Site-dates require 3–5 valid stations. Within each site-year use the SAME intersection of stations present on EVERY qualified date, requiring at least three. Primary group/site-years require at least three dates, at least one in each period, at least 20 specimens pooled across dates, and positive group catches on every date. These are sufficiently sampled panels, not all site-years. No contrast is used for inclusion.

Compute taxon catches per total station-hour for each date; average date vectors within each period; normalize each period's vector. Primary descriptive distance is total variation, TV=0.5 sum |p_early-p_late|. This is dissimilarity in normalized catch composition, not percentage species replacement. Also report expected taxon richness rarefied to 10 actual specimens in each period when both observed totals are at least ten, retaining the subset size separately.

## Whole-date null and replication
Enumerate allocations of whole date vectors to the observed number of early dates, holding all within-date covariance, observed effort, station identity and counts fixed. Subtract mean null TV from observed TV. Cap exact enumeration at 20,000 allocations; otherwise use 9,999 seeded allocations plus the observed one. Degenerate nulls are flagged rather than interpreted as absence of ecology. Date exchangeability is a model assumption; weather, serial dependence and trap selectivity are not eliminated.

Average years equally within site, then sites equally. Use 4,999 whole-site bootstrap draws for descriptive intervals. A separate macro randomization diagnostic samples a date allocation for each site-year and aggregates identically; report plus-one tails and Holm adjustment for the two primary groups. Interannual, spatial and temporal dependence remain limitations.

## Fixed sensitivities — report all
1. At least two dates in each period.
2. At least five group specimens on every date.
3. Deterministically coarsen official taxon units to first-token genus/coarse label. Higher-level labels remain explicitly unresolved. TV cannot increase under this coarsening.

No post hoc positive-result restrictions or season-window search. No trait imputation, causal mediation or new fitted FIT models.

## Interpretation boundary
A positive result supports seasonal organization of captured taxonomic composition within coarse guilds. It neither attributes the prior hoverfly FIT increase to those taxa nor measures individual preference, true background abundance, latent rewiring, fitness or adaptive cue routing. Link to previous FIT sites only as a labeled descriptive overlap, not independent replication. The source metadata and mandatory UK PoMS/UKCEH partnership acknowledgement accompany the reproduction package.
