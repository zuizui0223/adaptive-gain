"""Stage15 source contract, testable only with MOCK observations in this branch.

A future real study must supply ethically approved source data, concealed
assignments, independent pilot ranges, device calibration, and consent/ethics
requirements; public QA observations are never evidence about real bees.
"""
from __future__ import annotations
from collections import Counter
import math,random
from allocation import audit, MODES, WINDS

STATUS={'measured','verified_no_intake'}
MIN_ARM_PHYSICAL_COMPLIANCE=0.98
ROOT_REVEAL_S=1.0
FIRST_LEAF_DISPLAY_S=2.0
SECOND_LEAF_DISPLAY_S=3.0
FIXED_INTAKE_WINDOW_S=30.0


def mock_telemetry(assignments,seed=20261111):
    """Synthetic perfect-information example only, with injected reward cost."""
    audit(assignments)
    rng=random.Random(seed)
    rows=[]
    for r in assignments:
        mode=r['access_mode']
        # The first leaf is chosen by the animal BEFORE seeing R in precommit
        # arm. Public QA substitutes a deterministic counterbalanced fake.
        pre_leaf='U' if r['block'] in (1,3) else 'V'
        leaf=('U' if r['r']==0 else 'V') if mode=='contingent' else pre_leaf
        second=('U' if r['r']==0 else 'V') if leaf!=('U' if r['r']==0 else 'V') else None
        n=1+int(second is not None)
        val=lambda name:r['u'] if name=='U' else r['v']
        speed=0.1 if r['assigned_wind']=='calm' else 1.0
        mass=max(0.,30.0-2*(n-1)+rng.gauss(0,.5))
        rows.append({
            'trial_id':r['trial_id'],
            'source_pre_root_animal_motor_act_verified':True,
            'source_post_root_animal_motor_act_verified':True,
            'source_first_leaf_selector_origin':'animal',
            'source_second_leaf_selector_origin':'animal' if second is not None else None,
            'pre_root_request_leaf':pre_leaf,
            'pre_root_request_time_s':0.25,
            'pre_root_request_is_binding':mode=='precommit',
            'root_reveal_time_s':ROOT_REVEAL_S,
            'root_observed_value':r['r'],
            'post_root_request_leaf':leaf if mode=='contingent' else None,
            'post_root_request_time_s':1.3,
            'post_root_request_is_binding':mode=='contingent',
            'first_leaf_requested':leaf,
            'first_leaf_reveal_time_s':FIRST_LEAF_DISPLAY_S,
            'observed_first_leaf_value':val(leaf),
            'second_leaf_requested':second,
            'second_leaf_reveal_time_s':SECOND_LEAF_DISPLAY_S if second else None,
            'observed_second_leaf_value':val(second) if second else None,
            'physical_leaf_reveals':n,
            'both_options_accessible_time_s':4.0+(n-1),
            'source_trial_clock_anchor_s':ROOT_REVEAL_S,
            'analysis_window_seconds':FIXED_INTAKE_WINDOW_S,
            'final_target_choice':r['correct_target'],
            'sensor_status':'measured',
            'verified_consumed_sucrose_mg':mass,
            'feeding_contact_verified':True,
            'feeder_mass_calibrated':True,
            'blank_spillage_corrected':True,
            'both_physical_target_options_accessible':True,
            'predictive_cue_visible_at_choice':False,
            'actual_wind_scalar_m_s':speed,
            'actual_wind_vector_xyz_m_s':[0.,speed,0.],
            'actual_wind_turbulence_sd_m_s':.02,
            'source_clock_error_ms':2.0,
            'source_is_synthetic_QA_only':True,
        })
    return rows


