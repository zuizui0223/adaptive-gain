"""Stage14 synthetic prospective physical source compliance checker.

Real trials require separate ethical approval, private randomization register,
blinded image confirmation and pilot-calibrated instruments; no real animal
data or wind settings are contained in this module.
"""
from __future__ import annotations
from collections import Counter
import math
from allocation import TIMING,REFRESH,REFRESH_PAYLOAD,ORDER,WIND,audit

CUE_TIME_TOL_S=.12
CLOCK_SYNC_MAX_MS=5.
ARM_PROTOCOL_ADHERENCE=.98
STATUS={'measured','verified_no_intake'}

def _valid_ranges(ranges,keys,context):
    if not isinstance(ranges,dict) or set(ranges)!=set(keys):
        raise ValueError('NO_GO_MISSING_INDEPENDENT_PILOT_'+context)
    for arm in keys:
        bounds=ranges[arm]
        if (not isinstance(bounds,(list,tuple)) or len(bounds)!=2 or
            not all(isinstance(x,(float,int)) and math.isfinite(x) for x in bounds) or
            bounds[0]<0 or bounds[0]>=bounds[1]):
            raise ValueError('NO_GO_INVALID_PILOT_'+context)
    return True

def audit_future_source(assignments,telemetry,pilot_wind_ranges,pilot_luminance_ranges):
    """Synthetic-only end-to-end tester for a future independently calibrated trial."""
    audit(assignments)
    _valid_ranges(pilot_wind_ranges,WIND,'WIND')
    _valid_ranges(pilot_luminance_ranges,REFRESH,'PHOTOMETRIC')
    if pilot_wind_ranges['calm'][1]>=pilot_wind_ranges['crosswind'][0]:
        raise ValueError('NO_GO_OVERLAPPING_PILOT_WIND_CALIBRATION')
    if len(telemetry)!=len(assignments):
        raise ValueError('NO_GO_INCOMPLETE_TELEMETRY_ITT')
    source_rows={x['trial_id']:x for x in assignments}
    seen=set();arm=Counter();good=Counter();fail=Counter();valid=[]
    for rec in telemetry:
        trial=rec.get('trial_id')
        if trial in seen or trial not in source_rows:
            raise ValueError('NO_GO_DUPLICATE_OR_UNKNOWN_SOURCE_TRIAL')
        seen.add(trial)
        assigned=source_rows[trial]
        key=(assigned['wind'],assigned['order'],assigned['refresh'])
        arm[key]+=1
        if rec.get('sensor_status') not in STATUS:
            raise ValueError('NO_GO_SENSOR_FAILURE_IS_NOT_MEASURED_ZERO')
        mass=rec.get('verified_consumed_sucrose_mg')
        if not isinstance(mass,(int,float)) or not math.isfinite(mass) or mass<0:
            raise ValueError('NO_GO_UNVERIFIED_REAL_INTAKE_MASS')
        if rec.get('analysis_window_seconds')!=TIMING['window']:
            raise ValueError('NO_GO_TRIAL_MEASUREMENT_WINDOW')
        if rec['sensor_status']=='verified_no_intake' and mass!=0:
            raise ValueError('NO_GO_MISLABELLED_NO_INTAKE')
        if mass>0 and rec.get('feeding_contact_verified') is not True:
            raise ValueError('NO_GO_NO_VIDEO_VERIFIED_REAL_INGESTION')
        if rec.get('feeder_mass_calibrated') is not True or rec.get('blank_spillage_corrected') is not True:
            raise ValueError('NO_GO_UNCALIBRATED_SOURCE_REWARD_MASS')
        if rec.get('observed_predictive_graphics_at_release') is not False:
            raise ValueError('NO_GO_PREDICTIVE_CUES_VISIBLE_AT_GATE')
        if (rec.get('both_options_accessible') is not True or
            rec.get('actual_first_type')!=assigned['first_type'] or
            rec.get('actual_second_type')!=assigned['second_type'] or
            rec.get('actual_refresh_payload')!=REFRESH_PAYLOAD[assigned['refresh']]):
            raise ValueError('NO_GO_PHYSICAL_ALTERNATIVE_CUE_IDENTITY')
        times=(('actual_first_on_s','first_on'),('actual_first_off_s','first_off'),
               ('actual_second_on_s','second_on'),('actual_second_off_s','second_off'),
               ('actual_refresh_on_s','refresh_on'),('actual_refresh_off_s','refresh_off'),
               ('actual_gate_s','gate'))
        numbers=[]
        for field,meaning in times:
            actual=rec.get(field)
            if not isinstance(actual,(int,float)) or not math.isfinite(actual):
                raise ValueError('NO_GO_MISSING_PHYSICAL_SOURCE_TIMESTAMPS')
            if abs(actual-TIMING[meaning])>CUE_TIME_TOL_S:
                raise ValueError('NO_GO_ACTUAL_PHYSICAL_CUE_TIMING')
            numbers.append(actual)
        if not all(x<y for x,y in zip(numbers,numbers[1:])):
            raise ValueError('NO_GO_OVERLAPPING_SOURCE_CUE_EXPOSURES')
        scalar=rec.get('measured_wind_speed_m_s')
        vector=rec.get('measured_wind_xyz_m_s')
        turbulence=rec.get('measured_wind_turbulence_sd_m_s')
        if (not isinstance(scalar,(float,int)) or not math.isfinite(scalar) or scalar<0 or
            not isinstance(vector,(tuple,list)) or len(vector)!=3 or
            not all(isinstance(v,(float,int)) and math.isfinite(v) for v in vector) or
            not isinstance(turbulence,(float,int)) or not math.isfinite(turbulence) or turbulence<0):
            raise ValueError('NO_GO_MISSING_INSTRUMENTED_ORIGINAL_WIND_VECTOR')
        if abs(math.sqrt(sum(v*v for v in vector))-scalar)>.1:
            raise ValueError('NO_GO_WIND_VECTOR_SPEED_INCONSISTENT')
        photo=rec.get('measured_refresh_luminance_cd_m2')
        sync=rec.get('source_max_camera_anemometer_clock_error_ms')
        if (not isinstance(photo,(float,int)) or not math.isfinite(photo) or
            not isinstance(sync,(float,int)) or not math.isfinite(sync) or sync<0):
            raise ValueError('NO_GO_PHOTOMETRIC_OR_SENSOR_SOURCE_MISSING')
        failures=[]
        if not pilot_wind_ranges[assigned['wind']][0]<=scalar<=pilot_wind_ranges[assigned['wind']][1]:
            failures.append('pilot_wind_not_delivered')
        if not pilot_luminance_ranges[assigned['refresh']][0]<=photo<=pilot_luminance_ranges[assigned['refresh']][1]:
            failures.append('photometric_refresh_not_matched')
        if sync>CLOCK_SYNC_MAX_MS:failures.append('sensor_clock_unsynchronized')
        if not failures:good[key]+=1
        for x in failures:fail[x]+=1
        valid.append({'trial_id':trial,'verified_consumed_sucrose_mg':mass,
                      'analysis_window_seconds':TIMING['window'],
                      'sensor_status':rec['sensor_status']})
    if seen!=set(source_rows):raise ValueError('NO_GO_ORIGINAL_ITTS_MISSING')
    source_arms={'__'.join(k):{'total':arm[k],'compliant':good[k],
                 'fraction':good[k]/arm[k]} for k in sorted(arm)}
    compliant=all(x['fraction']>=ARM_PROTOCOL_ADHERENCE for x in source_arms.values())
    receipt={
      'status':'SYNTHETIC_HARDWARE_QA_PASSED' if compliant else
          'NO_GO_BELOW_EACH_ARM_98PCT_HARDWARE_ADHERENCE',
      'no_real_animal_data_in_this_codebase':True,
      'source_arms':source_arms,
      'protocol_failures':dict(fail),
      'all_assigned_trials_retained':len(valid)==len(assignments),
      'no_synthetic_physical_reading_substituted_for_real_source':True,
      'actual_pilot_speed_and_light_limits_required_separately':True,
      'all_verified_no_intakes_are_zero_not_missing':True,
      'minimum_arm_compliance':ARM_PROTOCOL_ADHERENCE,
    }
    return receipt,valid if compliant else None

