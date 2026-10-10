# Trial identity is not shared between bee information-request and latency files

**Status:** empirical source audit and STOP gate for adaptive-gain PR #67.
Source: He et al. (2026), *Uncertainty-Guided Decision-Making in Bumble Bees*,
bioRxiv DOI [10.64898/2026.09.15.751944](https://doi.org/10.64898/2026.09.15.751944).
The raw observations belong to their original repository
[Cuixiaojian21/bee_metacognition](https://github.com/Cuixiaojian21/bee_metacognition),
commit 7f886394b4de872ecdb19ca4ea214ec321d5dce9.

This note does **not** assert that the original authors have performed an
invalid join. It prevents a particular *proposed reanalysis of these public
files* from doing so.

## The joining problem

The available trial-level files are:
- data/4_active_information_seeking_trials.csv: information request / platform
  landing / subsequent discrimination.
- data/3_decision_process_metrics.csv: decision latency and antennal tapping
  in a different behavioral task.

Both datasets contain 192 individual IDs and 19,200 rows (100 trials per bee).
When pairing on the apparently precise triple
(Trial_ID, Bee_ID, Trial_Number), **every one of 19,200 keys matches.**
However, for 12,399 of those pairs (**64.578125%**) the task difficulty
is **different**. Only 6,801 have matching difficulty, which does NOT
establish they are the same physical trial.

A concrete example:

| Key | Information-seeking file | Latency file |
|---|---|---|
| Trial_ID=1, Bee_001, Trial_Number=1 | Easy, Regular, no platform landing | Hard, decision latency 2565.1 ms |
| Trial_ID=2, Bee_001, Trial_Number=2 | Hard, Regular, no platform landing | Hard, decision latency 2501.6 ms |
| Trial_ID=3, Bee_001, Trial_Number=3 | Impossible, Regular, landed | Easy, decision latency 1583.6 ms |

Matching one of these labels coincidentally (trial 2) is insufficient.
The numerical identifiers encode local ordering *within an experiment*,
not a globally unique encounter/session key.

The observed difficulty confusion among the 19,200 nominal join pairs is:

| Active task difficulty | Timing Easy | Timing Hard | Timing Impossible |
|---|---:|---:|---:|
| Easy | 2,990 | 3,133 | 1,557 |
| Hard | 3,053 | 3,051 | 1,576 |
| Impossible | 1,582 | 1,498 | 760 |

Any regression that assigns the latency of timing-file trial 1 to the
information request of active-file trial 1 manufactures paired observations.
It cannot identify whether buying an extra cue changes decision latency.

## What the raw active-information data *do* support

The other public source audit is in
validation/bee_2026_active_information_schema_audit_v1.json.
It records 192 bees x 100 trials; every bee has exactly 20
Random_Free_Cue trials and 80 Regular trials.

In Free-Cue trials, Info_Requested=1 indicates information *delivery*,
not necessarily a voluntary request/landing. There are 1,812 Free-Cue trials
with no landing despite Info_Requested=1. Regular-trial requests are best
operationalized as Actually_Landed_On_Platform and retain the authors'
difficulty-dependent pattern.

The Free-Cue trials are distributed across trial numbers 1--100, and
the sign of Free-minus-Regular platform landing holds in all five
20-trial blocks: positive for Easy and Hard, negative for Impossible.
This is a coarse temporal-order sensitivity check, not proof of
random assignment or a causal treatment effect.

## A limited possible alternative: individual-level association

If Bee_ID refers to the same individual across experimental files, it is
permissible to *explore* correlations of **per-bee summaries** from the
two tasks, with independent sample denominators. A pinned exploratory
192-bee analysis stratified by difficulty found the following:

| Difficulty | Per-bee Regular request rate vs per-bee latency in other task: Pearson r | Permutation two-sided p |
|---|---:|---:|
| Easy | 0.0023 | 0.9732 |
| Hard | 0.0612 | 0.3895 |
| Impossible | 0.0336 | 0.6441 |

The permutation samples individual labels (5,000 shuffles, fixed seed);
trials are never treated as independent subjects. These are unadjusted
exploratory correlations across different tasks and have no evidence of
a large monotone individual-level association. They do not prove a
zero relationship, and they **cannot** substitute for the missing
within-trial cost of information.

## Source and experimental boundary

The original preprint already demonstrated voluntary information
request in bumblebees under an experimentally imposed sucrose
reward reduction, and has separate controls concerning task
difficulty. That existing scientific accomplishment is not negated
by a warning about reusing nonmatching public file IDs.

The adaptive-gain question is substantially narrower:
does **fresh, optionally purchased information** change *when to
act and what to do*, relative to both
(i) an old-cue-conditional policy that waits optimally without buying
information and (ii) a fixed universal-query policy?

That requires old and fresh cue timestamps, actual state transitions,
request decision, optional post-query waiting, terminal choice and
reward **all within the same experimental encounter**.
These particular two source CSVs do not provide that joint table.

A future randomized PASSIVE / SHAM / INFORMATIVE assay must give
every encounter a namespace-safe identifier including study,
condition, session and subject; retain requested versus delivered
information separately. Its randomization and comparison policy
must be frozen before outcome exposure.

## Reproduction and stop rule

- scripts/audit_bee_2026_cross_experiment_join.py
  reads the two original unmodified CSVs provided as local input,
  detects the mismatching joins, checks trial order and computes
  exploratory per-bee correlations using deterministic
  bee-level label permutations.
- tests/test_bee_2026_cross_experiment_join_gate.py
  uses only synthetic example records to protect against accidental
  cross-experiment trial joins; raw third-party data are not copied.
- validation/bee_2026_cross_experiment_join_gate_v1.json
  freezes the observed counts and claim ceiling with source blob IDs.

**STOP:** no fitted effect of "information request on decision latency"
may be promoted from joining these two files on reused Trial_ID or
Bee_ID + Trial_Number. An exact matching difficulty is necessary but
still not sufficient to establish shared trial identity.

**GO:** retain the source as a behavioral feasibility anchor and use
the prospective matched-time experiment in
biology/PREREG_BUMBLEBEE_INFO_VERSUS_TIMING_V1.md
for a valid test of the dynamic ecological hypothesis.

V6's original three structural/fitness results remain unchanged.
