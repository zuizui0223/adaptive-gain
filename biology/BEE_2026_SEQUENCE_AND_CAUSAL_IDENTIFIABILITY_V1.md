# Bee information acquisition: sequential behavior is observable, its fitness benefit is not identified

**Status:** independent public-data exploratory audit and partial-identification
stress test for adaptive-gain PR #67, not V6 MAIN 4 or an independently
confirmed evolutionary selection mechanism.

## Primary sources and integrity

He et al. (2026), "Uncertainty-Guided Decision-Making in Bumble Bees,"
bioRxiv DOI https://doi.org/10.64898/2026.09.15.751944.
Public code/data: https://github.com/Cuixiaojian21/bee_metacognition
at pinned commit 7f886394b4de872ecdb19ca4ea214ec321d5dce9.
Main trial CSV: data/4_active_information_seeking_trials.csv,
Git blob 26259c9071c6d73141d56b9bedd396cab1a04491.

This dataset has 19,200 trials from 192 bees (100 trials/bee):
15,360 Regular voluntary-information trials and 3,840
Random_Free_Cue trials (20 each bee).
The authors report uncertainty-sensitive, voluntary, costly
information seeking, so **that behavior is prior art**, not
a new claim of adaptive-gain.

Two semantics must remain separate:
- On Regular trials, an information request means actually
  landing on the information platform and receiving a cue.
- On Free-Cue trials, information is automatically delivered.
  Info_Requested=1 for *all* such trials even when the bee
  does NOT land on the platform. A total of 1,812 Free-Cue
  trials have delivery without landing.

Never fit active requesting across the pooled two conditions
using Info_Requested as a universal voluntary response.

The public decision-latency experiment is different.
Although the separate latency file repeats all 19,200 numeric
Trial_ID/Bee_ID/Trial_Number triplets, the difficulty is different
in 12,399 (64.578%) nominal matches. Consequently no trialwise
regression of request action against "that trial's decision
latency" is permitted from these cross-task tables.

Detailed previously frozen audits:
- validation/bee_2026_active_information_schema_audit_v1.json
- validation/bee_2026_cross_experiment_join_gate_v1.json

## Exploratory within-experiment trial sequence: previous failure

Within the single *active-information* experiment, sort trial
number within each Bee_ID. Restrict lag pairs to the 12,132
instances in which both previous and current trials are
consecutive Regular trials. The outcome is actual platform
landing in the CURRENT trial, grouped by current difficulty.
The exposure is whether the PREVIOUS trial was incorrect.

A descriptive adjusted contrast compares previous failure
with previous success after forming cells by previous
difficulty, whether the previous animal requested information,
and current trial-order quintile (20 trial numbers).
Within each current difficulty, differences in landing rate
are standardized using the cell sizes for cells containing
both previous successes and failures. Resample the 192
individual bees in 1,500 bootstrap replicates.

| Current difficulty | Raw previous failure − success | Adjusted contrast | Bee-cluster bootstrap 95% |
|---|---:|---:|---:|
| Easy | +0.000717 | +0.005997 | [-0.01961, +0.03413] |
| Hard | -0.024311 | -0.029722 | [-0.07674, +0.01043] |
| Impossible | +0.009380 | -0.000198 | [-0.05538, +0.05032] |

No consistent positive one-trial error effect is demonstrated.
All intervals include zero; neither no-effect equivalence nor
absence of longer-horizon learning is established. A previous
error is not randomized, and the cell standardization
does not control unmeasured motivation or bee states.

## Exploratory prior Free-Cue exposure and the next Regular request

Retain all 15,205 current Regular trials preceded by a
consecutive trial of either type. Compare current platform
landing when the previous assignment was Random_Free_Cue
versus Regular. The adjusted cells use previous difficulty,
previous correctness and trial-order quintile. Bootstrap
bees, not individual rows, 1,500 times.

| Current difficulty | Raw prior Free − Regular | Adjusted contrast | Bee-cluster bootstrap 95% |
|---|---:|---:|---:|
| Easy | +0.008299 | +0.020636 | [-0.00328, +0.05177] |
| Hard | +0.000820 | -0.000204 | [-0.04155, +0.04285] |
| Impossible | +0.009942 | +0.038541 | [-0.01113, +0.07438] |

Again, all intervals include zero. The prior trial condition
potentially alters cue presentation, previous reward,
salience and motor behavior jointly. Even if the source
calls the 20% Free-Cue schedule randomly interleaved,
this does NOT by itself isolate information-only carryover.

