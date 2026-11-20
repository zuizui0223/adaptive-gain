"""Stage102: source-free independent stricter flower-size phrase gates."""
import unittest,tempfile,zipfile
from pathlib import Path
from authentic_WFO_diameter_strict_quality_audit import (
    strict_source_candidate_evidence,load_frozen_stage100,
    load_geographic_frame,audit_species
)

class SourceSpecificity(unittest.TestCase):
    def test_explicit_whole_flower_20mm(self):
        v,r,_=strict_source_candidate_evidence("Flowers pale yellow, 2 cm across.")
        self.assertEqual(v,[20.0])
        self.assertEqual(r["strict_clause_candidate"],1)
    def test_direct_label_before_value(self):
        v,r,_=strict_source_candidate_evidence("Flower diameter 12 mm, leaves green.")
        self.assertEqual(v,[12.0])
    def test_corolla_tube_is_not_whole_flower(self):
        v,r,_=strict_source_candidate_evidence("Flowers having corolla tubes 2 cm across.")
        self.assertEqual(v,[])
        self.assertGreater(r["risk_ambiguous_other_organ_in_clause"],0)
    def test_inflorescence_not_flower_display(self):
        v,r,_=strict_source_candidate_evidence("Flowers borne in dense inflorescences 3 cm across.")
        self.assertEqual(v,[])
        self.assertGreater(r["risk_ambiguous_other_organ_in_clause"],0)
    def test_petals_and_sepals_not_whole_flower(self):
        v,r,_=strict_source_candidate_evidence("Flowers with petals 10 mm wide.")
        self.assertEqual(v,[])
        self.assertTrue(r["risk_ambiguous_other_organ_in_clause"])
    def test_range_rejected(self):
        v,r,_=strict_source_candidate_evidence("Flowers 3–5 mm across.")
        self.assertEqual(v,[])
    def test_WFO_double_hyphen_range_not_single_upper_endpoint(self):
        v,q,_=strict_source_candidate_evidence(
            "Flowers violet, funnelform, 8--9 cm in diam.")
        self.assertEqual(v,[])
        self.assertGreater(q["risk_unresolved_numeric_range_or_upper_limit"],0)
    def test_WFO_hyphen_dash_and_to_range_not_single_endpoint(self):
        for vtxt in ("Flowers 8-9 cm across.","Flowers 8–9 cm in diam.",
                     "Flowers 8—9 cm across.","Flowers 8 to 9 cm wide.",
                     "Flowers 8~9 cm across."):
            v,q,_=strict_source_candidate_evidence(vtxt)
            self.assertEqual(v,[],vtxt)
            self.assertGreater(q["risk_unresolved_numeric_range_or_upper_limit"],0)
    def test_to_2cm_is_maximum_not_a_point_measurement(self):
        v,q,_=strict_source_candidate_evidence("Flowers to 2 cm in diam.")
        self.assertEqual(v,[])
        self.assertGreater(q["risk_unresolved_numeric_range_or_upper_limit"],0)
    def test_not_more_than_1cm_not_exact(self):
        v,q,_=strict_source_candidate_evidence("Flowers not more than 1 cm in diam.")
        self.assertEqual(v,[])
    def test_genuine_point_single_value_preserved(self):
        v,q,_=strict_source_candidate_evidence("Flowers dark violet, 6 cm in diam.")
        self.assertEqual(v,[60.0])
    def test_other_organ_sentence_does_not_promote(self):
        v,r,_=strict_source_candidate_evidence("Leaves 20 mm wide. Flowers white.")
        self.assertEqual(v,[])
    def test_strict_never_promotes_corolla_width_only(self):
        row={"source_202606_WFO_prose_state":"candidate_corolla_width_only_NOT_whole_flower"}
        ev={"flora alba":[{"original_old":[("corolla_width_TEXT_NOT_WHOLE_FLOWER",10)],
                            "stricter":[],"risk":{},"examples":[],
                            "text_sha256":"1234"}]}
        report=audit_species(ev,{"flora alba":row})
        self.assertEqual(report[0]["stricter_grammar_status"],"NO_STRICT_CLAUSE_CONSENSUS")
    def test_original_replay_must_agree_with_prior_source_state(self):
        row={"source_202606_WFO_prose_state":"candidate_flower_diameter_from_prose"}
        ev={"flora alba":[{"original_old":[],"stricter":[],"risk":{},"examples":[],
                            "text_sha256":"1234"}]}
        with self.assertRaisesRegex(ValueError,"PARSER_REPLAY_NOT_IDENTICAL"):
            audit_species(ev,{"flora alba":row})
    def test_stage100_original_archive_requires_pinned_sha(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("test.csv","no")
            with self.assertRaisesRegex(ValueError,"LEDGER_SHA_MISMATCH"):
                load_frozen_stage100(p)
    def test_stage98B_geo_fails_closed_without_real_source(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"fake.zip"
            p.write_bytes(b"not an original audit")
            with self.assertRaisesRegex(ValueError,"GEO_72_37_SHA_MISMATCH"):
                load_geographic_frame(p)

if __name__=="__main__": unittest.main()
