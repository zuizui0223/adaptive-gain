"""Stage39 QA with invented in-memory 3D trajectories only, no real bee rows."""
from __future__ import annotations

import csv
import io
import unittest
import zipfile

from inspect_original_tracks import (
    MEASURED_HEADER,profile_track,profile_original_kinematic_archive,
)


def fake_track(*,n=5,drop_last=False):
    out=io.StringIO()
    wr=csv.writer(out,lineterminator='\n')
    wr.writerow(MEASURED_HEADER)
    for i in range(n):
        vals=[]
        for j in range(7):
            vals.extend((.01*i+.001*j,.02*i,.03*i))
        if drop_last and i==n-1:
            vals[0]='NaN';vals[1]='';vals[2]='NA'
        wr.writerow(vals)
    return out.getvalue().encode('utf8')


def fake_complete_archive():
    output=io.BytesIO()
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as f:
        for i in range(157):
            bee=(i%28)+1
            wind=0 if i<56 else 1
            file=(f'kinematic data/B{bee:02d}_BC7000_F01_S0_P0_'
                  f'T{i+1:03d}_W{wind}_C001H001S0001xyzpts.csv')
            f.writestr(file,fake_track(n=4))
        f.writestr('kinematic data/analysis_code.m',
                   'sampleRate = 1000; butter(5,100); use xyzpts; DLT')
        f.writestr('__MACOSX/kinematic data/._fake.xyzpts.csv',b'not original')
    return output.getvalue()


class OriginalKinematicSourceGrainTests(unittest.TestCase):
    def test_frame_marker_coordinate_profile(self):
        x=profile_track(fake_track(n=5))
        self.assertEqual(x['frames'],5)
        self.assertEqual(x['complete_7_marker_frames'],5)
        self.assertEqual(x['at_least_one_complete_marker_frames'],5)
        self.assertEqual(x['marker_3d_complete_per_point'],[5]*7)
        self.assertEqual(x['all_coordinates_valid_fraction'],1.)
        self.assertTrue(x['source_header_21_marker_coordinates_verified'])
        self.assertTrue(x['no_assumed_physical_coordinate_units'])

    def test_missing_marker_triplet_cannot_be_called_complete(self):
        x=profile_track(fake_track(drop_last=True))
        self.assertEqual(x['frames'],5)
        self.assertEqual(x['marker_3d_complete_per_point'][0],4)
        self.assertEqual(x['complete_7_marker_frames'],4)
        self.assertEqual(x['at_least_one_complete_marker_frames'],5)
        self.assertEqual(x['marker1_valid_frames'],4)
        self.assertLess(x['all_coordinates_valid_fraction'],1.)

    def test_numeric_matched_source_header_is_mandatory(self):
        with self.assertRaisesRegex(ValueError,'MARKER_HEADER_NOT_VALIDATED'):
            profile_track(b'x,y,z\n0,1,2\n')

    def test_coordinate_row_arity_fails_closed(self):
        header=','.join(MEASURED_HEADER)
        with self.assertRaisesRegex(ValueError,'COORDINATE_ROW_ARITY'):
            profile_track((header+'\n1,2,3\n').encode())

    def test_invalid_numeric_source_value_fails_closed(self):
        row=','.join(['not_a_number']+['1']*20)
        with self.assertRaisesRegex(ValueError,'NON_NUMERIC_SOURCE_COORDINATE'):
            profile_track((','.join(MEASURED_HEADER)+'\n'+row+'\n').encode())

    def test_no_source_rows_cannot_establish_a_track(self):
        with self.assertRaisesRegex(ValueError,'EMPTY_SOURCE_TRACK'):
            profile_track((','.join(MEASURED_HEADER)+'\n').encode())

    def test_complete_fake_archive_tracks_not_equal_published_selected_cohort(self):
        audit=profile_original_kinematic_archive(fake_complete_archive())
        self.assertEqual(audit['source_trial_file_count'],157)
        self.assertEqual(audit['source_filename_B_labels'],28)
        self.assertEqual(audit['source_filename_W0_W1_file_count'],
                         {'W0':56,'W1':101})
        self.assertEqual(audit['total_original_frame_rows'],628)
        self.assertEqual(audit['paper_selected_tracks_primary_conditions'],112)
        self.assertEqual(audit['paper_selected_W0_W1'],{'W0':60,'W1':52})
        self.assertTrue(audit['published_112_selected_not_equal_157_original_files'])
        self.assertFalse(audit['physical_speed_or_deceleration_measured_m_s'])
        self.assertTrue(audit['no_original_track_rows_or_matlab_code_redistributed'])

    def test_invalid_source_zip_is_rejected_before_real_claim(self):
        with self.assertRaisesRegex(ValueError,'ORIGINAL_LANDING_ZIP_INVALID'):
            profile_original_kinematic_archive(b'not a ZIP')

    def test_duplicate_missing_filename_wind_condition_is_no_go(self):
        data=fake_complete_archive()
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            all_files={x:z.read(x) for x in z.namelist() if 'W1' not in x}
        output=io.BytesIO()
        with zipfile.ZipFile(output,'w') as z:
            for k,v in all_files.items():z.writestr(k,v)
        with self.assertRaisesRegex(ValueError,'ORIGINAL_157_FILES_28_LABELS_CHANGED'):
            profile_original_kinematic_archive(output.getvalue())


if __name__=='__main__':
    unittest.main()
