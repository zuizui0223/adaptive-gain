# Stage 8 result — individual-bee handling/reward history and later orientation choice

**Date: 2026-10-28. Status: COMPLETED ORIGINAL SOURCE QUALITY, 36-BEE CHRONOLOGICAL HELD-OUT PREDICTIONS.** The prior selected flower's **orientation** adds appreciable out-of-sample prediction of the next *touched flower orientation* beyond stationary bee choice frequencies; a further **previous observed drinking-action** variable adds only a very small, heterogeneous predictive increment. A direct difficult **vertical-hover** subset offers **no positive incremental drinking-action gain**. This does **not** establish individual causal memory of nectar intake, movement geometry, time of perceptual cue acquisition, or adaptive return from information search.

Dedicated original-source [GitHub Actions run 40619205100](https://github.com/zuizui0223/adaptive-gain/actions/runs/40619205100) **SUCCESS**, all **19 focused source/provenance/episode/model/regression tests passed**, source CSV original MD5 verified and own original SHA256 pinned. Original source stays on ephemeral CI only; non-identifying quality/summary receipts retained.

## Provenance and independent experimental contrast

Pattrick, Symington, Federle & Glover (2023), *Bumblebees negotiate a trade-off between nectar quality and floral biomechanics*, *iScience* 26:108071, article DOI **https://doi.org/10.1016/j.isci.2023.108071**. Original open data in University of Cambridge Apollo DSpace repository DOI **https://doi.org/10.17863/CAM.100572** (CC BY 4.0).

The official Cambridge `ORIGINAL` bundle itself, not an aliased file title on the publisher's landing page, supplies:
- `Observation_data.csv` original **4,576,155 bytes**, native provider **MD5 `c34200f5746389ac29a6f99b3c461819`**, independent original SHA256 `c38d18df02cb4feb492b86b0f4b5ca0c767388c69bac0be1b44262d0f39e7d33`.
- `Bee_masses.csv` original 714 bytes, provider MD5 `e5b8e52901a2889cebd34d4b6780daa6`, original SHA256 `a37ac38b137e35332a8fa1a62956617f0c4ea124f84636a6118fc73c99575f8b`.
- `README_observation_data.txt` provider MD5 `42d5e43299044e4f0be863e2c6183803`, original SHA256 `b07881ae90419b7dbf04a3ced8e3792dd4e9b08eea282389a2752799b8c1bad5`.
- `README_bee_masses.txt` provider MD5 `0b079f834f5a84b5c6dc226b71a7fa22`, original SHA256 `5e5158f6161346be6f51df10fd632d6ef00bb119f97ebada6cc28e74c91d11a5`.

Official Cambridge DSpace HAL API supplied the exact item DOI match, original bitstream UUIDs, contents, byte sizes and original MD5 checksums. The paper's description sometimes uses the aliases `TradeOffData.csv` and `BeeMasses.csv`; these are **not** the byte-owning original file names in the repository. This was corrected by probing the native source manifest.

The experiment offered individually tested *Bombus terrestris* workers **15 vertical and 15 horizontal physical flowers** across 3 colonies. The slippery **micro-rough** test phase was preceded by an easy-grip **coarse-rough** familiarization phase. Per the published experimental design:
- High Difference: vertical **50%** sucrose vs horizontal **20%**.
- Low Difference: vertical **50%** vs horizontal **35%**.
- Control: vertical **35%** vs horizontal **35%**.

The paper already documents *energetic rate versus handling cost* and the final experimental flower preferences. **Those original findings are NOT claimed as newly discovered.** Stage8 tests a distinct fixed chronological history-prediction contrast.

## Original source grain corrected and audited

Original `Observation_data.csv` has **61,592 source ACTION rows**, with exactly 38 individual bee identifiers in **3 source colonies** and **9 original action labels**:

`boutStartStop`, `leaveFlower`, `rest`, `horizontalLandVisit`, `horizontalLandDrink`, `landVisit`, `landDrink`, `hoverVisit`, `hoverDrink`.

- `Time (ms)` is **duration of the labeled action**, NOT an absolute event timestamp. The 38 missing durations correspond to original last recorded actions, without inventing observation dates.
- Source `Flower ID` identifies a **visit-episode cluster** that changes when a new floral interaction is recorded or the bee visits the same flower after rest; it is **NOT the physical position of an individual flower**. No legitimate flower-to-flower Euclidean distances, headings, or distinct physical flower IDs can be derived from these source IDs.
- Consecutive source action rows grouped within bee/surface/bout and per-visit episode produce **12,064 genuine touched-flower episodes**, of which **4,817** belong to the coarse-rough familiarization and **7,247** to micro-rough test.
- 3,800 other consecutive source groups have no original flower action, 17 original completely identical action rows were **retained** rather than assuming duplicate visits, and **0** reconstructed touched-flower episodes have conflicting vertical/horizontal orientations. All 38 bee tags were present in source; two incomplete test bees (**Yellow 4**, **Green 47**) are excluded **per the original README** in the predictive analysis, yielding **36 complete bees, exactly 12 from each original colony**.

Source action classes directly distinguish whether a bee **landed or hovered**, touched horizontal versus vertical flowers, and whether an original `*Drink` action was recorded. `*Drink` is **not** proof of the volume/sucrose actually swallowed; **no artificial negative-cue or reward-failure state is imputed**.

## Frozen before testing outcomes: fair source-trip chronological holdout

[Stage 8 frozen protocol](PROTOCOL_CAMBRIDGE_ORIGINAL_2026_10_28.md) recorded the main estimand and numeric hyperparameters after source-role audit but **before** any Stage8 empirical heldout forecast scores. Only original **micro-rough test phase** episodes in the same bee's real `Foraging trip` enter the next-orientation model. Consecutive physical visits are connected only if there is no intervening original `rest` or `boutStartStop` event for that bee; do not cross bee, trip, surface phase or source experiment.

- **7,247 micro-rough touched-flower episodes** originally recorded; **6,311** eligible true consecutive source-choice pairs across all 38 source bee keys. Among potential pairs, 358 between-bout/surface boundaries and 540 genuine rest/nest markers correctly prevented spurious transition links.
- For each complete bee, sort trips by the first original source action-row index (NOT `Time(ms)` duration), train on **first ceil(70%) of original micro-rough trips** and hold out **all later entire trips**. This keeps experimental colony, bee and all later choice labels out of fitted state, and avoids random-event CV leakage.
- All **36 original completed bee tags** passed the frozen ≥10 early-pair/≥5 later-pair thresholds; all **three original colonies** represented. Exactly **1,234 unique genuinely later next-touched-orientation decisions** formed the common, heldout test population.
- Fixed model probability smoothing, entirely learned on early trip outcomes, zero heldout tuning:
  - **M0**: bee's stationary next-horizontal preference `(H+.5)/(n+1)` (α=.5 symmetric binary prior).
  - **M1**: bee's previous horizontal versus vertical touched-episode identity, β=10 prior observations shrinking to bee M0.
  - **M2 (PRIMARY)**: bee's previous episode orientation AND whether an original `*Drink` action was observed in that same previous episode, γ=10 prior observations shrinking to bee M1.
- All three predict whether the **NEXT actual touched flower episode** is horizontal (versus vertical); unlike source reward treatment, source flower physical position is not recorded. All scored event probabilities are positive. Primary proper score is per-bee mean heldout **negative log likelihood (nats / actual next orientation decision)**. Source bee is the in-experiment behavioral unit; all three colonies are reported individually and the primary mean is **equal colony weights (n=3)**, not visit-weighted event totals.

## Actual independent test result

| Heldout model, 36 bees and 1,234 later source next choices | Bee-equal NLL, nats/choice |
| --- | ---: |
| **M0 — fixed individual horizontal-flower preference** | **0.3992831** |
| **M1 — fixed preference + previous orientation** | **0.3477576** |
| **M2 — previous orientation + previous actually recorded drink action** | **0.3430069** |

**Distinct positive sequence association (M0→M1):** bee-equal NLL improved **+0.0515255 nats / choice**. **28 of the 36 bees** had positive improvement (8 negative); all **three colonies** had positive bee-equal mean M0→M1 changes:

| Original colony | Completed bees | M0→M1 gain (nats / choice) | M1→M2 gain (nats / choice) |
| --- | ---: | ---: | ---: |
| 1 | 12 | **+0.0128984** | **+0.0010348** |
| 2 | 12 | **+0.0464718** | **+0.0019135** |
| 3 | 12 | **+0.0952064** | **+0.0113040** |

**PRIMARY immediate observed-drinking-history effect (M1→M2):** small bee-equal and colony-equal gain **+0.0047508 nats / choice**; **20 of 36 bees** improved, **16 worsened**. Although each colony's mean is slightly positive, these are only **three** independent original source colonies and must **not** be described as statistically convincing population-level memory effects. There is **no source randomization of prior animal nectar intake or of visual cue access** within the derived sequence.

**Fixed difficult-vertical-hover sensitivity:** Restrict test comparisons to later source actual episodes whose immediately preceding source visit was **vertical and had recorded hovering**; no model retuning. This subset has **489 genuine heldout next choices from 18 bee tags** each with ≥5 such events, passing the source predeclared support. Under identical trained M1 and M2, the additional drink-action information had mean individual-level predictive gain **−0.0055443 nats / choice**: slightly *worse* forecasts after adding the observed prior drinking action. **Do not promote the whole-source tiny positive +0.00475 into a successful difficult-flower memory mechanism.**

The strongest, directly supported cross-study pattern is therefore **nonexchangeable flower-type usage across time**, even after conditioning on each bee's own long-run choice frequencies. It is **not** evidence that the immediately realized outcome of the previous difficult flower is a robust additional selector of next flower type.

## Scientific interpretation and limits

- Stage4–6 earlier original 2019 Pasquaretta data showed ten tagged bees and strong geometric/directional destination prediction in a fixed 10-flower array: latest directional gain +0.1914 nats on 1,203 genuine final-day A→B→C triplets, with learned first-order history adding **no consistent improvement after direction**. That source was one single colony.
- **Independent Stage8** shows that an individual's *last visited flower orientation* predicts later touched orientation beyond a fixed preference across **36 source-complete bees from three independent colonies**, but the **actual physical flower ID is not in the dataset**, so route inertia/adjacency and time-dependent learned policies are not separated. The small M2 additional recorded drinking effect fails the difficult-vertical-hover positive-gain gate.
- Earlier Stage7b independent 2026 KU Leuven experiment had **18 colonies / 54,362 author-processed robot events** and detected **within-hour group reward-use composition smoothness in 16 colonies**, but lacked worker IDs. Thus Stage8 is a distinct intermediate source with multiple colonies, individual bee IDs and actual handling actions; it is **not the same source experiment** linking those particular group dynamics to individuals.

**Unidentified mechanisms**: real flower-to-flower movement distances, incoming 3D flight headings, instantaneous other-bee occupancy, individual visible cue arrival time, nectar intake volume, actual opportunity cost and reproductive fitness. The surface phase changes in fixed temporal order (easy then slippery) and cannot be treated as random surface intervention independently of elapsed experience. Source reward concentration is fixed by the original treatment and orientation, not independently randomized at every visit. The initial laboratory paper already showed the high-versus-low concentration handling trade-off; this analysis cannot recreate it as novel evidence.

**Stopping rule:** preserve this outcome with both **positive M0→M1** and **weak/nonrobust primary M1→M2 and negative difficult-hover sensitivity**. Do not retune β/γ, reallocate fixed train/test trips, or search post-hoc bee/treatment subsets to obtain a large positive handling-memory effect. Stronger claims require a separate, randomized **immediate sensory cue/reward availability reveal** manipulation with physically tracked flower locations, individual ID, measured motor handling, and replicated independent colonies.

## Reproducibility
- [Dedicated original-source verification and heldout model run 40619205100](https://github.com/zuizui0223/adaptive-gain/actions/runs/40619205100): **SUCCESS, 19 tests**, provider MD5/source SHA256 verified, original 61,592 activity records reconstructed into 12,064 actual visit episodes; 36 individually heldout bee models scored. A machine-readable ZIP artifact contains the source+original file audit, episode count ledger and all 36 individual model NLLs.
- Code paths: `research/bee_biomechanics_stage8/source_audit.py`, `episode_audit.py`, `heldout_experience_choice.py`, and tests. The source data and publisher README bytes are retained only transiently during the GitHub CI job; **no individual raw action event rows are distributed through this PR**.

**Attribution and license**: Pattrick, Symington, Federle & Glover (2023), DOI 10.1016/j.isci.2023.108071. Cambridge Apollo DOI 10.17863/CAM.100572. Original files CC BY 4.0; retain academic credit and sources in derivative publications.
