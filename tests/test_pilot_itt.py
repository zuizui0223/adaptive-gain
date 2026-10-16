"""Bee-randomized, colony-blocked policy-access ITT intake and sharp-null tests.

All rows are synthetic enrolled bees/trials, NOT empirical pollinator records.
The permutation oracle below is independent of the implementation's test code.
"""
from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
from itertools import combinations, product
import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

from adaptive_gain.pilot_itt import (
    PilotBee, PilotTrial, analyze_pilot_itt, read_bee_roster_csv,
    read_trial_log_csv,
)


def example():
    roster = []
    trials = []
    # Two colony strata, 2 assigned bees per access arm, 4 planned slots / bee.
    # Colony 1 contingent (1.00,.75) vs fixed (.50,.25): difference 0.50
    # Colony 2 contingent (.75,.50) vs fixed (.50,.25): difference 0.25
    profiles = {
        'colony_1': {'contingent': (4, 3), 'precommitted': (2, 1)},
        'colony_2': {'contingent': (3, 2), 'precommitted': (2, 1)},
    }
    for colony, rows in profiles.items():
        for arm, correct_counts in rows.items():
            for k, correct_count in enumerate(correct_counts):
                bee_id = f'{colony}_{arm}_{k}'
                roster.append(PilotBee(bee_id, colony, arm))
                for slot in range(1, 5):
                    target = slot % 2
                    correct = slot <= correct_count
                    trials.append(PilotTrial(
                        trial_id=f'{bee_id}_slot_{slot}',
                        bee_id=bee_id, slot=slot, target=target,
                        outcome_status='choice',
                        final_action=target if correct else 1-target,
                        unobserved_reason='',
                        delivered_access=arm,
                    ))
    return roster, trials


def independent_permutation_p(roster, trials):
    bees = {b.bee_id: b for b in roster}
    scores = {}
    for b in bees:
        outcomes = [t for t in trials if t.bee_id == b]
        scores[b] = Fraction(sum(t.final_action == t.target for t in outcomes), len(outcomes))
    colonies = sorted({r.colony_id for r in roster})
    cases = []
    for colony in colonies:
        ids = sorted(r.bee_id for r in roster if r.colony_id == colony)
        treated_count = sum(r.assigned_access == 'contingent' for r in roster if r.colony_id == colony)
        cases.append([(ids, frozenset(choice)) for choice in combinations(ids, treated_count)])

    def statistic(assignments):
        numerator = Fraction(0)
        for ids, treated in assignments:
            treated_scores = [scores[i] for i in ids if i in treated]
            control_scores = [scores[i] for i in ids if i not in treated]
            stratum = sum(treated_scores)/len(treated_scores) - sum(control_scores)/len(control_scores)
            numerator += Fraction(len(ids), len(roster))*stratum
        return numerator

    observed = statistic([(sorted(r.bee_id for r in roster if r.colony_id == colony),
                            frozenset(r.bee_id for r in roster if r.colony_id == colony
                                      and r.assigned_access == 'contingent'))
                           for colony in colonies])
    stats = [statistic(option) for option in product(*cases)]
    return observed, Fraction(sum(abs(t) >= abs(observed) for t in stats), len(stats)), len(stats)


def test_complete_pilot_bee_equal_weighted_colony_blocked_itt_and_randomization():
    roster, trials = example()
    r = analyze_pilot_itt(roster, trials, planned_trials_per_bee=4, exact_randomization=True)
    obs, exact_p, n_perm = independent_permutation_p(roster, trials)
    assert obs == Fraction(3, 8)
    assert r.trials == 32
    assert r.bees == 8
    assert r.colonies == 2
    assert r.contingent_bees == r.precommitted_bees == 4
    assert (r.correct, r.wrong, r.abstain, r.unobserved) == (18, 14, 0, 0)
    assert r.contingent_lower == r.contingent_upper == pytest.approx(0.75)
    assert r.precommitted_lower == r.precommitted_upper == pytest.approx(0.375)
    assert r.effect_lower == r.effect_upper == pytest.approx(float(obs))
    assert r.exact_randomization_p == pytest.approx(float(exact_p))
    assert r.exact_randomization_assignments == n_perm == 36
    assert r.exact_randomization_status == 'complete_sharp_null_test'


