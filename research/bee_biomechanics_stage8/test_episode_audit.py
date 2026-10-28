import csv
import unittest
from episode_audit import (
    EXPECTED_HEADERS,source_episode_audit,native_rows,
    VISIT_ACTIONS,NONVISIT
)

def synthetic():
    # One bee, 1 source bout, two actual flower episodes; current ID groups
    # behavior actions and is NOT a persistent spatial location.
    rows=[
        ["1","Bee A","Control","Micro-rough","1","boutStartStop","17","1","0","0"],
        ["1","Bee A","Control","Micro-rough","2","landVisit","80","1","1","0"],
        ["1","Bee A","Control","Micro-rough","2","hoverDrink","200","1","1","1"],
        ["1","Bee A","Control","Micro-rough","2","leaveFlower","40","1","1","1"],
        ["1","Bee A","Control","Micro-rough","3","horizontalLandVisit","30","1","2","1"],
        ["1","Bee A","Control","Micro-rough","3","horizontalLandDrink","50","1","2","2"],
        ["1","Bee A","Control","Micro-rough","3","leaveFlower","50","1","2","2"],
        ["1","Bee A","Control","Micro-rough","4","boutStartStop","NA","1","2","2"],
        ["2","Bee B","High Difference","Coarse-rough","9","hoverVisit","50","2","1","0"],
        ["2","Bee B","High Difference","Coarse-rough","9","hoverDrink","100","2","1","1"],
        ["3","Bee C","Low Difference","Coarse-rough","12","landVisit","150","2","1","0"],
    ]
    return [dict(zip(EXPECTED_HEADERS,r)) for r in rows]

class OriginalCambridgeEpisodeTests(unittest.TestCase):
    def test_episode_source_does_not_infer_coordinates(self):
        episodes,qa=source_episode_audit(synthetic(),source_expected=None)
        self.assertEqual(qa["original_action_rows"],11)
        self.assertEqual(qa["original_source_bee_keys"],3)
        self.assertEqual(qa["source_visit_episodes_reconstructed"],4)
        self.assertEqual(qa["source_no_valid_flower_action_episode_groups"],2)
        self.assertEqual(qa["source_flower_episodes_conflicting_orientation"],0)
        self.assertTrue(qa["Flower_ID_is_a_visit_episode_not_physical_coordinate"])
        self.assertTrue(qa["source_Time_ms_is_duration_NOT_absolute_timestamp"])
    def test_source_bout_boundary_held_without_faking_trip_sequence(self):
        rows=synthetic()
        rows.insert(8,dict(rows[4],**{"Flower ID":"4","Foraging trip":"2"}))
        eps,qa=source_episode_audit(rows,source_expected=None)
        self.assertEqual(qa["source_visit_episodes_reconstructed"],5)
        self.assertTrue(all("trip" in e for e in eps))
    def test_original_nine_action_labels_are_the_only_actions(self):
        self.assertEqual(len(set(VISIT_ACTIONS)|NONVISIT),9)
        rows=synthetic()
        rows[1]["Observation"]="fabricatedVisit"
        eps,qa=source_episode_audit(rows,source_expected=None)
        self.assertEqual(qa["n_source_bad_behavior_labels_or_assignments"],1)
    def test_source_38_bee_contract_not_silently_bypassed(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_ORIGINAL_CAMBRIDGE_SOURCE_POPULATION_CHANGED"):
            source_episode_audit(synthetic())
    def test_physical_visit_group_with_conflicting_landing_orientation_is_flagged(self):
        rows=synthetic()
        rows[2]["Observation"]="horizontalLandDrink"
        eps,qa=source_episode_audit(rows,source_expected=None)
        self.assertEqual(qa["source_flower_episodes_conflicting_orientation"],1)
        self.assertEqual([e["orientation"] for e in eps if
                          e["source_flower_group_id"]=="2"],["__AMBIGUOUS__"])
    def test_untrusted_order_not_sorted_by_duration(self):
        episodes,qa=source_episode_audit(synthetic(),source_expected=None)
        a=[e for e in episodes if e["bee"]=="Bee A"]
        self.assertLess(a[0]["source_first_row"],a[1]["source_first_row"])
        self.assertEqual(a[0]["initial_action"],"landVisit")
    def test_duration_is_exclusively_per_action_not_clock(self):
        rows=synthetic()
        rows[1]["Time (ms)"]="-1"
        eps,qa=source_episode_audit(rows,source_expected=None)
        self.assertEqual(qa["invalid_recorded_action_durations_ms"],1)

if __name__=="__main__":unittest.main()
