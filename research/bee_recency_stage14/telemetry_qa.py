"""Synthetic-only prospective trial source-contract receipt."""
from pathlib import Path
import argparse,json
from allocation import generate
from estimator import synthetic_outcomes
from source_contract import audit_future_source,synthetic_telemetry

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='bee_stage14_design_outputs')
    root=Path(p.parse_args().out);root.mkdir(parents=True,exist_ok=True)
    a=generate(4,4)
    o=synthetic_outcomes(a,noise_sd=0.)
    t=synthetic_telemetry(a,o)
    receipt,validated=audit_future_source(a,t,
        {'calm':(.05,.15),'crosswind':(.95,1.05)},
        {'informative':(19.5,20.5),'sham':(19.5,20.5)})
    if validated is None or receipt['status']!='SYNTHETIC_HARDWARE_QA_PASSED':
        raise RuntimeError('NO_GO_SOURCE_CONTRACT_SYNTHETIC_QA')
    receipt['all_wind_and_light_values_ARE_FAKE_QA_FIXTURES']=True
    receipt['real_source_trials']=0
    receipt['synthetic_QA_trial_count']=len(validated)
    (root/'stage14_synthetic_hardware_contract.json').write_text(json.dumps(receipt,indent=2))
    print('STAGE14_SYNTHETIC_SOURCE_CONTRACT_QA '+json.dumps(receipt),flush=True)
if __name__=='__main__':main()