The striking current-trial baseline is already the authors'
published gradient in Regular requests: Easy 591/6140 =
0.09625; Hard 2866/6108 = 0.46922; Impossible
2229/3112 = 0.71626. The new lagged observations do
not turn this existing result into evidence of evolutionary
routeability.

Reproducible standard-library-only sequence script:
scripts/analyze_bee_2026_lagged_acquisition.py,
synthetic tests tests/test_bee_2026_lagged_acquisition.py,
frozen public summary
validation/bee_2026_lagged_request_exploratory_v1.json.
No third-party raw data are republished in this repository.

## The stronger limitation: binary causal accuracy sign unidentifiable

Define A=1 when a bee voluntarily purchases a cue on a
Regular trial, and binary Y=1 when its terminal choice is
correct. The public file gives correct/incorrect outcomes
after requests and nonrequests, but no observed counterfactual
for the same encounter.

By consistency, with no randomization, ignorability or
monotonic treatment response assumption, the missing
potential-outcome Y(1) for A=0 and Y(0) for A=1 can each
be either zero or one.

Let n11 = number with A=1,Y=1; n10 with A=1,Y=0;
n01 with A=0,Y=1; n00 with A=0,Y=0, and
N=n11+n10+n01+n00. The sharp elementary missing-
counterfactual bounds on the sample average effect are

\[
\boxed{
\frac{n_{11}-n_{01}-(n_{11}+n_{10})}{N}
\le \overline{Y(1)-Y(0)}
\le
\frac{n_{11}+(n_{01}+n_{00})-n_{01}}{N}.
}
\]

They can be attained by explicit assignment of all missing
potential outcomes to zero or one. These are identification
bounds, NOT confidence intervals for population uncertainty.

| Regular difficulty | Correct if requested | Correct if not requested | Naive association (percentage points) | Sharp causal sample-effect bounds |
|---|---:|---:|---:|---:|
| Easy | 555/591=93.9% | 4163/5549=75.0% | +18.9 | [-68.4, +31.6] pp |
| Hard | 2662/2866=92.9% | 1600/3242=49.4% | +43.5 | [-29.5, +70.5] pp |
| Impossible | 2073/2229=93.0% | 183/883=20.7% | +72.3 | [-10.9, +89.1] pp |

**Even the sign of the effect of the animal's self-selected
request on correct choice is not identified by these Regular
trials.** This does NOT refute the preprint's separate
random Free-Cue intervention or observed cue-guided choice
accuracy. It sharply limits what can be inferred from
"requested versus did not request" observational correctness
rates alone.

The randomized or interleaved Free-Cue condition supplies
a **different intervention**: automatic cue delivery.
Observed correctness rates in Free-Cue trials are about
94.9%, 94.3% and 92.6% for Easy, Hard and Impossible.
An intention-to-treat offer contrast may be useful if
assignment procedures are independently verified, but
it does NOT identify the controlled effect of an
animal actively purchasing the cue. The exposure has
changed, and potential motor/attention/reward pathways
must be addressed.

Implementation:
adaptive_gain/partial_identification.py,
scripts/audit_bee_2026_request_accuracy_bounds.py,
tests/test_bee_2026_request_accuracy_bounds.py,
validation/bee_2026_request_ate_bounds_v1.json.
Do not publish an "information increases accuracy by
72.3 percentage points" causal claim based on the naive
Impossible-trial conditional success contrast.

## What remains genuinely open for adaptive-gain

Neither the one-trial behavioral history nor the partial
identification boundary validates:
1. Information *age* relative to independently logged
   state transitions in the payoff-relevant environment;
2. Optional fresh-query policy choice against both
   **optimal no-cue waiting** and matched-duration
   uninformative sham querying;
3. The value of the query for *subsequent cue acquisition*
   and *post-query decision timing*, including terminal
   reward, within one encounter;
4. Heritable architecture differences and fitness costs
   needed to infer evolutionary selection.

The pre-registered prospective plan is in
biology/PREREG_BUMBLEBEE_INFO_VERSUS_TIMING_V1.md.
Read the existing 2017 fluctuating nectar study (Dunlap,
Papaj & Dornhaus) and the 2026 information-purchase
preprint as near prior art. Proposed contribution is a
narrow intervention with matched control and a natural
ecological mechanism, not the claim that bees newly
discovered information seeking or uncertainty sensitivity.

**Decision:** STOP promoting the public-data gradient,
lagged association or naive correctness differences as
evidence for the dynamic adaptive routeability theorem.
This empirical archive supplies assay feasibility and
identification stress tests, not its selective-fitness
confirmation. V6 MAIN 1–3 remain unchanged.