def synthetic_telemetry(assignments,synthetic_outcomes,calm=.1,crosswind=1.0,light=20.0):
    """Mock readings for tests only; never imply measured wind or real bees."""
    byid={x['trial_id']:x for x in synthetic_outcomes}
    rows=[]
    for x in assignments:
        raw=byid[x['trial_id']]
        speed=calm if x['wind']=='calm' else crosswind
        rows.append({**raw,
           'actual_first_type':x['first_type'],
           'actual_second_type':x['second_type'],
           'actual_refresh_payload':REFRESH_PAYLOAD[x['refresh']],
           'actual_first_on_s':TIMING['first_on'],
           'actual_first_off_s':TIMING['first_off'],
           'actual_second_on_s':TIMING['second_on'],
           'actual_second_off_s':TIMING['second_off'],
           'actual_refresh_on_s':TIMING['refresh_on'],
           'actual_refresh_off_s':TIMING['refresh_off'],
           'actual_gate_s':TIMING['gate'],
           'both_options_accessible':True,
           'observed_predictive_graphics_at_release':False,
           'feeding_contact_verified':raw['verified_consumed_sucrose_mg']>0,
           'feeder_mass_calibrated':True,
           'blank_spillage_corrected':True,
           'measured_wind_speed_m_s':speed,
           'measured_wind_xyz_m_s':[0.,speed,0.],
           'measured_wind_turbulence_sd_m_s':.03,
           'measured_refresh_luminance_cd_m2':light,
           'source_max_camera_anemometer_clock_error_ms':2.0})
    return rows