# Public evidence gate for cue-age, environment-age and payoff-age

Status: source-schema and experimental-design triage, **no newly fitted field result**.
Only promote data to V6 if the same study provides the intervention and
performance endpoints required by the precise claim.

## Three different ways a cue becomes less useful

1. **Physical degradation**: cue concentration or detectability decays,
   even if the underlying environmental state is unchanged.
2. **Environmental staleness**: the external state changes after the
   signal is produced or observed, even if the signal is physically
   intact.
3. **Decision-value expiry**: the signal still changes beliefs but no
   longer changes the optimal action under the biological payoff
   matrix and background frequencies.

These have different causes; detecting one does not validate the other.
In the present two-state CTMC with reward contrast gaps r0,r1,
third-layer incremental value is
V(t)=[(r0+r1)pi0*pi1*exp(-kt)-B]_+,
where B is the Bayes action-threshold offset defined in
REWARD_WEIGHTED_CUE_EXPIRY_V1.md.

## Existing public data and eligibility

| Source | Actual observed intervention and endpoints | Identification decision |
|---|---|---|
| Lönnstedt et al. (2013), "Degradation of chemical alarm cues and assessment of risk throughout the day", https://pmc.ncbi.nlm.nih.gov/articles/PMC3810885/ | Coral reef damselfish experiment with chemical alarm cues aged 0,10,20,30 min; antipredator avoidance; 70-72 fish per age treatment. Exposure time of day varied. | Direct evidence for age-dependent *physical cue effectiveness*, not necessarily environmental switching or reward-weighted Bayes action expiry. Raw individual open-data receipt not established. |
| Baracchi et al. (2016), "Copy-when-uncertain: bumblebees rely on social information when rewards are highly variable", https://doi.org/10.5061/dryad.3jb68 | Public Dryad bee landings: treatment group, social/non-social cue type, flower rewards, visits and first/last landing time. | Public behavioral source for cue-utilization conditional on reward variability; does **not** isolate timestamped prior information expiry or evolved architecture fitness. |
| Yi et al. (2025), "Selective engagement of prefrontal VIP neurons in reversal learning", https://doi.org/10.5061/dryad.pk0p2ngzs | Public Dryad MATLAB example sessions and larger ZIPs; README declares odorCue, outcomeIdentity, outcomeProbability, stateTime, waterReward, reversal metadata. | Trial-level reward-contingency updating; not a clean manipulation of cue-to-decision age while holding state transition and payoff constant. No row-level empirical fit completed. |
| Kato-Namba et al. (2025) mosquito multisensory VR, https://doi.org/10.1038/s41598-025-13427-z | Context-dependent sensory-response modulation; code/data cited in prior audit. | Sensory integration anchor, not a source for the full decision-value expiry threshold. |
| Chandel et al. (2024) Aedes cue time course, https://doi.org/10.1038/s41586-024-07848-5 | Host-seeking behavior before/during/after CO2, IR and odor cue combinations. | Temporal aggregate response anchor, not independent estimates of environment switches and state-specific payoff gaps. |

All statuses concern the narrow *payoff-relevant information lifetime*
hypothesis, not whether a paper is otherwise ecologically valuable.

## Target biological experiment / minimum identifiable table

Unit: an individual encounter, with randomized schedule of cue presentation
and decision timing. Required fields:

- subject_id, trial_id, block_id, and individual random-effects metadata;
- cue_timestamp, cue_observation, physical_cue_age and cue_detectability;
- environment_state_cue_time, environment_state_action_time;
- randomized cue-to-action lag and recorded action_timestamp;
- choice, response latency, realized reward/loss and competing-action
  reward table (or experimentally controlled contrast costs);
- independent state-transition sample to estimate alpha, beta, occupancy pi;
- identical payoff/no-cue comparator, and optional fresh re-query condition;
- preregistered reward-gap treatment to vary theta while holding environment
  transition and state frequency constant.

If an observed response decreases for physically aged cues but state
transitions and payoff matrix are unrecorded, interpret as **sensory cue-age
effect only**. If actual state changes but reward contrasts are absent,
interpret as **state prediction / behavior**, not information decision
value. If a no-cue optimized baseline is missing, the estimated "information
benefit" is not identified.

### Discriminating predictions

P1. At fixed environment transitions, shift reward contrast ratio
d0/d1: the Bayes action-threshold theta moves and the intrinsic
decision-value cutoff moves accordingly (or becomes non-finite when
theta=pi1).

P2. Holding payoff constant, change physical cue detectability without
altering the cue-to-action environmental lag. Observed cue-usage
differences here cannot identify environmental turnover.

P3. Match state prevalence and measured stimulus mutual information
between two payoff treatments. The intrinsic action-value curves can
still differ, including zero versus positive value at identical cue age.

P4. Add a quantified per-decision usage debit K. Intrinsically
persistent decision value may still cease to be *economically* useful
at a finite lag; do not equate K with constitutive evolutionary
maintenance cost.

## Protocol before any manuscript claim

1. Download and checksum raw behavioral data.
2. Audit exact records and fields; distinguish per-trial data from
   only summarized group-level results.
3. Freeze a no-cue baseline, reward contrasts and age treatment
   *before* plotting the outcome.
4. Fit flexible empirical lag-dependent decision advantage first.
5. Compare the preregistered Markov/payoff model against non-Markov and
   physical-cue-decay controls with held-out animals or sessions.
6. State exactly which of P1-P4 was tested; no substitution of
   motor response with evolutionary fitness.

## Claim stop-rule

Neither the public damselfish cue-decay experiment, the Dryad bumblebee
study nor the mouse reversal datasets currently supplies a direct
single-system test of P1 under the required comparator semantics.
Do not fill this gap by plugging unrelated published quantities into
the same payoff equation and calling the result validated.

The near-term deliverable is a reproducible *mechanistic
falsification protocol*, not a newly claimed natural-history effect.
V6 MAIN 1--3 remain unchanged.
