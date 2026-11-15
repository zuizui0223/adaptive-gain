# Stage37: Original orchid-bee wind association under day and two-way clustering

**2026-11-15. Verified original published observations, no new insects. This is NOT a wind×scent ON/OFF experiment or a plant reproductive fitness analysis.**

## Source identity and estimand

Crall et al. (2020), Biology Letters DOI 10.1098/rsbl.2020.0103, original Zenodo DOI 10.5281/zenodo.3743898. Author archive SHA256: 4250cb51754e59b861f90ff7063dbbc223dd515a146809273fee055de81772af.

The original experimental grain is 70 20-minute fragrance-bait collection sessions, nine sites, 29 dates, 409 recorded male orchid-bee arrivals/collections. There were 67 cineole and three methyl-salicylate scent-bait sessions. THERE IS NO SCENT-FREE CONTROL GROUP. The estimand is an observational visit-rate ratio per DOUBLING of mean wind speed within sites and controlling for source-defined relative kinetic energy / turbulence.

## Source-verified independent reanalysis

| Numerical inference method | Wind coefficient per log10 wind | IRR per doubling | Interval, 95% approximation |
|---|---:|---:|---|
| Stage36 site-conditioned Poisson with source relative TKE | +1.11422048 | 1.39852 | Model-based 1.18842–1.64576 |
| Same model, sandwich clustered by site (9 groups) | +1.11422048 | 1.39852 | t8 approximately 1.07216–1.82423 |
| Same model, sandwich clustered by date (29 groups) | +1.11422048 | 1.39852 | t28 approximately 1.11958–1.74696 |
| Stage37 TWO-WAY sandwich, site+date | +1.11422048 | 1.39852 | t8 approximately 1.09658–1.78359 |
| Stage37 site+date FIXED intercepts Poisson, source relative TKE | +1.46962767 | 1.55644 | Unclustered model-based 1.23790–1.95695 |

Two-way variance is the inclusion-exclusion sandwich V(site)+V(date)−V(site×date). The t8 multiplier is a sensitivity approximation, NOT a guarantee of exact frequentist coverage in nine site clusters. The fixed-date model used 39 independent columns and 31 residual degrees of freedom in the original 70 sessions; this is a relatively high-parameter alternative specification, NOT the author model with random site+date intercepts, and its unclustered 95% CI may be too narrow.

The original paper R final formula is count ~ log10(wind.mean) + cover200m + rel.wind.KE + (1|site) + (1|date), family=Poisson. Our site-conditioned design absorbs static site-specific cover, whereas the date-fixed alternative adjusts date intercepts but does not impose or reproduce the same mixed-model distribution.

**Deletion stability:** 29 out of 29 leave-one-original-date-out fits had positive log-wind coefficients, range +0.895036 to +1.288767. Earlier Stage36 found nine out of nine leave-one-original-site-out positive coefficients, range +0.914924 to +1.317906.

## What the evidence does, and does not, establish

Supported for this source system: higher mean wind speed within a particular scented bait station is associated with higher male orchid-bee arrivals in the analyzed original data, robust in sign to deleting a single site/day, and supported by the original article. This is an original-DATA reanalysis, not a newly discovered ecological phenomenon in nature.

**Not identified**:
- A causal effect of manipulating wind rather than weather-correlated changes in animal activity;
- Scented vs scentless flowers or an experimental wind-by-scent factorial contrast (ALL sessions scented bait);
- Flower discovery distance or the local odor plume flux/concentration;
- Bee/moth/hoverfly learning, differential sensory cognition or flight control;
- Landing success, pollen removal or deposit, outcross pollen, viable seeds or actual plant fitness.

Nine sites are a small cluster count; the two-way sandwich and t8 approximation may understate or misstate uncertainty, and positive coefficients across deletion fits do not independently validate wind randomization. Between-site site-mean wind and mean visit rate are descriptively negatively correlated (Stage36 r≈−0.5104 across nine sites), but this is strongly susceptible to site habitat and background abundance confounding.

## Reproducibility

This Stage37 is stacked on Stage36 PR #116, preserving Stage36 and earlier stages. twoway_cluster_date_fixed.py independently computes site+date two-way sandwich covariance, rank-checked site+date fixed Poisson and leave-one-date-out conditional site Poisson; test_twoway_cluster_date_fixed.py tests math and source-identity refusal on wholly synthetic trial rows. The dedicated Actions job fetches original ZIP with its checksum and hash verified, and stores DERIVED JSON ONLY, never raw author data.

Original-source Stage37 dedicated CI on original author data **SUCCESS run 43701883787** after correcting a source-identity-vs-session-grain test expectation. Nine tests passed. Whole repository Python 3.10/3.11/3.12 CI on final PR commit must be checked separately.

Next biological identification problem: original randomized odor emission versus scent suppression, crossed with wind strength and measured distinct discovery, landing, pollen-transfer stages, ideally jointly in the same source cohort. Cross-paper studies cannot be multiplied as a measured natural flower reproduction rate.
