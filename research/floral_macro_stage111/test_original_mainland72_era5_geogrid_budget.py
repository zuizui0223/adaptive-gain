"""Stage111: source-only geography and physically honest public ERA5 source budget."""
import tempfile,zipfile,unittest,math
from pathlib import Path
from shapely.geometry import box
from original_mainland72_era5_geogrid_budget import (
    frozen_original_source_72,independent_geographic_choice,
    cheap_all72_source_grid_demand,exact_new_landsource_weights,
    EXPECTED_NEW_SOURCE_BLOCK_CODES,
    SOURCE_MIN_CELL_KM2_LOWER_BOUND,
    SOURCE_MAX_SITES_PER_PROVIDER_QUERY,
    ALREADY_TRUE_GRID_REGION_CODES)

def synthetic_original():
    train={}
    reg={}
    completed=[("WDC","OLD-A",184),("DEL","OLD-A",4811),("CAB","OLD-B",7560)]
    newly=[("GAM","NEW-C",9581),("KRY","NEW-D",24341),("BGM","NEW-E",33750)]
    for code,block,area in completed+newly:
        train[code]={"TDWG_L3":code,"spatial_block_id":block}
        reg[code]={"TDWG_L3":code,"spatial_block_id":block,
            "estimated_mainland_land_km2":str(area),
            "original_TDWG_invalid_polygon_repaired":"0"}
    # 72 total source regions, 17 source geoblocks. Do not introduce smaller
    # unrepresented geographic groups (we want the fixed selection above).
    for i in range(66):
        block="NEW-"+str(i%12+6)
        code=f"X{i:02d}"
        train[code]={"TDWG_L3":code,"spatial_block_id":block}
        reg[code]={"TDWG_L3":code,"spatial_block_id":block,
            "estimated_mainland_land_km2":str(50000+i*100),
            "original_TDWG_invalid_polygon_repaired":"0"}
    # Need 2 old +3 new + 12 further =17 real source geography blocks.
    return reg,train

class Stage111OriginalSourceGeometrySelection(unittest.TestCase):
    def test_source_first_three_noncontact_new_geoblocks(self):
        reg,train=synthetic_original()
        self.assertEqual(len(train),72)
        self.assertEqual(len({x["spatial_block_id"] for x in train.values()}),17)
        self.assertEqual(tuple(independent_geographic_choice(reg,train)),EXPECTED_NEW_SOURCE_BLOCK_CODES)
    def test_original_already_sourced_blocks_cannot_be_selected_again(self):
        reg,train=synthetic_original()
        self.assertEqual(independent_geographic_choice(reg,train),["GAM","KRY","BGM"])
        self.assertNotIn("DEL",EXPECTED_NEW_SOURCE_BLOCK_CODES)
        self.assertNotIn("CAB",EXPECTED_NEW_SOURCE_BLOCK_CODES)
    def test_no_large_region_biased_geo_intersection_by_smallarea(self):
        reg,train=synthetic_original()
        reg["GAM"]["estimated_mainland_land_km2"]="50001"
        with self.assertRaisesRegex(ValueError,"SELECTED_THREE_BLOCKS_DRIFT"):
            independent_geographic_choice(reg,train)
    def test_geography_selection_never_uses_wind_or_botanical_source(self):
        reg,train=synthetic_original()
        for c in reg:
            reg[c]["source_pattern_positive"]="10000"
            reg[c]["ERA5_gust_1991_2020"]="0"
        self.assertEqual(tuple(independent_geographic_choice(reg,train)),EXPECTED_NEW_SOURCE_BLOCK_CODES)
    def test_max_800km2_cell_area_means_source_lower_not_exact(self):
        self.assertEqual(SOURCE_MIN_CELL_KM2_LOWER_BOUND,800.0)
        self.assertEqual(SOURCE_MAX_SITES_PER_PROVIDER_QUERY,5)
        self.assertEqual(math.ceil(9581.1393/800),12)
        # Lower 12 distinct 0.25 cells * 3 decades with up to5/site =
        # at least 3*ceil(12/5)=9 API calls if that region is isolated.
        self.assertEqual(3*math.ceil(math.ceil(9581.1393/800)/5),9)
    def test_fake_stage94_file_rejected_before_any_climate(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("fake","not source")
            with self.assertRaisesRegex(ValueError,"STAGE106_ORIGINAL_STAGE94_MAINLAND_SOURCE_SHA_MISMATCH"):
                frozen_original_source_72(p,p)
    def test_geometry_cell_lower_bound_physical_not_mean_wind(self):
        self.assertEqual(ALREADY_TRUE_GRID_REGION_CODES,("WDC","DEL","CAB"))
        self.assertTrue(all(x not in ALREADY_TRUE_GRID_REGION_CODES for x in EXPECTED_NEW_SOURCE_BLOCK_CODES))
    def test_raw_nonoriginal_holdout_cannot_be_reassigned(self):
        reg,train=synthetic_original()
        train.pop("CAB")
        with self.assertRaises(KeyError):
            independent_geographic_choice(reg,train)

if __name__=="__main__":unittest.main()
