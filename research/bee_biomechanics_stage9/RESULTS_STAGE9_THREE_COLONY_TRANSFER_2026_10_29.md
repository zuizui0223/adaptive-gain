# Stage 9 — donor-only three-colony transport of floral-orientation transition associations

**Date:** 2026-10-29. **Status: complete exact-original-source test; positive raw colony-to-colony transition-rule transfer, but no positive source-segment-conditional *fine-order* transfer.** The predeclared positive-tail conditional test gives **p=1.000** because all 199 restricted null realizations have *greater* held-out transfer gains than the actual source order. This finding distinguishes background/contextual H/V use from a transferable sequential decision law. It **does not prove** opposite causal memory, absence of memory, or observational equivalence across the species.

## Original source, pre-result protocol and CI

Pattrick et al. (2023), *iScience*, DOI https://doi.org/10.1016/j.isci.2023.108071; Cambridge Apollo primary data DOI **https://doi.org/10.17863/CAM.100572**, source CC BY 4.0.

Original Cambridge `Observation_data.csv` 4,576,155 bytes, official provider MD5 `c34200f5746389ac29a6f99b3c461819`, independently checked SHA256 `c38d18df02cb4feb492b86b0f4b5ca0c767388c69bac0be1b44262d0f39e7d33`. Native DSpace published original README, bee masses and data were re-downloaded, hashes checked, and original per-action/episode chronology reconstructed. **No raw per-bee observations committed to Git**.

[Stage9 protocol](PROTOCOL_COLONY_TRANSFER_2026_10_29.md) was committed **before fitting the Stage9 donor transfer and original-segment null**, with donor treatments, exact population gate, fixed Dirichlet/logit smoothing, per-colony true holdout, separate conditional permutational falsification and stop rule. The analysis itself is **exploratory after Stage8/8b positive historical findings**, not independent prospective preregistration.

