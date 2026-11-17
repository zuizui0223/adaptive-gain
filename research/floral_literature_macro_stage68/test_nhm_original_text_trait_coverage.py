"""Mock-only guard tests. No remote data and no photos."""
import csv
import hashlib
import importlib.util
import io
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("nhm_original_text_trait_coverage.py")
SPEC = importlib.util.spec_from_file_location("stage68_text_traits", SCRIPT)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def raw_csv(rows):
    f = io.StringIO(newline="")
    w = csv.DictWriter(f, fieldnames=[
        "taxon", "flower colour", "petal colour", "corolla colour",
        "flower shape", "flower symmetry", "flower orientation",
        "corolla tube min. length [cm]", "corolla tube max. length [cm]",
        "pollination", "reward", "reproduction system", "source", "wfo",
    ])
    w.writeheader()
    w.writerows(rows)
    return f.getvalue().encode()


class Stage68TextTraitsTests(unittest.TestCase):
    def test_organ_colour_is_preserved_and_empty_is_unknown(self):
        records, meta = mod.extract(raw_csv([
            {"taxon": "Campanula punctata", "flower colour": "purple, white",
             "flower symmetry": "actinomorphic", "source": "TEST"},
            {"taxon": "Campanula takesimana", "petal colour": "white",
             "corolla tube min. length [cm]": "2 cm", "source": "TEST"},
            {"taxon": "Campanula islandica", "source": "TEST"},
        ]), "mock.csv")
        self.assertEqual(meta["original_text_description_taxon_rows"], 3)
        self.assertEqual(meta["visible_colour_any_of_three_organs_recorded"], 2)
        self.assertEqual(meta["structure_any_of_five_text_fields_recorded"], 2)
        self.assertEqual(meta["visible_colour_and_structure_recorded"], 2)
        self.assertEqual(records[0]["flower colour"], "purple, white")
        self.assertEqual(records[0]["corolla colour"], "")
        self.assertEqual(records[-1]["visible_text_colour_recorded"], 0)
        self.assertEqual(records[-1]["UV_spatial_guide_measurement"],
                         "UNKNOWN_NOT_MEASURED_IN_TEXT_SOURCE")
        self.assertFalse(meta["claim_global_colour_x_bee_effect"])

    def test_duplicate_taxon_labels_do_not_expand_distinct_species(self):
        _, meta = mod.extract(raw_csv([
            {"taxon": "Bellis perennis", "flower colour": "white"},
            {"taxon": "Bellis perennis", "corolla colour": "white"},
        ]), "mock.csv")
        self.assertEqual(meta["distinct_literal_taxon_labels"], 1)
        self.assertEqual(meta["duplicated_literal_taxon_labels"], 1)
        self.assertFalse(meta["stage67_species_atlas_taxonomic_overlap_calculated"])

    def test_github_blob_integrity_rejects_substitution(self):
        source = raw_csv([{"taxon": "Acanthus mollis", "flower colour": "white"}])
        exp = hashlib.sha1(f"blob {len(source)}\0".encode() + source).hexdigest()
        mod.verify_blob(source, exp)
        with self.assertRaisesRegex(ValueError, "SHA_MISMATCH"):
            mod.verify_blob(source + b"x", exp)

    def test_missing_observation_columns_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "REQUIRED_TEXT_COLUMNS_MISSING"):
            mod.extract(b"taxon,flower colour\nAcanthus mollis,white\n", "bad.csv")

    def test_unquoted_newlines_and_commas_are_parsed_as_csv_not_species(self):
        source = raw_csv([{"taxon": "Acanthus mollis",
                           "flower colour": "white,\npurple",
                           "corolla colour": "pink, red"}])
        records, meta = mod.extract(source, "mock.csv")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["flower colour"], "white,\npurple")
        self.assertEqual(meta["visible_colour_any_of_three_organs_recorded"], 1)

    def test_unknown_remote_file_is_rejected_without_network(self):
        with self.assertRaisesRegex(ValueError, "UNKNOWN_SOURCE"):
            mod.download("../cv-traits/photo.csv")


if __name__ == "__main__":
    unittest.main()
