"""Original conditional petal-width-by-gust-Bombus evidence gates."""
import importlib.util,unittest
from collections import Counter
from pathlib import Path
s=importlib.util.spec_from_file_location("stage79h",Path(__file__).with_name("petal_width_vs_era5_strong_gust_real_Bombus_network_gate.py"))
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

class StrongGustPetalWidth(unittest.TestCase):
    def test_original_width_site_network_positive_Bombus_score(self):
        k=("S","N","2020")
        plants=[("linum perenne",1.),("gentiana lutea",3.)]
        bee={(k,"linum perenne"):Counter(B=1,O=9),
             (k,"gentiana lutea"):Counter(B=9,O=1)}
        env={m.GUST15:"0.2",
            "original_ERA5_period_daily_T_mean_C":"16",
            "original_ERA5_period_precip_mm_per_day":"3"}
        r,reason=m.within_network_null_score(k,plants,bee,env)
        self.assertEqual(reason,"INFORMATIVE")
        self.assertGreater(r["original_source_width_local_null_score"],0)
        self.assertGreater(r["original_source_width_local_null_information"],0)
        self.assertEqual(r["original_source_strong_gust_per10pp"],2.0)

    def test_only_one_guild_recorded_is_not_trait_negative(self):
        k=("S","N","2020")
        p=[("gentiana lutea",3.),("linum perenne",2.)]
        bee={(k,"gentiana lutea"):Counter(O=9),
             (k,"linum perenne"):Counter(O=12)}
        r,why=m.within_network_null_score(k,p,bee,{m.GUST15:"0"})
        self.assertIsNone(r)
        self.assertEqual(why,"ONLY_ONE_IDENTIFIED_BEE_GUILD_IN_NETWORK")

    def test_lack_of_comparison_blocks_inference(self):
        d=m.descriptive_size_gust_relationship([])
        self.assertEqual(d["status"],"NO_GUILD_INFORMATIVE_SIZE_NETWORKS")
        self.assertTrue(d["nullscore_not_binomial_mle"])

    def test_strict_exposure_source_sample_pre_Bombus(self):
        sites=[]
        for i in range(152):
            sites.append({"Study_id":f"S{i%43}","Network_id":str(i),
              "Year":"2018","reanalysis_gust_is_not_visited_hour_actual_wind":"True"})
        traits=[{"Study_id":"S0","Network_id":"0","Year":"2018",
                 "original_plant_literal_accepted_name":s,
                 "source_petal_max_width_cm":v}
                for s,v in (("gentiana lutea","3"),("linum perenne","2"))]
        original,cohorts,info=m.source_preguild_frame(traits,sites)
        self.assertEqual(len(original),152)
        self.assertEqual(len(cohorts),1)
        self.assertEqual(info["source_networks_with_at_least_two_distinct_petal_widths_pre_guild"],1)

    def test_unknown_petal_width_never_zero(self):
        k=("S","N","2020")
        bee={(k,"gentiana lutea"):Counter(B=20,O=1)}
        r,reason=m.within_network_null_score(k,[("gentiana lutea",3.0)],bee,{m.GUST15:"0"})
        self.assertIsNone(r)
        self.assertEqual(reason,"FEWER_THAN_TWO_SOURCE_WIDTHS_WITH_IDENTIFIED_BEE_VISITS")

if __name__=="__main__":unittest.main()
