"""Stage109: public ERA5 model, original 1991–2020 WDC area weights."""
import json,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
import original_geogrid_public_ERA5_1991_2020_WDC_area_gust as m

def area_cells():
    return [
       {"TDWG_L3":"WDC","lat":38.75,"lon":-77.0,
        "source_grid_land_area_km2":41.6868537},
       {"TDWG_L3":"WDC","lat":39.0,"lon":-77.0,
        "source_grid_land_area_km2":142.95504263}
    ]
def original_site_climatology(value):
    return {"source_primary_fraction_days_daily_gust_strict_above_15_ms":value,
            "source_fraction_gust_greater_than_10_ms":value,
            "source_fraction_gust_greater_than_20_ms":0.}

class SourceOnly(unittest.TestCase):
    def test_original_land_geodesic_area_weighted_not_unweighted(self):
        s=area_cells()
        v=[{**s[0],"source_1991_2020_climatology":original_site_climatology(1.)},
           {**s[1],"source_1991_2020_climatology":original_site_climatology(0.)}]
        out=m.actual_source_area_averaged_climatology(v)
        self.assertAlmostEqual(out["source_1991_2020_original_ERA5_model_daily_gust15_frequency_area_weighted"],
            s[0]["source_grid_land_area_km2"]/sum(r["source_grid_land_area_km2"] for r in s))
        self.assertNotAlmostEqual(out["source_1991_2020_original_ERA5_model_daily_gust15_frequency_area_weighted"],.5)
        self.assertTrue(out["source_NO_original_CDS_hourly_10fg_byte_verification"])
    def test_neither_eligible_month_not_a_zero_gust(self):
        s=area_cells()
        v=[{**s[0],"source_1991_2020_climatology":original_site_climatology(None)},
           {**s[1],"source_1991_2020_climatology":original_site_climatology(None)}]
        with self.assertRaises(ValueError):
            m.actual_source_area_averaged_climatology(v)
    def test_95pct_source_land_with_valid_warm_months_required(self):
        s=area_cells()
        v=[{**s[0],"source_1991_2020_climatology":original_site_climatology(1.)},
           {**s[1],"source_1991_2020_climatology":original_site_climatology(None)}]
        with self.assertRaisesRegex(ValueError,"LAND_COVERAGE"):
            m.actual_source_area_averaged_climatology(v)
    def test_physical_era5_exact_grid_cell_coordinates_not_substituted(self):
        src=area_cells()[0]
        a=m.accepted_grid_coordinates(src,{"latitude":38.75,"longitude":-77.0})
        self.assertEqual(a["coordinate_offset_deg_lat"],0)
        with self.assertRaises(ValueError):
            m.accepted_grid_coordinates(src,{"latitude":38.90,"longitude":-77.0})
        with self.assertRaises(ValueError):
            m.accepted_grid_coordinates(src,{"latitude":38.75,"longitude":-76.7})
    def test_longitudes_use_periodic_equivalence_not_artificial_shift(self):
        v=m.accepted_grid_coordinates({"lat":38.75,"lon":-77.0},
                    {"latitude":38.75,"longitude":283.0})
        self.assertAlmostEqual(v["coordinate_offset_deg_lon"],0)
    def test_definitely_requires_explicit_era5_historical_daily_config(self):
        url=m.api_url(area_cells(),"1991-01-01","2000-12-31")
        self.assertIn("models=era5",url)
        self.assertIn("wind_speed_unit=ms",url)
        self.assertIn("timezone=GMT",url)
        self.assertIn("cell_selection=nearest",url)
        self.assertIn("elevation=nan",url)
        self.assertIn("wind_gusts_10m_max",url)
        self.assertNotIn("apikey=",url)
    def test_original_30yr_degenerate_weather_does_not_use_single_year(self):
        import sys
        from original_ERA5_1991_2020_gust_five_mainland_pilot import climatology
        from original_ERA5_1991_2020_gust_five_mainland_pilot import date_range
        days=date_range(1991,2020)
        sample=[(d,16. if int(d[5:7]) in (6,7) else 0.,
                 10. if int(d[5:7]) in (6,7) else 0.) for d in days]
        c=climatology(sample)
        self.assertEqual(c["source_eligible_climatological_months_T2m_strict_above_5C"],[6,7])
        self.assertAlmostEqual(c["source_primary_fraction_days_daily_gust_strict_above_15_ms"],1)
        self.assertEqual(c["source_ERA5_observed_30yr_days"],10958)
    def test_15_0_exact_daily_gust_fails_strict_gt15(self):
        from original_ERA5_1991_2020_gust_five_mainland_pilot import climatology,date_range
        days=date_range(1991,2020)
        sample=[(d,15.,10.) for d in days]
        c=climatology(sample)
        self.assertEqual(c["source_primary_fraction_days_daily_gust_strict_above_15_ms"],0)
    def test_fake_stage106_geography_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:
                z.writestr(m.GEO_MEMBER,"TDWG_L3\nWDC")
            with self.assertRaisesRegex(ValueError,"GEOMETRY_SOURCE_SHA_CHANGED"):
                m.original_geodesic_source_land_cells(p)
    def test_wrong_cell_count_never_area_extrapolation(self):
        v=[{**area_cells()[0],"source_1991_2020_climatology":original_site_climatology(.6)}]
        with self.assertRaisesRegex(ValueError,"NOT_WDC_TWO"):
            m.actual_source_area_averaged_climatology(v)
    def test_original_true_30_year_period_not_one_weather_year(self):
        self.assertEqual(m.YEARS,((1991,2000),(2001,2010),(2011,2020)))
        self.assertEqual(len(m.GUST_THRESHOLDS),3)

if __name__=="__main__":unittest.main()