def test_one_unobserved_correct_and_one_unobserved_wrong_produce_sharp_bounds():
    roster, trials = example()
    updates = []
    for t in trials:
        if t.bee_id == 'colony_1_contingent_0' and t.slot == 1:
            t = replace(t, outcome_status='unobserved', final_action=None,
                        unobserved_reason='camera_occlusion')
        if t.bee_id == 'colony_1_precommitted_0' and t.slot == 4:
            t = replace(t, outcome_status='unobserved', final_action=None,
                        unobserved_reason='recording_failure')
        updates.append(t)
    receipt = analyze_pilot_itt(roster, updates, planned_trials_per_bee=4)
    assert receipt.unobserved == 2
    assert receipt.effect_lower == pytest.approx(0.25)
    assert receipt.effect_upper == pytest.approx(0.375)
    assert receipt.exact_randomization_p is None
    with pytest.raises(ValueError, match='complete outcomes'):
        analyze_pilot_itt(roster, updates, planned_trials_per_bee=4, exact_randomization=True)
    # The observed records are consistent with two mutually exclusive extremes.
    for first_success, second_success, expected in ((False, True, 0.25), (True, False, 0.375)):
        completed = []
        for t in updates:
            if t.outcome_status == 'unobserved':
                chosen_success = first_success if t.bee_id.endswith('contingent_0') else second_success
                t = replace(t, outcome_status='choice',
                            final_action=t.target if chosen_success else 1-t.target,
                            unobserved_reason='')
            completed.append(t)
        observed = analyze_pilot_itt(roster, completed, planned_trials_per_bee=4)
        assert observed.effect_lower == observed.effect_upper == pytest.approx(expected)


def test_confirmed_no_choice_is_zero_not_unknown():
    roster, trials = example()
    results = [replace(t, outcome_status='abstain', final_action=None)
               if t.bee_id == 'colony_1_precommitted_0' and t.slot == 4 else t for t in trials]
    got = analyze_pilot_itt(roster, results, planned_trials_per_bee=4)
    assert got.abstain == 1
    assert got.unobserved == 0
    assert got.effect_lower == got.effect_upper == pytest.approx(0.375)


def test_wrong_choice_is_a_failure_not_an_unknown():
    roster, trials = example()
    result = analyze_pilot_itt(roster, trials, planned_trials_per_bee=4)
    assert result.wrong == 14
    assert result.unobserved == 0
    assert result.effect_lower == result.effect_upper


def test_noncompliance_does_not_reassign_the_itt_arm():
    roster, trials = example()
    changed = [replace(t, delivered_access='precommitted')
               if t.bee_id == 'colony_1_contingent_0' else t for t in trials]
    r = analyze_pilot_itt(roster, changed, planned_trials_per_bee=4)
    assert r.noncompliant_delivered_trials == 4
    assert r.effect_lower == r.effect_upper == pytest.approx(0.375)


def test_enrollment_roster_detects_entirely_unobserved_bee():
    roster, trials = example()
    dropped = [t for t in trials if t.bee_id != 'colony_2_precommitted_1']
    with pytest.raises(ValueError, match='planned slot'):
        analyze_pilot_itt(roster, dropped, planned_trials_per_bee=4)


def test_missing_trial_slot_must_be_explicit_unknown_row():
    roster, trials = example()
    with pytest.raises(ValueError, match='planned slot'):
        analyze_pilot_itt(roster, trials[:-1], planned_trials_per_bee=4)


def test_all_trials_unobserved_for_one_enrolled_bee_keeps_it_in_itt():
    roster, trials = example()
    changed = [replace(t, outcome_status='unobserved', final_action=None,
                       unobserved_reason='bee_dropout')
               if t.bee_id == 'colony_1_contingent_0' else t for t in trials]
    r = analyze_pilot_itt(roster, changed, planned_trials_per_bee=4)
    assert r.bees == 8
    assert r.unobserved == 4
    assert r.effect_lower == pytest.approx(0.125)
    assert r.effect_upper == pytest.approx(0.375)


@pytest.mark.parametrize('modifier', [
    lambda b,t: (b,t[:1]+[replace(t[1], trial_id=t[0].trial_id)]+t[2:]),
    lambda b,t: (b,t[:1]+[replace(t[1], slot=t[0].slot)]+t[2:]),
    lambda b,t: (b,t[:1]+[replace(t[1], bee_id='not_enrolled')]+t[2:]),
    lambda b,t: (b,t[:1]+[replace(t[1], outcome_status='choice', final_action=None)]+t[2:]),
    lambda b,t: (b,t[:1]+[replace(t[1], outcome_status='abstain', final_action=0)]+t[2:]),
    lambda b,t: (b,t[:1]+[replace(t[1], outcome_status='unobserved', final_action=None,
                                 unobserved_reason='')]+t[2:]),
    lambda b,t: (b,t[:1]+[replace(t[1], final_action=2)]+t[2:]),
    lambda b,t: (b,t[:1]+[replace(t[1], delivered_access='mystery')]+t[2:]),
    lambda b,t: ([b[0],replace(b[1], bee_id=b[0].bee_id)]+b[2:],t),
    lambda b,t: ([replace(b[0], assigned_access='unknown')]+b[1:],t),
    lambda b,t: ([replace(b[0], colony_id='')]+b[1:],t),
])
def test_fail_closed_malformed_roster_and_trial_rows(modifier):
    roster, trials = example()
    r,t = modifier(roster,trials)
    with pytest.raises(ValueError):
        analyze_pilot_itt(r,t,planned_trials_per_bee=4)


