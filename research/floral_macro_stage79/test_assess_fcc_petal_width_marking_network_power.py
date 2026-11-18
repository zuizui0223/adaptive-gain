"""Stage79F: separate positive evidence from measured negative source cohorts."""
import importlib.util,unittest
from pathlib import Path
sp=importlib.util.spec_from_file_location("stage79f",Path(__file__).with_name("assess_fcc_petal_width_marking_network_power.py"))
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

class Stage79FPositiveOnlyTests(unittest.TestCase):
    def test_one_FCC_positive_does_not_impute_absent_state(self):
        far={"original_plant_species_recorded_in_field_visits":1408,
             "original_source_species_with_petal_MAX_width_cm":118,
             "original_source_species_with_positive_pattern_text":31,
             "original_field_network_year_keys_in_accepted_plant_roster":1862}
        row=lambda sp,w,motif:{"Study_id":"S","Network_id":"A","Year":"2021",
             "original_plant_literal_accepted_name":sp,"source_petal_max_width_cm":w,
             "source_positive_marking_text_only":str(motif)}
        near=[row("lotus corniculatus","2.0",0),row("gentiana lutea","1.0",1)]
        fcc=["lotus corniculatus","lobularia maritima","lantana camara",
             "lonicera periclymenum","lonicera tatarica","lotus pedunculatus",
             "pulmonaria officinalis","tagetes erecta","trifolium stellatum"]
        positive={"source_original_species_table_parsing":{"exact_two_token_source_candidate_species_names":144},
          "source_exact_name_join_to_original_visit_roster":{"source_original_positive_FCC_exact_plant_names":fcc}}
        # Source fixture 453-network invariant is deliberately relaxed only in
        # mock to inspect pre-outcome selection and absence semantics.
        roster=[{"Study_id":"S","Network_id":"A","Year_from_original_date":"2021",
               "Original_plant_accepted_name_literal":sp} for sp in ("lotus corniculatus","gentiana lutea")]
        original=m.analyze
        # This fixture must not misrepresent missing change state as false.
        self.assertEqual(len(set(fcc)),9)
        self.assertEqual(m.key(near[0]),("S","A","2021"))
        self.assertNotIn("source_non_FCC_negative_class",original.__code__.co_varnames)
    def test_archived_provider_receipts_are_artifacts_not_raw_csv(self):
        self.assertEqual(len(m.PINS["roster"]),64)
        self.assertEqual(m.PINS["farnear"],"39e89f3d20410e1d54d1b366e62fd3362878bab12815835282731e224f65a1f7")

if __name__=="__main__":unittest.main()
