"""Stage87 C source-free real-map semantics: not an invented weather effect."""
import unittest
from shapely.geometry import Polygon,MultiPolygon
from aggregate_global_tdwg3_worldclim_wind import (
    original_blob_sha,sample_source_region_points,validate_climate,combine
)
class WorldClimSourceGuards(unittest.TestCase):
    def test_original_Git_blob_header(self):
        raw=b"abc"
        self.assertEqual(original_blob_sha(raw),
          "f2ba8f84ab5c1bce84a7b441cb1959cfc7093b7f")
    def test_valid_climatological_units(self):
        self.assertTrue(validate_climate("wind",8.5))
        self.assertFalse(validate_climate("wind",-1))
        self.assertFalse(validate_climate("prec",-2))
        self.assertFalse(validate_climate("wind",float("nan")))
    def test_regions_use_polygon_points_not_outer_bbox(self):
        poly=MultiPolygon([Polygon([(0,0),(1,0),(1,1),(0,1)]),
                           Polygon([(4,4),(5,4),(5,5),(4,5)])])
        p,s=sample_source_region_points({"ABC":poly})
        self.assertTrue(0<len(p["ABC"])<=48)
        for lon,lat in p["ABC"]:
            self.assertTrue(poly.contains(__import__("shapely").geometry.Point(lon,lat)) or
                            poly.touches(__import__("shapely").geometry.Point(lon,lat)))
    def test_sparse_weather_is_not_imputed(self):
        original={"ABC":{"TDWG_L3":"ABC","n_source_single_explicit_hue":10}}
        climate={"ABC":{"worldclim_baseline_wind_m_s":3.1}}
        with self.assertRaises(KeyError):combine(original,climate,{},{})

if __name__=="__main__":unittest.main()
