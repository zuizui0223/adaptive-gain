"""Source-free Stage70 tests. Exercises strict state logic and geometric ambiguity."""
from __future__ import annotations
import importlib.util
import unittest
from pathlib import Path
from collections import defaultdict
from shapely.geometry import box

p=Path(__file__).with_name("official_wcvp_native_tdwg_original_field_network.py")
spec=importlib.util.spec_from_file_location("stage70_wcvp_tdwg",p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class Stage70NativeSiteGates(unittest.TestCase):
    def test_wcvp_flags_blank_never_zero(self):
        self.assertEqual(m.string_flag("0"),0)
        self.assertEqual(m.string_flag("1"),1)
        self.assertEqual(m.string_flag(""),None)
        self.assertEqual(m.string_flag("NA"),None)
        self.assertEqual(m.string_flag("2"),None)

    def test_missing_region_does_not_equal_introduction(self):
        acc={"species a":{"123"},"species b":{"456"}}
        st=defaultdict(lambda:defaultdict(set))
        st["species a"]["FRA"]={"native"}
        st["species b"]["FRA"]={"introduced"}
        st["species a"]["GER"]={"native","introduced"}
        self.assertEqual(m.classify_origin("species a","FRA",acc,st),
                         "WCVP_NATIVE_L3_COMPATIBLE")
        self.assertEqual(m.classify_origin("species b","FRA",acc,st),
                         "WCVP_INTRODUCED_L3_RECORDED")
        self.assertEqual(m.classify_origin("species a","GER",acc,st),
                         "WCVP_L3_CONFLICTING_ORIGINS")
        self.assertEqual(m.classify_origin("species a","ESP",acc,st),
                         "WCVP_L3_NOT_RECORDED_UNKNOWN")
        self.assertEqual(m.classify_origin("species b","",acc,st),
                         "SITE_TDWG_L3_UNRESOLVED")
        self.assertEqual(m.classify_origin("species c","FRA",acc,st),
                         "WCVP_SPECIES_NOT_EXACT_ACCEPTED")

    def test_duplicate_wcvp_exact_accepted_taxonomic_concepts_unknown(self):
        acc={"species a":{"123","234"}}
        self.assertEqual(m.classify_origin("species a","FRA",acc,{}),
                         "WCVP_SPECIES_NOT_EXACT_ACCEPTED")

    def test_polygon_contains_and_near_border_conservative(self):
        geom=[("FR",box(0,0,10,10)),("DE",box(10,0,20,10))]
        code,status,edge=m.locate_l3({(5,5)},geom)
        self.assertEqual(code,"FR")
        self.assertEqual(status,"WITHIN_TDWG_L3_POLYGON")
        self.assertFalse(edge)
        _,near,edge=m.locate_l3({(5,9.995)},geom)
        self.assertEqual(near,"NEAR_BOUNDARY_SENSITIVITY")
        self.assertTrue(edge)
        _,amb,_=m.locate_l3({(5,10)},geom)
        self.assertEqual(amb,"MULTIPLE_OR_ZERO_TDWG_POLYGON_CONTAINS")
        _,status,_=m.locate_l3({(5,5),(6,6)},geom)
        self.assertEqual(status,"NO_SINGLE_UNAMBIGUOUS_SOURCE_COORDINATE")
        _,status,_=m.locate_l3(set(),geom)
        self.assertEqual(status,"NO_SINGLE_UNAMBIGUOUS_SOURCE_COORDINATE")

    def test_native_not_source_same_population(self):
        self.assertEqual(m.ORIGINAL_STRICT_SOURCE_NETWORKS,156)
        self.assertEqual(m.VISITS_PER_TAXON_MIN,3)
        self.assertEqual(m.UV_RANGE_PERCENT_POINTS_MIN,1.0)
        self.assertEqual(m.EDGE_ANGLE_DEG,0.02)

    def test_cannot_confuse_blob_and_zip_digest(self):
        self.assertNotEqual(m.original_git_blob_sha(b"abc"),
                            __import__("hashlib").sha256(b"abc").hexdigest())
        self.assertEqual(len(m.WCVP_ZIP_EXPECTED_SHA256),64)
        self.assertEqual(len(m.TDWG_GEOJSON_EXPECTED_BLOB_SHA1),40)


if __name__=="__main__":
    unittest.main()
