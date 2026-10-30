# Stage12 frozen real original-source response: wind × co-occurring other-pollinator fraction

**FROZEN 2026-10-30 AFTER native source-only metadata/behavior-count QA, BEFORE any biological Stage12 regression output.** This is exploratory secondary analysis of Harris et al. 2026 original field observations, not independent biological replication of Stage11.

## Fixed source and actual biological grain
Harris et al. 2026, Functional Ecology DOI 10.1111/1365-2435.70429; Dryad DOI 10.5061/dryad.9kd51c608 v456836 original provider SHA256 pinned to Stage11. Native source: 1,227 60s honeybee observations across 123 surveys; original weather for 122 surveys; original insect community 123 single-survey snapshots.

The **source-only** gate (CI 41034949444) passed six synthetic grain tests and exactly verifies 113 eligible original surveys, 1,130 original 60s records, 10,026 recorded flying movements and 6,652 walking movements, 16,678 events total, 18 native plant labels, 73 city×date clusters, 2 UK cities. This is NOT 16,678 independently sampled animals. Original non-honeybee taxon categories: 34; H is observed non-honeybee *proportion of counted insects* at the SAME survey, not an individual animal's observed cue.

The original 10 survey exclusions were fixed based on native source grain alone, before any regression: 8 insect-survey label/date metadata mismatch (C2/C3/C5/C9/N1/N4/N6/N8); 1 missing weather (N24); 1 impossible original `number of flights=-6` (N51), entire survey excluded rather than editing or dropping just one row. Seven mismatches are native forage `Prunus spp.` vs insect `Prunus avium`, not proof of different flower plots; C9 has an unresolved date/metadata issue even though plant/location labels agree. Do not guess metadata repairs. The 1,227-row first-source counts include legitimate repetition; source source-grain aggregator prevents cross-table joins multiplying behavior rows.

## Why we must NOT use a naive binomial logit fit
Source-only QA found 11/113 original surveys with **zero walking** and 4/4 `Borago officinalis` surveys exclusively record flights, which risks complete/quasi-separation in an unpenalized plant-fixed-effect binomial GLM. Avoid post-outcome model fixes by freezing a survey-equal descriptive log-ratio regression using a fixed half-event continuity correction. No source effects inspected to make this choice.

## ONE primary estimand; no alternate selection
For each surveyed patch i, let F_i be the total *recorded flights* and L_i the total *recorded walks*, aggregated over valid 60s observations in that survey.

**Response:** `y_i = log((F_i+0.5)/(L_i+0.5))`. This is a conditional allocation between two *recorded inter-flower movement types*, not the absolute number of visits and not an individual fitness outcome. The 0.5 correction is fixed across ALL surveys and eliminates undefined zero-walk log-ratios; do not tune.

**Covariates:**
- `w_i = mean native ordinal Beaufort_i − mean native ordinal Beaufort within same plant`. Ordinal wind is NOT metres per second.
- `h_i = (nonhoneybee_count/(nonhoneybee_count+honeybee_count) − within-plant mean share) / s_h`, where `s_h` is the pooled sample SD of the within-plant deviations (all **eligible** surveys). Categorized insect records are not actual richness or direct sensory interactions.
- `w_i*h_i`: **only primary cross-factor term**.
- Original plant identity fixed intercepts, city fixed intercept, mean original temperature, blue-sky fraction, sin+cos of actual source calendar DOY /365.25, log(1+observed flower density).
- All survey rows weight **one survey equally** (no event-count pseudo-replication), original city×date is cluster. OLS via fixed QR / normal-model sandwich. CR1 `G/(G−1) * (n−1)/(n−p)` cluster error, two-sided t test with `df=G−1`, 95% t interval, same implementation as Stage11. Numeric independent statsmodels verification.

`y_i = plant FE + city FE + beta_w w_i + beta_h h_i + beta_wh w_i h_i + beta_T T_i + beta_B blueSky_i/100 + beta_s sin(2π DOY/365.25) + beta_c cos(2π DOY/365.25) + beta_D log(1+density_i) + epsilon_i`.

**Primary:** `beta_wh` = association between co-survey other-insect fraction and wind-dependent log flight/walk ratio. H0: beta_wh=0. A positive/negative value describes an allocation shift conditional on plant, city, season and weather — NEVER evidence that honeybees **observe or use** a heterospecific cue or benefit in fitness terms. Wind and the insect composition are simultaneously observed, and wind itself may affect other insects; causal mediation and selection are not identified.

**Secondary, diagnostic only:** model conditional wind slopes at h=-1,0,+1 with same model and covariance, not three new primary tests. No city/taxon/model search following initial output; no alternative reward interaction and no subset re-tuning.

**Strict numerical / support NO_GO:** number of source-eligible surveys >=80, number of distinct city×date clusters>=30, exactly 2 source cities, design matrix full column rank, residual df>=40, finite and nonzero within-plant other-share SD. If any fail, do not modify frozen spec to rescue. All original 113 eligible surveys go into the same main model. No individual IDs or new wind experiment invented.

## Execution protocol
Implement in own Stage12 module; use existing tested Stage11 QR/CR1 helper and a new independent statsmodels comparison, plus synthetic small cases for log ratio, survey identity, rank and no-outcome leakage. Run source-gated CI where the real original archive checksum is checked again before scoring. The first real-source model result, whether positive/null/negative, is frozen and machine-readable; save source QC+model receipts and report limitations. No changes to Stage9b/Stage10/Stage11, frozen theoretical V5/V6 or main.
