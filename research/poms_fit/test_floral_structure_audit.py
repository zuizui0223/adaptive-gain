import unittest
import pandas as pd
from floral_structure_audit import profile_structure
from test_clock_observer_sensitivity import ClockObserverTests

class FloralAuditTests(unittest.TestCase):
    def fixture(self):
        x=ClockObserverTests().fixture(600)
        morphology={"Thistle":"Open", "Clover":"Closed", "Buttercup":"Open"}
        x["flower_structure"]=x.target_flower_corrected.map(morphology)
        x.loc[x.index[:10],"target_flower_corrected"]="Other - please describe below"
        return x
    def test_target_structure_overlap_audit(self):
        x=self.fixture()
        result=profile_structure(x,"one_km")
        self.assertEqual(result["eligible_surveys"],len(x))
        self.assertEqual(result["other_target_surveys"],10)
        self.assertEqual(result["named_target_structure_unique_fraction"],1.0)
        self.assertEqual(len(result["named_targets_with_multiple_structures"]),0)
        self.assertEqual({a["source_structure"] for a in result["normalized_structure_levels"]},{"open","closed"})
        self.assertEqual(sum(v["all_surveys"] for v in result["normalized_structure_levels"]),len(x))
        for v in result["normalized_structure_levels"]:
            self.assertTrue(v["pair_positive_surveys"]>0)
    def test_no_silent_collapse_across_different_morphology(self):
        x=self.fixture()
        x.loc[x.index[-1],"flower_structure"]="unknown"
        result=profile_structure(x,"one_km")
        self.assertIn("unknown",[r["source_structure"] for r in result["normalized_structure_levels"]])
    def test_required_morphology_field(self):
        x=self.fixture().drop(columns=["flower_structure"])
        with self.assertRaises(ValueError):profile_structure(x,"one_km")

if __name__=="__main__":unittest.main()
