# Automatic Free-Cue assignment improves observed accuracy; conditional information-acquisition value remains unidentified

**Status:** public-data reanalysis (descriptive, with a conditional
trial-condition causal interpretation). Supporting context only for
adaptive-gain PR #67; **not V6 MAIN 4** and **not evidence of evolved
fitness optimization**.

## Source and design

He et al. (2026), bioRxiv *Uncertainty-Guided Decision-Making in Bumble Bees*,
https://doi.org/10.64898/2026.09.15.751944.
Public trial data and original code:
https://github.com/Cuixiaojian21/bee_metacognition
Pinned source commit 7f886394b4de872ecdb19ca4ea214ec321d5dce9;
data/4_active_information_seeking_trials.csv
Git blob SHA 26259c9071c6d73141d56b9bedd396cab1a04491.

The preprint reports that Random Free-Cue trials were interleaved
on 20% of experimental trials. The public data have 192 bees,
100 trials each, including exactly 20 Free-Cue trials per bee.
It reports a 500-ms flash of the correct target, automatically
triggered before the final choice in Free-Cue trials. During
Regular trials, a bee can land on a cue platform to request this
information at a reduced sucrose reward for correct decisions.

In the raw trial file:
- Regular: Info_Requested = Actually_Landed_On_Platform
  (the active request). Correctness is in the Post_Request
  column for requested trials or Non_Request otherwise.
- Random_Free_Cue: Info_Requested=1 regardless of platform
  landing; correctness is in the Post_Request column.
  Information delivery **is not** voluntary information purchase.

Do not join the separate metacognition-latency file to these
trials based on a shared numeric trial ID; it is not the same
trial task (see bee_2026_cross_experiment_join_gate_v1.json).

## Primary estimand: trial-condition offer contrast

Let Z denote assignment to Free-Cue automatic delivery rather
than Regular optional information request. Let Y be the binary
correct final choice. In each prespecified difficulty stratum d:

\[
\Delta_{\rm offer}(d)
=E[Y\mid Z=1,d]-E[Y\mid Z=0,d].
\]

This is a difference in experimentally assigned **trial regimes**,
not a simple comparison of self-selected requesters and
nonrequesters. Under the authors' claimed random interleaving,
no interference, and correct measurement, it admits a
trial-condition intention-to-treat (ITT) accuracy interpretation.
The allocation code or original event log was not independently
audited here, so randomization integrity remains a documented
condition for that causal interpretation.

Source-level results, with bee-cluster bootstrap B=3,000,
xorshift32 seed 0x7A4408, ordinary percentile intervals:

| Difficulty | Regular accuracy | Free-Cue accuracy | Free - Regular | Bee-cluster 95% interval |
|---|---:|---:|---:|---|
| Easy | 4718/6140 = 76.84% | 1461/1540 = 94.87% | +18.03 pp | [+16.60,+19.46] pp |
| Hard | 4262/6108 = 69.78% | 1483/1572 = 94.34% | +24.56 pp | [+22.90,+26.18] pp |
| Impossible | 2256/3112 = 72.49% | 674/728 = 92.58% | +20.09 pp | [+17.75,+22.39] pp |

Equal-weighting each bee's within-difficulty Free-Cue minus
Regular correct-choice rate produces means +17.96, +24.76
and +19.56 pp. Positive within-bee differences occur in
179/192, 188/192 and 161/192 respectively; the remaining
are zero or negative. These are descriptive individual
distributions, not genetically independent replicates.

### Trial-order robustness and an assignment placebo

Repeat the basic Free-Cue versus Regular correct-choice
contrast separately within five 20-trial bins. Every one
of the 15 difficulty x order-bin contrasts is positive.
The range across bins is approximately:

- Easy +16.38 to +20.28 pp;
- Hard +23.24 to +25.26 pp;
- Impossible +16.30 to +22.63 pp.

As a modest assignment diagnostic, the *previous* trial's
correctness differs between current Free-Cue and current
Regular assignments by +1.65, +0.71 and +0.25 pp for
Easy, Hard and Impossible current difficulty respectively.
This is not proof of randomization, but it tests a
pre-assignment correlate rather than a post-assignment
outcome. There remain many untested assignment covariates.

## Ancillary within-offer control: does landing itself predict correctness?

Within the 3,840 Free-Cue trials, the predictive cue was shown
**regardless of landing**. This allows an observational comparison
of platform landing among trials that all received the informative cue.
It is *not* a randomized landing intervention:

| Difficulty | Free-Cue landed accuracy | Free-Cue did not land accuracy | Landed minus no-land | Bee-cluster 95% |
|---|---:|---:|---:|---|
| Easy | 906/950 = 95.37% | 555/590 = 94.07% | +1.30 pp | [-1.02,+3.63] pp |
| Hard | 871/925 = 94.16% | 612/647 = 94.59% | -0.43 pp | [-2.61,+1.71] pp |
| Impossible | 142/153 = 92.81% | 532/575 = 92.52% | +0.29 pp | [-5.00,+4.70] pp |

All three bee-cluster 95% intervals contain zero.
The result suggests the observed high correctness in Free-Cue
trials is not *strongly associated* with choosing to land
again at the information platform. It does **not** prove
no motor/attention effect: landing is self-selected, group
sizes differ (especially on Impossible), and accuracy is
near ceiling in both groups. In particular, the
automatically triggered flash can affect timing and
attention even if the bee never lands. A same-duration,
uninformative SHAM signal remains essential.

Reproducible receipt:
free_arm_landing_accuracy_control in
validation/bee_2026_random_free_cue_accuracy_v1.json.

## What this DOES and DOES NOT establish

The experimental-condition contrast is **stronger evidence**
for an offered-cue benefit than the unadjusted comparison
of self-selected Regular requesters and nonrequesters.
In that self-selected comparison, missing counterfactual
outcomes leave even the sign of the voluntary-request
accuracy effect unidentified without further assumptions
(see bee_2026_request_ate_bounds_v1.json).

Nevertheless, Free-Cue automatically displays a 500-ms
predictive flash at a different moment and changes the
incentive to land at the information platform. The treatment
may jointly change sensory stimulation, attention, flight
path, task timing, and reward contingencies relative to
a self-chosen request. The source CSV does not provide
within-encounter decision latency or realized sucrose
dose; information-only effects and ecological payoff
are not identified by final correctness alone.

In notation:
- Z: assigned free-information regime;
- M: delivery of the visual cue (in Free-Cue M=1,
  whereas in Regular M equals voluntary landing);
- D: voluntary approach/landing;
- T: sensing/decision/action timeline;
- Y: correctness;
- R: actual reward/payoff.

A randomized Z can identify the total **policy-offer**
effect on Y. It does not identify the mediation effect
M -> Y while holding D, T and reward consequences fixed.
Neither can it directly evaluate the adaptive-gain
control value

\[
G=E_O[\max\{P(O),Q(O)\}]
  -\max\{E_O P(O),E_O Q(O)\},
\]

where P is a fully optimized **no-new-information** timing
policy and Q is a paid optional query with post-cue timing
optimization. The Free-Cue arm grants information
automatically, whereas the conditional-Q strategy must
decide whether to seek it from previous information.
The key comparator and state-transition observations
are missing from this dataset.

Crucially, the original preprint has already reported high
accuracy in Free-Cue trials and proactive information seeking
across difficulty; **do not claim discovery priority** for
the positive offered-cue accuracy association. The useful
new output here is a pinned, trial-weighted and
bee-clustered independent audit with a formal distinction
between trial-regime ITT and optional information-acquisition
value.

## Operational next experiment

To distinguish source of gain, independently randomize
(1) a nonrewarding informative signal,
(2) a time- and motor-matched uninformative SHAM signal,
(3) a no-new-information PASSIVE condition permitting
the animal to choose its action time.

Use a programmed environmental state process that can switch
*between initial cue and final action*. Calibrate the
old cue, new-cue error, and real switching rates. Allow a
voluntary query action and adaptive waiting both before
and after new information, with action/reward and actual
state timestamped in the **same experimental encounter**.

Pre-register and validate separately:
- signal-delivery ITT (this source estimates a related
  baseline but with a different protocol),
- information-only change in final choice at matched time,
- conditional acquisition control premium against an
  optimal passive-timing competitor and universal query,
- follow-on timing and ultimately fitness/reproductive
  consequences. Require held-out animals/colonies and
  cluster-aware uncertainty for policy value selection.

Without these interventions, DO NOT relabel the published
offered-cue result as direct test of the V6 exact
finite routing frontier or evolutionary selection.

## Reproducibility

Standard-library reproduction, no third-party raw data redistributed:
- scripts/audit_bee_2026_random_free_cue_accuracy.py
- tests/test_bee_2026_random_free_cue_accuracy.py
- validation/bee_2026_random_free_cue_accuracy_v1.json

The script verifies raw bytes by exact Git-blob SHA if requested,
and can compare deterministic statistical outputs to the
frozen JSON. Do not treat bootstrap percentile intervals as
exact randomization-based confidence intervals.