def test_colony_without_both_assigned_arms_rejected():
    roster, trials = example()
    roster = [replace(b, assigned_access='contingent')
              if b.colony_id == 'colony_1' else b for b in roster]
    with pytest.raises(ValueError, match='both arms'):
        analyze_pilot_itt(roster,trials,planned_trials_per_bee=4)


def test_exact_permutations_capped_before_computation():
    roster, trials = example()
    with pytest.raises(ValueError, match='assignment configurations'):
        analyze_pilot_itt(roster,trials,planned_trials_per_bee=4,
                          exact_randomization=True,max_assignments=35)


@pytest.mark.parametrize('n', [0, True, 1.0, -3])
def test_invalid_planned_trial_count_rejected(n):
    roster, trials = example()
    with pytest.raises(ValueError):
        analyze_pilot_itt(roster,trials,planned_trials_per_bee=n)


def test_csv_inputs_and_cli_json_stdout(tmp_path):
    roster, trials = example()
    roster_path=tmp_path/'bees.csv'
    trial_path=tmp_path/'trials.csv'
    with roster_path.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f)
        w.writerow(('bee_id','colony_id','assigned_access'))
        for row in roster:w.writerow((row.bee_id,row.colony_id,row.assigned_access))
    with trial_path.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f)
        w.writerow(('trial_id','bee_id','slot','target','outcome_status','final_action',
                    'unobserved_reason','delivered_access','video_id'))
        for row in trials:
            w.writerow((row.trial_id,row.bee_id,row.slot,row.target,row.outcome_status,
                        row.final_action,row.unobserved_reason,row.delivered_access,'fake_camera'))
    parsed=analyze_pilot_itt(read_bee_roster_csv(roster_path),
        read_trial_log_csv(trial_path),planned_trials_per_bee=4,exact_randomization=True)
    assert parsed.effect_lower==pytest.approx(.375)
    proc=subprocess.run([sys.executable,'-m','adaptive_gain.pilot_itt','--roster',str(roster_path),
         '--trials',str(trial_path),'--planned-trials-per-bee','4','--exact-randomization'],
         capture_output=True,text=True,check=True)
    result=json.loads(proc.stdout)
    assert result['exact_randomization_assignments']==36
    assert result['effect_upper']==pytest.approx(.375)


def test_invalid_csv_header_rejected(tmp_path):
    p=tmp_path/'roster.csv'
    p.write_text('bee_id,assigned_access\nx,contingent\n',encoding='utf-8')
    with pytest.raises(ValueError,match='column'):
        read_bee_roster_csv(p)
    t=tmp_path/'trials.csv'
    t.write_text('trial_id,bee_id,slot\na,b,1\n',encoding='utf-8')
    with pytest.raises(ValueError,match='column'):
        read_trial_log_csv(t)


def test_checked_in_synthetic_templates_remain_a_verified_cli_fixture():
    root = Path(__file__).resolve().parents[1] / 'experiments' / 'templates'
    roster = read_bee_roster_csv(root / 'pilot_bee_roster_example.csv')
    trials = read_trial_log_csv(root / 'pilot_trial_log_example.csv')
    r = analyze_pilot_itt(roster, trials, planned_trials_per_bee=4,
                          exact_randomization=True)
    assert (r.trials, r.bees, r.colonies) == (32, 8, 2)
    assert r.effect_lower == r.effect_upper == pytest.approx(3/8)
    assert r.exact_randomization_p == pytest.approx(1/9)
    assert r.exact_randomization_assignments == 36


def test_synthetic_fixture_validation_receipt_matches_exact_results():
    root = Path(__file__).resolve().parents[1]
    receipt=json.loads((root / 'validation' / 'pilot_itt_v1.json').read_text(encoding='utf-8'))
    roster=read_bee_roster_csv(root / 'experiments/templates/pilot_bee_roster_example.csv')
    trials=read_trial_log_csv(root / 'experiments/templates/pilot_trial_log_example.csv')
    result=analyze_pilot_itt(roster,trials,planned_trials_per_bee=4,
                             exact_randomization=True)
    assert receipt['status'] == 'synthetic_fixture_only_no_real_bee_data'
    assert result.effect_lower == receipt['synthetic_example']['colony_block_standardized_itt']
    assert result.exact_randomization_assignments == receipt['synthetic_example']['assignment_configurations']
    assert result.exact_randomization_p == pytest.approx(Fraction(receipt['synthetic_example']['exact_sharp_null_permutation_p']))


def test_known_nondelivery_is_separate_from_unknown_delivery_and_cross_arm_noncompliance():
    roster, trials = example()
    updated = [replace(t, delivered_access='not_delivered') if t == trials[0]
               else replace(t, delivered_access='') if t == trials[1]
               else replace(t, delivered_access='precommitted') if t == trials[2]
               else t for t in trials]
    report = analyze_pilot_itt(roster, updated, planned_trials_per_bee=4)
    assert report.not_delivered_trials == 1
    assert report.unknown_delivery_trials == 1
    assert report.noncompliant_delivered_trials == 1
    assert report.effect_lower == report.effect_upper == pytest.approx(0.375)
