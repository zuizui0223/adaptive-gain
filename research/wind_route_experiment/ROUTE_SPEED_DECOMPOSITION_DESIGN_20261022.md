# Mechanistic decomposition of wind-associated speed change: route occupancy versus within-route motion

**2026-10-22, exploratory secondary analysis of the published 548-flight honeybee wind-tunnel data.** The two explanatory branches chosen below were selected **after inspecting route-support counts**, not registered before any outcomes. Treat every interval as exploratory; no positive interaction claim is preregistered. Do not edit main or frozen manuscripts.

## Question

In a randomized wind-versus-still experimental tunnel, does wind alter average flight speed primarily by (i) changing the fraction of flights whose **median altitude is above the obstacle field** versus (ii) altering the observed speeds among flights in each altitude-defined route category? This is an **algebraic partition, NOT a causal mediation analysis**: route occupancy is measured after wind exposure, and within-route subgroups are self-selected.

## Primary support restriction and weighting (before effect calculation in new pipeline)

Dryad Burnett, Badger & Combes (2022), DOI `10.25338/B8Z34Q`, CSV `Bee_route_choice_in_wind.csv` SHA256 `2361dccb523b97f1e5e542fc492d302a5e7c290cdde72eb2dfb2ce021153d6f7`. Data contain 548 flights, 58 distinct honeybees, height fixed per bee and wind randomized within bee. Route `A=1` if measured **median altitude > canopy height**; route=0 otherwise. This is not the trajectory or observed ecological route between flowers.

Stratum heights **98 and 127 mm primary**: at BOTH wind settings each has at least 8 'below/within' flights and 20 'above' flights, allowing a two-route descriptive decomposition. At 69 mm the 'within' wind arm has only 3 flights; 40 and 11 mm mostly cannot distinguish two route types. Each bee must have one recorded flight in both wind conditions (not necessarily both route types). A bee's flights under a given wind condition get a total weight of 1, regardless of how many films were obtained. Heights 98/127 are weighted **equally** (two physical conditions, with 11 and 10 bees) to avoid over-weighting a richer height. Secondary include 69 mm with caution, and split up/down tunnel flight directions where all four route cells have support.

## Exact symmetric change decomposition

For each canopy height h, wind condition w∈{still=0,wind=1} and route r∈{within=0,above=1}, compute with equal-per-bee within-w weights:

- p[h,w,r]=weighted fraction of films in observed route r;
- v[h,w,r]=weighted mean ground speed among films in observed route r (NOT average of per-bee route-specific means);
- μ[h,w]=∑_r p[h,w,r]v[h,w,r].

Then exact symmetric identity **Δμ = C + P**, where

C = 1/2 ∑_r (p_1r−p_0r)(v_1r+v_0r) = route-*composition* term;

P = 1/2 ∑_r (p_1r+p_0r)(v_1r−v_0r) = observed *within-route mean-speed* term.

Report changes in **m/s**, every height, and direct arithmetic errors <1e−12. Signs of C/P are descriptive, not causal effects or a decomposition of insect energetic expenditure. Report both routes' support counts. Derive estimates by height then average across heights equally.

## Uncertainty, diagnostic and stop rules

Whole-bee cluster bootstrap **9,999 replicates**, stratified within physical obstacle height; resample whole bees with all flights and both wind records, maintaining equal weight per sampled bee. The 95% intervals are percentile distributions, exploratory. Count any replicates with absent wind×route cells; do NOT impute a route-cell speed if no observations exist. Show sensitivity with height 69 added, and head/tail flight direction strata if possible. A conditional significant within-route component is *not* proof of wind causal action along a fixed route since route is post-treatment. A nonsignificant C is *not* equivalence/absence of rerouting. Report the fraction of difference due to contributions only if denominator is safely nonzero, otherwise avoid dividing by near zero.

No p-value fishing by choosing height subsets or changing altitude threshold after seeing estimates. Do not call flight corridor selection a species interaction, cue order, `C_A < C_F`, fitness or physiological efficiency. Distinguish measured **ground speed** from travel cost and from plant resource accessibility.

## Validation and deliverables

- Source SHA256, valid factor levels, fixed height-per-bee and matched wind status, no row/drop silent exclusions.
- Test decomposition identities (C+P=Δ), swapping route labels leaves contributions unchanged, zero route change yields C=0, zero speed shift gives P=0, hierarchical equal-bee weighting, impossible empty route cell raises a clear NO-GO, field independence not claimed.
- Recompute the primary three components independently from raw CSV using separate loops to detect shared implementation error.
- Save auditable JSON plus context/limitations, executable scripts and tests, and GitHub branch-only report. Never alter frozen manuscripts.
