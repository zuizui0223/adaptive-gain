"""Mock-only tests: original source authenticity, guild, absence semantics."""
from __future__ import annotations
import csv
import gzip
import importlib.util
import io
import unittest
from pathlib import Path

p = Path(__file__).with_name("ingest_original_corrected_EuPPollNet_network_NHM_spectra.py")
s = importlib.util.spec_from_file_location("stage69_source", p)
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)


class Stage69CorrectedNetworkTests(unittest.TestCase):
    def test_bombus_does_not_equal_all_hymenoptera(self):
        self.assertEqual(m.guild_of({"Pollinator_order": "Hymenoptera",
          "Pollinator_genus":"Bombus", "Pollinator_family":"Apidae"}), "Bombus")
        self.assertEqual(m.guild_of({"Pollinator_order":"Hymenoptera",
          "Pollinator_genus":"Apis", "Pollinator_family":"Apidae"}), "other_bee")
        self.assertEqual(m.guild_of({"Pollinator_order":"Hymenoptera",
          "Pollinator_genus":"Formica", "Pollinator_family":"Formicidae"}),
          "other_hymenoptera")
        self.assertEqual(m.guild_of({"Pollinator_order":"Diptera",
          "Pollinator_genus":"Eristalis","Pollinator_family":"Syrphidae"}),
          "diptera")
        self.assertEqual(m.guild_of({"Pollinator_order":"Lepidoptera",
          "Pollinator_genus":"Vanessa", "Pollinator_family":"Nymphalidae"}),
          "lepidoptera")
        self.assertEqual(m.guild_of({"Pollinator_order":"Passeriformes"}),
          "other_or_unknown")

    def test_uncertain_or_non_species_plants_cannot_be_misclassified(self):
        self.assertTrue(m.is_species({"Plant_rank":"SPECIES","Plant_unsure_id":"No"}))
        self.assertFalse(m.is_species({"Plant_rank":"GENUS","Plant_unsure_id":"No"}))
        self.assertFalse(m.is_species({"Plant_rank":"SPECIES","Plant_unsure_id":"Yes"}))
        self.assertFalse(m.is_species({"Plant_rank":"", "Plant_unsure_id":""}))

    def test_original_release_pinned_and_pre_correction_not_accepted(self):
        self.assertEqual(m.EXPECTED_INTERACTIONS, 623476)
        self.assertEqual(m.TAG, "v1.3.0")
        self.assertEqual(m.PIN["Interaction_data.csv.gz"][0],
                         "6e639d4af81feee76eefa6804622f8b901c39feb")
        with self.assertRaisesRegex(ValueError,"UNREGISTERED_SOURCE"):
            m.fetch_original("Interaction_data.rds")

    def test_header_is_30_original_columns_and_missing_schema_fails_closed(self):
        header=list(m.FIELDS)
        cols=header+[f"Original_{k}" for k in range(30-len(header))]
        b=io.StringIO(newline="")
        w=csv.writer(b);w.writerow(cols);w.writerow(["x"]*30)
        raw=gzip.compress(b.getvalue().encode("utf-8"))
        self.assertEqual(len(m.verify_header(raw)),30)
        self.assertEqual(len(list(m.dict_rows(raw,compressed=True))),1)
        cols.remove("Plant_accepted_name")
        b=io.StringIO(newline="")
        csv.writer(b).writerow(cols)
        with self.assertRaisesRegex(ValueError, "SCHEMA_CHANGED"):
            m.verify_header(gzip.compress(b.getvalue().encode()))

    def test_year_and_name_join_do_not_invent_site_or_synonymy(self):
        self.assertEqual(m.year_of("2017-07-08"), "2017")
        self.assertEqual(m.year_of("date unknown"), "UNKNOWN")
        self.assertEqual(m.strict_name(" Campanula punctata "), "campanula punctata")
        self.assertNotEqual(m.strict_name("Campanula punctata"),
                            m.strict_name("Campanula takesimana"))

    def test_blank_record_is_unknown_not_negative_evidence(self):
        self.assertFalse(m.is_species({"Plant_rank":"","Plant_unsure_id":""}))
        self.assertTrue(m.GUILDS[-1]=="other_or_unknown")
        self.assertFalse("bird" in m.GUILDS)
        self.assertFalse("no_pollinator" in m.GUILDS)


if __name__ == "__main__":
    unittest.main()
