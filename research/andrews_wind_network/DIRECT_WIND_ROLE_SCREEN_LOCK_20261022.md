# Wind and observed bee versus enemy-role flower-visitor activity (exploratory)

**Declared on 2026-10-22 after resolving source QC and after the temporal-order NO-GO, but before calculating the direct-wind outcomes.** This is a distinct ecological estimand, not a variant search to rescue the lag effect.

## Scope and frozen design

Use exactly the original SA026 version 8 watch data, 1,296 stable 15-minute watches, 19,440 observed minutes, 17 meadow units. Roles were frozen in `POST_SCHEMA_LOCK_20261022.md`: six source-coded bee visitor roles, seven strings for natural-history bee-enemy/predator role visitors, mutually exclusive. Each role's primary response is the **fraction of 15 observed minutes with at least one confirmed interaction**; no row or organism counts, with or without `NO_INT>1`, are treated as independent visits.

Wind is binary `ST` still vs `BR` breezy and must be constant across every row in a 15-min watch. Restrict comparison to the same `MEADOW × SAMPLEDATE` where at least one ST and at least one BR watch was performed. From schema-only QC: **92 paired meadow-days across 13 independent meadows, 578 total watches**. Both wind conditions are not experimentally allocated to plots; weather, flower location, visit time and observer could differ.

For each meadow-day, take the observed (mean of ST watches) and (mean of BR watches), their BR–ST difference, then average **equally across meadow-days** (reported alongside meadow-equal average as a sensitivity). Three related signed contrasts are fixed:
1. **Primary:** `Δ_enemy - Δ_bee` (difference in wind-linked change in proportion of visited minutes). This is an *absolute percentage-point difference of activity minutes*; it is **not** a relative predation effect or a causal dietary sorting coefficient.
2. Secondary `Δ_bee`.
3. Secondary `Δ_enemy`.

Randomize entire watches' wind labels **only within each meadow×date**, 9,999 simulations (within-day number of ST/BR watches preserved), calculate two-sided centered-at-zero p values. Apply Holm adjustment to **all three contrasts**, not just whichever is favorable. Bootstrap whole meadow clusters with all of their days intact (4,999 draws) for exploratory 95% intervals. Report direction of all three; do not claim ecological wind causation from label exchangeability.

Declared sensitivity (do not change endpoints): (i) require exact-date same-plot `SA02602` flower survey recorded as part of watch, giving from schema-only QC **57 meadow-days, 13 meadows, 313 watches**, and (ii) restrict to watches in 2014–2016, report support, do not relax conditions. Original 2019/2020 contain no source rows; all-15-minute analysis is effectively a restricted-year cohort.

Stop promotion if primary interaction q>=0.05 or sign reverses in exact-date flower subset; no additional group filters or target-only p-value promotions. A significant difference implies observational **different visitor-role activity frequencies under recorded wind**, not an observed interspecific attack, an indirect food web causal pathway, or an animal's adaptive information query.