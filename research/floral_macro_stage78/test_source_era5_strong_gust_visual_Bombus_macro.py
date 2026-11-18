"""Study-balanced strong gust data admission and compositional uncertainty guards."""
from __future__ import annotations
import importlib.util,datetime,unittest
from pathlib import Path
from collections import defaultdict

p=Path(__file__).with_name("source_era5_strong_gust_visual_Bombus_macro.py")
sp=importlib.util.spec_from_file_location("stage78b",p)
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

class SourceStrongWindMacroTests(unittest.TestCase):
    def test_gust_primary_15mps_not_climate_mean_wind(self):
        self.assertEqual(m.GUST_MAIN_THRESHOLD,15)
        self.assertEqual(m.GUST_THRESHOLDS,(10,15,20))
        self.assertEqual(m.MAX_NETWORKS_PER_STUDY,4)
        self.assertIn("wind_gusts_10m_max",m.DAILY_VARS)

    def test_request_same_original_study_year_observed_month(self):
        sites=[{"Study_id":"S","Network_id":"N","Year":"2018",
                "lat":53.03,"lon":-6.1,"original_visited_months":[6,7]},
               {"Study_id":"S2","Network_id":"B","Year":"2018",
                "lat":58.88,"lon":26.3,"original_visited_months":[6]}]
        tasks=m.build_requests(sites)
        self.assertEqual(len(tasks),2)
        self.assertEqual(tasks[0]["begin"],datetime.date(2018,6,1))
        self.assertEqual(tasks[0]["end"],datetime.date(2018,6,30))
        self.assertEqual(tasks[1]["end"],datetime.date(2018,7,31))
        self.assertIn("wind_speed_unit=ms",tasks[0]["original_API_URL"])
        self.assertIn("models=era5",tasks[0]["original_API_URL"])

    def test_era5_day_series_missing_not_mean_zero(self):
        start=datetime.date(2018,6,1)
        end=datetime.date(2018,6,30)
        dates=[(start+datetime.timedelta(days=i)).isoformat() for i in range(30)]
        fake={"daily":{"time":dates,**{v:[3.]*30 for v in m.DAILY_VARS}},
           "daily_units":{"wind_gusts_10m_max":"m/s","wind_speed_10m_max":"m/s"},
           "utc_offset_seconds":0}
        weather=m.source_days(fake,start,end)
        self.assertEqual(len(weather["wind_gusts_10m_max"]),30)
        fake["daily"]["wind_gusts_10m_max"][0]=None
        with self.assertRaisesRegex(ValueError,"MISSING_DAILY_VALUE"):
            m.source_days(fake,start,end)

    def test_source_ERA5_gust_exposure_indices_are_day_weighted(self):
        base={"Study_id":"S1","Network_id":"N1","Year":"2018",
              "lat":50.1,"lon":10.0,"original_visited_months":[6],
              "source_original_hue_species_count":3,
              "source_original_yellow_hue_species_count":1}
        wind={v:[0.]*30 for v in m.DAILY_VARS}
        wind["wind_gusts_10m_max"]=[5.]*20+[12.]*5+[15.]*4+[21.]
        wind["wind_speed_10m_max"]=[5.]*24+[8.]*6
        wind["temperature_2m_mean"]=[15.]*30
        wind["precipitation_sum"]=[1.]*30
        wind["shortwave_radiation_sum"]=[20.]*30
        source={(base["Study_id"],base["Network_id"],base["Year"]):{6:wind}}
        result=m.aggregate_exposure([base],source)[0]
        self.assertAlmostEqual(result["original_ERA5_fraction_days_10m_gust_ge_10_ms"],10/30)
        self.assertAlmostEqual(result["original_ERA5_fraction_days_10m_gust_ge_15_ms"],5/30)
        self.assertAlmostEqual(result["original_ERA5_fraction_days_10m_gust_ge_20_ms"],1/30)
        self.assertAlmostEqual(result["original_ERA5_period_daily_T_mean_C"],15)
        self.assertEqual(result["original_ERA5_period_precip_total_mm"],30)
        self.assertTrue(result["original_source_visit_months_selection_may_depend_on_observation"])

    def test_original_source_month_missing_is_not_extreme_zero(self):
        x={"Study_id":"S1","Network_id":"N","Year":"2018",
           "original_visited_months":[4,5]}
        with self.assertRaisesRegex(ValueError,"INCOMPLETE"):
            m.aggregate_exposure([x],{("S1","N","2018"):{}})

    def test_input_fixed_effect_wind_will_not_imply_scent_measured(self):
        self.assertIn("MAX_GUST",m.__doc__.upper() if m.__doc__ else "")

if __name__=="__main__":
    unittest.main()
