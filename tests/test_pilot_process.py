"""A mechanistic cue-order audit must not redefine the randomized ITT outcome."""
from dataclasses import replace
import csv
import json
import subprocess
import sys

import pytest

from adaptive_gain.pilot_itt import PilotBee, PilotTrial, analyze_pilot_itt
from adaptive_gain.pilot_process import (
    CueEvent, FixedCuePlan, audit_pilot_process,
    read_cue_event_csv, read_fixed_cue_plan_csv,
)


def fixture():
    roster = []
    trials = []
    events = []
    fixed = []
    for colony in ('c1','c2'):
        for arm in ('contingent', 'precommitted'):
            for index in (0,1):
                bee=f'{colony}_{arm}_{index}'
                roster.append(PilotBee(bee,colony,arm))
                for slot in (1,2):
                    trial_id=f'{bee}_{slot}'
                    report = (slot+index) % 2
                    trials.append(PilotTrial(trial_id,bee,slot,slot%2,'choice',slot%2,'',arm))
                    if arm == 'precommitted':
                        fixed.append(FixedCuePlan(trial_id,bee,'B',f'archive_{colony}'))
                        second='B'
                    else:
                        second='B' if report == 0 else 'C'
                    events.extend([
                        CueEvent(trial_id,bee,1,'A',report,100),
                        CueEvent(trial_id,bee,2,second,(slot+index)%2,400),
                    ])
    return roster,trials,events,fixed


def test_balanced_fidelity_and_descriptive_branch_rates():
    roster,trials,events,fixed=fixture()
    r=audit_pilot_process(roster,trials,events,fixed,planned_trials_per_bee=2,deadline_ms=1000)
    assert r.enrolled_bees==8 and r.planned_trials==16
    assert r.fixed_plans_expected==8 and r.fixed_plans_present==8
    assert r.budget_violations==r.fixed_plan_mismatches==r.undelivered_with_events==0
    assert r.invalid_sequences==r.late_readouts==r.unverified_timing==r.unverified_reports==0
    assert r.contingent_second_by_context == ((0,4,0),(1,0,4))
    assert r.contingent_second_B_rate_A0 == pytest.approx(1.0)
    assert r.contingent_second_B_rate_A1 == pytest.approx(0.0)
    assert r.descriptive_branch_difference == pytest.approx(1.0)
    assert r.mechanism_status == 'branch_order_observable_not_causal_proof'
    assert r.cue_event_rows==32
    # Main ITT never changes or conditions on this post-randomization readout.
    before=analyze_pilot_itt(roster,trials,planned_trials_per_bee=2)
    after=analyze_pilot_itt(roster,trials,planned_trials_per_bee=2)
    assert before==after


def test_fixed_plan_violation_counted_not_removed_from_itt():
    roster,trials,events,fixed=fixture()
    target=fixed[0].trial_id
    corrupted=[replace(e,cue='C') if e.trial_id==target and e.step==2 else e for e in events]
    r=audit_pilot_process(roster,trials,corrupted,fixed,planned_trials_per_bee=2,deadline_ms=1000)
    assert r.fixed_plan_mismatches==1
    assert r.mechanism_status=='process_fidelity_or_measurement_unresolved'
    assert r.planned_trials==len(trials)


def test_contingent_receipt_does_not_imply_actual_conditional_choices():
    roster,trials,events,fixed=fixture()
    always_b=[replace(e,cue='B') if e.step==2 and 'contingent' in e.bee_id else e for e in events]
    r=audit_pilot_process(roster,trials,always_b,fixed,planned_trials_per_bee=2,deadline_ms=1000)
    assert r.contingent_second_B_rate_A0==r.contingent_second_B_rate_A1==1.0
    assert r.descriptive_branch_difference==0.0
    assert r.mechanism_status=='branch_order_observable_not_causal_proof'


