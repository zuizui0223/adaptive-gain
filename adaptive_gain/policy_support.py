"""Audit a randomized second-cue report trial without off-support extrapolation.

This intentionally small estimator is for a *prespecified* two-stage cue policy:
context cue A is observed first; an externally randomized second cue B/C is
selected with recorded propensity; an independently elicited binary report is
compared against experimentally known target truth. A missing cue report blocks
evaluation rather than being interpreted as a behavioral abstention.

The Horvitz-Thompson estimate is unbiased for this hypothetical report-based
reward under correct logged randomization/consistency and observed reports.
There is no clustering/SE, model fitting, or claim of biological fitness.
"""
from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Mapping, Sequence
import math


@dataclass(frozen=True)
class CueReportTrial:
    trial_id: str
    bee_id: str
    target: int
    context_bit: int
    second_cue: int
    second_report: int | None
    assignment_probability: float


@dataclass(frozen=True)
class CuePolicyIPWReceipt:
    trials: int
    estimated_reward: float
    self_normalized_reward: float
    effective_sample_size: float
    total_matched: int
    matched_by_context: tuple[tuple[int, int], ...]
    estimator: str = 'HT_randomized_second_cue_prespecified_policy'


def evaluate_randomized_second_cue_policy(
    trials: Sequence[CueReportTrial],
    context_to_query: Mapping[int, int],
    *,
    correct_reward: float = 1.0,
    error_cost: float = 0.0,
) -> CuePolicyIPWReceipt:
    """IPW reward of one fixed policy mapping context bit to B/C.

    Recorded p is the *actual chosen cue's* randomization probability under
    the logged design. Without this probability or with unobserved policy
    arms, the estimate is refused. Every trial, including unmatched assigned
    cues, counts in the HT denominator. Observed no-report trials are not
    dropped; a missing binary cue report requires an observation model.
    Intervals/cluster uncertainty and policy learning are deliberately absent.
    """
    if dict(context_to_query) not in ({0: 1, 1: 1}, {0: 2, 1: 1},
                                      {0: 1, 1: 2}, {0: 2, 1: 2}):
        raise ValueError('policy must give a prespecified B/C choice for both contexts')
    if not trials:
        raise ValueError('at least one trial is required')
    v, loss = float(correct_reward), float(error_cost)
    if not math.isfinite(v) or v <= 0 or not math.isfinite(loss) or loss < 0:
        raise ValueError('correct_reward > 0 and error_cost >= 0 must be finite')

    policy = dict(context_to_query)
    ids: set[str] = set()
    contexts_seen = {0: 0, 1: 0}
    matches = {0: 0, 1: 0}
    contributions: list[float] = []
    weights: list[float] = []
    for trial in trials:
        if not isinstance(trial.trial_id, str) or not trial.trial_id.strip():
            raise ValueError('nonempty trial_id required')
        if trial.trial_id in ids:
            raise ValueError('duplicate trial_id')
        ids.add(trial.trial_id)
        if not isinstance(trial.bee_id, str) or not trial.bee_id.strip():
            raise ValueError('nonempty bee_id required')
        if trial.target not in (0, 1) or trial.context_bit not in (0, 1):
            raise ValueError('target and context must be binary')
        if trial.second_cue not in (1, 2):
            raise ValueError('second cue must be B=1 or C=2')
        if trial.second_report is None:
            raise ValueError('missing cue report; do not drop no-report trials')
        if trial.second_report not in (0, 1):
            raise ValueError('binary cue report required')
        prob = float(trial.assignment_probability)
        if not math.isfinite(prob) or not 0 < prob <= 1:
            raise ValueError('positive known assignment propensity required')
        contexts_seen[trial.context_bit] += 1
        if trial.second_cue == policy[trial.context_bit]:
            matches[trial.context_bit] += 1
            weight = 1.0 / prob
            reward = v if trial.second_report == trial.target else -loss
            contributions.append(weight * reward)
            weights.append(weight)

    if any(contexts_seen[c] == 0 or matches[c] == 0 for c in (0, 1)):
        raise ValueError('insufficient observed support for prespecified policy')
    n = len(trials)
    weighted = math.fsum(contributions)
    mass = math.fsum(weights)
    ess = mass * mass / math.fsum(w * w for w in weights)
    return CuePolicyIPWReceipt(
        trials=n,
        estimated_reward=weighted/n,
        self_normalized_reward=weighted/mass,
        effective_sample_size=ess,
        total_matched=sum(matches.values()),
        matched_by_context=tuple(sorted(matches.items())),
    )
