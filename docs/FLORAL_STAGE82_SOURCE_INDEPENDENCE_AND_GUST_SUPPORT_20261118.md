# Stage82 — Distinguishing original publication replication from plant trait replication

2026-11-18. **Original source falsification audit, not a confirmed floral cue-order or selection effect.**

## Existing measured source result

Ohashi et al. 2015 spectrometer source (Japan) contains 1,360 genuine sample worksheets for **28 strict botanical-name-matched source taxa**, in **53 early/late flower-part comparisons**. The corrected European EuPPollNet source contributes 18,798 plant-network-year rows. Freeze botanical comparison eligibility before checking bees: 537 networks with >=2 of the 28 measured taxa. Exactly **194 networks from 30 original publications** contain species-ranked *Bombus* and other bee information and a nonzero local null score. However only **23 of those 28 taxa** occur in the informative 194 networks.

The initial author-original local zero-effect score ratio for species-level early/late RAW spectral RMS was **-0.9883059**, with original publication-cluster bootstrap interval **[-2.181833, -0.525732]**. This is NOT a fitted binomial coefficient or a bee-receptor colour difference. The largest original paper alone supplies **51.20%** of source null information and the effective independent source-paper count is **3.353**.

## New Stage82 source independence diagnostics

The code re-reads only SHA-authenticated original EuPP 18,798 network rows and Stage81B original 53 flower-part summaries. It re-estimates source scores from raw cross-species observed counts rather than removing only points after estimation.

| Predefined source check | Result |
| --- | --- |
| Information-weighted 194-network local source score | -0.9883 |
| Original publication equal arithmetic mean of paper U/I scores | +2.3363; bootstrap [-1.5910, +9.7237] |
| Remove *Trifolium pratense* and recalculate all remaining networks | -0.4825; 93 networks/19 papers; interval [-1.2267,+0.3589] |
| Remove all *Trifolium* and recalculate all remaining networks | -0.4966; 39 networks/12 papers; interval [-1.5583,+0.4038] |
| Shuffle the 28 species-level RAW age-RMS labels 9,999 times while preserving true original bee counts | two-sided descriptive tail proportion **0.1747**; null 95% [-1.2736,+1.2965] |

**Both sample units matter.** The original paper bootstrap leaves repeated species traits unchanged even though the same plant occurs hundreds of times in field networks; the original taxon-label shuffle asks whether the apparent effect is unusually aligned with botanical taxa, and the answer is not compelling. But shuffling is **not phylogenetic exchangeability** and its value must never be advertised as a valid plant-evolutionary hypothesis p-value. The equal-paper mean of per-paper U/I is also unstable when papers have tiny Fisher information: its opposite point direction is a sensitivity warning, not evidence for a reverse ecological effect.

## New real ERA5 × flowering-age optical cohort support

The source-original Stage79I gust panel is the 151 network-years selected by original petal WIDTH and study-site/date coverage, not by gust or bee outcome. It is independently joined to original Stage81C's 194 age-spectral × strict-bee network scores on exact source Study_id/Network_id/Year. SHA checks lock both derived source CSVs.

- Match: **36 network-years**, **17 source study IDs**, **16 genuinely distinct publications**.
- **Seven** publications show at least one percentage point difference in fraction of ERA5 days with daily max 10 m gust >=15 m/s within original publication.
- Largest source publication supplies **84.42%** of null information. Information-equivalent number of publications only **1.3873**, even with 16 labels.
- Study-ID fixed effects + original 151-network weather-frame temperature/precipitation standardization; publication-clustered WLS score ratios per 10 percentage points of strong-gust days:
  - original Fisher-information weighted **+0.5997**, descriptive 95% interval **[-7.3364,+8.5358]**, two leave-one-paper sign flips;
  - source-publication equal information normalized **+6.9563**, interval **[-1.2355,+15.1480]**.
- Both intervals include zero; the **wind × age-spectral source effect is NO-GO** for macro inference. Neither number is an estimated bee sensory route, color-change effect, causal coefficient, fitted binomial beta or plant fitness coefficient.

ERA5 source periods are based on months in which visitor events were recorded; true sampled hours, odor plume, flower movement, actual floral age at visits and flower-specific gust speed were NOT measured. Japan spectrometer and Europe field records are separate populations. Floristic abundance and detection are not standardized for this combination.

## Next evidence admission

Ohashi et al. already distinguished distant green receptor contrast and close chromatic colour contrast, so this is prior art. Stage81D is designed to independently reconstruct hypothetical Apis D65 green-foliage-adapted photoreceptor and bee-hexagon contrasts of the true 28 matched taxa. It must not be misrepresented as species-specific Bombus physiology, an effective nectar guide, recognition distance or actually measured bee learning.

Only after genuine green and chromatic source traits have been verified and positive *and measured negative* flower-age shifts classified should they enter subsequent cross-guild network analysis. True ordered acquisition, scent dispersion and wind-driven landing risks additionally require compatible behavioural/environmental measures. No missing traits or field visitor records are reinterpreted as biological zero.

## Reproducibility

Original EuPPollNet source SHA256 475863c2b193dd9c1eaad848dae05a9f518b57446cad2661979ca582c7d88617. Ohashi derived 53-part source SHA256 bb8c7d497bf2e0fcea267aa88c685fdd87f475fd25b9d062b2011556819aa804. Stage79I survey-year gust exposure CSV SHA256 1188e639593437f07c8eaa559730d845269d9b1d2abca52917b7bbd6c2315f90. Stage81C real 194-score CSV SHA256 ddc3d56e536b34e7a31f78f0a4f9013739bc732d69c9d294151dec303bcb86ca.

Implementations: research/floral_macro_stage82/source_trait_independence_test.py, source_age_wind_join_gate.py and GitHub Actions real-original-source verification workflow. Derived outputs contain no redistributed original author XLS files.
