# Stage 9 — transportability of bee flower-orientation history across *independent original colonies*

**Frozen before Stage 9 actual held-out results: 2026-10-29.** This test is *exploratory relative to previous Stage8 and Stage8b discoveries* and therefore does not retroactively make them confirmatory. Scientific main goal is to distinguish a **repeatable colony-to-colony temporal decision rule** from a historical predictor that only works when each bee's own earlier decisions are used for fitting.

## Source and original causal/observational grain

Pattrick et al. (2023), *Bumblebees negotiate a trade-off between nectar quality and floral biomechanics*, *iScience*, DOI https://doi.org/10.1016/j.isci.2023.108071; Cambridge Apollo original data DOI https://doi.org/10.17863/CAM.100572, CC BY 4.0.

- Original institution-owned source file `Observation_data.csv`: 4,576,155 bytes, SHA256 **`c38d18df02cb4feb492b86b0f4b5ca0c767388c69bac0be1b44262d0f39e7d33`**, original MD5 **`c34200f5746389ac29a6f99b3c461819`**. Exact published README is required, no heuristic flower IDs or times.
- 61,592 native **action** rows and 38 source bee tags, 3 independent source colonies. Author excludes two unfinished test bees (`Yellow 4`, `Green 47`): **36 finished bees = exactly 12 in each colony**. Original `Flower ID` is a new **visit-episode ID**, not physical location. `Time(ms)` is action *duration*, not absolute time. **No physical individual route geometry or initial cue-reveal time**.
- Reuse exact source Stage8 reconstruction of 12,064 actual touched-flower episodes, source slippery/micro-rough test phase only, 6,311 within-bout candidate adjacent choice edges across original bees. Do not join physical routes between different `Foraging trip` IDs or through original rest/nest boundaries.
- For **each bee**, train on first `ceil(70%)` original slippery test trips in source row order and score the entire later visits. Preserve exactly **36 qualified bees, 3 source colonies, 1,234 source held-out true next-horizontal/vertical choices** across Stage8/8b. The following values are byte-verified model reconciliation gates, not model-selection targets: Stage8 M0→M1 bee-equal **+0.051525510437894245**, Stage8 M1→M2 **+0.004750769848322038**, within-trip-lag-null N1 raw M0→M1 **+0.0515255104**.

## Distinct hypothesis (no cherry-picked individual bees)
**Can an *orientation dependence* estimated from two original colonies' *early training trips* improve held-out next-flower orientation forecasts for individual bees in the third colony, without fitting that dependence to any bee or visit from the third colony?**

A positive 3/3 result would establish **bounded cross-colony predictability of this experimentally specific H/V transition association**. It is not a cognition/wind/foraging-fitness inference; flower physical layout, unreconstructed source time and individual floral handling remain confounds.

## Three frozen fair model comparators
All probabilities describe `P(Y=horizontal next actual touched flower | ...) `, log loss in **nats per true later H/V decision**, with each bee given equal weight within each of three equal-weight source colonies. No event-weighted 1,234 independent-bee inference.

1. `M0_b` (source Stage8): individual bee's own earlier-test-bout unconditional stationary propensity `p_b=(n_H+.5)/(n+.5+.5)`, using **α=0.5**. Test later b's trip decisions only.
2. `Mpersonal_b` (source Stage8): individual bee's own earlier-trip `P(Y=H | predecessor H/V)`, with predeclared **β=10** pseudoobservations shrinking to its own `M0_b`. This predictor **has access to that bee's own early orientation-transition history** and is an internal-study comparison, not a colony transfer.
3. `Mtransfer_{b}` (new primary): compute a *single source treatment-conditional orientation effect* from the **other two colonies only**, using **only those donor bees' earlier-test-trip outcomes**:
   - For each experimental treatment `T ∈ {Control, Low Difference, High Difference}` pool donor earlier-trip `(preceding H/V, next H/V)` pairs only. `p_{T,0}=(n_{H,T}+.5)/(n_T+1)` and `p_{T,o}=(n_{H,T,o}+10 p_{T,0})/(n_{T,o}+10)` (fixed β=10).
   - `δ_{T,o} = logit(p_{T,o})−logit(p_{T,0})` is a **donor-only adjustment** for previous orientation `o`. Use target bee's own early-trip stationary `p_b` *only as a calibration baseline*. Then `P_transfer(Y=H | T_b,o,b)= logistic(logit(p_b)+δ_{T_b,o})`.
   - **Do not include a donor colony as a source in that colony's transfer effect**; neither the target bee's own earlier transition counts nor any target colony H/V transitions may enter `δ`. No source later-test data ever train any model. Fix all smoothing to α=.5/β=10, no hyperparameter tuning or held-out source re-selection.
   - Source `Treatment` is defined per bee; verify one unique T for each bee and all three T groups are represented with actual donor training in both other colonies, no null labels.

