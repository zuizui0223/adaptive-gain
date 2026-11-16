"""Mock only strict botanical name/GBIF taxonomy gates."""
import unittest
from match_literature_visual_taxa_gbif import strict_match,combine_taxonomy

def g(name="Hibbertia cuneiformis",status="ACCEPTED"):
    return {"kingdom":"Plantae","rank":"SPECIES","matchType":"EXACT",
            "canonicalName":name,"confidence":99,"status":status,
            "usageKey":101,"acceptedUsageKey":201}

def row(name):
    return {"canonical_binomial_candidate_unreconciled":name,
            "published_taxon_string":name,
            "original_study_doi":"10.1016/j.cub.2020.08.077",
            "UV_spatial_guide_pattern_source_status":"NOT_CLASSIFIED_BY_TABLE_S1"}

class LiteratureTaxonomicSourceQA(unittest.TestCase):
    def test_exact_accepted_high_confidence_plant_only(self):
        q=strict_match("Hibbertia cuneiformis",g())
        self.assertEqual(q["taxonomy_status"],"EXACT_CONFIDENT_SPECIES_MAPPED")
        self.assertEqual(q["gbif_accepted_usage_key"],101)
        q=strict_match("Hibbertia cuneiformis",g(status="SYNONYM"))
        self.assertEqual(q["gbif_accepted_usage_key"],201)

    def test_imprecise_or_genus_only_match_never_accepted(self):
        for prop,val in [("confidence",92),("rank","GENUS"),
                         ("kingdom","Animalia"),("matchType","FUZZY"),
                         ("canonicalName","Hibbertia other")]:
            bad=g()
            bad[prop]=val
            self.assertEqual(strict_match("Hibbertia cuneiformis",bad)["taxonomy_status"],
                            "NOT_EXACT_95_CONFIDENCE_PLANT_SPECIES")

    def test_unresolved_name_not_bombus_or_plant_absence(self):
        self.assertEqual(strict_match("",{})["taxonomy_status"],
                         "UNRESOLVED_ORIGINAL_SOURCE_TAXON")

    def test_source_spatial_guide_missing_never_filled_from_gbif(self):
        original=[row("Hibbertia cuneiformis"),row("Mockus missing")]
        data={"Hibbertia cuneiformis":{
               "taxonomy_status":"EXACT_CONFIDENT_SPECIES_MAPPED",
               "gbif_accepted_usage_key":42},
              "Mockus missing":{
               "taxonomy_status":"NOT_EXACT_95_CONFIDENCE_PLANT_SPECIES"}}
        out,summary=combine_taxonomy(original,data)
        self.assertEqual(summary["n_exact_confident_species_records"],1)
        self.assertEqual(out[0]["UV_spatial_guide_pattern_source_status"],
                         "NOT_CLASSIFIED_BY_TABLE_S1")
        self.assertEqual(out[1]["gbif_accepted_species_key"],"")
        self.assertTrue(summary["no_formal_floral_visual_guide_Bombus_effect_estimated"])

if __name__=="__main__":
    unittest.main()
