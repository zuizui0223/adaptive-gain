"""Mock-only taxonomy mapping and infraspecific disagreement defense."""
import unittest
from map_nph2016_177_uv_gbif import attach_taxonomy

def r(code,name,state):
    return {
        "original_taxon_code":code,
        "original_S1_author_full_binomial_candidate":name,
        "source_measured_UV_pattern_present":state
    }
def m(key):
    return {"taxonomy_status":"EXACT_CONFIDENT_SPECIES_MAPPED",
            "gbif_accepted_usage_key":key,
            "gbif_matched_original_name":"Mockus first"}
class UVSourceTaxonomy(unittest.TestCase):
    def test_species_key_conflicts_never_majority_resolved(self):
        rows,receipt=attach_taxonomy([
          r("I_lycopodioides_megalopetala","Ivesia lycopodioides",1),
          r("I_lycopodioides_scandularis","Ivesia lycopodioides",0),
        ],{"Ivesia lycopodioides":m(42)})
        self.assertEqual(receipt["high_confidence_GBIF_mapped_original_UV_source_rows"],2)
        self.assertEqual(receipt["distinct_GBIF_accepted_species_keys"],1)
        self.assertEqual(len(receipt["accepted_species_key_with_conflicting_infraspecific_UV_states"]),1)
        self.assertTrue(receipt["species_trait_conflicts_never_resolved_by_majority_or_averaging"])
        self.assertEqual(rows[0]["UV_pattern_distribution_model_join"],"NOT_COMPUTED")

    def test_unmatched_source_name_never_becomes_zero(self):
        rows,receipt=attach_taxonomy([
            r("D_glandulosa","",1),
            r("P_eriocarpa","Potentilla eriocarpa",1)
        ],{"Potentilla eriocarpa":m(33)})
        self.assertEqual(rows[0]["accepted_GBIF_species_match_status"],
                         "ORIGINAL_S1_NAME_UNRESOLVED")
        self.assertEqual(rows[0]["accepted_GBIF_taxon_key_or_empty"],"")
        self.assertEqual(receipt["high_confidence_GBIF_mapped_original_UV_source_rows"],1)
        self.assertTrue(receipt["unmatched_source_taxa_not_absence"])

if __name__=="__main__":
    unittest.main()