**Primary estimand:** three-colony-equal mean `[NLL(M0)−NLL(Mtransfer)]` on exactly **the same** 1,234 genuine later H/V choices that Stage8 used. Report each of 3 actual colony means, positive colony count, all 36 bee-level gains, and Mtransfer relative to Mpersonal (source Stage8 upper-context comparison). Do not treat 1,234 event labels as 1,234 independent colonies. A sign/CI based only on three colonies is descriptive, not robust population generalization.

### Fixed source-support no-go gates
Before any source transfer parameter calculation or final-day scoring:
- exactly 36 author-complete bee tags/3 source colonies/1,234 held-out edges; source observed treatment fixed within each bee; at least **3 different source treatment labels** across the experiment.
- In each **outer target-colony** fold, at least **2 source donor colonies** have training data for **each** of the 3 treatment labels; for both `previous∈{H,V}` cells each donor pool has **≥15 genuine earlier-trip pairs**. If not, output `NO_GO_DONOR_TREATMENT_ORIENTATION_COVERAGE`, no zero-cell substitution or source train/test redefinition.
- For a source complete bee, no cross-trip event; no source rest/stop transition and no ambiguity about previous orientation. All model probabilities strictly between zero and one and no unseen test bee ID used in donor effect fitting.

## Falsification against source-trip state composition, fixed before transfer result
Source Stage8b revealed that a large proportion of the within-bee M0→Mpersonal gain is reproduced by shuffling predecessor states within true uninterrupted source handling segments. Therefore Stage9 **must not call its raw transfer score "true memory"**, even if positive.

Freeze the **same Stage8b source-segment conditional orientation-and-drink predecessor-state null** on each target bee's **same held-out trips**:
- **199 shuffles**, seed **20261029**. Within each actual source uninterrupted `(colony,bee,trip,segment)`, jointly permute previous H/V orientation and observed Drink bit, preserving source predecessor multiset, observed next H/V outcomes, original source row/grain, original trip, training models, source treatment and actual source colony.
- For each shuffled target future test record, recompute the *already trained* `Mtransfer` only using the permuted prior H/V; `M0_b` stays invariant. The three donor-conditional coefficients **must** remain unchanged and untouched.
- Require the same source Stage8b original permutation admission **≥200 exchangeable genuine source edges across ≥10 bees with ≥5 such edges**, otherwise `NO_GO_CONDITIONAL_EXCHANGEABILITY` (do not broaden segment definition).
- Report raw Stage9 primary gain, 199 mean conditional shuffled gains and their **difference**, 5th/95th null quantiles, one-tailed MC `(1 + # null gains≥ actual gain)/200`, *per original colony actual−null differences*. If primary transfer fails/negative, still run this declared null; report negative outcomes honestly.

**Interpretation/stop rule**: even positive donor→new-colony transfer and conditional lag signal only establish reproducible observation-level *flower-orientation temporal associations* in this laboratory setup. Physical flower position, motor inertia, nectar intake, direct flight kinematics, wind, species interactions, experimentally controlled cue-access order and reward/fitness costs are unmeasured. This is the final planned source-specific held-out/conditional transfer test: **do not tune treatment groups, source-split percentages, pseudocounts or shuffled source segment boundaries post hoc** to obtain significance. If associations fail to transfer, prioritize designing a new experiment with randomized cue/flower availability instead of more source mining.

Preserve published Stage4–8b receipts, original source files never committed, frozen theory V5/V6 manuscript untouched. New draft branch stacked on PR #83.
