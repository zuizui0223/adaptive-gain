"""Stage15 pure design verification receipt. Source-free; never executes on live bees."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from normative import benchmark
from allocation import generate,audit,receipt as allocation_receipt
from telemetry import mock_telemetry,validate_traces
from estimator import estimate

def main(root):
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    exact=benchmark(cost=.10)
    source=generate(24,12)
    allocation=audit(source,expected_colonies=24,expected_bees=12)
    observation=mock_telemetry(source)
    qa,verified=validate_traces(
        source,observation,
        # These are intentionally FAKE QA fixtures, not approved pilot values.
        {'calm':(.05,.15),'crosswind':(.95,1.05)})
    if verified is None or qa['status']!='SYNTHETIC_PHYSICAL_GATE_PASSED':
        raise ValueError('NO_GO_SYNTHETIC_INSTRUMENT_CONTRACT')
    modeled=estimate(source,verified)
    if modeled['status']!='SYNTHETIC_ESTIMATOR_QA_ONLY':
        raise ValueError('NO_GO_SYNTHETIC_ITT_ESTIMATOR')
    if abs(modeled['precommit_minus_contingent_leaf_requests']-.5)>1e-12:
        raise ValueError('NO_GO_PERFECT_POLICY_QUERY_SAVING')
    result={
      'status':'STAGE15_EXACT_MATH_AND_SYNTHETIC_PROTOCOL_VERIFIED',
      'studies_or_live_animals_executed':0,
      'worlds':exact['n_worlds'],
      'exact_restricted_precommit_vs_contingent':exact,
      'synthetic_allocation':allocation_receipt(),
      'synthetic_source_hardware_gate':qa,
      'synthetic_injected_perfect_policy_results':{
         'NO_REAL_ANIMAL_OUTCOMES':True,
         'injected_mock_consumption_model':'30 mg − 2 mg per extra leaf reveal + fake Gaussian 0.5 mg perturbation',
         'primary_contingent_minus_precommit_consumption_mg_not_real':
            modeled['primary_contingent_minus_precommit_sucrose_mg_per_fixed_30s'],
         'query_saving_from_mock_no_real_bees':
            modeled['precommit_minus_contingent_leaf_requests'],
         'mock_accuracy_by_mode':modeled['actual_correct_target_rate_by_arm'],
         'frozen_colony_equal_analysis_ready_to_test_future_real_source_only_after_approval':True
      },
      'estimated_power_from_real_bees':None,
      'hypothetical_24_colonies_do_not_define_real_recruitment':True,
      'no_conclusions_about_real_honeybees':True,
    }
    out=root/'stage15_synthetic_design_receipt.json'
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
    print('STAGE15_EXACT_AND_SYNTHETIC_QA '+json.dumps({
         'status':result['status'],
         'real_bees':result['studies_or_live_animals_executed'],
         'synthetic_trials':allocation['n_trials'],
         'source_worlds':exact['n_worlds'],
         'theorem_query_saving':exact['query_saving'],
         'simulated_query_saving':modeled['precommit_minus_contingent_leaf_requests'],
         'mock_consumption_difference_not_real':modeled['primary_contingent_minus_precommit_sucrose_mg_per_fixed_30s'],
         'n_focused_tests_are_separately_verified':True
      },ensure_ascii=False))
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',default='stage15_design_outputs')
    main(ap.parse_args().out)
