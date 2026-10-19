# UK PoMS original-data 2-flower × 2-month matched FIT results (2026-10-19)

**Execution:** [exact-source Actions receipt](https://github.com/zuizui0223/adaptive-gain/actions/runs/39220417404), with all eight local exact-condition/kernel tests passing and a completed original-data run. **Exploratory observational**, not a field validation of `C_A<C_F`.

## Source, QA, unit of observation

Official UK PoMS (2026), *Flower-Insect Timed Count data 2017–2023*, EIDC DOI 10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618. The full official ZIP is downloaded anew and SHA256 logged in the archived analysis receipt. The public original CSV SHA256 is `bcd2ef780d3208a5a4aba5c191178900ccef705e5b569dc0160b27d00652dc3c` and 1km original CSV is `29d3deb757c053774c26ece0a7683081a4b4fe81d9497877fe1179f232182e52`.

- 13,457 public original ten-minute FIT records; 3,053 selected 1-km square FIT records, **16,510 total records**.
- All ten insect guild count columns nonmissing in every record; sum exactly equals `all_insects_total` in all 16,510 records. Total zero-insect survey rows: 774 public, 271 1km.
- Plant labels grouped as `Other - please describe below` in 5,172 public and 985 1km FIT records. They are excluded from the main strict plant identity analysis; they cannot be treated as a single plant taxon.
- Valid positive floral-unit counts and named target-plant/guild observation leave **8,260 public** and **2,068 1km** surveys. Each survey is one chosen plant in a 50×50 cm patch for ten minutes. Plant species not surveyed were NOT coded zero or assumed coavailable.

## Strict within-site cross feasibility

A site × year is eligible only when the **same two named flower categories are each actually sampled in both of the same two months**, with consistent flower-unit definitions within each species. The selected 2×2 design is chosen by survey exposure, not observed insect counts. Each site contributes at most one site-year to the independent-site comparison.

| Feasibility | 1km | Public |
|---|---:|---:|
| eligible site-years | 26 | 65 |
| distinct independent sites (one year each) | 21 | 55 |
| strict pair comparisons sampled within seven days in each month | 20 sites | 37 sites |
| selected 2×2 survey rows at independent-site stage | 108 | 825 |
| seven-day restricted selected survey rows | 101 | 497 |
| median minimum survey count among the four cells | 1 | 1 |

**Coverage conclusion:** This is a *thin* matched longitudinal design, especially in the more standardized 1km survey. The full number of FIT surveys must never be reported as independent evidence for a 2-plant × 2-month switch.

## Exact conditional estimand and sensitivity

For a guild's observed count table `y[month,plant]`, under independent plant and month effects proportional to sampled exposure `E`, condition on guild visit margins by plant and month. The conditional null is Fisher noncentral hypergeometric with odds `E11 E22/(E12 E21)`. A table without an informative 2×2 count margin is **untestable**, not a zero effect. Site-specific exact two-sided p-values were combined by Fisher's method; BH across ten insect-guild summaries. Independent-site and conditional Poisson assumptions still warrant caution.

**1km within-seven-day results:**
- `other_flies`, site `n=14` with informative margins: flower-unit exposure `q=0.000175`, whereas **survey-count exposure q=0.50**. Not robust to the resource exposure model.
- `wasps`: survey-count q=0.054, flower-unit q=0.430, based on only two informative sites; insufficient for a claim.
- `hoverflies`, site n=11: flower-unit q=0.233, survey-only q=0.660. No promoted signal.
- All other tested guilds likewise fail to provide a strong, exposure-robust, broadly replicated independent-site result.

**Public within-seven-day results:**
- `insects_small` site n=20: flower-unit q=5.36×10^-10, survey-only q=8.83×10^-6; an exploratory group-level pattern in a **very broad and ambiguous insect category**, at volunteer-selected public patches.
- `other_flies` loses its all-crossed signal after the 7-day restriction (flower-unit q=0.982; survey-only q=0.934).
- Neither public result establishes site-matched behavioral plant preference, all alternative flowers in bloom, or a causal cue-selection process.

## Ecological claim ceiling

**Supported:** FIT observations contain true zero counts, measurable target-flower exposure and within-site/within-year repeated survey design. Some coarse insect groups exhibit flower-target × month changes under specific exposure models in matched observed flower categories.

**Not supported:** a general, stable target-plant redistribution mechanism common to bumblebees, honeybees, hoverflies, butterflies, beetles etc.; correction for availability of all flowering species; independent animal decisions or target-conditioned sensory inspection; adaptive-gain fitness, or true network link rewiring.

The outcome is an important qualification to the prior Schwarz positive-only archive: raw season-vs-date partner breadth is not a direct behavioral constraint, and an apparent broad temporal pattern can fail to transport when survey exposure is required. It does not negate the previous Schwarz pattern because the two datasets answer different estimands and PoMS has weak 2×2 overlap.

## Next orthogonal test

Use all **named-target** 10-minute FIT observations including zeros to test whether a `plant × month` term improves held-out insect-guild count prediction beyond plant, month, flower amount, weather and observation covariates. Hold out **whole sites** and report site-equal uncertainty and the effective plant-month support. This is wider than the strict 2×2 design but weaker for identifying simultaneous alternatives. Keep its model-level associations separate from direct routeability.
