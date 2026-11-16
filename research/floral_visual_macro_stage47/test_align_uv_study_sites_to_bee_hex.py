"""Source-free geographic exact-polygon tests; zero invented animal findings."""
import unittest

from pyproj import Transformer
from shapely.geometry import Polygon
from shapely.strtree import STRtree

from align_uv_study_sites_to_bee_hex import (
    STUDY_SITES,matching_original_hex,assign_study_sites,summarize,
)

def fixture():
    # synthetic squares, geographic coordinates, NOT authentic bee cells
    polys=[
        Polygon([(0,0),(2,0),(2,2),(0,2)]),
        Polygon([(2,0),(4,0),(4,2),(2,2)]),
    ]
    tree=STRtree(polys)
    names=["HEXexample1","HEXexample2"]
    transform=Transformer.from_crs("EPSG:4326","EPSG:4326",always_xy=True)
    byid={
       "HEXexample1":{
          "eligibility":"AUTHOR_TREE_AND_PA_CELL_CUTOFF",
          "n_source_tree_and_pa_cutoff_Bombus_taxa":0,
          "n_source_tree_and_pa_cutoff_all_bee_taxa":12,
       },
       "HEXexample2":{
          "eligibility":"OUTSIDE_AUTHOR_FILTERED_MODEL_NO_ABSENCE_INFERENCE",
          "n_source_tree_and_pa_cutoff_Bombus_taxa":None,
          "n_source_tree_and_pa_cutoff_all_bee_taxa":None,
       }
    }
    return names,tree,transform,byid


class OriginalSiteMappingContracts(unittest.TestCase):
    def test_original_site_definitions_have_two_exact_and_one_range(self):
        self.assertEqual(len(STUDY_SITES),3)
        self.assertEqual(sum(x["kind"]=="published_single_coordinate"
                             for x in STUDY_SITES),2)
        self.assertEqual(sum(x["kind"]=="published_coordinate_rectangle_not_point"
                             for x in STUDY_SITES),1)
        self.assertEqual(sum(len(x["coordinates_lonlat"]) for x in STUDY_SITES),7)
        self.assertTrue(all(x["country"]=="Brazil" for x in STUDY_SITES))

    def test_exact_polygon_assignment_not_nearest_centroid(self):
        names,tree,tr,_=fixture()
        self.assertEqual(matching_original_hex(1,1,names,tree,tr),["HEXexample1"])
        self.assertEqual(matching_original_hex(3,1,names,tree,tr),["HEXexample2"])
        self.assertEqual(matching_original_hex(10,10,names,tree,tr),[])
        # On shared polygon edge report TWO candidates, never guess
        self.assertEqual(matching_original_hex(2,1,names,tree,tr),
                         ["HEXexample1","HEXexample2"])

    def test_variable_source_sampling_rectangle_crosses_cells(self):
        names,tree,tr,values=fixture()
        sites=[{
            "name":"constructed rectangle","kind":"published_coordinate_rectangle_not_point",
            "coordinates_lonlat":[(1,1),(3,1),(1,1.5),(3,1.5),(2,1.25)]
        }]
        out=assign_study_sites(sites,names,tree,tr,values)
        self.assertEqual(out[0]["hex_assignment_status"],
                         "NO_GO_POINT_UNASSIGNED_OR_ON_POLYGON_BOUNDARY")
        self.assertEqual(len(out[0]["candidate_author_model_hex_cells"]),2)
        self.assertEqual(out[0]["candidate_author_model_hex_cells"][1]
                         ["n_modelled_source_Bombus_taxa_or_null"],None)

    def test_model_zero_distinct_from_unknown(self):
        names,tree,tr,values=fixture()
        sites=[{"name":"mock zero","kind":"published_single_coordinate",
                "coordinates_lonlat":[(1,1)]},
               {"name":"mock unknown","kind":"published_single_coordinate",
                "coordinates_lonlat":[(3,1)]}]
        out=assign_study_sites(sites,names,tree,tr,values)
        s=summarize(out)
        self.assertEqual(s["n_source_study_hex_author_eligible"],1)
        self.assertEqual(s["n_source_study_hex_author_unmodelled_unknown"],1)
        self.assertEqual(s["n_eligible_hex_with_zero_source_Bombus"],1)
        self.assertEqual(s["n_eligible_hex_with_positive_source_Bombus"],0)
        self.assertEqual(s["distinct_Bombus_source_modelled_richness_values"],[0])
        self.assertTrue(s["source_article_species_site_mapping_not_available"])

    def test_no_double_counting_same_study_hex(self):
        names,tree,tr,values=fixture()
        sites=[{"name":"mock a","kind":"published_single_coordinate",
                "coordinates_lonlat":[(1,1)]},
               {"name":"mock b","kind":"published_single_coordinate",
                "coordinates_lonlat":[(1.4,1.4)]}]
        s=summarize(assign_study_sites(sites,names,tree,tr,values))
        self.assertEqual(s["source_sites_tested"],2)
        self.assertEqual(s["distinct_source_grid_hex_in_site_range"],1)


if __name__=="__main__":
    unittest.main()
