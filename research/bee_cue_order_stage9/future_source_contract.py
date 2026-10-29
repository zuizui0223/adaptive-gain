"""Future Stage9 sensor/cue/wind provenance gate before colony-level ITT.

This is an INPUT CONTRACT, not a source of empirical bee observations.
Experimental wind-speed ranges must be locked from a private, independent
feasibility pilot BEFORE any real study effects are examined.
No unsuccessful visits dropped; no source failed sensor recoded as zero.
"""
from __future__ import annotations
from collections import Counter
import math
from randomization import WINDS,ORDERS,audit_allocation
from colony_contrast import (
    STATUS_VALID,OBSERVATION_SECONDS,estimate_colony_order_wind_interaction
)

EXPECTED_CUE1_S=2.0
EXPECTED_CUE2_S=4.0
EXPECTED_GATE_S=6.0
MAX_CUE_CLOCK_DEVIATION_S=0.20
MAX_CAMERA_CLOCK_ERROR_MS=5.0
MIN_FULL_PROTOCOL_COMPLIANCE=.98
CHOICES=("left","right","no_choice")

def validate_calibrated_wind_ranges(ranges):
    """Require nonoverlapping pilot-locked exposure limits; no guessed speed."""
    if not isinstance(ranges,dict) or set(ranges)!=set(WINDS):
        raise ValueError("NO_GO_MISSING_INDEPENDENT_PILOT_WIND_CALIBRATION")
    for arm,(lo,hi) in ranges.items():
        if not all(isinstance(x,(int,float)) and math.isfinite(x)
                   for x in (lo,hi)):
            raise ValueError("NO_GO_BAD_WIND_CALIBRATION_NUMBERS")
        if lo<0 or hi<=lo:
            raise ValueError("NO_GO_INVALID_REAL_WIND_RANGE")
    if ranges["calm"][1]>=ranges["crosswind"][0]:
        raise ValueError("NO_GO_EXPOSURE_CALIBRATION_RANGES_OVERLAP")
    return True

