"""Pre-enrolled bee-level randomized policy-access pilot: ITT and audit gates.

Primary outcome: experimentally verified *correct target action* by the declared
trial deadline. Wrong actions and CONFIRMED no-choice are 0; technically unknown
final actions are bounded [0, 1], never deleted. This is *not* a fitness payoff.

Randomization unit: bee, assigned once (no crossover), blocked by colony.
Each enrolled bee must have a complete roster of prespecified trial slots; an
unrun/dropout slot is an explicit 'unobserved' trial with a reason. No bee may
quietly disappear from the analysis. Potential interference, assignment
fidelity, and biological percepts cannot be verified from the CSV fields.

A two-sided exact bee-level within-colony assignment-permutation test is offered
only for COMPLETE outcomes, under a sharp no-effect null and prespecified
fixed treatment counts per colony. No confidence intervals or sequential
causal identification claims are made by the permutation p-value.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from fractions import Fraction
from itertools import combinations, product
import json
import math
from pathlib import Path
from typing import Sequence

_ARMS = ("contingent", "precommitted")
_STATUSES = ("choice", "abstain", "unobserved")


@dataclass(frozen=True)
class PilotBee:
    bee_id: str
    colony_id: str
    assigned_access: str


@dataclass(frozen=True)
class PilotTrial:
    trial_id: str
    bee_id: str
    slot: int
    target: int
    outcome_status: str
    final_action: int | None
    unobserved_reason: str = ""
    delivered_access: str = ""


@dataclass(frozen=True)
class PilotITTReceipt:
    trials: int
    bees: int
    colonies: int
    planned_trials_per_bee: int
    contingent_bees: int
    precommitted_bees: int
    correct: int
    wrong: int
    abstain: int
    unobserved: int
    noncompliant_delivered_trials: int
    unknown_delivery_trials: int
    contingent_lower: float
    contingent_upper: float
    precommitted_lower: float
    precommitted_upper: float
    effect_lower: float
    effect_upper: float
    exact_randomization_p: float | None
    exact_randomization_assignments: int | None
    exact_randomization_status: str
    estimand: str = "colony_block_standardized_equal_bee_ITT_success_rate_difference"


def _nonempty(s, label):
    if not isinstance(s, str) or not s.strip():
        raise ValueError(f"{label} must be a nonempty string")


def _validate(roster: Sequence[PilotBee], trials: Sequence[PilotTrial], n: int):
    if type(n) is not int or n < 1:
        raise ValueError('planned_trials_per_bee must be a positive integer')
    if not roster:
        raise ValueError('a pre-enrollment bee roster is required')
    members: dict[str, PilotBee] = {}
    by_colony: dict[str, dict[str, list[str]]] = {}
    for bee in roster:
        _nonempty(bee.bee_id, 'bee_id')
        _nonempty(bee.colony_id, 'colony_id')
        if bee.bee_id in members:
            raise ValueError('duplicate bee_id in enrollment roster')
        if bee.assigned_access not in _ARMS:
            raise ValueError('assigned_access must be contingent or precommitted')
        members[bee.bee_id] = bee
        by_colony.setdefault(bee.colony_id, {a: [] for a in _ARMS})[bee.assigned_access].append(bee.bee_id)
    for colony, arms in by_colony.items():
        if any(not arms[a] for a in _ARMS):
            raise ValueError(f'{colony} must have both arms represented in enrolled bees')
    ids: set[str] = set()
    slots: dict[str, dict[int, PilotTrial]] = {b: {} for b in members}
    counts = {'correct': 0, 'wrong': 0, 'abstain': 0, 'unobserved': 0}
    n_mismatch = n_unknown_delivery = 0
    for trial in trials:
        _nonempty(trial.trial_id, 'trial_id')
        if trial.trial_id in ids:
            raise ValueError('duplicate trial_id')
        ids.add(trial.trial_id)
        if trial.bee_id not in members:
            raise ValueError('trial bee_id missing from pre-enrollment roster')
        if type(trial.slot) is not int or not 1 <= trial.slot <= n:
            raise ValueError('trial slot must be a planned integer from 1 to planned_trials_per_bee')
        if trial.slot in slots[trial.bee_id]:
            raise ValueError('duplicate planned slot for a bee')
        if type(trial.target) is not int or trial.target not in (0, 1):
            raise ValueError('experimental target must be binary 0/1')
        if trial.outcome_status not in _STATUSES:
            raise ValueError('outcome_status must be choice, abstain, or unobserved')
        if trial.outcome_status == 'choice':
            if type(trial.final_action) is not int or trial.final_action not in (0, 1):
                raise ValueError('choice requires observed final_action 0/1')
            if trial.unobserved_reason:
                raise ValueError('observed choice cannot have unobserved_reason')
            counts['correct' if trial.final_action == trial.target else 'wrong'] += 1
        elif trial.outcome_status == 'abstain':
            if trial.final_action is not None or trial.unobserved_reason:
                raise ValueError('confirmed abstain requires final_action=None and no missing reason')
            counts['abstain'] += 1
        else:
            if trial.final_action is not None:
                raise ValueError('unobserved trial must have final_action=None')
            _nonempty(trial.unobserved_reason, 'unobserved_reason')
            counts['unobserved'] += 1
        if trial.delivered_access not in ('', 'not_delivered') + _ARMS:
            raise ValueError('delivered_access must be one of contingent, precommitted, not_delivered, blank')
        if trial.delivered_access in ('', 'not_delivered'):
            n_unknown_delivery += 1
        elif trial.delivered_access != members[trial.bee_id].assigned_access:
            n_mismatch += 1
        slots[trial.bee_id][trial.slot] = trial
    required = set(range(1, n + 1))
    for bee, observed in slots.items():
        if set(observed) != required:
            raise ValueError(f'planned slot coverage incomplete for enrolled bee {bee}; create explicit unobserved placeholders')
    return members, by_colony, slots, counts, n_mismatch, n_unknown_delivery


def _rates(slots: dict[str, dict[int, PilotTrial]], n: int):
    intervals = {}
    for bee, planned in slots.items():
        yes = sum(t.outcome_status == 'choice' and t.final_action == t.target
                  for t in planned.values())
        missing = sum(t.outcome_status == 'unobserved' for t in planned.values())
        intervals[bee] = (Fraction(yes, n), Fraction(yes + missing, n))
    return intervals


def _weighted_contrast(by_colony, intervals):
    n_bees = sum(len(ids) for arms in by_colony.values() for ids in arms.values())
    high_arm = {'contingent': Fraction(0), 'precommitted': Fraction(0)}
    low_arm = {'contingent': Fraction(0), 'precommitted': Fraction(0)}
    for arms in by_colony.values():
        block_size = sum(len(bee_ids) for bee_ids in arms.values())
        w = Fraction(block_size, n_bees)
        for arm in _ARMS:
            rows = [intervals[b] for b in arms[arm]]
            low_arm[arm] += w * sum((low for low, _ in rows), Fraction(0)) / len(rows)
            high_arm[arm] += w * sum((high for _, high in rows), Fraction(0)) / len(rows)
    return low_arm, high_arm


def _exact_sharp_null_p(by_colony, outcomes, actual_effect, max_assignments):
    blocks = []
    assignment_count = 1
    for arms in by_colony.values():
        bees = tuple(sorted(b for group in arms.values() for b in group))
        n_contingent = len(arms['contingent'])
        assignment_count *= math.comb(len(bees), n_contingent)
        blocks.append((bees, n_contingent))
    if assignment_count > max_assignments:
        raise ValueError(f'assignment configurations {assignment_count} exceed max_assignments={max_assignments}')
    total_bees = len(outcomes)
    tables = []
    for bees, n_contingent in blocks:
        assignments = []
        weight = Fraction(len(bees), total_bees)
        for choice in combinations(bees, n_contingent):
            chosen = set(choice)
            treated = sum((outcomes[b] for b in bees if b in chosen), Fraction(0)) / n_contingent
            fixed = sum((outcomes[b] for b in bees if b not in chosen), Fraction(0)) / (len(bees)-n_contingent)
            assignments.append(weight*(treated-fixed))
        tables.append(assignments)
    extremal = sum(abs(sum(rows, Fraction(0))) >= abs(actual_effect) for rows in product(*tables))
    return float(Fraction(extremal, assignment_count)), assignment_count


def analyze_pilot_itt(
    bee_roster: Sequence[PilotBee],
    trials: Sequence[PilotTrial],
    *,
    planned_trials_per_bee: int,
    exact_randomization: bool = False,
    max_assignments: int = 100000,
) -> PilotITTReceipt:
    """Analyze a bee-randomized, colony-blocked trial's assigned-policy arms.

    Each arm's success rate is a colony-block-standardized *equal-bee* average,
    not a pooled trial-weighted response proportion. The effect interval is
    sharp with respect to completions of the observed missing binary outcomes;
    it does not incorporate randomization uncertainty or guarantee any
    population-level confidence interval. Exact permutation p-value (complete
    outcomes only) tests Fisher's bee-level no-treatment-effect sharp null,
    conditional on observed arm totals within colonies. Stable trial schedules,
    no inter-bee interference, and actual randomized assignment are external
    design assumptions, NOT inferred from these rows.
    """
    if type(exact_randomization) is not bool:
        raise ValueError('exact_randomization must be boolean')
    if type(max_assignments) is not int or max_assignments < 1:
        raise ValueError('max_assignments must be a positive integer')
    members, by_colony, slots, counts, mismatch, unknown_delivery = _validate(
        bee_roster, trials, planned_trials_per_bee
    )
    intervals = _rates(slots, planned_trials_per_bee)
    lo, hi = _weighted_contrast(by_colony, intervals)
    effect_lo = lo['contingent'] - hi['precommitted']
    effect_hi = hi['contingent'] - lo['precommitted']
    assert effect_lo <= effect_hi
    p, assignments, status = None, None, 'not_requested'
    if exact_randomization:
        if counts['unobserved']:
            raise ValueError('exact randomization requires complete outcomes: report missing-completion bounds only')
        per_bee = {b: v[0] for b, v in intervals.items()}
        p, assignments = _exact_sharp_null_p(by_colony, per_bee, effect_lo, max_assignments)
        status = 'complete_sharp_null_test'
    return PilotITTReceipt(
        trials=len(trials), bees=len(members), colonies=len(by_colony),
        planned_trials_per_bee=planned_trials_per_bee,
        contingent_bees=sum(m.assigned_access == 'contingent' for m in members.values()),
        precommitted_bees=sum(m.assigned_access == 'precommitted' for m in members.values()),
        correct=counts['correct'], wrong=counts['wrong'], abstain=counts['abstain'],
        unobserved=counts['unobserved'],
        noncompliant_delivered_trials=mismatch,
        unknown_delivery_trials=unknown_delivery,
        contingent_lower=float(lo['contingent']), contingent_upper=float(hi['contingent']),
        precommitted_lower=float(lo['precommitted']), precommitted_upper=float(hi['precommitted']),
        effect_lower=float(effect_lo), effect_upper=float(effect_hi),
        exact_randomization_p=p, exact_randomization_assignments=assignments,
        exact_randomization_status=status,
    )


def _csv_rows(path, required):
    with Path(path).open('r', newline='', encoding='utf-8-sig') as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None or not set(required).issubset(reader.fieldnames):
            raise ValueError(f'CSV missing required column(s): {sorted(set(required)-set(reader.fieldnames or []))}')
        return list(reader)


def read_bee_roster_csv(path) -> tuple[PilotBee, ...]:
    rows = _csv_rows(path, ('bee_id', 'colony_id', 'assigned_access'))
    return tuple(PilotBee(r['bee_id'], r['colony_id'], r['assigned_access']) for r in rows)


def read_trial_log_csv(path) -> tuple[PilotTrial, ...]:
    required = ('trial_id', 'bee_id', 'slot', 'target', 'outcome_status',
                'final_action', 'unobserved_reason', 'delivered_access')
    rows = _csv_rows(path, required)
    out = []
    for row in rows:
        try:
            slot = int(row['slot'])
            target = int(row['target'])
            action = int(row['final_action']) if row['final_action'] not in ('', None) else None
        except (TypeError, ValueError) as exc:
            raise ValueError('invalid integer in slot, target or final_action') from exc
        out.append(PilotTrial(
            trial_id=row['trial_id'], bee_id=row['bee_id'], slot=slot,
            target=target, outcome_status=row['outcome_status'], final_action=action,
            unobserved_reason=row['unobserved_reason'],
            delivered_access=row['delivered_access'],
        ))
    return tuple(out)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Bee-randomized artificial-flower policy ITT intake')
    parser.add_argument('--roster', required=True, help='pre-enrollment bee-by-colony assignment CSV')
    parser.add_argument('--trials', required=True, help='one row per planned bee trial slot')
    parser.add_argument('--planned-trials-per-bee', required=True, type=int)
    parser.add_argument('--exact-randomization', action='store_true',
                        help='exact within-colony bee-assignment sharp-null test; only complete outcomes')
    parser.add_argument('--max-assignments', type=int, default=100000)
    args = parser.parse_args(argv)
    r = analyze_pilot_itt(
        read_bee_roster_csv(args.roster), read_trial_log_csv(args.trials),
        planned_trials_per_bee=args.planned_trials_per_bee,
        exact_randomization=args.exact_randomization,
        max_assignments=args.max_assignments,
    )
    print(json.dumps(asdict(r), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
