# Stage 3g — original Pan flowering-family composition × FIT wind/guild association (2026-10-28)

**Status:** Completed original-data exploratory/post-hoc analysis. The previously observed relative bumblebee-to-other-fly FIT visit association under strong wind **persists unchanged after adjusting a botanical family-composition summary** from the neighboring Pan flowering-plant inventories. The three family-composition terms do **not** show a detectable joint association in this model: **3-df Wald p=0.82221**. This **does not** show zero ecological influence from other plants or causal wind effects.

## Code, source, execution receipts

- [Source-controlled GitHub Actions original-data run 40528449499](https://github.com/zuizui0223/adaptive-gain/actions/runs/40528449499): **SUCCESS**, 25 original-source, join and modeling tests passing; both `POMS_PAN_JOIN_AUDIT_COMPLETE` and `POMS_PAN_FAMILY_MODEL_COMPLETE` logged.
- Protocol [PROTOCOL_STAGE3G_FAMILY_COMPOSITION_2026_10_28.md](PROTOCOL_STAGE3G_FAMILY_COMPOSITION_2026_10_28.md) committed **before** inspecting Stage 3g source-family covariate model outputs. The earlier positive wind–guild finding that motivated Stage 3g was observed beforehand; these are **not independent confirmatory results**.
- PoMS pan trap flowering original files (2017–2023): DOI https://doi.org/10.5285/5841bfae-471b-498c-af89-c30e5140d6c5; station CSV SHA256 `70f3429e5ed9022d3d7b80fc3f24c589ecc5faff608393bc53febfac49788277`, flowering occurrence CSV SHA256 `53daa167282092b7081190de00e020b4e2635fa5e7d4fc63d3454f7c338951ba`.
- PoMS structured FIT (2017–2023): DOI https://doi.org/10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618; exact 1km FIT CSV SHA256 `29d3deb757c053774c26ece0a7683081a4b4fe81d9497877fe1179f232182e52`.
- All original source microdata were read inside CI only, not committed. 11 orphan Pan flowering occurrences without parent station remain quarantined and explicitly reported.
- **Every FIT survey remains one unique observation** after strict `location_code × x1km_square × date` administrative linkage to five Pan stations. The same Stage 3f 2,210 paired positive FIT surveys from 95 structured sites are required for both models; all source, key, rank and no-imputed-absence gates passed.

## How botanical families were selected without using insect counts

Among **all original five-Pan-station site-days with one or more labelled flowering plant taxa**, choose the top three taxonomic *families* in descending order of **distinct Pan site-day presence**, breaking ties lexicographically. Presence of one taxon in multiple Pan stations is counted only once per site-day. Native source taxon version keys determine identities; if two nonmissing family labels conflict for one taxon identity, code fails closed. Missing family names are left in the denominator, not guessed from genus. The independent original-data source-only selection yielded:

| Botanical family | Pan 5-station site-days with family present | Independent source Pan sites | FIT sites with within-site fraction variation |
| --- | ---: | ---: | ---: |
| **Asteraceae** (キク科) | **844** | 87 | 78 |
| **Rosaceae** (バラ科) | **705** | 81 | 71 |
| **Ranunculaceae** (キンポウゲ科) | **613** | 84 | 73 |

The additional source-only distribution (not model-guided selection) includes Fabaceae (557 site-days), Caryophyllaceae (406), Plantaginaceae (365), Apiaceae (333) and others. All three selected families exceed the predeclared >=50 Pan site-days, >=10 original Pan sites and >=10 FIT sites with within-site variation.

Per Pan site-day, for each selected family use `(# distinct recorded Pan flower taxon labels in that family) / (# all distinct recorded Pan flower taxon labels)`, including unknown-family source taxa in the denominator. **Do not sum botanical floral-unit abundance between plant species; the source floral-unit categories differ.** In the 2,210 FIT pair-positive context surveys, Asteraceae has median fraction **0.1429** (25th–75th 0–0.2857), Rosaceae **0.0769** (0–0.1667) and Ranunculaceae **0** (0–0.1429).

## Fitted observational comparison on exactly matched surveys

Response is the previous grouped-binomial `[bumblebees, other_flies]` **recorded visit composition**, conditional on ≥1 paired-group visit in a ten-minute **single-target-flower FIT census**. The baseline retains all Stage 3d controls: categorical wind, target flower identity, floral-unit count/type, year, season spline, sunshine, time of day, observer ID familiarity class, flower cover, site fixed effects, and **log1p(Pan site-day richness)**, with covariance clustered by structured 1km site. The only extra terms are the **three source-selected family fractions**. No wind×family interaction is tested, no botanical species is reselected based on insect outcomes.

| Quantity | Stage 3f richness baseline, same 2,210 FIT surveys | Stage 3g richness + 3 family composition fractions |
| --- | ---: | ---: |
| **Strong wind vs calm bumblebee/other-fly OR** | **1.9102** | **1.9117** |
| **95% site-cluster CI** | **1.2600–2.8959** | **1.2611–2.8979** |
| Model design columns / rank | 140 / 140 | 143 / 143 |
| Pearson residual dispersion | 2.759 | 2.765 |
| **Joint family fraction 3-df Wald** | Not in baseline | **chi2=0.9133, p=0.8222** |

All fitted models converged. Each family coefficient's descriptive per-25%-share point-estimate and 95% site-cluster CI (without between-family multiplicity correction, so **not** a discovery claim):

| Source family | OR per +0.25 family fraction | 95% CI |
| --- | ---: | ---: |
| Asteraceae | 1.016 | 0.818–1.262 |
| Rosaceae | 0.971 | 0.712–1.324 |
| Ranunculaceae | 0.882 | 0.653–1.191 |

The three-family joint p-value is the declared source-adjustment test, not any of the individual nominal p-values. Both designs are full rank and the declared wind and family fraction covariance/intervals are finite. **Eight unrelated nuisance fixed-effect confidence-limit cells are nonfinite** in the fitted designs, so those nuisance coefficients must not be interpreted as resolved ecological effects. In-sample results cannot be called out-of-sample predictive superiority, especially after a series of post-hoc analyses.

## What this result can and cannot mean

**Supported, precisely:** the previous conditional wind–bumblebee/other-fly observed visit composition association is not explained away by the **recorded number of Pan flowering plant taxa or the fractions from the three most frequent source Pan botanical families** in the same administrative 1km grid on the same date, after many observed FIT controls. The family fractions offer no detected *joint* mean association in the declared model.

**Unsupported:** this is *not* evidence that surrounding plants have no effect on pollinator behavior or that wind affects pollinators independently of actual plant choice. Source Pan flowers are recorded within 2 metres of **different Pan station locations**, FIT counts visits to one investigator-selected 50×50cm floral quadrat for ten minutes. No simultaneous flower availability, pollen transfer, individual sensing, flight direction, insect competition, causal trophic cascade, reproductive success or adaptive routing `C_A,C_F` is identified. Pan botanical family and site-level composition may miss functionally relevant finer traits and microhabitat variation.

**Stopping rule for this line:** Stage 3e (coarse open/closed morphology) and Stage 3f (Pan richness interaction), and now the Stage 3g source-selected **family composition** test did not establish those specific proposed effect modifiers. Do **not** add a fourth/fifth post-hoc family or retrospectively search genus/plant subsets for a small p-value. The priority has shifted to independent actual floral-option availability and within-individual pollinator observation (preferably randomized wind/cue acquisition), rather than further significance-seeking using the same PoMS programme.

### Attribution
UK Pollinator Monitoring Scheme and original EIDC datasets/volunteer contributions (DOIs above), with funding by UKCEH, JNCC, Defra, devolved Governments/DAERA and NERC. Retain original publisher source references and the Open Government Licence in any derivative paper.
