"""Source-free topology sensitivity tests, never enable primary rescue."""
import importlib.util
import unittest
from pathlib import Path
from shapely.geometry import box
p=Path(__file__).with_name("historic_tdwg_invalid_geometry_diagnostic.py")
spec=importlib.util.spec_from_file_location("st70b_diag",p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class OriginalTDWGGeometrySensitivityTests(unittest.TestCase):
    def test_repaired_geometry_never_implies_primary(self):
        self.assertEqual(m.candidate_polygon_codes({(5,5)},[
          ("A",box(0,0,10,10))]),("ONE_POLYGON_CONTAINS",{"A"}))
        self.assertEqual(m.candidate_polygon_codes({(5,5)},[
          ("A",box(0,0,10,10)),("B",box(0,0,10,10))]),
          ("MULTIPLE_POLYGON_CODES_CONTAIN",{"A","B"}))
        self.assertEqual(m.candidate_polygon_codes(set(),[
          ("A",box(0,0,10,10))])[0],"NO_UNIQUE_SOURCE_COORDINATE")

    def test_no_false_geo_name_match(self):
        self.assertEqual(m.candidate_polygon_codes({(50,140)},[
            ("A",box(0,0,10,10))]),("ZERO_POLYGONS_CONTAIN",set()))

    def test_primary_and_sensitivity_have_separate_program_names(self):
        self.assertEqual(m.st.ORIGINAL_STRICT_SOURCE_NETWORKS,156)
        self.assertEqual(m.st.EDGE_ANGLE_DEG,0.02)


if __name__=="__main__":
    unittest.main()
