# Wind–flower partner structure within directly recorded blooming plants

**2026-10-22. Fixed before calculating any wind × observed-plant visitation outcome.** Extends the source-verified H.J. Andrews Experimental Forest SA026 v8 original 2011–2021 data. The previous source-locked direct wind bee/enemy role test was a NO-GO; this is an independent *endpoint* in the same observational dataset, not independent biological replication or a search for a significant predator effect. Do not alter main or frozen manuscripts.

## Original sources and known availability limitations

Official SA026 package `knb-lter-and.5216.8`, DOI `10.6073/pasta/eec55cbc3dbfc56428629773737ab3e5`. Exact original watch CSV source SHA1 `fcd28cf0c9623fbfbc5619136334265a65f13dc4`, 74,942 rows; original flower CSV SHA1 `c93b5496154245b9e94dc3362297ed354db3ebb6`, 23,642 rows. Require public checksums, complete 15 min observational effort, consistent wind ST/BR per watch, no minute-level conflicting status, positive visitor counts when marked positive. A flowering taxon is considered observed-available only where `FLW_STATUS=FLW` in an **exact same SAMPLEDATE × PLOT_ID × WATCH** flower inventory. Never fill unrecorded plant identities with zeros or assume bloom is complete. Exclude duplicates in the source flower watch×plant key. Different ST and BR watches may be different meadow plots; the same plant *name* appearing in both is not the same individual flower or equal rewards.

## Outcome-independent common-support gate

For a meadow × day, compare only botanical species codes directly recorded flowering in at least one ST AND one BR 15-min watch in that same meadow-day. Need >=2 such floral species per day. Whole-watch wind labels may be exchanged within each meadow-day with unchanged number of ST and BR watches. **For a label permutation to be admissible, all fixed compared plant species must STILL be observed flowering at least once in both label groups.** This conditions the wind-randomization reference on observed floral exposure; no fake zero-exposure cells. Require >=2 admissible assignments/day.

Pre-outcome metadata-only count: **35 meadow-days / 11 meadows / 162 distinct day×plant codes**; 207 watches on these days including watches not necessarily carrying any shared flower. Alternate threshold >=2 ST and >=2 BR watches per paired day has 23 days before audit.

## Primary wind × flower-link heterogeneity test

At each flowering plant p in watch w, let `z_all(w,p)=1` when at least one original confirmed visitor has an actual positive interaction to **that same plant code** in that exact watch, else 0 (flower was independently recorded and observed for 15 min). Define separately `z_bee(w,p)` for source-coded social/solitary/halictine/semi-social/pollenivore bees from the previous frozen SA026 role vocabulary. Multiple recorded visit events in a minute count only once for binary appearance, by watch×plant; this tests observed link incidence, not choice probability per individual.

For each day d and observed flowering plant p, compute
`delta(d,p) = mean_BR z(w,p) - mean_ST z(w,p)`.
For each day with >=2 plant codes compute
`H(d) = mean_p[(delta(d,p) - mean_p delta(d,p))^2]`,
the **between-plant variation in wind-related link incidence changes**. This removes the day's uniform decline/increase common to all plants; H>0 alone is inevitable when different plants have different visit rates. Subtract the **exact within-day admissible-label permutation mean**, `excess_H(d)=H(observed)-mean_permutation H`. Primary estimand: average excess_H **equally across meadows after averaging days within each meadow** (unweighted across sites, not 162 independent plants).

One-sided randomization p is probability of equally or more positive excess_H under independent, conditionally admissible *whole-watch* wind-label permutations, using 9,999 draws over day-level exact finite assignment lists, plus the observed. Two registered endpoints **H_all primary and H_bee secondary**, adjust their p-values by Holm across both. Bootstrap 4,999 whole meadows (with all days together) for exploratory percentile 95% intervals on excess H. This does NOT randomize wind in nature; garden plot location, time, flower quantity, phenology and observer may violate exchangeability.

## Secondary signed opportunity-adjusted wind response and sensitivities

For both visitor endpoints, report `mean_p delta(d,p)` with day→meadow equal weighting, and a two-sided whole-watch conditional permutation diagnostic; distinguish partner-specific heterogeneity from a uniform effect. Do not promote significance from this uncorrected diagnostic. Additional fixed sensitivity A: >=2 BR and >=2 ST watches/day and >=2 admissible assignments. Sensitivity B: require positive numeric NO_STALK and NO_FLWS in all included compared plant-watch cells, recompute admissible assignments and eligibility; NO_FLWS and NO_STALK may use unlike biological counting units, so do not multiply them into an invented unified flower opportunity count. Report eligible meadows/days and NO-GO when fewer than 8 meadows or 20 days. Sensitivity C: day-equal pooled H (not just meadow-equal). No post-result taxon/species filter tuning.

Scientific ceiling: positive excess_H would be **wind-associated, plant-identity-dependent observation of flower visitor links conditional on recorded bloom exposure**, not proof that insects actively switch flower preference, wind modifies encounter/search costs, or that predator/prey/competitor species cause an indirect pathway. True behavioral routeability needs concurrently measured choice set, randomized wind/flower access, and individual decisions/fitness. A null cannot establish no ecological wind effect given 11 meadows and limited paired watches.
