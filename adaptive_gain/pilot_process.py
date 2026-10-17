"""Prospective cue-history/process audit *separate* from randomized ITT.

Only presentation traces and precommitted schedule conformity are inspected;
the outcome estimator remains exactly adaptive_gain.pilot_itt.analyze_pilot_itt.
The code cannot establish that a fixed schedule was truly archived BEFORE
an encounter, or that a binary report measures internal insect perception.
Recording failures are flagged, not used to exclude assigned bees/trials.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Sequence

from .pilot_itt import PilotBee, PilotTrial, analyze_pilot_itt, read_bee_roster_csv, read_trial_log_csv


@dataclass(frozen=True)
class CueEvent:
    trial_id: str
    bee_id: str
    step: int
    cue: str
    response: int | None
    elapsed_ms: int | None


@dataclass(frozen=True)
class FixedCuePlan:
    trial_id: str
    bee_id: str
    second_cue: str
    plan_archive_id: str


@dataclass(frozen=True)
class PilotProcessReceipt:
    enrolled_bees: int
    planned_trials: int
    cue_event_rows: int
    fixed_plans_expected: int
    fixed_plans_present: int
    missing_fixed_plans: int
    no_cue_trials: int
    two_cue_trials: int
    budget_violations: int
    fixed_plan_mismatches: int
    wrong_first_cues: int
    invalid_sequences: int
    late_readouts: int
    unverified_timing: int
    unverified_reports: int
    undelivered_with_events: int
    unknown_delivery_trials: int
    noncompliant_delivered_trials: int
    contingent_second_by_context: tuple[tuple[int, int, int], ...]
    contingent_second_B_rate_A0: float | None
    contingent_second_B_rate_A1: float | None
    descriptive_branch_difference: float | None
    mechanism_status: str
    limitation: str = 'descriptive cue-history fidelity only, not routeability causality or fitness'


def _nonempty(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{name} must be a nonempty string')


def audit_pilot_process(
    roster: Sequence[PilotBee],
    trials: Sequence[PilotTrial],
    events: Sequence[CueEvent],
    fixed_plans: Sequence[FixedCuePlan],
    *,
    planned_trials_per_bee: int,
    deadline_ms: int,
) -> PilotProcessReceipt:
    """Inspect cue acquisition without dropping any assigned trial or bee.

    Assumes first cue is called A, further alternatives B/C, and budget two.
    The locked-plan file must independently predate all encounters; the
    plan_archive_id field is a recorded pointer, not proof of precommitment.
    Causality requires real bee randomization, no interference, and validated
    behavioral cue reports; NONE is established by this function.
    """
    if type(deadline_ms) is not int or deadline_ms <= 0:
        raise ValueError('deadline_ms must be a strictly positive integer')
    original = analyze_pilot_itt(roster, trials, planned_trials_per_bee=planned_trials_per_bee)
    trial_by_id = {t.trial_id: t for t in trials}
    arm_by_bee = {b.bee_id: b.assigned_access for b in roster}

    plans = {}
    for row in fixed_plans:
        _nonempty(row.trial_id, 'plan trial_id')
        _nonempty(row.bee_id, 'plan bee_id')
        _nonempty(row.plan_archive_id, 'plan_archive_id')
        if row.trial_id in plans:
            raise ValueError('duplicate fixed cue plan')
        if row.trial_id not in trial_by_id or trial_by_id[row.trial_id].bee_id != row.bee_id:
            raise ValueError('fixed plan references unknown/mismatched trial')
        if arm_by_bee[row.bee_id] != 'precommitted':
            raise ValueError('fixed plan recorded for non-precommitted bee')
        if row.second_cue not in ('B', 'C'):
            raise ValueError('precommitted second cue must be B or C')
        plans[row.trial_id] = row

    cue_rows = {}
    for e in events:
        _nonempty(e.trial_id, 'cue event trial_id')
        _nonempty(e.bee_id, 'cue event bee_id')
        if e.trial_id not in trial_by_id or trial_by_id[e.trial_id].bee_id != e.bee_id:
            raise ValueError('cue event references unknown/mismatched trial')
        if type(e.step) is not int or e.step < 1:
            raise ValueError('cue acquisition step must be a positive integer')
        if e.cue not in ('A', 'B', 'C'):
            raise ValueError('cue must be A, B, or C')
        if e.response is not None and (type(e.response) is not int or e.response not in (0, 1)):
            raise ValueError('per-cue report must be binary or unobserved')
        if e.elapsed_ms is not None and (type(e.elapsed_ms) is not int or e.elapsed_ms < 0):
            raise ValueError('cue acquisition elapsed_ms must be nonnegative or unobserved')
        row = cue_rows.setdefault(e.trial_id, {})
        if e.step in row:
            raise ValueError('duplicate cue acquisition step within trial')
        row[e.step] = e

    expected_fixed = {t.trial_id for t in trials if arm_by_bee[t.bee_id] == 'precommitted'}
    missing_plans = len(expected_fixed - set(plans))
    numbers = {key:0 for key in (
        'no_cue_trials','two_cue_trials','budget_violations','fixed_plan_mismatches',
        'wrong_first_cues','invalid_sequences','late_readouts','unverified_timing',
        'unverified_reports','undelivered_with_events',
    )}
    branch = {0:{'B':0,'C':0},1:{'B':0,'C':0}}
    for trial in trials:
        observed = cue_rows.get(trial.trial_id, {})
        trace = [observed[k] for k in sorted(observed)]
        if not trace:
            numbers['no_cue_trials'] += 1
        if len(trace) >= 2:
            numbers['two_cue_trials'] += 1
        if len(trace) > 2 or any(k > 2 for k in observed):
            numbers['budget_violations'] += 1
        if observed.get(1) is not None and observed[1].cue != 'A':
            numbers['wrong_first_cues'] += 1
        invalid = (
            sorted(observed) != list(range(1, len(trace)+1))
            or (len(trace) >= 2 and observed.get(2) is not None and observed[2].cue not in ('B','C'))
            or (len(trace) >= 2 and observed.get(1) is not None
                and observed.get(2) is not None and observed[1].cue == observed[2].cue)
        )
        if any(e.elapsed_ms is None for e in trace):
            numbers['unverified_timing'] += 1
        if any(e.response is None for e in trace):
            numbers['unverified_reports'] += 1
        timed = [e.elapsed_ms for e in trace]
        if any(t is not None and t > deadline_ms for t in timed):
            numbers['late_readouts'] += 1
        if len(timed) >= 2 and all(t is not None for t in timed) and any(
            timed[i] >= timed[i+1] for i in range(len(timed)-1)
        ):
            invalid = True
        if invalid:
            numbers['invalid_sequences'] += 1
        if trial.delivered_access == 'not_delivered' and trace:
            numbers['undelivered_with_events'] += 1
        if arm_by_bee[trial.bee_id] == 'precommitted' and 2 in observed and trial.trial_id in plans:
            if observed[2].cue != plans[trial.trial_id].second_cue:
                numbers['fixed_plan_mismatches'] += 1

        # Branch frequencies are descriptive and condition on a second cue
        # actually being obtained; NOT a causal contrast or an ITT estimand.
        if (
            arm_by_bee[trial.bee_id] == 'contingent'
            and trial.delivered_access == 'contingent'
            and set(observed) == {1,2}
            and observed[1].cue == 'A'
            and observed[2].cue in ('B','C')
            and observed[1].response is not None
            and not invalid
            and all(t is not None and t <= deadline_ms for t in timed)
        ):
            branch[observed[1].response][observed[2].cue] += 1

    pairs = tuple((a, branch[a]['B'], branch[a]['C']) for a in (0,1))
    den0, den1 = (sum(branch[a].values()) for a in (0,1))
    rate0 = branch[0]['B']/den0 if den0 else None
    rate1 = branch[1]['B']/den1 if den1 else None
    diagnostic_keys = (
        'budget_violations','fixed_plan_mismatches','wrong_first_cues',
        'invalid_sequences','late_readouts','unverified_timing',
        'unverified_reports','undelivered_with_events',
    )
    if (
        missing_plans or any(numbers[key] for key in diagnostic_keys)
        or original.noncompliant_delivered_trials or original.unknown_delivery_trials
    ):
        mechanism_status = 'process_fidelity_or_measurement_unresolved'
    elif rate0 is None or rate1 is None:
        mechanism_status = 'insufficient_branch_data'
    else:
        mechanism_status = 'branch_order_observable_not_causal_proof'
    return PilotProcessReceipt(
        enrolled_bees=original.bees, planned_trials=original.trials,
        cue_event_rows=len(events), fixed_plans_expected=len(expected_fixed),
        fixed_plans_present=len(plans), missing_fixed_plans=missing_plans,
        contingent_second_by_context=pairs,
        contingent_second_B_rate_A0=rate0,
        contingent_second_B_rate_A1=rate1,
        descriptive_branch_difference=rate0-rate1 if rate0 is not None and rate1 is not None else None,
        mechanism_status=mechanism_status,
        unknown_delivery_trials=original.unknown_delivery_trials,
        noncompliant_delivered_trials=original.noncompliant_delivered_trials,
        **numbers,
    )


def _csv(path, required):
    with Path(path).open('r', newline='', encoding='utf-8-sig') as handle:
        reader=csv.DictReader(handle)
        if reader.fieldnames is None or not set(required).issubset(reader.fieldnames):
            raise ValueError('CSV missing required column(s)')
        return list(reader)


def read_cue_event_csv(path) -> tuple[CueEvent, ...]:
    rows=_csv(path, ('trial_id','bee_id','step','cue','response','elapsed_ms'))
    out=[]
    for row in rows:
        try:
            step=int(row['step'])
            response=int(row['response']) if row['response'] not in ('',None) else None
            elapsed=int(row['elapsed_ms']) if row['elapsed_ms'] not in ('',None) else None
        except (ValueError,TypeError) as err:
            raise ValueError('invalid step/response/elapsed_ms integer') from err
        out.append(CueEvent(row['trial_id'],row['bee_id'],step,row['cue'],response,elapsed))
    return tuple(out)


def read_fixed_cue_plan_csv(path) -> tuple[FixedCuePlan, ...]:
    rows=_csv(path,('trial_id','bee_id','second_cue','plan_archive_id'))
    return tuple(FixedCuePlan(r['trial_id'],r['bee_id'],r['second_cue'],r['plan_archive_id']) for r in rows)


def main(argv=None):
    parser=argparse.ArgumentParser(description='Separate cue-trace process fidelity from bee-randomized ITT')
    parser.add_argument('--roster',required=True)
    parser.add_argument('--trials',required=True)
    parser.add_argument('--events',required=True)
    parser.add_argument('--fixed-plans',required=True)
    parser.add_argument('--planned-trials-per-bee',type=int,required=True)
    parser.add_argument('--deadline-ms',type=int,required=True)
    args=parser.parse_args(argv)
    roster=read_bee_roster_csv(args.roster)
    trials=read_trial_log_csv(args.trials)
    report=audit_pilot_process(roster,trials,read_cue_event_csv(args.events),
                                read_fixed_cue_plan_csv(args.fixed_plans),
                                planned_trials_per_bee=args.planned_trials_per_bee,
                                deadline_ms=args.deadline_ms)
    # File digests permit later byte-for-byte audit, but DO NOT establish
    # that any plan was actually sealed before the first cue was presented.
    inputs = {'roster': args.roster, 'trials': args.trials,
              'events': args.events, 'fixed_plans': args.fixed_plans}
    digest = {name: hashlib.sha256(Path(path).read_bytes()).hexdigest()
              for name, path in inputs.items()}
    itt = analyze_pilot_itt(roster, trials, planned_trials_per_bee=args.planned_trials_per_bee)
    print(json.dumps({'process': asdict(report), 'itt': asdict(itt),
                      'input_sha256': digest}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
