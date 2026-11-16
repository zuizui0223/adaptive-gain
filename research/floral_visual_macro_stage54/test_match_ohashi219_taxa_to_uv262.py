"""Offline original 219 named spectral taxa are NOT age-change labels."""
import unittest
from match_ohashi219_taxa_to_uv262 import (
 parse_original_folder,validate_source_219,join
)
class Ohashi2015SpectraSourceContracts(unittest.TestCase):
    def fixture(self):
        folders=["Abelia_spathulata_var_tetrasepala",
                 "Abelia_spathulata_var_sanguinea","Potentilla_erecta"]
        folders.extend(f"Mockus_sp_{i}" for i in range(216))
        assert len(set(folders))==219
        lookups={
          "Abelia spathulata":{
             "taxonomy_status":"EXACT_CONFIDENT_SPECIES_MAPPED",
             "gbif_accepted_usage_key":100},
          "Potentilla erecta":{
             "taxonomy_status":"EXACT_CONFIDENT_SPECIES_MAPPED",
             "gbif_accepted_usage_key":200}
        }
        uv={"100":{"source_measured_UV_spatial_pattern_or_missing":"1"}}
        return folders,lookups,uv

    def test_infraspecific_origins_do_not_count_as_independent_species(self):
        name=parse_original_folder("Abelia_spathulata_var_tetrasepala")
        self.assertEqual(name["binomial"],"Abelia spathulata")
        self.assertTrue(name["source_subspecific_rank_present"])
        self.assertFalse(parse_original_folder("Vanda_sp")["binomial"])

    def test_219_directories_two_unique_accepted_taxa_and_one_UV_overlap(self):
        rows,s=join(*self.fixture())
        self.assertEqual(s["n_original_spectral_age_sampled_taxon_directories"],219)
        self.assertEqual(s["n_exact_high_confidence_GBIF_mapped_original_2015_taxon_directories"],3)
        self.assertEqual(s["n_distinct_accepted_GBIF_species_in_original_2015_spectra"],2)
        self.assertEqual(s["n_distinct_accepted_species_also_in_UV262"],1)
        self.assertEqual(rows[0]["2015_bee_perceptible_colour_change"],
                         "NOT_CLASSIFIED_FROM_SOURCE_DIRECTORY")
        self.assertTrue(s["no_false_visual_information_negative_from_unread_2015_spectra"])

    def test_source_original_219_index_digest_and_directory_count(self):
        d={
          "status":"ORIGINAL_OHASHI_2015_219_SOURCE_SPECTRAL_TAXON_ZIP_DIRECTORY",
          "n_original_spectral_species_directory_names":219,
          "original_Zenodo_deposit_md5":"md5:d98ddd3b93fb79fdbaaa5eec5818c187",
          "species_source_directory_names":self.fixture()[0]
        }
        self.assertEqual(len(validate_source_219(d)),219)
        d["n_original_spectral_species_directory_names"]=218
        with self.assertRaisesRegex(ValueError,"NO_GO_UNAUTHENTICATED_OHASHI"):
            validate_source_219(d)

if __name__=="__main__":unittest.main()
