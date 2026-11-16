"""All climate/phylogeny pairing tests use invented plant species."""
import unittest
from match_original_uv_sources_on_genus_lat_UVB_temp import match_covariates,report

def sp(key,p,lat,uvb,t,share,genus="Potentilla",eligible=True):
    return {"gbif_accepted_species_key":str(key),
            "source_UV_binary":p,
            "source_lat":lat,"source_uvb":uvb,"source_temp":t,
            "original_author_genus":genus,"eligible":eligible,
            "source_modelled_Bombus_share_proxy_N":share if eligible else None,
            "source_modelled_Bombus_taxa_N":4 if p else 3,
            "source_modelled_all_bee_taxa_N":120 if p else 160}

class OriginalSourceMatchingDesign(unittest.TestCase):
    def test_original_genus_lat_UVB_temperature_pairing_ignores_bee_outcome(self):
        source=[sp(1,1,40,2500,5,.12),sp(2,0,42,2600,6,.06),
                sp(3,1,56,3900,3,.11),sp(4,0,57,4100,4,.08),
                sp(5,0,40,2500,5,.02,"Ivesia")]
        a=match_covariates(source,5,700,4)
        self.assertEqual(len(a),2)
        self.assertEqual({x["pattern_GBIF_accepted_species_key"] for x in a},{"1","3"})
        self.assertEqual({x["uniform_GBIF_accepted_species_key"] for x in a},{"2","4"})
        self.assertEqual(round(sum(x["source_modelled_Bombus_share_proxy_N_pattern_minus_uniform"] for x in a),2),.09)
        source[0]["source_modelled_Bombus_share_proxy_N"]=-20
        b=match_covariates(source,5,700,4)
        self.assertEqual(
           [(x["pattern_GBIF_accepted_species_key"],x["uniform_GBIF_accepted_species_key"]) for x in a],
           [(x["pattern_GBIF_accepted_species_key"],x["uniform_GBIF_accepted_species_key"]) for x in b]
        )

    def test_only_matched_valid_sources_and_no_p_values(self):
        rows=[sp(1,1,40,2600,5,.1),sp(2,0,42,2600,5,.04),
              sp(3,1,48,3500,1,.2),sp(4,0,50,3550,2,.08)]
        out=report(rows)
        self.assertTrue(out["source_matching_posthoc_after_initial_descriptives"])
        self.assertEqual(out["n_eligible_source_records"],4)
        self.assertEqual(len(out["fixed_source_covariate_only_match_specs"]),2)
        self.assertEqual(out["fixed_source_covariate_only_match_specs"][0]["n_disjoint_original_genus_environment_matched_pairs"],2)
        self.assertTrue(out["no_randomized_species_trait_or_independent_native_ranges"])

    def test_matching_without_source_genus_never_assumes_phylogenetic_equivalence(self):
        rows=[sp(1,1,40,2600,5,.1,"Potentilla"),sp(2,0,40,2600,5,.02,"Ivesia")]
        self.assertEqual(match_covariates(rows,5,700,4),[])
        with self.assertRaisesRegex(ValueError,"NO_GO_INVALID_COVARIATE_TOLERANCES"):
            match_covariates(rows,0,700,4)

if __name__=="__main__":
    unittest.main()
