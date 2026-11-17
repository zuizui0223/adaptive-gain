"""Original Kantsa same community source non-invention mock guards."""
import importlib.util,unittest
from pathlib import Path
p=Path(__file__).with_name("reconstruct_original_kantsa2018_41x168_VOC_crosswalk.py")
s=importlib.util.spec_from_file_location("s72c",p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

def plant(name,visits=2,links=1):
    return {"original_network_plant_literal":name,
        "author_original_visitor_event_count":visits,
        "author_original_nonzero_visitor_links":links,
        "Bombus_genus_literal_taxon_name_visitor_rows_without_guild_inference":0}
def scent(name):
    return {"original_figshare_VOC_plant_sheet_literal":name,
        "original_VOC_source_positive_compound_emission_rows":3,
        "original_VOC_total_emission_ng_per_g_per_hour":0.15}

class OriginalCrosswalkTests(unittest.TestCase):
    def test_strict_matching_does_not_merge_unknown_spelling(self):
        joined,receipt=m.strict_join(
          [plant("Cistus salvifolius")],[scent("Cistus salviifolius")])
        self.assertEqual(receipt["strict_original_literal_species_overlap"],0)
        self.assertEqual(receipt["network_only_original_plant_names"],["cistus salvifolius"])
        self.assertEqual(receipt["VOC_only_original_plant_names"],["cistus salviifolius"])
        self.assertEqual(joined[0]["source_strict_literal_name_VOC_match"],0)
        self.assertTrue(receipt["source_synonym_and_spelling_reconciliation_not_automated"])
    def test_same_name_case_spacing_exact(self):
        joined,s=m.strict_join([plant("  Lavandula  stoechas ")],[scent("Lavandula stoechas")])
        self.assertEqual(s["strict_original_literal_species_overlap"],1)
        self.assertEqual(joined[0]["original_2018_source_positive_VOC_compound_rows"],3)
    def test_visitor_is_genus_label_not_assumed_effective_pollination(self):
        joined,s=m.strict_join([plant("Anagallis arvensis",4,2)],[scent("Anagallis arvensis")])
        self.assertEqual(joined[0]["original_2018_visitor_event_counts"],4)
        self.assertEqual(joined[0]["original_2018_bombus_literal_genus_visitor_counts"],0)
        self.assertEqual(joined[0]["original_cross_region_independent_replication"],"NO")
    def test_source_no_plant_without_measured_scent_cannot_be_zero(self):
        joined,s=m.strict_join([plant("Tuberaria guttata")],[])
        self.assertEqual(joined[0]["original_2018_source_sum_VOC_emission_ng_g_h"],"")

if __name__=="__main__":unittest.main()
