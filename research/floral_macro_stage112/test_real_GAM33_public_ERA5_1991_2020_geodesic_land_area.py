"""Stage112: original Stage111 GAM 33 land cells, true full 30-year gust units."""
import tempfile,zipfile,unittest
from pathlib import Path
from real_GAM33_public_ERA5_1991_2020_geodesic_land_area import (
   original_source_GAM_cells,true_source_region_GAM_area_mean,
   SOURCE_CODE,FROZEN_SOURCE_CELLCOUNT,SOURCE_STAGE111_ORIGINAL_SHA,GROUP_SIZE,
   source_verified_prior30_GAM_full_decades,SOURCE_PRIOR30_COMPLETED_ARTIFACT_SHA)
from original_public_ERA5_model_34cells_DEL_CAB_landarea import normalize_source_era5_response
from original_geogrid_public_ERA5_1991_2020_WDC_area_gust import accepted_grid_coordinates

def fake_source(exceed=.1,missing=False):
    sites=[]
    for i in range(33):
        row={"source_mainland_cell_land_area_km2":1+i,
             "original_1991_2020_cell_model_ERA5_climatology":{
                 "source_ERA5_observed_30yr_days":10958,
                 "source_primary_fraction_days_daily_gust_strict_above_15_ms":
                     (None if i==32 and missing else exceed+i/500),
                 "source_fraction_gust_greater_than_10_ms":.5,
                 "source_fraction_gust_greater_than_20_ms":0.01}}
        sites.append(row)
    return sites,{"source_actual_polygon_mainland_land_area_km2":sum(
        r["source_mainland_cell_land_area_km2"] for r in sites)}

class GAMOriginalLandGrid(unittest.TestCase):
    def test_preselected_first_new_source_block_is_GAM_not_outcome(self):
        self.assertEqual(SOURCE_CODE,"GAM")
        self.assertEqual(FROZEN_SOURCE_CELLCOUNT,33)
        self.assertEqual(GROUP_SIZE,5)
        self.assertEqual(len(SOURCE_STAGE111_ORIGINAL_SHA),64)
    def test_geodesic_weighted_not_equal_cell_mean(self):
        sites,source=fake_source()
        a=true_source_region_GAM_area_mean(sites,source)
        x=[r["original_1991_2020_cell_model_ERA5_climatology"][
            "source_primary_fraction_days_daily_gust_strict_above_15_ms"] for r in sites]
        w=[r["source_mainland_cell_land_area_km2"] for r in sites]
        expected=sum(p*q for p,q in zip(x,w))/sum(w)
        self.assertAlmostEqual(a["source_1991_2020_daily_10m_gust_gt15_source_geodesic_area_weighted"],expected)
        self.assertNotAlmostEqual(expected,sum(x)/len(x))
        self.assertTrue(a["source_public_ERA5model_daily_NOT_original_CDS_hourly_10fg"])
        self.assertGreater(a["source_original_025_cell_GUST_gt15_area_weighted_sd"],0)
    def test_missing_3pct_land_area_accepted_but_not_zero_imputed(self):
        sites,source=fake_source(missing=True)
        # Last cell weighs 33/561=5.88% and fails >95 coverage.
        with self.assertRaisesRegex(ValueError,"BELOW95"):
            true_source_region_GAM_area_mean(sites,source)
    def test_all_warm_climate_cells_zero_strong_wind_is_a_valid_ERA5_model_result(self):
        sites,source=fake_source(exceed=0)
        for r in sites:r["original_1991_2020_cell_model_ERA5_climatology"][
            "source_primary_fraction_days_daily_gust_strict_above_15_ms"]=0.
        ans=true_source_region_GAM_area_mean(sites,source)
        self.assertEqual(ans["source_1991_2020_daily_10m_gust_gt15_source_geodesic_area_weighted"],0)
    def test_32_cells_not_source_33_rejected(self):
        sites,source=fake_source()
        with self.assertRaisesRegex(ValueError,"NOT_ALL_33"):
            true_source_region_GAM_area_mean(sites[:-1],source)
    def test_original_first30_completed_source_replay_must_be_SHA_pinned(self):
        self.assertEqual(len(SOURCE_PRIOR30_COMPLETED_ARTIFACT_SHA),64)
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"untrusted.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("fake","not the original 30")
            with self.assertRaisesRegex(ValueError,"PRIOR30_SOURCE_ARTIFACT_SHA_DRIFT"):
                source_verified_prior30_GAM_full_decades(p,[])
    def test_fake_original_Stage111_geo_zip_never_accepted(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("fake","untrusted")
            with self.assertRaisesRegex(ValueError,"GEOGRAPHY_SHA_DRIFT"):
                original_source_GAM_cells(p)
    def test_real_source_single_site_and_multi_site_json_shapes(self):
        src={"latitude":13.5,"longitude":-16.5,"daily":{"time":[]}}
        self.assertEqual(normalize_source_era5_response(src,1),[src])
        self.assertEqual(normalize_source_era5_response([src,src],2),[src,src])
        with self.assertRaises(ValueError):normalize_source_era5_response(src,5)
    def test_different_model_grid_returned_must_fail(self):
        original={"lat":13.50,"lon":-16.50}
        with self.assertRaisesRegex(ValueError,"DIFFERENT_ERA5_MODEL_CELL"):
            accepted_grid_coordinates(original,{"latitude":13.75,"longitude":-16.50})
    def test_original_30year_10958_days_and_3_full_decades(self):
        from original_ERA5_1991_2020_gust_five_mainland_pilot import YEARS,date_range
        self.assertEqual(YEARS,((1991,2000),(2001,2010),(2011,2020)))
        self.assertEqual(len(date_range(1991,2020)),10958)
    def test_open_meteo_ERA5_model_not_mean_wind_not_CDS_hourly(self):
        from original_ERA5_1991_2020_gust_five_mainland_pilot import api_url
        url=api_url([{"lat":13.5,"lon":-16.5}],"1991-01-01","2000-12-31")
        for expected in ("models=era5","elevation=nan","cell_selection=nearest",
                         "timezone=GMT","wind_gusts_10m_max","temperature_2m_mean"):
            self.assertIn(expected,url)
        self.assertNotIn("api_key=",url)

if __name__=="__main__": unittest.main()
