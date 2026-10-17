# Bee-level randomized cue-access experiment: minimal pilot protocol v1

**Status:** Prospective *artificial-flower* protocol and runnable data-quality/analysis intake for adaptive-gain PR #68. No real trials have been collected in this artifact. No fitness, natural selection, inferred rewiring, or mechanism of endogenous sensory attention is claimed. The frozen submission manuscripts remain unchanged.

## Biological question and treatment contrast

**Question:** With the same two-acquisition opportunity limit and known target reward, does allowing a flower visitor to select the *identity of the second cue conditional on the first observed cue* increase its probability of making a correct final target choice before the deadline, relative to a matched-cost precommitted cue schedule?

- **Contingent-access arm:** within the same two-cue budget, the next cue is chosen according to the previous visible cue report (or response-dependent availability). Participants may decline the offered next query or make an early final choice, provided the pre-registered treatment protocol makes the difference from fixed access explicit.
- **Precommitted arm:** the next-cue order is selected before seeing its first outcome; **final target choice may still depend on all acquired evidence and may be withheld**. The control must not be artificially handicapped by a universal-bundle completion requirement or a prohibition on guessing.
- **Assignment unit:** individual **bee**, once per pilot (no crossovers). Randomize bees within each colony to both arms with precomputed allocation counts. The colony is a blocking stratum; a bee's multiple trials are **not** independently randomized experimental units. Record the randomization sequence and maintain its immutable, pre-outcome roster.
- **Colony interference gate:** treatment spillover between bees (social learning, depleted/replenished feeders, odor marking) would violate the individual-unit no-interference assumption. If spillover cannot be prevented, use a genuinely colony-randomized design instead; the attached bee-level inference is then invalid and must not be reused.
- **Trial schedule:** predefine a fixed number `N` of target presentations (slots) per enrolled bee, including target allocation and deadline. **Every** bee from the assignment roster gets exactly `N` rows. An unrun, dropout, occluded or technical-failure slot is recorded as `unobserved` with a reason, rather than silently excluded. Pilot dropout can therefore widen uncertainty but cannot disappear from the denominator.

## Primary endpoint and estimand

The primary endpoint per slot is **verified correct final target action by the prespecified deadline**:

- `choice` with `final_action=target` = 1;
- observed wrong `choice`, or verified no action `abstain` by the deadline = 0;
- `unobserved` = unknown binary outcome, `[0,1]` for sensitivity.

This is a **successful-action probability** estimand, not a reward/fitness estimator. If the no-choice opportunity cost or energetic costs are biologically important, preregister a separate reward-based endpoint with measurements; do not retrofit the `L` or `K` of synthetic benchmarks as observed costs.

Define each bee's outcome as the mean of its **N planned slots**, not the mean of its *successfully recorded* choices. Average bees equally within each colony × assigned arm, then average colony-specific contrasts with weights equal to each colony's proportion of the enrolled bee roster. The signed contrast is **assigned contingent minus assigned precommitted**, i.e. bee-level **intention to treat (ITT)**. Actual access delivered, query sequence, learning and whether a bee used contingent options are reported as fidelity/process outcomes but must not redefine the randomized treatment arm.

For unknown outcomes, independently complete them with 0 or 1 to construct the exact lower/upper endpoints of the **observed, block-standardized ITT point-score**. They are not confidence or credible intervals for any population effect. Show the intervals beside missing fractions and counts. Do not claim a positive sign if they include zero.

If all planned outcomes are observed, an optional **two-sided exact within-colony bee-label permutation test** enumerates all assignments preserving the number of bees originally allocated to each arm within each colony. It tests Fisher's **sharp no-treatment-effect null** on enrolled bees' fixed scheduled-slot outcomes under the actual blocked randomization design and absence of between-bee interference. Its p-value does not test the weaker 'average treatment effect is zero' null in general, and is **not** a confidence interval. The code refuses the test when a slot is unobserved or the assignment space exceeds its stated computational cap; it never substitutes trials for bees as exchangeable units.

## Required datasets and retention

1. **Pre-enrolled allocation roster (`bee_roster.csv`)**, one row per bee, immutable before its first exposure: `bee_id,colony_id,assigned_access`, where arm is `contingent` or `precommitted`. Archive the randomization plan and sequence generation method separately. Every colony analyzed by this bee-randomized blocked specification must contain both arms.
2. **Scheduled trial log (`bee_trials.csv`)**, one row per `bee_id × slot` even if the bee drops out: `trial_id,bee_id,slot,target,outcome_status,final_action,unobserved_reason,delivered_access`. Only `choice`, `abstain`, and `unobserved` are valid statuses; if `unobserved`, reason is mandatory. `final_action` is 0/1 only for `choice`; leave it blank for the other statuses. `delivered_access` records what the apparatus actually offered (`contingent`, `precommitted`, `not_delivered`, or blank/unknown).
3. **Recommended raw metadata**, additional CSV columns or linked video/behavior tables: original video/frame ID, scorer and blinded review outcome, target-generation/randomization record, cue identities and visible/independently calibrated reports in order, branch choice, start and deadline timestamps, action latency, colony, sex/caste if known, learning block, reward history, environmental context, apparatus failure type and intervention compliance. The minimal Python CLI deliberately does **not** silently use these fields as primary-model covariates. Keep original recordings and full metadata for independent behavioral mechanism analyses.

