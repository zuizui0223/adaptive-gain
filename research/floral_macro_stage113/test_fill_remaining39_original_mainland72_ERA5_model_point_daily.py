"""Stage113 source-free guards for genuine 72 noncontact mainland ERA5-model point climate."""
import tempfile,unittest,zipfile
from pathlib import Path
from fill_remaining39_original_mainland72_ERA5_model_point_daily import (
   exact_geo_and_source_first50,returned_source_model_point,
   SHA_MAINLAND72,SHA_SOURCE_FIRST25,SHA_SOURCE_NEXT25,
   GEO_BLOCKS,ORIGINAL_MISSING_TRAIN_POINTS,ORIGINAL_PRIOR_TRAIN_POINTS,
   ORIGINAL_TOTAL_TRAIN_POINTS,BATCH_SITES)
from original_public_ERA5_model_34cells_DEL_CAB_landarea import normalize_source_era5_response

class SourceOnlyFills(unittest.TestCase):
    def test_frozen_stage98B_original_72_37_and_17_blocks(self):
        self.assertEqual(ORIGINAL_MISSING_TRAIN_POINTS,39)
        self.assertEqual(ORIGINAL_PRIOR_TRAIN_POINTS,33)
        self.assertEqual(ORIGINAL_TOTAL_TRAIN_POINTS,72)
        self.assertEqual(GEO_BLOCKS,17)
        self.assertEqual(ORIGINAL_PRIOR_TRAIN_POINTS+ORIGINAL_MISSING_TRAIN_POINTS,72)
    def test_39_source_points_8_actual_public_batches(self):
        sizes=[len(range(start,min(start+BATCH_SITES,39)))
               for start in range(0,39,BATCH_SITES)]
        self.assertEqual(sizes,[5,5,5,5,5,5,5,4])
        self.assertEqual(len(sizes)*3,24)
    def test_source_point_near_TDWG_and_one_degree_not_expanded(self):
        point={"lat":45.2,"lon":19.0}
        self.assertEqual(returned_source_model_point(point,{"latitude":45.0,"longitude":19.2}),[45.,19.2])
        with self.assertRaisesRegex(ValueError,"TOO_FAR"):
            returned_source_model_point(point,{"latitude":46.0,"longitude":19.0})
        with self.assertRaisesRegex(ValueError,"TOO_FAR"):
            returned_source_model_point(point,{"latitude":45.2,"longitude":19.9})
    def test_source_point_dateline_longitude_wraps(self):
        site={"lat":-10,"lon":-179.9}
        self.assertEqual(returned_source_model_point(site,{"latitude":-10,"longitude":180.0}),[-10.,180.])
    def test_missing_public_coordinate_is_invalid(self):
        with self.assertRaisesRegex(ValueError,"COORD_NOT_REPORTED"):
            returned_source_model_point({"lat":44,"lon":20},{"daily":{}})
    def test_nonfinite_original_source_coordinate_rejected(self):
        with self.assertRaisesRegex(ValueError,"COORD_NOT_FINITE"):
            returned_source_model_point({"lat":44,"lon":20},{"latitude":float("nan"),"longitude":20})
    def test_shape_single_site_object_or_valid_multisite_array_only(self):
        a={"latitude":35.0,"longitude":22.0,"daily":{"time":[]}}
        self.assertEqual(normalize_source_era5_response(a,1),[a])
        self.assertEqual(normalize_source_era5_response([a,a],2),[a,a])
        with self.assertRaises(ValueError):normalize_source_era5_response(a,5)
    def test_no_consent_to_any_unauthenticated_false_Stage94_or_TDWG(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            g=Path(td)/"false.geojson"
            g.write_text('{"type":"FeatureCollection","features":[]}')
            with zipfile.ZipFile(p,"w") as z:z.writestr("fake","incorrect source")
            with self.assertRaises(ValueError):
                exact_geo_and_source_first50(p,g,p,p,p)
    def test_three_source_ZIP_hashes_are_pinned_and_distinct(self):
        self.assertEqual(len({SHA_MAINLAND72,SHA_SOURCE_FIRST25,SHA_SOURCE_NEXT25}),3)
        self.assertTrue(all(len(x)==64 for x in (SHA_MAINLAND72,SHA_SOURCE_FIRST25,SHA_SOURCE_NEXT25)))
    def test_30_years_daily_temperature_and_gust_not_annual_proxy(self):
        from original_ERA5_1991_2020_gust_five_mainland_pilot import YEARS,date_range
        self.assertEqual(YEARS,((1991,2000),(2001,2010),(2011,2020)))
        self.assertEqual(len(date_range(1991,2020)),10958)
    def test_source_api_model_is_ERA5_not_downscaled(self):
        from original_ERA5_1991_2020_gust_five_mainland_pilot import api_url
        url=api_url([{"lat":45.2,"lon":19.}],"1991-01-01","2000-12-31")
        for x in ("models=era5","elevation=nan","wind_speed_unit=ms",
                  "wind_gusts_10m_max","temperature_2m_mean","cell_selection=nearest"):
            self.assertIn(x,url)
        self.assertNotIn("CDSAPI_KEY",url)

    def test_resume_wrong_bytes_fail_before_use(self):
        from fill_remaining39_original_mainland72_ERA5_model_point_daily import read_resume_batches
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"not_original.zip"
            p.write_bytes(b"unverified")
            with self.assertRaisesRegex(ValueError,"RESUME_ORIGINAL_ARTIFACT_SHA_DRIFT"):
                read_resume_batches(p,[],{})

    def test_resume_wrong_members_fail_even_with_mocked_hash(self):
        from unittest.mock import patch
        import fill_remaining39_original_mainland72_ERA5_model_point_daily as stage
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("wrong.json","{}")
            with patch.object(stage,"sha256",return_value=stage.SHA_RESUME_30):
                with self.assertRaisesRegex(ValueError,"RESUME_EXPECTED_EXACT_SIX_BATCHES"):
                    stage.read_resume_batches(p,[],{})

if __name__=="__main__":unittest.main()
