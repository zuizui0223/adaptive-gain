# Ecological routing empirical bridge: claims, non-support and decisive missing observations

**30 October 2026 | Working synthesis, not a merged main manuscript**

## Single defensible empirical headline

**Spatially conditioned movement-choice prediction is transferable, but a general information-processing mechanism is not empirically established.**

Do not reframe unrelated successful, negative or null endpoints as simultaneous replication of one physiological process. In `adaptive-gain`, the rigorous mathematical result is that **information-route structure and decision costs can vary dramatically while marginal observation statistics remain fixed**. The field and bee studies below test whether any particular ecological observation has predictive structure; none identifies the actual sequential *acquisition* of information or Darwinian fitness from cue use.

## Explicit evidence ledger

| Registered source/stage | Real biological unit and source | Newly tested endpoint | Actual observed result | Exactly what can be claimed |
|---|---|---|---|---|
| [Stage9b PR87](https://github.com/zuizui0223/adaptive-gain/pull/87) | Klein 2017 original 29 tagged bumblebees ×3 arrays, 1,958 distinct-flower heldout triplets, 2 source colonies | Add original incoming geometry to bee-specific early B→C route-frequency baseline | **Positive** in all 3 array outcomes; per-array bee-mean NLL improvement **+0.11105/+0.03290/+0.02390**, all 6 original colony×array cells positive | Source-frozen geometric incoming-order predictor adds *predictive* next-flower value beyond a trained per-bee first-order route baseline. Not measured actual 3D heading or adaptive information query. |
| [Stage10 PR88](https://github.com/zuizui0223/adaptive-gain/pull/88) | Chang et al. 2016 original 133 usable 3D landing tracks / 28 bee tags, 2 wind conditions | Predict *late within-approach physical flight heading* with earlier physical heading beyond wind/flower/position/speed | **Non-support**; bee-equal M0−M1 squared-error **−0.01418**, positive only 8/28 | Frozen added-heading model hurts prediction; not proof of missing movement memory or incompatibility with Stage9b's different response. |
| [Stage11 PR89](https://github.com/zuizui0223/adaptive-gain/pull/89) | Harris et al. 2026 114 original surveys, 1,140 60s observations, 74 city×date clusters, 18 plant labels | Wind×independently sampled potential nectar energy predicts observed probing rate | **Non-support** interaction +0.01423, CI [−.02255,.05101], p=.443 | No demonstrated buffering of wind-related probing by sampled nectar under the frozen observational model. Wind slope is secondary and geographically mixed. |
| [Stage12 PR90](https://github.com/zuizui0223/adaptive-gain/pull/90) | Same Harris source (NOT a new independent study): 113 original surveys, 1,130 60s observations, 16,678 recorded flight/walk transfers, 73 city×date clusters | Wind×co-survey nonhoneybee proportion predicts fly/walk **movement allocation** | **Non-support** interaction +0.05350, CI [−.13494,.24193], p=.573 | Co-occurrence does not show experimental sensory information use; 16,678 are movement events, not independent animals. The source has an impossible native N51=-6 flight count, quarantined as an entire survey prior to scoring. |
| [Stage13 PR91](https://github.com/zuizui0223/adaptive-gain/pull/91) | Smolla et al. 2016 original 57 individually tagged bees, only **3 source colonies** (4/35/18), 1,308 test visits and 1,233 true different-flower moves | Cue-state-same transition persistence given **fixed per-bee first choice AND exact per-flower visit frequencies** | **Non-support**: actual 0.48387 vs 999-permutation null 0.50961, contrast **−.02574**, fixed positive-tail p=.918, all 3 colony differences negative | The source author's published reward-dependent social first-choice copying is distinct from novel serial route-order clustering; no positive serial signal beyond visit marginals. Not evidence of a causal negative behavioral mechanism. |

**Do not pool p values, effect sizes or nominal observation counts across these rows:** they involve different underlying studies, responses, design-level replication, and cue definitions. Stage11/12 even share source observations. The negative signs in Stage10 and Stage13 are descriptive relative to their particular frozen hypotheses; they do not prove any universal reverse mechanism.

## What publication claims should be changed now

**Retain as a supported behavioral phenomenon:** next-flower destinations carry transferable prediction from an incoming geometric context feature beyond simpler flower-distance and early route-history comparators (Stage9b).

**Do not elevate:** earlier flight velocity as a universal movement-memory signal; wind-induced nectar buffering; wind-dependent benefits from co-occurring insects; an excess of same-cue serial flower routes; or the mathematical `C_A<C_F` advantage as experimentally observed.

**Possible synthesis question, still untested:** Is available information value conditional on a behavior's **task/choice architecture** rather than constant across travel (kinematics), destination selection (routing), and energetics? The current studies have different subjects, wind/environment manipulation, reward availability and outcome definitions, so stage contrasts do **not** identify task-scale causation.

## One concrete route to decisive evidence

Do not design another post hoc wind-co-occurrence association to rescue negative interaction terms. The existing source-validated [PR85 prospective cue-order×wind experiment](https://github.com/zuizui0223/adaptive-gain/pull/85) is the proper primary forward path, though **NO ANIMALS HAVE BEEN RECORDED**. Its physical manipulation changes cue **presentation order** and cue **recency** at the same time; an eventual interaction would not identify internal sensory processing order without recency-balanced controls. The decisive additional *real* records are: (1) synchronized individual identity and experimental original colony, (2) simultaneous alternative flower set, (3) source timestamps and sightlines at each cue access, (4) actual wind-vector/turbulence, (5) source-calibrated nectar consumed including genuine zeros/failed attempts, and (6) randomized left/right and order/recency conditions. Frozen original whole-colony ITT estimand and independent colony counts remain the analysis unit.

**Scientific STOP:** Retrospective source survey comparisons may be documented but must not be portrayed as causal confirmation of information acquisition order or adaptive gain. Preserve the negative results and original authorship of earlier effects. No changes to `main`, frozen V5/V6, or earlier Stage9b–12 PR scientific outputs are required by this synthesis.
