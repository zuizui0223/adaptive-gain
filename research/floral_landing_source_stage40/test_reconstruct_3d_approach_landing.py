"""Stage40 purely synthetic source-free numerical tests for m/s reconstruction."""
from __future__ import annotations
import csv
import io
import unittest

from inspect_original_tracks import MEASURED_HEADER
from reconstruct_3d_approach_landing import (
    inspect_track,_paired_by_bee,_matched_bee_stiffness_position,_bootstrap_pairs,analyze_original_zip
)


def fake_1000hz_track(*,n=160,internal_gap=False,double_flower=False):
    """Original 21-column schema, simulated tag approaches origin."""
    out=io.StringIO()
    wr=csv.DictWriter(out,fieldnames=MEASURED_HEADER,lineterminator='\n')
    wr.writeheader()
    for i in range(n):
        d=.095-.00055*i
        row={k:'NaN' for k in MEASURED_HEADER}
        for j in range(1,4):
            for axis,val in zip('XYZ',(d+(.001*(j-2)),0.,0.)):
                row[f'pt{j}_{axis}']=str(val)
        if internal_gap and i==30:
            row['pt1_X']='NaN';row['pt2_X']='NaN';row['pt3_X']='NaN'
        if i==0 or (double_flower and i==1):
            for axis in 'XYZ':
                row[f'pt7_{axis}']='0.'
        wr.writerow(row)
    return out.getvalue().encode('utf8')


class OriginalPhysicalSpeedTests(unittest.TestCase):
    def test_constant_ground_velocity_in_real_units_1000fps(self):
        r=inspect_track(fake_1000hz_track(),
                        {'B':'01','P':'0','S':'0','W':'W0'})
        self.assertTrue(r['one_static_flower_center'])
        self.assertTrue(r['valid_tag_frame_contiguous'])
        self.assertTrue(r['min_frames_for_both_stage_estimates'])
        self.assertAlmostEqual(r['approach_m_per_s_exploratory'],.55,delta=.03)
        self.assertAlmostEqual(r['near_flower_m_per_s_exploratory'],.55,delta=.03)
        self.assertAlmostEqual(r['speed_change_landing_minus_approach_m_per_s'],0.,delta=.03)

    def test_internal_missing_frame_is_not_false_one_ms_step(self):
        with self.assertRaisesRegex(ValueError,'NONCONSECUTIVE_PHYSICAL_FRAMES'):
            inspect_track(fake_1000hz_track(internal_gap=True),
                          {'B':'01','P':'0','S':'0','W':'W0'})

    def test_multiple_flower_centers_no_go(self):
        with self.assertRaisesRegex(ValueError,'TRACK_OR_FLOWER_STATIC_REFERENCE'):
            inspect_track(fake_1000hz_track(double_flower=True),
                          {'B':'01','P':'0','S':'0','W':'W0'})

    def test_source_wind_is_not_independent_replicate_of_same_bee(self):
        results=[
           {'B':'01','W':'W0','speed_change_landing_minus_approach_m_per_s':-.10},
           {'B':'01','W':'W0','speed_change_landing_minus_approach_m_per_s':-.30},
           {'B':'01','W':'W1','speed_change_landing_minus_approach_m_per_s':-.05},
           {'B':'02','W':'W0','speed_change_landing_minus_approach_m_per_s':-.50},
           {'B':'02','W':'W1','speed_change_landing_minus_approach_m_per_s':-.20},
        ]
        pairs=_paired_by_bee(results,'speed_change_landing_minus_approach_m_per_s')
        self.assertEqual(len(pairs),2)
        self.assertAlmostEqual(pairs[0][3],.15)
        self.assertAlmostEqual(pairs[1][3],.30)
        x=_bootstrap_pairs(pairs,replicates=100,seed=20261115)
        y=_bootstrap_pairs(pairs,replicates=100,seed=20261115)
        self.assertEqual(x,y)
        self.assertEqual(x['paired_bee_labels'],2)
        self.assertTrue(x['not_author_selected_112_or_colony_robust'])

    def test_conditional_original_bee_stiffness_and_flower_position_matching(self):
        records=[
          {'B':'01','S':'0','P':'0','W':'W0','speed':.10},
          {'B':'01','S':'0','P':'0','W':'W1','speed':.30},
          {'B':'01','S':'0','P':'1','W':'W0','speed':.40},
          {'B':'01','S':'0','P':'1','W':'W1','speed':.50},
          {'B':'02','S':'0','P':'0','W':'W0','speed':.40},
          {'B':'02','S':'1','P':'0','W':'W1','speed':.90},
        ]
        loose=_paired_by_bee(records,'speed')
        strict=_matched_bee_stiffness_position(records,'speed')
        self.assertEqual(len(loose),2)
        self.assertEqual(len(strict),1)
        self.assertEqual(strict[0][0],'01')
        self.assertAlmostEqual(strict[0][3],.15)
        self.assertTrue(_bootstrap_pairs(strict,replicates=50)
                        ['not_author_selected_112_or_colony_robust'])

    def test_ineligible_single_stage_cannot_generate_a_fake_delta(self):
        # A track truncated before reaching the floral landing region:
        r=inspect_track(fake_1000hz_track(n=85),
                        {'B':'03','W':'W1','P':'1','S':'1'})
        self.assertFalse(r['min_frames_for_both_stage_estimates'])
        self.assertIsNone(r['speed_change_landing_minus_approach_m_per_s'])

    def test_malformed_source_header_fails_closed(self):
        with self.assertRaisesRegex(ValueError,'3D_TRACK_SCHEMA_MISMATCH'):
            inspect_track(b'X,Y,Z\n.1,.2,.3\n',
                          {'B':'01','W':'W0'})

    def test_random_zip_does_not_look_like_157_original(self):
        with self.assertRaisesRegex(ValueError,'AUTHENTIC_ORIGINAL_ZIP'):
            analyze_original_zip(b'not zip')


if __name__=='__main__':
    unittest.main()
