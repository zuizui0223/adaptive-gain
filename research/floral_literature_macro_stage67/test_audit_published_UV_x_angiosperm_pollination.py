"""Offline provenance and original source-scoring missingness tests (not ecology)."""
import importlib.util,unittest
from pathlib import Path
from unittest.mock import patch
from io import BytesIO

HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location("p67",HERE/"audit_original_2023_pollination_vs_230_UV_literature.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def poll(name,mode="insect",scent="NA",rank="species"):
    return {"taxon_name":name,"pollination":mode,
            "syndrome_or_system":"syndrome","rank_scored_at":rank,
            "scent":scent,"nectar":"NA","pollination_data_source":"interpreted from the text",
            "ParFamTax":"Fabaceae"}

def fixtures():
    plants=[poll(f"Genus{i}_species{i}") for i in range(1201)]
    for r in plants[:41]:r["pollination"]="NA"
    plants[41]=poll("Lantana_camara","bee","NA")
    plants[42]=poll("Example_candida","insect","yes")
    u=[{"gbif_accepted_species_key":str(i+1000),
        "source_taxon_aliases":f"Others{i} plant{i}",
        "source_measured_UV_spatial_pattern_or_missing":"0",
        "source_study_DOIs":"10.1111/nph.13921"} for i in range(262)]
    u[0].update({"source_taxon_aliases":"Lantana camara",
                 "source_measured_UV_spatial_pattern_or_missing":"0"})
    u[1].update({"source_taxon_aliases":"Example candida",
                 "source_measured_UV_spatial_pattern_or_missing":"1"})
    return plants,u

class PublishedSourceUnitTests(unittest.TestCase):
    def test_true_2023_source_endpoint_and_pin(self):
        self.assertEqual(m.EXPECTED_POLLINATION_ORIGINAL,1201)
        self.assertEqual(len(m.GIT_BLOB_SHA1),40)
        self.assertTrue(m.URL.startswith("https://raw.githubusercontent.com/rubysaltbush/"))

    def test_exact_source_name_only_no_genus_imputation(self):
        plants,uv=fixtures()
        matches,rec=m.audit(plants,uv)
        self.assertEqual(rec["n_source_exact_original_binomials_across_papers"],2)
        self.assertEqual(rec["n_source_direct_UV_original_binomials_with_any_pollination_label"],2)
        self.assertTrue(rec["NO_GO_joint_uv_pollinator_species_effect_if_under30"])
        self.assertEqual(matches[0]["original_2023_scent_reported_or_UNKNOWN"],"NA")
        self.assertFalse(matches[0]["flower_photographed_in_either_source"])

    def test_no_missing_original_scent_inferred_negative(self):
        plants,uv=fixtures()
        _,rec=m.audit(plants,uv)
        self.assertEqual(rec["original_2023_scent_yes_no_unknown"]["NA"],1200)
        self.assertTrue(rec["no_nonmatching_plant_becomes_UV_or_scent_negative"])

    def test_bad_actual_source_taxon_count_refused(self):
        plants,uv=fixtures()
        with self.assertRaisesRegex(ValueError,"PUBLISHED_1201"):
            m.audit(plants[:-1],uv)

    def test_invalid_name_not_forced_into_two_word_species(self):
        self.assertEqual(m.literal_binomial("Costus_wilsonii"),"costus wilsonii")
        self.assertEqual(m.literal_binomial("Genus sp."),"")
        self.assertEqual(m.literal_binomial("Abc_def_variety"),"")
        self.assertEqual(m.literal_binomial(""),"")

if __name__=="__main__":unittest.main()