[Dedicated original-data GitHub Actions run 40849262759](https://github.com/zuizui0223/adaptive-gain/actions/runs/40849262759): **SUCCESS**, all 8 custom source/shape/independence/temporal tests passed, provider MD5 and original SHA256 validated, original Stage8 numerical baseline reproduced, full Stage9 result and 199 fixed-seed original source permutations printed. Downloadable non-identifying CI artifact contains `original_cambridge_source_audit.json`, `cambridge_behavior_episode_qa.json`, `bee_stage9_crosscolony_transfer_results.json`.

## Precisely identified experimental and observational units

The published record is **61,592 labeled actions from 38 tagged workers in 3 original experimental colonies**, of which 36 bees (12 per colony) completed the required original micro-rough/slippery test phase. Two unfinished bees are excluded based on **author documentation**, not outcomes. Source `Flower ID` is an **interaction-episode identifier** rather than a persistent physical flower ID, and `Time(ms)` is **action duration**, not a calendar timestamp. The same Stage8 source adapter reconstructed **12,064 actual touched-flower episodes** and **7,247 source micro-rough episodes**. Original `rest`/`boutStartStop` and real `Foraging trip` boundaries protect against fabricated action links.

Each original bee is trained exclusively on the *earliest ceil(70%)* of its original source micro-rough trips, with **all the later actual trips held out**. Exactly **36 bees, 3 colonies, 1,234 true subsequent H/V flower-touch choices** were scored, identically to Stage8 and Stage8b. A verified quality gate reconciles source Stage8 individual-preference→personal-history improvement `+0.051525510437894245` and previous-drink incremental effect `+0.004750769848322038`, before the novel donor model is scored.

The independent original experimental replication count is **three colonies**. Source bee tags are repeated individuals nested within colonies, not 36 independent colonies; the donor folds overlap and therefore must not be regarded as three uncorrelated entire experiments.

## Fixed before Stage9 results: three predictive models and independent donors

All predict probability `P(next touched source flower is horizontal)`, not actual arrival at a measured physical position.

- `M0`: source bee-specific stationary horizontal/vertical preference `p_b=(H_b+0.5)/(n_b+1)` estimated **only from that bee's earlier trips**.
- `Mpersonal`: that bee's original Stage8 earlier-trip first-order next H/V prediction based on preceding H/V, with fixed β=10 smoothing to M0. This model fits the individual early-trip history and is an **internal-source benchmark**, not out-of-colony model transport.
- `Mtransfer`: for a **target held-out colony c**, train **only the two other source colonies** on their earlier trips. For each of the three original experimental `Treatment` labels and each predecessor `previous∈{horizontal,vertical}`, estimate its donor-only smoothed next-horizontal probability, and log-odds difference from the corresponding donor treatment's baseline: `δ_{t,o}=logit(P_donor(H_next|t,o))−logit(P_donor(H_next|t))`. Predict a new target colony bee's later trip by `sigmoid(logit(p_b)+δ_{t,o})`, where `p_b` is **that target bee's own earlier-trip stationary preference only**. Thus the transferred **temporal correction**, not the bee baseline, is strictly leave-colony-out.

The locked α=0.5 and β=10 were not retuned. Original `Control`, `Low Difference`, `High Difference` treatments each have **12 actual complete source bees**. For each target fold the donor-other-two-colony training support passes all predefined gates: each original treatment is observed in both donor colonies, and even the rarest pooled `(treatment,previous H/V)` cell has **≥130** genuine earlier-trip transitions (required minimum ≥15). No target-source colony transitions enter its own transferred δ, and no held-out later outcome is used to select treatments, coefficients, source split or hyperparameters.

## Primary original-data result: transferable coarse association

Every model predicts **exactly the same 1,234 real later source decisions**. The following are **equal bee weights within each of three equal-weight experimental colonies**, proper held-out negative log likelihood in **nats per true next-flower H/V observation** (lower is better).

| Model | Mean held-out negative log likelihood |
| --- | ---: |
| M0: each bee's stationary own preference | **0.3992831** |
| **Mtransfer: other 2 colonies' earlier-trip orientation adjustment** | **0.3686055** |
| Mpersonal: own earlier-trip next-orientation adjustment | **0.3477576** |

M0→Mtransfer gives **+0.03067767 nats/choice**, **25/36** tagged source bees positive, **all 3 original colonies** showing positive average prediction gains. Mtransfer trails the own-bee Mpersonal model by **0.02084784 nats/choice** in the source overall average. It is a successful out-of-colony **transfer of one conditional predictive adjustment**, not evidence that all individual transition rules or mechanisms transport.

| Source target colony | Heldout true next-flower decisions | M0→Mtransfer improvement | M0→Mpersonal improvement | Source bees with M0→Mtransfer improvement |
| --- | ---: | ---: | ---: | ---: |
| **1** | 355 | **+0.0258276** | +0.0128984 | 10/12 |
| **2** | 371 | **+0.0204318** | +0.0464718 | 7/12 |
| **3** | 508 | **+0.0457736** | +0.0952064 | 8/12 |

The source colony 1 has more heldout score benefit from transferring donor adjustment than fitting its own previous-orientation effect, whereas source colonies 2 and 3 benefit more from the individually trained model. That variation is observed but does **not** identify an adaptation, specific worker memory or a robust population-level variance parameter with n=3 colonies.

## REQUIRED conditional source-segment null: transferable order-specific association NOT supported

The source Stage8b protocol had already demonstrated that part of the apparent within-bee M0→Mpersonal gain comes from original within-trip flower-type composition, not necessarily the realized predecessor→next alignment. The new Stage9 primary claim is therefore tested against the **frozen** source-consistent H/V predecessor-state null, not inferred merely from positive raw Mtransfer scores.

Exactly **199** permutations, RNG seed **20261029**, jointly shuffle *source previous H/V + recorded Drink bits* **only inside each original same-bee, same-bout, uninterrupted handling segment** in the *later test trips*, retaining the **actual next-flower H/V choices**, source IDs, temporal original trip boundaries, entire test population, and all earlier fitted individual M0 and donor-only Mtransfer coefficients. Source Stage8b original admission passes: **544 exchangeable original later test edges across 18 bee tags**, with all 1,234 genuine later decisions scored. Predeclared minimum was ≥200 edges and ≥10 tags each with ≥5 cases.

| Original-data source-matched statistic, nats/choice | Value |
| --- | ---: |
| Actual heldout cross-colony M0→Mtransfer gain | **+0.03067767** |
| Mean gain from 199 actual segment-structure-preserving predecessor shuffles | **+0.05757877** |
| 5th–95th percentile of conditional shuffle gains | **+0.05047890 to +0.06381046** |
| Full sampled shuffled gain range | **+0.04640158 to +0.07563167** |
| **Actual minus conditional shuffle mean** | **−0.02690110** |
| **Predeclared positive-tail p** `P(shuffled gain≥actual)` | **1.000** |

All **199/199** source-conditional randomized predecessor assignments yielded **greater** Mtransfer benefit than the actually observed source order. That means **the donor-only learned orientation correction does not explain the fine-scale true predecessor-to-next orientation alignment better than the trip/segment-conditioned null**. It does **not** prove negative causal influence of prior flower type or individual learning failure, since the shuffles create statistical predictor labels that need not form physically realizable bee tracks. We report the originally fixed **positive-tail p=1**; a secondary negative-tail would be a direction chosen after seeing these results and is **not** promoted as a registered statistical confirmation.

Original colony-specific residual contrasts (actual minus its own conditional null mean):

| Original target colony | Actual−source-conditioned shuffled gain |
| --- | ---: |
| 1 | **−0.02144384** |
| 2 | **−0.04784500** |
| 3 | **−0.01141446** |

All three target colonies have **negative** true-sequence-specific transfer increments under this particular conditional null. This is a genuine constraint on the interpretation of raw positive leave-colony-out forecasts.

## Scientific synthesis and stopping rule

Stage8 original source: individual prior floral **orientation** improves next H/V forecasting over each bee's long-term preference (`+0.05153`), while recorded prior drinking has a very small additional effect. Stage8b original source: genuine predecessor alignment within the same uninterrupted foraging segment provides **only +0.00702** extra gain beyond a within-segment source state-composition null, although the exact Monte Carlo test is positive relative to that null. **Stage9 now shows that a *broad* H/V transition correction can be transferred to new original colonies (+0.03068 raw), yet the *fine alignment* of genuine predecessors and subsequent choices does not transfer under the same strict source-state conditional null (−0.02690 real−null).**

Thus, in this dataset, **transferable information about the background floral-use *composition/state* is distinguishable from the fine sequential decision rule**. It is not valid to leap from a positive heldout transition predictive gain to **a universal bee memory mechanism, causal flower handling tradeoff, decision order or adaptive routeability**.

**Stop source-specific tuning here.** Do not revise pseudocounts, treatment groups, chronological cutoff, individual exclusions or null segment boundaries merely to obtain a positive fine-order transfer. The scientifically useful next experiment must measure individual bee ID and physical flower positions together with actual instantaneous flower options, observed action/reward intake, and randomized sensory cue availability or travel constraints across independent colonies. The original Stage4–6 spatial routes did not have source controlled cue timing; source Stage7b had colony counts but no workers; Stage8/9 has worker and action/nectar category but no persistent physical flower position/flight heading. These observational gaps cannot be healed by further numerical mining of the same experiments.

**No wind experiment was run in Stage9.** Any earlier UK PoMS wind-to-relative-guild-visit associations are a **separate observational ecological line** and must not be presented as independent replication of laboratory bee-choice mechanisms. No causal `C_A/C_F`, reproductive fitness, interspecific network competition or evolutionary generality identified.

### Reproducibility and data credit
- Original byte-verified complete [GitHub Actions run 40849262759](https://github.com/zuizui0223/adaptive-gain/actions/runs/40849262759), SUCCESS: eight focused tests, original Cambridge institution-owned download/source SHA and MD5 verification, original source observation/episode reconstruction, exactly preserved Stage8 results, all three actual donor-only folds, and 199 source-segment conditional shuffles.
- Code `research/bee_biomechanics_stage9/cross_colony_transfer.py`, synthetic tests `test_cross_colony_transfer.py`, dedicated source CI `.github/workflows/bee-stage9-colony-heldout-transfer.yml`.
- Source results archive `bee_stage9_crosscolony_transfer_results.json` plus full source provenance and episode receipt. Verified independently: arithmetic mean of all 36 per-bee gains equals the published colony-equal mean 0.030677670686656236, with all three source colony effects represented. **No raw individually tagged bee event records are redistributed**.
- Original data attribution: Pattrick et al. (2023), Cambridge Apollo DOI 10.17863/CAM.100572, CC BY 4.0. Article DOI 10.1016/j.isci.2023.108071.