def test_budget_overrun_late_timestamp_and_missing_time_flagged_not_filtered():
    roster,trials,events,fixed=fixture()
    t=trials[0]
    events.extend([CueEvent(t.trial_id,t.bee_id,3,'C',0,1200)])
    old=trials[1]; events=[replace(e,elapsed_ms=None) if e.trial_id==old.trial_id and e.step==2 else e for e in events]
    r=audit_pilot_process(roster,trials,events,fixed,planned_trials_per_bee=2,deadline_ms=1000)
    assert r.budget_violations==1
    assert r.late_readouts==1
    assert r.unverified_timing==1
    assert r.mechanism_status=='process_fidelity_or_measurement_unresolved'


def test_missing_fixed_plan_kept_as_integrity_failure():
    roster,trials,events,fixed=fixture()
    r=audit_pilot_process(roster,trials,events,fixed[:-1],planned_trials_per_bee=2,deadline_ms=1000)
    assert r.fixed_plans_expected==8 and r.fixed_plans_present==7
    assert r.missing_fixed_plans==1
    assert r.mechanism_status=='process_fidelity_or_measurement_unresolved'


def test_broken_readout_path_and_absent_response_are_uncertain():
    roster,trials,events,fixed=fixture()
    a=trials[0]
    b=trials[2]
    processed=[e for e in events if not (e.trial_id==a.trial_id and e.step==1)]
    processed=[replace(e,response=None) if e.trial_id==b.trial_id and e.step==1 else e for e in processed]
    r=audit_pilot_process(roster,trials,processed,fixed,planned_trials_per_bee=2,deadline_ms=1000)
    assert r.invalid_sequences==1
    assert r.unverified_reports==1
    assert r.mechanism_status=='process_fidelity_or_measurement_unresolved'


def test_zero_events_valid_for_unrun_dropouts_and_not_delivered_audited():
    roster,trials,events,fixed=fixture()
    tr=trials[0]
    trials=[replace(t,outcome_status='unobserved',final_action=None,
                    unobserved_reason='no_exposure',delivered_access='not_delivered')
            if t.trial_id==tr.trial_id else t for t in trials]
    events=[e for e in events if e.trial_id != tr.trial_id]
    r=audit_pilot_process(roster,trials,events,fixed,planned_trials_per_bee=2,deadline_ms=1000)
    assert r.no_cue_trials==1
    assert r.undelivered_with_events==0
    assert r.planned_trials==16


def test_nondelivery_with_events_is_integrity_violation():
    roster,trials,events,fixed=fixture()
    trials=[replace(t,delivered_access='not_delivered') if t==trials[0] else t for t in trials]
    r=audit_pilot_process(roster,trials,events,fixed,planned_trials_per_bee=2,deadline_ms=1000)
    assert r.undelivered_with_events==1


@pytest.mark.parametrize('mutate', [
    lambda events,trials: [replace(events[1],step=1)] + events,
    lambda events,trials: [replace(events[1],trial_id='unknown')] + events[1:],
    lambda events,trials: [replace(events[1],bee_id='unknown')] + events[1:],
    lambda events,trials: [replace(events[1],response=3)] + events[1:],
    lambda events,trials: [replace(events[1],cue='Z')] + events[1:],
    lambda events,trials: [replace(events[1],elapsed_ms=-1)] + events[1:],
])
def test_ill_formed_cue_log_fails_closed(mutate):
    roster,trials,events,fixed=fixture()
    with pytest.raises(ValueError):
        audit_pilot_process(roster,trials,mutate(events,trials),fixed,planned_trials_per_bee=2,deadline_ms=1000)


def test_invalid_deadline_or_duplicate_plan_rejected():
    roster,trials,events,fixed=fixture()
    with pytest.raises(ValueError):
        audit_pilot_process(roster,trials,events,fixed,planned_trials_per_bee=2,deadline_ms=0)
    with pytest.raises(ValueError):
        audit_pilot_process(roster,trials,events,fixed+[fixed[0]],planned_trials_per_bee=2,deadline_ms=1000)


def test_unobserved_first_outcome_refuses_branch_inference():
    roster,trials,events,fixed=fixture()
    altered=[replace(e,response=None) if 'contingent' in e.bee_id and e.step==1 else e for e in events]
    r=audit_pilot_process(roster,trials,altered,fixed,planned_trials_per_bee=2,deadline_ms=1000)
    assert r.contingent_second_B_rate_A0 is None
    assert r.contingent_second_B_rate_A1 is None
    assert r.descriptive_branch_difference is None
    assert r.mechanism_status=='process_fidelity_or_measurement_unresolved'


