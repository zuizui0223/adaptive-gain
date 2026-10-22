# UK PoMS wind-conditioned heteroguild sentinel test
Registered 2026-10-22 **before inspecting held-out scores**. Original source EIDC 10.5285/5841bfae-471b-498c-af89-c30e5140d6c5. No edits to frozen V5/V6.

At each of 5,506 valid focal pan stations across 1,139 site-days/92 sites (undisturbed 4–8 hour catches, wind within date range >=.5 Beaufort, >=3 traps/date, duplicate days excluded), predict target **hoverfly** counts; **bees** are a secondary outcome. All counts including actual zero are retained. Wind is ordinal 0–5 recorded at beginning/end; DO NOT translate to physical m/s or mix with FIT leaf-moving categories. Recorded flower-identity richness is observed only at some stations, and absence of lists is unknown, never zero flowering.

The key exploratory question is whether **parasitoid wasp and spider captures at OTHER pan stations that same site-date** add information beyond weather, floral richness, habitat, date, and captures of the SAME focal guild at OTHER stations. Other-trap leave-one-out exposure-adjusted group catch rate excludes the focal pan's own bycatch counts, preventing same-container mechanical correlations. Co-occurrence is NOT direct predation/parasitoid interaction or any insect's observed cue sequence.

Nested fixed feature groups:
- M0: ordinal wind, temperature, sun exposure, vegetation height, trap station, country, land cover, habitat, year/month, flower-list richness and missing-list flag, trap-hours exposure.
- M1: M0 + log1p other-trap **focal guild** count per hour (baseline for primary contrast).
- M2: M1 + log1p OTHER-trap parasitoid wasps and spiders per hour (primary added-value test).
- M3: M2 + local (within site-date-centered) wind × each heteroguild indicator (primary moderation test).

Poisson rate model with actual hours as exposure, PoissonRegressor alpha=.1 primary and declared .01,1.0 sensitivity. Training-site-only encoding/scaling, training 99th-percentile winsorization on external catch-rate features. Five GroupKFold by whole site; evaluate held-out Poisson negative log likelihood, averaging observations inside sites then sites equally. Fixed-fold site-bootstrap uncertainty conditional on already trained folds (4,999). Report country/year slices, influence and zero rates. M2 and M3 considered transferable *only* if improvement relative to immediately preceding model is positive under all alphas, the exploratory site-bootstrap interval excludes zero and leave-one-favorable-site-out retains direction; otherwise NO-GO. No sequential-tuning of hypotheses or additional guild predictors to rescue p-values. Note all nine-site Crall orchid bee count/composition evidence is distinct and cannot be numerically pooled.

Nothing here directly tests an ecological causal hierarchy, cognitive routing, prey/host contacts, fitness or \`C_A<C_F\`. The strong cross-life feeding-class wind signal is genus confounded and adjacent-plant moderation failed its fixed sample gate.