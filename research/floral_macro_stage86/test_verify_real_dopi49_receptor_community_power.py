"""Source-free admission checks: no invented biological absences or survey equivalence."""
import tempfile,unittest,zipfile
from pathlib import Path
from verify_real_dopi49_receptor_community_power import (
    source_traits,record_stratum,add_site,quantify_sites,CONDITIONS
)

class Stage86AdmissionTests(unittest.TestCase):
    def test_non_author_zip_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            fn=Path(td)/"no_author.zip"
            with zipfile.ZipFile(fn,"w") as z:z.writestr("not_author","x")
            with self.assertRaises(ValueError):source_traits(fn)
    def test_no_assumed_field_method_or_survey_all(self):
        row={"methodology":"PA","plant_survey":"All",
             "pollinator_survey":"All","pollination":"1"}
        self.assertEqual(record_stratum(row),["ALL_METADATA"])
        row["methodology"]="DO"
        self.assertEqual(record_stratum(row),list(CONDITIONS))
        row["pollination"]="3"
        self.assertNotIn("DO_ALL_AND_POLLEN_GRADE_1_2",record_stratum(row))
        row["pollinator_survey"]="Group"
        self.assertEqual(record_stratum(row),list(CONDITIONS[:2]))
    def test_cue_contrast_only_with_two_source_visited_genera_and_two_bee_groups(self):
        taxa={"rosa rugosa":{"median_delta_far_green_abs":1,
                  "median_delta_near_hex_chroma":-1,
                  "median_age_colour_shift_hex":2,
                  "descriptive_far_maintained_near_reduced":1},
              "deutzia scabra":{"median_delta_far_green_abs":-1,
                  "median_delta_near_hex_chroma":1,
                  "median_age_colour_shift_hex":0.5,
                  "descriptive_far_maintained_near_reduced":0}}
        k=("10.1234/abc","Germany","2021","6","48","8","Grassland")
        sites={label:{} for label in CONDITIONS}
        vals={"methodology":"DO","plant_survey":"All","pollinator_survey":"All"}
        for label in CONDITIONS:
            add_site(sites[label],k,"rosa rugosa","BOMBUS",vals)
            add_site(sites[label],k,"deutzia scabra","OTHER_BEE",vals)
        q=quantify_sites(sites,taxa,{"rosa rugosa"},{"deutzia scabra"})
        for condition in CONDITIONS:
            one=q[condition]
            self.assertEqual(one["source_metadata_blocks_with_2_distinct_bee_visited_plants_two_genera_and_both_guilds"],1)
            self.assertEqual(one["candidate_blocks_with_any_new_21_source_age_plant"],1)
            self.assertEqual(one["prior_original_28_only_candidate_blocks_same_filter"],0)
            self.assertEqual(one["source_receptor_predeclared_contrast_opportunity"]["median_delta_far_green_abs"]["metadata_blocks_with_at_least_two_distinct_source_trait_values"],1)
    def test_single_original_taxon_must_not_be_falsely_counted_as_network(self):
        k=("10.1234/abc","Germany","2021","6","48","8","Grassland")
        v={"methodology":"DO","plant_survey":"All","pollinator_survey":"All"}
        sites={c:{} for c in CONDITIONS}
        for cond in CONDITIONS:
            add_site(sites[cond],k,"rosa rugosa","BOMBUS",v)
            add_site(sites[cond],k,"rosa rugosa","OTHER_BEE",v)
        traits={"rosa rugosa":{t:1.0 for t in (
            "median_delta_far_green_abs","median_delta_near_hex_chroma",
            "median_age_colour_shift_hex","descriptive_far_maintained_near_reduced")}}
        q=quantify_sites(sites,traits,{"rosa rugosa"},set())
        self.assertEqual(q["ALL_METADATA"]["source_prebee_metadata_blocks_with_2_or_more_measured_plants"],0)
        self.assertEqual(q["ALL_METADATA"]["source_metadata_blocks_with_2_distinct_bee_visited_plants_two_genera_and_both_guilds"],0)

if __name__=="__main__":unittest.main()
