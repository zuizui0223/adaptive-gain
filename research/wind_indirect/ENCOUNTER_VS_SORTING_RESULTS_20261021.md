# Wind changes recorded arrivals and species composition differently — exploratory original-data source comparison (2026-10-21)

**Status:** original-data comparison completed locally and independently checked. This is NOT a novel field discovery of positive wind-to-orchid-bee arrivals (already published by Crall et al. 2020); NOT proof of unchanged composition or a causal predator-/competitor-mediated wind mechanism. No change to main or frozen V5/V6.

## Costa Rica orchid bee source, verified identity and counts

Crall et al. *Biology Letters* 16:20200103, https://doi.org/10.1098/rsbl.2020.0103; Zenodo 10.5281/zenodo.3675327, original ZIP **MD5 42e53512e4bdad2701593a89d1c87dfd**. Twenty-minute captures of male orchid bees visiting a scented bait, simultaneous sonic anemometer mean wind in m/s.

Original `integratedSpatialWindData.csv`: **70 wind-measured sessions, nine sites, 29 dates, 409 arrivals** including three genuine zero-catch sessions. The original `beedata.csv` has 450 specimen rows, but **41 rows belong to 7 keys with no matching wind session**, so only 409 specimens in 67 positive sessions can enter wind×taxonomic-composition analysis. Exact site/date/scent join reconciles all original per-session counts; 23 matched species. Never treat 450 as 409 observed visits + 41 missing visits or drop zero sessions from count analysis.

## Separate wind responses

**Encounter intensity (70 sessions):** Fixed site, month and scent Poisson count model gives per-doubling wind **RR 1.37089**, site-clustered exploratory 95% **[1.04005,1.80698]** (nine clusters; nominal p=.02518), Pearson dispersion **1.947**. Independently re-fit entire log-likelihood via SciPy BFGS: beta for log wind **0.455116810512** versus statsmodels **0.455116810513** (difference 9.03e-13). Cineole-only RR **1.38273**. Leave-one-site-out ratios range **1.26472–1.49665**. Original authors previously found increasing wind-associated scent-source visitation; this is a source-integrity reanalysis, not independent replication. Within site×month×scent permutations of **whole wind-session labels** (4,999) give signed partial count correlation **+0.32011**, two-sided p **.0236**, 15 permutable blocks / 64 sessions.

**Taxonomic composition (67 positive sessions):** Species identity conditional on already-captured session counts: per-block residual covariance whole-species score **0.25921**, within-site×month×scent 4,999 permutation null median **0.26176**, right-tail **p=.509**. Second independent, *post-result* Jensen–Shannon wind-high/low contrast: **equal blocks p=.0914** (observed JSD .42681 vs null mean .39858); **weight by caught individuals p=.0278** (.37341 vs .32946). Removing the `wilson1` site changes specimen-weighted JSD p to **.195** (nine delete-one-site analyses use 999 shuffles apiece). The composition conclusion **depends on the weighting and metric**. No equivalence/no-compositional-effect inference is warranted; counts and species identities answer different questions, and one small versus large p does not formally test their difference.

The between-site wind–count Spearman correlation is **−0.5167 across only nine sites**, whereas conditional within-site correlation is positive. This cross-scale direction difference is descriptive and was previously discussed by Crall et al.; spatial forest cover and other context can confound between-site associations.

## Independent wind-turbine behavioral event source: insufficient interspecific evidence

Weschler wind-turbine insect behavior Zenodo 10.5281/zenodo.15447016, `WindPollinatorData110823.csv`, original published **MD5 9bcab4765c4fe5a9edaaf096867caf5b** and independently computed SHA256 `55f514b6dfae277fcbae43e105e796667af77a897a1da558407f5c15929647e0` (both checked). It has **472 individual behavior rows** over **six sites**, but only **15 site/date observation blocks**; wind is constant inside each site/date block, and turbine distance is site-constant. `DifferentSpeciesInteraction=1` in just **five rows**, with no usable identity for the interacting partner species (18 `SameSpeciesInteraction` flags). **NO-GO** for wind×specific-other-species network or mediation. The unit of independent wind information is 15 site-dates, not 472 individual behavior rows.

## Cross-system interpretation and limits

Previously audited UK PoMS pan traps (5,506 station observations/92 sites; *different ordinal Beaufort instrument and capture process*) found bees RR .907 per Beaufort grade, 12-guild BH q=.121, hoverflies RR .894, q=.139, moths RR .593, q=.046 **but sensitive to unusual catch days**. UK PoMS ten-minute FIT count's ordinal wind and tropical sonic-anemometer wind are also not interchangeable. Prior PoMS EuPollTrait "zoophagous larval diet × wind" RR≈1.62 is primarily confounded with genus/flight biology; a nearby flower-richness mediator failed its locked sample gate and held-out predictions.

**New scientific framing worth pursuing:** wind can modify the accessibility/delivery of different ecological cues and opportunity to encounter resources without identically changing species identities. Whether a predator, shared plant, host or competing species mediates that change is **not identified** by shared-wind co-capture, historical host labels or Weschler's five unidentified interspecific event flags. Real identification requires species-resolved encounter histories, wind manipulation, resource inventory, predator/competitor/host identity, and a fair fixed-versus-contingent cue-acquisition intervention before referring to adaptive-gain's `C_A<C_F` field relevance.

## Reproducibility and source preservation

In-session portable archive `wind_encounter_sorting_20261021.zip` contains the exact published Crall ZIP, Weschler CSV, source-reconciliation code, 6 locally passing focused tests, 4999-shuffle results, independent likelihood optimization, alternative JSD tests and deletion sensitivity JSON. This report is the durable repository result; GitHub-wide CI is not declared green.

Original data credits: Crall et al. 2020; Weschler Zenodo 10.5281/zenodo.15447016; UK PoMS EIDC DOI 10.5285/5841bfae-471b-498c-af89-c30e5140d6c5 for external context, not refitted here. Licence terms and source acknowledgments remain with original archives.
