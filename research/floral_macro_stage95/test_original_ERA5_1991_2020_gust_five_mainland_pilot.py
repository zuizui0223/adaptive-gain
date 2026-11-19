"""Stage95 predeclared full 30-year climatological gust and uncertainty guards."""
import unittest,datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from original_ERA5_1991_2020_gust_five_mainland_pilot import (
    date_range,climatology,parse_decade,api_url,original_pilot_sites,
    YEARS
)

class Era5ThirtyYearClimatology(unittest.TestCase):
    def synthetic(self):
        rows=[]
        for day in date_range(1991,2020):
            warm=int(day[5:7]) in (6,7)
            temp=20 if warm else 0
            gust=15.0 if day.endswith("-01") else (20.0 if warm else 0.0)
            rows.append((day,gust,temp))
        return rows
    def test_true_30yr_leap_days(self):
        self.assertEqual(len(date_range(1991,2020)),10958)
        self.assertEqual(len(YEARS),3)
    def test_warm_months_from_all_30yr_monthly_temperature(self):
        v=climatology(self.synthetic())
        self.assertEqual(v["source_eligible_climatological_months_T2m_strict_above_5C"],[6,7])
        self.assertEqual(v["source_ERA5_observed_30yr_days"],10958)
    def test_strict_gt_is_not_gte_at_15(self):
        v=climatology(self.synthetic())
        self.assertLess(v["source_primary_fraction_days_daily_gust_strict_above_15_ms"],
                        v["source_fraction_gust_greater_OR_EQUAL_15_ms_DIAGNOSTIC_NOT_PRIMARY"])
    def test_no_warm_climatological_months_missing_not_zero(self):
        d=[(date,g,0.0) for date,g,_ in self.synthetic()]
        v=climatology(d)
        self.assertEqual(v["source_eligible_days"],0)
        self.assertIsNone(v["source_primary_fraction_days_daily_gust_strict_above_15_ms"])
    def test_days_from_one_visit_year_not_enough(self):
        with self.assertRaises(ValueError):
            climatology(self.synthetic()[:365])
    def test_daily_gap_fails_not_filled(self):
        d=self.synthetic()
        d[400]=d[399]
        with self.assertRaises(ValueError):
            climatology(d)
    def test_era5_daily_units_and_time_are_checked(self):
        dates=date_range(1991,2000)
        frame={"daily":{"time":dates,
                "wind_gusts_10m_max":[12.0]*len(dates),
                "temperature_2m_mean":[5.0]*len(dates)},
               "daily_units":{"wind_gusts_10m_max":"m/s","temperature_2m_mean":"°C"},
               "utc_offset_seconds":0}
        result=parse_decade(frame,1991,2000)
        self.assertEqual(len(result),len(dates))
        frame["daily_units"]["wind_gusts_10m_max"]="km/h"
        with self.assertRaises(ValueError):
            parse_decade(frame,1991,2000)
    def test_missing_day_never_zero(self):
        dates=date_range(1991,2000)
        frame={"daily":{"time":dates,
              "wind_gusts_10m_max":[12.0]*len(dates),
              "temperature_2m_mean":[5.0]*len(dates)},
              "daily_units":{"wind_gusts_10m_max":"m/s","temperature_2m_mean":"°C"},
              "utc_offset_seconds":0}
        frame["daily"]["wind_gusts_10m_max"][400]=None
        with self.assertRaises(ValueError):
            parse_decade(frame,1991,2000)
    def test_url_hard_codes_era5_gmt_ms_not_default_climate(self):
        sites=[{"lat":35.5,"lon":139.6}]
        q=api_url(sites,"1991-01-01","2000-12-31")
        self.assertIn("models=era5",q)
        self.assertIn("timezone=GMT",q)
        self.assertIn("wind_speed_unit=ms",q)
        self.assertIn("wind_gusts_10m_max",q)
    def test_not_any_unverified_sites_from_fake_archive(self):
        with TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            p.write_bytes(b"not source archive")
            with self.assertRaises(ValueError):
                original_pilot_sites(p,p)

if __name__=="__main__":unittest.main()
