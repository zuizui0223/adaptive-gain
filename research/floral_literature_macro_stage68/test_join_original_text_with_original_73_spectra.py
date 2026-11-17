"""Stage68 spectrum×botanical text join guards; mock only, no remote data."""
import importlib.util
import unittest
from pathlib import Path

p = Path(__file__).with_name("join_original_text_with_original_73_spectra.py")
s = importlib.util.spec_from_file_location("stage68_join", p)
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)


class Stage68OriginalSpectraTextCrosswalkTests(unittest.TestCase):
    def test_no_fuzzy_or_congener_match_and_missing_is_not_negative(self):
        n = [
            {"taxon": "Campanula punctata", "wfo": "wfo-1",
             "flower colour": "purple, white", "petal colour": "",
             "corolla colour": "", "flower shape": "campanulate",
             "flower symmetry": "", "flower orientation": "",
             "corolla tube min. length [cm]": "3 cm",
             "corolla tube max. length [cm]": "5 cm",
             "visible_text_colour_recorded": "1",
             "structural_text_trait_recorded": "1"}
        ]
        s = [
            {"original_2024_species_name": "Campanula punctata",
             "gbif_accepted_species_key_or_unknown": "111",
             "source_UV_300_399_mean_reflectance_original_percent": "3.5",
             "source_visible_400_700_mean_reflectance_original_percent": "42",
             "prior_817_atlas_accepted_taxon_overlap": "False"},
            {"original_2024_species_name": "Campanula takesimana",
             "gbif_accepted_species_key_or_unknown": "222",
             "source_UV_300_399_mean_reflectance_original_percent": "2",
             "source_visible_400_700_mean_reflectance_original_percent": "33",
             "prior_817_atlas_accepted_taxon_overlap": "False"},
        ]
        rows, summary = m.join_text_and_spectra(n, s)
        self.assertEqual(summary["n_exact_literal_name_overlap"], 1)
        self.assertEqual(summary["n_matched_with_both_text_colour_and_structure"], 1)
        self.assertEqual(rows[0]["NHM_original_recorded_flower_colour"], "purple, white")
        self.assertEqual(rows[1]["NHM_literal_species_name_match"], "NO")
        self.assertEqual(rows[1]["NHM_any_reported_colour"], "")
        self.assertEqual(rows[1]["source_join_scope"],
                         "NO_LITERAL_SPECIES_MATCH_NOT_TRUE_NEGATIVE")
        self.assertEqual(rows[0]["NHM_text_optical_spatial_UV_guide"],
                         "NOT_MEASURED")
        self.assertFalse(summary["same_taxonomic_concept_guaranteed_by_literal_name"])

    def test_duplicate_source_labels_fail_closed(self):
        n = [{"taxon": "Campanula punctata"}, {"taxon": "Campanula punctata"}]
        with self.assertRaisesRegex(ValueError, "DUPLICATE_LITERAL"):
            m.join_text_and_spectra(n, [])

    def test_bad_artifact_sha_rejected(self):
        with self.assertRaisesRegex(ValueError, "DIGEST_CHANGED"):
            m.verify_prior_archive(b"not an original spectral ZIP")

    def test_missing_token_does_not_download(self):
        with self.assertRaisesRegex(ValueError, "TOKEN_REQUIRED"):
            m.retrieve_prior_spectral_archive("")


if __name__ == "__main__":
    unittest.main()
