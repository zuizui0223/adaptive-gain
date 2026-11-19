"""Stage94 strict island/nonmainland geometry classification and source guards."""
import tempfile,unittest,zipfile
from pathlib import Path
from shapely.geometry import box,Point
from shapely.strtree import STRtree
from original_tdwg_naturalearth_strict_mainland import (
    area_km2,geometry_class,read_original_native_367,
    classify_original_regions,COAST_DISCREPANCY_TOL_KM2,
    NATURAL_EARTH_LAND_ZIP_SHA256,
    ANCHORS
)

class MainlandGeometryContract(unittest.TestCase):
    def test_known_greenland_omitted_from_continent_anchors(self):
        self.assertNotIn("greenland",ANCHORS)
        self.assertIn("australia",ANCHORS)
        self.assertIn("antarctica",ANCHORS)
        self.assertEqual(len(ANCHORS),6)
    def test_area_geodesic_positive(self):
        x=area_km2(box(-1,-1,1,1))
        self.assertTrue(45000<x<50000)
        self.assertEqual(area_km2(box(0,0,0,0)),0.0)
    def test_clean_mainland(self):
        self.assertEqual(geometry_class(2000,0),"mainland")
        self.assertEqual(geometry_class(20,0.09),"mainland")
    def test_mixed_continent_and_island_excluded(self):
        self.assertEqual(geometry_class(1000,200),"mixed")
        self.assertEqual(geometry_class(1000,0.2),"mixed")
        self.assertEqual(geometry_class(0.2,1000),"mixed")
    def test_real_island_excluded(self):
        self.assertEqual(geometry_class(0,2500),"island")
    def test_too_small_region_source_cannot_be_misread(self):
        self.assertEqual(geometry_class(0,0.02),"mixed")
        self.assertEqual(geometry_class(3,0),"mixed")
    def test_negative_area_rejected(self):
        with self.assertRaises(ValueError):
            geometry_class(-1,1)
    def test_overly_relaxed_island_tolerance_not_allowed(self):
        self.assertLessEqual(COAST_DISCREPANCY_TOL_KM2,0.1)
    def test_source_artifact_without_checksum_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:
                z.writestr("fake.csv","not original")
            with self.assertRaises(ValueError):
                read_original_native_367(p)
    def test_mainland_area_is_not_island_size_threshold(self):
        # Greenland is very large, but its size is not a criterion;
        # only connection to a declared continental anchor matters.
        self.assertEqual(geometry_class(0,2200000),"island")

if __name__=="__main__":unittest.main()
