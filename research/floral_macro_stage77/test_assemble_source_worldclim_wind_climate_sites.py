"""Source-free error checks for Stage77 macro environment matching.

Tests insist that 1970–2000 climate NORMALS and observed insect months are
never confused with actual date-specific wind, scent plume, no-visit absence.
"""
from __future__ import annotations
import importlib.util,unittest,io,zipfile
from collections import Counter
from pathlib import Path
from unittest.mock import patch

p=Path(__file__).with_name("assemble_source_worldclim_wind_climate_sites.py")
spec=importlib.util.spec_from_file_location("stage77_sites",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


class ActualMacroClimateDesignTests(unittest.TestCase):
    def test_original_ISO_months_only_if_explicit(self):
        self.assertEqual(m.original_month("2021-07-06"),(7,"DIRECT_YEAR_FIRST"))
        self.assertEqual(m.original_month("2015-12"),(12,"DIRECT_YEAR_FIRST"))
        self.assertEqual(m.original_month("03/04/2021"),(None,"AMBIGUOUS_DAY_MONTH"))
        self.assertEqual(m.original_month("25/04/2021"),(4,"DAY_FIRST_UNAMBIGUOUS"))
        self.assertEqual(m.original_month("04/25/2021"),(4,"MONTH_FIRST_UNAMBIGUOUS"))
        self.assertEqual(m.original_month("2021"),(None,"UNKNOWN_SOURCE_DATE_FORMAT"))
    def test_original_date_malformed_remains_missing(self):
        self.assertEqual(m.original_month("2021-13-01"),(None,"INVALID_MONTH"))
        self.assertEqual(m.original_month("2021-02-31"),(None,"INVALID_DATE"))
        self.assertEqual(m.original_month("XXX"),(None,"UNKNOWN_SOURCE_DATE_FORMAT"))
    def test_original_source_lat_long_missing_not_zero(self):
        self.assertIsNone(m.safe_coord("",90))
        self.assertIsNone(m.safe_coord("n/a",180))
        self.assertIsNone(m.safe_coord("800",90))
        self.assertEqual(m.safe_coord("47.12345678",90),47.1234568)
    def test_worldclim_monthly_tiff_members_exact(self):
        zio=io.BytesIO()
        with zipfile.ZipFile(zio,"w") as z:
            for mon in range(1,13):
                z.writestr(f"wc2.1_10m_wind_{mon:02d}.tif",b"dummy")
        with zipfile.ZipFile(io.BytesIO(zio.getvalue())) as z:
            out=m.archive_tiff_members(z,"wind")
        self.assertEqual(set(out),set(range(1,13)))
        self.assertEqual(out[7],"wc2.1_10m_wind_07.tif")
    def test_missing_worldclim_layer_never_imputed(self):
        zio=io.BytesIO()
        with zipfile.ZipFile(zio,"w") as z:
            for mon in range(1,12):
                z.writestr(f"wc2.1_10m_wind_{mon:02d}.tif",b"dummy")
        with zipfile.ZipFile(io.BytesIO(zio.getvalue())) as z:
            with self.assertRaisesRegex(ValueError,"12_MONTHS_NOT_AVAILABLE"):
                m.archive_tiff_members(z,"wind")
    def test_worldclim_units_and_outlier_no_silent_averaging(self):
        self.assertIsNone(m.validate_sample("wind",56))
        self.assertIsNone(m.validate_sample("prec",-9))
        self.assertIsNone(m.validate_sample("vapr",float("nan")))
        self.assertAlmostEqual(m.validate_sample("wind",3.2),3.2)
    def test_original_network_month_climatology_not_actual_daily_wind(self):
        k=("S1","NET","2021")
        p=(47.0,5.0)
        vals={p:{v:{m:float(m) for m in range(1,13)} for v in m.CLIMATE_VARS}}
        raw,coverage=m.site_climate_table(
            {k:{p}},{k:{5,6}},{k:Counter(B=10,O=2)},{k:Counter()},vals)
        self.assertEqual(len(raw),1)
        self.assertEqual(coverage["networks_with_5climate_visit_month"],1)
        self.assertAlmostEqual(raw[0]["WorldClim1970_2000_observed_month_mean_wind_speed_m_s"],5.5)
        self.assertAlmostEqual(raw[0]["WorldClim1970_2000_annual_mean_wind_speed_m_s"],6.5)
        self.assertEqual(raw[0]["source_seasonal_month_identified"],1)
        self.assertTrue(raw[0]["source_Bombus_fraction_is_realized_visit_composition_not_receiver_range"])
    def test_original_guild_missing_is_unknown_and_requires_unique_geo(self):
        k=("S1","NET","2021")
        raw,coverage=m.site_climate_table({k:set()},{}, {}, {}, {})
        self.assertEqual(coverage["networks_with_5climate_visit_month"],0)
        self.assertEqual(raw[0]["source_actual_strict_species_rank_Bombus_records"],0)
        self.assertEqual(raw[0]["source_Bombus_fraction_of_recorded_identified_bees"],"")
        self.assertTrue(raw[0]["source_observed_no_Bombus_not_biological_absence"])
        self.assertEqual(raw[0]["full_5variable_annual_climate_admitted"],0)
    def test_historical_normal_never_same_day_VOC_proxy(self):
        self.assertEqual(m.CLIMATE_PERIOD,"1970-2000")
        self.assertEqual(m.SOURCE_NETWORKS,1864)
        self.assertEqual(m.SOURCE_STUDIES,54)
        self.assertIn("wind",m.CLIMATE_VARS)

if __name__=="__main__":
    unittest.main()
