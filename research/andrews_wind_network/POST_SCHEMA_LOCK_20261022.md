# Post-schema, pre-result temporal species-order protocol — 2026-10-22

**Frozen before calculating any bee↔enemy lag-direction outcomes.** The prior registered general protocol and exact original sources remain unchanged. This amendment uses only source column schemas, row-quality diagnostics and outcome-independent eligibility counts.

## Source QA findings

Official SA026 v8 original watch rows **74,942** and independent floral survey rows **23,642**, verified by exact MD5 and DataONE entity SHA-1; 18 meadow codes, data present **2011–2018 and 2021** (NOT every year 2011–2021). Original interaction status '0' occurs in **13,917 rows** and '1' in 61,025 rows. **54 minute keys** (full raw data) mix status '0' and '1'; cannot force both zero and positive events for the same minute. The publisher's described key including `VISSP_NO` has repeated combinations; the correct analytic grain is the unique plot×watch×minute event *aggregation*, never raw row IDs as independent animals.

Observed `WIND` (ST/BR) can disagree **between rows of the same minute**. Rather than assign a wind by a majority vote, restrict to watches with all 15 distinct observed minutes, every row's minute in 1..15, every row WIND in ST/BR, and exactly one wind code across the whole watch; exclude entire watches with any minute containing both status=0 and status=1. No unrecorded minute is imputed zero.

Expected eligible samples from schema-only QC: **1,298 complete stable-wind watches** (925 ST,373 BR), 19,470 fully observed minute cells. Bee visitors and bee-associated enemy/nest-parasitoid/predator-role visitor types both appear in **164 watches** (123 ST,41 BR), in 17 meadows and 103 meadow-days. In 140 of these watches the two role classes visit at least one common recorded plant taxon (103 ST,37 BR). **17 meadow×year strata spanning 11 meadows** contain both wind classes within the same all-role-positive subset (79 watches), satisfying an a priori minimum 15 strata and 10 meadows for wind moderation; smaller cannot support this test.

## Source-coded a priori role labels

Bee focal class: exactly `social bee`, `solitary bee`, `halictine bee`, `semi-social bee`, `halictine bee/semi-social bee`, `pollenivore bee`.

"Bee-associated enemy" class: source `VISSP_TYPE` contains `bee-parasitic`, `bee-predaceous`, `bee-predator`, `pollinator-predaceous`, `predaceous onm bees`, `kleptoparasitic bee`, or source-typo `kloeptoparasitic bee`. These are **natural-history roles of visitors**, not field-observed attack/nest use, ecological competition or cross-species cue exposure. Bees do not include kleptoparasitic bees in the focal class. No selection of species-pairs or role group variants after looking at lag contrasts.

## A priori time-arrow statistic

Within each qualifying watch, create two binary (0,1) minute sequences `B[t]` and `E[t]` of **any focal bee** and **any bee-associated enemy-role visitor** among positive records, t=1..15. Multiple same-minute visits are counted ONCE per role. For each watch with both roles:

`D_watch = sum_{t=2..15} (B[t] E[t-1] - E[t] B[t-1]) / (sum_t B[t] * sum_t E[t])`.

D>0 = "enemy observed one minute **before** a bee" more often than the reverse, corrected for numbers of focal/enemy-positive minute opportunities. D<0 = "bee before enemy" predominates. Zero is absence of directional lag asymmetry **in the recorded watches**, NOT proof of no biological interaction. Statistic changes sign under exact reversal of both full sequences. A discrete observation minute does not establish individual animals noticed one another.

Second frozen endpoint **same-plant**: evaluate identical D using per-species plant-category B[t,p],E[t,p] arrays and denominator `sum_p n_Bp*n_Ep`. Only the 140 watches with at least one *shared* recorded plant enter. It does not assume that other plants were absent or unavailable, nor that source `PLTSP_CODE` means the same physical flower.

Primary wind moderation: site/year-blocked contrast of mean D in BR minus mean D in ST within only the **17 meadow×year blocks with both wind categories**, then average meadow-year block differences *equally* (no pseudo-replication of very prolific meadows). Randomly exchange the *watch* wind labels **only within those meadow×year blocks**, 9,999 simulations + observed statistic; report two-sided p. Wind is observational, so exchangeability can fail due to time of day/plant phenology/weather; this test assesses label alignment, not causation. For same-plant repeat the procedure on the independently feasible >=15 mixed blocks.

Additional no-wind directional check: mean D across all both-role watches, site-equal mean and 4,999 whole-meadow bootstrap interval; 9,999 whole-meadow time-reversal sign flips as an exploratory conditional no-direction null. Note that within-watch time trends break perfect reversal exchangeability.

Multiplicities: 2 wind-moderation tests (all recorded plants vs same recorded plant), adjust their two-sided p-values with **Holm**. Sensitivity (fixed): require >=2 bee-positive and >=2 enemy-positive distinct minutes within each watch, and independently exclude 2018 due to potential observer protocol drift. Recompute BOTH endpoints, no alternative taxon filters or selected wind cutoffs. Report proportion of all 4,616 source watches surviving each restriction and group sample support; if fewer than 15 mixed strata or 10 meadows under sensitivity, mark NO-GO for that sensitivity.

## Boundaries

A finding of timing asymmetry would be evidence of *observation-ordered cross-role sequence structure*, not predator deterrence, social learning, adaptive sensory routing, fitness or causal wind modification. An absent effect is a boundary on detecting such order in 1-minute aggregated data, not proof that enemies do not act. Data cannot link individual insects, larval hosts, repeated animals, actual attack events or adaptive gain; prevent all such promotions.

Source credit as in original protocol: Seo et al. (2022), LTER HJ Andrews SA026, DOI `10.6073/pasta/eec55cbc3dbfc56428629773737ab3e5`.