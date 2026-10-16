"""Missing-action audit for a prespecified randomized second-cue policy.

Separate OBSERVED ABSTENTION from UNOBSERVED trial outcome. A confirmed no-choice
is scored zero only under the *declared* payoff convention. Unobserved outcomes
are bounded over all admissible actions (including an error) rather than dropped.

The resulting endpoints are sharp missing-completion bounds on the realized
Horvitz--Thompson (HT) *sample score*. They are NOT population identification
intervals, confidence intervals, estimates of fitness, or bee-level SEs.
The external randomization/consistency assumption is not verified by this code.
"""
from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Mapping, Sequence
import math


@dataclass(frozen=True)
class ActionOutcomeTrial:
    trial_id: str
    bee_id: str
    target: int
    context_bit: int
    second_cue: int
    assignment_probability: float
    outcome_status: str
    final_action: int | None


@dataclass(frozen=True)
class ActionOutcomeBoundReceipt:
    randomized_trials: int
    unique_bees: int
    matched_trials: int
    matched_choices: int
    matched_correct: int
    matched_wrong: int
    matched_abstentions: int
    matched_missing: int
    matched_by_context: tuple[tuple[int, int], ...]
    lower_ht: float
    upper_ht: float
    width: float
    ess_matched: float
    estimator: str = "finite_sample_HT_missing_outcome_completion_bounds"


def bound_randomized_action_policy(
    trials: Sequence[ActionOutcomeTrial],
    context_to_query: Mapping[int, int],
    *,
    correct_reward: float = 1.0,
    error_cost: float = 0.0,
) -> ActionOutcomeBoundReceipt:
    """Bound HT action reward for a prespecified A->B/C policy.

    Design: within each observed first-cue bit A=a, the second cue J in {1,2}
    is experimentally randomized with a known, positive assignment probability
    mu(J|A=a) in the record. The estimate includes all randomized trials in the
    denominator. Recorded 'choice' actions are correct/wrong using known target;
    'abstain' is a confirmed no-choice with assigned payoff 0; 'unobserved'
    means final behavior could not be scored and contributes [-L,v] when its
    assigned cue matches the evaluation policy. No imputation or exclusion.

    Bound endpoints are EXACT over the missing outcomes of the observed matched
    HT score; sampling/randomization uncertainty is entirely separate. Do NOT
    interpret as statistically valid bounds on the unknown population policy
    value unless the design conditions, large-sample convergence, and coverage
    uncertainty are independently established. No causal guarantee is checked.
    """
    if not isinstance(context_to_query, Mapping) or set(context_to_query) != {0, 1} or (
        any(type(context_to_query[c]) is not int or context_to_query[c] not in (1, 2)
            for c in (0, 1))
    ):
        raise ValueError('policy must map contexts 0 and 1 to B=1 or C=2')
    if not trials:
        raise ValueError('at least one randomized trial required')
    v, loss = float(correct_reward), float(error_cost)
    if not math.isfinite(v) or v <= 0 or not math.isfinite(loss) or loss < 0:
        raise ValueError('correct_reward must be positive and error_cost nonnegative and finite')

    seen_ids: set[str] = set()
    seen_bees: set[str] = set()
    context_counts = {0: 0, 1: 0}
    matched_by_context = {0: 0, 1: 0}
    matched_choice = matched_correct = matched_wrong = matched_abstain = matched_missing = 0
    lower_contrib: list[float] = []
    upper_contrib: list[float] = []
    importance_weights: list[float] = []

    for trial in trials:
        if not isinstance(trial.trial_id, str) or not trial.trial_id.strip():
            raise ValueError('trial_id must be nonempty string')
        if trial.trial_id in seen_ids:
            raise ValueError('duplicate trial_id')
        seen_ids.add(trial.trial_id)
        if not isinstance(trial.bee_id, str) or not trial.bee_id.strip():
            raise ValueError('bee_id must be nonempty string')
        seen_bees.add(trial.bee_id)
        if any(type(x) is not int or x not in (0, 1)
               for x in (trial.target, trial.context_bit)):
            raise ValueError('target and context_bit must be binary integers')
        if type(trial.second_cue) is not int or trial.second_cue not in (1, 2):
            raise ValueError('second_cue must be integer 1 or 2')
        probability = float(trial.assignment_probability)
        if not math.isfinite(probability) or not 0 < probability <= 1:
            raise ValueError('known positive assignment propensity required')
        if trial.outcome_status == 'choice':
            if type(trial.final_action) is not int or trial.final_action not in (0, 1):
                raise ValueError('choice status requires a valid final target action')
        elif trial.outcome_status in ('abstain', 'unobserved'):
            if trial.final_action is not None:
                raise ValueError('abstain/unobserved status requires final_action=None')
        else:
            raise ValueError('invalid outcome status: choice/abstain/unobserved only')
        a = trial.context_bit
        context_counts[a] += 1
        if trial.second_cue != context_to_query[a]:
            continue
        matched_by_context[a] += 1
        w = 1.0 / probability
        if not math.isfinite(w) or w <= 0:
            raise ValueError('inverse probability weight overflow')
        importance_weights.append(w)
        if trial.outcome_status == 'choice':
            matched_choice += 1
            if trial.final_action == trial.target:
                matched_correct += 1
                value = v
            else:
                matched_wrong += 1
                value = -loss
            lower_contrib.append(w * value)
            upper_contrib.append(w * value)
        elif trial.outcome_status == 'abstain':
            matched_abstain += 1
            lower_contrib.append(0.0)
            upper_contrib.append(0.0)
        else:
            matched_missing += 1
            lower_contrib.append(-w * loss)
            upper_contrib.append(w * v)

    if any(context_counts[a] == 0 or matched_by_context[a] == 0 for a in (0, 1)):
        raise ValueError('insufficient observed support for policy in both contexts')
    denom = len(trials)
    lower = math.fsum(lower_contrib) / denom
    upper = math.fsum(upper_contrib) / denom
    mass = math.fsum(importance_weights)
    ess = mass**2 / math.fsum(w*w for w in importance_weights)
    return ActionOutcomeBoundReceipt(
        randomized_trials=denom,
        unique_bees=len(seen_bees),
        matched_trials=len(importance_weights),
        matched_choices=matched_choice,
        matched_correct=matched_correct,
        matched_wrong=matched_wrong,
        matched_abstentions=matched_abstain,
        matched_missing=matched_missing,
        matched_by_context=tuple(sorted(matched_by_context.items())),
        lower_ht=lower,
        upper_ht=upper,
        width=upper-lower,
        ess_matched=ess,
    )