def validate_traces(assignments,source_telemetry,pilot_wind_ranges):
    """Check exact source event chronology, no retyped first/second info."""
    audit(assignments)
    if not isinstance(source_telemetry,list) or len(assignments)!=len(source_telemetry):
        raise ValueError('NO_GO_INCOMPLETE_ALL_ASSIGNED_TRIALS')
    if set(pilot_wind_ranges)!=set(WINDS):
        raise ValueError('NO_GO_INDEPENDENT_PILOT_WIND_RANGES_REQUIRED')
    for wind,bounds in pilot_wind_ranges.items():
        if (not isinstance(bounds,(list,tuple)) or len(bounds)!=2 or
            not all(isinstance(v,(int,float)) and math.isfinite(v) for v in bounds) or
            not (0<=bounds[0]<bounds[1])):
            raise ValueError('NO_GO_INVALID_PRELOCKED_PILOT_RANGE')
    if pilot_wind_ranges['calm'][1]>=pilot_wind_ranges['crosswind'][0]:
        raise ValueError('NO_GO_OVERLAPPING_PILOT_WIND_RANGES')
    source={r['trial_id']:r for r in assignments}
    seen=set();arm=Counter();good=Counter();warnings=Counter();validated=[]
    for record in source_telemetry:
        tid=record.get('trial_id')
        if tid not in source or tid in seen:
            raise ValueError('NO_GO_DUPLICATE_OR_UNKNOWN_ORIGINAL_SOURCE_TRIAL')
        seen.add(tid)
        r=source[tid]
        mode=r['access_mode'];wind=r['assigned_wind']
        arm[(wind,mode)]+=1
        # Do not relabel an experimenter-programmed shutter choice as a bee's
        # source-verified voluntary information request.
        if (record.get('source_pre_root_animal_motor_act_verified') is not True or
            record.get('source_post_root_animal_motor_act_verified') is not True):
            raise ValueError('NO_GO_ANIMAL_REQUEST_SENSOR_OR_VIDEO_NOT_VERIFIED')
        if record.get('source_first_leaf_selector_origin')!='animal':
            raise ValueError('NO_GO_NOT_ACTUAL_ANIMAL_QUERY_SOURCE')
        if record.get('source_is_synthetic_QA_only') is not True:
            raise ValueError('NO_GO_REAL_ANIMAL_DATA_NOT_AUTHORIZED_IN_QA_BRANCH')
        if record.get('sensor_status') not in STATUS:
            raise ValueError('NO_GO_SENSOR_FAILURE_IS_NOT_ZERO')
        mass=record.get('verified_consumed_sucrose_mg')
        if not isinstance(mass,(int,float)) or not math.isfinite(mass) or mass<0:
            raise ValueError('NO_GO_NO_CALIBRATED_INTAKE')
        if record['sensor_status']=='verified_no_intake' and mass!=0:
            raise ValueError('NO_GO_VERIFIED_NO_INTAKE_IS_NOT_POSITIVE')
        if mass>0 and record.get('feeding_contact_verified') is not True:
            raise ValueError('NO_GO_MASS_IS_NOT_CONFIRMED_BEE_INGESTION')
        if record.get('feeder_mass_calibrated') is not True or record.get('blank_spillage_corrected') is not True:
            raise ValueError('NO_GO_UNCALIBRATED_OR_UNCORRECTED_SOURCE_MASS')
        choice=record.get('final_target_choice')
        if choice not in (0,1,'no_choice'):
            raise ValueError('NO_GO_INVALID_SOURCE_TARGET_CHOICE')
        if choice=='no_choice' and mass!=0:
            raise ValueError('NO_GO_NO_CHOICE_WITH_POSITIVE_MASS')
        if (record.get('both_physical_target_options_accessible') is not True or
            record.get('predictive_cue_visible_at_choice') is not False):
            raise ValueError('NO_GO_NOT_TWO_REAL_TARGET_OPTIONS_OR_LEAKED_CUE')
        if record.get('analysis_window_seconds')!=FIXED_INTAKE_WINDOW_S or record.get('source_trial_clock_anchor_s')!=ROOT_REVEAL_S:
            raise ValueError('NO_GO_SOURCE_OUTCOME_CLOCK_NOT_ROOT_ANCHORED')
        if record.get('root_observed_value')!=r['r']:
            raise ValueError('NO_GO_SOURCE_ROOT_CUE_VALUE_INVALID')
        pre=record.get('pre_root_request_leaf')
        post=record.get('post_root_request_leaf')
        first=record.get('first_leaf_requested')
        second=record.get('second_leaf_requested')
        if pre not in ('U','V') or first not in ('U','V'):
            raise ValueError('NO_GO_INVALID_SOURCE_FIRST_LEAF')
        t_pre=record.get('pre_root_request_time_s')
        t_root=record.get('root_reveal_time_s')
        t_post=record.get('post_root_request_time_s')
        t_first=record.get('first_leaf_reveal_time_s')
        if (not all(isinstance(t,(float,int)) and math.isfinite(t) for t in (t_pre,t_root,t_post,t_first)) or
            not (0<=t_pre<t_root<t_post<t_first)):
            raise ValueError('NO_GO_SOURCE_PRECOMMIT_OR_CONTINGENT_CUE_CLOCK')
        if abs(t_root-ROOT_REVEAL_S)>.1 or abs(t_first-FIRST_LEAF_DISPLAY_S)>.1:
            raise ValueError('NO_GO_SOURCE_ROOT_OR_FIRST_LEAF_TIMING_DRIFT')
        if mode=='precommit':
            if record.get('pre_root_request_is_binding') is not True or record.get('post_root_request_is_binding') is not False or post is not None or first!=pre:
                raise ValueError('NO_GO_PRECOMMIT_NOT_LOCKED_BEFORE_ROOT')
        else:
            if record.get('pre_root_request_is_binding') is not False or record.get('post_root_request_is_binding') is not True or post not in ('U','V') or first!=post:
                raise ValueError('NO_GO_CONTINGENT_REQUEST_NOT_SELECTED_AFTER_ROOT')
        leaf_value=r['u'] if first=='U' else r['v']
        if record.get('observed_first_leaf_value')!=leaf_value:
            raise ValueError('NO_GO_SOURCE_CUE_VALUE_MISMATCH')
        n=1
        if second is not None:
            if second not in ('U','V') or second==first:
                raise ValueError('NO_GO_SECOND_LEAF_NOT_DISTINCT')
            if record.get('source_second_leaf_selector_origin')!='animal':
                raise ValueError('NO_GO_SECOND_CUE_NOT_SELECTED_BY_ANIMAL')
            t2=record.get('second_leaf_reveal_time_s')
            if not isinstance(t2,(int,float)) or abs(t2-SECOND_LEAF_DISPLAY_S)>.1 or not t_first<t2:
                raise ValueError('NO_GO_SECOND_LEAF_DISPLAY_CLOCK')
            if record.get('observed_second_leaf_value')!=(r['u'] if second=='U' else r['v']):
                raise ValueError('NO_GO_SOURCE_CUE_SECOND_VALUE_MISMATCH')
            n=2
        elif (record.get('second_leaf_reveal_time_s') is not None or
              record.get('observed_second_leaf_value') is not None or
              record.get('source_second_leaf_selector_origin') is not None):
            raise ValueError('NO_GO_SOURCE_UNRECORDED_SECOND_LEAF')
        if record.get('physical_leaf_reveals')!=n:
            raise ValueError('NO_GO_SOURCE_PAID_LEAF_REVEALS_NOT_AUDITED')
        gate=record.get('both_options_accessible_time_s')
        if not isinstance(gate,(int,float)) or abs(gate-(4.0+n-1))>.1:
            raise ValueError('NO_GO_SOURCE_TARGET_ACCESS_TIME_NOT_QUERY_COST')
        speed=record.get('actual_wind_scalar_m_s')
        vector=record.get('actual_wind_vector_xyz_m_s')
        turbul=record.get('actual_wind_turbulence_sd_m_s')
        sync=record.get('source_clock_error_ms')
        if (not isinstance(speed,(int,float)) or not math.isfinite(speed) or speed<0 or
            not isinstance(vector,(tuple,list)) or len(vector)!=3 or
            not all(isinstance(v,(int,float)) and math.isfinite(v) for v in vector) or
            not isinstance(turbul,(int,float)) or not math.isfinite(turbul) or turbul<0 or
            not isinstance(sync,(int,float)) or not math.isfinite(sync) or sync<0):
            raise ValueError('NO_GO_ORIGINAL_WIND_VECTOR_OR_CLOCK_UNMEASURED')
        if abs(math.sqrt(sum(v*v for v in vector))-speed)>.1:
            raise ValueError('NO_GO_ORIGINAL_WIND_VECTOR_SPEED_INCONSISTENT')
        fails=[]
        if not pilot_wind_ranges[wind][0]<=speed<=pilot_wind_ranges[wind][1]:fails.append('source_wind_outside_independent_pilot')
        if sync>5.0:fails.append('source_camera_wind_clock_unsynchronized')
        if not fails:good[(wind,mode)]+=1
        for k in fails:warnings[k]+=1
        validated.append({**record,'access_mode':mode,'assigned_wind':wind,
                          'colony_id':r['colony_id'],'bee_id':r['bee_id'],
                          'correct_target':r['correct_target'],
                          'physical_leaf_reveals':n})
    if seen!=set(source):raise ValueError('NO_GO_MISSING_ALL_ASSIGNED_SOURCE_IDS')
    rates={'__'.join(k):{'source_trials':arm[k],
                        'in_spec':good[k],
                        'fraction':good[k]/arm[k]} for k in sorted(arm)}
    good_all=all(v['fraction']>=MIN_ARM_PHYSICAL_COMPLIANCE for v in rates.values())
    summary={
        'status':'SYNTHETIC_PHYSICAL_GATE_PASSED' if good_all else 'NO_GO_BELOW_ARM_PROTOCOL_COMPLIANCE',
        'source_arms':rates,'source_n_fake_trials':len(assignments),
        'all_assigned_trials_included':True,
        'source_failure_counts':dict(warnings),
        'arm_compliance_floor':MIN_ARM_PHYSICAL_COMPLIANCE,
        'precommit_before_root_contingent_after_root_verified':True,
        'actual_bees_tested':0,
        'all_device_values_synthetic_QA_only':True}
    return summary,validated if good_all else None

if __name__=='__main__':
    import json
    from allocation import generate
    a=generate(4,4)
    s=mock_telemetry(a)
    status,_=validate_traces(a,s,{'calm':(.05,.15),'crosswind':(.95,1.05)})
    print('STAGE15_SOURCE_QA '+json.dumps(status,sort_keys=True))
