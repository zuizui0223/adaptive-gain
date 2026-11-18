"""Stage77B source-free path algebra/absence/cluster identification controls."""
import importlib.util,unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd

p=Path(__file__).with_name("source_observational_visual_wind_climate_Bombus_piecewise.py")
sp=importlib.util.spec_from_file_location("stage77b_piecewise",p)
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

def toy_source_frame():
    rng=np.random.default_rng(77)
    rows=[]
    for study in range(12):
        for site in range(10):
            vis=(site-4.5)/4.5+0.1*rng.normal()
            w=(site-4.5)/4.5+study*0.11
            t=rng.normal()+study*.3
            p=rng.normal()-.2*study
            rad=rng.normal()
            v=rng.normal()
            y=0.45*vis-0.25*w+0.1*t+0.05*p+rng.normal(0,.15)
            rows.append({
               "Study_id":f"study{study}",
               "visual_reported_yellow_logodds":vis,
               "Bombus_observed_bee_logodds":y,
               "clim_wind":w,"clim_temperature":t,"clim_precipitation":p,
               "clim_srad":rad,"clim_vapr":v,
            })
    df=pd.DataFrame(rows)
    for key in ("wind","temperature","precipitation","srad","vapr"):
        df["z_"+key]=(df["clim_"+key]-df["clim_"+key].mean())/df["clim_"+key].std()
    return df

class ActualPathSourceControls(unittest.TestCase):
    def test_source_sha_locks_are_original_artifact_bytes(self):
        self.assertTrue(all(len(x)==64 for x in m.SOURCES.values()))
        with self.assertRaisesRegex(ValueError,"SOURCE_ARTIFACT_SHA256_CHANGED"):
            m.verify(Path(__file__),m.SOURCES["nhm"])

    def test_cohort_filters_without_real_Bombus_outcome(self):
        df=pd.DataFrame({
            "n_reported_hue_species":[1,2,2,3],
            "n_distinct_reported_hue_families":[1,1,2,3],
            "B":[5000,0,0,0]})
        a=m.to_sample(df,"cross_hue")
        self.assertEqual(len(a),2)
        b=m.to_sample(df,"two_species")
        self.assertEqual(len(b),3)
        df.loc[:,"B"]=0
        self.assertEqual(a.index.tolist(),m.to_sample(df,"cross_hue").index.tolist())

    def test_climate_standardization_before_guild_not_using_visitor_values(self):
        df=toy_source_frame()
        df["source_Bombus_present"]=0
        x,report=m.standardized_within_preoutcome(df)
        df["source_Bombus_present"]=100
        y,report2=m.standardized_within_preoutcome(df)
        self.assertTrue((x["z_wind"]==y["z_wind"]).all())
        self.assertEqual(report,report2)
        self.assertTrue(report["source_never_restandardized_from_observed_Bombus_outcomes"])
        self.assertAlmostEqual(x["z_wind"].mean(),0,places=6)

    def test_source_model_uses_study_fixed_effects_and_study_cluster(self):
        df=toy_source_frame()
        fit,summary=m.fit_descriptive_path(m.MODEL_FORMULA_B,df)
        self.assertEqual(summary["observational_network_units"],120)
        self.assertEqual(summary["source_independent_study_ID_groups"],12)
        self.assertEqual(summary["source_design_matrix_columns"],
                         summary["source_design_matrix_rank"])
        terms={x["term"] for x in summary["observed_coefficient_and_cluster_sampling_intervals"]}
        self.assertIn("visual_reported_yellow_logodds:z_wind",terms)
        self.assertIn("z_temperature",terms)
        self.assertTrue(summary["cluster_robust_interval_NOT_causal_SEM_interval"])

    def test_leave_study_out_fragility_is_not_false_independent_sample(self):
        df=toy_source_frame()
        diag=m.leave_study_out(m.MODEL_FORMULA_B,df,
            ["visual_reported_yellow_logodds","visual_reported_yellow_logodds:z_wind"])
        self.assertEqual(diag["source_study_leave_one_out_n"],12)
        self.assertIn("visual_reported_yellow_logodds",
                      diag["source_study_leave_one_out_terms"])
        self.assertTrue(diag["site_n_study_exclusion_does_not_make_species_independent"])

    def test_low_study_support_is_fatal_not_false_precision(self):
        df=toy_source_frame().loc[lambda x:x["Study_id"]=="study1"]
        with self.assertRaisesRegex(ValueError,"SAMPLE_TOO_SMALL"):
            m.fit_descriptive_path(m.MODEL_FORMULA_B,df)

    def test_thin_source_collinear_test_numerically_rank_limited(self):
        df=toy_source_frame()
        df["z_precipitation"]=df["z_temperature"]
        _,summary=m.fit_descriptive_path(m.MODEL_FORMULA_B,df)
        self.assertLess(summary["source_design_matrix_rank"],
                        summary["source_design_matrix_columns"])
        self.assertGreater(summary["source_condition_number"],1e10)

    def test_VOC_path_is_no_source_indicators_not_free_to_estimate(self):
        self.assertIn("visual_reported_yellow_logodds",m.MODEL_FORMULA_B)
        self.assertNotIn("VOC",m.MODEL_FORMULA_B)
        self.assertNotIn("VOC",m.MODEL_FORMULA_V)
        self.assertIn("z_wind",m.MODEL_FORMULA_B)

if __name__=="__main__":
    unittest.main()
