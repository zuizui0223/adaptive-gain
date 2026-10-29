# Stage 9 — independent 2017 three-layout transport of a 2019 directional bee-route predictor

**Date: 2026-10-29. Status: COMPLETED WITH SOURCE QUALITY AMENDMENT. POSITIVE OUT-OF-SOURCE, OUT-OF-BOUT PREDICTION IN ALL THREE ACTUAL ARRAYS AND BOTH ORIGINAL COLONIES, with explicit uncertainty/limitations.** Dedicated original-data [GitHub Actions run 40806410761](https://github.com/zuizui0223/adaptive-gain/actions/runs/40806410761) **SUCCESS**, **19 targeted tests**; all publisher original file SHA256s passed, source structural quality/figure gates passed, three actual original layouts scored, all predeclared 199 per-array direction nulls and 21 figure-coordinate jitter sensitivity computations completed. No prior frozen V5/V6 manuscripts or source-data papers modified.

## Biological hypothesis and why this is the first external geometric test

The earlier Pasquaretta et al. (2019) experiment supplied **one colony and one ten-flower arrangement**. Stage 6 found that the incoming 2D chord from flower `A` to `B` helps predict the next distinct flower `C` even after accounting for flower-specific bee preferences and Euclidean distance `d(B,C)`. The training-only source-2019 dimensionless direction coefficient was **κ=1.0**.

The **new independently published experiment** is Klein et al. (2017), *Inter-individual variability in the foraging behaviour of traplining bumblebees*, *Scientific Reports* 7:4561, DOI **https://doi.org/10.1038/s41598-017-04919-8**. It tests **29 individually identified foragers from TWO source colonies**, **THREE geometrically distinct four-flower layouts**, **20 chronological original foraging bouts per bee per layout**. This is a genuine new-source predictive **transportability test** of the **frozen 2019 κ**, not a repeated Stage 6 fit or a new claim that the authors never knew about trapline learning.

**Scientific unit:** Each source colony contains multiple repeatedly tested bees; the *same* 29 bees experienced all three arrays **in fixed order 1→2→3**. Therefore 29×3 array samples are **not 87 independent biological individuals or 6 independent colonies**, and neither array order nor landmarks were randomized. Confidence is limited by two original colony lineages and this fixed one experiment. The incoming direction variable remains **an endpoint-chord proxy from labeled 2D physical positions**, not an instrumented continuous 3D flight heading or actual sensory-cue query order.

## 1. Source integrity: exact original supplemented bytes and observation grain

Both original Springer-hosted supplementary files were obtained by publisher HTTP 200 and independently source-hashed:
- **Dataset S1** `41598_2017_4919_MOESM2_ESM.csv`: **104,034 original bytes**, SHA256 `e1b660125c389fc873a70eaf0edaaec053637cc814d8bcb50f1a61a01b7e3e04`; native columns `bee_ID,colony,age,body,array,bout,nb_flower,imm_revisit,non_imm_revisit,speed,prop,sqce_tot`.
- **Dataset S2** `41598_2017_4919_MOESM3_ESM.csv`: **10,432 original bytes**, SHA256 `68e663f50d7d741c3a162f67b03db89499aff4c328aecf09361cf15955440535`; 87 source bee×array summary records, **perfectly reconciled** to S1 identifiers.
- **S1 source observation grain:** **1,740 actual one-bee×one-array×one-original-bout rows** = 29×3×20, with **zero duplicate original experimental keys**, both original colonies (`jimmy` 840 rows and `tristan` 900), and exactly **580 original bouts per array**.
- The original source's `sqce_tot` sequence contains digit `0` for the nest and `1…4` for physical flowers within **that original array**. All **1,740 source sequence fields** include a single non-semantic trailing ASCII `"` quote; source code strips only this surrounding quote character, **never reorders, replaces or fills any source flower codes**. The original 1,740 rows contain **12,652 flower visit tokens, 10,919 flower-to-flower adjacent pairs and 8,357 nominal physical nonzero two-step triplets** *before* source-quality exclusions. **These are inventory counts, NOT the modeled observation denominator.**

### Exact observed nest-boundary quality exception, frozen BEFORE directional outcomes

A strict first source audit revealed **16 original `sqce_tot` bouts missing an outer `0` nest marker** and **4 other source bouts with an internal nest `0`**. The 20 original source rows were individually logged with `(original source row, bee, array, original bout, raw symbol string)`. It would be scientifically incorrect to connect visits across the internal nest, manufacture missing nest visits, drop the bee altogether, or automatically call a non-nest-bounded string a complete trip.

A distinct **post-source but pre-model-outcome** document [SOURCE_AMENDMENT](ORIGINAL_SOURCE_AMENDMENT_BEFORE_MODEL_2026_10_29.md) froze **exactly these 20 structurally questionable source bouts for exclusion ONLY from direction modeling**. All original 1,740 rows remain in the data QA. This leaves **1,720 original nest-bounded physically interpretable candidate bouts** containing **12,542 source flower visit tokens**. The original numeric source-bout split remains **1–15 training, 16–20 final heldout**, *without reassigning valid replacement bouts* after exclusions. There are zero fabricated inter-bout, cross-nest or across-array transitions. All source-original 87 bee×array identities still pass ≥10 clean training and ≥3 clean final bouts, with ≥5 genuine final-bout source triplets per bee. This exception was not selected or modified based on predictive performance.

## 2. Figure 1 original publisher layout geometry — clearly approximate

The original journal **Figure 1** was obtained from Springer Nature's publisher URL:
`https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41598-017-04919-8/MediaObjects/41598_2017_4919_Fig1_HTML.jpg`, native **675×675-pixel JPEG**, original **50,879 bytes**, SHA256 `4277dcc8ec52598037a7a4fd6d6bc47d4877a68593a400723508a2d7c0cd40ac`.

The source Figure1 panels b,c,d give **labeled F1–F4 positions on x/y axes measured in centimeters**. Positions were manually digitized to **nearest 10 centimeters**, frozen prior to fitting in [flower_positions_figure1_digitized.json](flower_positions_figure1_digitized.json), with **nominal ±10cm error for each coordinate**. They are **not GPS or exact measured flower positions**; digitized positions ignore landmarks and unobserved bee flight paths.

| Array | F1 cm | F2 cm | F3 cm | F4 cm |
| --- | --- | --- | --- | --- |
| 1 (paper Fig1b) | (600,200) | (400,100) | (100,200) | (150,450) |
| 2 (Fig1c) | (550,100) | (350,100) | (100,100) | (300,300) |
| 3 (Fig1d) | (620,50) | (50,150) | (100,350) | (400,450) |

Coordinates convert to metres by dividing by 100 **before distance calibration**. A post-source/pre-outcome frozen jitter checks the effect of drawing **21 independent perturbations for the 3 source maps**, seed 20261029, each nominal coordinate independently ±0.10 metres, with **each perturbed array's λ reselected from TRAINING source bouts only**. This tests digitization precision, not independent experimental conditions.

## 3. Exactly frozen external model and chronological holdout

For each bee×source array, compute static preference from genuine flower visits in first 15 source-numbered bouts, using **α=0.5** smoothing for all four physically available flower labels. For each array separately, select a single `λ ∈ {0,0.25,0.5,1,2,4} m⁻¹` on **all bees' first15 true switched flower pairs**, via the predeclared conditional next-*different*-flower negative log likelihood. There is **NO use of original bouts16–20 in selecting λ**.

Selected training-only distances:

| Array | Early source switched pairs used for λ | Selected λ (/m) | Best training NLL |
| --- | ---: | ---: | ---: |
| 1 | 2,566 | **0.50** | 0.90338 |
| 2 | 2,957 | **0.25** | 1.00079 |
| 3 | 2,362 | **0.25** | 1.03155 |

**Mgeo**: `P_b(C|B) ∝ P_static_bee(C) × exp[−λ_array d(B,C)]`, normalized over the three other physical flowers `C≠B`.

**Mtransport**: `P_b(C|A,B) ∝ P_Mgeo(C|B) × exp[κ cosθ(A,B,C)]`, normalized over the exact same three physical alternatives and with `cosθ` from true labeled coordinates. **κ=1.0 is FIXED FROM THE INDEPENDENT 2019 DATA SOURCE, NOT FIT HERE**. This tests transfer of a dimensionless direction weight across different geometry scales. No geometry-specific `κ` adjustment, source label/bee subset selection or heldout hyperparameter tuning.

The source evaluation is only **genuine within-one-original-bout triplets `A→B→C` with `A≠B` and `B≠C`**, from the original last five numbered bouts. The test sample from the **1,720 clean model-eligible original bouts** is:

| Source array | Heldout A→B→C triplets | Qualified tagged bees | Original independent source colonies |
| --- | ---: | ---: | ---: |
| 1 | **608** | **29** | **2** |
| 2 | **687** | **29** | **2** |
| 3 | **663** | **29** | **2** |
| Total (not independent animals) | **1,958** | Same **29** repeatedly tested bees | Same **2** colonies |

The 1,958 triplets are repeated observations from the same 29 bees and cannot be used as 1,958 independent biological replicates.

## 4. Main positive external-transfer result: fixed 2019 directional coefficient works on 2017 layouts

Exactly the same heldout genuine triplets are used for both Mgeo and Mtransport in each original array, with per-bee **proper negative log loss (nats per next distinct physical flower)** aggregated to equal bee weights.

| Original independent 2017 flower layout | Mgeo bee-equal NLL | Mtransport (external κ=1) NLL | **Improvement Mgeo−Mtransport** | **Tags positive / total** |
| --- | ---: | ---: | ---: | ---: |
| **Array 1** | 1.007672 | **0.848069** | **+0.159603 nats** | **23/29** |
| **Array 2** | 1.072200 | **1.008720** | **+0.063481 nats** | **18/29** |
| **Array 3** | 1.029743 | **0.941989** | **+0.087754 nats** | **17/29** |

**Both original colonies have positive average bee-level improvements in every layout**:

| Source colony (14 or 15 bees) | Array 1 | Array 2 | Array 3 |
| --- | ---: | ---: | ---: |
| jimmy | **+0.175416** | **+0.068575** | **+0.136086** |
| tristan | **+0.144844** | **+0.058726** | **+0.042645** |

**Supported scientific statement:** an independently estimated, geometrically defined **incoming-direction state variable** improves held-out prediction of a true next *different flower* in **three changed four-flower spatial layouts from a distinct published experiment**, even against a fair source- and bee-specific distance prior. The coefficient was transferred without retuning from the original 2019 fixed ten-flower array. This is an empirically inspectable predictive generality result, **not a randomized causal test** of flight inertia.

## 5. Source-preserving conditional negative control

Separate **199 fixed-seed shuffles per original array** reallocate only the **incoming source flower A within (same actual bee tag, same current physical flower B, same original array)** of the heldout source triplets. All **actual B→C outcomes**, 2017 train-only λ, bee priors, exact source array positions, physical destination options and **external κ=1** remain fixed. These shuffles are **not physically realizable new bee flights**; they test only source geometric lag alignment.

| Original array | Source triplets with exchangeable incoming flower A | Actual directional gain | Same-(bee,B) null mean gain | **Actual−null mean** | Conditional one-sided p |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 502/608; 26 bees | +0.159603 | +0.027392 | **+0.132211** | **0.005** |
| 2 | 585/687; 26 bees | +0.063481 | −0.010113 | **+0.073593** | **0.005** |
| 3 | 544/663; 27 bees | +0.087754 | +0.007556 | **+0.080198** | **0.005** |

In each original array the observed gain exceeds all 199 seed-frozen source-conditional shuffles, at the Monte Carlo resolution minimum **1/200=.005**. Source occurrence and experienced bee memory are *not* manipulated; this does **not** show randomized flight direction causality. Because the same bees/colonies experience the three arrays in fixed order, three p-values do **not** represent three independent experiments. The conditional permutations are exploratory negative-control distributions, not biological replications.

## 6. Figure-coordinate uncertainty, predeclared source-image digitization sensitivity

Original Figure1 axes are small; manual reading precision is limited. The pre-outcome frozen **21×±0.10 m source-image perturbations**, with training-only λ re-estimation in every perturbed array, gave:

| Source array | Min–max bee-equal gain (nats) | Positive perturbations / 21 | Early-only λ selection across 21 |
| --- | --- | ---: | --- |
| 1 | **+0.157210 to +0.161334** | **21/21** | λ=0.50 in 21/21 |
| 2 | **+0.058474 to +0.065094** | **21/21** | λ=0.25 in 21/21 |
| 3 | **+0.083082 to +0.091447** | **21/21** | λ=0.25 in 21/21 |

The source-digitization precision range does **not** reverse the model gain in these **fixed** trials. This does not validate continuous true bee flight path geometry, exact panel measurements, hidden landmarks or a broad error distribution beyond ±10cm. A future use should retain and cite the source figure SHA and describe positions as approximate, never as directly measured source coordinates.

## 7. Ecological significance and necessary restrictions

**Nontrivial affirmative inference:** Previous spatial position and **approach direction** are distinct pieces of recorded *geometric state information* relevant for predicting sequential flower visits. The direction term improves prediction not only in the original static 2019 artificial-flower array but **transfers out of dataset** to a different 2017 study with three different spatial arrangements. This is a concrete empirical reason to include **incoming direction or an equivalent two-step movement state** rather than using static edge distance or stationary resource use alone in spatially explicit foraging models.

**Not established:** motor inertia, directly measured orientation, visual/olfactory cue query ordering, attraction/repulsion, learning versus innate flight behavior, energetic payoff from directed routes, ecological wind exposure, interspecific competition, selection or evolutionary adaptive `C_A/C_F` information-access costs. The physical 4-flower array and geometrically derived turn angle are known; what each bee *perceived* at a given instant is not. Array presentation order (all sources 1→2→3), unmeasured landmark geometry, animal habituation across arrays, two rather than multiple independent colony replicates and manually digitized flower coordinates are important alternatives.

The original 2017 publication already reported trapline route development and inter-individual variability; this new work is a **fixed-parameter external predictive transport test** using published primary data, not the discovery of traplining itself.

**Decision / no-p-hacking stop:** preserve all three positive arrays, the source 20-bout anomaly exclusions and the approximate Figure1 geometry with their pre-outcome amendments. **Do not** retune κ, λ grid, original 15/5 split, manual flower coordinates, or cherry-pick source bee subgroups to maximize heldout gain. The next causal test would directly track flight headings with changes to visual/sensory flower accessibility randomized across layouts and **more independent colonies**, including natural flower sources and calibrated wind if the ecological wind hypothesis is to be addressed. Frozen V5/V6 manuscripts and previous Stage4–8 results remain untouched.

## Reproducibility / rights
- [Actual GitHub Actions source→original Figure1→pre-model anomaly gate→three-array heldout performance 40806410761](https://github.com/zuizui0223/adaptive-gain/actions/runs/40806410761): **SUCCESS**, 19 focused source tests, publisher original S1/S2 and Fig1 original SHA-256 receipts, complete all-three-array model and 199×3 conditional null and 21-map-jitter diagnostics.
- `research/bee_multiarray_stage9/source_audit.py`, `bout_grain.py`, `figure_source.py`, `external_turn_transfer.py`, `run_external_direction.py`, numerical source and model tests; author-independent raw event rows are ephemeral only in CI.
- The source belongs to Klein et al. (2017), *Scientific Reports*, Springer Nature, DOI 10.1038/s41598-017-04919-8. Attribute the 2017 original experimental data/figure and distinguish this independent reanalysis from the original paper's prior claims. If distributing source content, follow the original publication's current licensing and copyright restrictions; the GitHub repo stores no original experiment CSV nor publisher Figure1 image, only source URLs, hashes and manually digitized approximate coordinates.
