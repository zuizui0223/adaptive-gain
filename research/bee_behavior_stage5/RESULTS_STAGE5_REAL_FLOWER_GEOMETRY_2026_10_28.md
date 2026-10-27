# Stage 5 result — physical flower distance versus individual bee route history

**Date:** 2026-10-28. **Status: COMPLETED original-data observational follow-up, with a supported spatial predictability result but *no consistent individual-level switched-destination historical increment beyond geometry*.** This result constrains the earlier positive Stage 4 interpretation; it does not invalidate the raw previous-flower predictive finding. Dedicated [GitHub Actions run 40540408916](https://github.com/zuizui0223/adaptive-gain/actions/runs/40540408916) **SUCCESS**, 10 focused Stage 5 geometry/model tests and complete original S1 source execution. Machine-readable output `original_geometry_history_heldout.json` retained as a source-audited CI artifact. The same Stage 4 original S1 hash/records and outcomes were reconciled at run-time.

## 1. Source-backed geometry: actual original coordinates, not guessed flower numbering

Pasquaretta et al. (2019), *Movement Ecology* 7:4, Figure 2, https://doi.org/10.1186/s40462-019-0150-z. Original open-access ten-flower array figure was independently obtained on page 3 of the original original-publication PDF via https://d-nb.info/1181293162/34 (**1,112,178 bytes**, original PDF SHA256 `7f275a219fe0128d30f70cf6d812ab41d4b64727a740102549e8362b83d4ff8b`). The actual meter positions manually checked directly in Figure 2 are:

| Label | x (m) | y (m) |
| --- | ---: | ---: |
| F1 | 10 | 14.5 |
| F2 | 2 | 19 |
| F3 | 18 | 19 |
| F4 | 10 | 23.5 |
| F5 | 2 | 28 |
| F6 | 18 | 28 |
| F7 | 10 | 32.5 |
| F8 | 2 | 37 |
| F9 | 18 | 37 |
| F10 | 10 | 41.5 |

These ten coordinates are version-controlled in `flower_positions_figure2_verified.json` together with the **original source-PDF hash** and diagram citation. F1–F4 = **9.0 m**; F1–F6 = **15.692 m** from the printed rounded coordinates, consistent with the publisher text saying 15.8 m. The source estimates a **~9.6 m visual detection range** for the artificial flower at this scale. This is **not** a measured per-insect visual access set, not wind or flower pollen information. Predicted destination probabilities remain **strictly positive for all ten flowers**, even beyond the estimated visibility range.

The distance matrix and ten source labels pass direct test comparisons of example positions, symmetric positive distances, unit/source-digest guards and test-flower count.

## 2. Reused exact source and prospective train/test policy

Same independently published original bee sequences as Stage 4. Supplementary **Dataset S1**, direct publisher URL `https://static-content.springer.com/esm/art%3A10.1186%2Fs40462-019-0150-z/MediaObjects/40462_2019_150_MOESM2_ESM.csv`; **61,316 bytes**, pinned original SHA256 `0d30b0957c4b18602beebf60a915e03bee26142a8593f252badd77881b5e9dfe`.

Exactly **881 foraging bout rows**, **6,205 recorded flower visits**, **5,324 within-bout transitions**, **10 tagged bee individuals**, **5 data days**. Days **1–4** only are used for model training, including geometry scale calibration; **day 5** completely held out. No between-bout or overnight transitions are fabricated. The source has neither per-flower arrival timestamps nor source-labelled social-displacement outcomes.

The day-5 data contain **1,550 within-bout transition observations** (10 bee tags), of which **88 (5.68%)** were consecutive same-flower records and **1,462 (94.32%)** were *between two distinct flowers*. The empirical mean Euclidean distance of the 1,462 distinct-flower steps is **10.477 m**. **1,226 / 1,462 = 83.86%** of these recorded transitions connect flower pairs at or below the paper's **approximate** 9.6 m visual detection distance. This does **not** identify how much of the full 3D flight path was visually guided.

## 3. Four predeclared predictive models

All use **exactly the same original bee-specific earlier-day training data**. See `PROTOCOL_GEOMETRY_VS_SEQUENCE_2026_10_28.md` committed before inspecting these model outputs.

| Model | Definition |
| --- | --- |
| M0 static | Same bee's individual flower frequencies with additive Dirichlet α=0.5 per flower, as in Stage 4 |
| Mgeo distance | `P0_b(next) × exp(−λ × Euclidean distance(prev,next))`, renormalized over all ten destinations |
| M1 previous flower | Same-bee within-bout earlier-day transition counts `count(prev,next)`, smoothed β=5 toward M0 |
| Mgeo+history | Same transition counts and β=5, shrunk toward the *geometry-adjusted* Mgeo distribution |

A **single pooled spatial decay λ** was selected **on training days 1–4 only**, from a frozen grid `{0,0.025,0.05,0.1,0.2,0.4,0.8} m⁻¹`. Training-set grid mean NLLs: 2.1543, 2.1146, **2.1039**, 2.1701, 2.6171, 4.2726, 8.3507, respectively. Chosen **λ=0.05 m⁻¹** before the full day-5 test was scored; no heldout λ optimization, beta modification or hard visibility cutoff.

## 4. Primary predeclared result: genuinely switched-flower destination

Conditional on observing `next ≠ previous`, renormalize **each model's** ten-flower probabilities over the nine other physical flowers, with **no additional fitted parameters**. This isolates predictive information about **which different flower** the bee moves to, rather than just prediction of whether the same flower is revisited. There are 1,462 such observed transitions, and all **10 individual bee tags** pass the minimum ≥5 switch transitions.

| Model | Held-out bee-equal mean negative log likelihood (nats/switch) |
| --- | ---: |
| M0 static flower preference | **1.978895** |
| Mgeo static preference + verified distance | **1.848693** |
| M1 historical transition from previous flower | **1.783667** |
| Mgeo + historical transition | **1.782893** |

**Spatial geometry versus static preference:** mean per-bee improvement **+0.130202 nats/switch**, 10/10 tagged bees positive, two-sided within-colony sign-flip p **0.001953** (descriptive; one colony).

**Additional history after geometry — PRIMARY estimand:** `NLL(Mgeo)−NLL(Mgeo+history)` = **+0.0657995 nats/switch**. **Only 5/10 bees improve**, 5/10 worsen; two-sided within-colony sign-flip **p=0.23242** (descriptive). The point estimate is positive but not consistent across individual bees. Alternative historical M1 versus Mgeo is similarly uncertain: **+0.065026 nats**, 6/10 bees improve, p=0.23047. No evidence that *all* past-flower effects are exhausted by Euclidean distance can be inferred from a nonsignificant ten-bee test; conversely the data **do not support a robust cross-individual extra historical destination effect after geometry**.

Individual primary changes in nats/switch (positive favors Mgeo+history): w25 +0.21748, w37 +0.18563, w58 +0.04427, y35 +0.26722, y39 −0.04767, y45 −0.19899, y62 +0.23793, y63 −0.03358, y64 −0.01152, y67 −0.00277. These show biological heterogeneity and should not be hidden by 1,462 apparently numerous repeated observations.

## 5. All transitions and same-flower repeats — secondary diagnosis

For the *unconditioned* 1,550 test transition sample (includes the 88 same-flower repeat records):

| Model | Bee-equal held-out NLL (nats/transition) |
| --- | ---: |
| M0 static | 2.112873 |
| Mgeo | 2.055334 |
| M1 historical | 1.906346 |
| Mgeo+history | 1.903912 |

The **full-transitions** incremental history over Mgeo = **+0.151422 nats**, 9/10 bee tags positive, within-one-colony sign-flip p=0.02344 (descriptive), contrasting with the **weaker switched-destination primary**. Same-flower repeat *binary* NLL (bee-equal) is 0.29776 (M0), 0.36093 (Mgeo), 0.27540 (M1) and 0.27348 (Mgeo+history). The geometry kernel alone makes more same-flower repeats plausible from d=0, while the learned transitions better calibrate their true frequency. Thus an important component of **unconditional** Markov gain is repeat/switch event calibration, not necessarily choosing a different floral location or acquiring new information.

**Do not interchange the all-transitions and switched-destination endpoints.** The scientifically primary question here concerns physical transitions **between distinct flowers**. A Markov gain after including 88 same-flower repeats need not establish a destination-specific memory signal among different flowers.

## 6. Interpretation and stopping rule

**Positive new data-backed inference:** verified physical Euclidean flower distances explain real, held-out individual bee next-*different*-flower predictive structure that bee-specific stationary flower-use frequencies alone could not predict (10/10 tags improved); about 84% of switched flower pairs connect flowers no farther apart than the source *estimated* 9.6 m visual radius.

**Necessary limitation on Stage 4:** the earlier positive aggregate history result is real, but once physical geometry and true between-flower switching are evaluated fairly, the residual advantage is heterogeneous and **not consistently positive across the ten bees**. It is incorrect to use the Stage 4 result as proof of adaptive order-of-information acquisition or of a general species-level cognitive hierarchy.

**What remains unresolved:** flight heading/turning inertia, actual within-flight physical path geometry, insect line-of-sight, experienced landmarks, reward depletion, nectar intake, direct inter-bee displacement, fitness and cue-query temporal order. The site comprises **one 2010 single-colony, ten-flower static array** and **no wind manipulation**. There is no independent experimental colony replication, no natural multiple-plant community and no measured causal wind response. The present branch constrains a *single-study* prediction result only and does not close the adaptive-gain `C_A/C_F` identification problem.

**Decision:** freeze the positive spatial control and the **primary inconclusive incremental history** together. Do not search extra spatial hyperparameters or flower subsets to reverse the result. A real next discriminating manipulation needs controlled flower-array geometry and randomized perceptual access / route visibility with multiple independent bee colonies. If studying fine-scale natural floral interactions and wind, deploy cameras in actual patches with simultaneous floral alternatives, direction-resolved wind and individual route histories.

### Reproducibility, limitations and attribution

Dedicated original-source and geometry tests: [workflow run 40540408916](https://github.com/zuizui0223/adaptive-gain/actions/runs/40540408916), **SUCCESS**, 10 focused tests plus source SHA256 and exact Stage4 numerical cross-check; machine-readable artifact `original_geometry_history_heldout.json` and Figure2 source receipt. Ten flower positions are separately inspectable in `flower_positions_figure2_verified.json`. The original article is © Pasquaretta et al. (2019) under CC BY 4.0; source data original publication applies CC0 waiver unless otherwise indicated. Raw article PDF, original bee event CSV and Fig2 image are **not committed** into the repository, only source URLs, original SHA256 receipts and numerical results.

Frozen V5/V6 theory manuscripts and existing PoMS Stage 3e–g research remain untouched.
