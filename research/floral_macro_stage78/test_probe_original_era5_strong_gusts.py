"""Strong gust exposure must never be mean wind or a visited bee absence."""
import importlib.util,unittest,math
from pathlib import Path
p=Path(__file__).with_name("probe_original_era5_strong_gusts.py")
sp=importlib.util.spec_from_file_location("s78a",p)
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

class OriginalGustSourceChecks(unittest.TestCase):
    def test_gust_thresholds_fixed_before_outcome(self):
        self.assertEqual(m.SOURCE_GUST_THRESHOLDS,(10.,15.,20.))
        self.assertEqual(m.SOURCE_MAXSPEED_THRESHOLD,8.)
        self.assertEqual(m.PILOT_STUDIES,5)
    def test_query_force_era5_daily_gust_metre_per_second(self):
        import urllib.parse
        rows=[{"latitude":50.3,"longitude":11.2},{"latitude":49.2,"longitude":5.0}]
        url=m.query_sites(rows)
        d=urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        self.assertEqual(d["models"],["era5"])
        self.assertEqual(d["wind_speed_unit"],["ms"])
        self.assertIn("wind_gusts_10m_max",d["daily"][0])
        self.assertEqual(d["timezone"],["GMT"])
    def test_gust_count_threshold_includes_exact_boundary(self):
        first={"Study_id":"A","Network_id":"N"}
        dates=[f"2018-06-{day:02d}" for day in range(1,31)]
        values=[0.5]*25+[10.,15.,20.,14.9,21.]
        frame={"daily":{"time":dates,"wind_gusts_10m_max":values,
          "wind_speed_10m_max":[1.]*25+[8.,8.,8.,8.,8.]},
          "daily_units":{"wind_gusts_10m_max":"m/s",
          "wind_speed_10m_max":"m/s"},"utc_offset_seconds":0}
        r=m.original_wind_summary(first,frame)
        self.assertEqual(r["source_daily_max_gust_days_ge_10_ms"],5)
        self.assertEqual(r["source_daily_max_gust_days_ge_15_ms"],3)
        self.assertEqual(r["source_daily_max_gust_days_ge_20_ms"],2)
        self.assertAlmostEqual(r["source_daily_max_gust_fraction_ge_15_ms"],.1)
    def test_missing_weather_day_fails_not_imputed_zero(self):
        first={"Study_id":"A"}
        dates=[f"2018-06-{day:02d}" for day in range(1,31)]
        frame={"daily":{"time":dates,"wind_gusts_10m_max":[None]+[3.]*29,
          "wind_speed_10m_max":[3.]*30},
          "daily_units":{"wind_gusts_10m_max":"m/s",
          "wind_speed_10m_max":"m/s"},"utc_offset_seconds":0}
        with self.assertRaisesRegex(ValueError,"MISSING_GUST_DAYS"):
            m.original_wind_summary(first,frame)
    def test_historical_wind_does_not_become_scent_plume(self):
        self.assertIn("archive-api.open-meteo.com",m.API)
        self.assertEqual(m.YEAR,2018)
        self.assertEqual(m.MONTH,6)
    def test_source_URL_nonarchive_denied(self):
        with self.assertRaisesRegex(ValueError,"NON_OFFICIAL"):
            m.original_api("https://example.com/era5")
if __name__=="__main__":
    unittest.main()
