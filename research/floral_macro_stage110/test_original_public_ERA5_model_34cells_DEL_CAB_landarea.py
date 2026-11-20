"""Stage110 genuine model multi-ERA5-grid 1991-2020 area audit guards."""
import tempfile,zipfile,unittest
from pathlib import Path
from original_public_ERA5_model_34cells_DEL_CAB_landarea import (
    frozen_original_mainland_cell_sets,true_geodesic_region_area_average,
    normalize_source_era5_response,original_verified_partial_DEL15,
    SOURCE_REGIONS,EXPECTED_COUNTS,REQUEST_GROUP_MAX)
from original_geogrid_public_ERA5_1991_2020_WDC_area_gust import accepted_grid_coordinates

def synthetic_area_region(code,n=None,missing_index=None):
    n=n or EXPECTED_COUNTS[code]
    cells=[]
    for i in range(n):
        c={"source_grid_mainland_intersection_km2":1.0+i,
           "original_30y_cell_ERA5_model_daily":{
             "source_ERA5_observed_30yr_days":10958,
             "source_primary_fraction_days_daily_gust_strict_above_15_ms":i/(n+1),
             "source_fraction_gust_greater_than_10_ms":.5,
             "source_fraction_gust_greater_than_20_ms":.01}}
        if i==missing_index:c["original_30y_cell_ERA5_model_daily"]["source_primary_fraction_days_daily_gust_strict_above_15_ms"]=None
        cells.append(c)
    return cells

class Stage110SourceBoundaries(unittest.TestCase):
    def test_actual_public_ERA5_single_site_dict_vs_multisite_list(self):
        exemplar={"latitude":38.5,"longitude":-75.75,"daily":{"time":["1991-01-01"]}}
        self.assertEqual(normalize_source_era5_response(exemplar,1),[exemplar])
        self.assertEqual(normalize_source_era5_response([exemplar,exemplar],2),[exemplar,exemplar])
        with self.assertRaisesRegex(ValueError,"SOURCE_RESPONSE_SHAPE"):
            normalize_source_era5_response(exemplar,3)
        with self.assertRaisesRegex(ValueError,"SOURCE_RESPONSE_SHAPE"):
            normalize_source_era5_response({"reason":"Provider error"},1)
    def test_previous_original_15_source_zip_must_match_immutable_sha(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake_partial.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("fake","untrusted source")
            with self.assertRaisesRegex(ValueError,"SOURCE_ARCHIVE_SHA_MISMATCH"):
                original_verified_partial_DEL15(p,{"DEL":[]})
    def test_true_original_source_regional_geographies(self):
        self.assertEqual(SOURCE_REGIONS,("DEL","CAB"))
        self.assertEqual(EXPECTED_COUNTS,{"DEL":16,"CAB":18})
        self.assertEqual(REQUEST_GROUP_MAX,5)
    def test_area_mean_16_cells_not_point_or_equal_cell_mean(self):
        cells=synthetic_area_region("DEL")
        total=sum(v["source_grid_mainland_intersection_km2"] for v in cells)
        out=true_geodesic_region_area_average(cells,"DEL",total)
        expected=sum(v["source_grid_mainland_intersection_km2"]*
                v["original_30y_cell_ERA5_model_daily"]["source_primary_fraction_days_daily_gust_strict_above_15_ms"] for v in cells)/total
        self.assertAlmostEqual(out["source_1991_2020_ERA5model_daily_gust_gt15_area_weighted_fraction"],expected)
        self.assertNotAlmostEqual(expected,sum(v["original_30y_cell_ERA5_model_daily"]["source_primary_fraction_days_daily_gust_strict_above_15_ms"] for v in cells)/16)
        self.assertEqual(out["source_original_025_model_land_cells"],16)
        self.assertGreater(out["source_within_region_land_area_weighted_cell_sd_gust_gt15_fraction"],0)
    def test_18_Cabinda_grid_count_and_physical_variation(self):
        cells=synthetic_area_region("CAB")
        total=sum(v["source_grid_mainland_intersection_km2"] for v in cells)
        out=true_geodesic_region_area_average(cells,"CAB",total)
        self.assertEqual(out["source_original_025_model_land_cells"],18)
        self.assertTrue(0<out["source_original_effective_land_grid_cells"]<18)
        self.assertTrue(out["source_external_ERA5_model_daily_not_original_CDS_hourly_10fg"])
    def test_missing_more_than_5pct_land_cells_not_invented(self):
        cells=synthetic_area_region("DEL",missing_index=15)
        total=sum(v["source_grid_mainland_intersection_km2"] for v in cells)
        with self.assertRaisesRegex(ValueError,"LAND_COVERAGE"):
            true_geodesic_region_area_average(cells,"DEL",total)
    def test_source_area_integrity_required(self):
        cells=synthetic_area_region("CAB")
        with self.assertRaisesRegex(ValueError,"AREA_NOT_CONSERVED"):
            true_geodesic_region_area_average(cells,"CAB",3.0)
    def test_missing_one_cell_fails_before_area_extrapolation(self):
        cells=synthetic_area_region("DEL")[:-1]
        with self.assertRaisesRegex(ValueError,"COMPLETE_GRID"):
            true_geodesic_region_area_average(cells,"DEL",100)
    def test_original_cell_coords_must_match_returned_ERA5(self):
        original={"lat":38.5,"lon":-75.75}
        self.assertAlmostEqual(accepted_grid_coordinates(original,
          {"latitude":38.5,"longitude":-75.75})["coordinate_offset_deg_lat"],0)
        with self.assertRaisesRegex(ValueError,"DIFFERENT_ERA5_MODEL_CELL"):
            accepted_grid_coordinates(original,{"latitude":38.75,"longitude":-75.75})
    def test_fake_geo_zip_never_pass_source_sha(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"original_like_fake.zip"
            with zipfile.ZipFile(p,"w") as z:
                z.writestr("stage106_original_three_mainland_regions_ERA5_025deg_cell_landarea_weights.csv","fake")
            with self.assertRaisesRegex(ValueError,"TRUE_ORIGINAL_SOURCE_LANDAREA_SHA"):
                frozen_original_mainland_cell_sets(p)
    def test_30years_real_calendar_inherited_no_invalid_annual_proxy(self):
        from original_ERA5_1991_2020_gust_five_mainland_pilot import YEARS,date_range
        self.assertEqual(YEARS,((1991,2000),(2001,2010),(2011,2020)))
        self.assertEqual(len(date_range(1991,2020)),10958)
    def test_maximum_gust_vs_mean_speed_precise_source_api(self):
        from original_ERA5_1991_2020_gust_five_mainland_pilot import api_url
        url=api_url([{"lat":38.5,"lon":-75.75}],"1991-01-01","2000-12-31")
        self.assertIn("models=era5",url)
        self.assertIn("wind_gusts_10m_max",url)
        self.assertIn("wind_speed_unit=ms",url)
        self.assertNotIn("apikey",url)

if __name__=="__main__":unittest.main()