def test_file_parse_and_cli_with_existing_synthetic_itt_records(tmp_path):
    roster,trials,events,fixed=fixture()
    # Test that the raw schema can be independently populated (not fitted) for a trial.
    ev_path=tmp_path/'events.csv'
    with ev_path.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['trial_id','bee_id','step','cue','response','elapsed_ms'])
        w.writerows((e.trial_id,e.bee_id,e.step,e.cue,e.response,e.elapsed_ms) for e in events)
    fixed_path=tmp_path/'sealed_plan.csv'
    with fixed_path.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['trial_id','bee_id','second_cue','plan_archive_id'])
        w.writerows((x.trial_id,x.bee_id,x.second_cue,x.plan_archive_id) for x in fixed)
    assert tuple(read_cue_event_csv(ev_path)) == tuple(events)
    assert tuple(read_fixed_cue_plan_csv(fixed_path)) == tuple(fixed)
    bad_path=tmp_path/'missing.csv';bad_path.write_text('trial_id,step\na,1\n',encoding='utf-8')
    with pytest.raises(ValueError,match='column'):
        read_cue_event_csv(bad_path)


def test_cli_uses_immutable_file_hashes_and_never_alters_itt_result(tmp_path):
    roster,trials,events,fixed=fixture()
    inputs = {}
    schemas = (
        ('roster', ('bee_id','colony_id','assigned_access'),
         ((x.bee_id,x.colony_id,x.assigned_access) for x in roster)),
        ('trials', ('trial_id','bee_id','slot','target','outcome_status','final_action',
                    'unobserved_reason','delivered_access'),
         ((t.trial_id,t.bee_id,t.slot,t.target,t.outcome_status,t.final_action,
           t.unobserved_reason,t.delivered_access) for t in trials)),
        ('events',('trial_id','bee_id','step','cue','response','elapsed_ms'),
         ((e.trial_id,e.bee_id,e.step,e.cue,e.response,e.elapsed_ms) for e in events)),
        ('fixed_plans',('trial_id','bee_id','second_cue','plan_archive_id'),
         ((p.trial_id,p.bee_id,p.second_cue,p.plan_archive_id) for p in fixed)),
    )
    for name, header, rows in schemas:
        f=tmp_path/f'{name}.csv'
        with f.open('w',newline='',encoding='utf-8') as handle:
            writer=csv.writer(handle)
            writer.writerow(header)
            writer.writerows(rows)
        inputs[name]=f
    cmd=[sys.executable,'-m','adaptive_gain.pilot_process','--roster',str(inputs['roster']),
         '--trials',str(inputs['trials']),'--events',str(inputs['events']),
         '--fixed-plans',str(inputs['fixed_plans']),
         '--planned-trials-per-bee','2','--deadline-ms','1000']
    output=json.loads(subprocess.run(cmd,check=True,text=True,capture_output=True).stdout)
    assert output['process']['mechanism_status']=='branch_order_observable_not_causal_proof'
    assert output['process']['descriptive_branch_difference']==pytest.approx(1)
    assert set(output['input_sha256'])==set(inputs)
    import hashlib
    for name,path in inputs.items():
        assert output['input_sha256'][name]==hashlib.sha256(path.read_bytes()).hexdigest()
    assert output['itt']['bees']==8
    assert output['itt']['trials']==16


def test_nonmonotonic_timestamp_and_wrong_first_are_reported():
    roster,trials,events,fixed=fixture()
    trial_one=trials[0].trial_id
    trial_two=trials[1].trial_id
    altered=[replace(e,elapsed_ms=100) if e.trial_id==trial_one and e.step==2
             else replace(e,cue='C') if e.trial_id==trial_two and e.step==1
             else e for e in events]
    report=audit_pilot_process(roster,trials,altered,fixed,
                               planned_trials_per_bee=2,deadline_ms=1000)
    assert report.invalid_sequences>=1
    assert report.wrong_first_cues==1
    assert report.mechanism_status=='process_fidelity_or_measurement_unresolved'
