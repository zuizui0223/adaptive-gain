"""Stage40 static flower landmark test fixtures are invented, not bees."""
from __future__ import annotations
import csv
import io
import unittest
import zipfile
from inspect_original_tracks import MEASURED_HEADER
from static_landmark_gate import _profile,assess_original_archive


def mock_track(static_rows=(0,),missing_tag_rows=()):
    x=io.StringIO()
    wr=csv.DictWriter(x,fieldnames=MEASURED_HEADER,lineterminator='\n')
    wr.writeheader()
    for j,dist in enumerate((.06,.025,.04,.009)):
        row={k:'NaN' for k in MEASURED_HEADER}
        for i in range(1,4):
            for k,v in zip('XYZ',(dist+.001*i,0.,0.)):
                row[f'pt{i}_{k}']=str(v)
        if j in missing_tag_rows:
            row['pt1_X']='NaN'
        if j in static_rows:
            for i in range(4,8):
                for axis in 'XYZ':
                    row[f'pt{i}_{axis}']='0.0'
        wr.writerow(row)
    return x.getvalue().encode('utf-8')


def fake_157_archive():
    x=io.BytesIO()
    with zipfile.ZipFile(x,'w',zipfile.ZIP_DEFLATED) as z:
        for i in range(157):
            B=(i%28)+1
            W=0 if i<56 else 1
            path=(f'kinematic data/B{B:02d}_BC7000_F01_S0_P0_'
                  f'T{i+1:03d}_W{W}_C001H001S0001xyzpts.csv')
            z.writestr(path,mock_track())
    return x.getvalue()


class OriginalFloralLandmarkTests(unittest.TestCase):
    def test_static_flower_reference_one_row_and_stage_windows(self):
        a=_profile(mock_track())
        self.assertEqual(a['status'],'ORIGINAL_ONE_LANDMARK_PER_TRACK')
        self.assertEqual(a['landmark_pt7_records'],1)
        self.assertEqual(a['pt4_7_presence'],[1,1,1,1])
        self.assertEqual(a['complete_3tag_frames'],4)
        self.assertEqual(a['valid_consecutive_3tag_pairs'],3)
        self.assertEqual(a['approach_pt2_count'],1)
        self.assertEqual(a['landing_pt2_count'],1)
        self.assertTrue(a['flower_landmark_recorded_as_static_not_animal_tracking'])

    def test_two_static_ref_rows_must_fail_closed(self):
        a=_profile(mock_track(static_rows=(0,1)))
        self.assertEqual(a['status'],'NO_GO_NO_UNIQUE_FLOWER_LANDMARK')
        self.assertEqual(a['landmark_pt7_records'],2)
        self.assertIsNone(a['landing_pt2_count'])

    def test_missing_tag_frames_not_interpolated_to_new_video_frames(self):
        a=_profile(mock_track(missing_tag_rows=(1,)))
        self.assertEqual(a['complete_3tag_frames'],3)
        self.assertEqual(a['valid_consecutive_3tag_pairs'],1)
        self.assertEqual(a['landmark_pt7_records'],1)

    def test_fake_157_zip_all_have_static_flower(self):
        r=assess_original_archive(fake_157_archive())
        self.assertEqual(r['status'],'ORIGINAL_STATIC_FLOWER_LANDMARK_ENCODING_CONFIRMED')
        self.assertEqual(r['pt7_records_per_original_trajectory_distribution'],{1:157})
        self.assertEqual(r['source_archive_file_count'],157)
        self.assertEqual(r['original_track_frames_counted'],628)
        self.assertEqual(r['valid_3moving_tag_frames_counted'],628)
        self.assertEqual(r['consecutive_valid_frame_pairs_for_1000fps_speed'],471)
        self.assertEqual(r['pt4_7_record_totals'],{
          'pt4_nonmissing_frame_total':157,
          'pt5_nonmissing_frame_total':157,
          'pt6_nonmissing_frame_total':157,
          'pt7_nonmissing_frame_total':157})
        self.assertTrue(r['published_calm_tracks_exceed_archived_W0_if_one_file_per_path'])
        self.assertTrue(r['no_verified_original_112_track_selection'])
        self.assertTrue(r['physical_wind_effect_not_fit_by_this_audit'])

    def test_invalid_zip_refusal(self):
        with self.assertRaisesRegex(ValueError,'ORIGINAL_DATA_NOT_A_ZIP'):
            assess_original_archive(b'not an original file')


if __name__=='__main__':
    unittest.main()
