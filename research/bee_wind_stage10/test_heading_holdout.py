"""Original 2016 Stage10 method tests; SYNTHETIC trajectories only."""
import math
import tempfile
from pathlib import Path
import unittest
import numpy as np
from heading_holdout import (
    contiguous_runs,velocity_ls,trial_features,fit_ridge,predict,
    leave_one_bee_out, MIN_CONTIGUOUS_FRAMES, EXACT_HEADER, RIDGE_ALPHA,
    FROZEN_SOURCE_SHA256,native_trials,
)

class WindHeadingStage10MethodTests(unittest.TestCase):
    def test_original_21_xyz_header(self):
        self.assertEqual(len(EXACT_HEADER),21)
        self.assertEqual(EXACT_HEADER[:3],("pt1_X","pt1_Y","pt1_Z"))
        self.assertEqual(EXACT_HEADER[-3:],("pt7_X","pt7_Y","pt7_Z"))
        self.assertEqual(len(FROZEN_SOURCE_SHA256),64)
    def test_native_consecutive_frame_runs(self):
        self.assertEqual(contiguous_runs([False,True,True,False,True,False]),[(1,3),(4,5)])
    def test_observed_velocity_slope_uses_only_original_interval(self):
        xyz=np.array([[0.04-0.002*i,.1+.001*i,0] for i in range(40)])
        observed=velocity_ls(xyz,10,30)
        np.testing.assert_allclose(observed,[-2.0,1.0,0.0],atol=1e-10)
        changed=xyz.copy();changed[30:,:]+=100000
        np.testing.assert_allclose(velocity_ls(changed,10,30),observed,atol=1e-10)
    def make_source(self):
        a=np.full((175,21),np.nan,dtype=float)
        for i in range(175):
            x=.085-.0005*i
            a[i,0:3]=[x,-.001,0]
            a[i,3:6]=[x,.001,0]
            a[i,6:9]=[x,0,0]
        # The ORIGINAL data semantics: one observed flower landmark per file.
        a[0,18:21]=[0.,0.,0.]
        return a
    def test_true_early_then_late_landing_is_chronological(self):
        a=self.make_source()
        row,reason=trial_features(a,{"bee":1,"tag":123,"s":0,"p":0,"w":1},"synthetic.csv")
        self.assertIsNone(reason)
        self.assertGreaterEqual(row["n_early_frames"],MIN_CONTIGUOUS_FRAMES)
        self.assertGreaterEqual(row["n_late_frames"],MIN_CONTIGUOUS_FRAMES)
        self.assertLess(row["last_early_frame"],row["first_late_frame"])
        self.assertAlmostEqual(row["early_speed_m_s"],.5,places=7)
        self.assertAlmostEqual(row["x1"][-4],-1,places=7)
        self.assertAlmostEqual(row["y"][0],-1,places=7)
        self.assertEqual(len(row["x0"]),12)
        self.assertEqual(len(row["x1"]),16)
    def test_missing_real_flower_does_not_become_fake_zeros(self):
        a=self.make_source()
        a[:,18:21]=np.nan
        row,reason=trial_features(a,{"bee":1,"tag":123,"s":0,"p":0,"w":0},"synthetic.csv")
        self.assertIsNone(row)
        self.assertEqual(reason,"not_exactly_one_native_observed_flower_landmark")
    def test_single_real_source_landmark_can_be_on_nonbee_frame(self):
        a=self.make_source()
        # The original landmark is only encoded at a trial-level source row.
        a[0,:9]=np.nan
        row,reason=trial_features(a,{"bee":1,"tag":123,"s":0,"p":0,"w":0},"synthetic.csv")
        self.assertIsNone(reason)
        self.assertLess(row["last_early_frame"],row["first_late_frame"])
    def test_ambiguous_multiple_source_landmarks_fail_closed(self):
        a=self.make_source()
        a[1,18:21]=[0.,0.,0.]
        row,reason=trial_features(a,{"bee":1,"tag":123,"s":0,"p":0,"w":0},"synthetic.csv")
        self.assertIsNone(row)
        self.assertEqual(reason,"not_exactly_one_native_observed_flower_landmark")
    def test_no_temporal_crossing_returns_explicit_no_go(self):
        a=self.make_source()
        # Remove actual bee/flower detections in landing ring.
        a[110:,0:3]=np.nan
        row,reason=trial_features(a,{"bee":1,"tag":123,"s":0,"p":0,"w":0},"synthetic.csv")
        self.assertIsNone(row)
        self.assertEqual(reason,"no_later_original_landing_ring")
    def test_group_heldout_bees_and_train_only_ridge(self):
        rows=[]
        for bee in range(12):
            for k in range(4):
                W=k%2
                theta=(bee*17+k*29)%360*math.pi/180
                dx=math.cos(theta);dy=math.sin(theta)
                x0=np.zeros(12);x0[0]=W
                x1=np.r_[x0,[dx,dy,W*dx,W*dy]]
                rows.append({"bee":bee,"wind":W,"orientation":0,"stiffened":0,
                             "x0":x0,"x1":x1,"y":np.array([dx,dy])})
        r=leave_one_bee_out(rows)
        self.assertEqual(len(r),len(rows))
        self.assertGreater(sum(x["gain"] for x in r)/len(r),0)
        t=[x for x in rows if x["bee"]!=0];heldout=[x for x in rows if x["bee"]==0]
        p=predict(fit_ridge(t,"x1"),heldout,"x1")
        poisoned=[dict(row) for row in heldout]
        for row in poisoned:row["y"]=np.array([99.,99.])
        pp=predict(fit_ridge(t,"x1"),poisoned,"x1")
        np.testing.assert_allclose(p,pp,atol=0)
        with self.assertRaisesRegex(ValueError,"RIDGE_ALPHA"):
            fit_ridge(t,"x1",alpha=0.5)
    def test_source_hash_fail_closed_before_reading_bogus_data(self):
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)/"fake.zip";p.write_bytes(b"wrong")
            with self.assertRaisesRegex(ValueError,"SOURCE_MD5_SHA256_CHANGED"):
                native_trials(p)

if __name__=="__main__":unittest.main()
