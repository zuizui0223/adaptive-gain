# Stage71 | Corrected real-visitor flower census audit, outcome-blind native network frame, original UV–bee composition stress test

**Status 2026-11-17 JST:** original-source GitHub Actions [flower counts 44073758223](https://github.com/zuizui0223/adaptive-gain/actions/runs/44073758223) SUCCESS; original-source [native×identified-bee analysis 44075425920](https://github.com/zuizui0223/adaptive-gain/actions/runs/44075425920) SUCCESS. Draft stacked on Stage70 PR #149. No changes to `main`. **This is an exploratory observational result, NOT an evolutionary selection effect, true native-population status, measured site-specific UV guide, or causal mediation SEM.**

## Essential methodological correction before opening guild outcomes

Stage69B's 156-network screen required at least one *Bombus* and another visitor group in the same network. Stage70 then retained 73 conservative and 135 repaired-geometry networks from that **outcome-dependent sample**. Those networks are useful for proving comparison opportunity, but **not an unbiased entry frame for estimating a Bombus proportion association**. We therefore discarded the old 156/73/135 sets as inferential sampling cohorts.

The source-native Stage71B frame is built **before using any guild outcome**:

1. Start with 73 original 2024 **botanical-garden** real 300–700nm petal spectra and authentic, corrected [EuPPollNet v1.3.0](https://github.com/joseblanuza/EuPPollNet/tree/v1.3.0) 623,476 observed visitor-event records.
2. Of 2,557 original optical-plant × network/year units across 36 original spectrometer species, retain the **685 networks** with ≥2 distinct source-measured spectrometer plant species (not conditioned on bee guild). This still conditions on plants having at least one visitor record, so it is a **recorded-visitor** cohort rather than a full flowering community occupancy denominator.
3. Match exact WCVP source native Level3 and original field coordinates to original valid TDWG polygons. Only require ≥2 accepted native-region-compatible taxa with distinct original mean UV values and different genera. No original bee counts used. The conservative outcome-blind **primary frame has 452 networks / 35 study IDs / 28 optical taxa**. Historic invalid-polygon repair, *separately labelled*, gives **625 / 41 / 29**. Source 19 original invalid geometries are not silently promoted into primary.
4. Open source original event records only after freeze. Count **plant species-ranked** and **pollinator species-ranked**, non-affirmative unsure-ID, actual original *Bombus* genus versus other recognised bee families, no syndrome imputation. Network-level nonrecording is **not a biologically verified guild absence**. Without any species-rank bee records for a plant, its observed guild share is unobserved.
5. The optical predictor is original **single-garden-species mean 300–399nm petal reflectance in percent**. It is not an ultraviolet bullseye, nectar guide, field population signal, wind plume or bee colour-contrast computation.

## Independently audited floral-census denominator

The authentic original author `Flower_counts.csv` is **199,692 flower-census rows** (source Git blob SHA1 `8543e446a53f3b7cffece76e1699489e7169f7fd`), from the corrected original v1.3.0 release. Original visitor rows marked `Flower_data=Yes` number **550,346**, but this is metadata availability, **not 550,346 verified per-flower exposure denominators**.

The original source counts use a heterogenous mixture of percent cover, flowers/m², inflorescence/reproductive units, quadrat or transect counts, species-site mean flowers and other units; numeric zeros and missingness must remain distinct. The original file has 199,624 unique Study_id × Flower_data_merger keys (68 doubled keys) and many keys that represent site, not unique plant species. Among **2,557** original optical plant×network/year units:

| Primary-source exposure class | Plant×network units |
|---|---:|
| One single positive numeric count with labelled unit, but field/species comparability not yet established | **808** |
| Shared source join key among multiple plant names | **901** |
| Multiple original source flower-count keys requiring time alignment | **391** |
| No single valid positive count with unit | **457** |

These sum to 2,557. Exact original census-key taxon concepts and temporal matching remain unverified even for the 808. **NO globally comparable, source-validated per-flower visitation rate can be computed from the original unstandardised flower counts at present.** Source audit [Actions 44073758223](https://github.com/zuizui0223/adaptive-gain/actions/runs/44073758223), artifact **14323972293**, SHA256 `3795586c97344ff565782b908e4d0df5836df1759f73f2d8fb4226dea5f8acb3`.

## Outcome-blind network and identified bee data quality

- Main 452 source-native-compatible networks: 405 contain any strict accepted species-ranked bee observation and **314** have ≥2 native source optical plant species each with ≥1 strictly identified bee record; **155** with ≥3 each.
- Repaired-geometry 625 networks: 573 contain any source bee, **457** have ≥2 such plants each with ≥1 record; **218** with ≥3.
- Potentially informative within-network *Bombus-vs-other-bee* contrast depends further on detecting both groups in that network and distinct UV values among bee-recorded plants. These **post-freeze information checks are not entry criteria**. The original-source raw event audit excluded **476** insufficient pollinator-rank Hymenoptera records and **337** affirmative pollinator identity-uncertain Hymenoptera records from the strict bee contrast. These are source events, not independent biological replicates.

## Exact ecological source score and sensitivity

We pre-specified and implemented a **network-intercept binomial null score**, with one source optical species observation per plant in each network:

\[
S_k=\sum_{i \in k} (B_{ik}-N_{ik} \widehat p_k)(x_i-\bar x_{N,k}),\quad
I_k=\widehat p_k(1-\widehat p_k)\sum_{i\in k}N_{ik}(x_i-\bar x_{N,k})^2,
\quad \widehat p_k=\frac{\sum_i B_{ik}}{\sum_iN_{ik}},
\]
where \(B_{ik}\) counts recorded *Bombus*, \(N_{ik}\) counts all strictly identified bee events, and \(x_i\) is the original measured garden UV mean in units of **10 percentage points**. Networks with only one recorded guild, fewer than two bee-observed plants or no UV variation contribute zero inferential information (rather than imputed biological absences). The ratio \(\sum_k S_k/\sum_k I_k\) is **only a first-order local score approximation around logit coefficient zero, not a fitted regression beta, confidence interval, odds ratio, p-value or causal effect**.

Results from [source Actions 44075425920](https://github.com/zuizui0223/adaptive-gain/actions/runs/44075425920), original source-level reproducibility:

| Original-source population and informational rule | Informative networks | Study IDs | UV null-score / null-information ratio | Study leave-one-out sign flips | Species leave-one-out sign flips |
|---|---:|---:|---:|---:|---:|
| **Conservative 452**, each plant ≥1 strictly identified bee event | **93** | **22** | **+0.8468** | 0 | 0 |
| Conservative 452, each plant ≥3 strict bee events | 46 | 16 | +1.0436 | 0 | 0 |
| **Geographic repair 625**, each plant ≥1 strict bee event | **186** | **27** | **−0.0179** | 2 | 5 |
| Geographic repair 625, each plant ≥3 strict bee events | 99 | 22 | +0.0300 | 6 | 5 |

These values are sensitive to study source composition. One major transparent decomposition:

- The 93 conservative informative networks are *exactly contained* in the 186 repair-sensitive informative networks with unchanged within-network scores. No original informative network is lost.
- The 93 additional informative networks come from **six distinct study IDs**. Their source null UV score is **−54.2214** with information **92.9104**; the conservative subset has score **+51.4630**, information **60.7717**. Combined score ≈−2.7584, information ≈153.6820.
- The original additional negative contributions include `19_Jauker` (−59.6157 across 26 networks) and `21_Hopfenmuller` (−16.2454 across 15); positive added source `39_Schweiger` (+19.2426 across 25). This is **study-composition heterogeneity**, not proof that geography itself causally reverses floral signals.
- Source visible-reflectance marginal null-score ratios are **−0.9429** conservative and **−1.0514** repaired; the exploratory two-axis UV score adjusted for visible is +0.5271 conservative and −0.1298 repaired. These, too, are null-local approximations **without source phylogenetic or floral-abundance correction**, and their sign discordance is not evidence of causal optical trade-offs.

**Interpretation:** The apparent positive optical association in the conservative, accidentally geography-restricted cohort **does not survive** the alternative, source-preserving correction of historic invalid botanical polygons. Therefore a general positive *Bombus* preference for higher garden-measured UV petal reflectance is **not established**. The 17/27 repaired-sensitivity study scores that are positive do not resolve this, because studies share plant species, community composition and effort designs. The data also cannot identify within-species optical effects: `x_i` is **species-constant** and would be exactly absorbed by species fixed effects. No valid confirmatory p-value/95% interval was computed.

## Biological interpretation ceiling and next main data requirement

- This is **European** source observation rather than global optical signalling ecology; EuPPollNet has no bird-mediated network guild in this sample.
- Original 2024 garden petal UV spectra are not field-local measures, actual spatial UV nectar guides or bee receptor-specific contrast; floral VOC and atmospheric wind are not source-coincident.
- Genus/family/phylogenetic shared history and spatially covarying environment remain unadjusted. Each species may recur across dozens or hundreds of network years; 186 source networks are not 186 independent floral phenotypes.
- Observed bee visit counts reflect sampling design and floral abundance. Even conditional bee proportions can depend on floral abundance, taxon detectability and the sampled guilds. The original flower census cannot supply a standardized global denominator.
- Direct pollen transfer, plant reproduction and true mate fitness are unavailable; **do not claim selection, information value or adaptive nectar-guide loss**.

The next scientifically informative step is **to acquire actual field-site, co-temporal plant optical traits and documented visitor guild records** from independent original sources, including multiple regions and both positive and verified negative spatial UV-guide states. Validate native area, plant species concept, sampling unit and method before incorporating wind and fragrance. A secondary explicitly labelled exploratory analysis could compare study-heldout predictive accuracy, but no more regressions on the same garden-spectra observational proxy should be promoted to confirmatory ecological evidence.

## Source/implementation

- `research/floral_literature_macro_stage71/audit_original_flowers_sampling_exposure.py`
- `research/floral_literature_macro_stage71/build_outcome_blind_native_visitation_cohort.py`
- `research/floral_literature_macro_stage71/compare_original_uv_vs_identified_bees_null_score.py`
- **15 source-free tests total**: 5 flower-count, 3 outcome-blind cohort, 7 null-score guards, verified in the two Actions above. All source-native bytes SHA locked in the source scripts.
- [Stage71A author flower census workflow](../.github/workflows/floral-stage71-original-flower-exposure.yml) and [Stage71B/C outcome-blind source native guild workflow](../.github/workflows/floral-stage71b-unselected-native-bee.yml).
- Full Stage71B/C result artifact **14324287258**, digest `sha256:02323cb8e39cc6f601d0cae9a23b634991a69b1965c41685bea2a3d449dcc6e1`.

This is a falsifiable *observational limitation* result and an audited study-design finding, not a failed search to be rerun with progressively relaxed selection rules until positive.
