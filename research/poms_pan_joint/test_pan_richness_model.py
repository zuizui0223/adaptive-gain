import unittest
import numpy as np
import pandas as pd

from pan_richness_model import prepare_matched_context, _fit_one
from site_date_join import build_pan_environment

class PanContextModelTests(unittest.TestCase):
    def fixture(self):
        rng=np.random.default_rng(8727)
        surveys=[];stations=[];flowers=[]
        dates=pd.date_range("2022-05-04",periods=7,freq="15D")
        site_count=20
        for site in range(site_count):
            for di,date in enumerate(dates):
                # Seven distinct spatially paired dates; all five Pan
                # station-sample IDs are declared independently.
                richness=3+((site+2*di)%7)
                for st in range(5):
                    sid=f"P{site}_{di}_{st}"
                    stations.append({"sample_id":sid,"location_code":f"L{site}",
                         "x1km_square":f"G{site}","date":str(date.date()),
                         "year":2022,"pan_trap_station":str(st+1)})
                    for idx in range(st,richness,5):
                        flowers.append({"sample_id":sid,
                            "occurrence_id":f"{sid}_{idx}",
                            "taxon_source":f"Plant{idx}",
                            "source_taxon_version_key":f"Key{idx}",
                            "total_floral_units":rng.integers(1,20),
                            "year":2022})
                for j,wind in enumerate(["Leaves still/moving occasionally",
                                         "Leaves moving gently all the time",
                                         "Leaves moving strongly"]):
                    p=.27+.08*(j==2)+.02*(richness>5)
                    bee=int(rng.binomial(10,p))
                    surveys.append({
                        "sample_id":f"F{site}_{di}_{j}",
                        "location_code":f"L{site}","x1km_square":f"G{site}",
                        "date":str(date.date()),"year":2022,
                        "target_flower_corrected":rng.choice(["Thistle","Clover","Bramble"]),
                        "floral_unit":rng.choice(["flower head","individual flower"]),
                        "floral_unit_count":int(rng.integers(4,40)),
                        "wind_speed":wind,
                        "sunshine":rng.choice(["Entirely in sunshine","Partly in sun and partly shaded","Entirely shaded"]),
                        "count_start_time":rng.choice(["10:15","11:20","12:45","14:10","15:05","16:20"]),
                        "recorder_type":rng.choice(["experienced","beginner","Not stated"]),
                        "flower_cover":rng.choice(["less than half","about half","more than half"]),
                        "bumblebees":bee,"other_flies":10-bee,
                        "all_insects_total":10})
        return (pd.DataFrame(surveys),pd.DataFrame(stations),
                pd.DataFrame(flowers))
    def test_context_gate_and_no_fake_fit_surveys(self):
        fit,s,f=self.fixture()
        pan,report,_=build_pan_environment(s,f)
        d,info=prepare_matched_context(fit,pan)
        self.assertEqual(info["stage3d_covariate_eligible_fit"],len(fit))
        self.assertEqual(info["exact_five_pan_stations_with_flower_taxa"],len(fit))
        self.assertEqual(info["matched_pair_positive_fit_surveys"],len(fit))
        self.assertEqual(info["fit_row_multiplication"],0)
        self.assertEqual(info["model_gate"],"PASS_CONTEXTUAL_OVERLAP")
        self.assertGreater(info["recorded_pan_taxa_distinct_values"],3)
    def test_guild_context_model_and_wind_interaction(self):
        fit,s,f=self.fixture()
        pan,report,_=build_pan_environment(s,f)
        d,support=prepare_matched_context(fit,pan)
        one=_fit_one(d,"richness_main")
        self.assertEqual(one["status"],"FITTED",one.get("error",str(one)))
        self.assertTrue(one["converged"])
        self.assertEqual(one["design_rank"],one["design_columns"])
        interaction=_fit_one(d,"wind_by_richness")
        self.assertEqual(interaction["status"],"FITTED",interaction.get("error",str(interaction)))
        self.assertTrue(0<=interaction["joint_wind_by_richness"]["p"]<=1)
        self.assertIn("strong_wind_OR_at_pan_richness_q75",interaction)
    def test_eligibility_prevents_spatial_imputation(self):
        fit,s,f=self.fixture()
        pan,receipt,_=build_pan_environment(s,f)
        fit.loc[0,"x1km_square"]="different_grid"
        d,support=prepare_matched_context(fit,pan)
        self.assertEqual(support["exact_five_pan_stations_with_flower_taxa"],len(fit)-1)
        self.assertEqual(support["fit_row_multiplication"],0)
    def test_no_model_outcome_can_drive_richness_support_gate(self):
        fit,s,f=self.fixture()
        pan,receipt,_=build_pan_environment(s,f)
        fit.loc[:,"other_flies"]=0
        fit.loc[:,"bumblebees"]=0
        with self.assertRaisesRegex(ValueError,"no paired"):
            prepare_matched_context(fit,pan)

if __name__=="__main__":unittest.main()
