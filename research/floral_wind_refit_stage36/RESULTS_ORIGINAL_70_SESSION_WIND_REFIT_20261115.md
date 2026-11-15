# Stage36 verified empirical source refit — wind and male orchid-bee fragrance bait visits

**2026-11-15. NEW independently implemented reanalysis of original published Crall et al. 2020 session data, NOT a new biological observation, NOT a meta-analytic pooled effect or odor ON/OFF × wind experiment.**

## Source integrity and effective denominator

Original author dataset: Zenodo record 3743898, DOI 10.5281/zenodo.3743898. Original archive file CrallEtAl_OrchidBeeWindEcology.zip SHA-256 4250cb51754e59b861f90ff7063dbbc223dd515a146809273fee055de81772af. Publication DOI 10.1098/rsbl.2020.0103.

Two original author session tables match on site/date/scent, count, collection start time and wind (rounded in collection metadata, full precision in integrated source). Raw metadata includes Latin-1 non-UTF-8 annotations and R-exported unnamed row index; neither is used as a response. Seventy 20-minute sessions, nine sites, 29 distinct dates, count sum = **409 male orchid bees**, 67 cineole scent bait sessions and 3 methyl-salicylate sessions. Individual bee table contains 450 rows, which are not 450 independent wind-sampling sessions; the difference relative to published total requires a separate individual inclusion audit but does not enter the session-count regression.

## Author original statistical design versus our independent method

Author final original R code:

    glmer(count ~ log10(wind.mean) + cover200m + rel.wind.KE + (1|site) + (1|date), family="poisson")

Author publication reports within-site positive mean-wind and relative turbulence associations, but not positive between-site wind association. In this Stage36 we instead independently fit conditional Poisson on ORIGINAL session counts given the site total, with log10(mean wind) and original relative TKE as continuous covariates. Site conditioning removes the site-intercept and absorbs site-level forest cover differences; it does **NOT** reproduce the date random intercept or the full original GLMM likelihood.

The model is re-fit on the 70 original rows by dedicated GitHub Actions, which checks source hashes/joins. A second numerical implementation with Statsmodels fixed-site GLM and site/date sandwich variances has been submitted separately for independent validation; its status must be checked on the exact final head before claiming agreement.

## Verified original-data findings (Stage36 custom conditional site Poisson, source-locked run 43696348023)

| Model specification | Original sessions | Wind beta per log10 unit | Visits IRR per wind speed DOUBLING | Model-based 95% IRR |
|---|---:|---:|---:|---:|
| Wind only, conditional on site | 70 | +0.955050 | **1.33309** | 1.13838–1.56110 |
| Wind + relative turbulence, conditional on site | 70 | **+1.114220** | **1.39852** | **1.18842–1.64576** |
| Cineole-only wind + turbulence | 67 | +1.227443 | **1.44701** | 1.22191–1.71357 |

Primary original relative-TKE beta is +0.502685 (model-based SE .15847). The primary Pearson residual-to-df overdispersion ratio is **1.82847**, so naive independent-Poisson normal confidence bounds are likely too narrow. An approximate quasi-Poisson scale-only correction to the primary wind IRR gives **1.12220–1.74288** for a doubling. This corrects marginal variance scaling only; **it does not resolve date/session autocorrelation, nine-site cluster uncertainty or unmeasured confounding**.

Leave-one-original-site-out sensitivity: **9/9 log-wind slopes positive**, range +0.914924 to +1.317906 under this model. Between the nine site means, descriptive Pearson correlation of site-mean log10 wind and mean scent-bait visit count is **−0.510405**; site-level forest cover / background bee abundance are confounders, n=9 is small, and this is not a between-site causal estimate or a p-value. The direction difference is consistent with the original 2020 report.

### Statistical interpretation boundary

The 95% intervals above are **model-based**, not bootstrap confidence bounds with independent site/day random effects. The original study observed natural wind variation, NOT randomly assigned wind and odor; no no-scent flowers, no flower landing, pollen deposition, seed set or evolved floral scent amount are recorded. The relevant outcome is arrival/collection of MALE Euglossini at artificial fragrance bait for perfume collection. This is an ecological example of wind-associated access to an olfactory source, not direct evidence of increased natural floral pollination.

Therefore:
- A positive temporal wind–scent-bait arrival association is supported by this source.
- The claim "flowers with higher natural VOC emission benefit more from wind" remains **a testable cross-source hypothesis**, not a 2×2 interaction estimated here.
- A wind-related increase in visits must NOT be translated into an increase in legitimate flower entry or fruit/seed fitness.
- The visit-level 450 bee rows are not an independent n; inferential replication is 70 sessions, conditional on nine sites and with 29 dates.

## Direct computation and reproducibility

Code: audit_original_session_design.py (source identity/joins + author R model references); conditional_site_poisson.py (independent conditional Poisson optimizer, site leave-one-out, cineole sensitivity, model-based and quasi-Poisson CI); independent_statsmodels_check.py (second GLM solver and clustered sensitivity pending final CI), two source-free regression suites. Original Zenodo archive is downloaded into a temporary GitHub runner environment, never added to Git and never uploaded in artifacts. The numerical receipt is aggregate JSON only.

Dedicated workflow: floral-stage36-crall-session.yml.
Original first refit success: https://github.com/zuizui0223/adaptive-gain/actions/runs/43696348023.

**Current gate:** final commit (adding independent Statsmodels solver and quasi-Poisson CI) is only accepted once its workflow on its exact SHA succeeds. Full Python 3.10–3.12 repository CI is a separate gate. Draft stacked on Stage35, not merged.