The primary endpoint requires a known target. A camera-derived visit without independently known target truth is not enough; a final choice is also not a direct measure of an internally perceived cue bit. Scorers should be blinded to assigned access when possible, with preregistered adjudication of uncertain video. An observed timeout requires **clear proof of an available opportunity and complete recording through the declared deadline** before calling it `abstain` rather than `unobserved`.

## Reproducible intake and exact small-sample example

The example CSVs in `experiments/templates/` are **synthetic fixtures**: 8 individual bee identifiers, 2 colony strata, 4 planned slots per bee, 32 rows. No animal behavior is represented. Run from the repository root:

```bash
python -m adaptive_gain.pilot_itt \
  --roster experiments/templates/pilot_bee_roster_example.csv \
  --trials experiments/templates/pilot_trial_log_example.csv \
  --planned-trials-per-bee 4 \
  --exact-randomization
```

Expected synthetic results: 4 bees per arm, 18 correct target choices out of 32 scheduled trials, arm success rates 0.750 and 0.375, colony-block-standardized ITT contrast **+0.375**, and exact two-sided Fisher sharp-null p-value **1/9** over **36** within-colony bee assignment configurations. A large displayed effect but weak exact evidence in a tiny demonstration is not an estimate of pollinator behavior, a sample-size calculation, or a reason to infer a confirmed effect.

The test harness also demonstrates that technical missingness produces **outcome completion bounds** and suppresses the exact permutation test; confirmed abstentions count as 0 rather than missing. Entirely disappeared bees or planned slots without rows cause a hard failure. Cross-arm apparatus delivery is retained in the ITT assignment group but reported as noncompliance. Confirmed apparatus nondelivery (`not_delivered`) and missing delivery information (blank) are **counted separately** rather than conflated.

## Implementation gates / decision rules

- **GO for a feasibility pilot:** cue reports and final target actions can be scored reliably; the randomization roster is locked; actual offered cue modes are logged; required planned slots including missing are kept; at least one contingent and one fixed bee per colony; resource and time budgets are physically matched across treatments.
- **STOP primary analysis:** absent randomized roster, ambiguous final action versus technical occlusion, outcome-based removal of whole bees, no known target, crossed colony-only randomization, or unverified consistency/interference. The CLI's success is not itself validation of randomization, independence, treatment delivery or detection.
- **STOP significance claim:** any missing slot (report bounds, no exact p), changes to the declared N/trial target schedule after outcomes, or reanalysis that treats observed trials as independent bees. Small observed differences or non-significant p-values should not be interpreted as biological equivalence.
- **Secondary exploratory analyses:** stage-specific query order, response to observed first cue, wrong choice versus no choice, elapsed acquisition time, learning trajectories, treatment fidelity. Use bee/colony clustering and a holdout for learned cue policies. Specify multicomparison policy before confirmatory data. Do not condition the primary ITT on realized cue choice, because it occurs after randomization.
- **Before a confirmatory trial:** determine attainable bee numbers, observed within-bee correlation, colony effects, recording losses, training mastery, minimal biologically meaningful ITT effect and welfare limits from a pilot. Preregister the actual sample size/power and analysis plan; the synthetic effect 0.375 is **not** a justified power effect size.

## What this analysis cannot establish

This experiment tests **behavioral value of experimental access to contingent cues**. A positive ITT effect does not establish the finite-theory exact optimum, cue-state conditional error distribution, inherited variation, invasion fitness or natural selection. To attribute success specifically to routeability rather than greater attention or simpler stimuli, document actual cue histories, independent cue-reliability reports and matched effort, and perform the complementary randomized fixed-versus-contingent cue-order calibration. Ecological interaction rewiring also requires a separate detection-aware process model.

## Prior methods and ecological reporting

- ARRIVE 2.0 Essential 10 require explicit experimental unit, randomization, sample-size, outcome, exclusions and blinding reporting. https://arriveguidelines.org/arrive-guidelines
- Wu & Ding (2021), *Randomization Tests for Weak Null Hypotheses in Randomized Experiments*, JASA, https://doi.org/10.1080/01621459.2020.1750415, distinguishes the sharp-null Fisher exact test implemented here from more difficult weak-average-null inference.

These are established practices, **not** proposed new theorems. The addition supplies a concrete observation-to-analysis bridge for the ecological test in this repository.
