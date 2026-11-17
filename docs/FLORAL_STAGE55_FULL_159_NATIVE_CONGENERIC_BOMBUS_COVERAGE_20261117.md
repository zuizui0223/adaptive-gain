# Stage55 — source-original 159 UV plants, native-area congeneric comparisons and modelled Bombus source-guild coverage

Date: 2026-11-17 (JST). Status: **Original-source run succeeded; sensitivity/audit only; no ecological guild-selection or phylogenetic inference.**

## Provenance and executable result

- Stacked draft PR: https://github.com/zuizui0223/adaptive-gain/pull/134 (base PR #133 Stage54, not main)
- Successful original-source workflow: https://github.com/zuizui0223/adaptive-gain/actions/runs/44004224057, commit `cc0d94c07d2827bb87f76e623ac00d6a511c5a6c`
- GitHub Actions artifact ID **14293299351**, name `stage55-159-original-UV-Kew-native-congeners-Bombus-source-HEX-coverage`, ZIP SHA256 **e71deabd244e76b6bd83996a65910ff05e5685f1d1c3abc5b8779de4d75b83ed**.
- The artifact contains complete 159-plant source-exposure CSV, 159 pair-tier rows (61+53+45, overlapping comparisons across tiers), and source-coverage JSON receipt.
- Real source joins: Koski & Ashman (2016, DOI 10.1111/nph.13921) original 159 GBIF-accepted measured-UV species (81 measured UV-uniform and 78 measured UV-patterned); Kew WCVP native WGSRPD L3; Laborieux et al. original author-filtered 10,242 bee HEX (2,695 eligible) and modeled 3,370 bee taxa; 2000–2026 GBIF first indexed page in author northern-mean latitude ±4°.
- Source UV **1 means measured spatial patterned**, **0 means directly measured spatial uniform** in this recoded accepted-species input (the paper's separate raw coding is not assumed equivalent).
- Offline six contract tests and source download/coverage assertions passed.

## Actual botanical/GBIF source coverage

| Original source species | Number |
|---|---:|
| Total measured 2016 GBIF accepted UV species | 159 |
| At least one qualified sampled occurrence in eligible bee HEX | 132 |
| At least 5 qualified plant records and 2 original eligible bee HEX | 106 |
| GBIF API species queries unavailable | 0 |
| Direct native source-site UV+bee observation | 0 (not collected) |

**These are a bounded contemporary GBIF sample, not validated source-site points or the taxa's full native ranges.** The WCVP native L3 botanical overlap makes candidate pairs plausible but does not validate sympatric original photos or localized pollinator exposure. Missing model coverage remains unknown, never interpreted as zero Bombus.

## Non-overlapping opposite-UV congeneric pair results

Outcome = UV-patterned minus UV-uniform plant's **ratio of equal-visited-HEX mean modelled Bombus names / mean all-bee names**. Difference is unit-free, not actual visits, abundance, pollinator behaviour, pollination or fitness. Each row is independent only *within* its tier, and the three nested tiers reuse plants and are not three independent studies.

| Native/author source-match tier | Original candidate pairs | Both plant exposures (>=5 records/2 hex) | Mean pair difference | Median difference | Positive vs negative |
|---|---:|---:|---:|---:|---:|
| Same original genus and overlapping WCVP native L3 | 61 | 30 | -0.0194153 | -0.0014947 | 10 vs 20 |
| Also source lat <=10°, UVB <=1200, temperature <=6°C | 53 | 26 | -0.0033969 | -0.0014947 | 8 vs 18 |
| Also source lat <=5°, UVB <=700, temperature <=4°C | 45 | 24 | +0.0038944 | -0.0014947 | 7 vs 17 |

Alternative stricter sampling requirement **>=15 records, >=3 eligible HEX per plant**: original 61 / 53 / 45 candidate sets yield **20 / 17 / 15** covered pairs; mean fraction differences **-0.0191980 / -0.0068705 / +0.0043325**, medians about **-0.000650 / -0.000784 / -0.000784**. In strict source-climate tier, sample-pair leave-one-out mean ranges **[-0.0186468, +0.0248202]** (5/2) and **[-0.0326682, +0.0387418]** (15/3).

Only **two source genera** contribute to qualified comparisons. In the strict 5/2 tier **22 of 24** pairs are `Potentilla`, **2 `Ivesia`**; a third source genus `Horkelia` contributes one candidate to the two looser candidate sets, but no qualified pair. No phylogenetically independent 24-clade replication is present.

## Independent sensitivity audit of the original artifact

After retrieving and opening the exact workflow artifact ZIP, the **strict tier, 5/2** raw pair CSV was independently recomputed:

- 24 valid pairs: mean difference **+0.0038944**, median **-0.0014947**, 7 positive / 17 negative; raw Bombus taxon-name **mean** pair difference +0.3984, **median** -0.3952 (8 positive / 16 negative). Different metrics are not interchangeable.
- Extremes of the *fraction* paired difference are **-0.4773979** and **+0.5223430**. The two endpoints correspond to species source grid mean **all-bee taxa near 10.36 or 10.62** for a plant in each comparison; such a low denominator can yield a modelled Bombus share near **0.52–0.54**, even though it does not measure actual preferential use.
- **Exploratory, post-hoc denominator-only sensitivity**, requiring >=20 modelled all-bee names *for each plant* reduces to n=20, mean -0.008832, median -0.001948 (4 positive/16 negative). Requiring >=100 names for each plant leaves n=14, mean -0.000681, median -0.001948 (2 positive/12 negative). These are diagnostics, not registered hypothesis tests or independent confirmation.
- Thus the global pair-mean sign depends on climate tier, sampling coverage, denominator and influential pairs. The near-zero median is more stable, but this is not formal evidence for an ecological null.

## Scientific judgment and hard stop

The previous Stage52 60-source-plant descriptive pilot's raw +0.04804 Bombus/all-bee fraction contrast attenuated to +0.01115 under 12 post-hoc same-genus/climate matched pairs, sign-fragile. The **new non-posthoc-outcome-selected 159-source-plant audit provides no directionally robust positive UV-pattern × relative modelled Bombus richness relationship**. This does not establish an absence of visual-signal adaptation or Bombus selection; a UV-uniform flower can have visible guides, scent, other UV dynamics and learned age/reward signals.

**No significance tests, causal mediation, floral-guide behavioural interpretation or plant fitness claims are warranted:** only two genera supply covered pairs, original UV phenotype locality is not a modern GBIF point, native L3 plant regions are not site-level plant–bee overlap, present-day GBIF first pages are effort-biased, and modelled predicted bee species names are not actual visitors.

## Next scientifically identifiable gate (not automatically claimed)

1. Locate original source phenotyped population/vouchers and make site-resolved native plant occurrence selection instead of the 100-record GBIF index page, with spatial blocks and coverage balance.
2. Obtain lineage-independent clades/original phylogenies and estimate receiver-guild contrasts at actual phenotyped source localities; separate absolute Bombus richness from guild fraction and source denominator.
3. Keep reward-age spectral detectability (Ohashi original 219) separate until species-level receptor predictions are reconstructed. A 2025 review listing only positive colour-changing taxa cannot provide negatives.
4. Joint visual-signal × wind/flower movement × pollen-success evidence remains a separate mechanistic experiment, not inferred by multiplying unrelated literature observations.

**Stop rule:** Do not claim UV-pattern-dependent Bombus adaptation or a general ecological coefficient from this source frame. Keep PR Draft and main unchanged.
