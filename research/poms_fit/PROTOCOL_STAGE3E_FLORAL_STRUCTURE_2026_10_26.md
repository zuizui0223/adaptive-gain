# Stage 3e — Does floral structure modify the wind–pollinator-guild association?
Date: 2026-10-26. **Prospectively locked for this exploratory extension, after inspecting Stage 3b–d positive results. Not an independent confirmatory preregistration.**

## Target and biological question
Does the *observed association* between reported wind categories and the **conditional odds of bumblebee versus other-fly visits to the same preselected flower target** differ between the source-defined *open* and *closed* flower-structure classes? This asks about a **wind × floral structure interaction** in realised focal-flower visit composition, not flower-choice routeability, competition, or a wind intervention.

## Data, immutable provenance and observation grain
Original PoMS FIT Counts 2017–2023, one 10-minute survey of a single target flower within a 50×50 cm quadrat. Preserved original CSV members:
- structured 1km FIT: SHA256 `29d3deb757c053774c26ece0a7683081a4b4fe81d9497877fe1179f232182e52`
- opportunistic public FIT: SHA256 `bcd2ef780d3208a5a4aba5c191178900ccef705e5b569dc0160b27d00652dc3c`

**Audit first**: native `flower_structure` category levels and frequencies, exact target-name × structure contingency, treatment × structure × guild-positive support, sites exhibiting calm and strong within each structure, paired visitation totals, and unknown `Other` target extent. Original publisher's corrected morphology annotation is a coarse structural attribute, not a per-flower physical measurement.

## One locked estimand and explicit no-go rules
Primary structured 1km mode, initially eligible surveys under the Stage 3d covariate eligibility, then require exact source categories corresponding unambiguously to *open* and *closed*. Exclude null/uncertain/other flower structures; retain zeros in the original **total-count quality profile**, but the binomial composition outcome necessarily conditions on bumblebee + other-fly visits >=1. Exclude source target category `Other - please describe below` for the primary morphology test because it combines multiple biological taxa with potentially heterogeneous floral structures. Do not manufacture target descriptions.

First apply support gates within the named-target pair-positive population: >=100 surveys for each structure; >=30 pair-positive surveys in **each** structure × (strong, calm) cell; >=10 distinct 1km sites with samples in both calm and strong for **each** structure. If any fail, record `NO_GO_INSUFFICIENT_STRUCTURE_OVERLAP` rather than estimate a significant contrast from sparse support.

## Locked model
Aggregated binomial outcome `[bumblebees, other_flies]` with cluster-robust standard errors at 1km site. Include wind three source levels (reference calm), corrected target plant categorical FE, site categorical FE, log1p(floral_unit_count), recorded sunshine, year, day-of-year spline with 4 df, clock bins, recorder_type (missing category), flower_cover (source `Not recorded` retained).
- **Omit floral_unit type** as a separate main effect among named targets where it is *exactly aliased with corrected target*, as documented in Stage 3. Omit flower_structure main effect because it may be exactly determined by target FE.
- Add exactly **two** product contrasts `gentle_wind × closed` and `strong_wind × closed`. No alternate winds, grouping thresholds or tested plant structures selected by p-value.
- Primary inferential test: joint 2-df Wald test of both wind × structure interaction coefficients. Secondary strong-wind effect-modification odds ratio `exp(beta_strong_closed)`, with site-cluster CI, plus identifiable strong-wind OR in open/closed classes from the fitted covariance. Report support, design rank, convergence, overdispersion and full result irrespective of p-value.

## Sensitivities declared before Stage 3e interaction result
- Repeat the *same* contrast in the public FIT mode, with country/habitat control and 1km-square clustered covariance, preserving the same named-target and structure criteria. This is within a single monitoring programme, **not** independent experimental replication.
- Separately assess how adding heterogeneous `Other` target surveys changes structure coverage and the effect, but never promote a result supported only by that taxonomically mixed category to morphology adaptation.
- If structure classes are not operationally comparable, stop at **data-quality descriptive analysis**.

## Causal/interpretation firewall
Even a positive interaction is observational and a potential composite of species identity, flowering phenology, reward variation, target choice, intrinsic detection/identification, within-site wind selection, wind-dependent flower motion, and nonindependent insect visits. The data do not contain directional winds, individual foraging trajectories, competition, simultaneous floral alternatives, reproduction or sensory cue sequences. No adaptive `C_A/C_F`, fitness or causal niche partitioning inference. Keep frozen V5/V6 manuscript surfaces unchanged.
