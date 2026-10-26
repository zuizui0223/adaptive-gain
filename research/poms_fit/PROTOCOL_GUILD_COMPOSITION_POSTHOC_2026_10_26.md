# Post-hoc Stage 3b: within-FIT guild composition × wind (2026-10-26)

**Exploratory follow-up decided after Stage 3 totals and guild-specific outcomes were inspected. NOT preregistered; NOT independent confirmation.**

Question: within a 10-minute **single-target-flower** 1km FIT census, does the relative composition of observed insect visits change with wind category after controlling target flower, floral quantity/type, day-of-year spline, year, sunshine, and site? This is not a behavioral switching experiment, causal wind manipulation, predator/prey interaction, coexistence, or niche partition.

Fit three explicitly declared conditional binomial log-odds models using raw paired insect counts:
- bumblebees vs hoverflies,
- bumblebees vs other_flies,
- bumblebees vs butterflies_moths.

For each focal pair, include every eligible 1km survey with **at least one visit belonging to the pair**; surveys with both pair counts zero cannot define its composition and are excluded explicitly, while original all-zero surveys remain in the separate Stage 3 overall visit-rate analysis. The response is `[bumblebees, comparator]`, modeled with aggregated binomial GLM rather than expanding counts into falsely independent organisms. Use wind levels as unordered categories, reference calm/occasional leaf movement, and the same fixed spatial/season/flower covariate design as Stage 3. Cluster-sandwich SE by the same 1km site. Report strong-wind log-odds ratio, 95% cluster CI, and the two-level joint wind test. Holm-adjust the **three strong-wind** p-values; do not adjust or cherry-pick which pair appears in the report. Singular/nonfinite models are failed, not simplified for significance.

No zero-inclusive claim is made from this pairwise composition subset: it is conditional on at least one encounter in the pair. Sensitivities to floral target selection, count multiplicity, taxon-group misidentification, within-site correlated visits and unknown alternative plant availability remain. Results may suggest relative differences but cannot establish direct species–species interaction, competition, wind-driven signal routing or adaptation.
