# Stage12: Wind, co-occurring pollinators and between-flower movement mode

**2026-10-30 | ORIGINAL SOURCE VERIFIED | Primary wind×heterospecific-share hypothesis: NOT SUPPORTED**

## Central result
Among 113 actual original field surveys, the **wind × non-honeybee proportion** association with the *flight-vs-walk interflower movement log-ratio* is **+0.05349643** (city×date cluster CR1 SE 0.09452659, 95% t interval **[−0.13493888,+0.24193174]**, two-sided **p=0.57319387**). This does not support the prespecified observational interaction; it does not prove equivalence or that bees fail to use heterospecific cues.

At average within-plant non-honeybee share, the fixed secondary conditional wind slope is **+0.13105552** (95% **[−0.00920010,+0.27131114]**, nominal p=0.0665838). At −1/+1 SD of non-honeybee share slopes are +0.07755909 and +0.18455195, whose intervals also include zero. These are unadjusted *secondary conditional estimates* of the same model, not tests to substitute for the primary null. There is no demonstrated increase in flight share with wind.

**Interpretation must stay bounded:** Observed non-honeybee counts across an entire survey are **not cues demonstrably perceived by a particular honeybee**. Wind and co-occurrence are both observational and may be causally linked. This dataset identifies neither cue-acquisition order, intent, fitness advantage, honeybee colony independence, nor adaptive information routing. The study was conducted in relatively favorable weather (<10 km/h wind in the original authors' protocol) and cannot resolve strong-storm behavior.

## Original source and three distinct denominators
Harris, Ratnieks & Balfour (2026), *Functional Ecology*, DOI 10.1111/1365-2435.70429; native Dryad 10.5061/dryad.9kd51c608 version 456836. Three used author-original tables pinned to published provider SHA256:
- forage.csv `c5bb7b67780b8749014cb645fa43fc35bc1ffe8a4b1c8edcb5637d07a5146f61` (1,227 original 60s behavior rows / 123 original surveys)
- weather.csv `c7b09eaef978b4bc8bbd6bf093c2872130c8a6038ec206a4f36fa365896a9641` (127 native readings / 122 survey IDs)
- insect_surveys.csv `f0f899655d671f311f47100745790ae8618b57777a9cd8e5a35f0d0854619ee3` (123 community records / 123 survey IDs)

**Main eligible sample**: **113 original surveys** (NOT 1,130 independent trials and NOT 16,678 independent bees), **1,130 observed 60s behavior records**, **10,026 original flights and 6,652 original walks = 16,678 source movement events**, 18 native plant labels, 34 non-honeybee taxon *categories*, 2 cities and 73 city×date clusters. Source community other-insect fraction spans 0–0.85, SD of within-plant deviations 0.1664644083.

All survey exclusions fixed based ONLY on source/measurement checks, before fitting a Stage12 effect:
- 8 source metadata mismatches: C2/C3/C5/C9/N1/N4/N6/N8. Seven are behavior `Prunus spp.` versus insect survey `Prunus avium` (same dates/sites, but unequal taxonomic resolution), and C9 has another source date/metadata disagreement even though plant/location labels match. No species upgrade or guessed date fixes.
- N24 missing original weather.
- N51 original original-behavior CSV has **exactly one impossible negative flight count −6**, source index 902. Complete 1,227-record audit found no other nonfinite/nonintegral/negative movement count and no record where flights+walks exceed flowers probed. The entire N51 survey was quarantined, rather than imputing −6 or silently dropping just that row; explicitly frozen in the pre-outcome amendment.

Unlike Stage11, C52 (author-imputed nectar) remains in Stage12 because original nectar is **not a predictor or response** here. The Stage11 114-survey and Stage12 113-survey denominators therefore cannot be treated as identical or pooled without reconciling inclusion. Each original weather and insect record was matched at **survey grain**; repeated behavior or weather recordings were never multiplied by a many-to-many join.

## What is directly measured
The author source records `number of flights` and `number of walks` between flowers for individual 60s honeybee observations. The dataset has no persistent animal ID (the 1,130 rows are observations, not unique tagged bees) and no full flower availability set. The observational category of insect co-occurrence is counted at the survey level, not paired moment-by-moment with a particular honeybee flight.

Source QA showed 11/113 original surveys with zero walking (all four Borago officinalis surveys are flight-only); hence an unpenalized binomial model with plant fixed effects risks separation. Before any effect output, the only model was frozen at **one survey per row, equal survey weight** and
`Y_i = log((source_flights_i + 0.5)/(source_walks_i + 0.5))`.
The uniform +0.5 continuity correction was frozen before scoring. It is an observed movement-allocation log ratio, NOT a raw flight probability and NOT an experimental effect.

Within each source plant, Beaufort wind and co-survey non-honeybee fraction were centered; the fraction was additionally scaled by pooled within-plant SD. The only primary cross-factor was wind×nonhoneybee share. Plant fixed effects, city fixed effect, temperature, blue-sky fraction, sin/cos DOY, and log(1+flower density) were included. All 113 eligible surveys were assigned equal weights, and the city×date CR1 cluster covariance used finite-sample correction G/(G−1)·(n−1)/(n−p) with df=G−1=72. Design rank 27/27, residual df86, 73 independent *date-by-city error clusters*.

## Numerical receipt
| Target | Coefficient | 95% interval | p | Claim tier |
|---|---:|---|---:|---|
| Wind×non-honeybee fraction, within-plant | +0.05349643 | −0.13493888 to +0.24193174 | 0.57319387 | **Only prespecified primary** |
| Wind conditional at other fraction −1 SD | +0.07755909 | −0.10876200 to +0.26388018 | 0.40938877 | Descriptive only |
| Wind conditional at average other fraction | +0.13105552 | −0.00920010 to +0.27131114 | 0.06658378 | Descriptive only |
| Wind conditional at other fraction +1 SD | +0.18455195 | −0.09048162 to +0.45958552 | 0.18522187 | Descriptive only |

The response is **log flight/walk**, not log(1+flower visit rate) as in Stage11. Comparing coefficients directly across Stage11/12 is invalid. Wind is original *ordinal Beaufort* rather than measured m/s. Non-honeybee fraction is a count of other insects among counted insects, not experimentally exposed social signals or independently standardized species richness.

## Source integrity, code QA, and STOP
- [Stage12 source-only grain QA 41034949444](https://github.com/zuizui0223/adaptive-gain/actions/runs/41034949444), source hash verification, native count diagnostics, six synthetic source QA tests, **SUCCESS**.
- [First frozen actual Stage12 association 41035508706](https://github.com/zuizui0223/adaptive-gain/actions/runs/41035508706), native original file hashes and ten focused synthetic data/model tests **SUCCESS**; full result artifact includes derived one-survey-per-row cohort and model result, no raw individual animal event rows committed to Git.
- QR/CR1 calculation compared directly with statsmodels clustered OLS on the **actual 113 survey rows**: max coefficient disagreement 2.01e−14, max covariance 4.33e−13, primary p 6.22e−15. This verifies computation, not biological independence.
- No sample/model/parameter search is authorized after observing the null. Original impossible N51 flight count is not repaired; future corrected source version would require separate analysis with a new frozen protocol.
- This draft is stacked on Stage11 and remains distinct from unmerged Stage9b/10, frozen V5/V6 and main. No merge, submission or new animal experiment.

**Research decision:** Current original data support wind-associated changes in visitation performance and guild composition in other settings, but Stage11 (wind×nectar, null) and Stage12 (wind×co-occurring insect fraction for movement-mode allocation, null) do not reveal adaptive cue-use mechanisms. An actual randomized cue-order × wind experiment with real per-bee route sequence, simultaneous available alternatives, and measured reward/handling remains necessary for the target theory.
