"""Audit which original sources co-measure the necessary floral cue-stage components.

Source co-occurrence is NOT an estimated effect. 1 indicates a modality was
covered inside a source, not that the cue helped pollinators. 0 means unmeasured,
unverified, or unavailable; it never means that a trait was biologically absent.
"""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

FEATURES=('far_visual_same_source','near_visual_same_source',
 'volatile_emission_same_source','learning_discrimination_same_source',
 'wind_exposure_same_source','landing_success_or_kinematics_same_source',
 'field_visitor_response_same_source','fitness_same_source')
TESTS={
    'distal_and_near_signal_with_local_wind_and_visit':(
       'far_visual_same_source','near_visual_same_source',
       'wind_exposure_same_source','field_visitor_response_same_source'),
    'scent_plume_with_wind_and_field_visits':(
       'volatile_emission_same_source','wind_exposure_same_source',
       'field_visitor_response_same_source'),
    'learning_vs_visual_field_visits':(
       'far_visual_same_source','learning_discrimination_same_source',
       'field_visitor_response_same_source'),
    'wind_visual_guide_landing':(
       'wind_exposure_same_source','near_visual_same_source',
       'landing_success_or_kinematics_same_source'),
    'full_cue_route_and_fitness':FEATURES,
}

def audit(rows:list[dict])->dict:
    if len({r['source_id'] for r in rows})!=len(rows):
        raise ValueError('DUPLICATED_SOURCE_ID')
    for r in rows:
        for col in FEATURES+('raw_verified_by_existing_pipeline','site_time_coincident'):
            if r[col] not in ('0','1'):raise ValueError('UNVERIFIED_NONBINARY_LEDGER_'+col)
    output={}
    for test,cols in TESTS.items():
        matches=[r for r in rows if all(r[c]=='1' for c in cols)]
        output[test]={
           'necessary_same_source_modalities':list(cols),
           'original_source_count':len(matches),
           'source_ids':[r['source_id'] for r in matches],
           'raw_currently_verified_source_count':sum(r['raw_verified_by_existing_pipeline']=='1' for r in matches),
           'matched_site_time_source_count':sum(r['site_time_coincident']=='1' for r in matches),
           'inference_status':('SOURCE_MATERIAL_REQUIRES_DESIGN_REVIEW' if matches
                               else 'NO_SAME_SOURCE_COVERAGE_NOT_A_NULL_ECOLOGICAL_EFFECT'),
        }
    output['scope_notes']=[
        'Stage79 petal width is a third-party botanical proxy, not measured approach distance.',
        'ERA5 10m daily gust is a source study-month exposure, not actual wind around bee or odor plume.',
        'Laboratory artificial flowers do not create independent botanical taxa or field macro replicates.',
        'Raw-unverified data cannot be relabelled as downloaded, re-extracted, or inaccessible forever.',
        'Within-source co-measurement is necessary but not sufficient for true site-time or causal identification.',
        'Missing modality means no source evidence; it never means trait or insect phenotype is absent.',
        'Original EuPPollNet publication explicitly resolves 52 studies versus 54 Study IDs: a single study was split into ID 23, 24 and 25 for three habitats. Publication-level clustering, not label count, is required for independence.',
    ]
    output['schema']='stage80_original_source_stage_cooccurrence_NOT_effect_size_meta_analysis'
    output['original_source_rows']=len(rows)
    return output

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--ledger',type=Path,default=Path(__file__).with_name('source_stage_ledger.csv'))
    p.add_argument('--out',type=Path)
    a=p.parse_args()
    with a.ledger.open(newline='',encoding='utf-8') as f:res=audit(list(csv.DictReader(f)))
    body=json.dumps(res,indent=2,ensure_ascii=False,sort_keys=True)+'\n'
    if a.out:
        a.out.parent.mkdir(exist_ok=True,parents=True)
        a.out.write_text(body,encoding='utf-8')
    else:print(body)
if __name__=='__main__':main()
