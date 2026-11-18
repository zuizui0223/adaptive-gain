"""Actual 10/15/20mps gust study-cluster pre-specified sensitivity tests."""
import importlib.util,unittest
import numpy as np
import pandas as pd
from pathlib import Path
sp=importlib.util.spec_from_file_location("stage79j",Path(__file__).with_name("source_sizefirst_gust_threshold_study_sensitivity.py"))
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

class GustStudySourceTests(unittest.TestCase):
    def fake_rows(self):
        a=[];b=[]
        for i in range(37):
            site=f"study{i%15}"
            base={"Study_id":site,"Network_id":str(i),"Year":"2018"}
            a.append({**base,
                "original_ERA5_fraction_days_10m_gust_ge_10_ms":(.15+.01*i),
                "original_ERA5_fraction_days_10m_gust_ge_15_ms":(.02+.003*i),
                "original_ERA5_fraction_days_10m_gust_ge_20_ms":(.001*i),
                "original_ERA5_daily_max_gust_p95_m_s":10.+.4*i,
                "original_ERA5_period_daily_T_mean_C":12.+(i%7),
                "original_ERA5_period_precip_mm_per_day":1.+(i%5)})
            b.append({**base,
                "original_source_width_null_score_ratio":.4+.2*np.sin(i),
                "original_source_width_local_null_information":1.+i%4})
        return a,b
    def test_original_151_37_source_grain_rejected_if_changed(self):
        with self.assertRaisesRegex(ValueError,"151_37"):
            m.join_original_source([{}],[{}])
    def test_study_environment_controls_and_fixed_gust_thresholds(self):
        self.assertEqual(list(m.EXPOSURE_FIELDS),["gust10","gust15_primary","gust20","gust95"])
        self.assertEqual(m.PRE_FIXED_MIN_STUDIES_WITH_WIND_VARIABILITY,5)
    def test_original_151_37_join_and_study_identity(self):
        a,b=self.fake_rows()
        for i in range(37,151):
            a.append({**a[0],"Study_id":"otherstudy","Network_id":str(i)})
        f,info=m.join_original_source(a,b)
        self.assertEqual(len(f),37)
        self.assertEqual(info["source_original_independent_study_groups"],15)
        self.assertTrue(info["source_climate_scaling_defined_before_admitting_any_bee_outcome"])
    def test_study_wind_constant_no_identification(self):
        a,b=self.fake_rows()
        a=a[:37]
        for i,x in enumerate(a):x["original_ERA5_fraction_days_10m_gust_ge_15_ms"]=.2
        for i in range(37,151):
            a.append({**a[0],"Study_id":"otherstudy","Network_id":str(i)})
        f,_=m.join_original_source(a,b)
        result=m.robust_study_wls(f,"exposure_gust15_primary")
        self.assertEqual(result["status"],"NO_GO_TOO_FEW_STUDIES_WITH_WITHIN_STUDY_GUST_VARIATION")
    def test_count_not_misreported_as_receiver_colour_preference(self):
        self.assertIn("not a fitted",m.__doc__.lower() if m.__doc__ else "")
if __name__=="__main__":unittest.main()