def audit_real_trial_telemetry(assignment,source_telemetry,calibrated_ranges,
                               min_compliance=MIN_FULL_PROTOCOL_COMPLIANCE):
    """Return health receipt and an all-arm ITT sample only if recording valid."""
    audit_allocation(assignment)
    validate_calibrated_wind_ranges(calibrated_ranges)
    if len(assignment)!=len(source_telemetry):
        raise ValueError("NO_GO_REAL_RANDOMIZED_TRIALS_WITHOUT_SOURCE_TELEMETRY")
    byid={r["trial_id"]:r for r in assignment}
    seen=set();compliance=Counter();fail=Counter()
    validated=[]
    per_arm=Counter();per_arm_good=Counter()
    for original in source_telemetry:
        key=original.get("trial_id")
        if key not in byid or key in seen:
            raise ValueError("NO_GO_REAL_DUPLICATED_OR_UNKNOWN_TRIAL_DEVICE_ROW")
        seen.add(key)
        assigned=byid[key]
        arm=(assigned["assigned_wind"],assigned["assigned_cue_order"])
        per_arm[arm]+=1
        status=original.get("sensor_status")
        if status not in STATUS_VALID:
            raise ValueError("NO_GO_REAL_MISSING_TRIAL_OUTCOME_IN_STUDY")
        if original.get("analysis_window_seconds")!=OBSERVATION_SECONDS:
            raise ValueError("NO_GO_REAL_TRIAL_WINDOW_CHANGED")
        value=original.get("verified_consumed_sucrose_mg")
        if (not isinstance(value,(float,int)) or
            not math.isfinite(value) or value<0):
            raise ValueError("NO_GO_REAL_SUCROSE_MASS_UNVERIFIED")
        choice=original.get("choice")
        if choice not in CHOICES:
            raise ValueError("NO_GO_REAL_UNKNOWN_CHOICE_CODE")
        if (choice=="no_choice" and value!=0) or (
            status=="verified_no_intake" and value!=0):
            raise ValueError("NO_GO_REAL_CONTRADICTORY_NO_INTAKE_OR_NO_CHOICE")
        if (value>0 and
            original.get("feeding_contact_verified") is not True):
            raise ValueError("NO_GO_REAL_POSITIVE_INTAKE_NOT_LINKED_TO_BEE_FEEDING")
        if (original.get("feeder_mass_calibrated") is not True or
            original.get("blank_spillage_corrected") is not True):
            raise ValueError("NO_GO_REAL_UNCALIBRATED_MASS_LOSS_NOT_CONSUMPTION")
        timing=[
            original.get("cue1_actual_s"),original.get("cue2_actual_s"),
            original.get("gate_actual_s")
        ]
        if not all(isinstance(t,(int,float)) and math.isfinite(t) for t in timing):
            raise ValueError("NO_GO_MISSING_PHYSICAL_CUE_REVEAL_TIMESTAMPS")
        if not timing[0]<timing[1]<timing[2]:
            raise ValueError("NO_GO_REAL_INVERTED_CUE_PHYSICAL_TIME")
        actual_wind=original.get("measured_wind_m_s")
        if not isinstance(actual_wind,(int,float)) or not math.isfinite(actual_wind) or actual_wind<0:
            raise ValueError("NO_GO_REAL_NO_LOCAL_ANEMOMETER_MEASUREMENT")
        # Require actual instrumented 3D airflow, not only an operator's
        # categorical wind label or a scalar fan preset.
        vector=original.get("measured_wind_xyz_m_s")
        turbulence=original.get("measured_wind_turbulence_sd_m_s")
        if (not isinstance(vector,(tuple,list)) or len(vector)!=3 or
            not all(isinstance(x,(int,float)) and math.isfinite(x)
                    for x in vector)):
            raise ValueError("NO_GO_REAL_MISSING_3D_WIND_DIRECTION")
        if (not isinstance(turbulence,(int,float)) or
            not math.isfinite(turbulence) or turbulence<0):
            raise ValueError("NO_GO_REAL_MISSING_WIND_TURBULENCE")
        vector_speed=math.sqrt(sum(x*x for x in vector))
        if abs(vector_speed-actual_wind)>.10:
            raise ValueError("NO_GO_REAL_WIND_VECTOR_AND_SPEED_INCONSISTENT")
        sync=original.get("max_camera_anemometer_clock_error_ms")
        if not isinstance(sync,(int,float)) or not math.isfinite(sync) or sync<0:
            raise ValueError("NO_GO_REAL_MISSING_SENSOR_SYNCHRONIZATION_RECORD")
        cue_ok=all(
            abs(actual-target)<=MAX_CUE_CLOCK_DEVIATION_S
            for actual,target in zip(timing,
                                     (EXPECTED_CUE1_S,EXPECTED_CUE2_S,
                                      EXPECTED_GATE_S))
        )
        both_open=(original.get("left_accessible_at_release") is True and
                   original.get("right_accessible_at_release") is True)
        wind_ok=calibrated_ranges[assigned["assigned_wind"]][0] <= actual_wind <= (
            calibrated_ranges[assigned["assigned_wind"]][1])
        sync_ok=sync<=MAX_CAMERA_CLOCK_ERROR_MS
        failures=[]
        if not cue_ok:failures.append("cue_hardware_clock_out_of_tolerance")
        if not both_open:failures.append("one_flower_unavailable_at_release")
        if not wind_ok:failures.append("assigned_wind_not_physically_delivered")
        if not sync_ok:failures.append("source_clocks_out_of_sync")
        compliance.update({code:1 for code in failures})
        for f in failures:fail[f]+=1
        if not failures:per_arm_good[arm]+=1
        validated.append({
            "trial_id":key,
            "analysis_window_seconds":OBSERVATION_SECONDS,
            "sensor_status":status,
            "verified_consumed_sucrose_mg":value})
    if seen!=set(byid):
        raise ValueError("NO_GO_REAL_ITTs_SOURCE_TRIAL_LINKAGE_INCOMPLETE")
    rates={f"{w}__{o}":{
        "assigned_trials":per_arm[(w,o)],
        "all_hardware_steps_in_spec":per_arm_good[(w,o)],
        "compliance_fraction":per_arm_good[(w,o)]/per_arm[(w,o)]}
        for w in WINDS for o in ORDERS}
    min_arm=min(x["compliance_fraction"] for x in rates.values())
    ready=min_arm>=min_compliance
    receipt={
        "status":"HARDWARE_AND_MASS_CONTRACT_PASSED" if ready
                else "NO_GO_REAL_PROTOCOL_ADHERENCE_BELOW_98_PERCENT",
        "actual_animal_source_data_only_when_supplied":True,
        "not_a_prior_experiment_or_measured_data":False,
        "n_assigned_trials":len(byid),
        "source_arms":rates,
        "minimum_required_arm_adherence":min_compliance,
        "minimum_observed_arm_adherence":min_arm,
        "per_trial_protocol_failure_histogram":dict(fail),
        "ITT_retains_every_randomized_trial_regardless_of_adherence":True,
        "source_exposure_values_from_independent_pilot_not_automatically_guessed":True,
        "sensor_failure_NOT_equivalent_to_zero_sucrose":True
    }
    return receipt, validated if ready else None

def make_synthetic_QA_telemetry(assignments,outcomes,
                               calm=.10,crosswind=1.0):
    """Public tests only. Invented readings NEVER asserted for real bees."""
    raw=[]
    mapped={x["trial_id"]:x for x in outcomes}
    for r in assignments:
        v=mapped[r["trial_id"]]
        mass=v["verified_consumed_sucrose_mg"]
        raw.append({
            **v,
            "choice":"left" if mass>0 else "no_choice",
            "feeding_contact_verified":bool(mass>0),
            "feeder_mass_calibrated":True,
            "blank_spillage_corrected":True,
            "cue1_actual_s":2.0,
            "cue2_actual_s":4.0,
            "gate_actual_s":6.0,
            "left_accessible_at_release":True,
            "right_accessible_at_release":True,
            "measured_wind_m_s":calm if r["assigned_wind"]=="calm" else crosswind,
            "measured_wind_xyz_m_s":[0.0,calm if r["assigned_wind"]=="calm" else crosswind,0.0],
            "measured_wind_turbulence_sd_m_s":0.02,
            "max_camera_anemometer_clock_error_ms":2.0})
    return raw

def analyze_future_source(assignment,source_telemetry,pilot_wind_ranges):
    """Apply physical source audit before a colony-based experiment estimate."""
    receipt,validated=audit_real_trial_telemetry(
        assignment,source_telemetry,pilot_wind_ranges)
    if validated is None:
        return {"status":"NO_GO_CAUSAL_PROTOCOL_SOURCE_ADHERENCE",
                "hardware_audit":receipt}
    return {"status":"SOURCE_TELEMETRY_AND_COLONY_ESTIMATOR_APPLIED",
            "hardware_audit":receipt,
            "colony_estimand":estimate_colony_order_wind_interaction(
                assignment,validated)}
